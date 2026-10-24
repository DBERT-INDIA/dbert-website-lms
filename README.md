# DBERT Website & LMS Ecosystem

Welcome to the **DBERT (Digital Blaize Ecosystem for Research & Training)** platform repository.

---

## 🚀 Repository Highlights

This repository contains the complete ecosystem codebase, including the modernized **FastAPI + PostgreSQL REST API**, the database migration engine, documentation, and the legacy portal and website applications:

```
.
├── dbert-api-package/             ← PRODUCTION REST API (FastAPI, PostgreSQL 15, Docker)
│   ├── backend/                   ← 88 REST endpoints, SQLAlchemy 2.0 ORM, JWT auth
│   ├── data-migration/            ← SQLite to PostgreSQL ETL & parity auditor
│   ├── databases/                 ← Target folder for internship.db
│   ├── website-content/           ← Clean Next.js marketing content snapshot
│   ├── docs/                      # OpenAPI 3.1 JSON, schema.sql, handover spec
│   ├── nginx/                     ← Production reverse proxy configuration
│   ├── Dockerfile                 ← Multi-stage production container build
│   ├── docker-compose.yml         ← Complete stack (FastAPI, Postgres, Nginx)
│   ├── .env.example               ← Complete environment variable reference
│   └── README.md                  ← Detailed API deployment runbook
├── apps/
│   ├── portal/                    ← Legacy Flask monolith (Reference source)
│   └── website/                   ← Next.js marketing website (Reference source)
└── README.md                      ← This repository guide
```

---

## ⚡ Modern REST Backend: `dbert-api-package`

The core backend has been rebuilt from the monolithic Flask + SQLite codebase into a modern, decoupled **FastAPI + PostgreSQL REST API** ready for Docker Compose deployment.

### Key Capabilities
- **FastAPI (Python 3.11+)**: Async I/O, Pydantic v2 schemas, automated interactive Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **PostgreSQL 15**: All 74 database tables ported from SQLite with full foreign key graphs, indices, and Alembic migrations.
- **Authentication**: Dual-token JWT (HS256) access (1h) and refresh tokens (60d) with cryptographic JTI rotation across 5 roles: `intern`, `company`, `mentor`, `staff`, `admin`. Legacy SHA-256 passwords transparently upgrade to PBKDF2 upon login.
- **Data Migration Suite**: `data-migration/sqlite_to_pg.py` and `data-migration/verify_migration.py` tested with 100% row match (46,135 rows across all 74 tables).
- **Core Integrations**: Async Razorpay checkout/webhook verification, Google Gemini AI interview engine with round-robin key rotation and cooling periods, OneSignal push notifications, and transaction-safe SMTP outbox.

### Quick Start with Docker
```bash
cd dbert-api-package
cp .env.example .env
docker-compose up -d --build
curl http://localhost:8000/health
```

---

## 📚 Documentation & Specifications

- **Interactive API Documentation**: Run the container and visit `http://localhost:8000/docs`
- **Static OpenAPI 3.1 Spec**: `dbert-api-package/docs/openapi.json`
- **Frontend AI Agent Handover Guide**: `dbert-api-package/docs/FRONTEND_HANDOVER_SPECIFICATION.md`
- **PostgreSQL DDL (74 Tables)**: `dbert-api-package/docs/schema.sql`
- **Route Catalog (312 Monolith Routes)**: `dbert-api-package/docs/route_catalog.md`
- **Environment Variables**: `dbert-api-package/docs/env_vars.md`
- **State Machines**: `dbert-api-package/docs/state_machines.md`

---

## 🔒 Security Notice

Per security protocols, live SQLite database files (`*.db`) and sensitive production `.env` files are strictly excluded via `.gitignore` and retained on local environments only. Refer to `.env.example` and `.env.production.sample` for configuration templates.
