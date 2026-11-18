import sys
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

import requests
from services.database.adapter import get_db_adapter
from app import app, get_intern_flow_state, build_intern_next_action, create_session

conn = get_db_adapter()
acct = conn.execute("SELECT * FROM intern_accounts WHERE email='abhinav.sharma@dbert.vom'").fetchone()
print(f"Candidate 5624: id={acct['id']}, email={acct['email']}, name={acct['name']}, domain={acct['domain']}, college={acct['college']}")

flow = get_intern_flow_state(conn, 'abhinav.sharma@dbert.vom')
print(f"Flow state: stage_num={flow['stage_num']}, stage={flow['stage']}, label={flow['label']}, domain={flow['domain']}")
na = build_intern_next_action(flow)
print(f"Next action: stage_badge='{na['stage_badge']}', heading='{na['heading']}'")

app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False

client = app.test_client()

# Create authenticated session token
token = create_session('abhinav.sharma@dbert.vom', 'intern')
headers = {'X-Session-Token': token}

res_portal = client.get('/portal', headers=headers)
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

res_offer = client.get('/portal/offer', headers=headers)
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

print("Stage 5 accounts in DB:", conn.execute("SELECT id, email FROM intern_accounts WHERE email LIKE '%stage5%'").fetchall())

# Test other stages
for test_email, expected_stage in [
    ('stage1_apply@dbert.test', 1),
    ('stage2_review@dbert.test', 2),
    ('stage3_selected@dbert.test', 3),
    ('stage4_pending@dbert.test', 4),
    ('stage5_enrolled@dbert.test', 5),
    ('stage5_grace_expired@dbert.test', 5),
]:
    t = create_session(test_email, 'intern')
    h = {'X-Session-Token': t}
    r = client.get('/portal', headers=h)
    r_me = client.get('/intern/me', headers=h)
    me = r_me.get_json() or {}
    st_num = me.get('flow_state', {}).get('stage_num') if me.get('flow_state') else None
    badge = me.get('next_action', {}).get('stage_badge') if me.get('next_action') else None
    print(f"Persona {test_email}: Portal HTTP {r.status_code}, Me HTTP {r_me.status_code}, Stage={st_num} (Expected {expected_stage}), Badge='{badge}', Error={me.get('message')}")
