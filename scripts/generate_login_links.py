import sys
import subprocess

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

script_content = """
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import _email_sig

emails = [
    ("Observed Candidate (ID 5624)", "abhinav.sharma@dbert.vom", "Stage 5: Confirmed (Grace Expired)"),
    ("Stage 1: Apply Pending", "stage1_apply@dbert.test", "Stage 1: Application Received"),
    ("Stage 2: Under Review", "stage2_review@dbert.test", "Stage 2: Fast-Track Available"),
    ("Stage 3: Selected", "stage3_selected@dbert.test", "Stage 3: Selection & Offer Letter Ready"),
    ("Stage 4: Deposit Paid", "stage4_pending@dbert.test", "Stage 4: Verification in Progress"),
    ("Stage 5: Confirmed (Day 4/7)", "stage5_enrolled@dbert.test", "Stage 5: Active Intern (7-Day Window)"),
    ("Stage 5: Confirmed (Overdue)", "stage5_grace_expired@dbert.test", "Stage 5: Active Intern (Balance Due)"),
    ("Stage 5: Fully Paid (₹1,999)", "fellow_paid_1999@dbert.test", "Stage 5: Confirmed Fellow · Verified"),
    ("Alumnus: Provisional Credential", "stipend_gate1_locked@dbert.test", "Provisional Alumnus (Gate 1 Locked)"),
    ("Alumnus: Verified & Stipend Ready", "stipend_ready@dbert.test", "Verified Alumnus (Ready to Submit Capstone)"),
    ("Alumnus: LMS Wallet Coins", "stipend_wallet@dbert.test", "Alumnus (5,000 Coins in Referral Wallet)"),
]

for label, email, desc in emails:
    token = _email_sig('activate', email)
    url_portal = f"https://lms.dbert.in/auth/activate?e={email}&t={token}&next=/portal"
    url_offer = f"https://lms.dbert.in/auth/activate?e={email}&t={token}&next=/portal/offer"
    url_stipend = f"https://lms.dbert.in/auth/activate?e={email}&t={token}&next=/stipend/tasks"
    print(f"LABEL: {label}")
    print(f"EMAIL: {email}")
    print(f"DESCRIPTION: {desc}")
    print(f"PORTAL_LINK: {url_portal}")
    print(f"OFFER_LINK: {url_offer}")
    print(f"STIPEND_LINK: {url_stipend}")
    print("---")
"""

with open("temp_gen.py", "w") as f:
    f.write(script_content)

scp_cmd = ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", "temp_gen.py", f"{HOST}:/tmp/temp_gen.py"]
subprocess.run(scp_cmd, check=True)

run_cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3 /tmp/temp_gen.py"]
res = subprocess.run(run_cmd, capture_output=True, text=True)
print(res.stdout)
