import json
import csv
import urllib.parse
import re

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"

def clean_phone(phone_str):
    if not phone_str:
        return ""
    digits = re.sub(r'\D', '', str(phone_str))
    if len(digits) > 10 and digits.startswith('91'):
        digits = digits[2:]
    elif len(digits) > 10 and digits.startswith('0'):
        digits = digits[1:]
    return digits[-10:] if len(digits) >= 10 else digits

# Load cohort data
with open("data/linkedin_stipend_cohort_results.json", "r", encoding="utf-8") as f:
    cohort_data = json.load(f)

with open("data/provisional_completed_linkedin.json", "r", encoding="utf-8") as f:
    prov_38 = json.load(f)

# Candidates to message (strictly NOT present in Google Sheet)
# Tier 1: Strict 3 (Uday Bhasker, Kethavath Sruthi, Badugu Venkata Rajesh)
# Tier 2: In-sprints 2 (Jyothi Lalam, A Omeshwar Reddy)
# Tier 3: Completed provisional fellows (excluding Sruthi & Rajesh already in Tier 1)

candidates_to_message = []

# Tier 1
strict_ids = [2089, 4083, 4757]
for c in cohort_data.get("strict_only_299_pending", []):
    if c["id"] in strict_ids:
        c["priority_tier"] = "TIER_1_STRICT_100_READY"
        candidates_to_message.append(c)

# Tier 2
sprint_ids = [4523, 5217]
for c in cohort_data.get("linkedin_upi_unverified", []):
    if c["id"] in sprint_ids:
        c["priority_tier"] = "TIER_2_IN_SPRINTS_UPI_READY"
        candidates_to_message.append(c)

# Tier 3
existing_ids = {c["id"] for c in candidates_to_message}
for c in prov_38:
    if c["id"] not in existing_ids:
        c["priority_tier"] = "TIER_3_COMPLETED_PROVISIONAL_FELLOWS"
        candidates_to_message.append(c)

print(f"Total candidates queued for WhatsApp dispatch: {len(candidates_to_message)}")

# Generate formatted messages & 1-tap links
records = []
for c in candidates_to_message:
    c_id = c.get("id")
    name = (c.get("name") or "Candidate").strip()
    email = (c.get("email") or "").strip().lower()
    phone = clean_phone(c.get("phone"))
    domain = c.get("domain") or "Engineering"
    cert_id = c.get("cert_id") or ""
    tier = c.get("priority_tier")
    
    if cert_id:
        unlock_url = f"https://dbert.in/enroll/1999?certid={cert_id}&fee=299"
        verify_url = f"https://dbert.in/verify?certid={cert_id}"
    else:
        unlock_url = f"https://dbert.in/enroll/1999?email={email}&fee=299"
        verify_url = "https://dbert.in/verify"

    # WhatsApp message adhering to first 15 lines constraint
    msg = (
        f"🎓 *DBERT Milestone Stipend (₹5,000) & Credential Notice*\n"
        f"\n"
        f"Dear {name},\n"
        f"\n"
        f"Congratulations! Your DBERT internship tenure and LinkedIn profile have been recorded.\n"
        f"\n"
        f"🔗 *Verification & Dossier URL (Line 8):*\n"
        f"👉 {verify_url}\n"
        f"\n"
        f"📝 *Official ₹299 Verification & Claim Form (Line 11):*\n"
        f"👉 {unlock_url}\n"
        f"\n"
        f"💰 *₹5,000 Stipend Unlock Status:*\n"
        f"• *Tenure Completed:* Yes\n"
        f"• *LinkedIn Profile:* Linked & Recorded\n"
        f"• *Pending Action:* Complete ₹299 project evaluation to release your official 3-doc credential packet and unlock ₹5,000 LMS stipend submission.\n"
        f"\n"
        f"📜 *Next Steps:*\n"
        f"1️⃣ Tap your claim link: {unlock_url}\n"
        f"2️⃣ Confirm your ₹299 verification fee via UPI QR.\n"
        f"3️⃣ Submit your milestone contribution on LMS at https://lms.dbert.in/stipend/tasks for automated 5,000 coins release.\n"
        f"\n"
        f"Best regards,\n"
        f"*Abhinav Sharma*\n"
        f"Program Head & Project Mentor\n"
        f"*DBERT — Digital Blinc Education Research And Technology*\n"
        f"🌐 https://dbert.in"
    )

    encoded_text = urllib.parse.quote(msg)
    wa_direct_link = f"https://wa.me/91{phone}?text={encoded_text}"

    records.append({
        "intern_id": c_id,
        "name": name,
        "email": email,
        "phone": f"+91{phone}",
        "raw_phone": phone,
        "domain": domain,
        "cert_id": cert_id,
        "tier": tier,
        "unlock_url": unlock_url,
        "verify_url": verify_url,
        "wa_direct_link": wa_direct_link,
        "message": msg
    })

# Export to CSV
csv_path = "data/whatsapp_stipend_299_pending.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "intern_id", "name", "email", "phone", "raw_phone", "domain", 
        "cert_id", "tier", "unlock_url", "verify_url", "wa_direct_link"
    ])
    writer.writeheader()
    for r in records:
        row_copy = dict(r)
        del row_copy["message"]
        writer.writerow(row_copy)

# Export to JSON
json_path = "data/whatsapp_stipend_299_pending.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

print(f"Generated CSV at {csv_path}")
print(f"Generated JSON at {json_path}")
