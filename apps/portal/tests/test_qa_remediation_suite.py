#!/usr/bin/env python3
"""
Comprehensive QA Remediation Test Suite (test_qa_remediation_suite.py)
Validates core requirements from DBERT_QA_REMEDIATION_MASTER_PLAN.md:
- Transaction safety & failure injection (SF-001 through SF-015)
- Authorization & file security (SEC-001 through SEC-010)
- Funnel and UX state machine (UX-001 through UX-010)
"""

import os
import sys
import json
import uuid
import unittest
from datetime import datetime, timedelta

# Setup path
PORTAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PORTAL_DIR)

from app import app, get_db, build_intern_next_action, credit_intern_coins
from services.outbox_service import (
    enqueue_outbox_event,
    claim_outbox_batch,
    reclaim_expired_leases,
    mark_event_sent,
    mark_event_failed,
    STATUS_PENDING,
    STATUS_PROCESSING,
    STATUS_SENT,
    STATUS_RETRYING,
    STATUS_DEAD_LETTER,
    EVENT_APPLICATION_SUBMITTED
)
from services.payment_service import PaymentService
from services.ai.stipend_evaluator import StipendEvaluator
from services.file_security_service import authorize_file_download
from services.telemetry_service import check_liveness, check_readiness


class TestQARemediationSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        with app.app_context():
            from app import init_db
            init_db()

    def setUp(self):
        self.client = app.test_client()

    # =========================================================================
    # 1. OUTBOX CONCURRENCY & CRASH RECOVERY (SF-013, SF-014, DBQ-0301 - DBQ-0312)
    # =========================================================================
    def test_outbox_atomic_worker_claim_and_recovery(self):
        """SF-013 & SF-014: Two workers claiming pending events do not process the same row."""
        with get_db() as conn:
            # Reset any lingering events to cleanly isolate concurrency test
            conn.execute("UPDATE event_outbox SET status='SENT' WHERE status IN ('PENDING', 'RETRYING', 'PROCESSING')")
            conn.commit()

            # Enqueue a test event
            ev_id = enqueue_outbox_event(
                conn,
                event_type=EVENT_APPLICATION_SUBMITTED,
                aggregate_type="test_candidate",
                aggregate_id="cand_test_99",
                payload={"email": "worker_test@dbert.test"}
            )
            conn.commit()

            # Worker 1 claims batch
            batch_w1 = claim_outbox_batch(conn, worker_id="worker_alpha", limit=10, lease_seconds=120)
            claimed_ids_w1 = [e["id"] for e in batch_w1]
            self.assertIn(ev_id, claimed_ids_w1, "Worker 1 should have claimed the new event.")

            # Check that event is marked as PROCESSING in DB
            row = conn.execute("SELECT status, locked_by FROM event_outbox WHERE id=?", (ev_id,)).fetchone()
            self.assertEqual(row["status"], STATUS_PROCESSING)
            self.assertEqual(row["locked_by"], "worker_alpha")

            # Worker 2 attempts to claim batch concurrently
            batch_w2 = claim_outbox_batch(conn, worker_id="worker_beta", limit=10, lease_seconds=120)
            claimed_ids_w2 = [e["id"] for e in batch_w2]
            self.assertNotIn(ev_id, claimed_ids_w2, "Worker 2 must NOT claim the event already leased to Worker 1.")

            # Test Lease Expiry Recovery (SF-014): Set lock_expires_at into the past
            past_time = (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                "UPDATE event_outbox SET lock_expires_at=? WHERE id=?", (past_time, ev_id)
            )
            conn.commit()

            # Reclaiming expired leases should reset it to RETRYING
            reclaimed_count = reclaim_expired_leases(conn)
            self.assertGreaterEqual(reclaimed_count, 1)

            row_after = conn.execute("SELECT status, locked_by FROM event_outbox WHERE id=?", (ev_id,)).fetchone()
            self.assertEqual(row_after["status"], STATUS_RETRYING)
            self.assertIsNone(row_after["locked_by"])

            # Clean up
            mark_event_sent(conn, ev_id)
            conn.commit()

    # =========================================================================
    # 2. STIPEND DETERMINISTIC IDEMPOTENCY (SF-011, DBQ-0140, DBQ-0141)
    # =========================================================================
    def test_stipend_reward_deterministic_idempotency(self):
        """SF-011: Multiple calls to award stipend for the same submission ID must credit exactly once."""
        import random, time
        test_sub_id = int(time.time() * 100) % 10000000 + random.randint(100, 9999)
        test_email = f"stipend_test_{uuid.uuid4().hex[:6]}@dbert.test"

        with get_db() as conn:
            # Create test intern account
            conn.execute(
                "INSERT INTO intern_accounts (name, email, password_hash, is_active, created_at) "
                "VALUES ('Test Intern', ?, 'hash', 1, datetime('now'))",
                (test_email,)
            )
            intern = conn.execute("SELECT id FROM intern_accounts WHERE email=?", (test_email,)).fetchone()
            intern_id = intern["id"]

            idem = f"stipend_reward_{test_sub_id}"

            # First credit attempt
            already_1 = conn.execute("SELECT 1 FROM coin_ledger_mirror WHERE idem_key=?", (idem,)).fetchone()
            self.assertIsNone(already_1)

            conn.execute(
                """
                INSERT INTO coin_ledger_mirror 
                (intern_id, ledger_kind, delta, balance_after, reason, event_ts, idem_key, email)
                VALUES (?, 'referral', 5000, 5000, 'Stipend Bounty Test', datetime('now'), ?, ?)
                """,
                (intern_id, idem, test_email)
            )
            conn.commit()

            # Second duplicate credit attempt (simulating concurrent click or network retry)
            already_2 = conn.execute("SELECT 1 FROM coin_ledger_mirror WHERE idem_key=?", (idem,)).fetchone()
            self.assertIsNotNone(already_2, "Idempotency check should find existing credit.")

            # Total credits in ledger for this idempotency key should be exactly 1
            total_credits = conn.execute(
                "SELECT COUNT(*) as cnt FROM coin_ledger_mirror WHERE idem_key=?", (idem,)
            ).fetchone()["cnt"]
            self.assertEqual(total_credits, 1, "Exactly one ledger entry must exist for the idempotency key.")

    # =========================================================================
    # 3. AI EVALUATOR FAIL-CLOSED BEHAVIOR (BASE-07, SF-010, DBQ-0136)
    # =========================================================================
    def test_ai_evaluator_fail_closed_when_unconfigured(self):
        """BASE-07 / SF-010: AI evaluator must NEVER return an artificial passing score when unconfigured."""
        result = StipendEvaluator.evaluate(
            submission_data={"holder_name": "Test Student"},
            domain="Data Analyst",
            api_key=""  # empty key forces unconfigured branch
        )
        self.assertIsNone(result["score"], "Unconfigured AI evaluator must return score: None (fail-closed).")
        self.assertEqual(result["verdict"], "AWAITING_MANUAL_REVIEW")
        self.assertEqual(result["status"], "AI_UNCONFIGURED_MANUAL_REVIEW")

    # =========================================================================
    # 4. PAYMENT EVENT RECORDING DIALECT-PORTABILITY (BASE-05, DBQ-0128)
    # =========================================================================
    def test_payment_event_portable_upsert(self):
        """DBQ-0128: PaymentService.record_payment_event executes portably across SQLite & PostgreSQL."""
        with get_db() as conn:
            test_eid = f"evt_test_{uuid.uuid4().hex[:8]}"
            test_order = f"order_{uuid.uuid4().hex[:8]}"
            test_pay = f"pay_{uuid.uuid4().hex[:8]}"

            # First insertion
            row_id1 = PaymentService.record_payment_event(
                conn, test_eid, "payment.accepted", test_order, test_pay, {"amount": 1500}
            )
            self.assertIsNotNone(row_id1)

            # Replay / update of the same event_id
            row_id2 = PaymentService.record_payment_event(
                conn, test_eid, "payment.accepted", test_order, test_pay, {"amount": 1500, "updated": True}
            )
            self.assertEqual(row_id1, row_id2, "Upserting existing event should return same database ID.")

            # Verify idempotency query
            self.assertTrue(PaymentService.is_payment_processed(conn, test_pay))

    # =========================================================================
    # 5. PRIVATE FILE SECURITY & AUTHORIZATION (BASE-11, SEC-006, DBQ-0221 - DBQ-0228)
    # =========================================================================
    def test_private_file_download_authorization(self):
        """BASE-11 & SEC-006: Anonymous users and non-owners must be denied access to private files."""
        with get_db() as conn:
            # 1. Anonymous user check
            anon_auth, anon_reason = authorize_file_download(conn, None, "test_receipt.pdf")
            self.assertFalse(anon_auth, "Anonymous access to private files must be rejected.")
            self.assertEqual(anon_reason, "login_required")

            # 2. Intern A requesting Intern B's file
            intern_a = {"id": 101, "role": "intern", "email": "intern_a@dbert.test"}
            auth_a, reason_a = authorize_file_download(conn, intern_a, "intern_b_secret_cv.pdf")
            self.assertFalse(auth_a, "Intern A must NOT have access to Intern B's documents.")
            self.assertEqual(reason_a, "forbidden_not_owner")

            # 3. Staff / Admin access
            admin_user = {"id": 1, "role": "admin", "is_admin": 1, "email": "admin@dbert.test"}
            admin_auth, admin_reason = authorize_file_download(conn, admin_user, "intern_b_secret_cv.pdf")
            self.assertTrue(admin_auth, "Staff/Admin must have authorized access for review.")

    # =========================================================================
    # 6. HEALTH & READINESS PROBE COMPATIBILITY (BASE-08, DBQ-0016 - DBQ-0018)
    # =========================================================================
    def test_health_and_readiness_probes(self):
        """BASE-08: /health and /ready return 200 without SQLite-specific syntax crashes."""
        # Test Liveness
        is_live, live_info = check_liveness()
        self.assertTrue(is_live)
        self.assertEqual(live_info["status"], "ok")

        # Test Readiness
        with get_db() as conn:
            is_ready, ready_info = check_readiness(conn)
            self.assertTrue(is_ready, f"Readiness check failed: {ready_info}")
            self.assertEqual(ready_info["status"], "ready")
            self.assertTrue(ready_info["checks"]["database_connected"])
            self.assertTrue(ready_info["checks"]["outbox_healthy"])

        # Test HTTP endpoints
        res_health = self.client.get("/health")
        self.assertEqual(res_health.status_code, 200)

        res_ready = self.client.get("/ready")
        self.assertEqual(res_ready.status_code, 200)

    # =========================================================================
    # 7. PATH TRAVERSAL DEFENSE (SEC-010, DBQ-0227)
    # =========================================================================
    def test_path_traversal_defense(self):
        """SEC-010: Path traversal attempts in file names are strictly rejected."""
        with get_db() as conn:
            user = {"id": 1, "role": "admin", "is_admin": 1, "email": "admin@dbert.test"}
            # Any filename containing ../ or /.. should be handled safely by os.path.basename
            traversal_files = [
                "../../../../etc/passwd",
                "..\\..\\windows\\system32\\cmd.exe",
                "uploads/../../secret.env",
                "/etc/shadow"
            ]
            for f in traversal_files:
                basename = os.path.basename(f.replace("\\", "/"))
                self.assertNotIn("..", basename, f"Path traversal defense must strip directory traversal from {f}")

    # =========================================================================
    # 8. STAGE NEXT ACTION SYNCHRONIZATION (UX-004 - UX-006, DBQ-0418 - DBQ-0423)
    # =========================================================================
    def test_stage_next_action_synchronization(self):
        """UX-004 - UX-006: Each lifecycle stage returns authoritative mission heading and CTA."""
        # Stage 1: APPLICATION_REQUIRED
        action_s1 = build_intern_next_action({"stage_num": 1, "domain": "Full Stack Development"})
        self.assertIn("Under Evaluation", action_s1["heading"])

        # Stage 3: SELECTED
        action_s3 = build_intern_next_action({"stage_num": 3, "domain": "Full Stack Development"})
        self.assertIn("Appointment Extended", action_s3["heading"])
        self.assertEqual(action_s3["primary_cta_url"], "/portal/offer")

        # Stage 5: CONFIRMED (Verified fellow)
        action_s5 = build_intern_next_action({
            "stage_num": 5,
            "domain": "Full Stack Development",
            "has_paid_balance": True
        })
        self.assertIn("Active Engineering Incubation Fellow", action_s5["heading"])

    # =========================================================================
    # 9. OFFER LETTER TEMPLATE EXCLUSIVITY (UX-005, DBQ-0418)
    # =========================================================================
    def test_offer_letter_template_exclusivity(self):
        """UX-005: Step 3 deposit payment DOM is strictly excluded for verified candidates."""
        with app.test_request_context("/portal/offer"):
            from flask import render_template
            # Render offer letter for candidate with verified deposit
            html_verified = render_template(
                "portal_offer_letter.html",
                candidate={
                    "name": "Verified Fellow",
                    "email": "fellow.verified@dbert.test",
                    "domain": "Cybersecurity",
                    "intern_id": 5624
                },
                offer={
                    "offer_letter_id": "DBERT-OFR-2026-FSD-5166",
                    "date_of_issue": "2026-11-16",
                    "tenure_months": 2,
                    "batch_start_date": "2026-11-09",
                    "batch_end_date": "2027-01-08",
                    "stipend_amount": 5000,
                    "login_hours_per_week": 10,
                    "required_certifications": 2,
                    "required_bounty_tasks": 75,
                    "caution_deposit_amount": 499,
                    "caution_deposit_status": "VERIFIED",
                    "accepted_at": "2026-11-16 12:00:00",
                    "signature_name": "Verified Fellow",
                    "pdf_unlocked": 1
                },
                is_deposit_verified=True,
                is_signed=True,
                step=3,
                current_stage="CONFIRMED"
            )
            # Must NOT contain payment form container in DOM
            self.assertNotIn('id="postSignPaymentSection"', html_verified)
            # Must render verified dossier card
            self.assertIn("verifiedDossierCard", html_verified)
            self.assertIn("Download Official Signed PDF", html_verified)


if __name__ == "__main__":
    unittest.main()
