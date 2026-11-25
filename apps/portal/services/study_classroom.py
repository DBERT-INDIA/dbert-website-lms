"""Source-grounded classroom, learner-owned trail, and cohort study signals."""

import hashlib
import json
import re
import uuid
from collections import Counter
from datetime import date, datetime, timezone
from html.parser import HTMLParser

from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, url_for


EXPLORED = "explored"
NEEDS_REVIEW = "needs_review"
STOP_WORDS = frozenset("about after again all and are can could did does explain for from have how into is it its like me more my of on or please should than that the their them then there these they this those to use what when where which why will with would you your".split())


def init_study_classroom(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS study_classroom_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_id INTEGER NOT NULL REFERENCES intern_accounts(id) ON DELETE CASCADE,
            course_id INTEGER NOT NULL, lesson_id INTEGER NOT NULL,
            request_id TEXT NOT NULL, question TEXT NOT NULL, answer TEXT NOT NULL, citations_json TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'explored', created_at TEXT NOT NULL, updated_at TEXT NOT NULL, reviewed_at TEXT,
            UNIQUE(intern_id, course_id, request_id)
        );
        CREATE INDEX IF NOT EXISTS idx_study_trail_owner ON study_classroom_entries (intern_id, course_id, id);
        CREATE INDEX IF NOT EXISTS idx_study_review_owner ON study_classroom_entries (intern_id, status, updated_at);
        CREATE TABLE IF NOT EXISTS study_classroom_notes (
            intern_id INTEGER NOT NULL REFERENCES intern_accounts(id) ON DELETE CASCADE,
            course_id INTEGER NOT NULL, lesson_id INTEGER NOT NULL,
            text TEXT NOT NULL, version INTEGER NOT NULL, updated_at TEXT NOT NULL,
            PRIMARY KEY(intern_id, course_id, lesson_id)
        );
        CREATE TABLE IF NOT EXISTS study_classroom_review_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL REFERENCES study_classroom_entries(id) ON DELETE CASCADE,
            attempt_key TEXT NOT NULL, result TEXT NOT NULL, created_at TEXT NOT NULL,
            UNIQUE(entry_id, attempt_key)
        );
        CREATE TABLE IF NOT EXISTS study_classroom_followups (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cohort_id INTEGER NOT NULL REFERENCES program_cohorts(id),
            lesson_id INTEGER NOT NULL, title TEXT NOT NULL, message TEXT NOT NULL,
            due_on TEXT, created_by TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_study_followup_cohort ON study_classroom_followups(cohort_id, id);
    """)
    conn.commit()


def _utcnow():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class _LessonText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.ignored = False

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style"}:
            self.ignored = True
        elif tag in {"p", "li", "div", "br", "h2", "h3", "pre"}:
            self.parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style"}:
            self.ignored = False

    def handle_data(self, data):
        if not self.ignored:
            self.parts.append(data)


def _plain_lesson(value):
    if not re.search(r"</?(?:p|li|div|br|h[1-6]|pre|script|style|span|strong|em)\b", value, re.I):
        return value
    parser = _LessonText()
    parser.feed(value)
    return "".join(parser.parts)


def _lesson_sections(lesson):
    brief = _plain_lesson(lesson["brief"] or "")
    sections = []
    for index, block in enumerate(re.split(r"\n\s*\n", brief)):
        block = block.strip()
        if not block:
            continue
        # Cap each retrieval unit while preserving the section anchor across page loads.
        for offset in range(0, len(block), 1200):
            sections.append({"id": f"material-{index + 1}-{offset // 1200 + 1}",
                             "title": "Lesson material", "text": block[offset:offset + 1200]})
    try:
        takeaways = json.loads(lesson["key_takeaways_json"] or "[]")
    except (ValueError, TypeError):
        takeaways = []
    if isinstance(takeaways, list):
        for index, takeaway in enumerate(takeaways):
            if isinstance(takeaway, str) and takeaway.strip():
                sections.append({"id": f"takeaway-{index + 1}", "title": "Key takeaway",
                                 "text": _plain_lesson(takeaway).strip()[:1200]})
    return sections


def _tokens(text):
    terms = re.findall(r"[^\W_][\w+-]+", text.casefold(), re.UNICODE)
    return [term[:-1] if len(term) > 5 and term.endswith("s") and not term.endswith("ss") else term
            for term in terms if term not in STOP_WORDS]


def retrieve_lesson_sources(question, lessons, active_lesson):
    """Rank actual lesson text and return stable section references."""
    query = set(_tokens(question))
    if not query:
        return []
    candidates = []
    for lesson in lessons:
        title_words = set(_tokens(lesson["title"]))
        for section in _lesson_sections(lesson):
            text_words = Counter(_tokens(section["text"]))
            matched = query.intersection(text_words)
            if not matched:
                continue
            score = 3 * len(matched) + len(query & title_words) + sum(min(text_words[term], 2) for term in matched)
            candidates.append((score, lesson["id"] == active_lesson, lesson, section))
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    citations = []
    for _, _, lesson, section in candidates[:3]:
        citations.append({"lesson_id": lesson["id"], "section_id": section["id"],
                          "title": lesson["title"], "excerpt": section["text"].strip()})
    return citations


def _excerpt_answer(citations):
    if not citations:
        return "I couldn't find this topic in the available course material. Try a term from the lesson or ask your mentor."
    return "The closest explanation in your course is in " + citations[0]["title"] + ":\n\n" + citations[0]["excerpt"]


def _enrollment(conn, intern, course_id):
    return conn.execute(
        """SELECT current_day FROM course_enrollments WHERE course_id = ?
           AND (intern_id = ? OR (email IS NOT NULL AND email <> '' AND LOWER(email) = LOWER(?)))
           ORDER BY current_day DESC, id LIMIT 1""",
        (course_id, intern["id"], intern.get("email") or ""),
    ).fetchone()


def _lessons(conn, course_id):
    return conn.execute(
        """SELECT s.id, s.title, s.brief, s.key_takeaways_json, c.day_number FROM course_subtopics s
           JOIN course_chapters c ON c.id = s.chapter_id WHERE c.course_id = ?
           ORDER BY c.day_number, s.sort_order, s.id""", (course_id,),
    ).fetchall()


def _lesson(conn, course_id, lesson_id):
    return conn.execute(
        """SELECT s.id, s.title, s.brief, s.key_takeaways_json, c.day_number FROM course_subtopics s
           JOIN course_chapters c ON c.id = s.chapter_id WHERE c.course_id = ? AND s.id = ?""", (course_id, lesson_id),
    ).fetchone()


def _owned_entry(conn, intern_id, course_id, entry_id):
    return conn.execute("SELECT * FROM study_classroom_entries WHERE intern_id = ? AND course_id = ? AND id = ?",
                        (intern_id, course_id, entry_id)).fetchone()


def _entry(row):
    return {"id": row["id"], "lesson_id": row["lesson_id"], "question": row["question"], "answer": row["answer"],
            "citations": json.loads(row["citations_json"]), "status": row["status"], "created_at": row["created_at"],
            "practice_url": f"/courses/{row['course_id']}/study/review/{row['id']}"}


def due_study_reviews(conn, intern):
    rows = conn.execute(
        """SELECT q.id, q.course_id, s.title FROM study_classroom_entries q
           JOIN course_subtopics s ON s.id = q.lesson_id
           JOIN course_chapters ch ON ch.id = s.chapter_id AND ch.course_id = q.course_id
           WHERE q.intern_id = ? AND q.status = 'needs_review' AND EXISTS (
               SELECT 1 FROM course_enrollments e WHERE e.course_id=q.course_id AND
               (e.intern_id = ? OR (e.email IS NOT NULL AND e.email <> '' AND LOWER(e.email)=LOWER(?)))
           ) ORDER BY q.updated_at ASC, q.id ASC LIMIT 100""",
        (intern["id"], intern["id"], intern.get("email") or ""),
    ).fetchall()
    return [{"concept_id": f"study:{row['id']}", "concept_name": row["title"], "review_type": "study_trail",
             "review_url": f"/courses/{row['course_id']}/study/review/{row['id']}"} for row in rows]


def _notes(conn, intern_id, course_id, lesson_id):
    row = conn.execute("SELECT text, version FROM study_classroom_notes WHERE intern_id=? AND course_id=? AND lesson_id=?",
                       (intern_id, course_id, lesson_id)).fetchone()
    return dict(row) if row else {"text": "", "version": 0}


def _active_followups(conn, intern_id, course_id, current_day):
    rows = conn.execute(
        """SELECT f.title, f.message, f.due_on, f.lesson_id, ch.day_number,
                  CASE WHEN q.id IS NULL THEN 0 ELSE 1 END AS has_quiz
           FROM study_classroom_followups f JOIN program_cohorts c ON c.id = f.cohort_id
           JOIN course_subtopics s ON s.id = f.lesson_id
           JOIN course_chapters ch ON ch.id = s.chapter_id AND ch.course_id = c.course_id
           LEFT JOIN course_day_quizzes q ON q.course_id = c.course_id AND q.day_number = ch.day_number
           WHERE c.course_id = ? AND EXISTS (
               SELECT 1 FROM program_cohort_memberships m WHERE m.cohort_id=c.id AND m.intern_id=?
               AND m.status IN ('enrolled', 'completed')
           ) ORDER BY f.id DESC LIMIT 20""", (course_id, intern_id),
    ).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["practice_url"] = (f"/courses/{course_id}/quiz/{item['day_number']}"
                                if item["has_quiz"] and item["day_number"] <= current_day else None)
        result.append(item)
    return result


def _review_question(conn, course_id, lesson):
    from services.learning.concept_service import ConceptService
    concept = ConceptService.get_concept_by_subtopic(conn, lesson["id"])
    if not concept:
        return None
    quiz = conn.execute("SELECT questions_json FROM course_day_quizzes WHERE course_id = ? AND day_number = ?",
                        (course_id, lesson["day_number"])).fetchone()
    if not quiz:
        return None
    try:
        questions = json.loads(quiz["questions_json"])
    except (ValueError, TypeError):
        return None
    for question in questions if isinstance(questions, list) else ():
        if not isinstance(question, dict) or question.get("concept_id") != concept.concept_id:
            continue
        options, correct = question.get("options"), question.get("correct_index")
        if (isinstance(question.get("question"), str) and isinstance(options, list) and len(options) >= 2
                and all(isinstance(option, str) for option in options) and type(correct) is int and 0 <= correct < len(options)):
            fingerprint = hashlib.sha256(json.dumps(question, sort_keys=True).encode()).hexdigest()
            return {"text": question["question"], "options": options, "correct": correct, "fingerprint": fingerprint, "concept": concept}
    return None


def _record_review_mastery(conn, intern_id, entry_id, concept, selected, passed):
    from services.learning.evaluator import EvaluationResult
    from services.learning.mastery_policy import MasteryPolicy
    from services.learning.spaced_review import SpacedReviewScheduler
    now = _utcnow()
    conn.execute(
        """INSERT INTO gl_student_learning_profile (student_id, created_at, updated_at) VALUES (?,?,?)
           ON CONFLICT(student_id) DO UPDATE SET student_id=excluded.student_id RETURNING student_id""",
        (intern_id, now, now),
    ).fetchone()
    score = float(passed)
    evaluation = EvaluationResult(
        correctness=score, partial_correctness=False, reasoning_quality=0.0,
        concept_understanding=score, confidence=0.9, evidence_strength=0.7,
        suggested_action="ADVANCE" if passed else "RETEST",
    )
    MasteryPolicy.evaluate_and_update_mastery(
        conn, intern_id, concept, evaluation, f"study-review-{entry_id}", str(selected), commit=False,
    )
    SpacedReviewScheduler.schedule_next_review(conn, intern_id, concept.concept_id,
                                              "REINFORCEMENT" if passed else "REMEDIATION", score, commit=False)
    MasteryPolicy.update_student_profile(conn, intern_id, commit=False)


def study_classroom_blueprint(get_db, current_intern, can_study, require_admin, current_mentor, answer_with_tutor=None, *, now_str=_utcnow):
    bp = Blueprint("study_classroom", __name__)

    def viewer():
        intern = current_intern()
        return intern if intern and intern.get("id", 0) > 0 else None

    def access(conn, intern, course_id):
        return _enrollment(conn, intern, course_id) if intern and can_study(intern) else None

    def denied(intern):
        return jsonify(error="Course enrollment is required." if intern else "Sign in to continue."), (403 if intern else 401)

    @bp.get("/courses/<int:course_id>/study")
    def classroom(course_id):
        intern = viewer()
        if not intern:
            return redirect("/#signin")
        with get_db() as conn:
            enrollment = access(conn, intern, course_id)
            if not enrollment:
                abort(403)
            course = conn.execute("SELECT id, title FROM courses WHERE id=?", (course_id,)).fetchone()
            if not course:
                abort(404)
            lessons = [{key: row[key] for key in ("id", "title", "day_number")} for row in _lessons(conn, course_id)]
        requested = request.args.get("lesson_id", type=int)
        current_day = enrollment["current_day"] or 1
        default_lesson = next((lesson for lesson in lessons if lesson["day_number"] >= current_day),
                              lessons[-1] if lessons else None)
        return render_template("study_classroom.html", study_course=dict(course), study_lessons=lessons,
                               study_active_lesson=requested if any(row["id"] == requested for row in lessons)
                               else default_lesson["id"] if default_lesson else None)

    @bp.get("/api/study-classroom/<int:course_id>/state")
    def state(course_id):
        intern = viewer()
        with get_db() as conn:
            enrollment = access(conn, intern, course_id)
            if not enrollment:
                return denied(intern)
            lesson = _lesson(conn, course_id, request.args.get("lesson_id", type=int))
            if not lesson:
                return jsonify(error="Lesson not found in this course."), 404
            rows = conn.execute("SELECT * FROM study_classroom_entries WHERE intern_id=? AND course_id=? ORDER BY id DESC LIMIT 100",
                                (intern["id"], course_id)).fetchall()
            entry_id = request.args.get("entry_id", type=int)
            if entry_id is not None and all(row["id"] != entry_id for row in rows):
                linked = _owned_entry(conn, intern["id"], course_id, entry_id)
                if linked:
                    rows.append(linked)
            notes = _notes(conn, intern["id"], course_id, lesson["id"])
            followups = _active_followups(conn, intern["id"], course_id, enrollment["current_day"] or 1)
        return jsonify(lesson={key: lesson[key] for key in ("id", "title", "day_number")} | {"sections": _lesson_sections(lesson)},
                       trail=[_entry(row) for row in reversed(rows)], notes=notes, followups=followups)

    @bp.post("/api/study-classroom/<int:course_id>/ask")
    def ask(course_id):
        intern = viewer()
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Enter a course question."), 400
        question = data.get("question")
        key, lesson_id = data.get("request_id"), data.get("lesson_id")
        if (not isinstance(question, str) or not 3 <= len(question.strip()) <= 1200 or type(lesson_id) is not int
                or not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,100}", key)):
            return jsonify(error="Choose a lesson and enter a question of 3 to 1,200 characters."), 400
        question = question.strip()

        def replay(conn):
            return conn.execute("SELECT * FROM study_classroom_entries WHERE intern_id=? AND course_id=? AND request_id=?",
                                (intern["id"], course_id, key)).fetchone()

        def response(row):
            if row["question"] != question or row["lesson_id"] != lesson_id:
                return jsonify(error="This request key already belongs to a different question."), 409
            return jsonify(entry=_entry(row))

        with get_db() as conn:
            if not access(conn, intern, course_id):
                return denied(intern)
            existing = replay(conn)
            if existing:
                return response(existing)
            lessons = _lessons(conn, course_id)
            if not any(lesson["id"] == lesson_id for lesson in lessons):
                return jsonify(error="Lesson not found in this course."), 404

        citations = retrieve_lesson_sources(question, lessons, lesson_id)
        answer = _excerpt_answer(citations)
        if citations and answer_with_tutor:
            try:
                generated = answer_with_tutor(intern["id"], question, citations)
                if isinstance(generated, str) and generated.strip():
                    answer = generated.strip()[:6000]
            except Exception:
                current_app.logger.warning("The classroom tutor was unavailable; served a lesson excerpt.")
        now = now_str()
        with get_db() as conn:
            if not access(conn, intern, course_id):
                return denied(intern)
            conn.execute(
                """INSERT INTO study_classroom_entries(intern_id,course_id,lesson_id,request_id,question,answer,
                   citations_json,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(intern_id,course_id,request_id) DO NOTHING""",
                (intern["id"], course_id, lesson_id, key, question, answer, json.dumps(citations), now, now),
            )
            stored = replay(conn)
            conn.commit()
            return response(stored)

    @bp.patch("/api/study-classroom/<int:course_id>/trail/<int:entry_id>")
    def update_trail(course_id, entry_id):
        intern = viewer()
        data = request.get_json(silent=True)
        status = data.get("status") if isinstance(data, dict) else None
        if status not in (EXPLORED, NEEDS_REVIEW):
            return jsonify(error="Choose Explored or Needs review."), 400
        with get_db() as conn:
            if not access(conn, intern, course_id):
                return denied(intern)
            changed = conn.execute("UPDATE study_classroom_entries SET status=?, updated_at=? WHERE id=? AND intern_id=? AND course_id=?",
                                   (status, now_str(), entry_id, intern["id"], course_id))
            if changed.rowcount != 1:
                return jsonify(error="Study entry not found."), 404
            row = _owned_entry(conn, intern["id"], course_id, entry_id)
            conn.commit()
        return jsonify(entry=_entry(row))

    @bp.put("/api/study-classroom/<int:course_id>/notes/<int:lesson_id>")
    def save_notes(course_id, lesson_id):
        intern = viewer()
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="Enter valid lesson notes."), 400
        text, version = data.get("text"), data.get("version")
        if not isinstance(text, str) or len(text) > 6000 or type(version) is not int or version < 0:
            return jsonify(error="Notes may contain at most 6,000 characters."), 400
        with get_db() as conn:
            if not access(conn, intern, course_id):
                return denied(intern)
            if not _lesson(conn, course_id, lesson_id):
                return jsonify(error="Lesson not found in this course."), 404
            if version == 0:
                cur = conn.execute(
                    """INSERT INTO study_classroom_notes(intern_id,course_id,lesson_id,text,version,updated_at)
                       VALUES(?,?,?,?,1,?) ON CONFLICT(intern_id,course_id,lesson_id) DO NOTHING RETURNING version""",
                    (intern["id"], course_id, lesson_id, text, now_str()),
                )
                # The PostgreSQL adapter consumes RETURNING to populate its insert ID.
                cur.fetchone()
            else:
                cur = conn.execute("""UPDATE study_classroom_notes SET text=?,version=version+1,updated_at=?
                                     WHERE intern_id=? AND course_id=? AND lesson_id=? AND version=?""",
                                   (text, now_str(), intern["id"], course_id, lesson_id, version))
            saved = cur.rowcount == 1
            notes = _notes(conn, intern["id"], course_id, lesson_id)
            conn.commit()
        if not saved:
            return jsonify(error="Notes changed in another tab. Load the current version before saving.", notes=notes), 409
        return jsonify(notes=notes)

    @bp.route("/courses/<int:course_id>/study/review/<int:entry_id>", methods=["GET", "POST"])
    def review(course_id, entry_id):
        intern = viewer()
        if not intern:
            return redirect("/#signin")
        result = None
        with get_db() as conn:
            enrollment = access(conn, intern, course_id)
            if not enrollment:
                abort(403)
            if request.method == "POST":
                conn.execute("UPDATE study_classroom_entries SET updated_at=updated_at WHERE id=? AND intern_id=? AND course_id=?",
                             (entry_id, intern["id"], course_id))
            entry = _owned_entry(conn, intern["id"], course_id, entry_id)
            if not entry:
                abort(404)
            lesson = _lesson(conn, course_id, entry["lesson_id"])
            if not lesson:
                abort(404)
            # Reuse assessment questions only after the learner has passed that day.
            practice = _review_question(conn, course_id, lesson) if lesson["day_number"] < (enrollment["current_day"] or 1) else None
            if request.method == "POST":
                key = request.form.get("attempt_key", "")
                if not re.fullmatch(r"[0-9a-f]{32}", key):
                    abort(400)
                prior = conn.execute("SELECT result FROM study_classroom_review_attempts WHERE entry_id=? AND attempt_key=?",
                                     (entry_id, key)).fetchone()
                if prior:
                    result = prior["result"]
                elif entry["status"] != NEEDS_REVIEW:
                    result = "already-reviewed"
                else:
                    result = "read"
                    if practice:
                        selected = request.form.get("option", type=int)
                        if request.form.get("fingerprint") != practice["fingerprint"] or selected is None or not 0 <= selected < len(practice["options"]):
                            abort(409, "This practice question changed. Reload and try again.")
                        passed = selected == practice["correct"]
                        _record_review_mastery(conn, intern["id"], entry_id, practice["concept"], selected, passed)
                        result = "correct" if passed else "incorrect"
                    elif request.form.get("fingerprint"):
                        abort(409, "This practice question changed. Reload and try again.")
                    now = now_str()
                    conn.execute("INSERT INTO study_classroom_review_attempts(entry_id,attempt_key,result,created_at) VALUES(?,?,?,?)",
                                 (entry_id, key, result, now))
                    if result in {"read", "correct"}:
                        conn.execute("UPDATE study_classroom_entries SET status=?,updated_at=?,reviewed_at=? WHERE id=?",
                                     (EXPLORED, now, now, entry_id))
                        entry = _owned_entry(conn, intern["id"], course_id, entry_id)
                conn.commit()
        visible_question = {key: practice[key] for key in ("text", "options", "fingerprint")} if practice else None
        return render_template("study_classroom_review.html", course_id=course_id, entry=_entry(entry),
                               course_lesson=dict(lesson), practice=visible_question, attempt_key=uuid.uuid4().hex,
                               result=result)

    @bp.route("/program-cohorts/<int:cohort_id>/study", methods=["GET", "POST"])
    def cohort_study(cohort_id):
        admin = require_admin()
        mentor = current_mentor() if not admin else None
        if not admin and not mentor:
            abort(403)
        with get_db() as conn:
            if request.method == "POST":
                conn.execute("UPDATE program_cohorts SET updated_at=updated_at WHERE id=?", (cohort_id,))
            cohort = conn.execute("SELECT * FROM program_cohorts WHERE id=?", (cohort_id,)).fetchone()
            if not cohort:
                abort(404)
            if not admin and cohort["mentor_id"] != mentor["id"]:
                abort(403)
            lessons = _lessons(conn, cohort["course_id"])
            if request.method == "POST":
                lesson_id = request.form.get("lesson_id", type=int)
                title = request.form.get("title", "").strip()
                message = request.form.get("message", "").strip()
                due = request.form.get("due_on", "").strip()
                try:
                    due = date.fromisoformat(due).isoformat() if due else None
                except ValueError:
                    abort(400, "Enter a valid follow-up date.")
                if not any(row["id"] == lesson_id for row in lessons) or not 3 <= len(title) <= 150 or not 5 <= len(message) <= 2000:
                    abort(400, "Choose a course lesson and enter a title and instructions.")
                actor = f"admin:{admin['id']}" if admin else f"mentor:{mentor['id']}"
                conn.execute("""INSERT INTO study_classroom_followups(cohort_id,lesson_id,title,message,due_on,created_by,created_at)
                               VALUES(?,?,?,?,?,?,?)""", (cohort_id, lesson_id, title, message, due, actor, now_str()))
                conn.commit()
                return redirect(url_for("study_classroom.cohort_study", cohort_id=cohort_id, saved=1))

            signals = conn.execute(
                """SELECT s.title, ch.day_number, COUNT(DISTINCT q.intern_id) AS asking,
                          COUNT(DISTINCT CASE WHEN q.status='needs_review' THEN q.intern_id END) AS reviewing,
                          COUNT(DISTINCT CASE WHEN q.reviewed_at IS NOT NULL THEN q.intern_id END) AS reviewed
                   FROM study_classroom_entries q JOIN course_subtopics s ON s.id=q.lesson_id
                   JOIN course_chapters ch ON ch.id=s.chapter_id AND ch.course_id=q.course_id
                   JOIN program_cohort_memberships m ON m.intern_id=q.intern_id AND m.cohort_id=?
                   WHERE q.course_id=? AND m.status IN ('enrolled','completed')
                     AND SUBSTR(q.created_at,1,10)>=? AND SUBSTR(q.created_at,1,10)<=?
                     AND (m.enrolled_at IS NULL OR REPLACE(SUBSTR(q.created_at,1,19),'T',' ')
                                                   >= REPLACE(SUBSTR(m.enrolled_at,1,19),'T',' '))
                   GROUP BY s.id, s.title, ch.day_number HAVING COUNT(DISTINCT q.intern_id)>=2
                   ORDER BY reviewing DESC, asking DESC, ch.day_number""",
                (cohort_id, cohort["course_id"], cohort["starts_on"], cohort["ends_on"]),
            ).fetchall()
            followups = conn.execute(
                """SELECT f.title,f.message,f.due_on,s.title AS lesson_title FROM study_classroom_followups f
                   JOIN course_subtopics s ON s.id=f.lesson_id WHERE f.cohort_id=? ORDER BY f.id DESC LIMIT 30""",
                (cohort_id,),
            ).fetchall()
        return render_template("cohort_study_insights.html", cohort=dict(cohort), lessons=lessons,
                               signals=signals, followups=followups)

    @bp.after_request
    def private(response):
        response.headers["Cache-Control"] = "private, no-store"
        return response

    return bp
