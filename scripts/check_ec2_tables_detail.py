import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import psycopg2, os
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

tables = ['intern_accounts', 'enrollments', 'payments', 'payment_events', 'security_deposits', 'attendance', 'user_sessions', 'intern_certificates']

for t in tables:
    c.execute(f"SELECT count(*) FROM dbert_internship.{t};")
    cnt = c.fetchone()[0]
    c.execute(f\"\"\"
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_schema='dbert_internship' AND table_name='{t}'
        ORDER BY ordinal_position;
    \"\"\")
    cols = [r[0] for r in c.fetchall()]
    print(f"\\nTable: {t} (Count: {cnt})")
    print("  Cols: " + ", ".join(cols))
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
