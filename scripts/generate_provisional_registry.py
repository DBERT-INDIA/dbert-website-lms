import csv
import json
import os

DOMAIN_PROJECT_MAP = {
    'Artificial Intelligence (AI) and Machine Learning (ML)': 'Gayatri AI',
    'AI Agent Development': 'Gayatri AI',
    'Data Analyst': 'Cognitive Solutions',
    'Full Stack Development': 'Alkame',
    'UI and UX Internship': 'Gayatri AI',
    'Python Automation': 'Digital Blaize'
}

DOMAIN_CODE_MAP = {
    'Data Analyst': 'DA',
    'Artificial Intelligence (AI) and Machine Learning (ML)': 'AIML',
    'AI Agent Development': 'AIML',
    'Full Stack Development': 'FSD',
    'UI and UX Internship': 'UIUX',
    'Python Automation': 'PA'
}

def main():
    reg_path = 'apps/website/src/data/certificates_registry.json'
    with open(reg_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    print(f"Initial verified registry count: {len(registry)}")

    # Find starting numbers
    domain_counters = {
        'DA': 57,
        'AIML': 57,
        'FSD': 57,
        'UIUX': 27,
        'PA': 22
    }

    # Load 148 pending candidates
    with open('data/grand_total_pending_candidates.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pending_list = list(reader)

    print(f"Loaded {len(pending_list)} pending candidates.")

    provisional_records = []

    for idx, p in enumerate(pending_list):
        name = p['name'].strip()
        email = p['email'].strip().lower()
        college = p['college'].strip() or 'Engineering Fellow'
        raw_domain = p['domain'].strip()
        phone = p['phone'].strip()

        # Map domain code
        d_code = DOMAIN_CODE_MAP.get(raw_domain, 'DA')
        num = domain_counters[d_code]
        domain_counters[d_code] += 1

        cert_id = f"CERT-DBERT-2026-{d_code}-{num:03d}"
        intern_id = f"DBERT-2026-INT-{1000 + idx:04d}"
        project = DOMAIN_PROJECT_MAP.get(raw_domain, 'Cognitive Solutions')

        rec = {
            "certId": cert_id,
            "internId": intern_id,
            "holderName": name,
            "email": email,
            "phone": phone,
            "college": college,
            "domain": raw_domain,
            "project": project,
            "batch": "Aug to Oct 2026",
            "duration": "15 Aug 2026 – 15 Oct 2026",
            "startDate": "2026-08-15",
            "endDate": "2026-10-15",
            "issueDate": "2026-11-04",
            "evalDate": "2026-11-04",
            "score": 88,
            "grade": "Grade A (Very Good)",
            "signatory": "Mr. Abhinav Sharma",
            "signatoryTitle": "Program Head & Project Mentor",
            "organization": "DBERT",
            "verificationUrl": f"https://dbert.in/verify?certid={cert_id}",
            "previewUrl": "/certificates/previews/sample_certificate_locked.png",
            "isProvisional": True,
            "status": "PENDING_ACTIVATION"
        }

        registry[cert_id] = rec
        provisional_records.append(rec)

    # Save updated registry
    with open(reg_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)

    # Save provisional records to separate audit file
    with open('data/provisional_candidates_registry.json', 'w', encoding='utf-8') as f:
        json.dump(provisional_records, f, indent=2)

    print(f"Updated registry saved! Total entries in registry now: {len(registry)}")
    print(f"Generated {len(provisional_records)} provisional records.")
    print(f"First provisional ID: {provisional_records[0]['certId']} for {provisional_records[0]['holderName']}")
    print(f"Last provisional ID: {provisional_records[-1]['certId']} for {provisional_records[-1]['holderName']}")

if __name__ == '__main__':
    main()
