#!/usr/bin/env python3
"""
DBERT — Audit & Sync Intern GitHub PRs, LinkedIn URLs, and Real-Time Gate Notifications
Supports --dry-run (default) and --live.
"""

import argparse
import os
import sys
from pathlib import Path
import psycopg2
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
PORTAL_DIR = REPO_ROOT / "apps" / "portal"
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from services.github_verifier import GitHubVerifier
from services.linkedin_verifier import LinkedInVerifier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Commit changes to PostgreSQL")
    args = parser.parse_args()

    for env_path in [
        "/var/www/dbert-website-lms/apps/portal/.env",
        str(PORTAL_DIR / ".env"),
    ]:
        if os.path.exists(env_path):
            load_dotenv(env_path)
            break

    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL not found.")
        sys.exit(1)

    conn = psycopg2.connect(db_url)
    c = conn.cursor()
    c.execute("SET search_path TO dbert_internship, public;")

    # 1. Normalize LinkedIn URLs for all 299-verified interns
    c.execute("""
        SELECT DISTINCT ia.id, ia.name, LOWER(ia.email), ia.linkedin_url, ia.verified_github_org, ia.verified_github_repo
        FROM intern_accounts ia
        LEFT JOIN intern_certificates ic ON ia.id = ic.intern_id
        WHERE ic.tier = 'verified' OR ia.stipend_verified = 1;
    """)
    verified_interns = c.fetchall()
    li_normalized = 0
    for iid, name, email, li_url, v_org, v_repo in verified_interns:
        if li_url and li_url.strip():
            ok, canonical = LinkedInVerifier.validate_url(li_url)
            if ok and canonical != li_url.strip():
                li_normalized += 1
                if args.live:
                    c.execute(
                        "UPDATE intern_accounts SET linkedin_url = %s, updated_at = NOW() WHERE id = %s;",
                        (canonical, iid),
                    )

    # 2. Audit all pending task_submissions
    c.execute("""
        SELECT s.id, s.intern_id, ia.name, LOWER(ia.email), s.github_repo_url, s.status
        FROM task_submissions s
        JOIN intern_accounts ia ON ia.id = s.intern_id
        WHERE s.status = 'pending'
        ORDER BY s.id DESC;
    """)
    pending_subs = c.fetchall()
    print(f"Found {len(pending_subs)} pending task_submissions to audit.")

    pr_verified = 0
    marked_changes_requested = 0
    notified = 0

    for sub_id, iid, name, email, gh_url, status in pending_subs:
        cls = GitHubVerifier.classify_url(gh_url)
        if cls["status"] == "OFFICIAL_PR":
            api_res = GitHubVerifier.verify_pr_via_api(cls["org"], cls["repo"], cls["pr_number"])
            if api_res.get("exists"):
                pr_verified += 1
                print(f"  [VERIFIED PR] sub={sub_id} {name}: {cls['org']}/{cls['repo']}#{cls['pr_number']} merged={api_res.get('merged')}")
                if args.live:
                    c.execute(
                        """
                        UPDATE intern_accounts
                        SET verified_github_org = %s, verified_github_repo = %s, updated_at = NOW()
                        WHERE id = %s AND (COALESCE(verified_github_org, '') = '' OR COALESCE(verified_github_repo, '') = '');
                        """,
                        (cls["org"], f"{cls['org']}/{cls['repo']}", iid),
                    )
            else:
                marked_changes_requested += 1
                note = f"Submitted Pull Request #{cls['pr_number']} on {cls['org']}/{cls['repo']} could not be found on GitHub (HTTP {api_res.get('status_code')}). Please verify your PR URL and resubmit."
                print(f"  [PR NOT FOUND] sub={sub_id} {name}: {gh_url}")
                if args.live:
                    _flag_submission(c, sub_id, iid, note)
                    notified += 1
        elif cls["status"] in ("MISSING", "NON_GITHUB_URL", "INVALID_FORMAT", "PROFILE_ONLY", "OFFICIAL_REPO_NO_PR", "FORK_NO_PR", "UNOFFICIAL_REPO", "UNOFFICIAL_PR"):
            marked_changes_requested += 1
            note = f"{cls['message']} Please open and submit a valid Pull Request (/pull/<id>) on one of DBERT's 4 official product repositories (Alkameinc, Gayatri-Education, Aivaratechinfomatics, or DBERT-INDIA)."
            print(f"  [{cls['status']}] sub={sub_id} {name}: {gh_url}")
            if args.live:
                _flag_submission(c, sub_id, iid, note)
                notified += 1

    if args.live:
        conn.commit()
        print(f"COMMITTED: li_normalized={li_normalized}, pr_verified={pr_verified}, marked_changes_requested={marked_changes_requested}, notified={notified}")
    else:
        conn.rollback()
        print(f"DRY RUN: li_normalized={li_normalized}, pr_verified={pr_verified}, would_mark_changes_requested={marked_changes_requested}")

    conn.close()


def _flag_submission(c, sub_id: int, intern_id: int, note: str):
    c.execute(
        """
        UPDATE task_submissions
        SET status = 'changes_requested',
            ai_evaluation_notes = %s
        WHERE id = %s;
        """,
        (note, sub_id),
    )
    c.execute(
        """
        INSERT INTO notifications (intern_id, kind, title, body, link, is_read, created_at)
        VALUES (%s, 'warning', 'Action Required: Update GitHub PR URL', %s, '/stipend/tasks', 0, NOW()::text);
        """,
        (intern_id, note),
    )


if __name__ == "__main__":
    main()
