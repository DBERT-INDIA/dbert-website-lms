import subprocess

pem = r"C:\Users\user\.ssh\dbert-production-server.pem"
host = "ubuntu@3.26.237.171"

script = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, verify_password, hash_password

with get_db() as conn:
    print('--- STAFF ACCOUNTS ---')
    rows = conn.execute("SELECT email, password_hash FROM staff_accounts WHERE email LIKE '%dbert.test'").fetchall()
    for r in rows:
        h = r['password_hash']
        v1 = verify_password('TestPass123!', h)
        v2 = verify_password('admin123', h)
        v3 = (h == hash_password('TestPass123!'))
        print(r['email'], h[:30], f"TestPass123!:{v1}, admin123:{v2}, sha256:{v3}")

    print('--- INTERN ACCOUNTS ---')
    rows_i = conn.execute("SELECT email, password_hash FROM intern_accounts WHERE email LIKE '%@dbert.test' LIMIT 5").fetchall()
    for r in rows_i:
        h = r['password_hash']
        v1 = verify_password('TestPass123!', h)
        v3 = (h == hash_password('TestPass123!'))
        print(r['email'], (h or '')[:30], f"TestPass123!:{v1}, sha256:{v3}")
"""

p = subprocess.Popen(['ssh', '-i', pem, '-o', 'StrictHostKeyChecking=no', host, '/var/www/dbert-website-lms/apps/portal/.venv/bin/python', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
out, err = p.communicate(input=script)
print(out)
if err: print("ERR:", err)
