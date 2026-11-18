import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

script = """
import os, sys, json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    rows = conn.execute("SELECT id, title, published_url, status, domain FROM intern_articles WHERE status = 'PUBLISHED' ORDER BY id ASC").fetchall()
    print(f"=== Published Articles ({len(rows)}) ===")
    for r in rows:
        print(f"ID={r['id']} | Title={r['title']} | Domain={r['domain']} | URL={r['published_url']}")
"""

cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, f"cat << 'EOF' > /tmp/check_published.py\n{script}\nEOF\n/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/check_published.py"]
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
