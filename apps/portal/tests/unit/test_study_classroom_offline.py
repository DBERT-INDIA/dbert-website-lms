"""Offline integration coverage for the study classroom Blueprint."""

import json
import re
from contextlib import contextmanager
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit

import pytest
from flask import Flask, session

from services import study_classroom
from services.database.adapter import SQLiteAdapter
from services.learning.concept_service import ConceptService
from services.learning.learning_models import Concept, init_learning_tables
from services.program_cohorts import init_program_cohorts


PORTAL = Path(__file__).resolve().parents[2]
API = "/api/study-classroom/7"
CLASSROOM = "/courses/7/study"
INSIGHTS = "/program-cohorts/40/study"
QUESTION = "How do grouping buckets count rows?"
QUIZ = "What does grouping return for each key?"
QUESTION_TIME = "2026-05-18T09:30:00+00:00"


@pytest.fixture
def study(tmp_path):
    db_path = tmp_path / "study.db"

    @contextmanager
    def db():
        conn = SQLiteAdapter(str(db_path))
        try:
            with conn:
                yield conn
        finally:
            conn.close()

    with db() as conn:
        conn.executescript("""
            CREATE TABLE intern_accounts (id INTEGER PRIMARY KEY, email TEXT NOT NULL);
            CREATE TABLE mentors (id INTEGER PRIMARY KEY);
            CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT NOT NULL);
            CREATE TABLE course_enrollments (
                id INTEGER PRIMARY KEY, course_id INTEGER NOT NULL, intern_id INTEGER, email TEXT, current_day INTEGER
            );
            CREATE TABLE course_chapters (id INTEGER PRIMARY KEY, course_id INTEGER NOT NULL, day_number INTEGER NOT NULL);
            CREATE TABLE course_subtopics (
                id INTEGER PRIMARY KEY, chapter_id INTEGER NOT NULL, sort_order INTEGER NOT NULL,
                title TEXT NOT NULL, brief TEXT NOT NULL, key_takeaways_json TEXT DEFAULT '[]'
            );
            CREATE TABLE course_day_quizzes (
                id INTEGER PRIMARY KEY, course_id INTEGER NOT NULL, day_number INTEGER NOT NULL, questions_json TEXT NOT NULL
            );
            INSERT INTO intern_accounts VALUES (1, 'one@example.test'), (2, 'two@example.test'), (3, 'three@example.test');
            INSERT INTO mentors VALUES (4), (5);
            INSERT INTO courses VALUES (7, 'Record processing'), (8, 'Astronomy practice');
            INSERT INTO course_enrollments VALUES (1, 7, 1, NULL, 2), (2, 7, 2, NULL, 1),
                                                  (3, 7, 3, NULL, 2), (4, 8, 1, NULL, 1);
            INSERT INTO course_chapters VALUES (71, 7, 1), (72, 7, 2), (81, 8, 1);
            INSERT INTO course_subtopics (id, chapter_id, sort_order, title, brief) VALUES
                (11, 71, 1, 'Grouping records',
                 '<p>Grouping puts rows in buckets by key.</p><p>Count rows within each bucket.</p>'
                 || '<script>contenthiddenfromclassroom</script>'),
                (12, 72, 1, 'Checking records', 'Check rows against a schema before exporting the data.'),
                (99, 81, 1, 'Supernova observation', 'Supernova light curves describe changing stellar brightness.');
        """)
        init_program_cohorts(conn)
        init_learning_tables(conn)
        study_classroom.init_study_classroom(conn)
        conn.execute("""
            INSERT INTO program_cohorts
                (id,course_id,title,starts_on,ends_on,capacity,mentor_id,status,created_at,updated_at)
            VALUES (40,7,'Spring cohort','2026-05-01','2026-07-31',12,4,'open',?,?)
        """, (QUESTION_TIME, QUESTION_TIME))
        conn.executemany("""
            INSERT INTO program_cohort_memberships
               (cohort_id,intern_id,status,requested_at,enrolled_at,updated_at)
            VALUES (40,?,'enrolled',?,?,?)
        """, ((intern_id, joined, joined, joined) for intern_id, joined in (
            (1, "2026-05-01"), (2, "2026-05-10"),
        )))
        ConceptService.register_concept(conn, Concept(
            concept_id="record-grouping", name="Grouping records",
            description="Group valid rows by key.", domain="Data", subject="Records", subtopic_id=11,
        ))
        quizzes = [
            {"question": QUIZ, "concept_id": "record-grouping",
             "options": ["One record per row", "One record per key"], "correct_index": 1},
        ]
        conn.execute("INSERT INTO course_day_quizzes VALUES (1, 7, 1, ?)", (json.dumps(quizzes),))
        conn.commit()

    app = Flask(__name__, template_folder=str(PORTAL / "templates"))
    app.config.update(TESTING=True, SECRET_KEY="local-synthetic-study-tests")
    app.jinja_env.globals.update(csrf_token=lambda: "synthetic-csrf", csrf_field=lambda: "", csp_nonce=lambda: "test")
    tutor_calls = []
    identities = {
        "learner": {"id": 1, "role": "intern", "email": "one@example.test"},
        "peer": {"id": 2, "role": "intern", "email": "two@example.test"},
        "outside": {"id": 3, "role": "intern", "email": "three@example.test"},
        "mentor": {"id": 4, "role": "mentor"},
        "other-mentor": {"id": 5, "role": "mentor"},
        "admin": {"id": 6, "role": "admin"},
    }

    def actor(role):
        identity = identities.get(session.get("synthetic_identity"))
        return identity if identity and identity["role"] == role else None

    def tutor(intern_id, question, citations):
        tutor_calls.append((intern_id, question, citations))
        return None  # Use the service's real source-grounded fallback.

    app.register_blueprint(study_classroom.study_classroom_blueprint(
        db, lambda: actor("intern"), lambda intern: True, lambda: actor("admin"), lambda: actor("mentor"), tutor,
        now_str=lambda: QUESTION_TIME,
    ))

    def client(person=None):
        browser = app.test_client()
        if person:
            with browser.session_transaction() as stored:
                stored["synthetic_identity"] = person
        return browser

    return SimpleNamespace(db=db, client=client, tutor_calls=tutor_calls)


