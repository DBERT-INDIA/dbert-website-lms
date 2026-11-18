#!/usr/bin/env python3
"""
scripts/seed_ec2_test_personas.py
Seeds comprehensive test accounts across all user lifecycle roles directly into EC2 PostgreSQL.
Enforces foreign key order: applications -> intern_accounts -> enrollments.
Uniform password for all accounts: TestPass123!
"""
import sys
import os
import json
from datetime import datetime, timedelta, timezone

# Ensure portal path is available
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, hash_password, encrypt_upi, FERNET_KEY

TEST_PASSWORD = "TestPass123!"
TEST_PASSWORD_HASH = hash_password(TEST_PASSWORD)
TEST_UPI_ID = "testadmissions@okaxis"
ENCRYPTED_UPI = encrypt_upi(TEST_UPI_ID)

IST = timezone(timedelta(hours=5, minutes=30))
now_ist = datetime.now(IST)
now_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")

def run_seeding():
    print("=" * 70)
    print("Seeding Comprehensive EC2 Test Personas for DBERT Ecosystem")
    print("=" * 70)

    with get_db() as conn:
        # =====================================================================
        # 1. Administrative & Staff Personas
        # =====================================================================
        print("\n[1/7] Seeding Staff & Admin Accounts...")
        conn.execute("""
            INSERT INTO staff_accounts (id, name, email, password_hash, is_active, role, created_at)
            VALUES (9001, 'DBERT Super Admin QA', 'dbert_admin@dbert.test', ?, 1, 'admin', ?)
            ON CONFLICT (id) DO UPDATE SET
                password_hash = EXCLUDED.password_hash,
                is_active = 1,
                role = 'admin'
        """, (TEST_PASSWORD_HASH, now_str))

        conn.execute("""
            INSERT INTO staff_accounts (id, name, email, password_hash, is_active, role, created_at)
            VALUES (9002, 'Rohan Kulkarni (Mentor Staff QA)', 'mentor_staff@dbert.test', ?, 1, 'staff', ?)
            ON CONFLICT (id) DO UPDATE SET
                password_hash = EXCLUDED.password_hash,
                is_active = 1,
                role = 'staff'
        """, (TEST_PASSWORD_HASH, now_str))

        # Seed mentor availability slot for slot booking tests
        conn.execute("""
            INSERT INTO mentor_availability_slots (id, mentor_staff_id, start_time, end_time, capacity, seats_booked, is_booked, domain, topic)
            VALUES (901, 9002, '2026-11-20 18:00:00', '2026-11-20 19:00:00', 30, 2, 0, 'Full Stack Web Development', 'System Architecture & Deployment')
            ON CONFLICT (id) DO UPDATE SET
                mentor_staff_id = EXCLUDED.mentor_staff_id,
                start_time = EXCLUDED.start_time,
                seats_booked = 2,
                is_booked = 0
        """)

        # =====================================================================
        # 2. Fully Enrolled Fellow (Bounties, Web Push, Attendance, Quizzes)
        # =====================================================================
        print("\n[2/7] Seeding Fully Enrolled Fellow (fellow_enrolled@dbert.test)...")
        conn.execute("""
            INSERT INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (
                9105, 'Eshan Sen', 'fellow_enrolled@dbert.test', '+91 98765 43210', 'Bangalore', 'IIT Tech', 'B.Tech CSE', 7,
                2026, 'Full Stack Web Development', 'Passionate about engineering excellence and production deployments.', 'Enrolled', ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET status = 'Enrolled'
        """, (now_str, now_str))

        conn.execute("""
            INSERT INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status, upi_id_encrypted
            ) VALUES (
                9105, 9105, 'Eshan Sen', 'fellow_enrolled@dbert.test', '+91 98765 43210', 'Bangalore', 'IIT Tech', 'B.Tech CSE', 7,
                2026, 'Full Stack Web Development', ?, 1, 1, ?, ?, 1, 'active', ?
            )
            ON CONFLICT (id) DO UPDATE SET
                email = EXCLUDED.email,
                name = EXCLUDED.name,
                application_id = 9105,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1,
                domain = EXCLUDED.domain
        """, (TEST_PASSWORD_HASH, now_str, now_str, ENCRYPTED_UPI))

        conn.execute("""
            INSERT INTO enrollments (
                id, application_id, timestamp, name, email, phone, city, college, course, semester,
                year_of_passing, domain, joining_date, batch_label, payment_screenshot, payment_status,
                admin_note, product, amount, created_at, updated_at
            ) VALUES (
                9105, 9105, ?, 'Eshan Sen', 'fellow_enrolled@dbert.test', '+91 98765 43210', 'Bangalore', 'IIT Tech', 'B.Tech CSE', 7,
                2026, 'Full Stack Web Development', '2026-11-09', 'Batch-Nov-2026', '/uploads/test_receipt.png', 'Verified',
                'Enrolled Fellow', 'free_deposit', 499, ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET payment_status = 'Verified'
        """, (now_str, now_str, now_str))

        conn.execute("""
            INSERT INTO course_enrollments (id, intern_id, course_id, email, current_day, enrolled_at)
            VALUES (9105, 9105, 1, 'fellow_enrolled@dbert.test', 2, ?)
            ON CONFLICT (id) DO UPDATE SET current_day = 2
        """, (now_str,))

        # =====================================================================
        # 3. Capstone & Stipend Candidate (Gates 1-4 Cleared, Ready to Submit)
        # =====================================================================
        print("\n[3/7] Seeding Stipend Candidate Ready to Submit (stipend_ready@dbert.test)...")
        sixty_five_days_ago = (now_ist - timedelta(days=65)).strftime("%Y-%m-%d")

        conn.execute("""
            INSERT INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (
                9204, 'Ishita Roy', 'stipend_ready@dbert.test', '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8,
                2026, 'AI & Machine Learning', 'Completed 60-day sprint.', 'Enrolled', ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET status = 'Enrolled'
        """, (now_str, now_str))

        conn.execute("""
            INSERT INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status, upi_id_encrypted, linkedin_url, linkedin_verified,
                stipend_verified, stipend_amount
            ) VALUES (
                9204, 9204, 'Ishita Roy', 'stipend_ready@dbert.test', '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8,
                2026, 'AI & Machine Learning', ?, 1, 1, ?, ?, 1, 'active', ?,
                'https://linkedin.com/in/ishita-roy-ai-dbert', 1, 1, 5000
            )
            ON CONFLICT (id) DO UPDATE SET
                application_id = 9204,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1,
                upi_id_encrypted = EXCLUDED.upi_id_encrypted,
                linkedin_verified = 1,
                stipend_verified = 1
        """, (TEST_PASSWORD_HASH, now_str, now_str, ENCRYPTED_UPI))

        conn.execute("""
            INSERT INTO enrollments (
                id, application_id, timestamp, name, email, phone, city, college, course, semester,
                year_of_passing, domain, joining_date, batch_label, payment_screenshot, payment_status,
                admin_note, product, amount, created_at, updated_at
            ) VALUES (
                9204, 9204, ?, 'Ishita Roy', 'stipend_ready@dbert.test', '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8,
                2026, 'AI & Machine Learning', ?, 'Cohort-Sprint-Sep', '/uploads/receipt.png', 'Verified',
                'Completed 60 days', 'free_deposit', 499, ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET joining_date = EXCLUDED.joining_date, payment_status = 'Verified'
        """, (now_str, sixty_five_days_ago, now_str, now_str))

        # Seed verified certificate record in intern_certificates
        conn.execute("""
            INSERT INTO intern_certificates (
                id, intern_id, course_id, course_title, cert_id, issued_at, url, tier, email
            ) VALUES (
                9204, 9204, 1, 'AI & Machine Learning Production Incubation', 'CERT-DBERT-2026-AIML-904',
                ?, '/portal/certificate/CERT-DBERT-2026-AIML-904', 'Distinction', 'stipend_ready@dbert.test'
            )
            ON CONFLICT (id) DO UPDATE SET
                cert_id = EXCLUDED.cert_id,
                course_title = EXCLUDED.course_title,
                email = EXCLUDED.email
        """, (now_str,))

        # =====================================================================
        # 4. Withdrawable Wallet & UPI Payout Candidate (stipend_wallet@dbert.test)
        # =====================================================================
        print("\n[4/7] Seeding Withdrawable Wallet Candidate (stipend_wallet@dbert.test)...")
        conn.execute("""
            INSERT INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (
                9206, 'Kavya Nair', 'stipend_wallet@dbert.test', '+91 98765 22222', 'Delhi', 'DTU', 'B.Tech CSE', 8,
                2026, 'AI & Machine Learning', 'Wallet payout candidate.', 'Enrolled', ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET status = 'Enrolled'
        """, (now_str, now_str))

        conn.execute("""
            INSERT INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status, upi_id_encrypted, stipend_verified, stipend_amount
            ) VALUES (
                9206, 9206, 'Kavya Nair', 'stipend_wallet@dbert.test', '+91 98765 22222', 'Delhi', 'DTU', 'B.Tech CSE', 8,
                2026, 'AI & Machine Learning', ?, 1, 1, ?, ?, 1, 'active', ?, 1, 5000
            )
            ON CONFLICT (id) DO UPDATE SET
                application_id = 9206,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1,
                upi_id_encrypted = EXCLUDED.upi_id_encrypted
        """, (TEST_PASSWORD_HASH, now_str, now_str, ENCRYPTED_UPI))

        conn.execute("""
            INSERT INTO enrollments (
                id, application_id, timestamp, name, email, phone, city, college, course, semester,
                year_of_passing, domain, joining_date, batch_label, payment_screenshot, payment_status,
                admin_note, product, amount, created_at, updated_at
            ) VALUES (
                9206, 9206, ?, 'Kavya Nair', 'stipend_wallet@dbert.test', '+91 98765 22222', 'Delhi', 'DTU', 'B.Tech CSE', 8,
                2026, 'AI & Machine Learning', ?, 'Cohort-Sprint-Sep', '/uploads/receipt.png', 'Verified',
                'Completed 60 days', 'free_deposit', 499, ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET payment_status = 'Verified'
        """, (now_str, sixty_five_days_ago, now_str, now_str))

        # Credit 5,000 Coins to Kavya's referral/withdrawable ledger
        conn.execute("DELETE FROM coin_ledger_mirror WHERE intern_id = 9206")
        conn.execute("""
            INSERT INTO coin_ledger_mirror (
                intern_id, ledger_kind, delta, balance_after, reason, event_ts, received_at, idem_key, email
            ) VALUES (
                9206, 'referral', 5000, 5000, 'Stipend Milestone Approved: AI & Machine Learning Capstone',
                ?, ?, 'idem_seed_kavya_5000', 'stipend_wallet@dbert.test'
            )
        """, (now_str, now_str))

        # =====================================================================
        # 5. Provisional Fellow (Stipend Locked / ₹1,500 Balance Due)
        # =====================================================================
        print("\n[5/7] Seeding Provisional Fellow (provisional_fellow@dbert.test & stipend_gate1_locked@dbert.test)...")
        conn.execute("""
            INSERT INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (
                9201, 'Farhan Ali', 'provisional_fellow@dbert.test', '+91 98765 33333', 'Hyderabad', 'BITS', 'B.Tech CSE', 6,
                2026, 'Data Analytics', 'Provisional Incubation fellow.', 'Enrolled', ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET status = 'Enrolled'
        """, (now_str, now_str))

        conn.execute("""
            INSERT INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status
            ) VALUES (
                9201, 9201, 'Farhan Ali', 'provisional_fellow@dbert.test', '+91 98765 33333', 'Hyderabad', 'BITS', 'B.Tech CSE', 6,
                2026, 'Data Analytics', ?, 1, 1, ?, ?, 1, 'active'
            )
            ON CONFLICT (id) DO UPDATE SET
                application_id = 9201,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1
        """, (TEST_PASSWORD_HASH, now_str, now_str))

        conn.execute("""
            INSERT INTO enrollments (
                id, application_id, timestamp, name, email, phone, city, college, course, semester,
                year_of_passing, domain, joining_date, batch_label, payment_screenshot, payment_status,
                admin_note, product, amount, created_at, updated_at
            ) VALUES (
                9201, 9201, ?, 'Farhan Ali', 'provisional_fellow@dbert.test', '+91 98765 33333', 'Hyderabad', 'BITS', 'B.Tech CSE', 6,
                2026, 'Data Analytics', ?, 'Batch-Nov-2026', '/uploads/receipt.png', 'Verified',
                'Provisional Incubation', 'free_deposit', 499, ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET payment_status = 'Verified'
        """, (now_str, sixty_five_days_ago, now_str, now_str))

        # Explicit stipend_gate1_locked@dbert.test
        conn.execute("""
            INSERT INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (
                9200, 'Farhan Ali (Gate 1 Locked)', 'stipend_gate1_locked@dbert.test', '+91 98765 11111', 'Hyderabad', 'BITS', 'B.Tech CSE', 6,
                2026, 'Full Stack Web Development', 'Gate 1 Provisional Candidate.', 'Enrolled', ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET status = 'Enrolled'
        """, (now_str, now_str))

        conn.execute("""
            INSERT INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status
            ) VALUES (
                9200, 9200, 'Farhan Ali (Gate 1 Locked)', 'stipend_gate1_locked@dbert.test', '+91 98765 11111', 'Hyderabad', 'BITS', 'B.Tech CSE', 6,
                2026, 'Full Stack Web Development', ?, 1, 1, ?, ?, 1, 'active'
            )
            ON CONFLICT (id) DO UPDATE SET
                application_id = 9200,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1
        """, (TEST_PASSWORD_HASH, now_str, now_str))

        conn.execute("""
            INSERT INTO enrollments (
                id, application_id, timestamp, name, email, phone, city, college, course, semester,
                year_of_passing, domain, joining_date, batch_label, payment_screenshot, payment_status,
                admin_note, product, amount, created_at, updated_at
            ) VALUES (
                9200, 9200, ?, 'Farhan Ali (Gate 1 Locked)', 'stipend_gate1_locked@dbert.test', '+91 98765 11111', 'Hyderabad', 'BITS', 'B.Tech CSE', 6,
                2026, 'Full Stack Web Development', ?, 'Batch-Nov-2026', '/uploads/receipt.png', 'Verified',
                'Provisional Incubation', 'free_deposit', 499, ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET payment_status = 'Verified'
        """, (now_str, sixty_five_days_ago, now_str, now_str))

        conn.execute("""
            INSERT INTO intern_certificates (
                id, intern_id, course_id, course_title, cert_id, issued_at,
                received_at, url, tier, email
            ) VALUES (
                9201, 9200, 1, 'Full Stack Web Development Incubation',
                'CERT-DBERT-2026-FSD-901', ?,
                ?, '/portal/certificate/CERT-DBERT-2026-FSD-901', 'Provisional', 'stipend_gate1_locked@dbert.test'
            )
            ON CONFLICT (id) DO UPDATE SET
                intern_id = 9200,
                tier = 'Provisional',
                cert_id = 'CERT-DBERT-2026-FSD-901',
                email = 'stipend_gate1_locked@dbert.test'
        """, (now_str, now_str))

        # =====================================================================
        # 6. Stage 3 Selected Candidate (Caution Deposit Due)
        # =====================================================================
        print("\n[6/7] Seeding Stage 3 Selected Candidate (stage3_selected@dbert.test)...")
        conn.execute("""
            INSERT INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (
                9103, 'Chirag Gupta', 'stage3_selected@dbert.test', '+91 98765 55555', 'Pune', 'COEP', 'B.Tech IT', 7,
                2026, 'Data Analytics', 'Excited for real data pipelines.', 'Selected', ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET status = 'Selected'
        """, (now_str, now_str))

        conn.execute("""
            INSERT INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status
            ) VALUES (
                9103, 9103, 'Chirag Gupta', 'stage3_selected@dbert.test', '+91 98765 55555', 'Pune', 'COEP', 'B.Tech IT', 7,
                2026, 'Data Analytics', ?, 1, 1, ?, ?, 1, 'active'
            )
            ON CONFLICT (id) DO UPDATE SET
                application_id = 9103,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1
        """, (TEST_PASSWORD_HASH, now_str, now_str))

        # =====================================================================
        # 7. Digital Offer Letter Ready to Sign (offer_pending@dbert.test)
        # =====================================================================
        print("\n[7/7] Seeding Digital Offer Letter Candidate (offer_pending@dbert.test)...")
        conn.execute("""
            INSERT INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (
                9107, 'Aarav Mehta', 'offer_pending@dbert.test', '+91 98765 77777', 'Delhi', 'NSUT', 'B.Tech CSE', 7,
                2026, 'Python Automation', 'Interested in building autonomous RPA agents.', 'Selected', ?, ?
            )
            ON CONFLICT (id) DO UPDATE SET status = 'Selected'
        """, (now_str, now_str))

        conn.execute("""
            INSERT INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status
            ) VALUES (
                9107, 9107, 'Aarav Mehta', 'offer_pending@dbert.test', '+91 98765 77777', 'Delhi', 'NSUT', 'B.Tech CSE', 7,
                2026, 'Python Automation', ?, 1, 1, ?, ?, 1, 'active'
            )
            ON CONFLICT (id) DO UPDATE SET
                application_id = 9107,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1
        """, (TEST_PASSWORD_HASH, now_str, now_str))

        conn.execute("""
            INSERT INTO intern_offer_letters (
                offer_letter_id, intern_id, enrollment_id, email, name, domain, college,
                batch_start_date, batch_end_date, tenure_months, stipend_amount, login_hours_per_week,
                required_certifications, required_bounty_tasks, caution_deposit_amount, caution_deposit_status,
                signature_name, accepted_at, pdf_unlocked, created_at, updated_at
            ) VALUES (
                'DBERT-OFR-2026-PA-991', 9107, 9107, 'offer_pending@dbert.test', 'Aarav Mehta',
                'Python Automation', 'NSUT Delhi', '2026-11-23', '2027-01-23', 2, 5000, 10,
                1, 4, 499, 'unpaid', NULL, NULL, 0, ?, ?
            )
            ON CONFLICT (offer_letter_id) DO UPDATE SET
                signature_name = NULL,
                accepted_at = NULL,
                pdf_unlocked = 0
        """, (now_str, now_str))

        conn.commit()

    print("\n" + "=" * 70)
    print("SUCCESS: All 7 Ecosystem Test Personas Seeded on EC2 PostgreSQL!")
    print("Uniform Password for all test accounts: TestPass123!")
    print("=" * 70)

if __name__ == "__main__":
    run_seeding()
