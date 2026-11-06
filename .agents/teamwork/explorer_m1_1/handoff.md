# Handoff Report: Requirement R1 — Legacy Domain Audit & Remediation

**Agent**: `explorer_m1_1`  
**Archetype / Role**: Teamwork Explorer & Investigator  
**Date**: 2026-11-03  
**Recipient Orchestrator**: `d66c654e-a32e-4bd2-a554-e6ecbf8cc20c`  
**Scope**: Comprehensive repository-wide audit for legacy domains `dbert.online` and `internship.dbert.online` across all source directories, config files, static assets, database records, and distribution archives.

---

## Executive Summary

An exhaustive static code analysis, database record scan, and distribution archive audit was conducted across the entire repository (`c:\Users\user\Desktop\dbert-website-lms`). A total of **267 active workspace occurrences** across 78 non-scratch files were identified, analyzed, and classified into three distinct categories:

1. **Blockers (175 occurrences across 57 files)**: Functional URL, outbound navigation, metadata fallback, email address, CORS, and `.htaccess` defects that silently direct traffic to the legacy domain. Crucially, **all 175 blockers reside in `dbert-api-package/website-content/`** (an un-updated snapshot of `apps/website/src`). In addition, live SQLite databases (`internship.db` and `apps/portal/internship.db`) harbor **9,097 legacy domain records** that will poison PostgreSQL during EC2 migration.
2. **Intentional Redirect Rules (11 occurrences across 5 files)**: Valid 301 HTTP/HTTPS permanent redirection rules in Nginx (`deploy/dbert-unified-nginx.conf`), Apache (`.htaccess`), Certbot SSL SAN configuration, and DNS setup guidance designed to funnel legacy traffic to `dbert.in` and `lms.dbert.in`.
3. **Warnings (81 occurrences across 16 files)**: Outdated documentation files (markdown plans, release reports), inline code comments, CSS selector notes, and form placeholder strings.

| Finding Classification | Occurrences | Files Affected | Primary Locations | Operational Impact |
|---|:---:|:---:|---|---|
| **Blockers** | **175** | 57 files + 2 SQLite DBs | `dbert-api-package/website-content/`, `internship.db` | Silent 404s, broken links, SEO dilution, bad emails, DB pollution |
| **Intentional Redirect Rules** | **11** | 5 files | `deploy/dbert-unified-nginx.conf`, `.htaccess`, deploy scripts | None (Essential for domain migration routing) |
| **Warnings** | **81** | 16 files | `*.md` documentation, `docs/env_vars.md`, comments | Developer confusion, misleading documentation |
| **TOTAL** | **267** | **78 files** | Entire Repository | Live Deployment Blocked until R1 remediated |

---

## 1. Observation

### 1.1 Verification of Pre-Confirmed Baseline Findings (PRE-01 to PRE-08)

All 8 baseline findings from `ORIGINAL_REQUEST.md` were directly inspected on disk. The investigation revealed that all 8 items have been remediated in the current local working copy:

| # | ID | Cited File & Line | Baseline Issue | Current Workspace State (Observed) | Verdict |
|---|---|---|---|---|:---:|
| 1 | **PRE-01** | `apps/portal/.env:27` | `SMTP_HOST=dbert.online` | `SMTP_HOST=dbert.in` (Line 27) | **Remediated** |
| 2 | **PRE-02** | `apps/portal/.env:29` | `SMTP_USER=contactus@dbert.online` | `SMTP_USER=contactus@dbert.in` (Line 29) | **Remediated** |
| 3 | **PRE-03** | `apps/portal/.env:31` | `FROM_EMAIL=contactus@dbert.online` | `FROM_EMAIL=contactus@dbert.in` (Line 31) | **Remediated** |
| 4 | **PRE-04** | `apps/portal/app.py:309` | Fallback default `"dbert.online"` | `SMTP_HOST = os.environ.get("SMTP_HOST", "dbert.in")` | **Remediated** |
| 5 | **PRE-05** | `apps/portal/app.py:2698` | Hardcoded staff email `@dbert.online` | `staff_email = f"{ADMIN_USERNAME}@dbert.in"` | **Remediated** |
| 6 | **PRE-06** | `deploy/deploy_ec2_unified.sh:57-61` | Plaintext DB password `DBERT_SECURE_PASSWORD_123` | Dynamic evaluation via `openssl rand -hex 24` or env ingestion | **Remediated** |
| 7 | **PRE-07** | `cpanel_public_html/__next.__PAGE__.txt:49` | JSON-LD Organization schema legacy URLs | Line 49: `"url":"https://dbert.in"`, `"logo":"https://dbert.in/logo.svg"`, `"email":"contactus@dbert.in"` | **Remediated** |
| 8 | **PRE-08** | `apps/portal/templates/seo_landing.html:133` | Anchor text reads `dbert.online` | Line 133: `<a href="https://dbert.in" class="underline text-gray-400">dbert.in</a>` | **Remediated** |

### 1.2 Verification of Application Sources (`apps/website` and `apps/portal`)

- **`apps/website/src/`**: A complete filesystem search across all 250 files in `apps/website/src/` returned **ZERO occurrences** of `dbert.online` or `internship.dbert.online`. All metadata fallbacks (`layout.tsx`, `robots.ts`, `sitemap.ts`, `seo.ts`), JSON-LD schemas, and navigation components have already been unified to `https://dbert.in` and `https://lms.dbert.in`.
- **`apps/website/` compiled JS chunks (`_next/static/chunks/*.js`)**: Zero occurrences.
- **`cpanel_public_html/` compiled JS chunks (`_next/static/chunks/*.js`)**: Zero occurrences.
- **`cpanel_public_html/sitemap.xml` & `robots.txt`**: All 70 `<loc>` entries point to `https://dbert.in`.
- **`apps/portal/` Python Source**: All routes (`routes/`), services (`services/`), and templates (`templates/`) are free of active `dbert.online` occurrences in source code. Fallback emails in `services/auth_service.py` (lines 189, 195) specify `admin@dbert.in`.
- **`apps/portal/sitemap.xml`**: Single-line 628 KB XML file contains all canonical `<loc>` tags pointing exclusively to `https://lms.dbert.in/`.

### 1.3 Intentional Redirect Rules (11 Occurrences across 5 Files)

The following 11 occurrences are intentional, functional permanent redirection rules and operational configuration designed to route legacy traffic to the production domains:

