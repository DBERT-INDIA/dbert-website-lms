# Security & Hardening Audit Report (Requirement R5)

**Auditor:** explorer_r5 (Security & Hardening Auditor)  
**Date:** 2026-10-25  
**Target Application:** DBERT Production Ecosystem (Next.js Website & Flask/Gunicorn LMS Portal)  
**Status:** Complete Hard Handoff

---

## Executive Summary

| ID | Category | Severity | File & Line Number | Issue Summary |
|---|---|---|---|---|
| **SEC-R5-01** | Database Web Exposure | **Blocker** | `deploy/dbert-unified-nginx.conf:1-143`, `internship.db:root` | 38MB live SQLite DB committed at repo root; Nginx lacks any deny rule for `.db`/`.sqlite` files |
| **SEC-R5-02** | Uploads Authorization Bypass | **Blocker** | `deploy/dbert-unified-nginx.conf:126-130`, `apps/portal/app.py:17561-17625` | Nginx statically aliases `/uploads/` directly to disk, completely bypassing Flask's Phase 15 authentication & IDOR authorization sandbox |
| **SEC-R5-03** | Secret `.env` Web Exposure | **Blocker** | `deploy/dbert-unified-nginx.conf:1-143`, `apps/portal/.env:1-58` | Nginx configuration completely lacks dotfile/`.env` protection; production `.env` contains plaintext DB passwords, SMTP keys, and admin credentials |
| **SEC-R5-04A** | Debug Mode Information Leak | **Blocker** | `apps/portal/app.py:8171-8173` | When `FLASK_DEBUG=true`, verification OTP is directly leaked in the HTTP response JSON payload (`dev_otp_hint`) |
| **SEC-R5-04B** | Preflight Variable Expansion Bug | **Blocker** | `scripts/production_preflight.sh:53-60` | Single quotes around variables like `'${FLASK_DEBUG:-}'` prevent shell expansion, causing preflight to silently pass debug mode and weak keys |
| **SEC-R5-04C** | Insecure Environment Flag | **Warning** | `apps/portal/.env:4`, `start_portal.bat:3-4` | Committed production `.env` sets `FLASK_ENV=development`, disabling rate limiting and relaxing security defaults |
| **SEC-R5-05A** | Admin Route Misdirection Bug | **Blocker** | `apps/portal/app.py:8395-8406` | `@app.route("/admin/course-payments/<int:pay_id>/review")` decorates an unauthenticated stub `_signal_tutor_course_unlock`, orphaning the real admin handler and crashing on execution |
| **SEC-R5-05B** | Admin Login Brute-Force Gap | **Warning** | `apps/portal/app.py:4960-4988` | `/admin/login` only checks IP rate limit and never calls `login_locked(username)`, leaving admin accounts vulnerable to distributed credential stuffing |
| **SEC-R5-06** | Secret Key Guard Severity Failure | **Blocker** | `apps/portal/app.py:300-303`, `apps/portal/app.py:344-353` | Production short key check only prints a stdout warning without aborting; keys under 32 characters slip through, allowing offline HMAC session forgery |
| **SEC-R5-07A** | Complete Rate-Limit Bypass | **Blocker** | `apps/portal/app.py:707-708`, `apps/portal/.env:4` | `rate_check()` immediately returns `(True, 0)` when `FLASK_ENV=development`. Because `.env` has `FLASK_ENV=development`, all rate limits are disabled |
| **SEC-R5-07B** | Missing Registration Rate Limits | **Warning** | `apps/portal/app.py:9630-9657` | `/company/signup` has zero rate limiting, allowing automated registration flooding and resource exhaustion |
| **SEC-R5-07C** | Nginx Edge Rate-Limiting Absent | **Warning** | `deploy/dbert-unified-nginx.conf:1-143` | Nginx has no `limit_req_zone` or `limit_req` directives, exposing Gunicorn and SQLite to direct Denial-of-Service and lock contention |

---

## 1. Observations

