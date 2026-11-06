# Consolidated Findings Catalog: DBERT QA Audit

**Date:** 2026-10-25 / 2026-10-26  
**Compiled by:** Orchestrator (`orchestrator_1`)  
**Sources:** `explorer_r1`, `explorer_r2`, `explorer_r3`, `explorer_r4`, `explorer_r5`

---

## 1. Pre-Confirmed Blockers & Warnings (Verified)

| # | Finding ID | Severity | File & Line | Summary Description | Recommended Fix |
|---|---|---|---|---|---|
| 1 | PRE-01 | **Blocker** | `apps/portal/.env:27` | `SMTP_HOST=dbert.online` sends production emails to legacy host | Update to `SMTP_HOST=dbert.in` |
| 2 | PRE-02 | **Blocker** | `apps/portal/.env:29` | `SMTP_USER=contactus@dbert.online` uses legacy SMTP username | Update to `SMTP_USER=contactus@dbert.in` |
| 3 | PRE-03 | **Blocker** | `apps/portal/.env:31` | `FROM_EMAIL=contactus@dbert.online` causes replies/SPF to fail on legacy domain | Update to `FROM_EMAIL=contactus@dbert.in` |
| 4 | PRE-04 | **Blocker** | `apps/portal/app.py:304` | `SMTP_HOST = os.environ.get("SMTP_HOST", "dbert.online")` fallback default is legacy domain | Change fallback default to `"dbert.in"` |
| 5 | PRE-05 | **Blocker** | `apps/portal/app.py:2690` | `staff_email = f"{ADMIN_USERNAME}@dbert.online"` hardcoded staff admin email | Change to `f"{ADMIN_USERNAME}@dbert.in"` |
| 6 | PRE-06 | **Blocker** | `deploy/deploy_ec2_unified.sh:56, 110` | `DBERT_SECURE_PASSWORD_123` hardcoded database password in deployment script | Dynamically generate with `openssl rand -hex 24` or read from `.env` |
| 7 | PRE-07 | **Blocker** | `cpanel_public_html/__next.__PAGE__.txt:49`<br>`apps/website/__next.__PAGE__.txt:49` | JSON-LD schema `@type: Organization` has `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, and `"email": "contactus@dbert.online"` | Re-export static bundle from source where `metadataBase` is `https://dbert.in` |
| 8 | PRE-08 | **Warning** | `apps/portal/templates/seo_landing.html:133` | Anchor tag `href="https://dbert.in"` but link text displays `dbert.online` | Change link text from `dbert.online` to `dbert.in` |

---

## 2. Requirement R1: Domain Migration Completeness (`dbert.online` -> `dbert.in`)

