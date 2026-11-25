"""Milestone evidence and credential issuance for DBERT program cohorts."""

from datetime import date
import json
from uuid import uuid4

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for


MILESTONE_KINDS = {
    "quiz": "Distinct quizzes passed",
    "project": "Projects approved",
    "question": "Distinct lessons discussed",
    "course": "Course completed",
}

# Evidence belongs to the cohort's course and the learner's active membership.
# A roster query can evaluate every learner without reading any question or submission text.
_EVIDENCE = {
    "quiz": (
        "DISTINCT quiz.id",
        """JOIN day_quiz_attempts attempt ON attempt.enrollment_id = e.id
           JOIN course_day_quizzes quiz ON quiz.id = attempt.day_quiz_id
           WHERE quiz.course_id = e.course_id AND attempt.passed = 1""",
        "attempt.created_at",
    ),
    "project": (
        "DISTINCT project.id",
        """JOIN project_submissions project ON project.enrollment_id = e.id
           WHERE project.intern_id = m.intern_id AND project.course_id = e.course_id
             AND project.status = 'approved'""",
        "project.created_at",
    ),
    "question": (
        "DISTINCT lesson.id",
        """JOIN study_classroom_entries question
                ON question.intern_id = m.intern_id AND question.course_id = e.course_id
           JOIN course_subtopics lesson ON lesson.id = question.lesson_id
           JOIN course_chapters chapter ON chapter.id = lesson.chapter_id
           WHERE chapter.course_id = e.course_id""",
        "question.created_at",
    ),
    "course": (
        "DISTINCT e.course_id",
        """JOIN courses course ON course.id = e.course_id
           WHERE e.completed_at IS NOT NULL
             AND (
                 COALESCE(course.requires_project, 0) = 0 OR EXISTS (
                     SELECT 1 FROM project_submissions capstone
                     WHERE capstone.intern_id = m.intern_id AND capstone.course_id = e.course_id
                       AND capstone.status = 'approved'
                 )
             )""",
        None,
    ),
}