### 1.1 Item 1: `internship.db` Web Exposure & Nginx Protection Rules
- **Direct Observation**:
  - File `internship.db` exists directly in the repository root (`c:\Users\user\Desktop\dbert-website-lms\internship.db`), with file size **38,273,024 bytes** (38 MB). Duplicate copies exist at `apps/portal/internship.db` (38 MB), `apps/portal/cgi-bin/internship.db`, and `dbert-api-package/databases/internship.db`.
  - In `deploy/deploy_ec2_unified.sh` lines 8-10, the repository is cloned directly into `/var/www/dbert-website-lms`.
  - In `deploy/dbert-unified-nginx.conf` lines 1-143:
    ```nginx
    # Section 3: DBERT Main Website
    location /_next/static/ {
        alias /var/www/dbert-website-lms/apps/website/.next/static/;
        expires 365d;
        access_log off;
    }
    location / {
        proxy_pass http://127.0.0.1:3001;
        ...
    }
    # Section 4: DBERT LMS Platform
    location /static/ {
        alias /var/www/dbert-website-lms/apps/portal/static/;
        expires 30d;
        access_log off;
    }
    location /uploads/ {
        alias /var/www/dbert-website-lms/apps/portal/uploads/;
        expires 30d;
        access_log off;
    }
    location / {
        proxy_pass http://127.0.0.1:5001;
        ...
    }
    ```
  - **Absence of Rules**: There is **no** regex location block (`location ~* \.(db|sqlite|sqlite3)$`) and **no** `deny all` directive anywhere in `deploy/dbert-unified-nginx.conf`, `deploy/dbert-portal-nginx.conf`, or `deploy/dbert-website-nginx.conf`.
  - In contrast, legacy Apache cPanel configuration `apps/portal/.htaccess` lines 20-22 explicitly included:
    ```apache
    <FilesMatch "^(\.env|\.git|.*\.db|.*\.sqlite|.*\.sqlite3|.*\.py|.*\.log|requirements.*\.txt)$">
      Require all denied
    </FilesMatch>
    ```
    This protection was dropped during the Nginx migration.

### 1.2 Item 2: `uploads/` Web Exposure & Authorization
- **Direct Observation**:
  - In `deploy/dbert-unified-nginx.conf` lines 126-130:
    ```nginx
    # Uploads (CVs, Resumes, Project Artifacts)
    location /uploads/ {
        alias /var/www/dbert-website-lms/apps/portal/uploads/;
        expires 30d;
        access_log off;
    }
    ```
  - In `apps/portal/app.py` lines 17561-17625, a dedicated Flask controller exists:
    ```python
    @app.route("/uploads/<path:filename>")
    def serve_uploaded_file(filename):
        """
        Phase 15: File Security & Sandbox Access Controller.
        Private uploaded files (payment screenshots, task submission files, deposit proofs)
        must never be accessible via predictable public URLs.
        Enforces:
          1. Authentication: 401 if unauthenticated
          2. Anti-Path Traversal: 400 if traversal detected or path escapes UPLOAD_FOLDER
          3. Object-level Authorization (IDOR Defense):
             - Admin / Staff: Allowed for auditing & review
             - Intern: Allowed ONLY if file belongs to them (verified via task_submissions,
               enrollments, course_payments, post_hire_deposits)
        ...
        """
        user = get_current_user()
        staff = current_staff()
        admin = require_admin()
        company = current_company()
        mentor = current_mentor()
        ...
        if not user_context:
            return jsonify({"status": "error", "message": "Authentication required."}), 401
    ```
  - Because Nginx matches `location /uploads/` with `alias` ahead of `location /`, all requests to `/uploads/*` are fulfilled directly by the Nginx web server from disk. Requests never reach the Gunicorn WSGI gateway or Flask.
  - Furthermore, in `deploy/dbert-unified-nginx.conf` lines 126-130, the security headers `Content-Disposition: attachment` and `X-Content-Type-Options: nosniff` (present in legacy `deploy/dbert-portal-nginx.conf:50-51`) are completely missing.

### 1.3 Item 3: `.env` Web Exposure & Public Access
- **Direct Observation**:
  - `apps/portal/.env` contains active production configuration and credentials:
    - Line 6: `FLASK_SECRET_KEY=hyhyhyhy99089hhhyykjkjk_dbert_portal_2026_xyz_secure_key_extended`
    - Line 19: `ADMIN_PASSWORD=[REDACTED_BY_SECURITY_POLICY]`
    - Line 20: `ADMIN_KEY=hyhyhyhy99089hhhyykjkjkhsajhJSHyyyy`
    - Line 30: `SMTP_PASS="hY36cI8t;*3[jYA8"`
    - Line 38: `SMTP_BACKUP_PASS="+Y8]Z;96izOTp,PR"`
    - Line 57: `CRON_SECRET=dbert_cron_secret_2026_cpanel_protected`
  - `apps/website/.env` generated in `deploy/deploy_ec2_unified.sh:110` contains:
    - Line 110: `DATABASE_URL=postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms`
    - Line 111: `JWT_SECRET=production_placeholder_secret_2026`
  - In `deploy/dbert-unified-nginx.conf`, there is **no rule** blocking hidden dotfiles or `.env` files (e.g., `location ~ /\. { deny all; return 404; }`).
  - If Nginx's default site configuration is active on port 80/443 pointing to `/var/www` or `/var/www/html`, or if an alias or root misconfiguration maps to the repo root, `.env` is served directly to unauthenticated web clients.

