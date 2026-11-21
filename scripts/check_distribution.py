import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import psycopg2, os
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

c.execute("SELECT date_trunc('day', expires_at::timestamp) as exp, count(*) FROM dbert_internship.posts GROUP BY exp ORDER BY exp;")
print("=== EXPIRATION DATES NOW ===")
for row in c.fetchall():
    print(str(row[0])[:10], row[1])

c.execute("SELECT date_trunc('day', apply_by::date) as app, count(*) FROM dbert_internship.posts GROUP BY app ORDER BY app;")
print("\\n=== APPLY_BY DATES NOW ===")
for row in c.fetchall():
    print(str(row[0])[:10], row[1])
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
