"""Offline regression tests for job reports and employer pipeline ownership."""

from datetime import datetime, timedelta
import sqlite3
import unittest

from services.employer_pipeline import (
    IST, PipelineError, interview_form_value, mark_position_filled, update_employer_interview,
)
from services.listing_quality import (
    ListingReportError, listing_quality_queue, pending_listing_reports, report_listing, resolve_listing_report,
)


class HiringWorkflowTest(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.addCleanup(self.conn.close)
        self.conn.executescript("""
            CREATE TABLE companies (id INTEGER PRIMARY KEY, name, is_approved, is_active);
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY, company_id, title, description, slug, post_type, domain,
                location, status, expires_at, updated_at, published_at, created_at
            );
            CREATE TABLE post_applications (
                id INTEGER PRIMARY KEY, post_id, status,
                employer_interview_at, employer_interview_link, employer_interview_note
            );
            CREATE TABLE job_listing_reports (
                id INTEGER PRIMARY KEY, post_id, intern_id, reason, note, status DEFAULT 'pending',
                reviewed_by, reviewed_at, created_at DEFAULT (datetime('now','localtime')),
                UNIQUE (post_id, intern_id, reason)
            );
            INSERT INTO companies VALUES (10, 'Demo Employer', 1, 1), (20, 'Other Employer', 1, 1);
            INSERT INTO posts VALUES
                (1, 10, 'Demo Developer', 'Build software', 'demo-dev', 'job', 'Web', 'Delhi', 'published', NULL, datetime('now','localtime'), NULL, NULL),
                (2, 10, ' demo developer ', '', 'other-dev', 'job', 'Web', 'Delhi', 'published', '2020-01-01', NULL, NULL, '2020-01-01'),
                (3, 20, 'Demo Developer', 'Build software', 'third-dev', 'job', 'Web', 'Delhi', 'published', NULL, datetime('now','localtime'), NULL, NULL),
                (4, 10, 'Hidden Draft', '', 'hidden', 'job', 'Web', '', 'draft', NULL, NULL, NULL, NULL);
            INSERT INTO post_applications VALUES (15, 1, 'Shortlisted', NULL, NULL, NULL);
            INSERT INTO post_applications VALUES (16, 1, 'Hired', NULL, NULL, NULL);
        """)

    def interview(self):
        tomorrow = (datetime.now(IST) + timedelta(days=1)).date().isoformat()
        return {"start": tomorrow + "T15:00", "link": "https://meet.example.test/demo", "note": "Bring a project summary"}

    def test_interview_owner_scope_timezone_and_cancel(self):
        details = self.interview()
        with self.assertRaises(PipelineError):
            update_employer_interview(self.conn, company_id=20, app_id=15, **details)
        with self.assertRaises(PipelineError):
            update_employer_interview(self.conn, company_id=10, app_id=16, **details)
        post_id = update_employer_interview(self.conn, company_id=10, app_id=15, **details)
        self.assertEqual(post_id, 1)
        row = self.conn.execute("SELECT * FROM post_applications WHERE id = 15").fetchone()
        self.assertTrue(row["employer_interview_at"].endswith("T09:30:00+00:00"))
        self.assertEqual(interview_form_value(row["employer_interview_at"]), details["start"])
        self.assertEqual((row["employer_interview_link"], row["employer_interview_note"]), (details["link"], details["note"]))
        update_employer_interview(self.conn, company_id=10, app_id=15, cancel=True)
        self.assertIsNone(self.conn.execute("SELECT employer_interview_at FROM post_applications WHERE id=15").fetchone()[0])

    def test_mark_filled_keeps_applicants_and_repeats_safely(self):
        with self.assertRaises(PipelineError):
            mark_position_filled(self.conn, company_id=20, post_id=1)
        mark_position_filled(self.conn, company_id=10, post_id=1)
        mark_position_filled(self.conn, company_id=10, post_id=1)
        self.assertEqual(self.conn.execute("SELECT status FROM posts WHERE id=1").fetchone()[0], "filled")
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM post_applications WHERE post_id=1").fetchone()[0], 2)

    def test_reports_dedupe_and_quality_filters(self):
        with self.assertRaises(ListingReportError):
            report_listing(self.conn, post_id=4, intern_id=35, reason="inaccurate", note="Draft")
        for _ in range(2):
            report_listing(self.conn, post_id=3, intern_id=35, reason="inaccurate", note="Check details")
        queue = listing_quality_queue(self.conn)
        self.assertEqual(queue["total"], 3)
        posts = {post["id"]: post for post in queue["rows"]}
        self.assertEqual(posts[3]["report_count"], 1)
        self.assertEqual(posts[3]["duplicate"], 0)
        self.assertEqual(posts[1]["duplicate"], 1)
        self.assertEqual((posts[2]["duplicate"], posts[2]["stale"], posts[2]["incomplete"]), (1, 1, 1))
        self.assertEqual(listing_quality_queue(self.conn, view="automated")["total"], 2)
        [report] = pending_listing_reports(self.conn, 3)
        self.assertNotIn("intern_id", report)
        self.assertEqual(resolve_listing_report(self.conn, report_id=report["id"], staff_id=7), 3)
        self.assertEqual(listing_quality_queue(self.conn, view="reports")["total"], 0)
        self.assertEqual(self.conn.execute("SELECT reviewed_by FROM job_listing_reports").fetchone()[0], 7)
