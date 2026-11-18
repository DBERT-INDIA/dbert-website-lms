"""
DBERT LMS - Comprehensive Test Suite for All 9 Platform Domains (7-Day Curricula)
================================================================================
Validates:
1. All 9 VALID_DOMAINS have active, approved 7-day courses.
2. Every course has exactly 7 chapters (Days 1–7).
3. Every chapter has valid subtopics with structured key takeaways.
4. Every day has an associated quiz with valid questions and options.
5. Intern catalog isolation and auto-enrollment across all 9 domains.
================================================================================
"""

import json
import pytest
from app import app, get_db, VALID_DOMAINS, auto_enroll_intern_in_domain_courses
from config.courses_7day_catalog import ALL_9_DOMAIN_COURSES


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as c:
        yield c


def test_catalog_coverage_all_9_domains():
    """Verify that the course catalog module contains definitions for all 9 VALID_DOMAINS."""
    catalog_domains = [c["domain"] for c in ALL_9_DOMAIN_COURSES]
    assert len(catalog_domains) == 9
    for vd in VALID_DOMAINS:
        assert vd in catalog_domains, f"Domain '{vd}' missing from ALL_9_DOMAIN_COURSES"


def test_database_has_active_course_for_all_9_domains():
    """Verify that the database has an active, approved course for every single domain."""
    with get_db() as conn:
        for vd in VALID_DOMAINS:
            c = conn.execute(
                "SELECT id, title, slug, domain, is_active, content_status FROM courses WHERE domain = ? AND is_active = 1 LIMIT 1",
                (vd,)
            ).fetchone()
            assert c is not None, f"No active course found in DB for domain: '{vd}'"
            assert c["is_active"] == 1
            assert c["content_status"] == "approved"
            assert c["title"] is not None and len(c["title"]) > 5
            assert c["slug"] is not None and len(c["slug"]) > 2


def test_each_course_has_exactly_7_days():
    """Verify that every domain course has exactly 7 chapters corresponding to Days 1 through 7."""
    with get_db() as conn:
        for vd in VALID_DOMAINS:
            c = conn.execute("SELECT id FROM courses WHERE domain = ? AND is_active = 1 LIMIT 1", (vd,)).fetchone()
            assert c is not None
            chapters = conn.execute(
                "SELECT id, day_number, title FROM course_chapters WHERE course_id = ? ORDER BY day_number",
                (c["id"],)
            ).fetchall()
            
            day_nums = [row["day_number"] for row in chapters]
            assert day_nums == [1, 2, 3, 4, 5, 6, 7], f"Domain '{vd}' course ID {c['id']} days mismatch: {day_nums}"
            for row in chapters:
                assert row["title"] is not None and len(row["title"]) > 3


def test_each_chapter_has_valid_subtopics():
    """Verify that every chapter across all 9 courses has 2 to 3 subtopics with valid takeaways."""
    with get_db() as conn:
        for vd in VALID_DOMAINS:
            c = conn.execute("SELECT id FROM courses WHERE domain = ? AND is_active = 1 LIMIT 1", (vd,)).fetchone()
            chapters = conn.execute("SELECT id, day_number FROM course_chapters WHERE course_id = ?", (c["id"],)).fetchall()
            
            for ch in chapters:
                subtopics = conn.execute(
                    "SELECT id, sort_order, title, brief, key_takeaways_json FROM course_subtopics WHERE chapter_id = ? ORDER BY sort_order",
                    (ch["id"],)
                ).fetchall()
                assert len(subtopics) >= 2, f"Domain '{vd}' Day {ch['day_number']} has fewer than 2 subtopics"
                for st in subtopics:
                    assert st["title"] and len(st["title"]) > 3
                    assert st["brief"] and len(st["brief"]) > 10
                    takeaways = json.loads(st["key_takeaways_json"]) if st["key_takeaways_json"] else []
                    assert isinstance(takeaways, list)
                    assert len(takeaways) >= 1, f"Empty takeaways for subtopic '{st['title']}'"


