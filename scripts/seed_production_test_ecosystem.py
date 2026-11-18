import sys
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, get_db, hash_password, _email_sig
from werkzeug.security import generate_password_hash

IST = timezone(timedelta(hours=5, minutes=30))
now_ist = datetime.now(IST)
now_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")

TEST_PW = "TestPass123!"
PW_HASH = generate_password_hash(TEST_PW)
# Also provide PBKDF2 hash
from werkzeug.security import generate_password_hash

with app.app_context():
    conn = get_db()
    cur = conn.cursor()

    personas = [
        # Stage 1: Applied / New
        {
            "id": 9101, "name": "Arun Verma", "email": "stage1_apply@dbert.test",
            "domain": "Full Stack Web Development", "app_status": "Apply Pending",
            "pay_status": None, "deposit": 0, "balance": 0, "joining": None,
            "stage_desc": "Stage 1: Application Received (Interview / Assessment Pending)"
        },
        # Stage 2: Under Review
        {
            "id": 9102, "name": "Bhavna Patel", "email": "stage2_review@dbert.test",
            "domain": "AI & Machine Learning", "app_status": "Under Review",
            "pay_status": None, "deposit": 0, "balance": 0, "joining": None,
            "stage_desc": "Stage 2: Under Review (Sees Fast-Track Incubation Card for ₹499 Seat Confirmation)"
        },
        # Stage 3: Selected / Deposit Pending
        {
            "id": 9103, "name": "Chirag Gupta", "email": "stage3_selected@dbert.test",
            "domain": "Data Analytics", "app_status": "Selected",
            "pay_status": None, "deposit": 0, "balance": 0, "joining": None,
            "stage_desc": "Stage 3: Selected (Sees Offer Letter Preview & ₹499 Caution Deposit Gate)"
        },
        # Stage 4: Enrollment Pending (Deposit Paid / Verifying)
        {
            "id": 9104, "name": "Divya Rao", "email": "stage4_pending@dbert.test",
            "domain": "Python Automation", "app_status": "Enrollment Pending",
            "pay_status": "Pending Verification", "deposit": 1, "balance": 0, "joining": "2026-11-23",
            "stage_desc": "Stage 4: Deposit UTR Submitted (Offer Letter Digitally Signed, Verifying)"
        },
        # Stage 5: Confirmed Intern (Within 7-day balance grace period)
        {
            "id": 9105, "name": "Eshan Sen", "email": "stage5_enrolled@dbert.test",
            "domain": "Full Stack Development", "app_status": "Enrolled",
            "pay_status": "Accepted", "deposit": 1, "balance": 0, "joining": (now_ist - timedelta(days=3)).strftime("%Y-%m-%d"),
            "stage_desc": "Stage 5: Confirmed Intern (Day 3 of 7-Day Balance Grace Period, Sprints Active)"
        },
        # Stage 5 Overdue: Confirmed Intern (Past 7-day balance grace period)
        {
            "id": 9106, "name": "Gaurav Joshi", "email": "stage5_grace_expired@dbert.test",
            "domain": "AI Agent Development", "app_status": "Enrolled",
            "pay_status": "Accepted", "deposit": 1, "balance": 0, "joining": (now_ist - timedelta(days=15)).strftime("%Y-%m-%d"),
            "stage_desc": "Stage 5 (Overdue): Day 15 Intern (Sprints Active, Cert & Stipend Gated until ₹1,500 Balance)"
        },
        # Stage 5 Fully Paid: Incubation Fellow (₹1,999 Completed)
        {
            "id": 9108, "name": "Nisha Kulkarni", "email": "fellow_paid_1999@dbert.test",
            "domain": "Data Analytics", "app_status": "Enrolled",
            "pay_status": "Accepted", "deposit": 1, "balance": 1, "joining": (now_ist - timedelta(days=40)).strftime("%Y-%m-%d"),
            "stage_desc": "Stage 5 (Fully Paid ₹1,999): Balance Cleared, Full Cert & LOR Unlocked"
        },
        # Alumnus: Provisional Credential Holder (Sees Dual-Action Card on /stipend/tasks)
        {
            "id": 9200, "name": "Farhan Ali", "email": "stipend_gate1_locked@dbert.test",
            "domain": "Full Stack Web Development", "app_status": "Enrolled",
            "pay_status": "Verified", "deposit": 1, "balance": 0, "joining": (now_ist - timedelta(days=65)).strftime("%Y-%m-%d"),
            "stage_desc": "Alumnus (Provisional): Sees Dual-Action Card (Option A: ₹1,500 Upgrade vs Option B: Free Re-take)"
        },
        # Alumnus: Verified & Ready to Submit Capstone for ₹5,000 Stipend
        {
            "id": 9204, "name": "Ishita Roy", "email": "stipend_ready@dbert.test",
            "domain": "AI & Machine Learning", "app_status": "Enrolled",
            "pay_status": "Verified", "deposit": 1, "balance": 1, "joining": (now_ist - timedelta(days=65)).strftime("%Y-%m-%d"),
            "stage_desc": "Alumnus (Verified): 60 Days Elapsed, UPI & BYOK Configured, Ready to Submit Capstone for ₹5,000"
        },
        # Alumnus: 5,000 Coins Credited in LMS Wallet
        {
            "id": 9206, "name": "Kavya Nair", "email": "stipend_wallet@dbert.test",
            "domain": "AI & Machine Learning", "app_status": "Enrolled",
            "pay_status": "Verified", "deposit": 1, "balance": 1, "joining": (now_ist - timedelta(days=65)).strftime("%Y-%m-%d"),
            "stage_desc": "Alumnus (Coins in Wallet): 5,000 Coins in Referral Wallet, Ready to Request UPI Payout"
        }
    ]

    print("Seeding/updating personas in EC2 PostgreSQL...")
    for p in personas:
        # 1. Upsert intern_accounts
        cur.execute("""
            INSERT INTO intern_accounts (id, name, email, phone, city, college, course, semester, year_of_passing,
                                        domain, password_hash, password_set, is_active, created_at, updated_at, email_verified, account_status)
            VALUES (%s, %s, %s, '+91 98765 43210', 'New Delhi', 'IIT Delhi', 'B.Tech', 7, 2026,
                    %s, %s, 1, 1, %s, %s, 1, 'active')
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                domain = EXCLUDED.domain,
                password_hash = EXCLUDED.password_hash,
                password_set = 1,
                is_active = 1,
                updated_at = EXCLUDED.updated_at
        """, (p["id"], p["name"], p["email"], p["domain"], PW_HASH, now_str, now_str))

        # 2. Upsert applications
        cur.execute("""
            INSERT INTO applications (id, name, email, phone, city, college, course, semester, year_of_passing,
                                     domain, why_join, status, created_at, updated_at)
            VALUES (%s, %s, %s, '+91 98765 43210', 'New Delhi', 'IIT Delhi', 'B.Tech', 7, 2026,
                    %s, 'DBERT Fellowship Applicant', %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                email = EXCLUDED.email,
                domain = EXCLUDED.domain,
                status = EXCLUDED.status,
                updated_at = EXCLUDED.updated_at
        """, (p["id"], p["name"], p["email"], p["domain"], p["app_status"], now_str, now_str))

        # 3. Upsert enrollments if applicable
        if p["pay_status"]:
            amount = 1999 if p["balance"] == 1 else 499
            cur.execute("""
                INSERT INTO enrollments (id, application_id, intern_id, name, email, phone, college, domain,
                                        joining_date, payment_status, deposit_paid, balance_paid, amount, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, '+91 98765 43210', 'IIT Delhi', %s,
                        %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    name = EXCLUDED.name,
                    email = EXCLUDED.email,
                    domain = EXCLUDED.domain,
                    joining_date = EXCLUDED.joining_date,
                    payment_status = EXCLUDED.payment_status,
                    deposit_paid = EXCLUDED.deposit_paid,
                    balance_paid = EXCLUDED.balance_paid,
                    amount = EXCLUDED.amount,
                    updated_at = EXCLUDED.updated_at
            """, (p["id"], p["id"], p["id"], p["name"], p["email"], p["domain"],
                  p["joining"], p["pay_status"], p["deposit"], p["balance"], amount, now_str, now_str))
        else:
            cur.execute("DELETE FROM enrollments WHERE email = %s", (p["email"],))

    # Also ensure staff and admin accounts
    cur.execute("""
        INSERT INTO staff_accounts (id, name, email, password_hash, is_active, role, created_at)
        VALUES (9001, 'Super Admin QA', 'admin@dbert.test', %s, 1, 'admin', %s)
        ON CONFLICT (id) DO UPDATE SET password_hash = EXCLUDED.password_hash, is_active = 1
    """, (PW_HASH, now_str))

    cur.execute("""
        INSERT INTO staff_accounts (id, name, email, password_hash, is_active, role, created_at)
        VALUES (9002, 'Mentor Staff QA', 'staff@dbert.test', %s, 1, 'staff', %s)
        ON CONFLICT (id) DO UPDATE SET password_hash = EXCLUDED.password_hash, is_active = 1
    """, (PW_HASH, now_str))

    conn.commit()
    print("All personas successfully seeded and updated in EC2 PostgreSQL!")
