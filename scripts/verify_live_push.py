import sys, os, json
from dotenv import load_dotenv
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session, AUTH_COOKIE
from services.database.adapter import get_db_adapter
import time

app.config["TESTING"] = True
app.config["SESSION_COOKIE_DOMAIN"] = None
app.config["SESSION_COOKIE_SECURE"] = False
client = app.test_client()

token = create_session("stage3_selected@dbert.test", role="intern")
client.set_cookie(AUTH_COOKIE, token)

with client.session_transaction() as sess:
    sess["_csrf"] = "verify-csrf-token"

print("1. Calling POST /api/push/test as stage3_selected@dbert.test...")
res = client.post(
    "/api/push/test",
    json={
        "title": "🔔 DBERT Push Test",
        "body": "Your device is connected and receiving real-time cryptographic notifications!",
        "url": "/account/notifications"
    },
    headers={"X-CSRF-Token": "verify-csrf-token"}
)

print("HTTP Status:", res.status_code)
print("Response JSON:", res.get_json())
assert res.status_code == 200
assert res.get_json()["status"] == "success"

time.sleep(2)
with get_db_adapter() as db:
    log = db.execute("SELECT id, event_name, target_email, delivery_status, status_code, created_at FROM web_push_delivery_logs WHERE target_email = 'stage3_selected@dbert.test' ORDER BY id DESC LIMIT 1").fetchone()
    print("Latest Telemetry Log:", dict(log) if log else "None")
    dev = db.execute("SELECT id, user_email, device_name, last_pushed_at FROM web_push_devices WHERE user_email = 'stage3_selected@dbert.test'").fetchone()
    print("Device Status:", dict(dev) if dev else "None")

print("\n✓ Live verification for stage3_selected@dbert.test completed successfully!")
