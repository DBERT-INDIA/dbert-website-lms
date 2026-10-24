# DBERT REST API & Ecosystem Backend

> **Production-Grade FastAPI + PostgreSQL Architecture**  
> Complete backend port from Flask + SQLite monolith to async FastAPI, SQLAlchemy 2.0, PostgreSQL 15, and Docker Compose. Exposes 88 REST routes with auto-generated OpenAPI 3.0 documentation.

---

## 1. Architecture Overview

```
                                      +--------------------------+
                                      |   Next.js / Mobile App   |
                                      +-------------+------------+
                                                    | (HTTPS)
                                                    v
                                      +-------------+------------+
                                      |       Nginx (Proxy)      |
                                      |        Port 80/443       |
                                      +-------------+------------+
                                                    | (Reverse Proxy)
                                                    v
                                      +-------------+------------+
                                      |     FastAPI Backend      |
                                      |      Port 8000 / Uvicorn |
                                      +------+-------------+-----+
                                             |             |
                         +-------------------+             +------------------+
                         v                                                    v
            +------------+------------+                          +------------+------------+
            |  PostgreSQL 15 (Async)  |                          | Local Upload Sandbox    |
            |     74 Schema Tables    |                          | /app/uploads Volume     |
            +-------------------------+                          +-------------------------+
```

### Key Architectural Highlights
- **Framework**: FastAPI (Python 3.11+), fully async with type-safe Pydantic v2 schemas.
- **ORM / Database**: SQLAlchemy 2.0 (asyncpg) + PostgreSQL 15. All 74 production tables mapped with complete foreign key graphs and topological ordering.
- **Migrations**: Alembic (`backend/migrations/`) with autogenerate support.
- **Security & Auth**: Dual-token JWT architecture (1h access tokens + 60d refresh tokens stored in database with cryptographic JTI rotation). Dual-hash verifier supporting legacy SHA-256 with transparent runtime upgrade to PBKDF2/bcrypt.
- **Strict Role-Based Guards**: Pre-configured FastAPI `Depends()` guards for all 5 roles: `intern`, `company`, `admin`, `mentor`, `staff`.
- **Integrations**: Async Razorpay checkout/webhook verification, Google Gemini AI Interview engine with round-robin API key rotation & cooling off periods, OneSignal push notifications, and transactional SMTP outbox.

---

## 2. Directory Layout

```
dbert-api-package/
├── backend/                       # FastAPI Application Root
│   ├── api/v1/                   # Modular REST Routers
│   │   ├── auth/                 # All 5 user logins, multi-stage signup, OTP, password reset
│   │   ├── intern/               # Intern profile, wizard, AI interview, applications
│   │   ├── applications/         # Application submission & state machine
│   │   ├── enrollments/          # Enrollment flows & verification
│   │   ├── payments/             # Razorpay orders, verification & webhooks
│   │   ├── uploads/              # Magic-byte secure file upload sandbox
│   │   ├── courses/              # Course catalog, chapters, day quizzes
│   │   ├── learning/             # Socratic AI tutor dialogs & spaced repetition
│   │   ├── admin/                # Control plane, stats, CSV export, telemetry
│   │   ├── cron/                 # Automated background jobs (X-Cron-Secret secured)
│   │   ├── messaging/            # Direct conversations & messaging
│   │   ├── notifications/        # Notification center & read status
│   │   ├── credentials/          # Public CV & certificate verification
│   │   ├── ambassador/           # Referral tracking & cash withdrawals
│   │   ├── tasks/                # Practice task submission & scoring
│   │   ├── company/              # Employer dashboard, job authoring, applicant review
│   │   ├── marketplace/          # Public jobs, internships, comments & analytics
│   │   └── public/               # Open metrics, blog posts, and visitor tracking
│   ├── core/                     # Application Core
│   │   ├── config.py             # Pydantic BaseSettings environment configuration
│   │   ├── database.py           # Async engine & sessionmaker
│   │   ├── security.py           # JWT generation, token verification, password hashing
│   │   ├── dependencies.py       # Role guards (require_intern, require_admin, etc.)
│   │   └── middleware.py         # Request context, correlation IDs, CORS, logging
│   ├── models/                   # SQLAlchemy ORM Models (74 tables mapped)
│   ├── schemas/                  # Pydantic request & response models
│   ├── services/                 # Pure domain business logic & third-party clients
│   ├── migrations/               # Alembic database migrations
│   ├── main.py                   # FastAPI application entrypoint & lifespan
│   └── requirements.txt          # Python dependencies
├── data-migration/               # SQLite to PostgreSQL Migration Suite
│   ├── sqlite_to_pg.py           # High-speed topological ETL script
│   ├── verify_migration.py       # Parity auditor & spot-check verification
│   └── migration_report.json     # Audit report verifying 100% row matching
├── databases/
│   └── internship.db             # Original SQLite database (read-only reference)
├── website-content/              # Next.js marketing content snapshot for frontend rebuild
│   ├── src/                      # UI pages, MDX blogs, components
│   └── public/                   # Images, logos, branding assets
├── nginx/
│   └── default.conf              # Production reverse proxy configuration
├── docs/
│   ├── openapi.json              # Full static OpenAPI 3.0 specification
│   ├── schema.sql                # Complete PostgreSQL 15 DDL for all 74 tables
│   ├── route_catalog.md          # 312 routes cataloged from monolith
│   ├── env_vars.md               # 75 environment variables documented
│   ├── integrations.md           # Third-party integrations architecture
│   └── state_machines.md         # Application & enrollment state machines
├── Dockerfile                    # Multi-stage production container build
├── docker-compose.yml            # Production stack (FastAPI, Postgres, Nginx)
├── docker-compose.override.yml   # Local dev overrides (hot reload, SQLite)
├── .env.example                  # Template with all environment variables
├── .env.production.sample        # Hardened production template
└── README.md                     # This documentation
```

