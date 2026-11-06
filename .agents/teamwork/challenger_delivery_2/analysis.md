# Adversarial Stress Testing Analysis Report

**Agent**: `challenger_delivery_2`  
**Archetype**: EMPIRICAL CHALLENGER (critic, specialist)  
**Date**: 2026-11-05T00:05:00Z  
**Verdict**: **REQUEST_CHANGES**  

---

## Executive Summary

As the empirical challenger, we conducted comprehensive stress tests against the email delivery subsystem implemented by `worker_delivery_1`. We focused on three mandatory challenge vectors:
1. Multi-threaded concurrency, thread-safety, and lock contention in `EmailPacer`.
2. Synthetic domain interception under RFC 2606 (`DUMMY_EMAIL_DOMAINS`), specifically evaluating `test@example.com` and `candidate@test.invalid`.
3. RFC 8058 One-Click unsubscribe POST and CSRF exemption handling.

All tests were executed locally using mock transports, zero live sockets, and strict cooldown adherence.

### Test Results Matrix

| Test Suite | Objective | Status | Empirical Observation |
|---|---|---|---|
| **Suite 1: EmailPacer Concurrency** | Verify thread safety & inter-message delay under concurrent bursts | **FAIL** | 4 out of 5 threads woke up at the exact same millisecond (`0.0000s` interval); 8 of 9 intervals failed in 10-thread test. |
| **Suite 2: Synthetic Interception** | Intercept `test@example.com` and `candidate@test.invalid` without network dispatch | **FAIL** | `candidate@test.invalid`, `candidate@sub.example.com`, and `user@domain.invalid` leaked to SMTP dispatch. |
| **Suite 3: RFC 8058 & CSRF** | Verify HTTP 200 on valid POST without CSRF token; verify HMAC validation | **PASS** | Valid POST unsubscribes candidate; tampered HMAC rejects mutation; CSRF is active elsewhere (403 on `/login`). |

---

## Detailed Empirical Findings

### 1. [CRITICAL/HIGH] `EmailPacer` Thread-Safety & Concurrency Burst Failure

- **File**: `apps/portal/services/delivery_service.py:87-108`
- **Root Cause**:
  `EmailPacer.calculate_delay()` calculates sleep delay *outside* of `self._lock`. Furthermore, `self._last_dispatch_ts` is only recorded *after* `time.sleep(delay)` finishes.
  When $N$ threads execute `wait_and_record()` concurrently (e.g., during web traffic bursts or batch dispatch):
  1. Thread 1 calculates delay $0$, enters lock, updates `_last_dispatch_ts = T_0`.
  2. Threads 2 through $N$ all read `_last_dispatch_ts = T_0` and calculate identical delays of `min_interval`.
  3. All threads 2 through $N$ sleep concurrently in parallel for `min_interval`.
  4. At $T_0 + \text{min\_interval}$, all sleeping threads awaken simultaneously. They acquire the lock one after another in rapid succession ($< 0.1\text{ms}$) and dispatch emails concurrently.
- **Empirical Evidence**:
  Executed `test_stress_harness.py` with 5 threads and target interval $0.100\text{s}$:
  ```text
  Dispatched 5 threads simultaneously (target interval: 0.1s):
    Thread 4: start=1793836982.4277, done=1793836982.4277, elapsed=0.0000s, delay=0.0000s
    Thread 2: start=1793836982.4277, done=1793836982.5288, elapsed=0.1012s, delay=0.1000s
    Thread 3: start=1793836982.4277, done=1793836982.5288, elapsed=0.1012s, delay=0.1000s
    Thread 0: start=1793836982.4277, done=1793836982.5288, elapsed=0.1012s, delay=0.1000s
    Thread 1: start=1793836982.4277, done=1793836982.5288, elapsed=0.1012s, delay=0.1000s

  Consecutive intervals between finishes: [0.1012, 0.0, 0.0, 0.0]
  Minimum observed interval: 0.0000s (required: >= 0.0800s)
  Rate pacing violations: 3 / 4
  ```
  In a 10-thread test, 8 out of 9 consecutive intervals were `0.0000s`!
- **Blast Radius**:
  If multiple requests or jobs trigger emails simultaneously, Google Workspace SMTP will receive a burst of concurrent connections rather than evenly spaced messages, triggering Google velocity throttling and temporary account suspension.
