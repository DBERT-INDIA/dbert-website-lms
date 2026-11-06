# R1 Domain Migration Audit: `dbert.online` → `dbert.in`

**Auditor**: explorer_r1 (Role: Domain Migration Auditor)  
**Date**: 2026-10-25  
**Working Directory**: `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r1`  
**Report Destination**: `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r1\handoff.md`  

---

## Executive Summary

A comprehensive repository-wide static code analysis was performed across all Python files, HTML pages, TypeScript/JavaScript modules, CSS stylesheets, shell scripts, Nginx configurations, environment (`.env`) files, JSON specifications, XML sitemaps, and Markdown documentation.

The repository is in the midst of migrating from the legacy domains `dbert.online` (main website) and `internship.dbert.online` (portal) to `dbert.in` and `lms.dbert.in` respectively.

### Summary Metrics
| Severity | Count | Primary Impact |
|---|---|---|
| **Blocker** | **18 distinct locations** (affecting 300+ generated files/routes) | Silent email failure, credential lockouts, CORS rejection, crawler index poisoning, and broken user navigation sending traffic to obsolete domain |
| **Warning** | **22 distinct locations** | Misleading anchor text, obsolete comments/docstrings, legacy deployment guides, and sample test values |
| **Informational** | **7 locations** | Intentional 301 Nginx redirect rules, `.htaccess` rewrite rules, and historical changelog entries |

---

## 1. Observation

Direct observations citing exact relative file paths, line numbers, snippets, and verified statuses.

### 1.1 Verification of Pre-Confirmed Findings (R1 Mandate)

| # | File Path : Line | Pre-Scan Claim | Verified Content (Verbatim Snippet) | Status | Classification |
|---|---|---|---|---|---|
| **1** | `apps/portal/.env:27` | `SMTP_HOST=dbert.online` | `SMTP_HOST=dbert.online` | **CONFIRMED** | **Blocker** |
| **2** | `apps/portal/.env:29` | `SMTP_USER=contactus@dbert.online` | `SMTP_USER=contactus@dbert.online` | **CONFIRMED** | **Blocker** |
| **3** | `apps/portal/.env:31` | `FROM_EMAIL=contactus@dbert.online` | `FROM_EMAIL=contactus@dbert.online` | **CONFIRMED** | **Blocker** |
| **4** | `apps/portal/app.py:304` | `SMTP_HOST` code default = `"dbert.online"` | `SMTP_HOST = os.environ.get("SMTP_HOST", "dbert.online")` | **CONFIRMED** | **Blocker** |
| **5** | `apps/portal/app.py:2690` | `staff_email = f"{ADMIN_USERNAME}@dbert.online"` hardcode | `staff_email = f"{ADMIN_USERNAME}@dbert.online"` | **CONFIRMED** | **Blocker** |
| **7** | `cpanel_public_html/__next.__PAGE__.txt` (and `apps/website/__next.__PAGE__.txt:48-49`, `apps/website/index.html:1`, `apps/website/pricing.txt:20`) | JSON-LD schema `@type: Organization` has `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, and `"email": "contactus@dbert.online"` | Line 48: `{"property":"og:image","content":"https://dbert.online/og-image.jpg"}`<br>Line 49: `"url":"https://dbert.online","logo":"https://dbert.online/logo.svg","email":"contactus@dbert.online"` | **CONFIRMED** | **Blocker** |
| **8** | `apps/portal/templates/seo_landing.html:133` | anchor tag `href="https://dbert.in"` but link text reads `dbert.online` | `&copy; 2026 DBERT Labs. All rights reserved. \| <a href="https://dbert.in" class="underline text-gray-400">dbert.online</a>` | **CONFIRMED** | **Warning** |

*Note on Item 7 context*: In `cpanel_public_html/__next.__PAGE__.txt`, the homepage schema was partially updated to `dbert.in`, but `apps/website/__next.__PAGE__.txt:48-49`, `apps/website/index.html:1`, `apps/website/pricing.txt:20`, and 203 static export files across `apps/website/` and `apps/website/out/` still contain `dbert.online` in the JSON-LD schema and OG tags. Furthermore, all 110 HTML pages in `cpanel_public_html/` still contain active navigation links pointing to `https://internship.dbert.online/`.

