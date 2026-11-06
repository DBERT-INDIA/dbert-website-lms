import sys
import os
import time
import threading
import re
import socket
from email.utils import formataddr
from pathlib import Path
from unittest.mock import patch

# Setup sys.path
PORTAL_DIR = Path(__file__).resolve().parents[3] / "apps" / "portal"
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from services.delivery_service import (
    EmailDeliveryService,
    EmailPacer,
    DeliveryResult,
    build_mime_message,
    DUMMY_EMAIL_DOMAINS,
    EMAIL_REGEX
)

class NetworkAttemptError(Exception):
    pass

def forbid_network():
    def _disallow(*args, **kwargs):
        raise NetworkAttemptError(f"Network attempt detected: {args}, {kwargs}")
    return patch.multiple("socket.socket", connect=_disallow, connect_ex=_disallow)

def test_pacer_high_concurrency():
    print("\n--- Test: EmailPacer High Concurrency (10 threads, 0.05s interval) ---")
    interval = 0.05
    num_threads = 10
    pacer = EmailPacer(default_interval=interval)
    dispatches = []

    def worker(tid, barrier):
        barrier.wait()
        t0 = time.time()
        delay = pacer.wait_and_record("load_test@dbert.in", interval=interval, dry_run=False)
        t1 = time.time()
        dispatches.append((tid, t0, t1, delay))

    barrier = threading.Barrier(num_threads)
    threads = [threading.Thread(target=worker, args=(i, barrier)) for i in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    dispatches.sort(key=lambda x: x[2])  # sort by completion time
    finishes = [d[2] for d in dispatches]
    intervals = [finishes[i] - finishes[i-1] for i in range(1, len(finishes))]
    print(f"Observed intervals: {[round(x, 4) for x in intervals]}")
    violations = [x for x in intervals if x < (interval * 0.75)]
    print(f"Violations (< {interval*0.75:.4f}s): {len(violations)}")
    assert len(violations) == 0, f"Found {len(violations)} rate violations in EmailPacer"
    print("[PASS] EmailPacer successfully staggered 10 concurrent threads without race conditions.")

def test_synthetic_domains():
    print("\n--- Test: Synthetic Domain Interception Exhaustive ---")
    service = EmailDeliveryService()
    test_cases = [
        ("test@example.com", True),
        ("user@sub.example.com", True),
        ("candidate@test.invalid", True),
        ("foo@bar.invalid", True),
        ("alice@example.org", True),
        ("bob@deep.sub.example.net", True),
        ("test@localhost", True),
        ("admin@server.localhost", True),
        ("user@test.com", True),
        ("dev@dbert.test", True),
        ("intern@sub.dbert.test", True),
        ("temp@mailinator.com", True),
        ("fake@fakemail.com", True),
        ("no_at_symbol", True),
        (None, True),
        (1234, True),
        (["list@example.com"], True),
        ("ain.sharma.abhinav@gmail.com", False),
        ("ajnatechrpa@gmail.com", False),
        ("support@dbert.in", False),
        ("admissions@lms.dbert.in", False),
    ]

    for addr, expected_dummy in test_cases:
        actual = service.is_dummy_domain(addr)
        assert actual == expected_dummy, f"Failed for {addr}: expected {expected_dummy}, got {actual}"
    print(f"[PASS] All {len(test_cases)} synthetic domain test cases evaluated correctly.")

def test_rfc5322_regex():
    print("\n--- Test: Strict RFC 5322 Regex Validation ---")
    valid_emails = [
        "ain.sharma.abhinav@gmail.com",
        "ajnatechrpa@gmail.com",
        "support@dbert.in",
        "user.name+tag@sub.domain.co.uk",
        "first_last-123@example.org"
    ]
    invalid_emails = [
        "user@",
        "@domain.com",
        "user@@double-at.com",
        "user name@dbert.in",
        "user@domain..com",
        "user\r\n@domain.com",
        "user\n@domain.com",
        "user\x00@domain.com",
        "user@domain",
        ""
    ]

    for v in valid_emails:
        assert EMAIL_REGEX.match(v) is not None, f"Valid email rejected: {v}"
    for inv in invalid_emails:
        assert EMAIL_REGEX.match(inv) is None, f"Invalid email accepted: {inv}"
    print(f"[PASS] EMAIL_REGEX correctly categorized {len(valid_emails)} valid and {len(invalid_emails)} invalid addresses.")

def test_formataddr_and_mime():
    print("\n--- Test: formataddr RFC 2047 addr-spec isolation ---")
    msg = build_mime_message(
        to_email="ajnatechrpa@gmail.com",
        subject="Test Subject with\r\nNewline Injection Attempt",
        html_content="<p>Test</p>",
        from_name="DBERT शिक्षा एवं प्रौद्योगिकी",
        from_email="support@dbert.in"
    )
    # Check Subject CRLF sanitization
    assert "\r" not in msg["Subject"] and "\n" not in msg["Subject"]
    assert "Test Subject with Newline Injection Attempt" == msg["Subject"]

    # Check From header
    from_header = msg["From"]
    print(f"From Header: {from_header}")
    assert "<support@dbert.in>" in from_header
    # Check serialized bytes
    raw_bytes = msg.as_bytes()
    assert b"<support@dbert.in>" in raw_bytes
    print("[PASS] From header properly isolates <support@dbert.in> in clear ASCII and sanitizes Subject.")

def test_preflight_guard_zero_network():
    print("\n--- Test: Pre-flight Guard with Strict Network Prohibition ---")
    service = EmailDeliveryService()
    
    with forbid_network():
        # Dry-run with legitimate addresses
        r1 = service.send_email(to="ain.sharma.abhinav@gmail.com", subject="Test", html_content="<p>Test</p>", dry_run=True)
        assert r1.success is True
        assert r1.provider == "dry_run"
        assert r1.diagnostics.get("dry_run") is True

        r2 = service.send_email(to="ajnatechrpa@gmail.com", subject="Test", html_content="<p>Test</p>", dry_run=True)
        assert r2.success is True
        assert r2.provider == "dry_run"

        # Interception of synthetic domain
        r3 = service.send_email(to="candidate@test.invalid", subject="Test", html_content="<p>Test</p>", dry_run=False)
        assert r3.success is False
        assert r3.provider == "hard_bounce_guard"
        assert r3.diagnostics.get("intercepted") is True

        # Malformed recipient
        r4 = service.send_email(to="bad_recipient@", subject="Test", html_content="<p>Test</p>", dry_run=False)
        assert r4.success is False
        assert r4.provider == "hard_bounce_guard"

        # Non-string recipient
        r5 = service.send_email(to=12345, subject="Test", html_content="<p>Test</p>", dry_run=False)
        assert r5.success is False
        assert r5.provider == "hard_bounce_guard"

        # CRLF injection
        r6 = service.send_email(to="target@gmail.com\r\nBcc: evil@attacker.com", subject="Test", html_content="<p>Test</p>", dry_run=False)
        assert r6.success is False
        assert r6.provider == "hard_bounce_guard"

    print("[PASS] Pre-flight guards and dry-run execution triggered ZERO network socket calls.")

if __name__ == "__main__":
    test_pacer_high_concurrency()
    test_synthetic_domains()
    test_rfc5322_regex()
    test_formataddr_and_mime()
    test_preflight_guard_zero_network()
    print("\n=== ALL INDEPENDENT FORENSIC TESTS PASSED (100% CLEAN) ===")
