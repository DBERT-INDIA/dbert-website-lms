import json
import os
from collections import defaultdict

AUDIT_DATA_PATH = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\audit_data.json"
HANDOFF_PATH = r"c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_1\handoff.md"

with open(AUDIT_DATA_PATH, "r", encoding="utf-8") as f:
    findings = json.load(f)

blockers = [f for f in findings if f["classification"] == "Blocker"]
intentional = [f for f in findings if f["classification"] == "Intentional redirect rule"]
warnings = [f for f in findings if f["classification"] == "Warning"]

# Group blockers by file
blockers_by_file = defaultdict(list)
for b in blockers:
    blockers_by_file[b["file"]].append(b)

# Group warnings by file
warnings_by_file = defaultdict(list)
for w in warnings:
    warnings_by_file[w["file"]].append(w)

# Group intentional by file
intentional_by_file = defaultdict(list)
for i in intentional:
    intentional_by_file[i["file"]].append(i)

content = []

content.append("# Handoff Report: Requirement R1 — Legacy Domain Audit & Remediation\n")
content.append("**Agent**: `explorer_m1_1`  ")
content.append("**Archetype / Role**: Teamwork Explorer & Investigator  ")
content.append("**Date**: 2026-11-03  ")
content.append("**Recipient Orchestrator**: `d66c654e-a32e-4bd2-a554-e6ecbf8cc20c`  ")
content.append("**Scope**: Comprehensive repository-wide audit for legacy domains `dbert.online` and `internship.dbert.online` across all source directories, config files, static assets, database records, and distribution archives.\n")
content.append("---\n")

content.append("## Executive Summary\n")
content.append("An exhaustive static code analysis, database record scan, and distribution archive audit was conducted across the entire repository (`c:\\Users\\user\\Desktop\\dbert-website-lms`). A total of **267 active workspace occurrences** across 78 non-scratch files were identified, analyzed, and classified into three distinct categories:\n")
content.append("1. **Blockers (175 occurrences across 57 files)**: Functional URL, outbound navigation, metadata fallback, email address, CORS, and `.htaccess` defects that silently direct traffic to the legacy domain. Crucially, **all 175 blockers reside in `dbert-api-package/website-content/`** (an un-updated snapshot of `apps/website/src`). In addition, live SQLite databases (`internship.db` and `apps/portal/internship.db`) harbor **9,097 legacy domain records** that will poison PostgreSQL during EC2 migration.")
content.append("2. **Intentional Redirect Rules (11 occurrences across 5 files)**: Valid 301 HTTP/HTTPS permanent redirection rules in Nginx (`deploy/dbert-unified-nginx.conf`), Apache (`.htaccess`), Certbot SSL SAN configuration, and DNS setup guidance designed to funnel legacy traffic to `dbert.in` and `lms.dbert.in`.")
content.append("3. **Warnings (81 occurrences across 16 files)**: Outdated documentation files (markdown plans, release reports), inline code comments, CSS selector notes, and form placeholder strings.\n")

content.append("| Finding Classification | Occurrences | Files Affected | Primary Locations | Operational Impact |")
content.append("|---|:---:|:---:|---|---|")
content.append(f"| **Blockers** | **{len(blockers)}** | 57 files + 2 SQLite DBs | `dbert-api-package/website-content/`, `internship.db` | Silent 404s, broken links, SEO dilution, bad emails, DB pollution |")
content.append(f"| **Intentional Redirect Rules** | **{len(intentional)}** | 5 files | `deploy/dbert-unified-nginx.conf`, `.htaccess`, deploy scripts | None (Essential for domain migration routing) |")
content.append(f"| **Warnings** | **{len(warnings)}** | 16 files | `*.md` documentation, `docs/env_vars.md`, comments | Developer confusion, misleading documentation |")
content.append(f"| **TOTAL** | **{len(findings)}** | **78 files** | Entire Repository | Live Deployment Blocked until R1 remediated |")
content.append("\n---\n")