---

### 1.2 Environment Files (`.env`, `.env.example`, `.env.production.sample`)

#### 1. `apps/portal/.env`
- **Lines 27, 29, 31**:
  ```env
  27: SMTP_HOST=dbert.online
  28: SMTP_PORT=465
  29: SMTP_USER=contactus@dbert.online
  30: SMTP_PASS="hY36cI8t;*3[jYA8"
  31: FROM_EMAIL=contactus@dbert.online
  ```
  - **Classification**: **Blocker**
  - **Impact**: All live transactional emails sent by the portal connect to `dbert.online` SMTP and send emails with From header `contactus@dbert.online`. If `dbert.online` MX/mailserver records lapse or fail SPF/DKIM validation against `dbert.in`, emails will fail silently or land in spam. User replies will be sent to the old defunct domain mailbox.
  - **Recommended Fix**: Update to:
    ```env
    SMTP_HOST=dbert.in
    SMTP_USER=contactus@dbert.in
    FROM_EMAIL=contactus@dbert.in
    ```

#### 2. `apps/portal/.env.staging.example`
- **Lines 34, 36**:
  ```env
  34: SMTP_USER=staging@dbert.online
  35: SMTP_PASS=staging_test_only
  36: FROM_EMAIL=staging@dbert.online
  ```
  - **Classification**: **Warning**
  - **Impact**: When spinning up a staging environment, developers copying this sample will configure staging accounts with the legacy domain.
  - **Recommended Fix**: Change `staging@dbert.online` to `staging@dbert.in`.

#### 3. `dbert-api-package/.env.example`
- **Lines 45, 47, 49**:
  ```env
  45: SMTP_HOST=dbert.online
  46: SMTP_PORT=465
  47: SMTP_USER=contactus@dbert.online
  48: SMTP_PASS=your_smtp_password
  49: FROM_EMAIL=contactus@dbert.online
  ```
  - **Classification**: **Warning**
  - **Impact**: Standalone API package sample configuration instructs developers to configure obsolete domain mail credentials.
  - **Recommended Fix**: Update to `dbert.in` and `contactus@dbert.in`.

#### 4. `dbert-api-package/.env.production.sample`
- **Line 18**:
  ```env
  18: CORS_ORIGINS=https://dbert.online,https://internship.dbert.online
  ```
  - **Classification**: **Blocker**
  - **Impact**: If this package is deployed to production, FastAPI's CORS middleware will only allow requests originating from `dbert.online` and `internship.dbert.online`, completely blocking browser API calls originating from `dbert.in` and `lms.dbert.in`.
  - **Recommended Fix**: Update to:
    ```env
    CORS_ORIGINS=https://dbert.in,https://lms.dbert.in
    ```
- **Lines 33, 35, 37**:
  ```env
  33: SMTP_HOST=dbert.online
  34: SMTP_PORT=465
  35: SMTP_USER=contactus@dbert.online
  36: SMTP_PASS=your_smtp_password
  37: FROM_EMAIL=contactus@dbert.online
  ```
  - **Classification**: **Blocker**
  - **Impact**: Transactional email dispatch routes to obsolete SMTP host and sender address.
  - **Recommended Fix**: Update to `dbert.in` and `contactus@dbert.in`.

---

### 1.3 Portal Application Code (`apps/portal/`)

#### 1. `apps/portal/app.py:304`
- **Snippet**:
  ```python
  304: SMTP_HOST = os.environ.get("SMTP_HOST", "dbert.online")
  ```
  - **Classification**: **Blocker**
  - **Impact**: Code-level default for `SMTP_HOST` fallback is `"dbert.online"`. If `SMTP_HOST` is omitted or unset in any deployment environment, it defaults to the obsolete domain.
  - **Recommended Fix**: Change fallback default to `"dbert.in"` (or `"localhost"` / AWS SES host).

