import os
import sys

PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)

import app as portal_app


def test_lms_program_page_publishes_full_syllabi_and_1999_parity():
    portal_app.app.testing = True
    with portal_app.app.test_client() as client:
        resp = client.get("/program")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)

        assert "1,999" in html
        assert "2 Months" in html
        assert "Data Analytics" in html
        for keyword in [
            "Excel",
            "PostgreSQL",
            "Pandas",
            "NumPy",
            "Power BI",
            "Matplotlib",
            "Seaborn",
            "Jupyter",
            "Aivara",
            "Alkame",
            "https://dbert.in/learners/courses/data-analytics",
        ]:
            assert keyword in html, f"Missing '{keyword}' on /program"

        for forbidden in ["3 Months", "3-Month", "28,000", "9,999", "9999"]:
            assert forbidden not in html, f"Forbidden stale string '{forbidden}' found on /program"


def test_lms_launchpad_and_accelerate_enforce_canonical_2month_prices():
    portal_app.app.testing = True
    with portal_app.app.test_client() as client:
        lp = client.get("/launchpad")
        assert lp.status_code == 200
        lp_html = lp.get_data(as_text=True)
        assert "7,999" in lp_html
        assert "2 Months" in lp_html
        assert "DBERT Launchpad" in lp_html
        assert "3 Months" not in lp_html
        assert "28,000" not in lp_html

        acc = client.get("/accelerate")
        assert acc.status_code == 200
        acc_html = acc.get_data(as_text=True)
        assert "4,999" in acc_html
        assert "2 Months" in acc_html
        assert "DBERT Accelerate" in acc_html
        assert "3 Months" not in acc_html
        assert "28,000" not in acc_html


def test_city_slugify_normalizes_accents_and_sitemap_excludes_umlaut_noise():
    assert portal_app._city_slugify("Zürich") == "zurich"
    assert portal_app._city_slugify("München") == "munchen"
    assert portal_app._city_slugify("Bangalore, India") == "bangalore-india"

    portal_app.app.testing = True
    with portal_app.app.test_client() as client:
        resp = client.get("/sitemap.xml")
        assert resp.status_code == 200
        xml = resp.get_data(as_text=True)
        for bad_slug in ["/internships/zrich", "/internships/mnchen", "/jobs/zrich", "/jobs/mnchen"]:
            assert bad_slug not in xml


def _seed_cohort_user(
    db_path: str,
    *,
    iid: int,
    email: str,
    name: str,
    domain: str = "AI Agent Development",
    joining_days_ago: int = 73,
    product: str = "free_deposit",
    amount: int = 1999,
    amount_paid: int = 1999,
    payment_status: str = "Verified",
    stipend_verified: int = 0,
    stipend_release_date: str | None = None,
    offer_batch_end_days_ago: int | None = None,
):
    import sqlite3
    from datetime import datetime, timedelta
    from werkzeug.security import generate_password_hash

    conn = sqlite3.connect(db_path)
    pw = generate_password_hash("Pass1234!")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    j_date = (datetime.now() - timedelta(days=joining_days_ago)).strftime("%Y-%m-%d")

    conn.execute(
        """
        INSERT INTO applications
        (id, name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at, updated_at)
        VALUES (?, ?, ?, '+91 98765 22222', 'Delhi', 'DTU', 'B.Tech', '6', '2026', ?, 'Production engineering', 'Enrolled', ?, ?)
        """,
        (iid, name, email, domain, now_str, now_str),
    )
    conn.execute(
        """
        INSERT INTO intern_accounts
        (id, application_id, name, email, phone, domain, password_hash, password_set, is_active,
         signup_stage, email_verified, stipend_verified, stipend_amount, stipend_release_date, created_at, updated_at)
        VALUES (?, ?, ?, ?, '+91 98765 22222', ?, ?, 1, 1, 5, 1, ?, 5000, ?, ?, ?)
        """,
        (iid, iid, name, email, domain, pw, stipend_verified, stipend_release_date, now_str, now_str),
    )
    conn.execute(
        """
        INSERT INTO enrollments
        (id, application_id, intern_id, timestamp, name, email, phone, college, domain, joining_date,
         batch_label, payment_status, product, amount, amount_paid, deposit_paid, balance_paid, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, '+91 98765 22222', 'DTU', ?, ?, 'Cohort-Sprint-Test', ?, ?, ?, ?, 1, ?, ?, ?)
        """,
        (
            iid, iid, iid, now_str, name, email, domain, j_date, payment_status, product,
            amount, amount_paid, 1 if amount_paid >= 1999 else 0, now_str, now_str,
        ),
    )
    if offer_batch_end_days_ago is not None:
        b_start = (datetime.now() - timedelta(days=joining_days_ago)).strftime("%Y-%m-%d")
        b_end = (datetime.now() - timedelta(days=offer_batch_end_days_ago)).strftime("%Y-%m-%d")
        conn.execute(
            """
            INSERT INTO intern_offer_letters
            (offer_letter_id, intern_id, enrollment_id, email, name, domain, batch_start_date, batch_end_date,
             caution_deposit_status, pdf_unlocked, signature_name, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'VERIFIED', 1, ?, ?)
            """,
            (f"DBERT-OFR-{iid}", iid, iid, email, name, domain, b_start, b_end, name, now_str),
        )
    conn.commit()
    conn.close()


def _auth_intern(client, email: str):
    token = portal_app.create_session(email, "intern")
    client.set_cookie(portal_app.AUTH_COOKIE, token)


