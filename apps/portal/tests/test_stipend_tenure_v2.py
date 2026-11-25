"""Tests for /stipend/tasks V2 compliance (Invariants 7, 8 & 9)."""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from tests.conftest import seed_intern, login_as_intern


def test_stipend_template_has_no_legacy_299_or_verify_unlock():
    tpl_path = Path(__file__).resolve().parents[1] / "templates" / "stipend_tasks.html"
    content = tpl_path.read_text(encoding="utf-8")
    assert "/verify/unlock" not in content
    assert "₹299" not in content


def test_stipend_tasks_unverified_shows_not_yet_issued_not_raw_not_found(app_client):
    from datetime import date, timedelta
    client, db_path = app_client
    email = "unverified_v2@dbert.test"
    intern_id = seed_intern(db_path, email=email)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE intern_accounts SET signup_stage = 5, domain = 'Full Stack Development' WHERE id = ?",
            (intern_id,),
        )
        conn.commit()
    login_as_intern(client, db_path, email=email)

    resp = client.get("/stipend/tasks", follow_redirects=True)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Not Yet Issued" in html
    assert ">NOT_FOUND<" not in html
    assert "/verify/unlock" not in html


def test_stipend_tasks_expired_tenure_locks_submission_and_rejects_post(app_client):
    from datetime import date, timedelta
    client, db_path = app_client
    email = "expired_v2@dbert.test"
    intern_id = seed_intern(db_path, email=email)

    joined_80d_ago = (datetime.now() - timedelta(days=80)).strftime("%Y-%m-%d")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE intern_accounts SET signup_stage = 5, domain = 'Data Analyst', upi_id_encrypted = 'enc_upi_test' WHERE id = ?",
            (intern_id,),
        )
        conn.execute(
            """
            INSERT INTO enrollments (
                application_id, timestamp, name, email, domain, joining_date,
                payment_status, product, amount, created_at, updated_at
            ) VALUES (?, ?, 'Expired V2', ?, 'Data Analyst', ?, 'Verified', 'free_deposit', 499, ?, ?)
            """,
            (intern_id, joined_80d_ago, email, joined_80d_ago, joined_80d_ago, joined_80d_ago),
        )
        conn.execute(
            """
            INSERT INTO intern_certificates (
                intern_id, course_id, course_title, cert_id, issued_at, url, tier, email
            ) VALUES (?, 1, 'Data Analyst Fellowship', 'CERT-DBERT-2026-DA-8881', ?, 'https://dbert.in/verify/CERT-DBERT-2026-DA-8881', 'Executive Gold', ?)
            """,
            (intern_id, joined_80d_ago, email),
        )
        conn.commit()

    login_as_intern(client, db_path, email=email)

    resp = client.get("/stipend/tasks", follow_redirects=True)
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "Tenure Expired" in html
    assert "Tenure Expired for Previous Internship Program" in html
    assert "Join New Cohort" in html
    assert "Cohort Tenure Expired" in html
    # Stage 5B must NOT show the 5,000-coin bounty hero, progress bar, or 4-gate checklist
    assert "STIPEND PROGRESSION STATUS" not in html
    assert "Step 1: Course Certificate" not in html
    assert "Step 3: Payout UPI Account" not in html
    assert "Step 4: Public LinkedIn Experience" not in html
    assert "Milestone Bounty" not in html

    import re
    m = re.search(r'name="csrf-token"\s+content="([^"]+)"', html) or re.search(r'csrf_token["\']?\s*[:=]\s*["\']([^"\']+)["\']', html)
    headers = {"X-CSRF-Token": m.group(1)} if m else {}

    post_resp = client.post(
        "/stipend/tasks/9901/submit",
        json={"github_url": "https://github.com/dbert/repo"},
        headers=headers,
    )
    assert post_resp.status_code == 403
    assert "ended on" in post_resp.get_json()["message"]


def test_stage5b_tenure_expired_locks_internship_and_keeps_exit_surfaces_active(app_client):
    """
    Stage 5B Exit/Completion Rules:
    - /tasks, /mentors/slots, /portal/offer, /portal/offer/print redirect to /portal
    - /portal/offer/sign returns 403 JSON
    - /certificates, /profile, /jobs, /ambassador, /account/coins remain 200
    - /stipend/tasks and /portal link "Join New Cohort" to /enroll/1999?rejoin=1&...
    """
    from datetime import date, timedelta
    client, db_path = app_client
    email = "expired_v2@dbert.test"
    joined_80d_ago = (date.today() - timedelta(days=80)).strftime("%Y-%m-%d")

    login_as_intern(client, db_path, email=email)

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        conn.execute(
            """
            UPDATE intern_accounts
            SET name = 'Expired Exit V2', phone = '9876543210', college = 'IIT Test',
                domain = 'Data Analyst', signup_stage = 5
            WHERE LOWER(email) = LOWER(?)
            """,
            (email,),
        )
        intern_id = conn.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = LOWER(?)", (email,)).fetchone()["id"]
        conn.execute(
            """
            INSERT INTO enrollments (
                application_id, timestamp, name, email, domain, joining_date,
                payment_status, product, amount, created_at, updated_at
            ) VALUES (?, ?, 'Expired Exit V2', ?, 'Data Analyst', ?, 'Accepted', 'free_deposit', 499, ?, ?)
            """,
            (intern_id, joined_80d_ago, email, joined_80d_ago, joined_80d_ago, joined_80d_ago),
        )
        conn.execute(
            """
            INSERT INTO intern_certificates (
                intern_id, course_id, course_title, cert_id, issued_at, url, tier, email
            ) VALUES (?, 1, 'Data Analyst Fellowship', 'CERT-DBERT-2026-DA-8882', ?, 'https://dbert.in/verify/CERT-DBERT-2026-DA-8882', 'verified', ?)
            """,
            (intern_id, joined_80d_ago, email),
        )
        conn.commit()

    # 1. Locked internship routes redirect to /portal (or 403 JSON)
    for locked_route in ["/tasks", "/mentors/slots", "/portal/offer", "/portal/offer/print"]:
        r = client.get(locked_route, follow_redirects=False)
        assert r.status_code == 302, f"{locked_route} should redirect when tenure expired, got {r.status_code}"
        assert "/portal" in (r.headers.get("Location") or "")

    r_sign = client.post("/portal/offer/sign", json={"signature_name": "Test", "agreed": True})
    assert r_sign.status_code == 403

    # 2. Active post-internship routes stay 200
    for open_route in ["/portal", "/certificates", "/profile", "/jobs", "/ambassador", "/account/coins"]:
        r = client.get(open_route, follow_redirects=True)
        assert r.status_code == 200, f"{open_route} should stay 200 for Stage 5B, got {r.status_code}"

    # 3. Verify prefilled /enroll/1999?rejoin=1 CTA on /stipend/tasks and /portal
    stipend_html = client.get("/stipend/tasks").get_data(as_text=True)
    assert "/enroll/1999?" in stipend_html
    assert "rejoin=1" in stipend_html
    assert "expired_v2%40dbert.test" in stipend_html

    portal_html = client.get("/portal").get_data(as_text=True)
    assert "ovTenureExpired" in portal_html
    assert "rejoin=1" in portal_html
    assert "window._IS_TENURE_EXPIRED = true" in portal_html
