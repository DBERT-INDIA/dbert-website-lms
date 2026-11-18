
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
        print("  Copy preview:", (data.get("copy") or "")[:250].replace('\n', ' '))
    else:
        print("  Raw:", data)
