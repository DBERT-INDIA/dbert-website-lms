import sys, os
from dotenv import load_dotenv
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from services.notifications.web_push_service import dispatch_lifecycle_push
import time

print("Dispatching test push to stage3_selected@dbert.test...")
dispatch_lifecycle_push(
    event_name="self_test",
    target_email="stage3_selected@dbert.test",
    title="🔔 DBERT Push Test",
    body="Your device is connected and receiving real-time cryptographic notifications!",
    url="https://lms.dbert.in/account/notifications",
    sync_inapp=True
)

time.sleep(3)
from services.database.adapter import get_db_adapter
with get_db_adapter() as db:
    log = db.execute("SELECT id, event_name, target_email, delivery_status, status_code, error_message, created_at FROM web_push_delivery_logs WHERE target_email = 'stage3_selected@dbert.test' ORDER BY id DESC LIMIT 1").fetchone()
    print("DELIVERY RESULT:", dict(log) if log else "No log found")
    dev = db.execute("SELECT id, user_email, last_pushed_at, is_active FROM web_push_devices WHERE id = 5").fetchone()
    print("DEVICE STATUS:", dict(dev) if dev else "No device")
