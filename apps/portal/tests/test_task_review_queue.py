"""Offline staff queue regression tests with synthetic SQLite rows."""

import sqlite3
import unittest

from services.task_review_queue import build_task_review_queue


class TaskReviewQueueTest(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.addCleanup(self.conn.close)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript("""
            CREATE TABLE tasks (id, title, coin_reward, task_type, target_domain, payment_type, submission_type);
            CREATE TABLE task_submissions (id, task_id, intern_id, email, status, created_at);
            CREATE TABLE intern_accounts (id, name, email);
            CREATE TABLE intern_articles (id, task_submission_id, intern_id, status, title, published_url);
            CREATE TABLE staff_accounts (id, name);
            CREATE TABLE review_log (id, queue_name, subject_type, subject_id, staff_id, decision, reason_code, created_at);
            INSERT INTO tasks VALUES (1, 'Build an API', 10, 'domain_specific', 'Backend', 'paid', 'url');
            INSERT INTO tasks VALUES (2, 'Design a form', 0, 'domain_specific', 'Design', 'unpaid', 'url');
            INSERT INTO intern_accounts VALUES (1, 'Demo Learner', 'learner@example.test');
            INSERT INTO intern_accounts VALUES (2, 'Other Learner', 'other@example.test');
            INSERT INTO task_submissions VALUES
                (10, 1, 1, 'other@example.test', 'pending', datetime('now','localtime','-8 days')),
                (11, 2, 1, 'learner@example.test', 'pending', datetime('now','localtime','-2 hours')),
                (12, 1, 999, 'LEARNER@EXAMPLE.TEST', 'approved', datetime('now','localtime','-4 days'));
            INSERT INTO intern_articles VALUES
                (30, NULL, 1, 'PUBLISHED', 'Other case study', NULL),
                (31, 10, 1, 'DRAFT', 'Work in progress', NULL),
                (32, NULL, 1, 'PUBLISHED', 'Newer case study', NULL);
            INSERT INTO staff_accounts VALUES (1, 'Demo Reviewer');
            INSERT INTO review_log VALUES
                (1, 'tasks', 'task', 12, 1, 'approved', 'RUBRIC_MET', datetime('now','localtime')),
                (2, 'projects', 'project', 12, 1, 'rejected', 'UNRELATED', datetime('now','localtime'));
        """)

    def queue(self, *, status="pending", domain="", age="", page=1):
        return build_task_review_queue(self.conn, status=status, domain=domain, age=age, page=page)

    def test_filters_and_pending_summary_count_each_submission_once(self):
        result = self.queue(domain="Backend", age="168")
        self.assertEqual(result["pending_count"], 2)
        self.assertEqual(result["oldest_pending_age"], "8d 0h")
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["submissions"][0]["id"], 10)
        self.assertEqual(result["submissions"][0]["article_title"], "Work in progress")
        self.assertEqual(result["submissions"][0]["intern_name"], "Demo Learner")

    def test_history_is_scoped_and_legacy_email_fallback_still_works(self):
        [approved] = self.queue(status="approved")["submissions"]
        self.assertEqual(approved["intern_name"], "Demo Learner")
        self.assertEqual([row["reason_code"] for row in approved["review_history"]], ["RUBRIC_MET"])

    def test_out_of_range_page_clamps_to_last_page(self):
        self.conn.executemany(
            "INSERT INTO task_submissions VALUES (?, 1, 1, NULL, 'pending', '2025-01-01 12:00:00')",
            [(value,) for value in range(100, 125)],
        )
        result = self.queue(status="unknown", domain="unknown", age="unknown", page=500)
        self.assertEqual((result["status"], result["domain"], result["age"]), ("pending", "", ""))
        self.assertEqual((result["total"], result["page"], result["page_count"]), (27, 2, 2))
        self.assertEqual([row["id"] for row in result["submissions"]], [10, 11])
