import subprocess

remote_code = r"""
import os, sys, json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    print('Dialect:', getattr(conn, 'dialect', 'unknown'))
    cur = conn.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'enrollments' ORDER BY ordinal_position;")
    rows = cur.fetchall()
    print('Enrollments columns:')
    for r in rows:
        print(f"  {r[0]} ({r[1]})")

    print('\nLatest enrollments sample:')
    cur = conn.execute("SELECT * FROM enrollments ORDER BY id DESC LIMIT 2;")
    for r in cur.fetchall():
        print(dict(r) if hasattr(r, 'keys') else r)

    print('\nOffer letter for janvibamane61@gmail.com:')
    cur = conn.execute("SELECT * FROM intern_offer_letters WHERE LOWER(email) = 'janvibamane61@gmail.com';")
    for r in cur.fetchall():
        print(dict(r) if hasattr(r, 'keys') else r)

    print('\nEnrollment for janvibamane61@gmail.com:')
    cur = conn.execute("SELECT id, name, email, domain, payment_status, amount_paid, deposit_paid, joining_date, batch_label FROM enrollments WHERE LOWER(email) = 'janvibamane61@gmail.com';")
    for r in cur.fetchall():
        print(dict(r) if hasattr(r, 'keys') else r)

    print('\nApplication for janvibamane61@gmail.com:')
    cur = conn.execute("SELECT id, name, email, domain, status FROM applications WHERE LOWER(email) = 'janvibamane61@gmail.com';")
    for r in cur.fetchall():
        print(dict(r) if hasattr(r, 'keys') else r)

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
