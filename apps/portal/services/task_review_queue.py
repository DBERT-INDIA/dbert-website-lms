"""Bounded staff task queue and review history."""

from datetime import datetime, timedelta


STATUS_OPTIONS = (
    ("pending", "Pending review"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
)
AGE_OPTIONS = (("", "Any age"), ("24", "1 day"), ("72", "3 days"), ("168", "7 days"))
PAGE_SIZE = 25

SUBMISSION_JOIN = """
    FROM task_submissions ts
    JOIN tasks t ON ts.task_id = t.id
    JOIN intern_accounts a ON a.id = COALESCE(
        (SELECT account.id FROM intern_accounts account WHERE account.id = ts.intern_id),
        (SELECT account.id FROM intern_accounts account
         WHERE LOWER(account.email) = LOWER(ts.email) ORDER BY account.id LIMIT 1)
    )
"""

ARTICLE_JOIN = """
    LEFT JOIN intern_articles art ON art.id = COALESCE(
        (SELECT article.id FROM intern_articles article
         WHERE article.task_submission_id = ts.id ORDER BY article.id DESC LIMIT 1),
        (SELECT article.id FROM intern_articles article
         WHERE article.intern_id = ts.intern_id AND article.status = 'PUBLISHED'
         ORDER BY article.id DESC LIMIT 1)
    )
"""


def _timestamp(value):
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(value) if value else None
    except (TypeError, ValueError):
        return None


def _age_label(value, now):
    created = _timestamp(value)
    if created is None:
        return None
    if (created.tzinfo is None) != (now.tzinfo is None):
        if created.tzinfo is None:
            created = created.replace(tzinfo=now.tzinfo)
        else:
            now = now.replace(tzinfo=created.tzinfo)
    minutes = max(0, int((now - created).total_seconds() // 60))
    if minutes < 60:
        return "Under 1 hour"
    hours, days = minutes // 60, minutes // (60 * 24)
    if days:
        return f"{days}d {hours % 24}h"
    return f"{hours}h"


def _review_history(conn, submissions):
    if not submissions:
        return {}
    placeholders = ", ".join("?" for _ in submissions)
    sql = """
        SELECT r.subject_id, r.decision, r.reason_code, r.created_at, s.name AS reviewer
        FROM review_log r
        LEFT JOIN staff_accounts s ON s.id = r.staff_id
        WHERE r.queue_name = 'tasks' AND r.subject_type = 'task' AND r.subject_id IN ({})
        ORDER BY r.created_at DESC, r.id DESC
    """.format(placeholders)
    history = {}
    for row in conn.execute(sql, [item["id"] for item in submissions]):
        history.setdefault(row["subject_id"], []).append(dict(row))
    return history


def build_task_review_queue(conn, *, status, domain, age, page):
    """Return one page of unique submissions and the unfiltered pending totals."""
    status = status if status in dict(STATUS_OPTIONS) else "pending"
    domains = [row["target_domain"] for row in conn.execute(
        "SELECT DISTINCT target_domain FROM tasks "
        "WHERE target_domain IS NOT NULL AND target_domain <> '' ORDER BY target_domain"
    )]
    domain = domain if domain in domains else ""
    age = age if age in dict(AGE_OPTIONS) else ""
    now = _timestamp(conn.execute("SELECT datetime('now','localtime') AS now").fetchone()["now"])
    if now is None:
        now = datetime.now()

    pending = conn.execute(
        "SELECT COUNT(*) AS total, MIN(ts.created_at) AS oldest " + SUBMISSION_JOIN +
        " WHERE ts.status = 'pending'"
    ).fetchone()

    conditions = ["ts.status = ?"]
    values = [status]
    if domain:
        conditions.append("t.target_domain = ?")
        values.append(domain)
    if age:
        conditions.append("ts.created_at <= ?")
        cutoff = now - timedelta(hours=int(age))
        values.append(cutoff.isoformat(sep=" ", timespec="seconds"))
    where = " WHERE " + " AND ".join(conditions)

    total = conn.execute("SELECT COUNT(*) AS total " + SUBMISSION_JOIN + where, values).fetchone()["total"]
    page_count = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(1, min(page or 1, page_count))
    submissions = [dict(row) for row in conn.execute(
        "SELECT ts.*, t.title AS task_title, t.coin_reward, t.task_type, t.target_domain, "
        "t.payment_type, t.submission_type, a.name AS intern_name, a.email AS intern_email, "
        "art.status AS article_status, art.title AS article_title, art.published_url AS article_url "
        + SUBMISSION_JOIN + ARTICLE_JOIN + where +
        " ORDER BY ts.created_at IS NULL, ts.created_at ASC, ts.id ASC LIMIT ? OFFSET ?",
        values + [PAGE_SIZE, (page - 1) * PAGE_SIZE],
    )]
    history = _review_history(conn, submissions)
    for submission in submissions:
        submission["age_label"] = _age_label(submission["created_at"], now)
        submission["review_history"] = history.get(submission["id"], [])

    return {
        "status_options": STATUS_OPTIONS,
        "age_options": AGE_OPTIONS,
        "domains": domains,
        "status": status,
        "domain": domain,
        "age": age,
        "pending_count": pending["total"],
        "oldest_pending_age": _age_label(pending["oldest"], now),
        "total": total,
        "page": page,
        "page_count": page_count,
        "submissions": submissions,
    }
