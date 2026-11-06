# DISPATCH for worker_delivery_1

## Task
Permanent Robust Email Delivery Architecture Implementation & Post-Cooldown Verification Runner.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## STRICT CONSTRAINT: COOLDOWN ENFORCEMENT
UNDER NO CIRCUMSTANCES MAY ANY AGENT OR TOOL SEND LIVE OUTBOUND EMAILS DURING THIS TASK EXECUTION.
An immediate complete halt on active email sending is in effect for the cooldown window.
All tests executed by you must run in dry-run, mock, or local assertion mode.
DO NOT connect to external SMTP servers or external delivery APIs during development.

## Objectives & Scope

### 1. Robust Delivery Engine (`apps/portal/services/delivery_service.py` or integrated into `apps/portal`)
Implement a resilient, production-ready email delivery engine adhering to the contract in `SCOPE.md`:
`send_email(to, subject, html_content, text_content=None, tags=None, dry_run=False) -> DeliveryResult`
`DeliveryResult`: `success: bool`, `provider: str`, `message_id: str`, `error: Optional[str]`, `diagnostics: dict`

Key Requirements:
- **Primary Provider**: Google Workspace SMTP (`smtp.gmail.com:465` SSL / port 587 STARTTLS) with active App Password `rsupmvvvvwrsuxuh` loaded from environment `SMTP_PASS`.
- **Secondary Provider / Fallback**: Resilient fallback provider (e.g. transactional HTTPS API or backup SMTP with strict domain alignment). If the primary fails or is throttled, cleanly attempt the secondary provider and record diagnostics.
- **Pacing / Rate Limiter**: Configurable pacing (e.g. 10–15s inter-message delay or rate limiter) to prevent bursting and Google velocity throttling.
- **Header Synthesis (RFC 5322 & Deliverability Best Practices)**:
  - Valid `Message-ID` with FQDN `<uuid>@dbert.in`.
  - Accurate `Date` header (RFC 2822).
  - Explicit `From`: `DBERT Support <abhinav.sharma@dbert.in>` (aligned with SPF & DKIM).
  - Explicit `Reply-To`: `support@dbert.in`.
  - Clean `Return-Path` / envelope sender aligned with domain.
  - Multipart MIME: both clean plain text and responsive HTML parts.
- **Content Hygiene**:
  - Remove 1x1 tracking pixel (`/e/o.gif`) and marketing UTM queries on transactional emails.
  - Purge all dead `dbert.info` and legacy `dbert.online` links/footers. Standardize on `support@dbert.in` and `dbert.in`.
- **RFC 8058 One-Click Unsubscribe Fix**:
  - In `apps/portal/app.py`, update `@app.route("/unsubscribe")` to accept `methods=["GET", "POST"]` and return `HTTP 200 OK` on POST.
- **Hard Bounce Guard**:
  - Maintain and integrate the `DUMMY_EMAIL_DOMAINS` guard to intercept synthetic domains at zero network cost.
- **Persistent Diagnostics & Logging**:
  - Enhance `email_log` or logging to persist error message details, provider used, and message ID instead of just `"YES"` or `"NO"`. Never swallow exceptions silently.

### 2. Configuration & Environment Updates
- Update `apps/portal/.env` and `.env.production.sample`:
  - Set `SMTP_PASS=rsupmvvvvwrsuxuh`.
  - Remove dead `SMTP_BACKUP_HOST=dbert.info` and related credentials.
  - Ensure all email configuration variables are documented and cleanly loaded.

### 3. Automated Post-Cooldown Verification Runner (`scripts/verify_delivery_post_cooldown.py`)
Build an executable standalone script that the user can run locally after the cooldown window expires:
- Targets both `ain.sharma.abhinav@gmail.com` and `ajnatechrpa@gmail.com`.
- CLI Options:
  - `--dry-run` (DEFAULT/SAFE): Validates MIME construction, DNS SPF/DKIM/DMARC resolution, SMTP credential loading, recipient validation, and logs payload without opening network sockets or sending emails.
  - `--live`: Explicit flag required to perform actual live delivery after cooldown.
  - `--delay`: Configurable delay between recipient dispatches (default 15s).
- Detailed terminal output: Reports step-by-step progress, DNS authentication status, provider handshake status, message IDs, delivery status, and diagnostics.

### 4. Step-by-Step Documentation (`docs/EMAIL_DELIVERY_VERIFICATION_GUIDE.md`)
Create comprehensive user documentation covering:
- Deliverability root cause summary (DMARC, footers, rate bursts, RFC 8058).
- Explanation of the cooldown period and why pacing is essential.
- Instructions for running the verification runner (dry-run first, then post-cooldown live execution).
- How to inspect headers in Gmail ("Show original") to verify SPF: PASS, DKIM: PASS, DMARC: PASS.
- Troubleshooting common issues.

### 5. Automated Tests (Dry-Run / Mock)
- Add comprehensive unit tests in `apps/portal/tests/test_delivery_service.py` verifying:
  - MIME structure, headers, `Message-ID`, RFC 8058 unsubscribe response.
  - Multi-provider fallback logic with mocked SMTP/API clients.
  - Dry-run mode safety (zero live network dispatch).
  - Dummy domain interception.
  - Pacing and rate limiting.
- Run tests using `pytest` and verify 100% pass.

## Inputs
- `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\ORIGINAL_REQUEST.md`
- `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\orchestrator_3\ROOT_CAUSE_ANALYSIS.md`
- `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\orchestrator_3\SCOPE.md`

## Output Requirements
- Write your completion handoff in `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\worker_delivery_1\handoff.md` with full test commands and outputs.
- Notify the orchestrator when complete.


## 2026-11-04T23:39:23Z
Context: Important Implementation Nuance from explorer_survey_1
Content: Explorer 1 identified that in `apps/portal/tests/test_email_path_migration.py`, tests using `@example.com` were previously failing because the newly added `DUMMY_EMAIL_DOMAINS` guard at `app.py:4066` intercepts `@example.com` before invoking mocked transports.
When implementing the delivery service and updating tests, ensure tests can either:
1. Provide a test flag/fixture or use `@test.dbert.in` / valid mock domain for unit tests, or
2. Allow `test_email_path_migration.py` to test both the dummy domain interception path AND the delivery transport path cleanly.
Action: Keep this in mind when implementing `delivery_service.py` and running the test suite.
