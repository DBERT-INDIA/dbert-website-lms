"""Exercise search visibility and support ownership with synthetic records."""

import ast
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import pytest
from flask import Flask, jsonify, redirect, render_template, request

from services.product_tools import init_support_tables, product_tools_blueprint


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "product-tools.db"

    @contextmanager
    def db():
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    with db() as conn:
        init_support_tables(conn)
        conn.executescript("""
            CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, domain TEXT, is_active INTEGER, company_id INTEGER);
            CREATE TABLE companies (id INTEGER PRIMARY KEY, is_active INTEGER, is_approved INTEGER);
            CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, post_type TEXT, domain TEXT,
                                status TEXT, expires_at TEXT, company_id INTEGER);
            CREATE TABLE user_sessions (id INTEGER PRIMARY KEY, email TEXT, role TEXT,
                                        session_token TEXT, created_at TEXT, expires_at TEXT);
            CREATE TABLE event_outbox (status TEXT, created_at TEXT, payload_json TEXT);
            CREATE TABLE intern_accounts (id INTEGER PRIMARY KEY, email TEXT, name TEXT, domain TEXT, created_at TEXT);
            CREATE TABLE applications (email TEXT, name TEXT, domain TEXT);
            CREATE TABLE course_enrollments (id INTEGER PRIMARY KEY, intern_id INTEGER, email TEXT);
            CREATE TABLE day_quiz_attempts (enrollment_id INTEGER);
            CREATE TABLE course_subtopic_chats (enrollment_id INTEGER, role TEXT);
            CREATE TABLE device_profiles (visitor_id TEXT, created_at TEXT);
            CREATE TABLE intern_certificates (id INTEGER PRIMARY KEY, intern_id INTEGER, email TEXT, cert_id TEXT,
                course_title TEXT, issued_at TEXT, credential_status TEXT, replaced_by_cert_id TEXT);
            CREATE TABLE credential_status_history (credential_id INTEGER, actor_id TEXT, status TEXT, replacement_id TEXT,
                                                     reason TEXT, created_at TEXT);
            CREATE TABLE application_status_history (id INTEGER PRIMARY KEY, application_id INTEGER, changed_by TEXT,
                new_status TEXT, reason TEXT, changed_at TEXT, metadata TEXT);
            INSERT INTO application_status_history VALUES (1, 42, 'reviewer', 'Selected', 'Review complete', '2026-11-08', 'private debug payload');
            INSERT INTO intern_accounts VALUES
                (1, 'first@example.test', 'Sample One', 'Python', '2026-11-05'),
                (2, 'second@example.test', 'Sample Two', 'Python', '2026-11-06');
            INSERT INTO applications VALUES ('first@example.test', 'Sample One', 'Python');
            INSERT INTO course_enrollments VALUES (1, 1, 'first@example.test');
            INSERT INTO day_quiz_attempts VALUES (1);
            INSERT INTO device_profiles VALUES ('test-browser', '2026-11-05'), ('test-browser', '2026-11-06');
            INSERT INTO intern_certificates VALUES
                (1, 1, 'first@example.test', 'SAMPLE-OLD', 'Python Foundations', '2026-11-07', 'valid', NULL),
                (2, 1, 'first@example.test', 'SAMPLE-NEW', 'Python Foundations', '2026-11-08', 'valid', NULL),
                (3, 2, 'second@example.test', 'SAMPLE-OTHER', 'Independent credential', '2026-11-09', 'valid', NULL);
            INSERT INTO user_sessions VALUES
                (1, 'first@example.test', 'intern', 'synthetic-current', '2026-11-01', '2027-01-01'),
                (2, 'first@example.test', 'intern', 'synthetic-other', '2026-11-02', '2027-01-01'),
                (3, 'second@example.test', 'intern', 'synthetic-unrelated', '2026-11-03', '2027-01-01'),
                (4, 'first@example.test', 'staff', 'synthetic-staff', '2026-11-04', '2027-01-01');
            INSERT INTO event_outbox VALUES ('PENDING', '2026-11-09', 'synthetic-private-payload');
            INSERT INTO courses VALUES (1, 'Python Basics', 'Python', 1, NULL),
                                       (2, 'Python Inactive', 'Python', 0, NULL),
                                       (3, 'Python Partner', 'Python', 1, 1);
            INSERT INTO companies VALUES (1, 1, 1), (2, 1, 0);
            INSERT INTO posts VALUES (10, 'Python Internship', 'internship', 'Python', 'published', NULL, 1),
                                     (11, 'Python Draft', 'job', 'Python', 'draft', NULL, 1),
                                     (12, 'Python Expired', 'job', 'Python', 'published', '2000-01-01', 1),
                                     (13, 'Python Unapproved', 'job', 'Python', 'published', NULL, 2);
        """)

    def intern():
        user_id = request.headers.get("X-Synthetic-Learner")
        return {"id": int(user_id)} if user_id else None

    def admin():
        return {"id": 1, "role": "admin"} if request.headers.get("X-Synthetic-Admin") else None

    def signed_in():
        identity = request.headers.get("X-Synthetic-Session")
        with db() as conn:
            return conn.execute("SELECT * FROM user_sessions WHERE id = ?", (identity,)).fetchone()

    def telemetry():
        return {
            "total_requests": 42, "rates": {"5xx_error_rate_pct": 1.5},
            "latencies": {"count": 2, "p95_ms": 36},
            "failures": {"email_failures": 2, "payment_failures": 0, "ai_failures": 0},
        }

    templates = Path(__file__).resolve().parents[2] / "templates"
    app = Flask(__name__, template_folder=str(templates))
    app.config.update(TESTING=True, SECRET_KEY="synthetic-flask-test")
    app.jinja_env.globals.update(csp_nonce=lambda: "test", csrf_token=lambda: "test", csrf_field=lambda: "")
    portal_handlers = ast.parse((templates.parent / "app.py").read_text(encoding="utf-8"))
    credential_handlers = [node for node in portal_handlers.body if isinstance(node, ast.FunctionDef) and node.name in {
        "portal_view_certificate", "portal_print_certificate", "api_verify_certificate",
    }]
    exec(compile(ast.Module(body=credential_handlers, type_ignores=[]), "credential-handlers", "exec"), {
        "app": app, "request": request, "get_db": db, "render_template": render_template,
        "redirect": redirect, "jsonify": jsonify, "row_to_dict": dict, "clean_text": lambda value: value.strip(),
    })
    app.register_blueprint(product_tools_blueprint(
        db, intern, admin,
        "status='published' AND (expires_at IS NULL OR expires_at > datetime('now','localtime')) "
        "AND EXISTS (SELECT 1 FROM companies c WHERE c.id=company_id AND c.is_approved=1 AND c.is_active=1)",
        signed_in, lambda: "2026-11-10", telemetry,
    ))
    return app.test_client()


