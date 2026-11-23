"""
scripts/seed_local_test_ecosystem.py - Comprehensive Deterministic Local Test Seeding Engine

Seeds 15+ dedicated test personas, multi-domain 4-week structured curricula,
4-gate stipend lifecycle scenarios, outbox events, and website incubation registries.

All test accounts use uniform password: TestPass123!
Idempotent and safe: uses INSERT OR REPLACE to preserve existing data.
"""

import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Add apps/portal to sys.path so we can reuse app models, configs, and crypto
PORTAL_DIR = Path(__file__).resolve().parent.parent / "apps" / "portal"
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PORTAL_DIR))

from werkzeug.security import generate_password_hash
from cryptography.fernet import Fernet

# Configuration
TEST_PASSWORD = "TestPass123!"
TEST_PASSWORD_HASH = generate_password_hash(TEST_PASSWORD)
TEST_GEMINI_KEY = os.environ.get("TEST_GEMINI_KEY", "AQ.MOCK_TEST_KEY_DEV_ONLY_000000000000000000000000")
TEST_UPI_ID = "testadmissions@okaxis"

FERNET_SECRET = "AhYbKUNXpuCJKsgzhx7_R8xZaBarT51gSQPY4fyxZk4="
fernet = Fernet(FERNET_SECRET.encode())
ENCRYPTED_GEMINI_KEY = fernet.encrypt(TEST_GEMINI_KEY.encode()).decode()
ENCRYPTED_UPI_ID = fernet.encrypt(TEST_UPI_ID.encode()).decode()

from app import get_db, DB_FILE

DB_PATH = Path(DB_FILE)

IST = timezone(timedelta(hours=5, minutes=30))
now_ist = datetime.now(IST)
now_str = now_ist.strftime("%Y-%m-%d %H:%M:%S")


def get_conn():
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    conn.row_factory = sqlite3.Row
    return conn


def seed_administrative_personas(conn):
    print("-> Seeding Administrative & Staff Personas...")
    
    # 1. Super Admin
    conn.execute("""
        INSERT OR REPLACE INTO staff_accounts (id, name, email, password_hash, is_active, role, created_at)
        VALUES (9001, 'Super Admin QA', 'admin@dbert.test', ?, 1, 'admin', ?)
    """, (TEST_PASSWORD_HASH, now_str))

    # 2. Staff Reviewer / Mentor
    conn.execute("""
        INSERT OR REPLACE INTO staff_accounts (id, name, email, password_hash, is_active, role, created_at)
        VALUES (9002, 'Mentor Staff QA', 'staff@dbert.test', ?, 1, 'staff', ?)
    """, (TEST_PASSWORD_HASH, now_str))

    # Queue permissions for staff
    conn.execute("""
        INSERT OR REPLACE INTO staff_queue_roles (staff_id, queue_name)
        VALUES (9002, 'tasks'), (9002, 'applications'), (9002, 'enrollments')
    """)

    # 3. Company Hiring Partner
    conn.execute("""
        INSERT OR REPLACE INTO companies (id, name, email, password_hash, is_active, is_approved, created_at)
        VALUES (9003, 'TechCorp Labs QA', 'recruiter@techcorp.test', ?, 1, 1, ?)
    """, (TEST_PASSWORD_HASH, now_str))


