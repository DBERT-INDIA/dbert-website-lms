# DBERT Repository Architecture & System Map
**Audit As-of Date:** 9 November 2026  
**Auditor / Implementation Engine:** Antigravity / AI Agent Core  
**Domain Authority:** `https://dbert.in` (Public Studio) & `https://lms.dbert.in` (Learning Management Portal)  
**Legacy Domain:** `dbert.online` (HTTP 301/308 redirect to `dbert.in`)

---

## 1. System Overview & Technology Stack

The DBERT platform is a multi-tier venture studio, AI engineering incubator, and candidate vetting ecosystem hosted on a unified AWS EC2 Linux production environment.

```mermaid
graph TD
    User([Public Visitor / Recruiter]) -->|HTTPS:443| Nginx[Nginx Reverse Proxy & SSL]
    Learner([Fellow / Intern]) -->|HTTPS:443| Nginx
    Admin([DBERT Staff / Admin]) -->|HTTPS:443| Nginx

    subgraph "Production Host (AWS EC2: 3.26.237.171)"
        Nginx -->|Proxy: dbert.in:3000| NextApp[apps/website (Next.js 16 App Router)]
        Nginx -->|Proxy: lms.dbert.in:5001| FlaskLMS[apps/portal (Flask Python LMS)]
        Nginx -->|Proxy: api.dbert.in:8000| FastApiApp[dbert-api-package (FastAPI Uvicorn)]

        NextApp -->|Prisma / Direct JSON| MasterData[(Local Master JSON Data & Symlinks)]
        FlaskLMS -->|Psycopg2 / SQLAlchemy| Postgres[(PostgreSQL: dbert_lms)]
        FlaskLMS -->|Fallback Read/Write| SqliteDB[(SQLite: internship.db)]
        FastApiApp -->|AsyncPG / SQLAlchemy| Postgres

        FlaskLMS -->|Google Gemini API| GeminiAI[Google Gemini 2.5 Flash / Pro]
        FlaskLMS -->|SMTP:465| GoogleSMTP[Google Workspace SMTP: abhinav.sharma@dbert.in]
        FlaskLMS -->|Playwright Dual-Account| WhatsAppEngine[WhatsApp Dispatch Engine]
    end
```

---

## 2. Directory Layout & Monorepo Map

| Directory Path | Tech Stack | Role & Responsibility |
|---|---|---|
| `apps/website/` | Next.js 16.2.10 (App Router), React 19, TypeScript, Turbopack, Prisma | Sovereign public venture studio, candidate credential verification (`/verify/[certId]`), Pre-Vetted Engineers Directory (`/verify/directory`), Incubation Enrollment & UTR submission (`/enroll/1999`, `/eroll`), SEO hub, portfolio case studies. |
| `apps/portal/` | Python 3.12, Flask 3.1.3, Jinja2, Psycopg2, SQLite | Complete Learning Management System (`lms.dbert.in`), candidate registration, applicant tracking, sprint submissions, AI pre-screening evaluator, ambassador referral tracking, mentor dashboards, staff approval queues. |
| `dbert-api-package/`| Python 3.12, FastAPI, Uvicorn, SQLAlchemy, Alembic | High-throughput asynchronous backend service powering candidate lookups, public verification endpoints, and mobile/external API consumers. |
| `data/` | JSON, SQLite (WAL mode), CSV | Authoritative candidate registries (`certificates_registry.json`, `directory_candidates.json`), live balance submissions (`balance_enrollments_1500.json`), dual-account WhatsApp queue (`dbert_whatsapp.db`), email dispatch logs. |
| `scripts/` | Python 3.12, Shell, PowerShell | Automated production deployment daemons (`deploy_enrollment_1999_to_ec2.py`, `deploy_directory_to_ec2.py`), email batch dispatchers with circuit breakers, and WhatsApp session workers. |
| `docs/` | Markdown, SQL | Database schemas (`POSTGRES_SCHEMA.sql`), security audit reports, and delivery guides. |
| `outputs/cohort_2026/`| High-res PDFs, PNGs | Pre-generated 3-document credential packets (Certificate, Evaluation, LOR) for 2026 graduates. |

---

## 3. Production Infrastructure & Systemd Daemon Roster

- **Production Server:** `ubuntu@3.26.237.171` (AWS EC2, ap-south-1)
- **Deployment Root:** `/var/www/dbert-website-lms`
- **System Services:**
  1. `dbert-website.service` — Node.js Standalone server running `apps/website/.next/standalone/server.js` on `127.0.0.1:3000`.
  2. `dbert-portal.service` — Gunicorn WSGI server running `apps/portal/wsgi.py` on `127.0.0.1:5001`.
  3. `dbert-api.service` — Uvicorn ASGI server running `dbert-api-package/backend/main.py` on `127.0.0.1:8000`.
  4. `nginx.service` — SSL termination, Let's Encrypt certificates, reverse proxy, security headers.
  5. `postgresql.service` — PostgreSQL 15 hosting database `dbert_lms` with schema `dbert_internship`.

---

## 4. Persistent Asset & Symlink Strategy

Next.js standalone builds exclude files in `data/` and `public/` by default unless explicitly copied or linked. To prevent data desynchronization:
1. `apps/website/public` is copied to `.next/standalone/` and `.next/standalone/apps/website/`.
2. `/var/www/dbert-website-lms/data` is permanently symlinked to:
   - `/var/www/dbert-website-lms/apps/website/.next/standalone/data`
   - `/var/www/dbert-website-lms/apps/website/.next/standalone/apps/website/data`
This ensures all candidate lookups and UTR submissions record idempotently to single-source disks.
