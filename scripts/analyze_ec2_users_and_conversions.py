import subprocess

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

remote_script = '''
import psycopg2, os, json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

print("=================================================================")
print("=== 1. INTERN ACCOUNTS OVERVIEW & STAGES ===")
print("=================================================================")
c.execute("SELECT count(*) FROM dbert_internship.intern_accounts;")
total_interns = c.fetchone()[0]
print(f"Total Intern Accounts: {total_interns}")

c.execute("SELECT signup_stage, count(*) FROM dbert_internship.intern_accounts GROUP BY signup_stage ORDER BY count(*) DESC;")
print("\\nSignup Stage Distribution:")
for r in c.fetchall():
    print(f"  Stage '{r[0]}': {r[1]}")

c.execute("SELECT account_status, count(*) FROM dbert_internship.intern_accounts GROUP BY account_status ORDER BY count(*) DESC;")
print("\\nAccount Status Distribution:")
for r in c.fetchall():
    print(f"  Status '{r[0]}': {r[1]}")

c.execute("SELECT program, count(*) FROM dbert_internship.intern_accounts GROUP BY program ORDER BY count(*) DESC;")
print("\\nProgram Distribution:")
for r in c.fetchall():
    print(f"  Program '{r[0]}': {r[1]}")

c.execute("SELECT domain, count(*) FROM dbert_internship.intern_accounts GROUP BY domain ORDER BY count(*) DESC;")
print("\\nDomain Track Distribution:")
for r in c.fetchall():
    print(f"  Domain '{r[0]}': {r[1]}")

print("\\n=================================================================")
print("=== 2. LOGINS & USER ACTIVITY (LAST 15 DAYS: Since 2026-11-05) ===")
print("=================================================================")
c.execute("""
    SELECT count(*), count(DISTINCT email) 
    FROM dbert_internship.user_sessions 
    WHERE created_at::timestamp >= '2026-11-05 00:00:00';
""")
sess_15d, users_15d = c.fetchone()
print(f"Sessions in last 15 days: {sess_15d}")
print(f"Distinct Users logged in in last 15 days: {users_15d}")

c.execute("""
    SELECT email, count(*) as login_count, min(created_at), max(created_at)
    FROM dbert_internship.user_sessions 
    WHERE created_at::timestamp >= '2026-11-05 00:00:00'
    GROUP BY email
    ORDER BY login_count DESC;
""")
active_users = c.fetchall()
print(f"Top 15 Most Active Users (by logins in last 15 days):")
for u in active_users[:15]:
    print(f"  {u[0]:35s} | Logins: {u[1]:3d} | First: {str(u[2])[:16]} | Last: {str(u[3])[:16]}")

# Login frequency buckets
buckets = {"1 login": 0, "2-4 logins": 0, "5-9 logins": 0, "10+ logins": 0}
for u in active_users:
    cnt = u[1]
    if cnt == 1:
        buckets["1 login"] += 1
    elif 2 <= cnt <= 4:
        buckets["2-4 logins"] += 1
    elif 5 <= cnt <= 9:
        buckets["5-9 logins"] += 1
    else:
        buckets["10+ logins"] += 1
print("\\nLogin Frequency Buckets (Last 15 days):")
for b, cnt in buckets.items():
    print(f"  {b:15s}: {cnt} users")

print("\\n=================================================================")
print("=== 3. INTENT SIGNALS & ENGAGEMENT METRICS ===")
print("=================================================================")
c.execute("""
    SELECT 
        count(*) FILTER (WHERE linkedin_verified = 1) as linkedin_ver,
        count(*) FILTER (WHERE terms_accepted_at IS NOT NULL) as terms_acc,
        count(*) FILTER (WHERE gemini_api_key_encrypted IS NOT NULL) as gemini_key,
        count(*) FILTER (WHERE upi_id_encrypted IS NOT NULL) as upi_setup,
        count(*) FILTER (WHERE stipend_verified = 1) as stipend_ver,
        count(*) FILTER (WHERE password_set = 1) as pwd_set
    FROM dbert_internship.intern_accounts;
""")
intent_row = c.fetchone()
print(f"Password Set: {intent_row[5]}")
print(f"Terms Accepted: {intent_row[1]}")
print(f"LinkedIn Profile Verified: {intent_row[0]}")
print(f"Gemini API Key Configured: {intent_row[2]}")
print(f"UPI ID Configured (for stipend/withdrawal): {intent_row[3]}")
print(f"Stipend Marked Verified: {intent_row[4]}")

# Task and project submissions
c.execute("SELECT count(*), count(DISTINCT intern_id) FROM dbert_internship.task_submissions;")
ts_cnt, ts_users = c.fetchone()
print(f"Task Submissions: {ts_cnt} from {ts_users} distinct interns")

c.execute("SELECT status, count(*) FROM dbert_internship.task_submissions GROUP BY status ORDER BY count(*) DESC;")
for r in c.fetchall():
    print(f"  Task Status '{r[0]}': {r[1]}")

c.execute("SELECT count(*), count(DISTINCT intern_id) FROM dbert_internship.project_submissions;")
ps_cnt, ps_users = c.fetchone()
print(f"Project Submissions: {ps_cnt} from {ps_users} distinct interns")

# Ambassador withdrawals (stipend intent)
c.execute("""
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_schema='dbert_internship' AND table_name='ambassador_withdrawals';
""")
aw_cols = [r[0] for r in c.fetchall()]
print(f"Ambassador Withdrawals Columns: {aw_cols}")

c.execute("SELECT count(*), count(DISTINCT intern_id) FROM dbert_internship.ambassador_withdrawals;")
aw_cnt, aw_users = c.fetchone()
print(f"Ambassador/Stipend Withdrawal Requests: {aw_cnt} from {aw_users} users")

# Post applications
c.execute("SELECT count(*), count(DISTINCT intern_id) FROM dbert_internship.post_applications;")
pa_cnt, pa_users = c.fetchone()
print(f"Job/Internship Post Applications: {pa_cnt} from {pa_users} interns")

print("\\n=================================================================")
print("=== 4. FINANCIAL LEDGER & PAYMENT STATUSES ===")
print("=================================================================")
# Security deposits table
c.execute("""
    SELECT amount, status, count(*) 
    FROM dbert_internship.security_deposits 
    GROUP BY amount, status 
    ORDER BY count(*) DESC;
""")
print("Security Deposits (Caution Deposits / Gateways):")
for r in c.fetchall():
    print(f"  Amount: ₹{r[0]} | Status: {r[1]:15s} | Count: {r[2]}")

# Enrollments table
c.execute("""
    SELECT payment_status, count(*), coalesce(sum(amount_paid),0), coalesce(sum(deposit_paid),0), coalesce(sum(balance_paid),0)
    FROM dbert_internship.enrollments 
    GROUP BY payment_status 
    ORDER BY count(*) DESC;
""")
print("\\nEnrollments Table Payments:")
for r in c.fetchall():
    print(f"  Payment Status: {r[0]:15s} | Count: {r[1]:4d} | Total Paid: ₹{r[2]} | Deposit: ₹{r[3]} | Balance: ₹{r[4]}")

# Certificates table
c.execute("""
    SELECT tier, count(*) 
    FROM dbert_internship.intern_certificates 
    GROUP BY tier 
    ORDER BY count(*) DESC;
""")
print("\\nCertificates in DB:")
for r in c.fetchall():
    print(f"  Tier '{r[0]}': {r[1]}")
'''

ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