def init_cohort_progress_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS program_cohort_milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cohort_id INTEGER NOT NULL REFERENCES program_cohorts(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            kind TEXT NOT NULL CHECK(kind IN ('quiz', 'project', 'question', 'course')),
            threshold INTEGER NOT NULL CHECK(threshold > 0),
            due_on TEXT,
            required INTEGER NOT NULL CHECK(required IN (0, 1)),
            created_at TEXT NOT NULL,
            created_by TEXT NOT NULL,
            archived_at TEXT,
            archived_by TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_program_milestones_cohort
            ON program_cohort_milestones(cohort_id, archived_at);
        CREATE TABLE IF NOT EXISTS program_cohort_credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            membership_id INTEGER NOT NULL UNIQUE REFERENCES program_cohort_memberships(id) ON DELETE CASCADE,
            cert_id TEXT NOT NULL UNIQUE,
            issued_at TEXT NOT NULL,
            issued_by_type TEXT NOT NULL CHECK(issued_by_type IN ('intern', 'admin')),
            issued_by TEXT NOT NULL,
            evidence_json TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS program_cohort_checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            membership_id INTEGER NOT NULL REFERENCES program_cohort_memberships(id) ON DELETE CASCADE,
            actor_type TEXT NOT NULL CHECK(actor_type IN ('mentor', 'admin')),
            actor_id TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_program_checkins_membership
            ON program_cohort_checkins(membership_id, id);
    """)
    conn.ensure_column("program_cohorts", "milestones_locked_at", "TEXT")
    conn.execute("""
        UPDATE program_cohorts
        SET milestones_locked_at = graduates.first_issued_at
        FROM (
            SELECT m.cohort_id, MIN(c.issued_at) AS first_issued_at
            FROM program_cohort_credentials c
            JOIN program_cohort_memberships m ON m.id = c.membership_id
            GROUP BY m.cohort_id
        ) AS graduates
        WHERE program_cohorts.id = graduates.cohort_id
          AND program_cohorts.milestones_locked_at IS NULL
    """)
    conn.commit()


def _cohort(conn, cohort_id, lock=False):
    if lock:
        # Match the roster mutation lock so graduation cannot race a withdrawal.
        conn.execute(
            "UPDATE program_cohorts SET updated_at = updated_at WHERE id = ?", (cohort_id,)
        )
    row = conn.execute("SELECT * FROM program_cohorts WHERE id = ?", (cohort_id,)).fetchone()
    if row is None:
        abort(404)
    return dict(row)


def _members(conn, cohort_id, *, intern_id=None, membership_id=None):
    query = """
        SELECT m.id, m.intern_id, m.status, m.enrolled_at, a.name, a.email,
               credential.cert_id, credential.issued_at, wallet.credential_status
        FROM program_cohort_memberships m
        JOIN intern_accounts a ON a.id = m.intern_id
        LEFT JOIN program_cohort_credentials credential ON credential.membership_id = m.id
        LEFT JOIN intern_certificates wallet
               ON wallet.intern_id = m.intern_id AND wallet.cert_id = credential.cert_id
        WHERE m.cohort_id = ? AND m.status IN ('enrolled', 'completed')
    """
    params = [cohort_id]
    if intern_id is not None:
        query += " AND m.intern_id = ?"
        params.append(intern_id)
    if membership_id is not None:
        query += " AND m.id = ?"
        params.append(membership_id)
    return [
        dict(row)
        for row in conn.execute(query + " ORDER BY a.name, m.id", tuple(params)).fetchall()
    ]


def _milestones(conn, cohort_id):
    rows = conn.execute(
        """SELECT id, title, kind, threshold, required, due_on
           FROM program_cohort_milestones
           WHERE cohort_id = ? AND archived_at IS NULL
           ORDER BY CASE WHEN due_on IS NULL THEN 1 ELSE 0 END, due_on, id""",
        (cohort_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def _progress(conn, cohort, members, milestones, today):
    if not members:
        return

    evidence = {}
    for kind in {milestone["kind"] for milestone in milestones}:
        selection, joins, time_field = _EVIDENCE[kind]
        # SQL fragments come from the fixed evidence definitions above.
        query = f"""
            SELECT m.id, COUNT({selection}) AS evidence_count
            FROM program_cohort_memberships m
            JOIN intern_accounts a ON a.id = m.intern_id
            JOIN course_enrollments e ON e.course_id = ?
                AND (e.intern_id = m.intern_id OR LOWER(e.email) = LOWER(a.email))
            {joins}
            AND m.cohort_id = ? AND m.status = 'enrolled'
        """
        params = [cohort["course_id"], cohort["id"]]
        if time_field:
            query += f"""
                AND SUBSTR(CAST({time_field} AS TEXT), 1, 10) >= ?
                AND SUBSTR(CAST({time_field} AS TEXT), 1, 10) >= SUBSTR(m.enrolled_at, 1, 10)
            """
            params.append(cohort["starts_on"])
        if len(members) == 1:
            query += " AND m.id = ?"
            params.append(members[0]["id"])
        rows = conn.execute(query + " GROUP BY m.id", tuple(params)).fetchall()
        evidence[kind] = {row["id"]: row["evidence_count"] for row in rows}

    snapshots = {}
    if any(member["cert_id"] for member in members):
        query = """
            SELECT receipt.membership_id, receipt.evidence_json
            FROM program_cohort_credentials receipt
            JOIN program_cohort_memberships m ON m.id = receipt.membership_id
            WHERE m.cohort_id = ?
        """
        params = [cohort["id"]]
        if len(members) == 1:
            query += " AND m.id = ?"
            params.append(members[0]["id"])
        snapshots = {
            row["membership_id"]: json.loads(row["evidence_json"])
            for row in conn.execute(query, tuple(params)).fetchall()
        }

    for member in members:
        states = snapshots.get(member["id"])
        if states is None:
            states = []
            for milestone in milestones:
                count = evidence[milestone["kind"]].get(member["id"], 0)
                met = count >= milestone["threshold"]
                states.append({
                    **milestone,
                    "count": count,
                    "met": met,
                    "overdue": bool(not met and milestone["due_on"] and milestone["due_on"] < today),
                })
        required_total = sum(bool(state["required"]) for state in states)
        required_met = sum(bool(state["required"] and state["met"]) for state in states)
        member["milestones"] = states
        member["required_total"] = required_total
        member["required_met"] = required_met
        member["eligible"] = bool(
            member["status"] == "enrolled" and required_total and required_met == required_total
        )


def _goal(conn, cohort, actor_id, stamp, form):
    if cohort["milestones_locked_at"]:
        raise ValueError("Milestones are locked after the first cohort credential is issued.")

    title = form.get("title", "").strip()
    kind = form.get("kind", "")
    due_on = form.get("due_on", "").strip() or None
    try:
        threshold = int(form.get("threshold", ""))
    except ValueError:
        raise ValueError("Enter a whole-number target.") from None
    if not title or len(title) > 120:
        raise ValueError("Enter a milestone title of up to 120 characters.")
    if kind not in MILESTONE_KINDS:
        raise ValueError("Choose a supported evidence type.")
    if not 1 <= threshold <= 100 or (kind == "course" and threshold != 1):
        raise ValueError("Use a target from 1 to 100. Course completion has a target of 1.")
    if due_on:
        try:
            due_on = date.fromisoformat(due_on).isoformat()
        except ValueError:
            raise ValueError("Enter a valid due date.") from None
        if not cohort["starts_on"] <= due_on <= cohort["ends_on"]:
            raise ValueError("Choose a due date within the cohort schedule.")
    required = int(form.get("required") == "1")
    if len(_milestones(conn, cohort["id"])) >= 20:
        raise ValueError("A cohort can have up to 20 active milestones.")
    conn.execute(
        """INSERT INTO program_cohort_milestones
           (cohort_id, title, kind, threshold, due_on, required, created_at, created_by)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (cohort["id"], title, kind, threshold, due_on, required, stamp, actor_id),
    )
    conn.execute(
        """UPDATE program_cohorts SET schedule_locked_at = COALESCE(schedule_locked_at, ?)
           WHERE id = ?""",
        (stamp, cohort["id"]),
    )


