import os
import sys
import json
import shutil
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

# Candidate 1: MOLUGU NANDA YASOVARDHAN
CAND1_DATA = {
    "index": 91,
    "name": "Molugu Nanda Yaso Vardhan",
    "email": "nandayasovardhan@gmail.com",
    "phone": "9493476662",
    "college": "Vishnu Institute of Technology",
    "domain": "Full Stack Web Development",
    "batch": "Aug to Oct 2026",
    "project": "Alkame Full Stack Platform — Enterprise Technical Suite",
    "topics": "React, Next.js, Node.js, Express, PostgreSQL, REST APIs, System Architecture, State Management",
    "duration": "15 August 2026 – 15 October 2026 (2 Months)",
    "start_date": "August 2026",
    "end_date": "October 2026",
    "eval_date": "15 October 2026",
    "issue_date": "2026-11-21",
    "cert_id": "CERT-DBERT-2026-FSD-341",
    "intern_id": "DBERT-2026-INT-2345",
    "score": 87,
    "grade": "Grade: A (Very Good Performance)",
    "rubric_marks": [17, 9, 9, 8, 9, 9, 9, 9, 8],
    "source": "Website 299 Payment (UTR 375725311685)"
}

# Candidate 2: H A UDAY BHASKER
CAND2_DATA = {
    "index": 92,
    "name": "H A Uday Bhasker",
    "email": "ubhoysala@gmail.com",
    "phone": "7036073368",
    "college": "Geethanjali College of Engineering and Technology",
    "domain": "Full Stack Web Development",
    "batch": "Aug to Oct 2026",
    "project": "Enterprise Cloud SaaS & Full Stack Platform",
    "topics": "React, Next.js, TypeScript, PostgreSQL, RESTful APIs, Tailwind CSS, Docker, Microservices",
    "duration": "15 August 2026 – 15 October 2026 (2 Months)",
    "start_date": "August 2026",
    "end_date": "October 2026",
    "eval_date": "15 October 2026",
    "issue_date": "2026-11-21",
    "cert_id": "CERT-DBERT-2026-FSD-342",
    "intern_id": "DBERT-2026-INT-2089",
    "score": 86,
    "grade": "Grade: A (Very Good Performance)",
    "rubric_marks": [17, 8, 9, 8, 9, 8, 9, 9, 9],
    "source": "Website 299 Payment (UTR 930768222270)"
}

new_candidates = [CAND1_DATA, CAND2_DATA]

print("=" * 70)
print("GENERATING 3-DOC CREDENTIAL PACKETS & PREVIEWS FOR 2 CANDIDATES")
print("=" * 70)

for cand in new_candidates:
    cid = cand["cert_id"]
    folder_name = f"{cand['index']}_{cand['name'].lower().replace(' ', '_')}"
    cand_dir = os.path.join(OUTPUTS_DIR, folder_name)
    os.makedirs(cand_dir, exist_ok=True)
    
    doc1_pdf = os.path.join(cand_dir, f"1_Certificate_of_Completion_{cid}.pdf")
    doc2_pdf = os.path.join(cand_dir, f"2_Academic_Project_Evaluation_{cid}.pdf")
    doc3_pdf = os.path.join(cand_dir, f"3_Letter_of_Recommendation_{cid}.pdf")
    
    print(f"\nGenerating dossier for {cand['name']} ({cid})...")
    safe_save_canvas(None, doc1_pdf, draw_cert_completion, cand)
    safe_save_canvas(None, doc2_pdf, draw_cert_evaluation, cand)
    safe_save_canvas(None, doc3_pdf, draw_cert_lor, cand)
    
    cand["doc1_pdf"] = doc1_pdf
    cand["doc2_pdf"] = doc2_pdf
    cand["doc3_pdf"] = doc3_pdf
    cand["cand_dir"] = cand_dir
    
    # Copy preview PNG
    doc1_png = doc1_pdf.replace(".pdf", ".png")
    pub_png = os.path.join(WEBSITE_PREVIEWS_DIR, f"{cid}.png")
    if os.path.exists(doc1_png):
        shutil.copy2(doc1_png, pub_png)
        print(f"  Preview PNG copied to: {pub_png}")
    else:
        print(f"  Warning: {doc1_png} not found")

# Update Registry & Directory
with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {item.get("certId"): item for item in directory if item.get("certId")}

