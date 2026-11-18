import os
import sys
import json
import shutil
from pathlib import Path

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

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(WEBSITE_PREVIEWS_DIR, exist_ok=True)

# 7 Target Candidates from Google Sheet gid=1265293201
CANDIDATES = [
    {
        "index": 80,
        "name": "Rajveer Singh",
        "email": "rajveerpopli1@gmail.com",
        "phone": "9996160595",
        "college": "Chitkara University",
        "domain": "Artificial Intelligence & Machine Learning",
        "batch": "Aug to Oct 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Python, Scikit-Learn, PyTorch, Neural Networks, Computer Vision, NLP, Deep Learning, Model Deployment",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-AIML-100",
        "intern_id": "DBERT-INT-RS-0595-100",
        "score": 86,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 9, 8, 8, 9, 8, 9, 8]
    },
    {
        "index": 81,
        "name": "Deepanshu",
        "email": "hey.deepanshu2006@gmail.com",
        "phone": "9667798367",
        "college": "Delhi Skill and Entrepreneurship University",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-186",
        "intern_id": "DBERT-INT-DE-8367-186",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 9, 9, 8, 9, 8, 9, 8]
    },
    {
        "index": 82,
        "name": "Komma Hari Kesava",
        "email": "kommakesava1@gmail.com",
        "phone": "9381737701",
        "college": "Bapatla Engineering College",
        "domain": "Data Analyst",
        "batch": "July to Sep 2026",
        "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "July to September 2026 (2 Months)",
        "start_date": "July 2026",
        "end_date": "September 2026",
        "eval_date": "01 October 2026",
        "issue_date": "2026-10-01",
        "cert_id": "CERT-DBERT-2026-DA-127",
        "intern_id": "DBERT-INT-KH-7701-127",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 8, 8, 8, 9, 8, 8, 9]
    },
    {
        "index": 83,
        "name": "Arya Nitin Pawar",
        "email": "aryapawar1805@gmail.com",
        "phone": "9028550488",
        "college": "Vidyalankar Institute of Technology",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "Aivara — Autonomous AI Operations & Agentic Workflow Suite",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-187",
        "intern_id": "DBERT-INT-AP-0488-187",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 8, 8, 8, 9, 8, 8, 9]
    },
    {
        "index": 84,
        "name": "Piyush Solanki",
        "email": "piyushsolanki6569@gmail.com",
        "phone": "8307586695",
        "college": "Amity University Jaipur",
        "domain": "Artificial Intelligence & Machine Learning",
        "batch": "Aug to Oct 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Python, Scikit-Learn, PyTorch, Neural Networks, Computer Vision, NLP, Deep Learning, Model Deployment",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-AIML-064",
        "intern_id": "DBERT-INT-PS-6695-064",
        "score": 86,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 9, 8, 8, 9, 8, 9, 8]
    },
    {
        "index": 85,
        "name": "Ramparia Amrita R.",
        "email": "amritarampariya@gmail.com",
        "phone": "8160943890",
        "college": "Goverment MCA College Maninagar",
        "domain": "Data Analyst",
        "batch": "June to Aug 2026",
        "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "June to August 2026 (2 Months)",
        "start_date": "June 2026",
        "end_date": "August 2026",
        "eval_date": "01 September 2026",
        "issue_date": "2026-09-01",
        "cert_id": "CERT-DBERT-2026-DA-086",
        "intern_id": "DBERT-INT-RA-3890-086",
        "score": 84,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [17, 9, 8, 8, 8, 9, 8, 8, 9]
    },
    {
        "index": 51,
        "name": "Arnak Ray",
        "email": "arnakrayofficial@gmail.com",
        "phone": "6290747930",
        "college": "RCCIIT",
        "domain": "Artificial Intelligence & Machine Learning",
        "batch": "July to Sep 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Python, Scikit-Learn, PyTorch, Neural Networks, Computer Vision, NLP, Deep Learning, Model Deployment",
        "duration": "July to September 2026 (2 Months)",
        "start_date": "July 2026",
        "end_date": "September 2026",
        "eval_date": "01 October 2026",
        "issue_date": "2026-10-01",
        "cert_id": "CERT-DBERT-2026-AIML-178",
        "intern_id": "DBERT-INT-AR-7930-178",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 8, 8, 8, 9, 8, 8, 9]
    }
]

