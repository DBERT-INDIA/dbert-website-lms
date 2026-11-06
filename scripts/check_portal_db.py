import sqlite3
import os

db_path = os.path.join('apps', 'portal', 'internship.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='intern_certificates'")
    res = cur.fetchone()
    print("intern_certificates schema:")
    print(res[0] if res else "Table not found")
    if res:
        cur.execute("SELECT COUNT(*) FROM intern_certificates")
        print("Current count:", cur.fetchone()[0])
        cur.execute("SELECT * FROM intern_certificates LIMIT 3")
        rows = cur.fetchall()
        print("Sample rows:", rows)
else:
    print(f"{db_path} does not exist")