| File Path | Line | Snippet | Target Redirect | Purpose / Classification |
|---|:---:|---|---|---|
| `apps/website/.htaccess` | 12 | `# 1. 301 Permanent Redirect from legacy dbert.online -> dbert.in` | `dbert.in` | Intentional redirect rule |
| `apps/website/public/.htaccess` | 12 | `# 1. 301 Permanent Redirect from legacy dbert.online -> dbert.in` | `dbert.in` | Intentional redirect rule |
| `cpanel_public_html/.htaccess` | 12 | `# 1. 301 Permanent Redirect from legacy dbert.online -> dbert.in` | `dbert.in` | Intentional redirect rule |
| `deploy/dbert-unified-nginx.conf` | 31 | `server_name dbert.online www.dbert.online;` | `dbert.in` | Intentional redirect rule |
| `deploy/dbert-unified-nginx.conf` | 45 | `server_name internship.dbert.online;` | `lms.dbert.in` | Intentional redirect rule |
| `deploy/dbert-unified-nginx.conf` | 57 | `# Redirect legacy dbert.online -> https://dbert.in` | `dbert.in` | Intentional redirect rule |
| `deploy/dbert-unified-nginx.conf` | 61 | `server_name dbert.online www.dbert.online;` | `dbert.in` | Intentional redirect rule |
| `deploy/dbert-unified-nginx.conf` | 69 | `# Redirect legacy internship.dbert.online -> https://lms.dbert.in` | `lms.dbert.in` | Intentional redirect rule |
| `deploy/dbert-unified-nginx.conf` | 73 | `server_name internship.dbert.online;` | `lms.dbert.in` | Intentional redirect rule |
| `deploy/deploy_ec2_unified.sh` | 229 | `echo "  sudo certbot --nginx -d dbert.in -d www.dbert.in -d lms.dbert.in -d api.dbert.in -d dbert.online -d www.dbert.online -d internship.dbert.online"` | `lms.dbert.in` | Intentional redirect rule |
| `deploy/FILEZILLA_DEPLOYMENT_GUIDE.md` | 19 | `- (Optional for 301 redirects): `dbert.online`, `internship.dbert.online` $\rightarrow$ A records to `YOUR_EC2_IP`` | `lms.dbert.in` | Intentional redirect rule |


### 1.4 Blocker Defects: Legacy Domains in `dbert-api-package/website-content/` (175 Occurrences across 57 Files)

While `apps/website/src` was updated during prior refactoring, the companion standalone package `dbert-api-package/website-content/` was neglected. It contains **175 Blocker references** across 57 files. When this package is deployed or built, it renders invalid outbound links, incorrect JSON-LD structured data, and defunct email links:

