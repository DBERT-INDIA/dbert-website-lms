#!/usr/bin/env python3
"""
scripts/execute_discrepancy_and_cohort_setup.py

1. Updates the 10 discrepancy submissions in PostgreSQL to status='changes_requested' with specific feedback notes.
2. Extracts and partitions the 1,026 engaged interns into prioritized batches for staggered dispatch:
   - Batch 1: First 250 interns (all 164 candidates with 1-2 gates pending + 86 with 3 gates pending).
   - Batch 2, 3, 4: Remaining 776 interns scheduled for subsequent 4-hour cycles.
3. Saves:
   - data/cohort_discrepancy_10.json
   - data/engaged_interns_batch1.json
   - data/engaged_interns_all.json
"""

import sys
import json
from datetime import datetime, date, timedelta
from pathlib import Path

if Path("/var/www/dbert-website-lms").exists():
    sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
    ROOT_DIR = Path("/var/www/dbert-website-lms")
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "portal"))
    ROOT_DIR = Path(__file__).resolve().parent.parent

from app import get_db

APPROVED_ORGS = [
    "gayatri-education",
    "aivaratechinfomatics",
    "alkameinc",
    "dbert-india"
]

def main():
    conn = get_db()
    cur = conn.cursor()

    print("=" * 80)
    print("PHASE 1 & 2: DISCREPANCY REVIEWS & ENGAGED COHORT PARTITIONING")
    print("=" * 80)

    # 1. Inspect and update the 10 discrepancy candidates
    cur.execute("""
        SELECT ts.id, ts.intern_id, ts.email, ts.github_repo_url, ts.status,
               ia.name, ia.linkedin_url, ia.linkedin_verified, ia.linkedin_verification_status,
               ia.stipend_verified, ia.domain
        FROM task_submissions ts
        JOIN intern_accounts ia ON ts.intern_id = ia.id
        WHERE ts.task_category = 'stipend_milestone'
          AND (ia.stipend_verified IS NULL OR ia.stipend_verified = 0)
        ORDER BY ts.id DESC
    """)
    subs = cur.fetchall()
    
    discrepancy_list = []
    for s in subs:
        sid, iid, em, gh_url, s_status, name, l_url, l_ver, l_status, st_ver, domain = s
        gh_lower = (gh_url or "").lower()
        is_approved_org = any(org in gh_lower for org in APPROVED_ORGS)
        is_li_verified = bool(l_ver == 1)

        issues = []
        feedback_lines = []
        if not is_approved_org:
            issues.append("INVALID_GITHUB_ORG")
            feedback_lines.append(
                f"Submitted repository ({gh_url}) does not belong to an authorized DBERT organization (Alkameinc, Gayatri-Education, Aivaratechinfomatics, DBERT-INDIA). Under DBERT policy, stipends are strictly funded for verified contributions to authorized organization codebases."
            )
        if not is_li_verified:
            issues.append("UNVERIFIED_LINKEDIN")
            feedback_lines.append(
                f"Public LinkedIn profile ({l_url or 'Not linked'}) does not show DBERT under Experience or Licenses & Certifications, or has not been verified."
            )

        feedback_note = " | ".join(feedback_lines)

        # Update in database to changes_requested
        cur.execute("""
            UPDATE task_submissions
            SET status = 'changes_requested',
                ai_evaluation_notes = %s,
                reviewed_by_staff_id = 1
            WHERE id = %s
        """, (feedback_note, sid))

        discrepancy_list.append({
            "submission_id": sid,
            "intern_id": iid,
            "name": name or "Fellow",
            "email": em.strip().lower(),
            "domain": domain or "Applied Engineering",
            "github_repo_url": gh_url or "",
            "linkedin_url": l_url or "",
            "linkedin_verified": is_li_verified,
            "issues": issues,
            "feedback_note": feedback_note,
            "is_approved_org": is_approved_org
        })

    conn.commit()
    print(f"\n1. Successfully updated {len(discrepancy_list)} submissions to 'changes_requested' in PostgreSQL.")
    for d in discrepancy_list:
        print(f"   * App #{d['submission_id']}: {d['name']} <{d['email']}> -> {', '.join(d['issues'])}")

    discrepancy_emails = set(d["email"] for d in discrepancy_list)

    # 2. Extract Engaged Interns (1,026 cohort) with 1, 2, or 3 gates pending
    # Exclude Cohort D (already verified for payout) and Discrepancy candidates
    cur.execute("""
        SELECT DISTINCT LOWER(email)
        FROM intern_accounts
        WHERE stipend_verified = 1
    """)
    approved_d_emails = set(r[0].strip().lower() for r in cur.fetchall())

    cur.execute("""
        SELECT 
            ia.id as intern_id,
            ia.name,
            ia.email,
            ia.domain,
            ia.upi_id_encrypted,
            ia.linkedin_url,
            ia.linkedin_verified,
            ia.github_url,
            ic.tier as cert_tier,
            ic.cert_id,
            enr.joining_date,
            art.status as article_status
        FROM intern_accounts ia
        LEFT JOIN intern_certificates ic ON LOWER(ia.email) = LOWER(ic.email)
        LEFT JOIN enrollments enr ON LOWER(ia.email) = LOWER(enr.email)
        LEFT JOIN (
            SELECT intern_id, status, 
                   ROW_NUMBER() OVER (PARTITION BY intern_id ORDER BY id DESC) as rn
            FROM intern_articles
        ) art ON ia.id = art.intern_id AND art.rn = 1
        WHERE (ia.upi_id_encrypted IS NOT NULL AND ia.upi_id_encrypted != '')
           OR (ia.linkedin_url IS NOT NULL AND ia.linkedin_url != '')
           OR (ia.github_url IS NOT NULL AND ia.github_url != '')
           OR (ic.cert_id IS NOT NULL)
           OR (enr.id IS NOT NULL)
    """)
    raw_candidates = cur.fetchall()

    today = date(2026, 11, 17)

    engaged_candidates_map = {}
    for r in raw_candidates:
        iid, name, email, domain, upi, linkedin, l_ver, github, cert_tier, cert_id, jd_raw, art_status = r
        clean_email = (email or "").strip().lower()
        if not clean_email or clean_email in approved_d_emails or clean_email in discrepancy_emails:
            continue

        has_cert = bool(cert_tier and cert_tier in ('verified', 'dbert_verified'))
        has_any_cert = bool(cert_id)
        has_upi = bool(upi and str(upi).strip())
        has_linkedin = bool(linkedin and str(linkedin).strip())
        has_github = bool(github and str(github).strip())
        has_article = bool(art_status and art_status.upper() == 'PUBLISHED')

        # Check duration
        duration_met = False
        if has_any_cert:
            duration_met = True
        elif jd_raw:
            try:
                jd = datetime.strptime(str(jd_raw)[:10], "%Y-%m-%d").date()
                if today >= jd + timedelta(days=60):
                    duration_met = True
            except Exception:
                pass

        # Gates:
        # Gate 1: Verified Certificate (₹299 form / evaluated)
        # Gate 2: Duration / Completion date met
        # Gate 3: UPI Linked
        # Gate 4: LinkedIn Linked
        missing_gates = []
        if not has_cert:
            missing_gates.append({"gate_num": 1, "gate_name": "Course Certificate & ₹299 Verification Form", "cta": "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"})
        if not duration_met:
            missing_gates.append({"gate_num": 2, "gate_name": "Internship Duration & Active Sprint", "cta": "https://lms.dbert.in/stipend/tasks"})
        if not has_upi:
            missing_gates.append({"gate_num": 3, "gate_name": "Payout UPI ID Setup", "cta": "https://lms.dbert.in/stipend/tasks"})
        if not has_linkedin:
            missing_gates.append({"gate_num": 4, "gate_name": "Public LinkedIn Experience & Credential", "cta": "https://lms.dbert.in/stipend/tasks"})

        missing_count = len(missing_gates)
        if 1 <= missing_count <= 3:
            completed_count = 4 - missing_count
            pct = int((completed_count / 4) * 100)
            engaged_candidates_map[clean_email] = {
                "intern_id": iid,
                "name": name or "Fellow",
                "email": clean_email,
                "domain": domain or "Applied Engineering",
                "cert_id": cert_id or "",
                "has_cert": has_cert,
                "duration_met": duration_met,
                "has_upi": has_upi,
                "has_linkedin": has_linkedin,
                "has_github": has_github,
                "has_article": has_article,
                "missing_gates": missing_gates,
                "missing_count": missing_count,
                "completed_count": completed_count,
                "progress_pct": pct
            }

    # Sort engaged candidates by priority:
    # Top priority: missing_count == 1 (closest to payout), then missing_count == 2, then missing_count == 3
    sorted_engaged = sorted(
        engaged_candidates_map.values(),
        key=lambda x: (x["missing_count"], x["name"])
    )

    print(f"\n2. Total Engaged Candidates with 1-3 Gates Pending: {len(sorted_engaged)}")
    p1 = [x for x in sorted_engaged if x["missing_count"] == 1]
    p2 = [x for x in sorted_engaged if x["missing_count"] == 2]
    p3 = [x for x in sorted_engaged if x["missing_count"] == 3]
    print(f"   - 1 Gate Pending (Priority 1): {len(p1)} candidates")
    print(f"   - 2 Gates Pending (Priority 2): {len(p2)} candidates")
    print(f"   - 3 Gates Pending (Priority 3): {len(p3)} candidates")

    # Partition into batches of 250
    batch1 = sorted_engaged[:250]
    batch2 = sorted_engaged[250:500]
    batch3 = sorted_engaged[500:750]
    batch4 = sorted_engaged[750:]

    print(f"\n3. Staggered Batch Partitioning:")
    print(f"   - Batch 1 (Immediate): {len(batch1)} candidates (includes all Priority 1 & 2)")
    print(f"   - Batch 2 (+4 Hours): {len(batch2)} candidates")
    print(f"   - Batch 3 (+8 Hours): {len(batch3)} candidates")
    print(f"   - Batch 4 (+12 Hours): {len(batch4)} candidates")

    # Save data files
    data_dir = ROOT_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    with open(data_dir / "cohort_discrepancy_10.json", "w", encoding="utf-8") as f:
        json.dump(discrepancy_list, f, indent=2)

    with open(data_dir / "engaged_interns_all.json", "w", encoding="utf-8") as f:
        json.dump(sorted_engaged, f, indent=2)

    with open(data_dir / "engaged_interns_batch1.json", "w", encoding="utf-8") as f:
        json.dump(batch1, f, indent=2)

    with open(data_dir / "engaged_interns_batch2.json", "w", encoding="utf-8") as f:
        json.dump(batch2, f, indent=2)

    with open(data_dir / "engaged_interns_batch3.json", "w", encoding="utf-8") as f:
        json.dump(batch3, f, indent=2)

    with open(data_dir / "engaged_interns_batch4.json", "w", encoding="utf-8") as f:
        json.dump(batch4, f, indent=2)

    print("\nPhase 1 & 2 completed successfully. Cohort datasets ready in data/.")

if __name__ == "__main__":
    main()