| Finding ID | Severity | File & Line | Summary Description | Recommended Fix |
|---|---|---|---|---|
| R1-01 | **Blocker** | `apps/portal/sitemap.xml:1` | 85+ canonical `<loc>` tags point to `https://internship.dbert.online/...` | Bulk replace `https://internship.dbert.online` with `https://lms.dbert.in` |
| R1-02 | **Blocker** | `apps/website/sitemap.xml:4-420` | All 70 `<loc>` URLs point to `https://dbert.online/...` | Overwrite with `cpanel_public_html/sitemap.xml` using `dbert.in` |
| R1-03 | **Blocker** | `apps/website/robots.txt:13` | `Sitemap: https://dbert.online/sitemap.xml` directs crawlers to legacy domain | Change to `Sitemap: https://dbert.in/sitemap.xml` |
| R1-04 | **Blocker** | `cpanel_public_html/*` (all 110 HTML files) | 157 outbound link instances in Header/Footer link to `https://internship.dbert.online/` due to un-rebuilt Next.js export | Re-export static build (`npm run export:cpanel`) from updated source code |
| R1-05 | **Blocker** | `apps/website/out/` (203 static files) | Static export files contain `og:image`, `twitter:image`, and Organization schema on `dbert.online` | Re-export static website from `apps/website/src/` |
| R1-06 | **Blocker** | `dbert-api-package/.env.production.sample:18` | `CORS_ORIGINS=https://dbert.online,https://internship.dbert.online` blocks API requests from `dbert.in` | Update to `https://dbert.in,https://lms.dbert.in` |
| R1-07 | **Blocker** | `dbert-api-package/.env.production.sample:33,35,37` | `SMTP_HOST=dbert.online`, `SMTP_USER=contactus@dbert.online`, `FROM_EMAIL=contactus@dbert.online` | Update to `dbert.in` and `contactus@dbert.in` |
| R1-08 | **Blocker** | `dbert-api-package/backend/core/config.py:65,67,69` | Default values for `SMTP_HOST`, `SMTP_USER`, `FROM_EMAIL` point to `dbert.online` | Update defaults to `dbert.in` |
| R1-09 | **Blocker** | `dbert-api-package/backend/api/v1/auth/router.py:152,160` | Admin JWT token claims hardcode `email: f"{settings.ADMIN_USERNAME}@dbert.online"` | Update to `@dbert.in` |
| R1-10 | **Blocker** | `apps/portal/cgi-bin/fix_env.cgi:51` | Maintenance script overwrites `.env` with `FROM_EMAIL=contactus@dbert.online` | Update line 51 to `FROM_EMAIL=contactus@dbert.in` |
| R1-11 | **Warning** | `apps/portal/.env.staging.example:34,36` | `SMTP_USER=staging@dbert.online`, `FROM_EMAIL=staging@dbert.online` | Update to `@dbert.in` |
| R1-12 | **Warning** | `dbert-api-package/.env.example:45,47,49` | Sample SMTP settings use `dbert.online` | Update to `dbert.in` |
| R1-13 | **Warning** | `apps/portal/app.py:6008-6080` | Blog redirect docstrings and comments reference `dbert.online` (code itself redirects to `dbert.in/blog`) | Update docstrings to reference `dbert.in` |
| R1-14 | **Warning** | `apps/portal/deploy/nginx.conf:3,9,25` | Legacy standalone portal config references `internship.dbert.online` | Mark file as deprecated or replace with redirection |
| R1-15 | **Warning** | `deploy/dbert-portal-nginx.conf:3,9,25` | Obsolete portal config references `internship.dbert.online` | Mark as deprecated in favor of `dbert-unified-nginx.conf` |
| R1-16 | **Warning** | `deploy/dbert-website-nginx.conf:3,9,25` | Obsolete website config references `dbert.online` | Mark as deprecated in favor of `dbert-unified-nginx.conf` |
| R1-17 | **Info** | `deploy/dbert-unified-nginx.conf:24-46` | Intentional 301 redirect blocks for `dbert.online -> dbert.in` and `internship.dbert.online -> lms.dbert.in` | Keep redirects; update Certbot SAN to include legacy domains |

---

## 3. Requirement R2: Portal Production-Readiness Audit

