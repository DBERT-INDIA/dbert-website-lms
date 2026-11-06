import sqlite3

db_path = 'apps/portal/internship.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in c.fetchall()]
print(f"=== {db_path} ===")
for t in tables:
    c.execute(f"SELECT count(*) FROM {t}")
    cnt = c.fetchone()[0]
    print(f"  {t}: {cnt} rows")

print("\nColumns in tables:")
for t in tables:
    c.execute(f"PRAGMA table_info({t});")
    cols = [col[1] for col in c.fetchall()]
    print(f"  {t} columns: {cols}")

conn.close()