#### 2. `apps/portal/app.py:2690`
- **Snippet**:
  ```python
  2690: staff_email = f"{ADMIN_USERNAME}@dbert.online"
  ```
  - **Classification**: **Blocker**
  - **Impact**: When database seeding or startup initializes the UP3.1 default staff account, the staff account email is created with `@dbert.online`. Admin staff notifications and assignments will route to an unreachable email.
  - **Recommended Fix**: Change to:
    ```python
    staff_email = f"{ADMIN_USERNAME}@dbert.in"
    ```

#### 3. `apps/portal/app.py:6008-6080` (Portal Blog Redirect Routes & API)
- **Snippets**:
  - Line 6008: `# ── Canonical Blog Redirection to dbert.online ────────────────────────────────`
  - Line 6012: `"""Articles live strictly on the main website dbert.online/blog.`
  - Line 6015: `redirects visitors to the canonical live blog post on dbert.online."""`
  - Line 6027: Functional redirect code:
    ```python
    target_url = f"https://dbert.in/blog/{post_slug}"
    return redirect(target_url, code=302)
    ```
  - Line 6031: `# ── Public Blog Sync API for dbert.online Auto-Updates ─────────────────────────`
  - Line 6034: `"""Returns approved/published intern technical writing for dbert.online/blog real-time sync."""`
  - Line 6067: Functional API payload:
    ```python
    "canonicalUrl": f"https://dbert.in/blog/{slug}",
    ```
  - Line 6080: `"""Returns single post detail with markdown for dynamic reader on dbert.online."""`
  - **Classification**: **Warning**
  - **Impact**: The functional redirect routes at lines 6027 and 6067 **already correctly redirect to `https://dbert.in/blog/{slug}`**. However, the comments and docstrings at lines 6008, 6012, 6015, 6031, 6034, and 6080 explicitly reference `dbert.online`. Additionally, if any historical record in the `intern_articles` database table has a non-empty `published_url` starting with `https://dbert.online`, line 6025 (`target_url = art["published_url"]`) would honor it. (Static verification confirmed `intern_articles` table in `apps/portal/internship.db` has 0 rows with `dbert.online`).
  - **Recommended Fix**: Update comments and docstrings to reference `dbert.in/blog`.

#### 4. `apps/portal/cgi-bin/fix_env.cgi:51`
- **Snippet**:
  ```ini
  51: FROM_EMAIL=contactus@dbert.online
  ```
  - **Classification**: **Blocker**
  - **Impact**: If this cPanel diagnostic/maintenance script is executed, it overwrites `.env` and resurrects `FROM_EMAIL=contactus@dbert.online`.
  - **Recommended Fix**: Update line 51 to `FROM_EMAIL=contactus@dbert.in` (or delete the unused `.cgi` file).

#### 5. `apps/portal/deploy/nginx.conf`
- **Snippet**:
  ```nginx
  3:  # Domain: https://internship.dbert.online/
  9:  server_name internship.dbert.online;
  25: server_name internship.dbert.online;
  28: ssl_certificate /etc/letsencrypt/live/internship.dbert.online/fullchain.pem;
  29: ssl_certificate_key /etc/letsencrypt/live/internship.dbert.online/privkey.pem;
  ```
  - **Classification**: **Blocker** (if deployed) / **Warning** (legacy file)
  - **Impact**: Standalone legacy Nginx configuration for portal binds directly to `internship.dbert.online` with obsolete SSL cert paths. If copied into `/etc/nginx/sites-enabled/`, portal will not respond on `lms.dbert.in`.
  - **Recommended Fix**: Replace with redirection or deprecate file in favor of `deploy/dbert-unified-nginx.conf`.

---

### 1.4 Sitemaps and Robots.txt

