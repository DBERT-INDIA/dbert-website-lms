#!/usr/bin/env python3
"""
scripts/audit_stipend_gates.py
Comprehensive audit of intern stipend progression, gating completion, and payout eligibility.
"""
import sys
import os
import json
from datetime import datetime, date, timedelta
import calendar

# Path setup for EC2 / local
portal_dir = "/var/www/dbert-website-lms/apps/portal"
if os.path.isdir(portal_dir):
    sys.path.insert(0, portal_dir)
else:
    sys.path.insert(0, os.path.abspath("apps/portal"))

from app import get_db, FERNET_KEY
from services.certificate_service import CertificateService

def parse_flexible_date(date_str):
    if not date_str or not isinstance(date_str, str):
        return None
    clean = date_str.strip()
    for fmt in ("%Y-%m-%d", "%d %B %Y", "%d %b %Y"):
        try:
            return datetime.strptime(clean, fmt).date()
        except ValueError:
            pass
    for fmt in ("%B %Y", "%b %Y"):
        try:
            dt = datetime.strptime(clean, fmt)
            last_day = calendar.monthrange(dt.year, dt.month)[1]
            return date(dt.year, dt.month, last_day)
        except ValueError:
            pass
    return None

def main():
    today = date.today()
    print(f"================================================================================")
    print(f"DBERT STIPEND GATES AUDIT (Phase 13 & 14)")
    print(f"Current Date: {today.strftime('%Y-%m-%d')} ({today.strftime('%A, %d %B %Y')})")
    print(f"================================================================================")

    # 1. Load Registry
    registry_path = CertificateService.resolve_registry_path()
    registry_records = []
    reg_by_email = {}
    reg_by_cert = {}
    if registry_path and os.path.isfile(registry_path):
        with open(registry_path, "r", encoding="utf-8") as f:
            raw_reg = json.load(f)
            if isinstance(raw_reg, dict):
                registry_records = list(raw_reg.values())
            elif isinstance(raw_reg, list):
                registry_records = raw_reg
        for r in registry_records:
            if isinstance(r, dict):
                em = (r.get("email") or "").strip().lower()
                cid = (r.get("certId") or "").strip().lower()
                if em:
                    reg_by_email[em] = r
                if cid:
                    reg_by_cert[cid] = r
    print(f"Total Registry Records Loaded: {len(registry_records)}")
    verified_reg = [r for r in registry_records if isinstance(r, dict) and r.get("verified") and not r.get("isProvisional")]
    provisional_reg = [r for r in registry_records if isinstance(r, dict) and r.get("isProvisional")]
    print(f"  - Officially Verified: {len(verified_reg)}")
    print(f"  - Provisional Credentials: {len(provisional_reg)}")

    # 2. Query Database
    with get_db() as conn:
        interns = conn.execute("SELECT * FROM intern_accounts ORDER BY id ASC").fetchall()
        print(f"Total Registered Intern Accounts in LMS: {len(interns)}")

        enrollments = conn.execute("SELECT * FROM enrollments").fetchall()
        print(f"Total Course/Internship Enrollments in LMS: {len(enrollments)}")

        certificates = conn.execute("SELECT * FROM intern_certificates").fetchall()
        print(f"Total Issued Certificates in LMS: {len(certificates)}")

        submissions = conn.execute("SELECT * FROM task_submissions WHERE task_category = 'stipend_milestone' OR task_id IN (SELECT id FROM tasks WHERE task_type = 'stipend_milestone')").fetchall()
        print(f"Total Stipend Milestone Submissions: {len(submissions)}")

        coin_ledger = conn.execute("SELECT * FROM coin_ledger_mirror WHERE delta = 5000 OR ledger_kind = 'referral' OR LOWER(reason) LIKE '%stipend%'").fetchall()
        print(f"Total Stipend-related Coin Ledger Entries: {len(coin_ledger)}")

        # Map enrollments by email
        enrollments_by_email = {}
        for en in enrollments:
            em = (en["email"] or "").strip().lower()
            if em:
                enrollments_by_email.setdefault(em, []).append(en)

        # Map submissions by intern_id and email
        subs_by_intern = {}
        for s in submissions:
            subs_by_intern.setdefault(s["intern_id"], []).append(s)

        # Map coin rewards by intern_id
        coins_by_intern = {}
        for c in coin_ledger:
            coins_by_intern.setdefault(c["intern_id"], []).append(c)

        # Audit each intern account
        stats = {
            "total_accounts": len(interns),
            "gate_1_verified_cert": 0,
            "gate_1_provisional_cert": 0,
            "gate_2_duration_completed": 0,
            "gate_3_upi_linked": 0,
            "gate_4_linkedin_linked_or_verified": 0,
            "all_4_gates_completed": 0,
            "gates_3_completed": 0,
            "gates_2_completed": 0,
            "gates_1_completed": 0,
            "gates_0_completed": 0,
            "stipend_submitted": 0,
            "stipend_approved": 0,
            "stipend_released_5000": 0,
        }

        all_4_interns = []
        three_gates_interns = []
        verified_cert_interns = []

        for intern in interns:
            iid = intern["id"]
            name = intern["name"] or "Unknown"
            email = (intern["email"] or "").strip().lower()
            domain = intern["domain"] or ""
            
            # --- GATE 1: Certificate Verification ---
            ver_info = CertificateService.is_intern_verified(conn, intern_id=iid, email=email)
            g1_pass = bool(ver_info.get("verified"))
            is_prov = bool(ver_info.get("is_provisional"))
            if g1_pass:
                stats["gate_1_verified_cert"] += 1
                verified_cert_interns.append({"id": iid, "name": name, "email": email, "cert_id": ver_info.get("cert_id")})
            elif is_prov:
                stats["gate_1_provisional_cert"] += 1

            # --- GATE 2: Duration / Completion Date ---
            comp_info = CertificateService.get_intern_completion_info(conn, intern_id=iid, email=email)
            g2_pass = bool(comp_info.get("is_completed"))
            if g2_pass:
                stats["gate_2_duration_completed"] += 1

            # --- GATE 3: Payout UPI Linked ---
            g3_pass = bool(intern["upi_id_encrypted"])
            if g3_pass:
                stats["gate_3_upi_linked"] += 1

            # --- GATE 4: Public LinkedIn Linked or Verified ---
            has_li = bool(intern["linkedin_url"])
            li_ver = bool(intern["linkedin_verified"])
            g4_pass = has_li or li_ver
            if g4_pass:
                stats["gate_4_linkedin_linked_or_verified"] += 1

            # Gate count
            gates_count = sum([1 if g1_pass else 0, 1 if g2_pass else 0, 1 if g3_pass else 0, 1 if g4_pass else 0])

            # Check submissions & releases
            intern_subs = subs_by_intern.get(iid, [])
            sub_status = None
            if intern_subs:
                stats["stipend_submitted"] += 1
                sub_status = intern_subs[0]["status"]
                if any(s["status"] == "approved" for s in intern_subs):
                    stats["stipend_approved"] += 1

            intern_coins = coins_by_intern.get(iid, [])
            released_5k = any(c["delta"] == 5000 for c in intern_coins)
            if released_5k:
                stats["stipend_released_5000"] += 1

            rec = {
                "id": iid,
                "name": name,
                "email": email,
                "domain": domain,
                "g1_verified": g1_pass,
                "g1_status": ver_info.get("status"),
                "cert_id": ver_info.get("cert_id"),
                "g2_completed": g2_pass,
                "completion_date": comp_info.get("completion_date_display"),
                "g3_upi": g3_pass,
                "g4_linkedin": g4_pass,
                "linkedin_status": intern.get("linkedin_verification_status"),
                "gates_passed": gates_count,
                "submitted": len(intern_subs) > 0,
                "sub_status": sub_status,
                "coins_released": released_5k
            }

            if gates_count == 4:
                stats["all_4_gates_completed"] += 1
                all_4_interns.append(rec)
            elif gates_count == 3:
                stats["gates_3_completed"] += 1
                three_gates_interns.append(rec)
            elif gates_count == 2:
                stats["gates_2_completed"] += 1
            elif gates_count == 1:
                stats["gates_1_completed"] += 1
            else:
                stats["gates_0_completed"] += 1

    print("\n--------------------------------------------------------------------------------")
    print("STIPEND GATE AUDIT SUMMARY")
    print("--------------------------------------------------------------------------------")
    print(f"Total Registered Interns in LMS:             {stats['total_accounts']}")
    print(f"Gate 1 (Course Certificate Verified):        {stats['gate_1_verified_cert']}")
    print(f"  * (Provisional Credentials in LMS):        {stats['gate_1_provisional_cert']}")
    print(f"Gate 2 (Internship Duration Completed):      {stats['gate_2_duration_completed']}")
    print(f"Gate 3 (Payout UPI ID Linked):               {stats['gate_3_upi_linked']}")
    print(f"Gate 4 (LinkedIn Profile Linked/Verified):   {stats['gate_4_linkedin_linked_or_verified']}")
    print("--------------------------------------------------------------------------------")
    print(f"ALL 4 GATES COMPLETED (100% Ready):          {stats['all_4_gates_completed']}")
    print(f"3 of 4 Gates Completed (1 Gate Away):        {stats['gates_3_completed']}")
    print(f"2 of 4 Gates Completed:                      {stats['gates_2_completed']}")
    print(f"1 of 4 Gates Completed:                      {stats['gates_1_completed']}")
    print(f"0 of 4 Gates Completed:                      {stats['gates_0_completed']}")
    print("--------------------------------------------------------------------------------")
    print(f"Stipend Submissions Received:                {stats['stipend_submitted']}")
    print(f"Stipend Submissions Approved by Staff:       {stats['stipend_approved']}")
    print(f"₹5,000 Stipend Released (Coins Credited):    {stats['stipend_released_5000']}")
    print("--------------------------------------------------------------------------------")

    if all_4_interns:
        print("\nINTERNS WHO HAVE COMPLETED ALL 4 GATES:")
        for idx, a in enumerate(all_4_interns, 1):
            print(f"  {idx}. Intern #{a['id']}: {a['name']} ({a['email']})")
            print(f"     Cert: {a['cert_id']} | Domain: {a['domain']} | Completion: {a['completion_date']}")
            print(f"     Submission: {'Yes (' + str(a['sub_status']) + ')' if a['submitted'] else 'None'}")
            print(f"     Coins Released: {'Yes (5,000)' if a['coins_released'] else 'No'}")
    else:
        print("\nNO INTERNS HAVE COMPLETED ALL 4 GATES YET.")

    if three_gates_interns:
        print("\nINTERNS WITH 3 GATES COMPLETED (1 GATE MISSING):")
        for idx, a in enumerate(three_gates_interns, 1):
            missing = []
            if not a['g1_verified']: missing.append("Gate 1: Certificate Verification")
            if not a['g2_completed']: missing.append("Gate 2: Duration")
            if not a['g3_upi']: missing.append("Gate 3: UPI")
            if not a['g4_linkedin']: missing.append("Gate 4: LinkedIn")
            print(f"  {idx}. Intern #{a['id']}: {a['name']} ({a['email']}) - Missing: {', '.join(missing)}")

    # Check verified candidates from registry who have not yet logged in / created LMS account
    print("\n--------------------------------------------------------------------------------")
    print("VERIFIED CERTIFICATE HOLDERS (OFFICIALLY ELIGIBLE TO COMPLETE GATES)")
    print("--------------------------------------------------------------------------------")
    verified_reg_emails = set(r.get("email", "").strip().lower() for r in verified_reg if r.get("email"))
    lms_emails = set(i["email"].strip().lower() for i in interns if i["email"])
    
    in_lms_verified = verified_reg_emails.intersection(lms_emails)
    not_in_lms_verified = verified_reg_emails.difference(lms_emails)
    print(f"Total Officially Verified Certificate Holders in Registry: {len(verified_reg_emails)}")
    print(f"  - Active on LMS (LMS Account Created):                   {len(in_lms_verified)}")
    print(f"  - Not yet on LMS (Can 1-click onboard with password set): {len(not_in_lms_verified)}")

if __name__ == "__main__":
    main()
