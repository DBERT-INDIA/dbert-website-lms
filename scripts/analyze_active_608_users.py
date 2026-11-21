import subprocess
import json

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

# Query the 608 active users from EC2
remote_script = '''
import psycopg2, os, json
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

c.execute("""
    SELECT 
        ia.id,
        ia.email,
        ia.name,
        ia.phone,
        ia.domain,
        ia.signup_stage,
        ia.account_status,
        ia.created_at,
        ia.upi_id_encrypted IS NOT NULL as has_upi,
        ia.stipend_verified,
        ia.terms_accepted_at IS NOT NULL as terms_accepted,
        count(s.id) as login_count,
        max(s.created_at) as last_login,
        (SELECT count(*) FROM dbert_internship.task_submissions ts WHERE ts.intern_id = ia.id) as tasks_count,
        (SELECT count(*) FROM dbert_internship.post_applications pa WHERE pa.intern_id = ia.id) as apps_count
    FROM dbert_internship.intern_accounts ia
    JOIN dbert_internship.user_sessions s ON lower(s.email) = lower(ia.email)
    WHERE s.created_at::timestamp >= '2026-11-05 00:00:00'
    GROUP BY ia.id, ia.email, ia.name, ia.phone, ia.domain, ia.signup_stage, ia.account_status, ia.created_at, ia.upi_id_encrypted, ia.stipend_verified, ia.terms_accepted_at
    ORDER BY login_count DESC;
""")

active_users = []
for r in c.fetchall():
    active_users.append({
        "id": r[0],
        "email": (r[1] or "").strip().lower(),
        "name": r[2],
        "phone": r[3],
        "domain": r[4],
        "signup_stage": r[5],
        "account_status": r[6],
        "created_at": str(r[7]),
        "has_upi": r[8],
        "stipend_verified": r[9],
        "terms_accepted": r[10],
        "login_count": r[11],
        "last_login": str(r[12]),
        "tasks_count": r[13],
        "apps_count": r[14]
    })

print(f"Total Active Intern Accounts with sessions in last 15 days: {len(active_users)}")
with open("/tmp/active_15d_interns.json", "w", encoding="utf-8") as f:
    json.dump(active_users, f, indent=2)
print("Saved to /tmp/active_15d_interns.json on EC2.")
'''

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
