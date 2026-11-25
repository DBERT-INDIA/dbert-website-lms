"""Exercise turn persistence without loading the portal or any external provider."""

import sqlite3
from concurrent.futures import ThreadPoolExecutor

import pytest

from services.database.adapter import translate_sql
from services.learning.concept_service import ConceptService
from services.learning.learning_models import Concept, init_learning_tables
from services.learning.mastery_policy import MasteryPolicy
from services.learning.session_service import DuplicateTurnError, LearningSessionService


def connect(path):
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


@pytest.fixture
def learning_path(tmp_path):
    path = tmp_path / "learning.db"
    db = connect(path)
    try:
        init_learning_tables(db)
        ConceptService.register_concept(db, Concept(
            concept_id="python.variables",
            name="Variables",
            description="Store and update values",
            domain="Python",
            subject="Foundations",
            assessment_criteria=["assignment", "variable"],
        ))
        db.execute(
            """INSERT INTO gl_learning_sessions (
                   session_id, student_id, course_id, current_concept_id,
                   last_heartbeat_at, created_at, updated_at
               ) VALUES ('first', 1, 1, 'python.variables', '0', '0', '0'),
                        ('second', 2, 1, 'python.variables', '0', '0', '0')"""
        )
        db.commit()
    finally:
        db.close()
    return path


def submit(db, answer="A variable stores a value using assignment.", key="submission-1", session="first", student=1):
    return LearningSessionService.process_turn_atomic(db, session, student, answer, key)


def count(db, table):
    return db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def test_failure_rolls_back_the_entire_attempt(learning_path, monkeypatch):
    db = connect(learning_path)
    try:
        with monkeypatch.context() as patch:
            def fail_after_writes(*args, **kwargs):
                raise RuntimeError("synthetic write failure")

            patch.setattr(MasteryPolicy, "update_student_profile", fail_after_writes)
            with pytest.raises(RuntimeError, match="synthetic write failure"):
                submit(db)

        for table in (
            "gl_learning_turns", "gl_learning_events", "gl_student_mastery", "gl_student_learning_profile",
        ):
            assert count(db, table) == 0
        assert db.execute("SELECT updated_at FROM gl_learning_sessions WHERE session_id = 'first'").fetchone()[0] == "0"

        recovered = submit(db)
        assert recovered["mastery"]["total_attempts"] == 1
        assert count(db, "gl_learning_turns") == 1
    finally:
        db.close()


def test_old_key_replays_original_response_after_another_answer(learning_path):
    db = connect(learning_path)
    try:
        original = submit(db)
        submit(db, answer="Assignment changes what value a variable references.", key="submission-2")
        replay = submit(db)
        assert replay == {**original, "idempotent_replay": True}
        assert count(db, "gl_learning_turns") == 2
        with pytest.raises(DuplicateTurnError):
            submit(db, answer="Different answer.")
        assert count(db, "gl_learning_turns") == 2
        assert submit(db, session="second", student=2)["mastery"]["total_attempts"] == 1
    finally:
        db.close()


def test_concurrent_retries_record_one_turn(learning_path):
    def attempt():
        db = connect(learning_path)
        try:
            return submit(db)
        finally:
            db.close()

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(attempt) for _ in range(2)]
        results = [future.result(timeout=10) for future in futures]

    assert sorted(result.get("idempotent_replay", False) for result in results) == [False, True]
    db = connect(learning_path)
    try:
        assert count(db, "gl_learning_turns") == 1
        mastery = db.execute("SELECT total_attempts, review_count FROM gl_student_mastery").fetchone()
        assert tuple(mastery) == (1, 1)
    finally:
        db.close()


def test_grading_uses_the_postgres_keys_for_mastery_and_profile(learning_path):
    db = connect(learning_path)
    writes = {
        "gl_student_mastery": "student_id",
        "gl_student_learning_profile": "student_id",
    }
    translated_writes = set()

    class RecordingConnection:
        def __getattr__(self, name):
            return getattr(db, name)

        def execute(self, sql, params=()):
            for table, key in writes.items():
                if sql.lstrip().startswith(f"INSERT INTO {table}"):
                    translated = translate_sql(sql, auto_returning=True)
                    assert translated.strip().endswith(f"RETURNING {key}")
                    translated_writes.add(table)
            return db.execute(sql, params)

    try:
        assert submit(RecordingConnection())["mastery"]["total_attempts"] == 1
        assert translated_writes == set(writes)
    finally:
        db.close()
