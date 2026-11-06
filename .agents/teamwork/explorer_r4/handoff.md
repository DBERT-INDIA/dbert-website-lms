# Deployment Configuration Audit Report (Requirement R4)

**Auditor:** `explorer_r4` (Deployment Configuration Auditor)  
**Date:** 2026-10-25  
**Scope:** EC2 Deployment configurations under `deploy/`, systemd service units, `scripts/production_preflight.sh`, and port allocation safety.

---

## Executive Summary

| Category | Blocker | Warning | Info | Total |
| :--- | :---: | :---: | :---: | :---: |
| 1. Nginx Unified Config (`dbert-unified-nginx.conf`) | 2 | 3 | 1 | 6 |
| 2. Systemd Service Files | 0 | 2 | 2 | 4 |
| 3. Deployment Script (`deploy_ec2_unified.sh` & legacy) | 2 | 2 | 1 | 5 |
| 4. Preflight Script Expansion Bug (`production_preflight.sh`) | 7 | 1 | 0 | 8 |
| 5. Port Allocation & Binding Safety (:3001, :5001) | 0 | 1 | 2 | 3 |
| **Total Findings** | **11** | **9** | **6** | **26** |

---

## Section 1: Detailed Findings Catalog

### 1. Nginx Unified Configuration (`deploy/dbert-unified-nginx.conf`)

#### Finding 1.1: Missing Legacy Domains in SSL Certificate Path for 301 Redirect Blocks
- **File & Lines:** `deploy/dbert-unified-nginx.conf:30-31`, `deploy/dbert-unified-nginx.conf:42-43`
- **Classification:** **Blocker**
- **Observation:**
  ```nginx
  28:     server_name dbert.online www.dbert.online;
  29: 
  30:     ssl_certificate /etc/letsencrypt/live/dbert.in/fullchain.pem;
  31:     ssl_certificate_key /etc/letsencrypt/live/dbert.in/privkey.pem;
  32: 
  33:     return 301 https://dbert.in$request_uri;
  ...
  40:     server_name internship.dbert.online;
  41: 
  42:     ssl_certificate /etc/letsencrypt/live/dbert.in/fullchain.pem;
  43:     ssl_certificate_key /etc/letsencrypt/live/dbert.in/privkey.pem;
  44: 
  45:     return 301 https://lms.dbert.in$request_uri;
  ```
- **Explanation:**
  The 301 redirect blocks for legacy HTTPS traffic (`dbert.online`, `www.dbert.online`, and `internship.dbert.online`) point to `/etc/letsencrypt/live/dbert.in/fullchain.pem`. In `deploy/deploy_ec2_unified.sh:186`, certbot is instructed to request certificates only for `dbert.in`, `www.dbert.in`, and `lms.dbert.in`. Because the certificate SAN (Subject Alternative Names) lacks `dbert.online`, `www.dbert.online`, and `internship.dbert.online`, any client connecting over HTTPS to the legacy domains will abort with `SSL_ERROR_BAD_CERT_DOMAIN` / `NET::ERR_CERT_COMMON_NAME_INVALID` during the TLS handshake before the HTTP 301 redirect header is ever received.
- **Recommended Fix:**
  1. If DNS for the legacy domains points to this EC2 server, expand the Certbot certificate request to include legacy domains in the SAN:
     ```bash
     sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online
     ```
  2. If legacy domains maintain separate certificates, configure separate certificate paths (e.g. `/etc/letsencrypt/live/dbert.online/fullchain.pem`).
  3. Ensure Port 80 HTTP traffic redirects directly to `https://dbert.in` without bouncing through legacy HTTPS (see Finding 1.2).

---

#### Finding 1.2: Suboptimal Two-Hop / SSL-Failing Port 80 HTTP Redirection for Legacy Domains
- **File & Lines:** `deploy/dbert-unified-nginx.conf:8-21`
- **Classification:** **Warning**
- **Observation:**
  ```nginx
  8:  server {
  9:      listen 80;
  10:     listen [::]:80;
  11:     server_name dbert.in www.dbert.in lms.dbert.in dbert.online www.dbert.online internship.dbert.online;
  ...
  18:     location / {
  19:         return 301 https://$host$request_uri;
  20:     }
  21: }
  ```