| File Path | Line | Current Snippet | Required Replacement | Severity |
|---|:---:|---|---|:---:|
| `dbert-api-package/website-content/public/.htaccess` | 17 | `RewriteRule ^jobs/?$ https://internship.dbert.online/jobs [L,R=301]` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/public/.htaccess` | 20 | `RewriteRule ^internships/?(.*)$ https://internship.dbert.online/internships/$1 [L,R=301]` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/layout.tsx` | 51 | `metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online'),` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/layout.tsx` | 103 | `"url": process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/layout.tsx` | 104 | `"logo": `${process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online'}/logo.svg`,` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/layout.tsx` | 124 | `"email": "contactus@dbert.online",` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/robots.ts` | 5 | `const baseUrl = process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online';` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/sitemap.ts` | 7 | `* High-authority dynamic sitemap generator for dbert.online` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/sitemap.ts` | 11 | `const baseUrl = process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online';` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/about/careers/page.tsx` | 52 | `<a href="mailto:contactus@dbert.online" className="btn btn-outline">Submit Your Portfolio</a>` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/about/contact/page.tsx` | 37 | `<p><a href="mailto:contactus@dbert.online" className={styles.accentLink}>contactus@dbert.online</a></p>` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-consultant/page.tsx` | 44 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/page.tsx` | 53 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/page.tsx` | 60 | `url: 'https://dbert.online/ai-solutions'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/consultation/page.tsx` | 52 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/llm-training/page.tsx` | 45 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/llm-training/dbert-ai/page.tsx` | 52 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/llm-training/pipeline/page.tsx` | 55 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/llm-training/private-hosting/page.tsx` | 43 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/llm-training/private-hosting/page.tsx` | 50 | `url: 'https://dbert.online/ai-solutions/llm-training/private-hosting'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/page.tsx` | 79 | `url: 'https://dbert.online/ai-solutions/products',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/page.tsx` | 85 | `url: `https://dbert.online/ai-solutions/products/${p.slug}`,` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/certificate-verification-api/page.tsx` | 48 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/certificate-verification-api/page.tsx` | 56 | `url: 'https://dbert.online/ai-solutions/products/certificate-verification-api'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/certificate-verification-api/page.tsx` | 122 | `{`curl -X GET "https://api.dbert.online/v1/verify?certId=DBERT-ENG-2026-8894" \\` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/dbert-chat/page.tsx` | 48 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/dbert-chat/page.tsx` | 56 | `url: 'https://dbert.online/ai-solutions/products/dbert-chat'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/dbert-chat/page.tsx` | 133 | `{`curl -X POST "https://api.dbert.online/v1/chat" \\` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/document-ai/page.tsx` | 48 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/document-ai/page.tsx` | 56 | `url: 'https://dbert.online/ai-solutions/products/document-ai'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/document-ai/page.tsx` | 122 | `{`curl -X POST "https://api.dbert.online/v1/extract" \\` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/document-ai/page.tsx` | 126 | `"document_url": "https://secure-storage.dbert.online/client_invoices/inv_9981.pdf",` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/hiring-automation-suite/page.tsx` | 48 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/hiring-automation-suite/page.tsx` | 56 | `url: 'https://dbert.online/ai-solutions/products/hiring-automation-suite'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/intern-management-system/page.tsx` | 48 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/ai-solutions/products/intern-management-system/page.tsx` | 56 | `url: 'https://dbert.online/ai-solutions/products/intern-management-system'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/cohorts/aivara/page.tsx` | 144 | `<li><strong>Independent Credential Verification:</strong> Earn an accredited experience letter with a unique SHA-256 validation ID checkable on <code>dbert.online/verify</code>.</li>` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/hire/pre-vetted-engineers/page.tsx` | 88 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 26 | `... code screening challenge at internship.dbert.online.'` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 36 | `...R departments enter this ID directly at dbert.online/verify to inspect verified project deliverables without waiting for manual email confir...` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 56 | `url: 'https://dbert.online/learners/launchpad',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 62 | `url: 'https://dbert.online/learners/accelerate',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 68 | `url: 'https://dbert.online/learners/fellowship',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 74 | `url: 'https://dbert.online/learners/jobs',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 123 | `ctaHref: 'https://internship.dbert.online/',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 204 | `href: 'https://internship.dbert.online/',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 235 | `<a href="https://internship.dbert.online/" target="_blank" rel="noopener noreferrer" className="btn btn-outline">` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/page.tsx` | 408 | `<a href="https://internship.dbert.online/" target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-sm">Open Career Portal ↗</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 22 | `url: 'https://dbert.online/learners/courses/ai-agent-development',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 23 | `provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 30 | `url: 'https://dbert.online/learners/courses/generative-ai',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 31 | `provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 38 | `url: 'https://dbert.online/learners/courses/machine-learning',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 39 | `provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 46 | `url: 'https://dbert.online/learners/courses/python-automation',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 47 | `provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 54 | `url: 'https://dbert.online/learners/courses/full-stack-development',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 55 | `provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 62 | `url: 'https://dbert.online/learners/courses/data-analytics',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 63 | `provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 197 | `href="https://internship.dbert.online/"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 208 | `href="https://internship.dbert.online/internships/full-stack-development"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 217 | `href="https://internship.dbert.online/internships/data-analyst"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 226 | `href="https://internship.dbert.online/internships/python-automation"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/page.tsx` | 235 | `href="https://internship.dbert.online/internships/ai-agent-development"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 23 | `...essing our open institutional portal at dbert.online/verify.'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 45 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 57 | `url: 'https://dbert.online/learners/courses/ai-agent-development'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 271 | `hubHref="https://internship.dbert.online/internships/ai-agent-development"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 272 | `jobsHref="https://internship.dbert.online/jobs/ai-agent-development"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 280 | `href: 'https://internship.dbert.online/internships/ai-sales-assistant-bot-intern-mumbai-remote-14',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 289 | `href: 'https://internship.dbert.online/internships/ai-workflow-automation-intern-bangalore-remote-10',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 298 | `href: 'https://internship.dbert.online/internships/agentic-search-systems-intern-delhi-ncr-remote-11',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 307 | `href: 'https://internship.dbert.online/internships/ai-coding-assistant-intern-hyderabad-remote-12',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 316 | `href: 'https://internship.dbert.online/internships/knowledge-base-rag-agent-intern-pune-remote-13',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/ai-agent-development/page.tsx` | 325 | `href: 'https://internship.dbert.online/internships/rag-pipeline-engineering-intern-remote-1',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 23 | `... into our public verification portal at dbert.online/verify, enabling instant cryptographic HR checks.'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 45 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 57 | `url: 'https://dbert.online/learners/courses/data-analytics'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 342 | `hubHref="https://internship.dbert.online/internships/data-analyst"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 343 | `jobsHref="https://internship.dbert.online/jobs/data-analyst"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 351 | `href: 'https://internship.dbert.online/internships/survey-research-data-intern-mumbai-remote-32',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 360 | `href: 'https://internship.dbert.online/internships/operations-data-analyst-intern-bangalore-remote-28',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 369 | `href: 'https://internship.dbert.online/internships/customer-insights-analyst-delhi-ncr-remote-29',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 378 | `href: 'https://internship.dbert.online/internships/data-cleaning-etl-intern-hyderabad-remote-30',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 387 | `href: 'https://internship.dbert.online/internships/excel-reporting-automation-intern-pune-remote-31',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/data-analytics/page.tsx` | 396 | `href: 'https://internship.dbert.online/internships/power-bi-dashboard-intern-remote-21',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 27 | `...o our public authentication registry at dbert.online/verify, eliminating verification friction during enterprise hiring audits.'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 45 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 57 | `url: 'https://dbert.online/learners/courses/full-stack-development'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 271 | `hubHref="https://internship.dbert.online/internships/full-stack-development"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 272 | `jobsHref="https://internship.dbert.online/jobs/full-stack-development"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 280 | `href: 'https://internship.dbert.online/internships/booking-system-development-intern-mumbai-remote-50',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 289 | `href: 'https://internship.dbert.online/internships/saas-feature-development-intern-bangalore-remote-46',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 298 | `href: 'https://internship.dbert.online/internships/authentication-security-intern-delhi-ncr-remote-47',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 307 | `href: 'https://internship.dbert.online/internships/progressive-web-app-intern-pune-remote-49',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 316 | `href: 'https://internship.dbert.online/internships/react-frontend-development-intern-remote-37',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/full-stack-development/page.tsx` | 325 | `href: 'https://internship.dbert.online/internships/internal-tools-development-intern-hyderabad-remote-48',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/generative-ai/page.tsx` | 26 | `answer: 'Every credential issued by DBERT Labs contains a cryptographically signed UUID that HR managers and tech recruiters can verify in real-time at dbert.online/verify.'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/generative-ai/page.tsx` | 44 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/generative-ai/page.tsx` | 56 | `url: 'https://dbert.online/learners/courses/generative-ai'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/machine-learning/page.tsx` | 30 | `answer: 'Graduates receive a cryptographically verified credential serial number that recruiters can audit instantly at dbert.online/verify, coupled with verifiable Git commits.'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/machine-learning/page.tsx` | 44 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/machine-learning/page.tsx` | 56 | `url: 'https://dbert.online/learners/courses/machine-learning'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 27 | `...by inputting your unique serial code at dbert.online/verify.'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 45 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 57 | `url: 'https://dbert.online/learners/courses/python-automation'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 271 | `hubHref="https://internship.dbert.online/internships/python-automation"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 272 | `jobsHref="https://internship.dbert.online/jobs/python-automation"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 280 | `href: 'https://internship.dbert.online/internships/qa-automation-intern-mumbai-remote-68',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 289 | `href: 'https://internship.dbert.online/internships/lead-generation-automation-intern-bangalore-remote-64',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 298 | `href: 'https://internship.dbert.online/internships/price-monitoring-automation-intern-delhi-ncr-remote-65',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 307 | `href: 'https://internship.dbert.online/internships/document-processing-automation-intern-hyderabad-remote-66',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 316 | `href: 'https://internship.dbert.online/internships/social-media-automation-intern-pune-remote-67',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/courses/python-automation/page.tsx` | 325 | `href: 'https://internship.dbert.online/internships/web-scraping-intern-remote-55',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/fellowship/page.tsx` | 49 | `...e, a certificate ID anyone can check at dbert.online/verify, and commits on a real client repository. Partner startups review fellow perform...` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/fellowship/page.tsx` | 69 | `...a recruiter can verify independently at dbert.online/verify without contacting us. A letter nobody can check is worth roughly what it costs ...` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/fellowship/page.tsx` | 74 | `...DBERT internship platform at internship.dbert.online. The application asks for your code — a repository, a deployed project, or your screeni...` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/fellowship/page.tsx` | 89 | `url: 'https://dbert.online',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/fellowship/page.tsx` | 91 | `url: 'https://dbert.online/learners/fellowship',` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/fellowship/page.tsx` | 103 | `url: 'https://internship.dbert.online/',` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/fellowship/page.tsx` | 393 | `href="https://internship.dbert.online/"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/jobs/page.tsx` | 100 | `<a href="https://internship.dbert.online/" target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-sm">Apply via Portal</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/learners/jobs/page.tsx` | 116 | `<a href="https://internship.dbert.online/" target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-lg">Apply for Internship Track</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/pricing/page.tsx` | 45 | `url: 'https://dbert.online/pricing'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/privacy/page.tsx` | 31 | `...onal security across our website (<code>dbert.online</code>), learning platforms, and verification registries.` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/privacy/page.tsx` | 51 | `...dor, uses cookies to serve ads on <code>dbert.online</code>. Google&apos;s use of advertising cookies enables it and its partners to serve a...` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/refund/page.tsx` | 55 | `... available at <a href="mailto:contactus@dbert.online" className="accent-link">contactus@dbert.online</a>.` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/page.tsx` | 58 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/page.tsx` | 65 | `url: 'https://dbert.online/startups'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/investor-network/page.tsx` | 46 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/page.tsx` | 96 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/equity/page.tsx` | 51 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/equity/page.tsx` | 59 | `url: 'https://dbert.online/startups/services/equity'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/equity/term-sheets/page.tsx` | 47 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/equity/term-sheets/page.tsx` | 54 | `url: 'https://dbert.online/startups/services/equity/term-sheets'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/funding/page.tsx` | 51 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/funding/page.tsx` | 59 | `url: 'https://dbert.online/startups/services/funding'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/hiring/page.tsx` | 53 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/hiring/page.tsx` | 61 | `url: 'https://dbert.online/startups/services/hiring'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/infrastructure/page.tsx` | 51 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/infrastructure/page.tsx` | 59 | `url: 'https://dbert.online/startups/services/infrastructure'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/legal/page.tsx` | 51 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/legal/page.tsx` | 59 | `url: 'https://dbert.online/startups/services/legal'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/technical/page.tsx` | 52 | `url: 'https://dbert.online'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/app/startups/services/technical/page.tsx` | 60 | `url: 'https://dbert.online/startups/services/technical'` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/blog/BlogClientView.tsx` | 23 | `const res = await fetch('https://internship.dbert.online/api/public/blog-posts', {` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/blog/DynamicBlogReader.tsx` | 114 | `const res = await fetch(`https://internship.dbert.online/api/public/blog-posts/${slug}`);` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/cohorts/AivaraCohortForm.tsx` | 289 | `href="https://internship.dbert.online/apply?cohort=aivara"` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/AlkameCaseStudyContent.tsx` | 374 | `<a href="https://internship.dbert.online" target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-lg">Apply on internship.dbert.online</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 71 | `{ label: 'Full Stack Internships Mumbai', href: 'https://internship.dbert.online/internships/booking-system-development-intern-mumbai-remote-50', external: true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 72 | `{ label: 'Data Analyst Bangalore', href: 'https://internship.dbert.online/internships/operations-data-analyst-intern-bangalore-remote-28', external: true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 73 | `{ label: 'AI Agent Roles Delhi NCR', href: 'https://internship.dbert.online/internships/agentic-search-systems-intern-delhi-ncr-remote-11', external: true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 74 | `{ label: 'Python Automation Pune', href: 'https://internship.dbert.online/internships/social-media-automation-intern-pune-remote-67', external: true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 75 | `{ label: 'Virtual Remote Sprints', href: 'https://internship.dbert.online/internships/virtual-remote-internships', external: true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 76 | `{ label: 'Paid Internships With Stipend', href: 'https://internship.dbert.online/internships/paid-internships', external: true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 77 | `{ label: 'Job Board & Placement Hub', href: 'https://internship.dbert.online/jobs', external: true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 105 | `href="mailto:contactus@dbert.online"` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 108 | `contactus@dbert.online` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 184 | `<a href="https://internship.dbert.online/internships/full-stack-development" target="_blank" rel="noopener noreferrer">Full Stack Internships Mumbai &amp; Bangalore</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 186 | `<a href="https://internship.dbert.online/internships/data-analyst-internship-work-from-home" target="_blank" rel="noopener noreferrer">Data Analyst Work From Home</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 188 | `<a href="https://internship.dbert.online/internships/ai-automation-internship" target="_blank" rel="noopener noreferrer">AI Automation Internships Bangalore</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 190 | `<a href="https://internship.dbert.online/jobs/full-stack-development" target="_blank" rel="noopener noreferrer">Full Stack AI Developer Jobs</a>` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/Footer.tsx` | 205 | `<span>© {new Date().getFullYear()} DBERT · dbert.online · All rights reserved</span>` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/layout/ProgramDetailTemplate.tsx` | 153 | `"sameAs": "https://dbert.online"` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/seo/ArticleSchema.tsx` | 12 | `const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online';` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/components/seo/Breadcrumbs.tsx` | 6 | `const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online';` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/content/blog/ai-agent-frameworks-comparison.mdx` | 143 | `...er Discovery Portal](https://internship.dbert.online/internships/ai-agent-development).` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/content/blog/building-scalable-microservices-with-fastapi.mdx` | 10 | `canonicalUrl: "https://dbert.online/blog/building-scalable-microservices-with-fastapi"` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/data/nav.config.json` | 121 | `{ "label": "Job Board", "href": "https://internship.dbert.online/jobs", "external": true },` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/data/nav.config.json` | 122 | `{ "label": "Apply for Fellowship", "href": "https://internship.dbert.online/apply", "external": true, "highlight": true }` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/data/nav.config.json` | 146 | `"href": "https://internship.dbert.online/",` | `lms.dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/lib/email.ts` | 86 | `...ntial independently verifiable at <code>dbert.online/verify</code>.</p>` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/lib/email.ts` | 100 | `... engineering certification checkable on dbert.online/verify.${notesText}\n\nOur coordinators will reach out shortly with onboarding details....` | `dbert.in` | **Blocker** |
| `dbert-api-package/website-content/src/lib/seo.ts` | 4 | `const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL \|\| 'https://dbert.online';` | `dbert.in` | **Blocker** |