#### 1. `apps/portal/sitemap.xml:1`
- **Snippet**:
  ```xml
  1: <?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://internship.dbert.online/</loc>...
  ```
  - **Classification**: **Blocker**
  - **Observation**: 664 KB single-line XML containing 85+ canonical `<loc>` tags pointing to `https://internship.dbert.online/...` (e.g. `/jobs`, `/internships`, `/cv/*`, `/program`).
  - **Impact**: When search engines fetch `https://lms.dbert.in/sitemap.xml` (as instructed by `apps/portal/robots.txt:20`), they are fed hundreds of URLs on `internship.dbert.online`, diluting domain authority and causing index churn.
  - **Recommended Fix**: Bulk replace `https://internship.dbert.online` with `https://lms.dbert.in` across the file.

#### 2. `apps/website/sitemap.xml:4-420`
- **Snippet**:
  ```xml
  4:  <loc>https://dbert.online</loc>
  10: <loc>https://dbert.online/pricing</loc>
  16: <loc>https://dbert.online/verify</loc>
  22: <loc>https://dbert.online/privacy</loc>
  ... (70 URLs total)
  ```
  - **Classification**: **Blocker**
  - **Impact**: All 70 static website URLs in this file use `https://dbert.online`. If deployed as the static sitemap, Google will index `dbert.online`.
  - **Recommended Fix**: Replace all `https://dbert.online` with `https://dbert.in`.

#### 3. `apps/website/robots.txt:13`
- **Snippet**:
  ```robots
  13: Sitemap: https://dbert.online/sitemap.xml
  ```
  - **Classification**: **Blocker**
  - **Impact**: Search engine crawlers visiting `robots.txt` are instructed to fetch the sitemap from `https://dbert.online/sitemap.xml`.
  - **Recommended Fix**: Change to:
    ```robots
    Sitemap: https://dbert.in/sitemap.xml
    ```

#### 4. `cpanel_public_html/sitemap.xml` & `cpanel_public_html/robots.txt`
- **Observations**:
  - `cpanel_public_html/sitemap.xml`: Contains 70 `<loc>` entries, **all correctly formatted as `https://dbert.in/...`**. 0 occurrences of `dbert.online`.
  - `cpanel_public_html/robots.txt`: Line 13: `Sitemap: https://dbert.in/sitemap.xml`.
  - **Classification**: **Clean / No defect**.

---

### 1.5 Deployed Static Website Pages (`cpanel_public_html/` and `apps/website/out/`)

#### 1. Outbound Portal Links Across All 110 HTML Pages in `cpanel_public_html/`
- **Observation**:
  Every HTML page in `cpanel_public_html/` (110 files total, including `index.html`, `404.html`, `about/index.html`, `learners/index.html`, `startups/index.html`, `ai-solutions/index.html`, etc.) contains hardcoded header, drawer menu, and footer links:
  ```html
  <a href="https://internship.dbert.online/" class="btn btn-primary btn-sm" target="_blank" rel="noopener noreferrer">Apply for Fellowship</a>
  <a href="https://internship.dbert.online/jobs" target="_blank" rel="noopener noreferrer">Job Board</a>
  <a href="https://internship.dbert.online/apply" ...>Apply for Fellowship</a>
  <a href="https://internship.dbert.online/internships/booking-system-development-intern-mumbai-remote-50" ...>
  <a href="https://internship.dbert.online/internships/full-stack-development" ...>
  ```
  Total count: **157 occurrences in `cpanel_public_html`**.
- **Root Cause**:
  The Next.js source code in `apps/website/src/components/layout/Footer.tsx` and `MegaMenu.tsx` was previously updated to `https://lms.dbert.in/`, but `cpanel_public_html/` was generated from a build prior to that change and was never rebuilt.
- **Classification**: **Blocker**
- **Impact**: Real users visiting `https://dbert.in` who click any CTA button ("Apply for Fellowship", "Job Board", or any internship link in footer) are taken to `https://internship.dbert.online/` instead of `https://lms.dbert.in/`.
- **Recommended Fix**:
  Run `npm run build` inside `apps/website`, then execute `python scripts/stage_cpanel_export.py` to regenerate `cpanel_public_html` with verified `lms.dbert.in` URLs.

