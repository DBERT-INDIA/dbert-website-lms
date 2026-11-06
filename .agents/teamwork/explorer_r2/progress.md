# Progress Log - Explorer R2 (Portal Readiness Auditor)

Last visited: 2026-10-25T23:30:00Z

## Status: Audit Complete across all 9 R2 focus areas
1. Auth & session dead ends: Verified. `SESSION_COOKIE_DOMAIN` unset (host-only). `SESSION_COOKIE_SECURE` defaults True. `ProxyFix` has x_proto=1 and x_host=1. Nginx sends X-Forwarded-Proto $scheme but omits X-Forwarded-Host in portal block. Staff login sets session staff_id but omits auth token and admin_id.
2. CSRF gaps: Verified. `scraped_lead_comment_add` in `CSRF_EXEMPT_ENDPOINTS` mutates DB without CSRF token (Blocker). Form templates audited; `_head.html`/`_csrf.html` install global fetch interceptor.
3. Database fallback risk: Verified. `require_postgres` checks deprecated `FLASK_ENV == "production"`. `apps/portal/.env` has `REQUIRE_POSTGRES=false` and `DATABASE_URL=` which silently falls back to `internship.db` at repo root. Writes to enrollments and payments go to SQLite. `production_preflight.sh` has single-quote bug masking validation.
4. Default credential leakage: Verified. `assert not _insecure` checks all 4 defaults (FLASK_SECRET_KEY, ADMIN_PASSWORD, ADMIN_KEY, ADMIN_USERNAME). Bypassed completely if `FLASK_DEBUG=true`. Short key (<32) only prints warning.
5. Payment webhook: Verified. Razorpay webhook is CSRF-exempt, but HMAC validation is guarded by `if webhook_sec:`, which silently skips signature verification if `RAZORPAY_WEBHOOK_SECRET` is unset. Secret is missing from `.env.production.sample`.
6. Upload sandbox: Verified. Extension allowlist (`png`, `jpg`, `jpeg`, `pdf`) and magic bytes block `.py`, `.php`, `.sh`. Nginx does not execute scripts, but directly aliases `/uploads/`, bypassing Flask's IDOR defense and access control in `serve_uploaded_file`.
7. Email silent fails: Verified. `send_email_async` catches exceptions in background daemon thread and logs `sent="NO"`, while calling routes return HTTP 200 success to the user.
8. CSP connect-src: Verified. `connect-src` in `csp_policy_for()` omits `https://dbert.in` and `https://lms.dbert.in`, causing cross-origin API blocking under enforced CSP.
9. ProxyFix wiring: Verified. `x_proto=1, x_host=1` configured in `app.py:164`. Nginx portal block sends `X-Forwarded-Proto $scheme`, but omits `X-Forwarded-Host $host`.

Writing comprehensive handoff report to handoff.md.