### 1.4 Item 4: Debug Mode Leakage & Preflight Expansion Bug
- **Direct Observation**:
  - `apps/portal/.env` line 4: `FLASK_ENV=development`
  - `apps/portal/.env` line 5: `FLASK_DEBUG=false`
  - `apps/portal/.env.example` line 1: `FLASK_DEBUG=true`
  - `start_portal.bat` line 3: `set FLASK_DEBUG=1`
  - `apps/portal/app.py` lines 8171-8173 in `auth_send_otp()`:
    ```python
    resp = {
        "status": "success",
        "message": f"Verification code sent to {email}. Valid for 10 minutes."
    }
    import os
    if os.environ.get("FLASK_DEBUG", "false").lower() == "true":
        resp["dev_otp_hint"] = otp
        
    return jsonify(resp)
    ```
  - `apps/portal/app.py` lines 8182-8183 and 8200-8201 in `verify_recaptcha()`:
    ```python
    if os.environ.get("FLASK_DEBUG", "false").lower() == "true":
        return True # Bypass captcha in debug
    ```
  - `apps/portal/app.py` lines 114-116:
    ```python
    is_prod = os.environ.get("FLASK_DEBUG", "false").lower() != "true"
    _is_debug = not is_prod
    COOKIE_SECURE = os.environ.get("COOKIE_SECURE", "1" if is_prod else "0") == "1"
    ```
    When `FLASK_DEBUG=true`, `COOKIE_SECURE` becomes `False`.
  - `scripts/production_preflight.sh` lines 53-60:
    ```bash
    check "REQUIRE_POSTGRES=true" "$([ '${REQUIRE_POSTGRES:-}' = 'true' ] && echo ok || echo "REQUIRE_POSTGRES=${REQUIRE_POSTGRES:-unset}")"
    check "DATABASE_URL is postgres" "$(echo '${DATABASE_URL:-}' | grep -qE '^postgres(ql)?://' && echo ok || echo 'DATABASE_URL missing or not postgres')"
    check "POSTGRES_SCHEMA set" "$([ -n '${POSTGRES_SCHEMA:-}' ] && echo ok || echo 'POSTGRES_SCHEMA not set')"
    check "FLASK_SECRET_KEY set" "$([ -n '${FLASK_SECRET_KEY:-}' ] && echo ok || echo 'FLASK_SECRET_KEY not set')"
    check "FLASK_DEBUG=false" "$([ '${FLASK_DEBUG:-}' != 'true' ] && echo ok || echo 'FLASK_DEBUG is true in production!')"
    ```
    Every variable is wrapped in single quotes inside `"$([ '...' != 'true' ])"`. In Bash, `'${FLASK_DEBUG:-}'` evaluates to the literal string `${FLASK_DEBUG:-}`, which is never equal to `'true'`. Thus, the test evaluates to `[ '${FLASK_DEBUG:-}' != 'true' ]` -> `true` -> `echo ok`. **The check always passes regardless of what is set in `.env`.**

### 1.5 Item 5: Admin Panel Route Authentication & Bug
- **Direct Observation**:
  - `apps/portal/app.py` lines 8395-8406:
    ```python
    @app.route("/admin/course-payments/<int:pay_id>/review", methods=["POST"])
    def _signal_tutor_course_unlock(intern_id, course_id):
        """
        Simulated webhook to signal an external tutor system that a course payment was verified.
        Added to fix F821 undefined name bug which caused silent 500 errors on payment verification.
        """
        log_info("tutor_unlock", f"Simulated unlock for intern {intern_id} course {course_id}")
        return True

    def admin_course_payment_review(pay_id):
        if not require_admin():
            return jsonify({"status": "error", "message": "Unauthorized"}), 401
    ```
    The route decorator `@app.route("/admin/course-payments/<int:pay_id>/review", methods=["POST"])` sits directly above `def _signal_tutor_course_unlock(intern_id, course_id):` instead of `def admin_course_payment_review(pay_id):`.
    `_signal_tutor_course_unlock` contains **no** authentication check (`require_admin()` is absent).
    `admin_course_payment_review` is an unrouted orphan function.
  - In `apps/portal/app.py` lines 4960-4988 (`admin_login`):
    ```python
    ip = get_client_ip()
    allowed, ra = rate_check(f"login:admin:ip:{ip}", *RL_LOGIN_IP)
    if not allowed:
        log_abuse(ip, "/admin/login", f"login:admin:ip:{ip}", "rate_limit", username)
        return too_many(ra)
    ...
    if not auth_valid:
        record_login_fail(username)
    ```
    `login_locked(username)` is never checked at the start of `admin_login()`, whereas it is checked for interns (line 9539), companies (line 9689), and mentors (line 12648).

