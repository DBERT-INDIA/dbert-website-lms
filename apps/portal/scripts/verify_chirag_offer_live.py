import os
import sys

# Change to portal directory
portal_dir = "/var/www/dbert-website-lms/apps/portal"
if os.path.exists(portal_dir):
    sys.path.insert(0, portal_dir)
    os.chdir(portal_dir)

from app import app, create_session

token = create_session("stage3_selected@dbert.test", "intern")
client = app.test_client()
res = client.get("/portal/offer", headers={"X-Session-Token": token})

html = res.get_data(as_text=True)

print("=== CHIRAG GUPTA OFFER LETTER VERIFICATION ===")
print("HTTP Status:", res.status_code)
print("Screen 1 (#screenOfferReview) display:block:", 'id="screenOfferReview" class="offer-screen-view" style="display:block;' in html)
print("Screen 2 (#screenActionSteps) display:none:", 'id="screenActionSteps" class="offer-screen-view" style="display:none;' in html)
print("Signed Banner (#signedBanner) display:none:", 'id="signedBanner" style="display:none;' in html)
print("Payment Section (#postSignPaymentSection) display:none:", 'id="postSignPaymentSection" style="display:none;' in html)
print("Signature Card (#offerSignCard) rendered:", 'id="offerSignCard"' in html)
print("Top Button (#btnReviewSignTop) rendered as button:", '<button type="button" class="btn-emerald btn-gold-pulse" id="btnReviewSignTop"' in html)
print("Bottom Button (#btnAcceptAndSignBottom) rendered as button:", '<button type="button" id="btnAcceptAndSignBottom"' in html)
print("Back Button (#btnBackToReview) rendered:", 'id="btnBackToReview"' in html)
print("Inline onclick count:", html.count("onclick="))
print("Inline javascript: count:", html.count("javascript:"))
print("QR Code 115px rendered:", "width:115px; height:115px;" in html)
print("Download QR button rendered:", 'id="btnDownloadOfferQr"' in html)
print("Copy VPA button rendered:", 'id="copyVpaBtn"' in html)
print("Paytm Electric Cyan (#00baf2) rendered:", "background:#00baf2" in html)
print("CSP event listeners attached in script:", "btnReviewSignTop.addEventListener('click'" in html)
print("================================================")
