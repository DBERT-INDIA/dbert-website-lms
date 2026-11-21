import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(os.path.abspath("scripts"))

from generate_sample_packet import (
    draw_cert_completion,
    draw_cert_evaluation,
    draw_cert_lor,
    safe_save_canvas,
    BASE_DIR
)

OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs", "cohort_2026")
WEBSITE_PREVIEWS_DIR = os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews")
REGISTRY_FILE = os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json")
DIRECTORY_FILE = os.path.join(BASE_DIR, "apps", "website", "src", "data", "directory_candidates.json")
VERIFICATION_SUBMISSIONS_FILE = os.path.join(BASE_DIR, "data", "verification_submissions_299.json")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(WEBSITE_PREVIEWS_DIR, exist_ok=True)

# Load Registries and Submissions
with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {item["certId"]: item for item in directory}

with open(VERIFICATION_SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
    ver_subs = json.load(f)

# The 14 newly submitted payments from Nov 20, 2026 (index 4 onwards)
new_submissions = ver_subs[4:]
print(f"Loaded {len(registry)} in cert registry, {len(directory)} in directory.")
print(f"Processing {len(new_submissions)} submissions from Nov 20, 2026...")

# Candidate specific data for 3-doc generation if needed
BHARGAVI_POOLA_DATA = {
    "index": 75,
    "name": "Bhargavi Poola",
    "email": "bhargavi13032007@gmail.com",
    "phone": "9603742553",
    "college": "Full Stack Incubation Scholar",
    "domain": "Full Stack Web Development",
    "batch": "Monday, 9 Nov 2026",
    "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
    "topics": "HTML5, CSS3, JavaScript, TypeScript, React, Next.js, Node.js, REST APIs, PostgreSQL, Docker",
    "duration": "9 Nov 2026 – 9 Jan 2027 (2 Months)",
    "start_date": "November 2026",
    "end_date": "January 2027",
    "eval_date": "09 November 2026",
    "issue_date": "2026-11-05",
    "cert_id": "CERT-DBERT-2026-FSD-156",
    "intern_id": "DBERT-2026-INT-1412",
    "score": 88,
    "grade": "Grade: A+ (Outstanding Performance)",
    "rubric_marks": [18, 9, 9, 8, 9, 9, 9, 8, 9],
    "source": "Website 299 Payment (UTR 283246783618)"
}

# Generate Bhargavi Poola 3-doc packet & preview PNG
cand_dir = os.path.join(OUTPUTS_DIR, "75_bhargavi_poola")
os.makedirs(cand_dir, exist_ok=True)
doc1_pdf = os.path.join(cand_dir, "1_Certificate_of_Completion_CERT-DBERT-2026-FSD-156.pdf")
doc2_pdf = os.path.join(cand_dir, "2_Academic_Project_Evaluation_CERT-DBERT-2026-FSD-156.pdf")
doc3_pdf = os.path.join(cand_dir, "3_Letter_of_Recommendation_CERT-DBERT-2026-FSD-156.pdf")

print("\nGenerating 3-Document Dossier for Bhargavi Poola...")
safe_save_canvas(None, doc1_pdf, draw_cert_completion, BHARGAVI_POOLA_DATA)
safe_save_canvas(None, doc2_pdf, draw_cert_evaluation, BHARGAVI_POOLA_DATA)
safe_save_canvas(None, doc3_pdf, draw_cert_lor, BHARGAVI_POOLA_DATA)

# Copy PNG preview to public website previews
doc1_png = doc1_pdf.replace(".pdf", ".png")
pub_png = os.path.join(WEBSITE_PREVIEWS_DIR, "CERT-DBERT-2026-FSD-156.png")
if os.path.exists(doc1_png):
    shutil.copy2(doc1_png, pub_png)
    print(f"  Preview PNG generated and copied to: {pub_png}")

approved_cids = set()
now_iso = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")

for s in new_submissions:
    cid = s.get("certId")
    name = s.get("fullName")
    utr = s.get("utrNumber")
    approved_cids.add(cid)
    
    print(f"\nUpgrading [{cid}] {name} (UTR: {utr})...")
    
    # 1. Update certificates_registry.json
    if cid in registry:
        c_rec = registry[cid]
        c_rec["verified"] = True
        c_rec["isProvisional"] = False
        c_rec["status"] = "VERIFIED"
        c_rec["verificationDate"] = "2026-11-20"
        c_rec["previewUrl"] = f"/certificates/previews/{cid}.png"
        if cid == "CERT-DBERT-2026-FSD-156":
            c_rec["doc1Pdf"] = doc1_pdf
            c_rec["doc2Pdf"] = doc2_pdf
            c_rec["doc3Pdf"] = doc3_pdf
    else:
        print(f"  Warning: {cid} not in certificates_registry.json, creating entry...")
        registry[cid] = {
            "certId": cid,
            "holderName": name,
            "email": s.get("email"),
            "college": s.get("college"),
            "domain": s.get("domain"),
            "verified": True,
            "isProvisional": False,
            "status": "VERIFIED",
            "verificationDate": "2026-11-20",
            "previewUrl": f"/certificates/previews/{cid}.png"
        }
    
    # 2. Update directory_candidates.json
    first_letter = name.strip()[0].upper()
    if not first_letter.isalpha():
        first_letter = "#"
        
    c_info = registry[cid]
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
        print(f"  Promoted in directory to Tab 1 (Verified · Ready to Hire)")
    else:
        directory.append(dir_entry)
        dir_map[cid] = dir_entry
        print(f"  Added to directory under Tab 1 (Verified · Ready to Hire)")

# 3. Update verification_submissions_299.json
for s in ver_subs:
    if s.get("certId") in approved_cids:
        s["status"] = "APPROVED"
        s["approvedAt"] = now_iso
        s["verifiedAt"] = now_iso
        s["adminRemarks"] = "Payment verified, certificate officially upgraded to VERIFIED, and Gate 1 unlocked."

# Save all updated files
with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)
print(f"\nSaved updated {REGISTRY_FILE} ({len(registry)} records)")

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)
print(f"Saved updated {DIRECTORY_FILE} ({len(directory)} records)")

with open(VERIFICATION_SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(ver_subs, f, indent=2, ensure_ascii=False)
print(f"Saved updated {VERIFICATION_SUBMISSIONS_FILE} ({len(ver_subs)} submissions)")

print("\nAll 14 candidates successfully upgraded to VERIFIED!")
