import subprocess
import json

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_code = """
import psycopg2
import json
from collections import Counter
from datetime import datetime

conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
c = conn.cursor()

# Query sessions created in last 7 days (>= '2026-11-11 00:00:00')
c.execute(\"\"\"
    SELECT LOWER(email), role, count(*) as login_count, max(created_at) as last_login
    FROM dbert_internship.user_sessions
    WHERE created_at >= '2026-11-11 00:00:00'
      AND LOWER(email) NOT LIKE '%admin%'
      AND LOWER(email) NOT LIKE '%dbert.in%'
    GROUP BY LOWER(email), role
    ORDER BY login_count DESC, last_login DESC;
\"\"\")
recent_users = c.fetchall()

print(f"Total unique candidates with sessions in last 7 days: {len(recent_users)}")

# Also let's check total lifetime sessions for these candidates
user_details = []

for email, role, l_count_7d, last_log in recent_users:
    # Lifetime logins
    c.execute(\"\"\"
        SELECT count(*) FROM dbert_internship.user_sessions 
        WHERE LOWER(email) = %s;
    \"\"\", (email,))
    lifetime_logins = c.fetchone()[0]

    # Application details
    c.execute(\"\"\"
        SELECT id, name, phone, domain, college, status, created_at, reviewed_at
        FROM dbert_internship.applications 
        WHERE LOWER(email) = %s 
        ORDER BY id DESC LIMIT 1;
    \"\"\", (email,))
    app = c.fetchone()

    # Intern account details
    c.execute(\"\"\"
        SELECT id, name, phone, domain, college, account_status, is_active, created_at, signup_stage
        FROM dbert_internship.intern_accounts
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1;
    \"\"\", (email,))
    acc = c.fetchone()
    intern_id = acc[0] if acc else None

    # Offer letter details
    c.execute(\"\"\"
        SELECT offer_letter_id, caution_deposit_status, caution_deposit_amount, pdf_unlocked, accepted_at
        FROM dbert_internship.intern_offer_letters
        WHERE LOWER(email) = %s
        ORDER BY id DESC LIMIT 1;
    \"\"\", (email,))
    offer = c.fetchone()

    # Security deposit / 499 payment
    has_security_deposit = False
    sec_dep_status = None
    if intern_id:
        c.execute(\"\"\"
            SELECT status, amount FROM dbert_internship.security_deposits 
            WHERE intern_id = %s ORDER BY id DESC LIMIT 1;
        \"\"\", (intern_id,))
        dep = c.fetchone()
        if dep:
            has_security_deposit = True
            sec_dep_status = dep[0]

    # Certificate details
    c.execute(\"\"\"
        SELECT cert_id, tier FROM dbert_internship.intern_certificates 
        WHERE LOWER(email) = %s OR (intern_id IS NOT NULL AND intern_id = %s)
        ORDER BY id DESC LIMIT 1;
    \"\"\", (email, intern_id or -1))
    cert = c.fetchone()

    name = (app[1] if app and app[1] else (acc[1] if acc and acc[1] else "Candidate"))
    phone = (app[2] if app and app[2] else (acc[2] if acc and acc[2] else ""))
    domain = (app[3] if app and app[3] else (acc[3] if acc and acc[3] else "General"))
    college = (app[4] if app and app[4] else (acc[4] if acc and acc[4] else ""))
    app_status = app[5] if app else ("Account Only" if acc else "No Application")

    user_details.append({
        "email": email,
        "role": role,
        "name": name,
        "phone": phone,
        "domain": domain,
        "college": college,
        "app_status": app_status,
        "logins_7d": l_count_7d,
        "lifetime_logins": lifetime_logins,
        "last_login": str(last_log),
        "has_intern_account": bool(acc),
        "has_offer_letter": bool(offer),
        "offer_letter_id": offer[0] if offer else None,
        "caution_deposit_status": offer[1] if offer else None,
        "caution_deposit_amount": offer[2] if offer else None,
        "pdf_unlocked": offer[3] if offer else None,
        "has_security_deposit": has_security_deposit,
        "security_deposit_status": sec_dep_status,
        "has_certificate": bool(cert),
        "cert_id": cert[0] if cert else None,
        "cert_tier": cert[1] if cert else None,
    })

# Save JSON output
with open("/tmp/active_logins_7d.json", "w", encoding="utf-8") as f:
    json.dump(user_details, f, indent=2)

print(f"Successfully exported {len(user_details)} records to /tmp/active_logins_7d.json")

# Print summary
multi_users = [u for u in user_details if u["logins_7d"] > 1]
single_users = [u for u in user_details if u["logins_7d"] == 1]

print(f"\\n--- ENGAGEMENT METRICS (LAST 7 DAYS) ---")
print(f"Total Unique Candidates: {len(user_details)}")
print(f"Multi-Login Candidates (>= 2): {len(multi_users)} ({len(multi_users)/len(user_details)*100:.1f}%)")
print(f"Single-Login Candidates (== 1): {len(single_users)} ({len(single_users)/len(user_details)*100:.1f}%)")

print(f"\\n--- APPLICATION STATUS (ALL 501 CANDIDATES) ---")
for st, cnt in Counter(u["app_status"] for u in user_details).most_common():
    print(f"  {st}: {cnt}")

print(f"\\n--- APPLICATION STATUS (172 MULTI-LOGIN CANDIDATES) ---")
for st, cnt in Counter(u["app_status"] for u in multi_users).most_common():
    print(f"  {st}: {cnt}")

print(f"\\n--- DOMAIN BREAKDOWN (172 MULTI-LOGIN CANDIDATES) ---")
for dom, cnt in Counter(u["domain"] for u in multi_users).most_common(10):
    print(f"  {dom}: {cnt}")

print(f"\\n--- OFFER LETTER & DEPOSIT STATUS ---")
print(f"Candidates with Offer Letter generated: {sum(1 for u in user_details if u['has_offer_letter'])}")
print(f"Candidates with Caution Deposit Paid: {sum(1 for u in user_details if u['has_security_deposit'] or u['caution_deposit_status'] == 'paid')}")
print(f"Candidates with Verified Certificate: {sum(1 for u in user_details if u['has_certificate'])}")

conn.close()
"""

with open("scripts/remote_logins_query.py", "w", encoding="utf-8") as f:
    f.write(remote_code)

scp_cmd = f'scp -i "{PEM_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes scripts/remote_logins_query.py {REMOTE_HOST}:/tmp/remote_logins_query.py'
subprocess.run(scp_cmd, shell=True, check=True)

venv_py = "/var/www/dbert-website-lms/apps/portal/.venv/bin/python"
run_cmd = f'ssh -i "{PEM_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {REMOTE_HOST} "{venv_py} /tmp/remote_logins_query.py && rm -f /tmp/remote_logins_query.py"'
res = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)

fetch_cmd = f'scp -i "{PEM_KEY}" -o StrictHostKeyChecking=no -o BatchMode=yes {REMOTE_HOST}:/tmp/active_logins_7d.json data/active_logins_7d.json'
subprocess.run(fetch_cmd, shell=True, check=True)
print("Fetched data/active_logins_7d.json locally.")
