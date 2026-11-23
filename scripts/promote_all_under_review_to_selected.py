#!/usr/bin/env python3
"""
================================================================================
DBERT — Promote All Under Review Applications to 'Selected' on EC2
================================================================================
Updates:
  1. applications.status = 'Selected', reviewed_at = NOW(), updated_at = NOW()
     WHERE status = 'Under Review'
  2. intern_accounts.signup_stage = 3, account_status = 'Selected', updated_at = NOW()
     WHERE LOWER(email) in (promoted emails)
  3. intern_offer_letters deterministic record creation:
     offer_letter_id = 'DBERT-OFR-2026-{DOMAIN}-{APP_ID:04d}'
     batch_start_date = '2026-11-23', batch_end_date = '2027-01-22'
     caution_deposit_amount = 499, stipend_amount = 5000
================================================================================
"""

import os
import sys
import json
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

for env_path in [
    "/var/www/dbert-website-lms/apps/portal/.env",
    os.path.join(os.path.dirname(__file__), "..", "apps", "portal", ".env"),
    ".env"
]:
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break

db_url = os.environ.get("DATABASE_URL")
if not db_url:
    print("ERROR: DATABASE_URL not found.")
    sys.exit(1)

conn = psycopg2.connect(db_url)
c = conn.cursor()

DOMAIN_CODE_MAP = {
    "ai & machine learning": "AIML",
    "ai agent development": "AI",
    "artificial intelligence": "AI",
    "data analyst": "DA",
    "data analytics": "DA",
    "data science": "DS",
    "full stack web development": "FSD",
    "full stack development": "FSD",
    "python automation": "PA",
    "cybersecurity": "CS",
    "cyber security": "CS",
    "digital marketing": "DM",
    "cloud computing": "CC",
    "devops & cloud": "DOC",
    "ui/ux design": "UIUX",
    "mobile app development": "MAD"
}

def get_code(domain_str):
    if not domain_str:
        return "GEN"
    norm = domain_str.strip().lower()
    return DOMAIN_CODE_MAP.get(norm, "GEN")

print("Fetching all applications with status = 'Under Review'...")
c.execute("""
    SELECT id, name, email, phone, domain, college, city, why_join, status, created_at
    FROM dbert_internship.applications
    WHERE status = 'Under Review'
    ORDER BY id ASC;
""")
apps = c.fetchall()
total_apps = len(apps)
print(f"Found {total_apps} applications to promote to 'Selected'.")

if total_apps == 0:
    print("No 'Under Review' applications found! Exiting.")
    sys.exit(0)

promoted_records = []
now_iso = datetime.now().isoformat()
batch_start_date = "2026-11-23"
batch_end_date = "2027-01-22"

for idx, app in enumerate(apps, 1):
    app_id = app[0]
    name = (app[1] or "Fellow").strip()
    email = (app[2] or "").strip().lower()
    phone = (app[3] or "").strip()
    domain = (app[4] or "Engineering").strip()
    college = (app[5] or "").strip()

    # 1. Update applications table
    c.execute("""
        UPDATE dbert_internship.applications
        SET status = 'Selected',
            reviewed_at = NOW(),
            updated_at = NOW()
        WHERE id = %s;
    """, (app_id,))

    # 2. Update intern_accounts
    c.execute("""
        UPDATE dbert_internship.intern_accounts
        SET signup_stage = 3,
            account_status = 'Selected',
            updated_at = NOW()
        WHERE LOWER(TRIM(email)) = %s
        RETURNING id;
    """, (email,))
    ia_res = c.fetchone()
    intern_id = ia_res[0] if ia_res else None

    # 3. Create or update intern_offer_letters (collision-safe)
    c.execute("""
        SELECT id, offer_letter_id 
        FROM dbert_internship.intern_offer_letters 
        WHERE LOWER(TRIM(email)) = %s OR enrollment_id = %s;
    """, (email, app_id))
    offer_row = c.fetchone()

    offer_id_str = None
    if offer_row:
        offer_id_str = offer_row[1]
    else:
        domain_code = get_code(domain)
        base_offer_id = f"DBERT-OFR-2026-{domain_code}-{app_id:04d}"

        # Check if base_offer_id is already taken by someone else
        c.execute("SELECT id FROM dbert_internship.intern_offer_letters WHERE offer_letter_id = %s;", (base_offer_id,))
        if c.fetchone():
            offer_id_str = f"DBERT-OFR-2026-{domain_code}-A{app_id:04d}"
        else:
            offer_id_str = base_offer_id

        c.execute("""
            INSERT INTO dbert_internship.intern_offer_letters (
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
            )
            ON CONFLICT (offer_letter_id) DO UPDATE
            SET updated_at = NOW();
        """, (
            offer_id_str, intern_id, app_id, email, name, domain, college,
            batch_start_date, batch_end_date
        ))

    promoted_records.append({
        "serial": idx,
        "app_id": app_id,
        "name": name,
        "email": email,
        "phone": phone,
        "domain": domain,
        "college": college,
        "intern_id": intern_id,
        "offer_letter_id": offer_id_str,
        "status": "Selected",
        "batch_start_date": batch_start_date,
        "batch_end_date": batch_end_date,
        "promoted_at": now_iso
    })

conn.commit()
print(f"[✓] Successfully committed promotion of {len(promoted_records)} applications to 'Selected' in PostgreSQL!")

out_path = "/var/www/dbert-website-lms/data/selected_under_review_cohort_123.json"
try:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(promoted_records, f, indent=2)
    print(f"[✓] Saved cohort records -> {out_path}")
except Exception as e:
    print(f"Note: local file save: {e}")

c.close()
conn.close()