| Finding ID | Severity | File & Line | Summary Description | Recommended Fix |
|---|---|---|---|---|
| R2-01 | **Blocker** | `apps/portal/app.py:3691`<br>`apps/portal/app.py:18739-18833` | `scraped_lead_comment_add` in `CSRF_EXEMPT_ENDPOINTS` executes state mutations (`INSERT INTO scraped_internship_comments`) without CSRF token | Remove `scraped_lead_comment_add` from `CSRF_EXEMPT_ENDPOINTS` |
| R2-02 | **Blocker** | `apps/portal/services/database/adapter.py:844`<br>`apps/portal/.env:4-13` | Checks deprecated `FLASK_ENV == "production"`; `.env` has `REQUIRE_POSTGRES=false` & empty `DATABASE_URL`, silently falling back to SQLite `internship.db` in production | In `adapter.py:844`, evaluate production mode via `FLASK_DEBUG != "true"` and forbid SQLite in production |
| R2-03 | **Blocker** | `scripts/production_preflight.sh:53-60` | Variable expansion bug: single quotes around `'${REQUIRE_POSTGRES:-}'` prevent shell evaluation, silently passing invalid configs | Replace single quotes with double quotes |
| R2-04 | **Blocker** | `apps/portal/app.py:344-353` | Production credential assertion (`assert not _insecure`) is wrapped in `if FLASK_DEBUG != "true"`, allowing bypass if debug mode is active | Enforce credential assertion unconditionally on production hostnames |
| R2-05 | **Blocker** | `apps/portal/app.py:14734-14738`<br>`apps/portal/.env.production.sample` | In `api_razorpay_webhook()`, HMAC signature verification is guarded by `if webhook_sec:`. If `RAZORPAY_WEBHOOK_SECRET` is unset, signature verification is bypassed completely | Require `RAZORPAY_WEBHOOK_SECRET` to be non-empty; reject requests with 400 if signature fails or 500 if unconfigured; add to sample `.env` |
| R2-06 | **Blocker** | `deploy/dbert-unified-nginx.conf:126-130`<br>`apps/portal/app.py:17561-17580` | Nginx statically aliases `/uploads/` directly to disk, bypassing Flask's Phase 15 authentication and IDOR authorization controller in `serve_uploaded_file()` | Remove static `/uploads/` alias in Nginx; proxy to Flask to enforce `serve_uploaded_file()` |
| R2-07 | **Blocker** | `apps/portal/app.py:4042-4075`<br>`apps/portal/app.py:17780-17795` | `send_email_async` catches all SMTP exceptions in background daemon thread while endpoints return HTTP 200 success to user | Implement error propagation or transactional outbox queue for critical flows |
| R2-08 | **Warning** | `apps/portal/app.py:90-93`<br>`apps/portal/app.py:3654-3662` | `SESSION_COOKIE_DOMAIN` unset in config; cookies are host-only (`lms.dbert.in`), preventing cross-subdomain session recognition with `dbert.in` | Explicitly configure `app.config["SESSION_COOKIE_DOMAIN"] = os.environ.get("SESSION_COOKIE_DOMAIN", ".dbert.in")` |
| R2-09 | **Warning** | `apps/portal/app.py:6699-6725` | `staff_login` populates Flask session keys without calling `create_session()` or issuing `dbert_auth` token | Standardize `staff_login` to create a unified token session via `create_session()` |
| R2-10 | **Warning** | `apps/portal/app.py:300-302` | Secret key length < 32 characters only prints warning to stdout without aborting | Enforce `assert len(secret) >= 32` in production |
| R2-11 | **Warning** | `apps/portal/app.py:285` | `connect-src` in `csp_policy_for()` omits `https://dbert.in` and `https://lms.dbert.in`, blocking cross-subdomain fetch/API calls | Add `https://dbert.in https://lms.dbert.in` to `connect-src` |
| R2-12 | **Info** | `deploy/dbert-unified-nginx.conf:136-140` | `ProxyFix` has `x_proto=1, x_host=1`, but Nginx LMS block omits `proxy_set_header X-Forwarded-Host $host;` | Add `proxy_set_header X-Forwarded-Host $host;` to LMS block |

---

## 4. Requirement R3: Website Production-Readiness Audit

| Finding ID | Severity | File & Line | Summary Description | Recommended Fix |
|---|---|---|---|---|
| R3-01 | **Blocker** | `deploy/dbert-unified-nginx.conf:62` | Missing `error_page 404` directive in Nginx main website block (`https://dbert.in`). Unhandled 404s serve raw Nginx error page | Add `error_page 404 /404.html;` and internal location block |
| R3-02 | **Blocker** | `cpanel_public_html/learners/fellowship/index.html:1` | JSON-LD schema for Course contains `"offers": {"url": "https://internship.dbert.online/"}` and FAQ answer references `internship.dbert.online` | Regenerate static build via `npm run export:cpanel` |
| R3-03 | **Blocker** | `cpanel_public_html/learners/index.html:1` | JSON-LD FAQ schema contains `internship.dbert.online` in acceptedAnswer | Regenerate static build via `npm run export:cpanel` |
| R3-04 | **Blocker** | `deploy/dbert-unified-nginx.conf:72-76` | Static asset mismatch: Nginx `/_next/static/` points to `apps/website/.next/static/`, but 11 chunks referenced in `cpanel_public_html/` do not exist in `.next` | Align Nginx alias directory with the exact build artifact directory being served |
| R3-05 | **Warning** | `deploy/dbert-website-nginx.conf:36` | Missing `error_page 404` directive in standalone website Nginx config | Add `error_page 404 /404.html;` |
| R3-06 | **Warning** | `cpanel_public_html/ads.txt:1`<br>`apps/website/ads.txt:1` | Header reads `# Google AdSense Publisher Declaration for dbert.online` | Update header to `# Google AdSense Publisher Declaration for dbert.in` |
| R3-07 | **Warning** | `cpanel_public_html/admin/*` | Admin pages in source (`src/app/admin/`) omitted from static export (404 on static hosting) | Document that `/admin` requires Node.js runtime on EC2 port 3001 or add static fallback |
| R3-08 | **Info** | `apps/website/src/app/layout.tsx:50-75` | `twitter:site` omitted from root metadata configuration | Add `twitter: { site: '@dbert_india', creator: '@dbert_india' }` in `metadata` |
| R3-09 | **Info** | `cpanel_public_html/*` (89 internal paths) | All 89 distinct internal `href` targets resolve to existing directories with `index.html` (100% resolution for public routes) | None required (positive verification) |

