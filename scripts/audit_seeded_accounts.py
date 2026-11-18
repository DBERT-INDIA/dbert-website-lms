import subprocess

pem = r"C:\Users\user\.ssh\dbert-production-server.pem"
host = "ubuntu@3.26.237.171"

remote_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    print("=== ACCOUNTS AUDIT ===")
    emails = [
        'fellow_enrolled@dbert.test',
        'stipend_ready@dbert.test',
        'stipend_wallet@dbert.test',
        'stipend_gate1_locked@dbert.test',
        'provisional_fellow@dbert.test',
        'stage3_selected@dbert.test',
        'offer_pending@dbert.test',
        'mentor_staff@dbert.test'
    ]
    for email in emails:
        print(f"\\n--- {email} ---")
        acct = conn.execute("SELECT id, name, email, domain, stipend_verified, upi_id_encrypted, is_active FROM intern_accounts WHERE email=?", (email,)).fetchone()
        if acct:
            print("intern_account:", dict(acct))
            app = conn.execute("SELECT id, status, why_join FROM applications WHERE email=?", (email,)).fetchone()
            print("application:", dict(app) if app else "NONE")
            enr = conn.execute("SELECT id, joining_date, payment_status, batch_label FROM enrollments WHERE email=?", (email,)).fetchone()
            print("enrollment:", dict(enr) if enr else "NONE")
            cert = conn.execute("SELECT id, cert_id, course_title FROM intern_certificates WHERE email=?", (email,)).fetchone()
            print("certificate:", dict(cert) if cert else "NONE")
            coins = conn.execute("SELECT delta, balance_after, ledger_kind FROM coin_ledger_mirror WHERE email=?", (email,)).fetchall()
            print("coin_ledger:", [dict(c) for c in coins])
            offer = conn.execute("SELECT offer_letter_id, signature_name, accepted_at FROM intern_offer_letters WHERE email=?", (email,)).fetchone()
            print("offer_letter:", dict(offer) if offer else "NONE")
        else:
            staff = conn.execute("SELECT id, name, email, role, is_active FROM staff_accounts WHERE email=?", (email,)).fetchone()
            if staff:
                print("staff_account:", dict(staff))
                slots = conn.execute("SELECT id, start_time, capacity, seats_booked FROM mentor_availability_slots WHERE mentor_staff_id=?", (staff['id'],)).fetchall()
                print("mentor_slots:", [dict(s) for s in slots])
            else:
                print("NOT FOUND IN DATABASE")
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
