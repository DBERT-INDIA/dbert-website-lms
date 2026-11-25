"""
Comprehensive Multi-Stage & Tenure Locking Test Suite (V2)
Tests:
1. New application flow (/signup/stage1 -> /signup/stage2 -> /signup/stage3) sets signup_stage=2 (Under Review)
   and intern_login() does NOT bounce completed applicants back to /#signup.
2. Stage 0 (Rejected), Stage 1, Stage 2, Stage 3 (Selected Unpaid), Stage 4 (Deposit Verifying)
   gating across /tasks, /mentors/slots, /stipend/tasks.
3. Stage 5A (Active <= 65d) unlocked access on /tasks, /mentors/slots, /stipend/tasks.
4. Stage 5B (Expired > 65d, no 1999) locks /tasks, /mentors/slots, /portal/offer with enroll/1999 CTA,
   while keeping /certificates and /account/coins accessible (200).
5. Stage 5D (Expired > 65d with stipend_verified=1, stipend_amount=5499) keeps /tasks locked
   and surfaces ₹5,499 approved release & 5,499 coins in /account/coins & /intern/ambassador/withdraw.
"""

import sys
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import pytest

PORTAL_DIR = Path(__file__).resolve().parent.parent
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

import app as portal_app
from werkzeug.security import generate_password_hash


def _seed_intern(db_path, *, iid, email, stage, app_status, joining_days_ago=None, payment_status=None, stipend_verified=0, stipend_amount=0, coins=0):
    conn = sqlite3.connect(db_path)
    pw = generate_password_hash("TestPass123!")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        """
        INSERT INTO applications (id, name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at, updated_at)
        VALUES (?, ?, ?, '+91 98765 00000', 'Bengaluru', 'IIT Tech', 'B.Tech', '6', '2026', 'Full Stack Web Development', 'Build real software', ?, ?, ?)
        """,
        (iid, f"User {iid}", email, app_status, now_str, now_str),
    )
    conn.execute(
        """
        INSERT INTO intern_accounts (
            id, application_id, name, email, phone, domain, password_hash, password_set,
            is_active, signup_stage, email_verified, stipend_verified, stipend_amount, created_at, updated_at
        ) VALUES (?, ?, ?, ?, '+91 98765 00000', 'Full Stack Web Development', ?, 1, 1, ?, 1, ?, ?, ?, ?)
        """,
        (iid, iid, f"User {iid}", email, pw, stage, stipend_verified, stipend_amount, now_str, now_str),
    )
    if payment_status:
        j_date = (datetime.now() - timedelta(days=joining_days_ago or 10)).strftime("%Y-%m-%d")
        conn.execute(
            """
            INSERT INTO enrollments (id, application_id, timestamp, name, email, domain, joining_date, payment_status, product, amount, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'Full Stack Web Development', ?, ?, 'free_deposit', 499, ?, ?)
            """,
            (iid, iid, now_str, f"User {iid}", email, j_date, payment_status, now_str, now_str),
        )
    if coins > 0:
        conn.execute(
            """
            INSERT INTO coin_ledger_mirror (intern_id, email, delta, ledger_kind, reason, event_ts, idem_key)
            VALUES (?, ?, ?, 'referral', 'stipend_release_5499', ?, ?)
            """,
            (iid, email, coins, now_str, f"stipend_release_5499_{iid}"),
        )
    conn.commit()
    conn.close()


def _login_session(client, email):
    token = portal_app.create_session(email, "intern")
    client.set_cookie(portal_app.AUTH_COOKIE, token)


