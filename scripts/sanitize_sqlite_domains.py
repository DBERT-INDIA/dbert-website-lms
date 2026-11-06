"""
Sanitize SQLite databases for legacy domain references.
Replaces:
- 'internship.dbert.online' -> 'lms.dbert.in'
- '@dbert.online' -> '@dbert.in'
- 'dbert.online' -> 'dbert.in'
across all text columns in root internship.db and apps/portal/internship.db.
"""

import sqlite3
import os

DB_PATHS = [
    os.path.abspath('internship.db'),
    os.path.abspath('apps/portal/internship.db'),
    os.path.abspath('dbert-api-package/databases/internship.db')
]

def sanitize_db(db_path):
    if not os.path.exists(db_path):
        print(f"Skipping {db_path} (does not exist)")
        return

    print(f"\n--- Sanitizing {db_path} ---")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Pre-step for apps/portal/internship.db: Handle duplicate staff_accounts if superadmin already migrated
    try:
        cur.execute("SELECT id FROM staff_accounts WHERE email = 'dbert_superadmin@dbert.in'")
        row6 = cur.fetchone()
        cur.execute("SELECT id FROM staff_accounts WHERE email = 'dbert_superadmin@dbert.online'")
        row5 = cur.fetchone()
        if row6 and row5:
            id5 = row5[0]
            print(f"Resolving duplicate superadmin accounts (id {id5} -> migrated id {row6[0]})")
            cur.execute("DELETE FROM staff_queue_roles WHERE staff_id = ?", (id5,))
            cur.execute("DELETE FROM staff_accounts WHERE id = ?", (id5,))
            conn.commit()
    except Exception as e:
        print(f"Note on staff_accounts duplicate check: {e}")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall() if not r[0].startswith('sqlite_')]

    total_updated = 0
    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        columns = [c[1] for c in cur.fetchall()]

        for col in columns:
            try:
                cur.execute(f"SELECT COUNT(*) FROM [{table}] WHERE [{col}] LIKE '%dbert.online%'")
                count = cur.fetchone()[0]
                if count > 0:
                    print(f"Found {count} rows in {table}.{col} with 'dbert.online'")
                    
                    # 1. Replace internship.dbert.online with lms.dbert.in
                    cur.execute(f"""
                        UPDATE [{table}]
                        SET [{col}] = REPLACE([{col}], 'internship.dbert.online', 'lms.dbert.in')
                        WHERE [{col}] LIKE '%internship.dbert.online%'
                    """)

                    # 2. Replace remaining dbert.online with dbert.in
                    cur.execute(f"""
                        UPDATE [{table}]
                        SET [{col}] = REPLACE([{col}], 'dbert.online', 'dbert.in')
                        WHERE [{col}] LIKE '%dbert.online%'
                    """)

                    conn.commit()
                    total_updated += count

                    # Verify no dbert.online remains
                    cur.execute(f"SELECT COUNT(*) FROM [{table}] WHERE [{col}] LIKE '%dbert.online%'")
                    remaining = cur.fetchone()[0]
                    print(f"  Updated {table}.{col}. Remaining legacy occurrences: {remaining}")
            except sqlite3.OperationalError:
                pass

    conn.close()
    print(f"Finished {db_path}: {total_updated} rows sanitized.")

if __name__ == '__main__':
    for p in DB_PATHS:
        sanitize_db(p)