### 1.5 Database Contamination Audit (SQLite `internship.db`)

A deep SQL scan was executed against both SQLite databases (`internship.db` at repo root and `apps/portal/internship.db`). Because `scripts/migrate_all_ec2_data.py` transfers SQLite data into production PostgreSQL (`dbert_internship` schema), any uncleaned legacy URLs will be migrated directly into production:

| Database File | Table Name | Column Name | Legacy Occurrences | Sample Verbatim Snippet | Required Remediation |
|---|---|---|:---:|---|---|
| `internship.db` (root) | `staff_accounts` | `email` | 1 | `dbert_admin@dbert.online` | Replace `@dbert.online` with `@dbert.in` |
| `apps/portal/internship.db` | `staff_accounts` | `email` | 4 | `admin@dbert.online`, `dbert_admin@dbert.online` | Replace `@dbert.online` with `@dbert.in` |
| `apps/portal/internship.db` | `companies` | `website` | 1 | `https://internship.dbert.online` | Replace with `https://lms.dbert.in` |
| `apps/portal/internship.db` | `post_applications` | `comment` | 1 | `https://internship.dbert.online/internships/web-app-maintenance-intern-remote-45` | Replace with `https://lms.dbert.in/...` |
| `apps/portal/internship.db` | `notifications` | `link` | 5,976 | `https://internship.dbert.online` | Replace prefix with `https://lms.dbert.in` |
| `apps/portal/internship.db` | `device_profiles` | `referrer` | 3,114 | `https://internship.dbert.online/internship/profile` | Replace prefix with `https://lms.dbert.in` |
| **TOTAL DB RECORDS** | — | — | **9,097 rows** | — | Execute SQL sanitization script |


