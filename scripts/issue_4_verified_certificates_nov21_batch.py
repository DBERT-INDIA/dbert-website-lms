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

# Candidate 4 Data (Maroju Prince Karthik) for PDF Generation
CAND4_DATA = {
    "index": 93,
    "name": "Maroju Prince Karthik",
    "email": "marojuprincekarthik2007@gmail.com",
    "phone": "7093726609",
    "college": "Visvesvaraya National Institute of Technology, Nagpur",
    "domain": "Full Stack Web Development",
    "batch": "July to Sep 2026",
    "project": "Gayatri AI Platform — Enterprise Educational Intelligence",
    "topics": "React, Next.js, Node.js, Express, PostgreSQL, REST APIs, System Architecture, State Management",
    "duration": "15 July 2026 – 15 September 2026 (2 Months)",
    "start_date": "July 2026",
    "end_date": "September 2026",
    "eval_date": "15 September 2026",
    "issue_date": "2026-11-21",
    "cert_id": "CERT-DBERT-2026-FSD-343",
    "intern_id": "DBERT-2026-INT-3326",
    "score": 86,
    "grade": "Grade: A (Very Good Performance)",
    "rubric_marks": [17, 8, 9, 8, 9, 8, 9, 9, 9],
    "source": "Website 299 Payment (UTR 632598313488)"
}

print("=" * 70)
print("1. GENERATING 3-DOC CREDENTIAL PACKET FOR MAROJU PRINCE KARTHIK")
print("=" * 70)

cid4 = CAND4_DATA["cert_id"]
cand4_dir = os.path.join(OUTPUTS_DIR, f"{CAND4_DATA['index']}_maroju_prince_karthik")
os.makedirs(cand4_dir, exist_ok=True)

doc1_pdf = os.path.join(cand4_dir, f"1_Certificate_of_Completion_{cid4}.pdf")
doc2_pdf = os.path.join(cand4_dir, f"2_Academic_Project_Evaluation_{cid4}.pdf")
doc3_pdf = os.path.join(cand4_dir, f"3_Letter_of_Recommendation_{cid4}.pdf")

print(f"Generating dossier for {CAND4_DATA['name']} ({cid4})...")
safe_save_canvas(None, doc1_pdf, draw_cert_completion, CAND4_DATA)
safe_save_canvas(None, doc2_pdf, draw_cert_evaluation, CAND4_DATA)
safe_save_canvas(None, doc3_pdf, draw_cert_lor, CAND4_DATA)

CAND4_DATA["doc1_pdf"] = doc1_pdf
CAND4_DATA["doc2_pdf"] = doc2_pdf
CAND4_DATA["doc3_pdf"] = doc3_pdf
CAND4_DATA["cand_dir"] = cand4_dir

doc1_png = doc1_pdf.replace(".pdf", ".png")
pub_png = os.path.join(WEBSITE_PREVIEWS_DIR, f"{cid4}.png")
if os.path.exists(doc1_png):
    shutil.copy2(doc1_png, pub_png)
    print(f"  Preview PNG copied to: {pub_png}")
else:
    print(f"  Warning: {doc1_png} not found")

print("\n=" * 70)
print("2. UPDATING CERTIFICATES REGISTRY & DIRECTORY FOR ALL 4 CANDIDATES")
print("=" * 70)

with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {item.get("certId"): item for item in directory if item.get("certId")}

# The 4 candidates to verify
ALL_4_UPGRADES = [
    {
        "certId": "CERT-DBERT-2026-DA-044",
        "internId": "DBERT-INT-NM-1903-044",
        "name": "Nishant Makwane",
        "email": "nishantmakwane04@gmail.com",
        "phone": "7990611903",
        "college": "Asha M Tarsadiya Institute of computer science and technology",
        "domain": "Data Analyst",
        "trackCode": "DA",
        "project": "Aivara — Autonomous AI Operations & Agentic Workflow Suite",
        "duration": "August to October 2026 (2 Months)",
        "startDate": "August 2026",
        "endDate": "October 2026",
        "evalDate": "01 November 2026",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "utr": "630070793975",
        "doc1": os.path.join(OUTPUTS_DIR, "44_nishant_makwane", "1_Certificate_of_Completion_CERT-DBERT-2026-DA-044.pdf"),
        "doc2": os.path.join(OUTPUTS_DIR, "44_nishant_makwane", "2_Academic_Project_Evaluation_CERT-DBERT-2026-DA-044.pdf"),
        "doc3": os.path.join(OUTPUTS_DIR, "44_nishant_makwane", "3_Letter_of_Recommendation_CERT-DBERT-2026-DA-044.pdf"),
    },
    {
        "certId": "CERT-DBERT-2026-FSD-051",
        "internId": "DBERT-INT-JK-8667-051",
        "name": "Jay Kumar",
        "email": "jk316875@gmail.com",
        "phone": "9142938667",
        "college": "Excel Engineering College",
        "domain": "Full Stack Development",
        "trackCode": "FSD",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "duration": "August to October 2026 (2 Months)",
        "startDate": "August 2026",
        "endDate": "October 2026",
        "evalDate": "01 November 2026",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "utr": "997309144737",
        "doc1": os.path.join(OUTPUTS_DIR, "51_jay_kumar", "1_Certificate_of_Completion_CERT-DBERT-2026-FSD-051.pdf"),
        "doc2": os.path.join(OUTPUTS_DIR, "51_jay_kumar", "2_Academic_Project_Evaluation_CERT-DBERT-2026-FSD-051.pdf"),
        "doc3": os.path.join(OUTPUTS_DIR, "51_jay_kumar", "3_Letter_of_Recommendation_CERT-DBERT-2026-FSD-051.pdf"),
    },
    {
        "certId": "CERT-DBERT-2026-DA-005",
        "internId": "DBERT-INT-DA-5765-005",
        "name": "Danisaram Anji",
        "email": "anjidanisaram@gmail.com",
        "phone": "8179125765",
        "college": "Balaji institute of technology and science warangal",
        "domain": "Data Analyst",
        "trackCode": "DA",
        "project": "Aivara — Autonomous AI Operations & Agentic Workflow Suite",
        "duration": "August to October 2026 (2 Months)",
        "startDate": "August 2026",
        "endDate": "October 2026",
        "evalDate": "01 November 2026",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "utr": "187051075927",
        "doc1": os.path.join(OUTPUTS_DIR, "05_danisaram_anji", "1_Certificate_of_Completion_CERT-DBERT-2026-DA-005.pdf"),
        "doc2": os.path.join(OUTPUTS_DIR, "05_danisaram_anji", "2_Academic_Project_Evaluation_CERT-DBERT-2026-DA-005.pdf"),
        "doc3": os.path.join(OUTPUTS_DIR, "05_danisaram_anji", "3_Letter_of_Recommendation_CERT-DBERT-2026-DA-005.pdf"),
    },
    {
        "certId": "CERT-DBERT-2026-FSD-343",
        "internId": "DBERT-2026-INT-3326",
        "name": "Maroju Prince Karthik",
        "email": "marojuprincekarthik2007@gmail.com",
        "phone": "7093726609",
        "college": "Visvesvaraya National Institute of Technology, Nagpur",
        "domain": "Full Stack Web Development",
        "trackCode": "FSD",
        "project": "Gayatri AI Platform — Enterprise Educational Intelligence",
        "duration": "15 July 2026 – 15 September 2026 (2 Months)",
        "startDate": "July 2026",
        "endDate": "September 2026",
        "evalDate": "15 September 2026",
        "score": 86,
        "grade": "Grade: A (Very Good Performance)",
        "utr": "632598313488",
        "doc1": doc1_pdf,
        "doc2": doc2_pdf,
        "doc3": doc3_pdf,
    }
]