- **Recommended Mitigation**:
  Adopt an atomic reservation model under `self._lock` where each caller reserves a future time slot:
  ```python
  def wait_and_record(self, recipient: str, interval: Optional[float] = None, dry_run: bool = False) -> float:
      min_interval = interval if interval is not None else self.default_interval
      rcpt_key = (recipient or "").strip().lower()
      with self._lock:
          now = time.time()
          target_ts = max(now, self._last_dispatch_ts + min_interval)
          target_ts = max(target_ts, self._recipient_dispatch_ts.get(rcpt_key, 0.0) + min_interval)
          delay = max(0.0, target_ts - now)
          if not dry_run:
              self._last_dispatch_ts = target_ts
              self._recipient_dispatch_ts[rcpt_key] = target_ts
      if delay > 0 and not dry_run:
          time.sleep(delay)
      return delay
  ```
  Empirically tested: Under this reservation model, 100% of concurrent threads are spaced at exactly `0.1001s` intervals with zero violations.

---

### 2. [HIGH] Synthetic Domain Interception Leaks RFC 2606 Domains (`candidate@test.invalid`)

- **File**: `apps/portal/services/delivery_service.py:42-46, 293-300` and `apps/portal/app.py:4080-4084`
- **Root Cause**:
  `DUMMY_EMAIL_DOMAINS` specifies `"@invalid"` rather than `".invalid"`, and does not include wildcard subdomain matching for `example.com` or `example.org`.
  In `is_dummy_domain(email)`:
  ```python
  for dummy in DUMMY_EMAIL_DOMAINS:
      if clean.endswith(dummy) or dummy in clean:
          return True
  ```
  When tested with `candidate@test.invalid` (mandated by task dispatch):
  - The domain is `test.invalid`.
  - `clean.endswith("@invalid")` evaluates to `False` (character before `invalid` is `.`, not `@`).
  - `"@invalid" in clean` evaluates to `False`.
  - `.test` is not matched because `.test` is not in `candidate@test.invalid` (it is `@test.invalid`).
  - Consequently, `is_dummy_domain("candidate@test.invalid")` returns `False`!
- **Empirical Evidence**:
  Executed `test_stress_harness.py`:
  ```text
  [PASS] test@example.com          -> is_dummy: True  | Network attempted: False
  [FAIL] candidate@test.invalid    -> is_dummy: False | Network attempted: True
  [FAIL] candidate@sub.example.com -> is_dummy: False | Network attempted: True
  [FAIL] user@domain.invalid       -> is_dummy: False | Network attempted: True
  ```
  `send_email("candidate@test.invalid", ...)` invoked `_dispatch_primary_smtp()` and triggered `mock_ssl.SMTP_SSL()`. In live mode, this would dispatch an actual network SMTP request to Google and result in a hard bounce.
- **Blast Radius**:
  Automated tests and QA runs using RFC 2606 `.invalid` or test subdomains will bypass the guard, trigger external SMTP calls, and pollute Google Workspace sender reputation.
- **Recommended Mitigation**:
  Update `DUMMY_EMAIL_DOMAINS` in both `apps/portal/services/delivery_service.py` and `apps/portal/app.py`:
  ```python
  DUMMY_EMAIL_DOMAINS = (
      "@example.com", "@example.org", "@example.net",
      ".example.com", ".example.org", ".example.net", ".example",
      ".test", "@test.com", ".invalid", "@invalid", "@localhost", ".localhost",
      "@dbert.test", ".dbert.test", "@sample.com", "@demo.com",
      "@mailinator.com", "@fakemail.com"
  )
  ```

---

### 3. [PASS/CONFIRMED] RFC 8058 One-Click POST & CSRF Handling

- **File**: `apps/portal/app.py:3703, 4952-4981`
- **Empirical Evidence**:
  - `POST /unsubscribe?e=...&t=VALID` without CSRF token returned `HTTP 200` and updated `intern_accounts.newsletter_opt_in = 0`.
  - `POST /unsubscribe?e=...&t=INVALID` with tampered token returned `HTTP 200` and left `intern_accounts.newsletter_opt_in = 1` intact.
  - `POST /login` without CSRF token returned `HTTP 403` (`csrf_reject`), confirming CSRF enforcement remains active across the rest of the application.
  - `GET /unsubscribe` with valid token returned `HTTP 200` with the unsubscribe confirmation page.
  - `GET /unsubscribe` with invalid token returned `HTTP 200` with "This unsubscribe link is invalid or expired."
- **Assessment**:
  The implementation meets RFC 8058 requirements. Mail User Agents can successfully trigger automated unsubscribes via POST without CSRF friction, while state mutations remain cryptographically protected by HMAC tokens.

---

## Verdict & Recommendation

**Verdict**: **REQUEST_CHANGES**

The worker must apply the two required fixes:
1. Correct `EmailPacer.wait_and_record()` to use slot reservation under `self._lock` so concurrent callers are properly spaced out across time rather than releasing simultaneously.
2. Update `DUMMY_EMAIL_DOMAINS` in `services/delivery_service.py` and `app.py` to include `.invalid`, `.example`, and subdomain patterns so that `candidate@test.invalid` and related RFC 2606 domains are intercepted at zero network cost.
