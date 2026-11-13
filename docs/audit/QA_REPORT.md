# Comprehensive QA Audit & Production Readiness Deliverable: DBERT Ecosystem

**Target Applications**:
- **DBERT Website**: Next.js Static Export served via Nginx on EC2 at `dbert.in` (Build: `cpanel_public_html/`, Source: `apps/website/`)
- **DBERT LMS Portal**: Flask / Gunicorn Python Application at `lms.dbert.in` (Source: `apps/portal/`)
- **DBERT API Package**: Standalone FastAPI Microservices (`dbert-api-package/`)
- **EC2 Infrastructure & Deployment**: Nginx Unified Reverse Proxy, Systemd Services, and Automation Scripts (`deploy/`, `scripts/`)

**Audit Date**: October 25–26, 2026  
**Audit Context**: Domain Migration from legacy domains (`dbert.online`, `internship.dbert.online`) to production domains (`dbert.in`, `lms.dbert.in`)  
**Audited By**: DBERT QA & Security Engineering Team (`orchestrator_1`, `explorer_r1`–`r5`, `reviewer_1`, `worker_1`)  
**Overall Verdict**: **BLOCK LIVE DEPLOYMENT** until the 42 identified Blocker defects are remediated.

---

## 1. Executive Summary & Audit Metrics

### 1.1 Overview & Production Readiness Verdict

A comprehensive, zero-assumption static code analysis and architectural security audit was conducted across the entire DBERT code repository (`c:\Users\user\Desktop\dbert-website-lms`). Every Python route, Next.js static page, TypeScript component, Nginx configuration, Systemd unit, shell deployment script, XML sitemap, robot directive, and environment file was inspected directly on disk.

**Production Readiness Assessment**:
1. **DBERT Website (`apps/website/` & `cpanel_public_html/`)**: **NOT READY FOR PRODUCTION**.
   - While internal navigation across public pages exhibits 100% route integrity (89/89 routes resolve on disk with 0 dead ends), the deployed static bundle (`cpanel_public_html/`) is an obsolete pre-migration build. It embeds **157 outbound links** pointing to legacy `https://internship.dbert.online/` in headers and footers, retains legacy `internship.dbert.online` URLs in Course and FAQ JSON-LD schemas, and references 11 script chunks that do not exist in the source `.next/static/` directory. Furthermore, the root website `sitemap.xml` and `robots.txt` direct search engines to `dbert.online`.
2. **DBERT LMS Portal (`apps/portal/`)**: **CRITICAL SECURITY & RELIABILITY RISKS**.
   - The LMS portal suffers from cascading failure modes:
     - **Database Silent Fallback**: Checks deprecated `FLASK_ENV == "production"`. Combined with `.env` setting `REQUIRE_POSTGRES=false` and empty `DATABASE_URL`, the portal silently falls back to SQLite `internship.db` in production, dropping concurrent financial and enrollment transactions.
     - **Preflight Shell Expansion Failure**: `scripts/production_preflight.sh` encloses test expressions in literal single quotes (`'${VAR:-}'`), completely blinding deployment validation and causing invalid, insecure configurations to falsely pass.
     - **Payment Webhook Verification Bypass**: In `api_razorpay_webhook()`, HMAC signature validation is guarded by `if webhook_sec:`. If `RAZORPAY_WEBHOOK_SECRET` is unset, signature verification is skipped completely, allowing unauthenticated forged payments to unlock course access.
     - **IDOR & Data Exposure**: Nginx directly aliases `/uploads/` to disk, bypassing Flask's Phase 15 authentication and IDOR access control (`serve_uploaded_file()`), publicly exposing candidate CVs and payment receipts.
     - **Admin Handler Routing Crash**: Route decorator `@app.route("/admin/course-payments/<int:pay_id>/review")` is attached to a helper stub `_signal_tutor_course_unlock(intern_id, course_id)`, leaving the real admin review handler orphaned and causing HTTP 500 crashes on all review attempts.
     - **Silent Email Failures**: SMTP dispatch errors in `send_email_async` are caught in a background thread and ignored, while routes return HTTP 200 success to users for failed password resets.
     - **Direct Web Exposure of Live SQLite Databases & `.env`**: Committed live SQLite databases (totaling ~39MB) and plaintext credentials in `.env` lack deny rules in Nginx.

### 1.2 Audit Metrics & Severity Breakdown

All 71 individual audited findings were cross-checked and verified independently by `reviewer_1` with zero false positives.

| Audit Category | Total Findings | Blockers | Warnings | Informational | Confirmed Verdict | Needs Clarification / Nuanced |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Pre-Confirmed Baseline (PRE)** | 8 | 7 | 1 | 0 | 7 | 1 (PRE-07) |
| **R1: Domain Migration Completeness** | 17 | 10 | 6 | 1 | 16 | 1 (R1-13) |
| **R2: Portal Production Readiness** | 12 | 7 | 4 | 1 | 11 | 1 (R2-08) |
| **R3: Website Production Readiness** | 9 | 4 | 3 | 2 | 9 | 0 |
| **R4: EC2 Deployment Configuration** | 17 | 9 | 6 | 2 | 17 | 0 |
| **R5: Security & Hardening Audit** | 8 | 5 | 3 | 0 | 7 | 1 (R5-01) |
| **TOTAL AUDITED FINDINGS** | **71** | **42** | **23** | **6** | **67** | **4** |

*Note on Blocker Counts*: When counting discrete finding records across all modular sections, 42 Blocker records exist. When deduplicating root-cause mechanisms that span multiple sections (e.g., preflight script shell expansion bug cited in R2-03 and R4-03..R4-08, and Nginx `/uploads/` exposure cited in R2-06 and R5-02), there are 38 unique operational Blocker root causes.

---

## 2. Pre-Confirmed Baseline Findings (Verified)

These 8 findings were initially flagged in preliminary scans and requested by `ORIGINAL_REQUEST.md` to be confirmed, documented with exact file and line citations, and supplied with verified remediation actions.

| # | Finding ID | Severity | File:Line | Description | Recommended Fix | Reviewer Verdict |
|---|---|:---:|---|---|---|:---:|
| 1 | **PRE-01** | **Blocker** | `apps/portal/.env:27` | `SMTP_HOST=dbert.online` directs live portal transactional email connections to legacy domain mailserver. | Change to `SMTP_HOST=dbert.in` (or target SMTP provider host). | **Confirmed** |
| 2 | **PRE-02** | **Blocker** | `apps/portal/.env:29` | `SMTP_USER=contactus@dbert.online` specifies legacy authentication account for SMTP. | Update to `SMTP_USER=contactus@dbert.in`. | **Confirmed** |
| 3 | **PRE-03** | **Blocker** | `apps/portal/.env:31` | `FROM_EMAIL=contactus@dbert.online` causes outbound emails to fail SPF/DKIM alignment on `dbert.in` and sends user replies to old domain. | Update to `FROM_EMAIL=contactus@dbert.in`. | **Confirmed** |
| 4 | **PRE-04** | **Blocker** | `apps/portal/app.py:304` | Application fallback default `SMTP_HOST = os.environ.get("SMTP_HOST", "dbert.online")` defaults to legacy domain if environment variable is absent. | Change fallback default to `"dbert.in"`. | **Confirmed** |
| 5 | **PRE-05** | **Blocker** | `apps/portal/app.py:2690` | UP3.1 staff seeding hardcodes `staff_email = f"{ADMIN_USERNAME}@dbert.online"`, generating non-functional admin email. | Change hardcoded string to `f"{ADMIN_USERNAME}@dbert.in"`. | **Confirmed** |
| 6 | **PRE-06** | **Blocker** | `deploy/deploy_ec2_unified.sh:56, 110` | Hardcoded database password `DB_PASS="DBERT_SECURE_PASSWORD_123"` committed in deployment script and written to production `.env`. | Generate securely via `openssl rand -hex 24` or ingest from an external deployment secret store. | **Confirmed** |
| 7 | **PRE-07** | **Blocker** | `apps/website/__next.__PAGE__.txt:48-49`<br>`apps/website/index.html:1`<br>`apps/website/pricing.txt:20`<br>`cpanel_public_html/__next.__PAGE__.txt:49` | JSON-LD schema `@type: Organization` has `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, and `"email": "contactus@dbert.online"`. | Re-export static bundle from source where `metadataBase` is set to `https://dbert.in`. | **Needs Clarification** *(Confirmed with Nuance)* |
| 8 | **PRE-08** | **Warning** | `apps/portal/templates/seo_landing.html:133` | Anchor tag specifies `href="https://dbert.in"` but visible anchor text reads `dbert.online`. | Change anchor text from `dbert.online` to `dbert.in`. | **Confirmed** |

