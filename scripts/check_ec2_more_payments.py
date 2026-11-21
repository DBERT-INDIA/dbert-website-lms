import subprocess

remote_code = r"""
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    print('=== PAYMENTS TABLE ===')
    try:
        cur = conn.execute("SELECT * FROM payments ORDER BY id DESC LIMIT 5;")
        for r in cur.fetchall():
            print(dict(r))
    except Exception as e:
        print('payments err:', e)

    print('=== PAYMENT_EVENTS TABLE ===')
    try:
        cur = conn.execute("SELECT * FROM payment_events ORDER BY id DESC LIMIT 5;")
        for r in cur.fetchall():
            print(dict(r))
    except Exception as e:
        print('payment_events err:', e)

    print('=== COURSE_PAYMENTS TABLE ===')
    try:
        cur = conn.execute("SELECT * FROM course_payments ORDER BY id DESC LIMIT 5;")
        for r in cur.fetchall():
            print(dict(r))
    except Exception as e:
        print('course_payments err:', e)
"""

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

res = subprocess.run(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"],
    input=remote_code,
    text=True,
    capture_output=True
)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
