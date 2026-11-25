"""
Milestone Phase 4 Test Suite: Feature Gating & Application Gating Decorator.
Verifies require_confirmed_fellow decorator, multi-stage redirect policies,
flash messaging, POST route gating, and template JS globals.
"""

import sys
import re
from pathlib import Path
import pytest

PORTAL_DIR = Path(__file__).resolve().parent.parent
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from app import app as flask_app, get_db
from tests.conftest import seed_intern, login_as_intern


def _create_and_login_intern(client, db_path, stage: int, email: str, name: str = "Test Fellow"):
    """Helper to seed an intern, explicitly set signup_stage, and log in via client."""
    seed_intern(db_path, email=email, password="TestPassword123!", name=name, status="Accepted")
    with get_db() as conn:
        conn.execute("UPDATE intern_accounts SET signup_stage = ? WHERE email = ?", (stage, email))
        conn.commit()
    login_as_intern(client, db_path, email=email, password="TestPassword123!", name=name)
    return email


def _get_flashed_messages(client):
    """Helper to inspect flashed messages in the client session."""
    with client.session_transaction() as sess:
        return [msg for _, msg in sess.get("_flashes", [])]


def _seed_sprint_fixtures(db_path):
    """Helper to seed an active task and an available mentor slot for HTTP 200 tests."""
    with get_db() as conn:
        # Active sprint task
        conn.execute("""
            INSERT OR IGNORE INTO tasks (id, title, description, task_type, payment_type, coin_reward, submission_type, is_active)
            VALUES (401, 'Phase 4 Gated Sprint Task', 'Verify feature gating decorator', 'general', 'coins', 50, 'url', 1)
        """)
        # Staff account & mentor slot
        conn.execute("""
            INSERT OR IGNORE INTO staff_accounts (id, name, email, password_hash, is_active, role)
            VALUES (901, 'Sprint Mentor', 'sprint_mentor@test.com', 'dummy_hash', 1, 'staff')
        """)
        # Admin account
        conn.execute("""
            INSERT OR IGNORE INTO staff_accounts (id, name, email, password_hash, is_active, role)
            VALUES (101, 'Sprint Admin', 'admin@dbert.in', 'dummy_hash', 1, 'admin')
        """)
        conn.execute("""
            INSERT OR IGNORE INTO mentor_availability_slots (id, mentor_staff_id, start_time, end_time, is_booked, seats_booked)
            VALUES (402, 901, datetime('now', '+1 day'), datetime('now', '+1 day', '+45 minutes'), 0, 0)
        """)
        conn.commit()


# ============================================================================
# 1. Unauthenticated Request Redirection
# ============================================================================

def test_unauthenticated_request_to_tasks_redirects_to_login(app_client):
    """Unauthenticated visitor requesting /tasks must be redirected to /intern/login."""
    client, _ = app_client
    resp = client.get("/tasks", follow_redirects=False)
    assert resp.status_code == 302
    location = resp.headers.get("Location", "")
    assert location.endswith("/intern/login") or location == "/intern/login", f"Unexpected location: {location}"


def test_unauthenticated_request_to_gated_routes_redirects_to_login(app_client):
    """Unauthenticated requests to all sprint routes redirect to /intern/login."""
    client, _ = app_client
    for route in ["/tasks", "/mentors/slots", "/stipend/tasks"]:
        resp = client.get(route, follow_redirects=False)
        assert resp.status_code == 302, f"Expected 302 for unauthenticated {route}, got {resp.status_code}"
        location = resp.headers.get("Location", "")
        assert location.endswith("/intern/login") or location == "/intern/login", f"Unexpected location {location} for {route}"


# ============================================================================
# 2. Stage 1 Intern Redirection & Flash Message
# ============================================================================

def test_stage1_intern_tasks_redirects_to_portal_with_flash(app_client):
    """Stage 1 intern requesting /tasks redirects to /portal with review flash message."""
    client, db_path = app_client
    _create_and_login_intern(client, db_path, stage=1, email="stage1_fellow@test.com")

    resp = client.get("/tasks", follow_redirects=False)
    assert resp.status_code == 302
    location = resp.headers.get("Location", "")
    assert location.endswith("/portal") or location == "/portal"

    flashes = _get_flashed_messages(client)
    assert any("Your application is currently under review. Sprint features unlock upon selection." in msg for msg in flashes), \
        f"Flash message mismatch. Got: {flashes}"


# ============================================================================
# 3. Stage 2 Intern Redirection & Flash Message (/tasks, /mentors/slots, /stipend/tasks)
# ============================================================================

