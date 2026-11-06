# Root Cause Analysis: DBERT Email Deliverability & Transmission Failures

**Date**: 2026-11-04 (Local: 2026-11-05)  
**Authors**: Orchestration Team (explorer_survey_1, explorer_survey_2, explorer_survey_3, orchestrator_3)  
**Target Recipient Inboxes**: `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`  
**Sender Identity**: `abhinav.sharma@dbert.in` via Google Workspace SMTP (`smtp.gmail.com:465`)  

---

## Executive Summary

An exhaustive, multi-agent forensic investigation was conducted across the codebase (`apps/portal`), live DNS infrastructure, 6,805 historical database transmission records (`apps/portal/internship.db`), dispatch logs (`logs/email_dispatch_log.csv`), and execution transcripts.

**The primary findings confirm:**
1. **Zero SMTP connection or authentication failures occurred.** Every recent connection to `smtp.gmail.com:465` authenticated cleanly and returned `250 2.0.0 OK`.
2. **Deliverability is fundamentally achievable.** Test emails with clean domain text (`test_zero_links.py` and `test_link_formats.py` Test 5B) arrived directly in `ain.sharma.abhinav@gmail.com`'s Primary Inbox. Furthermore, `send_guaranteed_test.py` at 04:26 AM delivered directly to `ajnatechrpa@gmail.com`'s Primary Inbox.
3. **Downstream non-delivery and spam filtering were caused by 7 intersecting root causes**:
   - Missing DMARC record on `dbert.in` during initial tests (Google 2024 Bulk Sender non-compliance).
   - Inactive/suspended domain references (`mailto:careers@dbert.info`) embedded in CAN-SPAM email footers.
   - Asymmetric per-recipient rate limiting on `ain.sharma.abhinav@gmail.com` after >15 rapid test bursts within 35 minutes.
   - Sender reputation hit from RFC 7505 hard bounces (`candidate_delta@example.com`).
   - RFC 8058 One-Click Unsubscribe returning `HTTP 405 Method Not Allowed` on POST requests.
   - Aggressive content triggers (1x1 open-tracking pixel and UTM parameters) on transactional emails.
   - Silent error handling and credential drift (`ckxnpudkapzgzbxl` in `.env` vs `rsupmvvvvwrsuxuh` in scripts).

---

## Detailed Root Cause Diagnostics

### 1. Tri-Factor Authentication Deficiency (Historical DMARC Absence)
- **Mechanism**: Under Google's February 2024 Bulk and General Sender requirements, messages originating from custom domains sending to `@gmail.com` MUST authenticate with SPF, DKIM, and DMARC.
- **Evidence**: Initial DNS queries showed `dbert.in` had SPF (`v=spf1 include:_spf.google.com include:zoho.in ~all`) and DKIM (`google._domainkey.dbert.in`), but `_dmarc.dbert.in` returned `NXDOMAIN`.
- **Impact**: Without DMARC, Google Mail Security treats automated messages—especially those containing URLs—as unverified and susceptible to spoofing, steering them into Spam or silently dropping them.
- **Current Status**: **RESOLVED**. TXT record `_dmarc.dbert.in` has been published: `"v=DMARC1; p=none; sp=none; rua=mailto:abhinav.sharma@dbert.in"`. Tri-factor alignment is now active globally.

### 2. Embedded Suspended Domain (`dbert.info`) in Email Footers
- **Mechanism**: Receiving mail servers evaluate all domains and URLs found in message HTML and MIME bodies.
- **Evidence**:
  - `apps/portal/app.py:3953`: `... please contact <a href='mailto:careers@dbert.info'>careers@dbert.info</a>`
  - `apps/portal/app.py:3962`: `... <a href='mailto:careers@dbert.info'>Support</a>`
  - `apps/portal/.env:35-38`: `SMTP_BACKUP_HOST=dbert.info`, `SMTP_BACKUP_USER=contactus@dbert.info`
  - DNS Query: `Resolve-DnsName dbert.info` returns `PrimaryServer: ns1.verification-hold.suspended-domain.com`.
- **Impact**: Including links or mailto targets pointing to a registry-suspended domain triggers high-confidence spam classification across SpamAssassin and Google Cloudmark spam heuristics.

### 3. Velocity Throttling & Inbound Per-Recipient Rate Limiting
- **Mechanism**: Google Workspace enforces strict velocity limits on newly created App Passwords, and Gmail inbound gateways enforce per-recipient throttling to protect user inboxes from spam floods.
- **Evidence**:
  - At 04:26 AM, `send_guaranteed_test.py` sent identical emails to both addresses.
  - `ajnatechrpa@gmail.com` received the email in its Primary Inbox immediately.
  - `ain.sharma.abhinav@gmail.com` did not receive it. Prior to 04:26 AM, `ain` had received 16+ programmatic test emails within 35 minutes.
  - Subsequent bursts sent without inter-message pacing (<5 seconds apart) caused Google's outbound SMTP relay to temporarily defer or silently quarantine messages.