- **Explanation:**
  When a user or search bot accesses `http://dbert.online/page`, line 19 redirects to `https://dbert.online/page` (`$host` preserves the requested hostname). The client then connects to `https://dbert.online/page`, triggering an unnecessary 2-hop redirect chain (`http://dbert.online` $\rightarrow$ `https://dbert.online` $\rightarrow$ `https://dbert.in`). If `dbert.online` lacks a valid SSL certificate (per Finding 1.1), the request fails on the second hop instead of cleanly landing on `https://dbert.in`.
- **Recommended Fix:**
  Split port 80 redirection so legacy domains redirect directly to the new destination in 1 hop:
  ```nginx
  # Legacy domain HTTP redirects (1-hop to new HTTPS target)
  server {
      listen 80;
      listen [::]:80;
      server_name dbert.online www.dbert.online;
      location /.well-known/acme-challenge/ { root /var/www/certbot; }
      location / { return 301 https://dbert.in$request_uri; }
  }

  server {
      listen 80;
      listen [::]:80;
      server_name internship.dbert.online;
      location /.well-known/acme-challenge/ { root /var/www/certbot; }
      location / { return 301 https://lms.dbert.in$request_uri; }
  }

  # Production domain HTTP -> HTTPS redirect
  server {
      listen 80;
      listen [::]:80;
      server_name dbert.in www.dbert.in lms.dbert.in;
      location /.well-known/acme-challenge/ { root /var/www/certbot; }
      location / { return 301 https://$host$request_uri; }
  }
  ```

---

#### Finding 1.3: Unrestricted Public Disk Serving and Missing Security Headers on `/uploads/`
- **File & Lines:** `deploy/dbert-unified-nginx.conf:126-130`
- **Classification:** **Blocker**
- **Observation:**
  ```nginx
  126:     # Uploads (CVs, Resumes, Project Artifacts)
  127:     location /uploads/ {
  128:         alias /var/www/dbert-website-lms/apps/portal/uploads/;
  129:         expires 30d;
  130:         access_log off;
  131:     }
  ```
- **Explanation:**
  `apps/portal/uploads/` holds sensitive candidate CVs, resumes, certificates, and student artifacts.
  1. The unified config maps this directly to public disk without any authentication check.
  2. Unlike the standalone `deploy/dbert-portal-nginx.conf:48-58`, which enforced `types { image/png png; image/jpeg jpg jpeg; application/pdf pdf; } default_type application/octet-stream;` and `add_header Content-Disposition "attachment"`, `dbert-unified-nginx.conf` omits all MIME restrictions and download headers.
  3. If a student or attacker uploads an HTML file, SVG with inline scripts, or executable script, Nginx will serve it directly under `https://lms.dbert.in/uploads/`, permitting Stored Cross-Site Scripting (XSS), cookie theft, and CORS bypass.
- **Recommended Fix:**
  Add strict MIME typing, nosniff, and force download attachments:
  ```nginx
  location /uploads/ {
      alias /var/www/dbert-website-lms/apps/portal/uploads/;
      add_header Content-Disposition "attachment" always;
      add_header X-Content-Type-Options "nosniff" always;
      types {
          image/png png;
          image/jpeg jpg jpeg;
          application/pdf pdf;
      }
      default_type application/octet-stream;
      expires 30d;
      access_log off;
  }
  ```

---

#### Finding 1.4: Missing `X-Forwarded-Host` on Flask LMS Reverse Proxy
- **File & Lines:** `deploy/dbert-unified-nginx.conf:133-141`
- **Classification:** **Warning**
- **Observation:**
  ```nginx
  133:     location / {
  134:         proxy_pass http://127.0.0.1:5001;
  135:         proxy_http_version 1.1;
  136:         proxy_set_header Host $host;
  137:         proxy_set_header X-Real-IP $remote_addr;
  138:         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  139:         proxy_set_header X-Forwarded-Proto $scheme;
  140:         proxy_read_timeout 90;
  141:     }
  ```
- **Explanation:**
  Section 3 (Next.js, line 88) passes `proxy_set_header X-Forwarded-Host $host;`. Section 4 (LMS platform, lines 136-140) omits `X-Forwarded-Host`. When Werkzeug `ProxyFix(app, x_for=1, x_proto=1, x_host=1)` runs in Flask, it relies on `X-Forwarded-Host` to reconstruct canonical URL generation (e.g. `url_for(..., _external=True)`) and redirection.
