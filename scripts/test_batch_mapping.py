import csv
import re
from datetime import datetime

# Domain topics mapping
DOMAIN_TOPICS = {
    "Data Analyst": "Excel, SQL, Python, Pandas, Data Cleaning, Data Visualization, Power BI, Business Analytics",
    "Artificial Intelligence (AI) and Machine Learning (ML)": "Python, Scikit-Learn, PyTorch, Neural Networks, Computer Vision, NLP, Deep Learning, Model Deployment",
    "Full Stack Development": "HTML5, CSS3, JavaScript, TypeScript, React, Next.js, Node.js, REST APIs, PostgreSQL, Docker",
    "Python Automation": "Python, Selenium, Playwright, Beautiful Soup, AsyncIO, Web Scraping, REST APIs, CI/CD Automation",
    "UI and UX Internship": "Figma, Design Systems, User Research, Wireframing, High-Fidelity Prototyping, Usability Testing, WCAG Accessibility"
}

# Domain track code for IDs
DOMAIN_CODES = {
    "Data Analyst": "DA",
    "Artificial Intelligence (AI) and Machine Learning (ML)": "AIML",
    "Full Stack Development": "FSD",
    "Python Automation": "PA",
    "UI and UX Internship": "UIUX"
}

# Standardized Project Titles
PROJECT_TITLES = {
    "Gayatri Ai": "Gayatri AI — Enterprise Educational Intelligence Platform",
    "DBERT": "DBERT Enterprise Cloud & Technical Incubation Architecture",
    "Alkame": "Alkame — Quantitative Market Intelligence & Conformal Prediction Platform",
    "Aivara": "Aivara — Autonomous AI Operations & Agentic Workflow Suite",
    "Gayatri Ai, DBERT": "Gayatri AI — Enterprise Educational Intelligence Platform",
    "Aivara, Gayatri Ai, DBERT": "Aivara — Autonomous AI Operations & Agentic Workflow Suite",
    "Gayatri Ai, Alkame": "Gayatri AI — Enterprise Educational Intelligence Platform"
}

# Batch 2-Month Mapping
# Format: Start Date, End Date, Duration String
BATCH_DATES = {
    "July to Sep 2026": {
        "start_date": "01 July 2026",
        "end_date": "31 August 2026",
        "duration": "01 July 2026 to 31 August 2026 (2 Months)",
        "eval_date": "04 November 2026"
    },
    "Aug to Oct 2026": {
        "start_date": "01 August 2026",
        "end_date": "30 September 2026",
        "duration": "01 August 2026 to 30 September 2026 (2 Months)",
        "eval_date": "04 November 2026"
    },
    "June to Aug 2026": {
        "start_date": "01 June 2026",
        "end_date": "31 July 2026",
        "duration": "01 June 2026 to 31 July 2026 (2 Months)",
        "eval_date": "04 November 2026"
    },
    "May to July 2026": {
        "start_date": "01 May 2026",
        "end_date": "30 June 2026",
        "duration": "01 May 2026 to 30 June 2026 (2 Months)",
        "eval_date": "04 November 2026"
    }
}

def clean_name(raw_name):
    # Capitalize name nicely while preserving multi-part names
    parts = raw_name.strip().split()
    return " ".join(p.capitalize() for p in parts)

def extract_initials(name):
    parts = re.findall(r'[A-Za-z]', name)
    words = name.strip().split()
    if len(words) >= 2:
        return (words[0][0] + words[-1][0]).upper()
    elif len(words) == 1 and len(words[0]) >= 2:
        return words[0][:2].upper()
    return "ST"

def extract_phone_suffix(phone):
    digits = re.sub(r'\D', '', phone)
    if len(digits) >= 4:
        return digits[-4:]
    return "0000"

with open('sheet_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [r for r in reader if any(r.values())]

print(f"Total rows in sheet: {len(rows)}")

cert_ids = set()
intern_ids = set()
candidates = []

for idx, r in enumerate(rows, start=1):
    raw_name = r.get('Name', '').strip()
    name = clean_name(raw_name)
    email = r.get('Email Address', '').strip()
    college = r.get('College Name', '').strip()
    domain_raw = r.get('Select Internship', '').strip()
    batch_raw = r.get('Choose Internship Batch ', r.get('Choose Internship Batch', '')).strip()
    project_raw = r.get('Project Contibuted On', '').strip()
    phone = r.get('WhatsApp number ', r.get('WhatsApp number', '')).strip()
    
    # Track Code
    t_code = DOMAIN_CODES.get(domain_raw, "GEN")
    cert_id = f"CERT-DBERT-2026-{t_code}-{idx:03d}"
    
    # Intern ID
    initials = extract_initials(raw_name)
    ph_suffix = extract_phone_suffix(phone)
    intern_id = f"DBERT-INT-{initials}-{ph_suffix}-{idx:03d}"
    
    # Dates
    b_info = BATCH_DATES.get(batch_raw, {
        "start_date": "01 July 2026",
        "end_date": "31 August 2026",
        "duration": "01 July 2026 to 31 August 2026 (2 Months)",
        "eval_date": "04 November 2026"
    })
    
    # Domain Display
    domain_display = domain_raw
    if "Artificial Intelligence" in domain_raw:
        domain_display = "Artificial Intelligence & Machine Learning"
    elif "UI and UX" in domain_raw:
        domain_display = "UI & UX Design"
        
    # Project Title
    project_title = PROJECT_TITLES.get(project_raw, f"{project_raw} Platform Architecture")
    
    # Topics
    topics = DOMAIN_TOPICS.get(domain_raw, "Python, SQL, Cloud Architecture, Agile Engineering")
    
    # Deterministic Academic Score (82 - 90 range based on index)
    base_score = 83 + (idx % 8)
    rubric_m = [17, 9, 8, 8, 8, 9, 8, 8, 9]
    if base_score == 85:
        rubric_m = [18, 9, 8, 8, 8, 9, 8, 8, 9]
    elif base_score >= 86:
        rubric_m = [18, 9, 9, 8, 8, 9, 8, 9, 9]
        base_score = sum(rubric_m)
        
    grade = "Grade: A+ (Outstanding Performance)" if base_score >= 85 else "Grade: A (Very Good Performance)"
    
    c_entry = {
        "index": idx,
        "name": name,
        "email": email,
        "college": college,
        "domain": domain_display,
        "batch": batch_raw,
        "project": project_title,
        "topics": topics,
        "duration": b_info["duration"],
        "start_date": b_info["start_date"],
        "end_date": b_info["end_date"],
        "eval_date": b_info["eval_date"],
        "cert_id": cert_id,
        "intern_id": intern_id,
        "phone": phone,
        "score": base_score,
        "grade": grade,
        "rubric_marks": rubric_m
    }
    
    cert_ids.add(cert_id)
    intern_ids.add(intern_id)
    candidates.append(c_entry)

print(f"Processed Candidates: {len(candidates)}")
print(f"Unique Certificate IDs: {len(cert_ids)}")
print(f"Unique Intern IDs: {len(intern_ids)}")
print("\nSample mapped entries:")
for c in candidates[:5]:
    print(f"[{c['index']:02d}] {c['name']} | {c['domain']} | {c['batch']} -> {c['duration']} | ID: {c['cert_id']}")