def ask(client, key, question=QUESTION, lesson=11, api=API):
    return client.post(api + "/ask", json={"lesson_id": lesson, "question": question, "request_id": key})


def mark_for_review(client, entry_id):
    response = client.patch(f"{API}/trail/{entry_id}", json={"status": "needs_review"})
    assert response.status_code == 200
    return response.json["entry"]


class ReviewPage(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.hidden = {}
        self.links = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and attrs.get("type") == "hidden":
            self.hidden[attrs["name"]] = attrs["value"]
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])


def test_enrollment_ownership_and_lesson_boundaries(study):
    signed_out = study.client()
    redirect = signed_out.get(CLASSROOM)
    assert redirect.status_code == 302
    assert redirect.location == "/#signin"
    assert signed_out.get(API + "/state?lesson_id=11").status_code == 401
    assert ask(signed_out, "anonymous-key").status_code == 401

    learner = study.client("learner")
    peer = study.client("peer")
    launched = learner.get(CLASSROOM)
    assert launched.status_code == 200
    assert 'data-lesson-id="12"' in launched.get_data(as_text=True)
    assert learner.get(API + "/state?lesson_id=99").status_code == 404
    assert ask(learner, "outside-lesson-key", lesson=99).status_code == 404
    assert peer.get("/api/study-classroom/8/state?lesson_id=99").status_code == 403

    created = ask(learner, "owner-study-key")
    assert created.status_code == 200
    entry_id = created.json["entry"]["id"]
    assert peer.get(API + "/state?lesson_id=11").json["trail"] == []
    assert peer.patch(f"{API}/trail/{entry_id}", json={"status": "needs_review"}).status_code == 404
    assert peer.get(f"{CLASSROOM}/review/{entry_id}").status_code == 404
    assert learner.get(f"/courses/8/study/review/{entry_id}").status_code == 404
    assert learner.get("/api/study-classroom/8/state?lesson_id=99").json["trail"] == []
    assert learner.get(API + "/state?lesson_id=11").headers["Cache-Control"] == "private, no-store"