### 1.6 Packaged Distribution Archives

- `dbert-api-package-v1.zip`: Contains **67 internal files** referencing `dbert.online` and `internship.dbert.online` (including `.env.example`, `.env.production.sample`, `router.py`, `config.py`, and `website-content/`). Once `dbert-api-package` is remediated, this zip archive must be regenerated.

### 1.7 Warning Findings: Documentation, Comments, and Placeholders (81 Occurrences across 16 Files)

The following 81 findings are non-functional references in documentation, markdown files, and code comments:

| File Path | Line | Snippet | Replacement | Classification |
|---|:---:|---|---|:---:|
| `DBERT_LMS_MASTER_DEVELOPMENT_HARDENING_PLAN.md` | 6 | `**Primary production portal:** `https://internship.dbert.online/`\` | `lms.dbert.in` | Warning |
| `DBERT_LMS_MASTER_DEVELOPMENT_HARDENING_PLAN.md` | 641 | `mailer.dbert.online` | `dbert.in` | Warning |
| `DBERT_WEBSITE_UIUX_REDESIGN_PHASE_PLAN.md` | 3 | `- Production website: `https://dbert.online`` | `dbert.in` | Warning |
| `DBERT_WEBSITE_UIUX_REDESIGN_PHASE_PLAN.md` | 45 | `- break `internship.dbert.online` links,` | `lms.dbert.in` | Warning |
| `DBERT_WEBSITE_UIUX_REDESIGN_PHASE_PLAN.md` | 1102 | `Current live site is `https://dbert.online`.` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 5 | `...ive. The domain is being migrated from `dbert.online` → `dbert.in`.` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 17 | `1. `apps/portal/.env:27` — `SMTP_HOST=dbert.online` (blocker)` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 18 | `2. `apps/portal/.env:29` — `SMTP_USER=contactus@dbert.online` (blocker)` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 19 | `3. `apps/portal/.env:31` — `FROM_EMAIL=contactus@dbert.online` (blocker)` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 20 | `4. `apps/portal/app.py:304` — `SMTP_HOST` code default = `"dbert.online"` (blocker)` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 21 | `5. `apps/portal/app.py:2690` — `staff_email = f"{ADMIN_USERNAME}@dbert.online"` hardcode (blocker)` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 23 | `...ype: Organization` has `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, and `"email": "contactus@dbert.online"` (...` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 24 | `8. `apps/portal/templates/seo_landing.html:133` — anchor tag `href="https://dbert.in"` but link text reads `dbert.online` (warning — misleading UX)` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 30 | `### R1. Domain Migration Completeness — `dbert.online` → `dbert.in`` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 32 | `...kdown docs) for residual references to `dbert.online` that are NOT intentional redirect rules. Classify each reference:` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 39 | `- All Nginx configs under `deploy/` — intentional `dbert.online → dbert.in` redirect rules are OK; any other reference is a warning or blocker` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 43 | `- Portal blog redirect routes — confirm they redirect to `dbert.in/blog`, not `dbert.online`` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 69 | `...firmed the homepage JSON-LD still uses `dbert.online` — flag all pages with this issue)` | `dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 75 | `...or `dbert.in`. The redirect blocks for `dbert.online → dbert.in` and `internship.dbert.online → lms.dbert.in` are intentional — confirm they...` | `lms.dbert.in` | Warning |
| `ORIGINAL_REQUEST.md` | 96 | `- [ ] Complete list of all `dbert.online` references, each classified as Blocker/Warning/Info` | `dbert.in` | Warning |
| `QA_REPORT.md` | 10 | `**Audit Context**: Domain Migration from legacy domains (`dbert.online`, `internship.dbert.online`) to production domains (`dbert.in`, `lms.dbert.in`)` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 24 | `... pointing to legacy `https://internship.dbert.online/` in headers and footers, retains legacy `internship.dbert.online` URLs in Course and F...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 59 | `...** \| `apps/portal/.env:27` \| `SMTP_HOST=dbert.online` directs live portal transactional email connections to legacy domain mailserver. \| Cha...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 60 | `.../portal/.env:29` \| `SMTP_USER=contactus@dbert.online` specifies legacy authentication account for SMTP. \| Update to `SMTP_USER=contactus@dbe...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 61 | `...portal/.env:31` \| `FROM_EMAIL=contactus@dbert.online` causes outbound emails to fail SPF/DKIM alignment on `dbert.in` and sends user replies...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 62 | `...MTP_HOST = os.environ.get("SMTP_HOST", "dbert.online")` defaults to legacy domain if environment variable is absent. \| Change fallback defau...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 63 | `...codes `staff_email = f"{ADMIN_USERNAME}@dbert.online"`, generating non-functional admin email. \| Change hardcoded string to `f"{ADMIN_USERNA...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 65 | `...ype: Organization` has `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, and `"email": "contactus@dbert.online"`. ...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 66 | `...ert.in"` but visible anchor text reads `dbert.online`. \| Change anchor text from `dbert.online` to `dbert.in`. \| **Confirmed** \|` | `dbert.in` | Warning |
| `QA_REPORT.md` | 74 | `### Category R1: Domain Migration Completeness (`dbert.online` $\rightarrow$ `dbert.in`)` | `dbert.in` | Warning |
| `QA_REPORT.md` | 78 | `...>` tags pointing to `https://internship.dbert.online/...` (e.g. `/jobs`, `/internships`, `/cv/*`, `/program`), causing search crawlers to in...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 79 | `...0 `<loc>` tags all pointing to `https://dbert.online/...` (e.g. `/pricing`, `/verify`, `/privacy`). \| Overwrite `apps/website/sitemap.xml` w...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 80 | `... explicitly specifies `Sitemap: https://dbert.online/sitemap.xml`, directing all search engine robots to the legacy domain sitemap. \| Update...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 81 | `... HTML files link to `https://internship.dbert.online/` due to an outdated static export. \| Rebuild and export static site via `npm run expor...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 82 | `...iles) \| 203 static export files retain `dbert.online` in `og:image`, `twitter:image`, and Organization JSON-LD schemas. \| Re-export static b...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 83 | `...tion.sample:18` \| `CORS_ORIGINS=https://dbert.online,https://internship.dbert.online` restricts FastAPI CORS to legacy domains; API requests...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 84 | `... production sample specifies `SMTP_HOST=dbert.online`, `SMTP_USER=contactus@dbert.online`, and `FROM_EMAIL=contactus@dbert.online`. \| Update...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 85 | `...P_USER`, and `FROM_EMAIL` fall back to `dbert.online` if omitted from the environment. \| Update default fallbacks to `dbert.in` and `contact...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 86 | `...claims and user profile payload embed `@dbert.online` in admin authentication tokens (`f"{settings.ADMIN_USERNAME}@dbert.online"`). \| Update...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 87 | `...gacy sender email `FROM_EMAIL=contactus@dbert.online`. \| Update line 51 to `FROM_EMAIL=contactus@dbert.in` or remove obsolete `.cgi` file. \|...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 88 | `...nment file specifies `SMTP_USER=staging@dbert.online` and `FROM_EMAIL=staging@dbert.online`. \| Update to `staging@dbert.in`. \| **Confirmed**...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 90 | `... and section header comments reference `dbert.online` (code itself redirects to `https://dbert.in/blog/{slug}`). \| Update comments and docst...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 91 | `...nx configuration references `internship.dbert.online`. \| Mark file as deprecated or replace with redirection to `lms.dbert.in`. \| **Confirme...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 92 | `... under `deploy/` references `internship.dbert.online`. \| Deprecate in favor of `deploy/dbert-unified-nginx.conf`. \| **Confirmed** \|` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 93 | `...e standalone website config references `dbert.online`. \| Deprecate in favor of `deploy/dbert-unified-nginx.conf`. \| **Confirmed** \|` | `dbert.in` | Warning |
| `QA_REPORT.md` | 94 | `... \| Intentional 301 redirect blocks for `dbert.online -> dbert.in` and `internship.dbert.online -> lms.dbert.in`. \| Maintain redirect rules; ...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 122 | `...Offer", ..., "url": "https://internship.dbert.online/"}` and FAQ text references `internship.dbert.online`. \| Rebuild static export via `npm...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 123 | `...JSON-LD FAQ schema contains `internship.dbert.online` in `acceptedAnswer`. \| Rebuild static export via `npm run export:cpanel` in `apps/webs...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 126 | `...oogle AdSense Publisher Declaration for dbert.online`. \| Update header to `# Google AdSense Publisher Declaration for dbert.in`. \| **Confirm...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 137 | `...em`. Because the certificate SAN lacks `dbert.online` and `internship.dbert.online`, browser TLS handshakes abort before the 301 redirect is...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 138 | `...nginx.conf` routing only to `internship.dbert.online` on port 5001, overwriting the unified configuration. \| Replace legacy deploy script in...` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 146 | `...TP redirect for legacy domains (`http://dbert.online` $\rightarrow$ `https://dbert.online` $\rightarrow$ `https://dbert.in`), causing TLS ha...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 290 | `...D and OG tags still explicitly specify `dbert.online`.` | `dbert.in` | Warning |
| `QA_REPORT.md` | 294 | `...audit noted that blog routes reference `dbert.online`. Re-reading lines 6027 and 6067 revealed that the actual Python redirection logic issu...` | `dbert.in` | Warning |
| `QA_REPORT.md` | 315 | `- [x] **Complete list of all `dbert.online` references**: Cataloged across Python, TypeScript, HTML, XML, JSON, shell scripts, and configs, classified into Blocker, Warning, and Informational.` | `dbert.in` | Warning |
| `QA_REPORT.md` | 317 | `...site/sitemap.xml` and `robots.txt` use `dbert.online` (Blockers R1-02, R1-03), while `cpanel_public_html/sitemap.xml` uses `dbert.in`.` | `dbert.in` | Warning |
| `QA_REPORT.md` | 427 | `(Get-ChildItem -Path cpanel_public_html -Recurse -Filter *.html \| Select-String -Pattern "internship.dbert.online").Count` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 457 | `4. **Expand Certbot SAN**: Issue certificates covering `dbert.in`, `www.dbert.in`, `lms.dbert.in`, `dbert.online`, `www.dbert.online`, and `internship.dbert.online`.` | `lms.dbert.in` | Warning |
| `QA_REPORT.md` | 462 | `3. **Update Sitemaps in Portal**: Bulk replace `https://internship.dbert.online` with `https://lms.dbert.in` in `apps/portal/sitemap.xml`.` | `lms.dbert.in` | Warning |
| `WEBSITE_ROUTE_INVENTORY.md` | 4 | `- **Production URL**: `https://dbert.online`` | `dbert.in` | Warning |
| `WEBSITE_UIUX_PHASE_PLAN.md` | 4 | `- **Target Site**: `https://dbert.online` (Repository: `DBERT-INDIA/dbert-website-lms`, Scope: `apps/website/**`)` | `dbert.in` | Warning |
| `WEBSITE_UIUX_PHASE_PLAN.md` | 140 | `.../website/src/app/robots.ts` to `https://dbert.online` as the definitive production fallback, matching `sitemap.ts`.` | `dbert.in` | Warning |
| `WEBSITE_UIUX_PHASE_PLAN.md` | 171 | `- Verify that all `internship.dbert.online` outbound link targets remain active, consistent, and correctly tagged with `rel="noopener noreferrer"`.` | `lms.dbert.in` | Warning |
| `WEBSITE_UIUX_PRODUCTION_PREFLIGHT.md` | 7 | `**Target Domain**: `https://dbert.online`` | `dbert.in` | Warning |
| `WEBSITE_UIUX_PRODUCTION_PREFLIGHT.md` | 38 | `\| `NEXT_PUBLIC_SITE_URL` \| Global canonical \| Defaults strictly to authoritative `https://dbert.online` in `layout.tsx`, `sitemap.ts`, and `robots.ts` \| Verified \|` | `dbert.in` | Warning |
| `WEBSITE_UIUX_PRODUCTION_PREFLIGHT.md` | 82 | `...All links targeting `https://internship.dbert.online/` (fellowship applications, cohort registrations, job board) feature `target="_blank"` ...` | `lms.dbert.in` | Warning |
| `WEBSITE_UIUX_PROGRESS.md` | 29 | `...Canonical URL domain unified to https://dbert.online, robots.txt sitemap aligned, 64 SEO entries verified \|` | `dbert.in` | Warning |
| `.agent/FINAL_RELEASE_GATE_REPORT.md` | 4 | `**Primary Production Portal:** `https://internship.dbert.online/`` | `lms.dbert.in` | Warning |
| `dbert-api-package/docs/env_vars.md` | 30 | `\| `FROM_EMAIL` \| `contactus@dbert.online` \| NO \| Environment configuration parameter \|` | `dbert.in` | Warning |
| `dbert-api-package/docs/env_vars.md` | 65 | `\| `SITE_ORIGIN` \| `https://internship.dbert.online` \| NO \| Environment configuration parameter \|` | `lms.dbert.in` | Warning |
| `dbert-api-package/docs/env_vars.md` | 70 | `\| `SMTP_HOST` \| `dbert.online` \| NO \| Environment configuration parameter \|` | `dbert.in` | Warning |
| `dbert-api-package/docs/env_vars.md` | 73 | `\| `SMTP_USER` \| `contactus@dbert.online` \| NO \| Environment configuration parameter \|` | `dbert.in` | Warning |
| `dbert-api-package/docs/integrations.md` | 47 | `- **Primary Host**: `SMTP_HOST` (`dbert.online`), port 465 (SSL).` | `dbert.in` | Warning |
| `dbert-api-package/website-content/public/.htaccess` | 15 | `# 1.1 Redirect /jobs and /internships to internship.dbert.online subdomain` | `lms.dbert.in` | Warning |
| `dbert-api-package/website-content/public/ads.txt` | 1 | `# Google AdSense Publisher Declaration for dbert.online` | `dbert.in` | Warning |
| `dbert-api-package/website-content/src/components/ui/MultiStepForm.tsx` | 160 | `<input type="email" name="email" required value={formData.email} onChange={handleInputChange} placeholder="you@dbert.online" />` | `dbert.in` | Warning |
| `dbert-api-package/website-content/src/components/ui/RegionalOpportunityBento.module.css` | 2 | `Bilateral keyword anchors linking dbert.online -> internship.dbert.online */` | `lms.dbert.in` | Warning |
| `deploy/FIRST_TIME_EC2_DEPLOYMENT.md` | 134 | `sudo cp /var/www/dbert-website-lms/deploy/nginx.conf /etc/nginx/sites-available/internship.dbert.online` | `lms.dbert.in` | Warning |
| `deploy/FIRST_TIME_EC2_DEPLOYMENT.md` | 135 | `sudo ln -sf /etc/nginx/sites-available/internship.dbert.online /etc/nginx/sites-enabled/` | `lms.dbert.in` | Warning |
| `deploy/FIRST_TIME_EC2_DEPLOYMENT.md` | 141 | `sudo certbot --nginx -d internship.dbert.online` | `lms.dbert.in` | Warning |
| `deploy/FIRST_TIME_EC2_DEPLOYMENT.md` | 156 | `2. `https://internship.dbert.online/` loads with valid SSL.` | `lms.dbert.in` | Warning |