#### 2. JSON-LD Schema and OG Meta Tags in Stale Export Files (`apps/website/out/` and `apps/website/`)
- **Observation**:
  203 files in `apps/website/` and `apps/website/out/` (including `apps/website/__next.__PAGE__.txt`, `apps/website/index.html`, `apps/website/pricing.txt`, `apps/website/out/**/*.html`) contain:
  ```json
  "og:image": "https://dbert.online/og-image.jpg",
  "twitter:image": "https://dbert.online/og-image.jpg",
  "@context": "https://schema.org",
  "@type": "Organization",
  "url": "https://dbert.online",
  "logo": "https://dbert.online/logo.svg",
  "email": "contactus@dbert.online"
  ```
- **Classification**: **Blocker**
- **Impact**: Staged export or rebuild pipeline drawing from `apps/website/out` distributes `dbert.online` structured data to production.
- **Recommended Fix**: Rebuild static export from `apps/website/src/` where `metadataBase` and `org-schema` now resolve to `https://dbert.in`.

---

### 1.6 Nginx Configurations under `deploy/`

#### 1. `deploy/dbert-unified-nginx.conf`
- **Lines 11, 24-34, 36-46**:
  ```nginx
  11: server_name dbert.in www.dbert.in lms.dbert.in dbert.online www.dbert.online internship.dbert.online;
  ...
  24: # Redirect legacy dbert.online -> https://dbert.in
  25: server {
  26:     listen 443 ssl http2;
  27:     listen [::]:443 ssl http2;
  28:     server_name dbert.online www.dbert.online;
  29: 
  30:     ssl_certificate /etc/letsencrypt/live/dbert.in/fullchain.pem;
  31:     ssl_certificate_key /etc/letsencrypt/live/dbert.in/privkey.pem;
  32: 
  33:     return 301 https://dbert.in$request_uri;
  34: }
  35: 
  36: # Redirect legacy internship.dbert.online -> https://lms.dbert.in
  37: server {
  38:     listen 443 ssl http2;
  39:     listen [::]:443 ssl http2;
  40:     server_name internship.dbert.online;
  41: 
  42:     ssl_certificate /etc/letsencrypt/live/dbert.in/fullchain.pem;
  43:     ssl_certificate_key /etc/letsencrypt/live/dbert.in/privkey.pem;
  44: 
  45:     return 301 https://lms.dbert.in$request_uri;
  46: }
  ```
  - **Classification**: **Informational** (Intentional redirect rules as permitted by R1).
  - **Critical Caveat / Warning**:
    The SSL certificates specified at lines 30-31 and 42-43 use `/etc/letsencrypt/live/dbert.in/fullchain.pem`. In `deploy/deploy_ec2_unified.sh:186`, certbot is invoked with:
    `sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in`
    Because this certificate will **NOT** include `dbert.online`, `www.dbert.online`, or `internship.dbert.online` in its Subject Alternative Names (SAN), HTTPS requests hitting `https://dbert.online` will abort with `SSL_ERROR_BAD_CERT_DOMAIN` before the Nginx 301 redirect is served.
  - **Recommended Fix**: If legacy domains point DNS to this EC2 IP, expand the certbot SAN command:
    `sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online`

#### 2. `deploy/dbert-portal-nginx.conf`
- **Lines 3, 9, 25, 28, 29**:
  ```nginx
  3:  # Domain: https://internship.dbert.online/
  9:  server_name internship.dbert.online;
  25: server_name internship.dbert.online;
  28: ssl_certificate /etc/letsencrypt/live/internship.dbert.online/fullchain.pem;
  29: ssl_certificate_key /etc/letsencrypt/live/internship.dbert.online/privkey.pem;
  ```
  - **Classification**: **Blocker** (if used) / **Warning** (legacy file).
  - **Impact**: Obsolete standalone portal configuration.
  - **Recommended Fix**: Add a deprecation banner or delete file to ensure operators use `dbert-unified-nginx.conf`.

