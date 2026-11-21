import os
import sys

portal_dir = "/var/www/dbert-website-lms/apps/portal"
if os.path.exists(portal_dir):
    sys.path.insert(0, portal_dir)
    os.chdir(portal_dir)

from app import app, create_session

token = create_session("stage3_selected@dbert.test", "intern")
client = app.test_client()
res = client.get("/portal/offer", headers={"X-Session-Token": token})
html = res.get_data(as_text=True)

for i, line in enumerate(html.splitlines(), 1):
    if "screenActionSteps" in line or "signedBanner" in line or "offerSignCard" in line or "postSignPaymentSection" in line or "Signed by" in line:
        print(f"Line {i}: {line}")
