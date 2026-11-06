# Requirement R3: Website Readiness Audit Report

**Auditor**: `explorer_r3` (Website Readiness Auditor)  
**Target Subsystems**: `cpanel_public_html/` (deployed static build), `apps/website/` (Next.js source & build outputs), and `deploy/` (Nginx reverse proxy configurations)  
**Date**: 2026-10-25 / 2026-10-26  
**Status**: Complete Investigation — Ready for Review and Assembly  

---

## Executive Summary

A comprehensive, zero-assumption static audit of the DBERT static export (`cpanel_public_html/`) and the Next.js website source (`apps/website/`) was conducted across all seven (7) sub-requirements of R3.

Key discoveries:
1. **Dead Internal Links**: All **89 distinct internal `href` targets** starting with `/` present in `cpanel_public_html/` exist on disk as directories containing `index.html` (100% resolution for public static routes). However, **admin routes** (`/admin/login`, `/admin/leads`, `/admin/cohort-applications`, `/admin/alkame-contributors`) exist in source code (`apps/website/src/app/admin/`) but were excluded from `cpanel_public_html/` and will return 404 if accessed on static hosting. Furthermore, **1,226 outgoing links** across all 74 HTML files in `cpanel_public_html/` point to legacy `https://internship.dbert.online/...` because `cpanel_public_html` is a stale build exported before source link updates.
2. **Missing 404 Directive in Nginx**: `cpanel_public_html/404.html` (36,312 bytes) and `cpanel_public_html/404/index.html` exist. Apache `.htaccess` contains `ErrorDocument 404 /404.html`. However, in `deploy/dbert-unified-nginx.conf` (lines 49–91) and `deploy/dbert-website-nginx.conf` (lines 22–53), the `error_page 404` directive is **completely missing**.
3. **Sitemap Domain**: In `cpanel_public_html/sitemap.xml`, all 70 `<loc>` tags correctly use `https://dbert.in/...`. However, at `apps/website/sitemap.xml` (the root file in the website repository), all 70 `<loc>` tags point to `https://dbert.online/...` (**Blocker**).
4. **Robots.txt Directive**: `cpanel_public_html/robots.txt:13` correctly specifies `Sitemap: https://dbert.in/sitemap.xml`. However, `apps/website/robots.txt:13` specifies `Sitemap: https://dbert.online/sitemap.xml` (**Blocker**).
5. **OG / Meta Tags**: Across all 74 HTML files in `cpanel_public_html/`, 743 meta tags were verified; `og:image` and `twitter:image` point to `https://dbert.in/og-image.jpg`, and `og:url` uses `https://dbert.in/...`. However, `twitter:site` is completely omitted in `apps/website/src/app/layout.tsx:50–75`, and legacy static HTML/txt files committed at the root of `apps/website/` still contain `dbert.online` metadata. Both `cpanel_public_html/ads.txt:1` and `apps/website/ads.txt:1` reference `dbert.online`.
6. **_next/ Asset Integrity**: 40 distinct `/_next/static/` asset paths (JS chunks, CSS stylesheets, woff2 media fonts) are referenced across HTML files in `cpanel_public_html/`. 100% (40/40) are verified present on disk in `cpanel_public_html/_next/static/`. However, there is a build hash mismatch between `cpanel_public_html/_next/static/chunks/` and `apps/website/.next/static/chunks/`: 11 chunk files in `cpanel_public_html` do not exist in `apps/website/.next`. If Nginx's `location /_next/static/` alias points to `apps/website/.next/static/`, client browsers requesting `cpanel_public_html` HTML pages will receive HTTP 404 errors on script chunks.
7. **JSON-LD Structured Data**: 118 `<script type="application/ld+json">` elements were extracted across `cpanel_public_html/`. 114 use `dbert.in`, but **4 schema blocks** reference `internship.dbert.online` in `cpanel_public_html/learners/index.html` (FAQ) and `cpanel_public_html/learners/fellowship/index.html` (Course `offers.url` and FAQ) (**Blocker**). Pre-scan finding #7 was also verified: `apps/website/__next.__PAGE__.txt` contains Organization schema with `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, and `"email": "contactus@dbert.online"`.

---

## 1. Observations

### 1.1 Complete Internal Links Audit (`cpanel_public_html/`)
- Analyzed all 74 HTML files in `cpanel_public_html/` containing a total of **7,874 anchor tags (`<a>`)**.
- Identified **89 distinct internal `href` attributes** beginning with `/`.
- For each path, checked whether `cpanel_public_html/<path>/index.html` (or matching file) exists.
- **Results**: 89 / 89 targets exist. 0 dead ends among public static routes.