def _archive_goal(conn, cohort, actor_id, stamp, milestone_id):
    if cohort["milestones_locked_at"]:
        raise ValueError("Milestones are locked after the first cohort credential is issued.")
    changed = conn.execute(
        """UPDATE program_cohort_milestones SET archived_at = ?, archived_by = ?
           WHERE id = ? AND cohort_id = ? AND archived_at IS NULL""",
        (stamp, actor_id, milestone_id, cohort["id"]),
    ).rowcount
    if not changed:
        abort(404)


def _issue_credential(conn, cohort, member, actor_type, actor_id, stamp):
    if member["cert_id"]:
        return "This cohort credential has already been issued."
    _progress(conn, cohort, [member], _milestones(conn, cohort["id"]), stamp[:10])
    if not member["eligible"]:
        raise ValueError("Complete the required milestones before issuing a credential.")

    cert_id = f"DBERT-COHORT-{uuid4().hex.upper()}"
    title = f"{cohort['title']} · Cohort Completion"
    # The receipt keeps the course association. A wallet course_id represents an ordinary course credential.
    conn.execute(
        """INSERT INTO intern_certificates
           (intern_id, email, course_title, cert_id, issued_at, url, received_at, tier)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            member["intern_id"], member["email"], title, cert_id,
            stamp, f"/portal/certificate/{cert_id}", stamp, "program_cohort_completion",
        ),
    )
    conn.execute(
        """INSERT INTO program_cohort_credentials
           (membership_id, cert_id, issued_at, issued_by_type, issued_by, evidence_json)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (member["id"], cert_id, stamp, actor_type, actor_id, json.dumps(member["milestones"])),
    )
    conn.execute(
        """UPDATE program_cohort_memberships SET status = 'completed', updated_at = ?
           WHERE id = ? AND status = 'enrolled'""",
        (stamp, member["id"]),
    )
    conn.execute(
        "UPDATE program_cohorts SET milestones_locked_at = COALESCE(milestones_locked_at, ?) WHERE id = ?",
        (stamp, cohort["id"]),
    )
    return "Cohort credential issued."


def _staff_actor(cohort, admin, mentor):
    if admin:
        return "admin", str(admin["id"])
    if mentor and mentor["id"] == cohort["mentor_id"]:
        return "mentor", str(mentor["id"])
    abort(404)


def _checkins(conn, membership_id):
    return conn.execute(
        """SELECT actor_type, message, created_at
           FROM program_cohort_checkins WHERE membership_id = ?
           ORDER BY id DESC LIMIT 20""",
        (membership_id,),
    ).fetchall()


