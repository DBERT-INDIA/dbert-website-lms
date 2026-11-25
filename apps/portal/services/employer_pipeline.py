"""Employer-owned applicant interviews and role closure."""

from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit


IST = timezone(timedelta(hours=5, minutes=30), "IST")


class PipelineError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def interview_form_value(stored):
    if not stored:
        return ""
    return datetime.fromisoformat(stored).astimezone(IST).strftime("%Y-%m-%dT%H:%M")


def _interview_terms(start, link, note):
    try:
        date = datetime.strptime(start, "%Y-%m-%dT%H:%M").replace(tzinfo=IST)
    except (TypeError, ValueError):
        raise PipelineError("Choose an interview date and time in IST.") from None
    if date <= datetime.now(IST):
        raise PipelineError("Choose a future interview time.")
    link, note = link.strip(), note.strip()
    if link:
        try:
            parsed = urlsplit(link)
            valid_link = (parsed.scheme == "https" and parsed.hostname and not parsed.username
                          and not parsed.password and not any(c.isspace() or ord(c) < 32 for c in link))
        except ValueError:
            valid_link = False
        if not valid_link or len(link) > 500:
            raise PipelineError("Enter a valid HTTPS meeting link or leave it blank.")
    if len(note) > 1000:
        raise PipelineError("Keep interview instructions under 1,000 characters.")
    return date.astimezone(timezone.utc).isoformat(), link or None, note or None


def update_employer_interview(conn, *, company_id, app_id, start="", link="", note="", cancel=False):
    params = (None, None, None) if cancel else _interview_terms(start, link, note)
    can_schedule = " AND status NOT IN ('Hired', 'Rejected')" if not cancel else ""
    updated = conn.execute(
        "UPDATE post_applications SET employer_interview_at = ?, employer_interview_link = ?, employer_interview_note = ? "
        "WHERE id = ? AND EXISTS (SELECT 1 FROM posts p WHERE p.id = post_applications.post_id "
        "AND p.company_id = ? AND p.status <> 'deleted')" + can_schedule,
        (*params, app_id, company_id),
    ).rowcount
    if not updated:
        raise PipelineError("Choose an application you can manage.", 404)
    return conn.execute("SELECT post_id FROM post_applications WHERE id = ?", (app_id,)).fetchone()["post_id"]


def mark_position_filled(conn, *, post_id, company_id):
    changed = conn.execute(
        "UPDATE posts SET status = 'filled', updated_at = datetime('now','localtime') "
        "WHERE id = ? AND company_id = ? AND status = 'published'",
        (post_id, company_id),
    ).rowcount
    if changed:
        return
    existing = conn.execute("SELECT status FROM posts WHERE id = ? AND company_id = ?", (post_id, company_id)).fetchone()
    if existing is None:
        raise PipelineError("This role could not be found.", 404)
    if existing["status"] != "filled":
        raise PipelineError("Choose a published role to mark as filled.", 409)