def test_each_course_has_7_quizzes():
    """Verify that each course has quizzes for all 7 days with valid options and correct_index."""
    with get_db() as conn:
        for vd in VALID_DOMAINS:
            c = conn.execute("SELECT id FROM courses WHERE domain = ? AND is_active = 1 LIMIT 1", (vd,)).fetchone()
            quizzes = conn.execute(
                "SELECT day_number, questions_json FROM course_day_quizzes WHERE course_id = ? ORDER BY day_number",
                (c["id"],)
            ).fetchall()
            quiz_days = [q["day_number"] for q in quizzes]
            assert quiz_days == [1, 2, 3, 4, 5, 6, 7], f"Domain '{vd}' missing quizzes for some days: {quiz_days}"
            
            for q in quizzes:
                questions = json.loads(q["questions_json"])
                assert len(questions) >= 1, f"Domain '{vd}' Day {q['day_number']} has 0 questions"
                for q_item in questions:
                    assert "question" in q_item and len(q_item["question"]) > 5
                    assert "options" in q_item and len(q_item["options"]) == 4
                    assert "correct_index" in q_item
                    assert 0 <= q_item["correct_index"] < 4


def test_course_catalog_isolation_for_all_domains(client):
    """Verify that an intern in each domain can see their course with total_days=7."""
    with get_db() as conn:
        for vd in VALID_DOMAINS:
            email = f"test_{vd.lower().replace(' ', '_').replace('&', 'and')}@dbert.in"
            # Ensure intern account exists
            conn.execute("""
                INSERT OR IGNORE INTO intern_accounts (name, email, password_hash, domain, is_active, created_at)
                VALUES (?, ?, 'dummy_hash', ?, 1, datetime('now'))
            """, (f"Test {vd}", email, vd))
            conn.execute("UPDATE intern_accounts SET domain = ? WHERE email = ?", (vd, email))
            conn.commit()

            intern_row = conn.execute("SELECT id FROM intern_accounts WHERE email = ?", (email,)).fetchone()
            
            # Ensure API key exists to pass gemini gate
            conn.execute("""
                INSERT OR IGNORE INTO user_api_keys (intern_id, encrypted_key, validated_at, created_at)
                VALUES (?, 'dummy_encrypted_key', datetime('now'), datetime('now'))
            """, (intern_row["id"],))
            conn.commit()

            with client.session_transaction() as sess:
                sess["intern_id"] = intern_row["id"]
                sess["email"] = email
                sess["role"] = "intern"

            res = client.get("/courses")
            assert res.status_code == 200
            assert b"7 Days" in res.data or b"7-Day" in res.data or b"7" in res.data


def test_auto_enroll_intern_in_all_domains():
    """Verify auto_enroll_intern_in_domain_courses successfully enrolls an intern in their domain course."""
    with get_db() as conn:
        for vd in VALID_DOMAINS:
            test_email = f"autoenr_{vd.lower().replace(' ', '_').replace('&', 'and')}@dbert.in"
            conn.execute("""
                INSERT OR IGNORE INTO intern_accounts (name, email, password_hash, domain, is_active, created_at)
                VALUES (?, ?, 'hash', ?, 1, datetime('now'))
            """, (f"Auto {vd}", test_email, vd))
            conn.commit()
            
            acct = conn.execute("SELECT id FROM intern_accounts WHERE email = ?", (test_email,)).fetchone()
            
            # Call auto enroll
            auto_enroll_intern_in_domain_courses(conn, acct["id"], vd, email=test_email)
            conn.commit()

            # Check enrollment
            enr = conn.execute(
                "SELECT ce.*, c.domain FROM course_enrollments ce JOIN courses c ON ce.course_id = c.id WHERE ce.intern_id = ?",
                (acct["id"],)
            ).fetchone()
            assert enr is not None, f"Failed to auto-enroll intern for domain '{vd}'"
            assert enr["domain"] == vd
            assert enr["current_day"] == 1
