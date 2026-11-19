"""
Unit tests for Offer Letter Staged Flow and Academic Profile Option B Navigation.
"""
import unittest
import os
import sys

# Ensure portal root is on sys.path
PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)

if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = ""
os.environ["SECRET_KEY"] = "test-secret-key-12345"

from app import app
from flask import render_template


class TestOfferLetterStagedFlow(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()

    def test_unsigned_offer_letter_renders_signature_form_and_hides_payment(self):
        """Phase 1: Unsigned offer must hide payment and not show 'None on None' in signed banner."""
        with self.app.test_request_context("/portal/offer"):
            html = render_template(
                "portal_offer_letter.html",
                candidate={
                    "name": "Chirag Gupta",
                    "email": "chirag.test@dbert.test",
                    "domain": "Data Analytics",
                    "intern_id": 110
                },
                offer={
                    "offer_letter_id": "DBERT-OFR-2026-DA-0110",
                    "name": "Chirag Gupta",
                    "email": "chirag.test@dbert.test",
                    "domain": "Data Analytics",
                    "date_of_issue": "2026-11-19",
                    "batch_start_date": "2026-11-09",
                    "batch_end_date": "2027-01-08",
                    "tenure_months": 2,
                    "stipend_amount": 5000,
                    "login_hours_per_week": 10,
                    "required_certifications": 2,
                    "required_bounty_tasks": 75,
                    "caution_deposit_amount": 499,
                    "caution_deposit_status": "PENDING",
                    "signature_name": None,
                    "accepted_at": None,
                    "pdf_unlocked": 0
                },
                is_signed=False,
                is_deposit_verified=False,
                locked=False,
                preview_mode=True,
                enrollment=None,
                user={"email": "chirag.test@dbert.test", "role": "intern"},
                active_page="offer"
            )

            # Must render Step 2 Digital Signature form
            self.assertIn('id="offerSignCard"', html)
            self.assertIn("Full Legal Name (Digital Signature)", html)
            self.assertIn("Sign &amp; Accept Appointment Agreement", html)

            # Must NOT display Signed by None on None
            self.assertNotIn("Signed by None on None", html)
            self.assertNotIn("None &bull; Recorded", html)

            # Signed banner and payment section must NOT be in the HTML at all when unsigned
            self.assertNotIn('id="signedBanner"', html)
            self.assertNotIn('id="postSignPaymentSection"', html)

            # Stepper Step 3 must be locked/pending
            self.assertIn("Pending Signature", html)

            # Screen 1 (Review) must be active and Screen 2 (Action) hidden for unsigned candidate
            self.assertIn('id="screenOfferReview" class="offer-screen-view" style="display:block;', html)
            self.assertIn('id="screenActionSteps" class="offer-screen-view" style="display:none;', html)
            self.assertIn('id="btnAcceptAndSignBottom"', html)
            self.assertIn("Accept &amp; Sign Offer Letter", html)

    def test_signed_offer_letter_reveals_payment_and_enhancements(self):
        """Phase 2: Signed offer reveals signed banner, compact QR, Copy UPI ID, and high-contrast buttons."""
        with self.app.test_request_context("/portal/offer"):
            html = render_template(
                "portal_offer_letter.html",
                candidate={
                    "name": "Chirag Gupta",
                    "email": "chirag.test@dbert.test",
                    "domain": "Data Analytics",
                    "intern_id": 110
                },
                offer={
                    "offer_letter_id": "DBERT-OFR-2026-DA-0110",
                    "name": "Chirag Gupta",
                    "email": "chirag.test@dbert.test",
                    "domain": "Data Analytics",
                    "date_of_issue": "2026-11-19",
                    "batch_start_date": "2026-11-09",
                    "batch_end_date": "2027-01-08",
                    "tenure_months": 2,
                    "stipend_amount": 5000,
                    "login_hours_per_week": 10,
                    "required_certifications": 2,
                    "required_bounty_tasks": 75,
                    "caution_deposit_amount": 499,
                    "caution_deposit_status": "PENDING",
                    "signature_name": "Chirag Gupta",
                    "accepted_at": "19 Nov 2026, 03:30 PM IST",
                    "pdf_unlocked": 0
                },
                is_signed=True,
                is_deposit_verified=False,
                locked=False,
                preview_mode=True,
                enrollment=None,
                user={"email": "chirag.test@dbert.test", "role": "intern"},
                active_page="offer"
            )

            # Signature form must NOT be rendered
            self.assertNotIn('id="offerSignCard"', html)

            # Signed banner must be displayed with real signature name and date
            self.assertIn('id="signedBanner" style="display:flex;', html)
            self.assertIn("Chirag Gupta", html)
            self.assertIn("19 Nov 2026, 03:30 PM IST", html)

            # Payment section must be active
            self.assertIn('id="postSignPaymentSection" style="display:block;', html)

            # Compact QR code (130px)
            self.assertIn('width:130px; height:130px;', html)

            # Download QR button
            self.assertIn('id="btnDownloadOfferQr"', html)
            self.assertIn("Download QR", html)

            # Copy UPI ID button & VPA
            self.assertIn('id="copyVpaBtn"', html)
            self.assertIn("Q652429146@ybl", html)
            self.assertIn("copyUpiVpa", html)

            # High-contrast 1-Tap UPI Launchers matching /enroll/1999 standard
            self.assertIn("GPay", html)
            self.assertIn("PhonePe", html)
            self.assertIn("Paytm", html)
            self.assertIn("Any UPI", html)
            self.assertIn("background:#1A73E8", html)  # GPay Google Blue
            self.assertIn("background:#5F259F", html)  # PhonePe purple
            self.assertIn("background:#00BAF2", html)  # Paytm cyan (distinct from dark card)
            self.assertIn("background:#10B981", html)  # Any UPI emerald green

            # Screen 2 (Action) must be active and Screen 1 (Review) hidden for signed candidate
            self.assertIn('id="screenActionSteps" class="offer-screen-view" style="display:block;', html)
            self.assertIn('id="screenOfferReview" class="offer-screen-view" style="display:none;', html)
            self.assertIn("Review Appointment Letter", html)

    def test_csp_compliance_no_inline_click_handlers(self):
        """Enforce CSP compliance: Zero inline onclick or javascript: links; all attached in script."""
        with self.app.test_request_context("/portal/offer"):
            html = render_template(
                "portal_offer_letter.html",
                candidate={"name": "Chirag Gupta", "email": "chirag.test@dbert.test", "domain": "Data Analytics", "intern_id": 110},
                offer={
                    "offer_letter_id": "DBERT-OFR-2026-DA-0110",
                    "name": "Chirag Gupta",
                    "email": "chirag.test@dbert.test",
                    "domain": "Data Analytics",
                    "caution_deposit_status": "PENDING",
                    "signature_name": None,
                    "accepted_at": None,
                },
                is_signed=False,
                is_deposit_verified=False,
                locked=False,
                preview_mode=True,
                enrollment=None,
                user={"email": "chirag.test@dbert.test", "role": "intern"},
                active_page="offer"
            )

            # Strict CSP assertions: No inline onclick or javascript: pseudo-protocol
            self.assertNotIn("onclick=", html)
            self.assertNotIn("javascript:", html)

            # Assert programmatic event listener registrations in nonce script
            self.assertIn("btnReviewSignTop.addEventListener('click'", html)
            self.assertIn("btnAcceptAndSignBottom.addEventListener('click'", html)
            self.assertIn("btnBackToReview.addEventListener('click'", html)
            self.assertIn("copyBtn.addEventListener('click'", html)
            self.assertIn("step1.addEventListener('click'", html)
            self.assertIn("step2.addEventListener('click'", html)
            self.assertIn("step3.addEventListener('click'", html)

    def test_profile_redirects_to_portal_editprofile(self):
        """Option B: /profile route redirects to /portal?tab=editprofile."""
        res = self.client.get("/profile")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/portal?tab=editprofile", res.headers.get("Location", ""))


if __name__ == "__main__":
    unittest.main()
