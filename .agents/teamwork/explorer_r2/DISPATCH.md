# Dispatch for Explorer R2: Portal Production-Readiness

Objective: Audit apps/portal/ (app.py, routes, services, templates) for auth, CSRF, database fallback, credentials, payments, uploads, email, CSP, ProxyFix.
Working Directory: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2
Original Request: c:\Users\user\Desktop\dbert-website-lms\ORIGINAL_REQUEST.md
Report Destination: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2\handoff.md

## 2026-10-25T22:49:15Z
Sender: 3a4d7ac2-699c-47ca-9101-c0e51547ba94
Priority: MESSAGE_PRIORITY_HIGH
Content:
You are explorer_r2 (Role: Portal Readiness Auditor).
Your working directory is: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2
The project workspace root is: c:\Users\user\Desktop\dbert-website-lms
You MUST read: c:\Users\user\Desktop\dbert-website-lms\ORIGINAL_REQUEST.md

Your task is requirement R2 from ORIGINAL_REQUEST.md:
Audit `apps/portal/app.py` and the `routes/`, `services/`, and `templates/` directories for:
1. Auth & session dead ends: Login flows that can silently succeed but leave the user with no session — check SESSION_COOKIE_DOMAIN, SESSION_COOKIE_SECURE, and whether ProxyFix is wired with x_proto=1 so request.is_secure returns True behind Nginx.
2. CSRF gaps: Endpoints in CSRF_EXEMPT_ENDPOINTS that mutate state without justification; form templates that omit {{ csrf_field() }}.
3. Database fallback risk: Code paths where the SQLite fallback (internship.db) silently activates in production — look for dialect != "postgres" branches that handle writes (money, enrollments, auth). Check if accidental usage in production silently drops financial writes.
4. Default credential leakage: Confirm the production guard (assert not _insecure) fires for all four defaults (FLASK_SECRET_KEY, ADMIN_PASSWORD, ADMIN_KEY, ADMIN_USERNAME). Verify the guard cannot be bypassed by accidentally setting FLASK_DEBUG=true.
5. Payment webhook: Razorpay webhook endpoint must be CSRF-exempt AND have HMAC signature validation active simultaneously — check both conditions in the same handler.
6. Upload sandbox: Check UPLOAD_FOLDER path and extension allowlist — confirm .py, .php, .sh cannot be uploaded. Confirm uploaded files are not web-served with execute permission via Nginx.
7. Email silent fails: SMTP failure paths — does a failed email swallow the exception and return HTTP 200 to the user?
8. CSP connect-src: Does the Content Security Policy header include https://lms.dbert.in and https://dbert.in so cross-origin fetch calls between website and portal are not blocked?
9. ProxyFix wiring: Is x_proto=1, x_host=1 set on ProxyFix so behind Nginx, request.scheme == "https" and session cookies get Secure flag?

Requirements for output:
For EVERY finding, cite the exact relative file path and line number, classification (Blocker/Warning/Info), explanation, and recommended fix.
Write your complete, self-contained report to:
c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2\handoff.md
Update c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2\progress.md as you work.
When done, notify orchestrator via send_message with a brief summary and path to your handoff.md.