#### 3. `deploy/dbert-website-nginx.conf`
- **Lines 3, 9, 25, 29, 30**:
  ```nginx
  3:  # Domain: https://dbert.online/
  9:  server_name dbert.online www.dbert.online;
  25: server_name dbert.online www.dbert.online;
  29: ssl_certificate /etc/letsencrypt/live/dbert.online/fullchain.pem;
  30: ssl_certificate_key /etc/letsencrypt/live/dbert.online/privkey.pem;
  ```
  - **Classification**: **Blocker** (if used) / **Warning** (legacy file).
  - **Impact**: Obsolete standalone website configuration.
  - **Recommended Fix**: Add deprecation notice or delete file.

---

### 1.7 Deployment Guides & Documentation (`deploy/` & root)

| File Path : Line | Verbatim Content | Classification | Recommended Fix |
|---|---|---|---|
| `deploy/FILEZILLA_DEPLOYMENT_GUIDE.md:19` | `- (Optional for 301 redirects): dbert.online, internship.dbert.online -> A records to YOUR_EC2_IP` | **Informational** | Valid DNS instruction for legacy 301 redirects. |
| `deploy/FIRST_TIME_EC2_DEPLOYMENT.md:134-156` | `sudo cp ... /etc/nginx/sites-available/internship.dbert.online`<br>`sudo certbot --nginx -d internship.dbert.online` | **Warning** | Guide describes deploying `internship.dbert.online`. Update guide to `lms.dbert.in`. |
| `DBERT_LMS_MASTER_DEVELOPMENT_HARDENING_PLAN.md:6,641` | `Primary production portal: https://internship.dbert.online/`<br>`mailer.dbert.online` | **Warning** | Update doc reference to `https://lms.dbert.in/`. |
| `DBERT_WEBSITE_UIUX_REDESIGN_PHASE_PLAN.md:3,45,1102` | `Production website: https://dbert.online`<br>`break internship.dbert.online links` | **Warning** | Historical planning documentation. Update or annotate. |
| `WEBSITE_ROUTE_INVENTORY.md:4` | `Production URL: https://dbert.online` | **Warning** | Update to `https://dbert.in`. |
| `WEBSITE_UIUX_PHASE_PLAN.md:4,140,171` | Mentions `dbert.online` as production URL | **Warning** | Historical planning documentation. |
| `WEBSITE_UIUX_PRODUCTION_PREFLIGHT.md:7,38,82` | `Target Domain: https://dbert.online` | **Warning** | Update target domain to `https://dbert.in`. |
| `WEBSITE_UIUX_PROGRESS.md:29` | Historical changelog entry recording Phase 14 commit `b23ccb6` | **Informational** | Valid historical log; no change required. |
| `.agent/FINAL_RELEASE_GATE_REPORT.md:4` | `Primary Production Portal: https://internship.dbert.online/` | **Warning** | Update release report to `https://lms.dbert.in/`. |

---

### 1.8 Standalone Backend Package (`dbert-api-package/`)

