import subprocess

remote_code = r"""
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    print('=== CHECKING ENROLLMENTS for amount = 299 or amount_paid = 299 ===')
    cur = conn.execute("SELECT id, name, email, domain, amount, amount_paid, payment_status, utr, created_at FROM enrollments WHERE amount = 299 OR amount_paid = 299 ORDER BY id DESC LIMIT 10;")
    for r in cur.fetchall():
        print(dict(r))

    print('\n=== CHECKING ANY OTHER TABLES WITH 299 ===')
    # Check if there are other payment records
    try:
        cur = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_name ILIKE '%pay%' OR table_name ILIKE '%submiss%' OR table_name ILIKE '%transact%';")
        for r in cur.fetchall():
            print('Table:', r[0])
    except Exception as e:
        print('Error:', e)
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
