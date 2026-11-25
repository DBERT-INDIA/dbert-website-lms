import json
import os
import sys
import tempfile

import pytest

PORTAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test_inst.db")
    monkeypatch.setenv("DB_PATH", db_file)
    monkeypatch.setenv("DATABASE_URL", "")
    import app as portal_app
    monkeypatch.setattr(portal_app, "DB_PATH", db_file, raising=False)
    portal_app.CSRF_EXEMPT_ENDPOINTS.update(["signup_stage2", "api_admin_institutions_resolve"])
    portal_app.init_db()
    with portal_app.get_db() as conn:
        conn.execute("DELETE FROM intern_accounts WHERE email='insttest@example.com'")
        conn.execute("DELETE FROM applications WHERE email='insttest@example.com'")
        conn.execute("DELETE FROM institutions WHERE name IN ('Vellore Institute of Technology', 'New Local Tech College', 'VIT Vellore Typo')")
        conn.execute(
            """INSERT INTO institutions (name, aliases, affiliated_university, city, state, aishe_code, source, is_verified, created_at)
               VALUES ('Vellore Institute of Technology', '["VIT"]', 'Vellore Institute of Technology', 'Vellore', 'Tamil Nadu', 'U-0490', 'aishe', TRUE, '2026-11-25')"""
        )
        conn.execute(
            """INSERT INTO intern_accounts (name, email, phone, signup_stage, is_active, created_at, updated_at)
               VALUES ('Test Intern', 'insttest@example.com', '9999999999', 1, 1, '2026-11-25', '2026-11-25')"""
        )
        conn.execute(
            """INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at, updated_at)
               VALUES ('Test Intern', 'insttest@example.com', '9999999999', '', '', '', '', '', '', '', 'Apply Pending', '2026-11-25', '2026-11-25')"""
        )
        conn.commit()
    portal_app.app.config["TESTING"] = True
    with portal_app.app.test_client() as c:
        yield c, portal_app


def test_institution_search_by_name_and_acronym(client):
    c, _ = client
    r1 = c.get("/api/institutions/search?q=Vellore")
    assert r1.status_code == 200
    d1 = r1.get_json()
    assert d1["status"] == "success"
    assert any(x["name"] == "Vellore Institute of Technology" for x in d1["institutions"])

    r2 = c.get("/api/institutions/search?q=VIT")
    assert r2.status_code == 200
    d2 = r2.get_json()
    assert any(x["name"] == "Vellore Institute of Technology" for x in d2["institutions"])


def test_signup_stage2_authoritative_institution_and_other_queue(client, monkeypatch):
    c, portal_app = client
    monkeypatch.setattr(portal_app, "require_role", lambda role: {"email": "insttest@example.com", "role": "intern"} if role == "intern" else None)

    # Reject junk college
    bad = c.post("/signup/stage2", json={
        "city": "Chennai", "college": "Pending Profile", "course": "B.Tech",
        "semester": "6th Semester", "year_of_passing": "2027"
    })
    assert bad.status_code == 400

    # Valid master institution_id overrides client-supplied college/city
    inst_id = c.get("/api/institutions/search?q=VIT").get_json()["institutions"][0]["id"]
    ok = c.post("/signup/stage2", json={
        "institution_id": inst_id, "city": "WrongCity", "college": "WrongName",
        "course": "B.Tech", "semester": "6th Semester", "year_of_passing": "2027"
    })
    assert ok.status_code == 200

    with portal_app.get_db() as conn:
        ia = conn.execute("SELECT college, affiliated_university, city, institution_id FROM intern_accounts WHERE email='insttest@example.com'").fetchone()
        assert ia["college"] == "Vellore Institute of Technology"
        assert ia["affiliated_university"] == "Vellore Institute of Technology"
        assert ia["city"] == "Vellore"
        assert ia["institution_id"] == inst_id

    # Custom "Other" institution queues as unverified
    other = c.post("/signup/stage2", json={
        "is_other_institution": True, "college": "New Local Tech College",
        "affiliated_university": "Anna University", "city": "Coimbatore",
        "course": "B.Tech", "semester": "6th Semester", "year_of_passing": "2027"
    })
    assert other.status_code == 200
    with portal_app.get_db() as conn:
        pending = conn.execute("SELECT id, is_verified, source FROM institutions WHERE name='New Local Tech College'").fetchone()
        assert pending is not None
        assert not bool(pending["is_verified"])
        assert pending["source"] == "user_submitted"


def test_admin_pending_and_merge(client, monkeypatch):
    c, portal_app = client
    with portal_app.get_db() as conn:
        canon_id = conn.execute("SELECT id FROM institutions WHERE name='Vellore Institute of Technology'").fetchone()["id"]
        conn.execute(
            """INSERT INTO institutions (name, aliases, affiliated_university, city, source, is_verified, created_at)
               VALUES ('VIT Vellore Typo', '[]', '', 'Vellore', 'user_submitted', FALSE, '2026-11-25')"""
        )
        typo_id = conn.execute("SELECT id FROM institutions WHERE name='VIT Vellore Typo'").fetchone()["id"]
        conn.execute("UPDATE intern_accounts SET institution_id=?, college='VIT Vellore Typo' WHERE email='insttest@example.com'", (typo_id,))
        conn.commit()

    monkeypatch.setattr(portal_app, "require_role", lambda role: {"email": "admin@dbert.in", "role": "admin"} if role == "admin" else None)
    pend = c.get("/api/admin/institutions/pending")
    assert pend.status_code == 200
    assert any(p["id"] == typo_id for p in pend.get_json()["pending"])

    merged = c.post("/api/admin/institutions/resolve", json={"id": typo_id, "action": "merge", "target_id": canon_id})
    assert merged.status_code == 200
    with portal_app.get_db() as conn:
        ia = conn.execute("SELECT institution_id, college FROM intern_accounts WHERE email='insttest@example.com'").fetchone()
        assert ia["institution_id"] == canon_id
        assert ia["college"] == "Vellore Institute of Technology"
        gone = conn.execute("SELECT id FROM institutions WHERE id=?", (typo_id,)).fetchone()
        assert gone is None
