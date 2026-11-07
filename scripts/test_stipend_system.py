"""
scripts/test_stipend_system.py
Comprehensive automated test suite verifying:
1. Certificate Verification Gating
2. Completion Date Lifecycle Calculation
3. Gemini Health & Pre-flight Diagnostics
4. Stipend Route Registration
5. Database Schema & Task Bounties
6. LMS Coin Ledger Payout Parity
"""
import sys
import os
import unittest

os.environ["TESTING"] = "1"
os.environ["REQUIRE_POSTGRES"] = "false"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal")))

from app import app, get_db, get_coin_balances, credit_intern_coins
from services.certificate_service import CertificateService
from services.ai.stipend_evaluator import (
    StipendEvaluator, get_active_gemini_key, probe_gemini_key, DOMAIN_RUBRICS
)


class TestStipendSystem(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_01_certificate_verification_gating(self):
        """Test verification status detection for verified vs provisional candidates."""
        with get_db() as conn:
            # 1. Kushal Agarwal (Verified DA-001)
            v_res = CertificateService.is_intern_verified(conn, email="kushalagarwal27496@gmail.com")
            self.assertTrue(v_res["verified"], f"Expected verified=True, got {v_res}")
            self.assertFalse(v_res["is_provisional"])
            self.assertEqual(v_res["status"], "VERIFIED")
            self.assertEqual(v_res["cert_id"], "CERT-DBERT-2026-DA-001")

            # 2. Rajesh Badugu (Provisional DA-057)
            p_res = CertificateService.is_intern_verified(conn, email="rajeshbadugu67@gmail.com")
            self.assertFalse(p_res["verified"], f"Expected verified=False, got {p_res}")
            self.assertTrue(p_res["is_provisional"])
            self.assertEqual(p_res["status"], "PROVISIONAL")
            self.assertEqual(p_res["cert_id"], "CERT-DBERT-2026-DA-057")

            # 3. Unknown candidate
            u_res = CertificateService.is_intern_verified(conn, email="nonexistent_candidate_xyz@gmail.com")
            self.assertFalse(u_res["verified"])
            self.assertEqual(u_res["status"], "NOT_FOUND")

    def test_02_completion_date_calculation(self):
        """Test completion date gating and days remaining calculation."""
        with get_db() as conn:
            # 1. Completed Candidate (Kushal Agarwal - July to September 2026)
            c1 = CertificateService.get_intern_completion_info(conn, email="kushalagarwal27496@gmail.com")
            self.assertTrue(c1["is_completed"], "Kushal's internship should be marked completed")
            self.assertEqual(c1["days_remaining"], 0)
            self.assertEqual(c1["completion_date"], "2026-09-30")

            # 2. In-Progress Candidate (Bhargavi Poola - batch starting Nov 2026)
            c2 = CertificateService.get_intern_completion_info(conn, email="bhargavi13032007@gmail.com")
            self.assertFalse(c2["is_completed"], "Bhargavi's internship should be marked in-progress")
            self.assertGreater(c2["days_remaining"], 0)
            self.assertEqual(c2["completion_date"], "2027-01-31")

    def test_03_gemini_health_and_preflight(self):
        """Test that Gemini key probing handles empty and invalid keys without crashing."""
        # Empty key
        ok, msg = probe_gemini_key("")
        self.assertFalse(ok)
        self.assertIn("No Gemini API key provided", msg)

        # Invalid dummy key
        ok2, msg2 = probe_gemini_key("AIzaSyDummyKeyForTestingOnly1234567890")
        self.assertFalse(ok2)
        self.assertIn("Google API authentication failed", msg2)

    def test_04_ai_evaluator_fallback_and_rubrics(self):
        """Test AI pre-screening evaluator with simulated deliverables."""
        self.assertIn("AI & Machine Learning", DOMAIN_RUBRICS)
        self.assertIn("Data Analyst", DOMAIN_RUBRICS)
        self.assertIn("Full Stack Web Development", DOMAIN_RUBRICS)
        self.assertIn("Python Automation", DOMAIN_RUBRICS)

        # Test evaluation fallback when no key is present
        data = {
            "holder_name": "Test Student",
            "github_repo_url": "https://github.com/dbert/test-repo",
            "live_demo_url": "https://demo.dbert.in",
            "report_file_url": "/uploads/stipend/test.pdf",
            "submission_content": "Production AI pipeline built with Next.js and Flask."
        }
        res = StipendEvaluator.evaluate(data, domain="Full Stack Web Development", api_key="")
        self.assertIn("score", res)
        self.assertIn("verdict", res)
        self.assertIn("evaluated_at", res)

    def test_05_route_registration(self):
        """Verify all new stipend routes are registered on the Flask application."""
        routes = [r.rule for r in app.url_map.iter_rules()]
        self.assertIn("/stipend/tasks", routes)
        self.assertIn("/stipend/tasks/<int:task_id>/submit", routes)
        self.assertIn("/admin/api/stipend-health", routes)
        self.assertIn("/admin/api/stipend-health/set-gemini-key", routes)

    def test_06_database_schema_and_tasks(self):
        """Verify required columns and seeded 5,000-coin tasks exist in DB."""
        with get_db() as conn:
            # Check tasks
            tasks = conn.execute("SELECT * FROM tasks WHERE task_type = 'stipend_milestone'").fetchall()
            self.assertEqual(len(tasks), 4, f"Expected 4 stipend tasks, found {len(tasks)}")
            for t in tasks:
                self.assertEqual(t["coin_reward"], 5000, f"Task {t['title']} should have 5000 coin reward")
                self.assertEqual(t["payment_type"], "paid")

            # Check task_submissions columns
            cols = [r["name"] for r in conn.execute("PRAGMA table_info(task_submissions)").fetchall()]
            required = [
                "github_repo_url", "live_demo_url", "report_file_url",
                "ai_evaluation_score", "ai_evaluation_status", "ai_evaluation_notes",
                "ai_evaluated_at", "task_category"
            ]
            for col in required:
                self.assertIn(col, cols, f"Missing column {col} in task_submissions")

    def test_07_coin_ledger_payout_parity(self):
        """Verify that crediting 5000 coins into referral ledger increases withdrawable balance."""
        with get_db() as conn:
            # Use test intern_id = 99999
            test_id = 99999
            b_before = get_coin_balances(conn, test_id)["referral"]

            # Credit 5000 withdrawable coins
            conn.execute(
                """
                INSERT INTO coin_ledger_mirror 
                (intern_id, ledger_kind, delta, balance_after, reason, event_ts, idem_key, email)
                VALUES (?, 'referral', 5000, ?, 'Test Stipend Reward', datetime('now','localtime'), ?, ?)
                """,
                (test_id, b_before + 5000, f"test_stipend_{os.urandom(4).hex()}", "test@dbert.in")
            )
            conn.commit()

            b_after = get_coin_balances(conn, test_id)["referral"]
            self.assertEqual(b_after, b_before + 5000, f"Withdrawable balance should increase by 5000: {b_before} -> {b_after}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
