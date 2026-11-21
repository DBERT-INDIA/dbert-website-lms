import os
import sys
import json
from datetime import datetime

sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
os.chdir("/var/www/dbert-website-lms/apps/portal")

from app import get_db, decrypt_upi, mask_upi

def run_audit():
    with get_db() as conn:
        print("================================================================================")
        print("DBERT LMS: TILL-DATE STIPEND RELEASE GATES, DATES & CANDIDATE BREAKDOWN")
        print(f"Audit Executed At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}")
        print("================================================================================\n")

        # 1. CANDIDATES WITH EXPLICIT CONFIRMED STIPEND RELEASE DATES
        print("--- 1. CONFIRMED STIPEND RELEASE DATES (SCHEDULED CANDIDATES) ---")
        scheduled = conn.execute("""
            SELECT id, name, email, domain, stipend_verified, stipend_release_date, 
                   stipend_amount, verified_github_org, verified_github_repo,
                   linkedin_verified, upi_id_encrypted
            FROM intern_accounts 
            WHERE (stipend_release_date IS NOT NULL AND stipend_release_date != '') OR stipend_verified = 1
            ORDER BY stipend_release_date ASC NULLS LAST
        """).fetchall()

        for s in scheduled:
            upi_dec = ""
            if s.get("upi_id_encrypted"):
                try:
                    upi_dec = mask_upi(decrypt_upi(s["upi_id_encrypted"]))
                except Exception:
                    upi_dec = "Active (Encrypted)"
            print(f"Candidate: {s['name']} ({s['email']}) [ID: {s['id']}]")
            print(f"  • Domain: {s['domain']}")
            print(f"  • Confirmed Release Date: {s.get('stipend_release_date') or 'Pending Scheduling'}")
            print(f"  • Stipend Amount: Rs {s.get('stipend_amount')}")
            print(f"  • Gate 1 (Credential): Verified ({s.get('stipend_verified')})")
            print(f"  • Gate 3 (UPI): {upi_dec}")
            print(f"  • LinkedIn Verified: {bool(s.get('linkedin_verified'))}")
            print(f"  • Verified GitHub: {s.get('verified_github_org')}/{s.get('verified_github_repo')}")
            print()

        # 2. CAPSTONE TASK SUBMISSIONS (Tasks 3, 4, 5, 6)
        print("--- 2. CAPSTONE MILESTONE TASK SUBMISSIONS (Tasks 3, 4, 5, 6) ---")
        subs = conn.execute("""
            SELECT s.id, s.task_id, s.intern_id, s.status, s.created_at,
                   a.name, a.email, a.domain, a.stipend_release_date, a.stipend_verified
            FROM task_submissions s
            JOIN intern_accounts a ON s.intern_id = a.id
            WHERE s.task_id IN (3, 4, 5, 6)
            ORDER BY s.id DESC
        """).fetchall()
        print(f"Total Capstone Submissions: {len(subs)}")
        for sub in subs:
            print(f"Submission #{sub['id']} | Task #{sub['task_id']} | Intern: {sub['name']} ({sub['email']})")
            print(f"  Status: {sub['status']} | Submitted: {sub['created_at']} | Release Date: {sub.get('stipend_release_date') or 'Pending Review'}")
            print()

        # 3. COIN LEDGER CREDITS
        print("--- 3. COIN LEDGER CREDITS & WITHDRAWABLE BALANCES ---")
        try:
            coins = conn.execute("""
                SELECT c.id, c.intern_id, c.delta, c.ledger_kind, c.reason, c.received_at,
                       a.name, a.email
                FROM coin_ledger_mirror c
                JOIN intern_accounts a ON c.intern_id = a.id
                WHERE c.delta > 0
                ORDER BY c.id DESC
                LIMIT 30
            """).fetchall()
            print(f"Recent coin ledger credits: {len(coins)}")
            for c in coins:
                print(f"Credit #{c['id']} | Intern: {c['name']} ({c['email']}) | +{c['delta']} coins ({c['ledger_kind']}) | Reason: {c['reason']} | Date: {c['received_at']}")
        except Exception as e:
            print(f"Coin error: {e}")
        print()

        # 4. ALL VERIFIED INTERN CERTIFICATES SUMMARY
        print("--- 4. MASTER SUMMARY OF ALL VERIFIED INTERN CERTIFICATES ---")
        try:
            certs = conn.execute("""
                SELECT c.cert_id, c.tier, c.course_title,
                       a.id as intern_id, a.name, a.email, a.stipend_verified, a.stipend_release_date,
                       a.upi_id_encrypted
                FROM intern_certificates c
                LEFT JOIN intern_accounts a ON c.intern_id = a.id
                WHERE c.tier = 'verified'
                ORDER BY a.stipend_release_date ASC NULLS LAST, a.name ASC
            """).fetchall()
            print(f"Total Verified Tier Certificates in LMS Database: {len(certs)}")
            has_release_date = [c for c in certs if c.get('stipend_release_date')]
            pending_review = [c for c in certs if not c.get('stipend_release_date')]
            print(f"• Scheduled Release Date Assigned: {len(has_release_date)}")
            print(f"• Awaiting Capstone Review / Scheduling: {len(pending_review)}")
            print("\nBreakdown of Verified Candidates:")
            for ct in certs:
                stip_ver = ct.get("stipend_verified")
                rel_date = ct.get("stipend_release_date") or "Pending Review"
                has_upi = bool(ct.get("upi_id_encrypted"))
                print(f"  • {ct.get('cert_id')} | {ct.get('name')} ({ct.get('email')}) | Track: {ct.get('course_title')} | Scheduled Release: {rel_date} | UPI Active: {has_upi}")
        except Exception as e:
            print(f"Cert error: {e}")

if __name__ == "__main__":
    run_audit()