- **Recommended Fix:**
  Add `proxy_set_header X-Forwarded-Host $host;` to `location /` under `lms.dbert.in`.

---

#### Finding 1.5: Missing Nginx Protection for Sensitive Files (`.env`, `*.db`, `.git`)
- **File & Lines:** `deploy/dbert-unified-nginx.conf:49-142`
- **Classification:** **Warning**
- **Observation:**
  Neither Section 3 (`dbert.in`) nor Section 4 (`lms.dbert.in`) contains location blocks denying hidden files or database files.
- **Explanation:**
  If an administrator places backup files (`internship.db`, `.env`, schema dumps) in `static/` or if static routing expands, Nginx does not proactively deny access to dotfiles or sqlite/database files.
- **Recommended Fix:**
  Add explicit global deny blocks within both server blocks:
  ```nginx
  location ~ /\.(?!well-known) {
      deny all;
      return 404;
  }
  location ~* \.(sqlite|db|env|log|sql|bak)$ {
      deny all;
      return 404;
  }
  ```

---

#### Finding 1.6: Server Name, SSL Paths, and Upstream URLs Validation
- **File & Lines:** `deploy/dbert-unified-nginx.conf:11,28,40,52,54-55,80,97,99-100,134`
- **Classification:** **Info**
- **Observation:**
  - `server_name` lines correctly cover `dbert.in`, `www.dbert.in`, `lms.dbert.in`.
  - Next.js upstream is `http://127.0.0.1:3001` (matches `dbert-website.service:10`).
  - LMS Gunicorn upstream is `http://127.0.0.1:5001` (matches `dbert-portal.service:10`).
  - Next.js static alias `/var/www/dbert-website-lms/apps/website/.next/static/` matches standalone build structure.
  - Portal static alias `/var/www/dbert-website-lms/apps/portal/static/` matches repo structure.
- **Explanation:**
  All server names, SSL paths for `dbert.in`, and upstream ports are aligned for production operation.

---

### 2. Systemd Service Files Audit

#### Finding 2.1: `deploy/dbert-portal.service` Verified Correct
- **File & Lines:** `deploy/dbert-portal.service:1-18`
- **Classification:** **Info**
- **Observation:**
  ```ini
  [Service]
  User=ubuntu
  Group=ubuntu
  WorkingDirectory=/var/www/dbert-website-lms/apps/portal
  EnvironmentFile=/var/www/dbert-website-lms/apps/portal/.env
  ExecStart=/var/www/dbert-website-lms/apps/portal/.venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5001 --timeout 90 wsgi:app
  ```
- **Explanation:**
  Paths strictly match `/var/www/dbert-website-lms/`, user/group is standard EC2 `ubuntu:ubuntu`, entrypoint `wsgi:app` is verified present in `apps/portal/wsgi.py`, and bind port `5001` matches unified Nginx proxy pass.

---

#### Finding 2.2: `deploy/dbert-website.service` Hostname `0.0.0.0` Bypasses Nginx Reverse Proxy
- **File & Lines:** `deploy/dbert-website.service:11`
- **Classification:** **Warning**
- **Observation:**
  ```ini
  9:  Environment="NODE_ENV=production"
  10: Environment="PORT=3001"
  11: Environment="HOSTNAME=0.0.0.0"
  12: Environment="NEXT_PUBLIC_SITE_URL=https://dbert.in"
  13: Environment="NEXT_PUBLIC_LMS_URL=https://lms.dbert.in"
  14: 
  15: ExecStart=/usr/bin/node .next/standalone/server.js
  ```
- **Explanation:**
  Setting `HOSTNAME=0.0.0.0` causes the Next.js standalone Node process to listen on all network interfaces. If port 3001 is opened or reachable in the EC2 security group, clients can connect directly to port 3001 over unencrypted HTTP, evading Nginx SSL termination, Gzip, and HTTP security headers (`X-Frame-Options`, `X-Content-Type-Options`).
- **Recommended Fix:**
  Change line 11 to `Environment="HOSTNAME=127.0.0.1"` so Next.js listens only on the local loopback interface.

---

