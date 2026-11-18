#!/usr/bin/env python3
"""
scripts/reconcile_and_finalize_cohorts.py

1. Updates intern_accounts in PostgreSQL on EC2 with verified stipend metadata for all 6 Cohort D candidates.
2. Sanitizes Cohort A to ensure no already-certified or enrolled fellows receive initial offer emails.
3. Generates clean, ready-to-dispatch JSON tracking files in data/:
   - data/cohort_a_final.json
   - data/cohort_b_final.json
   - data/cohort_c_final.json
   - data/cohort_d_final.json
"""

import sys
import json
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path("/var/www/dbert-website-lms") if Path("/var/www/dbert-website-lms").exists() else Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from app import get_db

COHORT_D_CANDIDATES = [
    {
        "email": "sjha0940@gmail.com",
        "name": "Suraj shivsunder jha",
        "cert_id": "CERT-DBERT-2026-FSD-042",
        "domain": "Full Stack Development",
        "stipend_release_date": "2026-11-20",
        "stipend_release_date_display": "Friday, 20 November 2026",
        "verified_github_org": "Alkameinc",
        "verified_github_repo": "Alkameinc/alkame-nifty-50-educational",
        "linkedin_url": "https://www.linkedin.com/in/suraj-jha-777830405",
        "github_url": "https://github.com/sjha0940-design/alkame-nifty-50-educational",
        "amount": 5499
    },
    {
        "email": "gurkavinay22@gmail.com",
        "name": "GURKA VINAY KUMAR REDDY",
        "cert_id": "CERT-DBERT-2026-AIML-169",
        "domain": "AI Agent Development",
        "stipend_release_date": "2026-11-20",
        "stipend_release_date_display": "Friday, 20 November 2026",
        "verified_github_org": "Gayatri-Education",
        "verified_github_repo": "Gayatri-Education/Gayatri-AI-Educational-Platform",
        "linkedin_url": "https://www.linkedin.com/in/gurka-vinay-kumar-reddy-40336a33b",
        "github_url": "https://github.com/vinay1105-git/Gayatri-AI-Educational-Platform",
        "amount": 5499
    },
    {
        "email": "aryanbhakuni2006@gmail.com",
        "name": "ARYAN BHAKUNI",
        "cert_id": "CERT-DBERT-2026-DA-017",
        "domain": "Data Analyst",
        "stipend_release_date": "2026-11-29",
        "stipend_release_date_display": "Sunday, 29 November 2026",
        "verified_github_org": "Alkameinc",
        "verified_github_repo": "Alkameinc/alkame-nifty-50-educational",
        "linkedin_url": "https://www.linkedin.com/in/aryan-bhakuni-ab331631a",
        "github_url": "https://github.com/aryan-2006-max/alkame-nifty-50-educational",
        "amount": 5499
    },
    {
        "email": "priyanshukalondia@gmail.com",
        "name": "Priyanshu Kalondia",
        "cert_id": "CERT-DBERT-2026-AIML-016",
        "domain": "AI Agent Development",
        "stipend_release_date": "2026-12-30",
        "stipend_release_date_display": "Wednesday, 30 December 2026",
        "verified_github_org": "Alkameinc",
        "verified_github_repo": "Alkameinc/alkame-nifty-50-educational",
        "linkedin_url": "https://www.linkedin.com/in/priyanshu-kalondia-653517390",
        "github_url": "https://github.com/Alkameinc/alkame-nifty-50-educational/pull/29",
        "amount": 5499
    },
    {
        "email": "medisettyshanmukh@gmail.com",
        "name": "SHANMUKHA SRI SAIKUMAR MEDISETTY",
        "cert_id": "CERT-DBERT-2026-AIML-002",
        "domain": "AI Agent Development",
        "stipend_release_date": "2026-12-30",
        "stipend_release_date_display": "Wednesday, 30 December 2026",
        "verified_github_org": "Gayatri-Education",
        "verified_github_repo": "Gayatri-Education/Gayatri-AI",
        "linkedin_url": "https://www.linkedin.com/in/shanmukha-sri-saikumar-medisetty",
        "github_url": "https://github.com/editor-shannu/Gayatri-AI",
        "amount": 5499
    },
    {
        "email": "sakthi220107@gmail.com",
        "name": "Sakthi P",
        "cert_id": "CERT-DBERT-2026-DA-022",
        "domain": "Data Analyst",
        "stipend_release_date": "2026-12-30",
        "stipend_release_date_display": "Wednesday, 30 December 2026",
        "verified_github_org": "Gayatri-Education",
        "verified_github_repo": "Gayatri-Education/Gayatri-Exam-Portal",
        "linkedin_url": "https://www.linkedin.com/in/sakthi2201",
        "github_url": "https://github.com/sakthi220107-cmyk/Gayatri-Exam-Portal",
        "amount": 5499
    }
]

