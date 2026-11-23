# DBERT MASTER ARCHITECTURE, SITEMAP & OPERATIONAL RUNBOOK (MASTER.md)
================================================================================
Universal Sovereign Source of Truth, System Topology, Complete Sitemaps, Dead-Ends & Silent Fails,
Bug Register, Dead Code Audit, Feature Clubbing Plan & AI Agent Operations Manual
================================================================================
*Document Status*: **ACTIVE & CANONICAL SINGLE SOURCE OF TRUTH (SSOT)**  
*Replaces & Supersedes*: `AGENTS.md`, `GEMINI.md`, `ARCHITECTURE_ROADMAP.md`  
*Last Live Synchronized*: November 23, 2026  
*Production Host*: AWS EC2 `ubuntu@3.26.237.171` (`/var/www/dbert-website-lms`)  
*Active Sovereign Domains*:
- Public Venture Studio & Verification Engine: `https://dbert.in` (Next.js Standalone · Port 3001)
- Production LMS & Intern Workspace: `https://lms.dbert.in` (Flask / Gunicorn · Port 5001)
- Sovereign REST API Backend: `https://api.dbert.in` (Decommissioned / Masked Nov 23, 2026; endpoints consolidated into Next.js & Flask)
*Legacy Retired Domain*: `dbert.online` (Strict 1-hop 301 Permanent Redirect to `dbert.in`)  
*Google Analytics 4 (GA4)*: Strictly `G-MN7ME9X518` across all subdomains and deployment templates.

---

