import subprocess
import json

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import psycopg2
import json

conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
c = conn.cursor()

c.execute("SELECT id, title, slug, description, responsibilities, skills, eligibility, published_at, apply_by, expires_at FROM dbert_internship.posts WHERE id IN (1, 16)")
cols = [col[0] for col in c.description]
for row in c.fetchall():
    d = dict(zip(cols, row))
    print(f"=== POST #{d['id']}: {d['title']} ===")
    print(f"Slug: {d['slug']}")
    print(f"Dates: published_at={d['published_at']}, apply_by={d['apply_by']}, expires_at={d['expires_at']}")
    print(f"Desc: {d['description'][:200]}...")
    print(f"Responsibilities: {d['responsibilities'][:200]}...")
    print(f"Skills: {d['skills']}")
    print(f"Eligibility: {d['eligibility']}")
    print()
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