def test_search_limits_public_results_to_visible_records(client):
    page = client.get("/search?q=python")
    assert page.status_code == 200
    assert b"Python Basics" in page.data and b"Python Internship" in page.data
    for hidden in (b"Python Inactive", b"Python Partner", b"Python Draft", b"Python Expired", b"Python Unapproved"):
        assert hidden not in page.data
    assert b"No results found" in client.get("/search", query_string={"q": "%%"}).data


def test_search_separates_learner_navigation_and_public_results(client):
    public = client.get("/search?q=mentor")
    private = client.get("/search?q=mentor", headers={"X-Synthetic-Learner": "1"})
    assert b"/mentors/slots" not in public.data
    assert b"/mentors/slots" in private.data
    assert "no-store" in private.headers["Cache-Control"]
    assert client.get("/help").status_code == 200


def test_support_submission_and_staff_update_preserve_ownership(client):
    learner = {"X-Synthetic-Learner": "1"}
    other = {"X-Synthetic-Learner": "2"}
    assert client.get("/support").status_code == 302
    assert client.post("/support", headers=learner, data={"subject": "bad"}).status_code == 422
    response = client.post("/support", headers=learner, data={
        "subject": "Classroom audio",
        "details": "The sample course audio stops in the classroom.",
        "source": "/courses/1/learn?unused=value#fragment",
    })
    assert response.status_code == 302
    owned = client.get("/support", headers=learner).data
    assert b"Classroom audio" in owned and b"/courses/1/learn" in owned
    assert b"unused=value" not in owned and b"Classroom audio" not in client.get("/support", headers=other).data
    assert client.get("/staff/support", headers=learner).status_code == 403
    assert client.post("/staff/support/1", headers=learner, data={"status": "resolved"}).status_code == 403

    staff = {"X-Synthetic-Admin": "1"}
    assert b"Classroom audio" in client.get("/staff/support", headers=staff).data
    update = client.post("/staff/support/1", headers=staff, data={
        "status": "reviewing", "note": "The support team is checking the sample lesson.",
    })
    assert update.status_code == 302
    updated = client.get("/support", headers=learner).data
    assert b"In review" in updated and b"checking the sample lesson" in updated


