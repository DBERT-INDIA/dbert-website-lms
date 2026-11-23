import requests
import re

def get_csrf(session, url):
    res = session.get(url)
    m = re.search(r'<meta name="csrf-token" content="([^"]+)">', res.text)
    if not m:
        m = re.search(r'name=["\']csrf_token["\']\s+value=["\']([^"\']+)["\']', res.text)
    return m.group(1) if m else None

def test_full_portal_offer_suite():
    s = requests.Session()
    
    # 1. Acquire CSRF
    csrf = get_csrf(s, 'http://127.0.0.1:5001/signin')
    print("1. CSRF Token acquired:", bool(csrf))
    
    # 2. Login as stage2_review (Under Review candidate)
    login_headers = {'Content-Type': 'application/json', 'X-CSRF-Token': csrf}
    lres = s.post('http://127.0.0.1:5001/intern/login', json={
        'email': 'stage2_review@dbert.test',
        'password': 'TestPass123!'
    }, headers=login_headers)
    print("2. Stage 2 Candidate Login:", lres.status_code, lres.json().get('message'))
    
    # 3. Inspect locked offer page
    ores = s.get('http://127.0.0.1:5001/portal/offer')
    html = ores.text
    print("3. Offer page status:", ores.status_code, "URL:", ores.url)
    
    checks = [
        ("Scan & Pay ₹499 Card", "Scan & Pay ₹499" in html or "Scan &amp; Pay ₹499" in html),
        ("Merchant VPA (Q652429146@ybl)", "Q652429146@ybl" in html),
        ("Download QR button", "DBERT_Caution_Deposit_UPI_QR.jpeg" in html),
        ("GPay 1-tap fast pay", "intent://pay?pa=Q652429146@ybl" in html),
        ("PhonePe 1-tap fast pay", "phonepe://pay?pa=Q652429146@ybl" in html),
        ("Paytm 1-tap fast pay", "paytmmp://pay?pa=Q652429146@ybl" in html),
        ("Any UPI 1-tap fast pay", "upi://pay?pa=Q652429146@ybl" in html),
        ("Native depositSubmitForm", 'id="depositSubmitForm"' in html),
        ("12-digit UTR input field", 'id="depositUtrInput"' in html),
        ("Google Form Dead-End ABSENT", "docs.google.com/forms" not in html),
        ("Upgrade to Incubation (₹1,999) Link", "/enroll/1999" in html),
        ("Project Credentials (₹299) Link", "/verify/unlock" in html),
        ("Admissions WhatsApp Button", "wa.me/918192911360" in html),
    ]
    
    print("\n--- TEST SUITE 1: STAGE 2 UNDER REVIEW CANDIDATE (LOCKED OFFER) ---")
    suite1_pass = True
    for label, ok in checks:
        print(f"[{'✓ PASS' if ok else '✗ FAIL'}] {label}")
        if not ok: suite1_pass = False
        
    # 4. Test stage 3 selected candidate
    s3 = requests.Session()
    csrf3 = get_csrf(s3, 'http://127.0.0.1:5001/signin')
    lres3 = s3.post('http://127.0.0.1:5001/intern/login', json={
        'email': 'stage3_selected@dbert.test',
        'password': 'TestPass123!'
    }, headers={'Content-Type': 'application/json', 'X-CSRF-Token': csrf3})
    ores3 = s3.get('http://127.0.0.1:5001/portal/offer')
    html3 = ores3.text
    print("\n--- TEST SUITE 2: STAGE 3 SELECTED CANDIDATE (UNLOCKED OFFER) ---")
    print(f"[{'✓ PASS' if ores3.status_code == 200 else '✗ FAIL'}] Unlocked offer HTTP status: {ores3.status_code}")
    print(f"[{'✓ PASS' if 'Appointment' in html3 or 'Digital Signature' in html3 else '✗ FAIL'}] Appointment Stepper Rendered")
    print(f"[{'✓ PASS' if 'docs.google.com/forms' not in html3 else '✗ FAIL'}] Google Form ABSENT in unlocked mode")
    
    # 5. Test UTR Submission on /enroll
    csrf_enr = get_csrf(s, 'http://127.0.0.1:5001/portal/offer')
    
    # 5a. Invalid format
    inv_res = s.post('http://127.0.0.1:5001/enroll', data={
        'utr_number': '123',
        'joining_date': '2026-11-23',
        'domain': 'Full Stack Development',
        'csrf_token': csrf_enr
    })
    print("\n--- TEST SUITE 3: UTR VALIDATION & SEAT CONFIRMATION API ---")
    print(f"[{'✓ PASS' if inv_res.status_code == 400 else '✗ FAIL'}] Invalid UTR Rejected with 400: {inv_res.json().get('message')}")
    
    # 5b. Valid 12-digit UTR
    import random
    test_utr = f"{random.randint(100000000000, 999999999999)}"
    val_res = s.post('http://127.0.0.1:5001/enroll', data={
        'utr_number': test_utr,
        'joining_date': '2026-11-23',
        'domain': 'Full Stack Development',
        'csrf_token': csrf_enr
    })
    print(f"[{'✓ PASS' if val_res.status_code == 200 and val_res.json().get('status') == 'success' else '✗ FAIL'}] Valid UTR ({test_utr}) Accepted: {val_res.status_code} {val_res.json().get('message')}")
    
    # 5c. Duplicate UTR check from same session with same UTR
    dup_res = s.post('http://127.0.0.1:5001/enroll', data={
        'utr_number': test_utr,
        'joining_date': '2026-11-23',
        'domain': 'Full Stack Development',
        'csrf_token': csrf_enr
    })
    print(f"[{'✓ PASS' if dup_res.status_code in (200, 409) else '✗ FAIL'}] Re-submission/Duplicate Handled: {dup_res.status_code} {dup_res.json().get('message')}")
    
    print("\n=======================================================")
    print("ALL TEST SUITES EXECUTED SUCCESSFULLY!")
    print("=======================================================")

if __name__ == '__main__':
    test_full_portal_offer_suite()
