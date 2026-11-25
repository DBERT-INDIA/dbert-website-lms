"""Validate cohort progress and credentials against a synthetic offline database."""

import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from threading import Barrier

import pytest
from flask import Flask, request

from services.cohort_progress import cohort_progress_blueprint, init_cohort_progress_tables
from services.database.adapter import SQLiteAdapter
from services.study_classroom import init_study_classroom


LEARNER = "/program-cohorts/1/progress"
STAFF = "/program-cohorts/1/staff/progress"
ADMIN = {"X-Admin": "1"}
MENTOR = {"X-Mentor": "7"}
INTERN = {"X-Intern": "2"}


@pytest.fixture
def portal(tmp_path):
    @contextmanager
    def db():
        conn = SQLiteAdapter(str(tmp_path / "cohorts.sqlite"))
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    with db() as conn:
        conn.executescript("""
            CREATE TABLE intern_accounts (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
            CREATE TABLE courses (id INTEGER PRIMARY KEY, requires_project INTEGER);
            CREATE TABLE program_cohorts (id INTEGER PRIMARY KEY, course_id INTEGER, title TEXT,
                starts_on TEXT, ends_on TEXT, mentor_id INTEGER, updated_at TEXT, schedule_locked_at TEXT);
            CREATE TABLE program_cohort_memberships (id INTEGER PRIMARY KEY, cohort_id INTEGER
                REFERENCES program_cohorts(id), intern_id INTEGER REFERENCES intern_accounts(id)
                ON DELETE CASCADE, status TEXT, enrolled_at TEXT, updated_at TEXT);
            CREATE TABLE course_enrollments (id INTEGER PRIMARY KEY, intern_id INTEGER, email TEXT,
                course_id INTEGER, completed_at TEXT);
            CREATE TABLE course_day_quizzes (id INTEGER PRIMARY KEY, course_id INTEGER);
            CREATE TABLE day_quiz_attempts (enrollment_id INTEGER, day_quiz_id INTEGER,
                passed INTEGER, created_at TEXT);
            CREATE TABLE project_submissions (id INTEGER PRIMARY KEY, enrollment_id INTEGER,
                intern_id INTEGER, course_id INTEGER, status TEXT, created_at TEXT);
            CREATE TABLE course_chapters (id INTEGER PRIMARY KEY, course_id INTEGER);
            CREATE TABLE course_subtopics (id INTEGER PRIMARY KEY, chapter_id INTEGER);
            CREATE TABLE intern_certificates (id INTEGER PRIMARY KEY, intern_id INTEGER, email TEXT,
                course_id INTEGER, course_title TEXT, cert_id TEXT, issued_at TEXT, url TEXT,
                received_at TEXT, tier TEXT, credential_status TEXT DEFAULT 'valid',
                UNIQUE (intern_id, cert_id));
            INSERT INTO intern_accounts VALUES
                (2, 'Riya Example', 'riya@example.test'), (3, 'Anu Example', 'anu@example.test'),
                (4, 'Other Example', 'other@example.test');
            INSERT INTO courses VALUES (5, 0), (6, 0);
            INSERT INTO program_cohorts VALUES
                (1, 5, 'Studio Cohort', '2026-11-01', '2026-11-30', 7, '2026-10-31', NULL),
                (2, 5, 'Later Cohort', '2026-11-01', '2026-11-30', 8, '2026-10-31', NULL);
            INSERT INTO program_cohort_memberships VALUES
                (10, 1, 2, 'enrolled', '2026-11-05 09:00:00', '2026-11-05'),
                (11, 1, 3, 'waitlisted', NULL, '2026-11-06'),
                (12, 2, 4, 'enrolled', '2026-11-03 09:00:00', '2026-11-03'),
                (13, 2, 2, 'enrolled', '2026-11-03 09:00:00', '2026-11-03');
            INSERT INTO course_enrollments VALUES
                (20, 2, 'riya@example.test', 5, '2026-10-26'),
                (21, 2, 'riya@example.test', 6, NULL), (22, 3, 'anu@example.test', 5, NULL);
            INSERT INTO course_day_quizzes VALUES (25, 5), (26, 5), (27, 5), (28, 6);
            INSERT INTO day_quiz_attempts VALUES
                (20, 25, 1, '2026-11-05T09:01:00'), (20, 25, 1, '2026-11-06'), (20, 26, 0, '2026-11-07'),
                (20, 27, 1, '2026-11-05T08:59:59'), (21, 28, 1, '2026-11-09'), (22, 26, 1, '2026-11-10');
            INSERT INTO project_submissions VALUES
                (30, 20, 2, 5, 'pending', '2026-11-06'),
                (31, 21, 2, 6, 'approved', '2026-11-08'),
                (32, 20, 2, 5, 'approved', '2026-11-05 08:59:59');
            INSERT INTO course_chapters VALUES (40, 5), (41, 6);
            INSERT INTO course_subtopics VALUES (50, 40), (51, 40), (52, 41);
        """)
        init_study_classroom(conn)
        init_cohort_progress_tables(conn)
        conn.executemany(
            """INSERT INTO study_classroom_entries
               (intern_id, course_id, lesson_id, request_id, question, answer,
               citations_json, created_at, updated_at) VALUES (?, 5, ?, ?, ?, 'Private answer', '[]', ?, ?)""",
            (
                (2, 50, "a", "Private question 1", "2026-11-06", "2026-11-06"),
                (2, 50, "b", "Private question 2", "2026-11-08", "2026-11-08"),
                (3, 51, "c", "Another learner", "2026-11-06", "2026-11-06"),
                (2, 52, "d", "Other course", "2026-11-06", "2026-11-06"),
                (2, 51, "e", "Earlier question", "2026-11-05T08:59:59", "2026-11-05T08:59:59"),
            ),
        )

    def identity(header):
        actor = request.headers.get(header, type=int)
        return {"id": actor} if actor else None

    app = Flask(__name__, template_folder=str(Path(__file__).resolve().parents[2] / "templates"))
    app.config.update(TESTING=True, SECRET_KEY="synthetic")
    app.jinja_env.globals.update(csrf_field=lambda: "", csrf_token=lambda: "", csp_nonce=lambda: "")
    app.register_blueprint(cohort_progress_blueprint(
        db, lambda: identity("X-Intern"), lambda: identity("X-Admin"),
        lambda: identity("X-Mentor"), lambda: "2026-11-24 13:00:00",
    ))
    return app.test_client(), db


