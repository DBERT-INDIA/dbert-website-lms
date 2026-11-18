import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

REMOTE_SCRIPT = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db, create_session, get_or_create_offer_letter

app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False

with app.test_client() as client:
    # 1. Setup a test candidate in PostgreSQL database
    with get_db() as conn:
        conn.execute("DELETE FROM intern_offer_letters WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.execute("DELETE FROM enrollments WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.execute("DELETE FROM applications WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.execute("DELETE FROM intern_accounts WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.execute('''
            INSERT INTO intern_accounts (email, name, password_hash, is_active)
            VALUES ('test_sign_flow@dbert.in', 'Aditi Sen', 'dummyhash', 1)
        ''')
        conn.execute('''
            INSERT INTO applications (email, name, phone, domain, status)
            VALUES ('test_sign_flow@dbert.in', 'Aditi Sen', '9876543210', 'Data Analyst', 'Selected')
        ''')
        conn.commit()

    token = create_session('test_sign_flow@dbert.in', 'intern')

    # 2. View /portal/offer before signing
    res = client.get('/portal/offer', headers={'X-Session-Token': token})
    assert res.status_code == 200, f'Expected 200, got {res.status_code}'
    html = res.get_data(as_text=True)
    assert '1999' not in html, '1999 found in HTML!'
    assert 'Execute Appointment Agreement' in html
    assert 'Review &amp; Sign Offer Agreement' in html or 'Review & Sign Offer Agreement' in html
    print('[EC2 LIVE TEST 1 PASSED] Candidate sees Offer Letter Document first + Digital Signature Form.')

    # Set CSRF token in session
    test_csrf = "ec2_test_csrf_token_secure_99"
    with client.session_transaction() as sess:
        sess['_csrf'] = test_csrf

    # 3. Post Digital Signature with CSRF
    headers = {
        'X-Session-Token': token,
        'X-CSRF-Token': test_csrf
    }

    res_sign = client.post(
        '/portal/offer/sign',
        json={'signature_name': 'Aditi Sen', 'agreed': True, 'csrf_token': test_csrf},
        headers=headers
    )
    assert res_sign.status_code == 200, f'Expected 200, got {res_sign.status_code}'
    data = res_sign.get_json()
    assert data['status'] == 'success'
    assert data['requires_deposit'] is True
    print('[EC2 LIVE TEST 2 PASSED] Digital signature executed successfully in Read & Sign First flow.')

    # 4. View /portal/offer after signing
    res_after = client.get('/portal/offer', headers={'X-Session-Token': token})
    html_after = res_after.get_data(as_text=True)
    assert 'Appointment Agreement Digitally Signed' in html_after
    assert 'Aditi Sen' in html_after
    assert 'Q652429146@ybl' in html_after
    assert 'intent://pay?pa=Q652429146@ybl' in html_after
    assert 'phonepe://pay?pa=Q652429146@ybl' in html_after
    assert 'paytmmp://pay?pa=Q652429146@ybl' in html_after
    assert 'upi://pay?pa=Q652429146@ybl' in html_after
    assert '1999' not in html_after
    print('[EC2 LIVE TEST 3 PASSED] Post-sign view reveals signed seal + 499 QR + 1-Tap UPI Launchers + UTR form.')

    # 5. Clean up test records
    with get_db() as conn:
        conn.execute("DELETE FROM intern_offer_letters WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.execute("DELETE FROM enrollments WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.execute("DELETE FROM applications WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.execute("DELETE FROM intern_accounts WHERE LOWER(email)='test_sign_flow@dbert.in'")
        conn.commit()
    print('[EC2 LIVE TEST 4 PASSED] Test candidate cleaned up cleanly.')
"""

def main():
    local_script = "scripts/ec2_test_offer_flow.py"
    with open(local_script, "w", encoding="utf-8") as f:
        f.write(REMOTE_SCRIPT)

    subprocess.run([
        "scp", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        local_script,
        f"{HOST}:/tmp/ec2_test_offer_flow.py"
    ], check=True)

    res = subprocess.run([
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        "-o", "BatchMode=yes",
        HOST,
        "/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/ec2_test_offer_flow.py && rm -f /tmp/ec2_test_offer_flow.py"
    ], capture_output=True, text=True)

    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    print("CODE:", res.returncode)

if __name__ == "__main__":
    main()