@pytest.mark.parametrize("route", ["/tasks", "/mentors/slots", "/stipend/tasks", "/ambassador"])
def test_stage2_intern_routes_redirect_to_portal_with_flash(app_client, route):
    """Stage 2 intern requesting sprint routes redirects to /portal with review flash."""
    client, db_path = app_client
    clean_route = route.replace("/", "_")
    _create_and_login_intern(client, db_path, stage=2, email=f"stage2_{clean_route}@test.com")

    resp = client.get(route, follow_redirects=False)
    assert resp.status_code == 302, f"Failed for {route}: expected 302, got {resp.status_code}"
    location = resp.headers.get("Location", "")
    assert location.endswith("/portal") or location == "/portal", f"Failed for {route}: unexpected location {location}"

    flashes = _get_flashed_messages(client)
    assert any("Your application is currently under review. Sprint features unlock upon selection." in msg for msg in flashes), \
        f"Flash message missing for {route}: {flashes}"


# ============================================================================
# 4. Stage 3 Intern Redirection & Flash Message (/tasks, /mentors/slots, /stipend/tasks)
# ============================================================================

@pytest.mark.parametrize("route", ["/tasks", "/mentors/slots", "/stipend/tasks", "/ambassador"])
def test_stage3_intern_routes_redirect_to_offer_with_flash(app_client, route):
    """Stage 3 intern requesting sprint routes redirects to /portal/offer with seat confirmation flash."""
    client, db_path = app_client
    clean_route = route.replace("/", "_")
    _create_and_login_intern(client, db_path, stage=3, email=f"stage3_{clean_route}@test.com")

    resp = client.get(route, follow_redirects=False)
    assert resp.status_code == 302, f"Failed for {route}: expected 302, got {resp.status_code}"
    location = resp.headers.get("Location", "")
    assert location.endswith("/portal/offer") or location == "/portal/offer", f"Failed for {route}: unexpected location {location}"

    flashes = _get_flashed_messages(client)
    assert any("Please complete your seat confirmation on /portal/offer to unlock production sprint tasks." in msg for msg in flashes), \
        f"Flash message missing for {route}: {flashes}"


# ============================================================================
# 5. Stage 4 Intern Redirection & Flash Message (/tasks, /mentors/slots, /stipend/tasks)
# ============================================================================

@pytest.mark.parametrize("route", ["/tasks", "/mentors/slots", "/stipend/tasks", "/ambassador"])
def test_stage4_intern_routes_redirect_to_portal_with_flash(app_client, route):
    """Stage 4 intern requesting sprint routes redirects to /portal with payment verification flash."""
    client, db_path = app_client
    clean_route = route.replace("/", "_")
    _create_and_login_intern(client, db_path, stage=4, email=f"stage4_{clean_route}@test.com")

    resp = client.get(route, follow_redirects=False)
    assert resp.status_code == 302, f"Failed for {route}: expected 302, got {resp.status_code}"
    location = resp.headers.get("Location", "")
    assert location.endswith("/portal") or location == "/portal", f"Failed for {route}: unexpected location {location}"

    flashes = _get_flashed_messages(client)
    assert any("Your payment is being verified. Your workspace will unlock shortly." in msg for msg in flashes), \
        f"Flash message missing for {route}: {flashes}"


# ============================================================================
# 6. Stage 5 Confirmed Fellow HTTP 200 Access
# ============================================================================

@pytest.mark.parametrize("route", ["/tasks", "/mentors/slots", "/stipend/tasks", "/ambassador"])
def test_stage5_confirmed_fellow_routes_load_success_200(app_client, route):
    """Stage 5 confirmed fellow requesting sprint routes loads workspace successfully (HTTP 200)."""
    client, db_path = app_client
    _seed_sprint_fixtures(db_path)
    clean_route = route.replace("/", "_")
    _create_and_login_intern(client, db_path, stage=5, email=f"stage5_{clean_route}@test.com")

    resp = client.get(route, follow_redirects=False)
    assert resp.status_code == 200, f"Expected 200 for Stage 5 accessing {route}, got {resp.status_code}"


# ============================================================================
# 7. POST Route Gating: /tasks/<id>/submit
# ============================================================================

