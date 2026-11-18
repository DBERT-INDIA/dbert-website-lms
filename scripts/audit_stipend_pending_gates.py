import sys
import json
from pathlib import Path

if Path("/var/www/dbert-website-lms").exists():
    sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "portal"))

from app import get_db

conn = get_db()
cur = conn.cursor()

# Let's inspect the intern_accounts and their status across gates:
# 1. Certificate verification: intern_certificates (tier IN ('verified', 'dbert_verified'))
# 2. Completion date: enrollments (joining_date + 60 days <= NOW)
# 3. UPI linked: upi_id_encrypted IS NOT NULL AND upi_id_encrypted != ''
# 4. LinkedIn linked: linkedin_url IS NOT NULL AND linkedin_url != ''
# Also check article status: intern_articles (status = 'PUBLISHED')

print("=" * 80)
print("COMPREHENSIVE STIPEND GATE ELIGIBILITY AUDIT")
print("=" * 80)

# Query all intern_accounts
cur.execute("""
    SELECT 
        ia.id as intern_id,
        ia.name,
        ia.email,
        ia.domain,
        ia.upi_id_encrypted,
        ia.linkedin_url,
        ia.github_url,
        ia.stipend_verified,
        ic.tier as cert_tier,
        ic.cert_id,
        enr.joining_date,
        art.status as article_status,
        ts.status as submission_status
    FROM intern_accounts ia
    LEFT JOIN intern_certificates ic ON LOWER(ia.email) = LOWER(ic.email)
    LEFT JOIN enrollments enr ON LOWER(ia.email) = LOWER(enr.email)
    LEFT JOIN (
        SELECT intern_id, status, 
               ROW_NUMBER() OVER (PARTITION BY intern_id ORDER BY id DESC) as rn
        FROM intern_articles
    ) art ON ia.id = art.intern_id AND art.rn = 1
    LEFT JOIN (
        SELECT intern_id, status,
               ROW_NUMBER() OVER (PARTITION BY intern_id ORDER BY id DESC) as rn
        FROM task_submissions
        WHERE task_category = 'stipend_milestone'
    ) ts ON ia.id = ts.intern_id AND ts.rn = 1
""")
rows = cur.fetchall()
print(f"Total intern_accounts records: {len(rows)}")

# Let's evaluate gate definition standard:
# Standard A (Portal UI 4 Gates):
# Gate 1: Certificate Verified (ic.tier IN ('verified', 'dbert_verified'))
# Gate 2: Duration Met (joining_date + 60 days <= 2026-11-17 or certificate issued)
# Gate 3: UPI Linked (upi_id_encrypted)
# Gate 4: LinkedIn Linked (linkedin_url)

# Standard B (Deliverables-based 4 Gates):
# Gate 1: Certificate Verified
# Gate 2: Capstone Article / Deliverable Published (art.status == 'PUBLISHED')
# Gate 3: UPI Linked
# Gate 4: LinkedIn Linked

from datetime import datetime, date, timedelta

today = date(2026, 11, 17)

breakdown_a = {0: [], 1: [], 2: [], 3: [], 4: []} # by completed gates (0 to 4)
breakdown_b = {0: [], 1: [], 2: [], 3: [], 4: []}

# Also filter to interns who have at least started (e.g. have certificate OR enrollment OR submission OR upi/linkedin)
active_pool = []

