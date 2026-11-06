# DISPATCH for worker_remediation_1

## Task
Remediate Delivery Service Vulnerabilities & Edge Cases Identified by Adversarial Challengers.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## STRICT CONSTRAINT: COOLDOWN ENFORCEMENT
UNDER NO CIRCUMSTANCES SEND LIVE OUTBOUND EMAILS. All test execution must be in dry-run/mock mode with zero live network dispatch.

## Objectives & Remediation Items

1. **EmailPacer Atomic Reservation Model (`apps/portal/services/delivery_service.py`)**:
   Fix the concurrency race condition where threads awaken simultaneously and dispatch at `0.0000s` interval.
   In `EmailPacer.wait_and_record()`, reserve the future time-slot atomically inside `self._lock`:
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

2. **DUMMY_EMAIL_DOMAINS Interception (`apps/portal/services/delivery_service.py` & `apps/portal/app.py`)**:
   Add `.invalid`, `.example.com`, `.example.org`, `.example.net`, `.example`, `.test`, and ensure `is_dummy_domain(email)` catches `.invalid`, `test.invalid`, subdomains of `example.com`, etc., so `candidate@test.invalid` and `user@sub.example.com` are intercepted at zero network cost:
   ```python
   DUMMY_EMAIL_DOMAINS = (
       "@example.com", "@example.org", "@example.net",
       ".example.com", ".example.org", ".example.net", ".example",
       ".test", "@test.com", ".invalid", "@invalid", "@localhost", ".localhost",
       "@dbert.test", ".dbert.test", "@sample.com", "@demo.com",
       "@mailinator.com", "@fakemail.com"
   )
   ```

3. **RFC 2047 / RFC 5322 From Header Encoding (`apps/portal/services/delivery_service.py`)**:
   In `build_mime_message()`, do not use `msg["From"] = f"{from_name} <{from_email}>"`.
   Use `email.utils.formataddr` to guarantee that only `from_name` is encoded into an RFC 2047 word while `<from_email>` remains unencoded ASCII angle brackets, maintaining strict DMARC alignment:
   ```python
   from email.utils import formataddr
   msg["From"] = formataddr((from_name, from_email))
   ```

4. **Recipient Type Safety, CRLF Rejection, & RFC 5322 Syntax Regex (`apps/portal/services/delivery_service.py`)**:
   In `send_email()`, replace the weak `"@" not in clean_to` guard with:
   - Type check: ensure `to` is a string (avoid `AttributeError` on int/list).
   - Control character check: reject any `\r`, `\n`, or `\x00` in `to`.
   - Syntax validation: enforce `EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$")`. Return `DeliveryResult(success=False, provider="hard_bounce_guard", message_id="", error=..., diagnostics=diagnostics)`.

5. **Subject Header CRLF Sanitization (`apps/portal/services/delivery_service.py`)**:
   In `build_mime_message()`, sanitize subject:
   ```python
   clean_subject = re.sub(r"[\r\n]+", " ", str(subject or "")).strip()
   msg["Subject"] = clean_subject
   ```

6. **Empirical Verification**:
   Run both challenger test harnesses and existing suites to verify 100% pass:
   - `python .agents/teamwork/challenger_delivery_2/test_stress_harness.py` (all 3 suites must pass)
   - `python .agents/teamwork/challenger_delivery_1/adversarial_delivery_stress.py` (all 59 tests must pass)
   - `pytest apps/portal/tests/test_delivery_service.py`
   - `python scripts/verify_delivery_post_cooldown.py`

## Output Requirements
- Write your completion handoff report to `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\worker_remediation_1\handoff.md`.
- Notify the orchestrator when complete.


## 2026-11-05T00:06:21Z
You are worker_remediation_1, a worker subagent.
Your working directory is: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\worker_remediation_1
Read your task instructions at: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\worker_remediation_1\DISPATCH.md
Read the original request at: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\ORIGINAL_REQUEST.md
Read the findings in:
- c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\challenger_delivery_2\handoff.md
- c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\challenger_delivery_1\handoff.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

CRITICAL CONSTRAINT: COOLDOWN ENFORCEMENT
UNDER NO CIRCUMSTANCES SEND LIVE OUTBOUND EMAILS. All test execution must be in dry-run/mock mode with zero live network dispatch.

Implement the concrete remediations in apps/portal/services/delivery_service.py and apps/portal/app.py:
1. EmailPacer atomic slot reservation under lock.
2. DUMMY_EMAIL_DOMAINS interception (.invalid, .example, subdomains).
3. formataddr for RFC 2047 From header encoding.
4. Recipient type safety, CRLF rejection, and RFC 5322 regex validation.
5. Subject header CRLF sanitization.
Run both challenger test harnesses and existing test suites to verify 100% pass:
- python .agents/teamwork/challenger_delivery_2/test_stress_harness.py
- python .agents/teamwork/challenger_delivery_1/adversarial_delivery_stress.py
- pytest apps/portal/tests/test_delivery_service.py
- python scripts/verify_delivery_post_cooldown.py
Write your completion handoff report to c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\worker_remediation_1\handoff.md.
When finished, notify the orchestrator (conversation ID: 1954b148-861e-46e3-9273-69539bb3dcb5).
