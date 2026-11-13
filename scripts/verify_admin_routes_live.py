"""
scripts/verify_admin_routes_live.py
Verify authenticated rendering of all admin routes on EC2.
"""
import subprocess

EC2_HOST = "ubuntu@3.26.237.171"
SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"

remote_code = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session

token = create_session("admin@dbert.in", "admin")
client = app.test_client()

routes = [
    '/admin/job-applications',
    '/admin/stipend-funnel',
    '/admin/companies',
    '/admin/cohorts',
    '/admin/course-payments',
    '/admin/ledger',
    '/admin/post-hire-deposits',
    '/admin/articles',
    '/admin/ambassador-payouts',
    '/admin/sourcing-dashboard',
]

print('=== PROBING AUTHENTICATED ADMIN ROUTES ON FLASK ===')
for r in routes:
    res = client.get(r, headers={'X-Session-Token': token})
    is_ok = res.status_code == 200
    badge = 'PASS' if is_ok else 'FAIL'
    print(f'[{badge}] {r:30} -> HTTP {res.status_code} ({len(res.data)} bytes)')
    if not is_ok:
        print('   Error preview:', res.data[:200])
"""

def main():
    p = subprocess.Popen([
        "ssh", "-i", SSH_KEY,
        "-o", "StrictHostKeyChecking=no",
        EC2_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 -"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = p.communicate(input=remote_code)
    print(out)
    if err:
        print("STDERR:", err)

if __name__ == "__main__":
    main()
