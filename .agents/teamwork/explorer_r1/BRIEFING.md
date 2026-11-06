# BRIEFING — 2026-10-25T23:05:00Z

## Mission
Audit the entire repository for residual `dbert.online` references (Requirement R1) and produce a detailed classification report.

## 🔒 My Identity
- Archetype: explorer
- Roles: Domain Migration Auditor
- Working directory: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r1
- Original parent: 3a4d7ac2-699c-47ca-9101-c0e51547ba94
- Milestone: Requirement R1 - Domain Migration Audit

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Scan every file in repository (Python, HTML, JS, CSS, shell scripts, Nginx configs, .env samples, JSON, markdown docs) for residual references to `dbert.online` that are NOT intentional redirect rules
- Classify each reference: Blocker, Warning, Informational
- For every finding, cite exact relative file path and line number, classification, snippet, and recommended fix

## Current Parent
- Conversation ID: 3a4d7ac2-699c-47ca-9101-c0e51547ba94
- Updated: 2026-10-25T22:57:31Z

## Investigation State
- **Explored paths**:
  - `apps/portal/.env*`, `apps/portal/app.py`, `apps/portal/cgi-bin/*`, `apps/portal/deploy/*`, `apps/portal/templates/*`, `apps/portal/sitemap.xml`, `apps/portal/robots.txt`
  - `apps/website/src/**`, `apps/website/public/**`, `apps/website/.env*`, `apps/website/sitemap.xml`, `apps/website/robots.txt`, `apps/website/out/**`, `apps/website/*.html`
  - `cpanel_public_html/**` (HTML, sitemap.xml, robots.txt, .htaccess, ads.txt)
  - `deploy/**` (dbert-unified-nginx.conf, dbert-portal-nginx.conf, dbert-website-nginx.conf, deploy_ec2_unified.sh, markdown guides)
  - `dbert-api-package/**` (backend config, auth router, .env samples, docs)
  - Root markdown docs and scratch scripts
- **Key findings**:
  - Pre-confirmed blockers 1, 2, 3, 4, 5, 7, 8 confirmed with exact lines.
  - `cpanel_public_html` contains 157 outbound link references to `https://internship.dbert.online/` across all 110 HTML pages, because `apps/website/src` was migrated but Next.js export was not rebuilt before staging.
  - `apps/portal/sitemap.xml` has hundreds of `<loc>https://internship.dbert.online/...</loc>` entries.
  - `apps/website/sitemap.xml` has 70 `<loc>https://dbert.online/...</loc>` entries and `apps/website/robots.txt` points to `https://dbert.online/sitemap.xml`.
  - `deploy/dbert-portal-nginx.conf` and `deploy/dbert-website-nginx.conf` are legacy configs serving old domains.
  - `deploy/dbert-unified-nginx.conf` has intentional 301 redirect blocks for legacy domains, but certbot SAN in deploy script does not request certificates for `dbert.online` / `internship.dbert.online`, which will trigger SSL cert warnings before 301 redirects can execute.
  - `dbert-api-package` has multiple blockers in `.env.production.sample`, `backend/core/config.py`, and `backend/api/v1/auth/router.py`.
- **Unexplored areas**: None. Full codebase scanned and cataloged.

## Key Decisions Made
- Excluded unzipped vendor library packages and node_modules from raw traversal to prevent infinite loop.
- Grouped findings into 10 structured operational areas.
- Detailed recommended fix provided for each finding.

## Artifact Index
- .agents/teamwork/explorer_r1/DISPATCH.md — Dispatch log
- .agents/teamwork/explorer_r1/BRIEFING.md — Working memory
- .agents/teamwork/explorer_r1/progress.md — Progress heartbeat
- .agents/teamwork/explorer_r1/handoff.md — Final audit report
