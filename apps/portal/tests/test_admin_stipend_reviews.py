"""
Tests for /admin/stipend-reviews and /admin/stipend-reviews/comment:
1. Unauthenticated requests are rejected (302 / 401).
2. Admin can load /admin/stipend-reviews (JSON & HTML) and see Gate 1 + PR submitters.
3. Admin can save stipend_5000_status, release_date, comment, and visible_to_intern.
4. Intern /portal displays the comment when visible_to_intern=1 and hides it when visible_to_intern=0.
"""

import sys
import sqlite3
from datetime import datetime
from pathlib import Path

PORTAL_DIR = Path(__file__).resolve().parent.parent
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

import app as portal_app
from werkzeug.security import generate_password_hash


def _seed_stipend_intern(db_path):
    conn = sqlite3.connect(db_path)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pw = generate_password_hash("TestPass123!")
    conn.execute(
        "INSERT INTO applications (id, name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at, updated_at) "
        "VALUES (101, 'Stipend Tester', 'stipend.tester@example.com', '+91 98765 11111', 'Bengaluru', 'IIT', 'B.Tech', '6th Semester', '2026', 'AI Agent Development', 'Build', 'Accepted', ?, ?)",
        (now_str, now_str),
    )
    conn.execute(
        "INSERT INTO intern_accounts (id, application_id, name, email, phone, domain, password_hash, password_set, is_active, signup_stage, email_verified, stipend_verified, stipend_amount, linkedin_url, linkedin_verified, created_at, updated_at) "
        "VALUES (101, 101, 'Stipend Tester', 'stipend.tester@example.com', '+91 98765 11111', 'AI Agent Development', ?, 1, 1, 5, 1, 1, 5499, 'https://www.linkedin.com/in/stipend-tester', 1, ?, ?)",
        (pw, now_str, now_str),
    )
    conn.execute(
        "INSERT INTO task_submissions (intern_id, task_id, task_version_id, submission_content, status, github_repo_url, created_at) "
        "VALUES (101, 1, 1, 'PR merged and verified', 'approved', 'https://github.com/Alkameinc/alkame-nifty-50-educational/pull/99', ?)",
        (now_str,),
    )
    conn.commit()
    conn.close()


def test_unauthenticated_blocked(app_client):
    client, db_path = app_client
    _seed_stipend_intern(db_path)
    res_get = client.get("/admin/stipend-reviews")
    assert res_get.status_code in (301, 302)
    assert "/admin/login" in res_get.location

    portal_app.CSRF_EXEMPT_ENDPOINTS.add("admin_stipend_reviews_comment")
    res_post = client.post("/admin/stipend-reviews/comment", json={"intern_id": 101, "comment": "Hi"})
    assert res_post.status_code == 401


def test_admin_save_comment_and_portal_visibility(app_client, monkeypatch):
    client, db_path = app_client
    _seed_stipend_intern(db_path)
    monkeypatch.setattr(portal_app, "require_admin", lambda: {"id": 1, "username": "admin", "role": "admin"})
    portal_app.CSRF_EXEMPT_ENDPOINTS.add("admin_stipend_reviews_comment")

    res_json = client.get("/admin/stipend-reviews?format=json")
    assert res_json.status_code == 200
    payload = res_json.get_json()
    assert payload["count"] == 1
    cand = payload["candidates"][0]
    assert cand["has_dbert_pr"] is True
    assert cand["has_linkedin"] is True

    res_html = client.get("/admin/stipend-reviews")
    assert res_html.status_code == 200
    assert b"Stipend Tester" in res_html.data

    res_save = client.post(
        "/admin/stipend-reviews/comment",
        json={
            "intern_id": 101,
            "release_date": "2026-12-03",
            "stipend_5000_status": "Approved",
            "comment": "Merged PR verified and LinkedIn cert confirmed.",
            "visible_to_intern": 1,
        },
    )
    assert res_save.status_code == 200
    saved = res_save.get_json()
    assert saved["stipend_5000_status"] == "Approved"

    token = portal_app.create_session("stipend.tester@example.com", "intern")
    client.set_cookie(portal_app.AUTH_COOKIE, token)

    portal_res = client.get("/portal")
    assert portal_res.status_code == 200
    assert b"Merged PR verified and LinkedIn cert confirmed." in portal_res.data
    assert b"2026-12-03" in portal_res.data

    res_hide = client.post(
        "/admin/stipend-reviews/comment",
        json={
            "intern_id": 101,
            "release_date": "2026-12-03",
            "stipend_5000_status": "Approved",
            "comment": "Internal note only",
            "visible_to_intern": 0,
        },
    )
    assert res_hide.status_code == 200
    portal_res_hidden = client.get("/portal")
    assert portal_res_hidden.status_code == 200
    assert b"Internal note only" not in portal_res_hidden.data
