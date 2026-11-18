import subprocess
import json

remote_code = """
import sys, json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

conn = get_db()
c = conn.cursor()

# Get column names of intern_certificates
c.execute(\"\"\"
    SELECT column_name FROM information_schema.columns WHERE table_name = 'intern_certificates'
\"\"\")
cert_cols = [r[0] for r in c.fetchall()]

# Get all task submissions for stipend_milestone
c.execute(\"\"\"
    SELECT ts.id, ts.intern_id, ts.email, ts.github_repo_url, ts.live_demo_url, ts.status,
           ts.created_at, ts.ai_evaluation_score, ts.ai_evaluation_notes,
           ia.name, ia.domain, ia.upi_id_encrypted, ia.linkedin_url, ia.linkedin_verified,
           ia.stipend_verified, ia.stipend_release_date, ia.verified_github_org, ia.verified_github_repo
    FROM task_submissions ts
    JOIN intern_accounts ia ON ts.intern_id = ia.id
    WHERE ts.task_category = 'stipend_milestone'
    ORDER BY ts.id DESC
\"\"\")
submissions = []
for r in c.fetchall():
    submissions.append({
        'sub_id': r[0],
        'intern_id': r[1],
        'email': r[2],
        'github_repo_url': r[3],
        'live_demo_url': r[4],
        'sub_status': r[5],
        'created_at': str(r[6]),
        'ai_score': r[7],
        'ai_notes': r[8],
        'name': r[9],
        'domain': r[10],
        'has_upi': bool(r[11]),
        'linkedin_url': r[12],
        'linkedin_verified': bool(r[13]),
        'stipend_verified': bool(r[14]),
        'stipend_release_date': str(r[15]),
        'verified_github_org': r[16],
        'verified_github_repo': r[17]
    })

# Check published articles for these interns
c.execute(\"\"\"
    SELECT intern_id, cert_id, title, status, published_url
    FROM intern_articles
\"\"\")
articles_by_intern = {}
for r in c.fetchall():
    articles_by_intern[r[0]] = {
        'cert_id': r[1],
        'title': r[2],
        'status': r[3],
        'url': r[4]
    }

# Check intern certificates
c.execute(\"\"\"
    SELECT * FROM intern_certificates
\"\"\")
cert_rows = c.fetchall()
certs_by_intern = {}
for r in cert_rows:
    # map row with cert_cols
    d = dict(zip(cert_cols, r))
    for k, v in d.items():
        if hasattr(v, 'isoformat'): d[k] = str(v)
    certs_by_intern[d.get('intern_id')] = d

for s in submissions:
    iid = s['intern_id']
    s['article'] = articles_by_intern.get(iid)
    s['certificate'] = certs_by_intern.get(iid)

print(json.dumps({
    'cert_cols': cert_cols,
    'submissions_count': len(submissions),
    'submissions': submissions
}, indent=2))
"""

cmd = [
    "ssh",
    "-i", r"C:\Users\user\.ssh\dbert-production-server.pem",
    "-o", "StrictHostKeyChecking=no",
    "ubuntu@3.26.237.171",
    "/var/www/dbert-website-lms/apps/portal/.venv/bin/python",
    "-"
]

res = subprocess.run(cmd, input=remote_code, capture_output=True, text=True)
if res.returncode == 0:
    with open('data/ec2_stipend_submissions_audit.json', 'w', encoding='utf-8') as f:
        f.write(res.stdout)
    print("Saved EC2 stipend submissions audit to data/ec2_stipend_submissions_audit.json")
else:
    print("Error:", res.stderr)
