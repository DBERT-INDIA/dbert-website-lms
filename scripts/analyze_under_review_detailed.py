import os
import sys
import psycopg2
from dotenv import load_dotenv

load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')
conn = psycopg2.connect(os.environ['DATABASE_URL'])
c = conn.cursor()

# 1. Total Under Review
c.execute("SELECT count(*) FROM applications WHERE status = 'Under Review';")
print(f"Total 'Under Review' Applications: {c.fetchone()[0]}")

# 2. Query all Under Review
c.execute("""
    SELECT id, name, email, phone, domain, college, city, why_join, status, created_at
    FROM applications 
    WHERE status = 'Under Review'
    ORDER BY id DESC;
""")
apps = c.fetchall()

results = []
for a in apps:
    app_id = a[0]
    name = a[1]
    email = (a[2] or '').strip().lower()
    phone = (a[3] or '').strip()
    domain = a[4]
    college = a[5]
    city = a[6]
    why_join = a[7]
    created_at = str(a[9])

    # Exclude test accounts
    if 'test' in email or 'example' in email or 'stage2_review' in email:
        continue

    # Check intern_accounts in dbert_internship or public
    intern_id = None
    signup_stage = None
    try:
        c.execute("SELECT id, signup_stage, account_status, is_active FROM intern_accounts WHERE LOWER(email) = %s;", (email,))
        row = c.fetchone()
        if row:
            intern_id, signup_stage = row[0], row[1]
    except Exception as e:
        conn.rollback()

    # Check user_sessions
    sess_count = 0
    if email:
        try:
            c.execute("SELECT count(*) FROM user_sessions WHERE LOWER(email) = %s;", (email,))
            row = c.fetchone()
            if row:
                sess_count = row[0]
        except Exception:
            conn.rollback()

    # Check 499 payment
    paid_499 = False
    try:
        c.execute("SELECT count(*) FROM course_enrollments_499 WHERE LOWER(email) = %s;", (email,))
        row = c.fetchone()
        if row and row[0] > 0:
            paid_499 = True
    except Exception:
        conn.rollback()

    try:
        c.execute("SELECT count(*) FROM payments WHERE LOWER(email) = %s AND status = 'captured';", (email,))
        row = c.fetchone()
        if row and row[0] > 0:
            paid_499 = True
    except Exception:
        conn.rollback()

    if signup_stage in ('paid', 'enrolled', 'active'):
        paid_499 = True

    is_complete = bool(name and email and phone and len(phone) >= 10 and domain)

    results.append({
        "id": app_id,
        "name": name,
        "email": email,
        "phone": phone,
        "domain": domain,
        "college": college,
        "city": city,
        "why_join": why_join,
        "has_account": bool(intern_id),
        "intern_id": intern_id,
        "sessions_count": sess_count,
        "multiple_logins": sess_count > 1,
        "paid_499": paid_499,
        "is_complete": is_complete,
        "created_at": created_at,
    })

print(f"\nTotal real candidates analyzed: {len(results)}")
complete_count = sum(1 for r in results if r["is_complete"])
print(f"Complete applications: {complete_count}")
multi_login_count = sum(1 for r in results if r["multiple_logins"])
print(f"Candidates with MULTIPLE logins (>1 session): {multi_login_count}")
unpaid_count = sum(1 for r in results if not r["paid_499"])
print(f"Candidates who have NOT completed 499 payment: {unpaid_count}")

# TARGET COHORT: Complete + Multiple Logins + Unpaid 499
target_cohort = [r for r in results if r["is_complete"] and r["multiple_logins"] and not r["paid_499"]]
print(f"\n=======================================================")
print(f"=== TARGET COHORT (Complete + Multi-Login + Unpaid 499) ===")
print(f"Total Matches: {len(target_cohort)}")
print(f"=======================================================")
for i, t in enumerate(target_cohort, 1):
    print(f"{i:>2}. App ID {t['id']}: {t['name']} | {t['email']} | {t['phone']} | {t['domain']} | Logins: {t['sessions_count']} | Created: {t['created_at']}")

# Single login cohort
single_login_cohort = [r for r in results if r["is_complete"] and r["sessions_count"] == 1 and not r["paid_499"]]
print(f"\n=== Single Login Cohort (Complete + Sessions = 1 + Unpaid 499): {len(single_login_cohort)} candidates ===")
for i, t in enumerate(single_login_cohort, 1):
    print(f"{i:>2}. App ID {t['id']}: {t['name']} | {t['email']} | {t['phone']} | {t['domain']} | Logins: {t['sessions_count']} | Created: {t['created_at']}")

# Zero login cohort
zero_login_cohort = [r for r in results if r["is_complete"] and r["sessions_count"] == 0 and not r["paid_499"]]
print(f"\n=== Zero Login Cohort (Complete + Sessions = 0 + Unpaid 499): {len(zero_login_cohort)} candidates ===")
