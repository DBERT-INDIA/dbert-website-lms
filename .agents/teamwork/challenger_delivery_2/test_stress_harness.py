"""
c:\\Users\\user\\Desktop\\dbert-website-lms\\.agents\\teamwork\\challenger_delivery_2\\test_stress_harness.py
Empirical Adversarial Stress Test Harness for Email Delivery Architecture.
Author: challenger_delivery_2
Role: EMPIRICAL CHALLENGER (critic, specialist)

ZERO LIVE NETWORK CALLS: All tests run with mock transport or local database fixtures.
"""

import os
import sys
import time
import threading
import sqlite3
import smtplib
from pathlib import Path
from unittest.mock import patch, MagicMock

# Setup paths
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
PORTAL_DIR = WORKSPACE_ROOT / "apps" / "portal"
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

# Load environment
env_file = PORTAL_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

from services.delivery_service import (
    EmailPacer,
    EmailDeliveryService,
    DUMMY_EMAIL_DOMAINS,
    send_email
)
from app import app, _email_sig, get_db

# ANSI formatting
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def run_suite_1_email_pacer_concurrency():
    """
    Stress test EmailPacer concurrency, lock contention, and inter-message delays.
    Empirically verifies whether concurrent threads observe min_interval spacing.
    """
    print(f"\n{BOLD}======================================================================{RESET}")
    print(f"{BOLD}[SUITE 1] EmailPacer Multi-Threaded Concurrency & Race Condition Stress{RESET}")
    print(f"{BOLD}======================================================================{RESET}")

    interval = 0.1  # 100ms interval for empirical testing
    num_threads = 5
    pacer = EmailPacer(default_interval=interval)
    dispatches = []

    def pacer_worker(worker_id, barrier):
        barrier.wait()
        t_start = time.time()
        delay = pacer.wait_and_record("concurrency_test@dbert.in", interval=interval, dry_run=False)
        t_done = time.time()
        dispatches.append({
            "worker_id": worker_id,
            "start": t_start,
            "done": t_done,
            "elapsed": t_done - t_start,
            "delay": delay
        })

    barrier = threading.Barrier(num_threads)
    threads = [threading.Thread(target=pacer_worker, args=(i, barrier)) for i in range(num_threads)]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    dispatches.sort(key=lambda x: x["done"])

    print(f"Dispatched {num_threads} threads simultaneously (target interval: {interval}s):")
    for d in dispatches:
        print(f"  Thread {d['worker_id']}: start={d['start']:.4f}, done={d['done']:.4f}, elapsed={d['elapsed']:.4f}s, delay={d['delay']:.4f}s")

    consecutive_intervals = [
        dispatches[i]["done"] - dispatches[i-1]["done"] for i in range(1, len(dispatches))
    ]
    print(f"\nConsecutive intervals between finishes: {[round(x, 4) for x in consecutive_intervals]}")
    
    violations = [iv for iv in consecutive_intervals if iv < (interval * 0.8)]
    min_iv = min(consecutive_intervals) if consecutive_intervals else 0.0

    print(f"Minimum observed interval: {min_iv:.4f}s (required: >= {interval * 0.8:.4f}s)")
    print(f"Rate pacing violations: {len(violations)} / {len(consecutive_intervals)}")

    if len(violations) > 0:
        print(f"{RED}[FAIL] EmailPacer concurrency failure detected!{RESET}")
        print(f"       Threads awoke and dispatched simultaneously without inter-message spacing.")
        return False, {
            "num_threads": num_threads,
            "min_interval": interval,
            "consecutive_intervals": consecutive_intervals,
            "violations": len(violations),
            "min_observed": min_iv
        }
    else:
        print(f"{GREEN}[PASS] EmailPacer strictly paced all dispatches across threads.{RESET}")
        return True, {"violations": 0}


