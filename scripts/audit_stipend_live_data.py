import os
import sys
import json
from datetime import datetime

sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
os.chdir("/var/www/dbert-website-lms/apps/portal")

from app import get_db, decrypt_upi, mask_upi

def run_audit():
    with get_db() as conn:
        print("=== 1. STIPEND VERIFIED & SCHEDULED CANDIDATES (FROM intern_accounts) ===")
        scheduled = conn.execute("""
            SELECT id, name, email, domain, stipend_verified, stipend_release_date, 
                   stipend_amount, verified_github_org, verified_github_repo,
                   linkedin_verified, upi_id_encrypted
            FROM intern_accounts 
            WHERE stipend_verified = 1 OR (stipend_release_date IS NOT NULL AND stipend_release_date != '')
            ORDER BY stipend_release_date ASC NULLS LAST
        """).fetchall()
        
        print(f"Total explicitly scheduled/verified candidates: {len(scheduled)}")
        for row in scheduled:
            upi_raw = ""
            if row.get("upi_id_encrypted"):
                try:
                    upi_raw = mask_upi(decrypt_upi(row["upi_id_encrypted"]))
                except Exception:
                    upi_raw = "Active (Encrypted)"
            print(f"- ID: {row['id']} | Name: {row['name']} | Email: {row['email']}")
            print(f"  Domain: {row['domain']} | Stipend Amount: Rs {row.get('stipend_amount')}")
            print(f"  Stipend Verified: {row.get('stipend_verified')} | Release Date: {row.get('stipend_release_date')}")
            print(f"  UPI: {upi_raw} | LinkedIn Verified: {row.get('linkedin_verified')}")
            print(f"  Verified Repo: {row.get('verified_github_org')}/{row.get('verified_github_repo')}")
            print()

        print("=== 2. TASK SUBMISSIONS (task_submissions) ===")
        try:
            subs = conn.execute("""
                SELECT s.*, a.name, a.email, a.domain
                FROM task_submissions s
                JOIN intern_accounts a ON s.intern_id = a.id
                ORDER BY s.id DESC
            """).fetchall()
            print(f"Total task submissions found: {len(subs)}")
            for s in subs:
                status = s.get("status")
                sub_id = s.get("id")
                task_id = s.get("task_id")
                name = s.get("name")
                email = s.get("email")
                created = s.get("created_at") or s.get("submitted_at")
                print(f"- Submission #{sub_id} | Task: {task_id} | Intern: {name} ({email}) | Status: {status} | Created: {created}")
        except Exception as e:
            print(f"Error querying task_submissions: {e}")
        print()

        print("=== 3. AMBASSADOR WITHDRAWALS (ambassador_withdrawals) ===")
        try:
            withs = conn.execute("""
                SELECT w.*, a.name, a.email
                FROM ambassador_withdrawals w
                JOIN intern_accounts a ON w.intern_id = a.id
                ORDER BY w.id DESC
            """).fetchall()
            print(f"Total withdrawal requests found: {len(withs)}")
            for w in withs:
                w_id = w.get("id")
                name = w.get("name")
                email = w.get("email")
                coins = w.get("amount_coins") or w.get("coins") or w.get("amount")
                inr = w.get("inr_value") or w.get("inr")
                status = w.get("status")
                created = w.get("created_at")
                paid = w.get("processed_at") or w.get("paid_at")
                print(f"- Withdrawal #{w_id} | Intern: {name} ({email}) | Coins: {coins} (Rs {inr}) | Status: {status} | Created: {created} | Paid: {paid}")
        except Exception as e:
            print(f"Error querying ambassador_withdrawals: {e}")
        print()

        print("=== 4. COIN LEDGER CREDITS (coin_ledger_mirror) ===")
        try:
            coins = conn.execute("""
                SELECT c.*, a.name, a.email
                FROM coin_ledger_mirror c
                JOIN intern_accounts a ON c.intern_id = a.id
                WHERE c.amount > 0
                ORDER BY c.id DESC
                LIMIT 25
            """).fetchall()
            print(f"Recent coin ledger credits: {len(coins)}")
            for c in coins:
                c_id = c.get("id")
                name = c.get("name")
                email = c.get("email")
                amount = c.get("amount")
                kind = c.get("ledger_kind")
                desc = c.get("description")
                created = c.get("created_at")
                print(f"- Credit #{c_id} | Intern: {name} ({email}) | Coins: +{amount} ({kind}) | Desc: {desc} | At: {created}")
        except Exception as e:
            print(f"Error querying coin_ledger_mirror: {e}")
        print()

        print("=== 5. ALL VERIFIED CANDIDATES & GATES CALCULATION ===")
        try:
            certs = conn.execute("""
                SELECT c.id, c.cert_id, c.tier, c.domain, c.created_at,
                       a.id as intern_id, a.name, a.email, a.stipend_verified, a.stipend_release_date,
                       a.stipend_amount, a.upi_id_encrypted, a.linkedin_verified
                FROM intern_certificates c
                LEFT JOIN intern_accounts a ON c.intern_id = a.id
                WHERE c.tier = 'verified'
                ORDER BY a.stipend_release_date ASC NULLS LAST, c.id ASC
            """).fetchall()
            print(f"Total tier='verified' certificates in DB: {len(certs)}")
            for ct in certs:
                stip_ver = ct.get("stipend_verified")
                rel_date = ct.get("stipend_release_date")
                has_upi = bool(ct.get("upi_id_encrypted"))
                print(f"- Cert: {ct.get('cert_id')} | Name: {ct.get('name')} | Email: {ct.get('email')} | UPI: {has_upi} | StipendVerified: {stip_ver} | ReleaseDate: {rel_date}")
        except Exception as e:
            print(f"Error querying intern_certificates: {e}")

if __name__ == "__main__":
    run_audit()
