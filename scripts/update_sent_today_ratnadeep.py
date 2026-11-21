import json
from datetime import datetime
from pathlib import Path

p = Path("data/dbert_whatsapp_sent_today.json")
if p.exists():
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
else:
    d = []

d.append({
    "phone": "918591833879",
    "name": "Ratnadeep manojkumar bamane",
    "email": "ratnadeepratu737@gmail.com",
    "account": "Account 2",
    "campaign": "enrollment_confirmed_499",
    "status": "SENT",
    "timestamp": datetime.now().isoformat(),
    "details": "₹499 Payment Reconciled & Enrollment Confirmed via Account 2"
})

with open(p, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2)

print("Updated data/dbert_whatsapp_sent_today.json successfully.")