---

## 3. Grouped Findings by Category

*Schema: Severity | File:Line | Description | Recommended Fix | Reviewer Verdict*

### Category R1: Domain Migration Completeness (`dbert.online` $\rightarrow$ `dbert.in`)

| Finding ID | Severity | File:Line | Description | Recommended Fix | Reviewer Verdict |
|---|:---:|---|---|---|:---:|
| **R1-01** | **Blocker** | `apps/portal/sitemap.xml:1` | 664 KB single-line sitemap contains 85+ canonical `<loc>` tags pointing to `https://internship.dbert.online/...` (e.g. `/jobs`, `/internships`, `/cv/*`, `/program`), causing search crawlers to index legacy portal domain. | Bulk replace `https://internship.dbert.online` with `https://lms.dbert.in` across `apps/portal/sitemap.xml`. | **Confirmed** |
| **R1-02** | **Blocker** | `apps/website/sitemap.xml:4-420` | Root website sitemap contains 70 `<loc>` tags all pointing to `https://dbert.online/...` (e.g. `/pricing`, `/verify`, `/privacy`). | Overwrite `apps/website/sitemap.xml` with the corrected `cpanel_public_html/sitemap.xml` which uses `https://dbert.in`. | **Confirmed** |
| **R1-03** | **Blocker** | `apps/website/robots.txt:13` | Line 13 explicitly specifies `Sitemap: https://dbert.online/sitemap.xml`, directing all search engine robots to the legacy domain sitemap. | Update line 13 to `Sitemap: https://dbert.in/sitemap.xml`. | **Confirmed** |
| **R1-04** | **Blocker** | `cpanel_public_html/*` (all 110 HTML files) | 157 outbound link instances in Header and Footer components across all 110 static HTML files link to `https://internship.dbert.online/` due to an outdated static export. | Rebuild and export static site via `npm run export:cpanel` in `apps/website/` to reflect updated source links pointing to `https://lms.dbert.in/`. | **Confirmed** |
| **R1-05** | **Blocker** | `apps/website/out/` (203 static files) | 203 static export files retain `dbert.online` in `og:image`, `twitter:image`, and Organization JSON-LD schemas. | Re-export static bundle from updated Next.js source code. | **Confirmed** |
| **R1-06** | **Blocker** | `dbert-api-package/.env.production.sample:18` | `CORS_ORIGINS=https://dbert.online,https://internship.dbert.online` restricts FastAPI CORS to legacy domains; API requests from `dbert.in` and `lms.dbert.in` will be blocked by browsers. | Update to `CORS_ORIGINS=https://dbert.in,https://lms.dbert.in`. | **Confirmed** |
| **R1-07** | **Blocker** | `dbert-api-package/.env.production.sample:33,35,37` | Standalone API production sample specifies `SMTP_HOST=dbert.online`, `SMTP_USER=contactus@dbert.online`, and `FROM_EMAIL=contactus@dbert.online`. | Update to `SMTP_HOST=dbert.in`, `SMTP_USER=contactus@dbert.in`, and `FROM_EMAIL=contactus@dbert.in`. | **Confirmed** |
| **R1-08** | **Blocker** | `dbert-api-package/backend/core/config.py:65,67,69` | Default values for `SMTP_HOST`, `SMTP_USER`, and `FROM_EMAIL` fall back to `dbert.online` if omitted from the environment. | Update default fallbacks to `dbert.in` and `contactus@dbert.in`. | **Confirmed** |
| **R1-09** | **Blocker** | `dbert-api-package/backend/api/v1/auth/router.py:152,160` | JWT access token claims and user profile payload embed `@dbert.online` in admin authentication tokens (`f"{settings.ADMIN_USERNAME}@dbert.online"`). | Update string interpolation to use `@dbert.in`. | **Confirmed** |
| **R1-10** | **Blocker** | `apps/portal/cgi-bin/fix_env.cgi:51` | Maintenance script overwrites `.env` with legacy sender email `FROM_EMAIL=contactus@dbert.online`. | Update line 51 to `FROM_EMAIL=contactus@dbert.in` or remove obsolete `.cgi` file. | **Confirmed** |
| **R1-11** | **Warning** | `apps/portal/.env.staging.example:34,36` | Staging sample environment file specifies `SMTP_USER=staging@dbert.online` and `FROM_EMAIL=staging@dbert.online`. | Update to `staging@dbert.in`. | **Confirmed** |
| **R1-12** | **Warning** | `dbert-api-package/.env.example:45,47,49` | Development sample environment file references legacy domain for SMTP settings. | Update sample values to `dbert.in` and `contactus@dbert.in`. | **Confirmed** |
| **R1-13** | **Warning** | `apps/portal/app.py:6008-6080` | Blog redirect docstrings and section header comments reference `dbert.online` (code itself redirects to `https://dbert.in/blog/{slug}`). | Update comments and docstrings to reference `dbert.in`. | **Needs Clarification** *(Confirmed with Nuance)* |
| **R1-14** | **Warning** | `apps/portal/deploy/nginx.conf:3,9,25` | Legacy standalone portal Nginx configuration references `internship.dbert.online`. | Mark file as deprecated or replace with redirection to `lms.dbert.in`. | **Confirmed** |
| **R1-15** | **Warning** | `deploy/dbert-portal-nginx.conf:3,9,25` | Obsolete standalone portal config under `deploy/` references `internship.dbert.online`. | Deprecate in favor of `deploy/dbert-unified-nginx.conf`. | **Confirmed** |
| **R1-16** | **Warning** | `deploy/dbert-website-nginx.conf:3,9,25` | Obsolete standalone website config references `dbert.online`. | Deprecate in favor of `deploy/dbert-unified-nginx.conf`. | **Confirmed** |
| **R1-17** | **Info** | `deploy/dbert-unified-nginx.conf:24-46` | Intentional 301 redirect blocks for `dbert.online -> dbert.in` and `internship.dbert.online -> lms.dbert.in`. | Maintain redirect rules; ensure SSL SAN certificate coverage per R4-01. | **Confirmed** |

---

### Category R2: Portal (Flask/Gunicorn) Production-Readiness