def seed_application_stages(conn):
    print("-> Seeding Internship Application Stages (Stages 1 through 5)...")

    # Clean up previous test enrollments for stages 1, 2, and 3
    conn.execute("DELETE FROM enrollments WHERE email IN ('stage1_apply@dbert.test', 'stage2_review@dbert.test', 'stage3_selected@dbert.test')")

    stages_data = [
        # Stage 1: Apply Pending
        (9101, 'Arun Verma', 'stage1_apply@dbert.test', 'Full Stack Development', 'Apply Pending', None, None),
        # Stage 2: Under Review
        (9102, 'Bhavna Patel', 'stage2_review@dbert.test', 'AI Agent Development', 'Under Review', None, None),
        # Stage 3: Selected (Waiting for candidate to pick Monday & pay ₹499 caution deposit)
        (9103, 'Chirag Gupta', 'stage3_selected@dbert.test', 'Data Analyst', 'Selected', None, None),
        # Stage 4: Enrollment Pending (Candidate paid ₹499, waiting for staff review)
        (9104, 'Divya Rao', 'stage4_pending@dbert.test', 'Python Automation', 'Enrollment Pending', '2026-11-16', 'TEST499UTR001'),
        # Stage 5: Enrolled (Deposit verified, actively working in sprint cohort)
        (9105, 'Eshan Sen', 'stage5_enrolled@dbert.test', 'Full Stack Development', 'Enrolled', '2026-11-09', 'TEST499UTR002'),
    ]

    for intern_id, name, email, domain, status, joining_date, utr in stages_data:
        # 1. Intern Account
        conn.execute("""
            INSERT OR REPLACE INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status, gemini_api_key_encrypted
            ) VALUES (?, ?, ?, ?, '+91 98765 43210', 'Bangalore', 'IIT Tech', 'B.Tech CSE', 7, 2026,
                      ?, ?, 1, 1, ?, ?, 1, 'active', ?)
        """, (intern_id, intern_id, name, email, domain, TEST_PASSWORD_HASH, now_str, now_str, ENCRYPTED_GEMINI_KEY))

        # 2. Application Record
        conn.execute("""
            INSERT OR REPLACE INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (?, ?, ?, '+91 98765 43210', 'Bangalore', 'IIT Tech', 'B.Tech CSE', 7, 2026,
                      ?, 'Passionate about engineering excellence and production deployments.', ?, ?, ?)
        """, (intern_id, name, email, domain, status, now_str, now_str))

        # 3. Status History
        conn.execute("""
            INSERT INTO application_status_history (
                application_id, old_status, new_status, changed_by, changed_at, reason
            ) VALUES (?, 'New', ?, 'admin', ?, 'Automated QA Seeding')
        """, (intern_id, status, now_str))

        # 4. Enrollments table (for Stage 4 and Stage 5)
        if status in ('Enrollment Pending', 'Enrolled'):
            payment_status = 'Pending Verification' if status == 'Enrollment Pending' else 'Verified'
            conn.execute("""
                INSERT OR REPLACE INTO enrollments (
                    id, application_id, timestamp, name, email, phone, city, college, course, semester,
                    year_of_passing, domain, joining_date, batch_label, payment_screenshot, payment_status,
                    admin_note, product, amount, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, '+91 98765 43210', 'Bangalore', 'IIT Tech', 'B.Tech CSE', 7, 2026,
                          ?, ?, 'Batch-Nov-2026', '/uploads/test_receipt.png', ?, ?, 'free_deposit', 499, ?, ?)
            """, (intern_id, intern_id, now_str, name, email, domain, joining_date, payment_status, f"UTR: {utr}", now_str, now_str))