---

## 2. Logic Chain

### Step 1: Baseline Remediation Verification

- *Observation*: Files `apps/portal/.env`, `apps/portal/app.py`, `deploy/deploy_ec2_unified.sh`, `cpanel_public_html/__next.__PAGE__.txt`, and `apps/portal/templates/seo_landing.html` all display remediated `dbert.in` values on disk (Lines 27, 29, 31 in `.env`, Lines 309, 2698 in `app.py`, Line 49 in `__PAGE__.txt`).
- *Inference*: The 8 baseline issues flagged in preliminary scans were addressed in the active working tree but were never committed or reconciled across secondary packages.

### Step 2: Root-Cause Analysis of `dbert-api-package/website-content/`

- *Observation*: A full file comparison between `apps/website/src` (250 files) and `dbert-api-package/website-content/src` (225 files) reveals that 166 files are 100% byte-for-byte identical, while 59 files differ. Comparing the diffs (e.g. `Footer.tsx`, `layout.tsx`, course pages) demonstrates that the diff consists entirely of the domain migration replacements (`https://internship.dbert.online` $\rightarrow$ `https://lms.dbert.in`, `dbert.online` $\rightarrow$ `dbert.in`).
- *Inference*: `dbert-api-package/website-content` was duplicated from an older version of `apps/website` before domain migration occurred. It was never synchronized when `apps/website/src` was updated. Consequently, 175 blocker references exist in this sub-tree.

