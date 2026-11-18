import sqlite3
import os
import sys
import subprocess

print("--- SQLITE: apps/portal/internship.db ---")
if os.path.exists('apps/portal/internship.db'):
    conn = sqlite3.connect('apps/portal/internship.db')
    c = conn.cursor()
    c.execute("SELECT tbl_name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in c.fetchall()]
    print("Tables:", tables)
    for t in tables:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = c.fetchone()[0]
        c.execute(f"PRAGMA table_info({t})")
        cols = [col[1] for col in c.fetchall()]
        print(f"  {t}: {cnt} rows | cols: {cols[:6]}")
else:
    print("No internship.db found")

print("\n--- EC2 POSTGRESQL: tables related to jobs / internships / experience ---")
PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
remote_py = """
import psycopg2
conn = psycopg2.connect('dbname=dbert_portal user=ubuntu host=localhost')
c = conn.cursor()
c.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [t[0] for t in c.fetchall()]
job_tables = [t for t in tables if any(k in t.lower() for k in ['job', 'intern', 'scraped', 'post', 'experi'])]
print("Relevant tables on EC2:", job_tables)
for t in job_tables:
    c.execute(f'SELECT count(*) FROM {t}')
    cnt = c.fetchone()[0]
    c.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{t}'")
    cols = [col[0] for col in c.fetchall()]
    print(f'  {t}: {cnt} rows | cols: {cols[:8]}')
"""
ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, f"python3 -c \"{remote_py}\""]
res = subprocess.run(ssh_cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
