import subprocess
import json

remote_code = r"""
import os, sys, json
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

email = 'janvibamane61@gmail.com'

with get_db() as conn:
    print('Starting atomic database reconciliation for:', email)
    
    # 1. Update intern_offer_letters
    cur = conn.execute('''
        UPDATE intern_offer_letters
        SET caution_deposit_status = 'VERIFIED',
            pdf_unlocked = 1,
            signature_name = 'Janvi Bamane',
            name = 'Janvi Bamane',
            accepted_at = '20 Nov 2026, 04:45 PM IST',
            batch_start_date = '2026-11-23',
            batch_end_date = '2027-01-22',
            updated_at = NOW()
        WHERE LOWER(email) = ?
        RETURNING id, offer_letter_id, name, domain, caution_deposit_status, pdf_unlocked, signature_name, accepted_at, batch_start_date, batch_end_date;
    ''', (email,))
    offer_row = cur.fetchone()
    print('Updated intern_offer_letters:', dict(offer_row) if hasattr(offer_row, 'keys') else offer_row)

    # 2. Check if enrollment exists, if not insert
    cur = conn.execute("SELECT id FROM enrollments WHERE LOWER(email) = ?;", (email,))
    enr_existing = cur.fetchone()
    if enr_existing:
        cur = conn.execute('''
            UPDATE enrollments
            SET payment_status = 'Verified',
                amount_paid = 499,
                deposit_paid = 1,
                name = 'Janvi Bamane',
                batch_label = 'Cohort-Sprint-Nov23',
                joining_date = '2026-11-23',
                admin_note = 'Caution deposit ₹499 verified via manual admin reconciliation',
                updated_at = '2026-11-20 16:45:00'
            WHERE id = ?
            RETURNING id, name, email, domain, payment_status, amount_paid, deposit_paid;
        ''', (enr_existing[0],))
        enr_row = cur.fetchone()
        print('Updated existing enrollment:', dict(enr_row) if hasattr(enr_row, 'keys') else enr_row)
    else:
        cur = conn.execute('''
            INSERT INTO enrollments (
                application_id, intern_id, timestamp, name, email, phone, city, college,
                course, semester, year_of_passing, domain, joining_date, batch_label,
                payment_status, admin_note, created_at, updated_at, product, amount,
                amount_paid, deposit_paid, balance_paid
            ) VALUES (
                5180, 5638, '2026-11-20 16:45:00', 'Janvi Bamane', ?, '9324676478', 'Online / Remote', 'Pending Profile',
                'B.Tech', '6', '2026', 'AI Agent Development', '2026-11-23', 'Cohort-Sprint-Nov23',
                'Verified', 'Caution deposit ₹499 verified via manual admin reconciliation',
                '2026-11-20 16:45:00', '2026-11-20 16:45:00', 'Internship Caution Deposit', 499,
                499, 1, 0
            ) RETURNING id, name, email, domain, payment_status, amount_paid, deposit_paid;
        ''', (email,))
        enr_row = cur.fetchone()
        print('Inserted new enrollment:', dict(enr_row) if hasattr(enr_row, 'keys') else enr_row)

    # 3. Update applications table
    cur = conn.execute('''
        UPDATE applications
        SET status = 'Enrolled',
            name = 'Janvi Bamane',
            updated_at = '2026-11-20 16:45:00'
        WHERE LOWER(email) = ?
        RETURNING id, name, email, domain, status;
    ''', (email,))
    app_row = cur.fetchone()
    print('Updated application:', dict(app_row) if hasattr(app_row, 'keys') else app_row)

    # 4. Update intern_accounts
    cur = conn.execute('''
        UPDATE intern_accounts
        SET name = 'Janvi Bamane',
            signup_stage = 4,
            updated_at = '2026-11-20 16:45:00'
        WHERE LOWER(email) = ?
        RETURNING id, name, email, domain, signup_stage;
    ''', (email,))
    acc_row = cur.fetchone()
    print('Updated intern_account:', dict(acc_row) if hasattr(acc_row, 'keys') else acc_row)

    if hasattr(conn, 'commit'):
        conn.commit()
        print('Committed all transactions successfully!')
"""

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

res = subprocess.run(
    ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"],
    input=remote_code,
    text=True,
    capture_output=True
)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
