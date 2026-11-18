import subprocess

pem = r"C:\Users\user\.ssh\dbert-production-server.pem"
host = "ubuntu@3.26.237.171"

remote_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, verify_password

test_accounts = [
    ('staff', 'mentor_staff@dbert.test'),
    ('staff', 'dbert_admin@dbert.test'),
    ('intern', 'fellow_enrolled@dbert.test'),
    ('intern', 'stipend_ready@dbert.test'),
    ('intern', 'stipend_wallet@dbert.test'),
    ('intern', 'stipend_gate1_locked@dbert.test'),
    ('intern', 'provisional_fellow@dbert.test'),
    ('intern', 'stage3_selected@dbert.test'),
    ('intern', 'offer_pending@dbert.test'),
]

password = 'TestPass123!'

with get_db() as conn:
    for kind, email in test_accounts:
        if kind == 'staff':
            row = conn.execute('SELECT email, password_hash, is_active FROM staff_accounts WHERE email=?', (email,)).fetchone()
        else:
            row = conn.execute('SELECT email, password_hash, is_active, password_set FROM intern_accounts WHERE email=?', (email,)).fetchone()
        
        if not row:
            print(f'❌ {email}: NOT FOUND')
            continue
        
        ok = verify_password(row['password_hash'], password)
        print(f'✓ {email} ({kind}): Auth OK={ok}, Active={row["is_active"]}')
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
