import ast
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, render_template, request


def test_project_revision_keeps_review_feedback_and_history(tmp_path):
    path = tmp_path / "projects.db"

    @contextmanager
    def db():
        connection = sqlite3.connect(path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        finally:
            connection.close()

    with db() as connection:
        connection.executescript("""
            CREATE TABLE courses(id INTEGER PRIMARY KEY, title TEXT, requires_project INTEGER);
            CREATE TABLE course_enrollments(id INTEGER PRIMARY KEY, intern_id INTEGER, email TEXT, course_id INTEGER, current_day INTEGER);
            CREATE TABLE course_day_quizzes(id INTEGER PRIMARY KEY, course_id INTEGER);
            CREATE TABLE day_quiz_attempts(enrollment_id INTEGER, day_quiz_id INTEGER, passed INTEGER);
            CREATE TABLE course_projects(course_id INTEGER, brief TEXT);
            CREATE TABLE intern_accounts(id INTEGER PRIMARY KEY, name TEXT, email TEXT);
            CREATE TABLE project_submissions(id INTEGER PRIMARY KEY, enrollment_id INTEGER, intern_id INTEGER, course_id INTEGER,
              github_repo_url TEXT, project_title TEXT, project_description TEXT, status TEXT,
              review_feedback TEXT, review_rubric TEXT, reviewed_by_staff_id INTEGER, reviewed_at TEXT,
              created_at TEXT DEFAULT '2026-11-23');
            CREATE TABLE review_log(queue_name TEXT, staff_id INTEGER, subject_type TEXT,
                                    subject_id INTEGER, decision TEXT, reason_code TEXT);
            INSERT INTO courses VALUES (1, 'Sample course', 1);
            INSERT INTO course_enrollments VALUES (1, 1, 'learner@example.test', 1, 1);
            INSERT INTO intern_accounts VALUES (1, 'Sample learner', 'learner@example.test');
            INSERT INTO course_projects VALUES (1, 'Implement a small inventory tool.');
        """)
    root = Path(__file__).resolve().parents[2]
    app = Flask(__name__, template_folder=str(root / "templates"))
    app.config["TESTING"] = True
    app.jinja_env.globals.update(csp_nonce=lambda: "sample", csrf_token=lambda: "sample", csrf_field=lambda: "")
    source = ast.parse((root / "app.py").read_text(encoding="utf-8"))
    handlers = [node for node in source.body if isinstance(node, ast.FunctionDef)
                and node.name in {"course_submit_project", "staff_project_decision"}]
    exec(compile(ast.Module(body=handlers, type_ignores=[]), "project-handlers", "exec"), {
        "app": app, "request": request, "abort": abort, "jsonify": jsonify, "redirect": redirect,
        "render_template": render_template, "get_db": db, "row_to_dict": dict, "datetime": datetime, "json": json,
        "current_intern": lambda: {"id": 1, "email": "learner@example.test"},
        "current_staff": lambda: {"id": 2} if request.headers.get("X-Synthetic-Reviewer") else None,
    })

    client = app.test_client()
    workspace = "/courses/1/submit-project"
    revision = {"github_repo_url": "https://github.com/example/test-repo", "project_title": "Inventory app",
                "project_description": "A synthetic example with validation and a README."}
    assert client.post(workspace, json=revision).status_code == 200
    assert client.post(workspace, json=revision).status_code == 409
    feedback = {"decision": "changes_requested", "feedback": "Add a case for an empty inventory.",
                "rubric": {"verification": "Needs revision"}}
    assert client.post("/staff/projects/1/decision", json=feedback).status_code == 401
    review = client.post("/staff/projects/1/decision", json=feedback, headers={"X-Synthetic-Reviewer": "1"})
    assert review.status_code == 200
    visible = client.get(workspace)
    assert b"Revision history" in visible.data and b"empty inventory" in visible.data
    assert b"Needs revision" in visible.data
    assert client.post(workspace, json={**revision, "project_title": "Inventory app v2"}).status_code == 200
    status = client.get(workspace)
    assert b"Inventory app v2" in status.data and b"empty inventory" in status.data
    with db() as connection:
        assert connection.execute("SELECT COUNT(*) FROM project_submissions").fetchone()[0] == 2
        assert connection.execute("SELECT decision FROM review_log").fetchone()[0] == "changes_requested"