def test_availability_only_reports_open_roles(client):
    assert client.get("/saved-opportunities").status_code == 200
    availability = client.get("/api/opportunities/availability?ids=10,11,12,13")
    assert availability.status_code == 200 and availability.json == {"open_ids": [10]}
    assert client.get("/api/opportunities/availability?ids=invalid").status_code == 400


def test_security_center_revokes_only_other_sessions_for_current_identity(client):
    first = {"X-Synthetic-Session": "1"}
    assert client.get("/account/security").status_code == 302
    overview = client.get("/account/security", headers=first)
    assert b"Current session" in overview.data and b"2026-11-02" in overview.data
    assert b"2026-11-03" not in overview.data and b"synthetic-current" not in overview.data
    assert client.post("/account/security", headers=first, data={"session": "3"}).status_code == 302
    assert client.get("/account/security", headers={"X-Synthetic-Session": "3"}).status_code == 200
    assert client.post("/account/security", headers=first, data={"session": "others"}).status_code == 302
    assert client.get("/account/security", headers={"X-Synthetic-Session": "2"}).status_code == 302
    assert client.get("/account/security", headers={"X-Synthetic-Session": "4"}).status_code == 200
    assert client.get("/account/security", headers=first).status_code == 200


def test_platform_health_exposes_only_admin_aggregates(client):
    assert client.get("/admin/platform-health").status_code == 403
    authorized = client.get("/admin/platform-health", headers={"X-Synthetic-Admin": "1"})
    assert authorized.status_code == 200
    assert b"36 ms" in authorized.data and b"Pending" in authorized.data
    assert b"synthetic-private-payload" not in authorized.data


def test_funnel_is_aggregated_and_restricted(client):
    assert client.get("/admin/student-funnel").status_code == 403
    page = client.get("/admin/student-funnel?days=7", headers={"X-Synthetic-Admin": "1"})
    assert page.status_code == 200
    for needle in (b"<strong>Accounts created</strong> 2", b"<strong>Applied</strong> 1", b"<strong>Started learning</strong> 1",
                   b"1 distinct browser identifiers"):
        assert needle in page.data
    assert b"first@example.test" not in page.data


def test_credential_wallet_and_public_status(client):
    learner = {"X-Synthetic-Learner": "1"}
    owner = client.get("/account/credentials", headers=learner)
    assert owner.status_code == 200 and b"SAMPLE-OLD" in owner.data and b"SAMPLE-OTHER" not in owner.data
    update = {"cert_id": "SAMPLE-OLD", "status": "replaced", "replacement_id": "SAMPLE-OTHER", "reason": "Corrected certificate"}
    assert client.post("/admin/credential-status", headers=learner, data=update).status_code == 403
    staff = {"X-Synthetic-Admin": "1"}
    assert client.post("/admin/credential-status", headers=staff, data=update).status_code == 422
    assert client.get("/api/verify?certId=SAMPLE-OLD").json["verified"] is True
    update["replacement_id"] = "SAMPLE-NEW"
    assert client.post("/admin/credential-status", headers=staff, data=update).status_code == 302
    replaced = client.get("/api/verify?certId=SAMPLE-OLD")
    assert replaced.status_code == 410 and replaced.json == {
        "verified": False, "status": "replaced", "certId": "SAMPLE-OLD", "replacementId": "SAMPLE-NEW",
    }
    assert client.get("/portal/certificate/SAMPLE-OLD/print").status_code == 410
    assert b"Verify the replacement certificate" in client.get("/portal/certificate/SAMPLE-OLD").data


def test_action_history_exposes_reason_without_internal_snapshot(client):
    assert client.get("/admin/action-history?area=Applications").status_code == 403
    page = client.get("/admin/action-history?area=Applications", headers={"X-Synthetic-Admin": "1"})
    assert page.status_code == 200
    assert b"Record 42" in page.data and b"Review complete" in page.data
    assert b"private debug payload" not in page.data
