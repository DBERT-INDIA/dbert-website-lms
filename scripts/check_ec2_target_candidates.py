import subprocess
import json

remote_code = r"""
import sys, os
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

cids = [
    'CERT-DBERT-2026-FSD-043',
    'CERT-DBERT-2026-AIML-023',
    'CERT-DBERT-2026-FSD-045',
    'CERT-DBERT-2026-FSD-042',
    'CERT-DBERT-2026-UIUX-036',
    'CERT-DBERT-2026-AIML-169',
    'CERT-DBERT-2026-DA-112'
]

emails = [
    'subhradipd40@gmail.com',
    'thanveshburra@gmail.com',
    'reachshruthiv@gmail.com',
    'sjha0940@gmail.com',
    'devanshiyadav9131@gmail.com',
    'gurkavinay22@gmail.com',
    'bharathan45k@gmail.com'
]

with get_db() as conn:
    print('=== CHECKING intern_certificates in PostgreSQL ===')
    for cid in cids:
        cur = conn.execute("SELECT * FROM intern_certificates WHERE cert_id = ?;", (cid,))
        r = cur.fetchone()
        print(f"Cert [{cid}]: {dict(r) if r else 'NOT FOUND'}")

    print('\n=== CHECKING intern_accounts in PostgreSQL ===')
    for em in emails:
        cur = conn.execute("SELECT id, name, email, domain, stipend_verified, upi_id_encrypted IS NOT NULL as has_upi, is_active FROM intern_accounts WHERE LOWER(email) = ?;", (em.lower(),))
        r = cur.fetchone()
        print(f"Account [{em}]: {dict(r) if r else 'NOT FOUND'}")
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