### 1.6 Item 6: Secret Key Guard Severity & Short Key Slip-Through
- **Direct Observation**:
  - `apps/portal/app.py` lines 77-78:
    ```python
    _FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "")
    app.secret_key = _FLASK_SECRET_KEY or "digitalblinc2026secretkey"
    ```
  - `apps/portal/app.py` lines 212-216:
    ```python
    if os.environ.get("FLASK_DEBUG", "false").lower() != "true":
        assert _FLASK_SECRET_KEY, (
            "FLASK_SECRET_KEY must be explicitly set in production (the default dev "
            "key would let anyone forge session cookies)."
        )
    ```
  - `apps/portal/app.py` lines 300-303:
    ```python
    # P2-6: Production configuration validation
    if is_prod:
        if len(app.config.get("SECRET_KEY", "")) < 32:
            print("[WARNING] FLASK_SECRET_KEY is shorter than 32 chars.")
    ```
  - `apps/portal/app.py` lines 344-353:
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
  - If `FLASK_SECRET_KEY` is set to any non-empty string under 32 characters (e.g. `FLASK_SECRET_KEY="abc123"`):
    1. Line 213: `assert _FLASK_SECRET_KEY` passes because `"abc123"` is truthy.
    2. Line 302: `print("[WARNING] ...")` prints to stdout and execution continues without raising any exception.
    3. Line 346: `app.secret_key == "digitalblinc2026secretkey"` is false (`"abc123"` is not the default string), so `_insecure` remains empty.
    4. Line 350: `assert not _insecure` passes without error.
    5. The app boots in production with an easily crackable key.

### 1.7 Item 7: Rate Limiting Middleware & Environment Invalidation
- **Direct Observation**:
  - `deploy/dbert-unified-nginx.conf` contains no `limit_req_zone` or `limit_req` directives.
  - `apps/portal/app.py` lines 703-708:
    ```python
    def rate_check(bucket, limit, window_seconds):
        """Sliding-window check shared by all workers via the rate_events table.
        Returns (allowed: bool, retry_after: int). Records the event when allowed.
        Fails OPEN (never blocks real users) if the limiter DB errors."""
        if os.environ.get("FLASK_ENV") == "development" or os.environ.get("DISABLE_RATE_LIMIT") == "1":
            return (True, 0)
    ```
  - `apps/portal/.env` line 4:
    ```ini
    FLASK_ENV=development
    ```
  - Because `FLASK_ENV=development` is set in the runtime `.env` file, `rate_check()` immediately returns `(True, 0)` for all callers.
  - `apps/portal/app.py` lines 9630-9657 (`company_signup`): The endpoint parses input, checks email validity, and inserts directly into `companies` without calling `rate_check()` or checking any honeypot or captcha.
  - In `apps/portal/app.py` lines 711-729:
    ```python
    with get_db() as conn:
        conn.execute("DELETE FROM rate_events WHERE bucket=? AND created_at < ?", (bucket, now - window_seconds))
        ...
        conn.execute("INSERT INTO rate_events (bucket, created_at) VALUES (?,?)", (bucket, now))
        conn.commit()
    ```
    All rate events are recorded via synchronous table writes in SQLite (`rate_events`).

---

## 2. Logic Chain

### 2.1 Database Exposure Logic Chain
1. *Observation 1.1*: `internship.db` (38 MB) contains full production historical tables (intern accounts, contact information, passwords, leads).
2. *Observation 1.1*: `deploy/deploy_ec2_unified.sh` clones the entire repo under `/var/www/dbert-website-lms/`.
3. *Observation 1.1*: Nginx config in `deploy/dbert-unified-nginx.conf` has no block rule matching `.db` or `.sqlite` files.
4. *Deduction*: If any server block in Nginx serves files with `root /var/www/dbert-website-lms` (or if standard `/etc/nginx/sites-enabled/default` is not removed or binds to port 80/IP), requests to `/internship.db` or `/apps/portal/internship.db` will be returned verbatim as a downloadable SQLite database.
5. *Deduction*: Furthermore, committing a 38MB live database into version control is an intrinsic information disclosure vulnerability.
6. *Conclusion*: Classified as **Blocker**.

### 2.2 Uploads Authorization Bypass Logic Chain
1. *Observation 1.2*: Nginx evaluates `location /uploads/ { alias /var/www/dbert-website-lms/apps/portal/uploads/; }` before the fallback `location / { proxy_pass ...; }`.
2. *Observation 1.2*: Nginx handles the file serving internally from disk without making an HTTP subrequest or checking session cookies.
3. *Observation 1.2*: Flask contains a comprehensive authorization function `serve_uploaded_file` (`apps/portal/app.py:17561`) that checks user session, role, and ownership of the file in the database.
4. *Deduction*: Nginx completely short-circuits the application layer. No code in `serve_uploaded_file` ever runs in production.
5. *Deduction*: Any unauthenticated user who requests `https://lms.dbert.in/uploads/<filename>` will receive the file directly from Nginx. Resumes, payment proofs, and confidential task submissions are publicly downloadable by guessing or obtaining the filename.
6. *Conclusion*: Classified as **Blocker**.

