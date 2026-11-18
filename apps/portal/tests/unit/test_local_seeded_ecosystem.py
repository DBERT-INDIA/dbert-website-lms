import pytest
from app import app, get_db
from werkzeug.security import check_password_hash

TEST_PASSWORD = "TestPass123!"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_seeded_personas_exist_and_password_matches():
    with get_db() as conn:
        # 1. Admin
        admin = conn.execute("SELECT * FROM staff_accounts WHERE email = 'admin@dbert.test'").fetchone()
        assert admin is not None
        assert check_password_hash(admin["password_hash"], TEST_PASSWORD)
        assert admin["role"] == "admin"

        # 2. Staff
        staff = conn.execute("SELECT * FROM staff_accounts WHERE email = 'staff@dbert.test'").fetchone()
        assert staff is not None
        assert check_password_hash(staff["password_hash"], TEST_PASSWORD)
        assert staff["role"] == "staff"

        # 3. Company
        comp = conn.execute("SELECT * FROM companies WHERE email = 'recruiter@techcorp.test'").fetchone()
        assert comp is not None
        assert check_password_hash(comp["password_hash"], TEST_PASSWORD)

        # 4. Stages 1-5 Interns
        s1 = conn.execute("SELECT * FROM applications WHERE email = 'stage1_apply@dbert.test'").fetchone()
        assert s1 is not None and s1["status"] == "Apply Pending"

        s2 = conn.execute("SELECT * FROM applications WHERE email = 'stage2_review@dbert.test'").fetchone()
        assert s2 is not None and s2["status"] == "Under Review"

        s3 = conn.execute("SELECT * FROM applications WHERE email = 'stage3_selected@dbert.test'").fetchone()
        assert s3 is not None and s3["status"] == "Selected"

        s4 = conn.execute("SELECT * FROM applications WHERE email = 'stage4_pending@dbert.test'").fetchone()
        assert s4 is not None and s4["status"] == "Enrollment Pending"

        s5 = conn.execute("SELECT * FROM applications WHERE email = 'stage5_enrolled@dbert.test'").fetchone()
        assert s5 is not None and s5["status"] == "Enrolled"


def test_seeded_stipend_gates():
    with get_db() as conn:
        # Gate 1 Locked (Provisional)
        g1 = conn.execute("SELECT * FROM intern_certificates WHERE email = 'stipend_gate1_locked@dbert.test'").fetchone()
        assert g1 is not None and g1["cert_id"] == "CERT-DBERT-2026-FSD-901"

        # Gate 3 UPI Missing
        g3 = conn.execute("SELECT * FROM intern_accounts WHERE email = 'stipend_gate3_upi@dbert.test'").fetchone()
        assert g3 is not None and g3["upi_id_encrypted"] is None

        # Gate 4 Ready to Submit (Has encrypted UPI + LinkedIn verified)
        g4 = conn.execute("SELECT * FROM intern_accounts WHERE email = 'stipend_ready@dbert.test'").fetchone()
        assert g4 is not None
        assert g4["upi_id_encrypted"] is not None
        assert g4["linkedin_verified"] == 1

        # Staff queue task submission
        sub = conn.execute("SELECT * FROM task_submissions WHERE id = 9305").fetchone()
        assert sub is not None
        assert sub["ai_evaluation_score"] == 88
        assert sub["status"] == "submitted"

        # Wallet credited with 5,000 coins
        w = conn.execute("SELECT * FROM coin_ledger_mirror WHERE id = 9406").fetchone()
        assert w is not None
        assert w["delta"] == 5000
        assert w["balance_after"] == 5000

        # Payout in admin queue
        w_req = conn.execute("SELECT * FROM ambassador_withdrawals WHERE id = 9507").fetchone()
        assert w_req is not None
        assert w_req["amount"] == 5000
        assert w_req["status"] == "requested"


def test_seeded_courses_and_chapters():
    with get_db() as conn:
        courses = conn.execute("SELECT * FROM courses WHERE id IN (1, 2, 3, 4)").fetchall()
        assert len(courses) == 4
        # Verify chapters
        chapters = conn.execute("SELECT * FROM course_chapters WHERE course_id = 1 AND id >= 100").fetchall()
        assert len(chapters) == 4
        # Verify subtopics
        subtopics = conn.execute("SELECT * FROM course_subtopics WHERE chapter_id = 101").fetchall()
        assert len(subtopics) == 2