def _add(client, kind, threshold=1, required=True, due_on="", path=STAFF):
    return client.post(path, headers=ADMIN, follow_redirects=True, data={
        "action": "add", "title": f"{kind.capitalize()} milestone", "kind": kind,
        "threshold": threshold, "due_on": due_on, "required": "1" if required else "",
    })


def test_progress_scopes_distinct_evidence_and_credential_issuance(portal):
    client, db = portal
    assert b"Complete the required milestones" in client.post(
        LEARNER, headers=INTERN, follow_redirects=True
    ).data
    _add(client, "quiz", threshold=2)
    _add(client, "question", threshold=2)
    _add(client, "project", required=False, due_on="2026-11-20")
    _add(client, "course")

    display = client.get(LEARNER, headers=INTERN)
    assert display.headers["Cache-Control"] == "private, no-store"
    assert b"Distinct quizzes passed" in display.data and b"Distinct lessons discussed" in display.data
    assert display.data.count(b"1/2") == 2
    assert b"0/1" in display.data and b"Overdue" in display.data
    assert b"Claim credential" not in display.data
    assert b"Private question" not in client.get(STAFF, headers=MENTOR).data

    with db() as conn:
        conn.execute("INSERT INTO day_quiz_attempts VALUES (20, 26, 1, '2026-11-23')")
        conn.execute("""INSERT INTO study_classroom_entries
            (intern_id, course_id, lesson_id, request_id, question, answer, citations_json, created_at, updated_at)
            VALUES (2, 5, 51, 'f', 'Private late question', 'Answer', '[]', '2026-11-23', '2026-11-23')""")
    assert b"Claim credential" in client.get(LEARNER, headers=INTERN).data
    issued = client.post(LEARNER, headers=INTERN, follow_redirects=True)
    assert b"Cohort credential issued" in issued.data and b"View credential" in issued.data
    assert b"already been issued" in client.post(LEARNER, headers=INTERN, follow_redirects=True).data
    assert b"Milestones are locked" in _add(client, "quiz").data

    with db() as conn:
        member = conn.execute("SELECT * FROM program_cohort_memberships WHERE id=10").fetchone()
        receipt = conn.execute("SELECT * FROM program_cohort_credentials").fetchone()
        assert conn.execute("SELECT schedule_locked_at FROM program_cohorts WHERE id=1").fetchone()[0]
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_credentials").fetchone()[0] == 1
        wallet = conn.execute("SELECT * FROM intern_certificates WHERE cert_id=?", (receipt["cert_id"],)).fetchone()
        assert member["status"] == "completed" and receipt["membership_id"] == 10
        assert receipt["issued_by_type"] == "intern" and receipt["issued_by"] == "2"
        assert wallet["intern_id"] == 2 and wallet["course_id"] is None
        assert wallet["tier"] == "program_cohort_completion"
        assert "Private" not in receipt["evidence_json"]
        assert sum(bool(state["met"]) for state in json.loads(receipt["evidence_json"])) == 3
        conn.execute("DELETE FROM day_quiz_attempts")
    assert b"3 / 3" in client.get(LEARNER, headers=INTERN).data