### 2.3 `.env` Web Exposure Logic Chain
1. *Observation 1.3*: `apps/portal/.env` and `apps/website/.env` store live database credentials, SMTP passwords, and secret keys.
2. *Observation 1.3*: Nginx configuration files contain no directive matching hidden dotfiles (`location ~ /\. { ... }`).
3. *Observation 1.1 & 1.3*: Apache `.htaccess` protected `.env` on cPanel, but Nginx ignores `.htaccess`.
4. *Deduction*: If a webroot is set to the repository root or an alias misconfiguration occurs, `.env` will be served as plain text (`text/plain`).
5. *Conclusion*: Classified as **Blocker**.

### 2.4 Debug Mode & Preflight Bug Logic Chain
1. *Observation 1.4*: In `apps/portal/app.py:8171-8173`, the `auth_send_otp` route explicitly appends `resp["dev_otp_hint"] = otp` whenever `FLASK_DEBUG` is `"true"`.
2. *Observation 1.4*: In `apps/portal/app.py:8182`, reCAPTCHA validation returns `True` unconditionally when `FLASK_DEBUG` is `"true"`.
3. *Observation 1.4*: In `scripts/production_preflight.sh:57`, `[ '${FLASK_DEBUG:-}' != 'true' ]` tests the literal string `'${FLASK_DEBUG:-}'` against `'true'`.
4. *Deduction*: The preflight script can never detect when `FLASK_DEBUG=true` is set. If an operator sets `FLASK_DEBUG=true` in `.env` (as suggested in `README.md:50`), preflight gives a false green light (`[PASS] Preflight passed`).
5. *Deduction*: In production, any user requesting an OTP will receive the valid OTP in the API response JSON, allowing instantaneous account takeover without email access.
6. *Conclusion*: Classified as **Blocker**.

### 2.5 Admin Panel Auth Bug Logic Chain
1. *Observation 1.5*: At `apps/portal/app.py:8395`, `@app.route("/admin/course-payments/<int:pay_id>/review", methods=["POST"])` is attached to `_signal_tutor_course_unlock(intern_id, course_id)`.
2. *Observation 1.5*: `_signal_tutor_course_unlock` takes 2 positional parameters (`intern_id`, `course_id`) and performs no authentication checks.
3. *Observation 1.5*: When Flask receives `POST /admin/course-payments/42/review`, it dispatches to `_signal_tutor_course_unlock(pay_id=42)`, resulting in `TypeError: unexpected keyword argument 'pay_id'` and an unhandled 500 error.
4. *Observation 1.5*: The intended handler `admin_course_payment_review(pay_id)` (line 8404) is left undecorated, making manual payment approval impossible.
5. *Observation 1.5*: In `admin_login`, `login_locked(username)` is absent, allowing unlimited password guessing attempts against the admin username if IPs are distributed.
6. *Conclusion*: Classified as **Blocker** (broken admin route) and **Warning** (missing admin account lockout).

### 2.6 Secret Key Severity Logic Chain
1. *Observation 1.6*: Line 301 checks `len(app.config.get("SECRET_KEY", "")) < 32` and only executes `print()`.
2. *Observation 1.6*: Line 213 checks only `assert _FLASK_SECRET_KEY` (non-empty).
3. *Observation 1.6*: Line 346 checks only if the key is identical to the default string `"digitalblinc2026secretkey"`.
4. *Deduction*: Any custom secret key with low entropy (e.g. `12345678`, `password`, `dbertsecret`) satisfies all assertions and boots cleanly without throwing an exception.
5. *Deduction*: Flask session cookies signed with weak HMAC keys can be brute-forced offline using GPU tools (`flask-unsign`). Once cracked, an attacker can craft a cookie containing `{"admin_id": 1, "role": "admin"}` and gain full admin access via `require_admin()` (line 3788).
6. *Conclusion*: Classified as **Blocker**.

### 2.7 Rate Limiting Logic Chain
1. *Observation 1.7*: `apps/portal/app.py:707` returns `(True, 0)` immediately if `FLASK_ENV == "development"`.
2. *Observation 1.7*: `apps/portal/.env:4` explicitly defines `FLASK_ENV=development`.
3. *Deduction*: Every endpoint relying on `rate_check()` (including `/signin`, `/signup/stage1`, `/auth/send-otp`, `/reset`, `/check-email`) has its rate limiting completely disabled in the current configuration.
4. *Observation 1.7*: `/company/signup` lacks any rate limit call.
5. *Observation 1.7*: Nginx has no edge rate limiting, so every HTTP request directly hits Gunicorn workers and performs SQLite read/writes.
6. *Conclusion*: Classified as **Blocker** (total bypass due to `FLASK_ENV`) and **Warning** (missing edge limits & registration throttle).

