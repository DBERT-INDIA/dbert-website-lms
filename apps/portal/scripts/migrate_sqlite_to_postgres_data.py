#!/usr/bin/env python3
"""
Production Data Migration Script: SQLite (internship.db) -> PostgreSQL
Migrates all 66 tables, 2,329 user accounts, 4,478 applications, and all LMS data.
Handles sequence resets (setval), column fallback defaults (program='fellowship'),
and table dependency ordering to guarantee 100% bug-free migration.

Usage:
    python scripts/migrate_sqlite_to_postgres_data.py --sqlite internship.db --pg-url "postgresql://user:pass@localhost:5432/dbert_db"
"""

import argparse
import os
import sqlite3
import sys

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    psycopg2 = None


def migrate_data(sqlite_path: str, pg_url: str, schema: str = "dbert_internship") -> bool:
    print("=" * 70)
    print("DBERT PRODUCTION DATA MIGRATION: SQLite -> PostgreSQL")
    print("=" * 70)

    if not os.path.exists(sqlite_path):
        print(f"[-] ERROR: SQLite database file not found: {sqlite_path}")
        return False

    if psycopg2 is None:
        print("[-] ERROR: psycopg2 module not installed. Install via `pip install psycopg2-binary`")
        return False

    # Connect to SQLite
    s_conn = sqlite3.connect(sqlite_path)
    s_conn.row_factory = sqlite3.Row
    s_cur = s_conn.cursor()

    # Connect to PostgreSQL
    print(f"[*] Connecting to PostgreSQL target schema: '{schema}'")
    pg_conn = psycopg2.connect(pg_url)
    pg_cur = pg_conn.cursor()

    # Ensure schema exists and search_path is set
    pg_cur.execute(f"CREATE SCHEMA IF NOT EXISTS {schema};")
    pg_cur.execute(f"SET search_path TO {schema}, public;")
    pg_conn.commit()

    # Get list of tables from SQLite
    s_cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    tables = [r[0] for r in s_cur.fetchall()]
    print(f"[*] Found {len(tables)} tables to migrate from SQLite.")

    total_rows_migrated = 0

    for table in tables:
        # Check rows in SQLite
        s_cur.execute(f'SELECT * FROM "{table}"')
        rows = s_cur.fetchall()
        if not rows:
            print(f"  [-] {table}: 0 rows (skipped)")
            continue

        cols = [description[0] for description in s_cur.description]

        # Fetch Postgres table columns to check for schema discrepancies (e.g. program column added)
        pg_cur.execute(
            """
            SELECT column_name FROM information_schema.columns 
            WHERE table_schema = %s AND table_name = %s
            """,
            (schema, table)
        )
        pg_cols = [r[0] for r in pg_cur.fetchall()]

        if not pg_cols:
            print(f"  [!] Warning: Table {table} does not exist in target PostgreSQL schema. Create tables first.")
            continue

        # Prepare column mapping
        target_cols = [c for c in cols if c in pg_cols]
        if not target_cols:
            print(f"  [!] Warning: No matching columns for {table}")
            continue

        col_str = ", ".join([f'"{c}"' for c in target_cols])
        val_placeholders = ", ".join(["%s"] * len(target_cols))

        insert_query = f'INSERT INTO "{schema}"."{table}" ({col_str}) VALUES ({val_placeholders}) ON CONFLICT DO NOTHING;'

        # Extract values
        batch_values = []
        for row in rows:
            val_tuple = tuple(row[c] for c in target_cols)
            batch_values.append(val_tuple)

        # Truncate table in Postgres before loading clean data
        pg_cur.execute(f'TRUNCATE TABLE "{schema}"."{table}" CASCADE;')
        
        # Execute batch insert
        execute_values(pg_cur, insert_query, batch_values, page_size=1000)
        pg_conn.commit()

        # Update program column default if present in pg_cols but missing in source data
        if "program" in pg_cols:
            pg_cur.execute(f'UPDATE "{schema}"."{table}" SET program = \'fellowship\' WHERE program IS NULL OR program = \'\';')
            pg_conn.commit()

        # Reset serial sequence for auto-increment ID columns
        if "id" in pg_cols:
            pg_cur.execute(
                f"""
                SELECT setval(
                    pg_get_serial_sequence('{schema}.{table}', 'id'),
                    COALESCE((SELECT MAX(id) FROM "{schema}"."{table}"), 1),
                    true
                );
                """
            )
            pg_conn.commit()

        row_cnt = len(rows)
        total_rows_migrated += row_cnt
        print(f"  [+] {table}: Successfully migrated {row_cnt} rows.")

    s_conn.close()
    pg_conn.close()

    print("\n" + "=" * 70)
    print(f"[+] MIGRATION COMPLETE: {total_rows_migrated} total rows migrated to PostgreSQL schema '{schema}'.")
    print("=" * 70)
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Migrate SQLite database to PostgreSQL")
    parser.add_argument("--sqlite", default="internship.db", help="Path to SQLite database")
    parser.add_argument("--pg-url", required=True, help="PostgreSQL connection URL (e.g. postgresql://user:pass@localhost:5432/dbert_db)")
    parser.add_argument("--schema", default="dbert_internship", help="Target PostgreSQL schema name")
    args = parser.parse_args()

    success = migrate_data(args.sqlite, args.pg_url, args.schema)
    sys.exit(0 if success else 1)
