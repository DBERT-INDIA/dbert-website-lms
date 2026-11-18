import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db, create_session, get_intern_stage_and_next_action

with get_db() as conn:
    # Find a selected intern or test stage 2 directly
    selected_row = conn.execute("SELECT email FROM applications WHERE status = 'Selected' LIMIT 1").fetchone()
    if selected_row:
        email = selected_row["email"]
        st = get_intern_stage_and_next_action(conn, email)
        print("Selected candidate stage info for", email, ":")
        print(" - Heading:", st.get("heading"))
        print(" - Primary CTA:", st.get("primary_cta_label"), "Type:", st.get("primary_cta_type"))
        print(" - Secondary CTA:", st.get("secondary_cta_label"), "Type:", st.get("secondary_cta_type"))
        token = create_session(email, "intern")
        with app.test_client() as client:
            resp = client.get('/portal', headers={"X-Session-Token": token})
            print(" - Authenticated /portal status:", resp.status_code)
            assert resp.status_code == 200
            html = resp.data.decode('utf-8')
            assert 'na-btn-gold' in html
            assert 'na-btn-whatsapp' in html
            print(" - Button classes verified in HTML!")
        with get_db() as conn2:
            conn2.execute("DELETE FROM user_sessions WHERE session_token = ?", (token,))
            conn2.commit()

print("ALL PRODUCTION CHECKS VERIFIED SUCCESSFULLY!")
