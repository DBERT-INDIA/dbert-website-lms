import subprocess
import sys

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

check_code = """
import requests

# Test candidate 5624 (abhinav.sharma@dbert.vom)
from services.database.adapter import get_db_adapter
conn = get_db_adapter()
acct = conn.execute("SELECT * FROM intern_accounts WHERE email='abhinav.sharma@dbert.vom'").fetchone()
print(f"Candidate 5624: id={acct['id']}, email={acct['email']}, name={acct['name']}, domain={acct['domain']}, college={acct['college']}")

from app import get_intern_flow_state, build_intern_next_action
flow = get_intern_flow_state(conn, 'abhinav.sharma@dbert.vom')
print(f"Flow state: stage_num={flow['stage_num']}, stage={flow['stage']}, label={flow['label']}, domain={flow['domain']}")
na = build_intern_next_action(flow)
print(f"Next action: stage_badge='{na['stage_badge']}', heading='{na['heading']}'")

# Test live HTTP rendering via local test client or session
from app import app
client = app.test_client()

# Create intern session
with client.session_transaction() as sess:
    sess['user_id'] = acct['id']
    sess['email'] = acct['email']
    sess['role'] = 'intern'
    sess['name'] = acct['name']

res_portal = client.get('/portal')
portal_html = res_portal.get_data(as_text=True)

print(f"Portal HTTP status: {res_portal.status_code}")
has_stage5 = "Stage 5: " in portal_html or "Active Engineering Incubation Fellow" in portal_html or "Sprint Workspace Active" in portal_html
has_stage1 = "Stage 1: Under Evaluation" in portal_html
has_complete_profile = "Complete Your Academic Profile" in portal_html and 'style="display:none;' not in portal_html
has_ghost_nextstep = 'class="nextstep-card"' in portal_html and 'hidden' not in portal_html

print(f"Portal checks:")
print(f"  - Has Stage 5 active mission card: {has_stage5}")
print(f"  - Has Stage 1 fallback: {has_stage1} (Must be False)")
print(f"  - Has visible Complete Profile banner: {has_complete_profile} (Must be False)")
print(f"  - Has unhidden ghost nextStepCard: {has_ghost_nextstep} (Must be False)")

res_offer = client.get('/portal/offer')
offer_html = res_offer.get_data(as_text=True)
print(f"Offer HTTP status: {res_offer.status_code}")
has_verified_dossier = "verifiedDossierCard" in offer_html
has_download_pdf = "Download Official Signed PDF" in offer_html
has_step3_payment = 'id="postSignPaymentSection"' in offer_html
has_step3_qr = "Scan & Pay ₹499" in offer_html

print(f"Offer checks:")
print(f"  - Has verified dossier: {has_verified_dossier} (Must be True)")
print(f"  - Has download signed PDF: {has_download_pdf} (Must be True)")
print(f"  - Has Step 3 payment form in DOM: {has_step3_payment} (Must be False)")
print(f"  - Has Step 3 QR code in DOM: {has_step3_qr} (Must be False)")

# Test /intern/me JSON
res_me = client.get('/intern/me')
me_json = res_me.get_json()
print(f"/intern/me next_action stage_badge: {me_json.get('next_action', {}).get('stage_badge')}")
print(f"/intern/me flow_state stage_num: {me_json.get('flow_state', {}).get('stage_num')}")
print(f"/intern/me intern needs_academic_profile: {me_json.get('intern', {}).get('needs_academic_profile')}")
"""

cmd = [
    "ssh",
    "-i", SSH_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    HOST,
    f"cd /var/www/dbert-website-lms/apps/portal && /var/www/dbert-website-lms/apps/portal/.venv/bin/python3 -c \"{check_code}\""
]

res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