def test_role_and_membership_boundaries_and_mentor_checkins(portal):
    client, db = portal
    assert client.get(LEARNER).status_code == 404
    assert client.get(LEARNER, headers={"X-Intern": "3"}).status_code == 404
    assert client.get(STAFF, headers=INTERN).status_code == 404
    assert client.get(STAFF, headers={"X-Mentor": "8"}).status_code == 404
    assert client.post(STAFF, headers=MENTOR, data={"action": "add"}).status_code == 403
    assert client.post(STAFF, headers=MENTOR, data={"action": "graduate", "membership_id": "10"}).status_code == 403
    assert client.post(STAFF, headers=MENTOR, data={"action": "checkin", "membership_id": "12"}).status_code == 404
    message = "Please review your results. <private>"
    sent = client.post(STAFF, headers=MENTOR, follow_redirects=True, data={
        "action": "checkin", "membership_id": "10", "message": message,
    })
    assert b"Check-in saved" in sent.data and b"Please review your results. &lt;private&gt;" in sent.data
    assert b"Please review your results" in client.get(LEARNER, headers=INTERN).data
    assert b"Please review your results" not in client.get("/program-cohorts/2/progress", headers=INTERN).data
    with db() as conn:
        conn.execute("DELETE FROM intern_accounts WHERE id=2")
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_checkins").fetchone()[0] == 0


def test_admin_graduation_is_separate_for_two_cohorts_of_same_course(portal):
    client, db = portal
    _add(client, "course")
    _add(client, "course", path="/program-cohorts/2/staff/progress")
    assert b"Cohort credential issued" in client.post(STAFF, headers=ADMIN, follow_redirects=True, data={
        "action": "graduate", "membership_id": "10",
    }).data
    assert b"Cohort credential issued" in client.post(
        "/program-cohorts/2/progress", headers=INTERN, follow_redirects=True
    ).data
    with db() as conn:
        assert conn.execute("SELECT COUNT(DISTINCT cert_id) FROM intern_certificates").fetchone()[0] == 2
        receipt = conn.execute("SELECT * FROM program_cohort_credentials WHERE membership_id=10").fetchone()
        assert receipt["issued_by_type"] == "admin" and receipt["issued_by"] == "1"


def test_simultaneous_claims_create_one_credential(portal):
    client, db = portal
    _add(client, "course")
    ready = Barrier(2)

    def claim():
        ready.wait(timeout=5)
        return client.application.test_client().post(
            LEARNER, headers=INTERN, follow_redirects=True
        ).data

    with ThreadPoolExecutor(max_workers=2) as pool:
        requests = [pool.submit(claim) for _ in range(2)]
        replies = [pending.result(timeout=10) for pending in requests]
    assert sum(b"Cohort credential issued" in reply for reply in replies) == 1
    assert sum(b"already been issued" in reply for reply in replies) == 1
    with db() as conn:
        assert conn.execute("SELECT COUNT(*) FROM intern_certificates").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_credentials").fetchone()[0] == 1


def test_course_completion_requires_approved_capstone_when_configured(portal):
    client, db = portal
    _add(client, "course")
    with db() as conn:
        conn.execute("UPDATE courses SET requires_project = 1 WHERE id = 5")
        conn.execute("UPDATE project_submissions SET status = 'rejected' WHERE id = 32")
        conn.execute("INSERT INTO project_submissions VALUES (33, 22, 3, 5, 'approved', '2026-11-15')")

    # The final quiz can set completed_at while a capstone is pending or rejected.
    assert b"Claim credential" not in client.get(LEARNER, headers=INTERN).data
    assert b"Complete the required milestones" in client.post(
        LEARNER, headers=INTERN, follow_redirects=True,
    ).data
    with db() as conn:
        conn.execute("UPDATE project_submissions SET status = 'approved' WHERE id = 30")
    assert b"Claim credential" in client.get(LEARNER, headers=INTERN).data


@pytest.mark.parametrize("upgrade_existing", [False, True], ids=["new-issuance", "existing-receipt"])
def test_first_credential_lock_survives_account_deletion(portal, upgrade_existing):
    client, db = portal
    _add(client, "course")
    issued = client.post(LEARNER, headers=INTERN, follow_redirects=True)
    assert b"Cohort credential issued" in issued.data
    with db() as conn:
        if upgrade_existing:
            conn.execute("ALTER TABLE program_cohorts DROP COLUMN milestones_locked_at")
            init_cohort_progress_tables(conn)
            init_cohort_progress_tables(conn)
        lock = conn.execute("SELECT milestones_locked_at FROM program_cohorts WHERE id = 1").fetchone()
        assert lock[0] == "2026-11-24 13:00:00"
        conn.execute("DELETE FROM intern_accounts WHERE id = 2")
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_credentials").fetchone()[0] == 0

    assert b"Milestones are locked" in _add(client, "quiz").data
    archived = client.post(STAFF, headers=ADMIN, follow_redirects=True, data={"action": "archive", "milestone_id": "1"})
    assert b"Milestones are locked" in archived.data
    with db() as conn:
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_milestones").fetchone()[0] == 1
