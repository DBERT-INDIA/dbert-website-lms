import sys, os
from dotenv import load_dotenv
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session, AUTH_COOKIE
from services.database.adapter import get_db_adapter

app.config["TESTING"] = True
app.config["SESSION_COOKIE_DOMAIN"] = None
app.config["SESSION_COOKIE_SECURE"] = False
client = app.test_client()

token = create_session("admin@dbert.in", role="admin")
client.set_cookie(AUTH_COOKIE, token)

with client.session_transaction() as sess:
    sess["_csrf"] = "admin-csrf-token"
    sess["admin_id"] = 1
    sess["role"] = "admin"

print("Simulating admin call to /admin/enrollment/review for enrollment 454...")
res = client.post(
    "/admin/enrollment/review",
    json={"enrollment_id": 454, "action": "accept", "note": "Verified via test"},
    headers={"X-CSRF-Token": "admin-csrf-token"}
)

print("HTTP Status:", res.status_code)
print("Response JSON:", res.get_json())
