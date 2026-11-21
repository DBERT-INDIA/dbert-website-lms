import os
import sys
import json
from datetime import datetime, date

sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db
from services.certificate_service import CertificateService

with app.app_context():
    with get_db() as conn:
        cols_res = conn.execute("""
            SELECT column_name FROM information_schema.columns WHERE table_name = 'intern_accounts'
        """).fetchall()
        print("Columns in intern_accounts:", [r["column_name"] for r in cols_res])

        # Query all accounts with linkedin_url
        accounts = conn.execute("""
            SELECT id, email, name, phone, domain, college, upi_id_encrypted, linkedin_url, linkedin_verification_status
            FROM intern_accounts
            WHERE linkedin_url IS NOT NULL AND TRIM(linkedin_url) != ''
            ORDER BY id ASC
        """).fetchall()

        print(f"Total interns with LinkedIn URL: {len(accounts)}")

        cohort_only_299_pending = []
        cohort_linkedin_upi_unverified = []
        cohort_all_linkedin_unverified = []

        for acct in accounts:
            intern_id = acct["id"]
            email = (acct["email"] or "").strip().lower()
            name = acct["name"] or "Intern"
            phone = acct["phone"] or ""
            domain = acct["domain"] or ""
            linkedin_url = acct["linkedin_url"]
            has_upi = bool(acct["upi_id_encrypted"])

            # Gate 1: Verification
            ver_info = CertificateService.is_intern_verified(conn, intern_id=intern_id, email=email)
            is_verified = bool(ver_info.get("verified"))

            # Gate 2: Completion
            comp_info = CertificateService.get_intern_completion_info(conn, intern_id=intern_id, email=email)
            is_completed = bool(comp_info.get("is_completed"))
            comp_date = comp_info.get("completion_date")
            days_remaining = comp_info.get("days_remaining", 0)

            # Record item
            candidate_data = {
                "id": intern_id,
                "name": name,
                "email": email,
                "phone": phone,
                "domain": domain or ver_info.get("domain", ""),
                "college": acct["college"] or "",
                "linkedin_url": linkedin_url,
                "linkedin_status": acct["linkedin_verification_status"] or "UNVERIFIED",
                "has_upi": has_upi,
                "is_verified": is_verified,
                "cert_id": ver_info.get("cert_id", ""),
                "cert_status": ver_info.get("status", "UNVERIFIED"),
                "is_completed": is_completed,
                "completion_date": str(comp_date) if comp_date else "",
                "days_remaining": days_remaining,
            }

            if not is_verified:
                cohort_all_linkedin_unverified.append(candidate_data)
                if has_upi:
                    cohort_linkedin_upi_unverified.append(candidate_data)
                    if is_completed:
                        cohort_only_299_pending.append(candidate_data)

        print("\n--- RESULTS BREAKDOWN ---")
        print(f"1. Total with LinkedIn: {len(accounts)}")
        print(f"2. Total with LinkedIn & Unverified (Gate 1 needed): {len(cohort_all_linkedin_unverified)}")
        print(f"3. Total with LinkedIn + UPI Configured + Unverified: {len(cohort_linkedin_upi_unverified)}")
        print(f"4. STRICT ONLY ₹299 PENDING (LinkedIn + UPI Done + Completed/Tenure Passed + Unverified): {len(cohort_only_299_pending)}")

        output_file = "/tmp/linkedin_stipend_cohort_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({
                "counts": {
                    "total_linkedin": len(accounts),
                    "all_linkedin_unverified": len(cohort_all_linkedin_unverified),
                    "linkedin_upi_unverified": len(cohort_linkedin_upi_unverified),
                    "strict_only_299_pending": len(cohort_only_299_pending)
                },
                "strict_only_299_pending": cohort_only_299_pending,
                "linkedin_upi_unverified": cohort_linkedin_upi_unverified,
                "all_linkedin_unverified": cohort_all_linkedin_unverified
            }, f, indent=2)
        print(f"\nSaved detailed JSON to {output_file}")
