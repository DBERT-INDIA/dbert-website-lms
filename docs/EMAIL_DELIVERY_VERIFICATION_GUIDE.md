# DBERT Email Deliverability & Post-Cooldown Verification Guide

**Target Recipients**: `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`  
**Sender Identity**: `DBERT Support <abhinav.sharma@dbert.in>`  
**Domain**: `dbert.in` (MSME Registered, Government of India)  

---

## 1. Executive Summary & Root Cause Diagnostic

An exhaustive, multi-agent investigation across historical database records, DNS configurations, codebase paths, and transmission logs identified 7 root causes that contributed to message non-delivery and spam filtering during prior testing:

1. **Tri-Factor Authentication Deficiency (Absence of DMARC)**:
   - Under Google’s 2024 Bulk and General Sender requirements, messages originating from custom domains sending to `@gmail.com` must have SPF, DKIM, and DMARC aligned.
   - *Status*: **Resolved**. Global DNS TXT record `_dmarc.dbert.in` is published with `"v=DMARC1; p=none; sp=none; rua=mailto:abhinav.sharma@dbert.in"`. Tri-factor authentication is 100% active.
2. **Suspended Domain References (`dbert.info`) in Email Footers**:
   - Mail body templates contained links and mailto anchors to `careers@dbert.info`. Registry suspension of `dbert.info` caused spam filters (SpamAssassin and Google Cloudmark) to flag emails with high confidence.
   - *Status*: **Resolved**. All footers, error pages, and templates now point strictly to `support@dbert.in` and `https://lms.dbert.in`.
3. **Velocity Throttling & Inbound Per-Recipient Rate Limiting**:
   - Sending bursts of 16+ programmatic emails within 35 minutes triggered Gmail’s per-recipient inbound rate limiting on `ain.sharma.abhinav@gmail.com`.
   - *Status*: **Resolved**. Rate pacing is now implemented with an automated 15-second inter-message delay.
4. **Hard Bounce Reputation Hit**:
   - Automated scripts dispatched test emails to `candidate_delta@example.com`, producing RFC 7505 hard bounces (`550 5.1.2 Domain not found`) that degraded domain reputation.
   - *Status*: **Resolved**. Production pre-flight guard `DUMMY_EMAIL_DOMAINS` intercepts synthetic domains locally at zero network cost.
5. **RFC 8058 One-Click Unsubscribe Endpoint Returning HTTP 405 / CSRF 403**:
   - Google and Yahoo require `List-Unsubscribe-Post: List-Unsubscribe=One-Click` to support HTTP POST requests. Previously, the `/unsubscribe` route only accepted GET and was subject to session CSRF checks.
   - *Status*: **Resolved**. `@app.route("/unsubscribe", methods=["GET", "POST"])` is CSRF-exempted and authenticated via HMAC token, returning `HTTP 200 OK` on POST.
6. **Aggressive Content Triggers in Transactional Templates**:
   - Injected 1x1 tracking pixel (`/e/o.gif`) and marketing UTM queries on transactional messages (passwords, OTPs, verification emails).
   - *Status*: **Resolved**. Tracking pixel and UTM parameters have been stripped from transactional email dispatches.
7. **Credential Drift & Silent Error Handling**:
   - `.env` contained stale credentials (`ckxnpudkapzgzbxl`) while working scripts used the active app password (`rsupmvvvvwrsuxuh`). Failed email dispatches also swallowed exceptions in daemon threads without persisting error details.
   - *Status*: **Resolved**. `.env` updated with active credentials, and `email_log` now captures `provider`, `message_id`, and `error_message`.

---

## 2. Why the Cooldown Period & Pacing Are Essential

### The Cooldown Period
Google Workspace outbound SMTP relays and Gmail inbound spam filters employ **sliding-window velocity counters** (typically 1 to 4 hours). Rapid bursts of automated test messages trigger temporary throttling and heuristic spam quarantine. The multi-hour cooldown window allows these rolling counters to reset naturally to clean baseline levels.

### Rate Pacing
Never burst-send emails in rapid succession (<5 seconds apart) from newly configured credentials or to the same recipient address. The delivery service and verification runner enforce a **15-second pacing delay** between individual recipient dispatches.

---

## 3. Post-Cooldown Verification Runner

We have provided an automated standalone verification runner at:
`scripts/verify_delivery_post_cooldown.py`

### Step 3.1: Execute Dry-Run First (Safe Mode)
Always run dry-run validation first. This validates DNS records, SPF/DKIM/DMARC resolution, SMTP credential loading, recipient address validation, and RFC 5322 MIME construction with **zero live network calls**:

```powershell
python scripts/verify_delivery_post_cooldown.py
```
*(or explicitly with `--dry-run`)*:
```powershell
python scripts/verify_delivery_post_cooldown.py --dry-run
```

