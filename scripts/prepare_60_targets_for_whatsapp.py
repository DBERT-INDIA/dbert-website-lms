import json
import re
import os
from pathlib import Path

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")
DATA_DIR = PROJECT_ROOT / "data"

with open(DATA_DIR / "active_15d_interns.json", "r", encoding="utf-8") as f:
    active_interns = json.load(f)

with open(PROJECT_ROOT / "apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
    certs = json.load(f)

email_to_cert = {}
for cid, cdata in certs.items():
    em = (cdata.get("email") or "").strip().lower()
    if em:
        email_to_cert[em] = {
            "certId": cid,
            "verified": cdata.get("verified", False),
            "isProvisional": cdata.get("isProvisional", False),
            "score": cdata.get("score"),
            "domain": cdata.get("domain")
        }

# Filter out test accounts and invalid phones
all_real = []
for u in active_interns:
    em = u.get("email", "").strip().lower()
    if "dbert.test" in em:
        continue
    raw_phone = u.get("phone", "")
    digits = re.sub(r"\D", "", str(raw_phone))
    clean = digits[-10:] if len(digits) >= 10 else ""
    if not clean or len(clean) != 10 or "98765" in clean:
        continue

    cinfo = email_to_cert.get(em)
    u["cert_info"] = cinfo
    score = 0
    reasons = []
    if cinfo and cinfo.get("isProvisional"):
        score += 50
        reasons.append("Provisional Cert Holder")
    if u.get("has_upi"):
        score += 25
        reasons.append("Configured Payout UPI ID")
    if u.get("tasks_count", 0) > 0:
        score += 20
        reasons.append(f"{u['tasks_count']} Task Submissions")
    if u.get("login_count", 0) >= 5:
        score += 15
        reasons.append(f"High Frequency Logins ({u['login_count']})")
    elif u.get("login_count", 0) >= 2:
        score += 10
        reasons.append(f"Active Logins ({u['login_count']})")
    if u.get("apps_count", 0) > 0:
        score += 10
        reasons.append(f"Applied to {u['apps_count']} Posts")

    u["intent_score"] = score
    u["intent_reasons"] = reasons
    u["clean_phone"] = f"91{clean}"
    all_real.append(u)

# Sort descending by intent score
all_real.sort(key=lambda x: x["intent_score"], reverse=True)
top60 = all_real[:60]

print(f"Total valid real candidates: {len(all_real)}")
print(f"Top 60 selected. Lowest intent score in Top 60: {top60[-1]['intent_score']}")

# Build WhatsApp message queue
TEMPLATE = """Hello {name},

Regarding your {domain} Internship at DBERT:
Your milestone progress has been verified. To clear Gate 3 (Credential Verification) and unlock your ₹5,000 Milestone Stipend, please complete your official verification (₹299).

🌐 View Pre-Vetted Engineers Directory:
https://dbert.in/verify/directory

👉 Instant Verification & Stipend Unlock:
https://dbert.in/verify/unlock?certid={cert_id}&email={email}

Admissions & Verification Concierge (https://dbert.in)"""

queue_acc1 = []
queue_acc2 = []

for idx, u in enumerate(top60):
    cinfo = u.get("cert_info")
    cert_id = cinfo.get("certId") if cinfo else f"DBERT-VERIFY-{u['id']}"
    domain = u.get("domain") or (cinfo.get("domain") if cinfo else "Engineering Track")
    
    # Capitalize candidate first name
    name_parts = u["name"].strip().split()
    first_name = name_parts[0].capitalize() if name_parts else "Candidate"
    
    msg = TEMPLATE.format(
        name=first_name,
        domain=domain,
        cert_id=cert_id,
        email=u["email"].strip()
    )
    
    item = {
        "candidate_id": u["id"],
        "name": u["name"].strip(),
        "first_name": first_name,
        "email": u["email"].strip(),
        "phone": u["phone"],
        "clean_phone": u["clean_phone"],
        "domain": domain,
        "cert_id": cert_id,
        "intent_score": u["intent_score"],
        "intent_reasons": u["intent_reasons"],
        "message": msg,
        "type": "299_CREDENTIAL_VERIFICATION"
    }
    
    # 30 for Account 1, 30 for Account 2
    if idx % 2 == 0:
        item["assigned_account"] = 1
        queue_acc1.append(item)
    else:
        item["assigned_account"] = 2
        queue_acc2.append(item)

print(f"Queue Account 1: {len(queue_acc1)} candidates")
print(f"Queue Account 2: {len(queue_acc2)} candidates")

# Save queues
with open(DATA_DIR / "whatsapp_299_queue_acc1.json", "w", encoding="utf-8") as f:
    json.dump(queue_acc1, f, indent=2)

with open(DATA_DIR / "whatsapp_299_queue_acc2.json", "w", encoding="utf-8") as f:
    json.dump(queue_acc2, f, indent=2)

with open(DATA_DIR / "whatsapp_299_queue_master.json", "w", encoding="utf-8") as f:
    json.dump(top60, f, indent=2)

print("Saved queues to:")
print("  - data/whatsapp_299_queue_acc1.json")
print("  - data/whatsapp_299_queue_acc2.json")
print("  - data/whatsapp_299_queue_master.json")
