"""Run the real course quiz routes without booting unrelated portal integrations."""

import ast
import json
import re
import secrets
import sqlite3
import sys
from contextlib import contextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest
from flask import Flask, abort, jsonify, redirect, render_template, request, session


@pytest.fixture
def quiz(tmp_path):
    db_path = tmp_path / "quizzes.db"

    @contextmanager
    def db():
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        finally:
            connection.close()

    with db() as connection:
        connection.executescript("""
            CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, domain TEXT);
            CREATE TABLE course_chapters (id INTEGER PRIMARY KEY, course_id INTEGER, day_number INTEGER, title TEXT);
            CREATE TABLE course_enrollments (id INTEGER PRIMARY KEY, intern_id INTEGER, course_id INTEGER,
                                             email TEXT, current_day INTEGER, completed_at TEXT);
            CREATE TABLE course_day_quizzes (id INTEGER PRIMARY KEY, course_id INTEGER, day_number INTEGER, questions_json TEXT);
            CREATE TABLE day_quiz_attempts (enrollment_id INTEGER, day_quiz_id INTEGER, score INTEGER, max_score INTEGER,
                                            passed INTEGER, tab_switches INTEGER, time_taken_sec INTEGER);
            CREATE TABLE day_quiz_receipts (attempt_key TEXT PRIMARY KEY, enrollment_id INTEGER, quiz_id INTEGER,
                                            response_json TEXT, created_at TEXT);
            CREATE TABLE intern_certificates (id INTEGER PRIMARY KEY, intern_id INTEGER, course_id INTEGER,
                                              course_title TEXT, cert_id TEXT UNIQUE, issued_at TEXT, url TEXT,
                                              tier TEXT, email TEXT);
            CREATE TABLE event_outbox (id INTEGER PRIMARY KEY, event_type TEXT, aggregate_type TEXT, aggregate_id TEXT,
                                       payload_json TEXT, status TEXT, retry_count INTEGER, max_retries INTEGER,
                                       next_retry_at TEXT, created_at TEXT, updated_at TEXT);
            INSERT INTO courses VALUES (1, 'Sample Python course', 'Python');
            INSERT INTO course_chapters VALUES (1, 1, 1, 'Variables'), (2, 1, 2, 'Loops');
            INSERT INTO course_enrollments VALUES (1, 1, 1, NULL, 1, NULL);
        """)
        questions = [{"id": i, "question": f"Sample question {i}", "options": ["A", "B"], "correct_index": 0}
                     for i in range(1, 6)]
        connection.execute("INSERT INTO course_day_quizzes VALUES (1, 1, 1, ?)", (json.dumps(questions),))
        connection.commit()

    root = Path(__file__).resolve().parents[2]
    app = Flask(__name__, template_folder=str(root / "templates"))
    app.config.update(TESTING=True, SECRET_KEY="synthetic-quiz-handler-tests")
    app.jinja_env.globals.update(csp_nonce=lambda: "synthetic", csrf_token=lambda: "synthetic")
    clock = SimpleNamespace(now=1000)
    namespace = {
        "app": app, "current_intern": lambda: {"id": int(request.headers.get("X-Learner", "1"))},
        "get_db": db, "session": session, "request": request, "time": SimpleNamespace(time=lambda: clock.now),
        "render_template": render_template, "redirect": redirect, "jsonify": jsonify, "abort": abort,
        "json": json, "re": re, "secrets": secrets, "now_str": lambda: "2026-11-23 10:00:00",
        "log_error": lambda context, error: app.logger.error("%s: %s", context, error),
    }
    source = ast.parse((root / "app.py").read_text(encoding="utf-8"))
    handlers = [node for node in source.body if isinstance(node, ast.FunctionDef)
                and node.name in {"course_quiz_page", "course_quiz_submit", "_finalize_quiz_receipt"}]
    exec(compile(ast.Module(body=handlers, type_ignores=[]), "quiz-handlers", "exec"), namespace)
    return app.test_client(), clock, db


