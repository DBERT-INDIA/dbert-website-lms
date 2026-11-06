# Requirement R2: Portal (Flask/Gunicorn) Production-Readiness Audit Report

**Auditor**: `explorer_r2` (Role: Portal Readiness Auditor)  
**Date**: 2026-10-25  
**Working Directory**: `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r2`  
**Workspace Root**: `c:\Users\user\Desktop\dbert-website-lms`  
**Target Scope**: `apps/portal/app.py`, `apps/portal/routes/`, `apps/portal/services/`, `apps/portal/templates/`, `deploy/`, and `scripts/production_preflight.sh`  

---

## Executive Summary

A comprehensive static analysis and readiness audit was conducted across the DBERT Flask/Gunicorn LMS portal (`apps/portal/`) in accordance with Requirement R2 from `ORIGINAL_REQUEST.md`. 

The audit identified **6 Blockers**, **4 Warnings**, and **2 Informational** findings across the 9 designated readiness focus areas:
1. **Auth & session dead ends**: Missing explicit `SESSION_COOKIE_DOMAIN`; staff login issues auth-less session; `X-Forwarded-Host` header omitted in portal Nginx block.
2. **CSRF gaps**: `scraped_lead_comment_add` mutates database state without CSRF verification while in `CSRF_EXEMPT_ENDPOINTS` (Blocker).
3. **Database fallback risk**: `adapter.py` checks deprecated `FLASK_ENV == "production"`; default `.env` has `REQUIRE_POSTGRES=false` & empty `DATABASE_URL`, causing silent fallback to SQLite `internship.db` in production (Blocker). Preflight script has single-quote variable expansion bug (Blocker).
4. **Default credential leakage**: `assert not _insecure` checks all 4 default credentials, but the entire guard is bypassed if `FLASK_DEBUG=true` (Blocker). Secret key length < 32 characters only triggers a warning (Warning).
5. **Payment webhook**: Webhook HMAC signature verification is conditionally executed (`if webhook_sec:`), completely bypassing signature validation when `RAZORPAY_WEBHOOK_SECRET` is unset (Blocker). The variable is missing from `.env.production.sample` (Blocker).
6. **Upload sandbox**: File extensions (`.py`, `.php`, `.sh`) are strictly blocked by allowlist and magic bytes. However, Nginx directly aliases `/uploads/` to disk, completely bypassing Flask's IDOR access control and authorization logic (Blocker).
7. **Email silent fails**: `send_email_async` catches all SMTP exceptions in a background daemon thread, logging failure while calling routes return HTTP 200 success to users (Blocker).
8. **CSP connect-src**: `connect-src` in `csp_policy_for()` omits `https://dbert.in` and `https://lms.dbert.in`, blocking cross-subdomain fetch/API calls (Warning).
9. **ProxyFix wiring**: `ProxyFix` is properly initialized with `x_proto=1` and `x_host=1`; Nginx passes `X-Forwarded-Proto $scheme` but omits `X-Forwarded-Host $host` in the LMS block (Warning).

---

## Detailed Findings Table