| File Path : Line | Verbatim Snippet | Classification | Recommended Fix |
|---|---|---|---|
| `dbert-api-package/backend/core/config.py:65` | `SMTP_HOST: str = os.environ.get("SMTP_HOST", "dbert.online")` | **Blocker** | Change default to `"dbert.in"` |
| `dbert-api-package/backend/core/config.py:67` | `SMTP_USER: str = os.environ.get("SMTP_USER", "contactus@dbert.online")` | **Blocker** | Change default to `"contactus@dbert.in"` |
| `dbert-api-package/backend/core/config.py:69` | `FROM_EMAIL: str = os.environ.get("FROM_EMAIL", "contactus@dbert.online")` | **Blocker** | Change default to `"contactus@dbert.in"` |
| `dbert-api-package/backend/api/v1/auth/router.py:152` | `token_data = {"sub": "admin", "email": f"{settings.ADMIN_USERNAME}@dbert.online", ...}` | **Blocker** | Change to `f"{settings.ADMIN_USERNAME}@dbert.in"` |
| `dbert-api-package/backend/api/v1/auth/router.py:160` | `user={"id": "admin", "email": f"{settings.ADMIN_USERNAME}@dbert.online", ...}` | **Blocker** | Change to `f"{settings.ADMIN_USERNAME}@dbert.in"` |
| `dbert-api-package/.env.production.sample:18` | `CORS_ORIGINS=https://dbert.online,https://internship.dbert.online` | **Blocker** | Update to `https://dbert.in,https://lms.dbert.in` |
| `dbert-api-package/.env.production.sample:33,35,37` | `SMTP_HOST=dbert.online`<br>`SMTP_USER=contactus@dbert.online`<br>`FROM_EMAIL=contactus@dbert.online` | **Blocker** | Update to `dbert.in` and `contactus@dbert.in` |
| `dbert-api-package/docs/env_vars.md:47,74` | `SMTP_HOST=dbert.online`, `CORS_ORIGINS` docs | **Warning** | Update documentation examples to `dbert.in` |
| `dbert-api-package/docs/integrations.md:38` | `https://internship.dbert.online/api/` | **Warning** | Update documentation example |

---

## 2. Logic Chain

