"""
Milestone Phase 5 Test Suite: Student Profile Domain Switching & Account Security Engine.
Verifies POST /api/intern/profile/update and POST /api/account/change-password:
- Unauthorized access controls (HTTP 401)
- Pre-enrollment domain track switching for Stage < 5 (HTTP 200 + DB sync)
- Offer letter domain synchronization for Stage 3 interns (HTTP 200 + DB sync)
- Active cohort tenure lock (Stage >= 5) with 5-day grace period enforcement (HTTP 403)
- Expired tenure domain switching for completed interns (HTTP 200 + DB sync)
- Profile field updates (name, phone, college)
- Password validation, bcrypt hashing, and subsequent login verification
- /intern/me API is_tenure_expired payload verification
- Template UI element validation in portal.html
"""

import sys
import datetime
from pathlib import Path
import pytest
import bcrypt

PORTAL_DIR = Path(__file__).resolve().parent.parent
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from app import app as flask_app, get_db, CSRF_EXEMPT_ENDPOINTS
from tests.conftest import seed_intern, login_as_intern, logout

# Ensure endpoints are exempt from CSRF during test suite execution
CSRF_EXEMPT_ENDPOINTS.update(["api_intern_profile_update", "api_account_change_password"])


def _setup_test_intern(client, db_path, stage=2, domain="Full Stack Web Development",
                        batch_end_date=None, email="test_phase5_intern@test.com",
                        password="InitialPassword123!", name="Test Phase5 Intern"):
    """Helper to seed an intern with exact stage, domain, and optional offer letter."""
    intern_id = seed_intern(db_path, email=email, password=password, name=name, status="Accepted")
    with get_db() as conn:
        conn.execute(
            "UPDATE intern_accounts SET signup_stage = ?, domain = ?, phone = '9876543210', college = 'Test College' WHERE email = ?",
            (stage, domain, email)
        )
        conn.execute(
            "UPDATE applications SET domain = ? WHERE email = ?",
            (domain, email)
        )
        if batch_end_date:
            conn.execute("""
                INSERT OR REPLACE INTO intern_offer_letters (
                    offer_letter_id, intern_id, email, name, domain, college,
                    batch_start_date, batch_end_date, tenure_months, stipend_amount,
                    caution_deposit_amount, caution_deposit_status, pdf_unlocked
                ) VALUES (?, ?, ?, ?, ?, 'Test College', '2026-09-01', ?, 2, 5000, 499, 'VERIFIED', 1)
            """, (f"OFR-PH5-{intern_id}", intern_id, email, name, domain, str(batch_end_date)))
        conn.commit()

    login_as_intern(client, db_path, email=email, password=password, name=name)
    return intern_id, email


# ============================================================================
# 1. Authentication & Unauthorized Access (HTTP 401)
# ============================================================================

def test_profile_update_unauthorized_returns_401(app_client):
    """Unauthenticated visitor calling /api/intern/profile/update returns HTTP 401."""
    client, _ = app_client
    resp = client.post("/api/intern/profile/update", json={"domain": "Data Analyst"})
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Unauthorized"


def test_change_password_unauthorized_returns_401(app_client):
    """Unauthenticated visitor calling /api/account/change-password returns HTTP 401."""
    client, _ = app_client
    resp = client.post("/api/account/change-password", json={"current_password": "Old", "new_password": "New"})
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Unauthorized"


# ============================================================================
# 2. Pre-Enrollment Domain Track Switching (Stage < 5)
# ============================================================================

