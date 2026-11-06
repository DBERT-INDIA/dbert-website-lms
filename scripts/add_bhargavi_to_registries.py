import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

REG_PATH = "apps/website/src/data/certificates_registry.json"
DIR_PATH = "apps/website/src/data/directory_candidates.json"

with open(REG_PATH, "r", encoding="utf-8") as f:
    reg = json.load(f)

with open(DIR_PATH, "r", encoding="utf-8") as f:
    directory = json.load(f)

cert_id = "CERT-DBERT-2026-FSD-156"
intern_id = "DBERT-2026-INT-1412"

bhargavi_reg = {
    "certId": cert_id,
    "internId": intern_id,
    "holderName": "Bhargavi Poola",
    "email": "bhargavi13032007@gmail.com",
    "phone": "9603742553",
    "college": "Full Stack Incubation Scholar",
    "domain": "Full Stack Web Development",
    "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
    "batch": "Monday, 9 Nov 2026",
    "duration": "9 Nov 2026 – 9 Jan 2027 (2 Months)",
    "startDate": "November 2026",
    "endDate": "January 2027",
    "issueDate": "2026-11-05",
    "evalDate": "09 November 2026",
    "score": 88,
    "grade": "Grade: A+ (Outstanding Performance)",
    "signatory": "Mr. Abhinav Sharma",
    "signatoryTitle": "Program Head & Project Mentor",
    "organization": "DBERT (Digital Blinc Education Research and Technology)",
    "verificationUrl": f"https://dbert.in/verify?certid={cert_id}",
    "verified": True,
    "isProvisional": False,
    "status": "Verified",
    "previewUrl": "/certificates/previews/sample_certificate_locked.png"
}

reg[cert_id] = bhargavi_reg

dir_entry = {
    "certId": cert_id,
    "internId": intern_id,
    "holderName": "Bhargavi Poola",
    "domain": "Full Stack Web Development",
    "duration": "9 Nov 2026 – 9 Jan 2027 (2 Months)",
    "score": 88,
    "grade": "Grade: A+ (Outstanding Performance)",
    "isProvisional": False,
    "status": "VERIFIED",
    "firstLetter": "B",
    "verifyUrl": f"/verify/{cert_id}"
}

# Check if in directory
found_dir = False
for i, d in enumerate(directory):
    if d.get("certId") == cert_id or d.get("holderName") == "Bhargavi Poola":
        directory[i] = dir_entry
        found_dir = True
        break
if not found_dir:
    directory.append(dir_entry)

directory.sort(key=lambda x: x.get("holderName", "").lower())

with open(REG_PATH, "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=2, ensure_ascii=False)

with open(DIR_PATH, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)

print(f"Added Bhargavi Poola to certificates_registry ({len(reg)} records) and directory ({len(directory)} records).")