def test_stage5b_tenure_expired_sync_across_intern_me_program_portal_and_tasks(app_client):
    client, db_path = app_client
    _seed_cohort_user(
        db_path,
        iid=9206,
        email="kavya_stage5b@dbert.test",
        name="Kavya Nair",
        joining_days_ago=73,
        product="free_deposit",
        amount=1999,
        amount_paid=1999,
        stipend_verified=1,
        stipend_release_date=None,
        offer_batch_end_days_ago=13,
    )
    _auth_intern(client, "kavya_stage5b@dbert.test")

    me_resp = client.get("/intern/me")
    assert me_resp.status_code == 200
    me = me_resp.get_json()
    assert me["intern"]["is_tenure_expired"] is True
    assert me["is_paid_program_settled"] is True
    assert me["has_caution_deposit_only"] is False
    assert "rejoin=1" in me["rejoin_enroll_url"]
    assert "dbert.in/enroll/1999" in me["rejoin_enroll_url"]
    assert me["next_action"]["stage_badge"].startswith("Stage 5B:")

    portal_resp = client.get("/portal")
    assert portal_resp.status_code == 200
    portal_html = portal_resp.get_data(as_text=True)
    assert "window._IS_TENURE_EXPIRED = true" in portal_html
    assert "Previous 8-Week Cohort Ended" in portal_html

    prog_resp = client.get("/program")
    assert prog_resp.status_code == 200
    prog_html = prog_resp.get_data(as_text=True)
    assert 'id="ctaTenureExpired"' in prog_html
    assert 'id="ctaTenureOpenLmsFormBtn"' in prog_html
    assert "admin_note.includes('UTR')" not in prog_html

    tasks_resp = client.get("/tasks", follow_redirects=False)
    assert tasks_resp.status_code == 302


def test_stipend_verified_with_future_release_date_stays_active(app_client):
    from datetime import date, timedelta

    client, db_path = app_client
    future_release = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
    _seed_cohort_user(
        db_path,
        iid=4442,
        email="scheduled_fellow@dbert.test",
        name="Molugu Nanda",
        joining_days_ago=73,
        product="paid_program",
        amount=1999,
        amount_paid=1999,
        stipend_verified=1,
        stipend_release_date=future_release,
    )
    _auth_intern(client, "scheduled_fellow@dbert.test")

    me = client.get("/intern/me").get_json()
    assert me["intern"]["is_tenure_expired"] is False
    assert me["is_paid_program_settled"] is True

    tasks_resp = client.get("/tasks", follow_redirects=False)
    assert tasks_resp.status_code == 200


def test_caution_deposit_499_never_marked_paid_in_full(app_client):
    client, db_path = app_client
    _seed_cohort_user(
        db_path,
        iid=8101,
        email="deposit_only@dbert.test",
        name="Riya Sharma",
        joining_days_ago=3,
        product="free_deposit",
        amount=499,
        amount_paid=499,
    )
    _auth_intern(client, "deposit_only@dbert.test")

    me = client.get("/intern/me").get_json()
    assert me["intern"]["is_tenure_expired"] is False
    assert me["is_paid_program_settled"] is False
    assert me["has_caution_deposit_only"] is True


def test_rejoin_enrollment_sync_inserts_fresh_cohort_and_clears_stage5b(app_client):
    import sqlite3
    from datetime import date

    client, db_path = app_client
    _seed_cohort_user(
        db_path,
        iid=9207,
        email="rejoin_fellow@dbert.test",
        name="Kavya Rejoin",
        domain="AI Agent Development",
        joining_days_ago=73,
        product="free_deposit",
        amount=1999,
        amount_paid=1999,
        stipend_verified=1,
        stipend_release_date=None,
        offer_batch_end_days_ago=13,
    )

    sync_resp = client.post(
        "/api/internal/enrollment-sync",
        headers={"X-DBERT-Internal-Secret": portal_app.INTERNAL_SYNC_SECRET},
        json={
            "name": "Kavya Rejoin",
            "email": "rejoin_fellow@dbert.test",
            "domain": "Data Analytics",
            "amount": 1500,
            "payment_type": "balance",
            "utr": "998877665544",
            "submission_id": "DBERT-ENR-REJOIN-01",
            "remarks": "[REJOIN_NEW_COHORT]",
            "rejoin": True,
        },
    )
    assert sync_resp.status_code == 200, sync_resp.get_data(as_text=True)
    sync_data = sync_resp.get_json()
    assert sync_data["rejoin"] is True

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    enr_rows = conn.execute(
        "SELECT id, joining_date, product, amount, amount_paid FROM enrollments WHERE email='rejoin_fellow@dbert.test' ORDER BY id ASC"
    ).fetchall()
    acct = conn.execute(
        "SELECT signup_stage, domain FROM intern_accounts WHERE email='rejoin_fellow@dbert.test'"
    ).fetchone()
    conn.close()

    assert len(enr_rows) == 2
    assert enr_rows[-1]["joining_date"] > date.today().strftime("%Y-%m-%d")
    assert enr_rows[-1]["product"] == "paid_program"
    assert enr_rows[-1]["amount_paid"] == 1999
    assert acct["signup_stage"] == 5
    assert acct["domain"] == "Data Analyst"

    _auth_intern(client, "rejoin_fellow@dbert.test")
    me = client.get("/intern/me").get_json()
    assert me["intern"]["is_tenure_expired"] is False
    assert me["is_paid_program_settled"] is True
    assert client.get("/tasks", follow_redirects=False).status_code == 200

