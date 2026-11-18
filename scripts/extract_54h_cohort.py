import os
import sys
import json
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.environ.get("DATABASE_URL", "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")

now = datetime.now()
time_54h_ago = now - timedelta(hours=54)
iso_54h_ago = time_54h_ago.strftime("%Y-%m-%d %H:%M:%S")

print(f"Connecting to DB. 54-Hour Cutoff: {iso_54h_ago}")
conn = psycopg2.connect(DB_URL)
cur = conn.cursor(cursor_factory=RealDictCursor)

# 1. Fetch all distinct sessions in last 54h
cur.execute("""
    SELECT email, role, MAX(created_at) as last_login, COUNT(id) as session_count
    FROM user_sessions
    WHERE created_at >= %s
    GROUP BY email, role
    ORDER BY last_login DESC
""", (iso_54h_ago,))
sessions = cur.fetchall()

print(f"Total distinct users in last 54h: {len(sessions)}")

cohort = []
for s in sessions:
    email = (s["email"] or "").strip().lower()
    role = s["role"] or "intern"
    if not email:
        continue

    # Exclude purely administrative accounts from candidate dispatch
    if email in ("admin@dbert.in", "abhinav.sharma@dbert.in", "manoj.kumar@dbert.in", "sandeep.bannu@dbert.in", "pulkit.kunar@dbert.in", "contactus@dbert.in") and role == "admin":
        print(f"Skipping admin: {email}")
        continue

    # Lookup intern_account
    cur.execute("""
        SELECT id, name, email, phone, city, college, course, semester, year_of_passing,
               domain, linkedin_url, github_url, created_at, signup_stage
        FROM intern_accounts
        WHERE LOWER(email) = %s
        LIMIT 1
    """, (email,))
    acct = cur.fetchone()

    # Lookup latest application
    cur.execute("""
        SELECT id, name, email, phone, city, college, course, semester, year_of_passing,
               domain, status, why_join, created_at, updated_at
        FROM applications
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1
    """, (email,))
    app = cur.fetchone()

    # Lookup latest enrollment
    cur.execute("""
        SELECT id, payment_status, product, amount, joining_date, batch_label, utr, created_at
        FROM enrollments
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1
    """, (email,))
    enr = cur.fetchone()

    # Lookup certificates
    cur.execute("""
        SELECT id, cert_id, tier, course_title, issued_at, url
        FROM intern_certificates
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1
    """, (email,))
    cert = cur.fetchone()

    # Lookup articles
    art = None
    if acct:
        cur.execute("""
            SELECT id, title, status, published_url, created_at, updated_at
            FROM intern_articles
            WHERE intern_id = %s
            ORDER BY id DESC LIMIT 1
        """, (acct["id"],))
        art = cur.fetchone()

    name = (acct.get("name") if acct else None) or (app.get("name") if app else None) or "Candidate"
    domain = (acct.get("domain") if acct and acct.get("domain") != "Undeclared" else None) or \
             (app.get("domain") if app and app.get("domain") != "Undeclared" else None) or \
             "Full Stack Development"
    phone = (acct.get("phone") if acct else None) or (app.get("phone") if app else None) or ""
    college = (acct.get("college") if acct else None) or (app.get("college") if app else None) or ""

    app_status = (app.get("status") if app else "No Application")
    enr_status = (enr.get("payment_status") if enr else "No Enrollment")

    # Evaluate Gates
    g1_linkedin = bool(acct and acct.get("linkedin_url"))
    g2_article = bool(art and (art.get("status") or "").upper() == "PUBLISHED")
    g2_status = (art.get("status") or "NOT_SUBMITTED").upper() if art else "NOT_SUBMITTED"
    g3_verified = bool(cert and cert.get("tier") in ("verified", "dbert_verified"))
    g4_github = bool(acct and acct.get("github_url"))

    # Segment Assignment
    # 1. Verified Alumni
    if app_status == "Verified" or g3_verified:
        segment = "VERIFIED_ALUMNI"
    # 2. Accepted / Enrolled Fellows in Active Sprint
    elif app_status == "Accepted" or enr_status == "Accepted":
        segment = "ENROLLED_FELLOW"
    # 3. Enrollment Pending / Flagged Deposit
    elif app_status == "Enrollment Pending" or enr_status in ("Pending Verification", "Rejected"):
        segment = "ENROLLMENT_PENDING"
    # 4. Under Review
    elif app_status in ("Under Review", "Apply Pending", "On Hold"):
        segment = "UNDER_REVIEW"
    # 5. Selected
    elif app_status == "Selected":
        segment = "SELECTED"
    else:
        # Default fallback based on enrollment or review
        segment = "UNDER_REVIEW" if not enr else "ENROLLMENT_PENDING"

    cohort.append({
        "email": email,
        "name": name,
        "phone": phone,
        "college": college,
        "domain": domain,
        "segment": segment,
        "app_status": app_status,
        "enr_status": enr_status,
        "last_login": str(s["last_login"]),
        "session_count": s["session_count"],
        "batch_label": enr.get("batch_label") if enr else "Upcoming Cohort",
        "joining_date": enr.get("joining_date") if enr else "",
        "utr": enr.get("utr") if enr else "",
        "cert_id": cert.get("cert_id") if cert else "",
        "g1_linkedin": g1_linkedin,
        "linkedin_url": acct.get("linkedin_url") if acct else "",
        "g2_article": g2_article,
        "g2_status": g2_status,
        "g3_verified": g3_verified,
        "g4_github": g4_github,
        "github_url": acct.get("github_url") if acct else "",
    })

print(f"\nCohort Processing Complete: {len(cohort)} candidates categorized.")
segment_counts = {}
for c in cohort:
    segment_counts[c["segment"]] = segment_counts.get(c["segment"], 0) + 1

for seg, cnt in segment_counts.items():
    print(f"  * {seg}: {cnt}")

out_path = "data/active_54h_cohort.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(cohort, f, indent=2, ensure_ascii=False)

print(f"\nCohort saved to {out_path}")