for r in rows:
    iid, name, email, domain, upi, linkedin, github, stipend_ver, cert_tier, cert_id, jd_raw, art_status, sub_status = r
    
    has_cert = bool(cert_tier and cert_tier in ('verified', 'dbert_verified'))
    has_any_cert = bool(cert_id)
    has_upi = bool(upi and str(upi).strip())
    has_linkedin = bool(linkedin and str(linkedin).strip())
    has_github = bool(github and str(github).strip())
    has_article = bool(art_status and art_status.upper() == 'PUBLISHED')
    
    duration_met = False
    if has_any_cert:
        duration_met = True
    elif jd_raw:
        try:
            # parse date
            jd_str = str(jd_raw)[:10]
            jd = datetime.strptime(jd_str, "%Y-%m-%d").date()
            if today >= jd + timedelta(days=60):
                duration_met = True
        except Exception:
            pass

    # Standard A Gates:
    gA_1 = has_cert
    gA_2 = duration_met
    gA_3 = has_upi
    gA_4 = has_linkedin
    gates_a_passed = sum([gA_1, gA_2, gA_3, gA_4])
    breakdown_a[gates_a_passed].append({
        "intern_id": iid, "name": name, "email": email, "domain": domain,
        "gates": [gA_1, gA_2, gA_3, gA_4], "stipend_verified": stipend_ver
    })

    # Standard B Gates:
    gB_1 = has_cert
    gB_2 = has_article
    gB_3 = has_upi
    gB_4 = has_linkedin
    gates_b_passed = sum([gB_1, gB_2, gB_3, gB_4])
    breakdown_b[gates_b_passed].append({
        "intern_id": iid, "name": name, "email": email, "domain": domain,
        "gates": [gB_1, gB_2, gB_3, gB_4], "stipend_verified": stipend_ver
    })

print("\n--- STANDARD A (Gate 1: Cert Verified, Gate 2: Duration, Gate 3: UPI, Gate 4: LinkedIn) ---")
for k in range(5):
    pending = 4 - k
    print(f"Gates completed: {k}/4 (Pending: {pending}/4) -> {len(breakdown_a[k])} interns")

print("\n--- STANDARD B (Gate 1: Cert Verified, Gate 2: Article Published, Gate 3: UPI, Gate 4: LinkedIn) ---")
for k in range(5):
    pending = 4 - k
    print(f"Gates completed: {k}/4 (Pending: {pending}/4) -> {len(breakdown_b[k])} interns")

# Now let's check ONLY interns who have an enrolled course or certificate or application selected (i.e. legitimate candidates in pipeline)
cur.execute("""
    SELECT count(DISTINCT LOWER(email)) FROM intern_accounts
    WHERE (upi_id_encrypted IS NOT NULL AND upi_id_encrypted != '')
       OR (linkedin_url IS NOT NULL AND linkedin_url != '')
       OR (github_url IS NOT NULL AND github_url != '')
""")
engaged_count = cur.fetchone()[0]
print(f"\nInterns who have engaged with profile setup (UPI or LinkedIn or GitHub): {engaged_count}")

# Check active in last 48 hours:
t48 = (datetime.now() - timedelta(hours=48)).strftime('%Y-%m-%d %H:%M:%S')
cur.execute("""
    SELECT DISTINCT LOWER(s.email)
    FROM user_sessions s
    JOIN intern_accounts ia ON LOWER(s.email) = LOWER(ia.email)
    WHERE s.created_at >= %s
""", (t48,))
active_48h_emails = set(r[0] for r in cur.fetchall())
print(f"Interns active in last 48 hours: {len(active_48h_emails)}")

active_48h_pending_a = [x for k in [1, 2, 3] for x in breakdown_a[k] if x["email"].lower() in active_48h_emails]
active_48h_pending_b = [x for k in [1, 2, 3] for x in breakdown_b[k] if x["email"].lower() in active_48h_emails]

print(f"Active in last 48h with 1, 2, or 3 gates pending (Standard A): {len(active_48h_pending_a)}")
print(f"Active in last 48h with 1, 2, or 3 gates pending (Standard B): {len(active_48h_pending_b)}")

# Let's inspect certificate holders specifically:
cur.execute("""
    SELECT DISTINCT LOWER(email) FROM intern_certificates
""")
all_cert_emails = set(r[0] for r in cur.fetchall())
cert_pending_a = [x for k in [1, 2, 3] for x in breakdown_a[k] if x["email"].lower() in all_cert_emails]
cert_pending_b = [x for k in [1, 2, 3] for x in breakdown_b[k] if x["email"].lower() in all_cert_emails]

print(f"\nCertificate holders with 1, 2, or 3 gates pending (Standard A): {len(cert_pending_a)}")
print(f"Certificate holders with 1, 2, or 3 gates pending (Standard B): {len(cert_pending_b)}")