def test_post_task_submit_gating(app_client):
    """Unconfirmed interns cannot submit tasks (POST /tasks/<id>/submit)."""
    client, db_path = app_client
    _seed_sprint_fixtures(db_path)

    # 1. Unauthenticated request -> blocked
    r_unauth = client.post("/tasks/401/submit", data={"content": "https://github.com/test/repo"}, follow_redirects=False)
    assert r_unauth.status_code in (302, 401)
    if r_unauth.status_code == 302:
        assert r_unauth.headers.get("Location", "").endswith("/intern/login") or r_unauth.headers.get("Location", "") == "/intern/login"

    # 2. Stage 2 intern -> blocked (redirect /portal or 403)
    _create_and_login_intern(client, db_path, stage=2, email="submit_stage2@test.com")
    r_stage2 = client.post("/tasks/401/submit", data={"content": "https://github.com/test/repo"}, follow_redirects=False)
    assert r_stage2.status_code in (302, 403)
    if r_stage2.status_code == 302:
        assert r_stage2.headers.get("Location", "").endswith("/portal")

    # 3. Stage 3 intern -> blocked (redirect /portal/offer or 403)
    _create_and_login_intern(client, db_path, stage=3, email="submit_stage3@test.com")
    r_stage3 = client.post("/tasks/401/submit", data={"content": "https://github.com/test/repo"}, follow_redirects=False)
    assert r_stage3.status_code in (302, 403)
    if r_stage3.status_code == 302:
        assert r_stage3.headers.get("Location", "").endswith("/portal/offer")

    # 4. Stage 4 intern -> blocked (redirect /portal or 403)
    _create_and_login_intern(client, db_path, stage=4, email="submit_stage4@test.com")
    r_stage4 = client.post("/tasks/401/submit", data={"content": "https://github.com/test/repo"}, follow_redirects=False)
    assert r_stage4.status_code in (302, 403)
    if r_stage4.status_code == 302:
        assert r_stage4.headers.get("Location", "").endswith("/portal")

    # Verify zero submissions recorded in DB from blocked attempts
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM task_submissions WHERE task_id = 401").fetchone()["c"]
        assert count == 0, f"Expected 0 submissions, found {count}"

    # 5. Stage 5 intern -> passes decorator gate into view function
    _create_and_login_intern(client, db_path, stage=5, email="submit_stage5@test.com")
    r_stage5 = client.post("/tasks/401/submit", json={"content": "https://github.com/test/repo"}, follow_redirects=False)
    # Passed gating decorator; not redirected to gate URLs (/portal or /portal/offer)
    if r_stage5.status_code == 302:
        assert not r_stage5.headers.get("Location", "").endswith("/portal")
        assert not r_stage5.headers.get("Location", "").endswith("/portal/offer")


# ============================================================================
# 8. POST Route Gating: /mentors/slots/<id>/book
# ============================================================================

def test_post_mentor_slot_book_gating(app_client):
    """Unconfirmed interns cannot book mentor slots (POST /mentors/slots/<id>/book)."""
    client, db_path = app_client
    _seed_sprint_fixtures(db_path)

    # 1. Unauthenticated request -> blocked
    r_unauth = client.post("/mentors/slots/402/book", follow_redirects=False)
    assert r_unauth.status_code in (302, 401)

    # 2. Stage 2 intern -> blocked
    _create_and_login_intern(client, db_path, stage=2, email="book_stage2@test.com")
    r_stage2 = client.post("/mentors/slots/402/book", follow_redirects=False)
    assert r_stage2.status_code in (302, 403)
    if r_stage2.status_code == 302:
        assert r_stage2.headers.get("Location", "").endswith("/portal")

    # 3. Stage 3 intern -> blocked
    _create_and_login_intern(client, db_path, stage=3, email="book_stage3@test.com")
    r_stage3 = client.post("/mentors/slots/402/book", follow_redirects=False)
    assert r_stage3.status_code in (302, 403)
    if r_stage3.status_code == 302:
        assert r_stage3.headers.get("Location", "").endswith("/portal/offer")

    # 4. Stage 4 intern -> blocked
    _create_and_login_intern(client, db_path, stage=4, email="book_stage4@test.com")
    r_stage4 = client.post("/mentors/slots/402/book", follow_redirects=False)
    assert r_stage4.status_code in (302, 403)
    if r_stage4.status_code == 302:
        assert r_stage4.headers.get("Location", "").endswith("/portal")

    # Verify zero bookings recorded in DB from blocked attempts
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM mentor_session_bookings WHERE slot_id = 402").fetchone()["c"]
        assert count == 0, f"Expected 0 bookings, found {count}"

    # 5. Stage 5 intern -> passes decorator gate
    _create_and_login_intern(client, db_path, stage=5, email="book_stage5@test.com")
    r_stage5 = client.post("/mentors/slots/402/book", follow_redirects=False)
    if r_stage5.status_code == 302:
        assert not r_stage5.headers.get("Location", "").endswith("/portal")
        assert not r_stage5.headers.get("Location", "").endswith("/portal/offer")


