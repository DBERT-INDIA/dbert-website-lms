"""Student listing reports and staff triage of listing-quality signals."""

from datetime import datetime, timedelta


REPORT_REASONS = (
    ("stale", "Role appears closed or out of date"),
    ("duplicate", "Duplicate listing"),
    ("inaccurate", "Inaccurate listing details"),
    ("other", "Other issue"),
)
PAGE_SIZE = 25


class ListingReportError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def report_listing(conn, *, post_id, intern_id, reason, note):
    note = note.strip()
    if reason not in dict(REPORT_REASONS):
        raise ListingReportError("Choose a reason for the report.")
    if len(note) > 600:
        raise ListingReportError("Keep the report under 600 characters.")
    listing = conn.execute(
        "SELECT p.id, p.post_type, p.slug FROM posts p JOIN companies c ON c.id = p.company_id "
        "WHERE p.id = ? AND p.status = 'published' AND c.is_approved = 1 AND c.is_active = 1",
        (post_id,),
    ).fetchone()
    if not listing:
        raise ListingReportError("This listing could not be found.", 404)
    conn.execute(
        "INSERT INTO job_listing_reports (post_id, intern_id, reason, note) VALUES (?, ?, ?, ?) "
        "ON CONFLICT (post_id, intern_id, reason) DO NOTHING",
        (post_id, intern_id, reason, note or None),
    )
    return dict(listing)


QUEUE_SQL = """
    WITH duplicate_groups AS (
      SELECT company_id, post_type, LOWER(TRIM(title)) AS normalized_title,
             LOWER(TRIM(COALESCE(location, ''))) AS normalized_location
      FROM posts WHERE status = 'published'
      GROUP BY company_id, post_type, LOWER(TRIM(title)), LOWER(TRIM(COALESCE(location, '')))
      HAVING COUNT(*) > 1
    ), open_reports AS (
      SELECT post_id, COUNT(*) AS total FROM job_listing_reports WHERE status = 'pending' GROUP BY post_id
    ), flagged AS (
      SELECT p.id, p.title, p.post_type, p.slug, p.status, c.name AS company_name,
             COALESCE(r.total, 0) AS report_count,
             CASE WHEN p.status = 'published' AND d.company_id IS NOT NULL THEN 1 ELSE 0 END AS duplicate,
             CASE WHEN p.status = 'published' AND (
               p.expires_at <= datetime('now','localtime') OR COALESCE(p.updated_at, p.published_at, p.created_at) <= ?
             ) THEN 1 ELSE 0 END AS stale,
             CASE WHEN p.status = 'published' AND (
               NULLIF(TRIM(p.title), '') IS NULL OR NULLIF(TRIM(p.domain), '') IS NULL OR NULLIF(TRIM(p.description), '') IS NULL
             ) THEN 1 ELSE 0 END AS incomplete
      FROM posts p
      JOIN companies c ON c.id = p.company_id
      LEFT JOIN duplicate_groups d ON d.company_id = p.company_id AND d.post_type = p.post_type
           AND d.normalized_title = LOWER(TRIM(p.title)) AND d.normalized_location = LOWER(TRIM(COALESCE(p.location, '')))
      LEFT JOIN open_reports r ON r.post_id = p.id
      WHERE p.status = 'published' OR r.total > 0
    )
"""


def listing_quality_queue(conn, *, page=1, view="all"):
    view = view if view in ("all", "reports", "automated") else "all"
    filters = {
        "all": "report_count > 0 OR duplicate = 1 OR stale = 1 OR incomplete = 1",
        "reports": "report_count > 0",
        "automated": "duplicate = 1 OR stale = 1 OR incomplete = 1",
    }
    now = conn.execute("SELECT datetime('now','localtime') AS queue_now").fetchone()["queue_now"]
    if isinstance(now, str):
        now = datetime.fromisoformat(now)
    older_than = (now - timedelta(days=60)).isoformat(sep=" ", timespec="seconds")
    where = " WHERE " + filters[view]
    total = conn.execute(QUEUE_SQL + "SELECT COUNT(*) AS total FROM flagged" + where, (older_than,)).fetchone()["total"]
    page_count = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page or 1, page_count))
    rows = [dict(row) for row in conn.execute(
        QUEUE_SQL + "SELECT * FROM flagged" + where + " ORDER BY report_count DESC, id DESC LIMIT ? OFFSET ?",
        (older_than, PAGE_SIZE, (page - 1) * PAGE_SIZE),
    )]
    return {"rows": rows, "view": view, "page": page, "page_count": page_count, "total": total}


def pending_listing_reports(conn, post_id):
    return [dict(row) for row in conn.execute(
        "SELECT id, reason, note, created_at FROM job_listing_reports "
        "WHERE post_id = ? AND status = 'pending' ORDER BY created_at, id",
        (post_id,),
    )]


def resolve_listing_report(conn, *, report_id, staff_id):
    row = conn.execute(
        "SELECT post_id FROM job_listing_reports WHERE id = ? AND status = 'pending'",
        (report_id,),
    ).fetchone()
    if not row:
        raise ListingReportError("This report is already closed or could not be found.", 404)
    updated = conn.execute(
        "UPDATE job_listing_reports SET status = 'reviewed', reviewed_by = ?, reviewed_at = datetime('now','localtime') "
        "WHERE id = ? AND status = 'pending'",
        (staff_id, report_id),
    ).rowcount
    if not updated:
        raise ListingReportError("This report has already been reviewed.", 404)
    return row["post_id"]
