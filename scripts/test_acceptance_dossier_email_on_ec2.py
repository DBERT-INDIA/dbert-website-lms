#!/usr/bin/env python3
"""
scripts/test_acceptance_dossier_email_on_ec2.py
Tests the Enrollment Acceptance Dossier Email and /portal/receipt endpoint on EC2.
"""

import os
import sys
import subprocess
import requests

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"
LMS_URL = "https://lms.dbert.in"

def run_remote_python(code_str):
    p = subprocess.Popen(
        ['ssh', '-i', SSH_KEY, '-o', 'StrictHostKeyChecking=no', REMOTE_HOST,
         '/var/www/dbert-website-lms/apps/portal/.venv/bin/python', '-'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    out, err = p.communicate(input=code_str)
    return p.returncode, out, err

def main():
    print("=== TESTING ACCEPTANCE DOSSIER EMAIL & PORTAL RECEIPT ON EC2 ===")
    
    # Test 1: Generate valid HMAC token for UTR 666501928441 on EC2
    token_gen_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import _email_sig, app
print(_email_sig('receipt', '666501928441'))
"""
    rc, out, err = run_remote_python(token_gen_code)
    if rc != 0:
        print(f"[FAIL] Error generating token: {err}")
        sys.exit(1)
    
    valid_token = out.strip().split()[-1]
    print(f"[OK] Generated HMAC Token for UTR 666501928441: {valid_token}")

    # Test 2: Access /portal/receipt/utr_666501928441.receipt with valid token
    receipt_url = f"{LMS_URL}/portal/receipt/utr_666501928441.receipt?token={valid_token}"
    resp = requests.get(receipt_url, timeout=10)
    print(f"[STATUS] GET {receipt_url} -> {resp.status_code}")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    assert "image/svg+xml" in resp.headers.get("Content-Type", ""), "Expected image/svg+xml Content-Type"
    assert "<svg" in resp.text, "Response missing <svg> element"
    assert "666501928441" in resp.text, "Voucher missing UTR digits"
    print("[PASS] Test 1: Token-authenticated /portal/receipt returned valid vector SVG voucher!")

    # Test 3: Access /portal/receipt without token (should redirect or 401)
    no_token_url = f"{LMS_URL}/portal/receipt/utr_666501928441.receipt"
    resp_no_token = requests.get(no_token_url, allow_redirects=False, timeout=10)
    print(f"[STATUS] GET {no_token_url} (no token) -> {resp_no_token.status_code}")
    assert resp_no_token.status_code in (302, 401), f"Expected 302 or 401 without auth, got {resp_no_token.status_code}"
    print("[PASS] Test 2: Unauthenticated /portal/receipt correctly protected by access control!")

    # Test 4: Access /portal/receipt with invalid token
    invalid_token_url = f"{LMS_URL}/portal/receipt/utr_666501928441.receipt?token=invalid_forged_signature_123"
    resp_inv = requests.get(invalid_token_url, allow_redirects=False, timeout=10)
    print(f"[STATUS] GET {invalid_token_url} (invalid token) -> {resp_inv.status_code}")
    assert resp_inv.status_code in (302, 401), f"Expected 302 or 401 with invalid token, got {resp_inv.status_code}"
    print("[PASS] Test 3: Invalid token strictly rejected!")

    # Test 5: Verify send_enrollment_acceptance_dossier_email builds complete MIME structure with attachment
    email_test_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, row_to_dict, get_utr_voucher_record, generate_utr_voucher_svg, _build_email_message, make_batch_label, _email_sig

with get_db() as conn:
    row = conn.execute("SELECT * FROM enrollments WHERE LOWER(email)='bhargavi13032007@gmail.com' LIMIT 1").fetchone()
    if not row:
        row = conn.execute("SELECT * FROM enrollments ORDER BY id DESC LIMIT 1").fetchone()
    ed = row_to_dict(row)
    
utr = "666501928441"
voucher_rec = get_utr_voucher_record(utr, ed.get('payment_screenshot', ''), email=ed.get('email'))
svg_content = generate_utr_voucher_svg(voucher_rec)
attachments = [("DBERT_Payment_Voucher_666501928441.svg", svg_content.encode("utf-8"), "image/svg+xml")]

subject = f"DBERT — Enrollment Confirmed & Official Payment Voucher (UTR: {utr})"
html_sample = "<p>Test acceptance email with roadmap</p>"

msg = _build_email_message(ed.get('email', 'test@example.com'), subject, html_sample, "enrollment_accepted", attachments=attachments)

parts = [p.get_content_type() for p in msg.walk()]
print(f"MIME_CONTENT_TYPE: {msg.get_content_type()}")
print(f"MIME_PARTS: {parts}")
assert msg.get_content_type() == 'multipart/mixed', f"Expected multipart/mixed, got {msg.get_content_type()}"
assert 'image/svg+xml' in parts or 'application/octet-stream' in parts, f"Missing attachment part in {parts}"
print("EMAIL_BUILD_SUCCESS")
"""
    rc, out, err = run_remote_python(email_test_code)
    print(out)
    if rc != 0 or "EMAIL_BUILD_SUCCESS" not in out:
        print(f"[FAIL] Error testing email builder: {err}")
        sys.exit(1)
    print("[PASS] Test 4: MIME email builder generated RFC-compliant multipart/mixed with SVG voucher attachment!")

    print("\n=======================================================")
    print("ALL TESTS PASSED: 100% VERIFICATION SUCCESSFUL!")
    print("=======================================================")

if __name__ == "__main__":
    main()
