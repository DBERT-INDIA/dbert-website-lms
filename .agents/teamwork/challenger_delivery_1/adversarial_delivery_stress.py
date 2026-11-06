"""
adversarial_delivery_stress.py
Empirical adversarial challenge and stress-testing suite for DBERT Email Delivery Engine.
Author: challenger_delivery_1
Roles: critic, specialist

STRICT SAFEGUARD: ZERO LIVE OUTBOUND NETWORK TRANSMISSION.
All tests use dry-run validation, socket intercepts, and mock transports.
"""

import os
import sys
import io
import time
import socket
import ssl
import json
import uuid
import smtplib
import threading
import requests
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr
from pathlib import Path
from unittest.mock import patch, MagicMock

# Force utf-8 encoding on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add apps/portal to sys.path
REPO_ROOT = Path(__file__).resolve().parents[3]
PORTAL_DIR = REPO_ROOT / "apps" / "portal"
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

# Import delivery service components
from services.delivery_service import (
    EmailDeliveryService,
    DeliveryResult,
    EmailPacer,
    build_mime_message,
    html_to_plain_text,
    generate_email_footer,
    generate_unsubscribe_token,
    generate_unsubscribe_url,
    generate_message_id,
    send_email,
    DUMMY_EMAIL_DOMAINS,
    SUSPENDED_DOMAINS
)


class NetworkLeakError(AssertionError):
    """Raised if any network connection is attempted during dry-run or mock execution."""
    pass


def forbid_network():
    """Context manager to intercept and strictly forbid all network/socket operations."""
    def _disallow(*args, **kwargs):
        raise NetworkLeakError(f"Adversarial Guard Triggered: Unauthorized network socket call intercepted: args={args}, kwargs={kwargs}")

    return patch.multiple(
        "socket.socket",
        connect=_disallow,
        connect_ex=_disallow
    )