def test_sources_reject_unrelated_material_and_requests_replay(study):
    learner = study.client("learner")
    response = ask(learner, "repeat-study-key")
    assert response.status_code == 200
    entry = response.json["entry"]
    assert entry["citations"]
    assert "Grouping records" in entry["answer"]
    for source in entry["citations"]:
        lesson = learner.get(f'{API}/state?lesson_id={source["lesson_id"]}').json["lesson"]
        exact = next(section for section in lesson["sections"] if section["id"] == source["section_id"])
        assert source["excerpt"] == exact["text"]
        assert "contenthiddenfromclassroom" not in exact["text"]
        assert source["lesson_id"] != 99

    assert ask(learner, "repeat-study-key").json["entry"] == entry
    assert ask(learner, "repeat-study-key", "Is this a different question?").status_code == 409
    assert len(study.tutor_calls) == 1

    unsupported = ask(learner, "no-source-key", "What are supernova light curves?")
    assert unsupported.status_code == 200
    assert unsupported.json["entry"]["citations"] == []
    assert "available course material" in unsupported.json["entry"]["answer"]
    assert len(study.tutor_calls) == 1
    assert [item["id"] for item in learner.get(API + "/state?lesson_id=11").json["trail"]] == [
        entry["id"], unsupported.json["entry"]["id"],
    ]

    with study.db() as conn:
        text = "Consider the sample records. " * 27 + "Deduplication removes repeated records."
        conn.execute("UPDATE course_subtopics SET brief=? WHERE id=11", (text,))
        conn.commit()
    long_source = ask(learner, "long-source-key", "How does deduplication work?").json["entry"]
    assert "Deduplication removes repeated records." in long_source["citations"][0]["excerpt"]
    assert "Deduplication removes repeated records." in long_source["answer"]


def test_lesson_notes_are_private_and_reject_stale_versions(study):
    learner = study.client("learner")
    peer = study.client("peer")
    first = learner.put(API + "/notes/11", json={"text": "My grouping notes", "version": 0})
    assert first.status_code == 200
    assert first.json["notes"] == {"text": "My grouping notes", "version": 1}

    stale = learner.put(API + "/notes/11", json={"text": "A stale draft", "version": 0})
    assert stale.status_code == 409
    assert stale.json["notes"] == first.json["notes"]
    fresh = learner.put(API + "/notes/11", json={"text": "Updated notes", "version": 1})
    assert fresh.status_code == 200
    assert fresh.json["notes"] == {"text": "Updated notes", "version": 2}
    stale_update = learner.put(API + "/notes/11", json={"text": "Another stale draft", "version": 1})
    assert stale_update.status_code == 409
    assert stale_update.json["notes"] == fresh.json["notes"]
    assert learner.get(API + "/state?lesson_id=11").json["notes"] == fresh.json["notes"]
    assert learner.get(API + "/state?lesson_id=12").json["notes"] == {"text": "", "version": 0}
    assert peer.get(API + "/state?lesson_id=11").json["notes"] == {"text": "", "version": 0}
    assert learner.put(API + "/notes/99", json={"text": "Wrong course", "version": 0}).status_code == 404


def test_an_older_question_opens_only_for_its_owner(study):
    learner = study.client("learner")
    older = ask(learner, "older-study-question").json["entry"]
    with study.db() as conn:
        conn.executemany("""
            INSERT INTO study_classroom_entries (
                intern_id, course_id, lesson_id, request_id, question, answer,
                citations_json, created_at, updated_at
            ) VALUES (1, 7, 11, ?, 'Newer question', 'Synthetic answer', '[]', ?, ?)
        """, ((f"newer-question-{index}", QUESTION_TIME, QUESTION_TIME) for index in range(100)))
        conn.commit()

    latest = learner.get(API + "/state?lesson_id=11").json["trail"]
    assert len(latest) == 100
    assert older not in latest
    query = f"/state?lesson_id=11&entry_id={older['id']}"
    assert older in learner.get(API + query).json["trail"]
    peer = study.client("peer").get(API + query)
    assert peer.status_code == 200
    assert peer.json["trail"] == []