def test_dev_qa_matrix_route(client):
    res = client.get("/dev/qa-matrix")
    assert res.status_code == 200
    assert b"DBERT QA Matrix" in res.data
    assert b"stage1_apply@dbert.test" in res.data
    assert b"stipend_ready@dbert.test" in res.data


def test_dev_impersonate_route(client):
    # Impersonate Intern
    res = client.get("/dev/impersonate?email=stage5_enrolled@dbert.test&target=/portal", follow_redirects=False)
    assert res.status_code == 302
    assert res.headers["Location"] == "/portal"
    # Check that dbert_auth cookie is set
    set_cookie = res.headers.get("Set-Cookie", "")
    assert "dbert_auth=" in set_cookie


def test_leaderboard_and_certificates_routes(client):
    # Log in as stage 5 enrolled intern
    client.get("/dev/impersonate?email=stage5_enrolled@dbert.test&target=/portal")
    
    # Check /leaderboard redirect
    res_lb = client.get("/leaderboard", follow_redirects=False)
    assert res_lb.status_code == 302
    assert "/portal#leaderboard" in res_lb.headers["Location"]
    
    # Check /certificates redirect
    res_cert = client.get("/certificates", follow_redirects=False)
    assert res_cert.status_code == 302
    assert "/portal#certificate" in res_cert.headers["Location"]


def test_bounty_tasks_page_and_sidebar_links(client):
    # Log in as stage 5 enrolled intern
    client.get("/dev/impersonate?email=stage5_enrolled@dbert.test&target=/portal")
    
    # Fetch /tasks
    res = client.get("/tasks")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    
    # Verify sidebar additions
    assert "Cohort Leaderboard" in html
    assert "My Certificates" in html
    assert 'href="/leaderboard"' in html
    assert 'href="/certificates"' in html
    
    # Verify Bounty Tasks layout
    assert "bounty-hero" in html
    assert 'data-filter="all"' in html
    assert 'data-filter="domain"' in html
    assert 'data-filter="general"' in html
    assert 'data-filter="submitted"' in html
    assert "bounty-footer" in html
    assert "🪙 +" in html


def test_intern_articles_layout_clearance(client):
    # Log in as stage 5 enrolled intern
    client.get("/dev/impersonate?email=stage5_enrolled@dbert.test&target=/intern/articles")

    # Fetch /intern/articles
    res = client.get("/intern/articles")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Verify standard sidebar layout wrapper structure
    assert 'class="has-sidebar"' in html
    assert '<div class="main" id="main-content">' in html
    assert '<div class="content">' in html
    assert '<div class="articles-container">' in html
    assert 'class="nav-item active"' in html


def test_coins_ledger_and_enrolled_authorization(client):
    from app import _intern_payment_verified, calculate_coin_discount
    
    # 1. Verify stage 5 enrolled intern is recognized by _intern_payment_verified
    assert _intern_payment_verified("stage5_enrolled@dbert.test") is True
    
    # 2. Verify /account/coins renders with high-contrast dual ledgers
    client.get("/dev/impersonate?email=stage5_enrolled@dbert.test&target=/account/coins")
    res = client.get("/account/coins")
    assert res.status_code == 200
    html = res.data.decode("utf-8")
    
    assert "DBERT Coins" in html
    assert "Task Coins · Spendable" in html
    assert "Referral &amp; Stipend Coins · Withdrawable" in html
    assert "Transaction History" in html
    assert 'class="has-sidebar portal portal-light"' in html
    
    # 3. Verify stipend_wallet intern renders 5,000 withdrawable coins
    client.get("/dev/impersonate?email=stipend_wallet@dbert.test&target=/account/coins")
    res2 = client.get("/account/coins")
    assert res2.status_code == 200
    html2 = res2.data.decode("utf-8")
    assert "5000" in html2 or "5,000" in html2
    assert "Request UPI Payout" in html2
    
    # 4. Verify coin discount calculation engine
    with get_db() as conn:
        intern = conn.execute("SELECT id FROM intern_accounts WHERE email = 'stage5_enrolled@dbert.test'").fetchone()
        if intern:
            disc, coins, final_p = calculate_coin_discount(intern["id"], 100, email="stage5_enrolled@dbert.test")
            assert disc >= 0
            assert final_p == 100 - disc