#### Finding 2.3: `deploy/dbert-website.service` Verified Domains & Layout
- **File & Lines:** `deploy/dbert-website.service:8,12,13`
- **Classification:** **Info**
- **Observation:**
  `WorkingDirectory=/var/www/dbert-website-lms/apps/website`, `NEXT_PUBLIC_SITE_URL=https://dbert.in`, `NEXT_PUBLIC_LMS_URL=https://lms.dbert.in`.
- **Explanation:**
  No legacy `dbert.online` references; domains and EC2 working directory match requirements.

---

#### Finding 2.4: Obsolete Legacy Service Unit `apps/portal/deploy/internship.service`
- **File & Lines:** `apps/portal/deploy/internship.service:6-18`
- **Classification:** **Warning**
- **Observation:**
  `User=www-data`, `WorkingDirectory=/var/www/apps/internship`, `ExecStart=... --bind 127.0.0.1:5000 wsgi:app`.
- **Explanation:**
  This legacy file contains obsolete paths (`/var/www/apps/internship`), wrong user (`www-data`), and wrong port (`5000`). If copied by an operator, it breaks systemd startup.
- **Recommended Fix:**
  Remove or mark `apps/portal/deploy/internship.service` as deprecated.

---

### 3. Deploy Script Audit (`deploy/deploy_ec2_unified.sh` & legacy)