#### Table of All 89 Internal Links
| # | Internal `href` | Target Relative Path | Target Exists? | Occurrences | Sample Source Location |
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

#### Missing / Unexported Routes (Static 404 Dead Ends)
While all 89 public internal routes resolve, the following routes are defined and linked within source code (`apps/website/src/app/admin/`) but do NOT exist in `cpanel_public_html/`:
1. `/admin/login` (`apps/website/src/app/admin/login/page.tsx:1`) — missing in `cpanel_public_html/`
2. `/admin/leads` (`apps/website/src/app/admin/leads/page.tsx:54`) — missing in `cpanel_public_html/`
3. `/admin/cohort-applications` (`apps/website/src/app/admin/cohort-applications/page.tsx:48`) — missing in `cpanel_public_html/`
4. `/admin/alkame-contributors` (`apps/website/src/app/admin/alkame-contributors/page.tsx:47`) — missing in `cpanel_public_html/`

---

### 1.2 Missing 404 Page & Nginx Directive Audit
- `cpanel_public_html/404.html` exists on disk (36,312 bytes).
- `cpanel_public_html/404/index.html` exists on disk (36,312 bytes).
- `cpanel_public_html/_not-found/index.html` exists on disk (36,312 bytes).
- Apache `.htaccess` (`cpanel_public_html/.htaccess:45`) contains:
  ```apache
  ErrorDocument 404 /404.html
  ```
- **Nginx Configuration Check**:
  - `deploy/dbert-unified-nginx.conf` was inspected (lines 1–143). Line 49–91 configures the server block for `dbert.in` / `www.dbert.in`. There is **no `error_page 404` directive** anywhere in the file.
  - `deploy/dbert-website-nginx.conf` was inspected (lines 1–54). Line 22–53 configures the server block for `dbert.online`. There is **no `error_page 404` directive** anywhere in the file.
  - `grep_search` across `deploy/` for `error_page` returned **0 matches**.

---

### 1.3 `sitemap.xml` Domain Audit
- **`cpanel_public_html/sitemap.xml`**:
  - Parsed XML tree with Python `xml.etree.ElementTree`.
  - Total `<loc>` entries: **70**.
  - All 70 `<loc>` entries begin with `https://dbert.in/...` (e.g., `https://dbert.in`, `https://dbert.in/pricing`, `https://dbert.in/verify`).
  - Entries pointing to non-`dbert.in` domains: **0**.
- **`apps/website/sitemap.xml` (Committed at root of `apps/website/`)**:
  - Lines 1–424.
  - Total `<loc>` entries: **70**.
  - **70 out of 70 entries** use `https://dbert.online/...` (e.g., `https://dbert.online`, `https://dbert.online/pricing`, `https://dbert.online/verify`).
  - This is a legacy build artifact committed to version control.
- **`apps/website/src/app/sitemap.ts` (Next.js Dynamic Generator)**:
  - Line 11:
    ```typescript
    const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in';
    ```
  - The dynamic code uses `dbert.in` as fallback and environment variable default.

---

### 1.4 `robots.txt` Domain & Sitemap Directive Audit
- **`cpanel_public_html/robots.txt`**:
  - Inspected line 13:
    ```text
    Sitemap: https://dbert.in/sitemap.xml
    ```
  - Correct domain `dbert.in`.
- **`apps/website/robots.txt`**:
  - Inspected line 13:
    ```text
    Sitemap: https://dbert.online/sitemap.xml
    ```
  - Legacy domain `dbert.online` (**Blocker**).
- **`apps/website/src/app/robots.ts`**:
  - Line 5 & 23:
    ```typescript
    const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in';
    ...
    sitemap: `${baseUrl}/sitemap.xml`,
    ```
  - Dynamic route correctly falls back to `dbert.in`.

---

### 1.5 OG / Meta Tags Audit
- Parsed all 74 HTML files in `cpanel_public_html/` (743 meta tags):
  - `og:image`: Verified 1 unique value: `https://dbert.in/og-image.jpg`.
  - `twitter:image`: Verified 1 unique value: `https://dbert.in/og-image.jpg`.
  - `og:url`: Verified 58 unique values; all begin with `https://dbert.in/...`.
  - `canonical`: All `<link rel="canonical">` point to `https://dbert.in/...`.