def cohort_progress_blueprint(get_db, current_intern, require_admin, current_mentor, now_str):
    bp = Blueprint("cohort_progress", __name__)

    @bp.after_request
    def private(response):
        response.headers["Cache-Control"] = "private, no-store"
        return response

    @bp.route("/program-cohorts/<int:cohort_id>/progress", methods=["GET", "POST"])
    def learner(cohort_id):
        intern = current_intern()
        if not intern:
            abort(404)
        stamp = now_str()
        try:
            with get_db() as conn:
                cohort = _cohort(conn, cohort_id, lock=request.method == "POST")
                members = _members(conn, cohort_id, intern_id=intern["id"])
                if not members:
                    abort(404)
                member = members[0]
                if request.method == "POST":
                    message = _issue_credential(conn, cohort, member, "intern", str(intern["id"]), stamp)
                else:
                    _progress(conn, cohort, members, _milestones(conn, cohort_id), stamp[:10])
                    checkins = _checkins(conn, member["id"])
        except ValueError as exc:
            if request.method != "POST":
                raise
            flash(str(exc), "error")
        else:
            if request.method == "POST":
                flash(message)
        if request.method == "POST":
            return redirect(url_for(".learner", cohort_id=cohort_id), code=303)
        return render_template(
            "cohort_progress_learner.html", cohort=cohort, member=member,
            checkins=checkins, milestone_kinds=MILESTONE_KINDS,
        )

    @bp.route("/program-cohorts/<int:cohort_id>/staff/progress", methods=["GET", "POST"])
    def staff(cohort_id):
        admin = require_admin()
        mentor = None if admin else current_mentor()
        if not admin and not mentor:
            abort(404)
        stamp = now_str()
        try:
            with get_db() as conn:
                cohort = _cohort(conn, cohort_id)
                actor_type, actor_id = _staff_actor(cohort, admin, mentor)
                if request.method == "POST":
                    cohort = _cohort(conn, cohort_id, lock=True)
                    actor_type, actor_id = _staff_actor(cohort, admin, mentor)
                    action = request.form.get("action")
                    if action in {"add", "archive", "graduate"} and actor_type != "admin":
                        abort(403)
                    if action == "add":
                        _goal(conn, cohort, actor_id, stamp, request.form)
                        message = "Milestone added."
                    elif action == "archive":
                        _archive_goal(conn, cohort, actor_id, stamp, request.form.get("milestone_id", type=int))
                        message = "Milestone archived."
                    elif action in {"graduate", "checkin"}:
                        member_id = request.form.get("membership_id", type=int)
                        if member_id is None:
                            abort(400)
                        members = _members(conn, cohort_id, membership_id=member_id)
                        if not members:
                            abort(404)
                        member = members[0]
                        if action == "graduate":
                            message = _issue_credential(conn, cohort, member, actor_type, actor_id, stamp)
                        else:
                            checkin = request.form.get("message", "").strip()
                            if not checkin or len(checkin) > 500:
                                raise ValueError("Enter a check-in message of up to 500 characters.")
                            conn.execute(
                                """INSERT INTO program_cohort_checkins
                                   (membership_id, actor_type, actor_id, message, created_at)
                                   VALUES (?, ?, ?, ?, ?)""",
                                (member_id, actor_type, actor_id, checkin, stamp),
                            )
                            message = "Check-in saved to the learner’s progress page."
                    else:
                        abort(400)
                else:
                    members = _members(conn, cohort_id)
                    milestones = _milestones(conn, cohort_id)
                    frozen = bool(cohort["milestones_locked_at"])
                    _progress(conn, cohort, members, milestones, stamp[:10])
                    selected = request.args.get("member", type=int)
                    member = next((candidate for candidate in members if candidate["id"] == selected), None)
                    if selected is not None and member is None:
                        abort(404)
                    checkins = _checkins(conn, member["id"]) if member else []
        except ValueError as exc:
            if request.method != "POST":
                raise
            flash(str(exc), "error")
        else:
            if request.method == "POST":
                flash(message)
        if request.method == "POST":
            return redirect(
                url_for(".staff", cohort_id=cohort_id, member=request.form.get("membership_id", type=int)),
                code=303,
            )
        return render_template(
            "cohort_progress_staff.html", cohort=cohort, members=members, member=member,
            checkins=checkins, milestones=milestones, is_admin=actor_type == "admin",
            frozen=frozen, milestone_kinds=MILESTONE_KINDS,
        )

    return bp
