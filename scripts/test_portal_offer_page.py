import os
import sys
from dotenv import load_dotenv

portal_dir = "/var/www/dbert-website-lms/apps/portal"
if os.path.exists(portal_dir):
    os.chdir(portal_dir)
    sys.path.insert(0, portal_dir)
    load_dotenv(os.path.join(portal_dir, ".env"))

from app import app, create_session, AUTH_COOKIE

email = "stage3_selected@dbert.test"
token = create_session(email, "intern")

client = app.test_client()
client.set_cookie(AUTH_COOKIE, token)

resp = client.get("/portal/offer")
print("Status code:", resp.status_code)
html = resp.get_data(as_text=True)

for term in [
    'id="signedBanner"',
    'STEP 2 COMPLETED',
    'Signed by',
    'id="offerSignCard"',
    'id="postSignPaymentSection"',
    'STEP 3: COHORT SEAT CONFIRMATION'
]:
    pos = html.find(term)
    if pos != -1:
        print(f"Found '{term}' at {pos}: snippet: {html[pos:pos+150]!r}")
    else:
        print(f"NOT found: '{term}'")
