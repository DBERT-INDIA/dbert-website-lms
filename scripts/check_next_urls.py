import subprocess

code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    rows = conn.execute('''
        SELECT a.id, a.name, a.email, a.domain, a.college, a.created_at, s.next_url
        FROM applications a
        LEFT JOIN user_sessions s ON LOWER(s.email) = LOWER(a.email)
        WHERE a.id >= 5190
        ORDER BY a.id DESC
    ''').fetchall()
    for r in rows:
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