def seed_stipend_progression_scenarios(conn):
    print("-> Seeding 4-Gate Stipend Progression Matrix (6 Personas)...")

    # Personas configuration
    # Gate 1: Provisional Cert Locked (Not verified)
    # Gate 2: 60-Day Milestone Locked (Verified, but joined 20 days ago)
    # Gate 3: Missing UPI ID (Verified, 65 days elapsed, but no UPI)
    # Gate 4: Ready to Submit (Verified, 65 days elapsed, UPI configured, LinkedIn verified)
    # Gate 5: Submitted in Staff Review Queue (AI scored: 88/100, pending staff approval)
    # Gate 6: Wallet Credited (5,000 coins in wallet, ready to request payout)
    # Gate 7: Payout in Admin Queue (Withdrawal requested, waiting in /admin/ambassador-payouts)

    stipend_personas = [
        {
            "id": 9201, "name": "Farhan Ali (Gate 1 Locked)", "email": "stipend_gate1_locked@dbert.test",
            "domain": "Full Stack Web Development", "cert_id": "CERT-DBERT-2026-FSD-901",
            "is_provisional": True, "joining_days_ago": 65, "has_upi": True, "has_linkedin": True, "state": "gate1_locked"
        },
        {
            "id": 9202, "name": "Gauri Menon (Gate 2 Date Locked)", "email": "stipend_gate2_date@dbert.test",
            "domain": "AI & Machine Learning", "cert_id": "CERT-DBERT-2026-AIML-902",
            "is_provisional": False, "joining_days_ago": 20, "has_upi": True, "has_linkedin": True, "state": "gate2_locked"
        },
        {
            "id": 9203, "name": "Hari Prasad (Gate 3 UPI Missing)", "email": "stipend_gate3_upi@dbert.test",
            "domain": "Data Analytics", "cert_id": "CERT-DBERT-2026-DA-903",
            "is_provisional": False, "joining_days_ago": 65, "has_upi": False, "has_linkedin": True, "state": "gate3_locked"
        },
        {
            "id": 9204, "name": "Ishita Roy (Gate 4 Ready to Submit)", "email": "stipend_ready@dbert.test",
            "domain": "Python Automation", "cert_id": "CERT-DBERT-2026-PA-904",
            "is_provisional": False, "joining_days_ago": 65, "has_upi": True, "has_linkedin": True, "state": "ready_to_submit"
        },
        {
            "id": 9205, "name": "Jayesh Shah (In Staff Decision Queue)", "email": "stipend_eval_queue@dbert.test",
            "domain": "Full Stack Web Development", "cert_id": "CERT-DBERT-2026-FSD-905",
            "is_provisional": False, "joining_days_ago": 65, "has_upi": True, "has_linkedin": True, "state": "staff_review"
        },
        {
            "id": 9206, "name": "Kavya Nair (5,000 Coins in Wallet)", "email": "stipend_wallet@dbert.test",
            "domain": "AI & Machine Learning", "cert_id": "CERT-DBERT-2026-AIML-906",
            "is_provisional": False, "joining_days_ago": 65, "has_upi": True, "has_linkedin": True, "state": "coins_in_wallet"
        },
        {
            "id": 9207, "name": "Lalit Deshmukh (Payout in Admin Queue)", "email": "stipend_payout@dbert.test",
            "domain": "Data Analytics", "cert_id": "CERT-DBERT-2026-DA-907",
            "is_provisional": False, "joining_days_ago": 65, "has_upi": True, "has_linkedin": True, "state": "payout_queue"
        },
    ]

    # Pre-create or ensure task exists
    conn.execute("""
        INSERT OR REPLACE INTO tasks (
            id, title, description, coin_reward, is_active, task_type, target_domain, payment_type, submission_type
        ) VALUES (
            9901, 'DBERT Technical Capstone & Stipend Contribution Dossier',
            'Submit your production repository, live deployment, and technical architecture report for stipend verification.',
            5000, 1, 'capstone', 'Universal', 'stipend', 'dossier'
        )
    """)

    conn.execute("""
        INSERT OR REPLACE INTO task_versions (
            id, task_id, version_number, instructions, rubric, created_at
        ) VALUES (
            9901, 9901, 1,
            'Submit your production repository, live deployment, and technical architecture report.',
            'Standard Capstone Evaluation Rubric: Architecture (25), Implementation (25), Viability (25), Documentation (25)',
            ?
        )
    """, (now_str,))

    for p in stipend_personas:
        joining_date = (now_ist - timedelta(days=p["joining_days_ago"])).strftime("%Y-%m-%d")
        upi_val = ENCRYPTED_UPI_ID if p["has_upi"] else None
        linkedin_val = "https://linkedin.com/in/test-qa-" + str(p["id"]) if p["has_linkedin"] else None
        linkedin_ver = 1 if p["has_linkedin"] else 0

        # Intern Account
        conn.execute("""
            INSERT OR REPLACE INTO intern_accounts (
                id, application_id, name, email, phone, city, college, course, semester,
                year_of_passing, domain, password_hash, password_set, is_active, created_at, updated_at,
                email_verified, account_status, upi_id_encrypted, linkedin_url, linkedin_verified, gemini_api_key_encrypted
            ) VALUES (?, ?, ?, ?, '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8, 2026,
                      ?, ?, 1, 1, ?, ?, 1, 'active', ?, ?, ?, ?)
        """, (p["id"], p["id"], p["name"], p["email"], p["domain"], TEST_PASSWORD_HASH,
              now_str, now_str, upi_val, linkedin_val, linkedin_ver, ENCRYPTED_GEMINI_KEY))

        # Application
        conn.execute("""
            INSERT OR REPLACE INTO applications (
                id, name, email, phone, city, college, course, semester, year_of_passing,
                domain, why_join, status, created_at, updated_at
            ) VALUES (?, ?, ?, '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8, 2026,
                      ?, 'Stipend track candidate.', 'Enrolled', ?, ?)
        """, (p["id"], p["name"], p["email"], p["domain"], now_str, now_str))

        # Enrollment record with joining_date
        conn.execute("""
            INSERT OR REPLACE INTO enrollments (
                id, application_id, timestamp, name, email, phone, city, college, course, semester,
                year_of_passing, domain, joining_date, batch_label, payment_screenshot, payment_status,
                product, amount, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, '+91 98765 11111', 'Mumbai', 'BITS Pilani', 'B.Tech IT', 8, 2026,
                      ?, ?, 'Cohort-Sprint', '/uploads/receipt.png', 'Verified', 'free_deposit', 499, ?, ?)
        """, (p["id"], p["id"], now_str, p["name"], p["email"], p["domain"], joining_date, now_str, now_str))

        # Intern Certificate in SQLite
        conn.execute("""
            INSERT OR REPLACE INTO intern_certificates (
                id, intern_id, course_id, course_title, cert_id, issued_at, url, tier, email
            ) VALUES (?, ?, 1, ?, ?, ?, ?, 'Executive Gold', ?)
        """, (p["id"], p["id"], p["domain"] + " Advanced Fellowship", p["cert_id"],
              joining_date, f"https://dbert.in/verify/{p['cert_id']}", p["email"]))

        # Specific State Handling:
        if p["state"] == "staff_review":
            # Seed submitted task with AI evaluation score
            conn.execute("""
                INSERT OR REPLACE INTO task_submissions (
                    id, intern_id, task_id, task_version_id, submission_content, status, coins_awarded,
                    created_at, email, github_repo_url, live_demo_url, report_file_url,
                    ai_evaluation_score, ai_evaluation_status, ai_evaluation_notes, ai_evaluated_at, task_category
                ) VALUES (
                    9305, ?, 9901, 9901, 'Capstone contribution report and microservice repo.', 'submitted', 0,
                    ?, ?, 'https://github.com/dbert-incubator/production-showcase',
                    'https://showcase.dbert.in', '/uploads/capstone_report.pdf',
                    88, 'scored',
                    'Automated AI Pre-Screening: Strong architectural separation, robust error handling, passes all 4 domain criteria.',
                    ?, 'stipend'
                )
            """, (p["id"], now_str, p["email"], now_str))

        elif p["state"] == "coins_in_wallet":
            # Approved submission + coins in wallet
            conn.execute("DELETE FROM ambassador_withdrawals WHERE intern_id = ?", (p["id"],))
            conn.execute("""
                INSERT OR REPLACE INTO task_submissions (
                    id, intern_id, task_id, task_version_id, submission_content, status, coins_awarded,
                    reviewed_by_staff_id, created_at, email, github_repo_url, live_demo_url,
                    ai_evaluation_score, ai_evaluation_status
                ) VALUES (
                    9306, ?, 9901, 9901, 'Capstone contribution report.', 'approved', 5000,
                    9002, ?, ?, 'https://github.com/dbert-incubator/capstone-ml', 'https://ml.dbert.in', 94, 'scored'
                )
            """, (p["id"], now_str, p["email"]))

            conn.execute("""
                INSERT OR REPLACE INTO coin_ledger_mirror (
                    id, intern_id, ledger_kind, delta, balance_after, reason, event_ts, email
                ) VALUES (9406, ?, 'referral', 5000, 5000, 'Stipend Capstone Contribution Approved (Task #9901)', ?, ?)
            """, (p["id"], now_str, p["email"]))

        elif p["state"] == "payout_queue":
            # Coins credited then withdrawal requested
            conn.execute("""
                INSERT OR REPLACE INTO coin_ledger_mirror (
                    id, intern_id, ledger_kind, delta, balance_after, reason, event_ts, email
                ) VALUES (9407, ?, 'referral', 5000, 5000, 'Stipend Capstone Contribution Approved', ?, ?)
            """, (p["id"], now_str, p["email"]))

            conn.execute("""
                INSERT OR REPLACE INTO ambassador_withdrawals (
                    id, intern_id, amount, status, requested_at, admin_note
                ) VALUES (
                    9507, ?, 5000, 'requested', ?, 'Stipend withdrawal request for 5,000 coins via UPI'
                )
            """, (p["id"], now_str))


