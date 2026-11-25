"""Public discovery and authenticated support workflows."""

from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit

from flask import Blueprint, abort, jsonify, redirect, render_template, request, session, url_for


PUBLIC_LINKS = (
    ("Course catalog", "Browse DBERT courses", "/courses"),
    ("Internships", "Explore open internships", "/internships"),
    ("Jobs", "Explore open job listings", "/jobs"),
    ("Résumé checker", "Check a résumé and compare revisions", "/resume-checker"),
    ("Help center", "Get help with courses, accounts, and support requests", "/help"),
)
LEARNER_LINKS = (
    ("Learner dashboard", "Review progress and applications", "/portal"),
    ("Mentor sessions", "Browse or manage mentor appointments", "/mentors/slots"),
    ("Bounties and perks", "Find tasks and use earned coins", "/tasks"),
    ("Support requests", "Report a problem or check an existing request", "/support"),
    ("Notification settings", "Manage delivery and read recent notifications", "/account/notifications"),
    ("Account security", "Review active sessions and sign out other devices", "/account/security"),
    ("Credential wallet", "View and share your certificates", "/account/credentials"),
    ("Verified portfolio", "Choose approved projects and credentials to share", "/account/portfolio"),
)
STATUS_LABELS = {"open": "Open", "reviewing": "In review", "resolved": "Resolved"}
AUDIT_QUERIES = {
    "Applications": """SELECT application_id AS item_id, changed_by AS actor, new_status AS action,
                       reason, changed_at AS occurred_at FROM application_status_history ORDER BY id DESC LIMIT 30""",
    "Enrollments": """SELECT enrollment_id AS item_id, changed_by AS actor, new_status AS action,
                      reason, changed_at AS occurred_at FROM enrollment_status_history ORDER BY id DESC LIMIT 30""",
    "Reviews": """SELECT subject_id AS item_id, staff_id AS actor, decision AS action,
                  reason_code AS reason, created_at AS occurred_at FROM review_log ORDER BY id DESC LIMIT 30""",
    "Credentials": """SELECT credential_id AS item_id, actor_id AS actor, status AS action,
                      reason, created_at AS occurred_at FROM credential_status_history ORDER BY id DESC LIMIT 30""",
    "Course publishing": """SELECT course_id AS item_id, actor, 'Published edition' AS action,
                            NULL AS reason, published_at AS occurred_at FROM course_publication_history ORDER BY id DESC LIMIT 30""",
    "Support": """SELECT request_id AS item_id, actor, status AS action,
                  NULL AS reason, created_at AS occurred_at FROM support_request_updates ORDER BY id DESC LIMIT 30""",
}


