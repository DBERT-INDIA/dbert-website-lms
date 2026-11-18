import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

script = """
import os, sys
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import app, session, task_generate_content, create_session

token = create_session("bhargavi13032007@gmail.com", "intern")

with app.test_request_context(
    '/api/tasks/101/generate-content',
    method='POST',
    json={'task_id': 101},
    headers={'X-Session-Token': token, 'X-CSRF-Token': 'tok'}
):
    session['_csrf'] = 'tok'
    session['email'] = 'bhargavi13032007@gmail.com'

    resp = task_generate_content(101)
    data = resp.get_json() if hasattr(resp, 'get_json') else resp
    print("task_generate_content(101) output:")
    if isinstance(data, dict):
        print("  Status:", data.get("status"))
        print("  Model used:", data.get("model_used"))
        print("  Angle:", data.get("angle", {}).get("title"))
        print("  Copy preview:", (data.get("copy") or "")[:250].replace('\\n', ' '))
    else:
        print("  Raw:", data)
"""

with open("scripts/remote_test_func.py", "w") as f:
    f.write(script)

subprocess.run(f'scp -i "{SSH_KEY}" scripts/remote_test_func.py {HOST}:/tmp/test_func.py', shell=True)
res = subprocess.run(f'ssh -i "{SSH_KEY}" {HOST} "/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/test_func.py"', shell=True, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
