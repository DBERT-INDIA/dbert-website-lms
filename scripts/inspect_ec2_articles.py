import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

remote_code = '''
import sqlite3, os

paths = [
    "/var/www/dbert-website-lms/apps/portal/internship.db",
    "/var/www/dbert-website-lms/apps/portal/portal.db",
    "/var/www/dbert-website-lms/data/portal.db",
    "/var/www/dbert-website-lms/apps/portal/dbert.db"
]

for p in paths:
    if os.path.exists(p):
        try:
            conn = sqlite3.connect(p)
            tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type=?", ("table",)).fetchall()]
            if "intern_articles" in tables:
                rows = conn.execute("SELECT id, intern_id, domain, title, status, published_url, created_at, updated_at FROM intern_articles").fetchall()
                print(f"=== DB {p}: {len(rows)} intern_articles ===")
                for r in rows:
                    print(f"  ID={r[0]} | InternID={r[1]} | Status={r[4]} | Domain={r[2]} | Title={r[3][:60]}")
        except Exception as e:
            print(f"Error {p}: {e}")
'''

cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, f"python3 -c '{remote_code}'"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
