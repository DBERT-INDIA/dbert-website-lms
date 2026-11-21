import sys
import json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')

from app import app, get_db

with app.app_context():
    with get_db() as conn:
        print("=== PAYMENT EVENTS ===")
        events = conn.execute("SELECT * FROM payment_events ORDER BY id DESC").fetchall()
        for e in events:
            print(dict(e))

        print("\n=== RECENT SECURITY DEPOSITS (LAST 10) ===")
        deposits = conn.execute("SELECT * FROM security_deposits ORDER BY id DESC LIMIT 10").fetchall()
        for d in deposits:
            print(dict(d))

# Also check balance_enrollments_1500.json
json_path = "/var/www/dbert-website-lms/data/balance_enrollments_1500.json"
try:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"\n=== BALANCE ENROLLMENTS 1500 (Total {len(data)}) ===")
    for item in data:
        sub_at = item.get("submittedAt", "")
        print(f"ID: {item.get('id')} | Name: {item.get('fullName')} | Email: {item.get('email')} | Phone: {item.get('phone')} | SubmittedAt: {sub_at} | AmountPaid: {item.get('amountPaid')} | UTR: {item.get('utrNumber')} | Status: {item.get('status')}")
except Exception as ex:
    print("Error reading balance_enrollments_1500.json:", ex)