def run_suite_2_synthetic_domain_interception():
    """
    Stress test synthetic domain interception against RFC 2606 and dummy domains.
    Verifies zero network socket calls are made for dummy domains.
    """
    print(f"\n{BOLD}======================================================================{RESET}")
    print(f"{BOLD}[SUITE 2] Synthetic Domain Interception (DUMMY_EMAIL_DOMAINS) Stress{RESET}")
    print(f"{BOLD}======================================================================{RESET}")

    service = EmailDeliveryService(pacer=EmailPacer(default_interval=0.0))
    test_cases = [
        # Explicitly required test addresses
        ("test@example.com", True, "RFC 2606 example domain"),
        ("candidate@test.invalid", True, "RFC 2606 invalid TLD"),
        # Additional RFC / synthetic edge cases
        ("user@example.org", True, "RFC 2606 example.org"),
        ("user@example.net", True, "RFC 2606 example.net"),
        ("candidate@sub.example.com", True, "Subdomain under example.com"),
        ("user@domain.invalid", True, "Subdomain under .invalid"),
        ("tester@corp.test", True, "RFC 2606 .test TLD"),
        ("admin@localhost", True, "Localhost domain"),
        ("fake@fakemail.com", True, "Synthetic disposal domain"),
        ("temp@mailinator.com", True, "Synthetic disposal domain"),
        ("no_at_symbol_address", True, "Malformed address without @"),
        # Legitimate addresses (must NOT be intercepted)
        ("ain.sharma.abhinav@gmail.com", False, "Legitimate target 1"),
        ("ajnatechrpa@gmail.com", False, "Legitimate target 2"),
        ("student@dbert.in", False, "Legitimate organizational domain")
    ]

    results = []
    failures = []

    for email, expect_intercept, note in test_cases:
        is_dummy = service.is_dummy_domain(email)
        
        # Test send_email behavior under mock transport
        with patch("smtplib.SMTP_SSL") as mock_ssl, patch("smtplib.SMTP") as mock_smtp, patch("requests.post") as mock_post:
            res = service.send_email(
                to=email,
                subject="Synthetic Domain Interception Test",
                html_content="<p>Interception check</p>",
                dry_run=False
            )
            net_attempted = mock_ssl.called or mock_smtp.called or mock_post.called

            passed = (is_dummy == expect_intercept)
            if expect_intercept and net_attempted:
                passed = False

            status_str = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
            print(f"  [{status_str}] {email:<30} -> is_dummy: {str(is_dummy):<5} (expected: {str(expect_intercept):<5}) | Network attempted: {net_attempted} | {note}")
            
            results.append({
                "email": email,
                "is_dummy": is_dummy,
                "expected": expect_intercept,
                "network_attempted": net_attempted,
                "passed": passed,
                "note": note
            })

            if not passed:
                failures.append(email)

    if failures:
        print(f"\n{RED}[FAIL] Synthetic domain interception failed for {len(failures)} addresses:{RESET}")
        for f in failures:
            print(f"       - {f}")
        return False, results
    else:
        print(f"\n{GREEN}[PASS] All synthetic domains properly intercepted without network calls.{RESET}")
        return True, results


