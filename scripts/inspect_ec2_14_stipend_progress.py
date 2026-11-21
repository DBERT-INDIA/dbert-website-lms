import sys
import os
import json
from datetime import datetime, date

sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import get_db
from services.certificate_service import CertificateService

subs = json.load(open("/var/www/dbert-website-lms/data/verification_submissions_299.json"))[4:]

print(f"Inspecting 14 candidates' LMS Account & Stipend Progress:")
print("=" * 115)

with get_db() as conn:
    for idx, s in enumerate(subs, 1):
        email = (s.get("email") or "").strip().lower()
        cid = s.get("certId")
        name = s.get("fullName")
        phone_sub = s.get("phone")
        
        # 1. Check account
        acct = conn.execute(
            """
            SELECT id, email, phone, domain, upi_id_encrypted, stipend_verified, 
                   stipend_release_date, stipend_amount, linkedin_verified
            FROM intern_accounts 
            WHERE LOWER(email) = LOWER(?)
            """,
            (email,)
        ).fetchone()
        
        # 2. Gate status
        ver_info = CertificateService.is_intern_verified(conn, email=email)
        comp_info = CertificateService.get_intern_completion_info(conn, email=email)
        
        has_upi = bool(acct and acct["upi_id_encrypted"])
        stipend_rel_date = (acct["stipend_release_date"] if acct else "") or ""
        stipend_amt = (acct["stipend_amount"] if acct and acct["stipend_amount"] else 5499)
        stipend_ver = bool(acct and (acct["stipend_verified"] == 1 or acct["stipend_verified"] is True))
        
        print(f"\n{idx}. [{cid}] {name} ({email})")
        print(f"   Phone in sub: {phone_sub} | Account Phone: {acct['phone'] if acct else 'No Account'}")
        print(f"   Gate 1 (Cert Verified): {ver_info.get('verified')} ({ver_info.get('status')})")
        print(f"   Gate 2 (Completion): {comp_info.get('is_completed')} | Completion Date: {comp_info.get('completion_date')} | Days Remaining: {comp_info.get('days_remaining')}")
        print(f"   Gate 3 (UPI Encrypted): {has_upi}")
        print(f"   Stipend Amount: ₹{stipend_amt} | Stipend Verified: {stipend_ver} | Scheduled Release Date: {stipend_rel_date or 'Not scheduled yet (Pending contribution submission)'}")
