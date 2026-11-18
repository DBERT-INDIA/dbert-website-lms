import os
import sys
import unittest

# Add apps/portal to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps", "portal"))

from app import app, get_db, get_intern_flow_state, build_intern_next_action

class TestStageSynchronization(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

    def test_build_intern_next_action_stages(self):
        # Stage 1
        na1 = build_intern_next_action({"stage_num": 1, "domain": "Data Analyst"})
        self.assertEqual(na1["stage_badge"], "Stage 1: Under Evaluation")
        self.assertIn("Admissions Committee", na1["description"])

        # Stage 2
        na2 = build_intern_next_action({"stage_num": 2, "domain": "Full Stack Development"})
        self.assertEqual(na2["stage_badge"], "Stage 2: Fast-Track Available")
        self.assertIn("Fast-Track Incubation Review", na2["heading"])
        self.assertIn("499", na2["description"])
        self.assertEqual(na2["primary_cta_url"], "/portal/offer")

        # Stage 3
        na3 = build_intern_next_action({"stage_num": 3, "domain": "AI Agent Development"})
        self.assertEqual(na3["stage_badge"], "Stage 3: Selection & Appointment")
        self.assertIn("Seat Confirmation Required", na3["heading"])
        self.assertEqual(na3["primary_cta_url"], "/portal/offer")

        # Stage 4
        na4 = build_intern_next_action({"stage_num": 4, "domain": "Cybersecurity"})
        self.assertEqual(na4["stage_badge"], "Stage 4: Verification in Progress")
        self.assertIn("Administrative Verification", na4["heading"])

        # Stage 5 - within 7-day grace period
        na5_grace = build_intern_next_action({
            "stage_num": 5, "domain": "Python Automation",
            "has_paid_balance": False, "days_since_joining": 2
        })
        self.assertIn("Day 3 of 7-Day Window", na5_grace["stage_badge"])
        self.assertIn("5 Days Remaining", na5_grace["heading"])
        self.assertEqual(na5_grace["primary_cta_url"], "/courses")

        # Stage 5 - grace expired (> 7 days)
        na5_exp = build_intern_next_action({
            "stage_num": 5, "domain": "Python Automation",
            "has_paid_balance": False, "days_since_joining": 10
        })
        self.assertIn("Balance Completion Required", na5_exp["stage_badge"])
        self.assertEqual(na5_exp["primary_cta_url"], "https://dbert.in/enroll/1999")

        # Stage 5 - fully verified (balance paid)
        na5_paid = build_intern_next_action({
            "stage_num": 5, "domain": "Python Automation",
            "has_paid_balance": True
        })
        self.assertEqual(na5_paid["stage_badge"], "Stage 5: Confirmed Fellow · Verified")
        self.assertIn("Active Engineering Incubation Fellow", na5_paid["heading"])

    def test_offer_letter_template_exclusivity(self):
        """Verify that when is_deposit_verified is True, postSignPaymentSection and QR are absent."""
        with self.app.test_request_context():
            from flask import render_template
            dummy_offer = {
                "id": 999,
                "offer_letter_id": "DBERT-OFR-TEST-001",
                "name": "Test Candidate",
                "email": "test@dbert.test",
                "domain": "Cybersecurity",
                "batch_start_date": "2026-11-09",
                "accepted_at": "18 Nov 2026, 05:00 PM IST",
                "signature_name": "Test Candidate",
                "caution_deposit_status": "VERIFIED",
                "pdf_unlocked": 1
            }
            # Render with verified deposit
            html_verified = render_template(
                "portal_offer_letter.html",
                locked=False,
                preview_mode=False,
                is_signed=True,
                is_deposit_verified=True,
                offer=dummy_offer,
                enrollment={"deposit_paid": 1, "payment_status": "Verified"},
                user={"email": "test@dbert.test", "role": "intern"},
                active_page="offer"
            )
            self.assertIn("verifiedDossierCard", html_verified)
            self.assertIn("Download Official Signed PDF", html_verified)
            # Must NOT contain payment form or QR text in DOM
            self.assertNotIn('id="postSignPaymentSection"', html_verified)
            self.assertNotIn("STEP 3: COHORT SEAT CONFIRMATION", html_verified)
            self.assertNotIn("Scan & Pay ₹499", html_verified)
            self.assertNotIn('<form id="depositSubmitForm"', html_verified)

            # Render with unverified deposit
            html_unverified = render_template(
                "portal_offer_letter.html",
                locked=False,
                preview_mode=True,
                is_signed=True,
                is_deposit_verified=False,
                offer=dummy_offer,
                enrollment=None,
                user={"email": "test@dbert.test", "role": "intern"},
                active_page="offer"
            )
            self.assertNotIn("verifiedDossierCard", html_unverified)
            self.assertIn('id="postSignPaymentSection"', html_unverified)
            self.assertIn("STEP 3: COHORT SEAT CONFIRMATION", html_unverified)

    def test_portal_template_stage_synchronization(self):
        """Verify that portal.html renders exact stage next_action without Stage 1 fallback."""
        with self.app.test_request_context():
            from flask import render_template
            na5 = build_intern_next_action({
                "stage_num": 5, "domain": "Cybersecurity",
                "has_paid_balance": False, "days_since_joining": 2
            })
            html = render_template(
                "portal.html",
                active_page="dashboard",
                needs_academic_profile=False,
                flow_state={"stage_num": 5, "stage": "CONFIRMED"},
                current_stage=5,
                next_action=na5
            )
            # Next action card must display Stage 5 badge and heading
            self.assertIn("Stage 5: Active Intern", html)
            self.assertIn("Sprint Workspace Active", html)
            # Must NOT display fallback Stage 1 Under Evaluation
            self.assertNotIn("Stage 1: Under Evaluation", html)
            self.assertNotIn("Application Under Evaluation", html)
            # Academic profile banner must be hidden (display:none)
            self.assertIn('id="academicProfileBanner" class="academic-profile-banner" style="display:none;', html)
            # nextStepCard must have hidden class
            self.assertIn('class="nextstep-card hidden" id="nextStepCard"', html)

if __name__ == "__main__":
    unittest.main()