print("="*80)
print(f"ISSUING 3-DOCUMENT CREDENTIAL PACKETS FOR {len(CANDIDATES)} CANDIDATES")
print("="*80)

with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {item["certId"]: item for item in directory}

for c in CANDIDATES:
    cert_id = c["cert_id"]
    name = c["name"]
    slug = f"{c['index']:02d}_{name.lower().replace(' ', '_')}"
    cand_dir = os.path.join(OUTPUTS_DIR, slug)
    os.makedirs(cand_dir, exist_ok=True)

    doc1_pdf = os.path.join(cand_dir, f"1_Certificate_of_Completion_{cert_id}.pdf")
    doc2_pdf = os.path.join(cand_dir, f"2_Academic_Project_Evaluation_{cert_id}.pdf")
    doc3_pdf = os.path.join(cand_dir, f"3_Letter_of_Recommendation_{cert_id}.pdf")

    print(f"\n[{c['index']}] Generating Official 3-Document Packet for: {name} ({cert_id})...")
    safe_save_canvas(None, doc1_pdf, draw_cert_completion, c)
    safe_save_canvas(None, doc2_pdf, draw_cert_evaluation, c)
    safe_save_canvas(None, doc3_pdf, draw_cert_lor, c)
    print(f"  -> Generated: {doc1_pdf}")
    print(f"  -> Generated: {doc2_pdf}")
    print(f"  -> Generated: {doc3_pdf}")

    # Copy Doc 1 preview PNG to Next.js public certificates directory
    doc1_png = doc1_pdf.replace(".pdf", ".png")
    pub_png = os.path.join(WEBSITE_PREVIEWS_DIR, f"{cert_id}.png")
    if os.path.exists(doc1_png):
        shutil.copy2(doc1_png, pub_png)
        print(f"  -> Web Preview PNG copied to: {pub_png}")

    # Build or update master registry record
    reg_record = {
        "certId": cert_id,
        "internId": c["intern_id"],
        "holderName": name,
        "email": c["email"],
        "college": c["college"],
        "domain": c["domain"],
        "project": c["project"],
        "batch": c["batch"],
        "duration": c["duration"],
        "startDate": c["start_date"],
        "endDate": c["end_date"],
        "issueDate": c["issue_date"],
        "evalDate": c["eval_date"],
        "score": c["score"],
        "grade": c["grade"],
        "signatory": "Mr. Abhinav Sharma",
        "signatoryTitle": "Program Head & Project Mentor",
        "organization": "DBERT (Digital Blinc Education Research and Technology)",
        "verificationUrl": f"https://dbert.in/verify?certid={cert_id}",
        "verified": True,
        "isProvisional": False,
        "status": "Verified",
        "doc1Pdf": doc1_pdf,
        "doc2Pdf": doc2_pdf,
        "doc3Pdf": doc3_pdf,
        "previewUrl": f"/certificates/previews/{cert_id}.png"
    }
    registry[cert_id] = reg_record

    # Update directory candidates
    first_letter = name.strip()[0].upper()
    if not first_letter.isalpha():
        first_letter = "#"

    dir_entry = {
        "certId": cert_id,
        "internId": c["intern_id"],
        "holderName": name,
        "domain": c["domain"],
        "duration": c["duration"],
        "score": c["score"],
        "grade": c["grade"],
        "isProvisional": False,
        "status": "VERIFIED",
        "firstLetter": first_letter,
        "verifyUrl": f"/verify/{cert_id}"
    }

    if cert_id in dir_map:
        dir_map[cert_id].update(dir_entry)
        print(f"  -> Directory entry updated to VERIFIED for {cert_id}")
    else:
        directory.append(dir_entry)
        dir_map[cert_id] = dir_entry
        print(f"  -> New directory entry added for {cert_id}")

# Sort directory by name
directory.sort(key=lambda x: x.get("holderName", "").lower())

# Save Registries
with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("SUCCESS: ALL 7 CANDIDATES PROCESSED & MASTER REGISTRIES UPDATED!")
print(f"Total verified credentials in registry: {len(registry)}")
print(f"Total candidates in directory: {len(directory)}")
print("="*80)