def test_stage2_intern_domain_update_success(app_client):
    """Stage 2 intern successfully updates domain track; updates intern_accounts and applications."""
    client, db_path = app_client
    _, email = _setup_test_intern(client, db_path, stage=2, domain="Full Stack Web Development", email="stage2_dom@test.com")

    resp = client.post("/api/intern/profile/update", json={"domain": "AI Agent Development"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

    with get_db() as conn:
        acct = conn.execute("SELECT domain FROM intern_accounts WHERE email=?", (email,)).fetchone()
        assert acct["domain"] == "AI Agent Development"
        app_row = conn.execute("SELECT domain FROM applications WHERE email=? ORDER BY id DESC LIMIT 1", (email,)).fetchone()
        assert app_row["domain"] == "AI Agent Development"


def test_stage1_intern_domain_update_success(app_client):
    """Stage 1 intern successfully updates domain track."""
    client, db_path = app_client
    _, email = _setup_test_intern(client, db_path, stage=1, domain="Data Analyst", email="stage1_dom@test.com")

    resp = client.post("/api/intern/profile/update", json={"domain": "Python Automation"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

    with get_db() as conn:
        acct = conn.execute("SELECT domain FROM intern_accounts WHERE email=?", (email,)).fetchone()
        assert acct["domain"] == "Python Automation"


def test_stage3_intern_domain_update_syncs_offer_letter(app_client):
    """Stage 3 intern updating domain updates intern_accounts, applications, AND intern_offer_letters."""
    client, db_path = app_client
    _, email = _setup_test_intern(
        client, db_path, stage=3, domain="Full Stack Web Development",
        batch_end_date="2027-01-15", email="stage3_dom@test.com"
    )

    resp = client.post("/api/intern/profile/update", json={"domain": "Cybersecurity"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

    with get_db() as conn:
        acct = conn.execute("SELECT domain FROM intern_accounts WHERE email=?", (email,)).fetchone()
        assert acct["domain"] == "Cybersecurity"
        app_row = conn.execute("SELECT domain FROM applications WHERE email=? ORDER BY id DESC LIMIT 1", (email,)).fetchone()
        assert app_row["domain"] == "Cybersecurity"
        offer = conn.execute("SELECT domain FROM intern_offer_letters WHERE email=?", (email,)).fetchone()
        assert offer["domain"] == "Cybersecurity"


# ============================================================================
# 3. Active Cohort Domain Lock & Grace Period (Stage >= 5)
# ============================================================================

def test_stage5_active_intern_domain_locked_returns_403(app_client):
    """Active Stage 5 intern (batch_end in future) changing domain is locked (HTTP 403)."""
    client, db_path = app_client
    future_end = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    _, email = _setup_test_intern(
        client, db_path, stage=5, domain="Full Stack Web Development",
        batch_end_date=future_end, email="stage5_lock@test.com"
    )

    resp = client.post("/api/intern/profile/update", json={"domain": "AI Agent Development"})
    assert resp.status_code == 403
    assert resp.get_json()["error"] == "Track is locked during active cohort tenure."

    # Verify domain remains UNCHANGED
    with get_db() as conn:
        acct = conn.execute("SELECT domain FROM intern_accounts WHERE email=?", (email,)).fetchone()
        assert acct["domain"] == "Full Stack Web Development"


def test_stage5_grace_period_domain_locked_returns_403(app_client):
    """Stage 5 intern within 5-day grace period after batch_end is still locked (HTTP 403)."""
    client, db_path = app_client
    # Ended 2 days ago: today <= batch_end + 5 days
    ended_recently = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    _, email = _setup_test_intern(
        client, db_path, stage=5, domain="Full Stack Web Development",
        batch_end_date=ended_recently, email="stage5_grace@test.com"
    )

    resp = client.post("/api/intern/profile/update", json={"domain": "AI Agent Development"})
    assert resp.status_code == 403
    assert resp.get_json()["error"] == "Track is locked during active cohort tenure."


def test_stage5_active_intern_same_domain_allowed(app_client):
    """Active Stage 5 intern submitting same domain is permitted (HTTP 200)."""
    client, db_path = app_client
    future_end = (datetime.date.today() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    _, email = _setup_test_intern(
        client, db_path, stage=5, domain="Full Stack Web Development",
        batch_end_date=future_end, email="stage5_same@test.com"
    )

    resp = client.post("/api/intern/profile/update", json={"domain": "Full Stack Web Development", "phone": "9998887776"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


# ============================================================================
# 4. Expired Cohort Tenure Domain Switching (Stage >= 5, > 5 Days Post End)
# ============================================================================

def test_stage5_expired_tenure_domain_update_success(app_client):
    """Stage 5 intern with expired tenure (today > batch_end + 5 days) successfully changes domain."""
    client, db_path = app_client
    # Ended 10 days ago: today > batch_end + 5 days
    expired_end = (datetime.date.today() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
    _, email = _setup_test_intern(
        client, db_path, stage=5, domain="Full Stack Web Development",
        batch_end_date=expired_end, email="stage5_exp@test.com"
    )

    resp = client.post("/api/intern/profile/update", json={"domain": "DevOps & Cloud"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

    with get_db() as conn:
        acct = conn.execute("SELECT domain FROM intern_accounts WHERE email=?", (email,)).fetchone()
        assert acct["domain"] == "DevOps & Cloud"


def test_stage5_expired_tenure_human_date_format_success(app_client):
    """Stage 5 intern with human date format '%d %b %Y' successfully parses and changes domain."""
    client, db_path = app_client
    human_date = (datetime.date.today() - datetime.timedelta(days=15)).strftime("%d %b %Y")
    _, email = _setup_test_intern(
        client, db_path, stage=5, domain="Full Stack Web Development",
        batch_end_date=human_date, email="stage5_human_date@test.com"
    )

    resp = client.post("/api/intern/profile/update", json={"domain": "Mobile App Development"})
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

    with get_db() as conn:
        acct = conn.execute("SELECT domain FROM intern_accounts WHERE email=?", (email,)).fetchone()
        assert acct["domain"] == "Mobile App Development"


# ============================================================================
# 5. Non-Domain Profile Fields Update
# ============================================================================

def test_profile_update_name_phone_college_success(app_client):
    """Updating standard profile fields (name, phone, college) updates intern_accounts."""
    client, db_path = app_client
    _, email = _setup_test_intern(client, db_path, stage=2, email="profile_fields@test.com")

    payload = {
        "name": "Jane Developer",
        "phone": "9123456789",
        "college": "National Institute of Technology"
    }
    resp = client.post("/api/intern/profile/update", json=payload)
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

    with get_db() as conn:
        acct = conn.execute("SELECT name, phone, college FROM intern_accounts WHERE email=?", (email,)).fetchone()
        assert acct["name"] == "Jane Developer"
        assert acct["phone"] == "9123456789"
        assert acct["college"] == "National Institute of Technology"


# ============================================================================
# 6. Password Change Validation (HTTP 400)
# ============================================================================

def test_change_password_short_password_returns_400(app_client):
    """New password shorter than 8 characters returns HTTP 400."""
    client, db_path = app_client
    _setup_test_intern(client, db_path, password="InitialPassword123!", email="pw_short@test.com")

    resp = client.post("/api/account/change-password", json={
        "current_password": "InitialPassword123!",
        "new_password": "short"
    })
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Password must be at least 8 characters."


def test_change_password_invalid_current_returns_400(app_client):
    """Incorrect current password returns HTTP 400."""
    client, db_path = app_client
    _setup_test_intern(client, db_path, password="InitialPassword123!", email="pw_invalid@test.com")

    resp = client.post("/api/account/change-password", json={
        "current_password": "IncorrectPassword999!",
        "new_password": "BrandNewPassword123!"
    })
    assert resp.status_code == 400
    assert resp.get_json()["error"] == "Current password is incorrect."


# ============================================================================
# 7. Valid Password Change & Subsequent Login Flow
# ============================================================================

def test_change_password_success_and_subsequent_login(app_client):
    """Valid password change stores bcrypt hash and allows immediate login with new credentials."""
    client, db_path = app_client
    _, email = _setup_test_intern(client, db_path, password="InitialPassword123!", email="pw_valid@test.com")

    new_password = "BrandNewSuperSecurePass456!"
    resp = client.post("/api/account/change-password", json={
        "current_password": "InitialPassword123!",
        "new_password": new_password
    })
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}

    # Verify password_hash in DB is a valid bcrypt hash
    with get_db() as conn:
        acct = conn.execute("SELECT password_hash, password_set FROM intern_accounts WHERE email=?", (email,)).fetchone()
        stored_hash = acct["password_hash"]
        assert stored_hash.startswith("$2"), f"Stored hash does not look like bcrypt: {stored_hash}"
        assert acct["password_set"] == 1
        assert bcrypt.checkpw(new_password.encode("utf-8"), stored_hash.encode("utf-8"))

    # Log out existing session
    logout(client)

    # Attempt login with OLD password -> MUST fail (HTTP 401)
    resp_old = client.post("/intern/login", json={"email": email, "password": "InitialPassword123!"})
    assert resp_old.status_code == 401

    # Attempt login with NEW password -> MUST succeed (HTTP 200)
    resp_new = client.post("/intern/login", json={"email": email, "password": new_password})
    assert resp_new.status_code == 200
    assert resp_new.get_json()["status"] == "success"


# ============================================================================
# 8. /intern/me Tenure Expiration Payload Verification
# ============================================================================

def test_intern_me_returns_is_tenure_expired(app_client):
    """Verify GET /intern/me returns is_tenure_expired flag in intern dictionary."""
    client, db_path = app_client
    _setup_test_intern(client, db_path, stage=5, email="intern_me_tenure@test.com")

    resp = client.get("/intern/me")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "intern" in data
    assert "is_tenure_expired" in data["intern"]
    assert isinstance(data["intern"]["is_tenure_expired"], bool)


# ============================================================================
# 9. Profile UI Template Structure Verification
# ============================================================================

def test_portal_template_phase5_ui_elements():
    """Verify portal.html contains Phase 5 elements: domain select, lock badge, hint, password card."""
    portal_html_path = PORTAL_DIR / "templates" / "portal.html"
    assert portal_html_path.exists(), "portal.html does not exist"
    content = portal_html_path.read_text(encoding="utf-8")

    assert 'id="ep_domain"' in content
    assert 'id="domainLockBadge"' in content
    assert 'id="domainHint"' in content
    assert 'id="pw_current"' in content
    assert 'id="pw_new"' in content
    assert 'id="pw_confirm"' in content
    assert "submitPasswordChange" in content
    assert "populateProfileData" in content
