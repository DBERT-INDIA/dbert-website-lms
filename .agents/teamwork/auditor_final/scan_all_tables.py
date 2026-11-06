import sqlite3
import glob
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== THOROUGH SCAN ACROSS ALL TABLES FOR TARGET RECIPIENTS IN ALL DATABASES ===")
dbs = glob.glob("**/*.db", recursive=True)

targets = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com", "ain.sharma", "ajnatechrpa"]

for db in dbs:
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        for table in tables:
            cur.execute(f"PRAGMA table_info({table})")
            cols = [r[1] for r in cur.fetchall()]
            for target in targets:
                # search text columns
                where_clauses = [f'"{c}" LIKE ?' for c in cols]
                if not where_clauses:
                    continue
                q = f"SELECT * FROM \"{table}\" WHERE {' OR '.join(where_clauses)}"
                params = [f"%{target}%"] * len(cols)
                try:
                    cur.execute(q, params)
                    rows = cur.fetchall()
                    if rows:
                        for row in rows:
                            row_str = str(row)
                            if "2026-11" in row_str:
                                print(f"MATCH IN {db} table {table} (NOV 2026): {row}")
                except Exception:
                    pass
        conn.close()
    except Exception as e:
        print(f"Error {db}: {e}")

print("Scan complete. If no 'MATCH IN ... (NOV 2026)' appeared above, then ZERO records exist for target recipients in Nov 2026.")
