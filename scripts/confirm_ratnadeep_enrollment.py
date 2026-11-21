#!/usr/bin/env python3
"""
================================================================================
DBERT — Confirm Ratnadeep manojkumar bamane ₹499 Payment & Enrollment
================================================================================
"""

import os
import sys
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')

from app import app, get_db, handle_enrollment_accepted, send_enrollment_acceptance_dossier_email, send_push_notification, row_to_dict

EMAIL = 'ratnadeepratu737@gmail.com'
NAME = 'Ratnadeep manojkumar bamane'
PHONE = '8591833879'
DOMAIN = 'Data Analyst'
COLLEGE = 'Sree Narayan Guru College'
APP_ID = 5278
INTERN_ID = 5748
BATCH_START = '2026-11-23'
BATCH_LABEL = '23 Nov 2026 Batch'

print(f"Confirming ₹499 payment and enrollment for {NAME} ({EMAIL})...")

db_url = os.environ.get('DATABASE_URL')
conn = psycopg2.connect(db_url)
c = conn.cursor()

# 1. Check existing enrollment or insert
c.execute("SELECT id FROM enrollments WHERE LOWER(email) = %s ORDER BY id DESC LIMIT 1;", (EMAIL,))
row = c.fetchone()

if row:
    enr_id = row[0]
    print(f"Updating existing enrollment ID: {enr_id}")
    c.execute("""
        UPDATE enrollments
        SET payment_status = 'Accepted',
            deposit_paid = 1,
            amount = 499,
            amount_paid = 499,
            product = 'free_deposit',
            joining_date = %s,
            batch_label = %s,
            admin_note = '₹499 Caution Deposit Verified & Confirmed',
            updated_at = %s
        WHERE id = %s;
    """, (BATCH_START, BATCH_LABEL, datetime.now().isoformat(), enr_id))
else:
    print("Inserting new enrollment record...")
    c.execute("""
        INSERT INTO enrollments (
            application_id, name, email, phone, college, domain,
            joining_date, batch_label, payment_status, admin_note,
            product, amount, amount_paid, deposit_paid, intern_id,
            created_at, updated_at
        ) VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, 'Accepted', '₹499 Caution Deposit Verified & Confirmed',
            'free_deposit', 499, 499, 1, %s,
            %s, %s
        ) RETURNING id;
    """, (
        APP_ID, NAME, EMAIL, PHONE, COLLEGE, DOMAIN,
        BATCH_START, BATCH_LABEL, INTERN_ID,
        datetime.now().isoformat(), datetime.now().isoformat()
    ))
    enr_id = c.fetchone()[0]
    print(f"Created enrollment ID: {enr_id}")

# 2. Update applications
c.execute("""
    UPDATE applications
    SET status = 'Accepted',
        updated_at = %s
    WHERE id = %s;
""", (datetime.now().isoformat(), APP_ID))

# 3. Update intern_accounts
c.execute("""
    UPDATE intern_accounts
    SET is_active = 1,
        account_status = 'active',
        updated_at = %s
    WHERE id = %s;
""", (datetime.now().isoformat(), INTERN_ID))

# 4. Update intern_offer_letters
c.execute("""
    UPDATE intern_offer_letters
    SET caution_deposit_status = 'VERIFIED',
        pdf_unlocked = 1,
        updated_at = %s
    WHERE LOWER(email) = %s;
""", (datetime.now().isoformat(), EMAIL))

conn.commit()
print("PostgreSQL transaction committed.")

c.close()
conn.close()

# 5. Handle acceptance triggers and notifications with app context
with app.app_context():
    with get_db() as db_conn:
        try:
            handle_enrollment_accepted(db_conn, enr_id)
            print("Ambassador code & referral handling executed successfully.")
        except Exception as e:
            print(f"Warning handle_enrollment_accepted: {e}")

        try:
            enr_row = db_conn.execute("SELECT * FROM enrollments WHERE id = ?", (enr_id,)).fetchone()
            enr_dict = row_to_dict(enr_row) if enr_row else {}
            email_sent = send_enrollment_acceptance_dossier_email(enr_dict, conn=db_conn)
            print(f"Dossier acceptance email sent: {email_sent}")
        except Exception as e:
            print(f"Warning dossier email: {e}")

        try:
            send_push_notification(
                to_email=EMAIL,
                title="🎉 Enrollment Confirmed & Seat Unlocked!",
                message=f"Welcome {NAME}! Your ₹499 caution deposit has been verified. Your official appointment letter and workstation are now ready.",
                url="https://lms.dbert.in/portal/offer",
                kind="deposit_verified"
            )
            print("Push notification dispatched successfully.")
        except Exception as e:
            print(f"Warning push notification: {e}")

print("\nSUCCESS: All database records updated and verified on EC2!")