**Expected Dry-Run Output**:
- `[PASS] SPF Record on dbert.in: v=spf1 include:_spf.google.com ...`
- `[PASS] DKIM Record on google._domainkey.dbert.in: v=DKIM1 ...`
- `[PASS] DMARC Record on _dmarc.dbert.in: v=DMARC1; p=none ...`
- `[PASS] Recipient Address Validation: ain.sharma.abhinav@gmail.com`
- `[PASS] RFC 5322 MIME & Header Synthesis: Message-ID: <uuid@dbert.in>`
- `[DRY-RUN] Dry-Run Delivery Verification: Sockets opened: 0`
- `[PASS] Recipient Address Validation: ajnatechrpa@gmail.com`
- `Summary: 2 VALIDATED, 0 FAILED`

---

### Step 3.2: Execute Live Verification (Post-Cooldown)
Once the cooldown window has concluded, trigger the live verification runner using the explicit `--live` flag:

```powershell
python scripts/verify_delivery_post_cooldown.py --live --delay 15
```

**What the Runner Performs During Live Mode**:
1. Connects securely to `smtp.gmail.com:465` over SSL (`TLSv1.3`).
2. Authenticates using `abhinav.sharma@dbert.in` and app password `rsupmvvvvwrsuxuh`.
3. Dispatches message #1 to `ain.sharma.abhinav@gmail.com`.
4. Enforces a 15-second countdown pacing delay to prevent velocity throttling.
5. Dispatches message #2 to `ajnatechrpa@gmail.com`.
6. Prints a summary table of delivered message IDs and SMTP response codes (`250 2.0.0 OK`).

---

## 4. How to Inspect Headers in Gmail ("Show Original")

After running the live test, verify that the email achieved direct inbox delivery and passed all authentication gates:

1. Open Gmail at [mail.google.com](https://mail.google.com).
2. Open the verification email in both `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.
3. Click the **three vertical dots** (More actions) next to the Reply button in the top right of the message pane.
4. Click **Show original** (`Original Message`).
5. Inspect the summary table at the top of the Original Message page:

| Authentication Check | Expected Result | Interpretation |
|----------------------|-----------------|----------------|
| **SPF** | `PASS with IP ...` | Google Workspace SMTP authorized for `dbert.in` |
| **DKIM** | `'PASS' with domain dbert.in` | Cryptographic signature intact and validated |
| **DMARC** | `'PASS'` | Domain alignment complete; DMARC policy satisfied |

6. Verify headers:
   - `From: DBERT Support <abhinav.sharma@dbert.in>`
   - `Reply-To: support@dbert.in`
   - `Return-Path: <abhinav.sharma@dbert.in>`
   - `Message-ID: <...-uuid...@dbert.in>`
   - `List-Unsubscribe: <https://lms.dbert.in/unsubscribe?...>, <mailto:support@dbert.in?subject=unsubscribe>`
   - `List-Unsubscribe-Post: List-Unsubscribe=One-Click`

---

## 5. Troubleshooting Common Issues

### Issue 1: "SMTPAuthenticationError (535, b'Bad credentials')"
- **Cause**: Google App Password was regenerated or rotated.
- **Fix**: Open Google Account Security -> App Passwords -> Create a new App Password for "DBERT Mailer" -> Update `SMTP_PASS` in `apps/portal/.env`.

### Issue 2: "Message routed to Spam folder"
- **Check 1**: Did you include dead domain links (`dbert.info`)? Verify the body contains only `dbert.in` and `lms.dbert.in`.
- **Check 2**: Did you send without pacing (<5s between sends)? Wait 30 minutes and re-run with `--delay 15`.
- **Check 3**: Did you click "Report not spam" in Gmail? This trains Google's user-specific filter.

### Issue 3: "RFC 8058 One-Click Unsubscribe 405 or 403"
- **Cause**: Route missing POST handler or blocked by CSRF.
- **Fix**: Verified in `apps/portal/app.py`: `/unsubscribe` is registered with `methods=["GET", "POST"]` and included in `CSRF_EXEMPT_ENDPOINTS`.

---

## 6. Architecture & Code Layout

- **Delivery Service**: `apps/portal/services/delivery_service.py`
  - Multi-provider engine (Google Workspace SMTP primary + cPanel API fallback)
  - Pre-flight hard bounce prevention guard (`DUMMY_EMAIL_DOMAINS`)
  - Deliverability header synthesis (`Message-ID`, `Return-Path`, `Reply-To`, RFC 8058)
  - `EmailPacer` inter-message velocity limiter
- **Portal Integration**: `apps/portal/app.py`
  - `send_email_async` delegates to delivery service and persists rich diagnostics to `email_log`
  - `/unsubscribe` route handles RFC 8058 POST
- **Verification Runner**: `scripts/verify_delivery_post_cooldown.py`
  - Standalone verification script for dry-run validation and post-cooldown live delivery
- **Automated Test Suite**: `apps/portal/tests/test_delivery_service.py`
  - 100% mock/dry-run safe; zero live network sockets during tests
