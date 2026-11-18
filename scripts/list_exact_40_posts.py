import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = """
import psycopg2

conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
c = conn.cursor()

c.execute("SELECT id, post_type, domain, title, company_id, location FROM dbert_internship.posts WHERE post_type='job' ORDER BY created_at ASC NULLS LAST, id ASC LIMIT 20")
jobs = c.fetchall()

c.execute("SELECT id, post_type, domain, title, company_id, location FROM dbert_internship.posts WHERE post_type='internship' ORDER BY created_at ASC NULLS LAST, id ASC LIMIT 20")
internships = c.fetchall()

print('JOBS (20):')
for j in jobs:
    print(f'  ID {j[0]}: [{j[2]}] {j[3]} ({j[5]})')

print('\\nINTERNSHIPS (20):')
for i in internships:
    print(f'  ID {i[0]}: [{i[2]}] {i[3]} ({i[5]})')
"""

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
