#!/usr/bin/env python3
"""
Stage 1:
1. Apply PostgreSQL schema additions to intern_accounts.
2. Promote 16 'Under Review' applications to 'Selected'.
3. Extract candidate cohorts for downstream dispatches:
   - Cohort A: Selected & Unpaid (16 newly promoted + 67 active 48h selected)
   - Cohort B: Rejected Payments (Active in last 48h)
   - Cohort C: Pending Gates (Active in last 48h)
   - Cohort D: All Gates Candidates for GitHub Organization Contribution Verification
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

if Path("/var/www/dbert-website-lms").exists():
    ROOT_DIR = Path("/var/www/dbert-website-lms")
else:
    ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from app import get_db

def main():
    conn = get_db()
    cur = conn.cursor()

    print("=" * 80)
    print("STAGE 1: DB MIGRATION, PROMOTIONS & COHORT EXTRACTION")
    print("=" * 80)

    # 1. Schema Additions
    print("\n1. Ensuring schema columns on intern_accounts...")
    cur.execute("""
        ALTER TABLE intern_accounts ADD COLUMN IF NOT EXISTS stipend_verified INTEGER DEFAULT 0;
        ALTER TABLE intern_accounts ADD COLUMN IF NOT EXISTS stipend_release_date TEXT;
        ALTER TABLE intern_accounts ADD COLUMN IF NOT EXISTS stipend_amount INTEGER DEFAULT 5499;
        ALTER TABLE intern_accounts ADD COLUMN IF NOT EXISTS verified_github_org TEXT;
        ALTER TABLE intern_accounts ADD COLUMN IF NOT EXISTS verified_github_repo TEXT;
    """)
    conn.commit()
    print("   -> Schema columns validated.")

    # 2. Promote 'Under Review' -> 'Selected'
    print("\n2. Promoting 'Under Review' applications to 'Selected'...")
    cur.execute("""
        SELECT id, name, email, domain, created_at
        FROM applications
        WHERE status = 'Under Review'
    """)
    under_review_before = cur.fetchall()
    print(f"   -> Found {len(under_review_before)} applications in 'Under Review':")
    for r in under_review_before:
        print(f"      * App #{r[0]}: {r[1]} <{r[2]}> | Track: {r[3]}")

    cur.execute("""
        UPDATE applications
        SET status = 'Selected', updated_at = NOW()
        WHERE status = 'Under Review'
    """)
    promoted_count = cur.rowcount
    conn.commit()
    print(f"   -> Successfully promoted {promoted_count} applications to 'Selected'.")

    # 3. Extract Cohort A: Selected & Unpaid
    # (16 promoted + users active in last 48h whose application is 'Selected' and payment not accepted)
    t48 = (datetime.now() - timedelta(hours=48)).strftime('%Y-%m-%d %H:%M:%S')

    cur.execute("""
        SELECT DISTINCT LOWER(s.email) as email, a.name, a.domain, a.status, e.payment_status
        FROM user_sessions s
        JOIN applications a ON LOWER(s.email) = LOWER(a.email)
        LEFT JOIN enrollments e ON LOWER(s.email) = LOWER(e.email)
        WHERE s.created_at >= %s 
          AND a.status = 'Selected'
          AND (e.payment_status IS NULL OR e.payment_status NOT IN ('Accepted', 'Approved'))
    """, (t48,))
    active_selected_rows = cur.fetchall()

    cohort_a_map = {}
    # Add active 48h selected
    for r in active_selected_rows:
        em = r[0].strip().lower()
        cohort_a_map[em] = {
            "email": em,
            "name": r[1] or "Candidate",
            "domain": r[2] or "Applied Engineering",
            "source": "Active_48h_Selected",
            "payment_status": r[4] or "Unpaid"
        }

    # Add newly promoted 16
    for r in under_review_before:
        em = r[2].strip().lower()
        if em not in cohort_a_map:
            cohort_a_map[em] = {
                "email": em,
                "name": r[1] or "Candidate",
                "domain": r[3] or "Applied Engineering",
                "source": "Promoted_Under_Review",
                "payment_status": "Unpaid"
            }
        else:
            cohort_a_map[em]["source"] = "Promoted_And_Active_48h"

    cohort_a = list(cohort_a_map.values())
    print(f"\n3. Cohort A (Selected & Unpaid - Next CTA: Review Offer & Complete 499): {len(cohort_a)} candidates")

    # 4. Extract Cohort B: Rejected Payments (Active in Last 48 Hours)
    cur.execute("""
        SELECT DISTINCT LOWER(s.email) as email, e.name, e.phone, e.domain, e.amount, e.utr, e.admin_note, e.updated_at
        FROM user_sessions s
        JOIN enrollments e ON LOWER(s.email) = LOWER(e.email)
        WHERE s.created_at >= %s
          AND e.payment_status = 'Rejected'
    """, (t48,))
    rejected_rows = cur.fetchall()
    cohort_b = [
        {
            "email": r[0].strip().lower(),
            "name": r[1] or "Candidate",
            "phone": r[2] or "",
            "domain": r[3] or "Applied Engineering",
            "amount": r[4] or 499,
            "utr": r[5] or "",
            "admin_note": r[6] or "Transaction proof/UTR could not be reconciled.",
            "updated_at": str(r[7])
        }
        for r in rejected_rows
    ]
    print(f"4. Cohort B (Rejected Payments Active in 48h): {len(cohort_b)} candidates")

    # 5. Extract Cohort C: Pending Gates (Active in Last 48 Hours)
    # Check active users who have an intern account or application, but have 1-3 gates remaining
    cur.execute("""
        SELECT DISTINCT LOWER(s.email) as email, ia.id as intern_id, ia.name, ia.domain,
               ia.linkedin_url, ia.github_url, ia.upi_id_encrypted,
               ic.tier as cert_tier, ic.cert_id,
               art.status as article_status, art.title as article_title
        FROM user_sessions s
        JOIN intern_accounts ia ON LOWER(s.email) = LOWER(ia.email)
        LEFT JOIN intern_certificates ic ON LOWER(ia.email) = LOWER(ic.email)
        LEFT JOIN intern_articles art ON ia.id = art.intern_id
        WHERE s.created_at >= %s
    """, (t48,))
    active_interns = cur.fetchall()

    cohort_c = []
    cohort_d = []
    for r in active_interns:
        em = r[0]
        iid = r[1]
        name = r[2] or "Fellow"
        domain = r[3] or "Applied Engineering"
        has_linkedin = bool(r[4] and r[4].strip())
        has_github = bool(r[5] and r[5].strip())
        has_upi = bool(r[6] and r[6].strip())
        is_verified_tier = bool(r[7] and r[7] in ("verified", "dbert_verified"))
        cert_id = r[8] or ""
        article_status = r[9] or "NONE"
        article_title = r[10] or ""

        # Gates:
        # Gate 1: Verified Certificate (₹299 form / evaluation complete)
        # Gate 2: Case Study Article (published)
        # Gate 3: Payout UPI
        # Gate 4: Public LinkedIn
        missing_gates = []
        if not is_verified_tier:
            missing_gates.append({
                "gate_num": 1,
                "gate_name": "Course Certificate & Verification",
                "action": "Complete domain quizzes on LMS & submit ₹299 verification form",
                "cta_url": "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
            })
        if article_status != "PUBLISHED":
            missing_gates.append({
                "gate_num": 2,
                "gate_name": "Technical Case Study / Milestone Deliverable",
                "action": "Submit your capstone technical case study or open-source project",
                "cta_url": "https://lms.dbert.in/intern/articles"
            })
        if not has_upi:
            missing_gates.append({
                "gate_num": 3,
                "gate_name": "Payout UPI ID Setup",
                "action": "Link your UPI ID (GPay/PhonePe/Paytm) to receive payouts",
                "cta_url": "https://lms.dbert.in/stipend/tasks"
            })
        if not has_linkedin:
            missing_gates.append({
                "gate_num": 4,
                "gate_name": "Public LinkedIn Experience & Credential",
                "action": "Add DBERT under Experience or Licenses & Certifications",
                "cta_url": "https://lms.dbert.in/stipend/tasks"
            })

        cand_data = {
            "email": em,
            "intern_id": iid,
            "name": name,
            "domain": domain,
            "cert_id": cert_id,
            "linkedin_url": r[4],
            "github_url": r[5],
            "has_upi": has_upi,
            "is_verified_tier": is_verified_tier,
            "article_status": article_status,
            "article_title": article_title,
            "missing_gates": missing_gates,
            "missing_count": len(missing_gates)
        }

        if len(missing_gates) == 0 and has_github:
            cohort_d.append(cand_data)
        elif 1 <= len(missing_gates) <= 3:
            cohort_c.append(cand_data)

    print(f"5. Cohort C (Pending Gates Active in 48h): {len(cohort_c)} candidates")
    print(f"6. Cohort D (All 4 Gates Complete Active in 48h): {len(cohort_d)} candidates")

    # Also search entire database for any candidates with all 4 gates complete
    cur.execute("""
        SELECT ia.id as intern_id, ia.name, ia.email, ia.domain,
               ia.linkedin_url, ia.github_url, ia.upi_id_encrypted,
               ic.tier as cert_tier, ic.cert_id,
               art.status as article_status, art.title as article_title,
               enr.joining_date
        FROM intern_accounts ia
        LEFT JOIN intern_certificates ic ON LOWER(ia.email) = LOWER(ic.email)
        LEFT JOIN intern_articles art ON ia.id = art.intern_id
        LEFT JOIN enrollments enr ON LOWER(ia.email) = LOWER(enr.email)
        WHERE (ia.linkedin_url IS NOT NULL AND ia.linkedin_url != '')
          AND (ia.github_url IS NOT NULL AND ia.github_url != '')
          AND (ia.upi_id_encrypted IS NOT NULL AND ia.upi_id_encrypted != '')
          AND (ic.tier IN ('verified', 'dbert_verified'))
          AND (art.status = 'PUBLISHED')
    """)
    all_gates_system_wide = cur.fetchall()
    print(f"   -> System-wide Candidates with All 4 Gates: {len(all_gates_system_wide)}")
    for r in all_gates_system_wide:
        print(f"      * {r[1]} <{r[2]}> | Track: {r[3]} | GitHub: {r[5]} | Article: {r[10][:35]} | Joining: {r[11]}")

    cohort_d_system_wide = [
        {
            "intern_id": r[0],
            "name": r[1] or "Fellow",
            "email": r[2],
            "domain": r[3] or "Applied Engineering",
            "linkedin_url": r[4],
            "github_url": r[5],
            "upi_id_encrypted": r[6],
            "cert_tier": r[7],
            "cert_id": r[8],
            "article_status": r[9],
            "article_title": r[10],
            "joining_date": str(r[11]) if r[11] else None
        }
        for r in all_gates_system_wide
    ]

    # Save all cohorts to JSON files
    data_dir = ROOT_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    with open(data_dir / "cohort_a_selected_unpaid.json", "w", encoding="utf-8") as f:
        json.dump(cohort_a, f, indent=2, default=str)
    with open(data_dir / "cohort_b_rejected_payments.json", "w", encoding="utf-8") as f:
        json.dump(cohort_b, f, indent=2, default=str)
    with open(data_dir / "cohort_c_pending_gates.json", "w", encoding="utf-8") as f:
        json.dump(cohort_c, f, indent=2, default=str)
    with open(data_dir / "cohort_d_all_gates_verified.json", "w", encoding="utf-8") as f:
        json.dump(cohort_d_system_wide, f, indent=2, default=str)

    print("\nStage 1 completed successfully. Cohort files saved to data/")

if __name__ == "__main__":
    main()