# ============================================================================
# 9. Template JS Globals: window._USER_SIGNUP_STAGE & showGateModal
# ============================================================================

def test_template_output_contains_signup_stage_and_gate_modal(app_client):
    """LMS templates render window._USER_SIGNUP_STAGE and showGateModal JS definition."""
    client, db_path = app_client

    # Test Stage 2 intern
    _create_and_login_intern(client, db_path, stage=2, email="template_stage2@test.com")
    resp_s2 = client.get("/portal")
    assert resp_s2.status_code == 200
    html_s2 = resp_s2.data.decode("utf-8")
    assert "window._USER_SIGNUP_STAGE" in html_s2, "Missing window._USER_SIGNUP_STAGE in /portal output"
    assert "showGateModal" in html_s2, "Missing showGateModal in /portal output"
    assert re.search(r"window\._USER_SIGNUP_STAGE\s*=\s*2", html_s2) is not None, "window._USER_SIGNUP_STAGE should be 2"

    # Test Stage 3 intern
    _create_and_login_intern(client, db_path, stage=3, email="template_stage3@test.com")
    resp_s3 = client.get("/portal")
    assert resp_s3.status_code == 200
    html_s3 = resp_s3.data.decode("utf-8")
    assert re.search(r"window\._USER_SIGNUP_STAGE\s*=\s*3", html_s3) is not None, "window._USER_SIGNUP_STAGE should be 3"

    # Test Stage 5 intern
    _create_and_login_intern(client, db_path, stage=5, email="template_stage5@test.com")
    resp_s5 = client.get("/portal")
    assert resp_s5.status_code == 200
    html_s5 = resp_s5.data.decode("utf-8")
    assert re.search(r"window\._USER_SIGNUP_STAGE\s*=\s*5", html_s5) is not None, "window._USER_SIGNUP_STAGE should be 5"


# ============================================================================
# 10. Decorator Unit Test
# ============================================================================

def test_require_confirmed_fellow_decorator_unit(monkeypatch):
    """Direct isolated unit test of require_confirmed_fellow decorator."""
    import app
    assert hasattr(app, "require_confirmed_fellow"), "apps/portal/app.py must define require_confirmed_fellow"
    require_confirmed_fellow = app.require_confirmed_fellow

    from flask import Flask, get_flashed_messages

    dummy_app = Flask("dummy_gate_unit")
    dummy_app.secret_key = "dummy_secret_for_unit_tests_32chars"

    @dummy_app.route("/guarded")
    @require_confirmed_fellow
    def guarded_view():
        return "SUCCESS", 200

    # Case 1: Unauthenticated -> /intern/login
    with dummy_app.test_request_context("/guarded"):
        monkeypatch.setattr("app.get_current_intern", lambda: None)
        r1 = guarded_view()
        assert r1.status_code == 302
        assert r1.headers.get("Location") == "/intern/login"

    # Case 2: Stage 1 -> /portal with info flash
    with dummy_app.test_request_context("/guarded"):
        monkeypatch.setattr("app.get_current_intern", lambda: {"id": 1, "signup_stage": 1})
        r2 = guarded_view()
        assert r2.status_code == 302
        assert r2.headers.get("Location") == "/portal"
        assert any("Your application is currently under review" in msg for msg in get_flashed_messages())

    # Case 3: Stage 2 -> /portal with info flash
    with dummy_app.test_request_context("/guarded"):
        monkeypatch.setattr("app.get_current_intern", lambda: {"id": 2, "signup_stage": 2})
        r3 = guarded_view()
        assert r3.status_code == 302
        assert r3.headers.get("Location") == "/portal"
        assert any("Your application is currently under review" in msg for msg in get_flashed_messages())

    # Case 4: Stage 3 -> /portal/offer with warning flash
    with dummy_app.test_request_context("/guarded"):
        monkeypatch.setattr("app.get_current_intern", lambda: {"id": 3, "signup_stage": 3})
        r4 = guarded_view()
        assert r4.status_code == 302
        assert r4.headers.get("Location") == "/portal/offer"
        assert any("Please complete your seat confirmation" in msg for msg in get_flashed_messages())

    # Case 5: Stage 4 -> /portal with info flash
    with dummy_app.test_request_context("/guarded"):
        monkeypatch.setattr("app.get_current_intern", lambda: {"id": 4, "signup_stage": 4})
        r5 = guarded_view()
        assert r5.status_code == 302
        assert r5.headers.get("Location") == "/portal"
        assert any("Your payment is being verified" in msg for msg in get_flashed_messages())

    # Case 6: Stage 5 -> Allowed (HTTP 200)
    with dummy_app.test_request_context("/guarded"):
        monkeypatch.setattr("app.get_current_intern", lambda: {"id": 5, "signup_stage": 5})
        r6 = guarded_view()
        assert r6 == ("SUCCESS", 200)

    # Case 7: Staff session bypass -> Allowed (HTTP 200)
    with dummy_app.test_request_context("/guarded"):
        from flask import session
        session["staff_id"] = 901
        r7 = guarded_view()
        assert r7 == ("SUCCESS", 200)

    # Case 8: Admin session bypass -> Allowed (HTTP 200)
    with dummy_app.test_request_context("/guarded"):
        from flask import session
        session.clear()
        session["admin_id"] = 101
        r8 = guarded_view()
        assert r8 == ("SUCCESS", 200)

    # Case 9: Non-numeric signup_stage -> Safely defaults to Stage 2 (/portal with info flash)
    with dummy_app.test_request_context("/guarded"):
        from flask import session
        session.clear()
        monkeypatch.setattr("app.get_current_intern", lambda: {"id": 9, "signup_stage": "malformed_string"})
        r9 = guarded_view()
        assert r9.status_code == 302
        assert r9.headers.get("Location") == "/portal"
        assert any("Your application is currently under review" in msg for msg in get_flashed_messages())


