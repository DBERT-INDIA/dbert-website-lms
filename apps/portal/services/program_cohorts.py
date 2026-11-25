"""Course cohorts, fair seat allocation, and role-scoped rosters."""

from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for


AVAILABLE_COURSE = "c.is_active = 1 AND (c.content_status = 'approved' OR c.company_id IS NULL)"
DB_INTEGER_MAX = 2_147_483_647
COURSE_ACCESS = """
    EXISTS (
        SELECT 1 FROM course_enrollments e
        WHERE e.course_id = ? AND (e.intern_id = i.id OR LOWER(e.email) = LOWER(i.email))
    )
"""


def init_program_cohorts(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS program_cohorts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL REFERENCES courses(id),
            title TEXT NOT NULL,
            starts_on TEXT NOT NULL,
            ends_on TEXT NOT NULL CHECK (ends_on >= starts_on),
            capacity INTEGER NOT NULL CHECK (capacity > 0),
            mentor_id INTEGER REFERENCES mentors(id) ON DELETE SET NULL,
            status TEXT NOT NULL CHECK (status IN ('open', 'closed')),
            schedule_locked_at TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS program_cohort_memberships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cohort_id INTEGER NOT NULL REFERENCES program_cohorts(id),
            intern_id INTEGER NOT NULL REFERENCES intern_accounts(id) ON DELETE CASCADE,
            status TEXT NOT NULL CHECK (status IN ('enrolled', 'waitlisted', 'withdrawn', 'completed')),
            requested_at TEXT NOT NULL,
            enrolled_at TEXT,
            updated_at TEXT NOT NULL,
            queue_order INTEGER NOT NULL DEFAULT 0,
            UNIQUE(cohort_id, intern_id)
        );
        CREATE INDEX IF NOT EXISTS idx_program_cohorts_course ON program_cohorts(course_id);
        CREATE INDEX IF NOT EXISTS idx_program_cohorts_mentor ON program_cohorts(mentor_id);
        CREATE INDEX IF NOT EXISTS idx_program_cohort_queue
            ON program_cohort_memberships(cohort_id, status, queue_order);
        CREATE TABLE IF NOT EXISTS program_cohort_access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cohort_id INTEGER NOT NULL REFERENCES program_cohorts(id),
            intern_id INTEGER REFERENCES intern_accounts(id) ON DELETE SET NULL,
            action TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_program_cohort_log ON program_cohort_access_log(cohort_id, id);
    """)
    conn.commit()


def _get_cohort(conn, cohort_id, *, lock=False):
    if lock:
        # This acquires a PostgreSQL row lock or a SQLite writer lock before reading seat counts.
        conn.execute("UPDATE program_cohorts SET updated_at = updated_at WHERE id = ?", (cohort_id,))
    return conn.execute(
        f"""SELECT p.*, c.title AS course_title, m.name AS mentor_name,
                   CASE WHEN {AVAILABLE_COURSE} THEN 1 ELSE 0 END AS course_available,
                   (SELECT COUNT(*) FROM program_cohort_memberships
                    WHERE cohort_id = p.id AND status IN ('enrolled', 'completed')) AS seats_taken
            FROM program_cohorts p JOIN courses c ON c.id = p.course_id
            LEFT JOIN mentors m ON m.id = p.mentor_id WHERE p.id = ?""",
        (cohort_id,),
    ).fetchone()


def _accepting(cohort, now):
    return bool(cohort["course_available"] and cohort["status"] == "open" and now[:10] <= cohort["ends_on"])


def _log(conn, cohort_id, intern_id, action, now):
    conn.execute(
        "INSERT INTO program_cohort_access_log (cohort_id, intern_id, action, created_at) VALUES (?, ?, ?, ?)",
        (cohort_id, intern_id, action, now),
    )


def _fill_seats(conn, cohort, seats, now):
    if seats <= 0 or not _accepting(cohort, now):
        return seats

    next_members = conn.execute(
        f"""SELECT s.id, s.intern_id FROM program_cohort_memberships s
            JOIN intern_accounts i ON i.id = s.intern_id
            WHERE s.cohort_id = ? AND s.status = 'waitlisted' AND i.is_active = 1 AND {COURSE_ACCESS}
            ORDER BY s.queue_order, s.id LIMIT ?""",
        (cohort["id"], cohort["course_id"], seats),
    ).fetchall()
    for member in next_members:
        conn.execute(
            "UPDATE program_cohort_memberships SET status = 'enrolled', enrolled_at = ?, updated_at = ? WHERE id = ?",
            (now, now, member["id"]),
        )
        _log(conn, cohort["id"], member["intern_id"], "promoted", now)
    return seats - len(next_members)


def _membership(conn, cohort_id, intern_id):
    return conn.execute(
        "SELECT * FROM program_cohort_memberships WHERE cohort_id = ? AND intern_id = ?",
        (cohort_id, intern_id),
    ).fetchone()


def _has_course_access(conn, intern_id, course_id):
    return conn.execute(
        f"SELECT 1 FROM intern_accounts i WHERE i.id = ? AND i.is_active = 1 AND {COURSE_ACCESS}",
        (intern_id, course_id),
    ).fetchone() is not None


def _join(conn, cohort, intern_id, member, now):
    if not _accepting(cohort, now):
        raise ValueError("This cohort has closed registration.")
    if not _has_course_access(conn, intern_id, cohort["course_id"]):
        raise ValueError("Enroll in the course before joining this cohort.")

    seats = _fill_seats(conn, cohort, cohort["capacity"] - cohort["seats_taken"], now)
    # Filling seats above may have enrolled this learner on a repeated request.
    if member and member["status"] != "withdrawn":
        return

    queue_order = conn.execute(
        "SELECT COALESCE(MAX(queue_order), 0) + 1 AS next_order FROM program_cohort_memberships WHERE cohort_id = ?",
        (cohort["id"],),
    ).fetchone()["next_order"]
    status = "enrolled" if seats > 0 else "waitlisted"
    enrolled_at = now if status == "enrolled" else None
    conn.execute(
        """INSERT INTO program_cohort_memberships
           (cohort_id, intern_id, status, requested_at, enrolled_at, updated_at, queue_order)
           VALUES (?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT (cohort_id, intern_id) DO UPDATE SET
           status = excluded.status, requested_at = excluded.requested_at, enrolled_at = excluded.enrolled_at,
           updated_at = excluded.updated_at, queue_order = excluded.queue_order""",
        (cohort["id"], intern_id, status, now, enrolled_at, now, queue_order),
    )
    _log(conn, cohort["id"], intern_id, status, now)


def _withdraw(conn, cohort, intern_id, member, now):
    if not member or member["status"] not in ("enrolled", "waitlisted"):
        return
    conn.execute(
        "UPDATE program_cohort_memberships SET status = 'withdrawn', updated_at = ? WHERE id = ?",
        (now, member["id"]),
    )
    _log(conn, cohort["id"], intern_id, "withdrawn", now)
    released = 1 if member["status"] == "enrolled" else 0
    _fill_seats(conn, cohort, cohort["capacity"] - cohort["seats_taken"] + released, now)


def _cohort_fields(conn, form):
    title = form.get("title", "").strip()
    if not 3 <= len(title) <= 160:
        raise ValueError("Enter a cohort title with 3 to 160 characters.")
    try:
        starts_on = date.fromisoformat(form.get("starts_on", ""))
        ends_on = date.fromisoformat(form.get("ends_on", ""))
        capacity = int(form.get("capacity", ""))
        mentor_id = int(form["mentor_id"]) if form.get("mentor_id") else None
    except ValueError as exc:
        raise ValueError("Choose dates and a valid capacity.") from exc
    if ends_on < starts_on:
        raise ValueError("The end date must be on or after the start date.")
    if not 1 <= capacity <= DB_INTEGER_MAX:
        raise ValueError("Enter a positive whole number for capacity.")
    if mentor_id is not None and (not 1 <= mentor_id <= DB_INTEGER_MAX or not conn.execute(
        "SELECT 1 FROM mentors WHERE id = ? AND is_active = 1", (mentor_id,),
    ).fetchone()):
        raise ValueError("Choose an active mentor.")
    return title, starts_on.isoformat(), ends_on.isoformat(), capacity, mentor_id


def _create_cohort(conn, form, now):
    fields = _cohort_fields(conn, form)
    try:
        course_id = int(form.get("course_id", ""))
    except ValueError as exc:
        raise ValueError("Choose an available course.") from exc
    if not 1 <= course_id <= DB_INTEGER_MAX or not conn.execute(
        f"SELECT 1 FROM courses c WHERE c.id = ? AND {AVAILABLE_COURSE}", (course_id,),
    ).fetchone():
        raise ValueError("Choose an available course.")
    cohort_id = conn.execute(
        """INSERT INTO program_cohorts (course_id, title, starts_on, ends_on, capacity, mentor_id, status, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, 'open', ?, ?)""",
        (course_id, *fields, now, now),
    ).lastrowid
    _log(conn, cohort_id, None, "created", now)
    return cohort_id


def program_cohorts_blueprint(get_db, current_intern, require_admin, current_mentor, now_str):
    bp = Blueprint("program_cohorts", __name__)
    overview = f"""
        SELECT p.*, c.title AS course_title, m.name AS mentor_name,
               CASE WHEN {AVAILABLE_COURSE} AND p.status = 'open' AND p.ends_on >= ? THEN 1 ELSE 0 END AS accepting,
               (SELECT COUNT(*) FROM program_cohort_memberships
                WHERE cohort_id = p.id AND status IN ('enrolled', 'completed')) AS seats_taken,
               (SELECT COUNT(*) FROM program_cohort_memberships
                WHERE cohort_id = p.id AND status = 'waitlisted') AS waiting
        FROM program_cohorts p JOIN courses c ON c.id = p.course_id LEFT JOIN mentors m ON m.id = p.mentor_id
    """

    @bp.after_request
    def private(response):
        response.headers["Cache-Control"] = "private, no-store"
        return response

    @bp.get("/program-cohorts")
    def index():
        intern = current_intern()
        if not intern:
            return redirect("/#signin")
        with get_db() as conn:
            cohorts = conn.execute(
                f"""SELECT listed.*, s.status AS membership_status FROM ({overview}) listed
                    LEFT JOIN program_cohort_memberships s ON s.cohort_id = listed.id AND s.intern_id = ?
                    WHERE listed.accepting = 1 OR s.status IN ('enrolled', 'completed', 'waitlisted')
                    ORDER BY CASE WHEN s.status IN ('enrolled', 'completed', 'waitlisted') THEN 0 ELSE 1 END,
                        listed.starts_on, listed.id""",
                (now_str()[:10], intern["id"]),
            ).fetchall()
        return render_template("program_cohorts.html", cohorts=cohorts, role="learner")

    @bp.route("/program-cohorts/<int:cohort_id>", methods=["GET", "POST"])
    def detail(cohort_id):
        intern = current_intern()
        if not intern:
            return redirect("/#signin")
        now = now_str()
        with get_db() as conn:
            cohort = _get_cohort(conn, cohort_id, lock=request.method == "POST")
            if not cohort:
                abort(404)
            member = _membership(conn, cohort_id, intern["id"])
            if not member and not _accepting(cohort, now):
                abort(404)
            if request.method == "POST":
                action = request.form.get("action")
                try:
                    if action == "join":
                        _join(conn, cohort, intern["id"], member, now)
                    elif action == "withdraw":
                        _withdraw(conn, cohort, intern["id"], member, now)
                    else:
                        abort(400)
                    conn.commit()
                except ValueError as error:
                    conn.rollback()
                    flash(str(error), "error")
                return redirect(url_for(".detail", cohort_id=cohort_id))
            eligible = _has_course_access(conn, intern["id"], cohort["course_id"])
        return render_template(
            "program_cohort_detail.html", cohort=cohort, member=member, accepting=_accepting(cohort, now),
            eligible=eligible, role="learner",
        )

    @bp.route("/admin/program-cohorts", methods=["GET", "POST"])
    def admin_index():
        if not require_admin():
            abort(403)
        with get_db() as conn:
            if request.method == "POST":
                try:
                    cohort_id = _create_cohort(conn, request.form, now_str())
                    conn.commit()
                except ValueError as error:
                    conn.rollback()
                    flash(str(error), "error")
                else:
                    return redirect(url_for(".admin_detail", cohort_id=cohort_id))
            cohorts = conn.execute(overview + " ORDER BY p.starts_on DESC, p.id DESC", (now_str()[:10],)).fetchall()
            courses = conn.execute(
                f"SELECT c.id, c.title FROM courses c WHERE {AVAILABLE_COURSE} ORDER BY c.title, c.id"
            ).fetchall()
            mentors = conn.execute("SELECT id, name FROM mentors WHERE is_active = 1 ORDER BY name, id").fetchall()
        return render_template("program_cohorts.html", cohorts=cohorts, courses=courses, mentors=mentors, role="admin")

    @bp.route("/admin/program-cohorts/<int:cohort_id>", methods=["GET", "POST"])
    def admin_detail(cohort_id):
        if not require_admin():
            abort(403)
        now = now_str()
        with get_db() as conn:
            cohort = _get_cohort(conn, cohort_id, lock=request.method == "POST")
            if not cohort:
                abort(404)
            if request.method == "POST":
                try:
                    action = request.form.get("action")
                    status = request.form.get("status")
                    if action == "update":
                        title, starts_on, ends_on, capacity, mentor_id = _cohort_fields(conn, request.form)
                        if capacity < cohort["seats_taken"]:
                            raise ValueError("Capacity must cover the enrolled and completed learners.")
                        if cohort["schedule_locked_at"] and (starts_on, ends_on) != (cohort["starts_on"], cohort["ends_on"]):
                            raise ValueError("Cohort dates are fixed once a milestone is defined.")
                        conn.execute(
                            """UPDATE program_cohorts SET title = ?, starts_on = ?, ends_on = ?, capacity = ?, mentor_id = ?,
                               updated_at = ? WHERE id = ?""",
                            (title, starts_on, ends_on, capacity, mentor_id, now, cohort_id),
                        )
                        _log(conn, cohort_id, None, "updated", now)
                    elif status in ("open", "closed"):
                        if status == "open" and (now[:10] > cohort["ends_on"] or not cohort["course_available"]):
                            raise ValueError("Registration can reopen while the cohort dates and course are active.")
                        if status != cohort["status"]:
                            conn.execute(
                                "UPDATE program_cohorts SET status = ?, updated_at = ? WHERE id = ?", (status, now, cohort_id),
                            )
                            _log(conn, cohort_id, None, "reopened" if status == "open" else "closed", now)
                    elif action != "fill-seats":
                        abort(400)
                except ValueError as error:
                    conn.rollback()
                    flash(str(error), "error")
                    if action == "update":
                        return roster(conn, cohort, "admin"), 422
                else:
                    cohort = _get_cohort(conn, cohort_id)
                    free_seats = cohort["capacity"] - cohort["seats_taken"]
                    remaining = _fill_seats(conn, cohort, free_seats, now)
                    conn.commit()
                    if action == "fill-seats":
                        filled = free_seats - remaining
                        flash(f"Seats filled from the waitlist: {filled}.", "success")
                return redirect(url_for(".admin_detail", cohort_id=cohort_id))
            return roster(conn, cohort, "admin")

    @bp.get("/mentor/program-cohorts")
    def mentor_index():
        mentor = current_mentor()
        if not mentor:
            abort(403)
        with get_db() as conn:
            cohorts = conn.execute(
                overview + " WHERE p.mentor_id = ? ORDER BY p.starts_on DESC, p.id DESC", (now_str()[:10], mentor["id"]),
            ).fetchall()
        return render_template("program_cohorts.html", cohorts=cohorts, role="mentor")

    @bp.get("/mentor/program-cohorts/<int:cohort_id>")
    def mentor_detail(cohort_id):
        mentor = current_mentor()
        if not mentor:
            abort(403)
        with get_db() as conn:
            cohort = _get_cohort(conn, cohort_id)
            if not cohort or cohort["mentor_id"] != mentor["id"]:
                abort(404)
            return roster(conn, cohort, "mentor")

    def roster(conn, cohort, role):
        members = conn.execute(
            """SELECT s.status, s.requested_at, s.enrolled_at, i.name FROM program_cohort_memberships s
               JOIN intern_accounts i ON i.id = s.intern_id WHERE s.cohort_id = ?
               ORDER BY CASE s.status WHEN 'enrolled' THEN 1 WHEN 'waitlisted' THEN 2
                                      WHEN 'completed' THEN 3 ELSE 4 END, s.queue_order, s.id""",
            (cohort["id"],),
        ).fetchall()
        history = []
        mentors = []
        if role == "admin":
            history = conn.execute(
                """SELECT l.action, l.created_at, i.name FROM program_cohort_access_log l
                   LEFT JOIN intern_accounts i ON i.id = l.intern_id WHERE l.cohort_id = ?
                   ORDER BY l.id DESC LIMIT 50""",
                (cohort["id"],),
            ).fetchall()
            mentors = conn.execute("SELECT id, name FROM mentors WHERE is_active = 1 ORDER BY name, id").fetchall()
        return render_template(
            "program_cohort_detail.html", cohort=cohort, members=members, history=history, mentors=mentors,
            accepting=_accepting(cohort, now_str()), role=role,
        )

    return bp
