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

# 5 Candidates to Upgrade / Ingest as Verified
CANDIDATES = [
    {
        "index": 66,
        "name": "Aaditya Kadam",
        "email": "aadityakadam432@gmail.com",
        "phone": "9826012345",
        "college": "SVVV Indore",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "Aivara — Autonomous AI Operations & Agentic Workflow Suite",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-024",
        "intern_id": "DBERT-INT-AK-1659-024",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [17, 8, 8, 8, 8, 9, 8, 8, 9],
        "is_new": False
    },
    {
        "index": 67,
        "name": "Sakthi P",
        "email": "me250003067@iiti.ac.in",
        "phone": "7540083220",
        "college": "Indian Institute of Technology Indore",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-173",
        "intern_id": "DBERT-2026-INT-1367",
        "score": 88,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 9, 9, 8, 9, 9, 8, 9],
        "is_new": False
    },
    {
        "index": 68,
        "name": "Gurveer Singh",
        "email": "gurveer3057.beai25@chitkara.edu.in",
        "phone": "6280719402",
        "college": "Chitkara University, Punjab",
        "domain": "UI/UX Design",
        "batch": "Aug to Oct 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Figma, User Research, Wireframing, Prototyping, Usability Testing, Visual Design, Design Systems",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-UIUX-040",
        "intern_id": "DBERT-2026-INT-1365",
        "score": 76,
        "grade": "Grade: B+ (Good Performance)",
        "rubric_marks": [15, 8, 8, 7, 8, 7, 8, 7, 8],
        "is_new": False
    },
    {
        "index": 69,
        "name": "Yarlagadda Chandra Mahesh Goud",
        "email": "chandramahesh736@gmail.com",
        "phone": "9390234567",
        "college": "Bapatla Engineering College",
        "domain": "Full Stack Development",
        "batch": "Aug to Oct 2026",
        "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
        "topics": "HTML5, CSS3, JavaScript, TypeScript, React, Next.js, Node.js, REST APIs, PostgreSQL, Docker",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-FSD-071",
        "intern_id": "DBERT-2026-INT-1413",
        "score": 88,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 9, 8, 9, 9, 9, 8, 9],
        "is_new": True
    },
    {
        "index": 70,
        "name": "CH MONIKA SAI",
        "email": "monikach575@gmail.com",
        "phone": "8309123456",
        "college": "Pragati Engineering College",
        "domain": "Data Analyst",
        "batch": "May to July 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "May to July 2026 (2 Months)",
        "start_date": "May 2026",
        "end_date": "July 2026",
        "eval_date": "01 August 2026",
        "issue_date": "2026-08-01",
        "cert_id": "CERT-DBERT-2026-DA-185",
        "intern_id": "DBERT-2026-INT-1414",
        "score": 87,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 9, 8, 8, 9, 9, 8, 9],
        "is_new": True
    }
]

# Load Registries
with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

dir_map = {item["certId"]: item for item in directory}

print(f"Loaded {len(registry)} in cert registry, {len(directory)} in directory.")

# Process each candidate
for c in CANDIDATES:
    cert_id = c["cert_id"]
    name = c["name"]
    slug = f"{c['index']:02d}_{name.lower().replace(' ', '_')}"
    cand_dir = os.path.join(OUTPUTS_DIR, slug)
    os.makedirs(cand_dir, exist_ok=True)
    
    doc1_pdf = os.path.join(cand_dir, f"1_Certificate_of_Completion_{cert_id}.pdf")
    doc2_pdf = os.path.join(cand_dir, f"2_Academic_Project_Evaluation_{cert_id}.pdf")
    doc3_pdf = os.path.join(cand_dir, f"3_Letter_of_Recommendation_{cert_id}.pdf")
    
    print(f"\nGenerating Official Documents for [{cert_id}] {name}...")
    safe_save_canvas(None, doc1_pdf, draw_cert_completion, c)
    safe_save_canvas(None, doc2_pdf, draw_cert_evaluation, c)
    safe_save_canvas(None, doc3_pdf, draw_cert_lor, c)
    
    # Copy PNG preview to public website previews
    doc1_png = doc1_pdf.replace(".pdf", ".png")
    pub_png = os.path.join(WEBSITE_PREVIEWS_DIR, f"{cert_id}.png")
    if os.path.exists(doc1_png):
        shutil.copy2(doc1_png, pub_png)
        print(f"  Preview PNG copied to: {pub_png}")
        
    # Update certificates_registry.json
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
        "status": "VERIFIED",
        "doc1Pdf": doc1_pdf,
        "doc2Pdf": doc2_pdf,
        "doc3Pdf": doc3_pdf,
        "previewUrl": f"/certificates/previews/{cert_id}.png"
    }
    registry[cert_id] = reg_record
    
    # Update directory_candidates.json
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
    else:
        directory.append(dir_entry)
        dir_map[cert_id] = dir_entry

# Save files
with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)
print(f"\nSaved updated {REGISTRY_FILE} ({len(registry)} records)")

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)
print(f"Saved updated {DIRECTORY_FILE} ({len(directory)} records)")

print("\nAll 5 candidates successfully generated and registered as VERIFIED!")
