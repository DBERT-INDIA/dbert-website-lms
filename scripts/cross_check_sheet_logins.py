import os
import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.environ.get("DATABASE_URL", "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")

def run():
    print("=" * 70)
    print(" DBERT LMS Candidate Login Cross-Check (3,087 Google Sheet Applicants)")
    print("=" * 70)

    sheet_emails_file = "/tmp/sheet_emails_198139462.json"
    if not os.path.exists(sheet_emails_file):
        sheet_emails_file = "data/sheet_emails_198139462.json"

    with open(sheet_emails_file, "r", encoding="utf-8") as f:
        sheet_emails = json.load(f)

    total_sheet_candidates = len(sheet_emails)
    sheet_emails_set = set(e.strip().lower() for e in sheet_emails if e.strip())
    print(f"Loaded {len(sheet_emails_set)} unique emails from Google Sheet.")

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SET search_path TO dbert_internship, public;")

    # 1. Total records in applications matching sheet
    cur.execute("SELECT LOWER(email) as email, status FROM applications;")
    app_rows = cur.fetchall()
    all_app_dict = {r['email']: r['status'] for r in app_rows if r['email']}
    sheet_in_applications = {e: all_app_dict[e] for e in sheet_emails_set if e in all_app_dict}
    print(f"\n1. In 'applications' table: {len(sheet_in_applications)} / {total_sheet_candidates}")

    status_counts = {}
    for st in sheet_in_applications.values():
        st_clean = st or 'Empty'
        status_counts[st_clean] = status_counts.get(st_clean, 0) + 1
    print("   Application Status breakdown:")
    for st, c in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"     {st}: {c}")

    # 2. In intern_accounts
    cur.execute("SELECT id, LOWER(email) as email, name, password_set, is_active, created_at, updated_at FROM intern_accounts;")
    account_rows = cur.fetchall()
    all_accounts = {r['email']: r for r in account_rows if r['email']}
    sheet_in_accounts = {e: all_accounts[e] for e in sheet_emails_set if e in all_accounts}
    print(f"\n2. In 'intern_accounts' table: {len(sheet_in_accounts)} / {total_sheet_candidates}")

    # 3. In user_sessions (Real authenticated login sessions)
    cur.execute("SELECT DISTINCT LOWER(email) as email FROM user_sessions;")
    session_emails = set(r['email'] for r in cur.fetchall() if r['email'])
    sheet_with_sessions = sheet_emails_set.intersection(session_emails)
    print(f"\n3. In 'user_sessions' (confirmed login sessions): {len(sheet_with_sessions)} / {total_sheet_candidates}")

    # 4. In attendance
    cur.execute("SELECT * FROM attendance LIMIT 1;")
    sample_att = cur.fetchone()
    att_cols = list(sample_att.keys()) if sample_att else []
    print(f"\n4. Attendance columns: {att_cols}")
    
    cur.execute("SELECT * FROM attendance;")
    att_rows = cur.fetchall()
    sheet_att_rows = [r for r in att_rows if r.get('email') and r.get('email').strip().lower() in sheet_emails_set]
    sheet_att_emails = set(r['email'].strip().lower() for r in sheet_att_rows)
    print(f"   In 'attendance' table: {len(sheet_att_emails)} / {total_sheet_candidates}")
    
    # Check total_minutes > 0
    att_active = set(r['email'].strip().lower() for r in sheet_att_rows if (r.get('total_minutes') or 0) > 0)
    print(f"   With total_minutes > 0: {len(att_active)}")

    # 5. Check device_profiles
    cur.execute("SELECT DISTINCT LOWER(email) as email FROM device_profiles WHERE email IS NOT NULL;")
    dev_emails = set(r['email'] for r in cur.fetchall() if r['email'])
    sheet_with_device = sheet_emails_set.intersection(dev_emails)
    print(f"\n5. In 'device_profiles' (web visit with email stamped): {len(sheet_with_device)} / {total_sheet_candidates}")

    # 6. Check course enrollments
    cur.execute("SELECT DISTINCT ia.email FROM course_enrollments ce JOIN intern_accounts ia ON ce.intern_id = ia.id;")
    course_enr_emails = set(r['email'].strip().lower() for r in cur.fetchall() if r['email'])
    sheet_with_courses = sheet_emails_set.intersection(course_enr_emails)
    print(f"\n6. In 'course_enrollments': {len(sheet_with_courses)} / {total_sheet_candidates}")

    # 7. Check enrollments table
    cur.execute("SELECT DISTINCT LOWER(email) as email FROM enrollments;")
    enr_emails = set(r['email'] for r in cur.fetchall() if r['email'])
    sheet_in_enrollments = sheet_emails_set.intersection(enr_emails)
    print(f"\n7. In 'enrollments' table (caution deposit/form): {len(sheet_in_enrollments)} / {total_sheet_candidates}")

    # -------------------------------------------------------------
    # METRICS SUMMARY
    # -------------------------------------------------------------
    # Any confirmed login activity = session in user_sessions, or web visit in device_profiles, or attendance total_minutes > 0
    logged_in_active = set()
    logged_in_active.update(sheet_with_sessions)
    logged_in_active.update(sheet_with_device)
    logged_in_active.update(att_active)

    # Any credential provisioned / account exists
    has_account_or_attendance = set()
    has_account_or_attendance.update(sheet_in_accounts.keys())
    has_account_or_attendance.update(sheet_att_emails)

    never_logged_in = sheet_emails_set - logged_in_active
    never_even_provisioned = sheet_emails_set - has_account_or_attendance

    print("\n" + "=" * 70)
    print(" FINAL VERIFIED SUMMARY METRICS")
    print("=" * 70)
    print(f"Total Unique Candidates in Google Sheet: {total_sheet_candidates:,}")
    print(f"----------------------------------------------------------------------")
    print(f"Candidates who have LOGGED IN to LMS (Active Session/Pings): {len(logged_in_active):,}")
    print(f"Candidates who have NEVER LOGGED ON LMS:                     {len(never_logged_in):,} ({(len(never_logged_in)/total_sheet_candidates)*100:.2f}%)")
    print(f"----------------------------------------------------------------------")
    print(f"Breakdown of the {len(never_logged_in):,} candidates who NEVER logged in:")
    print(f"  - Completely un-provisioned (No LMS account or attendance created): {len(never_even_provisioned):,}")
    print(f"  - Account provisioned but NEVER logged in (0 sessions / 0 minutes): {len(never_logged_in - never_even_provisioned):,}")
    print("=" * 70)

    # Export lists for tracking
    export_data = {
        "total_sheet_candidates": total_sheet_candidates,
        "logged_in_count": len(logged_in_active),
        "never_logged_in_count": len(never_logged_in),
        "never_even_provisioned_count": len(never_even_provisioned),
        "logged_in_emails": sorted(list(logged_in_active)),
        "never_logged_in_emails": sorted(list(never_logged_in))
    }
    with open("/tmp/sheet_lms_login_analysis.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2)
    print("Saved detailed report to /tmp/sheet_lms_login_analysis.json on EC2.")

    conn.close()

if __name__ == '__main__':
    run()
