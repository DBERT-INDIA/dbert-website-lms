import subprocess
import json

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

# Let's inspect the registration dates and sources on EC2
remote_script = '''
import psycopg2, os, json
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

c.execute("""
    SELECT date_trunc('month', created_at::timestamp) as m, count(*) 
    FROM dbert_internship.intern_accounts 
    GROUP BY m 
    ORDER BY m;
""")
print("Registration by Month:")
for r in c.fetchall():
    print(f"  {str(r[0])[:10]}: {r[1]}")

c.execute("""
    SELECT date_trunc('day', created_at::timestamp) as d, count(*) 
    FROM dbert_internship.intern_accounts 
    WHERE created_at::timestamp >= '2026-10-01'
    GROUP BY d 
    ORDER BY d;
""")
print("\\nDaily Registrations (Oct - Nov 2026):")
for r in c.fetchall():
    print(f"  {str(r[0])[:10]}: {r[1]}")

# Export all intern emails to check against local campaign tracking
c.execute("SELECT id, email, name, domain, signup_stage, account_status, created_at, upi_id_encrypted IS NOT NULL as has_upi FROM dbert_internship.intern_accounts;")
interns = c.fetchall()
with open("/tmp/all_intern_accounts.json", "w", encoding="utf-8") as f:
    json.dump([
        {
            "id": r[0],
            "email": (r[1] or "").strip().lower(),
            "name": r[2],
            "domain": r[3],
            "signup_stage": r[4],
            "account_status": r[5],
            "created_at": str(r[6]),
            "has_upi": r[7]
        } for r in interns
    ], f)
print(f"\\nExported {len(interns)} interns to /tmp/all_intern_accounts.json")
'''

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