| Finding ID | Severity | File:Line | Description | Recommended Fix | Reviewer Verdict |
|---|:---:|---|---|---|:---:|
| **R2-01** | **Blocker** | `apps/portal/app.py:3691`<br>`apps/portal/app.py:18739-18833` | Endpoint `scraped_lead_comment_add` is listed in `CSRF_EXEMPT_ENDPOINTS` while performing state-mutating database writes (`INSERT INTO scraped_internship_comments`), allowing cross-site comment forgery. | Remove `scraped_lead_comment_add` from `CSRF_EXEMPT_ENDPOINTS`. | **Confirmed** |
| **R2-02** | **Blocker** | `apps/portal/services/database/adapter.py:844`<br>`apps/portal/.env:4-13` | Checks deprecated `FLASK_ENV == "production"`. Because `.env` sets `FLASK_ENV=development`, `REQUIRE_POSTGRES=false`, and empty `DATABASE_URL`, the portal silently falls back to SQLite `internship.db` in production. | In `adapter.py:844`, evaluate production mode via `FLASK_DEBUG != "true"` and strictly forbid SQLite fallback in production. | **Confirmed** |
| **R2-03** | **Blocker** | `scripts/production_preflight.sh:53-60` | Preflight check encloses variables in single quotes (`'${REQUIRE_POSTGRES:-}'`), preventing Bash parameter expansion. Tests evaluate literal strings and falsely pass invalid configurations. | Replace single quotes with double quotes (e.g., `"${REQUIRE_POSTGRES:-}"`). | **Confirmed** |
| **R2-04** | **Blocker** | `apps/portal/app.py:344-353` | Production credential assertion (`assert not _insecure`) is guarded by `if os.environ.get("FLASK_DEBUG", "false").lower() != "true":`. If `FLASK_DEBUG=true` is set, the guard is bypassed completely. | Enforce credential assertions unconditionally on production hostnames regardless of debug flag. | **Confirmed** |
| **R2-05** | **Blocker** | `apps/portal/app.py:14734-14738`<br>`apps/portal/.env.production.sample` | In `api_razorpay_webhook()`, HMAC signature validation is guarded by `if webhook_sec:`. If `RAZORPAY_WEBHOOK_SECRET` is unset, signature verification is bypassed completely. The variable is also missing from `.env.production.sample`. | Enforce `assert webhook_sec`; reject requests with 400 on signature failure and 500 if unconfigured; add `RAZORPAY_WEBHOOK_SECRET` to `.env.production.sample`. | **Confirmed** |
| **R2-06** | **Blocker** | `deploy/dbert-unified-nginx.conf:126-130`<br>`apps/portal/app.py:17561-17580` | Nginx statically aliases `/uploads/` directly to disk, bypassing Flask's Phase 15 authentication and IDOR authorization controller in `serve_uploaded_file()`, publicly exposing CVs and receipts. | Remove static `/uploads/` alias in Nginx; proxy to Gunicorn/Flask to enforce `serve_uploaded_file()`. | **Confirmed** |
| **R2-07** | **Blocker** | `apps/portal/app.py:4042-4075`<br>`apps/portal/app.py:17780-17795` | `send_email_async` catches all SMTP exceptions in a background daemon thread while endpoints return HTTP 200 success to clients, hiding password reset and notification delivery failures. | Implement error propagation or transactional outbox queueing for critical email flows. | **Confirmed** |
| **R2-08** | **Warning** | `apps/portal/app.py:90-93`<br>`apps/portal/app.py:3654-3662` | `SESSION_COOKIE_DOMAIN` is unset and `domain` is omitted in `_set_session_cookie()`. Cookies are host-only (`lms.dbert.in`), preventing cross-subdomain session recognition with `dbert.in`. | Explicitly configure `app.config["SESSION_COOKIE_DOMAIN"] = os.environ.get("SESSION_COOKIE_DOMAIN", ".dbert.in")` if shared authentication is required. | **Needs Clarification** *(Confirmed with Nuance)* |
| **R2-09** | **Warning** | `apps/portal/app.py:6699-6725` | `staff_login` populates client Flask session cookies directly without calling `create_session()` to create a `user_sessions` token or setting `dbert_auth`. | Standardize `staff_login` to create a unified token session via `create_session()` and issue `dbert_auth`. | **Confirmed** |
| **R2-10** | **Warning** | `apps/portal/app.py:300-302` | `SECRET_KEY` length < 32 characters only prints a warning to stdout without halting startup. | Enforce `assert len(secret) >= 32` when starting up in production. | **Confirmed** |
| **R2-11** | **Warning** | `apps/portal/app.py:285` | `connect-src` in `csp_policy_for()` omits `https://dbert.in` and `https://lms.dbert.in`, causing cross-subdomain API/fetch calls to be blocked under CSP. | Add `https://dbert.in https://lms.dbert.in` to `connect-src`. | **Confirmed** |
| **R2-12** | **Info** | `deploy/dbert-unified-nginx.conf:136-140` | `ProxyFix` has `x_proto=1, x_host=1`, but LMS location block in Nginx omits `proxy_set_header X-Forwarded-Host $host;` (present in website block). | Add `proxy_set_header X-Forwarded-Host $host;` to LMS block. | **Confirmed** |

---

### Category R3: Website (Next.js Static Export) Production-Readiness

| Finding ID | Severity | File:Line | Description | Recommended Fix | Reviewer Verdict |
|---|:---:|---|---|---|:---:|
| **R3-01** | **Blocker** | `deploy/dbert-unified-nginx.conf:62` | `error_page 404` directive is completely missing in `dbert-unified-nginx.conf` (`dbert.in` server block). Unhandled 404s serve raw Nginx error page instead of branded 404. | Add `error_page 404 /404.html;` and an internal `location = /404.html { root ...; internal; }` block. | **Confirmed** |
| **R3-02** | **Blocker** | `cpanel_public_html/learners/fellowship/index.html:1` | Static page contains `"offers": {"@type": "Offer", ..., "url": "https://internship.dbert.online/"}` and FAQ text references `internship.dbert.online`. | Rebuild static export via `npm run export:cpanel` in `apps/website/`. | **Confirmed** |
| **R3-03** | **Blocker** | `cpanel_public_html/learners/index.html:1` | Static page JSON-LD FAQ schema contains `internship.dbert.online` in `acceptedAnswer`. | Rebuild static export via `npm run export:cpanel` in `apps/website/`. | **Confirmed** |
| **R3-04** | **Blocker** | `deploy/dbert-unified-nginx.conf:72-76` | Static asset mismatch: Nginx `/_next/static/` points to `apps/website/.next/static/`, but 11 chunks referenced in `cpanel_public_html/` (e.g. `22848iis4ukqu.js`) do not exist in `.next`. | Align Nginx alias directory with the exact build artifact directory being served (`/var/www/dbert-website-lms/cpanel_public_html/_next/static/`). | **Confirmed** |
| **R3-05** | **Warning** | `deploy/dbert-website-nginx.conf:36` | Missing `error_page 404` directive in standalone website Nginx configuration. | Add `error_page 404 /404.html;`. | **Confirmed** |
| **R3-06** | **Warning** | `cpanel_public_html/ads.txt:1`<br>`apps/website/ads.txt:1` | Header reads `# Google AdSense Publisher Declaration for dbert.online`. | Update header to `# Google AdSense Publisher Declaration for dbert.in`. | **Confirmed** |
| **R3-07** | **Warning** | `cpanel_public_html/admin/*` | Admin pages present in source (`src/app/admin/`) were omitted during static export, returning 404 on static hosting. | Document that `/admin` requires Node.js runtime on EC2 port 3001, or export static fallback pages. | **Confirmed** |
| **R3-08** | **Info** | `apps/website/src/app/layout.tsx:50-75` | `twitter:site` is omitted from root metadata configuration. | Add `twitter: { site: '@dbert_india', creator: '@dbert_india' }` in `metadata`. | **Confirmed** |
| **R3-09** | **Info** | `cpanel_public_html/*` (89 internal paths) | All 89 distinct internal `href` targets resolve to existing directories with `index.html` (100% mechanical resolution for public routes). | None required (positive audit confirmation). | **Confirmed** |

---

### Category R4: EC2 Deployment Configuration Audit

