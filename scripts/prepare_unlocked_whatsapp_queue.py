import os
import sys
import json
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SUBMISSIONS_FILE = DATA_DIR / "verification_submissions_299.json"
REGISTRY_FILE = PROJECT_ROOT / "apps" / "website" / "src" / "data" / "certificates_registry.json"
DIRECTORY_FILE = PROJECT_ROOT / "apps" / "website" / "src" / "data" / "directory_candidates.json"

QUEUE_ACC1_FILE = DATA_DIR / "whatsapp_unlocked_queue_acc1.json"
QUEUE_ACC2_FILE = DATA_DIR / "whatsapp_unlocked_queue_acc2.json"

# Load submissions, registry, directory
with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
    submissions = json.load(f)

with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {item["certId"]: item for item in directory}

# The 17 candidates from Nov 20, 2026 (index 4 onwards)
today_subs = submissions[4:]
print(f"Loaded {len(today_subs)} submissions from Nov 20, 2026.")

now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

# Ensure all 17 are APPROVED in submissions and VERIFIED in registry/directory
for s in today_subs:
    cid = s.get("certId")
    name = s.get("fullName")
    s["status"] = "APPROVED"
    if not s.get("approvedAt"):
        s["approvedAt"] = now_iso
    s["verifiedAt"] = now_iso
    s["adminRemarks"] = "Payment verified, certificate officially upgraded to VERIFIED, and Gate 1 unlocked."

    if cid in registry:
        c_rec = registry[cid]
        c_rec["verified"] = True
        c_rec["isProvisional"] = False
        c_rec["status"] = "VERIFIED"
        c_rec["previewUrl"] = f"/certificates/previews/{cid}.png"

    first_letter = name.strip()[0].upper()
    if not first_letter.isalpha():
        first_letter = "#"

    c_info = registry.get(cid, {})
    dir_entry = {
        "certId": cid,
        "internId": c_info.get("internId", f"DBERT-2026-INT-{cid[-4:]}"),
        "holderName": c_info.get("holderName", name),
        "domain": c_info.get("domain", s.get("domain")),
        "duration": c_info.get("duration", "August to October 2026 (2 Months)"),
        "score": c_info.get("score", 85),
        "grade": c_info.get("grade", "Grade: A+ (Outstanding Performance)"),
        "isProvisional": False,
        "status": "VERIFIED",
        "firstLetter": first_letter,
        "verifyUrl": f"/verify/{cid}"
    }
    if cid in dir_map:
        dir_map[cid].update(dir_entry)
    else:
        directory.append(dir_entry)
        dir_map[cid] = dir_entry

# Save updated files
with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(submissions, f, indent=2, ensure_ascii=False)

with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)

print("Saved updated submissions, registry, and directory.")

# Build WhatsApp Messages for all 17 candidates
queue_all = []

