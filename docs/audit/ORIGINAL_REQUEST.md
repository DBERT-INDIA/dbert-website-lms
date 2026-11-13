# Original User Request

## 2026-10-25T22:45:09Z

Perform a thorough QA audit of the DBERT website (Next.js static export, served via Nginx on EC2 at `dbert.in`) and the DBERT LMS portal (Flask/Gunicorn app at `lms.dbert.in`), identifying every dead end, silent failure, and production bug before the system goes live. The domain is being migrated from `dbert.online` → `dbert.in`.

Working directory: `c:\Users\user\Desktop\dbert-website-lms`

Integrity mode: development

---

## Pre-confirmed Findings (verified by pre-scan — include in report but do not re-open)

The following issues are already confirmed by a preliminary scan. They must appear in the final report as confirmed blockers, but the team need not re-verify them from scratch:

1. `apps/portal/.env:27` — `SMTP_HOST=dbert.online` (blocker)
2. `apps/portal/.env:29` — `SMTP_USER=contactus@dbert.online` (blocker)
3. `apps/portal/.env:31` — `FROM_EMAIL=contactus@dbert.online` (blocker)
4. `apps/portal/app.py:304` — `SMTP_HOST` code default = `"dbert.online"` (blocker)
5. `apps/portal/app.py:2690` — `staff_email = f"{ADMIN_USERNAME}@dbert.online"` hardcode (blocker)
6. `deploy/deploy_ec2_unified.sh` — DB password `DBERT_SECURE_PASSWORD_123` committed in plaintext (blocker)
7. `cpanel_public_html/__next.__PAGE__.txt` — JSON-LD schema `@type: Organization` has `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, and `"email": "contactus@dbert.online"` (blocker — SEO and structured data uses wrong domain)
8. `apps/portal/templates/seo_landing.html:133` — anchor tag `href="https://dbert.in"` but link text reads `dbert.online` (warning — misleading UX)

---

## Requirements

### R1. Domain Migration Completeness — `dbert.online` → `dbert.in`

Scan every file in the repository (Python, HTML, JS, CSS, shell scripts, Nginx configs, `.env` samples, JSON, markdown docs) for residual references to `dbert.online` that are NOT intentional redirect rules. Classify each reference:
- **Blocker**: will silently send users/emails/API calls to the wrong domain in production
- **Warning**: comment/doc reference that is misleading but not functional
- **Informational**: historical changelog entry or intentional redirect rule

Pay special attention to:
- All `.env`, `.env.example`, `.env.production.sample` files
- All Nginx configs under `deploy/` — intentional `dbert.online → dbert.in` redirect rules are OK; any other reference is a warning or blocker
- `cpanel_public_html/sitemap.xml` and `robots.txt` — all `<loc>` and `Sitemap:` must be `dbert.in`
- All `og:url`, `og:image`, `twitter:site` meta tags in HTML pages
- JSON-LD structured data in all HTML files
- Portal blog redirect routes — confirm they redirect to `dbert.in/blog`, not `dbert.online`

### R2. Portal (Flask/Gunicorn) Production-Readiness Audit

Audit `apps/portal/app.py` and the `routes/`, `services/`, and `templates/` directories for:

1. **Auth & session dead ends**: Login flows that can silently succeed but leave the user with no session — check `SESSION_COOKIE_DOMAIN`, `SESSION_COOKIE_SECURE`, and whether `ProxyFix` is wired with `x_proto=1` so `request.is_secure` returns `True` behind Nginx
2. **CSRF gaps**: Endpoints in `CSRF_EXEMPT_ENDPOINTS` that mutate state without justification; form templates that omit `{{ csrf_field() }}`
3. **Database fallback risk**: Code paths where the SQLite fallback (`internship.db`) silently activates in production — look for `dialect != "postgres"` branches that handle writes (money, enrollments, auth). The `internship.db` file exists at repo root; if accidentally used in production it would silently drop financial writes
4. **Default credential leakage**: Confirm the production guard (`assert not _insecure`) fires for all four defaults (`FLASK_SECRET_KEY`, `ADMIN_PASSWORD`, `ADMIN_KEY`, `ADMIN_USERNAME`). Verify the guard cannot be bypassed by accidentally setting `FLASK_DEBUG=true`
5. **Payment webhook**: Razorpay webhook endpoint must be CSRF-exempt AND have HMAC signature validation active simultaneously — check both conditions are met in the same handler
6. **Upload sandbox**: Check `UPLOAD_FOLDER` path and extension allowlist — confirm `.py`, `.php`, `.sh` cannot be uploaded. Confirm uploaded files are not web-served with execute permission via Nginx
7. **Email silent fails**: SMTP failure paths — does a failed email swallow the exception and return HTTP 200 to the user?
8. **CSP `connect-src`**: Does the Content Security Policy header include `https://lms.dbert.in` and `https://dbert.in` so cross-origin fetch calls between website and portal are not blocked?
9. **ProxyFix wiring**: Is `x_proto=1, x_host=1` set on `ProxyFix` so behind Nginx, `request.scheme == "https"` and session cookies get `Secure` flag?

### R3. Website (Next.js static export) Production-Readiness Audit

Audit `cpanel_public_html/` (the deployed static build) and `apps/website/` source:

