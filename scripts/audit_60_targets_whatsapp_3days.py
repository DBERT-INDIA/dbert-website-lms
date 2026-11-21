import sqlite3
import json
import csv
import os
import re
from datetime import datetime

# 1. Regenerate full list of 60 ₹299 targets exactly as in generate_marketing_and_data_analytics.py
with open("data/active_15d_interns.json", "r", encoding="utf-8") as f:
    active_interns = json.load(f)

with open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
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

verified_299_emails = set()
if os.path.exists("data/verification_submissions_299.json"):
    with open("data/verification_submissions_299.json", "r", encoding="utf-8") as f:
        v299 = json.load(f)
        for x in v299:
            if x.get("email"):
                verified_299_emails.add(x["email"].strip().lower())

balance_1500_emails = set()
if os.path.exists("data/balance_enrollments_1500.json"):
    with open("data/balance_enrollments_1500.json", "r", encoding="utf-8") as f:
        b1500 = json.load(f)
        for x in b1500:
            if x.get("email"):
                balance_1500_emails.add(x["email"].strip().lower())

for u in active_interns:
    em = u["email"]
    cinfo = email_to_cert.get(em)
    u["cert_info"] = cinfo
    u["has_cert"] = cinfo is not None
    u["is_cert_verified"] = cinfo.get("verified", False) if cinfo else False
    u["is_cert_provisional"] = cinfo.get("isProvisional", False) if cinfo else False
    u["paid_299"] = em in verified_299_emails
    u["paid_1500"] = em in balance_1500_emails

targets_299 = []
for u in active_interns:
    if u.get("paid_299") or u.get("paid_1500"):
        continue
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
print(f"Total ₹299 Target Queue Candidates: {len(targets_299)}")

def normalize_phone(p):
    if not p:
        return ""
    digits = re.sub(r"\D", "", str(p))
    if len(digits) >= 10:
        return digits[-10:]
    return digits

# 2. Gather ALL WhatsApp sent records across all sources
all_whatsapp_sent = []

# Source A: data/dbert_whatsapp.db (whatsapp_sent_log)
if os.path.exists("data/dbert_whatsapp.db"):
    conn = sqlite3.connect("data/dbert_whatsapp.db")
    c = conn.cursor()
    c.execute("SELECT id, candidate_id, holder_name, user_email, clean_phone, cert_id, account_group, whatsapp_sent_at FROM whatsapp_sent_log;")
    for r in c.fetchall():
        all_whatsapp_sent.append({
            "source_file": "dbert_whatsapp.db:whatsapp_sent_log",
            "name": r[2],
            "email": (r[3] or "").strip().lower(),
            "phone": normalize_phone(r[4]),
            "cert_id": r[5],
            "sent_at": str(r[7])
        })
    # Source B: stipend_dispatch_log
    c.execute("SELECT id, intern_id, name, email, phone, cert_id, account_used, status, sent_at FROM stipend_dispatch_log;")
    for r in c.fetchall():
        if r[7] in ("SENT", "SUCCESS", "SENT_AUTO_LINKED", "SENT_OK") or not r[7] or "FAIL" not in str(r[7]).upper():
            all_whatsapp_sent.append({
                "source_file": "dbert_whatsapp.db:stipend_dispatch_log",
                "name": r[2],
                "email": (r[3] or "").strip().lower(),
                "phone": normalize_phone(r[4]),
                "cert_id": r[5],
                "sent_at": str(r[8])
            })
    # Source C: whatsapp_dispatch (if marked SENT)
    c.execute("SELECT candidate_id, holder_name, user_email, clean_phone, cert_id, whatsapp_status, whatsapp_sent_at FROM whatsapp_dispatch WHERE whatsapp_status='SENT';")
    for r in c.fetchall():
        all_whatsapp_sent.append({
            "source_file": "dbert_whatsapp.db:whatsapp_dispatch",
            "name": r[1],
            "email": (r[2] or "").strip().lower(),
            "phone": normalize_phone(r[3]),
            "cert_id": r[4],
            "sent_at": str(r[6])
        })
    conn.close()