---

## 5. Requirement R4: EC2 Deployment Configuration Audit

| Finding ID | Severity | File & Line | Summary Description | Recommended Fix |
|---|---|---|---|---|
| R4-01 | **Blocker** | `deploy/dbert-unified-nginx.conf:30-31, 42-43` | Missing legacy domains in SSL certificate path for 301 redirect blocks (`dbert.online`, `internship.dbert.online` point to `dbert.in/fullchain.pem` without SAN coverage) | Expand Certbot SAN to include legacy domains: `sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online` |
| R4-02 | **Blocker** | `deploy/deploy_ec2.sh:72` | Copies obsolete `dbert-portal-nginx.conf` routing only to `internship.dbert.online` on port 5001, overriding unified config | Replace with unified deployment script |
| R4-03 | **Blocker** | `scripts/production_preflight.sh:53` | `${REQUIRE_POSTGRES:-}` single-quoted: test always evaluates to FALSE, failing valid PostgreSQL configs | Replace `'${REQUIRE_POSTGRES:-}'` with `"${REQUIRE_POSTGRES:-}"` |
| R4-04 | **Blocker** | `scripts/production_preflight.sh:54` | `${DATABASE_URL:-}` single-quoted: grep for `^postgres` tests literal string and always fails | Replace `'${DATABASE_URL:-}'` with `"${DATABASE_URL:-}"` |
| R4-05 | **Blocker** | `scripts/production_preflight.sh:55` | `${POSTGRES_SCHEMA:-}` single-quoted: `-n` test always evaluates to TRUE, silently passing missing schema | Replace `'${POSTGRES_SCHEMA:-}'` with `"${POSTGRES_SCHEMA:-}"` |
| R4-06 | **Blocker** | `scripts/production_preflight.sh:56` | `${FLASK_SECRET_KEY:-}` single-quoted: `-n` test always evaluates to TRUE, silently passing missing secret key | Replace `'${FLASK_SECRET_KEY:-}'` with `"${FLASK_SECRET_KEY:-}"` |
| R4-07 | **Blocker** | `scripts/production_preflight.sh:57` | `${FLASK_DEBUG:-}` single-quoted: `!= 'true'` test always evaluates to TRUE, silently passing active debug mode | Replace `'${FLASK_DEBUG:-}'` with `"${FLASK_DEBUG:-}"` |
| R4-08 | **Blocker** | `scripts/production_preflight.sh:60` | Default key check greps literal `'${FLASK_SECRET_KEY:-}'`, never detecting default keys | Replace single quotes with double quotes |
| R4-09 | **Blocker** | `scripts/production_preflight.sh:73` | Preflight tests for `/etc/nginx/conf.d/dbert-portal.conf` which does not exist in unified deployment (`dbert-unified.conf`) | Update path to check `dbert-unified.conf` |
| R4-10 | **Warning** | `deploy/dbert-unified-nginx.conf:8-21` | Suboptimal 2-hop HTTP redirect for legacy domains (`http://dbert.online` -> `https://dbert.online` -> `https://dbert.in`), causing TLS errors on second hop | Split port 80 block to redirect legacy domains directly to `https://dbert.in` in 1 hop |
| R4-11 | **Warning** | `deploy/dbert-website.service:11` | `HOSTNAME=0.0.0.0` allows direct external access to Node.js port 3001, bypassing Nginx SSL & security headers | Change to `HOSTNAME=127.0.0.1` |
| R4-12 | **Warning** | `deploy/deploy_ec2_unified.sh:90-95` | `internship.db` remains in `apps/portal/` after PostgreSQL migration, risking accidental fallback | Move/archive `internship.db` upon successful migration |
| R4-13 | **Warning** | `apps/portal/deploy/internship.service:6-18` | Legacy service unit contains obsolete paths (`/var/www/apps/internship`) and user `www-data` | Deprecate or remove legacy unit |
| R4-14 | **Warning** | `scripts/production_preflight.sh:67` | Preflight checks `$PORTAL_DIR/internship.db` but omits root `internship.db` | Check both locations |
| R4-15 | **Warning** | `deploy/deploy_ec2_unified.sh:186` | Printed Certbot command omits legacy domains in SAN | Update printed instruction to include legacy domains |
| R4-16 | **Info** | `deploy/dbert-portal.service:1-18` | Systemd service unit verified correct: paths, user `ubuntu`, bind `127.0.0.1:5001` match architecture | Keep as is |
| R4-17 | **Info** | `deploy/dbert-unified-nginx.conf:80, 134` | Next.js port 3001 and Gunicorn port 5001 confirmed safe from system daemon collisions | Keep as is |