# Section 1: Observation
content.append("## 1. Observation\n")
content.append("### 1.1 Verification of Pre-Confirmed Baseline Findings (PRE-01 to PRE-08)\n")
content.append("All 8 baseline findings from `ORIGINAL_REQUEST.md` were directly inspected on disk. The investigation revealed that all 8 items have been remediated in the current local working copy:\n")
content.append("| # | ID | Cited File & Line | Baseline Issue | Current Workspace State (Observed) | Verdict |")
content.append("|---|---|---|---|---|:---:|")
content.append("| 1 | **PRE-01** | `apps/portal/.env:27` | `SMTP_HOST=dbert.online` | `SMTP_HOST=dbert.in` (Line 27) | **Remediated** |")
content.append("| 2 | **PRE-02** | `apps/portal/.env:29` | `SMTP_USER=contactus@dbert.online` | `SMTP_USER=contactus@dbert.in` (Line 29) | **Remediated** |")
content.append("| 3 | **PRE-03** | `apps/portal/.env:31` | `FROM_EMAIL=contactus@dbert.online` | `FROM_EMAIL=contactus@dbert.in` (Line 31) | **Remediated** |")
content.append('| 4 | **PRE-04** | `apps/portal/app.py:309` | Fallback default `"dbert.online"` | `SMTP_HOST = os.environ.get("SMTP_HOST", "dbert.in")` | **Remediated** |')
content.append('| 5 | **PRE-05** | `apps/portal/app.py:2698` | Hardcoded staff email `@dbert.online` | `staff_email = f"{ADMIN_USERNAME}@dbert.in"` | **Remediated** |')
content.append('| 6 | **PRE-06** | `deploy/deploy_ec2_unified.sh:57-61` | Plaintext DB password `DBERT_SECURE_PASSWORD_123` | Dynamic evaluation via `openssl rand -hex 24` or env ingestion | **Remediated** |')
content.append('| 7 | **PRE-07** | `cpanel_public_html/__next.__PAGE__.txt:49` | JSON-LD Organization schema legacy URLs | Line 49: `"url":"https://dbert.in"`, `"logo":"https://dbert.in/logo.svg"`, `"email":"contactus@dbert.in"` | **Remediated** |')
content.append('| 8 | **PRE-08** | `apps/portal/templates/seo_landing.html:133` | Anchor text reads `dbert.online` | Line 133: `<a href="https://dbert.in" class="underline text-gray-400">dbert.in</a>` | **Remediated** |\\n')

content.append("### 1.2 Verification of Application Sources (`apps/website` and `apps/portal`)\n")
content.append("- **`apps/website/src/`**: A complete filesystem search across all 250 files in `apps/website/src/` returned **ZERO occurrences** of `dbert.online` or `internship.dbert.online`. All metadata fallbacks (`layout.tsx`, `robots.ts`, `sitemap.ts`, `seo.ts`), JSON-LD schemas, and navigation components have already been unified to `https://dbert.in` and `https://lms.dbert.in`.")
content.append("- **`apps/website/` compiled JS chunks (`_next/static/chunks/*.js`)**: Zero occurrences.")
content.append("- **`cpanel_public_html/` compiled JS chunks (`_next/static/chunks/*.js`)**: Zero occurrences.")
content.append("- **`cpanel_public_html/sitemap.xml` & `robots.txt`**: All 70 `<loc>` entries point to `https://dbert.in`.")
content.append("- **`apps/portal/` Python Source**: All routes (`routes/`), services (`services/`), and templates (`templates/`) are free of active `dbert.online` occurrences in source code. Fallback emails in `services/auth_service.py` (lines 189, 195) specify `admin@dbert.in`.")
content.append("- **`apps/portal/sitemap.xml`**: Single-line 628 KB XML file contains all canonical `<loc>` tags pointing exclusively to `https://lms.dbert.in/`.\n")

content.append("### 1.3 Intentional Redirect Rules (11 Occurrences across 5 Files)\n")
content.append("The following 11 occurrences are intentional, functional permanent redirection rules and operational configuration designed to route legacy traffic to the production domains:\n")
content.append("| File Path | Line | Snippet | Target Redirect | Purpose / Classification |")
content.append("|---|:---:|---|---|---|")
for item in intentional:
    f = item["file"]
    l = item["line"]
    s = item["snippet"].replace("|", "\\|")
    t = item["replacement"]
    content.append(f"| `{f}` | {l} | `{s}` | `{t}` | Intentional redirect rule |")
content.append("\n")

content.append("### 1.4 Blocker Defects: Legacy Domains in `dbert-api-package/website-content/` (175 Occurrences across 57 Files)\n")
content.append("While `apps/website/src` was updated during prior refactoring, the companion standalone package `dbert-api-package/website-content/` was neglected. It contains **175 Blocker references** across 57 files. When this package is deployed or built, it renders invalid outbound links, incorrect JSON-LD structured data, and defunct email links:\n")
content.append("| File Path | Line | Current Snippet | Required Replacement | Severity |")
content.append("|---|:---:|---|---|:---:|")
for item in blockers:
    f = item["file"]
    l = item["line"]
    s = item["snippet"].replace("|", "\\|")
    t = item["replacement"]
    content.append(f"| `{f}` | {l} | `{s}` | `{t}` | **Blocker** |")
