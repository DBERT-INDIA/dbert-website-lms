# BRIEFING — 2026-10-25T23:05:00Z

## Mission
Website Readiness Auditor: Audit cpanel_public_html/ and apps/website/ source across 7 R3 areas (dead internal links, 404 page & Nginx error directive, sitemap.xml, robots.txt, OG/meta tags, _next/ assets, JSON-LD structured data).

## 🔒 My Identity
- Archetype: explorer
- Roles: Website Readiness Auditor
- Working directory: c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_r3
- Original parent: 3a4d7ac2-699c-47ca-9101-c0e51547ba94
- Milestone: Requirement R3 Audit

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Audit both cpanel_public_html/ and apps/website/
- Report findings with relative paths, line numbers, Blocker/Warning/Info classification, explanations, and fixes
- Self-contained handoff.md following 5-component report structure

## Current Parent
- Conversation ID: 3a4d7ac2-699c-47ca-9101-c0e51547ba94
- Updated: 2026-10-25T23:05:00Z

## Investigation State
- **Explored paths**:
  - `cpanel_public_html/` (all 74 HTML files, `sitemap.xml`, `robots.txt`, `ads.txt`, `_next/static/chunks/`, `404.html`, `.htaccess`)
  - `apps/website/` (`src/app/`, `src/lib/`, `src/data/`, `src/components/`, `package.json`, `next.config.js`, `sitemap.xml`, `robots.txt`, `ads.txt`, `.env`, `.env.example`, `out/`, `.next/standalone/`)
  - `deploy/` (`dbert-unified-nginx.conf`, `dbert-website-nginx.conf`, `deploy_ec2_unified.sh`)
- **Key findings**:
  1. Internal links: 89 distinct internal paths starting with `/` in `cpanel_public_html/` all exist as directories with `index.html` (0 dead ends among public static routes). However, `/admin` routes present in source (`src/app/admin/`) are omitted from static build (404 on static hosting).
  2. Legacy domain links in static build: 1,226 links across all 74 HTML files in `cpanel_public_html/` still point to `https://internship.dbert.online/` instead of `https://lms.dbert.in/`.
  3. 404 Page & Nginx: `cpanel_public_html/404.html` and `cpanel_public_html/404/index.html` exist, but `error_page 404` directive is completely missing in `deploy/dbert-unified-nginx.conf` and `deploy/dbert-website-nginx.conf`.
  4. Sitemap domain: `cpanel_public_html/sitemap.xml` has 70 `<loc>` pointing to `https://dbert.in` (correct), but `apps/website/sitemap.xml` at repo root has 70 `<loc>` pointing to `https://dbert.online` (Blocker).
  5. Robots.txt: `cpanel_public_html/robots.txt` points to `https://dbert.in/sitemap.xml` (correct), but `apps/website/robots.txt:13` points to `https://dbert.online/sitemap.xml` (Blocker).
  6. Meta/OG tags: `cpanel_public_html/` uses `https://dbert.in` for `og:url` and `og:image`. Missing `twitter:site` in `apps/website/src/app/layout.tsx`. Old static export in `apps/website/` root uses `dbert.online`. `ads.txt:1` has `dbert.online`.
  7. Asset integrity: 40/40 referenced `/_next/static/` chunks exist in `cpanel_public_html/_next/static/` (100% integrity). However, 11 chunks are missing in `apps/website/.next/static/chunks/` due to build hash divergence.
  8. JSON-LD structured data: 4 schema blocks in `cpanel_public_html/` use `internship.dbert.online` (`learners/index.html` FAQ, `learners/fellowship/index.html` Course offers.url & FAQ). Pre-scan finding #7 confirmed: `apps/website/__next.__PAGE__.txt` has Organization schema with `dbert.online`.
- **Unexplored areas**: None for R3.

## Key Decisions Made
- Fully documented exact relative paths, line numbers, classifications (Blocker/Warning/Info), root causes, and recommended fixes for all 7 areas.
- Formatted complete 89-entry Dead Internal Links verification table in handoff.md.

## Artifact Index
- handoff.md — Complete 5-component audit report for Requirement R3
- progress.md — Liveness & task execution tracker
- DISPATCH.md — Preserved incoming instructions