- **Omissions and Warnings**:
  - `twitter:site` meta tag is **omitted** across all pages in `cpanel_public_html/` and not configured in `apps/website/src/app/layout.tsx:50–75`.
  - `cpanel_public_html/ads.txt:1` and `apps/website/ads.txt:1` contain:
    ```text
    # Google AdSense Publisher Declaration for dbert.online
    ```
  - Root directory `apps/website/` contains legacy committed HTML/txt files (`apps/website/about.html`, `apps/website/terms.html`, etc.) where `og:url` is `https://dbert.online/...`.

---

### 1.6 `_next/` Asset Integrity Audit
- Scanned all 74 HTML files in `cpanel_public_html/` for asset references matching `/_next/static/...`.
- Extracted **40 unique asset paths** (33 JavaScript chunks in `_next/static/chunks/`, 4 CSS stylesheets, and 3 media font woff2 files).
- Tested existence of each asset against `cpanel_public_html/_next/static/`:
  - Assets verified present on disk: **40 / 40 (100%)**.
  - Missing assets in `cpanel_public_html`: **0**.
  - Sample verified assets:
    - `/_next/static/chunks/0cz1d0mv5g_q7.js` (112,594 bytes)
    - `/_next/static/chunks/1ce_t9p6e6jmd.css` (95,994 bytes)
    - `/_next/static/chunks/1gx_vpj24twrz.js` (47,681 bytes)
    - `/_next/static/chunks/turbopack-1jn-nl1sxiodu.js` (1,844 bytes)
- **Divergence with `apps/website/.next/static/`**:
  - `cpanel_public_html/_next/static/chunks/` contains 38 files from build `edkBX5J1Sjh_ThQVdswwo`.
  - `apps/website/.next/static/chunks/` contains 43 files from a different standalone build.
  - **11 chunk files** present in `cpanel_public_html` are missing from `apps/website/.next`:
    `22848iis4ukqu.js`, `2oezh9wstdq14.js`, `1_oj3cz2aubcl.js`, `turbopack-1jn-nl1sxiodu.js`, `1ossk8al_2eyy.js`, `31va23538h0hj.js`, `1wwtria7x7b6u.js`, `0959gajrrg6k-.js`, `1efphwo_o8v47.js`, `3qg39vbkkzp9v.js`, `2gzar0snbpg-l.js`.
  - If `deploy/dbert-unified-nginx.conf:72` sets `alias /var/www/dbert-website-lms/apps/website/.next/static/;` while Nginx serves static HTML from `cpanel_public_html/`, clients will receive 404 on those 11 script chunks.

---

### 1.7 JSON-LD Structured Data Audit
- Extracted 118 `<script type="application/ld+json">` elements across all 74 HTML files in `cpanel_public_html/`.
- 114 schema blocks correctly use `dbert.in`.
- **4 schema blocks reference `internship.dbert.online`** (**Blocker**):
  1. `cpanel_public_html/learners/index.html:1`:
     - Inside `FAQPage` schema: `acceptedAnswer.text` contains:
       `"...passing our rigorous external code screening challenge at internship.dbert.online."`
  2. `cpanel_public_html/learners/index.html:1`:
     - Inside `@graph` schema: duplicate FAQ text contains `internship.dbert.online`.
  3. `cpanel_public_html/learners/fellowship/index.html:1`:
     - Inside `Course` schema: `offers.url` contains:
       `"url": "https://internship.dbert.online/"`
  4. `cpanel_public_html/learners/fellowship/index.html:1`:
     - Inside `FAQPage` schema: `acceptedAnswer.text` contains:
       `"Applications run through the DBERT internship platform at internship.dbert.online."`
- **Confirmation of Pre-confirmed Finding #7**:
  - In `apps/website/__next.__PAGE__.txt:49` (and lines across other committed `*.txt` full-tree manifests in `apps/website/`), the Organization schema has:
    - `"url": "https://dbert.online"`
    - `"logo": "https://dbert.online/logo.svg"`
    - `"email": "contactus@dbert.online"`
  - Confirmed as **Blocker**.

---

### 1.8 Legacy Domain Links in `cpanel_public_html/` (Critical Systemic Discovery)
- While internal `href` attributes pointing to `/` are intact, full-text scan of all 74 HTML files in `cpanel_public_html/` revealed **1,226 occurrences** of outbound links pointing to:
  `https://internship.dbert.online/...`