for idx, s in enumerate(today_subs, 1):
    cid = s.get("certId")
    name = s.get("fullName", "").strip()
    raw_phone = s.get("phone", "")
    email = s.get("email", "").strip().lower()
    
    clean_digits = "".join(filter(str.isdigit, str(raw_phone)))[-10:]
    clean_phone = f"91{clean_digits}"
    
    # Capitalize first name
    name_parts = name.split()
    first_name = name_parts[0].capitalize() if name_parts else "Candidate"
    
    # Determine custom status by candidate
    if cid == "CERT-DBERT-2026-FSD-156":
        # Bhargavi Poola (In incubation sprints towards Jan 2027)
        gate2_str = "⏳ Active In Sprints (49 days remaining · Program Completion: 08 Jan 2027)"
        schedule_str = "Unlocks upon January 2027 milestone completion for capstone disbursement"
        next_step_str = "Track live incubation sprints on the LMS Stipend Dashboard:"
    elif cid == "CERT-DBERT-2026-DA-186":
        # Deepanshu (7 days remaining until Nov 27)
        gate2_str = "⏳ In Progress (7 days remaining · Official Completion: 27 Nov 2026)"
        schedule_str = "Unlocks on 27 Nov 2026 for immediate capstone milestone submission"
        next_step_str = "Track live milestone status on the LMS Stipend Dashboard:"
    elif cid == "CERT-DBERT-2026-AIML-002":
        # Shanmukha Sri Saikumar Medisetty (Already verified for 30 Dec 2026 release)
        gate2_str = "✅ PASSED (Completed on 10 July 2026)"
        schedule_str = "✅ Verified for Release: 30 December 2026"
        next_step_str = "Track live coin ledger & payout schedule on LMS Stipend Dashboard:"
    else:
        # Standard completed candidate
        reg_c = registry.get(cid, {})
        end_date = reg_c.get("endDate", "October 2026")
        gate2_str = f"✅ PASSED (Completed: {end_date})"
        schedule_str = "Ready for immediate milestone submission & disbursement scheduling"
        next_step_str = "Track live coin ledger & submit your capstone milestone on the LMS Stipend Dashboard:"

    msg = f"""Hello {first_name},

🎉 Congratulations! Your official DBERT Engineering Proof Dossier is now fully UNLOCKED and verified.

You are now officially listed on the Pre-Vetted Engineers Directory as "Available for Hire":
⭐ Pre-Vetted Directory:
https://dbert.in/verify/directory

🔒 Your Unlocked Proof Dossier:
https://dbert.in/verify/{cid}

📊 Live Stipend Milestone Progress (₹5,499 Withdrawable):
• Gate 1 (Credential Verification): ✅ PASSED (100-pt rubric & Turnitin clearance verified)
• Gate 2 (60-Day Sprint Completion): {gate2_str}
• Gate 3 (Payout UPI Account): ✅ Active & Encrypted
• Scheduled Release: {schedule_str}

👉 {next_step_str}
https://lms.dbert.in/stipend/tasks

Admissions & Engineering Concierge · DBERT Labs (https://dbert.in)"""

    # Validate first-15-lines rule
    lines = msg.strip().split("\n")
    dir_line = -1
    verify_line = -1
    for l_idx, line in enumerate(lines, 1):
        if "https://dbert.in/verify/directory" in line:
            dir_line = l_idx
        if f"https://dbert.in/verify/{cid}" in line:
            verify_line = l_idx

    assert dir_line > 0 and dir_line <= 15, f"Directory URL on line {dir_line} > 15!"
    assert verify_line > 0 and verify_line <= 15, f"Verify URL on line {verify_line} > 15!"
    assert "dbert.online" not in msg, "Found dbert.online in message!"

    item = {
        "index": idx,
        "name": name,
        "first_name": first_name,
        "clean_phone": clean_phone,
        "email": email,
        "cert_id": cid,
        "dir_line": dir_line,
        "verify_line": verify_line,
        "message": msg
    }
    queue_all.append(item)

# Partition into Account 1 (odd) and Account 2 (even)
queue_acc1 = [q for i, q in enumerate(queue_all) if i % 2 == 0]  # indices 0, 2, 4... (1st, 3rd...)
queue_acc2 = [q for i, q in enumerate(queue_all) if i % 2 != 0]  # indices 1, 3, 5... (2nd, 4th...)

with open(QUEUE_ACC1_FILE, "w", encoding="utf-8") as f:
    json.dump(queue_acc1, f, indent=2, ensure_ascii=False)

with open(QUEUE_ACC2_FILE, "w", encoding="utf-8") as f:
    json.dump(queue_acc2, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully built queues:")
print(f"  Account 1 ({len(queue_acc1)} candidates): {QUEUE_ACC1_FILE}")
print(f"  Account 2 ({len(queue_acc2)} candidates): {QUEUE_ACC2_FILE}")

print("\nCandidate Summary:")
for q in queue_all:
    print(f"  #{q['index']:2d} | {q['name']:<28} | +{q['clean_phone']} | {q['cert_id']} | DirL:{q['dir_line']} VerL:{q['verify_line']}")