def test_new_application_flow_lands_at_stage2_and_does_not_bounce(app_client):
    client, db_path = app_client
    portal_app.CSRF_EXEMPT_ENDPOINTS.update(["signup_stage1", "signup_stage2", "signup_stage3"])
    r1 = client.post("/signup/stage1", json={
        "name": "Fresh Applicant",
        "email": "fresh_app@gmail.com",
        "phone": "9876543210",
        "password": "Password123!",
        "domain": "Full Stack Web Development",
        "terms_accepted": True,
    })
    assert r1.status_code in (200, 201), r1.get_data(as_text=True)

    r2 = client.post("/signup/stage2", json={
        "college": "Test Institute",
        "city": "Bengaluru",
        "course": "B.Tech",
        "semester": "6th Semester",
        "year_of_passing": "2026",
    })
    assert r2.status_code == 200, r2.get_data(as_text=True)

    r3 = client.post("/signup/stage3", json={
        "why_join": "Build production software",
        "portfolio": "https://github.com/example",
    })
    assert r3.status_code == 200, r3.get_data(as_text=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT signup_stage, application_id FROM intern_accounts WHERE email='fresh_app@gmail.com'").fetchone()
    conn.close()
    assert row["signup_stage"] == 2
    assert row["application_id"] is not None

    # Logging in again must NOT bounce back to /#signup
    r_login = client.post("/intern/login", json={"email": "fresh_app@gmail.com", "password": "Password123!"})
    assert r_login.status_code == 200
    assert r_login.get_json().get("redirect") != "/#signup"

    # /tasks redirects to /portal (Stage 2 Under Review), NOT /portal/offer
    r_tasks = client.get("/tasks", follow_redirects=False)
    assert r_tasks.status_code == 302
    assert "/portal" in r_tasks.headers["Location"]
    assert "/portal/offer" not in r_tasks.headers["Location"]


@pytest.mark.parametrize("iid,stage,app_status,expected_loc", [
    (8100, 0, "Rejected", "/portal"),
    (8101, 1, "Apply Pending", "/portal"),
    (8102, 2, "Under Review", "/portal"),
    (8103, 3, "Selected", "/portal/offer"),
    (8104, 4, "Enrollment Pending", "/portal"),
])
def test_pre_confirmed_stages_gating(app_client, iid, stage, app_status, expected_loc):
    client, db_path = app_client
    email = f"stage_{stage}@dbert.test"
    _seed_intern(db_path, iid=iid, email=email, stage=stage, app_status=app_status)
    _login_session(client, email)

    for route in ["/tasks", "/mentors/slots", "/stipend/tasks"]:
        res = client.get(route, follow_redirects=False)
        assert res.status_code == 302
        assert expected_loc in res.headers["Location"]


def test_stage5_active_unlocked(app_client):
    client, db_path = app_client
    _seed_intern(db_path, iid=8105, email="active5@dbert.test", stage=5, app_status="Enrolled", joining_days_ago=15, payment_status="Verified")
    _login_session(client, "active5@dbert.test")

    for route in ["/portal", "/tasks", "/mentors/slots", "/stipend/tasks", "/account/coins"]:
        res = client.get(route, follow_redirects=False)
        assert res.status_code == 200, f"{route} returned {res.status_code}"


def test_stage5_expired_tenure_locks_sprints_but_allows_coins_and_certs(app_client):
    client, db_path = app_client
    _seed_intern(db_path, iid=8106, email="expired5@dbert.test", stage=5, app_status="Enrolled", joining_days_ago=80, payment_status="Verified")
    _login_session(client, "expired5@dbert.test")

    for locked_route in ["/tasks", "/mentors/slots", "/portal/offer"]:
        res = client.get(locked_route, follow_redirects=False)
        assert res.status_code == 302
        assert "/portal" in res.headers["Location"]

    r_portal = client.get("/portal")
    assert r_portal.status_code == 200
    html = r_portal.get_data(as_text=True)
    assert "Tenure Expired for Previous Internship Program" in html
    assert "https://dbert.in/enroll/1999" in html

    assert client.get("/account/coins").status_code == 200
    assert client.get("/certificates").status_code == 200


def test_stage5_expired_with_5499_approved_shows_in_coins(app_client):
    client, db_path = app_client
    _seed_intern(
        db_path, iid=8107, email="expired5499@dbert.test", stage=5, app_status="Enrolled",
        joining_days_ago=100, payment_status="Verified", stipend_verified=1, stipend_amount=5499, coins=5499
    )
    _login_session(client, "expired5499@dbert.test")

    assert client.get("/tasks", follow_redirects=False).status_code == 302

    r_coins = client.get("/account/coins")
    assert r_coins.status_code == 200
    coins_html = r_coins.get_data(as_text=True)
    assert "5499" in coins_html
    assert "Approved Stipend" in coins_html

    r_wd = client.get("/intern/ambassador/withdraw", follow_redirects=True)
    assert r_wd.status_code == 200
