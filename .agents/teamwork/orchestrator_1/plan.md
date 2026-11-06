# QA Audit Plan: DBERT Website & LMS Portal

## Overview
Comprehensive static code analysis and QA audit of DBERT Next.js static export (`cpanel_public_html/`, `apps/website/`) and LMS portal (`apps/portal/`), plus deployment configurations (`deploy/`).

## Milestones & Work Breakdown

### Phase 1: Specialized Discovery & Static Audits (5 Parallel Subagents)
1. **Explorer R1: Domain Migration Completeness (`dbert.online` -> `dbert.in`)**
   - Working Dir: `.agents/teamwork/explorer_r1/`
   - Scope: Repo-wide scan for `dbert.online`.
   - Classification: Blocker vs Warning vs Informational.
   - Specific checks: `.env*`, Nginx configs under `deploy/`, `sitemap.xml`, `robots.txt`, `og:*`/`twitter:*` tags, JSON-LD, blog redirects.
   - Pre-confirmed items check: verify pre-scan items #1, #2, #3, #4, #5, #7, #8.

2. **Explorer R2: Portal (Flask/Gunicorn) Production-Readiness**
   - Working Dir: `.agents/teamwork/explorer_r2/`
   - Scope: `apps/portal/app.py`, `routes/`, `services/`, `templates/`.
   - Specific checks:
     1. Auth & session dead ends (`SESSION_COOKIE_DOMAIN`, `SESSION_COOKIE_SECURE`, `ProxyFix`).
     2. CSRF gaps (`CSRF_EXEMPT_ENDPOINTS`, missing `{{ csrf_field() }}`).
     3. SQLite silent fallback risk (`dialect != "postgres"` on write paths).
     4. Default credential leakage & production guards (`FLASK_SECRET_KEY`, `ADMIN_PASSWORD`, etc.).
     5. Razorpay webhook (CSRF-exempt AND HMAC validation).
     6. Upload sandbox (`UPLOAD_FOLDER`, extension blocking for `.py`, `.php`, `.sh`, execution permissions).
     7. Email silent fails (exception swallowing returning 200).
     8. CSP `connect-src` (`lms.dbert.in`, `dbert.in`).
     9. ProxyFix wiring (`x_proto=1, x_host=1`).

3. **Explorer R3: Website (Next.js Static Export) Production-Readiness**
   - Working Dir: `.agents/teamwork/explorer_r3/`
   - Scope: `cpanel_public_html/` and `apps/website/`.
   - Specific checks:
     1. Dead internal links (hrefs in HTML vs existing static directory with `index.html`).
     2. Missing or broken 404 page & Nginx error_page 404.
     3. `sitemap.xml` domain verification (`<loc>` entries).
     4. `robots.txt` check (`Sitemap:`).
     5. OG / meta tags across all HTML pages.
     6. `_next/` static chunk asset integrity.
     7. JSON-LD structured data domain verification across all pages.

4. **Explorer R4: EC2 Deployment Configuration Audit**
   - Working Dir: `.agents/teamwork/explorer_r4/`
   - Scope: `deploy/` directory.
   - Specific checks:
     1. Nginx unified config (`dbert-unified-nginx.conf`) syntax, domains, SSL, upstream proxy_pass.
     2. Systemd service files (`WorkingDirectory`, `ExecStart`, `User/Group`, paths).
     3. Deploy script (`deploy_ec2_unified.sh`) - hardcoded password `DBERT_SECURE_PASSWORD_123`, certbot SAN domains.
     4. `production_preflight.sh` single-quoted variable expansion bug.
     5. Port safety (3001 Next.js, 5001 Gunicorn).

5. **Explorer R5: Security & Hardening Spot Checks**
   - Working Dir: `.agents/teamwork/explorer_r5/`
   - Scope: Repo-wide & deployment security.
   - Specific checks:
     1. `internship.db` web exposure via Nginx.
     2. `uploads/` web exposure & execution.
     3. `.env` web exposure via Nginx.
     4. Debug mode leakage in production.
     5. Admin panel auth decorators.
     6. Secret key short-length guard severity.
     7. Rate limiting on auth endpoints (login, signup, password reset).

### Phase 2: Synthesis & Aggregation
- Orchestrator aggregates all 5 reports into `.agents/teamwork/orchestrator_1/consolidated_findings.md`.
- Ensure all 8 pre-confirmed blockers are present and verified.

### Phase 3: Independent Verification (Reviewer)
- Dispatch independent Reviewer (`teamwork_preview_reviewer`) to:
  - Working Dir: `.agents/teamwork/reviewer_1/`
  - Re-read each cited file and line number.
  - Mark each finding as Confirmed, False Positive, or Needs Clarification.
  - Produce verification report: `.agents/teamwork/reviewer_1/handoff.md`.

### Phase 4: Final Report Assembly (Worker)
- Dispatch Worker (`teamwork_preview_worker`) to:
  - Working Dir: `.agents/teamwork/worker_1/`
  - Generate `c:\Users\user\Desktop\dbert-website-lms\QA_REPORT.md` following the exact schema:
    - Executive summary & metrics table (Blockers / Warnings / Info).
    - Grouped findings with Severity | File:Line | Description | Recommended Fix.
    - Verified status from reviewer.
  - Validate acceptance criteria checklist.

### Phase 5: Handoff & Notification
- Verify output report matches all acceptance criteria.
- Send completion message to parent.
