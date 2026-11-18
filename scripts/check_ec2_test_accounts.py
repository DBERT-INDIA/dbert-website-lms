import subprocess

pem = r"C:\Users\user\.ssh\dbert-production-server.pem"
host = "ubuntu@3.26.237.171"

remote_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    test_interns = conn.execute("SELECT id, name, email FROM intern_accounts WHERE email LIKE '%@dbert.test' LIMIT 10").fetchall()
    print("dbert.test interns count:", len(test_interns))
    for t in test_interns:
        print(dict(t))

    test_staff = conn.execute("SELECT id, name, email FROM staff_accounts WHERE email LIKE '%@dbert.test'").fetchall()
    print("dbert.test staff count:", len(test_staff))
    for s in test_staff:
        print(dict(s))
"""

p = subprocess.Popen(
    ["ssh", "-i", pem, "-o", "StrictHostKeyChecking=no", host, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = p.communicate(input=remote_code)
print("STDOUT:\n", stdout)
print("STDERR:\n", stderr)
