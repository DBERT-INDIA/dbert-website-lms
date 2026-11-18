import os
import sys
import unittest
from pathlib import Path

# Add portal root to sys.path
PORTAL_DIR = Path(__file__).resolve().parent.parent
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = ""

from app import app, get_db, create_session, get_or_create_offer_letter


class TestOfferLetterPortal(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        # Seed test candidates
        with get_db() as conn:
            # Clean previous test artifacts
            conn.execute("DELETE FROM intern_offer_letters WHERE email LIKE '%@testoffer.dbert.in'")
            conn.execute("DELETE FROM enrollments WHERE email LIKE '%@testoffer.dbert.in'")
            conn.execute("DELETE FROM intern_accounts WHERE email LIKE '%@testoffer.dbert.in'")
            conn.execute("DELETE FROM user_sessions WHERE email LIKE '%@testoffer.dbert.in'")

            # 1. Verified candidate (paid ₹499)
            conn.execute("""
                INSERT INTO enrollments (id, name, email, phone, college, domain, joining_date, payment_status, amount)
                VALUES (8801, 'Aayush Sharma', 'aayush.verified@testoffer.dbert.in', '9876543210', 'IIT Delhi', 'Data Analytics', '2026-11-09', 'Verified', 499)
            """)
            conn.execute("""
                INSERT INTO intern_accounts (id, name, email, domain, is_active)
                VALUES (8801, 'Aayush Sharma', 'aayush.verified@testoffer.dbert.in', 'Data Analytics', 1)
            """)

            # 2. Selected candidate (deposit pending verification)
            conn.execute("""
                INSERT INTO enrollments (id, name, email, phone, college, domain, joining_date, payment_status, amount)
                VALUES (8802, 'Rohan Verma', 'rohan.pending@testoffer.dbert.in', '9876543211', 'BITS Pilani', 'Python Automation', '2026-11-09', 'Pending Verification', 0)
            """)
            conn.execute("""
                INSERT INTO intern_accounts (id, name, email, domain, is_active)
                VALUES (8802, 'Rohan Verma', 'rohan.pending@testoffer.dbert.in', 'Python Automation', 1)
            """)

            # 3. Candidate under review (not yet selected, locked offer)
            conn.execute("""
                INSERT INTO applications (id, name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status)
                VALUES (8803, 'Priya Nair', 'priya.review@testoffer.dbert.in', '9876543212', 'New Delhi', 'Delhi University', 'B.Tech', '6', '2027', 'AI & Machine Learning', 'Interested in AI incubation', 'Under Review')
            """)
            conn.execute("""
                INSERT INTO intern_accounts (id, name, email, domain, is_active)
                VALUES (8803, 'Priya Nair', 'priya.review@testoffer.dbert.in', 'AI & Machine Learning', 1)
            """)
            conn.commit()

    def tearDown(self):
        with get_db() as conn:
            conn.execute("DELETE FROM intern_offer_letters WHERE email LIKE '%@testoffer.dbert.in'")
            conn.execute("DELETE FROM enrollments WHERE email LIKE '%@testoffer.dbert.in'")
            conn.execute("DELETE FROM applications WHERE email LIKE '%@testoffer.dbert.in'")
            conn.execute("DELETE FROM intern_accounts WHERE email LIKE '%@testoffer.dbert.in'")
            conn.execute("DELETE FROM user_sessions WHERE email LIKE '%@testoffer.dbert.in'")
            conn.commit()

    def test_unauthenticated_redirect(self):
        """Unauthenticated requests to /portal/offer must redirect to sign-in."""
        res = self.client.get("/portal/offer")
        self.assertEqual(res.status_code, 302)
        self.assertIn("#signin", res.headers.get("Location", ""))

    def test_unselected_candidate_sees_locked_view(self):
        """Candidate in Under Review stage sees locked gate."""
        token = create_session("priya.review@testoffer.dbert.in", "intern")
        res = self.client.get("/portal/offer", headers={"X-Session-Token": token})
        self.assertEqual(res.status_code, 200)
        content = res.get_data(as_text=True)
        self.assertIn("Official Offer Letter Gated", content)

    def test_selected_unverified_candidate_signs_first_and_pdf_remains_deposit_gated(self):
        """Selected candidate can review and digitally sign offer first; PDF download is gated until deposit is verified."""
        token = create_session("rohan.pending@testoffer.dbert.in", "intern")
        res = self.client.get("/portal/offer", headers={"X-Session-Token": token})
        self.assertEqual(res.status_code, 200)
        content = res.get_data(as_text=True)
        self.assertIn("Appointment Terms Preview", content)
        self.assertIn("PREVIEW ONLY", content)

        # Signing succeeds immediately in Read & Sign First model
        res_sign = self.client.post(
            "/portal/offer/sign",
            json={"signature_name": "Rohan Verma", "agreed": True},
            headers={"X-Session-Token": token}
        )
        self.assertEqual(res_sign.status_code, 200)
        data = res_sign.get_json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["requires_deposit"])

        # Attempting to access official signed PDF print view redirects until deposit is verified
        res_print = self.client.get("/portal/offer/print", headers={"X-Session-Token": token})
        self.assertEqual(res_print.status_code, 302)

    def test_verified_candidate_accesses_offer_and_generates_id(self):
        """Verified candidate accesses /portal/offer and gets deterministic Offer ID."""
        token = create_session("aayush.verified@testoffer.dbert.in", "intern")
        res = self.client.get("/portal/offer", headers={"X-Session-Token": token})
        self.assertEqual(res.status_code, 200)
        content = res.get_data(as_text=True)

        self.assertIn("DBERT-OFR-2026-DA-8801", content)
        self.assertIn("Aayush Sharma", content)
        self.assertIn("Two (2) Months", content)
        self.assertIn("5,000", content)
        self.assertIn("10 hours per week", content)
        self.assertIn("75 bounty tasks", content)
        self.assertIn("two (2) verified course certifications", content)
        self.assertIn("Abhinav Sharma", content)

    def test_digital_signature_execution_and_pdf_unlock(self):
        """Candidate submits digital signature, updates DB, and unlocks PDF printing."""
        token = create_session("aayush.verified@testoffer.dbert.in", "intern")

        # 1. Sign offer letter
        res = self.client.post(
            "/portal/offer/sign",
            json={
                "signature_name": "Aayush Sharma",
                "agreed": True
            },
            headers={"X-Session-Token": token}
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["signature_name"], "Aayush Sharma")
        self.assertIn("accepted_at", data)

        # 2. Verify record in database
        with get_db() as conn:
            row = conn.execute(
                "SELECT * FROM intern_offer_letters WHERE email='aayush.verified@testoffer.dbert.in'"
            ).fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row["signature_name"], "Aayush Sharma")
            self.assertEqual(row["pdf_unlocked"], 1)

        # 3. Verify /portal/offer displays accepted state
        res_view = self.client.get("/portal/offer", headers={"X-Session-Token": token})
        self.assertEqual(res_view.status_code, 200)
        view_content = res_view.get_data(as_text=True)
        self.assertIn("STATUS: ACCEPTED", view_content)
        self.assertIn("Download Official Signed PDF", view_content)

        # 4. Verify /portal/offer/print returns printable view
        res_print = self.client.get("/portal/offer/print", headers={"X-Session-Token": token})
        self.assertEqual(res_print.status_code, 200)
        print_content = res_print.get_data(as_text=True)
        self.assertIn("Executive Print View", print_content)
        self.assertIn("Aayush Sharma", print_content)


if __name__ == "__main__":
    unittest.main()