# ============================================================================
# 11. Staff & Admin Access, require_admin Fallback, and Malformed Stage
# ============================================================================

@pytest.mark.parametrize("route", ["/tasks", "/mentors/slots", "/stipend/tasks"])
def test_authenticated_staff_tasks_access_200(app_client, route):
    """Authenticated staff (session['staff_id']=901) accessing gated sprint routes returns HTTP 200."""
    client, db_path = app_client
    _seed_sprint_fixtures(db_path)
    with client.session_transaction() as sess:
        sess.clear()
        sess["staff_id"] = 901
        sess["staff_email"] = "sprint_mentor@test.com"
        sess["staff_name"] = "Sprint Mentor"
    resp = client.get(route, follow_redirects=False)
    assert resp.status_code == 200, f"Expected 200 for staff accessing {route}, got {resp.status_code}"


@pytest.mark.parametrize("route", ["/tasks", "/mentors/slots", "/stipend/tasks"])
def test_authenticated_admin_tasks_access_200(app_client, route):
    """Authenticated admin (session['admin_id']=101) accessing gated sprint routes returns HTTP 200."""
    client, db_path = app_client
    _seed_sprint_fixtures(db_path)
    with client.session_transaction() as sess:
        sess.clear()
        sess["admin_id"] = 101
        sess["staff_email"] = "admin@dbert.in"
        sess["staff_name"] = "Sprint Admin"
    resp = client.get(route, follow_redirects=False)
    assert resp.status_code == 200, f"Expected 200 for admin accessing {route}, got {resp.status_code}"


def test_require_admin_session_fallback():
    """require_admin() returns a valid admin dict from session fallback."""
    from app import app as flask_app, require_admin
    from flask import session

    with flask_app.test_request_context():
        session.clear()
        session["admin_id"] = 101
        session["staff_email"] = "admin@dbert.in"
        admin = require_admin()
        assert admin is not None
        assert admin["id"] == 101
        assert admin["role"] == "admin"
        assert admin["email"] == "admin@dbert.in"

    with flask_app.test_request_context():
        session.clear()
        session["role"] = "superadmin"
        session["staff_email"] = "superadmin@dbert.in"
        admin = require_admin()
        assert admin is not None
        assert admin["role"] == "superadmin"
        assert admin["email"] == "superadmin@dbert.in"


def test_non_numeric_signup_stage_defaults_to_stage2_redirect(app_client):
    """Non-numeric or malformed signup_stage safely defaults to Stage 2 redirect with info flash."""
    client, db_path = app_client
    email = "corrupt_stage@test.com"
    _create_and_login_intern(client, db_path, stage=2, email=email)

    with get_db() as conn:
        conn.execute("UPDATE intern_accounts SET signup_stage = ? WHERE email = ?", ("not_a_valid_number", email))
        conn.commit()

    resp = client.get("/tasks", follow_redirects=False)
    assert resp.status_code == 302, f"Expected 302, got {resp.status_code}"
    location = resp.headers.get("Location", "")
    assert location.endswith("/portal") or location == "/portal", f"Expected redirect to /portal, got {location}"

    flashes = _get_flashed_messages(client)
    assert any("Your application is currently under review. Sprint features unlock upon selection." in msg for msg in flashes), \
        f"Flash message mismatch. Got: {flashes}"