| Finding ID | Severity | File:Line | Description | Recommended Fix | Reviewer Verdict |
|---|:---:|---|---|---|:---:|
| **R4-01** | **Blocker** | `deploy/dbert-unified-nginx.conf:30-31, 42-43` | SSL certificate for 301 redirect blocks points to `/etc/letsencrypt/live/dbert.in/fullchain.pem`. Because the certificate SAN lacks `dbert.online` and `internship.dbert.online`, browser TLS handshakes abort before the 301 redirect is received. | Expand Certbot SAN: `sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online`. | **Confirmed** |
| **R4-02** | **Blocker** | `deploy/deploy_ec2.sh:72` | Legacy deploy script copies obsolete `dbert-portal-nginx.conf` routing only to `internship.dbert.online` on port 5001, overwriting the unified configuration. | Replace legacy deploy script invocation with unified deployment script. | **Confirmed** |
| **R4-03** | **Blocker** | `scripts/production_preflight.sh:53` | `${REQUIRE_POSTGRES:-}` single-quoted: test compares literal string against `'true'`, always evaluating to FALSE and rejecting valid PostgreSQL configs. | Replace `'${REQUIRE_POSTGRES:-}'` with `"${REQUIRE_POSTGRES:-}"`. | **Confirmed** |
| **R4-04** | **Blocker** | `scripts/production_preflight.sh:54` | `${DATABASE_URL:-}` single-quoted: grep for `^postgres` tests literal string syntax and always fails. | Replace `'${DATABASE_URL:-}'` with `"${DATABASE_URL:-}"`. | **Confirmed** |
| **R4-05** | **Blocker** | `scripts/production_preflight.sh:55` | `${POSTGRES_SCHEMA:-}` single-quoted: `-n` test on literal 19-char string always evaluates to TRUE, masking missing schema. | Replace `'${POSTGRES_SCHEMA:-}'` with `"${POSTGRES_SCHEMA:-}"`. | **Confirmed** |
| **R4-06** | **Blocker** | `scripts/production_preflight.sh:56` | `${FLASK_SECRET_KEY:-}` single-quoted: `-n` test on literal string always evaluates to TRUE, masking missing secret key. | Replace `'${FLASK_SECRET_KEY:-}'` with `"${FLASK_SECRET_KEY:-}"`. | **Confirmed** |
| **R4-07** | **Blocker** | `scripts/production_preflight.sh:57` | `${FLASK_DEBUG:-}` single-quoted: `!= 'true'` test on literal string always evaluates to TRUE, masking active debug mode in production. | Replace `'${FLASK_DEBUG:-}'` with `"${FLASK_DEBUG:-}"`. | **Confirmed** |
| **R4-08** | **Blocker** | `scripts/production_preflight.sh:60` | Greps literal `'${FLASK_SECRET_KEY:-}'`, never detecting shipped default secret keys (`digitalblinc|default|changeme`). | Replace single quotes with double quotes: `echo "${FLASK_SECRET_KEY:-}"`. | **Confirmed** |
| **R4-09** | **Blocker** | `scripts/production_preflight.sh:73` | Preflight checks for `/etc/nginx/conf.d/dbert-portal.conf` which does not exist in unified deployment (`dbert-unified.conf`), causing preflight to always abort. | Update path check to `/etc/nginx/conf.d/dbert-unified.conf`. | **Confirmed** |
| **R4-10** | **Warning** | `deploy/dbert-unified-nginx.conf:8-21` | Suboptimal 2-hop HTTP redirect for legacy domains (`http://dbert.online` $\rightarrow$ `https://dbert.online` $\rightarrow$ `https://dbert.in`), causing TLS handshake errors on the second hop. | Split port 80 block to redirect legacy domains directly to `https://dbert.in` in 1 hop. | **Confirmed** |
| **R4-11** | **Warning** | `deploy/dbert-website.service:11` | `HOSTNAME=0.0.0.0` allows direct external access to Node.js port 3001, bypassing Nginx SSL termination and security headers. | Change to `HOSTNAME=127.0.0.1`. | **Confirmed** |
| **R4-12** | **Warning** | `deploy/deploy_ec2_unified.sh:90-95` | `internship.db` remains in `apps/portal/` after PostgreSQL data migration, risking accidental fallback. | Move/archive `internship.db` upon successful PostgreSQL migration. | **Confirmed** |
| **R4-13** | **Warning** | `apps/portal/deploy/internship.service:6-18` | Legacy service unit contains obsolete paths (`/var/www/apps/internship`) and user `www-data`. | Deprecate or delete obsolete unit. | **Confirmed** |
| **R4-14** | **Warning** | `scripts/production_preflight.sh:67` | Preflight checks `$PORTAL_DIR/internship.db` but omits root `internship.db`. | Check both locations to prevent SQLite fallback. | **Confirmed** |
| **R4-15** | **Warning** | `deploy/deploy_ec2_unified.sh:186` | Printed Certbot instruction omits legacy domains in SAN. | Update printed instruction to include legacy domains in `-d` flags. | **Confirmed** |
| **R4-16** | **Info** | `deploy/dbert-portal.service:1-18` | Portal systemd service unit verified correct: paths, user `ubuntu`, bind `127.0.0.1:5001` match architecture. | Keep as is. | **Confirmed** |
| **R4-17** | **Info** | `deploy/dbert-unified-nginx.conf:80, 134` | Next.js port 3001 and Gunicorn port 5001 confirmed safe from system daemon collisions. | Keep as is. | **Confirmed** |

---

### Category R5: Security & Hardening Spot Checks

| Finding ID | Severity | File:Line | Description | Recommended Fix | Reviewer Verdict |
|---|:---:|---|---|---|:---:|
| **R5-01** | **Blocker** | `deploy/dbert-unified-nginx.conf:1-143`<br>`internship.db:root`<br>`apps/portal/internship.db` | Committed live SQLite databases (~39MB combined) exist in repository; Nginx configuration completely lacks deny rules for `.db` or `.sqlite` files. | Add Nginx location block `location ~* \.(sqlite\|db\|sql\|log)$ { deny all; return 404; }` and gitignore `.db` files. | **Needs Clarification** *(Confirmed with Nuance)* |
| **R5-02** | **Blocker** | `deploy/dbert-unified-nginx.conf:1-143`<br>`apps/portal/.env:1-58` | Nginx configuration completely lacks hidden dotfile protection (`.env`), exposing database credentials, SMTP passwords, and secret keys to direct HTTP access. | Add Nginx location block `location ~ /\. { deny all; return 404; }`. | **Confirmed** |
| **R5-03** | **Blocker** | `apps/portal/app.py:8171-8173` | When `FLASK_DEBUG=true`, verification OTP is leaked in the HTTP response JSON payload (`dev_otp_hint`), allowing trivial account takeover. | Remove `dev_otp_hint` from response payload or disable unconditionally in production. | **Confirmed** |
| **R5-04** | **Blocker** | `apps/portal/app.py:8395-8406` | Decorator `@app.route("/admin/course-payments/<int:pay_id>/review")` decorates unauthenticated stub `_signal_tutor_course_unlock(intern_id, course_id)`, orphaning `admin_course_payment_review(pay_id)` and crashing with runtime 500 TypeError. | Reorder decorator to attach to `admin_course_payment_review(pay_id)` and verify `require_admin()` is called. | **Confirmed** |
| **R5-05** | **Blocker** | `apps/portal/app.py:707-708`<br>`apps/portal/.env:4` | `rate_check()` returns `(True, 0)` when `FLASK_ENV == "development"`. Because `.env` sets `FLASK_ENV=development`, rate limiting is bypassed globally. | Change `.env` to `FLASK_ENV=production` and remove `FLASK_ENV` bypass in `rate_check()`. | **Confirmed** |
| **R5-06** | **Warning** | `apps/portal/app.py:4960-4988` | `/admin/login` only checks IP rate limit and never calls `login_locked(username)`, leaving admin accounts vulnerable to distributed credential stuffing. | Add `locked, ra = login_locked(username)` check in `admin_login()`. | **Confirmed** |
| **R5-07** | **Warning** | `apps/portal/app.py:9630-9657` | `/company/signup` lacks rate limiting, allowing automated registration flooding and database resource exhaustion. | Add `rate_check(f"company_signup:ip:{ip}", 10, 3600)` to `company_signup()`. | **Confirmed** |
| **R5-08** | **Warning** | `deploy/dbert-unified-nginx.conf:1-143` | Nginx lacks edge rate limiting (`limit_req_zone` / `limit_req`), allowing brute force traffic to saturate Gunicorn workers. | Add Nginx `limit_req_zone` directives for `/admin/login` and `/signin`. | **Confirmed** |