#### Finding 3.1: Hardcoded Committed Plaintext Database Password `DBERT_SECURE_PASSWORD_123`
- **File & Lines:** `deploy/deploy_ec2_unified.sh:56, 110`
- **Classification:** **Blocker** (Pre-confirmed finding #6)
- **Observation:**
  ```bash
  56:  DB_PASS="DBERT_SECURE_PASSWORD_123"
  ...
  110: DATABASE_URL=postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms
  111: JWT_SECRET=production_placeholder_secret_2026
  ```
- **Explanation:**
  Committed plaintext passwords in version-controlled scripts expose PostgreSQL credentials to any repository reader. Furthermore:
  - If PostgreSQL was already created with another password, `psql` schema loading will fail.
  - Line 111 commits a hardcoded `JWT_SECRET=production_placeholder_secret_2026`.
  - The same password is hardcoded in `deploy/FIRST_TIME_EC2_DEPLOYMENT.md:45,56,68`, `apps/portal/.env.production.sample:21`, and five portal test scripts (`apps/portal/scripts/check_counts.py:6`, `check_aaditya_pg.py:6`, `test_pg_query.py:7`, `test_attendance_migration.py:9`, `check_pg.py:5`).
- **Recommended Fix:**
  Extract or generate the database password dynamically in `deploy_ec2_unified.sh`:
  ```bash
  # Check if password already exists in apps/portal/.env
  if [ -f "$PORTAL_DIR/.env" ]; then
      DB_PASS=$(grep -E '^DATABASE_URL=' "$PORTAL_DIR/.env" | sed -E 's/.*:[^:]*:(.*)@.*/\1/' || true)
  fi
  # Otherwise generate a cryptographically strong random password
  if [ -z "${DB_PASS:-}" ]; then
      DB_PASS="${DB_PASSWORD:-$(openssl rand -hex 24)}"
  fi
  JWT_SEC="${JWT_SECRET:-$(openssl rand -hex 32)}"
  ```
  Inject `$DB_PASS` and `$JWT_SEC` when generating `.env` for `apps/website` and `apps/portal`.
  Rotate all database credentials in production.

---

#### Finding 3.2: Certbot Command SAN Coverage vs Nginx Configuration Mismatch
- **File & Lines:** `deploy/deploy_ec2_unified.sh:186`
- **Classification:** **Warning**
- **Observation:**
  ```bash
  185: echo "Next Step: Obtain production SSL certificates via Certbot:"
  186: echo "  sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in"
  ```
- **Explanation:**
  The printed certbot command covers all 3 production domains (`dbert.in`, `www.dbert.in`, `lms.dbert.in`). However, `deploy/dbert-unified-nginx.conf` also configures HTTPS redirect blocks for `dbert.online`, `www.dbert.online`, and `internship.dbert.online` that point to the same certbot certificate. Without including legacy domains in the certbot command, legacy HTTPS traffic fails with TLS certificate validation errors.
- **Recommended Fix:**
  If legacy DNS points to this EC2 server, update the printed instruction:
  ```bash
  echo "  sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online"
  ```

---

#### Finding 3.3: `deploy/deploy_ec2.sh` Copies Obsolete Single-App Nginx Config
- **File & Lines:** `deploy/deploy_ec2.sh:72`
- **Classification:** **Blocker**
- **Observation:**
  ```bash
  71: echo "[*] Installing nginx config..."
  72: sudo cp "$REPO_DIR/deploy/dbert-portal-nginx.conf" /etc/nginx/conf.d/dbert-portal.conf
  73: sudo nginx -t
  ```
- **Explanation:**
  `deploy/deploy_ec2.sh` installs `dbert-portal-nginx.conf`, which routes only to `internship.dbert.online` on port 5001 and completely omits `dbert.in` and `lms.dbert.in`. If an operator runs `deploy_ec2.sh`, it overrides Nginx configuration and breaks website and portal routing.
- **Recommended Fix:**
  Replace line 72 with the unified configuration or redirect `deploy_ec2.sh` to call `deploy_ec2_unified.sh`.

---

#### Finding 3.4: `internship.db` Left in `apps/portal/` After PostgreSQL Migration
- **File & Lines:** `deploy/deploy_ec2_unified.sh:90-95`
- **Classification:** **Warning**
- **Observation:**
  ```bash
  90: # Migrate data from SQLite to PostgreSQL if internship.db exists
  91: if [ -f "internship.db" ]; then
  92:     echo "[*] Migrating existing database records (including 6,622 scraped leads) from SQLite to PostgreSQL..."
  93:     PG_URL="postgresql://dbert_user:${DB_PASS}@localhost:5432/dbert_lms"
  94:     python scripts/migrate_sqlite_to_postgres_data.py --sqlite internship.db --pg-url "$PG_URL" || true
  95: fi
  ```
- **Explanation:**
  After data is migrated, `internship.db` remains in `apps/portal/`. If `REQUIRE_POSTGRES=true` fails or is not parsed, Flask could silently fall back to `internship.db`. Moreover, `scripts/production_preflight.sh:67` checks that `internship.db` does NOT exist.
- **Recommended Fix:**
  Add a step to archive and remove `internship.db` upon successful migration:
  ```bash
  mv internship.db "$BACKUP_DIR/internship_migrated_${TIMESTAMP}.db"
  ```

---

### 4. `production_preflight.sh` Variable Expansion Bug Audit

In bash, single quotes (`'...'`) completely disable parameter expansion. When enclosed in single quotes inside command substitutions `$( ... )`, the expression is treated as a literal string.

```bash
50: if [ -f "$PORTAL_DIR/.env" ]; then
51:     source "$PORTAL_DIR/.env" 2>/dev/null || true
52: 
53:     check "REQUIRE_POSTGRES=true" "$([ '${REQUIRE_POSTGRES:-}' = 'true' ] && echo ok || echo "REQUIRE_POSTGRES=${REQUIRE_POSTGRES:-unset}")"
54:     check "DATABASE_URL is postgres" "$(echo '${DATABASE_URL:-}' | grep -qE '^postgres(ql)?://' && echo ok || echo 'DATABASE_URL missing or not postgres')"
55:     check "POSTGRES_SCHEMA set" "$([ -n '${POSTGRES_SCHEMA:-}' ] && echo ok || echo 'POSTGRES_SCHEMA not set')"
56:     check "FLASK_SECRET_KEY set" "$([ -n '${FLASK_SECRET_KEY:-}' ] && echo ok || echo 'FLASK_SECRET_KEY not set')"
57:     check "FLASK_DEBUG=false" "$([ '${FLASK_DEBUG:-}' != 'true' ] && echo ok || echo 'FLASK_DEBUG is true in production!')"
58: 
59:     # Check no hardcoded default key
60:     if echo '${FLASK_SECRET_KEY:-}' | grep -qi 'digitalblinc\|default\|changeme'; then
61:         echo "[ERROR] FLASK_SECRET_KEY looks like a default value"
62:         ERRORS=$((ERRORS+1))
63:     fi
64: fi
```

#### Finding 4.1: Line 53 — `${REQUIRE_POSTGRES:-}` Single Quoted
- **File & Line:** `scripts/production_preflight.sh:53`
- **Classification:** **Blocker**
- **Evaluation:** `[ '${REQUIRE_POSTGRES:-}' = 'true' ]` tests if literal 20-character string `"${REQUIRE_POSTGRES:-}"` equals `"true"`.
- **Impact:** Always evaluates to FALSE. The check **ALWAYS FAILS**, even when `REQUIRE_POSTGRES=true` is set.
- **Fix:** Replace with `[ "${REQUIRE_POSTGRES:-}" = "true" ]`.

---

#### Finding 4.2: Line 54 — `${DATABASE_URL:-}` Single Quoted
- **File & Line:** `scripts/production_preflight.sh:54`
- **Classification:** **Blocker**
- **Evaluation:** `echo '${DATABASE_URL:-}'` sends literal string `${DATABASE_URL:-}` to grep for `^postgres(ql)?://`.
- **Impact:** Always evaluates to FALSE. The check **ALWAYS FAILS**, even when a valid PostgreSQL URL is present in `.env`.
- **Fix:** Replace with `echo "${DATABASE_URL:-}" | grep -qE '^postgres(ql)?://'`.

---

#### Finding 4.3: Line 55 — `${POSTGRES_SCHEMA:-}` Single Quoted
- **File & Line:** `scripts/production_preflight.sh:55`
- **Classification:** **Blocker**
- **Evaluation:** `[ -n '${POSTGRES_SCHEMA:-}' ]` tests if literal string `${POSTGRES_SCHEMA:-}` (19 chars) is non-empty.
- **Impact:** Always evaluates to TRUE. The check **SILENTLY PASSES**, even if `POSTGRES_SCHEMA` is empty or missing from `.env`.
- **Fix:** Replace with `[ -n "${POSTGRES_SCHEMA:-}" ]`.

---

#### Finding 4.4: Line 56 — `${FLASK_SECRET_KEY:-}` Single Quoted
- **File & Line:** `scripts/production_preflight.sh:56`
- **Classification:** **Blocker**
- **Evaluation:** `[ -n '${FLASK_SECRET_KEY:-}' ]` tests if literal string `${FLASK_SECRET_KEY:-}` (20 chars) is non-empty.
- **Impact:** Always evaluates to TRUE. The check **SILENTLY PASSES**, even if `FLASK_SECRET_KEY` is empty or missing from `.env`.
- **Fix:** Replace with `[ -n "${FLASK_SECRET_KEY:-}" ]`.

---

#### Finding 4.5: Line 57 — `${FLASK_DEBUG:-}` Single Quoted
- **File & Line:** `scripts/production_preflight.sh:57`
- **Classification:** **Blocker**
- **Evaluation:** `[ '${FLASK_DEBUG:-}' != 'true' ]` tests if literal string `${FLASK_DEBUG:-}` is not equal to `'true'`.
- **Impact:** Always evaluates to TRUE. The check **SILENTLY PASSES**, even if `FLASK_DEBUG=true` in `.env` (exposing interactive debug console in production).
- **Fix:** Replace with `[ "${FLASK_DEBUG:-}" != "true" ]`.

---

#### Finding 4.6: Line 60 — Default Key Check Echoes Literal Single-Quoted Variable
- **File & Line:** `scripts/production_preflight.sh:60`
- **Classification:** **Blocker**
- **Evaluation:** `echo '${FLASK_SECRET_KEY:-}' | grep -qi 'digitalblinc\|default\|changeme'` greps the literal variable syntax string.
- **Impact:** Guard **NEVER TRIGGERS**. Default and insecure keys slip into production without detection.
- **Fix:** Replace with `echo "${FLASK_SECRET_KEY:-}" | grep -qiE 'digitalblinc|default|changeme'`.

---

#### Finding 4.7: Line 73 — Stale Nginx Configuration Path Check
- **File & Line:** `scripts/production_preflight.sh:73`
- **Classification:** **Blocker**
- **Observation:**
  ```bash
  73: check "nginx config installed" "$([ -f /etc/nginx/conf.d/dbert-portal.conf ] && echo ok || echo 'Nginx config not installed')"
  ```
- **Evaluation:** Preflight looks for `/etc/nginx/conf.d/dbert-portal.conf`. The unified deployment installs `/etc/nginx/sites-available/dbert-unified.conf` (enabled via `/etc/nginx/sites-enabled/dbert-unified.conf`).
- **Impact:** Check **ALWAYS FAILS** on unified EC2 servers.
- **Fix:** Check for `dbert-unified.conf` across both `sites-enabled` and `conf.d`.

---

#### Finding 4.8: Line 67 — Checks Portal Dir But Omits Root `internship.db`
- **File & Line:** `scripts/production_preflight.sh:67`
- **Classification:** **Warning**
- **Observation:** `check "No internship.db in portal dir" "$([ ! -f $PORTAL_DIR/internship.db ] && echo ok || echo 'internship.db exists — check REQUIRE_POSTGRES')"`
- **Evaluation:** Only checks `$PORTAL_DIR/internship.db`. In this repository, `internship.db` also resides at `/var/www/dbert-website-lms/internship.db`.
- **Fix:** Check both locations: `[ ! -f "$PORTAL_DIR/internship.db" ] && [ ! -f "/var/www/dbert-website-lms/internship.db" ]`.

---

### 5. Port Allocation & Binding Safety Audit

#### Finding 5.1: Next.js Port 3001 Allocation Confirmed Safe
- **File & Lines:** `deploy/dbert-unified-nginx.conf:80`, `deploy/dbert-website.service:10`, `deploy/deploy_ec2_unified.sh:108`
- **Classification:** **Info**
- **Analysis:**
  - Standard Ubuntu Linux daemons do not use port 3001 (systemd, ssh, postfix, postgresql, nginx all avoid 3000-3999).
  - Port 3000 is often claimed by Grafana or dev processes. Shifting Next.js to 3001 eliminates potential port collisions.
  - Port 3001 is completely safe.

---

#### Finding 5.2: Gunicorn Port 5001 Allocation Confirmed Safe
- **File & Lines:** `deploy/dbert-unified-nginx.conf:134`, `deploy/dbert-portal.service:10`, `deploy/deploy_ec2_unified.sh:174`
- **Classification:** **Info**
- **Analysis:**
  - Standard Flask port is 5000. Port 5000 is frequently claimed by macOS AirPlay Receiver or Docker Registry.
  - Moving Gunicorn to 5001 eliminates conflicts.
  - Port 5001 has no conflicting Ubuntu system services.
  - Gunicorn explicitly binds to `127.0.0.1:5001`, preventing external direct access.

---

#### Finding 5.3: Discrepant Port Numbers in Legacy Guides and Units
- **File & Lines:** `deploy/FIRST_TIME_EC2_DEPLOYMENT.md:93,112`, `apps/portal/deploy/internship.service:14`, `apps/portal/deploy/deploy_ec2.sh:72-73`, `apps/portal/wsgi.py:4-5`
- **Classification:** **Warning**
- **Analysis:**
  Legacy documentation and old helper scripts instruct binding to ports `5000` and `3000`. Following those legacy instructions while using `dbert-unified-nginx.conf` (which reverse proxies to 3001 and 5001) will cause Nginx `502 Bad Gateway` errors.
- **Recommended Fix:**
  Update all legacy docs, comments, and scripts to reference ports 3001 and 5001.

---

## Section 2: Logic Chain

1. **Premise 1 (Nginx Unified Config & SSL):**
   - Direct observation of `deploy/dbert-unified-nginx.conf:30,42` shows that legacy HTTPS 301 redirects rely on `/etc/letsencrypt/live/dbert.in/fullchain.pem`.
   - Direct observation of `deploy/deploy_ec2_unified.sh:186` shows certbot requests SAN only for `dbert.in`, `www.dbert.in`, and `lms.dbert.in`.
   - Therefore, any HTTPS request to `https://dbert.online` or `https://internship.dbert.online` fails during TLS handshake before Nginx can issue the HTTP 301 redirect.

2. **Premise 2 (Uploads Directory Exposure):**
   - Direct observation of `deploy/dbert-unified-nginx.conf:126-130` shows an unauthenticated alias directly to `/apps/portal/uploads/` without MIME type enforcement or attachment headers.
   - Any uploaded file can be fetched by anyone over the web and SVG/HTML can execute scripts in the LMS domain context.

3. **Premise 3 (Plaintext DB Password):**
   - Direct observation of `deploy/deploy_ec2_unified.sh:56,110` confirms `DB_PASS="DBERT_SECURE_PASSWORD_123"` and `DATABASE_URL=postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms`.
   - This hardcoded password is in version control and creates database users and `.env` files with known default credentials.

4. **Premise 4 (Preflight Shell Expansion):**
   - Direct observation of `scripts/production_preflight.sh:53-60` shows variable names inside single quotes: `'${REQUIRE_POSTGRES:-}'`, `'${DATABASE_URL:-}'`, `'${POSTGRES_SCHEMA:-}'`, `'${FLASK_SECRET_KEY:-}'`, `'${FLASK_DEBUG:-}'`.
   - In shell evaluation, single quotes suppress variable expansion.
   - For string equality tests against `"true"` or regex match against `^postgres`, the checks test the literal string and always fail.
   - For non-empty tests (`[ -n '...' ]`) and inequality tests (`[ '...' != 'true' ]`), the checks test the non-empty literal string and always pass, silently bypassing security checks.

5. **Premise 5 (Port Allocation):**
   - Direct observation of `dbert-website.service:10` (`PORT=3001`) and `dbert-portal.service:10` (`bind 127.0.0.1:5001`) matches `dbert-unified-nginx.conf:80,134`.
   - These ports do not collide with standard Ubuntu services.

---

## Section 3: Caveats

1. **No Live EC2 Environment:** Findings are derived entirely from static code analysis of repository scripts, configuration files, and documentation. No active network probes were executed against a live EC2 server.
2. **DNS State Unknown:** The audit cannot verify whether DNS A/CNAME records for `dbert.online` or `internship.dbert.online` are currently pointed to the EC2 IP. If DNS for legacy domains is not pointed to this server, Certbot cannot issue certificates for them.
3. **Stand-alone Build Prerequisites:** Next.js standalone server execution in `dbert-website.service` assumes `npm run build` has succeeded with `output: 'standalone'` in `next.config.js`.

---

## Section 4: Conclusion

The deployment configuration under `deploy/` is well-structured for the unified ecosystem (`dbert.in` on port 3001 and `lms.dbert.in` on port 5001), but contains **four critical deployment blockers**:
1. **Committed DB Password:** `DBERT_SECURE_PASSWORD_123` hardcoded in `deploy/deploy_ec2_unified.sh`.
2. **Preflight Script Failure:** Single-quoted variable expansion bugs in `scripts/production_preflight.sh` cause false failures on valid postgres configs and silent passes on missing secret keys and debug mode.
3. **SSL Redirection Dead End:** `deploy/dbert-unified-nginx.conf` references a single certificate for legacy HTTPS redirects without including them in Certbot SAN, resulting in browser SSL errors.
4. **Unrestricted Uploads Exposure:** Public direct disk serving of `apps/portal/uploads/` without MIME restrictions or download attachment enforcement.

All four blockers must be remediated prior to production go-live.

---

## Section 5: Verification Method

To independently verify these findings:

1. **Verify Hardcoded DB Password:**
   ```bash
   grep -n "DBERT_SECURE_PASSWORD_123" deploy/deploy_ec2_unified.sh
   # Expected output: lines 56 and 110
   ```

2. **Verify Preflight Single-Quote Bug:**
   ```bash
   sed -n '50,65p' scripts/production_preflight.sh
   # Observe literal single quotes enclosing '${...}' variables on lines 53, 54, 55, 56, 57, 60.
   ```
   Execute reproduction in bash:
   ```bash
   bash -c "REQUIRE_POSTGRES=true; [ '\${REQUIRE_POSTGRES:-}' = 'true' ] && echo PASS || echo FAIL"
   # Output: FAIL (demonstrates the exact bug)
   ```

3. **Verify Nginx SSL Paths and Redirect Blocks:**
   ```bash
   grep -n -E "ssl_certificate|server_name|proxy_pass" deploy/dbert-unified-nginx.conf
   ```

4. **Verify Systemd Service Ports and Layout:**
   ```bash
   grep -n -E "WorkingDirectory|ExecStart|Environment" deploy/dbert-portal.service deploy/dbert-website.service
   ```

5. **Verify Uploads Block in Nginx:**
   ```bash
   sed -n '125,132p' deploy/dbert-unified-nginx.conf
   ```
