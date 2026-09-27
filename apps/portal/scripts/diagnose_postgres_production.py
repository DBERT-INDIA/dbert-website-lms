#!/usr/bin/env python3
"""
Production PostgreSQL Diagnostic Script for DBERT LMS.

Usage:
    cd /var/www/dbert-website-lms/apps/portal
    source .venv/bin/activate
    python scripts/diagnose_postgres_production.py

Exit codes:
    0 = healthy
    1 = warnings (investigate but not blocking)
    2 = critical (do not deploy / restart)
"""
import os
import sys

def main():
    db_url = os.environ.get("DATABASE_URL", "")
    schema = os.environ.get("POSTGRES_SCHEMA", "dbert_internship")

    if not db_url.startswith(("postgresql://", "postgres://")):
        print("[CRITICAL] DATABASE_URL is not set or not a PostgreSQL URL.")
        print(f"  DATABASE_URL={db_url!r}")
        sys.exit(2)

    try:
        import psycopg2
    except ImportError:
        print("[CRITICAL] psycopg2 not installed. Run: pip install psycopg2-binary")
        sys.exit(2)

    exit_code = 0

    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # 1. Connection identity
        cur.execute("SELECT current_database(), current_schema(), current_setting('search_path'), version()")
        db, cur_schema, search_path, version = cur.fetchone()
        print("── Connection ────────────────────────────────────")
        print(f"  database      : {db}")
        print(f"  current_schema: {cur_schema}")
        print(f"  search_path   : {search_path}")
        print(f"  configured    : {schema}")
        print(f"  server        : {version.split(',')[0]}")
        print()

        # 2. Set correct schema
        cur.execute(f"SET search_path TO {schema}, public")

        # 3. Table locations
        cur.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name IN ('intern_accounts','course_enrollments','courses')
            ORDER BY table_schema, table_name
        """)
        rows = cur.fetchall()
        print("── Table Locations ───────────────────────────────")
        schemas_with_table = {}
        for schema_name, table_name in rows:
            print(f"  {schema_name}.{table_name}")
            schemas_with_table.setdefault(table_name, []).append(schema_name)

        for tbl, schema_list in schemas_with_table.items():
            if len(schema_list) > 1:
                print(f"  [WARNING] '{tbl}' exists in multiple schemas: {schema_list}")
                exit_code = max(exit_code, 1)
        print()

        # 4. FK constraint targets
        cur.execute("""
            SELECT
                n.nspname AS schema,
                c.conname,
                c.conrelid::regclass AS child,
                c.confrelid::regclass AS referenced,
                pg_get_constraintdef(c.oid) AS definition
            FROM pg_constraint c
            JOIN pg_namespace n ON n.oid = c.connamespace
            WHERE c.conname IN (
                'course_enrollments_intern_id_fkey',
                'course_enrollments_course_id_fkey'
            )
        """)
        fk_rows = cur.fetchall()
        print("── Foreign Key Constraints ───────────────────────")
        if not fk_rows:
            print("  [CRITICAL] course_enrollments FK constraints NOT FOUND!")
            exit_code = 2
        for fk_schema, conname, child, referenced, defn in fk_rows:
            print(f"  {conname}")
            print(f"    child      : {child}")
            print(f"    referenced : {referenced}")
            print(f"    definition : {defn}")
            if schema not in str(referenced):
                print(f"  [WARNING] FK references {referenced!r} — expected schema {schema!r}")
                exit_code = max(exit_code, 1)
        print()

        # 5. Column type check
        cur.execute("""
            SELECT table_schema, table_name, column_name, data_type
            FROM information_schema.columns
            WHERE (table_name = 'intern_accounts' AND column_name = 'id')
               OR (table_name = 'course_enrollments' AND column_name IN ('id','intern_id','course_id'))
               OR (table_name = 'courses' AND column_name = 'id')
            ORDER BY table_name, column_name
        """)
        col_rows = cur.fetchall()
        print("── Column Types ──────────────────────────────────")
        for tbl_schema, tbl, col, dtype in col_rows:
            print(f"  {tbl_schema}.{tbl}.{col}: {dtype}")
        print()

        # 6. Orphan enrollment count
        try:
            cur.execute(f"""
                SELECT COUNT(*)
                FROM {schema}.course_enrollments ce
                LEFT JOIN {schema}.intern_accounts ia ON ia.id = ce.intern_id
                WHERE ia.id IS NULL
            """)
            orphan_count = cur.fetchone()[0]
            print("── Orphan Enrollments ────────────────────────────")
            print(f"  Orphan course_enrollments rows: {orphan_count}")
            if orphan_count > 0:
                print(f"  [CRITICAL] {orphan_count} orphan rows will cause FK violations!")
                exit_code = 2
            print()
        except Exception as e:
            print(f"  [WARNING] Could not check orphan enrollments: {e}")
            exit_code = max(exit_code, 1)

        # 7. Sequence sanity
        print("── Sequence Values ───────────────────────────────")
        for tbl in ['intern_accounts', 'course_enrollments', 'courses']:
            try:
                cur.execute(f"SELECT MAX(id) FROM {schema}.{tbl}")
                max_id = cur.fetchone()[0] or 0
                cur.execute(f"SELECT last_value FROM pg_sequences WHERE sequencename = '{tbl}_id_seq'")
                row = cur.fetchone()
                last_val = row[0] if row else "unknown"
                print(f"  {tbl}: max_id={max_id}, sequence_last={last_val}")
                if isinstance(last_val, int) and last_val < max_id:
                    print(f"  [CRITICAL] Sequence for {tbl} is BEHIND max id! Run setval().")
                    exit_code = 2
            except Exception as e:
                print(f"  [WARNING] Could not check sequence for {tbl}: {e}")
        print()

        cur.close()
        conn.close()

        # Summary
        print("── Result ────────────────────────────────────────")
        labels = {0: "HEALTHY", 1: "WARNINGS (investigate)", 2: "CRITICAL (do not deploy)"}
        print(f"  Status: {labels.get(exit_code, 'UNKNOWN')}")
        sys.exit(exit_code)

    except Exception as e:
        print(f"[CRITICAL] Could not connect to database: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