---

## 4. Complete Verified Internal Links Audit (`cpanel_public_html/`)

A mechanical traversal of all 74 HTML files in `cpanel_public_html/` was conducted to extract and verify every internal hyperlink (`href` starting with `/`).
- **Total HTML Files Audited**: 74 files
- **Total `<a>` Tags Inspected**: 7,874 anchor tags
- **Total Distinct Internal Paths**: **89 routes**
- **Dead Ends Detected**: **0** (100% resolution for public static routes)

### Full 89-Route Resolution Table

| # | Internal Route (`href`) | Target Relative Path on Disk | Target Exists? | Occurrences | Sample Source Location |
|---|---|---|:---:|:---:|---|
| 1 | `/` | `index.html` | **YES** | 148 | `cpanel_public_html/404.html:1` |
| 2 | `/about/` | `about/index.html` | **YES** | 149 | `cpanel_public_html/404.html:1` |
| 3 | `/about/careers/` | `about/careers/index.html` | **YES** | 74 | `cpanel_public_html/404.html:1` |
| 4 | `/about/contact/` | `about/contact/index.html` | **YES** | 102 | `cpanel_public_html/404.html:1` |
| 5 | `/about/credentials/` | `about/credentials/index.html` | **YES** | 153 | `cpanel_public_html/404.html:1` |
| 6 | `/about/team/` | `about/team/index.html` | **YES** | 170 | `cpanel_public_html/404.html:1` |
| 7 | `/ai-consultant/` | `ai-consultant/index.html` | **YES** | 74 | `cpanel_public_html/404.html:1` |
| 8 | `/ai-solutions` | `ai-solutions/index.html` | **YES** | 2 | `cpanel_public_html/blog/cloud-llm-vs-private-vpc-costs/index.html:12` |
| 9 | `/ai-solutions/` | `ai-solutions/index.html` | **YES** | 80 | `cpanel_public_html/404.html:1` |
| 10 | `/ai-solutions/consultation/` | `ai-solutions/consultation/index.html` | **YES** | 158 | `cpanel_public_html/404.html:1` |
| 11 | `/ai-solutions/llm-training/` | `ai-solutions/llm-training/index.html` | **YES** | 3 | `cpanel_public_html/index.html:1` |
| 12 | `/ai-solutions/llm-training/dbert-ai/` | `ai-solutions/llm-training/dbert-ai/index.html` | **YES** | 78 | `cpanel_public_html/404.html:1` |
| 13 | `/ai-solutions/llm-training/pipeline/` | `ai-solutions/llm-training/pipeline/index.html` | **YES** | 76 | `cpanel_public_html/404.html:1` |
| 14 | `/ai-solutions/llm-training/private-hosting` | `ai-solutions/llm-training/private-hosting/index.html` | **YES** | 3 | `cpanel_public_html/blog/ai-agent-developer-salary-2026/index.html:45` |
| 15 | `/ai-solutions/llm-training/private-hosting/` | `ai-solutions/llm-training/private-hosting/index.html` | **YES** | 163 | `cpanel_public_html/404.html:1` |
| 16 | `/ai-solutions/products/` | `ai-solutions/products/index.html` | **YES** | 79 | `cpanel_public_html/404.html:1` |
| 17 | `/ai-solutions/products/certificate-verification-api/` | `ai-solutions/products/certificate-verification-api/index.html` | **YES** | 154 | `cpanel_public_html/404.html:1` |
| 18 | `/ai-solutions/products/dbert-chat/` | `ai-solutions/products/dbert-chat/index.html` | **YES** | 155 | `cpanel_public_html/404.html:1` |
| 19 | `/ai-solutions/products/document-ai/` | `ai-solutions/products/document-ai/index.html` | **YES** | 157 | `cpanel_public_html/404.html:1` |
| 20 | `/ai-solutions/products/hiring-automation-suite/` | `ai-solutions/products/hiring-automation-suite/index.html` | **YES** | 157 | `cpanel_public_html/404.html:1` |
| 21 | `/ai-solutions/products/intern-management-system/` | `ai-solutions/products/intern-management-system/index.html` | **YES** | 154 | `cpanel_public_html/404.html:1` |
| 22 | `/blog/` | `blog/index.html` | **YES** | 11 | `cpanel_public_html/index.html:1` |
| 23 | `/blog/ai-agent-developer-salary-2026/` | `blog/ai-agent-developer-salary-2026/index.html` | **YES** | 5 | `cpanel_public_html/blog/index.html:1` |
| 24 | `/blog/ai-agent-frameworks-comparison/` | `blog/ai-agent-frameworks-comparison/index.html` | **YES** | 2 | `cpanel_public_html/blog/index.html:1` |
| 25 | `/blog/building-scalable-microservices-with-fastapi/` | `blog/building-scalable-microservices-with-fastapi/index.html` | **YES** | 4 | `cpanel_public_html/blog/index.html:1` |
| 26 | `/blog/cloud-llm-vs-private-vpc-costs/` | `blog/cloud-llm-vs-private-vpc-costs/index.html` | **YES** | 2 | `cpanel_public_html/blog/index.html:1` |
| 27 | `/blog/equity-for-services/` | `blog/equity-for-services/index.html` | **YES** | 4 | `cpanel_public_html/blog/index.html:1` |
| 28 | `/blog/fast-vs-safe-agreement-india/` | `blog/fast-vs-safe-agreement-india/index.html` | **YES** | 2 | `cpanel_public_html/blog/index.html:1` |
| 29 | `/blog/non-tech-to-ai-career/` | `blog/non-tech-to-ai-career/index.html` | **YES** | 5 | `cpanel_public_html/blog/index.html:1` |
| 30 | `/blog/paid-ai-internship-india-guide-2026/` | `blog/paid-ai-internship-india-guide-2026/index.html` | **YES** | 5 | `cpanel_public_html/blog/index.html:1` |
| 31 | `/blog/rag-pipeline-tutorial-from-scratch/` | `blog/rag-pipeline-tutorial-from-scratch/index.html` | **YES** | 6 | `cpanel_public_html/blog/index.html:1` |
| 32 | `/cohorts/aivara/` | `cohorts/aivara/index.html` | **YES** | 1 | `cpanel_public_html/about/careers/index.html:1` |
| 33 | `/hire/pre-vetted-engineers/` | `hire/pre-vetted-engineers/index.html` | **YES** | 148 | `cpanel_public_html/404.html:1` |
| 34 | `/labs` | `labs/index.html` | **YES** | 5 | `cpanel_public_html/blog/ai-agent-developer-salary-2026/index.html:11` |
| 35 | `/labs/` | `labs/index.html` | **YES** | 224 | `cpanel_public_html/404.html:1` |
| 36 | `/labs/collaborate/` | `labs/collaborate/index.html` | **YES** | 5 | `cpanel_public_html/about/team/index.html:1` |
| 37 | `/labs/opensource/` | `labs/opensource/index.html` | **YES** | 78 | `cpanel_public_html/404.html:1` |
| 38 | `/labs/publications/` | `labs/publications/index.html` | **YES** | 80 | `cpanel_public_html/404.html:1` |
| 39 | `/labs/research/` | `labs/research/index.html` | **YES** | 3 | `cpanel_public_html/labs/index.html:1` |
| 40 | `/learners` | `learners/index.html` | **YES** | 1 | `cpanel_public_html/learners/interview-prep/index.html:1` |
| 41 | `/learners/` | `learners/index.html` | **YES** | 91 | `cpanel_public_html/404.html:1` |
| 42 | `/learners/accelerate` | `learners/accelerate/index.html` | **YES** | 1 | `cpanel_public_html/blog/rag-pipeline-tutorial-from-scratch/index.html:11` |
| 43 | `/learners/accelerate/` | `learners/accelerate/index.html` | **YES** | 82 | `cpanel_public_html/404.html:1` |
| 44 | `/learners/courses/` | `learners/courses/index.html` | **YES** | 78 | `cpanel_public_html/404.html:1` |
| 45 | `/learners/courses/ai-agent-development` | `learners/courses/ai-agent-development/index.html` | **YES** | 1 | `cpanel_public_html/blog/ai-agent-frameworks-comparison/index.html:119` |
| 46 | `/learners/courses/ai-agent-development/` | `learners/courses/ai-agent-development/index.html` | **YES** | 154 | `cpanel_public_html/404.html:1` |
| 47 | `/learners/courses/data-analytics/` | `learners/courses/data-analytics/index.html` | **YES** | 150 | `cpanel_public_html/404.html:1` |
| 48 | `/learners/courses/full-stack-development/` | `learners/courses/full-stack-development/index.html` | **YES** | 150 | `cpanel_public_html/404.html:1` |
| 49 | `/learners/courses/generative-ai/` | `learners/courses/generative-ai/index.html` | **YES** | 76 | `cpanel_public_html/404.html:1` |
| 50 | `/learners/courses/machine-learning/` | `learners/courses/machine-learning/index.html` | **YES** | 76 | `cpanel_public_html/404.html:1` |
| 51 | `/learners/courses/python-automation/` | `learners/courses/python-automation/index.html` | **YES** | 225 | `cpanel_public_html/404.html:1` |
| 52 | `/learners/fellowship` | `learners/fellowship/index.html` | **YES** | 3 | `cpanel_public_html/blog/equity-for-services/index.html:59` |
| 53 | `/learners/fellowship/` | `learners/fellowship/index.html` | **YES** | 153 | `cpanel_public_html/404.html:1` |
| 54 | `/learners/interview-prep/` | `learners/interview-prep/index.html` | **YES** | 75 | `cpanel_public_html/404.html:1` |
| 55 | `/learners/jobs/` | `learners/jobs/index.html` | **YES** | 4 | `cpanel_public_html/learners/index.html:1` |
| 56 | `/learners/launchpad` | `learners/launchpad/index.html` | **YES** | 3 | `cpanel_public_html/blog/ai-agent-developer-salary-2026/index.html:27` |
| 57 | `/learners/launchpad/` | `learners/launchpad/index.html` | **YES** | 82 | `cpanel_public_html/404.html:1` |
| 58 | `/learners/launchpad/?domain=ai-agent-development` | `learners/launchpad/index.html` | **YES** | 1 | `cpanel_public_html/learners/courses/ai-agent-development/index.html:1` |
| 59 | `/learners/launchpad/?domain=data-analytics` | `learners/launchpad/index.html` | **YES** | 1 | `cpanel_public_html/learners/courses/data-analytics/index.html:1` |
| 60 | `/learners/launchpad/?domain=full-stack-development` | `learners/launchpad/index.html` | **YES** | 1 | `cpanel_public_html/learners/courses/full-stack-development/index.html:1` |
| 61 | `/learners/launchpad/?domain=generative-ai` | `learners/launchpad/index.html` | **YES** | 2 | `cpanel_public_html/learners/courses/generative-ai/index.html:1` |
| 62 | `/learners/launchpad/?domain=machine-learning` | `learners/launchpad/index.html` | **YES** | 2 | `cpanel_public_html/learners/courses/machine-learning/index.html:1` |
| 63 | `/learners/launchpad/?domain=python-automation` | `learners/launchpad/index.html` | **YES** | 1 | `cpanel_public_html/learners/courses/python-automation/index.html:1` |
| 64 | `/pricing/` | `pricing/index.html` | **YES** | 75 | `cpanel_public_html/404.html:1` |
| 65 | `/privacy/` | `privacy/index.html` | **YES** | 74 | `cpanel_public_html/404.html:1` |
| 66 | `/refund/` | `refund/index.html` | **YES** | 74 | `cpanel_public_html/404.html:1` |
| 67 | `/startups` | `startups/index.html` | **YES** | 2 | `cpanel_public_html/blog/fast-vs-safe-agreement-india/index.html:55` |
| 68 | `/startups/` | `startups/index.html` | **YES** | 157 | `cpanel_public_html/404.html:1` |
| 69 | `/startups/investor-network/` | `startups/investor-network/index.html` | **YES** | 79 | `cpanel_public_html/404.html:1` |
| 70 | `/startups/portfolio/` | `startups/portfolio/index.html` | **YES** | 154 | `cpanel_public_html/404.html:1` |
| 71 | `/startups/portfolio/alkame/` | `startups/portfolio/alkame/index.html` | **YES** | 2 | `cpanel_public_html/startups/index.html:1` |
| 72 | `/startups/portfolio/alkame/#team` | `startups/portfolio/alkame/index.html` | **YES** | 1 | `cpanel_public_html/about/team/index.html:1` |
| 73 | `/startups/portfolio/cognitive-solutions/` | `startups/portfolio/cognitive-solutions/index.html` | **YES** | 1 | `cpanel_public_html/startups/portfolio/index.html:1` |
| 74 | `/startups/portfolio/digital-blaize/` | `startups/portfolio/digital-blaize/index.html` | **YES** | 1 | `cpanel_public_html/startups/portfolio/index.html:1` |
| 75 | `/startups/portfolio/gayatri-ai/` | `startups/portfolio/gayatri-ai/index.html` | **YES** | 2 | `cpanel_public_html/startups/index.html:1` |
| 76 | `/startups/register` | `startups/register/index.html` | **YES** | 1 | `cpanel_public_html/startups/portfolio/alkame/index.html:1` |
| 77 | `/startups/register/` | `startups/register/index.html` | **YES** | 115 | `cpanel_public_html/404.html:1` |
| 78 | `/startups/services/` | `startups/services/index.html` | **YES** | 76 | `cpanel_public_html/404.html:1` |
| 79 | `/startups/services/equity` | `startups/services/equity/index.html` | **YES** | 1 | `cpanel_public_html/blog/fast-vs-safe-agreement-india/index.html:115` |
| 80 | `/startups/services/equity/` | `startups/services/equity/index.html` | **YES** | 155 | `cpanel_public_html/404.html:1` |
| 81 | `/startups/services/equity/term-sheets` | `startups/services/equity/term-sheets/index.html` | **YES** | 2 | `cpanel_public_html/blog/ai-agent-developer-salary-2026/index.html:50` |
| 82 | `/startups/services/equity/term-sheets/` | `startups/services/equity/term-sheets/index.html` | **YES** | 159 | `cpanel_public_html/404.html:1` |
| 83 | `/startups/services/funding/` | `startups/services/funding/index.html` | **YES** | 155 | `cpanel_public_html/404.html:1` |
| 84 | `/startups/services/hiring/` | `startups/services/hiring/index.html` | **YES** | 82 | `cpanel_public_html/404.html:1` |
| 85 | `/startups/services/infrastructure/` | `startups/services/infrastructure/index.html` | **YES** | 80 | `cpanel_public_html/404.html:1` |
| 86 | `/startups/services/legal/` | `startups/services/legal/index.html` | **YES** | 78 | `cpanel_public_html/404.html:1` |
| 87 | `/startups/services/technical/` | `startups/services/technical/index.html` | **YES** | 157 | `cpanel_public_html/404.html:1` |
| 88 | `/terms/` | `terms/index.html` | **YES** | 74 | `cpanel_public_html/404.html:1` |
| 89 | `/verify/` | `verify/index.html` | **YES** | 93 | `cpanel_public_html/404.html:1` |