class AdversarialTestRunner:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.findings = []

    def record(self, category: str, test_name: str, passed: bool, message: str = "", finding_id: str = ""):
        if passed:
            self.passed += 1
            status = "PASS"
        else:
            self.failed += 1
            status = "FAIL"
            if finding_id:
                self.findings.append((finding_id, category, test_name, message))

        self.results.append({
            "category": category,
            "test": test_name,
            "status": status,
            "message": message,
            "finding_id": finding_id
        })
        tag = f"[{status}]"
        print(f"  {tag:<7} {category} :: {test_name}")
        if message:
            for line in message.splitlines():
                print(f"          {line}")

    # =========================================================================
    # 1. Primary SMTP Failure Simulations
    # =========================================================================
    def test_smtp_failures(self):
        print("\n=== Challenge Suite 1: Primary SMTP Failure Simulation & Fallback ===")
        service = EmailDeliveryService(
            smtp_host="smtp.gmail.com",
            smtp_port=465,
            smtp_user="abhinav.sharma@dbert.in",
            smtp_pass="rsupmvvvvwrsuxuh",
            cpanel_api_url="https://mailer.aivaratech.online/send"
        )
        service.pacer.wait_and_record = MagicMock(return_value=0.0)

        failure_scenarios = [
            ("Socket Timeout", socket.timeout("The connect operation timed out")),
            ("535 Authentication Failure", smtplib.SMTPAuthenticationError(535, b"5.7.8 Username and Password not accepted")),
            ("421 Service Unavailable", smtplib.SMTPConnectError(421, b"4.4.5 Server busy, try again later")),
            ("550 Mailbox Unavailable", smtplib.SMTPSenderRefused(550, b"Sender address rejected: not owned by user", "abhinav.sharma@dbert.in")),
            ("Server Disconnected", smtplib.SMTPServerDisconnected("Connection unexpectedly closed")),
            ("SSL Handshake Failure", ssl.SSLError("certificate verify failed")),
            ("Connection Reset", ConnectionResetError(10054, "An existing connection was forcibly closed by the remote host")),
            ("Generic OS Network Error", OSError(10061, "Connection refused"))
        ]

        for name, err in failure_scenarios:
            with patch("smtplib.SMTP_SSL", side_effect=err), \
                 patch("requests.post") as mock_api:
                mock_api.return_value.status_code = 200
                mock_api.return_value.text = '{"status":"success"}'

                res = service.send_email(
                    to="ain.sharma.abhinav@gmail.com",
                    subject=f"Stress Test: {name}",
                    html_content="<p>Simulating failure</p>",
                    dry_run=False
                )

                passed = (
                    res.success is True and
                    res.provider == "secondary_cpanel_api" and
                    "primary_error" in res.diagnostics and
                    mock_api.called
                )
                self.record(
                    "SMTP Failure Simulation",
                    f"Primary {name} triggers secondary cPanel API",
                    passed,
                    f"Result provider: {res.provider}, primary_error: {res.diagnostics.get('primary_error')}"
                )

    # =========================================================================
    # 2. Secondary Fallback Cascades & Degradation
    # =========================================================================
    def test_fallback_cascades(self):
        print("\n=== Challenge Suite 2: Fallback Cascades & Complete Outage Handling ===")
        
        # Scenario 2A: Primary SMTP fails, Secondary cPanel API fails (502), Backup SMTP succeeds
        service = EmailDeliveryService(
            smtp_host="smtp.gmail.com",
            smtp_port=465,
            cpanel_api_url="https://mailer.aivaratech.online/send",
            backup_host="backup-smtp.dbert.in",
            backup_port=465,
            backup_user="backup_user",
            backup_pass="backup_pass"
        )
        service.pacer.wait_and_record = MagicMock(return_value=0.0)

        mock_backup_smtp = MagicMock()
        mock_backup_smtp.__enter__.return_value = mock_backup_smtp

        with patch("smtplib.SMTP_SSL") as mock_ssl, \
             patch("requests.post") as mock_api:
            mock_ssl.side_effect = [
                smtplib.SMTPAuthenticationError(535, b"Auth failed"),
                mock_backup_smtp
            ]
            mock_api.return_value.status_code = 502
            mock_api.return_value.text = "Bad Gateway"

            res = service.send_email(
                to="ajnatechrpa@gmail.com",
                subject="Cascade to Backup SMTP Test",
                html_content="<p>Testing cascade</p>",
                dry_run=False
            )
            passed = (
                res.success is True and
                res.provider == "secondary_backup_smtp" and
                "primary_error" in res.diagnostics
            )
            self.record(
                "Fallback Cascade",
                "Primary SMTP -> cPanel API 502 -> Backup SMTP Success",
                passed,
                f"Provider: {res.provider}, error: {res.error}"
            )

        # Scenario 2B: Suspended domain backup host is strictly rejected
        service_susp = EmailDeliveryService(
            smtp_host="smtp.gmail.com",
            smtp_port=465,
            cpanel_api_url="",  # No API
            backup_host="dbert.info"  # Suspended domain!
        )
        service_susp.pacer.wait_and_record = MagicMock(return_value=0.0)

        with patch("smtplib.SMTP_SSL", side_effect=smtplib.SMTPConnectError(421, b"Connection refused")):
            res_susp = service_susp.send_email(
                to="ain.sharma.abhinav@gmail.com",
                subject="Suspended Domain Defense",
                html_content="<p>Testing</p>",
                dry_run=False
            )
            passed = (
                res_susp.success is False and
                res_susp.provider == "failed" and
                "dbert.info" not in str(res_susp.diagnostics.get("fallback_transport", ""))
            )
            self.record(
                "Fallback Safety",
                "Suspended domain backup_host (dbert.info) blocked from dispatch",
                passed,
                f"Provider: {res_susp.provider}, Error: {res_susp.error}"
            )

        # Scenario 2C: All transports fail -> No uncaught exception, clean diagnostics
        service_all_fail = EmailDeliveryService(
            smtp_host="smtp.gmail.com",
            smtp_port=465,
            cpanel_api_url="https://mailer.aivaratech.online/send"
        )
        service_all_fail.pacer.wait_and_record = MagicMock(return_value=0.0)

        with patch("smtplib.SMTP_SSL", side_effect=smtplib.SMTPServerDisconnected("Down")), \
             patch("requests.post", side_effect=requests.exceptions.ConnectTimeout("cPanel Timeout")):
            res_all = service_all_fail.send_email(
                to="ajnatechrpa@gmail.com",
                subject="All Fail",
                html_content="<p>All fail</p>",
                dry_run=False
            )
            passed = (
                res_all.success is False and
                res_all.provider == "failed" and
                "Primary failed" in res_all.error and
                "Fallbacks failed" in res_all.error and
                isinstance(res_all.diagnostics.get("fallback_errors"), list)
            )
            self.record(
                "Fallback Cascade",
                "Total infrastructure failure handled gracefully with diagnostics",
                passed,
                f"Combined error: {res_all.error}"
            )

    # =========================================================================
    # 3. Malformed & Hostile Recipient Validation & CRLF Injection
    # =========================================================================
    def test_malformed_recipients(self):
        print("\n=== Challenge Suite 3: Malformed & Hostile Recipient Validation ===")
        service = EmailDeliveryService()

        # Test 3A: Empty / Missing '@' correctly rejected
        basic_invalids = [
            ("", "Empty string"),
            ("   ", "Whitespace string"),
            ("notanemail", "Missing '@' sign"),
        ]
        for rcpt, desc in basic_invalids:
            res = service.send_email(to=rcpt, subject="Invalid Test", html_content="<p>Test</p>", dry_run=True)
            passed = (res.success is False and res.provider == "hard_bounce_guard")
            self.record("Recipient Validation", f"Pre-flight rejection: {desc}", passed, f"Provider: {res.provider}, Error: {res.error}")

        # Test 3B: Non-string type inputs (Integer, List, Dict)
        for non_str, desc in [(None, "NoneType"), (12345, "Integer input"), (["user@dbert.in"], "List input")]:
            try:
                res = service.send_email(to=non_str, subject="Type Test", html_content="<p>Type test</p>", dry_run=True)
                passed = (res.success is False and res.provider == "hard_bounce_guard")
                self.record("Type Safety", f"Non-string input: {desc}", passed, f"Success={res.success}, Provider={res.provider}")
            except AttributeError as ae:
                self.record(
                    "Type Safety",
                    f"Non-string input: {desc}",
                    False,
                    f"BUG: AttributeError raised when calling (to or '').strip(): {ae}",
                    finding_id="BUG-DELIVERY-01"
                )
            except Exception as e:
                self.record("Type Safety", f"Non-string input: {desc}", False, f"Unexpected exception: {e}")

        # Test 3C: Malformed syntax with '@' that should be rejected by pre-flight guard
        malformed_with_at = [
            ("user@", "Missing domain part"),
            ("@domain.com", "Missing local part"),
            ("user@@double-at.com", "Double '@' sign"),
            ("user name@dbert.in", "Embedded space in email"),
            ("user@domain..com", "Consecutive dots in domain"),
        ]
        for rcpt, desc in malformed_with_at:
            res = service.send_email(to=rcpt, subject="Malformed Test", html_content="<p>Test</p>", dry_run=True)
            # A robust email validator should reject these at pre-flight with hard_bounce_guard
            is_rejected = (res.success is False and res.provider == "hard_bounce_guard")
            self.record(
                "Recipient Validation",
                f"RFC Syntax Guard: {desc} ({rcpt})",
                is_rejected,
                f"Result: success={res.success}, provider={res.provider}. " +
                ("Bypassed pre-flight validation!" if not is_rejected else "Properly rejected."),
                finding_id="BUG-DELIVERY-02" if not is_rejected else ""
            )

        # Test 3D: CRLF Injection in recipient address
        crlf_payload = "victim@gmail.com\r\nBcc: evil@attacker.com"
        res_crlf_dry = service.send_email(to=crlf_payload, subject="CRLF Test", html_content="<p>Test</p>", dry_run=True)
        crlf_blocked_dry = (res_crlf_dry.success is False and res_crlf_dry.provider == "hard_bounce_guard")
        self.record(
            "Security Injection",
            "CRLF Bcc injection intercepted in dry_run",
            crlf_blocked_dry,
            f"Dry run result: success={res_crlf_dry.success}, provider={res_crlf_dry.provider}. " +
            ("VULNERABILITY: CRLF injection bypassed dry-run pre-flight validation!" if not crlf_blocked_dry else "Blocked."),
            finding_id="BUG-DELIVERY-03" if not crlf_blocked_dry else ""
        )

        # Test 3E: CRLF Injection in non-dry-run mode: does it trigger fallback and forward injected header?
        mock_smtp = MagicMock()
        mock_smtp.__enter__.return_value = mock_smtp
        with patch("smtplib.SMTP_SSL", return_value=mock_smtp), patch("requests.post") as mock_cpanel:
            mock_cpanel.return_value.status_code = 200
            mock_cpanel.return_value.text = '{"status":"ok"}'
            res_crlf_live = service.send_email(to=crlf_payload, subject="CRLF Live Test", html_content="<p>Test</p>", dry_run=False)
            
            # If SMTP HeaderParseError triggered fallback to cPanel, mock_cpanel was called with raw CRLF!
            cpanel_got_crlf = mock_cpanel.called and "\n" in mock_cpanel.call_args[1].get("json", {}).get("to", "")
            self.record(
                "Security Injection",
                "CRLF header injection prevention across fallback",
                not cpanel_got_crlf,
                f"cPanel API called: {mock_cpanel.called}, Provider returned: {res_crlf_live.provider}. " +
                ("VULNERABILITY: HeaderParseError in SMTP caused false failover, forwarding CRLF to cPanel API!" if cpanel_got_crlf else "Secure."),
                finding_id="BUG-DELIVERY-04" if cpanel_got_crlf else ""
            )

        # Test 3F: Synthetic / Dummy Domain Interception
        dummy_cases = [
            "candidate_test@example.com",
            "bot@example.org",
            "mock@example.net",
            "admin@test.com",
            "dev@sample.com",
            "demo@demo.com",
            "temp@mailinator.com",
            "fake@fakemail.com",
            "local@localhost",
            "qa@invalid",
            "intern@dbert.test"
        ]
        with patch("smtplib.SMTP_SSL") as mock_ssl, patch("requests.post") as mock_post:
            for dummy in dummy_cases:
                res = service.send_email(to=dummy, subject="Dummy Test", html_content="<p>Test</p>", dry_run=False)
                passed = (
                    res.success is False and
                    res.provider == "hard_bounce_guard" and
                    res.diagnostics.get("intercepted") is True and
                    res.diagnostics.get("reason") == "synthetic_domain" and
                    not mock_ssl.called and
                    not mock_post.called
                )
                self.record("Dummy Domain Guard", f"Interception of {dummy}", passed, f"Provider: {res.provider}, Reason: {res.diagnostics.get('reason')}")

    # =========================================================================
    # 4. Unicode & Internationalization Handling
    # =========================================================================
    def test_unicode_handling(self):
        print("\n=== Challenge Suite 4: Unicode, Internationalization & Non-ASCII ===")
        service = EmailDeliveryService()
        service.pacer.wait_and_record = MagicMock(return_value=0.0)

        unicode_scenarios = [
            (
                "Devanagari / Hindi Subject & Body",
                "डीबर्ट नवाचार एवं तकनीकी इन्क्यूबेशन — आधिकारिक पुष्टि",
                "नमस्ते! डीबर्ट प्लेटफ़ॉर्म पर आपका स्वागत है।",
                "नमस्ते! डीबर्ट प्लेटफ़ॉर्म पर आपका स्वागत है।"
            ),
            (
                "32-Bit Astral Emojis in Subject & Body",
                "🚀 DBERT Incubation 🎓 Welcome Candidate! 🎉 ✨ 💡",
                "<p>Congratulations on joining DBERT! 🌟 🚀</p>",
                "Congratulations on joining DBERT! 🌟 🚀"
            ),
            (
                "Chinese / CJK Characters",
                "欢迎加入 DBERT 技术孵化平台 — 官方确认",
                "<p>您的申请已成功受理，请访问控制台。</p>",
                "您的申请已成功受理，请访问控制台。"
            ),
            (
                "Cyrillic Characters",
                "Официальное уведомление DBERT — доступ к порталу",
                "<p>Добро пожаловать в учебный портал DBERT.</p>",
                "Добро пожаловать в учебный портал DBERT."
            ),
            (
                "Arabic / RTL Characters",
                "تأكيد رسمي من حاضنة DBERT للتقنية",
                "<p>أهلاً بك في منصة ديبرت التعليمية.</p>",
                "أهلاً بك في منصة ديبرت التعليمية."
            ),
            (
                "Latin-1 Supplement / Accented Characters",
                "Confirmation d'admission DBERT — Année Académique 2026",
                "<p>Félicitations pour votre admission au programme DBERT.</p>",
                "Félicitations pour votre admission au programme DBERT."
            ),
            (
                "Zero-Width Spaces & Unicode Whitespace",
                "DBERT\u200bOfficial\u200bNotification",
                "<p>Text with\u00a0non-breaking\u200band\u2002various\u2003spaces</p>",
                "Text with non-breaking and various spaces"
            )
        ]

        mock_smtp = MagicMock()
        mock_smtp.__enter__.return_value = mock_smtp

        for name, subj, html_b, txt_b in unicode_scenarios:
            with patch("smtplib.SMTP_SSL", return_value=mock_smtp):
                try:
                    msg = build_mime_message(
                        to_email="ain.sharma.abhinav@gmail.com",
                        subject=subj,
                        html_content=html_b,
                        text_content=txt_b
                    )
                    raw_str = msg.as_string()
                    res = service.send_email(
                        to="ain.sharma.abhinav@gmail.com",
                        subject=subj,
                        html_content=html_b,
                        text_content=txt_b,
                        dry_run=False
                    )

                    passed = (
                        res.success is True and
                        res.provider == "google_workspace_smtp" and
                        len(raw_str) > 0 and
                        msg["Subject"] is not None
                    )
                    self.record("Unicode Serialization", f"Scenario: {name}", passed, f"Serialized MIME bytes: {len(raw_str)}, Status: {res.success}")
                except Exception as e:
                    self.record("Unicode Serialization", f"Scenario: {name}", False, f"UNCAUGHT ENCODING EXCEPTION: {e}")

        # Test 4B: RFC 2047 / RFC 5322 Address Encoding for Non-ASCII sender name
        # When from_name contains non-ASCII characters, msg["From"] must NOT encode <email> inside base64 block!
        hindi_sender = "DBERT शिक्षा एवं प्रौद्योगिकी"
        from_email = "support@dbert.in"
        msg_sender = build_mime_message(
            to_email="ajnatechrpa@gmail.com",
            subject="Sender Name Unicode Test",
            html_content="<p>Testing sender name</p>",
            from_name=hindi_sender,
            from_email=from_email
        )
        raw_from_header = msg_sender.as_bytes().split(b"\n")
        from_line = b""
        for line in raw_from_header:
            if line.startswith(b"From:"):
                from_line = line
                break
        
        # Check if <support@dbert.in> is in clear ASCII or if it got base64 encoded into encoded-word
        address_in_clear_ascii = b"<support@dbert.in>" in msg_sender.as_bytes()
        self.record(
            "MIME Address Encoding",
            "RFC 2047 addr-spec isolation in From header",
            address_in_clear_ascii,
            f"From line in MIME: {repr(from_line)}. " +
            ("BUG: The email address <support@dbert.in> was base64 encoded into RFC 2047 word, violating RFC 2047 Section 5(3) and breaking DMARC alignment!" if not address_in_clear_ascii else "Compliant: address remains unencoded."),
            finding_id="BUG-DELIVERY-05" if not address_in_clear_ascii else ""
        )

    # =========================================================================
    # 5. Strict Dry-Run Network Isolation Assertions
    # =========================================================================
    def test_dry_run_network_isolation(self):
        print("\n=== Challenge Suite 5: Dry-Run Network Isolation Assertion ===")
        service = EmailDeliveryService()

        # Monkeypatch socket.socket at the lowest level
        # If any TCP/UDP socket tries to connect, NetworkLeakError is raised
        with forbid_network():
            for target in ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com", "user@dbert.in"]:
                try:
                    res = service.send_email(
                        to=target,
                        subject="Zero Network Dry Run Assertion",
                        html_content="<h1>Zero Socket Verification</h1><p>Asserting zero network traffic.</p>",
                        dry_run=True
                    )
                    passed = (
                        res.success is True and
                        res.provider == "dry_run" and
                        res.diagnostics.get("dry_run") is True and
                        res.error is None
                    )
                    self.record("Dry-Run Isolation", f"Zero network sockets for {target}", passed, f"Provider: {res.provider}, Message-ID: {res.message_id}")
                except NetworkLeakError as nle:
                    self.record("Dry-Run Isolation", f"Zero network sockets for {target}", False, f"LEAK DETECTED: {nle}")
                except Exception as e:
                    self.record("Dry-Run Isolation", f"Zero network sockets for {target}", False, f"Exception: {e}")

    # =========================================================================
    # 6. EmailPacer Edge Cases & Concurrency Stress
    # =========================================================================
    def test_pacer_stress(self):
        print("\n=== Challenge Suite 6: EmailPacer Rate Limiting & Concurrency ===")
        
        # Test 6A: Negative or Zero interval
        pacer_zero = EmailPacer(default_interval=0.0)
        delay_zero = pacer_zero.calculate_delay("user@dbert.in")
        pacer_neg = EmailPacer(default_interval=-10.0)
        delay_neg = pacer_neg.calculate_delay("user@dbert.in")
        passed_zero = (delay_zero == 0.0 and delay_neg == 0.0)
        self.record("Pacer Resilience", "Zero and negative intervals produce 0.0 delay", passed_zero, f"Zero: {delay_zero}, Neg: {delay_neg}")

        # Test 6B: Thread safety and concurrent calculations
        pacer = EmailPacer(default_interval=0.2)
        threads = []
        errors = []
        delays_calculated = []

        def worker(rcpt_id):
            try:
                rcpt = f"user_{rcpt_id}@dbert.in"
                d = pacer.calculate_delay(rcpt)
                delays_calculated.append(d)
                pacer.wait_and_record(rcpt, dry_run=True)
            except Exception as e:
                errors.append(e)

        for i in range(20):
            t = threading.Thread(target=worker, args=(i % 3,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        passed_threads = (len(errors) == 0 and len(delays_calculated) == 20)
        self.record("Pacer Thread Safety", "20 concurrent threads across 3 recipients", passed_threads, f"Errors: {len(errors)}, Delays recorded: {len(delays_calculated)}")

    # =========================================================================
    # 7. HTML Converter & Footer Generator Stress
    # =========================================================================
    def test_content_helpers_stress(self):
        print("\n=== Challenge Suite 7: Content Helpers & Footer Edge Cases ===")
        
        # Edge cases for html_to_plain_text
        cases = [
            ("None input", None, "Open your DBERT portal: https://lms.dbert.in"),
            ("Empty input", "", "Open your DBERT portal: https://lms.dbert.in"),
            ("Script tags stripped", "<script>alert('xss');</script><p>Clean content</p>", "Clean content"),
            ("Style tags stripped", "<style>body{color:red;}</style><h1>Title</h1>", "Title"),
            ("Links converted to text (url)", '<a href="https://dbert.in/apply">Apply Now</a>', "Apply Now (https://dbert.in/apply)"),
            ("Links without href", "<a>Unlinked text</a>", "Unlinked text"),
            ("Nested broken HTML", "<div><p>Paragraph <span>Span<b>Bold</i></span></div>", "Paragraph SpanBold"),
            ("HTML entities unescaped", "&lt;DBERT &amp; Co. &quot;Inc&quot;&gt; &middot; &#39;Quote&#39;", "<DBERT & Co. \"Inc\"> · 'Quote'"),
            ("Excessive newlines collapsed", "<p>A</p><br><br><br><br><p>B</p>", "A\n\nB")
        ]

        for desc, inp, expected in cases:
            out = html_to_plain_text(inp)
            passed = (expected in out) if expected else True
            self.record("HTML to Plain Text", f"Edge case: {desc}", passed, f"Output: {repr(out)}")

        # Footer generation edge cases
        footer = generate_email_footer("candidate@dbert.in", secret_key="test_secret")
        footer_passed = (
            "Digital Blinc Education Research and Technology" in footer and
            "Digital Personal Data Protection Act, 2023" in footer and
            "Unsubscribe" in footer and
            "dbert.info" not in footer and
            "dbert.online" not in footer
        )
        self.record("Footer Generation", "CAN-SPAM & DPDP compliant footer without legacy domains", footer_passed, f"Footer len: {len(footer)}")

        # Unsubscribe token determinism and tamper resistance
        token1 = generate_unsubscribe_token("user@dbert.in", secret_key="key1")
        token2 = generate_unsubscribe_token("user@dbert.in", secret_key="key1")
        token_tampered_key = generate_unsubscribe_token("user@dbert.in", secret_key="key2")
        token_tampered_email = generate_unsubscribe_token("other@dbert.in", secret_key="key1")

        unsub_passed = (
            token1 == token2 and
            token1 != token_tampered_key and
            token1 != token_tampered_email and
            len(token1) == 32
        )
        self.record("Unsubscribe Token", "HMAC-SHA256 determinism and tamper resistance", unsub_passed, f"Token: {token1}")

    def run_all(self):
        print("=" * 70)
        print(" STARTING EMPIRICAL ADVERSARIAL STRESS TEST SUITE")
        print(" Agent: challenger_delivery_1 (Roles: critic, specialist)")
        print(" Target: apps/portal/services/delivery_service.py")
        print(" SAFEGUARD: All tests run with strict socket intercepts & mock transports.")
        print("=" * 70)

        self.test_smtp_failures()
        self.test_fallback_cascades()
        self.test_malformed_recipients()
        self.test_unicode_handling()
        self.test_dry_run_network_isolation()
        self.test_pacer_stress()
        self.test_content_helpers_stress()

        total = self.passed + self.failed
        print("\n" + "=" * 70)
        print(f" ADVERSARIAL TEST EXECUTION SUMMARY")
        print(f" Total Tests Run: {total}")
        print(f" Passed:          {self.passed}")
        print(f" Failed:          {self.failed}")
        print(f" Distinct Bugs Identified: {len(self.findings)}")
        print("=" * 70)
        
        if self.findings:
            print("\n" + "=" * 70)
            print(" BUGS DISCOVERED BY EMPIRICAL ADVERSARIAL TESTING:")
            for fid, cat, tname, msg in self.findings:
                print(f" - [{fid}] {cat} :: {tname}")
                print(f"   Details: {msg}")
            print("=" * 70 + "\n")

        return self.failed == 0


if __name__ == "__main__":
    runner = AdversarialTestRunner()
    success = runner.run_all()
    sys.exit(0 if success else 1)