- Found across all 74 HTML pages inside `<header>` (`MegaMenu`) and `<footer>` (`Footer`):
  - `https://internship.dbert.online/` (Navbar CTA, Drawer CTA)
  - `https://internship.dbert.online/jobs` (Navbar link, Footer link)
  - `https://internship.dbert.online/apply` (Navbar highlight link)
  - 37 deep links in Footer regional SEO mesh (e.g. `/internships/agentic-search-systems-intern-delhi-ncr-remote-11`, `/internships/booking-system-development-intern-mumbai-remote-50`, `/internships/data-analyst-internship-work-from-home`, etc.)
- In contrast, `apps/website/src/components/layout/Footer.tsx:71–77` and `apps/website/src/data/nav.config.json:121–146` have already been updated in source code to `https://lms.dbert.in`. The deployed static build `cpanel_public_html/` is stale and must be regenerated via `npm run export:cpanel`.

---

## 2. Logic Chain

1. **Dead Link Analysis**:
   - *Premise*: Next.js static HTML export generates route directories containing `index.html`.
   - *Observation*: `find_by_name` and python tree traversal confirmed all 89 distinct internal `href` values have a matching `<path>/index.html` in `cpanel_public_html/`.
   - *Observation*: The source code has `/admin` routes, but `next export` omitted them.
   - *Deduction*: The public site has 0 dead internal links, but administrative routes will return 404 if hosted statically without Next.js Node.js runtime.

2. **Nginx 404 Error Directive**:
   - *Premise*: Requirement R3.2 mandates verifying `404.html` exists and Nginx config has an `error_page 404` directive.
   - *Observation*: `cpanel_public_html/404.html` exists (36,312 bytes). Apache `.htaccess` contains `ErrorDocument 404 /404.html`.
   - *Observation*: Neither `deploy/dbert-unified-nginx.conf` nor `deploy/dbert-website-nginx.conf` contains an `error_page 404` directive or an internal redirect to `/404.html`.
   - *Deduction*: When Nginx encounters a non-existent static resource or upstream 404, it will serve its default, unbranded Nginx 404 response instead of the branded DBERT 404 page.

3. **Sitemap and Robots Domain Inconsistency**:
   - *Premise*: All indexing directives must strictly point to `dbert.in`.
   - *Observation*: `cpanel_public_html/sitemap.xml` and `cpanel_public_html/robots.txt` point to `dbert.in`.
   - *Observation*: `apps/website/sitemap.xml` and `apps/website/robots.txt` committed in the source repository point to `https://dbert.online/...`.
   - *Deduction*: If deployment scripts or CI/CD pipelines copy static files from `apps/website/` root, or if Nginx serves `apps/website/sitemap.xml`, crawlers will be directed to index the decommissioned domain `dbert.online`.

4. **Structured Data & Stale Static Build**:
   - *Premise*: Search engines and AI crawlers consume JSON-LD schema to index corporate entities, courses, and FAQs.
   - *Observation*: In `cpanel_public_html/learners/index.html` and `cpanel_public_html/learners/fellowship/index.html`, 4 JSON-LD blocks point to `internship.dbert.online`.
   - *Observation*: In source code (`apps/website/src/app/learners/page.tsx:27` and `apps/website/src/app/learners/fellowship/page.tsx:74, 103`), these have already been replaced with `lms.dbert.in`.
   - *Observation*: `cpanel_public_html/` contains 1,226 legacy `internship.dbert.online` links in `MegaMenu` and `Footer`.
   - *Deduction*: The files in `cpanel_public_html/` were generated from an older build prior to the domain migration commit. Deploying `cpanel_public_html/` directly without re-running `npm run export:cpanel` will expose thousands of dead domain references to users and search engines.

5. **_next/ Static Asset Serving Risk**:
   - *Premise*: Static chunk hashes change across Next.js build runs.
   - *Observation*: 40 referenced chunks in `cpanel_public_html` exist in `cpanel_public_html/_next/static/`. However, 11 of those chunks do not exist in `apps/website/.next/static/chunks/`.
   - *Observation*: `deploy/dbert-unified-nginx.conf:73` maps `location /_next/static/` to `alias /var/www/dbert-website-lms/apps/website/.next/static/;`.
   - *Deduction*: Serving `cpanel_public_html` HTML pages behind this Nginx configuration will cause client-side chunk loading failures (HTTP 404) for all 11 disparate chunks, breaking React hydration and client interactivity.

---

## 3. Detailed Classified Findings