def main():
    conn = get_db()
    cur = conn.cursor()

    print("=" * 80)
    print("RECONCILING AND FINALIZING ALL 4 COHORTS")
    print("=" * 80)

    # 1. Update intern_accounts for Cohort D
    data_dir = ROOT_DIR / "data"
    cohort_d_emails = set(c["email"].lower() for c in COHORT_D_CANDIDATES)
    print("\n1. Updating PostgreSQL intern_accounts for 6 Cohort D verified candidates...")
    for c in COHORT_D_CANDIDATES:
        cur.execute("""
            UPDATE intern_accounts
            SET stipend_verified = 1,
                stipend_release_date = %s,
                stipend_amount = %s,
                verified_github_org = %s,
                verified_github_repo = %s,
                github_url = COALESCE(NULLIF(github_url, ''), %s),
                linkedin_verified = 1
            WHERE LOWER(email) = LOWER(%s)
        """, (
            c["stipend_release_date"],
            c["amount"],
            c["verified_github_org"],
            c["verified_github_repo"],
            c["github_url"],
            c["email"]
        ))
        print(f"   -> Updated {c['name']} <{c['email']}>: release={c['stipend_release_date']}, org={c['verified_github_org']}")
    conn.commit()

    # 4. Load Cohort C (Pending Gates) and deduplicate by email, exclude Cohort D
    cohort_c_raw = json.load(open(data_dir / "cohort_c_pending_gates.json", encoding="utf-8"))
    cohort_c_map = {}
    for c in cohort_c_raw:
        em = c["email"].lower().strip()
        if em not in cohort_d_emails and em not in cohort_c_map:
            cohort_c_map[em] = c
    cohort_c_final = list(cohort_c_map.values())
    cohort_c_emails = set(cohort_c_map.keys())
    print(f"\n4. Cohort C (Pending Gates - Deduplicated): {len(cohort_c_raw)} -> {len(cohort_c_final)} candidates")

    # 2. Load Cohort A and sanitize against enrolled fellows, certificates, Cohort C, and Cohort D
    cohort_a_raw = json.load(open(data_dir / "cohort_a_selected_unpaid.json", encoding="utf-8"))
    
    # Get all emails that already have an approved certificate or enrollment
    cur.execute("SELECT LOWER(email) FROM intern_certificates WHERE email IS NOT NULL")
    cert_emails = set(r[0].strip().lower() for r in cur.fetchall())

    cur.execute("SELECT LOWER(email) FROM enrollments WHERE payment_status IN ('Accepted', 'Approved') AND email IS NOT NULL")
    approved_enr_emails = set(r[0].strip().lower() for r in cur.fetchall())

    exclusion_set = cert_emails | approved_enr_emails | cohort_c_emails | cohort_d_emails

    cohort_a_final = []
    excluded_from_a = []
    for c in cohort_a_raw:
        em = c["email"].lower().strip()
        if em in exclusion_set:
            excluded_from_a.append(em)
        else:
            cohort_a_final.append(c)

    print(f"\n2. Sanitized Cohort A: {len(cohort_a_raw)} -> {len(cohort_a_final)} candidates ({len(excluded_from_a)} excluded)")

    # 3. Load Cohort B (Rejected Payments)
    cohort_b_final = json.load(open(data_dir / "cohort_b_rejected_payments.json", encoding="utf-8"))
    print(f"\n3. Cohort B (Rejected Payments): {len(cohort_b_final)} candidate(s)")

    # 5. Finalize Cohort D
    cohort_d_final = COHORT_D_CANDIDATES
    print(f"\n5. Cohort D (All Gates Verified & Scheduled): {len(cohort_d_final)} candidates")

    # Save finalized cohort files
    with open(data_dir / "cohort_a_final.json", "w", encoding="utf-8") as f:
        json.dump(cohort_a_final, f, indent=2)
    with open(data_dir / "cohort_b_final.json", "w", encoding="utf-8") as f:
        json.dump(cohort_b_final, f, indent=2)
    with open(data_dir / "cohort_c_final.json", "w", encoding="utf-8") as f:
        json.dump(cohort_c_final, f, indent=2)
    with open(data_dir / "cohort_d_final.json", "w", encoding="utf-8") as f:
        json.dump(cohort_d_final, f, indent=2)

    print("\nAll finalized cohorts written to data/ successfully.")

if __name__ == "__main__":
    main()
