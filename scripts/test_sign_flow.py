import os
import sys
import re
from dotenv import load_dotenv

portal_dir = "/var/www/dbert-website-lms/apps/portal"
if os.path.exists(portal_dir):
    os.chdir(portal_dir)
    sys.path.insert(0, portal_dir)
    load_dotenv(os.path.join(portal_dir, ".env"))

from app import app, create_session, AUTH_COOKIE
from services.database.adapter import get_db_adapter

email = "stage3_selected@dbert.test"
token = create_session(email, "intern")

client = app.test_client()
client.set_cookie(AUTH_COOKIE, token)

# GET offer page to initialize session and mint CSRF
resp_before = client.get("/portal/offer")
html_before = resp_before.get_data(as_text=True)
print("Before sign - has offerSignCard:", 'id="offerSignCard"' in html_before)
print("Before sign - has signedBanner:", 'id="signedBanner"' in html_before)
print("Before sign - has postSignPaymentSection:", 'id="postSignPaymentSection"' in html_before)

# Extract CSRF token from rendered HTML
m = re.search(r"'X-CSRF-Token':\s*'([^']+)'", html_before)
csrf_token_val = m.group(1) if m else None
print("Extracted CSRF token from HTML:", csrf_token_val)

# Simulate signing via AJAX POST
resp_sign = client.post(
    "/portal/offer/sign",
    headers={"X-CSRF-Token": csrf_token_val, "X-Requested-With": "XMLHttpRequest"},
    json={"signature_name": "Chirag Gupta", "agreed": True, "csrf_token": csrf_token_val}
)
print("Sign response status:", resp_sign.status_code, resp_sign.get_json())

# Check state after sign (which is what page reload produces)
resp_after = client.get("/portal/offer")
html_after = resp_after.get_data(as_text=True)
print("After sign - has offerSignCard:", 'id="offerSignCard"' in html_after)
print("After sign - has signedBanner:", 'id="signedBanner"' in html_after)
print("After sign - has postSignPaymentSection:", 'id="postSignPaymentSection"' in html_after)
print("After sign - has Chirag Gupta in signed banner:", "Signed by <strong style=\"color:#0f172a;\" id=\"signedNameDisplay\">Chirag Gupta</strong>" in html_after)
print("After sign - has 1-Tap UPI buttons (GPay, PhonePe, Paytm, Any UPI):",
      "GPay" in html_after and "PhonePe" in html_after and "Paytm" in html_after and "Any UPI" in html_after)

# Reset Chirag Gupta to unsigned state so user can test live!
with get_db_adapter() as conn:
    conn.execute(
        "UPDATE intern_offer_letters SET signature_name = NULL, accepted_at = NULL, pdf_unlocked = 0 WHERE LOWER(email) = ?",
        (email,)
    )
    if hasattr(conn, "commit"):
        conn.commit()
print("Reset Chirag Gupta back to unsigned state for user live testing: DONE.")