- **Remediation**: The current multi-hour cooldown window allows Google's inbound/outbound sliding-window rate counters to reset. All future dispatch must enforce pacing (10–15 seconds between dispatches).

### 4. Hard Bounce Reputation Penalty from Dummy Test Addresses
- **Mechanism**: Google Workspace tracks the percentage of hard bounces (Null MX / invalid mailbox). Senders exceeding a 0.3% spam/bounce rate suffer automated delivery degradation.
- **Evidence**: At 04:23 AM, test submissions dispatched an automated confirmation to `candidate_delta@example.com`, generating a `mailer-daemon@googlemail.com` hard bounce: `Your message wasn't delivered to candidate_delta@example.com because the domain example.com couldn't be found`.
- **Remediation**: Hard bounce prevention guard `DUMMY_EMAIL_DOMAINS` was deployed in `apps/portal/app.py:4067`, intercepting synthetic/test domains locally at zero network cost.

### 5. RFC 8058 One-Click Unsubscribe Endpoint Returning HTTP 405
- **Mechanism**: Google and Yahoo require commercial and notification emails containing `List-Unsubscribe-Post: List-Unsubscribe=One-Click` to support HTTP POST requests without user interaction.
- **Evidence**:
  - `apps/portal/app.py:3984`: Injects `List-Unsubscribe-Post: List-Unsubscribe=One-Click`.
  - `apps/portal/app.py:4914`: `@app.route("/unsubscribe")` omitted `methods=["GET", "POST"]`, defaulting strictly to `GET`.
- **Impact**: Automated sender compliance scanners test this endpoint by issuing a POST request. Receiving a `405 Method Not Allowed` marks the sender as non-compliant with 2024 Bulk Sender rules.

### 6. Aggressive Content Triggers in Transactional Templates
- **Mechanism**: Clean, transactional emails (OTPs, password resets) should avoid marketing signals.
- **Evidence**:
  - `apps/portal/app.py:3972`: Injects 1x1 tracking pixel `<img src='.../e/o.gif'>` into every email.
  - `apps/portal/app.py:3918`: Appends UTM parameters (`?utm_source=email&utm_medium=...`) to all links.
- **Impact**: Inclusion of tracking pixels and marketing redirects in security-sensitive transactional emails trips heuristic spam rules.

### 7. Silent Failure Architecture & Credential Drift
- **Mechanism**: Fire-and-forget daemon threading in `send_email_async` catches all exceptions, does not record traceback details in `email_log`, and causes endpoints (`/forgot-password`, `/auth/send-otp`) to unconditionally return `200 OK` to users.
- **Evidence**:
  - `apps/portal/.env:30` contained `SMTP_PASS=ckxnpudkapzgzbxl`.
  - The working App Password generated by the user is `rsupmvvvvwrsuxuh`.
  - `deploy/run_cron_tasks.sh` targeted port 8000 with `X-Cron-Secret`, while `apps/portal` ran on port 5001 with `X-Cron-Key`, leaving outbox queues stuck in `STATUS_PENDING`.

---

## Architectural Remedy Roadmap

| # | Remediation Component | Action Plan |
|---|-----------------------|-------------|
| 1 | **Sanitize Domain References** | Purge all `dbert.info` and `dbert.online` references from `app.py` footers, templates, and `.env`. Replace with `support@dbert.in`. |
| 2 | **Fix RFC 8058 Unsubscribe** | Update `/unsubscribe` route to `methods=["GET", "POST"]` and return HTTP 200 on POST requests. |
| 3 | **Harmonize SMTP Credentials** | Update `apps/portal/.env` with `SMTP_PASS=rsupmvvvvwrsuxuh`, verify port 465 SSL, and remove suspended backup hosts. |
| 4 | **Robust Delivery Engine** | Implement unified `EmailDeliveryService` with multi-provider fallback (Google Workspace primary + transactional HTTPS fallback), delivery headers, error tracing, and configurable rate pacing. |
| 5 | **Cooldown & Dry-Run Safety** | Ensure dry-run / mock mode is default in automated testing. Zero live emails dispatched during active cooldown. |
| 6 | **Post-Cooldown Verification Runner** | Provide standalone script `scripts/verify_delivery_post_cooldown.py` with pacing, detailed diagnostics, and full execution instructions for live testing after the cooldown window. |