| ID | File:Line | Classification | Description | Recommended Fix |
|---|---|:---:|---|---|
| **R3-01** | `deploy/dbert-unified-nginx.conf:62` | **Blocker** | Missing `error_page 404` directive in Nginx main website server block (`https://dbert.in`). Unhandled 404s serve raw Nginx error page. | Add `error_page 404 /404.html;` and `location = /404.html { root /var/www/dbert-website-lms/cpanel_public_html; internal; }` or proxy intercept. |
| **R3-02** | `deploy/dbert-website-nginx.conf:36` | **Warning** | Missing `error_page 404` directive in standalone website Nginx config. | Add `error_page 404 /404.html;` directive. |
| **R3-03** | `apps/website/sitemap.xml:1–424` | **Blocker** | Committed `sitemap.xml` at root of `apps/website/` contains 70 `<loc>` entries pointing to `https://dbert.online/...`. | Overwrite `apps/website/sitemap.xml` with `cpanel_public_html/sitemap.xml` or regenerate via `npm run build`. |
| **R3-04** | `apps/website/robots.txt:13` | **Blocker** | Committed `robots.txt` at root of `apps/website/` has `Sitemap: https://dbert.online/sitemap.xml`. | Update line 13 to `Sitemap: https://dbert.in/sitemap.xml`. |
| **R3-05** | `cpanel_public_html/learners/fellowship/index.html:1` | **Blocker** | JSON-LD schema for Course contains `"offers": {"url": "https://internship.dbert.online/"}` and FAQ answer references `internship.dbert.online`. | Regenerate `cpanel_public_html/` via `npm run export:cpanel` (source file `apps/website/src/app/learners/fellowship/page.tsx` is already fixed). |
| **R3-06** | `cpanel_public_html/learners/index.html:1` | **Blocker** | JSON-LD FAQ schema contains `internship.dbert.online` in acceptedAnswer. | Regenerate `cpanel_public_html/` via `npm run export:cpanel` (source file `apps/website/src/app/learners/page.tsx` is already fixed). |
| **R3-07** | `apps/website/__next.__PAGE__.txt:49` | **Blocker** | Pre-confirmed Finding #7: JSON-LD Organization schema contains `"url": "https://dbert.online"`, `"logo": "https://dbert.online/logo.svg"`, `"email": "contactus@dbert.online"`. | Delete stale static files from `apps/website/` root or regenerate during production build. |
| **R3-08** | `cpanel_public_html/* (74 HTML files)` | **Blocker** | 1,226 anchor tags across all 74 HTML files in `cpanel_public_html/` link to `https://internship.dbert.online/...` (stale static build). | Re-run `npm run export:cpanel` in `apps/website` to compile current `Footer.tsx` and `nav.config.json` into static HTML. |
| **R3-09** | `deploy/dbert-unified-nginx.conf:72–76` | **Blocker** | Static asset mismatch: Nginx `/_next/static/` points to `apps/website/.next/static/`, but 11 chunks referenced in `cpanel_public_html/` do not exist in `.next`. | Ensure Nginx serves assets from the exact build artifact directory being delivered to clients. |
| **R3-10** | `cpanel_public_html/ads.txt:1` | **Warning** | Line 1 contains header `# Google AdSense Publisher Declaration for dbert.online`. | Update line 1 to `# Google AdSense Publisher Declaration for dbert.in`. |
| **R3-11** | `apps/website/ads.txt:1` | **Warning** | Line 1 contains header `# Google AdSense Publisher Declaration for dbert.online`. | Update line 1 to `# Google AdSense Publisher Declaration for dbert.in`. |
| **R3-12** | `apps/website/src/app/layout.tsx:50–75` | **Info** | `twitter:site` (e.g. `@dbert_india`) is omitted from root metadata configuration. | Add `twitter: { site: '@dbert_india', creator: '@dbert_india' }` in `metadata` in `layout.tsx`. |
| **R3-13** | `cpanel_public_html/admin/*` | **Warning** | Admin pages (`/admin/login`, `/admin/leads`, etc.) in source (`src/app/admin/`) are omitted from static build (404 on cPanel). | Document that `/admin` requires Node.js runtime (`standalone` server on EC2 port 3001) or add static fallback. |

---

## 4. Caveats

1. **Static vs. Node.js Dynamic Hosting Modes**:
   - The repository contains both a static export intended for cPanel / Apache (`cpanel_public_html/`) and a standalone Node.js server build for EC2 (`apps/website/.next/standalone`).
   - The findings distinguish between the two: `cpanel_public_html/` is an Apache-targeted static bundle, whereas `deploy/dbert-unified-nginx.conf` proxies `/` to Node.js on port 3001. If the project runs purely on EC2 via Node.js, `cpanel_public_html/` is not served by Nginx. However, if `cpanel_public_html/` is deployed to cPanel, all static issues (stale build links, 404 fallback, missing admin) apply immediately.