| ID | Category | Severity | File:Line | Description | Recommended Fix |
|---|---|---|---|---|---|
| **F-01** | Auth & Session | **Warning** | `apps/portal/app.py:90-93`<br>`apps/portal/app.py:3654-3662` | `SESSION_COOKIE_DOMAIN` is not explicitly configured in `app.config`, and `domain` is omitted in `_set_session_cookie()`. Cookies are host-only (`lms.dbert.in`), preventing cross-subdomain session recognition with `dbert.in`. | Explicitly configure `app.config["SESSION_COOKIE_DOMAIN"] = os.environ.get("SESSION_COOKIE_DOMAIN", ".dbert.in")` and pass `domain=app.config.get("SESSION_COOKIE_DOMAIN")` to `_set_session_cookie()`. |
| **F-02** | Auth & Session | **Warning** | `apps/portal/app.py:6699-6725` | `staff_login` only populates Flask session keys (`staff_id`, `staff_email`, `staff_name`) and does not invoke `create_session()` or `_set_session_cookie()`. Staff users receive no `dbert_auth` token and cannot access routes guarded by `require_admin()` (which expects `admin_id`). | Standardize `staff_login` to create a unified token session via `create_session(staff_email, "staff")` and attach it via `_set_session_cookie()`. |
| **F-03** | CSRF Protection | **Blocker** | `apps/portal/app.py:3691`<br>`apps/portal/app.py:18739-18833` | `scraped_lead_comment_add` is listed in `CSRF_EXEMPT_ENDPOINTS`. It executes authenticated database mutations (`INSERT INTO scraped_internship_comments`) without verifying `X-CSRF-Token`, enabling cross-site comment forgery. | Remove `scraped_lead_comment_add` from `CSRF_EXEMPT_ENDPOINTS` in `apps/portal/app.py:3691`. |
| **F-04** | Database Fallback | **Blocker** | `apps/portal/services/database/adapter.py:844`<br>`apps/portal/.env:4-13` | `require_postgres` checks `os.environ.get("FLASK_ENV") == "production"`. `FLASK_ENV` is deprecated/removed in Flask 2.3+. In `apps/portal/.env`, `REQUIRE_POSTGRES=false` and `DATABASE_URL=` are set, causing silent fallback to SQLite `internship.db` in production. | In `adapter.py:844`, evaluate production mode via `(os.environ.get("FLASK_DEBUG", "false").lower() != "true")` or `REQUIRE_POSTGRES=true`. Prohibit SQLite initialization when `FLASK_DEBUG != "true"`. |
| **F-05** | Database Fallback | **Blocker** | `scripts/production_preflight.sh:53-60` | Preflight check tests variables inside single-quoted strings (e.g. `'${REQUIRE_POSTGRES:-}' = 'true'`), preventing Bash parameter expansion. Checks always evaluate the literal string and silently pass. | Replace single quotes with double quotes (e.g. `"${REQUIRE_POSTGRES:-}" = "true"`). |
| **F-06** | Credential Leakage | **Blocker** | `apps/portal/app.py:344-353` | The production credential assertion guard (`assert not _insecure`) is wrapped in `if os.environ.get("FLASK_DEBUG", "false").lower() != "true":`. Setting `FLASK_DEBUG=true` in production completely bypasses the guard, allowing startup with default credentials. | Enforce production credential validation regardless of `FLASK_DEBUG` if running on EC2 or when `ENVIRONMENT=production`, or assert credentials unconditionally on non-local hostnames. |
| **F-07** | Credential Leakage | **Warning** | `apps/portal/app.py:300-302` | `SECRET_KEY` length < 32 characters only prints a warning to stdout and does not abort application startup. | Change the warning to an `assert len(app.config.get("SECRET_KEY", "")) >= 32` when running in production. |
| **F-08** | Payment Webhook | **Blocker** | `apps/portal/app.py:14734-14738`<br>`apps/portal/.env.production.sample` | In `api_razorpay_webhook()`, HMAC signature validation is guarded by `if webhook_sec:`. If `RAZORPAY_WEBHOOK_SECRET` is unset, verification is skipped entirely, leaving the CSRF-exempt endpoint vulnerable to unauthenticated fake payment injection. `RAZORPAY_WEBHOOK_SECRET` is also absent from `.env.production.sample`. | Remove `if webhook_sec:` bypass; require `RAZORPAY_WEBHOOK_SECRET` to be non-empty and return 500 if unconfigured, or 400 if signature fails. Add `RAZORPAY_WEBHOOK_SECRET` to `.env.production.sample`. |
| **F-09** | Upload Sandbox | **Blocker** | `deploy/dbert-unified-nginx.conf:126-130`<br>`apps/portal/app.py:17561-17580` | Nginx statically aliases `/uploads/` directly to disk without authentication or security headers. This completely bypasses Flask's IDOR and object-level authorization checks in `serve_uploaded_file()`, exposing candidate resumes, task files, and payment receipts publicly. | Remove direct static `/uploads/` alias in Nginx, proxy `/uploads/` to Gunicorn/Flask to enforce `serve_uploaded_file()`, and attach `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff`. |
| **F-10** | Email Failure | **Blocker** | `apps/portal/app.py:4042-4075`<br>`apps/portal/app.py:17780-17795` | `send_email_async` executes asynchronously in a daemon thread and catches all SMTP exceptions, logging `sent="NO"`. Calling endpoints (such as `forgot_password`) return HTTP 200 success to the client even when email delivery fails completely. | Implement synchronous validation or transactional outbox queueing with error propagation for critical flows like password reset, and notify the user if dispatch fails. |
| **F-11** | CSP Directives | **Warning** | `apps/portal/app.py:285` | `connect-src` in `csp_policy_for()` specifies `'self'` and third-party origins, but omits `https://dbert.in` and `https://lms.dbert.in`. Cross-origin API calls between website and portal are blocked by the browser when CSP is enforced. | Add `https://dbert.in https://lms.dbert.in` to `connect-src` in `apps/portal/app.py:285`. |
| **F-12** | ProxyFix Wiring | **Info** | `deploy/dbert-unified-nginx.conf:136-140` | `ProxyFix` is correctly configured with `x_proto=1, x_host=1` in `app.py:164`. However, `deploy/dbert-unified-nginx.conf` omits `proxy_set_header X-Forwarded-Host $host;` in the LMS block (though present in the website block). | Add `proxy_set_header X-Forwarded-Host $host;` to `location /` in the LMS block of `dbert-unified-nginx.conf`. |