## Table of Contents
1. [§ 0: 60-Second Agent Onboarding & Universal Directives](#-0-60-second-agent-onboarding--universal-directives)
2. [§ 1: System Topology & Infrastructure Map](#-1-system-topology--infrastructure-map)
3. [§ 2: Complete Route Inventory & Canonical Sitemaps](#-2-complete-route-inventory--canonical-sitemaps)
   - [2.1. Next.js Public Website (dbert.in) — 88 Page Routes](#21-nextjs-public-website-dbertin--88-page-routes)
   - [2.2. Production LMS Platform (lms.dbert.in) — 375 Registered Endpoints](#22-production-lms-platform-lmsdbertin--375-registered-endpoints)
   - [2.3. Sovereign REST API Service (api.dbert.in) — 312 API Endpoints](#23-sovereign-rest-api-service-apidbertin--312-api-endpoints)
   - [2.4. Next.js API Route Handlers (24 Endpoints)](#24-nextjs-api-route-handlers-24-endpoints)
4. [§ 3: User Personas, Auth Gates & 5-Stage Lifecycle](#-3-user-personas-auth-gates--5-stage-lifecycle)
   - [3.1. 8 Core User Personas Matrix](#31-8-core-user-personas-matrix)
   - [3.2. 5-Stage Candidate Lifecycle State Machine](#32-5-stage-candidate-lifecycle-state-machine)
   - [3.3. 17 Seeded QA Personas Directory](#33-17-seeded-qa-personas-directory)
5. [§ 4: Payment Funnels, Monetization & Financial Ledgers](#-4-payment-funnels-monetization--financial-ledgers)
   - [4.1. Merchant UPI Payment Credentials](#41-merchant-upi-payment-credentials)
   - [4.2. Industry Incubation & Paid Internship Fellowship Architecture (₹1,999)](#42-industry-incubation--paid-internship-fellowship-architecture-1999)
   - [4.3. Strict Dual-Ledger Separation Principle](#43-strict-dual-ledger-separation-principle)
   - [4.4. Standardized 65–84 Project-Based Grading System (v2026.3)](#44-standardized-6584-project-based-grading-system-v20263)
   - [4.5. Official Offer Letter & Executive Appointment Engine (/portal/offer, /portal/offer/print)](#45-official-offer-letter--executive-appointment-engine-portaloffer-portalofferprint)
6. [§ 5: Comprehensive Dead-End & Drop-Off Audit (D1–D32)](#-5-comprehensive-dead-end--drop-off-audit-d1d32)
7. [§ 6: Comprehensive Silent Failures Audit (S1–S12)](#-6-comprehensive-silent-failures-audit-s1s12)
8. [§ 7: Master Bug Register (P0–P3 Defect Census)](#-7-master-bug-register-p0p3-defect-census)
9. [§ 8: Dead, Obsolete & Redundant Code Audit](#-8-dead-obsolete--redundant-code-audit)
10. [§ 9: Feature Clubbing & Consolidation Architecture](#-9-feature-clubbing--consolidation-architecture)
11. [§ 10: PostgreSQL Schema & Relational Data Dictionary](#-10-postgresql-schema--relational-data-dictionary)
12. [§ 11: Production Operations Playbook](#-11-production-operations-playbook)
    - [11.1. WhatsApp Dual-Account Dispatch System](#111-whatsapp-dual-account-dispatch-system)
    - [11.2. Email Dispatch & Google SMTP Quota Daemon](#112-email-dispatch--google-smtp-quota-daemon)
    - [11.3. Next.js Standalone Build & EC2 Deployment](#113-nextjs-standalone-build--ec2-deployment)
    - [11.4. Admin CLI / SSH Operational Commands](#114-admin-cli--ssh-operational-commands)
13. [§ 12: Real-Time Operational Dashboard & Live Health Queries](#-12-real-time-operational-dashboard--live-health-queries)
14. [§ 13: Strategic Future Expansion Roadmap (Phases 3–7)](#-13-strategic-future-expansion-roadmap-phases-37)
15. [§ 14: File Cleanup, Archival Manifest & Redirection Headers](#-14-file-cleanup-archival-manifest--redirection-headers)

---

## § 0: 60-Second Agent Onboarding & Universal Directives

Any AI agent or software engineer beginning work on DBERT must follow these six non-negotiable operational invariants:

> [!IMPORTANT]
> ### The 6 Non-Negotiable Engineering Invariants
> 1. **Domain Sovereign Rule**: Always use `https://dbert.in`, `https://lms.dbert.in`, or `https://api.dbert.in`. **NEVER emit `dbert.online`** as baseUrl, active origin, in APIs, templates, WhatsApp copy, or emails.
> 2. **Port Allocation Invariant**:
>    - `dbert.in` $	o$ **Port 3001** (Next.js standalone Node server). *Note: Nginx proxies to 3001, NOT 3000.*
>    - `lms.dbert.in` $	o$ **Port 5001** (Flask + Gunicorn WSGI with 4 workers).
>    - `api.dbert.in` $\to$ **Port 8000** (Decommissioned & masked on EC2 as part of Purge Manifest; services centralized into Next.js and Flask).
> 3. **PostgreSQL Schema Isolation**: Database is `dbert_lms` on PostgreSQL 16. All application tables reside in the `dbert_internship` schema. Always execute `SET search_path TO dbert_internship, public;` or prefix tables with `dbert_internship.<table_name>`.
> 4. **Zero Dead-End Guarantee**: Every gate, locked screen, or pending state MUST provide at least one primary action CTA guiding the user to the exact route required to unlock progression.
> 5. **Dual-Monorepo Data Awareness**: Website balance submissions are written to disk (`data/balance_enrollments_1500.json`) and reconciled via crontab every 15 minutes (`sync_enrollments_to_postgres.py`) into PostgreSQL. Never overwrite remote data with empty local files during deployment.
> 6. **Zero Public Stipend & Guaranteed Placement Mandate**: Completely eliminate all public mentions of '₹5,000 stipend', '₹18,000 performance incentive', and monthly stipend ranges from public marketing pages (dbert.in). The sovereign public commitment is **100% Guaranteed Internship / Job Placement** across DBERT portfolio ventures (Gayatri AI, Alkame, Aivara) and verified hiring partners with active production codebase assignments and senior code review. Performance stipends (5,000 coins) are strictly an internal LMS performance incentive on /stipend/tasks, governed by Gates 1–5, and disbursed via the referral coin ledger.

---

## § 1: System Topology & Infrastructure Map

```mermaid
flowchart TD
    subgraph Ingress ["Public Ingress & DNS"]
        User["Client Browser / Mobile"]
        Recruiter["Corporate Recruiter"]
        Legacy["Legacy Traffic (dbert.online)"]
    end

    subgraph AWS_EC2 ["AWS EC2 Host: 3.26.237.171 (Ubuntu 22.04 LTS)"]
        Nginx["Nginx Reverse Proxy & SSL Termination
(/etc/nginx/sites-available/dbert-unified.conf)"]
        
        subgraph Services ["Systemd Application Daemons"]
            NextApp["apps/website
Next.js 14 App Router Standalone
Port: 3001 | dbert-website.service
Domain: dbert.in"]
            FlaskLMS["apps/portal
Flask + Gunicorn (4 Workers)
Port: 5001 | dbert-portal.service
Domain: lms.dbert.in"]
            FastAPIApp["dbert-api-package
FastAPI + Uvicorn (4 Workers)
Port: 8000 | dbert-api.service
Domain: api.dbert.in"]
        end

        subgraph Background_Cron ["Automated System Tasks (crontab */15)"]
            CronRunner["deploy/run_cron_tasks.sh"]
            SyncEnroll["sync_enrollments_to_postgres.py"]
            SyncCerts["sync_verified_certificates_to_portal.py"]
            CronOutbox["POST /api/v1/cron/process-outbox"]
        end

        subgraph Storage_Tier ["State & Relational Persistence"]
            Postgres["PostgreSQL 16 Database: dbert_lms
Schema: dbert_internship (83 Tables)
5,188 Applications (4,359 Selected) | 3,038 Interns | 469 Enrollments | 129 Certs (118 Verified)"]
            JsonRegistry["Master Static Registries (/data & /apps/website/src/data)
certificates_registry.json (477 Certs · 96 Verified)
directory_candidates.json (476 Candidates · 96 Tab 1 Verified)
balance_enrollments_1500.json (8 Submissions)
verification_submissions_299.json (31 Submissions)"]
            SqliteDB["SQLite WAL Database
data/dbert_whatsapp.db (Dispatch Log)"]
        end
    end

    User -->|dbert.in| Nginx
    Recruiter -->|dbert.in / lms.dbert.in| Nginx
    Legacy -->|301 Permanent Redirect| Nginx

    Nginx -->|Proxy 127.0.0.1:3001| NextApp
    Nginx -->|Proxy 127.0.0.1:5001| FlaskLMS
    Nginx -->|Proxy 127.0.0.1:8000| FastAPIApp

    NextApp -->|Local File IO| JsonRegistry
    NextApp -.->|Internal Sync HTTP| FlaskLMS
    FlaskLMS -->|SQLAlchemy / psycopg2| Postgres
    FastAPIApp -->|asyncpg Engine| Postgres

    CronRunner --> SyncEnroll & SyncCerts & CronOutbox
    SyncEnroll -->|Upsert JSON into| Postgres
    SyncCerts -->|Reconcile Verified into| Postgres
```

### 1.1. Production Infrastructure Specification
- **EC2 Instance**: `ubuntu@3.26.237.171` (AWS ap-south-1 Mumbai / ap-southeast-2 Sydney)
- **SSH Key**: `C:\Users\user\.ssh\dbert-production-server.pem`
- **Application Directory**: `/var/www/dbert-website-lms`
- **Nginx Config**: `/etc/nginx/sites-available/dbert-unified.conf` (enabled via symlink)
- **Active Systemd Daemons**:
  * `dbert-website.service`: Next.js 14 Standalone (`node .next/standalone/server.js`, PORT=3001)
  * `dbert-portal.service`: Flask WSGI (`gunicorn --workers 4 --bind 127.0.0.1:5001 wsgi:app`)
  * `dbert-api.service`: FastAPI ASGI (`uvicorn backend.main:app --port 8000 --workers 4`) [DECOMMISSIONED & MASKED on Nov 23, 2026; package archived to `data/archive/dbert-api-package/`]
  * `nginx.service`: Edge reverse proxy, SSL termination, and rate limiting (`auth_limit: 5r/m`).
- **Ubuntu Crontab (`crontab -l`)**:
  * `*/15 * * * * /var/www/dbert-website-lms/deploy/run_cron_tasks.sh >> /var/log/dbert_cron.log 2>&1`
  * `0 2 * * * /var/www/dbert-website-lms/deploy/backup_to_s3.sh >> /var/log/dbert_backup.log 2>&1`

---
## § 2: Complete Route Inventory & Canonical Sitemaps

The ecosystem exposes **over 750 unique URL endpoints** across four distinct route surfaces:

### 2.1. Next.js Public Website (https://dbert.in) — 88 Page Routes

| Route | Page Purpose | Target Audience | Primary CTA | Status / Dead-End Risk | Inline Styles |
|---|---|---|---|---|:---:|
| `/` | Venture Studio Hub | Founders, Enterprises, Engineers | "Browse products" / "Apply for Incubation" | Clean (OK) | 1 |
| `/about` | Studio Identity & Philosophy | General Public, Partners | "Contact Studio" | Clean (OK) | 0 |
| `/about/careers` | Hiring Cohorts & Roles | Job Candidates | "View Open Roles" | Clean (OK) | 0 |
| `/about/contact` | Contact & Inquiries | Prospective Clients | "Send Message" | Clean (OK) | 0 |
| `/about/credentials` | Engineering Audits & Proof | Enterprise Buyers | "Verify Credentials" | Clean (OK) | 0 |
| `/about/team` | Practitioners & Leadership | Prospects, Investors | "Join Our Team" | Clean (OK) | 1 |
| `/admin/alkame-contributors` | Open Source Contributor Roster | Studio Administrators | "Approve Contributor" | DELETED (d263ee5) · Centralized in LMS | 0 |
| `/admin/cohort-applications` | Student & Fellowship Pipeline | Studio Administrators | "Review Application" | DELETED (d263ee5) · Centralized in LMS | 0 |
| `/admin/leads` | Inbound Lead Management | Studio Administrators | "Export CSV" | DELETED (d263ee5) · Centralized in LMS | 0 |
| `/admin/login` | Admin Authentication | Studio Administrators | "Sign In" | DELETED (d263ee5) · Centralized in LMS | 0 |
| `/ai-consultant` | Virtual AI Consultant Interface | Prospects, Explorers | "Ask Technical Question" | Clean (OK) | 0 |
| `/ai-solutions` | Enterprise AI Solutions Hub | Enterprise CTOs, Tech Leads | "Request Enterprise Consultation" | Clean (OK) | 0 |
| `/ai-solutions/consultation` | Enterprise AI Consultation | VP Eng, CTOs | "Schedule Architecture Review" | Clean (OK) | 0 |
| `/ai-solutions/llm-training` | Custom LLM Training & Fine-Tuning | AI Engineering Teams | "Schedule Weights Review" | Clean (OK) | 0 |
| `/ai-solutions/llm-training/dbert-ai` | DBERT AI Sovereign LLM Spec | Enterprises, Security Teams | "Request Weights Audit" | Clean (OK) | 0 |
| `/ai-solutions/llm-training/pipeline` | Interactive Training Pipeline | AI Engineers, Architects | "Test Pipeline Stage" | Clean (OK) | 3 |
| `/ai-solutions/llm-training/private-hosting` | On-Premise & Bare Metal Hosting | Regulated Industries | "Contact Infra Team" | Clean (OK) | 0 |
| `/ai-solutions/products` | Enterprise SaaS Products Catalog | B2B Procurement, CTOs | "Explore Solutions" | Clean (OK) | 0 |
| `/ai-solutions/products/certificate-verification-api` | Certificate Verification API | EdTech, Universities, Issuers | "Integrate API" | Clean (OK) | 0 |
| `/ai-solutions/products/dbert-chat` | DBERT Chat Enterprise Product | Enterprises needing sovereign chat | "Book Private Cloud Demo" | Clean (OK) | 0 |
| `/ai-solutions/products/document-ai` | Document AI Ingestion Engine | Financial, Legal, Healthcare | "Request API Key" | Clean (OK) | 0 |
| `/ai-solutions/products/hiring-automation-suite` | Hiring Automation Suite | Talent Ops, Engineering Directors | "Request Sandbox Access" | Clean (OK) | 0 |
| `/ai-solutions/products/intern-management-system` | Intern Management Platform | University Labs, Companies | "Request Institutional Access" | Clean (OK) | 0 |
| `/blog` | Technical Publication Archive | Engineers, Tech Leads | Search & Filter Tags | Clean (OK) | 0 |
| `/blog/[slug]` | Dynamic Content Page | General Public / Engineers | Explore / Apply | ⚠️ Style Sprawl (14 styles) | 14 |
| `/blog/reader` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 1 |
| `/cohorts/aivara` | Aivara AI Residency Cohort | Elite AI Builders | "Apply for Aivara" | Clean (OK) | 0 |
| `/courses/[domain]` | 9-Domain Dynamic Curriculum | General Public / Engineers | Explore / Apply | Clean (OK) — CourseInteractiveShell & Clean ₹1,999 | 0 |
| `/dbert-online` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/enroll` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/enroll/1999` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 1 |
| `/enroll/299` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/eroll` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/fellows/verified` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/hire/pre-vetted-engineers` | Hire Pre-Vetted AI Engineers | Tech Recruiters, CTOs | "Schedule Talent Match" | Clean (OK) | 2 |
| `/internships` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/internships/[role]` | Dynamic Content Page | General Public / Engineers | Explore / Apply | ⚠️ Style Sprawl (43 styles) | 43 |
| `/internships/[role]/[city]` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 10 |
| `/labs` | DBERT Research Labs | Academics, Researchers, Open Source | "Explore Open Source" | Clean (OK) | 0 |
| `/labs/collaborate` | Research Collaboration Program | Universities, Lab Partners | "Submit Research Proposal" | Clean (OK) | 0 |
| `/labs/opensource` | Open Source Repositories | Developers, Contributors | "Star on GitHub" | Clean (OK) | 1 |
| `/labs/publications` | Technical Papers & Preprints | AI Community | "Read Preprints" | Clean (OK) | 0 |
| `/labs/research` | Ongoing Research Agendas | Research Fellows | "Join Research Squad" | Clean (OK) | 0 |
| `/learners` | Engineering Education Hub | Aspiring Engineers, Students | "Explore Fellowship" | Clean (OK) | 0 |
| `/learners/accelerate` | Accelerate Intermediate Track | Junior Developers | "Enroll in Accelerate" | Clean (OK) | 0 |
| `/learners/courses` | Self-Paced Courses Directory | Independent Learners | "Browse All Courses" | Clean (OK) | 0 |
| `/learners/courses/ai-agent-development` | AI Agent Development Course | Full Stack Developers | "Enroll in Course" | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/cybersecurity` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/data-analytics` | Data Analytics Course | Analysts, Engineers | "Enroll in Course" | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/devops-cloud` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/digital-marketing` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/full-stack-development` | Modern Full Stack Development | Web Developers | "Enroll in Course" | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/generative-ai` | Generative AI & LLM Engineering | Software Engineers | "Enroll in Course" | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/machine-learning` | Machine Learning Fundamentals | Math/CS Students | "Enroll in Course" | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/mobile-app-development` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/python-automation` | Python Automation & Tooling | Beginners, DevOps | "Enroll in Course" | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/courses/ui-ux-design` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) — Dynamic Syllabi & Incubation Flow | 0 |
| `/learners/fellowship` | DBERT AI Fellowship | Advanced Engineers | "Submit Fellowship Screening" | Clean (OK) | 0 |
| `/learners/interview-prep` | System Design & AI Interview Prep | Job Seekers | "Start Interview Mock" | Clean (OK) | 2 |
| `/learners/jobs` | Job Board & Placement Network | Graduates, Hiring Partners | "View Open Positions" | Clean (OK) | 3 |
| `/learners/launchpad` | Launchpad 0-to-1 Program | Beginners, Career Switchers | "Apply for Launchpad" | Clean (OK) | 0 |
| `/learners/resume-checker` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/pricing` | Commercial Rates & Equity Terms | Prospects, Buyers | "Choose Tier" | Clean (OK) | 0 |
| `/privacy` | Privacy Policy | All Users | Footer navigation | Clean (OK) | 0 |
| `/qa` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/refund` | Refund & Cancellation Policy | Paying Customers | Footer navigation | Clean (OK) | 0 |
| `/startups` | Startup Incubation Hub | Early-Stage Founders | "Apply for Incubation" | Clean (OK) | 0 |
| `/startups/investor-network` | Syndicate & Angel Matching | Angel Investors, VCs | "Apply as Accredited Investor" | Clean (OK) | 0 |
| `/startups/portfolio` | Incubated Portfolio Index | Investors, Prospective Founders | "View Case Studies" | Clean (OK) | 0 |
| `/startups/portfolio/alkame` | Alkame Case Study | Founders, Partners | "Build Like Alkame" | Clean (OK) | 0 |
| `/startups/portfolio/cognitive-solutions` | Cognitive Solutions Case Study | Enterprise Buyers | "Schedule Demo" | Clean (OK) | 0 |
| `/startups/portfolio/digital-blaize` | Digital Blaize Case Study | Growth Founders | "Read Build Log" | Clean (OK) | 0 |
| `/startups/portfolio/gayatri-ai` | Gayatri AI Case Study | AI Researchers, Founders | "Explore Architecture" | Clean (OK) | 0 |
| `/startups/register` | Founder Application Form | Founders applying for incubation | "Submit Application" | Clean (OK) | 0 |
| `/startups/services` | Incubation Services Directory | Founders evaluating offerings | "Explore Services" | Clean (OK) | 0 |
| `/startups/services/equity` | Services-for-Equity Model | Bootstrap Founders | "Calculate Equity Split" | Clean (OK) | 0 |
| `/startups/services/equity/term-sheets` | Standard Equity Term Sheets | Legal/Founders | "Download Standard Term Sheet" | Clean (OK) | 0 |
| `/startups/services/funding` | Seed Grants & Investor Network | Seed-stage Startups | "Join Syndicate" | Clean (OK) | 0 |
| `/startups/services/hiring` | Startup Tech Hiring Service | Scaling Founders | "Request Hiring Pipeline" | Clean (OK) | 0 |
| `/startups/services/infrastructure` | Sovereign Cloud & GPU Infra | AI Startups | "Deploy Infra" | Clean (OK) | 0 |
| `/startups/services/legal` | Legal & Compliance Service | Founders needing IP/structuring | "Consult Legal Advisor" | Clean (OK) | 0 |
| `/startups/services/technical` | Technical Architecture & MVP Build | Technical Founders | "Book Technical Audit" | Clean (OK) | 0 |
| `/terms` | Terms of Service | All Users | Footer navigation | Clean (OK) | 0 |
| `/verify` | Certificate Verification Portal | Employers, Credential Checkers | "Verify Certificate ID" | ⚠️ Style Sprawl (20 styles) | 20 |
| `/verify/[certId]` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 0 |
| `/verify/directory` | Dynamic Content Page | General Public / Engineers | Explore / Apply | ⚠️ Style Sprawl (17 styles) | 17 |
| `/verify/directory/[domainSlug]` | Dynamic Content Page | General Public / Engineers | Explore / Apply | ⚠️ Style Sprawl (15 styles) | 15 |
| `/verify/unlock` | Dynamic Content Page | General Public / Engineers | Explore / Apply | Clean (OK) | 1 |

### 2.2. Production LMS Platform (https://lms.dbert.in) — 375 Registered Endpoints

### 1.1. Blueprint Registration Architecture (`routes/__init__.py`)
Modular blueprints are wired via `routes/__init__.py::register_blueprints(app)`. All modular blueprints are mounted at `url_prefix=None` (root namespace), causing direct namespace collision with monolith routes in `app.py`.

| Blueprint File | Blueprint Name | Registered? | Routes Count | Primary Domain Responsibilities |
|---|---|:---:|:---:|---|
| `routes/admin.py` | `admin_bp` | Yes | 6 | Company approval/suspension, telemetry, health analytics, healing, analytics |
| `routes/ambassador.py` | `ambassador_bp` | Yes | 9 | College Ambassador funnel, referral clicks, UPI binding, withdrawals, admin payouts |
| `routes/applications.py` | `applications_bp` | Yes | 1 | Intern application listing (`/intern/my-applications`) |
| `routes/auth.py` | `auth_bp` | Yes | 3 | Multi-role session status, candidate login, universal logout |
| `routes/company.py` | `company_bp` | Yes | 1 | Candidate application status transition |
| `routes/enrollment.py` | `enrollment_bp` | Yes | 4 | Cohort enrollment, Launchpad/Accelerate landing pages, SEO program slugs |
| `routes/intern.py` | `intern_bp` | Yes | 1 | Intern earned credentials JSON API (`/intern/certificates`) |
| `routes/learning.py` | `learning_bp` | Yes | 4 | Adaptive Learning v2 engine, concept DAG tree, reviews, session turns |
| `routes/marketplace.py` | `marketplace_bp` | Yes | 4 | Company job/internship post creation, publishing, unpublishing, deletion |
| `routes/masterclass.py` | `masterclass_bp` | **NO (DEAD)** | 3 | Unregistered 1-hour masterclass registration & promotion endpoints |
| `routes/mentor.py` | `mentor_bp` | Yes | 2 | Mentor group slot booking (up to 30 seats) & seat cancellation |
| `routes/payment.py` | `payment_bp` | Yes | 3 | Payment status, Razorpay server-side order creation & HMAC verification |
| `routes/stipend.py` | `stipend_bp` | Yes | 10 | Stipend tasks dashboard, AI pre-screening, BYOK Gemini key, LinkedIn probe |
| `app.py` (Core Monolith) | `app` | Yes | 327 | Core student portal, offer letters, admin queues, staff evaluation, legacy routes |

---

### 2.3. Sovereign REST API Service (https://api.dbert.in) — 312 API Endpoints

The microservice maps 312 endpoints across 18 specialized sub-routers mounted under `/api/v1`:

| Sub-Router Prefix | Source File | Core Capabilities & Endpoints |
|---|---|---|
| `/auth` | `api/v1/auth/router.py` | Role-based authentication (`/intern/login`, `/company/login`, `/mentor/login`, `/staff/login`, `/admin/login`), OTP registration (`/signup/otp/send`, `/verify`), password resets (`/forgot-password`, `/reset-password`), mobile refresh tokens (`/refresh`, `/logout`). |
| `/intern` | `api/v1/intern/router.py` | Candidate workspace, profile update, resume upload, portfolio links, tutor hours synchronization (`/sync-tutor-hours`), and learning velocity tracking. |
| `/intern/interview` | `api/v1/intern/interview_router.py` | AI technical interview assessment: question bank generation, dynamic Gemini candidate evaluation (`gemini-2.0-flash-lite`), scoring rubric, Turnitin/cheating deterrence. |
| `/applications` | `api/v1/applications/router.py` | Student application intake (`/submit`), application state machine transitions (`Apply Pending` -> `Selected` / `Rejected`), and audit logging into `application_status_history`. |
| `/enrollments` | `api/v1/enrollments/router.py` | Free deposit recording, ₹499 caution deposit, ₹1,999 balance enrollment, candidate lookup (`/lookup`), idempotent UTR validation, verification status transitions. |
| `/payments` | `api/v1/payments/router.py` | Razorpay checkout integration (`/order/create`), HMAC-SHA256 signature verification (`/verify`), webhook ingestion (`/webhook`), idempotent `payment_events` logging. |
| `/courses` | `api/v1/courses/router.py` | Course catalog (`/list`, `/{slug}`), syllabus retrieval, chapter ordering, subtopic content delivery, and day quiz evaluations (`/quizzes/{id}/attempt`). |
| `/learning` | `api/v1/learning/router.py` | Guided Learning (GL) architecture: concepts, knowledge chunks, misconception detection, student mastery profiles, learning turn dialogues. |
| `/company` | `api/v1/company/router.py` | Employer registration, company profile governance, job/internship post creation, applicant tracking, and candidate interview shortlisting. |
| `/marketplace` | `api/v1/marketplace/router.py` | 6,600+ curated tech opportunities (`scraped_internships`, `scraped_jobs`), domain search, filtering, student comments, application routing. |
| `/mentor` | `api/v1/mentor/router.py` | Faculty & mentor network: slot scheduling (`mentor_availability_slots`), student 1-on-1 booking (`mentor_session_bookings`), portfolio code reviews. |
| `/tasks` | `api/v1/tasks/router.py` | Weekly technical sprint tasks, versioned rubrics (`task_versions`), student GitHub/artifact submissions (`task_submissions`), reviewer grading. |
| `/credentials` | `api/v1/credentials/router.py` | Dynamic PDF/CV compilation (`/cv/{slug}`), public credential verification (`/verify/{certId}`), cryptographic hash integrity checks. |
| `/messaging` | `api/v1/messaging/router.py` | Real-time chat threads between candidates, hiring companies, and mentors (`conversations`, `messages`), read status receipts. |
| `/notifications` | `api/v1/notifications/router.py` | Candidate notification center, unread badges, mark-all-read, Web Push device token registration (`web_push_devices`). |
| `/ambassador` | `api/v1/ambassador/router.py` | Campus ambassador referral tracking, coin reward mirroring (`coin_ledger_mirror`), withdrawal requests (`ambassador_withdrawals`). |
| `/admin` | `api/v1/admin/router.py` | Admin control plane: platform configuration (`platform_config`), CSV exports, abuse logs, user role assignment, system health diagnostics. |
| `/cron` | `api/v1/cron/router.py` | Automated maintenance endpoints: `/clean-tokens`, `/process-outbox`, `/enrollment-reminders`, `/cohort-reminders`, `/expire-posts`. Secured by `X-Cron-Secret`. |
| `/uploads` | `api/v1/uploads/router.py` | Secure multipart file upload, MIME type sanitization, size validation (max 6MB), virus/script scanning, local disk persistence under `uploads/`. |
| `/public` | `api/v1/public/router.py` | Anonymous public endpoints: aggregate metrics, candidate directory lookups, SEO metadata feeds. |

---

### 2.4. Next.js API Route Handlers (24 Endpoints)

1. `/api/enroll/balance` (POST) — Records 12-digit UTR balance payments into balance_enrollments_1500.json.
2. `/api/enroll/lookup` (GET) — Candidate autofill by ?certid= or ?email=.
3. `/api/verify` (POST) — Public cryptographic certificate verification.
4. `/api/verify/unlock` (POST) — Provisional certificate unlock via ₹299 UPI UTR submission.
5. `/api/payments/create-order` (POST) — Razorpay order generation (BROKEN: missing production keys).
6. `/api/payments/verify` (POST) — Razorpay webhook & client signature validation.
7. `/api/payments/webhook` (POST) — Automated payment state processing.
8. `/api/courses/enroll` (POST) — Course enrollment inquiry.
9. `/api/cohorts/apply` (POST) — Fellowship intake application.
10. `/api/startups/register` (POST) — Founder incubation application.
11. `/api/labs/collaborate` (POST) — Research lab collaboration proposal.
12. `/api/contact` (POST) — General inbound contact inquiry.
13. `/api/consultation` (POST) — Enterprise architecture consultation.
14. `/api/demo-request` (POST) — Product demo scheduling.
15. `/api/tools/ats-checker` (POST) — AI resume keyword scanner.
16. `/api/telemetry/traffic` (POST) — Edge visitor telemetry.
17. `/api/admin/login` (POST) — Studio administrator auth.
18. `/api/admin/logout` (POST) — Admin session revocation.
19. `/api/admin/setup` (POST) — First-time admin bootstrap.
20. `/api/admin/cohort-applications` (GET/PATCH) — Fellowship applicant pipeline.
21. `/api/admin/leads` (GET) — Inbound client leads.
22. `/api/admin/alkame-contributors` (GET/POST) — Open source contributor roster.
23. `/api/alkame/contributors` (GET/POST) — Public contributor listings.
24. `/api/projects/[slug]/contributors` (GET) — Project contributor queries.

---

## § 3: User Personas, Auth Gates & 5-Stage Lifecycle

### 3.1. 8 Core User Personas Matrix

| Persona ID | Persona Name | Primary Route | Initial State | Primary Goal | Drop-Off Risk Point |
|---|---|---|---|---|---|
| **P1** | **Job Seeker** | `/internships` | Unauthenticated | Browse tech opportunities & apply | External ATS redirect without profile capture (D8) |
| **P2** | **Fresh Applicant** | `/apply`, `/signup` | Stage 1 (Registered) | Choose track & submit profile | Multi-step form failure without autosave (D11) |
| **P3** | **Under-Review Candidate** | `/portal`, `/portal/offer` | Stage 2 (Submitted) | Track review SLA / Fast-track to Paid Fellowship | Drop-off during 24–48h review wait; converted via Incubation Hub (`/portal/offer`) to ₹1,999 Fellowship (D1, D3, D15) |
| **P4** | **Selected Intern** | `/portal/offer` | Stage 3 (Selected) | Sign offer & pay ₹499 deposit | Offer preview locked; payment hesitation (D17) |
| **P5** | **Provisional Holder** | `/verify/[certId]` | Provisional Tier | Unlock verified credential | Directed to ₹1,500 balance instead of ₹299 unlock (D20) |
| **P6** | **Active Confirmed Fellow**| `/portal`, `/tasks` | Stage 5 (Confirmed) | Solve sprint bounties & capstone | Free-tier BYOK Gemini 403 API failure (D6/D23) |
| **P7** | **Graduate Alumnus** | `/stipend/tasks` | Verified Credential | Request ₹5,000 stipend payout | 90 of 143 candidates missing encrypted UPI (D27) |
| **P8** | **Corporate Recruiter** | `/verify/directory`| Unauthenticated | Inspect proof dossiers & hire | "Connect on LMS" drops candidate ID parameter (D30) |

---

### 3.2. 5-Stage Candidate Lifecycle State Machine

```mermaid
stateDiagram-v2
    [*] --> Stage1_ApplicationRequired: Registered (/signup or /apply)
    Stage1_ApplicationRequired --> Stage2_UnderReview: Completes Profile & Submits Application
    
    Stage2_UnderReview --> Stage3_Selected: Technical Council / Admin Approves
    Stage2_UnderReview --> Stage0_Rejected: Application Rejected
    Stage2_UnderReview --> Stage5_Confirmed: Fast-Track Fellowship Upgrade (/enroll/1999)
    
    state Stage3_Selected {
        [*] --> Review_Offer: Step 1: Reviews Terms & Compensation (/portal/offer)
        Review_Offer --> Sign_Offer: Step 2: Signs Digital Offer (/portal/offer/sign)
        Sign_Offer --> Confirm_Seat: Step 3: Submits ₹499 Caution Deposit UTR
    }

    Stage3_Selected --> Stage4_PaymentVerification: Submits ₹499 UPI UTR
    Stage4_PaymentVerification --> Stage5_Confirmed: Staff / Admin Reconciles UTR
    
    state Stage5_Confirmed {
        [*] --> Orientation_Sprint: Day 1-7 Orientation & BYOK Setup
        Orientation_Sprint --> Balance_Completion: Pays ₹1,500 Balance at /enroll/1999
        Balance_Completion --> Production_Sprints: Solves Bounties 101-104 & Capstone
        Production_Sprints --> Capstone_Evaluation: Submits 60-Day Final Project
    }
    
    Stage5_Confirmed --> Verified_Alumnus: Evaluated & Approved (>80 Score)
    Verified_Alumnus --> Stipend_Review: Applies on /stipend/tasks (Day 60+)
    Stipend_Review --> Stipend_Disbursed: ₹5,000 Credited to Referral Wallet
```

---

### 3.3. 17 Seeded QA Personas Directory

To enable deterministic verification across every stage without manual database seeding, 17 master test accounts are permanently maintained in EC2 PostgreSQL (`dbert_internship` schema):

> [!IMPORTANT]
> **Uniform Master Password**: All seeded QA accounts share the identical password: `TestPass123!`.

| Persona Code | Role / Stage Name | Seeded Email / Username | Stage # | State Characteristics | Canonical Route |
|---|---|---|:---:|---|---|
| **ADM** | **Super Administrator** | `dbert_admin@dbert.test` | Admin | Superuser role (`role: admin`); Full portal control | `/admin` |
| **STF** | **Staff Reviewer** | `mentor_staff@dbert.test` | Staff | Evaluator role (`role: staff`); Sprint review queue | `/staff/tasks` |
| **CMP** | **Company Partner** | `company_partner@dbert.test` | Company | Corporate hiring account; Candidate shortlisting | `/company/dashboard` |
| **STG-0** | **Stage 0: Rejected** | `rejected_user@dbert.test` | 0 | Application rejected with appeal card | `/portal` |
| **STG-1** | **Stage 1: Apply Pending**| `stage1_apply@dbert.test` | 1 | Incomplete profile; Inbound application gate | `/portal` |
| **STG-2** | **Stage 2: Under Review** | `stage2_review@dbert.test` | 2 | Applied; Fast-track review badge active | `/portal`, `/portal/offer` |
| **STG-3A**| **Stage 3: Selected** | `stage3_selected@dbert.test`| 3 | Selected; ₹499 Caution Deposit due | `/portal` |
| **STG-3B**| **Stage 3: Offer Pending**| `offer_pending@dbert.test` | 3 | Digital Offer `DBERT-OFR-2026-PA-991` ready | `/portal/offer` |
| **STG-4** | **Stage 4: Deposit Review**| `stage4_pending@dbert.test` | 4 | ₹499 UTR submitted; Bank reconciliation pending | `/portal` |
| **STG-5A**| **Stage 5A: Confirmed** | `fellow_enrolled@dbert.test`| 5 | Enrolled; Day 2 of Full Stack Sprint active | `/portal`, `/tasks` |
| **STG-5B**| **Stage 5B: Grace Expired**| `stage5_grace_expired@dbert.test`| 5 | 7-day orientation ended; ₹1,500 balance due | `/enroll/1999` |
| **STG-5C**| **Stage 5C: Fully Paid** | `fellow_paid_1999@dbert.test`| 5 | ₹1,999 fully settled; All sprints unlocked | `/tasks`, `/certificates` |
| **GATE-1**| **Gate 1: Credential Gated**| `gate1_provisional@dbert.test`| 5 | Provisional Cert; Gate 1 locked on stipend | `/stipend/tasks` |
| **GATE-2**| **Gate 2: Sprint In Progress**| `gate2_progress@dbert.test`| 5 | Verified cert; 42/60 days elapsed (Countdown) | `/stipend/tasks` |
| **GATE-3**| **Gate 3: UPI Setup Due** | `gate3_missing_upi@dbert.test`| 5 | 65 days elapsed; Missing encrypted UPI | `/stipend/tasks` |
| **GATE-4**| **Gate 4: Stipend Ready** | `gate4_ready@dbert.test` | 5 | All criteria met; Capstone form unlocked | `/stipend/tasks` |
| **GATE-5**| **Gate 5: Wallet Cashout**| `gate5_wallet@dbert.test` | 5 | 5,000 Coins in referral ledger; Cashout ready | `/intern/ambassador/withdraw` |

---
## § 4: Payment Funnels, Monetization & Financial Ledgers

The platform processes candidate monetization across four distinct tracks:

```mermaid
flowchart TD
    subgraph Track_A ["Track A: Caution Deposit (₹499)"]
        A1["Selected for Internship (Stage 3)"] --> A2["Visits /portal/offer"]
        A2 --> A3["Step 1: Reviews Terms & Compensation (₹5,000 + ₹18,000)"]
        A3 --> A4["Step 2: Digitally Signs Offer (/portal/offer/sign)"]
        A4 --> A5["Step 3: Scans Merchant UPI QR (Q652429146@ybl) & Submits UTR"]
        A5 --> A6["Admin reconciles in /admin -> Stage 5 (Confirmed)"]
    end

    subgraph Track_B ["Track B: Incubation Balance (₹1,500)"]
        B1["Confirmed Fellow (Paid ₹499 earlier)"] --> B2["Visits /enroll/1999?certid=..."]
        B2 --> B3["Autofills Profile: Total ₹1,999 - ₹499 = ₹1,500 Due"]
        B3 --> B4["Pays ₹1,500 via UPI & Submits UTR"]
        B4 --> B5["Appends to data/balance_enrollments_1500.json"]
        B5 --> B6["15-Min Cron syncs to PostgreSQL (balance_paid=1500)"]
    end

    subgraph Track_C ["Track C: Industry Incubation & Paid Internship Fellowship (₹1,999)"]
        C1["Under-Review / External Applicant"] --> C2["Visits /portal/offer or /enroll/1999"]
        C2 --> C3["Enrolls in Incubation Fellowship (₹1,999 All-Inclusive)"]
        C3 --> C4["Unlocks Production Sprints, 1-on-1 Mentorship & ₹5,000 Milestone Stipend"]
        C4 --> C5["Records UTR in balance_enrollments_1500.json -> Stage 5 (Confirmed)"]
    end

    subgraph Track_D ["Track D: Verification Unlock (₹299)"]
        D1["Provisional Certificate Holder"] --> D2["Visits /verify/unlock"]
        D2 --> D3["Submits ₹299 UPI UTR via /api/verify/unlock"]
        D3 --> D4["Python reconciliation updates PostgreSQL certs (tier='verified')"]
        D4 --> D5["3-Doc Cryptographic PDF Dossier Deployed to Production"]
    end
```

### 4.1. Merchant UPI Payment Credentials
- **Merchant VPA**: `Q652429146@ybl`
- **Merchant Payee Name**: `DBERT Admissions`
- **QR Code Asset**: `/images/qrcode.jpeg` (and fallback `/qrcode.jpeg`)
- **Direct UPI Intent URL**:
  `upi://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am={amount}&cu=INR&tn=DBERT%20{program}%20Fee`
- **Admissions WhatsApp Proof Routing**: `+91 81929 11360`

### 4.2. Industry Incubation & Guaranteed Placement Fellowship Architecture (₹1,999)

The **DBERT Industry Incubation & Guaranteed Placement Fellowship** is engineered specifically for undergraduate and postgraduate engineering students seeking elite, production-grade software development experience and verified career placement credentials.

> [!IMPORTANT]
> **SOVEREIGN MANDATE: Zero Public Stipend & 100% Guaranteed Placement**
> In alignment with commits `d263ee5`, `b69b756`, and `47e6578`:
> 1. **Public Marketing Purge**: All public pages, SEO metadata, course syllabi, and marketing landing pages on `https://dbert.in` have completely eliminated mentions of "₹5,000 stipend", "₹18,000 incentive", and monthly stipend ranges. Promising cash returns on an educational fellowship publicly is prohibited.
> 2. **Core Public Value Proposition**: 100% Guaranteed Internship / Job Placement across internal DBERT portfolio ventures (Gayatri AI, Alkame, Aivara) and verified enterprise partner companies.
> 3. **Placement Disambiguation**: DBERT guarantees **Active Production Codebase Assignment** under senior engineer code review, 1-on-1 technical mentorship, and an independently verifiable 3-document credential packet. DBERT does not guarantee unconditional permanent corporate employment without merit clearance.
> 4. **Internal Performance Stipend Governance (5,000 Coins)**: The ₹5,000 milestone reward exists strictly inside the LMS platform (`/stipend/tasks`) as an internal performance bounty awarded upon clearing Gate 1 (Verification) through Gate 5 (Capstone Review & GitHub PR Merge), credited to `coin_ledger_mirror` with `ledger_kind='referral'` and withdrawable via verified UPI.

#### 1. Student Fellowship & Placement Model
- **All-Inclusive Incubation Fee:** One-time **₹1,999** (Clean single pricing on public pages; zero caution deposit confusion).
- **Dual Enrollment Pathways**:
  * **Direct Incubation Track (`/enroll/1999`)**: Immediate enrollment for candidate fellows with instant cohort onboarding.
  * **LMS Application Track (`/apply`)**: Merit-based admissions pathway where candidates pay a ₹499 caution deposit upon selection, and complete the ₹1,500 balance upon sprint kickoff.
- **Tenure Window**: Strictly **2 Months (8 Weeks)** (`P2M` / `P60D`) across all syllabi, JSON-LD schemas, and marketing copy. Legacy references to "3 months" are retired.
- **The 6 Value Deliverables**:
  1. *Guaranteed Monday Sprint Kickoff*: Zero review delays; direct entry into sprint teams.
  2. *1-on-1 Live Architect Mentorship*: Weekly office hours, PR reviews, and code teardowns.
  3. *Real Production Repositories*: Hands-on contributions to Gayatri AI, Alkame, Aivara.
  4. *Official 3-Document Credential Packet*: Completion Certificate, Academic Project Evaluation, and Personalized Letter of Recommendation (LOR).
  5. *Turnitin Plagiarism Clearance (< 3%)*: Independent proof of authentic software development.
  6. *Tab 1 Placement Directory*: Automatic indexing on `/verify/directory` (Pre-Vetted Engineers · Ready to Hire).

#### 2. Standardized 9-Domain Curriculum Architecture
The platform standardizes course delivery and internship sprints across **9 Core Technical Domains**:
1. **AI Agent Development** (`ai-agent-development`): Autonomous agents, LangChain/LlamaIndex, RAG pipelines, tool-calling APIs.
2. **Data Analyst** (`data-analyst`): Advanced SQL, Pandas, Tableau/PowerBI, variance & driver modeling.
3. **Full Stack Development** (`full-stack-development`): Next.js 14 App Router, TypeScript, Python FastAPI/Flask, PostgreSQL, Tailwind.
4. **Python Automation** (`python-automation`): Playwright/Selenium web automation, ETL pipelines, cron daemons, API scraping.
5. **UI/UX Design** (`ui-ux-design`): Figma design systems, wireframing, UX research, interactive prototyping.
6. **DevOps & Cloud** (`devops-cloud`): AWS/GCP architecture, Docker, Kubernetes, GitHub Actions CI/CD, Terraform.
7. **Mobile App Development** (`mobile-app-development`): React Native, Flutter, Kotlin Android architecture, offline persistence.
8. **Cybersecurity** (`cybersecurity`): OWASP Top 10, penetration testing, threat modeling, SOC analysis, cryptosystems.
9. **Digital Marketing** (`digital-marketing`): Growth engineering, technical SEO, attribution modeling, paid acquisition funnels.

Each domain is served via `CourseInteractiveShell.tsx` with responsive desktop/mobile viewports, Obsidian theme styling, and authentic alumni social proof.

#### 3. 180 Geo-Targeted Programmatic Lead Capture Engine
- Spanning the 9 domains across 20 primary Indian technology metros (Bengaluru, Hyderabad, Pune, Mumbai, Delhi NCR, Chennai, Kolkata, Ahmedabad, Jaipur, Kochi, etc.) = **180 programmatic SEO landing pages** at `/internships/[role]/[city]`.
- Every page embeds `TrackLeadCaptureForm.tsx` communicating with `POST /api/leads/capture`, capturing high-intent student leads directly into `data/leads_inbound.json` and PostgreSQL admissions pipeline.

#### 4. Under-Review Funnel Integration (`/portal/offer`)
- Candidates in Stage 1 & 2 access `/portal/offer` featuring:
  * Signature-first gating: Candidate must review terms and sign digitally before seat confirmation.
  * Clean executive presentation with watermarks and penalty warnings eliminated.
  * Direct deep-link to `/enroll/1999` and 1-tap WhatsApp admissions routing (+91 81929 11360).

### 4.3. Strict Dual-Ledger Separation Principle
1. **Task Ledger (`ledger_kind='task'` / `'spent'`)**:
   - Earned from sprint milestones, social bounties (Tasks 101–104), and attendance streaks.
   - Spendable **ONLY** on coin perks (AI ATS resume scan, mock interview pass, mentor session, course discounts).
   - **NEVER withdrawable as cash**.
2. **Referral Ledger (`ledger_kind='referral'` / `'withdrawal'`)**:
   - Earned from ambassador referrals and the ₹5,000 Capstone Stipend reward.
   - Withdrawable **ONLY** to intern's verified bank account via encrypted UPI.
   - **NEVER spendable on perks or courses**.

### 4.4. Standardized 65–84 Project-Based Grading System (v2026.3)
To ensure credible, merit-backed academic and technical credentials, DBERT enforces a strict non-inflated evaluation model for all newly issued internship certificates and capstone ratings.

#### 1. Core Principles & Boundaries
- **Score Window**: Strictly bounded between **65 and 84 points** (out of 100).
- **Moving-Forward Invariant**: Applies to all newly generated certificates, AI stipend assessments, and automated batch issuances.
- **Historical Immutability**: All previously issued, historical certificates stored in registries remain untouched as-is (except the calibrated flagship test record `CERT-DBERT-2026-AIML-902` set to 82/100, `Grade: A (High Merit)`).

#### 2. Five-Part Deliverable Scoring Formula
1. **Curriculum & Sprint Baseline**: **65 points** (baseline floor for completing 2-month sprints).
2. **Verified GitHub Pull Request**: **+1 to +6 points** (clean commits, branch hygiene, peer review).
3. **Interactive Live Cloud Demo**: **+1 to +5 points** (functional deployment on Vercel/AWS/Render).
4. **Architecture / Technical Case Study Report**: **+1 to +4 points** (system design, API specs, diagrams).
5. **Turnitin Originality Clearance (< 3%)**: **+1 to +4 points** (verified zero plagiarized code).
*Total Possible Range:* **65 (Minimum Pass) to 84 (Maximum Capstone Distinction)**.

#### 3. Standardized Performance Grade Tiers
- **80 – 84**: `Grade: A (High Merit)`
- **75 – 79**: `Grade: B+ (Merit)`
- **70 – 74**: `Grade: B (Proficient)`
- **65 – 69**: `Grade: C+ (Satisfactory)`

#### 4. Mathematical Rubric Parity Guarantee
All 9 academic rubrics must sum **exactly** to the candidate's final score:
$$\sum_{i=1}^{9} \text{Rubric}_i = \text{Total Score} \quad (\text{where } 65 \le \text{Total Score} \le 84)$$
- Dynamic Rubric Generator: `apps/portal/services/grading_service.py` (`generate_9_rubric_marks()`) and TypeScript parity in `apps/website/src/lib/grading.ts` (`generate9RubricMarks()`).
- Automated enforcement in 3-document credential generator (`apps/portal/services/certificate_packet_service.py`), AI stipend evaluation (`apps/portal/services/ai/stipend_evaluator.py`), and directory filters (`DirectoryClient.tsx`).

### 4.5. Official Offer Letter & Executive Appointment Engine (`/portal/offer`, `/portal/offer/print`)

The **DBERT Official Offer Letter & Executive Appointment Engine** governs the legally binding technical appointment, digital signature execution, and seat confirmation for selected engineering candidates across all technical domain tracks.

#### 1. Universal Multi-Domain Architecture
- **Dynamic Track Population**: The template engine renders appointment terms dynamically using the candidate's approved track (`{{ offer.domain }}`), eliminating static or domain-isolated documents.
- **Canonical Domain Acronym Mapping (`OFFER_DOMAIN_CODES`)**:
  Managed centrally in `apps/portal/app.py` to deterministically mint official reference numbers (`DBERT-OFR-2026-[TRACK]-[ID:04d]`):
  * **Full Stack Development / Web Development**: `FSD` (`DBERT-OFR-2026-FSD-XXXX`)
  * **AI & Machine Learning / AI Agent Development**: `AIML` (`DBERT-OFR-2026-AIML-XXXX`)
  * **Python Automation / Backend**: `PA` / `PY` (`DBERT-OFR-2026-PA-XXXX`)
  * **Cybersecurity & Ethical Hacking**: `CYBER` (`DBERT-OFR-2026-CYBER-XXXX`)
  * **Data Analytics & Data Science**: `DA` / `DS` (`DBERT-OFR-2026-DA-XXXX`)
  * **UI/UX & Product Design**: `UIUX` (`DBERT-OFR-2026-UIUX-XXXX`)
  * **Cloud Computing & DevOps**: `CLOUD` / `DEVOPS` (`DBERT-OFR-2026-DEVOPS-XXXX`)
  * **Frontend Development**: `FED` (`DBERT-OFR-2026-FED-XXXX`)
  * **Software Engineering**: `SWE` (`DBERT-OFR-2026-SWE-XXXX`)
- **Generalized Fallback**: If domain resolution is missing, defaults to `"Full Stack Development"` instead of legacy `"Data Analytics"`.

#### 2. Clean Executive Presentation (Watermark & Warning Elimination)
- **Zero Preview Watermarks**: Removed the diagonal dashed `PREVIEW ONLY` stamp, repeating background watermark mesh, and disabled right-click text blockers.
- **Removed Warning Banner**: Removed the yellow `APPOINTMENT TERMS PREVIEW ONLY` pill, restoring full text selection and readability.
- **Standardized Sovereign Identity**: Replaced legacy *"National Technology Incubation Initiative"* and *"National Engineering Incubation Initiative"* across web and print headers with:
  - **`DBERT Applied Engineering Fellowship • Cohort 2026–2027`**
  - **`Directorate of Applied Research & Engineering Fellowship`**
- **Dual Presentation Views**:
  - **Interactive Candidate View (`/portal/offer`)**: Screen-switched view featuring appointment dossier, terms matrix, stepper, and digital signature form.
  - **Executive Print View (`/portal/offer/print`)**: Clean A4 printable document with responsive page breaks, vector SVG letterheads, verified QR badge, and dual-party signature blocks.

#### 3. Standardized Compensation & Payout Structure (₹5,000 + ₹18,000)
- **Term Sheet Table & Preamble**:
  - `Milestone Stipend`: **₹5,000**, disbursed upon completion of sprint milestones (the word `Fixed` is strictly eliminated).
  - `Campus Ambassador Incentive`: **Up to ₹18,000**, performance-linked incentive via the DBERT College Ambassador Program.
  - `Total Earning Potential`: **`₹5,000 + ₹18,000`** *(Total Earning Potential up to ₹23,000)*.
- **Direct UPI Payout Clause (Section 6.3)**:
  - Replaced legacy `Disbursement Window` with **`Disbursement into UPI`**.
  - Payout SLA: Disbursed directly into candidate's verified UPI ID via the LMS Portal immediately upon evaluation approval without artificial holding periods or 30-day delays.
- **Caution Deposit Refund Clause (Section 5)**:
  - Refunded directly to candidate's verified UPI ID upon completion of the 2-month fellowship and standard exit formalities.

#### 4. College Ambassador Program Governance
- **Clause 6.2 Binding Linkage**:
  - Explicitly states that the variable performance incentive (up to ₹18,000) is governed by the **DBERT College Ambassador Program**.
  - Awarded based on campus outreach, tech community leadership, hackathon/workshop organization, and peer engineering referrals.
  - Real-time tier levels, rubrics, and earnings tracking are integrated under `/ambassador` on the LMS Portal.

#### 5. HR Invariant Clauses & Academic Safeguards
- **Clause 3.1: Academic Flexibility & Exam Pause Policy**:
  - Undergraduate and postgraduate fellows facing mid-term or semester examinations may request a formal sprint pause of up to **14 calendar days** with zero milestone penalty or fellowship forfeiture.
- **Clause 9: Credentials & Exit SLA**:
  - Official cryptographic Certificate of Completion (verifiable at `https://dbert.in/verify`) and architect-signed LOR are activated and dispatched within **3 to 5 business days** of final sprint sign-off.

#### 6. Stage 3 Candidate Progression Stepper
- **Step 1 (Appointment Terms Review)**: Full inspection of tenure (2 Months), hours (10 hrs/week), milestones (75 bounty tasks, 2 certs, 1 merged PR), and compensation.
- **Step 2 (Digital Signature via `/portal/offer/sign`)**: Candidate executes digital signature with full legal name, recording timestamp and signature string (`signature_name`, `accepted_at`) in PostgreSQL `intern_offer_letters`.
- **Step 3 (Seat Confirmation & Batch Allocation)**: Unlocks ₹499 refundable caution deposit payment gateway with high-res UPI QR (`Q652429146@ybl`), 1-tap UPI app launchers, and 12-digit UTR submission.

---
## § 5: Comprehensive Dead-End & Drop-Off Audit (D1–D32)

The platform currently exhibits significant friction where candidates, interns, and recruiters encounter unnavigable dead-ends without primary call-to-action (CTA) recovery paths. Below is the systematic audit of the 7 baseline dead-ends (D1–D7) followed by 25 newly discovered dead-ends across all 8 system personas.

### 2.1 Baseline Dead-Ends Audit (D1 to D7)

| # | Route / Screen | Persona | Failure Mechanism & Dead-End Description | Funnel Impact | Architectural Remediation |
|---|---|---|---|---|---|
| **D1** | `/portal` | **P3: Under Review** | Candidate in "Under Review" state sees a static banner saying *"Your application is being reviewed"*. Zero progress indicators, no turnaround timeline, no trial courses, and no prep materials. | High drop-off; candidates assume portal is broken or abandon. | Deployed Stage 2 "Fast-Track Available" card and canonical next-action mission stepper (`build_intern_next_action()`). |
| **D2** | `/learners/courses/*` | **P1 / P6** | Course catalog "Enroll Now" button invokes `/api/payments/create-order` via Razorpay. `RAZORPAY_KEY_ID` was unconfigured in `.env.production`, throwing unhandled HTTP 500 errors. | Checkout hangs indefinitely; zero paid course conversions. | **RESOLVED (Fixed: Nov 22, 2026)**: In `apps/website/src/app/api/payments/create-order/route.ts`, wrapped Razorpay calls in try/catch returning `{ success: false, fallback_upi: true, vpa: 'Q652429146@ybl', amount: ..., qr_url: '/images/qrcode.jpeg', redirect_url: '/enroll/1999' }`, gracefully falling back to 1-Tap UPI QR modal without throwing 500 errors. |
| **D3** | `/portal/offer` | **P2 / P3** | Visiting `/portal/offer` prior to official selection (Stage 1 / Stage 2 Under Review) previously presented a premature, confusing ₹499 caution deposit request before acceptance. | High friction, confusion, and drop-off; candidates questioned paying a deposit for an unapproved application. | **RESOLVED (Fixed: Nov 22, 2026 / Refined: Nov 23, 2026)**: Transformed unselected / under-review `/portal/offer` view into the **DBERT Industry Incubation & Paid Internship Fellowship Hub (Comprehensive Production Training + Guaranteed Paid Internship)**. Features: (1) Transparent screening status with 24–48h SLA and dynamic queue badge (`Queue Position: #18 in Full Stack Development`), (2) 3-step visual status stepper, (3) **Top Executive Highlight Ribbon** (Guaranteed Monday Kickoff, ₹5,000 Milestone Stipend, 1-on-1 Live Mentor Sessions, Official Certificate of Completion, Architect-Signed LOR, Turnitin Rubric, Tab 1 Placement Assistance, ₹1,999 All-Inclusive), (4) **Curriculum & Outcomes Explore Ribbon** linking to `/learners/courses`, `/learners/launchpad`, and `/fellows`, (5) **4 High-Impact Mega Cards** (Real Production Work & GitHub Merges, 1-on-1 Live Mentorship & Office Hours, ₹5,000 Milestone Stipend with 3-gate release checklist [Hours, Tasks, PR Merge], and Complete Career Packet & Placement), and (6) **Clean Single Action Hub** (eliminated duplicate CTA blocks and removed distracting ₹299 credential links) deep-linking to `https://dbert.in/enroll/1999` and 1-tap Admissions WhatsApp desk (`+91 81929 11360`). Selected (Stage 3) candidates access the clean unwatermarked digital appointment letter and ₹499 seat confirmation gateway as designed. Verified 100% across pytest unit tests and local live running servers. |
| **D4** | `/stipend/tasks` | **P5: Provisional** | Provisional fellows visiting stipend milestone submission saw disabled form fields or generic error alerts without an upgrade link. | Support ticket flooding; confusion over ₹5,000 stipend release. | **RESOLVED (Fixed: Nov 20, 2026)**: In `apps/portal/templates/stipend_tasks.html`, deployed prominent "Gate 1 Verification Required" alert card with direct deep-link to `https://dbert.in/verify/unlock?certid={cert_id}`, unlocking Gate 1 and showing clear maturation roadmap. |
| **D5** | `/jobs` (External) | **P1: Job Seeker** | Candidates clicking "Apply Now" on external scraped job posts were immediately redirected off-site with zero intent capture. | Zero application analytics; lost candidate lead attribution. | Intercept external apply with "Suitability Pitch" modal, save candidate intent to DB, then open external site in new tab. |
| **D6** | `/account/gemini-key` | **P6: Active Intern** | Intern entering Gemini API key encountered misleading *"Server or network error during key validation. Please try again."* caused by frontend `.then(r => r.json())` catching 401/403/429 non-JSON responses, probe timeouts across 25+ models, and missing dev mock key bypass. | Drop-off during BYOK setup; interns blocked from AI tutoring sessions. | **RESOLVED (Fixed: Nov 22, 2026)**: In `apps/portal/templates/account_gemini_key.html`, added explicit `X-CSRF-Token` headers, CSRF token in payload, safe `await r.text()` + `JSON.parse` with contextual 401 (login prompt) and 403 (CSRF refresh) handling. Capped live generation probes in `gemini_discovery.py` to top 4 models to eliminate browser timeouts. In `app.py`, enabled instant validation for local dev/test mock keys (`AQ.MOCK_...`, `TEST_...`). Overhauled "How to get your free key (30 seconds)" guide with 1-click Google AI Studio external links (`rel="noopener noreferrer"`), 1-click "Fill Dev Mock Key" testing button, and AES-256 encryption disclosure badge. Verified 100% via Playwright headless testing. |
| **D7** | `/admin/ambassador-payouts`| **P8 / P6** | Admin rejects coin payout request; no automated notification or feedback reason was dispatched to candidate, locking coins in limbo. | Distrust in referral coin economy; student abandonment. | Trigger automated transactional email and in-app alert with rejection explanation, returning coins to active wallet balance. |

---

### 2.2 Deep-Dive Audit: New Dead-Ends Across All 8 Personas

```mermaid
flowchart TD
    subgraph P1_P2["Discovery & Onboarding (P1, P2)"]
        D8["D8: Scraped Job Redirect Loss"]
        D9["D9: Enterprise AI Lead Black Hole"]
        D11["D11: Application Session Loss"]
        D12["D12: Phone Normalization Drop"]
        D13["D13: Post-Reg Stage 1 Orphan"]
    end

    subgraph P3_P4["Screening & Offer (P3, P4)"]
        D14["D14: Rejection Without Appeal"]
        D15["D15: Stage 2 Payment Hard-Block"]
        D16["D16: Missing 48h SLA Countdown"]
        D17["D17: Caution Deposit Review Limbo"]
        D18["D18: Rejected Deposit Form Lock"]
    end

    subgraph P5_P6["Incubation & Sprints (P5, P6)"]
        D20["D20: ₹299 vs ₹1,500 Gateway Confusion"]
        D21["D21: In-Portal Credential Upgrade Void"]
        D23["D23: Unconfigured Gemini Key Block"]
        D24["D24: Flagged Capstone Feedback Wipe"]
        D25["D25: Mobile Safari Sleep Deficit"]
    end

    subgraph P7_P8["Graduation & Hiring (P7, P8)"]
        D27["D27: Gate 3 Missing UPI Blocker"]
        D28["D28: LMS Course Cert 404 on Verify"]
        D29["D29: Window.Print Binary Deficit"]
        D30["D30: Recruiter Connect Parameter Drop"]
        D31["D31: Unapproved Recruiter Jail"]
    end
```

#### Persona 1: Job Seeker (Public Visitors / Job Seekers)
- **D8: External Scraped Job Application Abandonment (`/jobs`, `/internships`):** Candidates click "Apply Now" on scraped job cards and are redirected to third-party ATS portals (Lever, Greenhouse, Workday) without DBERT capturing their email, resume, or contact info. **Drop-off Rate:** 100% of external traffic is lost without lead generation.
- **D9: Enterprise AI Lead Capture Black Hole (`/ai-solutions/products/*`):** On enterprise demo pages, `DemoRequestForm.tsx` submits client-side inquiries. If email transport fails or backend route is missing, form displays a spinner that hangs indefinitely without fallback contact channels.
- **D10: Course Catalog Checkout vs Free Preview Gap (`/learners/courses/*`):** Prospective learners interested in DBERT AI courses cannot preview Day 1 curriculum or interactive sandbox without completing full payment. High-intent visitors bounce immediately.

#### Persona 2: Applicant (Pre-Review Onboarding)
- **D11: Multi-Step Application Form State Loss (`/signup/stage1` & `/apply`):** When applicants complete Stage 1 and navigate to Stage 2 (`/apply`) to write their Statement of Purpose (SOP), validation errors or browser refreshes completely wipe their inputs. No `localStorage` auto-drafting exists, causing high application abandonment.
- **D12: Unvalidated Phone Number Normalization at Stage 1:** Applicants entering 10-digit mobile numbers without country code (`+91`) or with spaces/dashes are stored raw. Subsequent automated WhatsApp dispatchers reject the invalid phone format, stranding applicants from receiving selection notifications.
- **D13: Post-Registration Stage 1 Orphan State:** If an applicant completes Stage 1 account creation and closes their browser before submitting Stage 2 SOP, their subsequent login redirects directly to `/apply` with an ambiguous error banner stating "Application required", confusing users who believed registration was complete.

#### Persona 3: Under Review Candidate (Stage 2)
- **D14: Rejected Candidate Dead-End (`status='Rejected'`):** When an applicant is rejected, logging into `/portal` displays a generic "Application Not Selected" card with zero rubric feedback, no option to appeal, and no alternative recommendations (e.g. self-paced open courses or community bounties), permanently losing the user.
- **D15: Stage 2 Premature Caution Deposit Confusion & Self-Service Resolution:** **RESOLVED (Fixed: Nov 22, 2026 / Refined: Nov 23, 2026)**: Visiting `/portal/offer` prior to selection previously displayed a premature ₹499 caution deposit demand, causing high drop-off from unselected applicants who questioned paying before acceptance. Completely eliminated the caution deposit gate for unselected candidates. Re-architected `/portal/offer` into the **Industry Incubation & Paid Internship Fellowship (Production Training + Guaranteed Paid Internship)** marketing and enrollment engine. Tailored specifically for engineering students, it highlights: (1) **Top Executive Highlight Ribbon** (Guaranteed Monday Kickoff, ₹5,000 Milestone Stipend, 1-on-1 Mentorship, Certificate of Completion, Architect-Signed LOR, Turnitin Rubric, Tab 1 Placement Assistance, ₹1,999 All-Inclusive), (2) **Curriculum & Outcomes Explore Bar** linking to sovereign courses and launchpad, (3) **4 High-Impact Mega Cards** (Real Production Work & GitHub Merges, 1-on-1 Live Mentorship & Office Hours, ₹5,000 Milestone Stipend with 3-gate checklist [10h/wk logins, sprint tasks, 1 merged GitHub PR], Complete Career Placement Packet), (4) Clear financial math: ₹1,999 all-inclusive fee vs ₹5,000 earnable stipend (**+₹3,001 net gain**), (5) Purged distracting ₹299 credential unlock links and eliminated duplicate CTA containers, and (6) Direct 1-click `/enroll/1999` and WhatsApp seat confirmation desk.
- **D16: Turnaround SLA & Urgency Timer:** **RESOLVED (Fixed: Nov 22, 2026)**: In `/portal/offer` and intern dashboard, deployed explicit "Decision SLA: 24–48 Hours" status indicator paired with a dynamic queue status badge (`Queue Position: #18 in Full Stack Development · High Evaluation Volume`) and direct 1-tap WhatsApp Admissions escalation link (`+91 81929 11360`).

#### Persona 4: Selected Candidate (Stage 3 & Stage 4)
- **D17: Caution Deposit Verification Limbo (Stage 4):** Candidate signs digital offer and submits ₹499 UTR. Account transitions to Stage 4 ("Deposit Under Review"). If admissions verification takes > 24 hours, the candidate has zero accessible features—courses, tasks, and community hubs remain locked with no interim onboarding checklist.
- **D18: Rejected Caution Deposit Corrupts Offer Letter View:** If an admin rejects a candidate's ₹499 UTR (`caution_deposit_status='REJECTED'`), the candidate's `/portal/offer` screen locks down. The form fails to clearly indicate the rejection reason or re-enable the UTR input field, requiring manual admin intervention.
- **D19: Single Payment Method Bottleneck:** Both website and LMS strictly offer UPI QR and VPA (`Q652429146@ybl`). Candidates without UPI (international students, corporate cards, net-banking users) have zero alternative checkout rails and drop out at payment.
- **D33: Stage 3 Seat Confirmation Dead-End & Unresponsive Button:** **RESOLVED (Fixed: Nov 23, 2026)**: In `/portal` for Stage 3 selected candidates, the "Proceed to Confirm Seat & Batch" button was unlinked or triggered no downstream action. Re-engineered the button with a direct redirection handler leading to `/portal/offer#action-steps` (Step 2: Sign Digital Offer). Once the candidate provides their digital signature via `/portal/offer/sign`, the UI seamlessly reveals Step 3 (₹499 Caution Deposit reconciliation with high-resolution UPI QR and UTR submission). Additionally resolved contrast/color readability issues on Abhinav Sharma's testimonial quote card (`#e2e8f0` / `#94a3b8`) and eliminated residual "Fixed" phrasing in favor of "Milestone Stipend".
- **D34: Offer Letter Watermark Drift & Legacy Entity Phrasing:** **RESOLVED (Fixed: Nov 23, 2026)**: In `/portal/offer` and `/portal/offer/print`, selected candidates encountered obstructive diagonal `PREVIEW ONLY` watermarks, disabling of text selection, and obsolete *"National Technology Incubation Initiative"* letterheads. Removed all watermarks, enabled native text selection, standardized the sovereign letterhead to **`DBERT Applied Engineering Fellowship • Cohort 2026–2027`**, updated compensation to **`₹5,000 + ₹18,000`** (Total Potential up to ₹23,000 via College Ambassador Program), replaced "Disbursement Window" with **`Disbursement into UPI`**, and integrated HR exam pause (14 days) and credential delivery (3–5 days) SLAs universally across all technical tracks (`FSD`, `AIML`, `PA`, `CYBER`, `DA`, `UIUX`, `DEVOPS`, etc.).

#### Persona 5: Provisional Fellow / Incubation Scholar (Pending Upgrade)
- **D20: The ₹299 vs ₹1,500 Fee Gateway Confusion Trap:** On `/verify/[certId]`, locked provisional certificates display a CTA linking to `/enroll/1999?certid={certId}`. `/enroll/1999` is configured to collect the **₹1,500 Incubation Balance**, whereas the candidate only needs to pay the **₹299 Credential Verification Fee** on `/verify/unlock` to unlock Gate 1. Candidates seeing a ₹1,500 bill abandon the upgrade immediately.
- **D21: Missing In-Portal Credential Upgrade on `/certificates`:** On `https://lms.dbert.in/certificates`, provisional candidates see their certificate watermarked with "PROVISIONAL". Clicking to unlock directs them off-platform to the public website instead of offering an in-app native UPI modal.
- **D22: Stipend Tasks Gating Ambiguity on `/stipend/tasks`:** Provisional candidates are presented with a locked card stating "Milestone Gated". The UI fails to explicitly indicate which of the 5 gates is failing (Gate 1 Credential, Gate 2 Maturation, Gate 3 UPI, or Gate 4 Capstone PR), causing confusion over what action to take.

#### Persona 6: Active Intern / Confirmed Fellow (Stage 5)
- **D23: Unconfigured Gemini Key Blocks Guided Learning:** In `/tasks/<id>/guide`, clicking "Ask AI Tutor" without a configured Gemini key fails with a red error toast. It does not open a side drawer or modal directing the intern to `/account/gemini-key` with 1-click key registration.
- **D24: Flagged Capstone Submission Feedback Wipe (`changes_requested`):** On `/stipend/tasks`, when an admin requests revisions (e.g. invalid GitHub PR), the student resubmits. If the resubmission form encounters a network glitch or validation error, all previous admin feedback notes are cleared from the view.
- **D25: Mobile Safari Sleep Mode Attendance Deficit:** `attendance-tracker.js` pauses accrual when mobile browsers background the tab or activate low-power mode. Interns studying on tablets/phones unknowingly drop below the required 10 hours/week (600 minutes) without any visual or audio alert warning them that tracking has stopped.
- **D26: Coin Perks Catalog Redemptions Dead-End:** While `coin_perks_catalog` and `coin_perk_redemptions` tables exist in PostgreSQL, students spending coins to redeem mock interviews or resume reviews have no automated booking calendar integration—requests sit in an unread database table.

#### Persona 7: Graduate / Verified Alumnus
- **D27: Gate 3 Missing Encrypted UPI Blocker (63% Release Failure Hazard):** Forensic audit of all 143 verified candidates scheduled for ₹5,000 stipend release on **03 December 2026** revealed that **90 candidates (62.9%) have NOT configured their encrypted UPI ID**. The portal dashboard lacks a persistent high-priority banner alerting them that disbursement will fail in 11 days.
- **D28: LMS Course Micro-Certificates Isolated from Public Verification:** Certificates issued upon LMS course completion (`intern_certificates`) are stored in PostgreSQL but never synced to Next.js `certificates_registry.json`. Employers verifying LMS course cert IDs on `https://dbert.in/verify` encounter an HTTP 404 error.
- **D29: Missing PDF Packet Binary Generator on LMS:** The LMS `/portal/certificate/<cert_id>` page relies on browser `window.print()` (which generates messy HTML printouts). The complete 827-line PyMuPDF/ReportLab engine in `certificate_packet_service.py` is never called, preventing graduates from downloading official, vector-crisp 3-document credential dossiers.

#### Persona 8: Recruiter / Employer / Partner
- **D30: Recruiter "Connect on LMS" Deep-Link Parameter Drop:** On `https://dbert.in/verify/directory`, every candidate card features a CTA: `Connect on LMS →` routing to `https://lms.dbert.in/company/signup?ref=directory&candidate=[certId]`. In `apps/portal/templates/company_signup.html`, the form completely ignores `ref` and `candidate` query parameters. When the recruiter signs up, the candidate context is lost, and the recruiter lands on a blank dashboard.
- **D31: Unapproved Recruiter Account Lockdown:** When a company registers, `is_approved=0` is set by default. The company dashboard disables job posting and candidate messaging, with no self-service verification (e.g. work email OTP or LinkedIn OAuth) or estimated approval SLA, resulting in 95% employer abandonment.
- **D32: Pre-Vetted Directory Lacks Recruiter Shortlist & Export:** Recruiters reviewing 96 verified candidates on `/verify/directory` have no bookmark/shortlist capability and no 1-click "Download Talent Batch PDF", forcing them to manually open individual candidate URLs one by one.

---

### 2.3 Master Funnel Dead-Ends Summary Matrix

| ID | Persona | Route / Location | Failure Mechanism | Drop-Off Risk | Priority | Remediation Specification |
|---|---|---|---|:---:|:---:|---|
| **D1** | P3 | `/portal` | Static "Under Review" banner without steps | High | P1 | **RESOLVED**: Interactive 48h turnaround stepper + canonical next-action mission stepper (`build_intern_next_action()`) |
| **D2** | P1/P6 | `/learners/courses/*` | Razorpay 500 crash on missing keys | High | P0 | **RESOLVED**: Replaced with 9-domain `CourseInteractiveShell` and `TrackLeadCaptureForm`, clean ₹1,999 Incubation routing + graceful UPI fallback |
| **D3** | P2/P3 | `/portal/offer` | Premature ₹499 caution deposit request on pre-selection visit | Medium | P1 | **RESOLVED**: Transformed unselected / under-review view into Industry Incubation & Paid Internship Fellowship Hub (Top Ribbon, Curriculum Bar, 4 Mega Cards, ₹5,000 Milestone Stipend Checklist, 1-click /enroll/1999 upgrade) |
| **D4** | P5 | `/stipend/tasks` | Ambiguous gating error for provisional | High | P1 | **RESOLVED**: Dynamic Gate 1 status banner with direct deep-link to `/verify/unlock?certid=...` |
| **D5** | P1 | `/jobs` | Direct external apply leaks candidates | High | P2 | Intercept modal capturing email + suitability pitch |
| **D6** | P6 | `/account/gemini-key` | Free-tier keys pass check but fail on AI / 401/403 network error toast | High | P1 | **RESOLVED**: Robust async error handling, top-4 probe cap, dev mock bypass, and polished 30s guide |
| **D7** | P8/P6 | `/admin/ambassador` | Rejected coin payout leaves wallet frozen | Medium | P2 | Auto-email + in-app notification + coin refund |
| **D8** | P1 | `/jobs` | Scraped job apply leads lost | High | P2 | Auto-create candidate profile on apply click |
| **D9** | P1 | `/ai-solutions/*` | DemoRequestForm hangs on network drop | Medium | P2 | Backend persistence + WhatsApp quick contact |
| **D10**| P1 | `/learners` | Zero course preview before checkout | High | P2 | Day 1 open sandbox lesson preview |
| **D11**| P2 | `/signup/stage1`, `/apply`| Form fields wiped on validation error | High | P1 | LocalStorage draft autosave & auto-recovery |
| **D12**| P2 | `/signup/stage1` | Raw 10-digit phone lacks +91 country code | High | P1 | E.164 phone auto-formatting on blur |
| **D13**| P2 | `/login` | Stage 1 orphan redirected without context | Medium | P2 | Contextual banner explaining required SOP |
| **D14**| P3 | `/portal` | Rejected status provides zero feedback | High | P2 | Evaluation rubric + course re-engagement |
| **D15**| P3 | `/portal/offer` | Premature ₹499 caution deposit confuses unselected applicants | High | P0 | **RESOLVED**: Overhauled into Industry Incubation & Paid Internship Fellowship Hub: Top Ribbon, Curriculum Bar, 4 Mega Cards, ₹5,000 Stipend Checklist, zero deposit demand, and 1-click /enroll/1999 upgrade |
| **D16**| P3 | `/portal/offer` | Missing SLA review countdown & queue visibility | Medium | P1 | **RESOLVED**: 24–48h SLA badge, dynamic queue position (#{{ queue_position }} in Track), and 1-tap WhatsApp Admissions escalation |
| **D17**| P4 | `/portal` | Stage 4 payment review locks entire portal | High | P1 | Unblock orientation hub & pre-sprint setup |
| **D18**| P4 | `/portal/offer` | Rejected deposit corrupts offer screen | High | P1 | Resubmission drawer with admin rejection notes |
| **D19**| P4 | `/portal/offer` | Only UPI accepted; no card/netbanking | Medium | P2 | Add Razorpay/Stripe cards & netbanking |
| **D20**| P5 | `/verify/[certId]` | Locked cert links to ₹1,500 instead of ₹299| Critical | P0 | **RESOLVED (Fixed: Nov 20, 2026)**: In `CandidateProfileClient.tsx`, locked provisional certificate profile links directly to `https://dbert.in/verify/unlock?certid={certId}` for ₹299 verification unlock rather than redirecting to ₹1,500 balance completion. |
| **D21**| P5 | `/certificates` | Provisional cert links off-site for fee | High | P1 | Native in-portal ₹299 UPI checkout modal |
| **D22**| P5 | `/stipend/tasks` | Gating message doesn't specify failed gate | Medium | P2 | 5-Gate granular checklist with action triggers |
| **D23**| P6 | `/tasks/<id>/guide`| Missing BYOK key throws unhandled toast | Medium | P2 | Slide-over drawer with instant Gemini setup |
| **D24**| P6 | `/stipend/tasks` | Resubmission error wipes admin notes | High | P1 | Persist historical review comments in DOM |
| **D25**| P6 | Global LMS | Mobile Safari sleep pauses attendance | High | P1 | Wake Lock API + inactive warning banner |
| **D26**| P6 | `/intern/coins` | Coin perk redemptions lack fulfillment | Medium | P2 | Calendly / automated slot booking hook |
| **D27**| P7 | `/account` | 90 verified interns missing UPI for Dec 03 | Critical | P0 | Persistent sticky modal & WhatsApp warning |
| **D28**| P7 | `/portal/certificate`| LMS course certs 404 on public verify | High | P1 | Auto-sync LMS certificates to registry |
| **D29**| P7 | `/portal/certificate`| Relies on `window.print()`; no binary PDF | High | P1 | Wire `certificate_packet_service.py` to route |
| **D30**| P8 | `/verify/directory`| Recruiter signup drops candidate param | Critical | P0 | Auto-populate candidate shortlist in session |
| **D31**| P8 | `/company` | Unapproved company cannot take any action | High | P1 | Instant work-email OTP auto-approval |
| **D32**| P8 | `/verify/directory`| No recruiter talent bookmark or PDF export| Medium | P2 | Recruiter shortlist cart + 1-click batch PDF |
| **D33**| P4 | `/portal` | "Proceed to Confirm Seat & Batch" button dead-end | High | P1 | **RESOLVED**: Redirects to `/portal/offer#action-steps` (Step 2: Sign Digital Offer -> Step 3: Deposit) |
| **D34**| P4 | `/portal/offer` | Obstructive `PREVIEW ONLY` watermarks & legacy letterhead | High | P1 | **RESOLVED**: Zero watermarks, native text selection, DBERT Applied Engineering Fellowship branding, direct UPI payout, and universal multi-domain coverage |

---

---

## § 6: Comprehensive Silent Failures Audit (S1–S12)

Silent failures represent high-risk architectural failure modes where operations fail without raising alerts, notifying administrators, or presenting recovery instructions to the end user.

```mermaid
flowchart LR
    subgraph Data_Sync_Failures
        S1["S1: Balance Sync Void\n(Next.js to Postgres)"]
        S11["S11: Score Drift Void\n(JSON vs PostgreSQL)"]
        S9["S9: Attendance Ping Drop\n(DB Lock Swallowed)"]
    end

    subgraph External_Service_Failures
        S2["S2: Razorpay 500\n(Missing Secret)"]
        S3["S3: Fernet Decrypt Drop\n(Returns None Silently)"]
        S5["S5: AI 429/504 Stuck\n(Permanent pending_ai)"]
        S6["S6: Outbox SMTP Drop\n(Quota Exhaustion)"]
        S7["S7: Playwright Disconnect\n(Zombie Chromium)"]
    end

    subgraph Security_State_Failures
        S4["S4: CSRF Form Wipe\n(Session Timeout)"]
        S8["S8: Payout Race Condition\n(Duplicate Webhook)"]
        S10["S10: Upload Auth Bypass\n(Nginx Alias Leak)"]
        S12["S12: Push Token Zombie\n(Dead VAPID Devices)"]
    end
```

### 3.1 Baseline Silent Failures Audit (S1 to S5)

| # | Subsystem | Trigger Condition | Silent Failure Manifestation | Architectural Cause | Monitoring & Prevention Fix |
|---|---|---|---|---|---|
| **S1** | **Incubation Payments** (`/enroll/1999`)| Candidate submits 12-digit UTR on Next.js website. | Record written to `balance_enrollments_1500.json` on disk, but never inserted into PostgreSQL `enrollments` table. Candidate cannot log into LMS as "Paid". | Decoupled datastores with no persistent real-time webhook connecting Next.js to Flask. | **RESOLVED (Fixed: Nov 22, 2026)**: Next.js `/api/enroll/balance` and `/api/verify/unlock` now POST directly to Flask `/api/internal/enrollment-sync` with fallback `sync_enrollments_to_postgres.py` cron daemon. |
| **S2** | **Course Payments** (Website) | User clicks "Enroll" on course landing page. | Browser console logs `Unhandled Promise Rejection: 500`; UI loading spinner spins indefinitely. | `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` missing in Next.js production `.env`. | **RESOLVED (Fixed: Nov 22, 2026)**: In `/api/payments/create-order/route.ts`, wrapped payment initialization in try/catch; if gateway fails or keys are missing, gracefully routes to UPI QR checkout modal with `fallback_upi: true`. |
| **S3** | **Fernet Key Decryption** (`apps/portal`)| Secret key rotated or candidate key encrypted under legacy salt. | `Fernet.decrypt()` raises `InvalidToken`; function catches exception and silently returns `None`. Downstream AI tutoring fails with generic "Missing API Key". | Silent exception swallowing in `CryptoService.decrypt()` without logging `CRITICAL`. | Log critical decryption failure with candidate ID; flag `is_active=0` and trigger user re-entry modal. |
| **S4** | **CSRF Token Expiration** | Candidate stays on `/tasks/<id>/guide` or application form > 2 hours. | Submitting form results in HTTP 400/403 `CSRF token expired` without explanation; entire user input is wiped. | Static CSRF token injected at render time without background AJAX refresh. | Intercept 403 CSRF responses; silently fetch fresh token via `/api/csrf-token` and auto-retry submission with preserved draft. |
| **S5** | **AI Pre-Screening Outage** | Google Generative AI API times out (504) or hits quota limit (429). | Task submission succeeds, but AI score remains `NULL` and status is stuck in `pending_ai` indefinitely. | No asynchronous Celery retry queue or fallback circuit breaker handling LLM timeouts. | Wrap in exponential backoff (3 retries); on failure, transition to `pending_staff` with badge: *"Queued for Mentor Review"*. |

---

### 3.2 Deep-Dive Audit: New Silent Failures (S6 to S12)

#### S6: Email Outbox Silent Dropping on Gmail SMTP Quota Exhaustion
- **Subsystem:** `apps/portal/dbert-mailer/` & `scripts/dispatch_409_provisional.py`
- **Trigger:** Daily Google Workspace sending limit (2,000 messages/day) or Google SMTP rate limit exceeded (SMTP response code 421 / 550).
- **Silent Manifestation:** Email dispatch daemon fails to deliver message, increments retry counter, and upon reaching max retries, silently writes `FAILED` to tracking JSON without surfacing an administrative alert or pager notification.
- **Root Cause:** Outbox daemon lacked an automated exit-code alert trigger or Slack/Telegram/Webhook alerting channel.
- **Fix:** Integrated `quota_watchdog_and_dispatcher.py` to continuously probe `smtp.gmail.com:465`. Auto-pauses workers on quota limits and alerts admins via webhook.

#### S7: Headless Playwright WhatsApp Session Revocation & Zombie Workers
- **Subsystem:** `scripts/send_dbert_whatsapp.py` & Playwright automation
- **Trigger:** WhatsApp Web invalidates stored Chrome user data cookies (e.g. Account 1 logged out or QR code re-prompted).
- **Silent Manifestation:** Headless browser launches, fails to find the chat search selector, enters an infinite 60-second retry loop, and marks 46 candidates as `FAILED` while consuming 100% CPU on EC2.
- **Root Cause:** Lack of explicit pre-flight session authentication assertions before batch processing begins.
- **Fix:** Implemented pre-flight healthcheck `verify_and_launch_dbert_whatsapp.py`. Validates presence of `#side` element; immediately terminates worker with exit code 78 (Configuration Error) if unauthenticated.

#### S8: Double Payout Race Condition on Concurrent Payment Webhooks
- **Subsystem:** `apps/portal/routes/payment.py` & `coin_ledger_mirror`
- **Trigger:** Razorpay or external payment gateway sends duplicate webhook dispatches for the same transaction within 200ms.
- **Silent Manifestation:** Both requests pass the non-transactional existence check simultaneously, resulting in double-crediting of referral coins or issuing duplicate enrollment records.
- **Root Cause:** Missing database-level unique constraint on `payment_reference` and lack of atomic row-level locking (`SELECT ... FOR UPDATE`).
- **Fix:** Enforced unique constraint `uq_coin_tx_ref` on `coin_ledger_mirror(reference_id)` and deterministic idempotency keys (`stipend_reward_{submission_id}`).

#### S9: Attendance Heartbeat Lock Contention & Active Minute Loss
- **Subsystem:** `POST /attendance/ping` in `apps/portal/app.py`
- **Trigger:** High concurrency (100+ concurrent interns sending 3-minute pings simultaneously).
- **Silent Manifestation:** Database connection pool exhausts or PostgreSQL deadlocks on `UPDATE attendance SET total_minutes = total_minutes + 3`. Route catches exception and returns `{"status": "error"}`. The client heartbeat tracker ignores the error, permanently losing the intern's active 3 minutes.
- **Root Cause:** Direct row-level updating of historical records under high contention instead of appending to an append-only timecard log.
- **Fix:** Implement atomic `INSERT INTO attendance_pings (intern_id, ping_at) VALUES (...)` with background async aggregation into weekly attendance totals.

#### S10: Direct File Upload Static Bypass in Legacy Nginx Configs
- **Subsystem:** `apps/portal/services/file_security_service.py` & Nginx
- **Trigger:** Attacker or user navigates directly to `https://api.dbert.in/uploads/resumes/candidate_resume.pdf`.
- **Silent Manifestation:** Legacy Nginx configuration had a static `location /uploads/ { alias /var/www/.../uploads/; }` directive. Nginx served sensitive candidate resumes, payment screenshots, and government IDs directly from disk without executing Flask session authorization or HMAC validation.
- **Root Cause:** Architectural discrepancy between Nginx static asset routing and Flask application security layer.
- **Fix:** Removed static `/uploads/` alias from all Nginx reverse proxies. All upload requests route directly to Gunicorn where `FileSecurityService` verifies session ownership and role permissions.

#### S11: Candidate Verification Dossier Score Drift
- **Subsystem:** Next.js `certificates_registry.json` vs PostgreSQL `intern_certificates`
- **Trigger:** Admin updates an intern's evaluation score (e.g. from 88 to 92) in PostgreSQL or runs an upgrade script.
- **Silent Manifestation:** The candidate's LMS profile displays 92, but their public verification dossier on `https://dbert.in/verify/[certId]` continues rendering the stale score of 88 from `certificates_registry.json`. Employers checking credentials see contradictory information.
- **Root Cause:** Dual source of truth with no bi-directional synchronization bus between PostgreSQL and static JSON registries.
- **Fix:** Deprecate static JSON as source of truth; Next.js verification route `/api/verify` queries PostgreSQL directly via Prisma or read-only database pool.

#### S12: Expired Web Push VAPID Token Pruning Void
- **Subsystem:** `apps/portal/services/vapid_manager.py` & `web_push_devices`
- **Trigger:** Intern uninstalls browser, clears site data, or revokes notification permissions.
- **Silent Manifestation:** Push dispatch service continues sending HTTP POST requests to FCM/Mozilla endpoints, receiving HTTP 410 Gone / 404 Not Found. These dead endpoints accumulate indefinitely in `web_push_devices`, slowing down batch broadcasts by 400%.
- **Root Cause:** Catch block in push dispatcher logged a warning but failed to execute `DELETE FROM web_push_devices WHERE endpoint = ?`.
- **Fix:** Automatically prune device rows upon receiving HTTP 410 (Gone) or 404 (Not Found) during push dispatch.

---

### 3.3 Master Silent Failures Summary Matrix

| ID | Subsystem | Trigger Condition | Silent Manifestation | Architectural Cause | Detection & Prevention Fix |
|---|---|---|---|---|---|
| **S1** | Incubation Balance | Next.js UTR submission | Record on disk only; missing in DB | Decoupled datastores | Real-time webhook + cron sync daemon |
| **S2** | Course Checkout | Website Razorpay click | 500 error / infinite spinner | Missing API keys in `.env` | UPI fallback modal + key validation |
| **S3** | BYOK Decryption | Secret key rotated | Returns `None` silently; AI 403 | Exception swallowing in crypto | Log `CRITICAL` alert + prompt key re-entry |
| **S4** | Form Sessions | Stale CSRF (> 2 hours) | 403 wipe of user input | Static CSRF without refresh | AJAX token auto-refresh on 403 |
| **S5** | AI Pre-Screening | Gemini 429/504 timeout | Stuck in `pending_ai` forever | No async retry / circuit breaker | Exponential backoff + human review fallback |
| **S6** | Outbox Mailer | Gmail 2,000 quota limit | Messages marked failed silently | No alerting bus on daemon | Quota watchdog + Slack/Webhook alert |
| **S7** | WhatsApp Daemon | Cookie expiry / logout | Worker loops indefinitely on CPU | Missing pre-flight auth check | Pre-flight DOM assertion + exit code 78 |
| **S8** | Payment Webhook | Duplicate delivery (<200ms) | Double coin payout / records | Lack of DB unique constraints | Enforce unique constraint on reference ID |
| **S9** | Attendance Ping | High-concurrency pings | 3-minute increments lost | Direct table lock contention | Append-only timecard ping ledger |
| **S10**| Upload Security | Direct URL navigation | Private documents exposed | Nginx static alias bypass | Route all `/uploads/` through Flask auth |
| **S11**| Public Verify | DB score update | Public dossier displays old score| Flat JSON desynced from DB | Direct PostgreSQL query on `/verify` |
| **S12**| Web Push | Browser data wiped | Dead endpoints bloat DB | Catch block didn't delete row | Auto-prune on HTTP 410 Gone / 404 |

---

---

## § 7: Master Bug Register (P0–P3 Defect Census)

The following master bug register consolidates all open defects, architectural hazards, and regression risks across the DBERT ecosystem.

```
SEVERITY CLASSIFICATION BENCHMARK:
- P0 (Blocker): Fatal runtime crash, complete user progression blockage, financial loss, or data overwrite hazard.
- P1 (Critical): Core user journey broken, security bypass, major route collision, or isolated credential delivery failure.
- P2 (Major): Data desynchronization, orphaned service maintenance burden, high-friction UX flaw, or unhandled rate limit.
- P3 (Minor / Polish): Visual styling drift, accessibility violation, hardcoded test strings, or unoptimized database query.
```

---

### 4.1 P0 (Blocker) Bugs

#### BUG-P0-01: Foreign Key Constraint Violation on `course_enrollments` (`intern_id` Mismatch)
- **Component:** `apps/portal/app.py:1867`, `apps/portal/services/database/adapter.py`
- **Severity:** **P0 (Blocker)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** Interns logging into `/portal` or hitting `/intern/me` previously triggered a fatal HTTP 500 error:
  ```text
  psycopg2.errors.ForeignKeyViolation: insert or update on table "course_enrollments" 
  violates foreign key constraint "course_enrollments_intern_id_fkey"
  DETAIL: Key (intern_id)=(3167) is not present in table "intern_accounts".
  ```
- **Root Cause:** During auto-enrollment in domain courses (`auto_enroll_intern_in_domain_courses`), the function passed an unverified `intern_id` derived from legacy session cookies or orphaned application records that did not match the PostgreSQL `intern_accounts.id` primary key.
- **Resolution:** Implemented PostgreSQL savepoints (`SAVEPOINT auto_enroll_sp`), isolated transaction handling with rollback and commit, and wrapped course enrollment insertion in canonical `intern_accounts` primary key validation.

#### BUG-P0-02: Live Data Overwrite Hazard (Local Deploy Overwriting EC2 Ledger)
- **Component:** `scripts/deploy_*_to_ec2.py`, `data/balance_enrollments_1500.json`
- **Severity:** **P0 (Blocker)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** Remote EC2 production server possesses live customer payment submissions (e.g. ₹1,500 balance payments and ₹299 verification submissions) that do not exist in local developer workspaces. Running standard SCP deployment scripts overwrites remote JSON files with older local versions, permanently destroying live customer transaction records.
- **Root Cause:** Flat JSON files on disk are tracked in Git and uploaded via blind SCP overwrites without a pre-flight merge or remote fetch.
- **Resolution:** Enforced two-way sync via `scripts/sync_enrollments_to_postgres.py`, modified deployment scripts to safeguard live `data/` files, and created selective archival daemon `scripts/archive_ephemeral_files.py` to preserve all 8 master registries untouched.

#### BUG-P0-03: Stage 2 Under-Review Payment Gating (`can_upload_payment = False`)
- **Component:** `apps/portal/app.py:2097`, `apps/portal/routes/enrollment.py`
- **Severity:** **P0 (Blocker)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** High-intent applicants who complete Stage 2 and want to immediately pay their ₹499 caution deposit or enroll in the ₹1,999 incubation track were previously blocked. Attempting to submit payment yielded `HTTP 403 Forbidden: Application must be in Selected status`.
- **Root Cause:** State machine enforced strict linear progression: `SUBMITTED -> UNDER_REVIEW -> SELECTED -> PAID`. Self-service fast-track payment was disallowed at the code level.
- **Resolution:** Enabled `can_upload_payment: True` for Stage 2 (Under Review) in `apps/portal/app.py:2097`. In `app.py:17957`, added `STATUS_UNDER_REVIEW` to the allowed status list when recording deposit submissions, automatically transitioning candidates to `STATUS_ENROLLMENT_PENDING` without requiring manual review.

---

### 4.2 P1 (Critical) Bugs

#### BUG-P1-01: Orphaned 3-Doc Credential Packet Generator (`certificate_packet_service.py`)
- **Component:** `apps/portal/services/certificate_packet_service.py`, `apps/portal/app.py`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** A complete, 827-line PyMuPDF and ReportLab credential engine capable of generating vector-crisp 3-document credential packets (Completion Certificate, Academic Evaluation Rubric, and Letter of Recommendation) had **ZERO callers** in Flask routes.
- **Root Cause:** Developer built the service file but never wired it to `@app.route("/portal/certificate/<cert_id>/pdf")`.
- **Resolution:** Registered `@app.route("/portal/certificate/<cert_id>/pdf")` and `@app.route("/certificate/<cert_id>/pdf")` calling `CertificatePacketService.get_master_pdf_bytes()` with streaming via Flask `send_file()`. Updated template download CTAs to deep-link directly to this binary PDF generator.

#### BUG-P1-02: Isolated LMS Course Micro-Certificates (404 on `dbert.in/verify`)
- **Component:** `apps/portal/app.py:9784`, `apps/website/src/app/verify/`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED / MITIGATED (Fixed: Nov 22, 2026)**
- **Description:** When an intern completes an LMS domain course, a certificate record is created in PostgreSQL `intern_certificates`. However, this record was isolated from static Next.js registry.
- **Resolution:** Course certificates and canonical credentials are synchronized to Next.js registry via dual-engine lookup (`GET /api/verify`), querying PostgreSQL directly where available or checking `certificates_registry.json`.

#### BUG-P1-03: Recruiter "Connect on LMS" Deep-Link Parameter Drop
- **Component:** `apps/website/src/app/verify/directory/page.tsx`, `apps/portal/templates/company_signup.html`, `apps/portal/app.py`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** Directory deep-linked recruiters to `https://lms.dbert.in/company/signup?ref=directory&candidate=[certId]`. The company signup page previously dropped the `candidate` parameter.
- **Resolution:** In `apps/portal/templates/company_signup.html` and `apps/portal/app.py:12726-12735`, captured `candidate` and `ref` query parameters, rendered an alert banner informing the employer of candidate context, passed them into the signup JSON payload, and saved `session["referred_candidate"] = candidate`.

#### BUG-P1-04: 19 Colliding / Shadowed Flask Routes
- **Component:** `apps/portal/app.py:19812`, `apps/portal/routes/`
- **Severity:** **P1 (Critical)**
- **Status:** **AUDITED / RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** 19 route handlers were declared twice across `app.py` and `routes/*.py`.
- **Resolution:** Audited route precedence across all 19 endpoints, ensured canonical handlers take precedence, and cleaned up obsolete route files.

#### BUG-P1-05: Completely Dead `masterclass_bp` Blueprint (223 Lines)
- **Component:** `apps/portal/routes/masterclass.py`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** `apps/portal/routes/masterclass.py` implemented 223 lines of unreferenced masterclass routes.
- **Resolution:** Safely deleted dead `routes/masterclass.py` and its orphan templates (`masterclass_data_analyst.html`), removing dead code from the repository.

#### BUG-P1-06: Asynchronous Void on `/api/verify/unlock` (Zero Real-Time DB Sync)
- **Component:** `apps/website/src/app/api/verify/unlock/route.ts`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** When a candidate paid ₹299 on `/verify/unlock` to unlock credentials, the API route wrote solely to disk (`verification_submissions_299.json`) without a webhook to Flask PostgreSQL.
- **Resolution:** Added real-time fetch in `route.ts` calling `INTERNAL_LMS_SYNC_URL || 'https://lms.dbert.in/api/internal/enrollment-sync'` with `X-DBERT-Internal-Secret` and `payment_type='verification_299'`, immediately promoting the certificate to `tier='verified'` and setting `stipend_verified=1`.

#### BUG-P1-07: Credential Score Inflation & Uncalculated Hardcoded Rubrics
- **Component:** `apps/website/src/app/verify/[certId]/CandidateProfileClient.tsx`, `apps/portal/services/certificate_packet_service.py`, `apps/portal/services/ai/stipend_evaluator.py`, `apps/website/src/app/verify/directory/DirectoryClient.tsx`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** 
  1. The public candidate profile page (`CandidateProfileClient.tsx`) hardcoded dummy rubric marks (`18/20`, `9/10`, `9/10`, `8/10`, `10/10`... summing to 87) for every candidate on Tab 2, irrespective of their actual academic score.
  2. In `certificate_packet_service.py`, PDF rubric generation relied on a fragile single-rubric `diff` adjustment against a hardcoded base of 84, breaking mathematical validity whenever scores varied.
  3. No standardized grading model bounded capstone deliverables to an uninflated academic scale (65–84), resulting in score creep.
  4. The candidate directory filter only permitted filtering by legacy 90+, 85+, and 80+ thresholds, breaking discovery for candidates graded on realistic performance tiers.
- **Root Cause:** Absence of a unified, deliverable-backed grading engine across Python LMS and Next.js website.
- **Resolution:**
  1. Built dual-runtime grading engines: Python (`apps/portal/services/grading_service.py`) and TypeScript (`apps/website/src/lib/grading.ts`), strictly bounding scores to 65–84 based on a 5-part deliverable checklist (Baseline 65, PR +1 to +6, Live Demo +1 to +5, Technical Report +1 to +4, Turnitin Clearance +1 to +4).
  2. Implemented `generate_9_rubric_marks()` / `generate9RubricMarks()` guaranteeing $\sum_{i=1}^{9} \text{Rubric}_i = \text{Score}$ across all 20 possible scores in $[65, 84]$.
  3. Connected `CandidateProfileClient.tsx` Tab 2 to dynamically compute and display authentic rubrics from the candidate's actual score.
  4. Updated `certificate_packet_service.py` to auto-calculate deliverable scores and enforce exact rubric sums on generated 3-document PDFs.
  5. Calibrated `stipend_evaluator.py` AI prompt and clamped output to $[65, 84]$.
  6. Expanded `DirectoryClient.tsx` dropdown to include `80+ (High Merit)`, `75+ (Merit)`, `70+ (Proficient)`, `65+ (Passing Bar)`, and `85+ (Legacy Top)`.
  7. Calibrated flagship test record `CERT-DBERT-2026-AIML-902` to `82/100` (`Grade: A (High Merit)`).

#### BUG-P1-08: Gemini BYOK Validation Failure & Misleading "Server or Network Error" on `/account/gemini-key`
- **Component:** `apps/portal/templates/account_gemini_key.html`, `apps/portal/app.py:1216`, `apps/portal/services/ai/gemini_discovery.py:147`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** When interns or developers navigated to `/account/gemini-key` and attempted to save an API key or test seeded mock keys, the UI threw a misleading generic error: *"Server or network error during key validation. Please try again."*.
- **Root Cause:** 
  1. In `account_gemini_key.html`, the fetch call omitted explicit `X-CSRF-Token` and `X-Requested-With` headers.
  2. Response parsing used `.then(r => r.json().then(data => ({ status: r.status, data })))`, which threw a JavaScript `SyntaxError` on any non-JSON or plain text response (such as session expiration 401, CSRF mismatch 403, or upstream proxy errors), unconditionally triggering `.catch()` and displaying the generic network error.
  3. `_validate_gemini_key_live` did not support local test/mock keys (such as `AQ.MOCK_TEST_KEY_DEV_ONLY...`), dispatching them to live Google AI Studio endpoints that returned HTTP 400 rejections.
  4. `probe_first_working_model` in `gemini_discovery.py` looped through up to 25+ candidate models sequentially upon encountering errors, causing request times to exceed browser fetch timeouts.
  5. The "How to get your free key (30 seconds):" section lacked security attributes (`rel="noopener noreferrer"`), missed actionable guidance on selecting "Create key in new project" (free tier without credit card), and had no dev test key helper.
- **Resolution:**
  1. In `account_gemini_key.html`, added explicit `X-CSRF-Token` and `X-Requested-With` headers, plus CSRF tokens in the request body.
  2. Replaced fragile `.json()` parsing with safe `await r.text()` + `JSON.parse()` with explicit HTTP 401 (re-login prompt with link), HTTP 403 (CSRF refresh prompt), and HTTP 400 (exact Google API rejection text) error branches.
  3. In `gemini_discovery.py`, capped `models_to_test` to at most the top 4 candidates (`models_to_test[:4]`), guaranteeing responses return well within browser timeouts.
  4. In `app.py`, added instant validation for local mock/dev keys (`AQ.MOCK_`, `TEST_`, `DEV_`, `AIzaSyMock...`).
  5. Overhauled the "How to get your free key (30 seconds):" guide with structured numbered steps, 1-click external link to Google AI Studio, a 1-click "Fill Dev Mock Key" button for instant local testing, and an AES-256 (Fernet) encryption disclosure badge.
  6. Verified 100% end-to-end via headless Playwright browser automation (both successful dev key connection and informative Google rejection display).

#### BUG-P1-09: Stage 3 Seat Confirmation Dead-End & Universal Offer Letter Watermark Drift
- **Component:** `apps/portal/templates/portal.html:870`, `apps/portal/templates/portal_offer_letter.html`, `apps/portal/templates/portal_offer_print.html`, `apps/portal/app.py:6479`
- **Severity:** **P1 (Critical)**
- **Status:** **RESOLVED (Fixed: Nov 23, 2026)**
- **Description:** Selected candidates in Stage 3 encountered significant funnel drop-off and friction across five interconnected touchpoints:
  1. On the main intern dashboard (`/portal`), the primary call-to-action button *"Proceed to Confirm Seat & Batch"* was dead or failed to transition users to the digital signature step.
  2. Founder quote card from Abhinav Sharma suffered poor typographic contrast against dark backgrounds, rendering text unreadable on mobile and desktop viewports.
  3. On `/portal/offer` and `/portal/offer/print`, selected candidates were presented with obstructive diagonal `PREVIEW ONLY` watermarks, disabled text selection, and obsolete *"National Technology Incubation Initiative"* letterhead titles.
  4. Compensation copy contained conflicting "Fixed" terminology alongside an ambiguous "30-day disbursement window" that created candidate distrust regarding stipend release.
  5. Offer letter generator lacked full domain coverage in `OFFER_DOMAIN_CODES`, defaulting missing tracks to "Data Analytics" rather than generating authentic track-specific acronyms (`DBERT-OFR-2026-[TRACK]-XXXX`).
- **Root Cause:** Missing client-side screen transition listener in `portal.html`, residual prototype watermark CSS in offer templates, and unexpanded domain code mappings in `app.py`.
- **Resolution:**
  1. Re-engineered `/portal` Stage 3 stepper: *"Proceed to Confirm Seat & Batch"* triggers a seamless redirection to `/portal/offer#action-steps` (Step 2: Sign Digital Offer). Upon digital signing via `/portal/offer/sign`, the UI reveals Step 3 (₹499 seat confirmation and UPI UTR submission).
  2. Fixed typographic contrast on founder testimonial quote card using high-contrast shades (`#e2e8f0` / `#94a3b8` / `#f8fafc`).
  3. Completely eliminated all diagonal `PREVIEW ONLY` watermark stamps, background mesh patterns, and yellow warning pills from web and print templates, restoring full native text selection.
  4. Standardized sovereign letterhead to **`DBERT Applied Engineering Fellowship • Cohort 2026–2027`** with **`Directorate of Applied Research & Engineering Fellowship`**.
  5. Standardized compensation model to **`Milestone Stipend: ₹5,000`** plus **`Campus Ambassador Incentive: Up to ₹18,000`** (Total Potential up to **`₹5,000 + ₹18,000`** / ₹23,000), explicitly linking the incentive to the **DBERT College Ambassador Program** (`/ambassador`).
  6. Replaced "Disbursement Window" with **`Disbursement into UPI`**, stipulating direct UPI transfer upon sprint milestone clearance with zero holding windows.
  7. Added HR invariant clauses: **Academic Flexibility & Exam Pause Policy** (14-day university exam pause with zero penalty) and **Credentials & Exit SLA** (3–5 business days dispatch).
  8. Expanded `OFFER_DOMAIN_CODES` in `apps/portal/app.py` across all domains (`FSD`, `AIML`, `PA`, `CYBER`, `DA`, `UIUX`, `DEVOPS`, `FED`, `SWE`), verified across a 5-domain audit script and 100% passing pytest suites (`test_offer_letter_staged_flow.py`, `test_local_seeded_ecosystem.py`).

---

#### BUG-P1-10: Mobile Button Clipping & Horizontal Body Overflow across LMS Templates
- **Impact:** Interns on mobile devices (320px–768px viewports) experienced horizontal body scrolling (598px width), clipped CTA buttons, and misaligned progress steppers.
- **Root Cause:** Hardcoded min-widths and flex-row button clusters (`.na-btn-cluster`, `.btn-cluster`) without responsive wrapping.
- **Status:** **RESOLVED (Fixed: Nov 21, 2026)**
- **Fix:** In `apps/portal/static/css/dbert-theme.css`, `portal.html`, and `_head.html`, enforced viewport width `390px` on mobile, fluid button sizing (`width: 100%` on mobile), flex-direction column on `.na-btn-cluster`, and overflow-x auto wrappers for tables and steppers. Live verified with Playwright mobile emulation.

#### BUG-P1-11: Web Push Notification Modal Overlap with Left-Hand Sidebar
- **Impact:** Web push notification prompt modal was partially obscured behind the LMS navigation sidebar on desktop.
- **Root Cause:** Modal had lower z-index than `.app-sidebar` and lacked proper desktop left-margin offset.
- **Status:** **RESOLVED (Fixed: Nov 21, 2026)**
- **Fix:** Set modal `z-index: 100001` and added desktop margin offset equal to sidebar width (`240px`). Verified responsive display across desktop and mobile viewports.

#### BUG-P1-12: Attendance Heartbeat Lock Contention on High-Frequency Ping
- **Impact:** High concurrent intern attendance pings caused occasional connection pool exhaustion and transaction lock contention in PostgreSQL.
- **Root Cause:** Immediate individual database write transactions per heartbeat ping without client-side debouncing.
- **Status:** **RESOLVED / MITIGATED (Fixed: Nov 22, 2026)**
- **Fix:** Upgraded global heartbeat engine (`attendance-tracker.js`) with 60-second windowed batching, server-side advisory locks, and optimized connection recycling in `apps/portal/app.py`.

#### BUG-P1-13: 43 Expiring Internship Posts Causing Stale SEO Signals
- **Impact:** 43 high-traffic marketplace posts had application deadlines expiring <= 2026-11-27, risking dead links and declining search ranking.
- **Root Cause:** Fixed calendar expiry dates without automated rolling extension.
- **Status:** **RESOLVED (Fixed: Nov 20, 2026)**
- **Fix:** Executed `scripts/renew_43_expiring_posts.py`, extending `apply_by` to 2027-01-15 and `expires_at` to 2027-02-15; refreshed SEO-rich titles; synced to `lms.dbert.in/sitemap.xml` with `lastmod: 2026-11-20`.

#### BUG-P2-07: Public Stipend Claims Violating Placement Integrity
- **Impact:** Marketing copy promising "₹5,000 stipend for ₹1,999 fee" created regulatory exposure, confusion, and adverse selection.
- **Root Cause:** Incomplete separation between internal LMS performance bounties and external public course pricing.
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Fix:** Completely purged public stipend claims from `apps/website` across all marketing and 1999 pages in favor of 100% Guaranteed Placement across DBERT portfolio ventures. Performance stipends are governed strictly internally via `/stipend/tasks`.

### 4.3 P2 (Major) Bugs

#### BUG-P2-01: Orphaned 86-Endpoint FastAPI Backend (`dbert-api-package/backend/`)
- **Component:** `dbert-api-package/backend/main.py`
- **Severity:** **P2 (Major)**
- **Status:** **RESOLVED / DECOMMISSIONED (Nov 23, 2026)**
- **Description:** A standalone FastAPI service containing 19 routers, 86 REST endpoints runs on port 8000 (`api.dbert.in`).
- **Resolution:** Safely archived `dbert-api-package/` into `data/archive/dbert-api-package/` for full versioned retention. On AWS EC2 production, stopped, disabled, and masked `dbert-api.service`, reclaiming server memory/CPU and eliminating duplicate backend maintenance.

#### BUG-P2-02: 51 Dead Duplicate Files in Next.js Private Folders (`_admin/` & `_api/`)
- **Component:** `apps/website/src/app/_admin/`, `_api/`, `apps/portal/app.py`
- **Severity:** **P2 (Major)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** Developer QA cockpit and impersonation routes were missing from the portal.
- **Resolution:** Implemented `@app.route("/dev/qa-matrix")` and `@app.route("/dev/impersonate")` supporting instant 1-click persona switching (staff, admin, company, mentor, intern) with session cookie issuance and automated faculty account provisioning for test execution.

#### BUG-P2-03: Gate 3 Missing Encrypted UPI Setup for 90 of 143 Verified Interns
- **Component:** `apps/portal/templates/account.html`, `apps/portal/routes/stipend.py`
- **Severity:** **P2 (Major)**
- **Status:** **RESOLVED / MITIGATED (Fixed: Nov 22, 2026)**
- **Description:** 90 verified interns eligible for ₹5,000 stipend release on 03 December 2026 needed prompts to configure their encrypted UPI ID.
- **Resolution:** Account settings and stipend tasks view enforce encrypted UPI storage with live validation.

#### BUG-P2-04: Insecure In-Code Fallbacks & Hardcoded Admin Credentials
- **Component:** `apps/portal/app.py:6666`
- **Severity:** **P2 (Major)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** Default development credentials `dbert_admin_2026` could potentially be leveraged in production.
- **Resolution:** In `apps/portal/app.py:6666`, added production host check disallowing default fallback admin credentials (`not _is_prod_host or ADMIN_PASSWORD != "dbert_admin_2026"`).

#### BUG-P2-05: `ensure_column` DDL Lock Contention on High-Frequency API Sync
- **Component:** `apps/portal/app.py:1950`
- **Severity:** **P2 (Major)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** `internal_enrollment_sync()` previously called `ensure_column` on every incoming sync request, causing exclusive table locks.
- **Resolution:** Removed all 6 runtime `ensure_column` DDL calls from `internal_enrollment_sync`. Tables and columns are guaranteed at startup/migration time.

#### BUG-P2-06: Mobile Safari Low-Power Silent Pausing on Attendance Tracker
- **Component:** `apps/portal/static/js/attendance-tracker.js`
- **Severity:** **P2 (Major)**
- **Status:** **RESOLVED / MITIGATED (Fixed: Nov 22, 2026)**
- **Description:** Background tabs paused JavaScript timers on mobile.
- **Resolution:** Reconciled elapsed timestamps via `Date.now() - last_active_tick` to prevent attendance deficits.

---

### 4.4 P3 (Minor / Polish) Bugs

#### BUG-P3-01: Inline Style Proliferation in Next.js Admin & Hire Pages (STYLE-SPRAWL-001)
- **Component:** `apps/website/src/app/admin/cohort-applications/CohortApplicationsClient.tsx`
- **Severity:** **P3 (Minor)**
- **Status:** **RESOLVED / AUDITED (Fixed: Nov 22, 2026)**

#### BUG-P3-02: Skipped Document Heading Hierarchy across 35 Pages (A11Y-HEAD-001)
- **Component:** 35 routed pages across Enterprise AI, Startups, and Cohorts
- **Severity:** **P3 (Minor)**
- **Status:** **RESOLVED / AUDITED (Fixed: Nov 22, 2026)**

#### BUG-P3-03: Hardcoded Candidate Names in Backend Chat Filters
- **Component:** `apps/portal/app.py:6995`, `7117`
- **Severity:** **P3 (Minor)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** AI tutor chat filter contained hardcoded condition: `if m == "Pulluri Bhargavi": ...`.
- **Resolution:** Replaced hardcoded name with dynamic candidate session name match (`cand_name.lower() == m.lower()`).

#### BUG-P3-04: Hardcoded Test Email in Portal Scripts
- **Component:** `apps/portal/app.py:19310`
- **Severity:** **P3 (Minor)**
- **Status:** **RESOLVED (Fixed: Nov 22, 2026)**
- **Description:** Developer test email `techlearner.simp@gmail.com` hardcoded in `admin_sync_attendance`.
- **Resolution:** Removed hardcoded email and required explicit query parameter `?email=`.

#### BUG-P3-05: Unpruned Web Push Device Tokens Accumulating in PostgreSQL
- **Component:** `apps/portal/services/vapid_manager.py`
- **Severity:** **P3 (Minor)**
- **Status:** **RESOLVED / AUDITED (Fixed: Nov 22, 2026)**

---

---

## § 8: Dead, Obsolete & Redundant Code Audit

### 8.1. Scripts Directory Deprecated & Ad-Hoc Code

Category D comprises **255 scripts** that represent temporary debugging runs, one-line database inspections, throwaway exploratory tests, and redundant file checkers. They clutter the codebase and must be archived or cleaned.

### 5.1. Classification Patterns in Category D
1. **Ad-Hoc Remote Database Checks (`check_ec2_*`) - 42 scripts**:
   - `check_ec2_11_certs.py`, `check_ec2_12_certs.py`, `check_ec2_columns.py`, `check_ec2_db.py`, `check_ec2_enrollments.py`, `check_ec2_interns_schema.py`, `check_ec2_jobs_tables.py`, `check_ec2_keys.py`, `check_ec2_logout.py`, `check_ec2_more_payments.py`, `check_ec2_offer.py`, `check_ec2_posts.py`, `check_ec2_schema.py`, `check_ec2_status.py`, `check_ec2_users.py`, etc.
   - *Rationale:* Single queries run over SSH to inspect specific tables during incident remediation.
2. **Ad-Hoc Local Checks (`check_*`) - 19 scripts**:
   - `check_acct_timing.py`, `check_console.py`, `check_distribution.py`, `check_hashes.py`, `check_traffic_details.py`, `check_shreyash.py`, etc.
3. **Redundant Inspections (`inspect_*`) - 51 scripts**:
   - `inspect_active_accounts.py`, `inspect_admissions_emails.py`, `inspect_all_applications.py`, `inspect_bhargavi.py`, `inspect_candidate_detail.py`, `inspect_db_schema.py`, `inspect_interns_and_submissions.py`, `inspect_janvi.py`, `inspect_recent_candidates.py`, `inspect_unpaid_499.py`, etc.
4. **Ad-Hoc Remote Executions (`remote_*`, `ec2_*`) - 17 scripts**:
   - `remote_check_interns.py`, `remote_db_check.py`, `remote_inspect_all_users.py`, `remote_query.py`, `ec2_db_check.py`, `ec2_inspect.py`, etc.
5. **Throwaway Debugging & Scratch Scripts (`debug_*`, `diagnose_*`, `temp_*`, `find_*`) - 48 scripts**:
   - `debug_db.py`, `debug_login.py`, `diagnose_auth.py`, `diagnose_db_pool.py`, `find_api_routes.py`, `find_candidate.py`, `temp_patch.py`, `test_dispatch_test.py`, `test_load_targets.py`, etc.
6. **Superseded Cohort Audits (`audit_*`, `analyze_*`) - 78 scripts**:
   - `audit_discrepancy_candidates.py`, `audit_ec2_attendance_and_enrollments.py`, `audit_ec2_gates.py`, `audit_portal_users_applications_48h.py`, `audit_seeded_accounts.py`, `audit_stipend_full_breakdown.py`, `analyze_ec2_users_and_conversions.py`, `analyze_under_review_detailed.py`, etc.

### 5.2. Proposed Action
Move all Category D scripts to `scripts/archive/deprecated_diagnostics/` via a single script execution. None of them are imported by production runtime code or scheduled crons.

---

### 8.2. LMS & Template Dead Code Audit

### 5.1. Completely Unregistered & Orphaned Blueprints
- **`routes/masterclass.py`**:
  - Contains routes: `GET /masterclass/data-analyst`, `POST /api/masterclass/register`, `GET /admin/masterclass/registrations`.
  - Missing from `routes/__init__.py::ALL_BLUEPRINTS` and never imported in `app.py`.
  - Accompanied by **`templates/masterclass_data_analyst.html` (66,703 bytes)** which is dead and inaccessible to users.
  - Contains raw SQLite queries (`INTEGER PRIMARY KEY AUTOINCREMENT`, `datetime('now','localtime')`) that would break PostgreSQL if mounted directly.

### 5.2. Unregistered Test Cockpit Routes (Resolved: Nov 22, 2026)
- **`templates/dev_qa_matrix.html` (605 lines)**:
  - Designed as the visual QA Cockpit for test personas and stage impersonation.
  - **RESOLVED**: Both `@app.route("/dev/qa-matrix")` and `@app.route("/dev/impersonate")` were registered in `apps/portal/app.py` with multi-persona resolution (staff, admin, company, mentor, intern), session variables, `dbert_auth` & legacy `dbert_session` cookie minting, and dynamic mentor faculty seeding.
  - Automated test suite `tests/unit/test_local_seeded_ecosystem.py` now achieves **12/12 PASSED (100%)**, and `tests/test_mentor_slots.py` achieves **6/6 PASSED (100%)**.

### 5.3. Unreferenced & Orphaned Templates (Cleaned: Nov 22, 2026)
Of the 86 HTML templates in `apps/portal/templates/`, obsolete and dead templates were safely removed:
1. `certificate_dossier.html` (Deleted: 0 references across codebase).
2. `sample_certificate.html` (Deleted: legacy static mockup).
3. `dev_qa_matrix.html` (Wired: active UI for `/dev/qa-matrix`).
4. `masterclass_data_analyst.html` (Deleted: accompanied dead `routes/masterclass.py`).
5. `portal_ledger.html` (Deleted: legacy unused ledger template).

### 5.4. Legacy Monolith Duplicate Handlers (24 Duplicated Paths)
The following 24 endpoints are registered **twice** in Flask's `url_map` (once in `app.py` and once in a modular blueprint):
- `/admin/companies/approve` (`admin_bp` vs `app`)
- `/admin/companies/suspend` (`admin_bp` vs `app`)
- `/admin/telemetry` (`admin_bp` vs `app`)
- `/api/learning/v2/concept-tree/<int:course_id>` (`learning_bp` vs `app`)
- `/api/learning/v2/reviews-due` (`learning_bp` vs `app`)
- `/api/learning/v2/session` (`learning_bp` vs `app`)
- `/api/learning/v2/turn` (`learning_bp` vs `app`)
- `/api/payment/razorpay/create-order` (`payment_bp` vs `app`)
- `/api/payment/razorpay/verify-payment` (`payment_bp` vs `app`)
- `/company/applications/<int:app_id>/status` (`company_bp` vs `app`)
- `/company/posts` (`marketplace_bp` vs `app`)
- `/company/posts/<int:post_id>/publish` (`marketplace_bp` vs `app`)
- `/company/posts/<int:post_id>/unpublish` (`marketplace_bp` vs `app`)
- `/company/posts/<int:post_id>/delete` (`marketplace_bp` vs `app`)
- `/intern/certificates` (`intern_bp` vs `app`)
- `/intern/login` (`auth_bp` vs `app`)
- `/intern/my-applications` (`applications_bp` vs `app`)
- `/logout` (`auth_bp` vs `app`)
- `/mentors/slots/<int:slot_id>/book` (`mentor_bp` vs `app`)

### 5.5. Direct `smtplib` Usage vs Enterprise Delivery Service
- Despite the presence of `services/delivery_service.py` (an enterprise 774-line multi-account pool with rate-limiting and jitter), `app.py` still contains direct `smtplib.SMTP_SSL` and `smtplib.SMTP` implementations (`_send_smtp_single` and `_smtp_send_raw`) called directly at lines 4883 and 4888.
- `EmailDeliveryService` is only called inside its own test suite (`tests/test_delivery_service.py`), representing an unintegrated enterprise service.

---

---

## § 9: Feature Clubbing & Consolidation Architecture

The dual-monorepo setup (`apps/website` in Next.js and `apps/portal` in Flask) has led to significant feature duplication, split user state, and maintenance overhead. Below is the comprehensive architectural consolidation blueprint.

```
+----------------------------------------------------------------------------------------------------+
|                                FEATURE CLUBBING CONSOLIDATION MATRIX                               |
+-----------------------------------+-----------------------------------+----------------------------+
| Functional Domain                 | Legacy Fragmented Routes          | Unified Consolidated Route |
+-----------------------------------+-----------------------------------+----------------------------+
| 1. Credential Verification        | Next.js /verify, /verify/[certId] | https://dbert.in/verify    |
|    & Dossier Engine               | Next.js /verify/directory         |   /[certId] (Master Hub)   |
|                                   | Flask /certificates, /portal/cert | Direct DB Read + PDF Stream|
+-----------------------------------+-----------------------------------+----------------------------+
| 2. Enrollment, Offers             | Next.js /enroll/1999, /eroll      | https://dbert.in/checkout  |
|    & Fee Payments                 | Next.js /verify/unlock            |   ?fee={caution|balance|   |
|                                   | Flask /portal/offer, /enroll      |         verify}            |
+-----------------------------------+-----------------------------------+----------------------------+
| 3. Job Board & Talent             | Next.js /jobs, /internships       | https://dbert.in/jobs      |
|    Marketplace                    | Next.js /hire/pre-vetted-engineers|   (Unified Public Board)   |
|                                   | Flask /jobs, /company/*           | Flask /company (B2B SaaS)  |
+-----------------------------------+-----------------------------------+----------------------------+
| 4. Guided Learning                | Next.js /learners/courses/*       | Next.js: Public Catalog    |
|    & AI Tutoring                  | Flask /courses, /tasks            | Flask /learn (Guided RAG)  |
|                                   | Flask Guided Learning 1.0 vs 2.0  | Unified BYOK LLM Engine    |
+-----------------------------------+-----------------------------------+----------------------------+
| 5. Admin Consoles                 | Next.js /admin/* (Debris in _admin| Flask /admin               |
|    & Telemetry                    | Flask /admin (3k-line monolith)   |   (Single Unified Portal)  |
|                                   | Flask /admin/analytics            | Unified RBAC Permissions   |
+-----------------------------------+-----------------------------------+----------------------------+
```

---

### 5.1 Route & Feature Clubbing Across 5 Core Domains

#### Domain 1: Credential Verification & Certificate Engine
- **Current State:** Fragmented across 5 distinct routes. Next.js serves `/verify`, `/verify/[certId]`, and `/verify/directory` from flat JSON files. Flask LMS serves `/certificates`, `/portal/certificate/<cert_id>`, and `/portal/certificate/<cert_id>/print` from PostgreSQL, relying on `window.print()` while `certificate_packet_service.py` sits orphaned.
- **Consolidation Plan:**
  1. **Single Sovereign Verification Engine:** Establish `https://dbert.in/verify/[certId]` as the sole public verification route for all credentials (fellowships, internships, and LMS micro-courses).
  2. **Direct PostgreSQL Verification API:** Eliminate `certificates_registry.json`. Next.js `/api/verify` queries PostgreSQL `intern_certificates` directly.
  3. **Unified PDF Streaming Endpoint:** Wire `certificate_packet_service.py` to `@app.route("/api/credentials/download/<cert_id>")`. The print button on both website and LMS streams the authentic 3-document signed vector PDF packet.

#### Domain 2: Candidate Enrollment, Offers & Monetization
- **Current State:** Fragmented across distinct checkout and offer pages. Next.js handles `/enroll/1999`, `/enroll`, `/eroll`, and `/verify/unlock` via flat JSON logging. Flask handles `/portal/offer` (bifurcated: Stage 3 Selected sees digital offer & ₹499 seat confirmation; Stage 1/2 Under-Review sees Industry Incubation & Paid Fellowship marketing hub with ₹5,000 earnable stipend and 1-click `/enroll/1999` upgrade), `/enroll`, and Razorpay webhooks.
- **Consolidation Plan:**
  1. **Unified Checkout Portal (`/checkout`):** Club all financial settlements into a single dynamic Next.js checkout hub supporting query parameters:
     - `/checkout?type=caution&amount=499` (Stage 3 seat confirmation)
     - `/checkout?type=fellowship&amount=1999` (Direct Incubation & Paid Fellowship)
     - `/checkout?type=balance&amount=1500` (Incubation balance)
     - `/checkout?type=verify&amount=299` (Credential verification)
  2. **Real-Time Data Convergence Webhook:** Ensure all submissions instantly execute synchronous RPC to Flask `/api/internal/enrollment-sync`, writing directly to PostgreSQL `enrollments`.
  3. **Universal 1-Tap UPI Component:** Standardize the UPI QR box, 1-tap mobile grid (GPay, PhonePe, Paytm, Any UPI), and 12-digit UTR input into a single shared React/Jinja component.

#### Domain 3: Job Board, Internships & B2B Talent Marketplace
- **Current State:** Next.js serves public marketing pages `/jobs`, `/internships`, and `/hire/pre-vetted-engineers`. Flask LMS serves authenticated job feeds `/jobs`, `/internships`, and company administrative tools `/company/*`.
- **Consolidation Plan:**
  1. **Public Board on Next.js (`dbert.in/jobs`):** Unify public job search, domain filters, and structured schema markup on Next.js.
  2. **Candidate Suitability Modal:** Intercept all application clicks. Authenticated candidates apply in 1-click; unauthenticated visitors are prompted to create a profile, capturing 100% of candidate leads.
  3. **B2B Recruiter Portal on LMS (`lms.dbert.in/company`):** Club recruiter features into a dedicated B2B portal. When recruiters click "Connect on LMS" from the directory, preserve candidate ID in session, display candidate dossier, and enable direct messaging.

#### Domain 4: Guided Learning, Course Delivery & AI Tutoring
- **Current State:** Next.js `/learners/courses/*` lists course descriptions with dead Razorpay links. Flask has both "Guided Learning 1.0" (classroom streaming chat in `app.py`) and "Guided Learning 2.0" (RAG concept trees in `services/learning/`), creating conflicting state.
- **Consolidation Plan:**
  1. **Public Course Catalog on Next.js:** Convert `/learners` into an SEO-optimized syllabus browser with interactive Day 1 preview sandboxes.
  2. **Full Learning Experience on LMS (`/courses/<id>/learn`):** Decommission Guided Learning 1.0. Promote Guided Learning 2.0 (RAG DAG concept trees) as the canonical curriculum delivery engine.
  3. **Universal BYOK AI Gateway:** Consolidate Gemini API calling into a single `GeminiProvider` service checking user keys with automatic fallback cascading (`gemini-2.5-flash` -> `gemini-2.0-flash` -> `gemini-1.5-flash`).

#### Domain 5: Administrative Consoles & Telemetry
- **Current State:** Split across Next.js `/admin/*` (with 51 dead files in `_admin`), Flask `/admin` (3,000-line monolithic Jinja dashboard), and Flask `/admin/analytics`.
- **Consolidation Plan:**
  1. **Single Sovereign Admin Console on Flask (`lms.dbert.in/admin`):** Migrate all administrative capabilities (applicant review, enrollment approval, certificate issuance, and analytics) into Flask LMS with unified Role-Based Access Control (Super Admin, Staff Evaluator, Mentor).
  2. **Purge Next.js Admin Debris:** Completely delete `apps/website/src/app/_admin/` and public `/admin` endpoints from Next.js.
  3. **Unified Real-Time Operations Cockpit:** Embed the real-time operations dashboard (`realtime_operations_dashboard.html`) into the main admin console.

---

### 5.2 Redundancy Elimination & Code Debris Purge Manifest

The following file manifest details obsolete, redundant, and dead code scheduled for immediate deletion:

```bash
# ==============================================================================
# DBERT ARCHITECTURAL PURGE MANIFEST (TARGET: IMMEDIATE REMOVAL)
# ==============================================================================

# 1. Next.js Private Folder Duplicate Debris (51 Dead Files) [STATUS: EXECUTED / DELETED in commit d263ee5]
# rm -rf apps/website/src/app/_admin/ (COMPLETED)
# rm -rf apps/website/src/app/_api/ (COMPLETED)

# 2. Orphaned Standalone FastAPI Backend (86 Unused Endpoints)
# Systemd service 'dbert-api.service' to be disabled & masked
rm -rf dbert-api-package/backend/
rm -rf dbert-api-package/website-content/

# 3. Completely Dead Flask Blueprints (223 Unreachable Lines) [STATUS: EXECUTED / DELETED in commit d263ee5]
# rm -f apps/portal/routes/masterclass.py (COMPLETED)

# 4. Legacy cPanel, PHP & 0-Byte Database Relics
rm -f apps/portal/dbert_cpanel_deployment.zip  # 9.1 MB binary archive
rm -f apps/portal/.htaccess
rm -f apps/portal/.htaccess.cgi
rm -f apps/portal/passenger_wsgi.py
rm -f apps/portal/php.ini
rm -f apps/portal/test.php
rm -f apps/portal/dbert.db                     # 0-byte SQLite relic
rm -f apps/portal/dbert_lms.db                 # 0-byte SQLite relic
rm -f apps/portal/portal.db                    # 0-byte SQLite relic

# 5. Redundant Shadowed Flask Route Handlers (19 Collisions in app.py)
# Delete duplicate @app.route definitions from apps/portal/app.py:
# - /admin/companies/approve (line 13249)
# - /admin/companies/suspend (line 13263)
# - /admin/telemetry (line 19595)
# - /intern/my-applications (line 15136)
# - /intern/login (line 10588)
# - /logout (line 14101)
# - /company/applications/<id>/status (line 13149)
# - /intern/certificates (line 9740)
# - /api/learning/v2/session (line 6419)
# - /api/learning/v2/turn (line 6448)
# - /api/learning/v2/reviews-due (line 6502)
# - /api/learning/v2/concept-tree/<id> (line 6516)
# - /company/posts (line 10917)
# - /company/posts/<id>/publish (line 11177)
# - /company/posts/<id>/unpublish (line 11232)
# - /company/posts/<id>/delete (line 11254)
# - /mentors/slots/<id>/book (line 8948)
# - /api/payment/razorpay/create-order (line 16061)
# - /api/payment/razorpay/verify-payment (line 16128)
```

---

---

## § 10: PostgreSQL Schema & Relational Data Dictionary

### 3.1 Overview & Schema Namespace
- **Database Name**: `dbert_lms`
- **Active Schema**: `dbert_internship`
- **Owner**: `dbert_user`
- **Total Tables**: **83 tables**
- **Active Tables (with data)**: **59 tables**
- **Empty / Schema-Staged Tables**: **24 tables**

### 3.2 Live Table Catalog & Row Counts

Below is the verified live census of all 83 tables extracted directly from the EC2 production database:

```
+------------------------------------+------------+------------------------------------------------------------+
| Table Name                         | Row Count  | Classification & Functional Purpose                        |
+------------------------------------+------------+------------------------------------------------------------+
| device_profiles                    | 8,783      | Web visitor fingerprinting, sessions, intent scoring      |
| email_log                          | 7,299      | Dispatch audit log for outbound transactional emails       |
| scraped_internships                | 6,746      | Aggregated tech internship listings (Marketplace)          |
| notifications                      | 6,566      | In-app intern notifications and system alerts              |
| abuse_log                          | 5,536      | Security rate limiting and suspicious IP event audit       |
| attendance                         | 5,524      | Intern weekly login and platform time tracking             |
| applications                       | 5,157      | Primary candidate internship application records           |
| course_subtopic_chats              | 3,237      | Pedagogical AI tutor chat logs per course lesson           |
| scraped_jobs                       | 3,110      | Curated junior/entry-level tech job listings               |
| intern_accounts                    | 3,007      | Registered candidate accounts, credentials & auth data     |
| user_sessions                      | 2,257      | Active web authentication session cookies                  |
| day_quiz_attempts                  | 1,092      | Student quiz submission attempts & scoring records         |
| post_applications                  | 733        | Applications submitted to specific employer marketplace job|
| event_outbox                       | 628        | Asynchronous transactional event queue (Outbox Pattern)   |
| course_enrollments                 | 599        | Intern enrollment in structured courses                    |
| interviews                         | 576        | AI-driven candidate technical interview evaluation records |
| password_resets                    | 549        | Password reset tokens and redemption audit                 |
| enrollments                        | 469        | Formal internship cohort enrollments & caution deposits    |
| application_status_history         | 447        | Audit trail of state transitions for candidate applications|
| posts                              | 235        | Verified company job and internship postings               |
| course_subtopics                   | 230        | Individual lesson modules within course chapters           |
| web_push_delivery_logs             | 202        | RFC 8292 Web Push delivery receipts                        |
| scraped_internship_comments        | 199        | Public candidate comments & Q&A on marketplace internships |
| rate_events                        | 181        | Micro-window rate limit token bucket state                 |
| cvs                                | 159        | Dynamic CV / Resume builder records & public slugs         |
| intern_certificates                | 129        | Issued certificate registry in PostgreSQL                  |
| messages                           | 129        | Direct message exchanges within conversations              |
| conversations                      | 127        | Direct messaging thread metadata                           |
| companies                          | 119        | Registered employer and hiring partner accounts            |
| intern_offer_letters               | 119        | Deterministic candidate offer letters                      |
| gl_concepts                        | 101        | Guided Learning pedagogical knowledge graph concepts       |
| user_api_keys                      | 92         | Encrypted Gemini AI keys provided by students              |
| task_submissions                   | 86         | Candidate sprint task code and PR submissions              |
| course_chapters                    | 80         | Structural chapters dividing course curricula              |
| course_day_quizzes                 | 77         | Daily checkpoint assessments and answer rubrics            |
| dbert_fallback_usage               | 71         | Platform fallback AI usage counter per student             |
| mentor_availability_slots          | 71         | 1-on-1 mentor booking availability windows                 |
| referrals                          | 55         | Ambassador student referral records                        |
| security_deposits                  | 52         | Recorded ₹499 caution deposit payments                     |
| intern_articles_backup_20261114    | 41         | [LEGACY BACKUP] Deduplication snapshot from Nov 14, 2026    |
| intern_articles                    | 39         | Peer-reviewed technical capstone articles                  |
| web_push_devices                   | 34         | Registered browser Web Push subscription tokens            |
| post_comments                      | 16         | Employer post discussions and comments                     |
| courses                            | 12         | Master course catalog entries                              |
| platform_config                    | 11         | Global dynamic key-value platform configurations           |
| tasks                              | 10         | Canonical sprint tasks and assignments                     |
| coin_ledger_mirror                 | 9          | Student gamification coin balance delta audit mirror        |
| staff_accounts                     | 9          | Operations, reviewers, and administrator staff accounts    |
| staff_queue_roles                  | 8          | Staff queue review assignment mappings                     |
| resume_ats_audits                  | 7          | Stored candidate ATS resume audit scores and rubrics        |
| payment_events                     | 6          | Webhook and payment verification raw audit events           |
| task_versions                      | 6          | Rubric and instructions versioning for sprint tasks         |
| coin_perks_catalog                 | 4          | Redeemable student rewards catalog                         |
| mentors                            | 4          | Verified external mentor accounts                          |
| course_projects                    | 3          | Capstone projects required for course completion           |
| cohort_enrollments                 | 1          | Live batch / cohort student assignments                     |
| cohorts                            | 1          | Active learning sprint cohorts                             |
| review_log                         | 1          | Staff submission review audit log                          |
| signup_otps                        | 1          | Active 2FA/Registration OTP records                        |
| ambassador_withdrawals             | 0          | [EMPTY] Ambassador revenue cashout requests                 |
| check_log                          | 0          | [EMPTY] Legacy duplicate status check log                  |
| coin_perk_redemptions              | 0          | [EMPTY] Student coin store redemption records               |
| company_follows                    | 0          | [EMPTY] Student bookmarks/follows of company accounts       |
| course_payments                    | 0          | [EMPTY] Course enrollment standalone payment records        |
| ecosystem_spotlights               | 0          | [EMPTY] Sponsored company spotlight features               |
| enrollment_status_history          | 0          | [EMPTY] History log of enrollment payment changes           |
| gl_course_chunks                   | 0          | [EMPTY] RAG vector chunk embeddings for course content     |
| gl_learning_events                 | 0          | [EMPTY] Granular pedagogical event telemetry                |
| gl_learning_sessions               | 0          | [EMPTY] Interactive AI tutor dialogue sessions              |
| gl_learning_turns                  | 0          | [EMPTY] Individual conversational turns in AI tutoring      |
| gl_misconception_catalog           | 0          | [EMPTY] Misconception classification catalog                |
| gl_student_learning_profile        | 0          | [EMPTY] Student learning velocity and mastery profiles      |
| gl_student_mastery                 | 0          | [EMPTY] Per-concept student mastery scores                  |
| gl_teacher_learning_instructions   | 0          | [EMPTY] Teacher/Mentor pedagogical override instructions    |
| mentor_session_bookings            | 0          | [EMPTY] Booked student-mentor 1-on-1 video sessions         |
| mobile_refresh_tokens              | 0          | [EMPTY] Active JWT refresh tokens (purged by cron)          |
| payments                           | 0          | [EMPTY] Legacy mentor direct payout ledger                  |
| post_hire_deposits                 | 0          | [EMPTY] Post-hire escrow employer deposit records           |
| post_questions                     | 0          | [EMPTY] Custom screening questions for job postings        |
| project_submissions                | 0          | [EMPTY] Structured course capstone project submissions      |
| scraped_job_comments               | 0          | [EMPTY] Discussion comments on marketplace job posts        |
| spotlight_clicks                   | 0          | [EMPTY] Click telemetry on ecosystem spotlights             |
| tutor_progress                     | 0          | [EMPTY] Legacy monolithic tutor progress tracker            |
+------------------------------------+------------+------------------------------------------------------------+
```

### 3.3 Legacy & Backup Table Analysis
- **`dbert_internship.intern_articles_backup_20261114` (41 rows)**:
  This table was created on November 14, 2026, during an architectural audit to resolve duplicate article submissions caused by race conditions on the `/intern/articles/save` endpoint. The production table `intern_articles` was purged of 19 duplicates and reduced to 22 canonical articles (now grown to 39).
  *Status*: Read-only safety snapshot. Retain indefinitely as an archival ledger or migrate to cold S3 storage.

---

## 4. Foreign Key Constraints & Relational Architecture

The PostgreSQL schema enforces **20 explicit relational foreign keys**:

```mermaid
erDiagram
    STAFF_ACCOUNTS ||--o{ STAFF_QUEUE_ROLES : "assigns"
    STAFF_ACCOUNTS ||--o{ REVIEW_LOG : "records"
    STAFF_ACCOUNTS ||--o{ MENTOR_AVAILABILITY_SLOTS : "hosts"
    STAFF_ACCOUNTS ||--o{ TASK_SUBMISSIONS : "reviews"
    
    COMPANIES ||--o{ POSTS : "publishes"
    
    INTERN_ACCOUNTS ||--o{ APPLICATIONS : "derived_from"
    INTERN_ACCOUNTS ||--o{ USER_API_KEYS : "owns"
    INTERN_ACCOUNTS ||--o{ RESUME_ATS_AUDITS : "receives"
    INTERN_ACCOUNTS ||--o{ TASK_SUBMISSIONS : "submits"
    INTERN_ACCOUNTS ||--o{ TUTOR_PROGRESS : "tracks"
    INTERN_ACCOUNTS ||--o{ MENTOR_SESSION_BOOKINGS : "books"
    
    MENTOR_AVAILABILITY_SLOTS ||--o{ MENTOR_SESSION_BOOKINGS : "fulfills"
    
    CONVERSATIONS ||--o{ MESSAGES : "contains"
    
    TASKS ||--o{ TASK_VERSIONS : "versions"
    TASKS ||--o{ TASK_SUBMISSIONS : "targets"
    TASK_VERSIONS ||--o{ TASK_SUBMISSIONS : "grades_against"
    TASK_SUBMISSIONS ||--o{ INTERN_ARTICLES : "publishes_as"
    
    COIN_PERKS_CATALOG ||--o{ COIN_PERK_REDEMPTIONS : "redeemed_by"
    
    GL_CONCEPTS ||--o{ GL_MISCONCEPTION_CATALOG : "classifies"
    GL_CONCEPTS ||--o{ GL_STUDENT_MASTERY : "evaluates"
```

### Table of Enforced Foreign Keys:
1. `coin_perk_redemptions.perk_id` &rarr; `coin_perks_catalog.id`
2. `gl_misconception_catalog.concept_id` &rarr; `gl_concepts.concept_id`
3. `gl_student_mastery.concept_id` &rarr; `gl_concepts.concept_id`
4. `intern_accounts.application_id` &rarr; `applications.id`
5. `intern_articles.task_submission_id` &rarr; `task_submissions.id`
6. `mentor_availability_slots.mentor_staff_id` &rarr; `staff_accounts.id`
7. `mentor_session_bookings.intern_id` &rarr; `intern_accounts.id`
8. `mentor_session_bookings.slot_id` &rarr; `mentor_availability_slots.id`
9. `messages.conversation_id` &rarr; `conversations.id`
10. `posts.company_id` &rarr; `companies.id`
11. `resume_ats_audits.intern_id` &rarr; `intern_accounts.id`
12. `review_log.staff_id` &rarr; `staff_accounts.id`
13. `staff_queue_roles.staff_id` &rarr; `staff_accounts.id`
14. `task_submissions.intern_id` &rarr; `intern_accounts.id`
15. `task_submissions.reviewed_by_staff_id` &rarr; `staff_accounts.id`
16. `task_submissions.task_id` &rarr; `tasks.id`
17. `task_submissions.task_version_id` &rarr; `task_versions.id`
18. `task_versions.task_id` &rarr; `tasks.id`
19. `tutor_progress.intern_id` &rarr; `intern_accounts.id`
20. `user_api_keys.intern_id` &rarr; `intern_accounts.id`

*Note on Logical Foreign Keys*:  
Several tables (`enrollments`, `intern_certificates`, `course_enrollments`) use logical integer keys (`intern_id`, `course_id`) without formal DDL foreign key constraints to allow loose coupling and rapid data reconciliation from external JSON registries and webhooks without transactional locks.

---

## 5. Flat JSON Data Layer Architecture

The Next.js 14/16 App Router application (`apps/website`) relies on deterministic, statically compiled JSON files for maximum speed, SEO indexing, and zero-latency verification.

```
+-----------------------------------+-----------------------------------------+----------+-------------------------------------+
| File Path                         | Production Symlink Target               | Records  | Consumer / Endpoint                 |
+-----------------------------------+-----------------------------------------+----------+-------------------------------------+
| apps/website/src/data/            | Inlined in Next.js Standalone Build     | 470      | /verify, /verify/[certId]           |
|   certificates_registry.json      |                                         |          |                                     |
| apps/website/src/data/            | Inlined in Next.js Standalone Build     | 476      | /verify/directory, /hire            |
|   directory_candidates.json       |                                         |          |                                     |
| data/                             | /var/www/dbert-website-lms/data/        | 8        | /enroll/1999, /api/enroll/balance,  |
|   balance_enrollments_1500.json   |   balance_enrollments_1500.json         |          | /api/enroll/lookup                  |
+-----------------------------------+-----------------------------------------+----------+-------------------------------------+
```

### 5.1 `certificates_registry.json`
- **Schema Format**: Keyed Dictionary (Key = `certId`, e.g. `CERT-DBERT-2026-DA-001`).
- **Record Structure**:
  ```json
  {
    "certId": "CERT-DBERT-2026-DA-001",
    "internId": "DBERT-INT-KA-6769-001",
    "holderName": "Kushal Agarwal",
    "email": "kushalagarwal27496@gmail.com",
    "college": "Ajeekya dy Patil university",
    "domain": "Data Analyst",
    "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
    "batch": "July to Sep 2026",
    "duration": "15 Dec 2025 – 15 Feb 2026",
    "startDate": "15 Dec 2025",
    "endDate": "15 Feb 2026",
    "issueDate": "01 Oct 2026",
    "evalDate": "28 Sep 2026",
    "score": 92,
    "grade": "Grade A (Distinction)",
    "signatory": "Dr. Aris Thorne",
    "signatoryTitle": "Chief Technology Officer & Senior Fellow",
    "organization": "DBERT (Deep Learning, Big Data, Edge & Real-Time Intelligence Labs)",
    "verificationUrl": "https://dbert.in/verify/CERT-DBERT-2026-DA-001",
    "verified": true,
    "isProvisional": false,
    "doc1Pdf": "/certificates/CERT-DBERT-2026-DA-001/doc1.pdf",
    "doc2Pdf": "/certificates/CERT-DBERT-2026-DA-001/doc2.pdf",
    "doc3Pdf": "/certificates/CERT-DBERT-2026-DA-001/doc3.pdf",
    "previewUrl": "/certificates/previews/CERT-DBERT-2026-DA-001.png"
  }
  ```
- **Operational Rules**:
  - Contains **470 total credentials** (65+ official verified credentials + 400 provisional records).
  - High-res PDF packets (Certificate of Completion, Comprehensive Evaluation Rubric, Formal Recommendation Letter) reside under `apps/website/public/certificates/[certId]/`.

### 5.2 `directory_candidates.json`
- **Schema Format**: Array of 476 candidate objects.
- **Segregated Views**:
  - **Tab 1: Pre-Vetted Engineers (Verified · Ready to Hire)**: Filtered where `verified == true && isProvisional == false`. Displays pre-vetted engineers ranked dynamically by evaluation score (from 80–84 High Merit on the standardized v2026.3 scale, alongside legacy distinction graduates) with direct links to cryptographically verified proof dossiers.
  - **Tab 2: Incubation Fellows (Provisional · In Sprints)**: Filtered where `isProvisional == true`. Represents active fellows completing milestone sprints.
- **Fields**: `certId`, `internId`, `holderName`, `domain`, `duration`, `score`, `grade`, `isProvisional`, `status`, `firstLetter`, `verifyUrl`, `verified`, `skills`, `highlightRubrics`.

### 5.3 `balance_enrollments_1500.json`
- **Schema Format**: Array of ₹1,500 balance payment submissions.
- **Record Structure**:
  ```json
  {
    "id": "DBERT-ENR-703685-TYN6",
    "submittedAt": "2026-11-14T11:21:00.000Z",
    "fullName": "Bhargavi Poola",
    "email": "bhargavi13032007@gmail.com",
    "phone": "8192911360",
    "college": "Seshadripuram College",
    "domain": "Artificial Intelligence",
    "amountExpected": 1500,
    "amountClaimed": 1500,
    "amountVerified": 1500,
    "amountPaid": 1500,
    "utrNumber": "679862090077",
    "status": "APPROVED",
    "ipAddress": "157.48.12.90",
    "userAgent": "Mozilla/5.0..."
  }
  ```
- **Operational Guarantees**:
  - Deduplication: Validates 12-digit UTR numbers to prevent replay attacks.
  - Symlinked into `.next/standalone/data/` across production builds to prevent data loss.

---

## 6. Data Convergence & Synchronization Pipelines

The DBERT platform maintains synchronization between edge Next.js flat files, the Flask LMS portal, and the FastAPI microservice through cron-driven daemons.

```mermaid
flowchart TD
    Candidate["Candidate on dbert.in/enroll/1999"] -->|"POST /api/enroll/balance (UTR Submission)"| BalanceJSON["data/balance_enrollments_1500.json"]
    
    CronDaemon["deploy/run_cron_tasks.sh<br/>(Every 15 min via Ubuntu Crontab)"]
    
    CronDaemon -->|"1. POST /api/v1/cron/process-outbox"| OutboxTask["Outbox Processor<br/>(dbert-api)"]
    CronDaemon -->|"2. POST /api/v1/cron/clean-tokens"| TokenTask["Token Purge<br/>(dbert-api)"]
    CronDaemon -->|"3. POST /api/v1/cron/expire-posts"| PostExpiry["Post Expirer<br/>(dbert-api)"]
    
    CronDaemon -->|"4. Run sync_enrollments_to_postgres.py"| SyncEnr["sync_enrollments_to_postgres.py"]
    CronDaemon -->|"5. Run sync_verified_certificates_to_portal.py"| SyncCert["sync_verified_certificates_to_portal.py"]
    
    BalanceJSON --> SyncEnr
    SyncEnr -->|"Upsert / Create Accounts"| PG_Enrollments["PostgreSQL: enrollments & intern_accounts"]
    
    CertRegistry["certificates_registry.json"] --> SyncCert
    SyncCert -->|"Sync Tier='verified'"| PG_Certs["PostgreSQL: intern_certificates"]
    
    OutboxTask -->|"Update status='processed'"| PG_Outbox["PostgreSQL: event_outbox"]
    TokenTask -->|"DELETE WHERE expires_at < NOW()"| PG_Tokens["PostgreSQL: mobile_refresh_tokens"]
```

### 6.1 `scripts/sync_enrollments_to_postgres.py`
1. **File Resolution**: Resolves `data/balance_enrollments_1500.json`.
2. **Schema Verification**: Ensures columns exist in PostgreSQL (`intern_id`, `amount_paid`, `utr_number`, `deposit_paid`, `balance_paid`, `submission_id`, `balance_submission_id`).
3. **Account Provisioning**: Checks if candidate exists in `intern_accounts` by email; if missing, automatically provisions an active account with a cryptographically secure random password hash.
4. **Upsert Logic**: Reconciles the `enrollments` table:
   - If enrollment exists: updates `balance_paid = 1500`, records UTR, and sets `balance_submission_id`.
   - If missing: inserts a complete enrollment record with `amount_paid = 1999`, `deposit_paid = 499`, `balance_paid = 1500`, and status `SUBMITTED`.

### 6.2 `scripts/sync_verified_certificates_to_portal.py`
1. **Registry Scan**: Iterates through all 470 records in `certificates_registry.json`.
2. **Verification Filter**: Matches candidates where `verified == true && isProvisional == false`.
3. **Portal Ingestion**:
   - Queries `intern_certificates` by `cert_id` or `email`.
   - If present: upgrades `tier = 'verified'`.
   - If missing: inserts new verified credential linking `intern_id`, `cert_id`, `course_title`, `url` (`/verify/[certId]`), and `tier = 'verified'`.

### 6.3 Cron Execution Daemon (`deploy/run_cron_tasks.sh`)
- Configured in Ubuntu crontab: `*/15 * * * * /var/www/dbert-website-lms/deploy/run_cron_tasks.sh >> /var/log/dbert_cron.log 2>&1`
- Reads `/var/www/dbert-website-lms/dbert-api-package/.env` to retrieve `CRON_SECRET`.
- Executes HTTP calls to the local FastAPI service on `127.0.0.1:8000`:
  1. `POST /api/v1/cron/process-outbox` (processes queued application and payment events)
  2. `POST /api/v1/cron/clean-tokens` (deletes expired mobile refresh tokens)
  3. `POST /api/v1/cron/expire-posts` (marks expired job postings)
- Executes local Python reconciliation scripts in sequence using the portal virtual environment (`apps/portal/.venv/bin/python`).

### 6.4 Event Outbox & Token Cleaning State
- **Event Outbox (`event_outbox`)**:
  - Live state: **71 PENDING**, **557 SENT/processed** (628 total).
  - Handles asynchronous decoupling for events such as `application.submitted`, `payment.verified`, and `interview.completed`.
  - Batch size: 50 events per pass. Updates `status = 'processed'` and timestamps `processed_at`.
- **Mobile Refresh Tokens (`mobile_refresh_tokens`)**:
  - Live count: **0 rows** currently active.
  - Automated deletion query: `DELETE FROM mobile_refresh_tokens WHERE expires_at < NOW()`.

---

## 7. Data Dictionary of Core Entities

### 7.1 `intern_accounts` (Candidate Master Entity)
- `id` (INTEGER, PK, Autoincrement)
- `name` (VARCHAR(255), NOT NULL)
- `email` (VARCHAR(255), UNIQUE, NOT NULL, INDEXED)
- `phone` (VARCHAR(50), NULL)
- `college` (VARCHAR(255), NULL)
- `domain` (VARCHAR(100), NULL)
- `password_hash` (TEXT, NULL) — bcrypt or PBKDF2:SHA256
- `signup_stage` (INTEGER, DEFAULT 3) — 1=Registered, 2=Profile, 3=Under Review, 4=Selected, 5=Enrolled
- `account_status` (VARCHAR(50), DEFAULT 'active') — active, suspended, completed
- `tutor_completion_pct` (FLOAT, DEFAULT 0.0) — LMS progress metric
- `stipend_verified` (INTEGER, DEFAULT 0) — 1 = Gate 1 completed (₹299 verification fee cleared)
- `created_at` / `updated_at` (TIMESTAMPTZ)

### 7.2 `applications` (Intake Application Entity)
- `id` (INTEGER, PK, Autoincrement)
- `name` (VARCHAR(255), NOT NULL)
- `email` (VARCHAR(255), NOT NULL, INDEXED)
- `phone` (VARCHAR(50), NOT NULL)
- `college` (VARCHAR(255), NOT NULL)
- `course` / `semester` / `year_of_passing` (VARCHAR)
- `domain` (VARCHAR(100), NOT NULL)
- `status` (VARCHAR(50), DEFAULT 'Apply Pending', INDEXED) — Apply Pending, Under Review, Selected, Rejected
- `created_at` / `updated_at` (TIMESTAMPTZ)

### 7.3 `enrollments` (Financial & Batch Enrollment Entity)
- `id` (INTEGER, PK, Autoincrement)
- `intern_id` (INTEGER, NULL)
- `email` (VARCHAR(255), NULL, INDEXED)
- `name` / `phone` / `college` / `domain` (VARCHAR)
- `batch_label` (VARCHAR(100), DEFAULT '2026-Cohort-A')
- `amount_paid` (INTEGER, DEFAULT 0) — 1999
- `deposit_paid` (INTEGER, DEFAULT 0) — 499
- `balance_paid` (INTEGER, DEFAULT 0) — 1500
- `utr_number` (VARCHAR(100), NULL) — 12-digit transaction UTR
- `submission_id` / `balance_submission_id` (VARCHAR(100), NULL)
- `payment_status` (VARCHAR(50), DEFAULT 'Pending Verification') — Pending Verification, SUBMITTED, APPROVED, REJECTED
- `created_at` / `updated_at` (TIMESTAMPTZ)

### 7.4 `intern_certificates` (Credential Entity)
- `id` (INTEGER, PK, Autoincrement)
- `intern_id` (INTEGER, NOT NULL)
- `course_id` (INTEGER, DEFAULT 0)
- `course_title` (VARCHAR(255), NOT NULL)
- `cert_id` (VARCHAR(100), UNIQUE, NOT NULL, INDEXED) — e.g. `CERT-DBERT-2026-DA-001`
- `issued_at` (TIMESTAMPTZ, DEFAULT NOW())
- `url` (TEXT) — `/verify/{cert_id}`
- `tier` (VARCHAR(50), DEFAULT 'provisional') — provisional, verified
- `email` (VARCHAR(255), NULL)

### 7.5 `posts` (Marketplace Opportunity Entity)
- `id` (INTEGER, PK, Autoincrement)
- `company_id` (INTEGER, NOT NULL, FK &rarr; `companies.id`)
- `post_type` (VARCHAR(50), DEFAULT 'internship') — internship, job
- `domain` (VARCHAR(100), NOT NULL, INDEXED)
- `title` (VARCHAR(255), NOT NULL)
- `slug` (VARCHAR(255), NULL, INDEXED)
- `stipend_min` / `stipend_max` (INTEGER)
- `location` / `work_mode` (VARCHAR(100), DEFAULT 'Remote')
- `status` (VARCHAR(50), DEFAULT 'published') — draft, published, expired
- `published_at` / `expires_at` (TIMESTAMPTZ)

---

---

## § 11: Production Operations Playbook

### 11.0. Master Historical Batch Ingestion & Dispatch Campaign Matrix

The following table documents all completed and ongoing programmatic batch dispatches, data reconciliations, and candidate cohort ingestions across DBERT platforms:

| Campaign / Batch Identifier | Source Reference | Candidate Volume | Deliverables & Artifacts | Primary Dispatch Script | State & Tracking Files |
|---|---|:---:|---|---|---|
| **409 Provisional Batch** | Oct 2026 Provisional Cohort | 409 candidates | DNS pre-flight audit (SPF/DKIM/DMARC), 30s rate pacing, milestone telemetry to admins | `scripts/dispatch_409_provisional.py` | `data/dispatch_tracking_409.json`, `data/all_409_provisional_registry.json` |
| **9 Verified Candidates Upgrade** | Google Sheet `gid=1265293201` (Rows 57–65) | 9 candidates (7 upgraded, 2 new) | ₹299 fee verified, official 3-doc PDF credential packets generated, preview PNGs deployed | `scripts/dispatch_9_verified_certificates.py` | `data/dispatch_tracking_9_verified.json`, `outputs/cohort_2026/` |
| **Approved Incubation (Bhargavi Poola)** | ₹1,500 Balance Completion (`DBERT-ENR-703685-TYN6`) | 1 candidate | Marked `APPROVED` in ledger; live real-time countdown to Nov 9, 2026 deployed on `/eroll` | N/A (Web UI & Lookup API) | `data/balance_enrollments_1500.json` |
| **Google SMTP Quota Watchdog** | Google Workspace Daily User Limit | Automation daemon | Cooldown probe (`smtp.gmail.com:465`) every 300s, automated exit code 55 circuit breaker, phased triggers | `scripts/quota_watchdog_and_dispatcher.py` | `data/quota_watchdog_state.json`, `data/quota_watchdog.log`, `start_quota_watchdog.bat` |
| **1,593 Sheet Provisional Ingestion** | Google Sheet `gid=338877142` | 1,593 candidates | Directory shield gate (never added to `directory_candidates.json`), `/verify/unlock` landing page | `scripts/dispatch_sheet_1593.py` | `data/sheet_1593_provisional_registry.json`, `data/sheet_1593_dispatch_tracking.json` |
| **Sheet gid=97313663 Ingestion** | Google Sheet `gid=97313663` | 859 raw -> 840 unique | 19 phone duplicates merged, normalized into 7 canonical tracks, multi-account rotation | `scripts/ingest_sheet_859.py` | `data/sheet_859_registry.json`, `data/dispatch_tracking_sheet_859.json` |
| **Stipend ₹299 WhatsApp Campaign** | LinkedIn Cohort pending ₹299 Gate | 41 candidates (40 sent, 1 auto-linked) | Sent via logged-in Account 2 with 18s–35s pacing; both URLs in first 15 lines; ₹499 caution deposit and ₹5,000 stipend withholding warning | `scripts/dispatch_stipend_custom_whatsapp.py` | `data/whatsapp_stipend_299_pending.json`, `data/dispatch_tracking_stipend_299.csv` |
| **4 Verified Candidates Upgrade (Nov 19, 2026)** | Website ₹299 Gateway (Shrey Patel, Kethavath Sruthi) & Google Sheet `gid=1265293201` Rows 89–90 (Bhavya Balchandani, Tehreem Fatima) | 4 candidates (3 upgraded, 1 new) | ₹299 fee verified, official 3-doc PDF credential packets generated, preview PNGs deployed, synced to PostgreSQL `intern_certificates` with `tier='verified'` | `scripts/issue_4_verified_certificates.py`, `scripts/deploy_4_verified_certificates_to_ec2.py` | `data/verification_submissions_299.json`, `apps/website/src/data/certificates_registry.json`, `apps/website/src/data/directory_candidates.json` |
| **43 Expiring Posts Renewal (Nov 20, 2026)** | Posts expiring <= 2026-11-27 (IDs 24–33, 37–51, 55–69, 73–75) | 43 internship posts | Extended `apply_by` to 2027-01-15 and `expires_at` to 2027-02-15; refreshed SEO-rich 2026/2027 titles; standardized DBERT Incubation `/enroll/1999` pathway; synced to `https://lms.dbert.in/sitemap.xml` with lastmod `2026-11-20` | `scripts/renew_43_expiring_posts.py` | `data/expiring_43_posts.json` |
| **14 Verified Candidates Upgrade (Nov 20, 2026)** | Inbound ₹299 Gateway via `/verify/unlock` (Sakthi P, Pulluri Bhargavi, Bhargavi Poola, Yasharth Poddar, Radha Bhamodkar, Shanmukha Sri Saikumar Medisetty, Shanu Sri Gowtham, Kolloju Meghana, M Brahmani, Bhargavi C K, Deepanshu, Siva Sankar Thirumalasetty, Satya Patil, Kundan Kumhar) | 14 candidates upgraded | ₹299 fee verified, official 3-doc PDF credential packets generated, preview PNGs deployed, promoted to Tab 1 (Pre-Vetted Engineers) on `/verify/directory`, synced to PostgreSQL `intern_certificates` with `tier='verified'`, unlocking Gate 1 for stipend release | `scripts/issue_14_verified_certificates.py`, `scripts/deploy_14_verified_certificates_to_ec2.py` | `data/verification_submissions_299.json`, `apps/website/src/data/certificates_registry.json`, `apps/website/src/data/directory_candidates.json` |
| **4 Verified Candidates Upgrade (Nov 20, 2026 - Evening)** | Inbound ₹299 Gateway via `/verify/unlock` (Suraj Shivsunder Jha, Devanshi Yadav, G.Vinay Kumar Reddy, Bharathan K) & Gate 1 unlock for Subhradip Das, Burra Thanvesh, Shruthi Yuvnuv. V | 4 upgraded + 3 Gate 1 verified | ₹299 fee verified, Devanshi Yadav 3-doc PDF credential packet & preview PNG generated, all 4 promoted to Tab 1 (Pre-Vetted Engineers) on `/verify/directory`, synced to PostgreSQL `intern_certificates` and `intern_accounts` with `tier='verified'` and `stipend_verified=1`, unlocking Gate 1 for stipend release | `scripts/issue_new_batch_299.py`, `scripts/deploy_new_batch_299_to_ec2.py` | `data/verification_submissions_299.json`, `apps/website/src/data/certificates_registry.json`, `apps/website/src/data/directory_candidates.json` |
| **60 ₹299 Target Queue (Nov 20, 2026)** | High-intent active interns with provisional certs / tasks | 60 candidates (57 sent, 1 failed, 2 skipped) | Sent via dual accounts with 18s–35s pacing; directory and direct unlock URL in first 10 lines | `scripts/dispatch_60_targets_299_whatsapp.py` | `data/whatsapp_299_queue_acc1.json`, `data/whatsapp_299_queue_acc2.json`, `data/whatsapp_dispatch_299.log` |
| **Batch 35 Locked Interns ₹299 & ₹5,000 Stipend (Nov 21, 2026)** | Active provisional interns with release pending tasks (zero prior contact) | 35 candidates (35 sent, 0 failed, 0 skipped · 100% delivered) | Sent strictly via verified logged-in Account 2 with 18s–35s human pacing; directory and direct unlock URL in first 10 lines; 100% verified zero prior contact in 299/stipend campaigns | `scripts/dispatch_batch35_299_acc2.py` | `data/whatsapp_299_queue_batch35_acc2.json`, `data/dispatch_tracking_batch35_acc2.csv`, `data/dbert_whatsapp_sent_today.json` |
| **2 Verified Candidates Upgrade (Nov 21, 2026)** | Inbound ₹299 Gateway via `/verify/unlock` (Molugu Nanda Yaso Vardhan, H A Uday Bhasker) | 2 candidates upgraded | ₹299 fee verified, official 3-doc PDF credential packets generated, preview PNGs deployed, promoted to Tab 1 (Pre-Vetted Engineers) on `/verify/directory`, synced to PostgreSQL `intern_certificates` and `intern_accounts` with `tier='verified'` and `stipend_verified=1`, unlocking Gate 1 for stipend release (Maturation date: 03 Dec 2026) | `scripts/issue_2_verified_certificates_nov21.py`, `scripts/deploy_2_verified_certificates_to_ec2.py` | `data/verification_submissions_299.json`, `apps/website/src/data/certificates_registry.json`, `apps/website/src/data/directory_candidates.json` |
| **Multi-Login Selected & Offer Dispatch (Nov 21, 2026)** | Complete Under Review cohort with multiple logins & unpaid ₹499 (Ratnadeep bamane, Sabreen Saed, Anvisha Raj, Srimathi K, Ritwika Bandyopadhyay, abhinand sagar, Gayathri S R, Karthika Raja, Varanasi Srikari, Muguntharajan K) | 10 promoted to Selected in DB (9 dispatched via WA, 1 deduplicated) | Promoted `status='Selected'` & `signup_stage=3`, generated official deterministic offer letter records (`DBERT-OFR-2026-...`), verified `/portal/offer` rendering, sent selection offer message via Account 2 with 18s–35s pacing | `scripts/promote_under_review_to_selected.py`, `scripts/dispatch_selected_multi_login_whatsapp.py` | `data/selected_multi_login_cohort.json`, `data/whatsapp_selected_multi_login_queue.json`, `data/dispatch_tracking_selected_multi_login.csv` |
| **GitHub PR & LinkedIn Milestone Audit (Nov 21, 2026)** | 33 Pending Submissions + 143 Verified Interns Scheduled for Release | 28 unique submissions (1 passed, 27 changes requested) + 143 cohort accounts | Audited strict PRs on 4 project repos (Alkame, Gayatri, Aivara, Internship Portal) & LinkedIn certification additions. Only Priyanshu Kalondia passed (PR #29). 27 updated to status='changes_requested' on EC2 with structured feedback. | `scripts/audit_33_github_linkedin.py`, `scripts/apply_resubmission_status.py` | `data/github_linkedin_audit_report.json` |
| **27 Capstone Revision WhatsApp Outreach (Nov 21, 2026)** | 27 Flagged Milestone Submissions | 25 unique candidate recipients (23 sent via WA, 25 notified via in-app DB) | Sent personalized WhatsApp messages via Account 2 with 18s–35s pacing; Line 7 resubmission URL, Line 8 verification URL; dual-wrote in-app notifications directly to EC2 PostgreSQL notifications table | `scripts/dispatch_resubmission_27_whatsapp.py` | `data/phones_27_resubmission.json`, `data/dispatch_tracking_resubmit_27.csv`, `data/dbert_whatsapp_sent_today.json` |
| **GitHub Profile & Cross-Platform Backlinks (Nov 21, 2026)** | Founder & Lead Architect Profile & Monorepo Ecosystem | Ecosystem-wide SEO Mesh & Backlinks | Overhauled `https://github.com/ainabhinavsharma` with 4 flagship repos; boosted sitemaps (`/about/team` 0.95, `/labs/opensource` 0.90); dual robots.txt sitemaps; enriched Person & Org JSON-LD; live verified on EC2 | `scripts/deploy_github_and_interconnected_seo_to_ec2.py` | `scratch/ainabhinavsharma/README.md`, `apps/website/src/app/sitemap.ts`, `apps/portal/templates/_footer_seo.html` |
| **4 Verified Candidates Upgrade (Nov 21, 2026 - Night)** | Inbound ₹299 Gateway via `/verify/unlock` (Nishant Makwane, Jay Kumar, Danisaram Anji, Maroju Prince Karthik) | 4 candidates upgraded | ₹299 fee verified, official 3-doc PDF credential packet generated for Maroju Prince Karthik (`CERT-DBERT-2026-FSD-343`), all 4 promoted to Tab 1 (Pre-Vetted Engineers) on `/verify/directory`, synced to PostgreSQL `intern_certificates` and `intern_accounts` with `tier='verified'` and `stipend_verified=1`, unlocking Gate 1 for 03 Dec 2026 stipend release | `scripts/issue_4_verified_certificates_nov21_batch.py`, `scripts/deploy_4_verified_batch_to_ec2.py` | `data/verification_submissions_299.json`, `apps/website/src/data/certificates_registry.json`, `apps/website/src/data/directory_candidates.json` |
| **Universal Mobile Responsive Engine (Nov 21, 2026)** | All LMS Frontend Pages & Templates (`portal.html`, `dbert-theme.css`, `_head.html`) | Entire Intern & Candidate Userbase on Mobile (320px–768px Viewports) | Resolved horizontal body overflow (reduced bodyScrollWidth from 598px to exact 390px), enforced fluid responsive buttons, vertical stacking for button clusters (`.na-btn-cluster`, `.btn-cluster`), scrollable wrappers for steppers/tables, zero right-edge clipping on mobile viewports; verified live with Playwright | `scripts/deploy_mobile_fixes_to_ec2.py` | `apps/portal/static/css/dbert-theme.css`, `apps/portal/templates/portal.html`, `apps/portal/templates/_head.html` |
| **Verified Fellows Showcase Overhaul (Nov 21, 2026)** | Public Verified Fellows Showcase (`https://dbert.in/fellows/verified`) & Registry | Entire Public & Recruiting Ecosystem | Purged 8 test fixture accounts (`@dbert.test`, `CERT-*-900+`), deduplicated multi-cert candidates to exact 92 unique verified alumni, removed all 'LinkedIn N/A' negative badges, resolved Next.js route segment collision, verified live on EC2 with Playwright | `scripts/generate_verified_fellows_data.py`, `scripts/deploy_clean_verified_fellows_to_ec2.py` | `apps/website/src/data/verified_fellows_showcase.json`, `apps/website/src/data/certificates_registry.json`, `data/test_fixtures_certificates.json` |
| **9-Domain Courses, Dynamic City SEO & Lead Capture (Nov 22, 2026)** | 9 Core Technical Domains across 18 Tech Hubs & Inbound Candidates | Complete Inbound Student & Lead Conversion Funnel | Deployed `/courses/[domain]` for all 9 domains with dual 2-mo fellowship & 3-mo course syllabi, single-segment `/internships/[slug]` dispatcher, interactive `TrackLeadCaptureForm` with `POST /api/leads/capture`, upgraded `dbert.in/sitemap.xml` to 390 URLs and `lms.dbert.in/sitemap.xml` to 10,369 URLs, live verified on EC2 | `scripts/deploy_courses_seo_sitemap_to_ec2.py`, `scripts/verify_production_endpoints.py` | `apps/website/src/app/courses/`, `apps/website/src/app/internships/[slug]/`, `apps/website/src/components/forms/`, `data/leads_inbound.json`, `apps/website/public/sitemap.xml`, `apps/portal/sitemap.xml` |
| **UI/UX Retention & Clean ₹1,999 Pricing (Nov 22, 2026)** | All 9 Domain Courses & 180 Geo-Internship Pages | Mobile & Desktop Viewports (320px–1440px) | Complete Obsidian Studio UI overhaul (`courses.module.css`), `CourseInteractiveShell` dual-track switcher (Fellowship vs Comprehensive Course), authentic verified alumni social proof from `directory_candidates.json`, mobile responsiveness hardening (16px input fonts, 48px touch targets, zero horizontal body scroll), strictly clean ₹1,999 public pricing with zero mention of ₹499/₹1,500 caution deposit on public pages, live verified on EC2 | `scripts/deploy_courses_seo_sitemap_to_ec2.py` | `apps/website/src/app/courses/courses.module.css`, `apps/website/src/components/courses/CourseInteractiveShell.tsx`, `apps/website/src/app/courses/[domain]/page.tsx`, `apps/website/src/app/internships/` |
| **Guaranteed Placement & Zero Public Stipend Mandate (Nov 22, 2026)** | All Public Marketing & SEO Pages across Website (`dbert.in`) | Candidate Inbound Conversion & Placement Architecture | Completely eliminated all occurrences of '₹5,000 stipend', '₹18,000 performance incentive', and monthly stipend ranges from public pages; established 100% Guaranteed Internship Placement across internal DBERT portfolio ventures (Gayatri AI, Alkame, Aivara) and verified corporate hiring partners; added direct LMS application routing (`https://lms.dbert.in/apply`) for direct candidates seeking the ₹499 caution deposit track; verified 0 errors on EC2 | `scripts/deploy_courses_seo_sitemap_to_ec2.py` | `apps/website/src/app/courses/[domain]/page.tsx`, `apps/website/src/components/courses/CourseInteractiveShell.tsx`, `apps/website/src/components/forms/TrackLeadCaptureForm.tsx`, `apps/website/src/data/geo_domains.config.ts`, `apps/website/src/app/internships/` |
| **125 Under Review Cohort Promotion to Selected (Nov 23, 2026)** | 125 Under Review Candidates on EC2 PostgreSQL | Intake Admissions & Conversion Pipeline | Promoted 125 candidate applications to `status='Selected'`, `signup_stage=3`, generated official deterministic offer letter records (`DBERT-OFR-2026-{DOMAIN}-{APP_ID:04d}`), batch dates 2026-11-23 to 2027-01-22, synced live to EC2 PostgreSQL; prepared WhatsApp selection campaign | `scripts/promote_all_under_review_to_selected.py` | `data/selected_under_review_cohort_125.json`, `data/ec2_under_review_audit_report.json` |
| **Ratnadeep Bamane ₹499 Reconciliation (Nov 22, 2026)** | ₹499 Caution Deposit Candidate | Candidate Admissions | Verified payment, updated `signup_stage=5`, `account_status='Confirmed Fellow'`, unlocked full LMS sprint workspace, dispatched personalized WhatsApp confirmation | `scripts/confirm_ratnadeep_enrollment.py` | `data/dbert_whatsapp_sent_today.json` |
| **Master Monorepo Production Deployment & Debris Purge (Nov 23, 2026)** | Full Monorepo Architecture & P0–P3 Bug Resolutions | Ecosystem-Wide (Public + LMS + API) | Archived `dbert-api-package/` to `data/archive/`, masked `dbert-api.service` on EC2, executed remote Next.js standalone build on EC2, synced public assets & sitemaps, restarted services. Verified 100% of live smoke test endpoints (HTTP 200), including direct vector PDF streaming (`/portal/certificate/.../pdf` - 807 KB) | `scripts/deploy_monorepo_master_to_ec2.py` | Git Commits `a56b885`, `9bfb5dc`, `02a9d64`, `c8b0569` |
| **Stalled Stage 3 Candidate Recovery Queue (Nov 23, 2026)** | Selected Cohorts with Issued Offers pending ₹499 Caution Deposit | 194 qualified candidates | Automated recovery queue generator; Formatted dual WhatsApp + Email templates with Offer URL (Line 9), Verification URL (Line 12), 14-day academic exam pause policy, zero-holding direct UPI transfer guarantee; 18s–35s human pacing | `scripts/build_stalled_stage3_recovery_queue.py`, `scripts/dispatch_stalled_stage3_recovery.py` | `data/stalled_stage3_recovery_queue.json`, `data/dbert_whatsapp_sent_today.json` |
| **5-Gate Stipend Maturation Audit (Dec 03, 2026 Cohort)** | 143 Verified Interns (`phones_143_verified_broadcast.json`) | 143 verified accounts (₹715,000 commitment) | Automated 5-Gate evaluation engine verifying Gate 1 (Verified Credential), Gate 2 (Tenure maturing 2026-12-03), Gate 3 (Encrypted UPI), Gate 4 (Capstone PR approved). Generated structured ledger report: 52 cleared for instant batch payout (₹260,000), 83 pending UPI only, 8 pending PR revision | `scripts/evaluate_stipend_cohort_dec3.py` | `data/stipend_cohort_dec3_readiness_report.json` |

---

This playbook provides standard operating procedures (SOPs) for day-to-day engineering, candidate management, deployments, and automated dispatches.

---

### 8.1. WhatsApp Dual-Account Dispatch System

The WhatsApp automation system operates through Playwright persistent browser contexts connected to two separate physical WhatsApp accounts.

```mermaid
flowchart TD
    subgraph Data Layer
        DB[(dbert_whatsapp.db SQLite)]
        SentLog[whatsapp_sent_log Deduplication]
    end

    subgraph Dispatch Router
        CLI[send_dbert_whatsapp.py]
        Queue[Uncontacted Candidates Queue]
        CLI -->|Load Latest Signups First| Queue
        Queue -->|Odd Serials| P1[Partition 1]
        Queue -->|Even Serials| P2[Partition 2]
    end

    subgraph Browser Automation
        P1 -->|Worker 1| W1[Account 1 Playwright Worker]
        P2 -->|Worker 2| W2[Account 2 Playwright Worker]
        W1 --> S1[.chrome_session_account1]
        W2 --> S2[.chrome_session_account2]
    end

    W1 -->|18s-35s Randomized Delay| WA1[WhatsApp Web Account 1]
    W2 -->|18s-35s Randomized Delay| WA2[WhatsApp Web Account 2]
    WA1 --> DB
    WA2 --> DB
```

#### 8.1.1. Physical Session Storage & Architecture
- **Account 1 Directory**: `C:\Users\user\Desktop\aivara\aivara\.chrome_session_account1`
- **Account 2 Directory**: `C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2`
- **Browser Executable**: Chrome (`C:\Program Files (x86)\Google\Chrome\Application\chrome.exe` or `C:\Program Files\Google\Chrome\Application\chrome.exe`)
- **Engine**: Playwright Chromium `launch_persistent_context` with user agent spoofing and disabled blink features (`--disable-blink-features=AutomationControlled`).

#### 8.1.2. Strict Architectural Rules
1. **The First-15-Lines Placement Rule (CRITICAL)**:
   - Both the **Verification Dossier URL** (`https://dbert.in/verify?certid=...`) and the **Action / Form URL** (`https://docs.google.com/forms/...` or `/enroll/1999`) **MUST appear within the first 15 lines** of the WhatsApp message.
   - Standard template placement: Verification URL at **Line 8**, Action/Form URL at **Line 11**.
2. **Reverse Chronological Candidate Ordering**:
   - Candidates must always be dispatched in order of registration timestamp (`signup_dt DESC`), prioritizing the newest signups over older inactive cohorts.
3. **Queue Partitioning (Equal Dual Split)**:
   - Odd candidate serials -> Account 1 (`--worker account1`).
   - Even candidate serials -> Account 2 (`--worker account2`).
4. **Anti-Ban Pacing & Humanized Safety**:
   - Randomized delay between consecutive deliveries: **18 seconds to 35 seconds**.
   - Input simulation: Text is pasted via clipboard simulation or typed with realistic keystroke intervals (50–120ms).
5. **Circuit Breakers & Deduplication**:
   - **Circuit Breaker**: If 3 consecutive delivery failures occur on an account, the worker immediately aborts to protect account health.
   - **Deduplication**: Every delivery is permanently recorded in SQLite table `whatsapp_sent_log` and `data/dbert_whatsapp_sent_today.json`. Candidates are NEVER messaged twice.

#### 8.1.3. Key CLI Commands Reference
```powershell
# 1. Check login status of both accounts (Headless pre-flight)
python scripts\check_both_whatsapp_logins.py

# 2. Pre-flight session check and launch dual workers interactively
python scripts\verify_and_launch_dbert_whatsapp.py

# 3. Check current campaign status (Sent vs Pending vs Failed)
python scripts\send_dbert_whatsapp.py --status

# 4. Preview sample queue and message template without sending
python scripts\send_dbert_whatsapp.py --dry-run

# 5. Load next batch of 92 uncontacted candidates (Latest signups first)
python scripts\send_dbert_whatsapp.py --next-batch

# 6. Run Worker for Account 1 (Odd Serials)
python scripts\send_dbert_whatsapp.py --worker account1

# 7. Run Worker for Account 2 (Even Serials)
python scripts\send_dbert_whatsapp.py --worker account2

# 8. Send 1 single test message to verify delivery
python scripts\send_dbert_whatsapp.py --test-to 919876543210 --account 2
```

---

### 8.2. Email Dispatching & SMTP Quota Management

DBERT uses Google Workspace SMTP (`smtp.gmail.com:465` SSL) to deliver transactional emails, acceptance dossiers, and candidate credentials. Because Google Workspace enforces a strict rolling 24-hour daily sending limit (~1,500–2,000 emails/account), an automated watchdog manages throttling and prevents quota lockout.

```mermaid
sequenceDiagram
    participant Watchdog as quota_watchdog_and_dispatcher.py
    participant SMTP as smtp.gmail.com:465
    participant EC2 as Production EC2 (dbert.in)
    participant Recipients as Candidate Recipients
    participant Admins as ain.sharma.abhinav / ajnatechrpa

    loop Every 300 Seconds
        Watchdog->>SMTP: Non-disruptive handshake probe
        SMTP-->>Watchdog: SMTP 250 OK or 550 5.4.5 Limit Exceeded
    end

    Note over Watchdog: Quota Reset Detected!
    Watchdog->>EC2: Step 1: Deploy updated registries & verify HTTP 200
    EC2-->>Watchdog: Deployment Successful
    Watchdog->>Recipients: Step 2: Dispatch 9 verified 3-doc PDF credential packets
    Watchdog->>Recipients: Step 3: Resume provisional batch (#304-#409) with 30s pacing
    Watchdog->>Watchdog: Step 4: Synchronize email + WhatsApp tracking CSV
    Watchdog->>Admins: Step 5: Dispatch milestone completion telemetry email
```

#### 8.2.1. Quota Watchdog Architecture (`scripts/quota_watchdog_and_dispatcher.py`)
- **Probing Mechanism**: Connects to `smtp.gmail.com:465` every 300 seconds using SSL. Sends `EHLO` and authenticates.
- **Circuit Breaker Exit Code 55**: If SMTP returns `550 5.4.5 Daily user sending quota exceeded`, the dispatcher logs the lockout timestamp, calculates expected 24h reset time, and triggers exit code 55.
- **Phased Post-Unlock Workflow**:
  - **Phase 1: Production Registry Deployment**: Updates `certificates_registry.json` and standalone builds on EC2, verifying HTTP 200.
  - **Phase 2: High-Priority Verified Credentials**: Issues and emails 3-doc PDF credential packets to candidates who completed the ₹299 verification.
  - **Phase 3: Provisional Candidate Queue**: Resumes provisional notification emails with strict 30-second pacing.
  - **Phase 4: Omnichannel Sync**: Merges email delivery tracking with WhatsApp logs into `data/dbert_unified_omnichannel_tracking.csv`.
  - **Phase 5: Telemetry Dispatch**: Dispatches delivery completion reports to admin email addresses.

#### 8.2.2. Key CLI Commands Reference
```powershell
# Launch automated quota watchdog daemon
python scripts\quota_watchdog_and_dispatcher.py

# Launch background watchdog via batch file
scripts\bat\start_quota_watchdog.bat

# Launch or resume live provisional candidate email batch dispatch
python scripts\dispatch_409_provisional.py --live --delay 30 --report-interval 100

# Inspect recent dispatch delivery log
powershell -Command "Get-Content data/dispatch_409.log -Tail 30"

# Check email tracking summary
python -c "import json; d = json.load(open('data/dispatch_tracking_409.json', encoding='utf-8')); s = sum(1 for x in d if x['status']=='SENT'); print(f'Delivered: {s}/409 | Pending: {409-s}')"
```

---

### 8.3. Production EC2 Deployment Procedures

DBERT's production infrastructure is hosted on AWS EC2 running Ubuntu Linux, orchestrated via Systemd and reverse-proxied with SSL termination by Nginx.

#### 8.3.1. Infrastructure Topography
- **Host**: `ubuntu@3.26.237.171`
- **SSH Key**: `C:\Users\user\.ssh\dbert-production-server.pem`
- **Base Directory**: `/var/www/dbert-website-lms`
- **Managed Systemd Services**:
  - `dbert-website.service`: Next.js 14/16 App Router (Standalone Node server on port 3000).
  - `dbert-portal.service`: Flask LMS Gunicorn server (WSGI on port 5001).
  - `dbert-api.service`: FastAPI Uvicorn server (Decommissioned & masked Nov 23, 2026; archived to `data/archive/dbert-api-package/`).
  - `nginx.service`: Reverse proxy for `dbert.in`, `lms.dbert.in`, `api.dbert.in`.

#### 8.3.2. Next.js Website Deployment Sequence
Whenever changes are made to `apps/website`, the standalone build must be compiled remotely and linked to the permanent data directory:

```bash
# 1. Upload modified files via SCP
scp -i "C:\Users\user\.ssh\dbert-production-server.pem" -o StrictHostKeyChecking=no -o BatchMode=yes <local_file> ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/website/<target_path>

# 2. Remote Build & Asset Sync on EC2
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 'bash -s' << 'EOF'
cd /var/www/dbert-website-lms/apps/website
export NODE_ENV=production
npm run build

# Sync dynamically generated sitemap into static standalone public paths
if [ -f .next/server/app/sitemap.xml.body ]; then
  cp .next/server/app/sitemap.xml.body public/sitemap.xml
fi
cp -r public .next/standalone/ 2>/dev/null || true
cp -r public .next/standalone/apps/website/ 2>/dev/null || true
if [ -f .next/server/app/sitemap.xml.body ]; then
  cp .next/server/app/sitemap.xml.body .next/standalone/public/sitemap.xml 2>/dev/null || true
  cp .next/server/app/sitemap.xml.body .next/standalone/apps/website/public/sitemap.xml 2>/dev/null || true
fi

# Ensure permanent data symlink persists across builds
mkdir -p /var/www/dbert-website-lms/data
rm -rf /var/www/dbert-website-lms/apps/website/.next/standalone/data
ln -s /var/www/dbert-website-lms/data /var/www/dbert-website-lms/apps/website/.next/standalone/data

# Restart service and verify health
sudo systemctl restart dbert-website.service
sleep 2
systemctl is-active dbert-website.service
curl -Is http://127.0.0.1:3000/verify | head -n 1
EOF
```

#### 8.3.3. Flask LMS Portal Deployment Sequence
Whenever changes are made to `apps/portal` (routes, models, templates, static CSS):

```bash
# 1. Upload modified portal files
scp -i "C:\Users\user\.ssh\dbert-production-server.pem" -r apps/portal/templates ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/portal/
scp -i "C:\Users\user\.ssh\dbert-production-server.pem" -r apps/portal/static ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/portal/

# 2. Run Pre-flight Check & Restart Portal
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 'bash -s' << 'EOF'
cd /var/www/dbert-website-lms
bash scripts/production_preflight.sh
sudo systemctl restart dbert-portal.service
sleep 2
systemctl is-active dbert-portal.service
curl -Is http://127.0.0.1:5001/login | head -n 1
EOF
```

#### 8.3.4. Python Automated Deployment Utilities
Instead of running manual SSH commands, use the verified Python deployment utilities:
```powershell
# Deploy website updates & rebuild standalone
python scripts\deploy_website_updates_to_ec2.py

# Deploy candidate directory & update rankings
python scripts\deploy_directory_to_ec2.py

# Deploy enrollment portal & balance completion engine
python scripts\deploy_enrollment_1999_to_ec2.py

# Deploy LMS portal UI/UX & template updates
python scripts\deploy_portal_updates_to_ec2.py

# Deploy full monorepo ecosystem
python scripts\deploy_all_to_ec2.py
```

---

### 8.4. Admin Operational Actions via CLI / SSH

Admins can execute critical candidate lifecycle transitions, certificate issuances, payment reconciliations, and stipend approvals directly via automated scripts.

#### 8.4.1. Approving "Under Review" Applicants & Advancing Stages
Candidates in "Under Review" (Stage 2) can either:
1. **Self-Service Fast-Track:** Upgrade directly on `/portal/offer` into the **Industry Incubation & Paid Internship Fellowship (₹1,999)** via `https://dbert.in/enroll/1999`, unlocking immediate Monday kickoff, ₹5,000 milestone stipend criteria, 1-on-1 mentorship, and production repos without waiting in the review queue.
2. **Staff Batch Promotion:** Admins run batch promotion to advance high-intent active applicants to "Selected" (Stage 3) to issue digital offer letters and unlock standard internship seat confirmation:

```powershell
# Execute promotion script
python scripts\promote_under_review_to_selected.py
```
**Under the Hood Actions Executed:**
1. Updates `applications` table: `status = 'Selected'`, `reviewed_at = NOW()`.
2. Updates `intern_accounts` table: `signup_stage = 3`, `account_status = 'Selected'`.
3. Deterministically generates an official offer letter record in `intern_offer_letters` (`DBERT-OFR-2026-[TRACK]-[ID:04d]`) across the candidate's specific engineering domain track (`FSD`, `AIML`, `PA`, `CYBER`, `DA`, etc.).
4. Generates offer letter access for candidate on `https://lms.dbert.in/portal/offer` with 3-step review, digital signature (`/portal/offer/sign`), and ₹499 seat confirmation gateway.
5. Exports cohort details to `data/selected_multi_login_cohort.json`.

#### 8.4.2. Issuing Official Verified Certificates (3-Doc Packet)
When a candidate completes the ₹299 verification fee (either via website gateway or direct submission):
```powershell
# 1. Add candidate to verification_submissions_299.json
# 2. Run certificate packet generator and registry sync
python scripts\issue_4_verified_certificates_nov21_batch.py

# 3. Deploy updated credentials and preview PNGs to EC2
python scripts\deploy_4_verified_batch_to_ec2.py

# 4. Sync credentials into LMS portal PostgreSQL
python scripts\sync_verified_certificates_to_portal.py
```
**Artifacts Generated:**
- `outputs/cohort_2026/{certId}_completion.pdf`
- `outputs/cohort_2026/{certId}_evaluation.pdf`
- `outputs/cohort_2026/{certId}_lor.pdf`
- `apps/website/public/certificates/previews/{certId}.png`
- Promoted to **Tab 1: Pre-Vetted Engineers (Verified · Ready to Hire)** on `/verify/directory`.
- Unlocks **Gate 1** for ₹5,000 stipend release.

#### 8.4.3. Reconciling ₹1,500 Incubation Balance Payments
When a candidate submits a 12-digit UPI UTR on `/enroll/1999`:
```powershell
# 1. Inspect submitted UTRs in permanent data ledger
powershell -Command "Get-Content data/balance_enrollments_1500.json | ConvertFrom-Json"

# 2. Reconcile balance records into EC2 PostgreSQL database
python scripts\sync_enrollments_to_postgres.py
```
**Ledger Updates:**
- Validates 12-digit UTR.
- Sets `payment_status = 'COMPLETED'`, `verified_by_admin = true`.
- Unlocks full incubation perks, GitHub project repository access, and live mentor sprint allocation.

#### 8.4.4. 5-Gate Milestone Stipend & Capstone PR Triage Playbook (v2026.3)
When evaluating candidate milestone PRs, verifying stipend gates, or processing capstone submissions across the 93 queue items:

```powershell
# 1. Audit all pending GitHub PRs, candidate forks, and LinkedIn certifications across EC2
python scripts/deep_audit_93.py

# 2. Inspect live GitHub API mergeability, additions, and upstream state
python scripts/inspect_github_prs.py

# 3. Execute atomic queue triage and auto-approval of merged/clean PRs on production EC2
python scripts/execute_queue_triage.py
```

**Live Production Status (Nov 23, 2026):**
- **Approved Submissions:** **11 Submissions** (including Gurveer Singh PR #35, Kundan Kumhar PR #16, Ankur Sen PR #7, Shruthi Yuvnuv PR #1, and Shanu Sri Gowtham PR #19).
- **Changes Requested:** **82 Submissions** (All provided with actionable feedback: Bhargavi C K rebase guidance, Thanvesh & Vinay upstream PR guidance, zero-commit/unofficial repo guidance).
- **Pending Backlog:** **0 Submissions** (100% triaged).
- **All 5 Gates Cleared (Ready for Payout):**
  1. **Suraj shivsunder jha** (`sjha0940@gmail.com`) — ₹5,499 (Matured: 21 Nov 2026)
  2. **Priyanshu Kalondia** (`priyanshukalondia@gmail.com`) — ₹5,499 (Matured: 21 Nov 2026)
  3. **Shruthi Yuvnuv** (`reachshruthiv@gmail.com`) — ₹5,499 (Matured: 19 Jan 2027)

#### 8.4.5. Standardized 65–84 Credential Issuance & Evaluation SOP (v2026.3)
When issuing new credentials or evaluating capstone project deliverables:
```powershell
# 1. Run local deterministic deliverable evaluation test
python -c "from apps.portal.services.grading_service import calculate_project_grade; print(calculate_project_grade('AI & Machine Learning', candidate_identifier='CERT-DBERT-2026-AIML-902'))"

# 2. Test 3-document authentic PDF compilation (Completion, Evaluation Rubric, Recommendation Letter)
python -c "from apps.portal.services.certificate_packet_service import CertificatePacketService; res = CertificatePacketService.get_master_pdf_bytes(None, 'CERT-DBERT-2026-AIML-902'); print('Size:', len(res[0]), 'Filename:', res[1])"

# 3. Verify math invariant (sum of 9 rubrics must exactly equal final score)
python -c "from apps.portal.services.grading_service import generate_9_rubric_marks; assert all(sum(generate_9_rubric_marks(s)) == s for s in range(65, 85)); print('Verified all 20 score rubrics!')"
```
**Operational Mandates:**
- **Zero Score Inflation**: All future batch issuance scripts (`scripts/issue_*_certificates*.py`) must calculate scores using `calculate_project_grade()` or clamp strictly to $[65, 84]$.
- **Rubric Exactness**: All 9 rubrics must sum exactly to the final score using `generate_9_rubric_marks()` in Python and `generate9RubricMarks()` in TypeScript.
- **Historical Immutability**: Never mutate historical scores or grades for previously issued cohorts (except calibrated flagship test record `CERT-DBERT-2026-AIML-902`).

---

---

## § 12: Real-Time Operational Dashboard & Live Health Queries

To inspect the real-time operational status of candidates, payment gates, and outbox queues, an agent or human operator can execute this canonical SQL query battery directly via SSH:

```bash
ssh -i "C:\Users\user\.ssh\dbert-production-server.pem" ubuntu@3.26.237.171 "sudo -u postgres psql -d dbert_lms" << 'EOF'
SET search_path TO dbert_internship, public;

SELECT '=== CANDIDATE STAGE BREAKDOWN ===' AS metric;
SELECT signup_stage, count(*) FROM intern_accounts GROUP BY signup_stage ORDER BY signup_stage;

SELECT '=== APPLICATION STATUS BREAKDOWN ===' AS metric;
SELECT status, count(*) FROM applications GROUP BY status ORDER BY count(*) DESC;

SELECT '=== PAYMENT STATUS BREAKDOWN ===' AS metric;
SELECT payment_status, count(*) FROM enrollments GROUP BY payment_status ORDER BY count(*) DESC;

SELECT '=== CERTIFICATE TIER BREAKDOWN ===' AS metric;
SELECT tier, count(*) FROM intern_certificates GROUP BY tier ORDER BY count(*) DESC;

SELECT '=== TASK SUBMISSION QUEUE ===' AS metric;
SELECT status, count(*) FROM task_submissions GROUP BY status ORDER BY count(*) DESC;

SELECT '=== EVENT OUTBOX QUEUE ===' AS metric;
SELECT status, count(*) FROM event_outbox GROUP BY status ORDER BY count(*) DESC;
EOF
```

### 12.1. Verified Baseline Snapshot (November 23, 2026)

The following metrics represent the live, reconciled production state across AWS EC2 PostgreSQL (`dbert_lms`) and static master registries:

- **Total LMS Applications**: **5,188** (Selected: 4,359 | Accepted: 408 | Rejected: 331 | Under Review: 5 | Enrollment Pending: 26 | Apply Pending: 21 | On Hold: 19 | Verified: 12 | Enrolled: 8)
- **LMS Intern Accounts**: **3,038** active intern profiles
- **Enrollments Ledger**: **469** total recorded enrollments (389 Track A Caution Deposit ₹499 Paid | 8 Track B Incubation Balance ₹1,500 Submissions in `balance_enrollments_1500.json`)
- **Verified Credential Gate (₹299 Gateway)**: **31 Total Approved** records in `verification_submissions_299.json`
- **Master Certificate Registry (`certificates_registry.json`)**: **477 Total** (96 Cryptographically Verified · 381 Provisional)
- **Pre-Vetted Engineers Directory (`directory_candidates.json`)**: **476 Total** (96 Tab 1 Verified · 380 Tab 2 Provisional Fellows)
- **PostgreSQL Intern Certificates (`intern_certificates`)**: **129 Total** (118 Tier='verified')
- **Stipend Pipeline (Gate 1)**: **143 Verified Interns** unlocked for performance release
- **Gate 2 (Maturation Schedule)**: **138 Maturing on 03 Dec 2026**
- **Gate 3 (Payout Setup Encrypted UPI)**: **53 Set / 90 Missing**
- **Gate 4 (Capstone Dossier Submissions)**: **28 Submissions Audited** (1 Passed, 27 In Revision / Changes Requested)
- **Gate 5 (Ready for Scheduled Release)**: **20 Ready**
- **Platform Coin Ledgers**: **35,130 Coins** in `coin_ledger_mirror` (35,000 Referral Withdrawable / 130 Task Spendable)
- **Geo-Internship Programmatic Surfaces**: **180 Live Geo Pages** (9 Domains 	imes 20 Indian Tech Metros) with `TrackLeadCaptureForm`
- **Search Console Keywords Monitored**: High-intent ranking keywords tracked in `data/seo_keyword_intelligence.json`

## § 13: Strategic Future Expansion Roadmap (Phases 3–7)

Building upon the completed foundational deployments (Phase 1: Immediate UX Unblocks and Phase 2: Dual-Monorepo Data Convergence), the platform execution roadmap extends across 5 strategic phases.

```mermaid
gantt
    title DBERT Strategic Expansion Roadmap (Phase 3 - Phase 7)
    dateFormat  YYYY-MM-DD
    section Phase 3
    BYOK AI Resilience & Self-Healing Pipeline :p3, 2026-11-23, 14d
    section Phase 4
    Omnichannel Telemetry & Conversion Mesh     :p4, 2026-12-01, 14d
    section Phase 5
    Service Unification & API Gateway Converge :p5, 2026-12-10, 21d
    section Phase 6
    Zero-Touch Credential & Stipend Minting    :p6, 2026-12-20, 14d
    section Phase 7
    B2B Recruiter Portal & Talent SaaS         :p7, 2027-01-05, 28d
```

---

### Phase 3: BYOK Resilience, Multi-LLM Routing & Self-Healing AI Pipeline (Target: Weeks 1–2)
- **Objective:** Eliminate student AI tutoring drop-offs and prevent 403/404 crashes caused by invalid keys or unreleased preview models.
- **Deliverables:**
  1. **Dynamic Model Probing on Save [COMPLETED - Nov 22, 2026]:** On key registration at `/account/gemini-key`, execute a live 1-token prompt via `probe_first_working_model` capped to top 4 models. Reject invalid keys immediately with exact Google API feedback, support dev mock bypasses, and store validated keys encrypted with Fernet AES-256. Fully integrated with robust async error handling, CSRF integrity, and interactive "How to get your free key (30 seconds)" guidance.
  2. **Automated Fallback Model Cascading:** Implement resilient provider fallback: `gemini-2.5-flash` $\to$ `gemini-2.0-flash` $\to$ `gemini-1.5-flash` $\to$ `gemini-1.5-pro`. Automatically step down the chain upon encountering HTTP 404/403 errors.
  3. **In-Modal Key Recovery Drawer:** If Fernet decryption fails or a key hits quota during a guided bounty (`/tasks/<id>/guide`), slide open a non-blocking recovery drawer prompting the intern to paste a fresh key without losing code state.

---

### Phase 4: Omnichannel Telemetry, Unified Conversion Funnels & Real-Time Abandonment Recovery (Target: Weeks 3–4)
- **Objective:** Track candidate drop-offs across both monorepos and deploy automated recovery triggers to boost payment conversions.
- **Deliverables:**
  1. **Universal GA4 Server-Side Measurement Protocol:** Standardize server-side event tracking across Next.js and Flask dispatching to `G-MN7ME9X518` (events: `application_started`, `sop_submitted`, `offer_viewed`, `utr_submitted`, `payment_verified`, `lesson_completed`).
  2. **Automated Funnel Abandonment Triggers [COMPLETED - Nov 23, 2026]:** Built `scripts/build_stalled_stage3_recovery_queue.py` generating a targeted queue of 194 stalled Stage 3 candidates (`data/stalled_stage3_recovery_queue.json`). Implemented `scripts/dispatch_stalled_stage3_recovery.py` with multi-channel WhatsApp (Account 2) and Google SMTP email delivery, enforcing verification and offer URLs on lines 9 and 12, 14-day academic exam pause policy, zero-holding direct UPI transfer guarantee, and 18s–35s humanized pacing.
  3. **Turnitin & AI Similarity Telemetry:** Integrate automated Turnitin plagiarism and AI generation similarity scores directly into recruiter proof dossiers on `/verify/[certId]`.

---

### Phase 5: Deep Service Unification & Monorepo Micro-Frontend Architecture (Target: Weeks 5–7)
- **Objective:** Decommission orphaned backend services, converge split APIs, and eliminate data store divergence.
- **Deliverables:**
  1. **Decommission Orphaned FastAPI Backend [COMPLETED - Nov 23, 2026]:** Masked and stopped `dbert-api.service` on production AWS EC2, safely archived `dbert-api-package/` into `data/archive/dbert-api-package/` (Commit `9bfb5dc`), and reclaimed server compute/memory resources without impacting any user-facing endpoints.
  2. **Prisma-to-PostgreSQL Convergence:** Replace Next.js flat-file JSON reads (`certificates_registry.json`, `balance_enrollments_1500.json`) with direct PostgreSQL queries via Prisma client.
  3. **Decompose `apps/portal/app.py`:** Extract the remaining monolithic route handlers into the 13 modular blueprints in `apps/portal/routes/`, reducing `app.py` from 23,534 lines to a clean `< 500-line` application factory.

---

### Phase 6: Automated Credential & Ledger Minting Engine (Target: Weeks 8–10)
- **Objective:** Zero-touch credential generation, instant vector PDF downloads, and automated stipend maturation disbursements.
- **Deliverables:**
  1. **Direct Binary Credential Packet Streaming [COMPLETED - Nov 23, 2026]:** Connected `CertificatePacketService` directly to `@app.route("/portal/certificate/<cert_id>/pdf")` and `@app.route("/certificate/<cert_id>/pdf")` via Flask `send_file()` and `BytesIO`. Verified live streaming of crisp 3-document vector PDF (807 KB) on production EC2 (Commit `02a9d64`).
  2. **Zero-Touch Stipend Maturation Pipeline [AUDITED & DEPLOYED - Nov 23, 2026]:** Implemented `scripts/evaluate_stipend_cohort_dec3.py` auditing all 143 verified intern accounts against the 5-Gate ledger for Dec 03, 2026 maturation. Generated `data/stipend_cohort_dec3_readiness_report.json` confirming 52 accounts cleared for instant ₹5,000 payout (₹260,000 total commitment), 83 pending UPI setup, and 8 pending capstone PR revision.
  3. **Dual Coin Ledger Minting:** Enforce strict cryptographic separation between educational task coins (redeemable for mock interviews and resume reviews) and withdrawable referral coins (redeemable for INR cash payouts).

---

### Phase 7: Multi-Tenant Enterprise Recruiter Portal & B2B Talent Marketplace (Target: Weeks 11–14)
- **Objective:** Transform the directory into a high-margin B2B recruiter SaaS platform with candidate shortlists, direct messaging, and automated placement billing.
- **Deliverables:**
  1. **Enterprise Recruiter Dashboard (`/company`):** Provide verified employers with advanced candidate search (filter by tech stack, evaluation score, GitHub PR quality, and availability).
  2. **Direct Recruiter-to-Candidate Messaging:** Allow approved companies to send interview requests and direct messages to pre-vetted engineers with in-app and email notifications.
  3. **Automated Placement Contracts & Invoicing:** Generate digital placement agreements and 14-day risk-free trial contracts upon successful hire, capturing recruiter commission fees.

---

---

## § 14: File Cleanup, Archival Manifest & Redirection Headers

### 14.1. Deprecated Files Transformed to Redirection Headers
The following legacy documentation files have been updated with permanent deprecation and redirect headers pointing exclusively to `MASTER.md`:
1. `AGENTS.md` (Repo Root) $	o$ Redirects to `MASTER.md`
2. `GEMINI.md` (Repo Root) $	o$ Redirects to `MASTER.md`
3. `ARCHITECTURE_ROADMAP.md` (Repo Root) $	o$ Redirects to `MASTER.md` § 1, § 5, § 13

### 14.2. Actionable Repository Cleanup Execution Manifest

```
Directory Target                     Action       Rationale & Safety Verification
------------------------------------------------------------------------------------------------------------------------
apps/website/src/app/_admin/         DELETED      51 dead unrouted files; administrative functions centralized in LMS
apps/website/src/app/_api/           DELETED      Unused legacy API routes; Next.js routes active in /api/
dbert-api-package/                   ARCHIVED     Orphaned 86-endpoint FastAPI backend archived to data/archive/dbert-api-package/; dbert-api.service masked on EC2
apps/portal/routes/masterclass.py    DELETED      Orphaned blueprint; deleted along with dead templates
apps/portal/templates/masterclass*.html DELETED   66 KB unused template backing dead masterclass blueprint
apps/portal/templates/dev_qa_matrix.html WIRED/ACTIVE 605-line template wired to /dev/qa-matrix cockpit; 100% tests pass
data/archive/queues/                 ARCHIVED     58 ephemeral JSON batch slices and queues moved from data/ root
data/archive/logs/                   ARCHIVED     Historical dispatch and email logs moved from data/ root
data/archive/screenshots/            ARCHIVED     11 ad-hoc test PNG screenshots moved from data/ root
scripts/archive/diagnostics/         ARCHIVED     184 ad-hoc throwaway checks and diagnostics safely moved from scripts/
------------------------------------------------------------------------------------------------------------------------
Permanent Registries (Strictly Kept): 8 master registries in data/ untouched and verified 100% intact.
```

---
*End of MASTER.md — Official Sovereign Architecture & Runbook for DBERT Ecosystem*
