#!/usr/bin/env python3
"""
================================================================================
DBERT — Promote 10 Multi-Login Under Review Candidates to 'Selected'
================================================================================
- Targets: 10 verified candidates with sessions_count > 1 and unpaid 499
- Updates:
    1. applications.status = 'Selected', reviewed_at = NOW()
    2. intern_accounts.signup_stage = 3, account_status = 'Selected'
    3. intern_offer_letters deterministic record creation
- Output: data/selected_multi_login_cohort.json
================================================================================
"""

import os
import sys
import json
from datetime import datetime, timedelta
import psycopg2
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load environment
for env_path in [
    '/var/www/dbert-website-lms/apps/portal/.env',
    os.path.join(os.path.dirname(__file__), '..', 'apps', 'portal', '.env')
]:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("ERROR: DATABASE_URL not found.")
    sys.exit(1)

conn = psycopg2.connect(db_url)
c = conn.cursor()

TARGET_APP_IDS = [5278, 5252, 5241, 5233, 5224, 5217, 5148, 5144, 4874, 4816]

DOMAIN_CODE_MAP = {
    "ai & machine learning": "AI",
    "ai agent development": "AI",
    "artificial intelligence": "AI",
    "data analyst": "DA",
    "data analytics": "DA",
    "data science": "DS",
    "full stack web development": "FS",
    "full stack development": "FS",
    "python automation": "PY",
    "cybersecurity": "CS",
    "cyber security": "CS",
    "digital marketing": "DM",
    "cloud computing": "CC",
}

def get_code(domain_str):
    if not domain_str:
        return "GEN"
    norm = domain_str.strip().lower()
    return DOMAIN_CODE_MAP.get(norm, "GEN")

print(f"Fetching {len(TARGET_APP_IDS)} target candidates...")

c.execute("""
    SELECT id, name, email, phone, domain, college, city, why_join, status, created_at
    FROM applications
    WHERE id = ANY(%s)
    ORDER BY id DESC;
""", (TARGET_APP_IDS,))
apps = c.fetchall()

if len(apps) != len(TARGET_APP_IDS):
    print(f"Warning: Found {len(apps)} matching applications out of {len(TARGET_APP_IDS)} requested.")

promoted_records = []
now_iso = datetime.now().isoformat()

for app in apps:
    app_id = app[0]
    name = app[1]
    email = (app[2] or '').strip().lower()
    phone = (app[3] or '').strip()
    domain = app[4] or "Engineering"
    college = app[5] or ""
    current_status = app[8]

    print(f"\nProcessing App ID {app_id} | {name} | {email} | Current: {current_status}")

    # 1. Update applications table
    c.execute("""
        UPDATE applications
        SET status = 'Selected',
            reviewed_at = NOW(),
            updated_at = NOW()
        WHERE id = %s;
    """, (app_id,))

    # 2. Update intern_accounts
    c.execute("""
        UPDATE intern_accounts
        SET signup_stage = 3,
            account_status = 'Selected',
            updated_at = NOW()
        WHERE LOWER(email) = %s
        RETURNING id;
    """, (email,))
    ia_res = c.fetchone()
    intern_id = ia_res[0] if ia_res else None

    # 3. Create or update intern_offer_letters
    c.execute("SELECT id, offer_letter_id FROM intern_offer_letters WHERE LOWER(email) = %s;", (email,))
    offer_row = c.fetchone()

    offer_id_str = None
    if offer_row:
        offer_id_str = offer_row[1]
        print(f"  Existing offer letter found: {offer_id_str}")
    else:
        domain_code = get_code(domain)
        offer_id_str = f"DBERT-OFR-2026-{domain_code}-{app_id:04d}"
        batch_start_date = "2026-11-23"
        batch_end_date = "2027-01-22"

        c.execute("""
            INSERT INTO intern_offer_letters (
                offer_letter_id, intern_id, enrollment_id, email, name, domain, college,
                batch_start_date, batch_end_date, tenure_months, stipend_amount,
                login_hours_per_week, required_certifications, required_bounty_tasks,
                caution_deposit_amount, caution_deposit_status, signature_name,
                accepted_at, pdf_unlocked, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, 2, 5000,
                10, 2, 75,
                499, 'PENDING', NULL,
                NULL, 0, NOW(), NOW()
            );
        """, (
            offer_id_str, intern_id, app_id, email, name, domain, college,
            batch_start_date, batch_end_date
        ))
        print(f"  Created new offer letter: {offer_id_str}")

    promoted_records.append({
        "app_id": app_id,
        "name": name,
        "email": email,
        "phone": phone,
        "domain": domain,
        "college": college,
        "intern_id": intern_id,
        "offer_letter_id": offer_id_str,
        "status": "Selected",
        "promoted_at": now_iso
    })

conn.commit()
print(f"\nSuccessfully committed promotion of {len(promoted_records)} candidates in PostgreSQL.")

# Save output JSON
out_path = '/var/www/dbert-website-lms/data/selected_multi_login_cohort.json'
try:
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(promoted_records, f, indent=2)
    print(f"Saved cohort details to {out_path}")
except Exception as e:
    print(f"Note: local file save: {e}")

c.close()
conn.close()
