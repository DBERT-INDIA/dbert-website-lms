# SQLite Retirement & Migration Report

**Date:** 2026-09-25  
**Project:** DBERT LMS  
**Target:** Legacy SQLite (`apps/portal/internship.db`) Retirement

---

## 1. Migration Verification Summary

- **SQLite Database File:** `apps/portal/internship.db`
- **Current Runtime DB Engine:** PostgreSQL (`PostgreSQLAdapter`)
- **Runtime Fallback Status:** **Disabled**. `get_db_adapter()` in `apps/portal/services/database/adapter.py` raises `RuntimeError` when `REQUIRE_POSTGRES=true` or in `FLASK_ENV=production`.
- **Migration Script:** `apps/portal/scripts/migrate_sqlite_to_postgres_data.py` (migrates all tables, user accounts, applications, sequences, and defaults).

---

## 2. Table & Schema Parity Checklist

| Domain | SQLite Parity Verified | PostgreSQL Schema Target |
|--------|------------------------|--------------------------|
| User & Intern Accounts | Verified | `dbert_internship.intern_accounts` |
| Applications | Verified | `dbert_internship.applications` |
| Enrollments | Verified | `dbert_internship.enrollments` |
| Courses & Quizzes | Verified | `dbert_internship.courses` |
| Payments & Transactions | Verified | `dbert_internship.course_payments` |
| Attendance & Telemetry | Verified | `dbert_internship.attendance_logs` |

---

## 3. Artifact & Script Deletion Policy

- `apps/portal/internship.db` has been retired from production runtime.
- Deployment scripts (`deploy/deploy_ec2.sh`) run automated PostgreSQL schema initialization and data migration engine prior to startup.
- `.gitignore` ensures `*.db`, `*.sqlite`, `*.sqlite3` and `internship.db` are strictly excluded from repository commits.
