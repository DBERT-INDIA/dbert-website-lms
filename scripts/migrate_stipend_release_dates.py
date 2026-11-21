import os
import sys

sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
os.chdir("/var/www/dbert-website-lms/apps/portal")

from app import get_db

def migrate():
    with get_db() as conn:
        print("=== BEFORE MIGRATION: Candidates with stipend_release_date < '2026-12-03' ===")
        rows = conn.execute("""
            SELECT id, name, email, domain, stipend_release_date 
            FROM intern_accounts 
            WHERE stipend_release_date IS NOT NULL 
              AND stipend_release_date != '' 
              AND stipend_release_date < '2026-12-03'
        """).fetchall()
        for r in rows:
            print(f"- ID: {r['id']} | Name: {r['name']} | Email: {r['email']} | Current Date: {r['stipend_release_date']}")

        print(f"\nUpdating {len(rows)} rows to '2026-12-03'...")
        conn.execute("""
            UPDATE intern_accounts 
            SET stipend_release_date = '2026-12-03' 
            WHERE stipend_release_date IS NOT NULL 
              AND stipend_release_date != '' 
              AND stipend_release_date < '2026-12-03'
        """)
        conn.commit()
        print("Update committed.")

        print("\n=== AFTER MIGRATION: All scheduled candidates ===")
        all_scheduled = conn.execute("""
            SELECT id, name, email, domain, stipend_release_date, stipend_verified 
            FROM intern_accounts 
            WHERE (stipend_release_date IS NOT NULL AND stipend_release_date != '') OR stipend_verified = 1
            ORDER BY stipend_release_date ASC NULLS LAST
        """).fetchall()
        for s in all_scheduled:
            print(f"- {s['name']} ({s['email']}) | Release Date: {s.get('stipend_release_date')} | Stipend Verified: {s.get('stipend_verified')}")

if __name__ == "__main__":
    migrate()
