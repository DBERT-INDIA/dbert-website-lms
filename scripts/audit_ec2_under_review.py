#!/usr/bin/env python3
import psycopg2
import json
import os
from collections import Counter
from dotenv import load_dotenv

# Try multiple .env locations
for p in [
    "/var/www/dbert-website-lms/apps/portal/.env",
    os.path.join(os.path.dirname(__file__), "..", "apps", "portal", ".env"),
    ".env"
]:
    if os.path.exists(p):
        load_dotenv(p)
        break

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("DATABASE_URL not found!")
    exit(1)

conn = psycopg2.connect(db_url)
c = conn.cursor()

# 1. Total applications by status
c.execute("SELECT status, count(*) FROM dbert_internship.applications GROUP BY status ORDER BY count(*) DESC;")
all_statuses = c.fetchall()

# 2. Total Under Review
c.execute("SELECT count(*) FROM dbert_internship.applications WHERE status = 'Under Review';")
total_under_review = c.fetchone()[0]

# 3. Fetch all Under Review applications with full join to user_sessions, device_profiles, intern_accounts
query = """
SELECT 
    a.id,
    a.name,
    a.email,
    a.phone,
    a.domain,
    a.college,
    a.city,
    a.why_join,
    a.created_at,
    COALESCE(s.session_count, 0) as session_count,
    COALESCE(s.first_login, '') as first_login,
    COALESCE(s.last_login, '') as last_login,
    COALESCE(d.total_visits, 0) as device_visits,
    COALESCE(d.device_type, '') as device_type,
    ia.id as intern_id,
    ia.signup_stage,
    ia.account_status,
    ia.terms_accepted_at,
    ia.interview_attempts
FROM dbert_internship.applications a
LEFT JOIN (
    SELECT 
        LOWER(TRIM(email)) as email,
        COUNT(*) as session_count,
        MIN(created_at) as first_login,
        MAX(created_at) as last_login
    FROM dbert_internship.user_sessions
    GROUP BY LOWER(TRIM(email))
) s ON LOWER(TRIM(a.email)) = s.email
LEFT JOIN (
    SELECT 
        LOWER(TRIM(email)) as email,
        SUM(COALESCE(visit_count, 1)) as total_visits,
        MAX(device_type) as device_type
    FROM dbert_internship.device_profiles
    GROUP BY LOWER(TRIM(email))
) d ON LOWER(TRIM(a.email)) = d.email
LEFT JOIN dbert_internship.intern_accounts ia 
    ON LOWER(TRIM(a.email)) = LOWER(TRIM(ia.email))
WHERE a.status = 'Under Review'
ORDER BY session_count DESC, device_visits DESC, a.id DESC;
"""

c.execute(query)
rows = c.fetchall()

fields = [
    "id", "name", "email", "phone", "domain", "college", "city", "why_join",
    "created_at", "session_count", "first_login", "last_login",
    "device_visits", "device_type", "intern_id", "signup_stage",
    "account_status", "terms_accepted_at", "interview_attempts"
]

results = [dict(zip(fields, r)) for r in rows]

# Summaries
session_buckets = Counter()
for r in results:
    cnt = r["session_count"]
    if cnt == 0:
        bucket = "0 Logins (Never Logged In)"
    elif cnt == 1:
        bucket = "1 Login (Single Initial Session)"
    elif cnt == 2:
        bucket = "2 Logins (Multiple)"
    elif 3 <= cnt <= 5:
        bucket = "3-5 Logins (High Repeat)"
    else:
        bucket = "6+ Logins (Power User)"
    session_buckets[bucket] += 1

domain_breakdown = Counter(r["domain"] for r in results)
multi_login_users = [r for r in results if r["session_count"] > 1]
single_login_users = [r for r in results if r["session_count"] == 1]
zero_login_users = [r for r in results if r["session_count"] == 0]

# Output structured JSON
report = {
    "summary": {
        "total_under_review": total_under_review,
        "multiple_logins_count": len(multi_login_users),
        "multiple_logins_pct": round(100.0 * len(multi_login_users) / total_under_review, 2) if total_under_review else 0,
        "single_login_count": len(single_login_users),
        "single_login_pct": round(100.0 * len(single_login_users) / total_under_review, 2) if total_under_review else 0,
        "zero_login_count": len(zero_login_users),
        "zero_login_pct": round(100.0 * len(zero_login_users) / total_under_review, 2) if total_under_review else 0,
    },
    "session_buckets": dict(session_buckets),
    "domain_breakdown": dict(domain_breakdown),
    "multi_login_candidates": multi_login_users,
    "all_statuses_overview": dict(all_statuses),
    "all_candidates": results
}

print(f"=== UNDER REVIEW APPLICATIONS SUMMARY ===")
print(f"Total Under Review Applications: {total_under_review}")
print(f"Multiple Logins (>1): {len(multi_login_users)} ({report['summary']['multiple_logins_pct']}%)")
print(f"Single Login (=1): {len(single_login_users)} ({report['summary']['single_login_pct']}%)")
print(f"Zero Logins (=0): {len(zero_login_users)} ({report['summary']['zero_login_pct']}%)")
print("\nSession Buckets:")
for k, v in session_buckets.items():
    print(f"  {k}: {v}")

print(f"\n=== CANDIDATES WITH MULTIPLE LOGINS ({len(multi_login_users)}) ===")
for idx, c in enumerate(multi_login_users, 1):
    print(f"#{idx:02d} | App ID: {c['id']} | {c['name']:<24} | {c['email']:<30} | Phone: {c['phone']} | Logins: {c['session_count']} | Visits: {c['device_visits']} | Domain: {c['domain']} | Created: {c['created_at']}")

# Save report locally
with open("/tmp/under_review_audit_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, default=str)
print("\nReport saved to /tmp/under_review_audit_report.json")
