import os
import unittest
from datetime import datetime, timedelta
import sys

# Add apps/portal to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, get_db, create_session, get_intern_stage_and_next_action


class TestUserFlowStages(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        with get_db() as conn:
            # Clean test fixtures in child-to-parent order
            conn.execute("DELETE FROM attendance WHERE intern_id IN (SELECT id FROM intern_accounts WHERE email LIKE '%@stagetest.dbert.in')")
            conn.execute("DELETE FROM user_sessions WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM intern_offer_letters WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM course_enrollments WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM enrollments WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM applications WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM intern_accounts WHERE email LIKE '%@stagetest.dbert.in'")
            conn.commit()

    def tearDown(self):
        with get_db() as conn:
            conn.execute("DELETE FROM attendance WHERE intern_id IN (SELECT id FROM intern_accounts WHERE email LIKE '%@stagetest.dbert.in')")
            conn.execute("DELETE FROM user_sessions WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM intern_offer_letters WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM course_enrollments WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM enrollments WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM applications WHERE email LIKE '%@stagetest.dbert.in'")
            conn.execute("DELETE FROM intern_accounts WHERE email LIKE '%@stagetest.dbert.in'")
            conn.commit()

    def test_stage_1_under_review(self):
        """Candidate who only applied is in Under Review stage."""
        email = "candidate.applied@stagetest.dbert.in"
        with get_db() as conn:
            conn.execute("""
                INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status)
                VALUES ('Candidate One', ?, '9000000001', 'Delhi', 'DU', 'BTech', '4', '2027', 'Data Analyst', 'Learning', 'Under Review')
            """, (email,))
            conn.execute("INSERT INTO intern_accounts (name, email, domain, is_active) VALUES ('Candidate One', ?, 'Data Analyst', 1)", (email,))
            conn.commit()

            st = get_intern_stage_and_next_action(conn, email)
            self.assertEqual(st["stage_num"], 1)
            self.assertEqual(st["stage_name"], "Under Review")
            self.assertIn("/courses", st["primary_cta_url"])

    def test_stage_2_selected_pending_deposit(self):
        """Selected candidate without deposit has Next Action to review terms and confirm seat."""
        email = "candidate.selected@stagetest.dbert.in"
        with get_db() as conn:
            conn.execute("""
                INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status)
                VALUES ('Candidate Two', ?, '9000000002', 'Delhi', 'DU', 'BTech', '4', '2027', 'Data Analyst', 'Learning', 'Selected')
            """, (email,))
            conn.execute("INSERT INTO intern_accounts (name, email, domain, is_active) VALUES ('Candidate Two', ?, 'Data Analyst', 1)", (email,))
            conn.commit()

            st = get_intern_stage_and_next_action(conn, email)
            self.assertEqual(st["stage_num"], 2)
            self.assertEqual(st["stage_name"], "Selected · Action Required")
            self.assertEqual(st["primary_cta_url"], "/portal/offer")

    def test_stage_3_deposit_verification_in_progress(self):
        """Candidate with submitted ₹499 UTR sees Verification in Progress."""
        email = "candidate.submitted@stagetest.dbert.in"
        with get_db() as conn:
            conn.execute("""
                INSERT INTO enrollments (name, email, phone, college, domain, joining_date, payment_status, utr, amount)
                VALUES ('Candidate Three', ?, '9000000003', 'DU', 'Data Analyst', '2026-11-09', 'Pending Verification', '123456789012', 499)
            """, (email,))
            conn.execute("INSERT INTO intern_accounts (name, email, domain, is_active) VALUES ('Candidate Three', ?, 'Data Analyst', 1)", (email,))
            conn.commit()

            st = get_intern_stage_and_next_action(conn, email)
            self.assertEqual(st["stage_num"], 3)
            self.assertEqual(st["stage_name"], "Verification in Progress")
            self.assertEqual(st["primary_cta_url"], "/portal/offer")

    def test_stage_4_official_offer_unlocked(self):
        """Candidate with verified deposit can sign official offer letter."""
        email = "candidate.verified@stagetest.dbert.in"
        with get_db() as conn:
            conn.execute("""
                INSERT INTO enrollments (name, email, phone, college, domain, joining_date, payment_status, utr, amount)
                VALUES ('Candidate Four', ?, '9000000004', 'DU', 'Data Analyst', '2026-11-09', 'Verified', '123456789012', 499)
            """, (email,))
            conn.execute("INSERT INTO intern_accounts (name, email, domain, is_active) VALUES ('Candidate Four', ?, 'Data Analyst', 1)", (email,))
            conn.commit()

            st = get_intern_stage_and_next_action(conn, email)
            self.assertEqual(st["stage_num"], 4)
            self.assertEqual(st["stage_name"], "Official Offer Unlocked")
            self.assertIn("Sign", st["primary_cta_label"])
            self.assertEqual(st["primary_cta_url"], "/portal/offer")

    def test_stage_5_active_sprint_with_attendance_tracking(self):
        """Accepted/signed candidate in active sprint tracks weekly 10 hrs login."""
        email = "candidate.active@stagetest.dbert.in"
        with get_db() as conn:
            conn.execute("""
                INSERT INTO enrollments (name, email, phone, college, domain, joining_date, payment_status, utr, amount)
                VALUES ('Candidate Five', ?, '9000000005', 'DU', 'Data Analyst', '2026-11-09', 'Verified', '123456789012', 499)
            """, (email,))
            cur = conn.execute("INSERT INTO intern_accounts (name, email, domain, is_active) VALUES ('Candidate Five', ?, 'Data Analyst', 1)", (email,))
            intern_id = cur.lastrowid
            conn.execute("""
                INSERT INTO intern_offer_letters (email, name, domain, offer_letter_id, batch_start_date, batch_end_date, caution_deposit_status, pdf_unlocked, signature_name, accepted_at)
                VALUES (?, 'Candidate Five', 'Data Analyst', 'DBERT-OFR-2026-DA-8805', '2026-11-09', '2027-01-09', 'VERIFIED', 1, 'Candidate Five', datetime('now'))
            """, (email,))
            conn.commit()

            st = get_intern_stage_and_next_action(conn, email)
            self.assertEqual(st["stage_num"], 5)
            self.assertEqual(st["stage_name"], "Active Sprint")
            self.assertEqual(st["hours_target"], 10)
            self.assertIn("/courses", st["primary_cta_url"])

    def test_cross_domain_attendance_cors_and_ping(self):
        """Attendance endpoint accepts OPTIONS preflight from dbert.in and logs presence."""
        email = "attendance.test@stagetest.dbert.in"
        with get_db() as conn:
            conn.execute("""
                INSERT INTO enrollments (name, email, phone, college, domain, joining_date, payment_status, amount)
                VALUES ('Att Tester', ?, '9000000006', 'DU', 'Data Analyst', '2026-11-09', 'Verified', 499)
            """, (email,))
            cur = conn.execute("INSERT INTO intern_accounts (name, email, domain, is_active) VALUES ('Att Tester', ?, 'Data Analyst', 1)", (email,))
            intern_id = cur.lastrowid
            conn.commit()

        token = create_session(email, "intern")

        # 1. OPTIONS preflight
        res_opts = self.client.open(
            "/attendance/ping",
            method="OPTIONS",
            headers={
                "Origin": "https://dbert.in",
                "Access-Control-Request-Method": "POST"
            }
        )
        self.assertIn(res_opts.status_code, (200, 204))
        self.assertEqual(res_opts.headers.get("Access-Control-Allow-Origin"), "https://dbert.in")
        self.assertEqual(res_opts.headers.get("Access-Control-Allow-Credentials"), "true")

        # 2. POST attendance ping from dbert.in
        res_ping = self.client.post(
            "/attendance/ping",
            headers={
                "Origin": "https://dbert.in",
                "X-Session-Token": token
            }
        )
        self.assertEqual(res_ping.status_code, 200)
        data = res_ping.get_json()
        self.assertIn(data["status"], ("ok", "success"))
        self.assertIn("total_minutes", data)


if __name__ == "__main__":
    unittest.main()