### Step 3: Architectural Legitimacy of Intentional Redirect Rules

- *Observation*: `deploy/dbert-unified-nginx.conf` contains dedicated server blocks for `dbert.online` (lines 28-40, 58-67) and `internship.dbert.online` (lines 42-54, 70-79) issuing `return 301 https://dbert.in$request_uri` and `return 301 https://lms.dbert.in$request_uri`. In addition, line 229 of `deploy/deploy_ec2_unified.sh` includes `dbert.online` and `internship.dbert.online` in the Certbot command.
- *Inference*: These rules must NOT be removed. Without them, existing inbound traffic, search engine bookmarks, and legacy external links would fail to connect or trigger SSL certificate mismatch warnings. These are intentional, production-grade 301 redirect blocks.

### Step 4: The Database Contamination Threat Vector

- *Observation*: The SQLite databases `apps/portal/internship.db` and root `internship.db` store 9,097 rows containing legacy domain strings across `staff_accounts`, `notifications`, `device_profiles`, `companies`, and `post_applications`.
- *Inference*: `scripts/migrate_all_ec2_data.py` reads SQLite tables and inserts records directly into PostgreSQL (`dbert_internship` schema). If the database is migrated without string replacement, every historical and seeded notification link will send users to `https://internship.dbert.online`, and staff email logins will retain `@dbert.online`, causing authentication and notification failures.

