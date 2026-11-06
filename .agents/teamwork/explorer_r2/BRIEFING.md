# BRIEFING — 2026-10-25T23:35:00Z

## Mission
Audit apps/portal/ (app.py, routes/, services/, templates/) for auth/session, CSRF, DB fallback, default credentials, payment webhook, upload sandbox, email failures, CSP connect-src, and ProxyFix wiring per R2.

## 🔒 My Identity
- Archetype: explorer
- Roles: Portal Readiness Auditor
- Working directory: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2
- Original parent: 3a4d7ac2-699c-47ca-9101-c0e51547ba94
- Milestone: R2 Portal Production-Readiness Audit

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Audit apps/portal/ (app.py, routes/, services/, templates/) for 9 specific focus areas in R2
- Every finding must cite exact relative file path and line number, classification (Blocker/Warning/Info), explanation, and recommended fix
- Write report to c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2\handoff.md
- Maintain progress.md as heartbeat

## Current Parent
- Conversation ID: 3a4d7ac2-699c-47ca-9101-c0e51547ba94
- Updated: 2026-10-25T22:49:15Z

## Investigation State
- **Explored paths**: `apps/portal/app.py`, `apps/portal/routes/`, `apps/portal/services/`, `apps/portal/templates/`, `apps/portal/.env*`, `deploy/`, `scripts/`
- **Key findings**:
  1. `SESSION_COOKIE_DOMAIN` unset in Flask; cookies scoped host-only to `lms.dbert.in`. `staff_login` misses session token creation.
  2. `scraped_lead_comment_add` in `CSRF_EXEMPT_ENDPOINTS` mutates DB without CSRF validation (Blocker).
  3. `require_postgres` checks deprecated `FLASK_ENV == "production"`; `.env` has `REQUIRE_POSTGRES=false` & empty `DATABASE_URL`, silently falling back to `internship.db`.
  4. Credential guard `assert not _insecure` checks all 4 defaults, but is bypassed if `FLASK_DEBUG=true`.
  5. Webhook HMAC verification is bypassed when `RAZORPAY_WEBHOOK_SECRET` is unset.
  6. Upload extensions blocked; Nginx `/uploads/` static alias bypasses Flask's IDOR defense.
  7. Async emails swallow SMTP exceptions and report HTTP 200 success.
  8. CSP `connect-src` omits `https://dbert.in` and `https://lms.dbert.in`.
  9. ProxyFix has `x_proto=1, x_host=1`, but Nginx unified conf omits `X-Forwarded-Host`.
- **Unexplored areas**: None for R2 scope.

## Key Decisions Made
- All 9 focus areas thoroughly verified with exact line numbers and code snippets.
- Documented Blocker/Warning/Info classifications and concrete fixes.

## Artifact Index
- DISPATCH.md — incoming dispatch records
- BRIEFING.md — working memory and identity
- progress.md — activity log & heartbeat
- handoff.md — final audit report
