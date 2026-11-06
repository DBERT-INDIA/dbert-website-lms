# BRIEFING — 2026-11-04T23:37:30Z

## Mission
Conduct a thorough static analysis of all email dispatch logic, SMTP configuration, MIME/header generation, error handling, and configuration defaults in apps/portal and across the repository to diagnose email deliverability failures.

## 🔒 My Identity
- Archetype: explorer
- Roles: explorer, survey, static analysis
- Working directory: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_survey_1
- Original parent: 1954b148-861e-46e3-9273-69539bb3dcb5
- Milestone: Email Deliverability Analysis & Diagnosis

## 🔒 Key Constraints
- Read-only investigation — do NOT implement code fixes or send emails
- STRICT COOLDOWN ENFORCEMENT: Under NO circumstances send live emails or connect to external SMTP/API servers
- Write findings to analysis.md and handoff.md in working directory
- Deliver message to parent via send_message

## Current Parent
- Conversation ID: 1954b148-861e-46e3-9273-69539bb3dcb5
- Updated: 2026-11-04T23:37:30Z

## Investigation State
- **Explored paths**:
  - `apps/portal/app.py` (email helpers, MIME builder, SMTP transports, auth/payment routes)
  - `apps/portal/services/outbox_service.py`
  - `apps/portal/services/notification_service.py`
  - `apps/portal/services/notifications/dispatch.py`
  - `apps/portal/routes/payment.py`, `auth.py`, `applications.py`, `enrollment.py`
  - `apps/portal/.env`, `.env.example`, `.env.production.sample`, `.env.staging.example`
  - `deploy/run_cron_tasks.sh`, `deploy/dbert-portal.service`
  - `scripts/verify_delivery_dual_test.py`, `scripts/dispatch_certificates.py`, `scripts/test_isolation_matrix.py`, `scripts/test_link_formats.py`, `scripts/test_clean_alternative.py`, `scripts/send_verified_production_test.py`, `scripts/read_bounces.py`, `scripts/check_imap.py`
  - `logs/email_dispatch_log.csv`
- **Key findings**:
  - `send_email_async` executes in an unmonitored daemon thread that swallows all SMTP exceptions and returns HTTP 200 OK across all routes.
  - RFC 8058 One-Click unsubscribe fails with 405 Method Not Allowed because `/unsubscribe` lacks POST method registration.
  - Secondary backup SMTP causes DMARC SPF alignment mismatch (`dbert.info` vs `dbert.in`).
  - Open tracking pixels (`/e/o.gif`) and UTM query params are injected into all transactional emails, triggering spam heuristics.
  - STARTTLS failures in `_send_smtp_single` are swallowed with `except Exception: pass`.
  - Transactional event outbox is never drained by cron because `deploy/run_cron_tasks.sh` sends `X-Cron-Secret` to port 8000 instead of `X-Cron-Key` to port 5001.
  - Password drift: `.env` has `ckxnpudkapzgzbxl` whereas recent tests used `rsupmvvvvwrsuxuh`.
  - Account was throttled by Google Workspace after 56 certificate emails with attachments were dispatched in 14 minutes.
- **Unexplored areas**: None within the static code analysis scope.

## Key Decisions Made
- Completed deep static audit covering all 17 email dispatch functions, transport mechanisms, MIME headers, error suppression patterns, and configuration drift.
- Compiled comprehensive findings into `analysis.md` and structured 5-component handoff into `handoff.md`.

## Artifact Index
- DISPATCH.md — Task instructions and dispatch log
- BRIEFING.md — Working memory and status
- progress.md — Liveness heartbeat and step tracker
- analysis.md — Full static analysis report
- handoff.md — 5-component completion handoff report
