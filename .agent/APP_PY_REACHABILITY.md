# app.py Reachability & Dependency Graph

**Date:** 2026-09-25  
**Target:** `apps/portal/app.py` (~15,800+ lines)

## Architectural Layer Classification

### 1. Application Bootstrap Layer (`BOOTSTRAP`)
- `create_app()` / App instantiation & extension init (`Flask(__name__)`, CORS, CSRFProtect, Limiter)
- Database connection lifecycle (`get_db()`, `close_db()`, `init_db()`)
- Blueprint registrations (`auth_bp`, `admin_bp`, `intern_bp`, `applications_bp`, `enrollment_bp`, `learning_bp`, `payment_bp`, `mentor_bp`, `company_bp`, `ambassador_bp`, `marketplace_bp`)
- Core error handlers (`bad_request`, `unauthorized`, `forbidden`, `not_found`, `internal_server_error`, `request_entity_too_large`)
- Security middleware & security response headers (`_security_headers()`)
- Process health probes (`/health`, `/ready`)

### 2. Extracted Modular Services (Active in `services/` & `routes/`)
- **Database Abstraction:** `apps/portal/services/database/` (`adapter.py`, `schema_translator.py`, `connection_pool.py`)
- **Auth & Identity Service:** `apps/portal/services/auth_service.py` & `routes/auth.py`
- **Application Workflow Service:** `apps/portal/services/application_service.py` & `routes/applications.py`
- **Enrollment & Payment Service:** `apps/portal/services/enrollment_service.py`, `payment_service.py`, `routes/payment.py`
- **Guided Learning Engine:** `apps/portal/services/learning/` & `routes/learning.py`
- **Outbox & Notification Service:** `apps/portal/services/outbox_service.py`, `notification_service.py`
- **File Security & Upload Sandbox:** `apps/portal/services/file_security_service.py`

### 3. Active Business Logic Remaining in `app.py` (`ACTIVE_BUSINESS_LOGIC`)
- `init_db()` fallback schema initialization & SQLite PRAGMA execution (Target for Phase 2 & Phase 3)
- Legacy direct `_send()` / `_smtp_send_raw()` helper routines (Target for Phase 5 & Phase 6)
- Monolithic administrative helper handlers & inline CSV parsing (`_csv_import_logic`, `admin_upload_csv`)
- Inline course catalog filtering (`courses_catalog()`)

### 4. Legacy / Duplicate Logic Candidates (`DUPLICATE` / `LEGACY`)
- Direct SQLite query helper methods duplicated in `app.py` that have extracted equivalents in `services/database/adapter.py`
- `_legacy_internship_root()`, `_legacy_internship_redirect()`
