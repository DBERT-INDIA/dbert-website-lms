from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from threading import Barrier

import pytest
from flask import Flask, request

from services.database.adapter import SQLiteAdapter
from services.program_cohorts import init_program_cohorts, program_cohorts_blueprint


@pytest.fixture
def cohort_app(tmp_path):
    path = str(tmp_path / "program-cohorts.db")

    @contextmanager
    def db():
        conn = SQLiteAdapter(path)
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    with db() as conn:
        conn.executescript("""
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY, title TEXT, company_id INTEGER, content_status TEXT, is_active INTEGER
            );
            CREATE TABLE mentors (id INTEGER PRIMARY KEY, name TEXT, is_active INTEGER);
            CREATE TABLE intern_accounts (id INTEGER PRIMARY KEY, name TEXT, email TEXT, is_active INTEGER);
            CREATE TABLE course_enrollments (id INTEGER PRIMARY KEY, intern_id INTEGER NOT NULL, course_id INTEGER, email TEXT);

            INSERT INTO courses VALUES (1, 'Web fundamentals', NULL, 'approved', 1), (2, 'Draft course', 9, 'pending', 1);
            INSERT INTO mentors VALUES (1, 'Assigned mentor', 1), (2, 'Other mentor', 1), (3, 'Inactive mentor', 0);
            INSERT INTO intern_accounts VALUES
                (1, 'First learner', 'first@example.test', 1), (2, 'Legacy learner', 'legacy@example.test', 1),
                (3, 'Third learner', 'third@example.test', 1), (4, 'No course access', 'other@example.test', 1),
                (5, 'Inactive learner', 'inactive@example.test', 0);
            INSERT INTO course_enrollments VALUES
                (1, 1, 1, NULL), (2, 5, 1, 'LEGACY@example.test'), (3, 3, 1, NULL);
        """)
        init_program_cohorts(conn)
        init_program_cohorts(conn)

    templates = Path(__file__).resolve().parents[2] / "templates"
    app = Flask(__name__, template_folder=str(templates))
    app.config.update(TESTING=True, SECRET_KEY="synthetic-only")
    app.jinja_env.globals.update(csp_nonce=lambda: "test", csrf_token=lambda: "test", csrf_field=lambda: "")

    def actor(role):
        identifier = request.headers.get(f"X-Synthetic-{role}")
        if identifier:
            return {"id": int(identifier)}
        return None

    day = {"now": "2026-11-24 08:00:00"}
    app.register_blueprint(program_cohorts_blueprint(
        db, lambda: actor("Intern"), lambda: actor("Admin"), lambda: actor("Mentor"), lambda: day["now"],
    ))
    return app, db, day


ADMIN = {"X-Synthetic-Admin": "1"}
CREATE = {
    "title": "November web cohort", "starts_on": "2026-11-26", "ends_on": "2026-12-02",
    "capacity": "1", "course_id": "1", "mentor_id": "1",
}
LEARNER = "/program-cohorts/1"
STAFF = "/admin/program-cohorts/1"


def learner(identifier):
    return {"X-Synthetic-Intern": str(identifier)}


def test_course_entitlement_registration_roster_and_promotion(cohort_app):
    app, db, _ = cohort_app
    client = app.test_client()
    assert client.get("/program-cohorts").location == "/#signin"
    assert client.post("/admin/program-cohorts", headers=learner(1), data=CREATE).status_code == 403
    assert client.post("/admin/program-cohorts", headers=ADMIN, data={**CREATE, "course_id": "2"}).status_code == 200
    assert client.post("/admin/program-cohorts", headers=ADMIN, data={**CREATE, "mentor_id": "3"}).status_code == 200
    assert client.post("/admin/program-cohorts", headers=ADMIN, data=CREATE).location == STAFF
    assert b"November web cohort" in client.get("/program-cohorts", headers=learner(4)).data
    denied = client.post(LEARNER, headers=learner(4), data={"action": "join", "intern_id": "1"}, follow_redirects=True)
    assert b"Enroll in the course before joining this cohort" in denied.data

    for identifier in (1, 2, 3, 3):
        assert client.post(LEARNER, headers=learner(identifier), data={"action": "join"}).location == LEARNER
    enrolled = client.get(LEARNER, headers=learner(1)).data
    assert b"/courses/1/study" in enrolled
    assert b"View my progress" in enrolled
    waiting = client.get(LEARNER, headers=learner(2)).data
    assert b"You are on the waitlist" in waiting
    assert b"Third learner" not in waiting
    assert b"View my progress" not in waiting
    assert client.get(STAFF, headers=learner(1)).status_code == 403
    assert client.get("/mentor/program-cohorts/1", headers={"X-Synthetic-Mentor": "2"}).status_code == 404
    mentor_roster = client.get("/mentor/program-cohorts/1", headers={"X-Synthetic-Mentor": "1"}).data
    assert b"Legacy learner" in mentor_roster
    assert b"/program-cohorts/1/study" in mentor_roster
    assert b"example.test" not in mentor_roster
    assert b"Recent registration activity" not in mentor_roster
    assert b"Recent registration activity" in client.get(STAFF, headers=ADMIN).data

    with db() as conn:
        conn.execute("DELETE FROM course_enrollments WHERE id = 2")
    # Posting another member's ID cannot withdraw them. The signed-in learner controls the target.
    client.post(LEARNER, headers=learner(1), data={"action": "withdraw", "intern_id": "3"})
    with db() as conn:
        members = conn.execute("SELECT intern_id, status FROM program_cohort_memberships ORDER BY intern_id").fetchall()
        assert [tuple(member) for member in members] == [(1, "withdrawn"), (2, "waitlisted"), (3, "enrolled")]
        history = conn.execute("SELECT intern_id, action FROM program_cohort_access_log ORDER BY id").fetchall()
        assert [tuple(event) for event in history] == [
            (None, "created"), (1, "enrolled"), (2, "waitlisted"), (3, "waitlisted"),
            (1, "withdrawn"), (3, "promoted"),
        ]
        conn.execute("DELETE FROM mentors WHERE id = 1")
        conn.execute("DELETE FROM intern_accounts WHERE id = 1")
        assert conn.execute("SELECT mentor_id FROM program_cohorts").fetchone()[0] is None
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_memberships").fetchone()[0] == 2