def test_admin_payment_verification_modal_scrollbar(client):
    # Log in as admin
    client.get("/dev/impersonate?email=admin@dbert.test&target=/admin")
    res = client.get("/admin")
    assert res.status_code == 200
    html = res.data.decode("utf-8")

    # Verify enrModal structure and scrollbar rules
    assert 'id="enrModal"' in html
    assert 'overflow-y:auto !important' in html or 'overflow-y: auto !important' in html
    assert 'max-height:90vh' in html or 'max-height: 90vh' in html
    assert 'scrollbar-color' in html
    assert 'id="screenshotLink"' in html
    assert 'Open Full-Size Screenshot' in html


def test_intern_ambassador_withdraw_get_and_post(client):
    # Ensure test isolation: remove lingering withdrawals & rate limits for test personas
    with get_db() as conn:
        conn.execute("DELETE FROM ambassador_withdrawals WHERE intern_id IN (9206, 9203)")
        conn.execute("DELETE FROM rate_events WHERE bucket LIKE 'wd:%'")
        conn.commit()

    # 1. Unauthenticated GET redirects to /#signin
    r_unauth = client.get("/intern/ambassador/withdraw")
    assert r_unauth.status_code == 302
    assert "/#signin" in r_unauth.headers.get("Location")

    # 2. Authenticated GET redirects to /ambassador#withdraw
    client.get("/dev/impersonate?email=stipend_wallet@dbert.test&target=/portal")
    r_auth = client.get("/intern/ambassador/withdraw")
    assert r_auth.status_code == 302
    assert "/ambassador#withdraw" in r_auth.headers.get("Location")

    # 3. Authenticated GET with JSON accept header
    r_json = client.get("/intern/ambassador/withdraw", headers={"Accept": "application/json"})
    assert r_json.status_code == 200
    data = r_json.get_json()
    assert data["status"] == "success"
    assert data["balance"] == 5000
    assert data["available_to_withdraw"] == 5000

    # 4. POST without UPI configured returns 400
    client.get("/dev/impersonate?email=stipend_gate3_upi@dbert.test&target=/portal")
    with client.session_transaction() as sess:
        sess["_csrf"] = "test_csrf_token"
    r_post = client.post(
        "/intern/ambassador/withdraw",
        json={"amount": 500},
        headers={"X-CSRF-Token": "test_csrf_token"}
    )
    assert r_post.status_code == 400
    assert "Add your UPI id" in r_post.get_json()["message"]


def test_dashboard_offer_cta_and_offer_letter_table_proportions(client):
    """Verify that dashboard CTA is prominent and full-width, and offer tables have proper column proportions without clipping."""
    # 1. Impersonate stage5_enrolled and verify dashboard CTA
    r_portal = client.get("/dev/impersonate?email=stage5_enrolled@dbert.test&target=/portal", follow_redirects=True)
    assert r_portal.status_code == 200
    portal_html = r_portal.get_data(as_text=True)
    assert "Review &amp; Sign Offer Letter &rarr;" in portal_html
    assert "btn-emerald-action" in portal_html
    assert "Executive Appointment A4" in portal_html
    assert "View Stipend Portal &amp; Tasks &rarr;" in portal_html
    assert "btn-indigo-action" in portal_html

    # 2. Verify offer letter table proportions
    r_offer = client.get("/portal/offer")
    assert r_offer.status_code == 200
    offer_html = r_offer.get_data(as_text=True)
    assert "1. APPOINTMENT TERM SHEET AT A GLANCE" in offer_html
    assert "table-layout:auto" in offer_html
    assert "overflow-x:auto" in offer_html
    assert "min-width:180px" in offer_html
    assert "Directly to verified UPI ID via LMS Wallet within 30 days of completion" in offer_html

    # 3. Verify print view
    r_print = client.get("/portal/offer/print")
    assert r_print.status_code == 200
    print_html = r_print.get_data(as_text=True)
    assert "1. APPOINTMENT TERM SHEET AT A GLANCE" in print_html
    assert "min-width:170px" in print_html






