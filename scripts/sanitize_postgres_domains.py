#!/usr/bin/env python3
"""
scripts/sanitize_postgres_domains.py
Sanitize PostgreSQL database on EC2 for legacy domain references.
Replaces:
- 'internship.dbert.online' -> 'lms.dbert.in'
- '@dbert.online' -> '@dbert.in'
- 'dbert.online' -> 'dbert.in'
across all text/varchar columns in schema 'dbert_internship' and 'public'.
"""

import os
import psycopg2
from psycopg2 import sql

PG_URL = os.environ.get("DATABASE_URL", "postgresql://dbert_user:19d0b2647ef39526fa3fafff9f594026639ec2865c73d753@localhost:5432/dbert_lms")
SCHEMAS = ["dbert_internship", "public"]

def run_postgres_sanitization():
    print("=" * 70)
    print(f"[*] Connecting to PostgreSQL: {PG_URL.split('@')[-1]}")
    print("=" * 70)

    conn = psycopg2.connect(PG_URL)
    conn.autocommit = True
    cur = conn.cursor()

    total_scanned_columns = 0
    total_matches_found = 0
    total_updated_rows = 0

    for schema in SCHEMAS:
        # Check if schema exists
        cur.execute("SELECT 1 FROM information_schema.schemata WHERE schema_name = %s;", (schema,))
        if not cur.fetchone():
            print(f"[-] Schema {schema} does not exist, skipping.")
            continue

        print(f"\n[*] Scanning schema: {schema}")

        # Handle potential duplicate staff_accounts in schema
        try:
            cur.execute(sql.SQL("""
                SELECT id FROM {}.staff_accounts WHERE email = 'dbert_superadmin@dbert.in';
            """).format(sql.Identifier(schema)))
            row_in = cur.fetchone()
            cur.execute(sql.SQL("""
                SELECT id FROM {}.staff_accounts WHERE email = 'dbert_superadmin@dbert.online';
            """).format(sql.Identifier(schema)))
            row_online = cur.fetchone()

            if row_in and row_online:
                id_online = row_online[0]
                print(f"[!] Resolving duplicate superadmin accounts in {schema}.staff_accounts (id {id_online} -> migrated id {row_in[0]})")
                try:
                    cur.execute(sql.SQL("DELETE FROM {}.staff_queue_roles WHERE staff_id = %s;").format(sql.Identifier(schema)), (id_online,))
                except Exception:
                    pass
                cur.execute(sql.SQL("DELETE FROM {}.staff_accounts WHERE id = %s;").format(sql.Identifier(schema)), (id_online,))
                print(f"[+] Cleaned up duplicate superadmin id {id_online}")
        except Exception as e:
            # Table may not exist or column not present
            pass

        # Find all textual columns in this schema
        cur.execute("""
            SELECT table_name, column_name, data_type 
            FROM information_schema.columns 
            WHERE table_schema = %s 
              AND data_type IN ('text', 'character varying', 'character')
            ORDER BY table_name, column_name;
        """, (schema,))
        columns = cur.fetchall()

        for table_name, column_name, data_type in columns:
            total_scanned_columns += 1
            query_count = sql.SQL("""
                SELECT COUNT(*) FROM {}.{} 
                WHERE {} LIKE '%dbert.online%';
            """).format(
                sql.Identifier(schema),
                sql.Identifier(table_name),
                sql.Identifier(column_name)
            )
            try:
                cur.execute(query_count)
                count = cur.fetchone()[0]
                if count > 0:
                    total_matches_found += count
                    print(f"  [FOUND] {schema}.{table_name}.{column_name}: {count} matching row(s)")

                    # Step 1: Replace internship.dbert.online -> lms.dbert.in
                    query_upd1 = sql.SQL("""
                        UPDATE {}.{} 
                        SET {} = REPLACE({}, 'internship.dbert.online', 'lms.dbert.in')
                        WHERE {} LIKE '%internship.dbert.online%';
                    """).format(
                        sql.Identifier(schema),
                        sql.Identifier(table_name),
                        sql.Identifier(column_name),
                        sql.Identifier(column_name),
                        sql.Identifier(column_name)
                    )
                    cur.execute(query_upd1)
                    upd1 = cur.rowcount

                    # Step 2: Replace remaining dbert.online -> dbert.in
                    query_upd2 = sql.SQL("""
                        UPDATE {}.{} 
                        SET {} = REPLACE({}, 'dbert.online', 'dbert.in')
                        WHERE {} LIKE '%dbert.online%';
                    """).format(
                        sql.Identifier(schema),
                        sql.Identifier(table_name),
                        sql.Identifier(column_name),
                        sql.Identifier(column_name),
                        sql.Identifier(column_name)
                    )
                    cur.execute(query_upd2)
                    upd2 = cur.rowcount

                    print(f"    -> Updated: {upd1} rows (internship subdomain), {upd2} rows (root/other)")
                    total_updated_rows += (upd1 + upd2)
            except Exception as e:
                print(f"  [ERROR] querying {schema}.{table_name}.{column_name}: {e}")

    print("\n" + "=" * 70)
    print(f"[+] SUMMARY: Scanned {total_scanned_columns} columns.")
    print(f"[+] Matches found: {total_matches_found}")
    print(f"[+] Total row updates: {total_updated_rows}")
    print("=" * 70)

    cur.close()
    conn.close()

if __name__ == "__main__":
    run_postgres_sanitization()
