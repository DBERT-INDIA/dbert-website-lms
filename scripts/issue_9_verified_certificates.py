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
PROV_FILE = os.path.join(BASE_DIR, "data", "all_409_provisional_registry.json")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(WEBSITE_PREVIEWS_DIR, exist_ok=True)

# Define the 9 candidates
CANDIDATES = [
    {
        "index": 57,
        "name": "N Deekshitha",
        "email": "ndeekshitha07@gmail.com",
        "alt_email": "ndeekshitha07.24@kgpian.iitkgp.ac.in",
        "phone": "9440282987",
        "college": "Indian Institute of Technology Kharagpur",
        "domain": "Artificial Intelligence & Machine Learning",
        "batch": "Aug to Oct 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Python, Scikit-Learn, PyTorch, Neural Networks, Computer Vision, NLP, Deep Learning, Model Deployment",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-AIML-092",
        "intern_id": "DBERT-2026-INT-1089",
        "score": 78,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [16, 8, 8, 8, 8, 8, 7, 7, 8],
        "is_new": False
    },
    {
        "index": 58,
        "name": "M Brahmani",
        "email": "chinniprincess842@gmail.com",
        "phone": "7288981392",
        "college": "Aditya degree women's college",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-117",
        "intern_id": "DBERT-2026-INT-1130",
        "score": 79,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [16, 8, 8, 8, 8, 8, 8, 7, 8],
        "is_new": False
    },
    {
        "index": 59,
        "name": "Ankit Saini",
        "email": "ankitsaini9438@gmail.com",
        "phone": "6387738082",
        "college": "Abes Engineering College, Ghaziabad",
        "domain": "Full Stack Development",
        "batch": "Aug to Oct 2026",
        "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
        "topics": "HTML5, CSS3, JavaScript, TypeScript, React, Next.js, Node.js, REST APIs, PostgreSQL, Docker",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-FSD-070",
        "intern_id": "DBERT-2026-INT-1049",
        "score": 83,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [17, 9, 8, 8, 8, 9, 8, 8, 8],
        "is_new": False
    },
    {
        "index": 60,
        "name": "Lucky kumar",
        "email": "luckygupta929490@gmail.com",
        "phone": "9135739965",
        "college": "Rit",
        "domain": "Python Automation",
        "batch": "Aug to Oct 2026",
        "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
        "topics": "Python, Selenium, Playwright, Beautiful Soup, AsyncIO, Web Scraping, REST APIs, CI/CD Automation",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-PA-023",
        "intern_id": "DBERT-2026-INT-1002",
        "score": 80,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [16, 8, 8, 8, 8, 8, 8, 8, 8],
        "is_new": False
    },
    {
        "index": 61,
        "name": "Rohit Ranjan Tiwari",
        "email": "piyush2100a@gmail.com",
        "phone": "+918960656191",
        "college": "Amity University Lucknow",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "Aivara — Autonomous AI Operations & Agentic Workflow Suite",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-124",
        "intern_id": "DBERT-2026-INT-1142",
        "score": 81,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [17, 8, 8, 8, 8, 8, 8, 8, 8],
        "is_new": False
    },
    {
        "index": 62,
        "name": "Shreyash Sambhaji Kamble",
        "email": "shreyashk07004@gmail.com",
        "phone": "8766036310",
        "college": "Walchand College of engineering Sangli",
        "domain": "Data Analyst",
        "batch": "May to July 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "May to July 2026 (2 Months)",
        "start_date": "May 2026",
        "end_date": "July 2026",
        "eval_date": "01 August 2026",
        "issue_date": "2026-08-01",
        "cert_id": "CERT-DBERT-2026-DA-077",
        "intern_id": "DBERT-2026-INT-1031",
        "score": 86,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 9, 8, 8, 9, 8, 9, 8],
        "is_new": False
    },
    {
        "index": 63,
        "name": "Vasu Rakholiya",
        "email": "vasurakholiya108@gmail.com",
        "phone": "7778066181",
        "college": "Symbiosis Skills And Professional University",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "Gayatri AI — Enterprise Educational Intelligence Platform",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-183",
        "intern_id": "DBERT-2026-INT-1410",
        "score": 82,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [17, 8, 8, 8, 8, 9, 8, 8, 8],
        "is_new": True
    },
    {
        "index": 64,
        "name": "Satya Patil",
        "email": "patilsatya004@gmail.com",
        "phone": "8999864760",
        "college": "Shri sant gajanan maharaj college of engineering",
        "domain": "Data Analyst",
        "batch": "July to Sep 2026",
        "project": "Alkame — Quantitative Market Intelligence & Conformal Prediction Platform",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "July to September 2026 (2 Months)",
        "start_date": "July 2026",
        "end_date": "September 2026",
        "eval_date": "01 October 2026",
        "issue_date": "2026-10-01",
        "cert_id": "CERT-DBERT-2026-DA-109",
        "intern_id": "DBERT-2026-INT-1111",
        "score": 79,
        "grade": "Grade: A (Very Good Performance)",
        "rubric_marks": [16, 8, 8, 8, 8, 8, 8, 7, 8],
        "is_new": False
    },
    {
        "index": 65,
        "name": "Janhvi singh",
        "email": "janhvichandel3@gmail.com",
        "phone": "7905859140",
        "college": "Chhatrapati shahu Ji Maharaj university , kanpur",
        "domain": "Data Analyst",
        "batch": "Aug to Oct 2026",
        "project": "DBERT Enterprise Cloud & Technical Incubation Architecture",
        "topics": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
        "duration": "August to October 2026 (2 Months)",
        "start_date": "August 2026",
        "end_date": "October 2026",
        "eval_date": "01 November 2026",
        "issue_date": "2026-11-01",
        "cert_id": "CERT-DBERT-2026-DA-184",
        "intern_id": "DBERT-2026-INT-1411",
        "score": 85,
        "grade": "Grade: A+ (Outstanding Performance)",
        "rubric_marks": [18, 9, 8, 8, 8, 9, 8, 8, 9],
        "is_new": True
    }
]

