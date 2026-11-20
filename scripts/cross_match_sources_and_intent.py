import json
import os
import sqlite3

# Load intern accounts
with open("data/all_intern_accounts.json", "r", encoding="utf-8") as f:
    interns = json.load(f)

# Load campaign files
campaign_409_emails = set()
if os.path.exists("data/all_409_provisional_registry.json"):
    with open("data/all_409_provisional_registry.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            if x.get("email"):
                campaign_409_emails.add(x["email"].strip().lower())

sheet_1593_emails = set()
if os.path.exists("data/sheet_1593_provisional_registry.json"):
    with open("data/sheet_1593_provisional_registry.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            if x.get("email"):
                sheet_1593_emails.add(x["email"].strip().lower())

sheet_859_emails = set()
if os.path.exists("data/sheet_859_registry.json"):
    with open("data/sheet_859_registry.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            if x.get("email"):
                sheet_859_emails.add(x["email"].strip().lower())

stipend_wa_emails = set()
if os.path.exists("data/whatsapp_stipend_299_pending.json"):
    with open("data/whatsapp_stipend_299_pending.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        for x in data:
            if x.get("email"):
                stipend_wa_emails.add(x["email"].strip().lower())

whatsapp_db_phones = set()
if os.path.exists("data/dbert_whatsapp.db"):
    try:
        conn = sqlite3.connect("data/dbert_whatsapp.db")
        c = conn.cursor()
        c.execute("SELECT recipient_phone FROM whatsapp_dispatch;")
        for r in c.fetchall():
            whatsapp_db_phones.add(r[0])
        conn.close()
    except:
        pass

# Also load certificates registry
verified_cert_emails = set()
if os.path.exists("apps/website/src/data/certificates_registry.json"):
    with open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
        certs = json.load(f)
        for cid, cdata in certs.items():
            if cdata.get("email") and cdata.get("verified"):
                verified_cert_emails.add(cdata["email"].strip().lower())

print(f"Loaded Campaign Email Sets:")
print(f"  409 Provisional Campaign Emails: {len(campaign_409_emails)}")
print(f"  1593 Sheet Campaign Emails:      {len(sheet_1593_emails)}")
print(f"  859 Sheet Campaign Emails:       {len(sheet_859_emails)}")
print(f"  Stipend WhatsApp Campaign Emails:{len(stipend_wa_emails)}")
print(f"  Verified Certificate Holders:    {len(verified_cert_emails)}")

# Cross match each intern
source_counts = {
    "Email Campaign (409 Provisional)": 0,
    "Sheet 1593 Ingestion / Campaign": 0,
    "Sheet 859 Campaign": 0,
    "Stipend WhatsApp Campaign": 0,
    "Organic / Direct LMS Registration": 0
}

matched_interns = []

for u in interns:
    email = u["email"]
    src = "Organic / Direct LMS Registration"
    if email in campaign_409_emails:
        src = "Email Campaign (409 Provisional)"
    elif email in stipend_wa_emails:
        src = "Stipend WhatsApp Campaign"
    elif email in sheet_1593_emails:
        src = "Sheet 1593 Ingestion / Campaign"
    elif email in sheet_859_emails:
        src = "Sheet 859 Campaign"
    
    source_counts[src] += 1
    u["source"] = src
    matched_interns.append(u)

print("\n==================================================")
print("=== SOURCE BREAKDOWN (Out of 2,947 Interns) ===")
print("==================================================")
for src, cnt in source_counts.items():
    pct = (cnt / len(interns)) * 100
    print(f"  {src:35s}: {cnt:4d} ({pct:5.1f}%)")

# Breakdown by stage within each source
print("\n=== STAGES BY SOURCE ===")
for src in source_counts.keys():
    stage_breakdown = {}
    for u in matched_interns:
        if u["source"] == src:
            st = str(u.get("signup_stage"))
            stage_breakdown[st] = stage_breakdown.get(st, 0) + 1
    print(f"  {src}:")
    for st, c in sorted(stage_breakdown.items()):
        print(f"    Stage {st}: {c}")

with open("data/matched_interns_source.json", "w", encoding="utf-8") as f:
    json.dump(matched_interns, f, indent=2)
print("\nSaved matched sources to data/matched_interns_source.json")
