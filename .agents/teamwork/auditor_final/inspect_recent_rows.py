import sqlite3
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite3.connect("apps/portal/internship.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("SELECT * FROM email_log WHERE id >= 6745 ORDER BY id ASC")
rows = cur.fetchall()
print(f"Total rows with id >= 6745: {len(rows)}")
for r in rows:
    print(dict(r))

conn.close()
