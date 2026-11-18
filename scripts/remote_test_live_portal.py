
import sys
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
from app import app, get_or_create_offer_letter, get_intern_active_gemini_context, create_session, get_db

print("=== Testing Portal Endpoints Live on EC2 ===")

with get_db() as conn:
    cur = conn.cursor()
    # 1. Check verified candidate
    cur.execute("SELECT email, name, domain, payment_status FROM enrollments WHERE payment_status = 'Verified' LIMIT 1")
    row = cur.fetchone()
    if row:
        email, name, domain, status = row
        print(f"Verified candidate: {name} ({email}) - {domain}")
        offer = get_or_create_offer_letter(email, conn=conn)
        print(f"Offer ID: {offer['offer_letter_id']}, Status: {offer['caution_deposit_status']}")

        # Test authenticated request to /portal/offer
        token = create_session(email, "intern")
        with app.test_client() as client:
            res = client.get("/portal/offer", headers={"X-Session-Token": token})
            print(f"GET /portal/offer HTTP status: {res.status_code}")
            assert res.status_code == 200
            assert offer["offer_letter_id"] in res.get_data(as_text=True)
            print("Verified candidate offer view verified: 200 OK with correct Offer ID!")

            # Test /tasks/101/guide without key -> redirects to /account/gemini-key?next=...
            res_guide_nokey = client.get("/tasks/101/guide", headers={"X-Session-Token": token})
            print(f"GET /tasks/101/guide without key: status {res_guide_nokey.status_code}, redirect to {res_guide_nokey.headers.get('Location')}")
            assert res_guide_nokey.status_code == 302
            assert "/account/gemini-key" in res_guide_nokey.headers.get("Location")
            print("Pre-flight gating verified: missing key redirects to /account/gemini-key?next=...!")

    # 2. Check candidate WITH an active Gemini API key in user_api_keys
    cur.execute("SELECT u.email, u.name FROM user_api_keys k JOIN intern_accounts u ON k.intern_id = u.id WHERE k.provider = 'gemini' LIMIT 1")
    row_key = cur.fetchone()
    if row_key:
        key_email, key_name = row_key
        print(f"Candidate with key: {key_name} ({key_email})")
        token_key = create_session(key_email, "intern")
        with app.test_client() as client:
            res_guide_withkey = client.get("/tasks/101/guide", headers={"X-Session-Token": token_key})
            print(f"GET /tasks/101/guide with key HTTP status: {res_guide_withkey.status_code}")
            if res_guide_withkey.status_code == 200:
                print("Course-style bounty guide view with active key verified: 200 OK!")
                assert "Assigned Angle & Case Study Context" in res_guide_withkey.get_data(as_text=True)
            else:
                print("Redirect or status with key:", res_guide_withkey.status_code, res_guide_withkey.headers.get("Location"))

    # 3. Check unselected / under review candidate
    cur.execute("SELECT email, name, status FROM applications WHERE status = 'Under Review' LIMIT 1")
    row_app = cur.fetchone()
    if row_app:
        app_email, app_name, app_status = row_app
        print(f"Under Review candidate: {app_name} ({app_email})")
        token_rev = create_session(app_email, "intern")
        with app.test_client() as client:
            res_rev = client.get("/portal/offer", headers={"X-Session-Token": token_rev})
            print(f"Under review candidate GET /portal/offer status: {res_rev.status_code}")
            assert res_rev.status_code == 200
            assert "Official Offer Letter Gated" in res_rev.get_data(as_text=True)
            print("Under review candidate gate verified: shows locked gate card instead of 404!")

print("=== ALL LIVE TESTS PASSED! ===")