---

## 1. Observation

### 1.1 Auth & Session Configuration
- **Observation 1.1.1** (`apps/portal/app.py:90-93`):
  ```python
  app.config["SESSION_COOKIE_NAME"] = "dbert_flask"
  app.config["SESSION_COOKIE_HTTPONLY"] = True
  app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
  ```
  `SESSION_COOKIE_DOMAIN` is not defined anywhere in `apps/portal/app.py` or `.env`.
- **Observation 1.1.2** (`apps/portal/app.py:114-116, 160`):
  ```python
  is_prod = os.environ.get("FLASK_DEBUG", "false").lower() != "true"
  _is_debug = not is_prod
  COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "1" if is_prod else "0") == "1"
  ...
  app.config["SESSION_COOKIE_SECURE"] = COOKIE_SECURE
  ```
- **Observation 1.1.3** (`apps/portal/app.py:3652-3663`):
  ```python
  def _set_session_cookie(resp, token):
      """The ONE place the auth cookie is issued (spec §5.1)."""
      resp.set_cookie(
          AUTH_COOKIE,
          token,
          max_age=SESSION_DAYS * 86400,
          httponly=True,
          secure=COOKIE_SECURE,
          samesite="Lax",
          path="/"
      )
      return resp
  ```
  No `domain` parameter is passed to `set_cookie()`.
- **Observation 1.1.4** (`apps/portal/app.py:164`):
  ```python
  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
  ```
- **Observation 1.1.5** (`deploy/dbert-unified-nginx.conf:136-140`):
  ```nginx
  location / {
      proxy_pass http://127.0.0.1:5001;
      proxy_http_version 1.1;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_read_timeout 90;
  }
  ```
  `X-Forwarded-Proto $scheme;` is present. `X-Forwarded-Host $host;` is absent in this block (lines 136-140), whereas line 88 in the website server block contains `proxy_set_header X-Forwarded-Host $host;`.

### 1.2 CSRF Protection & Form Templates
- **Observation 1.2.1** (`apps/portal/app.py:3691`):
  ```python
  CSRF_EXEMPT_ENDPOINTS = {"scraped_lead_click_track", "scraped_lead_comment_add"}
  ```
- **Observation 1.2.2** (`apps/portal/app.py:3721-3725`):
  ```python
  ep = request.endpoint or ""
  ep_short = ep.split(".")[-1]
  if request.path.startswith("/api/payment/razorpay/webhook") or ep in CSRF_EXEMPT_ENDPOINTS or ep_short in CSRF_EXEMPT_ENDPOINTS:
      return None
  ```