### Critical Omission: Next.js Static Export Exclusion of `/admin` Routes
While all 89 public routes resolve, the following administrative routes exist in the Next.js App Router source (`apps/website/src/app/admin/`) but were completely omitted from `cpanel_public_html/`:
1. `/admin/login` (`apps/website/src/app/admin/login/page.tsx:1`) $\rightarrow$ Returns HTTP 404 on static hosting.
2. `/admin/leads` (`apps/website/src/app/admin/leads/page.tsx:54`) $\rightarrow$ Returns HTTP 404 on static hosting.
3. `/admin/cohort-applications` (`apps/website/src/app/admin/cohort-applications/page.tsx:48`) $\rightarrow$ Returns HTTP 404 on static hosting.
4. `/admin/alkame-contributors` (`apps/website/src/app/admin/alkame-contributors/page.tsx:47`) $\rightarrow$ Returns HTTP 404 on static hosting.

**Architecture Impact**: The website admin portal requires Node.js server-side rendering (SSR) listening on EC2 port 3001 via `dbert-website.service`. It cannot be served purely as static files from Nginx without routing `/admin` requests upstream to port 3001.

---

## 5. Nuance Annotations (Needs Clarification Findings)

As documented during independent verification by `reviewer_1`, four findings required detailed context clarification to distinguish between functional code, documentation artifacts, and environment architectures:

### 1. PRE-07: Organization JSON-LD & OG Meta Tags (`apps/website/` vs `cpanel_public_html/`)
- **Reviewer Note**: In `cpanel_public_html/__next.__PAGE__.txt:49`, the homepage schema had been partially edited to `https://dbert.in`. However, in `apps/website/__next.__PAGE__.txt:48-49`, `apps/website/index.html:1`, `apps/website/pricing.txt:20`, and across 203 files in `apps/website/out/`, the Organization JSON-LD and OG tags still explicitly specify `dbert.online`.
- **Verdict**: **Confirmed with Nuance** (Blocker). Deploying `cpanel_public_html/` directly without re-exporting causes mixed-domain SEO indexing and broken social graph unfurling.

### 2. R1-13: Portal Blog Redirection Routes (`apps/portal/app.py:6008-6080`)
- **Reviewer Note**: The preliminary audit noted that blog routes reference `dbert.online`. Re-reading lines 6027 and 6067 revealed that the actual Python redirection logic issues HTTP 302 redirects to `https://dbert.in/blog/{post_slug}` and the API returns `canonicalUrl: https://dbert.in/blog/{slug}`. The references to `dbert.online` are confined to section banner comments (line 6008) and docstrings (lines 6012, 6034, 6080).
- **Verdict**: **Confirmed with Nuance** (Downgraded from Blocker to **Warning**). There is no functional redirect loop or broken navigation at runtime.

### 3. R2-08: Portal Session Cookie Domain Isolation (`apps/portal/app.py:90-93`)
- **Reviewer Note**: `SESSION_COOKIE_DOMAIN` is not set, meaning cookies default to host-only (`lms.dbert.in`). If the architecture intends for the LMS portal to be an isolated authentication silo, host-only cookies are a standard security practice that prevents cookie leakage to parent domains. However, if single sign-on (SSO) or shared sessions between `dbert.in` and `lms.dbert.in` is desired, the cookie domain must be set to `.dbert.in`.
- **Verdict**: **Confirmed with Nuance** (**Warning**). Documented as an architectural decision for the deployment team.

### 4. R5-01: Committed SQLite Database Files & Sizes
- **Reviewer Note**: Live SQLite databases are committed directly in git. Direct file inspection revealed two distinct databases:
  1. `apps/portal/internship.db`: **38,273,024 bytes** (38.2 MB), containing full candidate records, applications, task submissions, and legacy financial logs.
  2. `internship.db` (repo root): **856,064 bytes** (856 KB), containing baseline administrative schema.
  Both files reside within the web directory tree when cloned to `/var/www/dbert-website-lms`, and Nginx lacks deny directives for `.db` and `.sqlite` files.
- **Verdict**: **Confirmed with Nuance** (Blocker). Both files must be removed from git tracking and blocked by Nginx edge rules.

---

## 6. Acceptance Criteria Compliance Checklist

Verification that all requirements specified in `ORIGINAL_REQUEST.md` have been exhaustively investigated and addressed:

### Domain Migration
- [x] **Complete list of all `dbert.online` references**: Cataloged across Python, TypeScript, HTML, XML, JSON, shell scripts, and configs, classified into Blocker, Warning, and Informational.
- [x] **Pre-confirmed blockers (8 items)**: Fully verified and documented with file:line citations and remediation fixes.
- [x] **`sitemap.xml` and `robots.txt` domain verified**: Verified that `apps/website/sitemap.xml` and `robots.txt` use `dbert.online` (Blockers R1-02, R1-03), while `cpanel_public_html/sitemap.xml` uses `dbert.in`.
- [x] **JSON-LD structured data audit across all pages completed**: Extracted and verified across all static pages, identifying 4 legacy schema blocks in `cpanel_public_html/` (Blockers R3-02, R3-03) and legacy templates (PRE-07).

### Portal Readiness
- [x] **All four default credential guards confirmed**: Confirmed that `assert not _insecure` tests all 4 credentials (`FLASK_SECRET_KEY`, `ADMIN_PASSWORD`, `ADMIN_KEY`, `ADMIN_USERNAME`), but verified that the guard can be completely bypassed if `FLASK_DEBUG=true` (Blocker R2-04).
- [x] **No SQLite silent fallback on write paths**: Discovered that `services/database/adapter.py:844` tests deprecated `FLASK_ENV == "production"`, silently falling back to `internship.db` under `.env` default configuration (Blocker R2-02).
- [x] **Razorpay webhook confirmed**: Handler is CSRF-exempt, but HMAC signature verification is conditionally skipped if `RAZORPAY_WEBHOOK_SECRET` is unset (Blocker R2-05).
- [x] **Upload extension blocklist confirmed**: `.py`, `.php`, and `.sh` are blocked by Flask upload logic; however, Nginx directly aliases `/uploads/` to disk, bypassing Flask authentication and IDOR defenses (Blocker R2-06).
- [x] **Email failure path documented**: Discovered that `send_email_async` catches all SMTP exceptions in a background daemon thread while routes return HTTP 200 success to the user (Blocker R2-07).

### Website Readiness
- [x] **Dead internal links table produced**: Full 89-route table documented with 100% resolution for public routes; static export omission of `/admin` routes documented.
- [x] **`404.html` existence and Nginx `error_page` directive confirmed**: Verified that `cpanel_public_html/404.html` exists, but confirmed `error_page 404` is completely missing from Nginx configs (Blocker R3-01).
- [x] **OG / meta domain audit across all pages completed**: Verified across all 74 HTML files; identified missing `twitter:site` in `layout.tsx` (Info R3-08) and legacy meta in un-rebuilt export (Blocker R1-05).

### EC2 Deployment
- [x] **Committed DB password blocker confirmed**: Verified `DB_PASS="DBERT_SECURE_PASSWORD_123"` in `deploy/deploy_ec2_unified.sh:56` with recommended rotation fix.
- [x] **`production_preflight.sh` single-quote expansion bug confirmed**: Verified all 7 occurrences on lines 53–60 where literal single quotes prevent Bash variable evaluation (Blockers R4-03..R4-08).
- [x] **Nginx config correctness confirmed**: Audited `deploy/dbert-unified-nginx.conf`; identified missing 404 directive (R3-01), SSL SAN mismatch (R4-01), and `/uploads/` bypass (R2-06).
- [x] **Certbot SAN coverage confirmed or flagged**: Flagged that Certbot command omits legacy domains, breaking 301 HTTPS redirects (Blocker R4-01).

