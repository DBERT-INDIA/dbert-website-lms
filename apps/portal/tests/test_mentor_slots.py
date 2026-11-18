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

from app import app, get_db, create_session


class TestMentorSlots(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

        with get_db() as conn:
            conn.execute("DELETE FROM mentor_session_bookings WHERE intern_id IN (9101, 9102)")
            conn.execute("DELETE FROM enrollments WHERE id IN (9101, 9102)")
            conn.execute("DELETE FROM intern_accounts WHERE id IN (9101, 9102)")
            conn.execute("DELETE FROM user_sessions WHERE email LIKE '%@test.dbert.in'")

            # Intern 1: With regular domain
            conn.execute("""
                INSERT INTO enrollments (id, name, email, phone, college, domain, joining_date, payment_status, amount)
                VALUES (9101, 'Aditi Rao', 'aditi.slots@test.dbert.in', '9876543210', 'IIT Madras', 'Full Stack Web Development', '2026-11-09', 'Verified', 499)
            """)
            conn.execute("""
                INSERT INTO intern_accounts (id, name, email, domain, is_active)
                VALUES (9101, 'Aditi Rao', 'aditi.slots@test.dbert.in', 'Full Stack Web Development', 1)
            """)

            # Intern 2: Without domain (NULL domain)
            conn.execute("""
                INSERT INTO enrollments (id, name, email, phone, college, domain, joining_date, payment_status, amount)
                VALUES (9102, 'Varun Nair', 'varun.nodomain@test.dbert.in', '9876543211', 'NIT Trichy', NULL, '2026-11-09', 'Verified', 499)
            """)
            conn.execute("""
                INSERT INTO intern_accounts (id, name, email, domain, is_active)
                VALUES (9102, 'Varun Nair', 'varun.nodomain@test.dbert.in', NULL, 1)
            """)
            # Create a test mentor availability slot
            conn.execute("DELETE FROM mentor_availability_slots WHERE id = 9999")
            conn.execute("""
                INSERT INTO mentor_availability_slots (id, mentor_staff_id, start_time, end_time, topic, domain, capacity, seats_booked, is_booked)
                VALUES (9999, 1, '2026-11-20 15:00:00', '2026-11-20 15:45:00', 'Test Architecture Session', 'Full Stack Web Development', 30, 0, 0)
            """)
            conn.commit()

    def tearDown(self):
        with get_db() as conn:
            conn.execute("DELETE FROM mentor_session_bookings WHERE intern_id IN (9101, 9102)")
            conn.execute("DELETE FROM mentor_availability_slots WHERE id = 9999")
            conn.execute("DELETE FROM enrollments WHERE id IN (9101, 9102)")
            conn.execute("DELETE FROM intern_accounts WHERE id IN (9101, 9102)")
            conn.execute("DELETE FROM user_sessions WHERE email LIKE '%@test.dbert.in'")
            conn.commit()

    def test_unauthenticated_redirect(self):
        res = self.client.get("/mentors/slots")
        self.assertEqual(res.status_code, 302)
        self.assertTrue("/#signin" in res.headers.get("Location", ""))

    def test_mentor_slots_page_loads_with_domain(self):
        token = create_session("aditi.slots@test.dbert.in", "intern")
        self.client.set_cookie("dbert_session", token)

        res = self.client.get("/mentors/slots")
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn("Select Domain Track & Mentor", html)
        self.assertIn("rawSlots", html)
        self.assertIn("Full Stack Web Development", html)

    def test_mentor_slots_page_loads_with_null_domain(self):
        """Tests that intern with None/NULL domain renders without Undefined JSON serialization error."""
        token = create_session("varun.nodomain@test.dbert.in", "intern")
        self.client.set_cookie("dbert_session", token)

        res = self.client.get("/mentors/slots")
        self.assertEqual(res.status_code, 200)
        html = res.data.decode("utf-8")
        self.assertIn("Select Domain Track & Mentor", html)
        self.assertIn("All Tracks", html)

    def test_book_slot_and_cancel_slot(self):
        token = create_session("aditi.slots@test.dbert.in", "intern")
        self.client.set_cookie("dbert_session", token)

        # 1. Book slot 9999
        res_book = self.client.post("/mentors/slots/9999/book")
        self.assertEqual(res_book.status_code, 200)
        data = res_book.get_json()
        self.assertEqual(data["status"], "success")

        # 2. Verify slot capacity incremented in DB
        with get_db() as conn:
            slot = conn.execute("SELECT seats_booked FROM mentor_availability_slots WHERE id = 9999").fetchone()
            self.assertEqual(slot["seats_booked"], 1)

            # Check that an in-app confirmation notification was created for intern 9101
            notif = conn.execute("SELECT * FROM notifications WHERE intern_id = 9101 AND kind = 'mentorship'").fetchone()
            self.assertIsNotNone(notif)
            self.assertIn("Confirmed", notif["title"])

        # 3. Pacing check: Cannot book another slot while one is active
        res_book_again = self.client.post("/mentors/slots/9999/book")
        self.assertEqual(res_book_again.status_code, 400)
        data_again = res_book_again.get_json()
        self.assertEqual(data_again["status"], "error")

        # 4. Cancel reservation
        res_cancel = self.client.post("/mentors/slots/9999/cancel")
        self.assertEqual(res_cancel.status_code, 200)
        data_cancel = res_cancel.get_json()
        self.assertEqual(data_cancel["status"], "success")

        # 5. Verify seat restored
        with get_db() as conn:
            slot_after = conn.execute("SELECT seats_booked FROM mentor_availability_slots WHERE id = 9999").fetchone()
            self.assertEqual(slot_after["seats_booked"], 0)

            # Check cancellation notification
            canc_notif = conn.execute("SELECT * FROM notifications WHERE intern_id = 9101 AND title LIKE '%Cancelled%'").fetchone()
            self.assertIsNotNone(canc_notif)

    def test_mentor_console_attendee_roster_and_meeting_link(self):
        # 1. Intern books slot 9999 (owned by staff 1)
        token_intern = create_session("aditi.slots@test.dbert.in", "intern")
        self.client.set_cookie("dbert_session", token_intern)
        res_book = self.client.post("/mentors/slots/9999/book")
        self.assertEqual(res_book.status_code, 200)

        # 2. Mentor (staff id 1: dbert_admin_prod@dbert.in) logs in
        token_staff = create_session("dbert_admin_prod@dbert.in", "staff")
        self.client.set_cookie("dbert_session", token_staff)
        with self.client.session_transaction() as sess:
            sess["staff_id"] = 1
            sess["staff_name"] = "DBERT Admin Staff"

        # 3. Request /staff/mentor-slots
        res_slots = self.client.get("/staff/mentor-slots")
        self.assertEqual(res_slots.status_code, 200)
        html = res_slots.data.decode("utf-8")

        # 4. Verify attendee roster rendered
        self.assertIn("1 Interns View", html)
        self.assertIn("Aditi Rao", html)
        self.assertIn("aditi.slots@test.dbert.in", html)
        self.assertIn("https://meet.google.com/dbert-mentor-slot-9999", html)
        self.assertNotIn('href="None"', html)

    def test_dev_impersonate_mentor_faculty(self):
        # Test impersonating Dr. Ananya Sen
        res = self.client.get("/dev/impersonate?email=ananya.sen@dbert.in&target=/staff/mentor-slots")
        self.assertEqual(res.status_code, 302)
        self.assertTrue(res.headers["Location"].endswith("/staff/mentor-slots"))

        # Follow into mentor console
        res_page = self.client.get("/staff/mentor-slots")
        self.assertEqual(res_page.status_code, 200)
        html = res_page.data.decode("utf-8")
        self.assertIn("Dr. Ananya Sen", html)
        self.assertIn("Mentor Faculty Console", html)


if __name__ == "__main__":
    unittest.main()
