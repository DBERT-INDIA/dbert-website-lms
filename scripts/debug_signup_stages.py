import subprocess

code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    print('=== Signup stages breakdown in intern_accounts ===')
    for r in conn.execute('SELECT signup_stage, COUNT(id) AS cnt FROM intern_accounts GROUP BY signup_stage ORDER BY signup_stage').fetchall():
        print(dict(r))

    print('\\n=== Recent 25 intern_accounts created ===')
    for r in conn.execute('SELECT id, name, email, signup_stage, college, domain, created_at FROM intern_accounts ORDER BY id DESC LIMIT 25').fetchall():
        print(dict(r))

    print('\\n=== Breakdown of applications with Pending Profile ===')
    for r in conn.execute("SELECT domain, status, COUNT(id) AS cnt FROM applications WHERE college='Pending Profile' GROUP BY domain, status").fetchall():
        print(dict(r))

    print('\\n=== Applications total breakdown by status and college == Pending Profile vs Real ===')
    for r in conn.execute("SELECT (college='Pending Profile') AS is_pending, status, COUNT(id) AS cnt FROM applications GROUP BY (college='Pending Profile'), status").fetchall():
        print(dict(r))
"""

p = subprocess.Popen(
    ["ssh", "-i", r"C:\Users\user\.ssh\dbert-production-server.pem", "-o", "StrictHostKeyChecking=no", "ubuntu@3.26.237.171", "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
out, err = p.communicate(input=code)
print(out)
if err:
    print("ERR:", err)
