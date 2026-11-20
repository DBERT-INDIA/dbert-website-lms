"""
test_admin_enrollment_review_flow.py
Comprehensive test suite verifying the Admin Enrollment Payment Review Pipeline:
- Unauthenticated access prevention (401)
- Validation of payload inputs (400)
- End-to-end Accept payment workflow:
    * enrollments.payment_status -> 'Accepted'
    * applications.status -> 'Accepted'
    * intern_offer_letters.caution_deposit_status -> 'VERIFIED', pdf_unlocked = 1
    * intern_accounts.is_active = 1
- End-to-end Reject payment workflow:
    * enrollments.payment_status -> 'Rejected', admin_note recorded
    * applications.status -> 'Enrollment Pending'
    * intern_offer_letters.caution_deposit_status -> 'REJECTED'
- Frontend admin.html template compliance:
    * viewScreenshot passes enrollment ID: [r.id, ...]
    * Modal buttons have IDs btnEnrAccept and btnEnrReject
    * Delegated data-act-click="reviewEnrollment" binding
    * apiFetch includes X-CSRF-Token header
"""
import os
import sys
import unittest
from unittest.mock import patch

PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)

if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = ""
os.environ["SECRET_KEY"] = "test-admin-review-secret-key-98765"

from app import app, get_db, create_session, AUTH_COOKIE, STATUS_ACCEPTED, STATUS_ENROLLMENT_PENDING


class TestAdminEnrollmentReviewFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SESSION_COOKIE_DOMAIN"] = None
        app.config["SESSION_COOKIE_SECURE"] = False

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["SESSION_COOKIE_DOMAIN"] = None
        self.app.config["SESSION_COOKIE_SECURE"] = False
        self.client = app.test_client()

        # Create or verify admin user session
        self.admin_email = "admin_test_review@dbert.test"
        with get_db() as conn:
            # Create test intern records
            self.test_email = "review_candidate@dbert.test"
            self.test_domain = "Data Analytics"

            # Clean previous test records
            conn.execute("DELETE FROM enrollments WHERE LOWER(email)=?", (self.test_email.lower(),))
            conn.execute("DELETE FROM applications WHERE LOWER(email)=?", (self.test_email.lower(),))
            conn.execute("DELETE FROM intern_offer_letters WHERE LOWER(email)=?", (self.test_email.lower(),))
            conn.execute("DELETE FROM intern_accounts WHERE LOWER(email)=?", (self.test_email.lower(),))

            # Insert application
            conn.execute("""
                INSERT INTO applications (
                    name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at, updated_at
                ) VALUES (
                    'Review Candidate', ?, '9876543210', 'Delhi', 'IIT', 'BTech', '6', '2026', ?, 'Learning', 'Enrolled', '2026-11-20 10:00:00', '2026-11-20 10:00:00'
                )
            """, (self.test_email, self.test_domain))

            # Insert intern_offer_letters
            conn.execute("""
                INSERT INTO intern_offer_letters (
                    email, name, domain, offer_letter_id, batch_start_date, batch_end_date,
                    caution_deposit_status, pdf_unlocked, created_at, updated_at
                ) VALUES (
                    ?, 'Review Candidate', ?, 'DBERT-OFR-TEST-001', '2026-11-20', '2027-01-20',
                    'SUBMITTED', 0, '2026-11-20 10:00:00', '2026-11-20 10:00:00'
                )
            """, (self.test_email, self.test_domain))

            # Insert intern_account
            conn.execute("""
                INSERT INTO intern_accounts (name, email, domain, is_active, created_at, updated_at)
                VALUES ('Review Candidate', ?, ?, 0, '2026-11-20 10:00:00', '2026-11-20 10:00:00')
            """, (self.test_email, self.test_domain))

            # Insert enrollment
            conn.execute("""
                INSERT INTO enrollments (
                    name, email, domain, product, payment_status, utr, payment_screenshot, created_at, updated_at
                ) VALUES (
                    'Review Candidate', ?, ?, 'free_deposit', 'Pending Verification', '667064018232', 'utr_667064018232.receipt', '2026-11-20 10:00:00', '2026-11-20 10:00:00'
                )
            """, (self.test_email, self.test_domain))

            enr_row = conn.execute("SELECT id FROM enrollments WHERE LOWER(email)=?", (self.test_email.lower(),)).fetchone()
            self.test_enr_id = enr_row["id"]
            conn.commit()

        # Admin session token
        self.admin_token = create_session(self.admin_email, "admin")

    def test_unauthorized_review_returns_401(self):
        """Unauthenticated caller receives 401 Unauthorized."""
        res = self.client.post("/admin/enrollment/review", json={
            "enrollment_id": self.test_enr_id,
            "action": "accept"
        })
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertEqual(data.get("status"), "error")

    def test_invalid_payload_returns_400(self):
        """Missing action or enrollment_id returns 400 Bad Request."""
        self.client.set_cookie(AUTH_COOKIE, self.admin_token)
        res = self.client.post("/admin/enrollment/review", json={
            "enrollment_id": self.test_enr_id
            # missing action
        })
        self.assertEqual(res.status_code, 400)

        res2 = self.client.post("/admin/enrollment/review", json={
            "action": "accept"
            # missing enrollment_id
        })
        self.assertEqual(res2.status_code, 400)

    @patch("app.send_enrollment_acceptance_dossier_email")
    @patch("app.send_push_notification")
    def test_review_accept_synchronizes_all_tables(self, mock_push, mock_email):
        """Accepting payment synchronizes enrollments, applications, offer letters, and accounts."""
        self.client.set_cookie(AUTH_COOKIE, self.admin_token)
        res = self.client.post("/admin/enrollment/review", json={
            "enrollment_id": self.test_enr_id,
            "action": "accept",
            "note": "Payment verified via admissions ledger."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("Accepted", data.get("message", ""))

        # Verify Database state
        with get_db() as conn:
            enr = conn.execute("SELECT payment_status, admin_note FROM enrollments WHERE id=?", (self.test_enr_id,)).fetchone()
            self.assertEqual(enr["payment_status"], "Accepted")
            self.assertEqual(enr["admin_note"], "Payment verified via admissions ledger.")

            app_row = conn.execute("SELECT status FROM applications WHERE LOWER(email)=?", (self.test_email.lower(),)).fetchone()
            self.assertEqual(app_row["status"], STATUS_ACCEPTED)

            offer = conn.execute("SELECT caution_deposit_status, pdf_unlocked FROM intern_offer_letters WHERE LOWER(email)=?", (self.test_email.lower(),)).fetchone()
            self.assertEqual(offer["caution_deposit_status"], "VERIFIED")
            self.assertEqual(offer["pdf_unlocked"], 1)

            acct = conn.execute("SELECT is_active FROM intern_accounts WHERE LOWER(email)=?", (self.test_email.lower(),)).fetchone()
            self.assertEqual(acct["is_active"], 1)

    @patch("app.send_status_update_email")
    @patch("app.send_push_notification")
    def test_review_reject_synchronizes_all_tables(self, mock_push, mock_email):
        """Rejecting payment updates statuses to Rejected / Enrollment Pending."""
        self.client.set_cookie(AUTH_COOKIE, self.admin_token)
        res = self.client.post("/admin/enrollment/review", json={
            "enrollment_id": self.test_enr_id,
            "action": "reject",
            "note": "UTR digits do not match banking ledger."
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("Rejected", data.get("message", ""))

        # Verify Database state
        with get_db() as conn:
            enr = conn.execute("SELECT payment_status, admin_note FROM enrollments WHERE id=?", (self.test_enr_id,)).fetchone()
            self.assertEqual(enr["payment_status"], "Rejected")
            self.assertEqual(enr["admin_note"], "UTR digits do not match banking ledger.")

            app_row = conn.execute("SELECT status FROM applications WHERE LOWER(email)=?", (self.test_email.lower(),)).fetchone()
            self.assertEqual(app_row["status"], STATUS_ENROLLMENT_PENDING)

            offer = conn.execute("SELECT caution_deposit_status FROM intern_offer_letters WHERE LOWER(email)=?", (self.test_email.lower(),)).fetchone()
            self.assertEqual(offer["caution_deposit_status"], "REJECTED")

    @patch("app.send_enrollment_acceptance_dossier_email")
    @patch("app.send_push_notification")
    def test_bulk_review_accept(self, mock_push, mock_email):
        """Bulk review accept synchronizes all target enrollments and offer letters."""
        self.client.set_cookie(AUTH_COOKIE, self.admin_token)
        res = self.client.post("/admin/enrollment/bulk-review", json={
            "ids": [self.test_enr_id],
            "action": "accept",
            "note": "Bulk accepted"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("processed"), 1)

        with get_db() as conn:
            enr = conn.execute("SELECT payment_status FROM enrollments WHERE id=?", (self.test_enr_id,)).fetchone()
            self.assertEqual(enr["payment_status"], "Accepted")
            offer = conn.execute("SELECT caution_deposit_status, pdf_unlocked FROM intern_offer_letters WHERE LOWER(email)=?", (self.test_email.lower(),)).fetchone()
            self.assertEqual(offer["caution_deposit_status"], "VERIFIED")
            self.assertEqual(offer["pdf_unlocked"], 1)

    def test_admin_html_markup_compliance(self):
        """Validate admin.html template bindings for viewScreenshot, modal buttons, and apiFetch."""
        tmpl_path = os.path.join(PORTAL_DIR, "templates", "admin.html")
        with open(tmpl_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 1. viewScreenshot call must pass r.id
        self.assertIn("${actAttr('click','viewScreenshot',[r.id,r.payment_screenshot,r.name,r.utr||''])}", content)
        self.assertIn("${actAttr('click','viewScreenshot',[r.id,r.payment_screenshot,r.name,''])}", content)

        # 2. Modal action buttons must have IDs and delegated bindings
        self.assertIn('id="btnEnrAccept"', content)
        self.assertIn('id="btnEnrReject"', content)
        self.assertIn('data-act-click="reviewEnrollment"', content)
        self.assertIn('data-arg-click=\'["accept"]\'', content)
        self.assertIn('data-arg-click=\'["reject"]\'', content)

        # 3. viewScreenshot function must accept id as first parameter
        self.assertIn("function viewScreenshot(id, filename, name, utr)", content)
        self.assertIn("_currentEnrId = id;", content)

        # 4. apiFetch must attach X-CSRF-Token
        self.assertIn("opts.headers['X-CSRF-Token'] = csrfTok;", content)


if __name__ == "__main__":
    unittest.main()