1. **Email Delivery Failure Chain**:
   - Observations 1.1 (#1, #2, #3), 1.2 (#1), 1.3 (#1, #2), 1.8 demonstrate that `SMTP_HOST`, `SMTP_USER`, `FROM_EMAIL`, and `staff_email` are configured with `dbert.online` in both `apps/portal/.env` and as code defaults in `apps/portal/app.py` and `dbert-api-package`.
   - Therefore, unless overridden by an external deployment injection, any email dispatched by the portal (password resets, OTPs, welcome emails, application confirmations) attempts to connect to `dbert.online` mail server with user `contactus@dbert.online`.
   - Because `dbert.online` mail servers may no longer exist or lack SPF/DKIM alignment with `dbert.in`, outgoing mail will fail silently or be rejected by receiving MTAs.

2. **User Navigation Disconnect Chain**:
   - Observation 1.5 (#1) confirms 157 instances of `https://internship.dbert.online/` across all 110 HTML pages in `cpanel_public_html/`.
   - In Next.js static exports, these links are baked into compiled static HTML.
   - Observation 1.5 (#1) reveals that `apps/website/src/components/layout/Footer.tsx` has already been updated to `https://lms.dbert.in/`, but `cpanel_public_html` was never re-exported.
   - Therefore, live users browsing `https://dbert.in` will click navigation buttons and be redirected to `internship.dbert.online`, bypassing the new `lms.dbert.in` portal.

3. **Search Engine Index Poisoning Chain**:
   - Observations 1.4 (#1, #2, #3) show `apps/portal/sitemap.xml` with 85+ entries pointing to `https://internship.dbert.online/...`, `apps/website/sitemap.xml` with 70 entries pointing to `https://dbert.online/...`, and `apps/website/robots.txt` pointing to `https://dbert.online/sitemap.xml`.
   - When Googlebot crawls the deployed sites, it will discover and prioritize the legacy domain URLs, harming organic ranking and preventing the indexing of `dbert.in` and `lms.dbert.in`.

4. **SSL / Nginx Redirection Failure Chain**:
   - Observation 1.6 (#1) shows that `deploy/dbert-unified-nginx.conf` correctly defines 301 redirects for `dbert.online` and `internship.dbert.online`.
   - However, the SSL certificates configured for those virtual hosts point to `/etc/letsencrypt/live/dbert.in/fullchain.pem`.
   - Observation 1.6 (#1) notes that the deploy script `deploy/deploy_ec2_unified.sh:186` only requests certificates for `dbert.in`, `www.dbert.in`, and `lms.dbert.in`.
   - Therefore, any HTTPS user navigating to `https://dbert.online` will trigger a browser SSL certificate mismatch warning before the 301 redirect can occur.

---

## 3. Caveats

1. **Active Live DNS / External Mailservers**: This audit was performed strictly via static code analysis of the local repository. The live DNS status and MX records of `dbert.online` versus `dbert.in` on AWS Route 53 or Cloudflare cannot be verified from local disk.
2. **Database Seed State**: Analysis of `apps/portal/internship.db` confirmed 0 article records with `dbert.online`. However, production PostgreSQL on EC2 may contain records imported from older backups.
3. **Build Artifact Overwriting**: `apps/website/out` and `cpanel_public_html` are static generated assets. Making manual text replacements in `cpanel_public_html` without running a clean Next.js build will be undone the next time `npm run build` or `stage_cpanel_export.py` is executed.

---

## 4. Conclusion

The repository has completed source-level code updates in `apps/website/src/`, but suffers from **three critical categories of blockers**:

1. **Configuration & Code Hardcodes**:
   - `apps/portal/.env` (SMTP_HOST, SMTP_USER, FROM_EMAIL)
   - `apps/portal/app.py:304` (SMTP_HOST fallback default)
   - `apps/portal/app.py:2690` (staff_email hardcode)
   - `apps/portal/cgi-bin/fix_env.cgi:51` (FROM_EMAIL hardcode)
   - `dbert-api-package/.env.production.sample` (CORS_ORIGINS and SMTP)
   - `dbert-api-package/backend/core/config.py` (SMTP defaults)
   - `dbert-api-package/backend/api/v1/auth/router.py:152,160` (Admin JWT email)

2. **Stale Static Builds and Sitemaps**:
   - `cpanel_public_html/` contains 157 outbound links to `https://internship.dbert.online/` across 110 HTML pages.
   - `apps/portal/sitemap.xml` contains hundreds of `internship.dbert.online` URLs.
   - `apps/website/sitemap.xml` contains 70 `dbert.online` URLs.
   - `apps/website/robots.txt` points to `https://dbert.online/sitemap.xml`.

3. **Nginx & SSL Configuration**:
   - `deploy/dbert-portal-nginx.conf` and `deploy/dbert-website-nginx.conf` are obsolete and must not be used.
   - `deploy/deploy_ec2_unified.sh` must include legacy domains in certbot SAN if 301 HTTPS redirects are to function without browser SSL warnings.

---

## 5. Verification Method

To independently verify all findings in this report, execute the following commands in PowerShell from the repository root:

1. **Verify Pre-Confirmed Portal Findings**:
   ```powershell
   Get-Content apps/portal/.env | Select-String "dbert.online"
   Select-String -Path apps/portal/app.py -Pattern "dbert.online"
   Select-String -Path apps/portal/templates/seo_landing.html -Pattern "dbert.online"
   ```

2. **Verify Sitemaps and Robots**:
   ```powershell
   Select-String -Path apps/website/robots.txt -Pattern "dbert.online"
   Select-String -Path apps/website/sitemap.xml -Pattern "dbert.online"
   Select-String -Path apps/portal/sitemap.xml -Pattern "dbert.online"
   ```

3. **Verify cPanel Static HTML Outbound Links**:
   ```powershell
   Get-ChildItem -Path cpanel_public_html -Filter *.html -Recurse | Select-String "internship.dbert.online" | Measure-Object
   ```
   *(Confirms 157 link instances across 110 HTML files).*

4. **Verify Clean Website Source**:
   ```powershell
   Get-ChildItem -Path apps/website/src -Recurse | Select-String "dbert.online"
   ```
   *(Confirms 0 occurrences — source code is already clean).*

5. **Verify API Package Blockers**:
   ```powershell
   Select-String -Path dbert-api-package/backend/core/config.py -Pattern "dbert.online"
   Select-String -Path dbert-api-package/backend/api/v1/auth/router.py -Pattern "dbert.online"
   Select-String -Path dbert-api-package/.env.production.sample -Pattern "dbert.online"
   ```
