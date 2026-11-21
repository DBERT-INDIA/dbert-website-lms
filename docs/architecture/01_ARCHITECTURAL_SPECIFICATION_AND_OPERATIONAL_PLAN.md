# DBERT Architectural Specification & Multi-Agent Operational Plan
================================================================================
Comprehensive Platform Architecture, Target SEO Engine, Financial Ledgers,
5-Gate Stipend Protocol, and Multi-Agent Execution Plan
================================================================================

- **Document Identifier**: `DBERT-SPEC-ARCH-2026-R1`
- **As-of Date**: 21 November 2026
- **Version**: 3.0 (Enterprise Production Baseline)
- **Authoring Role**: Architectural & Operational Planning Specialist (`worker_r1_arch`)
- **Target Monorepo**: `c:\Users\user\Desktop\dbert-website-lms`
- **Production Host**: AWS EC2 `ubuntu@3.26.237.171` (`/var/www/dbert-website-lms`)
- **Active Sovereign Domains**: `https://dbert.in` (Website/SSG), `https://lms.dbert.in` (Portal/LMS), `https://api.dbert.in` (FastAPI)
- **Legacy Retired Domain**: `dbert.online` (Strict HTTP 301 Permanent Redirect to `dbert.in`)
- **Unified GA4 Measurement ID**: `G-MN7ME9X518`

---

