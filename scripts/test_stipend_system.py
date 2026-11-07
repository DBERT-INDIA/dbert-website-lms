"""
scripts/test_stipend_system.py
Comprehensive automated test suite verifying all 6 phases:
Phase 1: Certificate Verification Gating & Sync Engine
Phase 2: Completion Date Engine & Seamless Auto-Provisioning
Phase 3: Silent-Fail Elimination & Admin Health Card Telemetry
Phase 4: Domain Milestone Tasks & Submission Architecture
Phase 5: Automated AI Pre-Screening & Staff 1-Click Approval
Phase 6: Wallet UPI Payout Parity & Withdrawal Readiness
"""
import sys
import os
import json
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

    def test_01_phase1_verification_gating(self):
        """Phase 1: Verification status detection for verified vs provisional candidates."""
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

    def test_02_phase2_completion_date_calculation(self):
        """Phase 2: Completion date gating and days remaining calculation."""
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

    def test_03_phase2_auto_provisioning_and_activation(self):
        """Phase 2: Seamless account auto-provisioning and password activation for verified candidates."""
        test_email = "kushalagarwal27496@gmail.com"
        csrf_tok = "test_csrf_token_stipend_2026"
        with self.client.session_transaction() as sess:
            sess["_csrf"] = csrf_tok

        # 1. Test /stipend/activate endpoint
        res = self.client.post(
            "/stipend/activate",
            json={"email": test_email},
            headers={"X-CSRF-Token": csrf_tok}
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Password activation link dispatched", data["message"])

        # 2. Verify account exists in intern_accounts
        with get_db() as conn:
            acct = conn.execute("SELECT * FROM intern_accounts WHERE LOWER(email) = LOWER(?)", (test_email,)).fetchone()
            self.assertIsNotNone(acct, "Account should be auto-provisioned in intern_accounts")
            self.assertEqual(acct["email"].lower(), test_email.lower())
            self.assertEqual(acct["name"], "Kushal Agarwal")

            # Verify token created in password_resets
            reset = conn.execute("SELECT * FROM password_resets WHERE LOWER(email) = LOWER(?) AND used = 0", (test_email,)).fetchone()
            self.assertIsNotNone(reset, "Password reset token should be recorded")

    def test_04_phase3_gemini_health_and_preflight(self):
        """Phase 3: Silent-Fail elimination: probe handles missing/invalid keys without throwing exceptions."""
        # Empty key
        ok, msg = probe_gemini_key("")
        self.assertFalse(ok)
        self.assertIn("No Gemini API key provided", msg)

        # Invalid dummy key
        ok2, msg2 = probe_gemini_key("AIzaSyDummyKeyForTestingOnly1234567890")
        self.assertFalse(ok2)
        self.assertIn("Google API authentication failed", msg2)

    def test_05_phase4_domain_tasks_and_schema(self):
        """Phase 4: Verify 4 domain milestone tasks (5,000 coins) and schema columns exist."""
        with get_db() as conn:
            # Check 4 tasks
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

    def test_06_phase5_ai_evaluator_rubrics_and_pre_screening(self):
        """Phase 5: Automated AI pre-screening against all 4 domain rubrics."""
        for d in ["AI & Machine Learning", "Data Analyst", "Full Stack Web Development", "Python Automation"]:
            self.assertIn(d, DOMAIN_RUBRICS)
            self.assertEqual(len(DOMAIN_RUBRICS[d]["criteria"]), 4)

        data = {
            "holder_name": "Test Student",
            "github_repo_url": "https://github.com/dbert/test-repo",
            "live_demo_url": "https://demo.dbert.in",
            "report_file_url": "/uploads/stipend/test.pdf",
            "submission_content": "Enterprise cloud microservice built with Flask and PostgreSQL."
        }
        res = StipendEvaluator.evaluate(data, domain="Full Stack Web Development", api_key="")
        self.assertIn("score", res)
        self.assertIn("verdict", res)
        self.assertIn("evaluated_at", res)

    def test_07_phase6_wallet_coin_ledger_payout_parity(self):
        """Phase 6: Verify 5,000 coin credit into referral ledger increases withdrawable balance for UPI payout."""
        with get_db() as conn:
            test_id = 99999
            b_before = get_coin_balances(conn, test_id)["referral"]

            conn.execute(
                """
                INSERT INTO coin_ledger_mirror 
                (intern_id, ledger_kind, delta, balance_after, reason, event_ts, idem_key, email)
                VALUES (?, 'referral', 5000, ?, 'Stipend Bounty: Capstone Approved', datetime('now','localtime'), ?, ?)
                """,
                (test_id, b_before + 5000, f"test_stipend_{os.urandom(4).hex()}", "test@dbert.in")
            )
            conn.commit()

            b_after = get_coin_balances(conn, test_id)["referral"]
            self.assertEqual(b_after, b_before + 5000, f"Withdrawable balance should increase by 5,000: {b_before} -> {b_after}")

    def test_08_all_stipend_routes_registered(self):
        """Verify all new stipend routes are registered and healthy on Flask app."""
        routes = [r.rule for r in app.url_map.iter_rules()]
        self.assertIn("/stipend/tasks", routes)
        self.assertIn("/stipend/tasks/<int:task_id>/submit", routes)
        self.assertIn("/stipend/activate", routes)
        self.assertIn("/admin/api/stipend-health", routes)
        self.assertIn("/admin/api/stipend-health/set-gemini-key", routes)


if __name__ == "__main__":
    unittest.main(verbosity=2)