# Source D: data/dispatch_tracking_stipend_299.csv
if os.path.exists("data/dispatch_tracking_stipend_299.csv"):
    with open("data/dispatch_tracking_stipend_299.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("status") in ("SENT", "SENT_AUTO_LINKED", "SUCCESS"):
                all_whatsapp_sent.append({
                    "source_file": "dispatch_tracking_stipend_299.csv",
                    "name": r.get("name"),
                    "email": (r.get("email") or "").strip().lower(),
                    "phone": normalize_phone(r.get("phone")),
                    "cert_id": r.get("cert_id"),
                    "sent_at": r.get("sent_at") or r.get("timestamp") or ""
                })

# Source E: EC2 whatsapp logs
ec2_files = [
    "data/whatsapp_70_selected_sent_log.json",
    "data/whatsapp_followup_sent_log.json",
    "data/whatsapp_stipend_10_dispatch.json",
    "data/dbert_whatsapp_sent_today.json"
]
for ef in ec2_files:
    if os.path.exists(ef):
        try:
            with open(ef, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for item in data:
                        status = item.get("status") or item.get("whatsapp_status") or "SENT"
                        all_whatsapp_sent.append({
                            "source_file": ef,
                            "name": item.get("name") or item.get("holder_name"),
                            "email": (item.get("email") or item.get("user_email") or "").strip().lower(),
                            "phone": normalize_phone(item.get("phone") or item.get("clean_phone")),
                            "cert_id": item.get("cert_id"),
                            "status": status,
                            "type": item.get("type") or item.get("campaign"),
                            "account": item.get("account") or item.get("account_used") or item.get("account_group"),
                            "sent_at": str(item.get("sent_at") or item.get("whatsapp_sent_at") or item.get("timestamp") or "")
                        })
                elif isinstance(data, dict):
                    for k, item in data.items():
                        if isinstance(item, dict):
                            status = item.get("status") or item.get("whatsapp_status") or "SENT"
                            all_whatsapp_sent.append({
                                "source_file": ef,
                                "name": item.get("name") or item.get("holder_name"),
                                "email": (item.get("email") or item.get("user_email") or "").strip().lower(),
                                "phone": normalize_phone(item.get("phone") or item.get("clean_phone")),
                                "cert_id": item.get("cert_id"),
                                "status": status,
                                "type": item.get("type") or item.get("campaign"),
                                "account": item.get("account") or item.get("account_used") or item.get("account_group"),
                                "sent_at": str(item.get("sent_at") or item.get("whatsapp_sent_at") or item.get("timestamp") or "")
                            })
        except Exception as ex:
            print(f"Error reading {ef}: {ex}")

print(f"Total WhatsApp Sent Records Indexed across all sources: {len(all_whatsapp_sent)}")

# Filter records to last 3 days: >= '2026-11-17 00:00:00'
THRESHOLD_DATE = "2026-11-17"
sent_3d = []
for s in all_whatsapp_sent:
    sat = s.get("sent_at") or ""
    # Check if timestamp contains 2026-11-17, 2026-11-18, 2026-11-19, or 2026-11-20
    is_recent = False
    for day in ["2026-11-17", "2026-11-18", "2026-11-19", "2026-11-20"]:
        if day in sat:
            is_recent = True
            break
    if is_recent:
        sent_3d.append(s)

print(f"WhatsApp Sent Records in Last 3 Days (>= {THRESHOLD_DATE}): {len(sent_3d)}")

# Build lookup by phone, email
sent_3d_phones = set()
sent_3d_emails = set()
sent_records_by_key = {}

for s in sent_3d:
    p = s["phone"]
    e = s["email"]
    if p:
        sent_3d_phones.add(p)
        sent_records_by_key[p] = s
    if e:
        sent_3d_emails.add(e)
        sent_records_by_key[e] = s

# Also track all-time sent phones & emails
all_time_phones = {s["phone"] for s in all_whatsapp_sent if s.get("phone")}
all_time_emails = {s["email"] for s in all_whatsapp_sent if s.get("email")}

print("\n=======================================================")
print("=== AUDIT: 60 ₹299 TARGET LEADS VS WHATSAPP MESSAGES ===")
print("=======================================================")

contacted_in_last_3_days = []
contacted_older = []
never_contacted = []

for i, t in enumerate(targets_299, 1):
    em = t["email"]
    ph = normalize_phone(t.get("phone"))
    name = t["name"]
    cid = t["cert_info"]["certId"] if t.get("cert_info") else "No Cert"
    score = t["intent_score"]
    
    # Check if in last 3 days
    match_3d = None
    if ph and ph in sent_3d_phones:
        match_3d = sent_records_by_key[ph]
    elif em and em in sent_3d_emails:
        match_3d = sent_records_by_key[em]
        
    if match_3d:
        contacted_in_last_3_days.append({
            "target": t,
            "rank": i,
            "sent_record": match_3d
        })
    else:
        # Check all time
        is_all_time = (ph and ph in all_time_phones) or (em and em in all_time_emails)
        if is_all_time:
            contacted_older.append({
                "target": t,
                "rank": i
            })
        else:
            never_contacted.append({
                "target": t,
                "rank": i
            })

print(f"\nRESULTS OUT OF 60 ₹299 TARGET LEADS:")
print(f"  1. Contacted via WhatsApp in LAST 3 DAYS: {len(contacted_in_last_3_days)}")
print(f"  2. Contacted via WhatsApp BEFORE last 3 days: {len(contacted_older)}")
print(f"  3. NEVER Contacted via WhatsApp: {len(never_contacted)}")

print("\n--- 1. CONTACTED IN LAST 3 DAYS (Nov 17 - Nov 20) ---")
for x in contacted_in_last_3_days:
    t = x["target"]
    s = x["sent_record"]
    cid = t["cert_info"]["certId"] if t.get("cert_info") else "No Cert"
    status = s.get("status", "SENT")
    campaign = s.get("type", "N/A")
    account = s.get("account", "N/A")
    print(f"  #{x['rank']:2d} | {t['name'][:24]:24s} | {t['email']:30s} | Phone: {t['phone']} | Status: {status} | Type: {campaign} | Acc: {account} | Sent: {s['sent_at'][:19]} | Cert: {cid}")

print("\n--- 2. CONTACTED PRIOR TO LAST 3 DAYS ---")
for x in contacted_older:
    t = x["target"]
    cid = t["cert_info"]["certId"] if t.get("cert_info") else "No Cert"
    # Find last sent date
    ph = normalize_phone(t.get("phone"))
    em = t["email"]
    prev_s = [s for s in all_whatsapp_sent if (ph and s.get("phone") == ph) or (em and s.get("email") == em)]
    last_sent = prev_s[-1].get("sent_at", "") if prev_s else "N/A"
    src = prev_s[-1].get("source_file", "") if prev_s else "N/A"
    print(f"  #{x['rank']:2d} | {t['name'][:24]:24s} | {t['email']:30s} | Phone: {t['phone']} | Last Sent: {last_sent[:19]} | Source: {src} | Cert: {cid}")

print(f"\n--- 3. UNCONTACTED / FRESH LEADS READY FOR IMMEDIATE OUTREACH ({len(never_contacted)} candidates) ---")
for x in never_contacted:
    t = x["target"]
    cid = t["cert_info"]["certId"] if t.get("cert_info") else "No Cert"
    logins = t.get("recent_logins", 0)
    print(f"  #{x['rank']:2d} | {t['name'][:24]:24s} | {t['email']:30s} | Phone: {t['phone']} | Logins(15d): {logins} | Score: {t['intent_score']} | Cert: {cid}")
