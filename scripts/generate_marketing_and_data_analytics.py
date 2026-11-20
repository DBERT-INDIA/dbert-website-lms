import json
import os
import sqlite3
from collections import Counter

# Load active 15-day interns
with open("data/active_15d_interns.json", "r", encoding="utf-8") as f:
    active_interns = json.load(f)

# Load matched sources
with open("data/matched_interns_source.json", "r", encoding="utf-8") as f:
    all_interns = json.load(f)

# Load certificates registry
with open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
    certs = json.load(f)

# Map certificates by email and certId
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

# Load existing 299 verification submissions
verified_299_emails = set()
if os.path.exists("data/verification_submissions_299.json"):
    with open("data/verification_submissions_299.json", "r", encoding="utf-8") as f:
        v299 = json.load(f)
        for x in v299:
            if x.get("email"):
                verified_299_emails.add(x["email"].strip().lower())

# Load existing 1500 balance enrollments
balance_1500_emails = set()
if os.path.exists("data/balance_enrollments_1500.json"):
    with open("data/balance_enrollments_1500.json", "r", encoding="utf-8") as f:
        b1500 = json.load(f)
        for x in b1500:
            if x.get("email"):
                balance_1500_emails.add(x["email"].strip().lower())

print(f"Total Active Interns (Last 15 Days): {len(active_interns)}")
print(f"Existing 299 Paid Submissions: {len(verified_299_emails)}")
print(f"Existing 1500 Balance Paid: {len(balance_1500_emails)}")

# Cross match active interns with cert status and payment status
for u in active_interns:
    em = u["email"]
    cinfo = email_to_cert.get(em)
    u["cert_info"] = cinfo
    u["has_cert"] = cinfo is not None
    u["is_cert_verified"] = cinfo.get("verified", False) if cinfo else False
    u["is_cert_provisional"] = cinfo.get("isProvisional", False) if cinfo else False
    u["paid_299"] = em in verified_299_emails
    u["paid_1500"] = em in balance_1500_emails

# Segment active interns
provisional_active = [u for u in active_interns if u.get("is_cert_provisional") and not u.get("paid_299")]
print(f"\nActive Interns with Provisional Certificate (Pending ₹299 Unlock): {len(provisional_active)}")

# Top Prime Targets for 299:
# 1. Active interns who have a provisional certificate and have logged in in last 15 days
# 2. Interns with UPI setup or task submissions who need verification to unlock stipend
targets_299 = []
for u in active_interns:
    if u.get("paid_299") or u.get("paid_1500"):
        continue
    # Score intent: logins + tasks + has_upi + cert
    score = 0
    reasons = []
    if u.get("is_cert_provisional"):
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
    
    if score >= 30:
        u["intent_score"] = score
        u["intent_reasons"] = reasons
        targets_299.append(u)

targets_299.sort(key=lambda x: x["intent_score"], reverse=True)
print(f"\nPrime Targets for ₹299 Payment: {len(targets_299)} high-intent candidates")
for i, t in enumerate(targets_299[:15], 1):
    cert_str = t['cert_info']['certId'] if t.get('cert_info') else 'No Cert'
    print(f" {i:2d}. {t['name'][:22]:22s} | {t['email']:30s} | Score: {t['intent_score']:3d} | Logins: {t['login_count']:2d} | Cert: {cert_str:24s} | Reasons: {', '.join(t['intent_reasons'])}")

# Top Prime Targets for 499 (Caution Deposit / Incubation Entry):
# Who are the candidates for ₹499?
# - Candidates who are in Stage 2, or Stage 3 with account_status in ('Selected', 'pending_approval', 'deposit_pending', 'active')
# - They have applied to posts or completed onboarding, logged in recently, but haven't paid caution deposit
targets_499 = []
for u in active_interns:
    if u.get("paid_1500"):
        continue
    # For 499 caution deposit, we target candidates who are actively pursuing the fellowship/internship
    score = 0
    reasons = []
    if str(u.get("signup_stage")) in ["2", "3"]:
        score += 20
        reasons.append(f"Stage {u['signup_stage']}")
    if u.get("account_status") in ["Selected", "pending_approval", "deposit_pending"]:
        score += 30
        reasons.append(f"Status '{u['account_status']}'")
    if u.get("apps_count", 0) >= 2:
        score += 25
        reasons.append(f"{u['apps_count']} Post Applications")
    elif u.get("apps_count", 0) == 1:
        score += 15
        reasons.append(f"1 Post Application")
    if u.get("login_count", 0) >= 5:
        score += 20
        reasons.append(f"{u['login_count']} Logins in 15d")
    elif u.get("login_count", 0) >= 2:
        score += 10
        reasons.append(f"{u['login_count']} Logins in 15d")
    if u.get("terms_accepted"):
        score += 10
        reasons.append("Terms Accepted")
        
    if score >= 35 and not u.get("is_cert_verified"):
        u["caution_score"] = score
        u["caution_reasons"] = reasons
        targets_499.append(u)

targets_499.sort(key=lambda x: x["caution_score"], reverse=True)
print(f"\nPrime Targets for ₹499 Caution Deposit: {len(targets_499)} high-intent candidates")
for i, t in enumerate(targets_499[:25], 1):
    print(f" {i:2d}. {t['name'][:22]:22s} | {t['email']:30s} | Domain: {str(t['domain'])[:20]:20s} | Score: {t['caution_score']:3d} | Logins: {t['login_count']:2d} | Reasons: {', '.join(t['caution_reasons'])}")

# Save targeted cohorts
with open("data/top_targets_299.json", "w", encoding="utf-8") as f:
    json.dump(targets_299[:30], f, indent=2)

with open("data/top_targets_499.json", "w", encoding="utf-8") as f:
    json.dump(targets_499[:40], f, indent=2)

print("\nSaved top targets to data/top_targets_299.json and data/top_targets_499.json")