1. **Dead internal links**: Enumerate every `href` in every HTML file pointing to `/something` — check whether that path exists as a directory with `index.html` in `cpanel_public_html/`. List all 404 dead ends
2. **Missing or broken 404 page**: Verify `cpanel_public_html/404.html` or `cpanel_public_html/404/index.html` exists; check Nginx config has `error_page 404` directive
3. **`sitemap.xml` domain check**: Every `<loc>` entry must be `https://dbert.in/...`
4. **`robots.txt` check**: `Sitemap:` directive must point to `https://dbert.in/sitemap.xml`
5. **OG / meta tags across all pages**: `og:url`, `og:image`, `twitter:site` must use `dbert.in`
6. **`_next/` asset integrity**: Sample-check that JS/CSS `src` and `href` paths referenced in HTML files (`/_next/static/chunks/...`) actually exist in `cpanel_public_html/_next/static/`
7. **JSON-LD structured data**: Any `Organization`, `WebSite`, `BreadcrumbList` schema markup must use `dbert.in` URLs (pre-scan confirmed the homepage JSON-LD still uses `dbert.online` — flag all pages with this issue)

### R4. EC2 Deployment Configuration Audit

Audit `deploy/` directory:

1. **Nginx unified config** (`dbert-unified-nginx.conf`): All `server_name`, SSL cert paths, upstream `proxy_pass` URLs correct for `dbert.in`. The redirect blocks for `dbert.online → dbert.in` and `internship.dbert.online → lms.dbert.in` are intentional — confirm they are syntactically correct
2. **Systemd service files**: Check `WorkingDirectory`, `ExecStart`, `User/Group` — no old domain references, paths match expected EC2 layout (`/var/www/dbert-website-lms/`)
3. **Deploy script** (`deploy_ec2_unified.sh`): Committed DB password `DBERT_SECURE_PASSWORD_123` is a blocker — document the fix. Also check: certbot command covers `dbert.in`, `www.dbert.in`, and `lms.dbert.in` in SAN
4. **`production_preflight.sh` variable expansion bug**: The script uses single-quoted strings like `'${REQUIRE_POSTGRES:-}'` inside a `check` function — single quotes prevent shell expansion, so every check always sees the literal string `${REQUIRE_POSTGRES:-}` and silently passes. Identify all such occurrences and document the fix (use double quotes)
5. **Port safety**: Next.js :3001 and Gunicorn :5001 — confirm no conflicts with system services

### R5. Security & Hardening Spot Checks

1. **`internship.db` web exposure**: The SQLite file exists at repo root. If cloned to `/var/www/`, it would be under the web root. Check the Nginx config for a rule blocking `.db` file access or blocking the repo root from direct file serving
2. **`uploads/` web exposure**: Is `apps/portal/uploads/` blocked at the Nginx level or restricted to authenticated sessions only?
3. **`.env` web exposure**: Is `.env` blocked by Nginx from public access?
4. **Debug mode leakage**: Any `FLASK_DEBUG=true`, `app.run(debug=True)`, or `DEBUG=True` that could be active in production
5. **Admin panel auth**: Confirm `/admin` routes check `ADMIN_PASSWORD` and are not accidentally open (no missing auth decorator)
6. **Secret key guard severity**: The production guard `print("[WARNING] FLASK_SECRET_KEY is shorter than 32 chars.")` — this prints a warning but does NOT abort. Is this enough? Compare with the `assert not _insecure` guard to determine if short keys can slip through
7. **Rate limiting**: Is there any rate-limiting middleware on login, signup, and password-reset endpoints? Brute force with no rate limit is a production risk

---

## Acceptance Criteria

### Domain Migration
- [ ] Complete list of all `dbert.online` references, each classified as Blocker/Warning/Info
- [ ] Pre-confirmed blockers (8 items above) appear in the report with Confirmed status
- [ ] `sitemap.xml` and `robots.txt` domain verified
- [ ] JSON-LD structured data audit across all pages completed

### Portal Readiness
- [ ] All four default credential guards confirmed to fire correctly (or flagged if they can be bypassed)
- [ ] No SQLite silent fallback on financial/enrollment/auth write paths under PostgreSQL mode
- [ ] Razorpay webhook confirmed: CSRF-exempt AND HMAC-verified
- [ ] Upload extension blocklist confirmed; `.py`/`.php`/`.sh` blocked
- [ ] Email failure path behaviour documented — silent fail = blocker

### Website Readiness
- [ ] Dead internal links table produced (href → does target exist? yes/no)
- [ ] `404.html` existence and Nginx `error_page` directive confirmed
- [ ] OG/meta domain audit across all pages completed

### EC2 Deployment
- [ ] Committed DB password blocker confirmed with recommended fix
- [ ] `production_preflight.sh` single-quote expansion bug confirmed and all occurrences listed with fix
- [ ] Nginx config correctness confirmed (or specific errors flagged)
- [ ] Certbot SAN coverage confirmed or flagged

### Security
- [ ] `internship.db`, `.env`, `uploads/` Nginx access control verified or flagged as missing
- [ ] Rate limiting presence/absence on auth endpoints documented
- [ ] Secret key short-length guard severity assessed

### Output
- [ ] `QA_REPORT.md` produced in the working directory with:
  - Summary table: total Blockers / Warnings / Info findings
  - Findings grouped by category
  - Each finding: **Severity** | **File:Line** | **Description** | **Recommended Fix**
- [ ] A reviewer agent independently re-reads each cited file+line, marks each finding as **Confirmed**, **False Positive**, or **Needs Clarification**
- [ ] False positives removed; Needs Clarification findings annotated before final report

---

## Verification

All findings are based on static code analysis of the local repository only — no live EC2 instance is available. Every finding must cite the exact file path relative to the working directory and line number. A dedicated reviewer agent must re-read each cited location and verify the finding before it enters the final report.

---

*Expecting this to run as a full team: domain scanner + portal auditor + website auditor + deployment auditor + security auditor + reviewer + report assembler.*