# Load Registries
with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
    registry = json.load(f)

with open(DIRECTORY_FILE, "r", encoding="utf-8") as f:
    directory = json.load(f)

with open(PROV_FILE, "r", encoding="utf-8") as f:
    prov_registry = json.load(f)

dir_map = {item["certId"]: item for item in directory}
prov_map = {item["certId"]: item for item in prov_registry}

print(f"Loaded {len(registry)} in cert registry, {len(directory)} in directory, {len(prov_registry)} in prov.")

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
        "status": "Verified",
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
        print(f"  Directory record updated to VERIFIED for {cert_id}")
    else:
        directory.append(dir_entry)
        dir_map[cert_id] = dir_entry
        print(f"  New directory record added as VERIFIED for {cert_id}")
        
    # Update prov_registry if present
    if cert_id in prov_map:
        prov_map[cert_id].update({
            "isProvisional": False,
            "status": "VERIFIED",
            "email": c["email"]
        })
    else:
        prov_registry.append(reg_record)
        prov_map[cert_id] = reg_record

# Sort directory by name
directory.sort(key=lambda x: x.get("holderName", "").lower())

# Save Registries
with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

with open(DIRECTORY_FILE, "w", encoding="utf-8") as f:
    json.dump(directory, f, indent=2, ensure_ascii=False)

with open(PROV_FILE, "w", encoding="utf-8") as f:
    json.dump(prov_registry, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print(f"ALL 9 CERTIFICATES ISSUED & REGISTRIES UPDATED SUCCESSFULLY!")
print(f"Total in certificates_registry.json: {len(registry)}")
print(f"Total in directory_candidates.json: {len(directory)}")
print(f"Total in all_409_provisional_registry.json: {len(prov_registry)}")
print("="*80)
