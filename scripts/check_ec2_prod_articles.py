import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

# Remote python code
remote_py = """
import os, sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    rows = conn.execute('''
        SELECT a.id, a.intern_id, a.domain, a.title, a.status, a.published_url, a.created_at, a.updated_at,
               a.github_repo_url, a.live_demo_url, a.content_markdown,
               i.name as intern_name, i.email as intern_email
        FROM intern_articles a
        LEFT JOIN intern_accounts i ON a.intern_id = i.id
        ORDER BY a.id ASC
    ''').fetchall()
    print(f"=== Total Articles in EC2 PostgreSQL: {len(rows)} ===")
    for r in rows:
        d = dict(r)
        print(f"ID={d['id']} | Status={d['status']} | Intern={d['intern_name']} <{d['intern_email']}>")
        print(f"   Domain: {d['domain']} | Title: {d['title']}")
        print(f"   URL: {d['published_url']} | GitHub: {d['github_repo_url']} | Demo: {d['live_demo_url']}")
        content_preview = (d.get('content_markdown') or '')[:120].replace('\\n', ' ')
        print(f"   Content Preview: {content_preview}...")
        print("-" * 60)
"""

# Write script to EC2 and execute
scp_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, f"cat << 'EOF' > /tmp/check_articles.py\n{remote_py}\nEOF\n/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/check_articles.py"]
res = subprocess.run(scp_cmd, capture_output=True, text=True)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