content.append("\n")

content.append("### 1.5 Database Contamination Audit (SQLite `internship.db`)\n")
content.append("A deep SQL scan was executed against both SQLite databases (`internship.db` at repo root and `apps/portal/internship.db`). Because `scripts/migrate_all_ec2_data.py` transfers SQLite data into production PostgreSQL (`dbert_internship` schema), any uncleaned legacy URLs will be migrated directly into production:\n")
content.append("| Database File | Table Name | Column Name | Legacy Occurrences | Sample Verbatim Snippet | Required Remediation |")
content.append("|---|---|---|:---:|---|---|")
content.append("| `internship.db` (root) | `staff_accounts` | `email` | 1 | `dbert_admin@dbert.online` | Replace `@dbert.online` with `@dbert.in` |")
content.append("| `apps/portal/internship.db` | `staff_accounts` | `email` | 4 | `admin@dbert.online`, `dbert_admin@dbert.online` | Replace `@dbert.online` with `@dbert.in` |")
content.append("| `apps/portal/internship.db` | `companies` | `website` | 1 | `https://internship.dbert.online` | Replace with `https://lms.dbert.in` |")
content.append("| `apps/portal/internship.db` | `post_applications` | `comment` | 1 | `https://internship.dbert.online/internships/web-app-maintenance-intern-remote-45` | Replace with `https://lms.dbert.in/...` |")
content.append("| `apps/portal/internship.db` | `notifications` | `link` | 5,976 | `https://internship.dbert.online` | Replace prefix with `https://lms.dbert.in` |")
content.append("| `apps/portal/internship.db` | `device_profiles` | `referrer` | 3,114 | `https://internship.dbert.online/internship/profile` | Replace prefix with `https://lms.dbert.in` |")
content.append("| **TOTAL DB RECORDS** | — | — | **9,097 rows** | — | Execute SQL sanitization script |")
content.append("\n")

content.append("### 1.6 Packaged Distribution Archives\n")
content.append("- `dbert-api-package-v1.zip`: Contains **67 internal files** referencing `dbert.online` and `internship.dbert.online` (including `.env.example`, `.env.production.sample`, `router.py`, `config.py`, and `website-content/`). Once `dbert-api-package` is remediated, this zip archive must be regenerated.\n")

content.append("### 1.7 Warning Findings: Documentation, Comments, and Placeholders (81 Occurrences across 16 Files)\n")
content.append("The following 81 findings are non-functional references in documentation, markdown files, and code comments:\n")
content.append("| File Path | Line | Snippet | Replacement | Classification |")
content.append("|---|:---:|---|---|:---:|")
for item in warnings:
    f = item["file"]
    l = item["line"]
    s = item["snippet"].replace("|", "\\|")
    t = item["replacement"]
    content.append(f"| `{f}` | {l} | `{s}` | `{t}` | Warning |")
content.append("\n---\n")

# Section 2: Logic Chain
content.append("## 2. Logic Chain\n")
content.append("### Step 1: Baseline Remediation Verification\n")
content.append("- *Observation*: Files `apps/portal/.env`, `apps/portal/app.py`, `deploy/deploy_ec2_unified.sh`, `cpanel_public_html/__next.__PAGE__.txt`, and `apps/portal/templates/seo_landing.html` all display remediated `dbert.in` values on disk (Lines 27, 29, 31 in `.env`, Lines 309, 2698 in `app.py`, Line 49 in `__PAGE__.txt`).")
content.append("- *Inference*: The 8 baseline issues flagged in preliminary scans were addressed in the active working tree but were never committed or reconciled across secondary packages.\n")

content.append("### Step 2: Root-Cause Analysis of `dbert-api-package/website-content/`\n")
content.append("- *Observation*: A full file comparison between `apps/website/src` (250 files) and `dbert-api-package/website-content/src` (225 files) reveals that 166 files are 100% byte-for-byte identical, while 59 files differ. Comparing the diffs (e.g. `Footer.tsx`, `layout.tsx`, course pages) demonstrates that the diff consists entirely of the domain migration replacements (`https://internship.dbert.online` $\\rightarrow$ `https://lms.dbert.in`, `dbert.online` $\\rightarrow$ `dbert.in`).")
content.append("- *Inference*: `dbert-api-package/website-content` was duplicated from an older version of `apps/website` before domain migration occurred. It was never synchronized when `apps/website/src` was updated. Consequently, 175 blocker references exist in this sub-tree.\n")

