"""Mentor schedule workflow tests with synthetic data and no external services."""

from datetime import datetime, timedelta
import sqlite3
import unittest

from services.database.adapter import SQLiteAdapter
from services.mentor_schedule import (
    BookingError, IST, confirmed_meeting_link, create_slot, ensure_mentor_schedule_schema,
    owner_slots, release_slot, reserve_slot, session_calendar, student_calendar, student_reservations,
    update_learner_question, update_session_details,
)


class MentorScheduleTest(unittest.TestCase):
    def setUp(self):
        self.raw = sqlite3.connect(":memory:")
        self.raw.row_factory = sqlite3.Row
        self.addCleanup(self.raw.close)
        self.conn = SQLiteAdapter(self.raw)
        self.raw.executescript("""
            PRAGMA foreign_keys = ON;
            CREATE TABLE staff_accounts (id INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE mentors (id INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE intern_accounts (id INTEGER PRIMARY KEY, name TEXT, email TEXT);
            CREATE TABLE notifications (id INTEGER PRIMARY KEY, intern_id, kind, title, body, link);
            CREATE TABLE mentor_availability_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mentor_staff_id INTEGER NOT NULL REFERENCES staff_accounts(id),
                start_time TEXT NOT NULL, end_time TEXT NOT NULL, is_booked INTEGER DEFAULT 0, created_at TEXT
            );
            CREATE TABLE mentor_session_bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slot_id INTEGER NOT NULL UNIQUE REFERENCES mentor_availability_slots(id),
                intern_id INTEGER NOT NULL REFERENCES intern_accounts(id),
                meeting_link TEXT, status TEXT DEFAULT 'booked', created_at TEXT
            );
            INSERT INTO staff_accounts VALUES (1, 'Demo Staff');
            INSERT INTO mentors VALUES (1, 'Demo Mentor');
            INSERT INTO intern_accounts VALUES (1, 'Learner One', 'one@example.test');
            INSERT INTO intern_accounts VALUES (2, 'Learner Two', 'two@example.test');
            INSERT INTO intern_accounts VALUES (3, 'Learner Three', 'three@example.test');
            INSERT INTO intern_accounts VALUES (4, 'Learner Four', 'four@example.test');
        """)
        self.start = (datetime.now(IST) + timedelta(days=1)).replace(hour=15, minute=0, second=0, microsecond=0)
        self.end = self.start + timedelta(minutes=45)
        self.raw.execute(
            "INSERT INTO mentor_availability_slots (mentor_staff_id, start_time, end_time, is_booked) VALUES (1, ?, ?, 1)",
            (self.start.strftime("%Y-%m-%d %H:%M:%S"), self.end.strftime("%Y-%m-%d %H:%M:%S")),
        )
        self.raw.execute("""
            INSERT INTO mentor_session_bookings (slot_id, intern_id, meeting_link, status)
            VALUES (1, 1, 'https://meet.google.com/dbert-mentor-slot-1', 'booked')
        """)
        self.raw.commit()
        self.migrate()

    def migrate(self):
        with self.conn:
            ensure_mentor_schedule_schema(self.conn, lambda conn, *column: conn.ensure_column(*column))

    def new_slot(self):
        with self.conn:
            create_slot(
                self.conn, staff_id=None, mentor_id=1,
                payload={"start_time": self.start.isoformat(), "end_time": self.end.isoformat(),
                    "capacity": 2, "topic": "Synthetic, review", "domain": "Backend",
                    "meeting_link": "https://meet.example.test/demo"},
                domains=("Backend",),
            )
        return self.raw.execute("SELECT MAX(id) FROM mentor_availability_slots").fetchone()[0]

    def test_migration_preserves_legacy_booking_and_mentor_ownership(self):
        self.migrate()
        self.assertEqual(self.raw.execute("PRAGMA foreign_key_check").fetchall(), [])
        [legacy] = student_reservations(self.conn, 1)
        self.assertEqual(legacy["slot_id"], 1)
        self.assertIsNone(legacy["meeting_link"])
        slot_id = self.new_slot()
        self.assertEqual([slot["id"] for slot in owner_slots(self.conn, staff_id=1, mentor_id=None)], [1])
        self.assertEqual([slot["id"] for slot in owner_slots(self.conn, staff_id=None, mentor_id=1)], [slot_id])
        _, mentors = student_calendar(self.conn, 1)
        self.assertEqual({mentor["id"] for mentor in mentors}, {"staff-1", "mentor-1"})

    def test_group_capacity_replay_and_cancellation(self):
        slot_id = self.new_slot()
        with self.conn:
            reserve_slot(self.conn, intern_id=2, slot_id=slot_id)
        with self.conn:
            reserve_slot(self.conn, intern_id=2, slot_id=slot_id)
        with self.conn:
            reserve_slot(self.conn, intern_id=3, slot_id=slot_id)
        with self.assertRaisesRegex(BookingError, "full"), self.conn:
            reserve_slot(self.conn, intern_id=4, slot_id=slot_id)
        self.assertEqual(self.raw.execute("SELECT COUNT(*) FROM notifications WHERE intern_id=2").fetchone()[0], 1)
        with self.conn:
            release_slot(self.conn, intern_id=2, slot_id=slot_id)
        self.assertEqual(student_reservations(self.conn, 2), [])
        with self.conn:
            reserve_slot(self.conn, intern_id=4, slot_id=slot_id)
        count = self.raw.execute("SELECT seats_booked FROM mentor_availability_slots WHERE id=?", (slot_id,)).fetchone()[0]
        self.assertEqual(count, 2)

    def test_workspace_requires_slot_ownership_and_confirmed_reservation(self):
        slot_id = self.new_slot()
        details = dict(slot_id=slot_id, agenda="Review milestones", follow_up="Share an updated outline",
                       meeting_link="https://meet.example.test/revised")
        with self.assertRaisesRegex(BookingError, "could not be found"), self.conn:
            update_session_details(self.conn, staff_id=1, mentor_id=None, **details)
        with self.conn:
            reserve_slot(self.conn, intern_id=2, slot_id=slot_id)
        with self.assertRaisesRegex(BookingError, "you have reserved"), self.conn:
            update_learner_question(self.conn, intern_id=3, slot_id=slot_id, question="Review my plan")
        with self.conn:
            update_learner_question(self.conn, intern_id=2, slot_id=slot_id, question="Review my plan")
            update_session_details(self.conn, staff_id=None, mentor_id=1, **details)
        [booking] = student_reservations(self.conn, 2, slot_id)
        self.assertEqual((booking["agenda"], booking["follow_up"], booking["meeting_link"]),
                         (details["agenda"], details["follow_up"], details["meeting_link"]))
        [slot] = owner_slots(self.conn, staff_id=None, mentor_id=1)
        self.assertEqual(slot["attendees"][0]["question"], "Review my plan")

    def test_calendar_exports_utc_with_confirmed_link(self):
        result = session_calendar({"slot_id": 1, "start_time": "2035-11-23 15:00", "end_time": "2035-11-23 15:45",
                                   "topic": "Demo, project", "mentor_name": "Demo Mentor",
                                   "meeting_link": "https://meet.example.test/session"})
        self.assertIn("DTSTART:20351123T093000Z\r\n", result)
        self.assertIn("DTEND:20351123T101500Z\r\n", result)
        self.assertIn("SUMMARY:Demo\\, project\r\n", result)
        self.assertIn("URL:https://meet.example.test/session\r\n", result)
        self.assertIsNone(confirmed_meeting_link("http://meet.example.test/session"))