- **Observation 1.2.3** (`apps/portal/app.py:18739-18833`):
  ```python
  def scraped_lead_comment_add(job_id):
      """Submit a public engagement comment on a scraped internship lead.
      Requires login. Rate-limited per IP to prevent spam."""
      intern = current_intern()
      ...
      conn.execute(
          "INSERT INTO scraped_internship_comments (job_id, intern_id, intern_name, body) VALUES (?,?,?,?)",
          (job_id, intern.get("id", 0), intern.get("name", "Intern"), body),
      )
  ```
  The handler writes directly to the database on behalf of the logged-in user without CSRF validation.
- **Observation 1.2.4** (`apps/portal/templates/`):
  - Form search scan over all 61 HTML templates confirmed all templates include `_head.html`, `_csrf.html`, or define `csrf_token`.
  - Classic POST forms (`company_profile_edit.html:30` and `_app_shell.html:82`) both include `{{ csrf_field() }}`.
  - The remaining 22 `<form>` tags in templates use AJAX event interception (`data-act-submit`, `data-prevent-submit`, or JS event listeners with `_csrf.html` fetch interceptor).

### 1.3 Database Adapter & Fallback Paths
- **Observation 1.3.1** (`apps/portal/services/database/adapter.py:844-856`):
  ```python
  require_postgres = os.environ.get("REQUIRE_POSTGRES", "false").lower() == "true" or os.environ.get("FLASK_ENV") == "production"

  if is_postgres_target:
      return PostgreSQLAdapter(db_target)

  if require_postgres:
      raise RuntimeError(
          "PostgreSQL runtime database is enforced (REQUIRE_POSTGRES=true or production env). "
          "SQLite connections and fallbacks are strictly prohibited."
      )

  # 4. Default SQLiteAdapter (Allowed ONLY for legacy unit testing when REQUIRE_POSTGRES is false)
  return SQLiteAdapter(db_target, timeout=timeout)
  ```
- **Observation 1.3.2** (`apps/portal/.env:4, 11, 13`):
  ```ini
  FLASK_ENV=development
  REQUIRE_POSTGRES=false
  DATABASE_URL=
  ```
  `apps/portal/app.py:333` resolves `default_db = os.path.join(os.path.dirname(__file__), "internship.db")`.
- **Observation 1.3.3** (`apps/portal/services/sourcing/pipeline.py:43-52`):
  ```python
  try:
      from services.database.adapter import get_db_adapter
      return get_db_adapter()
  except Exception:
      # Fallback to direct sqlite
      import sqlite3
      db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "internship.db"))
      conn = sqlite3.connect(db_path)
      conn.row_factory = sqlite3.Row
      return conn
  ```
- **Observation 1.3.4** (`scripts/production_preflight.sh:53-60`):
  ```bash
  check "REQUIRE_POSTGRES=true" "$([ '${REQUIRE_POSTGRES:-}' = 'true' ] && echo ok || echo "REQUIRE_POSTGRES=${REQUIRE_POSTGRES:-unset}")"
  check "DATABASE_URL is postgres" "$(echo '${DATABASE_URL:-}' | grep -qE '^postgres(ql)?://' && echo ok || echo 'DATABASE_URL missing or not postgres')"
  check "POSTGRES_SCHEMA set" "$([ -n '${POSTGRES_SCHEMA:-}' ] && echo ok || echo 'POSTGRES_SCHEMA not set')"
  check "FLASK_DEBUG=false" "$([ '${FLASK_DEBUG:-}' != 'true' ] && echo ok || echo 'FLASK_DEBUG is true in production!')"
  ```

### 1.4 Production Credential Guards
- **Observation 1.4.1** (`apps/portal/app.py:344-353`):
  ```python
  if os.environ.get("FLASK_DEBUG", "false").lower() != "true":
      _insecure = []
      if app.secret_key == "digitalblinc2026secretkey": _insecure.append("FLASK_SECRET_KEY")
      if ADMIN_PASSWORD == "dbert_admin_2026":           _insecure.append("ADMIN_PASSWORD")
      if ADMIN_KEY == "dbert_admin_2026":                _insecure.append("ADMIN_KEY")
      if ADMIN_USERNAME == "dbert_admin":                _insecure.append("ADMIN_USERNAME")
      assert not _insecure, (
          "Refusing to start in production with default value(s) for: " + ", ".join(_insecure) +
          ". Set strong values in .env (or set FLASK_DEBUG=true for local dev)."
      )
  ```
