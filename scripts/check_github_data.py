import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

conn = get_db()
cur = conn.cursor()
cur.execute("SELECT name, email, github_url FROM intern_accounts WHERE github_url IS NOT NULL AND github_url != ''")
rows = cur.fetchall()
print(f"Total intern accounts with GitHub URLs: {len(rows)}")
for r in rows:
    print(f"* {r[0]} ({r[1]}): {r[2]}")

cur.execute("SELECT to_regclass('public.task_submissions')")
if cur.fetchone()[0]:
    cur.execute("SELECT id, intern_id, submission_url, github_repo_url FROM task_submissions WHERE (submission_url IS NOT NULL AND submission_url != '') OR (github_repo_url IS NOT NULL AND github_repo_url != '')")
    subs = cur.fetchall()
    print(f"\nTask Submissions with GitHub ({len(subs)}):")
    for s in subs:
        print(s)
