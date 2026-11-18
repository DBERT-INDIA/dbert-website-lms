
import os, sys
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import app, _enforce_csrf, session, CSRF_HEADER, CSRF_FIELD
from flask import request

with app.test_request_context('/api/tasks/101/generate-content', method='POST', headers={'X-CSRF-Token': 'my_token'}):
    session['_csrf'] = 'my_token'
    print("Expected:", repr(session.get('_csrf')))
    print("Supplied:", repr(request.headers.get(CSRF_HEADER)))
    res = _enforce_csrf()
    print("_enforce_csrf() result:", res)