def test_review_reuses_passed_quizzes_and_deduplicates_attempts(study):
    learner = study.client("learner")
    peer = study.client("peer")
    entry = mark_for_review(learner, ask(learner, "practice-study-key").json["entry"]["id"])
    review_url = entry["practice_url"]
    with study.db() as conn:
        due = study_classroom.due_study_reviews(conn, {"id": 1, "email": "one@example.test"})
        assert [item["review_url"] for item in due] == [review_url]

    practice = learner.get(review_url)
    assert practice.status_code == 200
    html = practice.get_data(as_text=True)
    form = ReviewPage(html)
    assert QUIZ in html
    assert "One record per key" in html
    assert "correct_index" not in html
    citation = entry["citations"][0]
    assert any(
        parse_qs(urlsplit(link).query) == {
            "lesson_id": [str(citation["lesson_id"])], "section_id": [str(citation["section_id"])],
        } for link in form.links
    )

    wrong = {**form.hidden, "option": "0"}
    assert learner.post(review_url, data={**wrong, "fingerprint": "stale-question"}).status_code == 409
    assert "Try again" in learner.post(review_url, data=wrong).get_data(as_text=True)
    # A changed selection using the same attempt key remains the original result.
    assert "Try again" in learner.post(review_url, data={**wrong, "option": "1"}).get_data(as_text=True)
    attempted = learner.get(API + "/state?lesson_id=11").json["trail"][0]
    assert attempted["status"] == "needs_review"

    current = ReviewPage(learner.get(review_url).get_data(as_text=True))
    correct = learner.post(review_url, data={**current.hidden, "option": "1"})
    assert "Correct. Your Study Trail is updated." in correct.get_data(as_text=True)
    with study.db() as conn:
        assert study_classroom.due_study_reviews(conn, {"id": 1, "email": "one@example.test"}) == []
        outcomes = conn.execute("SELECT result FROM study_classroom_review_attempts ORDER BY id").fetchall()
        assert [row["result"] for row in outcomes] == ["incorrect", "correct"]
        mastery = conn.execute(
            "SELECT total_attempts, successful_attempts, review_count FROM gl_student_mastery WHERE student_id=1 "
            "AND concept_id='record-grouping'"
        ).fetchone()
        assert dict(mastery) == {"total_attempts": 2, "successful_attempts": 1, "review_count": 2}

    peer_entry = mark_for_review(peer, ask(peer, "locked-review-key").json["entry"]["id"])
    preview = peer.get(peer_entry["practice_url"]).get_data(as_text=True)
    assert "Reading review" in preview
    assert QUIZ not in preview


def test_cohort_insights_and_followups_respect_membership(study):
    learner = study.client("learner")
    peer = study.client("peer")
    outsider = study.client("outside")
    mentor = study.client("mentor")
    admin = study.client("admin")
    unassigned = study.client("other-mentor")
    assert learner.get(INSIGHTS).status_code == 403
    assert unassigned.get(INSIGHTS).status_code == 403

    first = ask(learner, "cohort-first-ask")
    mark_for_review(learner, first.json["entry"]["id"])
    assert "There is no shared lesson activity" in mentor.get(INSIGHTS).get_data(as_text=True)
    ask(peer, "cohort-peer-ask", "Can you explain grouping buckets?")
    ask(outsider, "outside-ask-key", "What are grouping buckets for?")
    ask(learner, "other-cohort-lesson", "How do schema checks work?", lesson=12)
    ask(peer, "old-cohort-lesson", "When should I check an export schema?", lesson=12)
    with study.db() as conn:
        conn.execute("UPDATE study_classroom_entries SET created_at='2026-05-10 08:00:00' WHERE request_id='old-cohort-lesson'")
        conn.execute("UPDATE program_cohort_memberships SET enrolled_at='2026-05-10T09:00:00' WHERE intern_id=2")
        conn.commit()

    insights = admin.get(INSIGHTS)
    assert insights.status_code == 200
    html = insights.get_data(as_text=True)
    assert re.search(r"Grouping records</th>\s*<td>2</td>\s*<td>1</td>\s*<td>0</td>", html)
    assert "Checking records</th>" not in html
    assert QUESTION not in html
    assert "one@example.test" not in html

    followup = {"title": "Practice grouped records", "message": "Review keys, then practice the quiz.",
                "lesson_id": 11, "due_on": "2026-05-28"}
    assert unassigned.post(INSIGHTS, data=followup).status_code == 403
    assert mentor.post(INSIGHTS, data={**followup, "lesson_id": 99}).status_code == 400
    assert mentor.post(INSIGHTS, data={**followup, "due_on": "not-a-date"}).status_code == 400
    saved = mentor.post(INSIGHTS, data=followup, follow_redirects=True)
    assert saved.status_code == 200
    assert followup["title"] in saved.get_data(as_text=True)
    for member in (learner, peer):
        assigned = member.get(API + "/state?lesson_id=11").json["followups"]
        assert len(assigned) == 1
        assert assigned[0]["title"] == followup["title"]
        assert assigned[0]["due_on"] == followup["due_on"]
        assert assigned[0]["practice_url"] == "/courses/7/quiz/1"
    assert outsider.get(API + "/state?lesson_id=11").json["followups"] == []

    reading = {**followup, "title": "Revisit schema checks", "lesson_id": 12}
    assert mentor.post(INSIGHTS, data=reading).status_code == 302
    assigned = peer.get(API + "/state?lesson_id=12").json["followups"]
    assert assigned[0]["title"] == reading["title"]
    assert assigned[0]["practice_url"] is None