2. **Third-Party External Links**:
   - Outbound links to external partner sites (`https://alkameinc.info/`, `https://digitalblaize.in/`, `https://gayatridevi.ai/`, `https://github.com/DBERT-INDIA`) were verified as intentional external outbound links.
3. **No Live Network Queries**:
   - All observations are based on local filesystem analysis without outbound internet access to test live domain DNS resolution or third-party SSL certificates.

---

## 5. Conclusion

1. **Public Internal Navigation is Mechanically Intact**: Every internal route in `cpanel_public_html/` resolves to an existing directory and `index.html`. No 404 broken internal links exist among public routes.
2. **The Deployed Static Build is Stale**: `cpanel_public_html/` contains 1,226 legacy `internship.dbert.online` links and 4 JSON-LD schema blocks using `internship.dbert.online`. Re-exporting via `npm run export:cpanel` will immediately eliminate these, as the source code in `apps/website/src/` has already been updated.
3. **Nginx Configuration Needs 404 Directive**: `error_page 404` must be explicitly added to `dbert-unified-nginx.conf` and `dbert-website-nginx.conf`.
4. **Committed Root SEO Files Need Alignment**: `apps/website/sitemap.xml` and `apps/website/robots.txt` must be updated or replaced with their `dbert.in` equivalents.

---

## 6. Verification Method

To independently reproduce and verify all findings in this report, run the following commands from the workspace root (`c:\Users\user\Desktop\dbert-website-lms`):

### Verify Internal Links & Dead Ends:
```powershell
python -c "
import os, urllib.parse
from html.parser import HTMLParser

class H(HTMLParser):
    def __init__(self): super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for k, v in attrs:
                if k == 'href' and v and v.startswith('/'): self.links.append(v)

base = 'cpanel_public_html'
hrefs = set()
for r, _, fs in os.walk(base):
    for f in fs:
        if f.endswith('.html'):
            p = H(); p.feed(open(os.path.join(r, f), encoding='utf-8', errors='ignore').read())
            hrefs.update(p.links)

dead = []
for h in hrefs:
    clean = urllib.parse.urlparse(h).path.strip('/')
    target = os.path.join(base, clean, 'index.html') if clean else os.path.join(base, 'index.html')
    if not (os.path.isfile(target) or os.path.isfile(os.path.join(base, clean))):
        dead.append(h)
print(f'Distinct internal hrefs: {len(hrefs)}, Dead: {len(dead)}')
"
```

### Verify Nginx Missing 404 Directive:
```powershell
Select-String -Path "deploy\*.conf" -Pattern "error_page\s+404"
# Returns 0 results (Directive is missing)
```

### Verify Sitemap & Robots Domains:
```powershell
Select-String -Path "apps\website\robots.txt" -Pattern "Sitemap:"
# Returns: Sitemap: https://dbert.online/sitemap.xml (Blocker)

Select-String -Path "cpanel_public_html\robots.txt" -Pattern "Sitemap:"
# Returns: Sitemap: https://dbert.in/sitemap.xml (Correct)

python -c "
import xml.etree.ElementTree as ET
t1 = ET.parse('apps/website/sitemap.xml')
ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
bad = [u.find('ns:loc', ns).text for u in t1.getroot().findall('ns:url', ns) if 'dbert.online' in u.find('ns:loc', ns).text]
print(f'apps/website/sitemap.xml bad locs: {len(bad)}/70')
"
```

### Verify Legacy Links in `cpanel_public_html/`:
```powershell
python -c "
import os
hits = sum(open(os.path.join(r, f), encoding='utf-8', errors='ignore').read().count('internship.dbert.online')
    for r, _, fs in os.walk('cpanel_public_html') for f in fs if f.endswith('.html'))
print(f'Total internship.dbert.online occurrences in HTML: {hits}')
"
# Returns: 1226 occurrences across 74 HTML files
```

### Invalidation Conditions:
- Re-running `npm run export:cpanel` invalidates findings **R3-05**, **R3-06**, and **R3-08** by regenerating static HTML from the updated source components.
- Adding `error_page 404 /404.html;` to `deploy/dbert-unified-nginx.conf` invalidates finding **R3-01**.
- Updating line 13 of `apps/website/robots.txt` and overwriting `apps/website/sitemap.xml` invalidates findings **R3-03** and **R3-04**.