def test_registration_lifecycle_and_rejoining_moves_to_end_of_queue(cohort_app):
    app, db, day = cohort_app
    client = app.test_client()
    client.post("/admin/program-cohorts", headers=ADMIN, data=CREATE)
    for identifier, action in ((1, "join"), (2, "join"), (3, "join"), (2, "withdraw"), (2, "join")):
        client.post(LEARNER, headers=learner(identifier), data={"action": action})
    client.post(STAFF, headers=ADMIN, data={"status": "closed"})
    assert client.get(LEARNER, headers=learner(4)).status_code == 404
    client.post(LEARNER, headers=learner(1), data={"action": "withdraw"})
    with db() as conn:
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_memberships WHERE status = 'enrolled'").fetchone()[0] == 0
    client.post(STAFF, headers=ADMIN, data={"status": "open"})
    with db() as conn:
        first_in_line = conn.execute("SELECT intern_id FROM program_cohort_memberships WHERE status = 'enrolled'").fetchone()
        assert first_in_line[0] == 3
    day["now"] = "2026-12-03 00:00:00"
    client.post(LEARNER, headers=learner(3), data={"action": "withdraw"})
    closed = client.post(STAFF, headers=ADMIN, data={"status": "open"}, follow_redirects=True)
    assert b"Registration can reopen while the cohort dates and course are active" in closed.data
    with db() as conn:
        assert conn.execute("SELECT COUNT(*) FROM program_cohort_memberships WHERE status = 'enrolled'").fetchone()[0] == 0


def test_simultaneous_joins_cannot_overbook_the_last_seat(cohort_app):
    app, db, _ = cohort_app
    app.test_client().post("/admin/program-cohorts", headers=ADMIN, data=CREATE)
    released = Barrier(2)

    def join(identifier):
        client = app.test_client()
        released.wait(timeout=5)
        return client.post(LEARNER, headers=learner(identifier), data={"action": "join"}).status_code

    with ThreadPoolExecutor(max_workers=2) as workers:
        assert list(workers.map(join, (1, 2))) == [302, 302]
    with db() as conn:
        rows = conn.execute("SELECT status, queue_order FROM program_cohort_memberships ORDER BY queue_order").fetchall()
        assert [tuple(row) for row in rows] == [("enrolled", 1), ("waitlisted", 2)]


def test_admin_capacity_mentor_reassignment_and_manual_promotion(cohort_app):
    app, db, _ = cohort_app
    client = app.test_client()
    client.post("/admin/program-cohorts", headers=ADMIN, data=CREATE)
    for identifier in (1, 2, 3):
        client.post(LEARNER, headers=learner(identifier), data={"action": "join"})

    updated = {**CREATE, "action": "update", "capacity": "2", "mentor_id": "2", "course_id": "2"}
    assert client.post(STAFF, headers=ADMIN, data=updated).status_code == 302
    with db() as conn:
        cohort = conn.execute("SELECT course_id, mentor_id, capacity FROM program_cohorts").fetchone()
        assert tuple(cohort) == (1, 2, 2)
        conn.execute("UPDATE program_cohorts SET schedule_locked_at = '2026-11-24 09:00:00'")
    assert client.get("/mentor/program-cohorts/1", headers={"X-Synthetic-Mentor": "1"}).status_code == 404
    assert client.get("/mentor/program-cohorts/1", headers={"X-Synthetic-Mentor": "2"}).status_code == 200

    rejected = client.post(STAFF, headers=ADMIN, data={**updated, "capacity": "1"})
    assert rejected.status_code == 422
    assert b"Capacity must cover the enrolled and completed learners" in rejected.data
    reschedule = client.post(STAFF, headers=ADMIN, data={**updated, "starts_on": "2026-11-27"})
    assert reschedule.status_code == 422
    assert b"Cohort dates are fixed once a milestone is defined" in reschedule.data
    with db() as conn:
        conn.execute("DELETE FROM intern_accounts WHERE id = 1")
    filled = client.post(STAFF, headers=ADMIN, data={"action": "fill-seats"}, follow_redirects=True)
    assert b"Seats filled from the waitlist: 1." in filled.data
    with db() as conn:
        members = conn.execute("SELECT intern_id, status FROM program_cohort_memberships ORDER BY intern_id").fetchall()
        assert [tuple(member) for member in members] == [(2, "enrolled"), (3, "enrolled")]