def init_support_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS support_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            details TEXT NOT NULL,
            source_path TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'open',
            assigned_actor TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_support_owner ON support_requests (intern_id, updated_at);
        CREATE INDEX IF NOT EXISTS idx_support_status ON support_requests (status, updated_at);
        CREATE TABLE IF NOT EXISTS support_request_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL REFERENCES support_requests(id),
            actor TEXT NOT NULL,
            status TEXT NOT NULL,
            note TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_support_updates ON support_request_updates (request_id, id);
    """)
    conn.commit()


def _safe_path(value):
    try:
        parsed = urlsplit(value)
    except ValueError:
        return ""
    if parsed.scheme or parsed.netloc or not parsed.path.startswith("/") or parsed.path.startswith("//"):
        return ""
    return parsed.path[:300] if "\\" not in parsed.path else ""


def _pattern(query):
    return "%" + query.lower().replace("!", "!!").replace("%", "!%").replace("_", "!_") + "%"


def _search(conn, query, learner, live_post_clause):
    pattern = _pattern(query)
    courses = conn.execute(
        """SELECT id, title, domain FROM courses
           WHERE is_active = 1 AND company_id IS NULL
             AND (LOWER(title) LIKE ? ESCAPE '!' OR LOWER(domain) LIKE ? ESCAPE '!')
           ORDER BY title LIMIT 12""",
        (pattern, pattern),
    ).fetchall()
    posts = conn.execute(
        f"""SELECT id, title, post_type, domain FROM posts
           WHERE {live_post_clause}
             AND (LOWER(title) LIKE ? ESCAPE '!' OR LOWER(domain) LIKE ? ESCAPE '!')
           ORDER BY id DESC LIMIT 12""",
        (pattern, pattern),
    ).fetchall()
    course_links = [(row["title"], row["domain"], f"/courses/{row['id']}") for row in courses]
    post_links = [
        (row["title"], row["domain"], f"/{'internships' if row['post_type'] == 'internship' else 'jobs'}/{row['id']}")
        for row in posts
    ]
    links = PUBLIC_LINKS + (LEARNER_LINKS if learner else ())
    navigation = [link for link in links if query.casefold() in " ".join(link[:2]).casefold()]
    return (("Courses", course_links), ("Jobs and internships", post_links), ("Pages", navigation))


def product_tools_blueprint(get_db, current_intern, support_actor, live_post_clause, signed_in_user, now_str, telemetry):
    bp = Blueprint("product_tools", __name__)

    @bp.get("/search")
    def search():
        query = request.args.get("q", "").strip()[:100]
        results = ()
        learner = bool(current_intern())
        if len(query) >= 2:
            with get_db() as conn:
                results = _search(conn, query, learner, live_post_clause)
        return render_template("product_search.html", query=query, results=results, learner=learner)

    @bp.get("/help")
    def help_center():
        return render_template("product_search.html", help_page=True, learner=bool(current_intern()))

    @bp.get("/saved-opportunities")
    def saved_opportunities():
        return render_template("saved_opportunities.html")

    @bp.get("/api/opportunities/availability")
    def opportunity_availability():
        ids = request.args.get("ids", "").split(",")
        if len(ids) > 50 or any(not item.isascii() or not item.isdecimal() or len(item) > 12 for item in ids):
            return jsonify({"error": "Supply up to 50 opportunity IDs."}), 400
        placeholders = ",".join("?" for _ in ids)
        with get_db() as conn:
            open_posts = conn.execute(
                f"SELECT id FROM posts WHERE ({live_post_clause}) AND id IN ({placeholders})", tuple(map(int, ids)),
            ).fetchall()
        return jsonify({"open_ids": [row["id"] for row in open_posts]})

    @bp.route("/support", methods=["GET", "POST"])
    def support():
        intern = current_intern()
        if not intern or int(intern["id"]) <= 0:
            session["next"] = "/support"
            return redirect("/#signin")
        draft = {
            "subject": request.form.get("subject", "").strip(),
            "details": request.form.get("details", "").strip(),
            "source_path": _safe_path(request.values.get("source", "")),
        }
        error = None
        with get_db() as conn:
            if request.method == "POST":
                if not 5 <= len(draft["subject"]) <= 120 or not 10 <= len(draft["details"]) <= 2000:
                    error = "Use 5 to 120 characters for the subject and 10 to 2,000 for the details."
                else:
                    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    conn.execute(
                        """INSERT INTO support_requests (intern_id, subject, details, source_path, created_at, updated_at)
                           VALUES (?, ?, ?, ?, ?, ?)""",
                        (intern["id"], draft["subject"], draft["details"], draft["source_path"], now, now),
                    )
                    conn.commit()
                    return redirect(url_for("product_tools.support", submitted=1))
            tickets = conn.execute(
                """SELECT r.*, (SELECT note FROM support_request_updates u WHERE u.request_id = r.id
                               ORDER BY u.id DESC LIMIT 1) AS latest_note
                   FROM support_requests r WHERE r.intern_id = ? ORDER BY r.updated_at DESC, r.id DESC LIMIT 50""",
                (intern["id"],),
            ).fetchall()
        return render_template(
            "support_requests.html", tickets=tickets, draft=draft, error=error,
            status_labels=STATUS_LABELS, staff=False,
        ), (422 if error else 200)

    @bp.get("/staff/support")
    def staff_support():
        if not support_actor():
            abort(403)
        status = request.args.get("status", "open")
        if status not in STATUS_LABELS:
            abort(400)
        with get_db() as conn:
            tickets = conn.execute(
                "SELECT * FROM support_requests WHERE status = ? ORDER BY created_at, id LIMIT 50", (status,),
            ).fetchall()
        return render_template("support_requests.html", tickets=tickets, status_labels=STATUS_LABELS, staff=True, status=status)

    @bp.post("/staff/support/<int:ticket_id>")
    def staff_update(ticket_id):
        actor = support_actor()
        if not actor:
            abort(403)
        status = request.form.get("status", "")
        note = request.form.get("note", "").strip()
        if status not in STATUS_LABELS or len(note) > 500:
            abort(400)
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        actor_id = f"{actor.get('role', 'staff')}:{actor['id']}"
        with get_db() as conn:
            updated = conn.execute(
                "UPDATE support_requests SET status = ?, assigned_actor = ?, updated_at = ? WHERE id = ?",
                (status, actor_id, now, ticket_id),
            )
            if updated.rowcount != 1:
                abort(404)
            conn.execute(
                "INSERT INTO support_request_updates (request_id, actor, status, note, created_at) VALUES (?, ?, ?, ?, ?)",
                (ticket_id, actor_id, status, note, now),
            )
            conn.commit()
        return redirect(url_for("product_tools.staff_support", status=status))

    @bp.route("/account/security", methods=["GET", "POST"])
    def account_security():
        user = signed_in_user()
        if not user:
            session["next"] = "/account/security"
            return redirect("/#signin")
        scope = (user["email"].lower(), user["role"], user["id"], now_str())
        with get_db() as conn:
            if request.method == "POST":
                target = request.form.get("session", "")
                if target == "others":
                    conn.execute(
                        """DELETE FROM user_sessions WHERE LOWER(email) = ? AND role = ?
                           AND id <> ? AND expires_at > ?""", scope,
                    )
                elif target.isascii() and target.isdecimal() and len(target) <= 12:
                    conn.execute(
                        """DELETE FROM user_sessions WHERE LOWER(email) = ? AND role = ?
                           AND id <> ? AND expires_at > ? AND id = ?""", (*scope, int(target)),
                    )
                else:
                    abort(400)
                conn.commit()
                return redirect(url_for("product_tools.account_security", updated=1))
            sessions = conn.execute(
                """SELECT id, created_at, expires_at, CASE WHEN id = ? THEN 1 ELSE 0 END AS is_current
                   FROM user_sessions WHERE LOWER(email) = ? AND role = ? AND expires_at > ?
                   ORDER BY is_current DESC, created_at DESC LIMIT 50""",
                (scope[2], scope[0], scope[1], scope[3]),
            ).fetchall()
        return render_template("account_security.html", sessions=sessions)

    @bp.get("/admin/platform-health")
    def platform_health():
        if not support_actor():
            abort(403)
        with get_db() as conn:
            queue = conn.execute(
                """SELECT status, COUNT(*) AS total, MIN(created_at) AS oldest
                   FROM event_outbox GROUP BY status ORDER BY status""",
            ).fetchall()
        snapshot = telemetry()
        metrics = {
            "Requests": snapshot["total_requests"],
            "Server error rate": f"{snapshot['rates']['5xx_error_rate_pct']}%",
            "95th-percentile response time": f"{snapshot['latencies']['p95_ms']} ms"
            if snapshot["latencies"].get("count") else "No samples",
            "Email failures": snapshot["failures"]["email_failures"],
            "Payment failures": snapshot["failures"]["payment_failures"],
            "AI failures": snapshot["failures"]["ai_failures"],
        }
        return render_template("platform_health.html", metrics=metrics, queue=queue)

    @bp.get("/admin/action-history")
    def action_history():
        if not support_actor():
            abort(403)
        category = request.args.get("area", "")
        if category and category not in AUDIT_QUERIES:
            abort(400)
        sections = (category,) if category else tuple(AUDIT_QUERIES)
        events = []
        with get_db() as conn:
            for section in sections:
                for item in conn.execute(AUDIT_QUERIES[section]).fetchall():
                    events.append({"category": section, **dict(item)})
        events.sort(key=lambda event: str(event["occurred_at"] or "").replace("T", " "), reverse=True)
        return render_template("admin_action_history.html", events=events[:80], sections=AUDIT_QUERIES, active=category)

    @bp.get("/admin/student-funnel")
    def student_funnel():
        if not support_actor():
            abort(403)
        days = request.args.get("days", type=int, default=30)
        if days not in (7, 30, 90):
            abort(400)
        cutoff = (datetime.fromisoformat(now_str()) - timedelta(days=days)).isoformat(sep=" ")
        with get_db() as conn:
            counts = conn.execute(
                """WITH cohort AS (
                       SELECT id, LOWER(email) AS email FROM intern_accounts
                       WHERE created_at >= ? AND email IS NOT NULL AND email <> ''
                   ), milestones AS (
                       SELECT DISTINCT c.email,
                              CASE WHEN EXISTS (
                                  SELECT 1 FROM applications a WHERE LOWER(a.email) = c.email
                              ) THEN 1 ELSE 0 END AS has_application,
                              CASE WHEN EXISTS (
                                  SELECT 1 FROM course_enrollments e
                                  WHERE e.intern_id = c.id OR LOWER(e.email) = c.email
                              ) THEN 1 ELSE 0 END AS is_enrolled,
                              CASE WHEN EXISTS (
                                  SELECT 1 FROM course_enrollments e
                                  WHERE (e.intern_id = c.id OR LOWER(e.email) = c.email)
                                  AND (EXISTS (SELECT 1 FROM day_quiz_attempts q WHERE q.enrollment_id = e.id)
                                    OR EXISTS (SELECT 1 FROM course_subtopic_chats ch
                                               WHERE ch.enrollment_id = e.id AND ch.role = 'user'))
                              ) THEN 1 ELSE 0 END AS has_studied
                       FROM cohort c
                   ), deduped AS (
                       SELECT email, MAX(has_application) AS applied, MAX(is_enrolled) AS enrolled,
                              MAX(has_studied) AS studied FROM milestones GROUP BY email
                   )
                   SELECT COUNT(*) AS accounts, COALESCE(SUM(applied), 0) AS applications,
                          COALESCE(SUM(applied * enrolled), 0) AS enrollments,
                          COALESCE(SUM(applied * enrolled * studied), 0) AS started
                   FROM deduped""",
                (cutoff,),
            ).fetchone()
            visitors = conn.execute(
                """SELECT COUNT(DISTINCT visitor_id) AS count FROM device_profiles
                   WHERE created_at >= ? AND visitor_id IS NOT NULL AND visitor_id <> ''""",
                (cutoff,),
            ).fetchone()["count"]
        stages = [
            ("Accounts created", counts["accounts"]), ("Applied", counts["applications"]),
            ("Enrolled in a course", counts["enrollments"]), ("Started learning", counts["started"]),
        ]
        return render_template("student_funnel.html", days=days, stages=stages, visitors=visitors)

    @bp.get("/account/credentials")
    def credential_wallet():
        intern = current_intern()
        if not intern:
            session["next"] = "/account/credentials"
            return redirect("/#signin")
        email = intern.get("email") or ""
        with get_db() as conn:
            credentials = conn.execute(
                """SELECT cert_id, course_title, issued_at, credential_status, replaced_by_cert_id
                   FROM intern_certificates WHERE cert_id IS NOT NULL
                     AND (intern_id = ? OR (email IS NOT NULL AND email <> '' AND LOWER(email) = LOWER(?)))
                   ORDER BY id DESC""",
                (intern["id"], email),
            ).fetchall()
        return render_template("credential_wallet.html", credentials=credentials)

    @bp.route("/account/portfolio", methods=["GET", "POST"])
    def portfolio():
        intern = current_intern()
        if not intern:
            session["next"] = "/account/portfolio"
            return redirect("/#signin")
        from services.verified_portfolio import read_portfolio_selection, verified_choices, write_portfolio_selection

        with get_db() as conn:
            projects, credentials = verified_choices(conn, intern["id"], intern.get("email") or "")
            chosen_projects, chosen_credentials = read_portfolio_selection(conn, intern["id"])
            if request.method == "POST":
                try:
                    chosen_projects = {int(value) for value in request.form.getlist("project")}
                    chosen_credentials = {int(value) for value in request.form.getlist("credential")}
                except ValueError:
                    abort(400)
                if (not chosen_projects.issubset({item["id"] for item in projects})
                        or not chosen_credentials.issubset({item["id"] for item in credentials})):
                    abort(400)
                write_portfolio_selection(conn, intern["id"], chosen_projects, chosen_credentials)
                conn.commit()
                return redirect(url_for("product_tools.portfolio", updated=1))
        return render_template(
            "verified_portfolio.html", projects=projects, credentials=credentials,
            chosen_projects=chosen_projects, chosen_credentials=chosen_credentials,
        )

    @bp.route("/admin/credential-status", methods=["GET", "POST"])
    def credential_status():
        actor = support_actor()
        if not actor:
            abort(403)
        error = None
        if request.method == "POST":
            certificate = request.form.get("cert_id", "").strip()
            status = request.form.get("status", "")
            replacement = request.form.get("replacement_id", "").strip() if status == "replaced" else None
            reason = request.form.get("reason", "").strip()
            if not 1 <= len(certificate) <= 120 or status not in {"replaced", "revoked"} or not 5 <= len(reason) <= 500:
                error = "Enter a certificate ID, an action, and a reason of 5 to 500 characters."
            else:
                with get_db() as conn:
                    source = conn.execute(
                        "SELECT id, intern_id FROM intern_certificates WHERE cert_id = ? AND credential_status = 'valid'",
                        (certificate,),
                    ).fetchall()
                    if len(source) != 1:
                        error = "This certificate is unavailable or its ID is ambiguous."
                    elif status == "replaced" and (not replacement or replacement == certificate or not conn.execute(
                        "SELECT id FROM intern_certificates WHERE cert_id = ? AND intern_id = ? AND credential_status = 'valid'",
                        (replacement, source[0]["intern_id"]),
                    ).fetchone()):
                        error = "Select another valid certificate belonging to the same learner."
                    else:
                        updated = conn.execute(
                            """UPDATE intern_certificates SET credential_status = ?, replaced_by_cert_id = ?
                               WHERE id = ? AND credential_status = 'valid'""",
                            (status, replacement, source[0]["id"]),
                        )
                        if updated.rowcount != 1:
                            abort(409)
                        conn.execute(
                            """INSERT INTO credential_status_history
                               (credential_id, actor_id, status, replacement_id, reason, created_at)
                               VALUES (?, ?, ?, ?, ?, ?)""",
                            (source[0]["id"], str(actor["id"]), status, replacement, reason, now_str()),
                        )
                        conn.commit()
                        return redirect(url_for("product_tools.credential_status", updated=1))
        return render_template("credential_wallet.html", admin=True, error=error), (422 if error else 200)

    @bp.after_request
    def prevent_shared_caching(response):
        response.headers["Cache-Control"] = "private, no-store"
        return response

    return bp
