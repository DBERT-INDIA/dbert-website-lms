import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import psycopg2, os, json
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

c.execute(\"\"\"
    SELECT id, post_type, domain, title, slug, published_at, apply_by, expires_at, description, responsibilities, skills, eligibility 
    FROM dbert_internship.posts 
    WHERE expires_at::timestamp <= '2026-11-27 23:59:59'
    ORDER BY id ASC;
\"\"\")

rows = c.fetchall()
print(f"Found {len(rows)} expiring posts:")
posts = []
for r in rows:
    p = {
        "id": r[0],
        "post_type": r[1],
        "domain": r[2],
        "title": r[3],
        "slug": r[4],
        "published_at": str(r[5]),
        "apply_by": str(r[6]),
        "expires_at": str(r[7]),
        "desc_preview": (r[8] or "")[:80],
        "resp_preview": (r[9] or "")[:80],
        "skills": r[10],
        "elig_preview": (r[11] or "")[:80]
    }
    posts.append(p)
    print(f"[{p['id']}] {p['post_type']} | {p['domain']} | {p['title']} | slug: {p['slug']}")

with open("/tmp/expiring_43_posts.json", "w", encoding="utf-8") as f:
    json.dump([
        {
            "id": r[0],
            "post_type": r[1],
            "domain": r[2],
            "title": r[3],
            "slug": r[4],
            "published_at": str(r[5]),
            "apply_by": str(r[6]),
            "expires_at": str(r[7]),
            "description": r[8],
            "responsibilities": r[9],
            "skills": r[10],
            "eligibility": r[11]
        } for r in rows
    ], f, indent=2)
print("Saved full details to /tmp/expiring_43_posts.json on remote.")
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