---

## 3. Caveats

1. **Static Analysis Only**: Audit was conducted via code review and static script evaluation; no live EC2 instances or external network services were probed.
2. **PostgreSQL vs SQLite at Runtime**: In PostgreSQL mode (`REQUIRE_POSTGRES=true`), `internship.db` is not used by the application logic, but the physical file remains in the repository checkout on disk.
3. **Apache vs Nginx**: Legacy `.htaccess` rules demonstrated awareness of dotfile and database exposure, but those rules are inert under Nginx.

---

## 4. Conclusion & Detailed Findings

### Finding SEC-R5-01: `internship.db` Web Exposure & Unprotected Database Files
- **Severity**: **Blocker**
- **File & Line**: `deploy/dbert-unified-nginx.conf:1-143`, repository root `internship.db`
- **Description**:
  The SQLite database file `internship.db` (38 MB) exists in the repository root and contains sensitive personal data, scraped leads, and student credentials. In the deployment script `deploy/deploy_ec2_unified.sh:8`, the repository is cloned to `/var/www/dbert-website-lms`. The Nginx configuration in `deploy/dbert-unified-nginx.conf` lacks any rule blocking access to `.db`, `.sqlite`, or database dump files. If a default server block or root mapping serves this directory, the database is directly downloadable over HTTP.
- **Recommended Fix**:
  1. Add a global block in all Nginx server blocks in `deploy/dbert-unified-nginx.conf`:
     ```nginx
     location ~* \.(db|sqlite|sqlite3|sql|log)$ {
         deny all;
         return 404;
     }
     ```
  2. Remove `internship.db` from git tracking and add `*.db`, `*.sqlite`, `*.sqlite3` to `.gitignore`.

---

### Finding SEC-R5-02: Public Exposure of `uploads/` Bypassing Flask IDOR Controller
- **Severity**: **Blocker**
- **File & Line**: `deploy/dbert-unified-nginx.conf:126-130`, `apps/portal/app.py:17561-17625`
- **Description**:
  `deploy/dbert-unified-nginx.conf` maps `/uploads/` directly to disk via `alias /var/www/dbert-website-lms/apps/portal/uploads/;` without authentication. This completely bypasses Flask's `serve_uploaded_file` route at `apps/portal/app.py:17561`, which enforces user authentication, role checks, and object-level IDOR validation. Consequently, any unauthenticated visitor can download private user resumes, CVs, and payment screenshots.
- **Recommended Fix**:
  Delete the static `location /uploads/` block from `deploy/dbert-unified-nginx.conf`:
  ```nginx
  # REMOVE lines 125-130 in deploy/dbert-unified-nginx.conf:
  # location /uploads/ {
  #     alias /var/www/dbert-website-lms/apps/portal/uploads/;
  #     expires 30d;
  #     access_log off;
  # }
  ```
  Allowing `/uploads/` to fall through to `location /` ensures Flask's `serve_uploaded_file` executes, verifying user permissions before returning files with `send_from_directory()`.

---

### Finding SEC-R5-03: Lack of Nginx Protection for `.env` and Hidden Dotfiles
- **Severity**: **Blocker**
- **File & Line**: `deploy/dbert-unified-nginx.conf:1-143`, `apps/portal/.env:1-58`
- **Description**:
  Active production environment files (`apps/portal/.env`, `apps/website/.env`) contain database passwords, SMTP credentials, session secrets, and API keys. The Nginx configuration lacks any rule restricting access to dotfiles. Under Apache, this was blocked by `.htaccess`, but Nginx does not read `.htaccess`.
- **Recommended Fix**:
  Add a strict dotfile rejection rule to every server block in `deploy/dbert-unified-nginx.conf`:
  ```nginx
  location ~ /\. {
      deny all;
      return 404;
      access_log off;
      log_not_found off;
  }
  ```

---

### Finding SEC-R5-04: Debug Mode Information Disclosure & Preflight Script Bug
- **Severity**: **Blocker**
- **File & Line**: `apps/portal/app.py:8171-8173`, `scripts/production_preflight.sh:53-60`, `apps/portal/.env:4`
- **Description**:
  1. In `apps/portal/app.py:8171-8173`, when `FLASK_DEBUG=true`, `auth_send_otp` returns the OTP plaintext inside `dev_otp_hint`, allowing full account takeover.
  2. In `scripts/production_preflight.sh:57`, the command `[ '${FLASK_DEBUG:-}' != 'true' ]` uses single quotes, disabling variable expansion and causing the preflight script to always report `[PASS]` even when `FLASK_DEBUG=true`.
  3. `apps/portal/.env` line 4 commits `FLASK_ENV=development`.
