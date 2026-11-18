import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

script = """
import os, sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    for aid in [44, 40, 9, 2]:
        r = conn.execute("SELECT id, intern_id, title, domain, content_markdown FROM intern_articles WHERE id = ?", (aid,)).fetchone()
        if r:
            d = dict(r)
            print(f"=== ID {d['id']}: {d['title']} ===")
            print(d['content_markdown'][:800])
            print("="*60)
"""

cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, f"cat << 'EOF' > /tmp/inspect_content.py\n{script}\nEOF\n/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/inspect_content.py"]
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
