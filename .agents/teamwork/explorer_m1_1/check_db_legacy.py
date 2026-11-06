import sqlite3
import os

for db_path in ['internship.db', 'apps/portal/internship.db']:
    if not os.path.exists(db_path):
        continue
    print(f"=== Database: {db_path} ===")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for (tname,) in tables:
        try:
            cols = [col[1] for col in cursor.execute(f"PRAGMA table_info('{tname}');").fetchall()]
            for c in cols:
                try:
                    q = f"SELECT count(*) FROM '{tname}' WHERE \"{c}\" LIKE '%dbert.online%';"
                    res = cursor.execute(q).fetchone()[0]
                    if res > 0:
                        print(f"  Table: {tname}, Column: {c} -> {res} matching rows")
                        # Show sample
                        s_q = f"SELECT \"{c}\" FROM '{tname}' WHERE \"{c}\" LIKE '%dbert.online%' LIMIT 2;"
                        samples = cursor.execute(s_q).fetchall()
                        for s in samples:
                            val = str(s[0])
                            if len(val) > 120:
                                val = val[:120] + "..."
                            print(f"    Sample: {val}")
                except Exception:
                    pass
        except Exception:
            pass
    conn.close()