- **Observation 1.4.2** (`apps/portal/app.py:300-302`):
  ```python
  if is_prod:
      if len(app.config.get("SECRET_KEY", "")) < 32:
          print("[WARNING] FLASK_SECRET_KEY is shorter than 32 chars.")
  ```

### 1.5 Razorpay Payment Webhook
- **Observation 1.5.1** (`apps/portal/app.py:14723-14738`):
  ```python
  @app.route("/api/payment/razorpay/webhook", methods=["POST"])
  def api_razorpay_webhook():
      """
      Idempotent webhook endpoint for asynchronous Razorpay events.
      Validates X-Razorpay-Signature header against RAZORPAY_WEBHOOK_SECRET.
      """
      try:
          sig = request.headers.get("X-Razorpay-Signature", "")
          raw_body = request.data

          # Verify webhook signature if secret configured
          _, _, webhook_sec = razorpay_client.get_razorpay_keys()
          if webhook_sec:
              if not razorpay_client.verify_webhook_signature(raw_body, sig):
                  log_abuse(get_client_ip(), "/api/payment/razorpay/webhook", "bad_webhook_sig", "signature_mismatch")
                  return jsonify({"status": "error", "message": "Invalid webhook signature"}), 400
  ```
- **Observation 1.5.2** (`apps/portal/.env.production.sample:35-37`):
  ```ini
  # Razorpay Production Keys
  RAZORPAY_KEY_ID=your_razorpay_key_id
  RAZORPAY_KEY_SECRET=your_razorpay_key_secret
  ```
  `RAZORPAY_WEBHOOK_SECRET` is not defined anywhere in `.env.production.sample` or `apps/portal/.env`.

### 1.6 Upload Sandbox & Execution Exposure
- **Observation 1.6.1** (`apps/portal/app.py:79, 336` & `services/file_security_service.py:13`):
  ```python
  app.config["UPLOAD_FOLDER"] = os.environ.get("UPLOAD_FOLDER", "uploads")
  ALLOWED_EXT = {"png", "jpg", "jpeg", "pdf"}
  ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
  ```
- **Observation 1.6.2** (`services/file_security_service.py:24-36`):
  Explicitly rejects `MALICIOUS_PAYLOAD_SIGNATURES`: `<?php`, `<?= `, `<script`, `#!/bin/sh`, `#!/bin/bash`, `eval(`, etc.
- **Observation 1.6.3** (`deploy/dbert-unified-nginx.conf:126-130`):
  ```nginx
  # Uploads (CVs, Resumes, Project Artifacts)
  location /uploads/ {
      alias /var/www/dbert-website-lms/apps/portal/uploads/;
      expires 30d;
      access_log off;
  }
  ```
- **Observation 1.6.4** (`apps/portal/app.py:17561-17580`):
  Flask defines `serve_uploaded_file(filename)` at `/uploads/<path:filename>` with authentication, object-level authorization (IDOR defense), and security headers.

### 1.7 SMTP Failure & Silent Drops
- **Observation 1.7.1** (`apps/portal/app.py:4042-4074`):
  ```python
  def send_email_async(to_email, subject, html_body, name="", campaign="transactional"):
      ...
      def _send():
          sent = "YES"
          try:
              ...
              elif EMAIL_PROVIDER == "smtp":
                  _smtp_send_raw(msg, to_email)
          except Exception as e:
              sent = "NO"; log_error("EMAIL[" + EMAIL_PROVIDER + "]", e)
          finally:
              ...
      threading.Thread(target=_send, daemon=True).start()
  ```
