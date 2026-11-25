"""Explicit learner selections for public CV evidence."""

import json
from urllib.parse import urlsplit


def init_verified_portfolio(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS verified_portfolio (
        intern_id INTEGER PRIMARY KEY,
        project_ids_json TEXT NOT NULL,
        credential_ids_json TEXT NOT NULL
    )""")
    conn.commit()


def _github_repository(url):
    try:
        address = urlsplit(url)
        return address.scheme == "https" and address.netloc == "github.com" and bool(address.path.strip("/"))
    except ValueError:
        return False


def verified_choices(conn, intern_id, email):
    projects = [dict(row) for row in conn.execute(
        """SELECT id, project_title, github_repo_url FROM project_submissions
           WHERE intern_id = ? AND status = 'approved' ORDER BY id DESC LIMIT 50""", (intern_id,),
    ).fetchall() if _github_repository(row["github_repo_url"])]
    credentials = [dict(row) for row in conn.execute(
        """SELECT id, course_title, cert_id, issued_at FROM intern_certificates WHERE credential_status = 'valid'
             AND cert_id IS NOT NULL AND
                 (intern_id = ? OR (email IS NOT NULL AND email <> '' AND LOWER(email) = LOWER(?)))
           ORDER BY id DESC LIMIT 50""", (intern_id, email),
    ).fetchall()]
    for credential in credentials:
        credential["url"] = "/portal/certificate/" + credential["cert_id"]
    return projects, credentials


def read_portfolio_selection(conn, intern_id):
    row = conn.execute("SELECT * FROM verified_portfolio WHERE intern_id = ?", (intern_id,)).fetchone()
    if not row:
        return set(), set()
    return set(json.loads(row["project_ids_json"])), set(json.loads(row["credential_ids_json"]))


def write_portfolio_selection(conn, intern_id, projects, credentials):
    conn.execute(
        """INSERT INTO verified_portfolio (intern_id, project_ids_json, credential_ids_json) VALUES (?, ?, ?)
           ON CONFLICT(intern_id) DO UPDATE SET project_ids_json = excluded.project_ids_json,
               credential_ids_json = excluded.credential_ids_json RETURNING intern_id""",
        (intern_id, json.dumps(sorted(projects)), json.dumps(sorted(credentials))),
    )


def published_portfolio(conn, intern_id, email):
    projects, credentials = read_portfolio_selection(conn, intern_id)
    if not projects and not credentials:
        return [], []
    available_projects, available_credentials = verified_choices(conn, intern_id, email)
    return ([item for item in available_projects if item["id"] in projects],
            [item for item in available_credentials if item["id"] in credentials])
