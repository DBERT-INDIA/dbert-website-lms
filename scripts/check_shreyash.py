import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

script = """
import os, sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    shreyash = conn.execute("SELECT id, name, email FROM intern_accounts WHERE email LIKE '%shreyash%'").fetchall()
    print("Shreyash accounts:", [dict(s) for s in shreyash])
    if shreyash:
        sid = shreyash[0]['id']
        subs = conn.execute("SELECT * FROM task_submissions WHERE intern_id = ?", (sid,)).fetchall()
        print("Task submissions:", [dict(s) for s in subs])
"""

cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, f"cat << 'EOF' > /tmp/check_shreyash.py\n{script}\nEOF\n/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/check_shreyash.py"]
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