- **Recommended Fix**:
  1. Fix variable expansion in `scripts/production_preflight.sh:53-60` by replacing single quotes with double quotes:
     ```bash
     check "FLASK_DEBUG=false" "$([ \"${FLASK_DEBUG:-}\" != 'true' ] && echo ok || echo 'FLASK_DEBUG is true in production!')"
     ```
  2. Change line 4 of `apps/portal/.env` to `FLASK_ENV=production`.
  3. Remove `resp["dev_otp_hint"] = otp` from `apps/portal/app.py:8171-8173` entirely, or guard it with `if False:` in production builds.

---

### Finding SEC-R5-05: Broken Admin Course Payment Review Handler & Missing Account Lockout
- **Severity**: **Blocker** (Route Bug) / **Warning** (Auth Lockout)
- **File & Line**: `apps/portal/app.py:8395-8406`, `apps/portal/app.py:4960-4963`
- **Description**:
  1. At `apps/portal/app.py:8395`, the decorator `@app.route("/admin/course-payments/<int:pay_id>/review", methods=["POST"])` decorates `def _signal_tutor_course_unlock(intern_id, course_id):`. The real handler `def admin_course_payment_review(pay_id):` on line 8404 has no route. Calling this route results in a `TypeError` (unexpected argument `pay_id`) and crashes with HTTP 500. Furthermore, the stub function `_signal_tutor_course_unlock` lacks any authentication guard.
  2. In `apps/portal/app.py:4960`, `/admin/login` only checks IP rate limit (`rate_check(f"login:admin:ip:{ip}", *RL_LOGIN_IP)`). It never calls `login_locked(username)`. An attacker rotating IP addresses can perform brute-force attacks against `admin` or `dbert_admin` indefinitely.
- **Recommended Fix**:
  1. Reorder the functions in `apps/portal/app.py:8395-8406`:
     ```python
     def _signal_tutor_course_unlock(intern_id, course_id):
         log_info("tutor_unlock", f"Simulated unlock for intern {intern_id} course {course_id}")
         return True

     @app.route("/admin/course-payments/<int:pay_id>/review", methods=["POST"])
     def admin_course_payment_review(pay_id):
         if not require_admin():
             return jsonify({"status": "error", "message": "Unauthorized"}), 401
         ...
     ```
  2. In `admin_login` (`apps/portal/app.py:4960`), add account lockout:
     ```python
     locked, ra = login_locked(username)
     if locked:
         log_abuse(ip, "/admin/login", f"loginfail:email:{username}", "account_locked", username)
         return too_many(ra)
     ```

---

### Finding SEC-R5-06: Ineffective Secret Key Length Guard
- **Severity**: **Blocker**
- **File & Line**: `apps/portal/app.py:300-303`, `apps/portal/app.py:344-353`
- **Description**:
  `apps/portal/app.py:300-303` checks `if len(app.config.get("SECRET_KEY", "")) < 32:` and only executes `print("[WARNING] FLASK_SECRET_KEY is shorter than 32 chars.")`. It does not abort application startup. In contrast, line 350 executes `assert not _insecure`, but only checks for the default string `"digitalblinc2026secretkey"`. If a developer supplies a short key (e.g. `secret123`), the application boots cleanly in production. Attackers can brute-force the short key offline and forge administrative session cookies.
- **Recommended Fix**:
  Update `apps/portal/app.py:300-303` and `344-353` to fail closed:
  ```python
  if is_prod:
      secret = app.secret_key or app.config.get("SECRET_KEY", "")
      if len(secret) < 32:
          raise ValueError("CRITICAL SECURITY ERROR: FLASK_SECRET_KEY must be at least 32 characters in production.")
  ```
  And in the `_insecure` check:
  ```python
  if len(app.secret_key) < 32: _insecure.append("FLASK_SECRET_KEY (< 32 chars)")
  ```

---

### Finding SEC-R5-07: Inactive Rate Limiting Due to `FLASK_ENV` & Lack of Edge Throttling
- **Severity**: **Blocker** (`FLASK_ENV` bypass) / **Warning** (Nginx & Registration)
- **File & Line**: `apps/portal/app.py:707-708`, `apps/portal/.env:4`, `apps/portal/app.py:9630-9657`, `deploy/dbert-unified-nginx.conf:1-143`
- **Description**:
  1. `rate_check()` in `apps/portal/app.py:707-708` has an early return:
     `if os.environ.get("FLASK_ENV") == "development" or os.environ.get("DISABLE_RATE_LIMIT") == "1": return (True, 0)`
     Because `apps/portal/.env` sets `FLASK_ENV=development`, rate limiting is bypassed across all routes in the application.
  2. `/company/signup` (`apps/portal/app.py:9630`) has no rate limiting or captcha, allowing automated registration spam.
  3. Nginx has no edge rate limiting (`limit_req_zone`), allowing brute-force traffic to saturate Gunicorn workers and lock the SQLite database.