---

## 3. Caveats

1. **Pre-existing Local Working Tree Modifications**: Several files in the working directory (such as `apps/portal/app.py`, `apps/portal/.env`, `apps/website/.htaccess`, `dbert-api-package/.env.example`) have uncommitted modifications from prior development work. These changes were validated as correct and aligned with `dbert.in`.
2. **Historical Phase Documentation**: The 8 markdown documentation files at the repository root (`DBERT_LMS_MASTER_DEVELOPMENT_HARDENING_PLAN.md`, etc.) describe past architectural phases where `dbert.online` was the active production target. While classified as Warnings, updating them is optional and should not take precedence over functional code changes.
3. **External Certbot Issuance**: The Nginx 301 HTTPS redirect rules require valid SSL certificates for `dbert.online` and `internship.dbert.online`. If DNS A-records for the legacy domains are not pointed to the EC2 IP (`3.26.237.171`), Certbot will fail to issue certificates for those SAN domains. In that scenario, Nginx will fail to start if the certificate path does not exist.

---

## 4. Conclusion & Actionable Remediation Plan

To achieve 100% domain migration completeness under Requirement R1, the implementation team must execute four scoped remediation actions:

### Remediation Action 1: Synchronize `dbert-api-package/website-content` with `apps/website`

Because `dbert-api-package/website-content/src/` is an exact subset of `apps/website/src/`, all 175 Blocker defects in `dbert-api-package/website-content/` can be remediated cleanly and without regression by copying the updated files from `apps/website/src/`:

```bash
# In repository root:
cp -r apps/website/src/* dbert-api-package/website-content/src/
cp apps/website/.htaccess dbert-api-package/website-content/public/.htaccess
cp apps/website/ads.txt dbert-api-package/website-content/public/ads.txt
```

### Remediation Action 2: Update API Documentation (`dbert-api-package/docs/`)

- In `dbert-api-package/docs/env_vars.md`:

  - Line 30: Change `contactus@dbert.online` to `contactus@dbert.in`

  - Line 65: Change `https://internship.dbert.online` to `https://lms.dbert.in`

  - Line 70: Change `dbert.online` to `dbert.in`

  - Line 73: Change `contactus@dbert.online` to `contactus@dbert.in`

- In `dbert-api-package/docs/integrations.md`:

  - Line 47: Change `dbert.online` to `dbert.in`

### Remediation Action 3: Database Legacy Domain Sanitization

Execute the following SQL update statements across both `apps/portal/internship.db` and root `internship.db` (or incorporate into `scripts/migrate_all_ec2_data.py` before inserting rows into PostgreSQL):

```sql
-- 1. Update staff account emails
UPDATE staff_accounts
SET email = REPLACE(email, '@dbert.online', '@dbert.in')
WHERE email LIKE '%@dbert.online';

-- 2. Update company website URLs
UPDATE companies
SET website = REPLACE(website, 'internship.dbert.online', 'lms.dbert.in')
WHERE website LIKE '%internship.dbert.online%';

-- 3. Update application comments
UPDATE post_applications
SET comment = REPLACE(comment, 'internship.dbert.online', 'lms.dbert.in')
WHERE comment LIKE '%internship.dbert.online%';

-- 4. Update notifications links
UPDATE notifications
SET link = REPLACE(link, 'https://internship.dbert.online', 'https://lms.dbert.in')
WHERE link LIKE '%https://internship.dbert.online%';

-- 5. Update device profiles referrer
UPDATE device_profiles
SET referrer = REPLACE(referrer, 'https://internship.dbert.online', 'https://lms.dbert.in')
WHERE referrer LIKE '%https://internship.dbert.online%';
```

### Remediation Action 4: Regenerate `dbert-api-package-v1.zip`

Once `dbert-api-package/website-content/` and `dbert-api-package/docs/` are remediated, re-package the standalone archive:

```bash
zip -r dbert-api-package-v1.zip dbert-api-package/ -x "*/__pycache__/*" "*/.git/*"
```

### Remediation Action 5: EC2 Nginx Configuration Verification

Preserve the 301 redirect blocks in `deploy/dbert-unified-nginx.conf` (lines 28-79). Ensure that DNS A-records for `dbert.online`, `www.dbert.online`, and `internship.dbert.online` point to EC2 IP `3.26.237.171` before Certbot issues SSL certificates.

---

## 5. Verification Method

### Independent Verification Commands

1. **Repository-Wide Grep for Unintended Occurrences**:

   Run the following command to verify zero unintended references remain in source files:

   ```powershell
   git grep -n -I "dbert.online" -- ':!deploy/dbert-unified-nginx.conf' ':!apps/website/.htaccess' ':!apps/website/public/.htaccess' ':!cpanel_public_html/.htaccess' ':!deploy/deploy_ec2_unified.sh' ':!deploy/FILEZILLA_DEPLOYMENT_GUIDE.md' ':!*.md' ':!scratch/'
   ```

   *Expected output*: Zero matches.


2. **Verification of `dbert-api-package/website-content`**:

   ```powershell
   git grep -n -I "dbert.online" dbert-api-package/website-content/
   ```

   *Expected output*: Zero matches.


3. **Database Verification Query**:

   ```powershell
   python -c "
   import sqlite3
   conn = sqlite3.connect('apps/portal/internship.db')
   for table in ['staff_accounts', 'companies', 'post_applications', 'notifications', 'device_profiles']:
       cnt = conn.execute(f\"SELECT count(*) FROM {table} WHERE email LIKE '%dbert.online%' OR website LIKE '%dbert.online%' OR comment LIKE '%dbert.online%' OR link LIKE '%dbert.online%' OR referrer LIKE '%dbert.online%'\").fetchone()[0] if table != 'device_profiles' else conn.execute(f\"SELECT count(*) FROM {table} WHERE referrer LIKE '%dbert.online%'\").fetchone()[0]
       print(f'{table}: {cnt} legacy records')
   "
   ```

   *Expected output*: All counts equal 0.


4. **Invalidation Conditions**:

   - If any active route, metadata tag, JSON-LD schema, or email in `apps/website/`, `apps/portal/`, or `dbert-api-package/` resolves to `dbert.online`.

   - If Nginx removes the legacy 301 redirect server blocks, causing old bookmarks to drop.