content.append("### Step 3: Architectural Legitimacy of Intentional Redirect Rules\n")
content.append("- *Observation*: `deploy/dbert-unified-nginx.conf` contains dedicated server blocks for `dbert.online` (lines 28-40, 58-67) and `internship.dbert.online` (lines 42-54, 70-79) issuing `return 301 https://dbert.in$request_uri` and `return 301 https://lms.dbert.in$request_uri`. In addition, line 229 of `deploy/deploy_ec2_unified.sh` includes `dbert.online` and `internship.dbert.online` in the Certbot command.")
content.append("- *Inference*: These rules must NOT be removed. Without them, existing inbound traffic, search engine bookmarks, and legacy external links would fail to connect or trigger SSL certificate mismatch warnings. These are intentional, production-grade 301 redirect blocks.\n")

content.append("### Step 4: The Database Contamination Threat Vector\n")
content.append("- *Observation*: The SQLite databases `apps/portal/internship.db` and root `internship.db` store 9,097 rows containing legacy domain strings across `staff_accounts`, `notifications`, `device_profiles`, `companies`, and `post_applications`.")
content.append("- *Inference*: `scripts/migrate_all_ec2_data.py` reads SQLite tables and inserts records directly into PostgreSQL (`dbert_internship` schema). If the database is migrated without string replacement, every historical and seeded notification link will send users to `https://internship.dbert.online`, and staff email logins will retain `@dbert.online`, causing authentication and notification failures.\n")

content.append("---\n")

# Section 3: Caveats
content.append("## 3. Caveats\n")
content.append("1. **Pre-existing Local Working Tree Modifications**: Several files in the working directory (such as `apps/portal/app.py`, `apps/portal/.env`, `apps/website/.htaccess`, `dbert-api-package/.env.example`) have uncommitted modifications from prior development work. These changes were validated as correct and aligned with `dbert.in`.")
content.append("2. **Historical Phase Documentation**: The 8 markdown documentation files at the repository root (`DBERT_LMS_MASTER_DEVELOPMENT_HARDENING_PLAN.md`, etc.) describe past architectural phases where `dbert.online` was the active production target. While classified as Warnings, updating them is optional and should not take precedence over functional code changes.")
content.append("3. **External Certbot Issuance**: The Nginx 301 HTTPS redirect rules require valid SSL certificates for `dbert.online` and `internship.dbert.online`. If DNS A-records for the legacy domains are not pointed to the EC2 IP (`3.26.237.171`), Certbot will fail to issue certificates for those SAN domains. In that scenario, Nginx will fail to start if the certificate path does not exist.\n")

content.append("---\n")

# Section 4: Conclusion & Actionable Remediation Plan
content.append("## 4. Conclusion & Actionable Remediation Plan\n")
content.append("To achieve 100% domain migration completeness under Requirement R1, the implementation team must execute four scoped remediation actions:\n")

content.append("### Remediation Action 1: Synchronize `dbert-api-package/website-content` with `apps/website`\n")
content.append("Because `dbert-api-package/website-content/src/` is an exact subset of `apps/website/src/`, all 175 Blocker defects in `dbert-api-package/website-content/` can be remediated cleanly and without regression by copying the updated files from `apps/website/src/`:\n")
content.append("```bash\n# In repository root:\ncp -r apps/website/src/* dbert-api-package/website-content/src/\ncp apps/website/.htaccess dbert-api-package/website-content/public/.htaccess\ncp apps/website/ads.txt dbert-api-package/website-content/public/ads.txt\n```\n")

content.append("### Remediation Action 2: Update API Documentation (`dbert-api-package/docs/`)\n")
content.append("- In `dbert-api-package/docs/env_vars.md`:\n")
content.append("  - Line 30: Change `contactus@dbert.online` to `contactus@dbert.in`\n")
content.append("  - Line 65: Change `https://internship.dbert.online` to `https://lms.dbert.in`\n")
content.append("  - Line 70: Change `dbert.online` to `dbert.in`\n")
content.append("  - Line 73: Change `contactus@dbert.online` to `contactus@dbert.in`\n")
content.append("- In `dbert-api-package/docs/integrations.md`:\n")
content.append("  - Line 47: Change `dbert.online` to `dbert.in`\n")