- **Observation 1.7.2** (`apps/portal/app.py:17780-17791`):
  ```python
  try:
      send_password_reset_email(target_name, email, reset_url)
      log_security_event("password_reset_email_sent", {"account_type": account_type, "account_id": account_id})
  except Exception as mail_err:
      log_error("forgot-password:email", mail_err)

  return jsonify({
      "status": "success",
      "message": "If that email exists, a reset link has been sent."
  })
  ```
- **Observation 1.7.3** (`apps/portal/app.py:304` & `apps/portal/.env:27`):
  ```python
  SMTP_HOST = os.environ.get("SMTP_HOST", "dbert.online")
  ```

### 1.8 Content Security Policy `connect-src`
- **Observation 1.8.1** (`apps/portal/app.py:285`):
  ```python
  "connect-src 'self' https://onesignal.com https://*.onesignal.com https://api.onesignal.com https://www.googletagmanager.com https://www.google-analytics.com https://*.google-analytics.com https://*.analytics.google.com; "
  ```
- **Observation 1.8.2** (`apps/portal/app.py:18139-18143`):
  ```python
  policy = csp_policy_for(csp_nonce())
  if CSP_ENFORCE:
      resp.headers.setdefault("Content-Security-Policy", policy)
  ```
  `CSP_ENFORCE` defaults to `True` (`apps/portal/app.py:257`).

---

## 2. Logic Chain

### 2.1 Auth & Session Dead Ends
1. From **Observation 1.1.1**, `SESSION_COOKIE_DOMAIN` is `None` in Flask config, and from **Observation 1.1.3**, `_set_session_cookie()` omits the `domain` argument.
2. Browsers treat cookies without an explicit `domain` attribute as host-only cookies (restricted strictly to the request host `lms.dbert.in`).
3. If an intern interacts with `https://dbert.in` (the Next.js website), the `dbert_auth` and `dbert_flask` cookies are not transmitted, preventing shared session recognition across subdomains.
4. From **Observation 1.1.2** and **1.1.4**, `COOKIE_SECURE=True` in production and `ProxyFix` is initialized with `x_proto=1`.
5. From **Observation 1.1.5**, Nginx sends `X-Forwarded-Proto $scheme;`. When accessed over HTTPS, `ProxyFix` sets `wsgi.url_scheme = "https"`, ensuring `request.is_secure == True` and cookies with the `Secure` flag are retained.
6. However, `staff_login` (**Finding F-02**) fails to call `create_session()`, leaving staff authenticated solely via Flask's client-side cookie session without an entry in `user_sessions` or the `dbert_auth` token.

### 2.2 CSRF Vulnerability Chain
1. From **Observation 1.2.1** and **1.2.2**, `_enforce_csrf()` explicitly bypasses verification for all endpoints in `CSRF_EXEMPT_ENDPOINTS`.
2. From **Observation 1.2.3**, `scraped_lead_comment_add` is in `CSRF_EXEMPT_ENDPOINTS` and mutates database state by executing `INSERT INTO scraped_internship_comments`.
3. Because the endpoint relies on cookies for authentication (`current_intern()` / `current_user`) and omits CSRF token validation, an attacker hosting a malicious site can force an authenticated visitor's browser to execute a POST request to `/api/lead/<job_id>/comment`, forging public spam or malicious comments.
4. This violates the security boundary since CSRF exemption is only valid for non-mutating pings or server-to-server calls.

### 2.3 Database Fallback & Preflight Failure Chain
1. From **Observation 1.3.1**, `require_postgres` checks `os.environ.get("FLASK_ENV") == "production"`. In Flask 2.3 and 3.0, `FLASK_ENV` is no longer supported or set by the framework.
2. From **Observation 1.3.2**, the committed `apps/portal/.env` defines `REQUIRE_POSTGRES=false` and `DATABASE_URL=`.
3. If this `.env` is loaded on EC2, `is_postgres_target` evaluates to `False`, `require_postgres` evaluates to `False`, and `get_db_adapter()` returns `SQLiteAdapter("internship.db")`.
4. In production under multiple Gunicorn worker processes, concurrent writes to SQLite (`enrollments`, `course_payments`, `user_sessions`) fail due to lock contention or remain trapped in the local SQLite file, silently dropping financial records upon container rebuild.
5. From **Observation 1.3.4**, `production_preflight.sh` was designed to block this, but single quotes around `'${REQUIRE_POSTGRES:-}'` prevent variable expansion. The check tests the literal string `${REQUIRE_POSTGRES:-}` instead of the environment value, producing false `[OK]` results.