def seed_multi_domain_curricula(conn):
    print("-> Seeding Multi-Domain Full Curricula (4 Structured Tracks)...")

    tracks = [
        (1, "Full Stack Web Development: Next.js 16, PostgreSQL & Microservices", "full-stack-web-dev", "Full Stack Web Development",
         "Production engineering track covering Next.js App Router, SSR, REST/GraphQL APIs, Prisma, PostgreSQL indexing, Docker, and CI/CD pipelines.",
         "linear-gradient(135deg, #0284c7, #2563eb)"),
        (2, "Applied AI Agents: Production RAG, Tool Calling & Multi-Agent Swarms", "ai-agent-development", "AI & Machine Learning",
         "Design and deploy production autonomous agents using Google Gemini 2.0/Flash, LangChain, vector retrieval (ChromaDB/Pinecone), function calling, and swarm orchestration.",
         "linear-gradient(135deg, #8B5CF6, #6D28D9)"),
        (3, "Data Analytics Accelerated: SQL, Business Intelligence & Statistical EDA", "data-analytics-accelerated", "Data Analytics",
         "End-to-end data pipelines: SQL window functions, Pandas ETL, dashboarding with Tableau/Streamlit, predictive modeling, and executive KPI reporting.",
         "linear-gradient(135deg, #10B981, #059669)"),
        (4, "Python Automation & RPA Architecture: Playwright, Celery & Telemetry", "python-automation-rpa", "Python Automation",
         "Enterprise test automation, web scraping with Playwright, distributed task queues with Celery/Redis, error recovery daemons, and system telemetry.",
         "linear-gradient(135deg, #F59E0B, #D97706)"),
    ]

    for c_id, title, slug, domain, desc, grad in tracks:
        conn.execute("""
            INSERT OR REPLACE INTO courses (
                id, title, slug, domain, is_paid, price_inr, content_status, is_active,
                created_at, level, estimated_hours, requires_project, banner_gradient
            ) VALUES (?, ?, ?, ?, 0, 0, 'approved', 1, ?, 'Intermediate to Advanced', 24, 1, ?)
        """, (c_id, title, slug, domain, now_str, grad))

        # Seed 4 weekly sprint chapters per track
        for w in range(1, 5):
            ch_id = c_id * 100 + w
            conn.execute("""
                INSERT OR REPLACE INTO course_chapters (
                    id, course_id, day_number, title, created_at
                ) VALUES (?, ?, ?, ?, ?)
            """, (ch_id, c_id, w, f"Sprint Week {w}: Core Principles & Production Architecture", now_str))

            # 2 subtopics per chapter
            for s in range(1, 3):
                sub_id = ch_id * 10 + s
                conn.execute("""
                    INSERT OR REPLACE INTO course_subtopics (
                        id, chapter_id, sort_order, title, brief, key_takeaways_json, prompt_seed, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (sub_id, ch_id, s, f"Sprint {w}.{s}: Practical Implementation & Diagnostics",
                      f"Deep dive into {domain} design patterns, writing maintainable code, and testing edge cases.",
                      json.dumps([f"Master {domain} architectures", "Write clean robust tests", "Deploy to staging safely"]),
                      f"Explain how {domain} concepts apply to production microservices.",
                      now_str))

        # Seed a Capstone Project for each course
        conn.execute("""
            INSERT OR REPLACE INTO course_projects (
                id, course_id, brief, created_at
            ) VALUES (?, ?, ?, ?)
        """, (c_id, c_id,
              f"{domain} Production Capstone Architecture: Build and deploy an enterprise-grade service featuring CI/CD, live deployment URL, and comprehensive technical documentation.",
              now_str))


def sync_website_registries():
    print("-> Syncing Website Registries (certificates_registry.json & balance_enrollments_1500.json)...")

    # 1. Update certificates_registry.json
    cert_reg_path = REPO_ROOT / "apps" / "website" / "src" / "data" / "certificates_registry.json"
    with open(cert_reg_path, "r", encoding="utf-8") as f:
        certs = json.load(f)

    # Ensure it's a list or dict
    test_certs = [
        {
            "certId": "CERT-DBERT-2026-FSD-901", "internId": "DBERT-2026-INT-9201",
            "holderName": "Farhan Ali (Gate 1 Locked)", "email": "stipend_gate1_locked@dbert.test",
            "phone": "+91 98765 11111", "domain": "Full Stack Web Development", "college": "BITS Pilani",
            "status": "PROVISIONAL", "isProvisional": True, "score": 85, "grade": "Merit",
            "issueDate": "2026-10-15", "endDate": "2026-11-14"
        },
        {
            "certId": "CERT-DBERT-2026-AIML-902", "internId": "DBERT-2026-INT-9202",
            "holderName": "Gauri Menon (Gate 2 Date Locked)", "email": "stipend_gate2_date@dbert.test",
            "phone": "+91 98765 11111", "domain": "AI & Machine Learning", "college": "BITS Pilani",
            "status": "VERIFIED", "isProvisional": False, "score": 82, "grade": "Grade: A (High Merit)",
            "issueDate": "2026-10-25", "endDate": "2026-12-25"
        },
        {
            "certId": "CERT-DBERT-2026-DA-903", "internId": "DBERT-2026-INT-9203",
            "holderName": "Hari Prasad (Gate 3 UPI Missing)", "email": "stipend_gate3_upi@dbert.test",
            "phone": "+91 98765 11111", "domain": "Data Analytics", "college": "BITS Pilani",
            "status": "VERIFIED", "isProvisional": False, "score": 92, "grade": "Distinction",
            "issueDate": "2026-09-10", "endDate": "2026-11-10"
        },
        {
            "certId": "CERT-DBERT-2026-PA-904", "internId": "DBERT-2026-INT-9204",
            "holderName": "Ishita Roy (Gate 4 Ready to Submit)", "email": "stipend_ready@dbert.test",
            "phone": "+91 98765 11111", "domain": "Python Automation", "college": "BITS Pilani",
            "status": "VERIFIED", "isProvisional": False, "score": 95, "grade": "Distinction",
            "issueDate": "2026-09-10", "endDate": "2026-11-10"
        },
        {
            "certId": "CERT-DBERT-2026-FSD-905", "internId": "DBERT-2026-INT-9205",
            "holderName": "Jayesh Shah (In Staff Decision Queue)", "email": "stipend_eval_queue@dbert.test",
            "phone": "+91 98765 11111", "domain": "Full Stack Web Development", "college": "BITS Pilani",
            "status": "VERIFIED", "isProvisional": False, "score": 91, "grade": "Distinction",
            "issueDate": "2026-09-10", "endDate": "2026-11-10"
        },
        {
            "certId": "CERT-DBERT-2026-AIML-906", "internId": "DBERT-2026-INT-9206",
            "holderName": "Kavya Nair (5,000 Coins in Wallet)", "email": "stipend_wallet@dbert.test",
            "phone": "+91 98765 11111", "domain": "AI & Machine Learning", "college": "BITS Pilani",
            "status": "VERIFIED", "isProvisional": False, "score": 97, "grade": "Distinction",
            "issueDate": "2026-09-10", "endDate": "2026-11-10"
        },
        {
            "certId": "CERT-DBERT-2026-DA-907", "internId": "DBERT-2026-INT-9207",
            "holderName": "Lalit Deshmukh (Payout in Admin Queue)", "email": "stipend_payout@dbert.test",
            "phone": "+91 98765 11111", "domain": "Data Analytics", "college": "BITS Pilani",
            "status": "VERIFIED", "isProvisional": False, "score": 93, "grade": "Distinction",
            "issueDate": "2026-09-10", "endDate": "2026-11-10"
        },
    ]

    # Merge into certs
    if isinstance(certs, list):
        cert_map = {c.get("certId"): c for c in certs}
        for tc in test_certs:
            cert_map[tc["certId"]] = tc
        updated_certs = list(cert_map.values())
    elif isinstance(certs, dict):
        for tc in test_certs:
            certs[tc["certId"]] = tc
        updated_certs = certs

    with open(cert_reg_path, "w", encoding="utf-8") as f:
        json.dump(updated_certs, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Added/updated {len(test_certs)} test certificates in certificates_registry.json")

    # 2. Update data/balance_enrollments_1500.json
    balance_file = REPO_ROOT / "data" / "balance_enrollments_1500.json"
    if balance_file.exists():
        with open(balance_file, "r", encoding="utf-8") as f:
            balances = json.load(f)
    else:
        balances = []

    test_balances = [
        # Candidate 1: Balance Payable ₹1,500
        {
            "id": "DBERT-ENR-TEST-1500",
            "submittedAt": now_str,
            "fullName": "Kunal Sharma (₹1,500 Balance Payable)",
            "email": "balance1500@dbert.test",
            "phone": "+91 98111 22233",
            "college": "Delhi Technological University",
            "domain": "Full Stack Web Development",
            "certId": "CERT-DBERT-2026-FSD-901",
            "amountExpected": 1500,
            "amountClaimed": 1500,
            "amountVerified": 0,
            "amountPaid": 0,
            "utrNumber": "TEST1500UTR01",
            "status": "SUBMITTED"
        },
        # Candidate 2: Approved Enrollment with Live Standup Countdown
        {
            "id": "DBERT-ENR-TEST-APPROVED",
            "submittedAt": now_str,
            "fullName": "Meera Joshi (Approved & Seat Confirmed)",
            "email": "approved_fellow@dbert.test",
            "phone": "+91 98222 33344",
            "college": "BITS Pilani",
            "domain": "AI & Machine Learning",
            "certId": "CERT-DBERT-2026-AIML-902",
            "amountExpected": 1500,
            "amountClaimed": 1500,
            "amountVerified": 1500,
            "amountPaid": 1500,
            "utrNumber": "TESTAPPROVED01",
            "status": "APPROVED",
            "batchStartDate": "2026-11-16T18:00:00+05:30",
            "batchStartDisplay": "Monday, 16 Nov 2026"
        }
    ]

    balance_map = {b.get("id"): b for b in balances}
    for tb in test_balances:
        balance_map[tb["id"]] = tb

    with open(balance_file, "w", encoding="utf-8") as f:
        json.dump(list(balance_map.values()), f, indent=2, ensure_ascii=False)
    print(f"  ✓ Added/updated {len(test_balances)} test records in balance_enrollments_1500.json")


def main():
    print("====================================================================")
    print("DBERT ECOSYSTEM: LOCAL TEST DATA SEEDING ENGINE")
    print("====================================================================")
    print(f"Target Database: {DB_PATH}")
    print(f"Uniform Test Password: {TEST_PASSWORD}")
    print(f"Active Gemini Key: {TEST_GEMINI_KEY[:6]}...{TEST_GEMINI_KEY[-6:]}")

    conn = get_conn()
    with conn:
        seed_administrative_personas(conn)
        seed_application_stages(conn)
        seed_stipend_progression_scenarios(conn)
        seed_multi_domain_curricula(conn)
    conn.close()

    sync_website_registries()

    print("\n[SUCCESS] Local test data seeding completed successfully!")
    print("Next step: Access /dev/qa-matrix on your local LMS server to navigate all test personas.\n")


if __name__ == "__main__":
    main()