---

## 6. Requirement R5: Security & Hardening Spot Checks

| Finding ID | Severity | File & Line | Summary Description | Recommended Fix |
|---|---|---|---|---|
| R5-01 | **Blocker** | `deploy/dbert-unified-nginx.conf:1-143`<br>`internship.db:root` | 38MB live SQLite database committed at repo root; Nginx lacks any deny rule for `.db`/`.sqlite` files | Add Nginx location block `location ~* \.(sqlite\|db\|sql\|log)$ { deny all; return 404; }` and gitignore `.db` |
| R5-02 | **Blocker** | `deploy/dbert-unified-nginx.conf:1-143`<br>`apps/portal/.env:1-58` | Nginx configuration completely lacks dotfile / `.env` protection, exposing database credentials, SMTP passwords, and secret keys | Add Nginx location block `location ~ /\. { deny all; return 404; }` |
| R5-03 | **Blocker** | `apps/portal/app.py:8171-8173` | When `FLASK_DEBUG=true`, verification OTP is leaked in HTTP response JSON (`dev_otp_hint`), allowing account takeover | Remove `dev_otp_hint` from response or disable in production |
| R5-04 | **Blocker** | `apps/portal/app.py:8395-8406` | `@app.route("/admin/course-payments/<int:pay_id>/review")` decorates unauthenticated stub `_signal_tutor_course_unlock(intern_id, course_id)`, orphaning `admin_course_payment_review(pay_id)` and crashing with 500 | Reorder decorator to attach to `admin_course_payment_review(pay_id)` and ensure `require_admin()` is called |
| R5-05 | **Blocker** | `apps/portal/app.py:707-708`<br>`apps/portal/.env:4` | `rate_check()` returns `(True, 0)` when `FLASK_ENV == "development"`. Because `.env` sets `FLASK_ENV=development`, rate limiting is bypassed globally | Change `.env` to `FLASK_ENV=production` and remove `FLASK_ENV` bypass in `rate_check()` |
| R5-06 | **Warning** | `apps/portal/app.py:4960-4988` | `/admin/login` only checks IP rate limit and never calls `login_locked(username)`, leaving admin accounts vulnerable to distributed brute force | Add `locked, ra = login_locked(username)` check in `admin_login()` |
| R5-07 | **Warning** | `apps/portal/app.py:9630-9657` | `/company/signup` lacks rate limiting, allowing automated registration spam | Add `rate_check(f"company_signup:ip:{ip}", 10, 3600)` |
| R5-08 | **Warning** | `deploy/dbert-unified-nginx.conf:1-143` | Nginx lacks edge rate limiting (`limit_req_zone` / `limit_req`), allowing brute force to saturate Gunicorn workers | Add Nginx `limit_req_zone` directives for `/admin/login` and `/signin` |
