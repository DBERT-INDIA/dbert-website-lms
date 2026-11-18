import subprocess
PEM_PATH = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

REMOTE_SCRIPT = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    print('intern_accounts matching fellow or 9105:')
    rows = conn.execute("SELECT id, email, name FROM intern_accounts WHERE id=9105 OR email LIKE '%fellow%' OR email LIKE '%eshan%' OR email LIKE '%stage5%'").fetchall()
    for r in rows:
        print(dict(r))
"""

p = subprocess.Popen(['ssh', '-i', PEM_PATH, '-o', 'StrictHostKeyChecking=no', REMOTE_HOST, '/var/www/dbert-website-lms/apps/portal/.venv/bin/python', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = p.communicate(input=REMOTE_SCRIPT)
print(stdout)
if stderr:
    print("STDERR:", stderr)
