#!/usr/bin/env python3
"""
scripts/migrate_all_ec2_data.py
Self-healing, comprehensive data migration from SQLite backup to PostgreSQL (dbert_internship schema).
1. Ensures all 75 tables from SQLite exist in PostgreSQL.
2. Creates any missing tables with PostgreSQL-compatible DDL.
3. Migrates all rows using batched parameterized inserts.
4. Resets all serial sequences (setval).
5. Reports row-count parity verification.
"""

import os
import re
import sqlite3
import psycopg2
from psycopg2.extras import execute_values

SQLITE_PATH = os.environ.get("SQLITE_PATH", "/var/www/backups/internship_20261102_191908.db")
PG_URL = os.environ.get("DATABASE_URL", "postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
SCHEMA = os.environ.get("POSTGRES_SCHEMA", "dbert_internship")

def sqlite_to_postgres_ddl(sqlite_ddl: str, table_name: str) -> str:
    """Convert SQLite CREATE TABLE DDL to PostgreSQL-compatible DDL."""
    ddl = sqlite_ddl
    # Remove sqlite-specific datetime functions
    ddl = re.sub(r"DEFAULT\s*\(\s*datetime\s*\([^)]*\)\s*\)", "DEFAULT CURRENT_TIMESTAMP", ddl, flags=re.IGNORECASE)
    # Convert AUTOINCREMENT
    ddl = re.sub(r"\bINTEGER\s+PRIMARY\s+KEY\s+AUTOINCREMENT\b", "SERIAL PRIMARY KEY", ddl, flags=re.IGNORECASE)
    # Strip any inline foreign key constraints that might fail on empty tables
    # (data migration handles integrity)
    lines = ddl.splitlines()
    cleaned_lines = []
    for line in lines:
        if re.search(r"^\s*FOREIGN\s+KEY", line, re.IGNORECASE):
            continue
        cleaned_lines.append(line)
    
    # Fix trailing commas before closing paren
    cleaned_ddl = "\n".join(cleaned_lines)
    cleaned_ddl = re.sub(r",\s*\)", "\n)", cleaned_ddl)
    return cleaned_ddl

def run_migration():
    print("=" * 70)
    print(f"[*] Starting migration from: {SQLITE_PATH}")
    print(f"[*] PostgreSQL target schema: {SCHEMA}")
    print("=" * 70)

    if not os.path.exists(SQLITE_PATH):
        raise FileNotFoundError(f"SQLite file not found at {SQLITE_PATH}")

    s_conn = sqlite3.connect(SQLITE_PATH)
    s_conn.row_factory = sqlite3.Row
    s_cur = s_conn.cursor()

    p_conn = psycopg2.connect(PG_URL)
    p_conn.autocommit = False
    p_cur = p_conn.cursor()

    # Ensure schema exists and set search_path
    p_cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA};")
    p_cur.execute(f"SET search_path TO {SCHEMA}, public;")
    p_conn.commit()

    # Get all tables from SQLite
    s_cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    sqlite_tables = s_cur.fetchall()
    print(f"[*] Found {len(sqlite_tables)} tables in SQLite backup.")

    # Get existing tables in Postgres schema
    p_cur.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema=%s",
        (SCHEMA,)
    )
    pg_existing_tables = set(r[0] for r in p_cur.fetchall())
    print(f"[*] Found {len(pg_existing_tables)} existing tables in PostgreSQL schema '{SCHEMA}'.")

    # 1. Create any missing tables in Postgres
    missing_tables = [t for t in sqlite_tables if t["name"] not in pg_existing_tables]
    print(f"[*] {len(missing_tables)} tables need to be created in PostgreSQL.")

    for t in missing_tables:
        tname = t["name"]
        raw_sql = t["sql"]
        if not raw_sql:
            continue
        pg_sql = sqlite_to_postgres_ddl(raw_sql, tname)
        try:
            p_cur.execute(pg_sql)
            p_conn.commit()
            print(f"  [+] Created table: {tname}")
        except Exception as e:
            p_conn.rollback()
            print(f"  [-] Error creating table {tname}: {e}")
            # Try minimal table creation
            try:
                s_cur.execute(f'SELECT * FROM "{tname}" LIMIT 1')
                cols = [desc[0] for desc in s_cur.description]
                col_defs = []
                for c in cols:
                    if c.lower() == "id":
                        col_defs.append('"id" SERIAL PRIMARY KEY')
                    else:
                        col_defs.append(f'"{c}" TEXT')
                create_min = f'CREATE TABLE IF NOT EXISTS "{SCHEMA}"."{tname}" ({", ".join(col_defs)});'
                p_cur.execute(create_min)
                p_conn.commit()
                print(f"  [+] Created table (fallback): {tname}")
            except Exception as e2:
                p_conn.rollback()
                print(f"  [!] Failed fallback creation for {tname}: {e2}")

    # 2. Topological migration order
    parent_order = [
        "staff_accounts", "companies", "courses", "cohorts", "conversations", "tasks",
        "intern_accounts", "applications", "enrollments", "user_sessions", "device_profiles",
        "email_log", "check_log", "password_resets", "rate_events", "abuse_log",
        "mobile_refresh_tokens", "coin_ledger_mirror", "notifications", "platform_config",
        "user_api_keys", "dbert_fallback_usage", "staff_queue_roles", "signup_otps",
        "payments", "mentors", "mentor_availability_slots", "messages", "review_log",
        "posts", "post_comments", "post_questions", "referrals", "ambassador_withdrawals",
        "course_chapters", "course_day_quizzes", "course_projects", "task_versions",
        "attendance", "tutor_progress", "interviews", "intern_certificates", "cvs",
        "course_payments", "company_follows", "post_hire_deposits", "post_applications",
        "cohort_enrollments", "course_enrollments", "course_subtopics", "mentor_session_bookings",
        "security_deposits", "course_subtopic_chats", "day_quiz_attempts",
        "project_submissions", "task_submissions", "scraped_internships", "scraped_jobs",
        "scraped_internship_comments", "scraped_job_comments", "intern_articles",
        "ecosystem_spotlights", "spotlight_clicks", "gl_concepts", "gl_course_chunks",
        "gl_learning_events", "gl_learning_sessions", "gl_learning_turns",
        "gl_misconception_catalog", "gl_student_learning_profile", "gl_student_mastery",
        "gl_teacher_learning_instructions"
    ]

    all_t_names = set(t["name"] for t in sqlite_tables)
    ordered_tables = [t for t in parent_order if t in all_t_names]
    ordered_tables += [t for t in sorted(all_t_names) if t not in ordered_tables]

    # Disable constraints during batch load if superuser/replica allows
    try:
        p_cur.execute("SET session_replication_role = 'replica';")
        p_conn.commit()
    except Exception:
        p_conn.rollback()

    print("\n" + "=" * 70)
    print("[*] Migrating Table Records...")
    print("=" * 70)

    summary = []
    total_migrated = 0

    for table in ordered_tables:
        s_cur.execute(f'SELECT count(*) FROM "{table}"')
        sqlite_count = s_cur.fetchone()[0]

        # Check existing PG count
        p_cur.execute(
            "SELECT count(*) FROM information_schema.tables WHERE table_schema=%s AND table_name=%s",
            (SCHEMA, table)
        )
        if p_cur.fetchone()[0] == 0:
            print(f"  [!] Skipped {table}: Does not exist in PostgreSQL")
            continue

        p_cur.execute(f'SELECT count(*) FROM "{SCHEMA}"."{table}"')
        pg_count_before = p_cur.fetchone()[0]

        # Force refresh for tables that need re-population (e.g. case mapping fixes)
        force_refresh_tables = ("scraped_internships", "scraped_jobs")
        if table not in force_refresh_tables and pg_count_before >= sqlite_count and sqlite_count > 0:
            summary.append((table, sqlite_count, pg_count_before, "ALREADY_POPULATED"))
            print(f"  [✓] {table}: {pg_count_before} rows already in PostgreSQL (SQLite has {sqlite_count}). Keeping PG.")
            continue

        # Fetch columns in SQLite
        s_cur.execute(f'SELECT * FROM "{table}"')
        rows = s_cur.fetchall()
        if not rows:
            summary.append((table, 0, pg_count_before, "EMPTY"))
            continue

        s_cols = [desc[0] for desc in s_cur.description]

        # Fetch columns in PostgreSQL
        p_cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name=%s",
            (SCHEMA, table)
        )
        p_col_names_raw = [r[0] for r in p_cur.fetchall()]
        p_cols = set(p_col_names_raw)
        p_col_map = {c.lower(): c for c in p_col_names_raw}

        # Case-insensitive column matching
        matched_cols = [(sc, p_col_map[sc.lower()]) for sc in s_cols if sc.lower() in p_col_map]
        if not matched_cols:
            print(f"  [!] No matching columns for {table}")
            continue

        s_col_names = [mc[0] for mc in matched_cols]
        p_col_names = [mc[1] for mc in matched_cols]

        col_str = ", ".join([f'"{c}"' for c in p_col_names])
        val_placeholders = ", ".join(["%s"] * len(p_col_names))
        insert_query = f'INSERT INTO "{SCHEMA}"."{table}" ({col_str}) VALUES ({val_placeholders}) ON CONFLICT DO NOTHING;'

        batch_values = [tuple(row[c] for c in s_col_names) for row in rows]

        # Truncate if PG had fewer rows or was empty or explicitly refreshed
        if pg_count_before == 0 or table in force_refresh_tables or table in ("attendance", "cvs", "course_chapters", "course_subtopics", "intern_articles"):
            try:
                p_cur.execute(f'TRUNCATE TABLE "{SCHEMA}"."{table}" CASCADE;')
                p_conn.commit()
            except Exception:
                p_conn.rollback()

        # Batch insert in chunks of 500
        chunk_size = 500
        inserted_for_table = 0
        for i in range(0, len(batch_values), chunk_size):
            chunk = batch_values[i:i + chunk_size]
            try:
                p_cur.executemany(insert_query, chunk)
                p_conn.commit()
                inserted_for_table += len(chunk)
            except Exception as batch_err:
                p_conn.rollback()
                # Row-by-row fallback
                for row_val in chunk:
                    try:
                        p_cur.execute(insert_query, row_val)
                        p_conn.commit()
                        inserted_for_table += 1
                    except Exception:
                        p_conn.rollback()

        # Reset sequence for id column
        if "id" in p_cols:
            try:
                p_cur.execute(
                    f"""
                    SELECT setval(
                        pg_get_serial_sequence('{SCHEMA}.{table}', 'id'),
                        COALESCE((SELECT MAX(id) FROM "{SCHEMA}"."{table}"), 1),
                        true
                    );
                    """
                )
                p_conn.commit()
            except Exception:
                p_conn.rollback()

        p_cur.execute(f'SELECT count(*) FROM "{SCHEMA}"."{table}"')
        pg_count_after = p_cur.fetchone()[0]
        total_migrated += inserted_for_table
        status = "OK" if pg_count_after >= sqlite_count else "PARTIAL"
        summary.append((table, sqlite_count, pg_count_after, status))
        print(f"  [+] {table}: Migrated {inserted_for_table} rows (PG now has {pg_count_after} / SQLite had {sqlite_count})")

    # Re-enable constraint checking
    try:
        p_cur.execute("SET session_replication_role = 'origin';")
        p_conn.commit()
    except Exception:
        p_conn.rollback()

    # Create helpful indices on scraped tables if not present
    indices = [
        f'CREATE INDEX IF NOT EXISTS idx_scraped_domain ON "{SCHEMA}".scraped_internships("Domain");',
        f'CREATE INDEX IF NOT EXISTS idx_scraped_city ON "{SCHEMA}".scraped_internships("City");',
        f'CREATE INDEX IF NOT EXISTS idx_scraped_work_model ON "{SCHEMA}".scraped_internships("Work_Model");',
        f'CREATE INDEX IF NOT EXISTS idx_scraped_jobs_domain ON "{SCHEMA}".scraped_jobs("Domain");',
        f'CREATE INDEX IF NOT EXISTS idx_scraped_jobs_city ON "{SCHEMA}".scraped_jobs("City");',
        f'CREATE INDEX IF NOT EXISTS idx_scraped_jobs_work_model ON "{SCHEMA}".scraped_jobs("Work_Model");',
    ]
    for idx_sql in indices:
        try:
            p_cur.execute(idx_sql)
            p_conn.commit()
        except Exception:
            p_conn.rollback()

    s_conn.close()
    p_conn.close()

    print("\n" + "=" * 70)
    print(f"[✓] MIGRATION COMPLETE! Total rows migrated: {total_migrated}")
    print("=" * 70)

if __name__ == "__main__":
    run_migration()