### 2.4 Credential Guard Bypass Chain
1. From **Observation 1.4.1**, the startup assertion `assert not _insecure` verifies `FLASK_SECRET_KEY`, `ADMIN_PASSWORD`, `ADMIN_KEY`, and `ADMIN_USERNAME`.
2. However, the assertion is enclosed inside `if os.environ.get("FLASK_DEBUG", "false").lower() != "true":`.
3. If `FLASK_DEBUG=true` is set, the entire block is skipped. The server starts with hardcoded secrets (`digitalblinc2026secretkey`, `dbert_admin_2026`).
4. Furthermore, from **Observation 1.4.2**, keys shorter than 32 bytes only generate a terminal warning without preventing startup.

### 2.5 Razorpay Webhook Insecurity Chain
1. From **Observation 1.5.1**, incoming POST requests to `/api/payment/razorpay/webhook` are CSRF-exempt.
2. In `api_razorpay_webhook()`, line 14735 executes `if webhook_sec:`.
3. From **Observation 1.5.2**, `RAZORPAY_WEBHOOK_SECRET` is not defined in `.env.production.sample` or `apps/portal/.env`.
4. Therefore, `webhook_sec` is empty string (`""`), causing `if webhook_sec:` to evaluate to `False`.
5. The entire HMAC signature verification block (`verify_webhook_signature`) is bypassed. Any attacker can POST forged JSON payment payloads to `/api/payment/razorpay/webhook` and have them processed without credentials.

### 2.6 Upload Sandbox IDOR Bypass Chain
1. From **Observation 1.6.1** and **1.6.2**, uploaded files are restricted to `png`, `jpg`, `jpeg`, and `pdf`, with active rejection of script headers (`<?php`, `#!/bin/bash`).
2. From **Observation 1.6.4**, Flask provides `serve_uploaded_file()` with strict IDOR controls preventing unauthorized access to other candidates' resumes or receipts.
3. However, from **Observation 1.6.3**, Nginx unified config defines `location /uploads/ { alias /var/www/dbert-website-lms/apps/portal/uploads/; }`.
4. Nginx resolves requests to `/uploads/*` directly from disk before Flask ever receives the request. Flask's IDOR authorization logic is completely bypassed, rendering private candidate uploads publicly downloadable by filename.

### 2.7 Email Silent Failure Chain
1. From **Observation 1.7.1**, `send_email_async` executes in a daemon thread.
2. If SMTP fails (such as connecting to invalid default `SMTP_HOST="dbert.online"` from **Observation 1.7.3**), `_send()` catches `Exception`, logs to `email_log` as `sent="NO"`, and suppresses the exception.
3. From **Observation 1.7.2**, `forgot_password()` returns HTTP 200 `{"status": "success", "message": "If that email exists, a reset link has been sent."}` before the thread completes.
4. Users attempting password resets or receiving enrollment confirmations are falsely informed of success while the email silently drops.

### 2.8 CSP Blocking Cross-Origin Calls
1. From **Observation 1.8.1**, `connect-src` lists `'self'` but lacks explicit entries for `https://dbert.in` and `https://lms.dbert.in`.
2. From **Observation 1.8.2**, `CSP_ENFORCE=True` is enabled by default.
3. When the browser executes JavaScript on `lms.dbert.in` attempting to fetch resources or data from `dbert.in`, the browser enforces the policy and blocks the request due to origin mismatch.

---

## 3. Caveats