## Table of Contents
1. [Executive Summary & Architectural Context](#1-executive-summary--architectural-context)
2. [Executive Architecture Audit of the DBERT Platform](#2-executive-architecture-audit-of-the-dbert-platform)
   - [2.1 Monorepo Subsystems & Service Topology](#21-monorepo-subsystems--service-topology)
   - [2.2 Sovereign Domain Mandate & Domain Migration Rules](#22-sovereign-domain-mandate--domain-migration-rules)
   - [2.3 Unified Telemetry & Analytics Protocol (GA4)](#23-unified-telemetry--analytics-protocol-ga4)
   - [2.4 Production EC2 Infrastructure & Service Management](#24-production-ec2-infrastructure--service-management)
   - [2.5 Next.js 16 Standalone Build & Deployment Procedures](#25-nextjs-16-standalone-build--deployment-procedures)
   - [2.6 Relational & Flat-File Data Architecture](#26-relational--flat-file-data-architecture)
3. [Target SEO & User Journey Architecture](#3-target-seo--user-journey-architecture)
   - [3.1 Persona Taxonomy & Universal Entry Points](#31-persona-taxonomy--universal-entry-points)
   - [3.2 5-Stage Candidate Lifecycle State Machine](#32-5-stage-candidate-lifecycle-state-machine)
   - [3.3 Programmatic SEO Architecture across Touchpoints](#33-programmatic-seo-architecture-across-touchpoints)
   - [3.4 Infallible 3-Tier Job Query Fallback Engine](#34-infallible-3-tier-job-query-fallback-engine)
   - [3.5 Generative Engine Optimization (GEO) & AI Assistant Citation Architecture](#35-generative-engine-optimization-geo--ai-assistant-citation-architecture)
   - [3.6 Frictionless Lead Capture & Ingestion Pipelines](#36-frictionless-lead-capture--ingestion-pipelines)
4. [Comprehensive Financial Ledger & Credential Gates](#4-comprehensive-financial-ledger--credential-gates)
   - [4.1 Strict Dual-Ledger Separation Principle](#41-strict-dual-ledger-separation-principle)
   - [4.2 Program Monetization & Fee Structures](#42-program-monetization--fee-structures)
   - [4.3 5-Gate Stipend Disbursement Protocol (₹5,000 Milestone Payout)](#43-5-gate-stipend-disbursement-protocol-5000-milestone-payout)
   - [4.4 The 4 Official Partner Repositories & Upstream PR Requirements](#44-the-4-official-partner-repositories--upstream-pr-requirements)
5. [Multi-Agent Operational Execution Plan](#5-multi-agent-operational-execution-plan)
   - [5.1 Multi-Agent Topology & Hierarchy](#51-multi-agent-topology--hierarchy)
   - [5.2 RACI Matrix Across Execution Milestones](#52-raci-matrix-across-execution-milestones)
   - [5.3 File Workspace Protocol & Isolation Discipline](#53-file-workspace-protocol--isolation-discipline)
   - [5.4 Verification Gates & Multi-Stage Quality Assurance](#54-verification-gates--multi-stage-quality-assurance)
   - [5.5 Production Deployment & Rollout Runbook](#55-production-deployment--rollout-runbook)
6. [Appendices & Authoritative Reference Catalog](#6-appendices--authoritative-reference-catalog)
   - [Appendix A: Canonical 9 Technical Domains](#appendix-a-canonical-9-technical-domains)
   - [Appendix B: Canonical 18 Geo Cities & Technical Corridors](#appendix-b-canonical-18-geo-cities--technical-corridors)
   - [Appendix C: Authoritative 9-Dimension Rubric (100 Marks Total)](#appendix-c-authoritative-9-dimension-rubric-100-marks-total)
   - [Appendix D: Seeded QA Test Personas](#appendix-d-seeded-qa-test-personas)

---

## 1. Executive Summary & Architectural Context

The DBERT platform represents an end-to-end technical incubation venture studio, higher-education engineering ecosystem, and pre-vetted talent marketplace. The ecosystem bridges the gap between academic theory and high-rigor production engineering by offering:
1. **2-Month Incubation Fellowships**: 8-week intensive agile sprint programs (10 hrs/week logged attendance capped at 80h) with real upstream pull requests (PRs) merged into 4 flagship partner repositories, a 9-dimension performance evaluation rubric (100 marks), Turnitin plagiarism screening (<5%), official 3-document credential packages (Certificate, Evaluation Rubric, Letter of Recommendation), and an eligible ₹5,000 completion stipend.
2. **3-Month Paid Learner Courses**: 12-week structured diploma programs spanning 9 technical domains with comprehensive foundation-to-advanced syllabi, daily interactive lab quizzes, 2 full-scale production capstone deployments, and career placement services.
3. **Dynamic City-Targeted Landing Pages**: Programmatic SEO architecture connecting engineering candidates across 18 major Indian technology hubs to localized internships and tech roles.
4. **Generative Engine Optimization (GEO)**: Multi-entity JSON-LD graphs (`Course`, `EducationalOccupationalProgram`, `JobPosting`, `FAQPage`, `BreadcrumbList`) and `/llms.txt` knowledge corpus specifically optimized for discovery and citation by conversational AI engines (ChatGPT, Perplexity, Gemini, Claude).

This specification establishes the architectural requirements, domain constraints, financial ledgers, and multi-agent execution governance required for zero-defect implementation across the monorepo.

---

## 2. Executive Architecture Audit of the DBERT Platform

```
+--------------------------------------------------------------------------------------------------+
|                                    Client & Crawler Ingress                                      |
|    +-----------------------------+ +-----------------------------+ +------------------------+    |
|    | Web Browsers / Mobile Users | | Search Engines / AI Crawlers| | Corporate Recruiters   |    |
|    +-----------------------------+ +-----------------------------+ +------------------------+    |
+-------------------------------------------------+------------------------------------------------+
                                                  | HTTPS (TLS 1.3 / Let's Encrypt)
                                                  v
+--------------------------------------------------------------------------------------------------+
|                     AWS EC2 Host: ubuntu@3.26.237.171 (Ubuntu 22.04 LTS)                         |
|                                                                                                  |
|   +------------------------------------------------------------------------------------------+   |
|   |                      Nginx Reverse Proxy & SSL Termination (Port 80/443)                 |   |
|   |   - dbert.in / www.dbert.in           --> Proxy Pass 127.0.0.1:3000                      |   |
|   |   - lms.dbert.in                      --> Proxy Pass 127.0.0.1:5001                      |   |
|   |   - api.dbert.in                      --> Proxy Pass 127.0.0.1:8000                      |   |
|   |   - dbert.online (HTTP 301 Permanent) --> Redirect 301 https://dbert.in$request_uri      |   |
|   +---------------------------------------------+--------------------------------------------+   |
|                                                 |                                                |
|          +--------------------------------------+--------------------------------------+         |
|          | (Port 3000)                          | (Port 5001)                          | (8000)  |
|          v                                      v                                      v         |
|   +------------------------+             +------------------------+             +------------+   |
|   |   apps/website         |             |   apps/portal          |             | apps/api   |   |
|   |   Next.js 16.2.10      |             |   Flask + Gunicorn     |             | FastAPI    |   |
|   |   Turbopack Standalone |             |   Python 3.10+         |             | Microserv  |   |
|   |   React 19.2.7         |             |   LMS, Tasks, Offers   |             | Port 8000  |   |
|   |   Prisma 7.8.0         |             |   Stipend Dossiers     |             +------------+   |
|   +-----------+------------+             +-----------+------------+                              |
|               |                                      |                                           |
|               | Read/Write                           | Read/Write                                |
|               v                                      v                                           |
|   +------------------------------------------------------------------------------------------+   |
|   |                                Decoupled Data & State Tier                               |   |
|   |   - PostgreSQL 14 (dbert_lms / dbert_internship schema): Users, Offers, Tasks, Ledger    |   |
|   |   - Flat JSON Registries (/data & apps/website/src/data): Master Registries (465)        |   |
|   |   - SQLite WAL Queues (data/dbert_whatsapp.db): WhatsApp Dispatch & Deduplication Logs  |   |
|   +------------------------------------------------------------------------------------------+   |
+--------------------------------------------------------------------------------------------------+
```

### 2.1 Monorepo Subsystems & Service Topology

The DBERT platform is organized into three primary operational subtrees and a shared data layer:

1. **`apps/website` (`https://dbert.in`)**:
   - **Framework**: Next.js `16.2.10`, React `19.2.7`, TypeScript `6.0.3`, Tailwind CSS `3.4.1`, Prisma ORM `7.8.0`.
   - **Build Target**: Turbopack Standalone (`output: 'standalone'`).
   - **Runtime**: Node.js 18+ running on `127.0.0.1:3000` via systemd unit `dbert-website.service`.
   - **Core Responsibilities**: Sovereign public portal, programmatic SEO directories (`/internships/[role]/[city]`), learner course catalog (`/learners/courses/*`), candidate verification engine (`/verify`, `/verify/[certId]`), 465-candidate recruiter talent directory (`/verify/directory`), balance completion portal (`/enroll/1999`, `/enroll`, `/eroll`), and JSON API routes (`/api/enroll/lookup`, `/api/enroll/balance`, `/api/verify`).

2. **`apps/portal` (`https://lms.dbert.in`)**:
   - **Framework**: Python 3.10+, Flask, SQLAlchemy, Gunicorn WSGI.
   - **Runtime**: Gunicorn running on `127.0.0.1:5001` via systemd unit `dbert-portal.service`.
   - **Session Security**: Cookie name `dbert_flask` (segregated from auth token `dbert_auth`), Fernet-encrypted session storage.
   - **Core Responsibilities**: Student onboarding, 5-stage lifecycle state management, appointment offer generation (`/portal/offer`), BYOK Gemini AI tutor (`/account/gemini-key`), sprint task and bounty submissions (`/tasks`), ambassador referral ledger (`/intern/ambassador`), 5-gate stipend release interface (`/stipend/tasks`), and administrative governance (`/admin`, `/staff/tasks`).

3. **`apps/api` (`https://api.dbert.in`)**:
   - **Framework**: Python FastAPI, Uvicorn ASGI.
   - **Runtime**: Uvicorn running on `127.0.0.1:8000` via systemd unit `dbert-api.service`.
   - **Core Responsibilities**: High-throughput candidate verification queries, programmatic webhook ingestion, and real-time telemetry streaming.

4. **Shared Data Tier (`data/`)**:
   - **Master Candidate Registries**: `data/all_409_provisional_registry.json`, `apps/website/src/data/directory_candidates.json` (465 candidate records), `apps/website/src/data/certificates_registry.json`.
   - **Financial & Verification Ledgers**: `data/balance_enrollments_1500.json` (live ₹1,500 candidate submissions), `data/verification_submissions_299.json` (live ₹299 verification submissions).
   - **Omnichannel Dispatch State**: `data/dbert_whatsapp.db` (SQLite in WAL mode), `data/dispatch_tracking_409.json`.

---

### 2.2 Sovereign Domain Mandate & Domain Migration Rules

The platform maintains absolute domain authority under strict SEO governance:

1. **Active Sovereign Domain**:
   - The primary origin is strictly **`https://dbert.in`** (with subdomains `lms.dbert.in` and `api.dbert.in`).
   - Every canonical tag, OpenGraph tag, API route, email link, certificate PDF, and WhatsApp template MUST strictly emit `https://dbert.in`.

2. **Legacy Retired Domain (`dbert.online`)**:
   - `dbert.online` is permanently retired and strictly redirected to `dbert.in` via HTTP 301 permanent redirect.
   - **Strict Prohibition**: Under no circumstances should `dbert.online` be used in active source code, metadata `baseUrl`, or external communication.

3. **Dual SEO Migration Headlines**:
   To preserve search equity, reassure returning users, and prevent phishing, high-traffic entry points maintain two explicit SEO phrases:
   - **Headline 1 (Migration Notice)**: *"DBERT.online is Now DBERT.in"*
   - **Headline 2 (Security Advisory)**: *"dbert.online is not the active platform"*
   - **Target Locations**: Global Header/Footer, About Credentials (`/about/credentials`), Learner Hub (`/learners`), Verification Engine (`/verify`), and Migration Page (`/dbert-online`).

4. **Dedicated Migration Page (`/dbert-online`)**:
   - Canonical URL: `https://dbert.in/dbert-online`.
   - Title: `DBERT.online is Now DBERT.in — Domain Migration | DBERT` (58 chars).
   - Meta Description: `Official notice: DBERT.online is now DBERT.in. Discover our verified venture incubation, LMS portal, AI careers, and certificate verification on dbert.in.` (154 chars).
   - Rich Data: `BreadcrumbList` and `FAQPage` JSON-LD schemas.

5. **Nginx & Apache 301 Redirect Rules**:
   - **Nginx (`/etc/nginx/sites-available/dbert-unified-nginx.conf`)**:
     ```nginx
     server {
         listen 80;
         listen 443 ssl http2;
         server_name dbert.online www.dbert.online;
         ssl_certificate /etc/letsencrypt/live/dbert.online/fullchain.pem;
         ssl_certificate_key /etc/letsencrypt/live/dbert.online/privkey.pem;
         return 301 https://dbert.in$request_uri;
     }
     ```
   - **Apache (`.htaccess`)**:
     ```apache
     RewriteCond %{HTTP_HOST} ^(www\.)?dbert\.online$ [NC]
     RewriteRule ^(.*)$ "https://dbert.in/$1" [R=301,L]
     ```

---

### 2.3 Unified Telemetry & Analytics Protocol (GA4)

- **Measurement ID**: Strictly **`G-MN7ME9X518`** across all services. (Deprecated ID `G-GZ17KZ7MDW` is strictly decommissioned).
- **Client Script Injection (`apps/website/src/app/layout.tsx`)**:
  Loaded via Next.js `Script` with `strategy="lazyOnload"` to safeguard Core Web Vitals (LCP < 2.5s, FID < 100ms, CLS < 0.1).
- **Client Helper (`apps/website/src/lib/analytics.ts`)**:
  ```typescript
  export const trackEvent = (eventName: string, params?: Record<string, unknown>) => {
    if (typeof window !== 'undefined' && typeof window.gtag === 'function') {
      window.gtag('event', eventName, params);
    }
  };
  ```
- **Server-Side Measurement Protocol (`apps/portal/app.py`)**:
  Dispatches offline backend conversions (offer letter signing, deposit payment, task completions) directly to Google Analytics Measurement Protocol:
  `POST https://www.google-analytics.com/mp/collect?measurement_id=G-MN7ME9X518&api_secret={GA4_API_SECRET}`.

---

### 2.4 Production EC2 Infrastructure & Service Management

- **Server IP**: `3.26.237.171` (AWS EC2, Ubuntu 22.04 LTS).
- **SSH Authentication**: `ubuntu@3.26.237.171` using key `C:\Users\user\.ssh\dbert-production-server.pem`.
- **Base Project Directory**: `/var/www/dbert-website-lms`.
- **Systemd Service Topology**:
  - `dbert-website.service`: Next.js Standalone Node.js server (`NODE_ENV=production node server.js`) binding to `127.0.0.1:3000`.
  - `dbert-portal.service`: Gunicorn WSGI server (`gunicorn -w 4 -b 127.0.0.1:5001 app:app`) managing LMS state.
  - `dbert-api.service`: Uvicorn ASGI server (`uvicorn main:app --host 127.0.0.1 --port 8000`) for API endpoints.
  - `nginx.service`: Front-facing reverse proxy handling Let's Encrypt SSL certificates, HTTP/2 termination, and gzip/brotli compression.

---

### 2.5 Next.js 16 Standalone Build & Deployment Procedures

All code updates deployed to `apps/website` on the production server must strictly adhere to the standalone build pipeline:

```bash
# 1. SCP modified source files from local repository
scp -i "C:\Users\user\.ssh\dbert-production-server.pem" -o StrictHostKeyChecking=no -o BatchMode=yes <local_file> ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/website/<target_path>

# 2. SSH into production EC2 and execute build
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 'bash -s' << 'EOF'
set -e
cd /var/www/dbert-website-lms/apps/website
export NODE_ENV=production

# Execute standalone production build
npm run build

# Sync dynamic sitemap output to static public directories
if [ -f .next/server/app/sitemap.xml.body ]; then
  cp .next/server/app/sitemap.xml.body public/sitemap.xml
fi

# Copy public static assets into standalone bundles
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true
if [ -f .next/server/app/sitemap.xml.body ]; then
  cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
  cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
fi

# Ensure persistent data directory symlink exists within standalone build
mkdir -p /var/www/dbert-website-lms/data
rm -rf /var/www/dbert-website-lms/apps/website/.next/standalone/data
ln -s /var/www/dbert-website-lms/data /var/www/dbert-website-lms/apps/website/.next/standalone/data

# Restart service and verify liveness
sudo systemctl restart dbert-website.service
sleep 2
systemctl is-active dbert-website.service
EOF
```

---

### 2.6 Relational & Flat-File Data Architecture

```
+--------------------------------------------------------------------------------------------------+
|                                  PostgreSQL Relational Schema (dbert_lms)                        |
|                                                                                                  |
|   +-----------------------+     +-----------------------+     +-------------------------------+  |
|   |   intern_accounts     |     |   enrollments         |     |   intern_certificates         |  |
|   |   -----------------   |     |   -----------------   |     |   -------------------------   |  |
|   |   id (PK, UUID/Int)   |<--->|   id (PK)             |     |   id (PK)                     |  |
|   |   email (Unique)      |     |   intern_id (FK)      |     |   cert_id (Unique)            |  |
|   |   full_name           |     |   amount (499 / 1500) |     |   intern_id (FK)              |  |
|   |   status (Stages 1-5) |     |   utr_number (12 dig) |     |   tier ('provisional'/'ver')  |  |
|   |   track_domain        |     |   payment_status      |     |   stipend_verified (Boolean)  |  |
|   |   encrypted_upi_id    |     |   created_at          |     |   score (Numeric 0-100)       |  |
|   +-----------+-----------+     +-----------------------+     +---------------+---------------+  |
|               |                                                               |                  |
|               v                                                               v                  |
|   +-----------------------+     +-----------------------+     +-------------------------------+  |
|   |   coin_ledger_mirror  |     |   posts (Job/Intern)  |     |   user_api_keys (BYOK)        |  |
|   |   -----------------   |     |   -----------------   |     |   -------------------------   |  |
|   |   id (PK)             |     |   id (PK)             |     |   id (PK)                     |  |
|   |   intern_id (FK)      |     |   company_id (FK)     |     |   intern_id (FK)              |  |
|   |   ledger_kind         |     |   domain / title      |     |   encrypted_key (Fernet)      |  |
|   |   ('task'/'referral') |     |   location / mode     |     |   is_active (Boolean)         |  |
|   |   delta_coins         |     |   stipend_min/max     |     |   model_probe_cache           |  |
|   +-----------------------+     +-----------------------+     +-------------------------------+  |
+--------------------------------------------------------------------------------------------------+
```

1. **PostgreSQL Relational Schema (`dbert_lms`)**:
   - `intern_accounts`: Master table managing intern identities, hashed passwords, 5-stage application progress, track domain, and encrypted UPI identifiers.
   - `enrollments`: Tracks ₹499 caution deposits and ₹1,500 balance transactions with 12-digit UPI UTR validation.
   - `intern_certificates`: Issued credential records containing `cert_id`, `tier` (`provisional` vs `verified`), `stipend_verified` boolean, Turnitin percentage, and evaluation rubric scores.
   - `coin_ledger_mirror`: Enforces strict dual-ledger separation (`task` vs `referral`).
   - `posts`: Relational job and internship catalog with geographic location, stipend range, and application deadlines.
   - `user_api_keys`: Encrypted BYOK Gemini API keys with Fernet encryption using `FLASK_SECRET_KEY`.

2. **Master Flat JSON Registries (`data/` and `apps/website/src/data/`)**:
   - `certificates_registry.json`: Master certificate registry powering `/verify` and `/verify/[certId]`.
   - `directory_candidates.json`: 465 candidates (65 verified pre-vetted engineers + 400 provisional fellows) with 9-parameter rubric scores and technology pills.
   - `balance_enrollments_1500.json`: Live ledger for ₹1,500 balance completions.
   - `verification_submissions_299.json`: Inbound ₹299 verification submissions.

---

## 3. Target SEO & User Journey Architecture

### 3.1 Persona Taxonomy & Universal Entry Points

The DBERT platform serves 8 primary user personas across organic search, social campaigns, email dispatches, and recruiter referrals:

| Persona ID | Persona Role | Primary Landing Pages | Starting State | Target Goal | Primary Conversion Action |
|---|---|---|---|---|---|
| **P1** | Anonymous Job Seeker | `/internships/[role]/[city]`, `/jobs` | Anonymous / Unauthenticated | Discover localized tech roles | Clicks "Apply Now" $\rightarrow$ LMS Registration |
| **P2** | Fresh Course Applicant | `/learners/courses/[courseSlug]`, `/apply` | Unauthenticated Visitor | Enroll in 3-Month Course | Completes lead capture form / EMI application |
| **P3** | Under-Review Candidate | `/portal`, `/login` | Stage 2 (Under Review) | Track admission status | Receives fast-track preview modules |
| **P4** | Selected / Deposit Pending | `/portal/offer`, `/payment` | Stage 3 (Selected, Unpaid) | Review offer & confirm seat | Pays ₹499 caution deposit & submits UTR |
| **P5** | Provisional Fellow | `/enroll/1999`, `/verify/[certId]` | Provisional Credential (`isProvisional: true`) | Finalize incubation / unlock verified badge | Pays ₹1,500 balance or ₹299 verification fee |
| **P6** | Active Confirmed Intern | `/portal`, `/tasks`, `/account/gemini-key` | Stage 5 (Confirmed Fellow) | Complete sprint tasks & bounties | Submits PR on partner repo & logs attendance |
| **P7** | Verified Graduate Alumnus | `/stipend/tasks`, `/intern/ambassador` | Verified Alumnus (`isProvisional: false`) | Claim ₹5,000 milestone stipend | Completes 5-gate disbursement protocol |
| **P8** | Corporate Recruiter | `/verify/directory`, `/hire/pre-vetted-engineers` | Enterprise Talent Seeker | Inspect dossiers & hire candidates | Deep-links to `/verify/[certId]` & connects on LMS |

---

### 3.2 5-Stage Candidate Lifecycle State Machine

```
+--------------------------------------------------------------------------------------------------+
|                                5-Stage Candidate Lifecycle State Machine                         |
|                                                                                                  |
|   [Stage 1: Application Required]                                                                |
|                 | Candidate submits profile & domain track on /apply or /internships             |
|                 v                                                                                |
|   [Stage 2: Under Review]                                                                        |
|                 | Technical Council evaluates GitHub/resume; emits fast-track preview            |
|                 v                                                                                |
|   [Stage 3: Selected / Deposit Pending]                                                          |
|                 | Formal offer issued (DBERT-OFR-2026-XXXX); signs agreement on /portal/offer   |
|                 | Pays ₹499 Caution Deposit via UPI (Q652429146@ybl) and submits 12-digit UTR    |
|                 v                                                                                |
|   [Stage 4: Deposit In Review]                                                                   |
|                 | Automated & Staff UTR reconciliation in /admin                                 |
|                 v                                                                                |
|   [Stage 5: Confirmed Fellow & Active Sprints]                                                   |
|                 | Official PDF Appointment Letter unlocked; BYOK Gemini setup on /account        |
|                 | Logs 10 hrs/week attendance; solves sprint bounties on /tasks                  |
|                 v                                                                                |
|   [Graduation & Stipend Release Pipeline]                                                        |
|                 | Merges Upstream PR on Partner Repo; Earns Grade A/A+ on 9-Dimension Rubric     |
|                 | 5-Gate Stipend Protocol unlocks ₹5,000 Payout to Encrypted UPI ID              |
+--------------------------------------------------------------------------------------------------+
```

---

### 3.3 Programmatic SEO Architecture across Touchpoints

1. **Dynamic City-Targeted Landing Pages (`/internships/[role]/[city]`)**:
   - **URL Structure**: `https://dbert.in/internships/${role}/${city}`
   - **Taxonomy Footprint**: 18 Canonical Cities $\times$ 9 Canonical Roles = **162 Pre-Rendered SSG Routes**.
   - **Static Generation**: Pre-rendered via `generateStaticParams()` at build time with 0ms server compute overhead.
   - **Bounded Dynamic Metadata Formulas**:
     - **Title**: `${RoleTitle} Internships in ${CityName} (2026 Batch) | DBERT` (Strictly $\le 56$ characters including suffix).
     - **Meta Description**: `Apply for ${RoleTitle} internships in ${CityName}. Build production client codebases, earn performance stipends, and earn verifiable MSME credentials.` (Strictly 140–155 characters).
     - **Canonical Tag**: `https://dbert.in/internships/${role}/${city}`.
     - **OpenGraph & Twitter Card**: Previews generated with role, city name, and verified badge.

2. **Master & Specialized Course Pages (`/learners/courses/[courseSlug]`)**:
   - **URL Structure**: `https://dbert.in/learners/courses/${courseSlug}`
   - **Metadata Formula**: `${CourseTitle} Course & Certification | DBERT` ($\le 56$ chars).
   - **Interactive Elements**: Weekly 12-week syllabus accordion, live tuition ledger (Upfront vs 9-mo Zero-Cost EMI), Regional Opportunity Bento highlighting tech corridors, and 1-click lead capture modal.

3. **Pre-Vetted Talent Directory (`/verify/directory`)**:
   - **URL Structure**: `https://dbert.in/verify/directory` and `/verify/directory/[domainSlug]`.
   - **Segregated Tab Architecture**:
     - **Tab 1: Pre-Vetted Engineers (Verified · Ready to Hire)**: 65 verified candidates with completed evaluations, Turnitin scans, and unlocked proof dossiers.
     - **Tab 2: Incubation Fellows (Provisional · In Sprints)**: 400 active fellows completing milestones.
   - **Dynamic Hireability Ranking**: Ranked dynamically by highest evaluation scores (98, 97, 96...) with verified candidates surfaced first.
   - **Recruiter Actions**: `View Proof Dossier →` (deep-link to `/verify/[certId]`) and `Connect on LMS →` (routes to `https://lms.dbert.in/company/signup?ref=directory&candidate=[certId]`).

---

### 3.4 Infallible 3-Tier Job Query Fallback Engine

To guarantee a **0% empty-state rate** on every dynamic landing page regardless of local posting density, the query engine applies a deterministic 3-tier cascade:

```
+--------------------------------------------------------------------------------------------------+
|                            Infallible 3-Tier Job Query Fallback Engine                           |
|                                                                                                  |
|   Query: Role = 'ai-agent-development', City = 'jaipur'                                          |
|                                                                                                  |
|   +------------------------------------------------------------------------------------------+   |
|   | Tier 1: Exact City Query                                                                 |   |
|   | Query PostgreSQL: WHERE domain = :role AND location ILIKE '%jaipur%' AND status = 'pub'  |   |
|   +---------------------------------------------+--------------------------------------------+   |
|                                                 | Found >= 3 Listings?                           |
|                                                 +--> YES: Render Tier 1 Exact Localized Cards    |
|                                                 +--> NO: Fallback to Tier 2                      |
|                                                 v                                                |
|   +------------------------------------------------------------------------------------------+   |
|   | Tier 2: Regional Tech Corridor Query                                                     |   |
|   | Expand search to regional cluster: Jaipur -> Delhi-NCR / Noida / Gurgaon Tech Corridor   |   |
|   | Query: WHERE domain = :role AND location IN ('Delhi-NCR', 'Noida', 'Gurgaon')            |   |
|   +---------------------------------------------+--------------------------------------------+   |
|                                                 | Combined Tier 1 + Tier 2 >= 3 Listings?       |
|                                                 +--> YES: Render Cluster Cards with Region Badge |
|                                                 +--> NO: Fallback to Tier 3                      |
|                                                 v                                                |
|   +------------------------------------------------------------------------------------------+   |
|   | Tier 3: Universal Remote & Telecommute Query                                             |   |
|   | Query: WHERE domain = :role AND work_mode IN ('Remote', 'Hybrid') AND status = 'pub'     |   |
|   | GUARANTEE: Infallible 100% fill-rate with verified pan-India telecommute opportunities.   |   |
|   +------------------------------------------------------------------------------------------+   |
+--------------------------------------------------------------------------------------------------+
```

---

### 3.5 Generative Engine Optimization (GEO) & AI Assistant Citation Architecture

Conversational AI platforms (ChatGPT Search, Perplexity AI, Google Gemini, Claude) represent approximately 30% of technical candidate discovery. To maximize citation frequency and accuracy, every page injects an authoritative multi-entity Schema.org `@graph`:

1. **`JobPosting` Schema (Google for Jobs & AI Ingestion)**:
   - `title`: `${RoleTitle} Intern (2026 Batch)`
   - `hiringOrganization`: `Digital Blinc Education Research And Technology` (`https://dbert.in`)
   - `jobLocation`: Physical `PostalAddress` populated from `INDIAN_CITY_DIRECTORY` with street address, postal code, and country `IN`.
   - `jobLocationType`: For remote roles, set to `'TELECOMMUTE'` with `applicantLocationRequirements: { "@type": "Country", "name": "IN" }`.
   - `baseSalary`: Explicit `MonetaryAmount` in `INR` (e.g., minValue: 5000, maxValue: 23000, unitText: 'MONTH').
   - `directApply`: `true`.

2. **`Course` & `EducationalOccupationalProgram` Schema**:
   - `name`: Full course title and code (`DBERT-ENG-XXXX-2026`).
   - `educationalCredentialAwarded`: `Verified Professional Systems Diploma`.
   - `offers`: Structured tuition pricing (`price: 28000` to `38000`, `priceCurrency: INR`).
   - `hasCourseInstance`: Syllabus breakdown with module schedule.

3. **`BreadcrumbList` & `FAQPage` Schema**:
   - Explicit breadcrumb path (`Home` $\rightarrow$ `Internships` $\rightarrow$ `Role` $\rightarrow$ `City`).
   - 3–5 high-intent conversational FAQs addressing eligibility, stipend amounts, and verification.

4. **Global Knowledge Manifest (`/llms.txt`)**:
   - Published at `https://dbert.in/llms.txt` and linked in `layout.tsx` via `<link rel="alternate" type="text/markdown" href="/llms.txt" />`.
   - Contains raw Markdown documentation of DBERT credentials, sovereign domain rules, course codes, and partner repositories for automated crawler indexing.

---

### 3.6 Frictionless Lead Capture & Ingestion Pipelines

1. **Instant Candidate Profile Lookup (`GET /api/enroll/lookup`)**:
   - Cascading query supporting `?certid=` or `?email=` across:
     1. `balance_enrollments_1500.json`
     2. `verification_submissions_299.json`
     3. `all_409_provisional_registry.json`
     4. `certificates_registry.json`
     5. `sheet_1593_provisional_registry.json`
   - Enforces PII masking on public requests (masks email `abc***@domain.com`, phone `+91 ******1234`).
   - Returns candidate full name, college, domain track, certificate ID, and next cohort standup dates.

2. **Idempotent 12-Digit UTR Balance Payment (`POST /api/enroll/balance`)**:
   - Accepts candidate identifier, domain, and 12-digit UPI UTR number.
   - **Duplicate Protection**: Intercepts repeated UTR submissions and returns HTTP 200 with `{ alreadySubmitted: true }`, preventing double-crediting.
   - Generates unique deterministic submission ID (`DBERT-ENR-[timestamp]-[randomHex]`).
   - Appends record to `data/balance_enrollments_1500.json` and syncs with PostgreSQL.

3. **Typo Forwarding & Alias Redirection**:
   - Routes `/enroll` and `/eroll` automatically forward to `/enroll/1999` while preserving all URL parameters (`?certid=...&email=...`).

---

## 4. Comprehensive Financial Ledger & Credential Gates

### 4.1 Strict Dual-Ledger Separation Principle

The platform enforces strict cryptographic and accounting separation between student learning incentives and withdrawable monetary balances. Zero cross-pollination is permitted.

```
+--------------------------------------------------------------------------------------------------+
|                            STRICT DUAL-LEDGER SEPARATION PRINCIPLE                               |
|                                                                                                  |
|   +----------------------------------------------+ +-----------------------------------------+   |
|   |         TASK LEDGER ('task' / 'spent')       | |   REFERRAL LEDGER ('referral' / 'withdr')   |   |
|   |----------------------------------------------| |-----------------------------------------|   |
|   | • Source: Sprint tasks, quizzes, daily       | | • Source: Ambassador referral bounties  |   |
|   |   streaks, omnichannel bounties (101-104).   | |   and ₹5,000 Capstone Milestone Stipend.|   |
|   |                                              | |                                         |   |
|   | • Purpose: Internal gamification and perks. | | • Purpose: Direct monetary disbursement |   |
|   |                                              | |   to candidate bank accounts.           |   |
|   |                                              | |                                         |   |
|   | • Redeemable ONLY in Perks Store (/tasks):   | | • Withdrawable ONLY via Encrypted UPI:  |   |
|   |   - 100 Coins: AI ATS Resume Audit Pass      | |   - 1 Coin = ₹1.00 INR                  |   |
|   |   - 100 Coins: 1-on-1 AI Mock Interview      | |   - Processed via /admin/ambassador-    |   |
|   |   - 500 Coins: Senior Mentor Strategy Call   | |     payouts with decrypted UPI ID.      |   |
|   |   - 1 Coin = ₹1: Course Tuition Discount     | |                                         |   |
|   |                                              | | • CANNOT BE SPENT on Perks or Course    |   |
|   | • CANNOT BE CASHED OUT AS REAL MONEY.        | |   Discounts.                            |   |
|   +----------------------------------------------+ +-----------------------------------------+   |
+--------------------------------------------------------------------------------------------------+
```

---

### 4.2 Program Monetization & Fee Structures

| Track Identifier | Fee Amount | Target Stage & Lifecycle Event | Payment Mechanism & Ingress Route | Ledger Persistence & Database Destination |
|---|---|---|---|---|
| **Track A: Caution Deposit** | **₹499** | Seat confirmation for Selected candidates (Stage 3 $\rightarrow$ Stage 5) | Scan UPI QR (`Q652429146@ybl` - DBERT Admissions), submit 12-digit UTR on `/portal/offer` | PostgreSQL `enrollments` table (`payment_status = 'Accepted'`) |
| **Track B: Incubation Balance Completion** | **₹1,500** | Net balance for fellows with prior ₹499 caution deposit credit | Autofilled via `/enroll/1999?certid=...` or `?email=...`, submit 12-digit UPI UTR | Appended to `data/balance_enrollments_1500.json` on disk & synced to DB |
| **Track C: Direct Full Incubation** | **₹1,999** | Fresh direct enrollees joining incubation without prior caution deposit credit | Full ₹1,999 payment via UPI QR, instant UTR submission at `/enroll/1999` | Appended to `data/balance_enrollments_1500.json` |
| **Track D: Credential Verification & Gate 1 Unlock** | **₹299** | Upgrades provisional credentials (`isProvisional: true`) to verified status | Inbound submission via `/verify/unlock` or `/enroll/1999?fee=299` | Reconciled in `data/verification_submissions_299.json`, `certificates_registry.json`, `intern_certificates` |

---

### 4.3 5-Gate Stipend Disbursement Protocol (₹5,000 Milestone Payout)

Every candidate seeking release of the ₹5,000 capstone stipend must pass through 5 sequential gates:

```
+--------------------------------------------------------------------------------------------------+
|                            5-GATE STIPEND DISBURSEMENT PROTOCOL (₹5,000)                         |
|                                                                                                  |
|   Candidate visits /stipend/tasks                                                                |
|                 |                                                                                |
|                 v                                                                                |
|   +------------------------------------------------------------------------------------------+   |
|   | GATE 1: CREDENTIAL VERIFICATION GATE                                                     |   |
|   | Check: intern_certificates.tier == 'verified' AND isProvisional == false                |   |
|   +---------------------------------------------+--------------------------------------------+   |
|                                                 | Passed?                                        |
|                                                 +--> NO: Show locked card -> Upgrade at /enroll  |
|                                                 +--> YES: Proceed to Gate 2                      |
|                                                 v                                                |
|   +------------------------------------------------------------------------------------------+   |
|   | GATE 2: TENURE MATURATION TIMELINE GATE                                                  |   |
|   | Public Standard: Current Date >= joining_date + 60 calendar days                         |   |
|   | Internal Staging Floor: Release Date = max(end_date + 60 days, 2026-12-03)               |   |
|   +---------------------------------------------+--------------------------------------------+   |
|                                                 | Passed?                                        |
|                                                 +--> NO: Show real-time countdown timer          |
|                                                 +--> YES: Proceed to Gate 3                      |
|                                                 v                                                |
|   +------------------------------------------------------------------------------------------+   |
|   | GATE 3: ENCRYPTED PAYOUT CONFIGURATION GATE                                              |   |
|   | Check: Valid encrypted UPI ID registered on /account/settings or /portal?tab=editprofile |   |
|   +---------------------------------------------+--------------------------------------------+   |
|                                                 | Passed?                                        |
|                                                 +--> NO: Show setup card -> Enter UPI ID         |
|                                                 +--> YES: Proceed to Gate 4                      |
|                                                 v                                                |
|   +------------------------------------------------------------------------------------------+   |
|   | GATE 4: CAPSTONE DELIVERABLES & UPSTREAM PR GATE                                         |   |
|   | 1. Active Pull Request merged/open on 1 of the 4 official partner repositories           |   |
|   | 2. Verified DBERT credential added to LinkedIn under 'Licenses & Certifications'         |   |
|   +---------------------------------------------+--------------------------------------------+   |
|                                                 | Passed?                                        |
|                                                 +--> NO: Status = 'changes_requested' with notes |
|                                                 +--> YES: Proceed to Gate 5                      |
|                                                 v                                                |
|   +------------------------------------------------------------------------------------------+   |
|   | GATE 5: ACADEMIC COUNCIL & STAFF APPROVAL GATE                                           |   |
|   | 1. Technical Council audits deliverables across 9-dimension rubric (Score >= 80/100)     |   |
|   | 2. Turnitin originality scan verifies similarity < 5%                                    |   |
|   | 3. Staff clicks 'Approve Payout' in /staff/tasks/<id>/decision                           |   |
|   | 4. System atomically credits 5,000 coins to referral ledger (coin_ledger_mirror)          |   |
|   | 5. Intern clicks 'Request Payout' -> Admin executes bank transfer via decrypted UPI      |   |
|   +------------------------------------------------------------------------------------------+   |
+--------------------------------------------------------------------------------------------------+
```

---

### 4.4 The 4 Official Partner Repositories & Upstream PR Requirements

For any milestone or capstone deliverable to satisfy Gate 4, pull requests must be submitted directly against one of DBERT's 4 official partner repositories:

1. **Alkame (`Alkameinc/alkame-nifty-50-educational`)**:
   - **Repository URL**: `https://github.com/Alkameinc/alkame-nifty-50-educational`
   - **Focus Area**: Nifty 50 algorithmic trading indicators, technical analysis metrics (RSI, MACD, Bollinger Bands), backtesting engines, and financial time-series visualization.
   - **Accepted Deliverables**: Quantitative models, signal generation algorithms, vector backtesters, and Dash/Streamlit dashboards.

2. **Gayatri AI (`Gayatri-Education/Gayatri-Demo`)**:
   - **Repository URL**: `https://github.com/Gayatri-Education/Gayatri-Demo` (and `gayatri-ai`, `gayatri-tutor-v3`)
   - **Focus Area**: Autonomous educational AI tutor, conversational interview simulators, student knowledge state tracking, and pedagogical evaluation pipelines.
   - **Accepted Deliverables**: LLM prompt chains, RAG knowledge retrieval, student response classifiers, and WebSocket chat handlers.

3. **DBERT Agent / Aivara (`DBERT-INDIA/dbert-agent`)**:
   - **Repository URL**: `https://github.com/DBERT-INDIA/dbert-agent` (and `aivara-technologies/aivara-insight-lite`)
   - **Focus Area**: Multi-agent autonomous support systems, LangGraph/CrewAI execution loops, arbitrary CSV semantic ingestion, and automated PowerPoint (`.pptx`) report generation.
   - **Accepted Deliverables**: Multi-agent worker nodes, semantic ingestion routers, and corporate slide synthesis engines.

4. **Internship Portal (`DBERT-INDIA/Internshipportal`)**:
   - **Repository URL**: `https://github.com/DBERT-INDIA/Internshipportal` (and `dbert-website-lms`)
   - **Focus Area**: Production LMS engineering, attendance heartbeat daemons, RFC 8292 VAPID Web Push notifications, Turnitin rubric integrations, and pre-vetted engineer directory search.
   - **Accepted Deliverables**: Flask routes, Next.js UI components, PostgreSQL schema migrations, and anti-tamper attendance filters.

---

## 5. Multi-Agent Operational Execution Plan

### 5.1 Multi-Agent Topology & Hierarchy

To execute complex platform engineering tasks without collision or regression, the multi-agent system operates in a structured hierarchy:

```
+--------------------------------------------------------------------------------------------------+
|                                Teamwork Multi-Agent Hierarchy                                    |
|                                                                                                  |
|                               +-------------------------------+                                  |
|                               |   Team Orchestrator (Lead)    |                                  |
|                               |   c2ae26fc-d263-4b5a-87c2...  |                                  |
|                               +---------------+---------------+                                  |
|                                               |                                                  |
|         +---------------------+---------------+---------------------+--------------------+       |
|         |                     |                                     |                    |       |
|         v                     v                                     v                    v       |
|  +--------------+    +--------------------+                   +--------------+    +--------------+
|  | Spec Miners  |    | Architecture       |                   | Curriculum   |    | Dynamic SEO  |
|  | & Explorers  |    | Worker (R1)        |                   | Workers (R2) |    | Workers (R3) |
|  | (Completed)  |    | worker_r1_arch     |                   |              |    |              |
|  +--------------+    +--------------------+                   +--------------+    +--------------+
|                               |                                                          |
|                               | Produces 01_ARCHITECTURAL_...                            |
|                               v                                                          |
|                      +--------------------+                                              |
|                      | GEO & Lead Capture |<---------------------------------------------+
|                      | Workers (R4)       |
|                      +---------+----------+
|                                |
|                                v
|                      +--------------------+
|                      | Parallel QA Wave:  |
|                      | - 2 Reviewers      |
|                      | - 2 Challengers    |
|                      | - 1 Forensic Audit |
|                      +--------------------+
+--------------------------------------------------------------------------------------------------+
```

---

### 5.2 RACI Matrix Across Execution Milestones

| Milestone Identifier | Scope & Deliverable Files | Responsible (R) | Accountable (A) | Consulted (C) | Informed (I) |
|---|---|---|---|---|---|
| **M1: Architectural Audit & Operational Plan** | `docs/architecture/01_ARCHITECTURAL_SPECIFICATION_AND_OPERATIONAL_PLAN.md` | `worker_r1_arch` | Orchestrator | Spec Miners, Explorers | Full Team |
| **M2: 9-Domain Curriculum Architecture** | `docs/architecture/02_NINE_DOMAIN_CURRICULUM_ARCHITECTURE.md` | Curriculum Workers | Orchestrator | Academic Council, Lead Architect | Recruiters, Students |
| **M3: Dynamic City Pages & SEO Strategy** | `docs/architecture/03_DYNAMIC_CITY_SEO_LANDING_PAGES_SPECIFICATION.md` | SEO Workers | Orchestrator | Growth Lead, SEO Specialist | Marketing Team |
| **M4: GEO & Lead Capture Architecture** | `docs/architecture/04_GEO_AND_LEAD_CAPTURE_ARCHITECTURE.md` | GEO Specialists | Orchestrator | Admissions, DevOps | Inbound Sales |
| **M5: Master Summary & Forensic Audit** | `docs/architecture/05_MASTER_ARCHITECTURAL_BLUEPRINT_SUMMARY.md` | Reviewers / Forensic Auditor | Orchestrator | All Authors | Executive Council |

---

### 5.3 File Workspace Protocol & Isolation Discipline

1. **Working Directory vs State Directory Separation**:
   - **Working Directory (`c:\Users\user\Desktop\dbert-website-lms`)**: Contains strictly application source code, configuration files, and deliverables in `docs/architecture/`. Under no circumstances should agent metadata (`DISPATCH.md`, `BRIEFING.md`, `progress.md`, `handoff.md`) be written here.
   - **Agent State Directory (`<appDataDir>/scratch/teamwork/<run_id>/.agents/teamwork/<agent_id>/`)**: Contains agent memory, dispatch records, heartbeats, and handoffs.

2. **Strict File Ownership Rules**:
   - Each worker agent has exclusive write ownership of designated files (e.g., `docs/architecture/01_ARCHITECTURAL_SPECIFICATION_AND_OPERATIONAL_PLAN.md` owned exclusively by `worker_r1_arch`).
   - Cross-agent overwrites are strictly prohibited. Agents may read any peer report but write only to their own state folder and assigned workspace deliverables.

3. **Liveness Heartbeat via `progress.md`**:
   - Agents must update `progress.md` after every meaningful step with an updated timestamp: `Last visited: [ISO-8601 Timestamp]`.

4. **Self-Contained 5-Component Handoff Protocol (`handoff.md`)**:
   Every completing agent writes a 5-component handoff report:
   - **Section 1: Observation** (Direct quotes, file paths, line numbers, tool output).
   - **Section 2: Logic Chain** (Step-by-step reasoning from observations to conclusions).
   - **Section 3: Caveats** (Assumptions, uninvestigated areas, constraints).
   - **Section 4: Conclusion** (Actionable final assessment).
   - **Section 5: Verification Method** (Exact reproducible commands to verify results).

---

### 5.4 Verification Gates & Multi-Stage Quality Assurance

Every architectural change and code modification must pass 4 verification gates:

1. **Gate A: Static SEO & Bounded Metadata Audit**:
   - Run `npm run check:seo` or execute `node scripts/check-seo.mjs`.
   - Verifies all titles $\le 52$ characters (prior to ` | DBERT` append), descriptions strictly 140–155 characters, and no duplicate keywords.

2. **Gate B: TypeScript Compilation & Next.js Build Integrity**:
   - In `apps/website`: `npm run build` must complete with 0 errors and 0 unhandled promise rejections.
   - Verifies `generateStaticParams()` successfully pre-renders all 162 programmatic geo-internship routes.

3. **Gate C: Schema Graph Validation**:
   - Extract rendered JSON-LD scripts and validate against Schema.org definitions using `@validator/schema` or Google Rich Results Test API.
   - Ensure all `JobPosting` entities contain valid `baseSalary`, `jobLocation`, and `hiringOrganization`.

4. **Gate D: Adversarial Challenger Review & Forensic Audit**:
   - Two independent Challenger agents evaluate deliverables for dead-ends, silent failures, hardcoded test strings, or unverified claims.
   - A Forensic Auditor verifies that all data models, file paths, and system behaviors are genuine and functional.

---

### 5.5 Production Deployment & Rollout Runbook

```
+--------------------------------------------------------------------------------------------------+
|                            Production Deployment & Rollout Runbook                               |
|                                                                                                  |
|   Step 1: Local Pre-Flight Audit                                                                 |
|   - Run TypeScript checks: `npm run type-check` (apps/website)                                   |
|   - Run SEO validator: `npm run check:seo`                                                       |
|   - Verify no unstaged debug statements or mock test values exist                                |
|                                                                                                  |
|   Step 2: Asset Synchronization via SCP                                                          |
|   - Target: `ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/website/`                       |
|   - Sync modified components, configurations, and public assets                                  |
|                                                                                                  |
|   Step 3: Remote Standalone Next.js Build                                                        |
|   - Execute `npm run build` on EC2                                                               |
|   - Sync dynamic sitemap `.next/server/app/sitemap.xml.body` -> `public/sitemap.xml`             |
|   - Copy `public/` into `.next/standalone/` and `.next/standalone/apps/website/`                 |
|   - Relink persistent data directory: `ln -s /var/www/dbert-website-lms/data .next/standalone/`  |
|                                                                                                  |
|   Step 4: Systemd Service Restart & Liveness Check                                               |
|   - Execute `sudo systemctl restart dbert-website.service`                                       |
|   - Assert `systemctl is-active dbert-website.service` returns `active`                          |
|   - Curl localhost:3000 and sovereign URL `https://dbert.in` (Verify HTTP 200 OK)                |
|                                                                                                  |
|   Step 5: Post-Deployment Smoke Test & Telemetry Verification                                    |
|   - Check `/internships/ai-agent-development/bengaluru` returns HTTP 200 with JSON-LD           |
|   - Check `/verify/directory` displays 465 candidates with active tabs                           |
|   - Verify GA4 real-time debug view registers `G-MN7ME9X518` page_view event                     |
+--------------------------------------------------------------------------------------------------+
```

---

## 6. Appendices & Authoritative Reference Catalog

### Appendix A: Canonical 9 Technical Domains

| # | Domain ID & URL Slug | Canonical Track Title | Course Code | Tuition Fee | Starting Salary Benchmark | Key Technologies Mastered |
|---|---|---|---|:---:|:---:|---|
| **1** | `ai-agent-development` | AI Agent Development & Multi-Agent Systems | `DBERT-ENG-AGNT-2026` | ₹35,000 | ₹5.0 – ₹12.0 LPA | LangChain, CrewAI, LangGraph, Ollama, vLLM, Python, Docker, PostgreSQL |
| **2** | `generative-ai-ml` | Generative AI & Machine Learning Engineering | `DBERT-ENG-GENAI-2026` | ₹34,000 | ₹5.5 – ₹15.0 LPA | PyTorch, Hugging Face, LoRA/QLoRA, GGUF, Scikit-Learn, LiteLLM, FastAPI |
| **3** | `full-stack-development` | Full Stack AI Software Development | `DBERT-ENG-FSTCK-2026` | ₹38,000 | ₹4.0 – ₹10.0 LPA | Next.js 16, React 19, TypeScript, Node.js, Express, PostgreSQL, Prisma, Tailwind |
| **4** | `data-analytics` | Data Analytics & Corporate BI | `DBERT-ENG-DATA-2026` | ₹28,000 | ₹3.5 – ₹9.0 LPA | Python, Pandas, NumPy, SQL, PostgreSQL, Power BI, Excel, Matplotlib, Jupyter |
| **5** | `cybersecurity` | Cybersecurity & Threat Defense | `DBERT-ENG-CYBER-2026` | ₹28,000 | ₹4.5 – ₹10.5 LPA | Wireshark, Nmap, Burp Suite, Metasploit, OWASP Top 10, Wazuh, Linux Hardening |
| **6** | `devops-cloud` | DevOps & Cloud Infrastructure Engineering | `DBERT-ENG-DEVOPS-2026` | ₹28,000 | ₹4.5 – ₹11.0 LPA | Docker, Kubernetes, AWS (EC2/S3/RDS), GitHub Actions, Terraform, Linux, Nginx |
| **7** | `mobile-app-development` | Cross-Platform Mobile App Development | `DBERT-ENG-MOBILE-2026` | ₹28,000 | ₹4.0 – ₹9.0 LPA | Flutter, Dart, React Native, Firebase, REST APIs, State Management, SQLite Mobile |
| **8** | `python-automation` | Python Automation & Web Scraping | `DBERT-ENG-PYAUT-2026` | ₹28,000 | ₹3.5 – ₹8.0 LPA | Python, Selenium, Playwright, BeautifulSoup, Requests, Celery, Redis, Docker |
| **9** | `ui-ux-design` | UI/UX & Product Design Systems | `DBERT-ENG-UIUX-2026` | ₹28,000 | ₹3.5 – ₹7.5 LPA | Figma, Auto-Layout, Design Systems, FigJam, Miro, Wireframing, WCAG 2.1 AA |

---

### Appendix B: Canonical 18 Geo Cities & Technical Corridors

| # | City Slug | Display Name | State / Region | Metro Tier | Primary Tech Corridor & Ecosystem Focus |
|---|---|---|---|:---:|---|
| **1** | `bengaluru` | Bengaluru | Karnataka | Tier 1 Metro | Silicon Valley of India: Outer Ring Road, Whitefield, Electronic City |
| **2** | `delhi-ncr` | Delhi NCR | National Capital Region | Tier 1 Metro | National Capital Tech Cluster, Connaught Place, Okhla |
| **3** | `mumbai` | Mumbai | Maharashtra | Tier 1 Metro | Financial Technology (Fintech) Capital, BKC, Andheri East, Powai |
| **4** | `hyderabad` | Hyderabad | Telangana | Tier 1 Metro | HITEC City, Gachibowli, Financial District, Cyberabad |
| **5** | `pune` | Pune | Maharashtra | Tier 1 Metro | IT & Automotive Engineering Hub, Hinjawadi Infotech Park, Magarpatta |
| **6** | `chennai` | Chennai | Tamil Nadu | Tier 1 Metro | SaaS & Enterprise Capital, OMR (IT Corridor), Tidel Park, Guindy |
| **7** | `kolkata` | Kolkata | West Bengal | Tier 1 Metro | Salt Lake Sector V, Rajarhat New Town IT Corridor |
| **8** | `ahmedabad` | Ahmedabad | Gujarat | Tier 2 Hub | GIFT City Fintech Hub, SG Highway, Prahlad Nagar |
| **9** | `jaipur` | Jaipur | Rajasthan | Tier 2 Hub | Mahindra World City, Malviya Nagar, Sitapura Tech Area |
| **10** | `lucknow` | Lucknow | Uttar Pradesh | Tier 2 Hub | IT City Chak Ganjaria, Gomti Nagar Tech Corridors |
| **11** | `chandigarh` | Chandigarh | Punjab / Haryana | Tier 2 Hub | Rajiv Gandhi Chandigarh Technology Park (RGCTP), Mohali IT Hub |
| **12** | `indore` | Indore | Madhya Pradesh | Tier 2 Hub | Crystal IT Park, Super Corridor Indore |
| **13** | `coimbatore` | Coimbatore | Tamil Nadu | Tier 2 Hub | TIDEL Park Coimbatore, Saravanampatti IT Corridor |
| **14** | `kochi` | Kochi | Kerala | Tier 2 Hub | Infopark Kochi, SmartCity Kochi, Kakkanad Tech Hub |
| **15** | `bhubaneswar` | Bhubaneswar | Odisha | Tier 2 Hub | Infocity, Chandaka IT Special Economic Zone |
| **16** | `noida` | Noida | Uttar Pradesh | Tier 1 NCR | Sector 62 IT Hub, Noida-Greater Noida Expressway |
| **17** | `gurgaon` | Gurgaon | Haryana | Tier 1 NCR | Cyber City DLF, Golf Course Extension, Udyog Vihar |
| **18** | `remote` | Universal Remote | Pan-India | Universal | Work-from-Home, Telecommute, Distributed Engineering Teams |

---

### Appendix C: Authoritative 9-Dimension Rubric (100 Marks Total)

Extracted directly from `apps/portal/services/certificate_packet_service.py:503`:

| # | Evaluation Dimension | Assessment Scope & Criteria | Max Marks | Passing Standard |
|---|---|---|:---:|:---:|
| **1** | **Technical Architecture & System Design** | Modular structuring, data flow patterns, clean separation of concerns | **20** | $\ge 16$ |
| **2** | **Code Quality & PEP 8 / Clean Code** | Readability, formatting, docstrings, defensive syntax, exception hygiene | **10** | $\ge 8$ |
| **3** | **Core Algorithms & Implementation** | Application of domain-specific logic, libraries, APIs, and data structures | **10** | $\ge 8$ |
| **4** | **Data Integrity, Security & Validation** | Defensive programming, input sanitization, boundaries, boundary assertions | **10** | $\ge 8$ |
| **5** | **Testing & Verification Coverage** | Unit assertions, automated test runs, edge condition handling, debugging | **10** | $\ge 8$ |
| **6** | **Project Documentation & Deliverables** | Architecture specs, API documentation, sprint logs, README hygiene | **10** | $\ge 8$ |
| **7** | **Problem Solving & Analytical Agility** | Autonomous reasoning, blocker resolution, engineering initiative | **10** | $\ge 8$ |
| **8** | **Sprint Cadence & Delivery Rigor** | Punctual milestone completions, attendance logging, commit consistency | **10** | $\ge 8$ |
| **9** | **Code Review & Technical Viva** | Architectural defense, system comprehension, technical oral defense | **10** | $\ge 8$ |
| **TOTAL** | **Aggregate Performance Score** | **Cumulative across all 9 technical competency dimensions** | **100** | **$\ge 80$ (Merit / Verified)** |

- **Academic Honors Classification**:
  - **90–100 Marks**: Grade A+ (Top Tier Distinction · Surfaced on Tab 1 with High Merit Badge)
  - **80–89 Marks**: Grade A (Merit · Verified Pre-Vetted Engineer)
  - **70–79 Marks**: Grade B (Proficient · Requires revision before corporate referral)
  - **< 70 Marks**: Incomplete / Changes Requested (Resubmission required)

---

### Appendix D: Seeded QA Test Personas

To enable deterministic end-to-end verification across every stage of the student and recruiter lifecycle, 12 master test accounts are permanently seeded and maintained on production EC2 PostgreSQL (`dbert_internship` schema):

| Account Email | Lifecycle Stage | Track Domain | Certificate Status | Key Test Scenario |
|---|---|---|---|---|
| `fresh.applicant@dbert.test` | Stage 1 (Application Required) | `ai-agent-development` | None | Registration, track selection, application submission |
| `under.review@dbert.test` | Stage 2 (Under Review) | `full-stack-development` | None | Application preview, fast-track badge, status polling |
| `selected.deposit@dbert.test` | Stage 3 (Selected / Unpaid) | `generative-ai-ml` | None | Offer letter preview, ₹499 UPI payment, UTR submission |
| `deposit.review@dbert.test` | Stage 4 (Deposit In Review) | `data-analytics` | None | Deposit status banner, UTR reconciliation queue |
| `confirmed.fellow@dbert.test` | Stage 5 (Confirmed Fellow) | `ai-agent-development` | None | Signed appointment letter, BYOK key setup, task dashboard |
| `provisional.fellow@dbert.test` | Stage 5 (Provisional Fellow) | `full-stack-development` | `isProvisional: true` | Balance portal `/enroll/1999`, Gate 1 locked status |
| `verified.graduate@dbert.test` | Stage 5 (Verified Alumnus) | `ai-agent-development` | `isProvisional: false` | 5-Gate stipend release, 5,000 coin credit, UPI cashout |
| `ambassador.leader@dbert.test` | Active Ambassador | `devops-cloud` | Verified Alumnus | Referral code generation, coin withdrawal via UPI |
| `task.perks.tester@dbert.test` | Active Intern (Coin Rich) | `python-automation` | Confirmed Fellow | Task coin accumulation, Perks Store voucher redemption |
| `corporate.recruiter@dbert.test` | Recruiter Persona | Enterprise / Employer | Recruiter Account | Directory search, filter by score $\ge 90$, LMS connect |
| `staff.reviewer@dbert.test` | Staff / Faculty | Administration | Staff Role | Review queue `/staff/tasks`, UTR approval in `/admin` |
| `forensic.auditor@dbert.test` | Forensic Audit Persona | All Tracks | Auditor Role | Read-only inspection of ledgers, schemas, and logs |

*Uniform Master Password for QA accounts*: `TestPass123!`