def run_suite_3_rfc8058_unsubscribe_and_csrf():
    """
    Stress test RFC 8058 One-Click unsubscribe POST and CSRF bypass handling.
    """
    print(f"\n{BOLD}======================================================================{RESET}")
    print(f"{BOLD}[SUITE 3] RFC 8058 One-Click POST & CSRF Exemption Stress{RESET}")
    print(f"{BOLD}======================================================================{RESET}")

    client = app.test_client()
    test_email = "rfc8058_stress@dbert.in"

    # Seed test user
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO intern_accounts (name, email, password_hash, newsletter_opt_in) VALUES (?, ?, ?, ?)",
            ("RFC8058 Tester", test_email, "dummyhash", 1)
        )
        conn.commit()

    # Verify seed
    with get_db() as conn:
        row = conn.execute("SELECT newsletter_opt_in FROM intern_accounts WHERE email = ?", (test_email,)).fetchone()
        assert row and row["newsletter_opt_in"] == 1, "Failed to seed intern_accounts"

    valid_token = _email_sig("unsub", test_email)
    tampered_token = "invalid_tampered_token_9999"

    suite_failures = []

    # 1. Valid RFC 8058 POST without CSRF token
    resp_valid_post = client.post(
        f"/unsubscribe?e={test_email}&t={valid_token}",
        data={"List-Unsubscribe": "One-Click"}
    )
    with get_db() as conn:
        row_after_valid = conn.execute("SELECT newsletter_opt_in FROM intern_accounts WHERE email = ?", (test_email,)).fetchone()
        opt_in_valid = row_after_valid["newsletter_opt_in"] if row_after_valid else None

    print(f"  Test 3.1: Valid POST (no CSRF cookie/header):")
    print(f"            HTTP Status: {resp_valid_post.status_code} (Expected: 200)")
    print(f"            Database newsletter_opt_in: {opt_in_valid} (Expected: 0)")
    if resp_valid_post.status_code != 200 or opt_in_valid != 0:
        suite_failures.append("Test 3.1: Valid RFC 8058 POST did not return 200 or did not unsubscribe")
        print(f"            {RED}[FAIL]{RESET}")
    else:
        print(f"            {GREEN}[PASS]{RESET}")

    # Reset opt-in to 1
    with get_db() as conn:
        conn.execute("UPDATE intern_accounts SET newsletter_opt_in = 1 WHERE email = ?", (test_email,))
        conn.commit()

    # 2. Invalid RFC 8058 POST with tampered token
    resp_invalid_post = client.post(
        f"/unsubscribe?e={test_email}&t={tampered_token}",
        data={"List-Unsubscribe": "One-Click"}
    )
    with get_db() as conn:
        row_after_invalid = conn.execute("SELECT newsletter_opt_in FROM intern_accounts WHERE email = ?", (test_email,)).fetchone()
        opt_in_invalid = row_after_invalid["newsletter_opt_in"] if row_after_invalid else None

    print(f"  Test 3.2: Invalid POST (tampered HMAC token):")
    print(f"            HTTP Status: {resp_invalid_post.status_code}")
    print(f"            Database newsletter_opt_in: {opt_in_invalid} (Expected: 1 - NOT modified)")
    if opt_in_invalid != 1:
        suite_failures.append("Test 3.2: Tampered HMAC token unexpectedly modified database opt-in!")
        print(f"            {RED}[FAIL]{RESET}")
    else:
        print(f"            {GREEN}[PASS]{RESET}")

    # 3. Global CSRF Protection Verification (Protected route without CSRF token)
    resp_csrf_check = client.post("/login", data={"email": test_email, "password": "pass"})
    print(f"  Test 3.3: Protected route POST (/login without CSRF token):")
    print(f"            HTTP Status: {resp_csrf_check.status_code} (Expected: 403 CSRF Reject)")
    if resp_csrf_check.status_code != 403:
        suite_failures.append(f"Test 3.3: Global CSRF protection not enforcing 403 on /login (got {resp_csrf_check.status_code})")
        print(f"            {RED}[FAIL]{RESET}")
    else:
        print(f"            {GREEN}[PASS]{RESET}")

    # 4. Valid GET request to /unsubscribe
    resp_valid_get = client.get(f"/unsubscribe?e={test_email}&t={valid_token}")
    html_get = resp_valid_get.data.decode("utf-8")
    print(f"  Test 3.4: Browser GET request with valid token:")
    print(f"            HTTP Status: {resp_valid_get.status_code} (Expected: 200)")
    print(f"            Contains confirmation: {'unsubscribed' in html_get.lower()}")
    if resp_valid_get.status_code != 200 or "unsubscribed" not in html_get.lower():
        suite_failures.append("Test 3.4: Valid GET request did not display unsubscribed confirmation")
        print(f"            {RED}[FAIL]{RESET}")
    else:
        print(f"            {GREEN}[PASS]{RESET}")

    # 5. Invalid GET request to /unsubscribe
    resp_invalid_get = client.get(f"/unsubscribe?e={test_email}&t={tampered_token}")
    html_inv_get = resp_invalid_get.data.decode("utf-8")
    print(f"  Test 3.5: Browser GET request with invalid token:")
    print(f"            HTTP Status: {resp_invalid_get.status_code} (Expected: 200)")
    print(f"            Contains invalid warning: {'invalid or expired' in html_inv_get.lower()}")
    if resp_invalid_get.status_code != 200 or "invalid or expired" not in html_inv_get.lower():
        suite_failures.append("Test 3.5: Invalid GET request did not display invalid/expired warning")
        print(f"            {RED}[FAIL]{RESET}")
    else:
        print(f"            {GREEN}[PASS]{RESET}")

    if suite_failures:
        print(f"\n{RED}[FAIL] Suite 3 encountered {len(suite_failures)} failures.{RESET}")
        return False, suite_failures
    else:
        print(f"\n{GREEN}[PASS] Suite 3: RFC 8058 One-Click & CSRF handling verified.{RESET}")
        return True, []


def main():
    print(f"\n{BOLD}######################################################################{RESET}")
    print(f"{BOLD} DBERT EMAIL INFRASTRUCTURE EMPIRICAL STRESS TEST HARNESS {RESET}")
    print(f"{BOLD} Challenger: challenger_delivery_2 | Mode: Zero Live Network Calls {RESET}")
    print(f"{BOLD}######################################################################{RESET}")

    s1_pass, s1_data = run_suite_1_email_pacer_concurrency()
    s2_pass, s2_data = run_suite_2_synthetic_domain_interception()
    s3_pass, s3_data = run_suite_3_rfc8058_unsubscribe_and_csrf()

    print(f"\n{BOLD}======================================================================{RESET}")
    print(f"{BOLD} FINAL SUITE SUMMARY {RESET}")
    print(f"{BOLD}======================================================================{RESET}")
    print(f" Suite 1 (EmailPacer Concurrency & Rate Limiting):    {'PASS' if s1_pass else 'FAIL (Race Condition / Burst)'}")
    print(f" Suite 2 (Synthetic Domain Interception):             {'PASS' if s2_pass else 'FAIL (candidate@test.invalid leaked)'}")
    print(f" Suite 3 (RFC 8058 One-Click POST & CSRF Bypass):     {'PASS' if s3_pass else 'FAIL'}")

    all_passed = s1_pass and s2_pass and s3_pass
    verdict = "APPROVE" if all_passed else "REQUEST_CHANGES"
    verdict_color = GREEN if all_passed else RED
    print(f"\n Adversarial Verdict: {verdict_color}{BOLD}{verdict}{RESET}")
    print(f"{BOLD}======================================================================{RESET}\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