---

## 3. Quick Start with Docker Compose

### Prerequisites
- Docker Engine 24.0+
- Docker Compose v2.20+
- 2 GB RAM minimum (4 GB recommended for PostgreSQL in production)

### Step 1: Clone or Extract the Package
```bash
cd dbert-api-package
```

### Step 2: Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your desired secrets, PostgreSQL credentials, and API keys
```

### Step 3: Launch Services
```bash
docker-compose up -d --build
```

Check the health status:
```bash
curl http://localhost:8000/health
# Response: {"status":"healthy","project":"DBERT API","version":"1.0.0"}
```

---

## 4. Database Migration Runbook (SQLite → PostgreSQL)

The package includes a comprehensive migration engine that transforms the live SQLite database (`databases/internship.db`) into PostgreSQL with strict foreign key topological ordering and sequence synchronization.

### Step 1: Ensure Target Database Schema Exists
Inside the container or python environment:
```bash
alembic upgrade head
```

### Step 2: Run the Migration ETL
```bash
python data-migration/sqlite_to_pg.py \
  --source databases/internship.db \
  --target-url postgresql://postgres:postgres@localhost:5432/dbert_db \
  --clean
```

### Step 3: Audit Parity & Integrity
```bash
python data-migration/verify_migration.py \
  --source databases/internship.db \
  --target-url postgresql://postgres:postgres@localhost:5432/dbert_db
```

Expected output:
```
Summary: 74/74 tables passed.
Total Rows: Source=46135 | Target=46135
Overall Status: [OK] PASS
```

---

## 5. API Documentation & Explorer

FastAPI automatically serves interactive API documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc UI**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Static OpenAPI JSON**: Available at `docs/openapi.json` (for Postman / Insomnia / frontend SDK generation).

---

## 6. Authentication Guide

All authenticated endpoints use standard HTTP Bearer tokens:
```http
Authorization: Bearer <your_jwt_access_token>
```

### Token Endpoints
- **Intern Login**: `POST /api/v1/auth/intern/login`
- **Company Login**: `POST /api/v1/auth/company/login`
- **Admin Login**: `POST /api/v1/auth/admin/login`
- **Mentor Login**: `POST /api/v1/auth/mentor/login`
- **Staff Login**: `POST /api/v1/auth/staff/login`
- **Token Refresh**: `POST /api/v1/auth/refresh` (accepts `{ "refresh_token": "..." }`)

---

## 7. Automated Background Cron Endpoints

All cron endpoints are mounted under `/api/v1/cron/` and protected by the `X-Cron-Secret` header:

```bash
curl -X POST http://localhost:8000/api/v1/cron/process-outbox \
  -H "X-Cron-Secret: your_cron_secret_here"
```

Configured cron tasks:
- `POST /api/v1/cron/enrollment-reminders` — Triggers automated email reminders for pending enrollments.
- `POST /api/v1/cron/cohort-reminders` — Triggers notifications 24 hours before cohort starts.
- `POST /api/v1/cron/clean-tokens` — Purges expired refresh tokens and password resets.
- `POST /api/v1/cron/process-outbox` — Dispatches pending asynchronous emails.
- `POST /api/v1/cron/expire-posts` — Moves expired job marketplace postings to draft/expired status.

---

## 8. Package Artifact Statistics

- **Zip File**: `dbert-api-package-v1.zip`
- **Total Packaged Files**: 311 files
- **Uncompressed Size**: 37.56 MB
- **Compressed Archive Size**: 8.83 MB
- **Database Snapshot**: `databases/internship.db` (33.3 MB, 74 tables, 46,135 rows)
- **API Endpoints**: 88 paths, 89 operations, OpenAPI 3.1 specification at `docs/openapi.json`

---

## 9. License & Support

DBERT Ecosystem REST Backend. Internal engineering release v1.0.0.
