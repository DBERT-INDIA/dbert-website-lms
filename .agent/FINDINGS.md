# Baseline Architectural & Static Findings

**Date:** 2026-09-25  
**Baseline Commit:** `cfc7e95`

## Baseline Scan Summary

### 1. Database & SQLite Scan
- Multiple references to `sqlite3` and `internship.db` in `apps/portal/app.py`, migration scripts, deployment scripts (`deploy/deploy_ec2.sh`), and unit test suites (`tests/`).
- `apps/portal/internship.db` was untracked/deleted in working directory.
- `apps/portal/app.py` contains SQLite PRAGMA execution and SQLite fallback helper logic in `init_db()`.

### 2. Email Transport Scan
- `apps/portal/dbert-mailer/` is present with standalone SMTP delivery logic.
- Documentation (`docs/EXTERNAL_SERVICES.md`, `docs/INCIDENT_RUNBOOK.md`) still refers to legacy direct SMTP and obsolete configurations.
- `apps/portal/app.py` and outbox mechanisms contain references to direct `smtplib` and `SMTP_PASS` fallbacks.

### 3. Test Suite Baseline
- **Total Tests:** 347 | **Passed:** 344 | **Failed:** 3 | **Duration:** 148.94s
- **Existing Baseline Failures:**
  1. `test_intern_auth_workflow`: Failed due to direct SMTP connection attempt (`530 5.7.0 Authentication Required`).
  2. `test_chat_without_csrf_returns_403`: Failed expecting 403, received 401 UNAUTHORIZED.
  3. `test_cron_endpoint_with_valid_secret_is_csrf_exempt`: Failed with HTTP 403 on `/cron/clean-tokens`.