for cand in new_candidates:
    cid = cand["cert_id"]
    reg_entry = {
        "certId": cid,
        "internId": cand["intern_id"],
        "holderName": cand["name"],
        "email": cand["email"],
        "phone": cand["phone"],
        "college": cand["college"],
        "domain": cand["domain"],
        "trackCode": "FSD",
        "project": cand["project"],
        "batch": cand["batch"],
        "duration": cand["duration"],
        "startDate": cand["start_date"],
        "endDate": cand["end_date"],
        "issueDate": cand["issue_date"],
        "evalDate": cand["eval_date"],
        "score": cand["score"],
        "grade": cand["grade"],
        "signatory": "Mr. Abhinav Sharma",
        "signatoryTitle": "Program Head & Project Mentor",
        "organization": "DBERT",
        "verificationUrl": f"https://dbert.in/verify/{cid}",
        "previewUrl": f"/certificates/previews/{cid}.png",
        "verified": True,
        "isProvisional": False,
        "status": "VERIFIED",
        "verificationDate": "2026-11-21",
        "topics": cand["topics"],
        "doc1Pdf": cand["doc1_pdf"],
        "doc2Pdf": cand["doc2_pdf"],
        "doc3Pdf": cand["doc3_pdf"]
    }
    registry[cid] = reg_entry
    print(f"Registry updated: {cid} -> VERIFIED")
    
    first_letter = cand["name"].strip()[0].upper()
    if not first_letter.isalpha():
        first_letter = "#"
        
    dir_entry = {
        "certId": cid,
        "internId": cand["intern_id"],
        "holderName": cand["name"],
        "email": cand["email"],
        "college": cand["college"],
        "domain": cand["domain"],
        "duration": cand["duration"],
        "score": cand["score"],
        "grade": cand["grade"],
        "isProvisional": False,
        "status": "VERIFIED",
        "verified": True,
        "firstLetter": first_letter,
        "previewUrl": f"/certificates/previews/{cid}.png",
        "verifyUrl": f"/verify/{cid}"
    }
    if cid in dir_map:
        dir_map[cid].update(dir_entry)
    else:
        directory.append(dir_entry)
        dir_map[cid] = dir_entry
    print(f"Directory updated: {cid} -> Tab 1 Pre-Vetted Engineers")

# Update verification_submissions_299.json
with open(VERIFICATION_SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
    subs = json.load(f)

# Also load the 2 new submissions from EC2 or add them if not present
new_submissions_payload = [
    {
        "id": "DBERT-VER-128605-KWKJ",
        "submittedAt": "2026-11-21T11:23:36.547Z",
        "approvedAt": "2026-11-21T11:45:00.000Z",
        "verifiedAt": "2026-11-21T11:45:00.000Z",
        "fullName": "MOLUGU NANDA YASOVARDHAN",
        "email": "nandayasovardhan@gmail.com",
        "phone": "9493476662",
        "college": "Vishnu Institute of Technology",
        "domain": "Full Stack Web Development",
        "certId": "CERT-DBERT-2026-FSD-341",
        "internId": "DBERT-2026-INT-2345",
        "amountExpected": 299,
        "amountPaid": 299,
        "utrNumber": "375725311685",
        "status": "APPROVED",
        "adminRemarks": "Payment verified, official 3-doc credential packet generated, Tab 1 unlocked, Gate 1 released."
    },
    {
        "id": "DBERT-VER-433495-L1XZ",
        "submittedAt": "2026-11-21T11:23:43.511Z",
        "approvedAt": "2026-11-21T11:45:00.000Z",
        "verifiedAt": "2026-11-21T11:45:00.000Z",
        "fullName": "H A Uday Bhasker",
        "email": "ubhoysala@gmail.com",
        "phone": "7036073368",
        "college": "Geethanjali College of Engineering and Technology",
        "domain": "Full Stack Web Development",
        "certId": "CERT-DBERT-2026-FSD-342",
        "internId": "DBERT-2026-INT-2089",
        "amountExpected": 299,
        "amountPaid": 299,
        "utrNumber": "930768222270",
        "status": "APPROVED",
        "adminRemarks": "Payment verified, official 3-doc credential packet generated, Tab 1 unlocked, Gate 1 released."
    }
]

existing_sub_ids = {s.get("id") for s in subs}
for ns in new_submissions_payload:
    if ns["id"] in existing_sub_ids:
        for s in subs:
            if s.get("id") == ns["id"]:
                s.update(ns)
    else:
        subs.append(ns)
        existing_sub_ids.add(ns["id"])
    print(f"Submission recorded & APPROVED: {ns['id']} ({ns['fullName']})")

# Save updated files
with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)
print(f"\nSaved {REGISTRY_FILE} ({len(registry)} certificates).")

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)
print(f"Saved {DIRECTORY_FILE} ({len(directory)} candidates).")

with open(VERIFICATION_SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(subs, f, indent=2, ensure_ascii=False)
print(f"Saved {VERIFICATION_SUBMISSIONS_FILE} ({len(subs)} submissions).")
