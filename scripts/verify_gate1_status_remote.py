import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_code = r"""
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db
from services.certificate_service import CertificateService

target_emails = [
    'subhradipd40@gmail.com',
    'thanveshburra@gmail.com',
    'reachshruthiv@gmail.com',
    'sjha0940@gmail.com',
    'devanshiyadav9131@gmail.com',
    'gurkavinay22@gmail.com',
    'bharathan45k@gmail.com'
]

with get_db() as conn:
    print('=== VERIFYING GATE 1 STATUS FOR STIPEND ON LMS ===')
    for em in target_emails:
        acct = conn.execute("SELECT id, name, email, domain, stipend_verified, upi_id_encrypted IS NOT NULL as has_upi FROM intern_accounts WHERE LOWER(email) = ?;", (em.lower(),)).fetchone()
        if acct:
            res = CertificateService.is_intern_verified(conn, intern_id=acct['id'], email=em)
            stipend_gate1 = bool(res.get('verified') and not res.get('is_provisional'))
            print(f"Candidate: {acct['name']} ({em})")
            print(f"   Certificate: {res.get('cert_id')} | Status: {res.get('status')} | Prov: {res.get('is_provisional')}")
            print(f"   Gate 1 Unlocked: {stipend_gate1} | Account stipend_verified: {acct['stipend_verified']} | UPI Bound: {acct['has_upi']}")
            print('-' * 70)
        else:
            print(f"Candidate not found in intern_accounts: {em}")
"""

res = subprocess.run(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"],
    input=remote_code,
    text=True,
    capture_output=True
)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
