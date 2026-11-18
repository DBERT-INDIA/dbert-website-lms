import subprocess

PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

REMOTE_CODE = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    rows = conn.execute('''
        SELECT id, name, email, domain, college, course, semester, year_of_passing, status, source, created_at, why_join
        FROM applications
        WHERE id >= 5190
        ORDER BY id DESC
    ''').fetchall()
    for r in rows:
        d = dict(r)
        why = (d.get('why_join') or '')[:40].replace('\\n', ' ')
        print(f"{d['id']} | {d['name']} | {d['email']} | {d['domain']} | {d['college']} | status={d.get('status')} | src={d.get('source')}")

    print('\\n--- Checking corresponding intern_accounts for these emails ---')
    for r in rows:
        email = r['email']
        acc = conn.execute("SELECT id, name, email, signup_stage, college, is_active FROM intern_accounts WHERE LOWER(email)=LOWER(?)", (email,)).fetchone()
        if acc:
            print(f"Account for {email}: stage={acc['signup_stage']}, college={acc.get('college')}")
        else:
            print(f"Account for {email}: NO intern_accounts record")
"""

p = subprocess.Popen(
    ["ssh", "-i", PEM_PATH, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = p.communicate(input=REMOTE_CODE)
print(stdout)
if stderr:
    print("STDERR:", stderr)
