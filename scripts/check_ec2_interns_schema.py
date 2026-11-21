import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import psycopg2, os
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

c.execute(\"\"\"
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='dbert_internship' 
    ORDER BY table_name;
\"\"\")
tables = [r[0] for r in c.fetchall()]
print(f"Total tables in dbert_internship: {len(tables)}")
print(", ".join(tables))

# Check users/interns count
c.execute("SELECT count(*) FROM dbert_internship.interns;")
print(f"Total interns: {c.fetchone()[0]}")

# Check columns of interns
c.execute(\"\"\"
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema='dbert_internship' AND table_name='interns'
    ORDER BY ordinal_position;
\"\"\")
print("\\nColumns in interns table:")
for col in c.fetchall():
    print(f"  {col[0]}: {col[1]}")
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