content.append("### Remediation Action 3: Database Legacy Domain Sanitization\n")
content.append("Execute the following SQL update statements across both `apps/portal/internship.db` and root `internship.db` (or incorporate into `scripts/migrate_all_ec2_data.py` before inserting rows into PostgreSQL):\n")
content.append("```sql\n-- 1. Update staff account emails\nUPDATE staff_accounts\nSET email = REPLACE(email, '@dbert.online', '@dbert.in')\nWHERE email LIKE '%@dbert.online';\n\n-- 2. Update company website URLs\nUPDATE companies\nSET website = REPLACE(website, 'internship.dbert.online', 'lms.dbert.in')\nWHERE website LIKE '%internship.dbert.online%';\n\n-- 3. Update application comments\nUPDATE post_applications\nSET comment = REPLACE(comment, 'internship.dbert.online', 'lms.dbert.in')\nWHERE comment LIKE '%internship.dbert.online%';\n\n-- 4. Update notifications links\nUPDATE notifications\nSET link = REPLACE(link, 'https://internship.dbert.online', 'https://lms.dbert.in')\nWHERE link LIKE '%https://internship.dbert.online%';\n\n-- 5. Update device profiles referrer\nUPDATE device_profiles\nSET referrer = REPLACE(referrer, 'https://internship.dbert.online', 'https://lms.dbert.in')\nWHERE referrer LIKE '%https://internship.dbert.online%';\n```\n")

content.append("### Remediation Action 4: Regenerate `dbert-api-package-v1.zip`\n")
content.append("Once `dbert-api-package/website-content/` and `dbert-api-package/docs/` are remediated, re-package the standalone archive:\n")
content.append("```bash\nzip -r dbert-api-package-v1.zip dbert-api-package/ -x \"*/__pycache__/*\" \"*/.git/*\"\n```\n")

content.append("### Remediation Action 5: EC2 Nginx Configuration Verification\n")
content.append("Preserve the 301 redirect blocks in `deploy/dbert-unified-nginx.conf` (lines 28-79). Ensure that DNS A-records for `dbert.online`, `www.dbert.online`, and `internship.dbert.online` point to EC2 IP `3.26.237.171` before Certbot issues SSL certificates.\n")

content.append("---\n")

# Section 5: Verification Method
content.append("## 5. Verification Method\n")
content.append("### Independent Verification Commands\n")
content.append("1. **Repository-Wide Grep for Unintended Occurrences**:\n")
content.append("   Run the following command to verify zero unintended references remain in source files:\n")
content.append("   ```powershell\n   git grep -n -I \"dbert.online\" -- ':!deploy/dbert-unified-nginx.conf' ':!apps/website/.htaccess' ':!apps/website/public/.htaccess' ':!cpanel_public_html/.htaccess' ':!deploy/deploy_ec2_unified.sh' ':!deploy/FILEZILLA_DEPLOYMENT_GUIDE.md' ':!*.md' ':!scratch/'\n   ```\n")
content.append("   *Expected output*: Zero matches.\n\n")

content.append("2. **Verification of `dbert-api-package/website-content`**:\n")
content.append("   ```powershell\n   git grep -n -I \"dbert.online\" dbert-api-package/website-content/\n   ```\n")
content.append("   *Expected output*: Zero matches.\n\n")

content.append("3. **Database Verification Query**:\n")
content.append("   ```powershell\n   python -c \"\n   import sqlite3\n   conn = sqlite3.connect('apps/portal/internship.db')\n   for table in ['staff_accounts', 'companies', 'post_applications', 'notifications', 'device_profiles']:\n       cnt = conn.execute(f\\\"SELECT count(*) FROM {table} WHERE email LIKE '%dbert.online%' OR website LIKE '%dbert.online%' OR comment LIKE '%dbert.online%' OR link LIKE '%dbert.online%' OR referrer LIKE '%dbert.online%'\\\").fetchone()[0] if table != 'device_profiles' else conn.execute(f\\\"SELECT count(*) FROM {table} WHERE referrer LIKE '%dbert.online%'\\\").fetchone()[0]\n       print(f'{table}: {cnt} legacy records')\n   \"\n   ```\n")
content.append("   *Expected output*: All counts equal 0.\n\n")

content.append("4. **Invalidation Conditions**:\n")
content.append("   - If any active route, metadata tag, JSON-LD schema, or email in `apps/website/`, `apps/portal/`, or `dbert-api-package/` resolves to `dbert.online`.\n")
content.append("   - If Nginx removes the legacy 301 redirect server blocks, causing old bookmarks to drop.\n")

with open(HANDOFF_PATH, "w", encoding="utf-8") as out:
    out.write("\n".join(content))

print(f"Handoff report written to {HANDOFF_PATH}")
