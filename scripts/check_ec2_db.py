import sys, os
from dotenv import load_dotenv
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from services.database.adapter import get_db_adapter

with get_db_adapter() as db:
    logs = db.execute("SELECT id, event_name, target_email, title, target_url, delivery_status, created_at FROM web_push_delivery_logs ORDER BY id DESC LIMIT 5").fetchall()
    print('LOGS COUNT:', len(logs))
    for l in logs:
        print(dict(l))