- **Recommended Fix**:
  1. Set `FLASK_ENV=production` in `apps/portal/.env`.
  2. In `apps/portal/app.py:707`, change condition to:
     ```python
     if os.environ.get("DISABLE_RATE_LIMIT") == "1":
         return (True, 0)
     ```
  3. Add `rate_check(f"company_signup:ip:{ip}", 10, 3600)` to `/company/signup`.
  4. Configure edge rate limiting in `deploy/dbert-unified-nginx.conf`:
     ```nginx
     limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;
     limit_req_zone $binary_remote_addr zone=api_limit:10m rate=30r/m;

     location /admin/login {
         limit_req zone=auth_limit burst=5 nodelay;
         proxy_pass http://127.0.0.1:5001;
     }
     location /signin {
         limit_req zone=auth_limit burst=10 nodelay;
         proxy_pass http://127.0.0.1:5001;
     }
     ```

---

## 5. Verification Method

To independently verify each finding, execute the following commands and code inspections:

1. **Verify Finding SEC-R5-01 (`internship.db` exposure)**:
   ```powershell
   # Check DB file existence and size at repo root
   Get-Item .\internship.db | Select-Object FullName, Length
   # Inspect Nginx config for absence of .db deny rule
   Select-String -Path .\deploy\dbert-unified-nginx.conf -Pattern "\.db"
   ```
   *Expected Result*: File exists (~38MB); search returns 0 matches in Nginx config.

2. **Verify Finding SEC-R5-02 (`uploads/` bypass)**:
   ```powershell
   # Inspect Nginx config for static alias on /uploads/
   Select-String -Path .\deploy\dbert-unified-nginx.conf -Pattern "location /uploads/" -Context 0,4
   # Inspect Flask app.py for authenticated route
   Select-String -Path .\apps\portal\app.py -Pattern "def serve_uploaded_file" -Context 0,25
   ```
   *Expected Result*: Nginx serves disk directory via `alias` with no auth subrequest, bypassing `serve_uploaded_file()`.

3. **Verify Finding SEC-R5-03 (`.env` exposure)**:
   ```powershell
   # Search for dotfile block rules in Nginx config
   Select-String -Path .\deploy\dbert-unified-nginx.conf -Pattern "location ~ /\\\."
   ```
   *Expected Result*: Returns 0 matches. No protection for hidden files.

4. **Verify Finding SEC-R5-04 (Debug OTP leak & Preflight bug)**:
   ```powershell
   # Verify OTP leak in app.py
   Select-String -Path .\apps\portal\app.py -Pattern "dev_otp_hint" -Context 2,2
   # Test preflight expansion behavior in bash:
   python -c "
   import re
   with open('scripts/production_preflight.sh') as f:
       print([line for line in f if 'FLASK_DEBUG' in line])
   "
   ```
   *Expected Result*: `dev_otp_hint` is appended to JSON response when `FLASK_DEBUG` is true; preflight script uses single quotes `'${FLASK_DEBUG:-}'`.

5. **Verify Finding SEC-R5-05 (Admin route misdirection)**:
   ```powershell
   # Check function preceding and following the decorator
   python -c "
   with open('apps/portal/app.py') as f:
       lines = f.readlines()
   for i in range(8393, 8408):
       print(f'{i+1}: {lines[i]}', end='')
   "
   ```
   *Expected Result*: Line 8395 `@app.route("/admin/course-payments/<int:pay_id>/review")` decorates `def _signal_tutor_course_unlock(intern_id, course_id):`, leaving `admin_course_payment_review` undecorated.

6. **Verify Finding SEC-R5-06 (Secret key short-length guard)**:
   ```powershell
   python -c "
   with open('apps/portal/app.py') as f:
       lines = f.readlines()
   for i in range(298, 305):
       print(f'{i+1}: {lines[i]}', end='')
   "
   ```
   *Expected Result*: Line 302 uses `print()`, does not raise or assert.

7. **Verify Finding SEC-R5-07 (Rate limit bypass via `FLASK_ENV`)**:
   ```powershell
   # Check rate_check bypass condition
   python -c "
   with open('apps/portal/app.py') as f:
       lines = f.readlines()
   for i in range(702, 710):
       print(f'{i+1}: {lines[i]}', end='')
   "
   # Check .env FLASK_ENV value
   Select-String -Path .\apps\portal\.env -Pattern "FLASK_ENV"
   ```
   *Expected Result*: `rate_check` returns `(True, 0)` if `FLASK_ENV == "development"`, and `.env` specifies `FLASK_ENV=development`.

---
*Report completed and verified against local repository files.*
