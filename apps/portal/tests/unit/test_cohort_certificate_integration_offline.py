from contextlib import contextmanager
from pathlib import Path

import pytest
from flask import Flask, render_template

from services.certificate_service import CertificateService
from services.cohort_progress import cohort_progress_blueprint, init_cohort_progress_tables
from services.database.adapter import SQLiteAdapter
from services.privacy_service import serialize_public_certificate
from services.program_cohorts import init_program_cohorts


@pytest.mark.parametrize("course_first", (True, False), ids=("course-first", "cohort-first"))
def test_program_credential_coexists_with_ordinary_and_formal_credentials(tmp_path, monkeypatch, course_first):
    path = str(tmp_path / "certificates.sqlite")

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
            CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, domain TEXT);
            CREATE TABLE mentors (id INTEGER PRIMARY KEY);
            CREATE TABLE intern_accounts (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
            CREATE TABLE applications (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
            CREATE TABLE course_enrollments (id INTEGER PRIMARY KEY, course_id INTEGER, intern_id INTEGER, email TEXT);
            CREATE TABLE course_day_quizzes (id INTEGER PRIMARY KEY, course_id INTEGER);
            CREATE TABLE day_quiz_attempts (enrollment_id INTEGER, day_quiz_id INTEGER, passed INTEGER, created_at TEXT);
            CREATE TABLE intern_certificates (
                id INTEGER PRIMARY KEY, intern_id INTEGER NOT NULL, course_id INTEGER REFERENCES courses(id),
                course_title TEXT, cert_id TEXT, issued_at TEXT, url TEXT, received_at TEXT, tier TEXT, email TEXT,
                credential_status TEXT DEFAULT 'valid', UNIQUE(intern_id, cert_id)
            );
            INSERT INTO courses VALUES (1, 'Web Fundamentals', 'Web'), (0, 'Formal Internship Credential', 'Web');
            INSERT INTO intern_accounts VALUES (1, 'Example Learner', 'learner@example.test');
            INSERT INTO course_enrollments VALUES (1, 1, 1, NULL);
            INSERT INTO course_day_quizzes VALUES (1, 1);
            INSERT INTO day_quiz_attempts VALUES (1, 1, 1, '2026-11-23');
        """)
        init_program_cohorts(conn)
        init_cohort_progress_tables(conn)
        conn.execute(
            """INSERT INTO program_cohorts (course_id, title, starts_on, ends_on, capacity, status, created_at, updated_at)
               VALUES (1, 'Studio Cohort', '2026-11-01', '2026-11-30', 10, 'open', '2026-11-01', '2026-11-01')"""
        )
        conn.execute(
            """INSERT INTO program_cohort_memberships (cohort_id, intern_id, status, requested_at, enrolled_at, updated_at)
               VALUES (1, 1, 'enrolled', '2026-11-01', '2026-11-01', '2026-11-01')"""
        )
        conn.execute(
            """INSERT INTO program_cohort_milestones (cohort_id, title, kind, threshold, required, created_at, created_by)
               VALUES (1, 'Pass a quiz', 'quiz', 1, 1, '2026-11-01', '1')"""
        )
        if course_first:
            CertificateService.issue_course_completion_certificate(conn, 1, 1)
        conn.execute(
            """INSERT INTO intern_certificates (intern_id, course_id, course_title, cert_id, tier, email)
               VALUES (1, 0, 'Formal Internship Credential', 'FORMAL-DBERT-1', 'verified', 'learner@example.test')"""
        )

    templates = Path(__file__).resolve().parents[2] / "templates"
    app = Flask(__name__, template_folder=str(templates))
    app.config.update(TESTING=True, SECRET_KEY="synthetic")
    app.jinja_env.globals.update(csp_nonce=lambda: "test", csrf_token=lambda: "test", csrf_field=lambda: "")
    app.register_blueprint(cohort_progress_blueprint(
        db, lambda: {"id": 1}, lambda: None, lambda: None, lambda: "2026-11-24 08:00:00",
    ))
    monkeypatch.setattr(CertificateService, "load_registry_record", staticmethod(lambda **kwargs: None))
    client = app.test_client()
    assert client.post("/program-cohorts/1/progress").status_code == 303

    with db() as conn:
        formal = CertificateService.is_intern_verified(conn, intern_id=1)
        assert formal["verified"]
        assert formal["cert_id"] == "FORMAL-DBERT-1"

        ordinary = CertificateService.issue_course_completion_certificate(conn, 1, 1)
        repeat = CertificateService.issue_course_completion_certificate(conn, 1, 1)
        assert repeat["cert_id"] == ordinary["cert_id"]
        assert ordinary["already_issued"] == course_first

        wallet = CertificateService.get_intern_certificates(conn, 1, "learner@example.test")
        cohort = next(cert for cert in wallet if cert["tier"] == "program_cohort_completion")
        assert cohort["course_id"] is None
        assert cohort["cert_id"] != ordinary["cert_id"]
        wallet_courses = [record for record in wallet if record["course_id"] == 1]
        assert [record["tier"] for record in wallet_courses] == ["course_completion"]
        found = CertificateService.verify_certificate(conn, cohort["cert_id"])

    with app.test_request_context("/portal/certificate/" + cohort["cert_id"]):
        result = render_template("cert_verify.html", cert=serialize_public_certificate(found))
        assert "Valid certificate" in result
        assert "Studio Cohort" in result
        assert "learner@example.test" not in result
