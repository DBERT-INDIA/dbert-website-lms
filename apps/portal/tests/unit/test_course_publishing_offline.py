import sqlite3
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from flask import Flask, request

from services.course_publishing import course_publishing_blueprint, init_course_publishing


def test_author_drafts_admin_publishes_and_rolls_back(tmp_path):
    path = tmp_path / "publishing.db"

    @contextmanager
    def db():
        conn = sqlite3.connect(path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    with db() as conn:
        conn.executescript("""
            CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, company_id INTEGER, content_status TEXT);
            CREATE TABLE course_chapters (id INTEGER PRIMARY KEY, course_id INTEGER, day_number INTEGER);
            CREATE TABLE course_subtopics (id INTEGER PRIMARY KEY, chapter_id INTEGER, title TEXT, brief TEXT, sort_order INTEGER);
            INSERT INTO courses VALUES (1, 'Original course', 7, 'approved');
            INSERT INTO course_chapters VALUES (1, 1, 1);
            INSERT INTO course_subtopics VALUES (1, 1, 'Original lesson', 'Original brief.', 1);
        """)
        init_course_publishing(conn)

    templates = Path(__file__).resolve().parents[2] / "templates"
    app = Flask(__name__, template_folder=str(templates))
    app.config["TESTING"] = True
    app.jinja_env.globals.update(csp_nonce=lambda: "test", csrf_token=lambda: "test", csrf_field=lambda: "")

    def company():
        company_id = request.headers.get("X-Synthetic-Company")
        return {"id": int(company_id)} if company_id else None

    app.register_blueprint(course_publishing_blueprint(
        db, company, lambda: {"id": 1} if request.headers.get("X-Synthetic-Admin") else None,
        lambda: "2026-11-23 10:00:00",
    ))
    client = app.test_client()
    endpoint = "/course-publishing/1"
    author = {"X-Synthetic-Company": "7"}
    admin = {"X-Synthetic-Admin": "1"}
    assert client.get(endpoint).status_code == 403
    assert client.get(endpoint, headers={"X-Synthetic-Company": "8"}).status_code == 404
    form = {"action": "draft", "title": "Revised course", "title_1": "Revised lesson", "brief_1": "Updated material."}
    assert client.post(endpoint, headers=author, data={**form, "brief_1": ""}).status_code == 422
    saved = client.post(endpoint, headers=author, data=form)
    assert saved.status_code == 302
    edition_id = parse_qs(urlsplit(saved.headers["Location"]).query)["edition_id"][0]
    assert b"Updated material." in client.get(saved.headers["Location"], headers=author).data
    with db() as conn:
        assert conn.execute("SELECT title FROM courses").fetchone()[0] == "Original course"
    publish = {"action": "publish", "edition_id": edition_id}
    assert client.post(endpoint, headers=author, data=publish).status_code == 403
    assert client.post(endpoint, headers=admin, data=publish).status_code == 302
    with db() as conn:
        assert conn.execute("SELECT title, brief FROM course_subtopics").fetchone()["brief"] == "Updated material."
        baseline = conn.execute("SELECT id FROM course_editions WHERE author='baseline'").fetchone()["id"]
    assert client.post(endpoint, headers=admin, data={"action": "publish", "edition_id": baseline}).status_code == 302
    with db() as conn:
        assert conn.execute("SELECT title FROM courses").fetchone()[0] == "Original course"
        assert conn.execute("SELECT COUNT(*) FROM course_publication_history").fetchone()[0] == 2