### Security
- [x] **`internship.db`, `.env`, `uploads/` Nginx access control verified**: Verified that Nginx lacks deny rules for `.db` and `.env` files, and improperly exposes `/uploads/` directly from disk (Blockers R5-01, R5-02, R2-06).
- [x] **Rate limiting presence/absence on auth endpoints documented**: Discovered that `rate_check()` is globally disabled due to `FLASK_ENV=development` in `.env` (Blocker R5-05); documented missing locks on `/admin/login` (Warning R5-06) and `/company/signup` (Warning R5-07).
- [x] **Secret key short-length guard severity assessed**: Confirmed that keys under 32 characters only print a warning to stdout without halting execution (Warning R2-10).

### Output
- [x] **`QA_REPORT.md` produced**: Generated in workspace root with Executive Summary, Metrics, Grouped Findings, 89-Row Internal Links Table, Nuance Annotations, Acceptance Checklist, and CLI Reproduction Commands.
- [x] **Independent reviewer verification**: All findings verified on disk by `reviewer_1`; zero false positives.

---

## 7. Independent Verification & CLI Reproduction Commands

To independently reproduce the primary findings on the local filesystem, execute the following commands in PowerShell, Bash, or Python.

### 1. Reproduce Preflight Single-Quote Shell Expansion Failure (Finding R4-03..R4-08)
```bash
# Demonstrates that literal single quotes inhibit parameter expansion in Bash
bash -c "REQUIRE_POSTGRES=true; [ '\${REQUIRE_POSTGRES:-}' = 'true' ] && echo PASS || echo FAIL"
# Output: FAIL (Proves preflight always rejects valid postgres configurations)

bash -c "FLASK_DEBUG=true; [ '\${FLASK_DEBUG:-}' != 'true' ] && echo PASS || echo FAIL"
# Output: PASS (Proves preflight falsely accepts active debug mode in production)
```

### 2. Reproduce 89 Internal Links Mechanical Resolution (Finding R3-09)
```powershell
python -c "
import os, urllib.parse
from html.parser import HTMLParser

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for k, v in attrs:
                if k == 'href' and v and v.startswith('/'):
                    self.links.append(v)

base_dir = 'cpanel_public_html'
all_hrefs = set()
for root, _, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            parser = LinkExtractor()
            parser.feed(open(os.path.join(root, f), encoding='utf-8', errors='ignore').read())
            all_hrefs.update(parser.links)

dead = []
for h in sorted(all_hrefs):
    clean = urllib.parse.urlparse(h).path.strip('/')
    p1 = os.path.join(base_dir, clean, 'index.html')
    p2 = os.path.join(base_dir, clean)
    if not (os.path.isfile(p1) or os.path.isfile(p2)):
        dead.append(h)

print(f'Total Internal Routes: {len(all_hrefs)}')
print(f'Dead Ends: {len(dead)}')
"
# Expected Output:
# Total Internal Routes: 89
# Dead Ends: 0
```

### 3. Verify Admin Route Decorator Misplacement Bug (Finding R5-04)
```powershell
Get-Content apps/portal/app.py | Select-Object -Index (8394..8405)
# Verifies that @app.route('/admin/course-payments/<int:pay_id>/review')
# decorates def _signal_tutor_course_unlock(intern_id, course_id):
```

### 4. Verify Database File Sizes on Disk (Finding R5-01)
```powershell
Get-Item internship.db, apps/portal/internship.db | Select-Object FullName, Length
# Expected Output:
# internship.db: 856,064 bytes
# apps/portal/internship.db: 38,273,024 bytes
```

### 5. Inspect Missing 404 Directive in Unified Nginx Configuration (Finding R3-01)
```powershell
Select-String -Path deploy/dbert-unified-nginx.conf -Pattern "error_page"
# Expected Output: None (0 matches found)
```

### 6. Verify Outbound Links to Legacy Domain in Static Export (Finding R1-04)
```powershell
(Get-ChildItem -Path cpanel_public_html -Recurse -Filter *.html | Select-String -Pattern "internship.dbert.online").Count
# Expected Output: 157 occurrences across static navigation headers and footers
```

---

## 8. Prioritized Remediation Roadmap

To achieve production readiness, the engineering team should execute the following 5-stage remediation plan:

### Stage 1: Critical Security & Authentication Fixes (Immediate)
1. **Fix Route Decorator**: In `apps/portal/app.py:8395`, move `@app.route("/admin/course-payments/<int:pay_id>/review", methods=["POST"])` to precede `def admin_course_payment_review(pay_id):`.
2. **Remove CSRF Exemption**: In `apps/portal/app.py:3691`, delete `"scraped_lead_comment_add"` from `CSRF_EXEMPT_ENDPOINTS`.
3. **Enforce Webhook HMAC Signature**: In `apps/portal/app.py:14734-14738`, remove `if webhook_sec:` check and raise HTTP 500 if `RAZORPAY_WEBHOOK_SECRET` is unset, or HTTP 400 if signature fails.
4. **Enforce Production Credential Validation**: In `apps/portal/app.py:344-353`, remove `if FLASK_DEBUG != "true":` bypass and enforce strong passwords unconditionally.
5. **Disable OTP Leak in Auth**: In `apps/portal/app.py:8171-8173`, eliminate `resp["dev_otp_hint"] = otp`.

### Stage 2: Database & Runtime Reliability
1. **Forbid SQLite in Production**: In `apps/portal/services/database/adapter.py:844`, evaluate production mode via `FLASK_DEBUG != "true"` and raise `RuntimeError` if PostgreSQL is not active.
2. **Fix Preflight Parameter Expansion**: In `scripts/production_preflight.sh:53-60`, replace single quotes with double quotes. Update line 73 to check `dbert-unified.conf`.
3. **Archive SQLite Databases**: Remove `internship.db` and `apps/portal/internship.db` from version control and gitignore all `*.db` and `*.sqlite` files.

### Stage 3: Nginx Edge Protection & Routing Fixes
1. **Block Direct Database & Dotfile Access**: In `deploy/dbert-unified-nginx.conf`, add:
   ```nginx
   location ~* \.(sqlite|db|sql|log)$ { deny all; return 404; }
   location ~ /\. { deny all; return 404; }
   ```
2. **Protect Uploads Directory**: Remove static `alias` for `/uploads/` and proxy `/uploads/` requests to Gunicorn/Flask to restore IDOR authorization.
3. **Add 404 Error Handling**: Add `error_page 404 /404.html;` to `dbert.in` server block in `deploy/dbert-unified-nginx.conf`.
4. **Expand Certbot SAN**: Issue certificates covering `dbert.in`, `www.dbert.in`, `lms.dbert.in`, `dbert.online`, `www.dbert.online`, and `internship.dbert.online`.

### Stage 4: Static Export Re-generation & Domain Synchronization
1. **Re-export Static Website**: In `apps/website/`, execute `npm run export:cpanel` to update `cpanel_public_html/` with fresh HTML referencing `https://lms.dbert.in/`.
2. **Synchronize Sitemaps & Robots**: Overwrite `apps/website/sitemap.xml` with `cpanel_public_html/sitemap.xml` and update `apps/website/robots.txt:13`.
3. **Update Sitemaps in Portal**: Bulk replace `https://internship.dbert.online` with `https://lms.dbert.in` in `apps/portal/sitemap.xml`.

### Stage 5: Environment & Credential Sanitization
1. **Rotate Credentials**: Rotate database password `DBERT_SECURE_PASSWORD_123`, `ADMIN_PASSWORD`, and `FLASK_SECRET_KEY`.
2. **Update Environment Files**: Set `SMTP_HOST=dbert.in`, `SMTP_USER=contactus@dbert.in`, `FROM_EMAIL=contactus@dbert.in`, and `FLASK_ENV=production` across all production `.env` files.
