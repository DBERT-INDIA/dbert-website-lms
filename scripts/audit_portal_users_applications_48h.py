import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor

# Connect to database
DB_URL = os.environ.get("DATABASE_URL", "postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
except Exception as e:
    print(f"Error connecting to database: {e}")
    sys.exit(1)

now = datetime.now()
time_48h_ago = now - timedelta(hours=48)
iso_48h_ago = time_48h_ago.strftime("%Y-%m-%d %H:%M:%S")

report = {
    "generated_at": now.strftime("%Y-%m-%d %H:%M:%S IST"),
    "window_48h_since": iso_48h_ago,
}

print("=" * 80)
print(f"DBERT PORTAL AUDIT: APPLICATIONS, SESSIONS (LAST 48H), AND STIPEND GATES")
print(f"Audit Run Time: {report['generated_at']}")
print(f"48-Hour Cutoff: {report['window_48h_since']}")
print("=" * 80)

# 1. APPLICATION STATUS BREAKDOWN
cur.execute("""
    SELECT status, COUNT(*) as count 
    FROM applications 
    GROUP BY status 
    ORDER BY count DESC
""")
app_statuses = cur.fetchall()
print("\n--- 1. OVERALL APPLICATION STATUS BREAKDOWN ---")
for r in app_statuses:
    print(f"  * {r['status'] or 'NULL / Unassigned'}: {r['count']}")

# 2. APPLICATIONS CREATED/UPDATED IN LAST 48 HOURS
cur.execute("""
    SELECT id, name, email, domain, status, created_at, updated_at
    FROM applications
    WHERE created_at >= %s OR updated_at >= %s
    ORDER BY updated_at DESC
""", (iso_48h_ago, iso_48h_ago))
recent_apps = cur.fetchall()
print(f"\n--- 2. APPLICATIONS IN LAST 48 HOURS ({len(recent_apps)} found) ---")
for r in recent_apps:
    print(f"  * ID {r['id']}: {r['name']} <{r['email']}> | Domain: {r['domain']} | Status: {r['status']} | Updated: {r['updated_at']}")

# 3. USER SESSIONS IN LAST 48 HOURS
cur.execute("""
    SELECT id, email, role, created_at, expires_at, next_url
    FROM user_sessions
    WHERE created_at >= %s
    ORDER BY created_at DESC
""", (iso_48h_ago,))
recent_sessions = cur.fetchall()
print(f"\n--- 3. USER SESSIONS CREATED IN LAST 48 HOURS ({len(recent_sessions)} total sessions) ---")

# Group by unique email and role
unique_users_48h = {}
for s in recent_sessions:
    em = s['email'].lower().strip()
    if em not in unique_users_48h:
        unique_users_48h[em] = {
            "email": em,
            "role": s['role'],
            "first_session_in_window": s['created_at'],
            "last_session_in_window": s['created_at'],
            "session_count": 0
        }
    unique_users_48h[em]["session_count"] += 1
    if s['created_at'] > unique_users_48h[em]["last_session_in_window"]:
        unique_users_48h[em]["last_session_in_window"] = s['created_at']
    if s['created_at'] < unique_users_48h[em]["first_session_in_window"]:
        unique_users_48h[em]["first_session_in_window"] = s['created_at']

print(f"Unique users logged in (last 48h): {len(unique_users_48h)}")
by_role = {}
for u in unique_users_48h.values():
    by_role[u['role']] = by_role.get(u['role'], 0) + 1
for role, cnt in by_role.items():
    print(f"  * Role '{role}': {cnt} unique users")

# 4. ENROLLMENT STATUS BREAKDOWN
cur.execute("""
    SELECT payment_status, COUNT(*) as count
    FROM enrollments
    GROUP BY payment_status
    ORDER BY count DESC
""")
enr_statuses = cur.fetchall()
print("\n--- 4. ENROLLMENTS PAYMENT STATUS BREAKDOWN ---")
for r in enr_statuses:
    print(f"  * {r['payment_status'] or 'NULL / Unassigned'}: {r['count']}")

# 5. DETAILED AUDIT FOR USERS LOGGED IN IN LAST 48 HOURS
print("\n--- 5. PROFILE & MILESTONE STAGE OF USERS ACTIVE IN LAST 48 HOURS ---")
users_detail = []
for em, uinfo in unique_users_48h.items():
    # Lookup intern_account
    cur.execute("""
        SELECT id, name, email, domain, linkedin_url, github_url, is_active, created_at, signup_stage
        FROM intern_accounts
        WHERE LOWER(email) = %s
    """, (em,))
    acct = cur.fetchone()
    
    # Lookup application
    cur.execute("""
        SELECT id, status, domain, created_at, updated_at
        FROM applications
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1
    """, (em,))
    app = cur.fetchone()

    # Lookup enrollment
    cur.execute("""
        SELECT id, payment_status, joining_date, batch_label, created_at
        FROM enrollments
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1
    """, (em,))
    enr = cur.fetchone()

    # Lookup certificate verification
    cur.execute("""
        SELECT id, cert_id, tier, course_title, issued_at
        FROM intern_certificates
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1
    """, (em,))
    cert = cur.fetchone()

    # Lookup articles
    art = None
    if acct:
        cur.execute("""
            SELECT id, title, status, created_at, updated_at
            FROM intern_articles
            WHERE intern_id = %s
            ORDER BY id DESC LIMIT 1
        """, (acct["id"],))
        art = cur.fetchone()

    # Determine gates
    g1_linkedin = bool(acct and acct.get('linkedin_url'))
    g2_article = bool(art and art.get('status') == 'published')
    g2_article_status = art.get('status') if art else 'No Article'
    g3_verified = bool(cert and cert.get('tier') in ('verified', 'dbert_verified'))
    g4_github = bool(acct and acct.get('github_url'))
    stipend_ready = g1_linkedin and g2_article and g3_verified and g4_github

    detail = {
        "email": em,
        "role": uinfo["role"],
        "sessions_48h": uinfo["session_count"],
        "last_login": uinfo["last_session_in_window"],
        "name": acct["name"] if acct else (app["name"] if app else "Unknown"),
        "has_account": bool(acct),
        "account_domain": acct.get("domain") if acct else None,
        "app_id": app.get("id") if app else None,
        "app_status": app.get("status") if app else "No Application",
        "enr_status": enr.get("payment_status") if enr else "No Enrollment",
        "g1_linkedin": g1_linkedin,
        "g2_article_status": g2_article_status,
        "g3_verified": g3_verified,
        "g4_github": g4_github,
        "stipend_ready": stipend_ready,
    }
    users_detail.append(detail)
    print(f"\nUser: {em} ({uinfo['role']}) | Last active: {uinfo['last_session_in_window']}")
    print(f"  Name: {detail['name']} | App Status: {detail['app_status']} | Enrollment: {detail['enr_status']}")
    print(f"  Gates -> G1(LinkedIn): {g1_linkedin} | G2(CaseStudy): {g2_article_status} | G3(Verified): {g3_verified} | G4(GitHub): {g4_github} | Stipend Ready: {stipend_ready}")

# 6. GLOBAL STIPEND FUNNEL & GATES AUDIT ACROSS ALL COHORT INTERNS
cur.execute("""
    SELECT 
        COUNT(*) as total_accounts,
        COUNT(CASE WHEN linkedin_url IS NOT NULL AND linkedin_url != '' THEN 1 END) as g1_linkedin_count,
        COUNT(CASE WHEN github_url IS NOT NULL AND github_url != '' THEN 1 END) as g4_github_count
    FROM intern_accounts
""")
gates_global = cur.fetchone()

cur.execute("""
    SELECT status, COUNT(*) as count
    FROM intern_articles
    GROUP BY status
""")
art_global = cur.fetchall()

cur.execute("""
    SELECT tier, COUNT(*) as count
    FROM intern_certificates
    GROUP BY tier
""")
cert_global = cur.fetchall()

print("\n--- 6. GLOBAL FUNNEL TOTALS (ALL INTERNS) ---")
print(f"  Total Intern Accounts: {gates_global['total_accounts']}")
print(f"  Gate 1 (LinkedIn Profile Connected): {gates_global['g1_linkedin_count']}")
print(f"  Gate 4 (GitHub URL Connected): {gates_global['g4_github_count']}")
print(f"  Gate 2 (Articles by Status): {[dict(r) for r in art_global]}")
print(f"  Gate 3 (Certificates by Tier): {[dict(r) for r in cert_global]}")

# 7. CANDIDATES WITH ALL 4 GATES UNLOCKED OR CLOSEST TO STIPEND RELEASE
cur.execute("""
    SELECT 
        ia.id, ia.name, ia.email, ia.domain, ia.linkedin_url, ia.github_url,
        ic.tier, ic.cert_id,
        art.status as article_status
    FROM intern_accounts ia
    LEFT JOIN intern_certificates ic ON (ia.id = ic.intern_id OR (ic.email IS NOT NULL AND LOWER(ia.email) = LOWER(ic.email)))
    LEFT JOIN intern_articles art ON ia.id = art.intern_id
    WHERE (ia.linkedin_url IS NOT NULL AND ia.linkedin_url != '')
       OR (ic.tier IN ('verified', 'dbert_verified'))
       OR (art.id IS NOT NULL)
       OR (ia.github_url IS NOT NULL AND ia.github_url != '')
""")
high_progression = cur.fetchall()
print(f"\n--- 7. CANDIDATES WITH MULTIPLE GATES UNLOCKED ({len(high_progression)} found) ---")
for r in high_progression:
    g1 = bool(r['linkedin_url'])
    g2 = r['article_status'] or 'None'
    g3 = bool(r['tier'] in ('verified', 'dbert_verified'))
    g4 = bool(r['github_url'])
    score = (1 if g1 else 0) + (1 if g2 == 'published' else (0.5 if g2 == 'in_review' else 0)) + (1 if g3 else 0) + (1 if g4 else 0)
    print(f"  * {r['name']} <{r['email']}> [{r['domain']}] -> G1:{g1}, G2:{g2}, G3:{g3}, G4:{g4} (Score: {score}/4)")

# Save JSON output for reporting
output_data = {
    "report_meta": report,
    "app_statuses": [dict(r) for r in app_statuses],
    "recent_apps_48h": [dict(r) for r in recent_apps],
    "unique_users_48h_count": len(unique_users_48h),
    "by_role_48h": by_role,
    "users_detail_48h": users_detail,
    "global_totals": {
        "intern_accounts": dict(gates_global),
        "articles": [dict(r) for r in art_global],
        "certificates": [dict(r) for r in cert_global]
    }
}
with open("data/audit_portal_48h.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, default=str)

print("\nAudit complete. Data saved to data/audit_portal_48h.json")