def test_quiz_refresh_keeps_attempt_and_server_timer(quiz):
    client, clock, _ = quiz
    opened = client.get("/courses/1/quiz/1")
    assert opened.status_code == 200
    with client.session_transaction() as state:
        started = dict(state["quiz_attempt_1_1"])
    clock.now += 23
    refreshed = client.get("/courses/1/quiz/1")
    assert refreshed.status_code == 200
    assert b"const initialSeconds = 23" in refreshed.data
    with client.session_transaction() as state:
        assert state["quiz_attempt_1_1"] == started


def test_quiz_receipt_replays_after_completion_with_no_duplicate_grade(quiz):
    client, clock, db = quiz
    assert client.get("/courses/1/quiz/1").status_code == 200
    with client.session_transaction() as state:
        key = state["quiz_attempt_1_1"]["key"]
    clock.now += 18
    endpoint = "/courses/1/quiz/1/submit"
    submit = {"attempt_key": key, "answers": {"1": 0, "2": 0, "3": 0, "4": 1, "5": 1}}
    first = client.post(endpoint, json=submit)
    assert first.status_code == 200 and first.json["score"] == 3 and first.json["passed"] is False
    again = client.post(endpoint, json=submit)
    assert again.json == first.json
    assert client.post(endpoint, headers={"X-Learner": "2"}, json=submit).status_code == 403
    with db() as connection:
        assert connection.execute("SELECT COUNT(*) FROM day_quiz_attempts").fetchone()[0] == 1
        assert connection.execute("SELECT time_taken_sec FROM day_quiz_attempts").fetchone()[0] == 18


def test_completed_quiz_replays_and_repairs_failed_certificate_issuance(quiz, monkeypatch):
    from services.certificate_service import CertificateService

    client, clock, db = quiz
    email = "learner@example.test"
    with db() as connection:
        connection.execute("DELETE FROM course_chapters WHERE day_number = 2")
        connection.execute("UPDATE course_enrollments SET email = ?", (email,))
        connection.commit()

    issue_certificate = CertificateService.issue_course_completion_certificate
    issuance_attempts = []

    def issue_after_temporary_failure(*args, **kwargs):
        issuance_attempts.append(kwargs["email"])
        if len(issuance_attempts) == 1:
            raise sqlite3.OperationalError("Temporary certificate database failure")
        return issue_certificate(*args, **kwargs)

    completed_notifications = []
    monkeypatch.setattr(CertificateService, "issue_course_completion_certificate", issue_after_temporary_failure)
    monkeypatch.setitem(sys.modules, "services.notifications.web_push_service", SimpleNamespace(
        notify_course_completed_push=lambda *args: completed_notifications.append(args),
        notify_quiz_passed_push=lambda *_: pytest.fail("Expected the course completion notification"),
    ))

    assert client.get("/courses/1/quiz/1").status_code == 200
    with client.session_transaction() as state:
        key = state["quiz_attempt_1_1"]["key"]
    clock.now += 18
    endpoint = "/courses/1/quiz/1/submit"
    submission = {"attempt_key": key, "answers": {str(i): 0 for i in range(1, 6)}}
    completed = client.post(endpoint, json=submission)
    assert completed.status_code == 200 and completed.json["course_completed"] is True
    assert "certificate_issued" not in completed.json

    recovered = client.post(endpoint, json=submission)
    assert recovered.status_code == 200 and recovered.json["certificate_issued"] is True
    assert recovered.json["cert_url"].endswith(recovered.json["cert_id"])
    assert client.post(endpoint, json=submission).json == recovered.json
    assert issuance_attempts == [email, email]
    assert completed_notifications == [(email, "Sample Python course", recovered.json["cert_id"])]

    with db() as connection:
        assert connection.execute("SELECT COUNT(*) FROM day_quiz_attempts").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM intern_certificates").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM event_outbox").fetchone()[0] == 1
        stored = connection.execute("SELECT response_json FROM day_quiz_receipts").fetchone()["response_json"]
        assert json.loads(stored) == recovered.json