1. **Static Analysis Only**: Testing was conducted purely against local source code and deployment templates; no live AWS EC2 or production PostgreSQL instance was available during this audit.
2. **Session Sharing Intent**: The audit assumed that cross-domain authentication between `dbert.in` and `lms.dbert.in` may be desired. If LMS authentication is intentionally isolated as a separate silo on `lms.dbert.in`, setting `SESSION_COOKIE_DOMAIN` to host-only is acceptable, provided no website components make credentialed cross-origin requests.
3. **CPanel Legacy Traces**: `apps/portal/` contains legacy files from older cPanel/CGI deployments (`cgi-bin/`, `.htaccess`, `passenger_wsgi.py`). These do not affect standard EC2 Gunicorn/Nginx operations, but could cause confusion if deployed into shared hosting.

---

## 4. Conclusion

The LMS portal contains critical architectural and security vulnerabilities that must be remediated prior to production deployment:
- **Blockers**:
  1. `scraped_lead_comment_add` in `CSRF_EXEMPT_ENDPOINTS` allowing CSRF state mutation.
  2. Silent SQLite fallback on financial writes due to outdated `FLASK_ENV` checks and `.env` misconfigurations.
  3. Preflight script (`production_preflight.sh`) single-quote variable expansion bug masking PostgreSQL absence.
  4. Credential assert bypass when `FLASK_DEBUG=true`.
  5. Webhook HMAC validation bypass when `RAZORPAY_WEBHOOK_SECRET` is unset.
  6. Nginx `/uploads/` direct disk serving bypassing Flask's IDOR access control.
  7. Silent failure of password reset and transactional emails under SMTP failure.
- **Warnings & Informational**:
  1. Omission of `SESSION_COOKIE_DOMAIN` causing cross-origin session loss.
  2. Asymmetric session in `staff_login`.
  3. Missing `https://dbert.in` and `https://lms.dbert.in` in CSP `connect-src`.
  4. Missing `proxy_set_header X-Forwarded-Host $host;` in the Nginx portal reverse proxy block.

---

## 5. Verification Method

### 5.1 Static Verification Commands

1. **Verify CSRF Exemption in `app.py`**:
   ```bash
   grep -n "CSRF_EXEMPT_ENDPOINTS" apps/portal/app.py
   # Confirms scraped_lead_comment_add is present at line 3691
   ```

2. **Verify Database Adapter Fallback Logic**:
   ```bash
   grep -n -C 5 "require_postgres" apps/portal/services/database/adapter.py
   # Confirms line 844 checks FLASK_ENV == "production"
   ```

3. **Verify Preflight Single-Quote Bug**:
   ```bash
   grep -n "REQUIRE_POSTGRES" scripts/production_preflight.sh
   # Confirms single-quote literal string at line 53
   ```

4. **Verify Webhook HMAC Bypass**:
   ```bash
   grep -n -C 5 "if webhook_sec:" apps/portal/app.py
   # Confirms signature verification is skipped if webhook_sec is falsy at line 14735
   ```

5. **Verify Nginx Uploads IDOR Bypass**:
   ```bash
   grep -n -C 5 "location /uploads/" deploy/dbert-unified-nginx.conf
   # Confirms direct alias to disk without authorization at lines 126-130
   ```

6. **Verify CSP connect-src**:
   ```bash
   grep -n "connect-src" apps/portal/app.py
   # Confirms omission of dbert.in at line 285
   ```

### 5.2 Test Execution Command
To verify existing test coverage:
```bash
pytest apps/portal/tests/
```
In particular, run:
```bash
pytest apps/portal/tests/security/test_security_regression.py
pytest apps/portal/tests/test_postgres_enforcement.py
```
*(Note: `test_postgres_enforcement.py` verifies runtime assertion behavior).*

### 5.3 Invalidation Conditions
This report is invalidated if:
- `scraped_lead_comment_add` is removed from `CSRF_EXEMPT_ENDPOINTS`.
- `REQUIRE_POSTGRES` enforcement is decoupled from `FLASK_ENV` and defaults to mandatory under Gunicorn.
- `api_razorpay_webhook()` unconditionally rejects requests when `RAZORPAY_WEBHOOK_SECRET` is unconfigured.
- Nginx `/uploads/` location is removed or updated to use `X-Accel-Redirect` / proxying to Flask.
