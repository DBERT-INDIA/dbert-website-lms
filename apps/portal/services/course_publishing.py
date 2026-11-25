"""Versioned drafts for course authors and publication by DBERT admins."""

import json
import re

from flask import Blueprint, abort, redirect, render_template, request, url_for

from services.spotlight_schedule import spotlight_url_allowed


def init_course_publishing(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS course_editions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL REFERENCES courses(id),
            author TEXT NOT NULL,
            snapshot_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            first_published_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_course_editions ON course_editions(course_id, id);
        CREATE TABLE IF NOT EXISTS course_live_edition (
            course_id INTEGER PRIMARY KEY REFERENCES courses(id),
            edition_id INTEGER NOT NULL REFERENCES course_editions(id)
        );
        CREATE TABLE IF NOT EXISTS course_publication_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            edition_id INTEGER NOT NULL,
            actor TEXT NOT NULL,
            published_at TEXT NOT NULL
        );
    """)
    conn.commit()


def _current_material(conn, course):
    lessons = conn.execute(
        """SELECT s.id, s.title, s.brief FROM course_subtopics s
           JOIN course_chapters ch ON ch.id = s.chapter_id WHERE ch.course_id = ?
           ORDER BY ch.day_number, s.sort_order, s.id""", (course["id"],),
    ).fetchall()
    return {"title": course["title"], "lessons": [dict(lesson) for lesson in lessons]}


def _draft_from_form(current, form):
    title = form.get("title", "").strip()
    if not 3 <= len(title) <= 160:
        raise ValueError("The course title must be 3 to 160 characters.")
    if not current["lessons"]:
        raise ValueError("Add lesson material through the course creation workflow first.")
    lessons = []
    for item in current["lessons"]:
        lesson = {"id": item["id"], "title": form.get(f"title_{item['id']}", "").strip(),
                  "brief": form.get(f"brief_{item['id']}", "").strip()}
        if not 1 <= len(lesson["title"]) <= 160 or not 1 <= len(lesson["brief"]) <= 8000:
            raise ValueError("Each lesson needs a title and material of up to 8,000 characters.")
        if any(re.search(r"</?[a-zA-Z][^>]*>", value) for value in (title, lesson["title"], lesson["brief"])):
            raise ValueError("Use plain text or Markdown for lesson material.")
        urls = re.findall(r"https?://[^\s<>]+", lesson["brief"], re.IGNORECASE)
        if any(not spotlight_url_allowed(url) for url in urls):
            raise ValueError("Use HTTPS for links in lesson material.")
        lessons.append(lesson)
    return {"title": title, "lessons": lessons}


def _publish(conn, course, current, edition, actor, now):
    snapshot = json.loads(edition["snapshot_json"])
    if {item["id"] for item in current["lessons"]} != {item["id"] for item in snapshot["lessons"]}:
        raise ValueError("The underlying lesson list changed. Create a draft against the current course.")

    previous = conn.execute("SELECT edition_id FROM course_live_edition WHERE course_id = ?", (course["id"],)).fetchone()
    if not previous:
        conn.execute(
            """INSERT INTO course_editions (course_id, author, snapshot_json, created_at, first_published_at)
               VALUES (?, ?, ?, ?, ?)""",
            (course["id"], "baseline", json.dumps(current), now, now),
        )
    conn.execute("UPDATE courses SET title = ? WHERE id = ?", (snapshot["title"], course["id"]))
    for lesson in snapshot["lessons"]:
        conn.execute("UPDATE course_subtopics SET title = ?, brief = ? WHERE id = ?",
                     (lesson["title"], lesson["brief"], lesson["id"]))
    conn.execute("UPDATE course_editions SET first_published_at = COALESCE(first_published_at, ?) WHERE id = ?",
                 (now, edition["id"]))
    conn.execute(
        """INSERT INTO course_live_edition (course_id, edition_id) VALUES (?, ?)
           ON CONFLICT(course_id) DO UPDATE SET edition_id = excluded.edition_id RETURNING course_id""",
        (course["id"], edition["id"]),
    )
    conn.execute("INSERT INTO course_publication_history (course_id, edition_id, actor, published_at) VALUES (?, ?, ?, ?)",
                 (course["id"], edition["id"], actor, now))


def course_publishing_blueprint(get_db, current_company, require_admin, now_str):
    bp = Blueprint("course_publishing", __name__)

    @bp.get("/course-publishing")
    def courses():
        admin = require_admin()
        company = current_company() if not admin else None
        if not admin and not company:
            abort(403)
        with get_db() as conn:
            rows = conn.execute(
                "SELECT id, title, content_status FROM courses WHERE (? = 1 OR company_id = ?) ORDER BY id DESC LIMIT 100",
                (int(bool(admin)), company["id"] if company else None),
            ).fetchall()
        return render_template("course_publishing.html", courses=rows, publishing_admin=bool(admin))

    @bp.route("/course-publishing/<int:course_id>", methods=["GET", "POST"])
    def edit(course_id):
        admin = require_admin()
        company = current_company() if not admin else None
        if not admin and not company:
            abort(403)
        actor = f"admin:{admin['id']}" if admin else f"company:{company['id']}"
        error = None
        display = None
        with get_db() as conn:
            course = conn.execute(
                "SELECT id, title, company_id, content_status FROM courses WHERE id = ? AND (? = 1 OR company_id = ?)",
                (course_id, int(bool(admin)), company["id"] if company else None),
            ).fetchone()
            if not course:
                abort(404)
            if request.method == "POST":
                locked = conn.execute(
                    "UPDATE courses SET title = title WHERE id = ? AND (? = 1 OR company_id = ?)",
                    (course_id, int(bool(admin)), company["id"] if company else None),
                )
                if locked.rowcount != 1:
                    abort(404)
                course = conn.execute("SELECT id, title, company_id, content_status FROM courses WHERE id = ?", (course_id,)).fetchone()
            current = _current_material(conn, course)
            if request.method == "POST":
                try:
                    action = request.form.get("action")
                    if action == "draft":
                        draft = _draft_from_form(current, request.form)
                        saved = conn.execute(
                            "INSERT INTO course_editions (course_id, author, snapshot_json, created_at) VALUES (?, ?, ?, ?)",
                            (course_id, actor, json.dumps(draft), now_str()),
                        )
                        selected = saved.lastrowid
                    elif action == "publish" and admin:
                        selected = request.form.get("edition_id", type=int)
                        edition = conn.execute("SELECT * FROM course_editions WHERE course_id = ? AND id = ?",
                                               (course_id, selected)).fetchone()
                        if not edition:
                            abort(404)
                        _publish(conn, course, current, edition, actor, now_str())
                    else:
                        abort(403)
                    conn.commit()
                    return redirect(url_for("course_publishing.edit", course_id=course_id, edition_id=selected))
                except ValueError as exc:
                    conn.rollback()
                    error = str(exc)
                    if request.form.get("action") == "draft":
                        display = {"title": request.form.get("title", ""), "lessons": [
                            {"id": item["id"], "title": request.form.get(f"title_{item['id']}", ""),
                             "brief": request.form.get(f"brief_{item['id']}", "")} for item in current["lessons"]
                        ]}

            revisions = conn.execute(
                """SELECT id, author, created_at, first_published_at FROM course_editions
                   WHERE course_id = ? ORDER BY id DESC LIMIT 30""", (course_id,),
            ).fetchall()
            live = conn.execute("SELECT edition_id FROM course_live_edition WHERE course_id = ?", (course_id,)).fetchone()
            selected = request.args.get("edition_id", type=int)
            edition = conn.execute("SELECT id, snapshot_json FROM course_editions WHERE course_id = ? AND id = ?",
                                   (course_id, selected)).fetchone() if selected else None
            if selected and not edition:
                abort(404)
        if display is None:
            display = json.loads(edition["snapshot_json"]) if edition else current
        return render_template(
            "course_publishing.html", course=course, material=display, edition=edition, revisions=revisions,
            live_id=live["edition_id"] if live else None, publishing_admin=bool(admin), error=error,
        ), (422 if error else 200)

    @bp.after_request
    def private(response):
        response.headers["Cache-Control"] = "private, no-store"
        return response

    return bp