for cand in ALL_4_UPGRADES:
    cid = cand["certId"]
    
    # 1. Update Registry
    if cid in registry:
        registry[cid]["status"] = "VERIFIED"
        registry[cid]["verified"] = True
        registry[cid]["isProvisional"] = False
        registry[cid]["verificationDate"] = "2026-11-21"
        registry[cid]["doc1Pdf"] = cand["doc1"]
        registry[cid]["doc2Pdf"] = cand["doc2"]
        registry[cid]["doc3Pdf"] = cand["doc3"]
        registry[cid]["previewUrl"] = f"/certificates/previews/{cid}.png"
    else:
        registry[cid] = {
            "certId": cid,
            "internId": cand["internId"],
            "holderName": cand["name"],
            "email": cand["email"],
            "phone": cand["phone"],
            "college": cand["college"],
            "domain": cand["domain"],
            "trackCode": cand["trackCode"],
            "project": cand["project"],
            "batch": "July to Sep 2026",
            "duration": cand["duration"],
            "startDate": cand["startDate"],
            "endDate": cand["endDate"],
            "issueDate": "2026-11-21",
            "evalDate": cand["evalDate"],
            "score": cand["score"],
            "grade": cand["grade"],
            "signatory": "Mr. Abhinav Sharma",
            "signatoryTitle": "Program Head & Project Mentor",
            "organization": "DBERT (Digital Blinc Education Research and Technology)",
            "verificationUrl": f"https://dbert.in/verify/{cid}",
            "previewUrl": f"/certificates/previews/{cid}.png",
            "verified": True,
            "isProvisional": False,
            "status": "VERIFIED",
            "verificationDate": "2026-11-21",
            "doc1Pdf": cand["doc1"],
            "doc2Pdf": cand["doc2"],
            "doc3Pdf": cand["doc3"]
        }
    print(f"Registry updated: {cid} ({cand['name']}) -> VERIFIED")
    
    # 2. Update Directory (Tab 1 Promotion)
    first_letter = cand["name"].strip()[0].upper()
    if not first_letter.isalpha():
        first_letter = "#"
        
    dir_entry = {
        "certId": cid,
        "internId": cand["internId"],
        "name": cand["name"],
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
        print(f"Directory updated (existing): {cid} -> VERIFIED")
    else:
        # Check by email
        matched = False
        for d in directory:
            if d.get("email", "").lower() == cand["email"].lower():
                d.update(dir_entry)
                matched = True
                print(f"Directory updated by email: {cid} -> VERIFIED")
                break
        if not matched:
            directory.append(dir_entry)
            print(f"Directory appended: {cid} -> VERIFIED (Tab 1)")

with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)

print("\n=" * 70)
print("3. UPDATING VERIFICATION SUBMISSIONS 299 LEDGER")
print("=" * 70)

with open(VERIFICATION_SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
    submissions = json.load(f)

for s in submissions:
    for cand in ALL_4_UPGRADES:
        if s.get("utrNumber") == cand["utr"] or s.get("email", "").lower() == cand["email"].lower():
            s["status"] = "APPROVED"
            s["amountPaid"] = 299
            s["certId"] = cand["certId"]
            s["approvedAt"] = datetime.now().isoformat()
            print(f"Approved submission for {cand['name']} | UTR: {s.get('utrNumber')} | Cert: {s.get('certId')}")

with open(VERIFICATION_SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
    json.dump(submissions, f, indent=2, ensure_ascii=False)

print("\n[SUCCESS] Local registry, directory, and 299 ledger updated successfully!")
