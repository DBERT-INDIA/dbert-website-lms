import subprocess
import json

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

remote_py = """
import os, sys, json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    rows = conn.execute('''
        SELECT a.id, a.intern_id, a.domain, a.title, a.status, a.published_url, a.created_at, a.updated_at,
               a.github_repo_url, a.live_demo_url, a.rubric_score, a.stipend_status,
               LENGTH(COALESCE(a.content_markdown, '')) as content_len,
               LEFT(COALESCE(a.content_markdown, ''), 150) as content_preview,
               i.name as intern_name, i.email as intern_email
        FROM intern_articles a
        LEFT JOIN intern_accounts i ON a.intern_id = i.id
        ORDER BY a.status ASC, a.id ASC
    ''').fetchall()
    
    articles = [dict(r) for r in rows]
    print(json.dumps(articles, default=str))
"""

cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, f"cat << 'EOF' > /tmp/analyze_articles.py\n{remote_py}\nEOF\n/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/analyze_articles.py"]
res = subprocess.run(cmd, capture_output=True, text=True)

try:
    articles = json.loads(res.stdout)
    print(f"Total articles retrieved: {len(articles)}")
    pending = [a for a in articles if a['status'] == 'PENDING_REVIEW']
    published = [a for a in articles if a['status'] == 'PUBLISHED']
    other = [a for a in articles if a['status'] not in ('PENDING_REVIEW', 'PUBLISHED')]
    
    print(f"PENDING_REVIEW: {len(pending)}")
    print(f"PUBLISHED: {len(published)}")
    print(f"OTHER: {len(other)}")
    print("\n=== PENDING_REVIEW QUEUE ===")
    for p in pending:
        print(f"ID {p['id']}: '{p['title']}' | Intern: {p['intern_name']} ({p['intern_email']}) | Domain: {p['domain']} | Len: {p['content_len']}")
        print(f"   GitHub: {p['github_repo_url']} | Demo: {p['live_demo_url']}")
        print(f"   Preview: {p['content_preview']}...")
        print()
except Exception as e:
    print("Error parsing JSON:", e)
    print("RAW STDOUT:\n", res.stdout)
    if res.stderr:
        print("RAW STDERR:\n", res.stderr)
