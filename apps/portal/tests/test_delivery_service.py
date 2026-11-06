"""
apps/portal/tests/test_delivery_service.py
Unit tests for the resilient DBERT Email Delivery Engine (services/delivery_service.py).
Strictly mock-based and dry-run safe: ZERO live network dispatch.
"""

import os
import time
import smtplib
import pytest
from unittest.mock import patch, MagicMock

from services.delivery_service import (
    EmailDeliveryService,
    DeliveryResult,
    EmailPacer,
    build_mime_message,
    generate_message_id,
    generate_unsubscribe_token,
    generate_unsubscribe_url,
    generate_email_footer,
    html_to_plain_text,
    send_email,
    DUMMY_EMAIL_DOMAINS
)


def test_dry_run_safety_zero_network_dispatch():
    """Verify dry_run mode performs zero network connections and returns valid diagnostics."""
    service = EmailDeliveryService()
    with patch("smtplib.SMTP_SSL") as mock_ssl, patch("smtplib.SMTP") as mock_smtp, patch("requests.post") as mock_http:
        res = service.send_email(
            to="ain.sharma.abhinav@gmail.com",
            subject="Dry Run Safety Test",
            html_content="<p>Test Content</p>",
            dry_run=True
        )
        assert res.success is True
        assert res.provider == "dry_run"
        assert res.error is None
        assert res.message_id.startswith("<")
        assert res.message_id.endswith("@dbert.in>")
        assert res.diagnostics.get("dry_run") is True
        assert "headers" in res.diagnostics
        assert not mock_ssl.called
        assert not mock_smtp.called
        assert not mock_http.called


def test_rfc5322_and_rfc8058_headers():
    """Verify compliance with RFC 5322 (Message-ID, Date, From, Reply-To) and RFC 8058 (List-Unsubscribe)."""
    to_email = "ajnatechrpa@gmail.com"
    msg = build_mime_message(
        to_email=to_email,
        subject="Header Verification Test",
        html_content="<p>Body</p>",
        text_content="Body",
        from_name="DBERT Support",
        from_email="abhinav.sharma@dbert.in",
        reply_to="support@dbert.in",
        secret_key="test_secret_key"
    )
    
    # Message-ID format
    msg_id = msg.get("Message-ID")
    assert msg_id is not None
    assert msg_id.startswith("<")
    assert msg_id.endswith("@dbert.in>")
    
    # From and Reply-To
    assert msg.get("From") == "DBERT Support <abhinav.sharma@dbert.in>"
    assert msg.get("Reply-To") == "support@dbert.in"
    assert msg.get("To") == to_email
    assert msg.get("Date") is not None
    assert msg.get("Auto-Submitted") == "auto-generated"
    
    # RFC 8058 One-Click List-Unsubscribe
    unsub = msg.get("List-Unsubscribe")
    assert unsub is not None
    assert "https://lms.dbert.in/unsubscribe?e=" in unsub
    assert "<mailto:support@dbert.in?subject=unsubscribe>" in unsub
    assert msg.get("List-Unsubscribe-Post") == "List-Unsubscribe=One-Click"


def test_content_hygiene_and_domain_sanitization():
    """Verify that transactional emails omit tracking pixels, omit UTM queries, and purge dbert.info."""
    msg = build_mime_message(
        to_email="test.user@dbert.in",
        subject="Content Hygiene Test",
        html_content="<p>Welcome to <a href='https://lms.dbert.in/portal'>DBERT Portal</a></p>",
        from_name="DBERT Support",
        from_email="abhinav.sharma@dbert.in"
    )
    
    html_text = ""
    plain_text = ""
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_text = part.get_payload(decode=True).decode("utf-8")
        elif part.get_content_type() == "text/plain":
            plain_text = part.get_payload(decode=True).decode("utf-8")
            
    # No tracking pixel /e/o.gif
    assert "/e/o.gif" not in html_text
    
    # No UTM marketing parameters injected
    assert "utm_source=email" not in html_text
    
    # No suspended dbert.info or dead domains
    assert "dbert.info" not in html_text
    assert "dbert.info" not in plain_text
    assert "dbert.online" not in html_text
    assert "dbert.online" not in plain_text
    
    # Standardized support email present
    assert "support@dbert.in" in html_text
    assert "support@dbert.in" in plain_text
    assert "Digital Personal Data Protection Act, 2023" in html_text


def test_multipart_alternative_mime_structure():
    """Verify message contains both text/plain and text/html parts, with text part first."""
    msg = build_mime_message(
        to_email="candidate@dbert.in",
        subject="Multipart Structure Test",
        html_content="<h1>Header</h1><p>Paragraph with <a href='https://lms.dbert.in'>Link</a></p>"
    )
    assert msg.is_multipart()
    parts = msg.get_payload()
    assert len(parts) >= 2
    assert parts[0].get_content_type() == "text/plain"
    assert parts[1].get_content_type() == "text/html"
    
    plain_content = parts[0].get_payload(decode=True).decode("utf-8")
    assert "Header" in plain_content
    assert "Link (https://lms.dbert.in)" in plain_content


def test_dummy_email_domain_interception():
    """Verify hard bounce guard intercepts synthetic dummy domains at zero network cost."""
    service = EmailDeliveryService()
    test_dummies = [
        "candidate_delta@example.com",
        "intern@example.org",
        "qa@example.net",
        "user@test.com",
        "mock@sample.com",
        "bot@fakemail.com",
        "throwaway@mailinator.com",
        "missing_at_symbol_string"
    ]
    with patch("smtplib.SMTP_SSL") as mock_ssl, patch("requests.post") as mock_post:
        for dummy in test_dummies:
            res = service.send_email(to=dummy, subject="Test", html_content="<p>Hi</p>", dry_run=False)
            assert res.success is False
            assert res.provider == "hard_bounce_guard"
            assert "intercepted" in res.error.lower() or "invalid" in res.error.lower()
        assert not mock_ssl.called
        assert not mock_post.called


def test_primary_google_workspace_smtp_success():
    """Verify primary Google Workspace SMTP path with SSL on port 465."""
    service = EmailDeliveryService(
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        smtp_user="abhinav.sharma@dbert.in",
        smtp_pass="rsupmvvvvwrsuxuh",
        from_email="abhinav.sharma@dbert.in"
    )
    # Bypass pacing sleep during unit test
    service.pacer.wait_and_record = MagicMock(return_value=0.0)

    mock_smtp_instance = MagicMock()
    with patch("smtplib.SMTP_SSL", return_value=mock_smtp_instance) as mock_ssl:
        mock_smtp_instance.__enter__.return_value = mock_smtp_instance
        res = service.send_email(
            to="ain.sharma.abhinav@gmail.com",
            subject="Primary SMTP Delivery",
            html_content="<p>Delivered via Primary</p>",
            dry_run=False
        )
        assert res.success is True
        assert res.provider == "google_workspace_smtp"
        assert res.error is None
        mock_ssl.assert_called_once()
        mock_smtp_instance.login.assert_called_with("abhinav.sharma@dbert.in", "rsupmvvvvwrsuxuh")
        mock_smtp_instance.sendmail.assert_called_once()


def test_secondary_cpanel_api_fallback_when_primary_fails():
    """Verify graceful fallback to secondary transactional API when primary SMTP fails."""
    service = EmailDeliveryService(
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        smtp_user="abhinav.sharma@dbert.in",
        smtp_pass="rsupmvvvvwrsuxuh",
        cpanel_api_url="https://mailer.aivaratech.online/send"
    )
    service.pacer.wait_and_record = MagicMock(return_value=0.0)

    # Primary fails with SMTPAuthenticationError
    with patch("smtplib.SMTP_SSL", side_effect=smtplib.SMTPAuthenticationError(535, b"Bad credentials")), \
         patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = '{"status":"success"}'

        res = service.send_email(
            to="ajnatechrpa@gmail.com",
            subject="Fallback Delivery",
            html_content="<p>Testing fallback</p>",
            dry_run=False
        )
        assert res.success is True
        assert res.provider == "secondary_cpanel_api"
        assert "primary_error" in res.diagnostics
        assert "Bad credentials" in res.diagnostics["primary_error"]
        assert mock_post.called


def test_secondary_backup_smtp_fallback_rejects_suspended_domain():
    """Verify that secondary fallback refuses to connect to suspended domain dbert.info."""
    service = EmailDeliveryService(
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        cpanel_api_url="",  # No API configured
        backup_host="dbert.info"  # Suspended domain
    )
    service.pacer.wait_and_record = MagicMock(return_value=0.0)

    with patch("smtplib.SMTP_SSL", side_effect=smtplib.SMTPConnectError(421, b"Connection refused")):
        res = service.send_email(
            to="ain.sharma.abhinav@gmail.com",
            subject="Suspended Backup Check",
            html_content="<p>Check</p>",
            dry_run=False
        )
        assert res.success is False
        assert res.provider == "failed"
        assert "No valid fallback" in res.error or "Primary failed" in res.error


def test_all_providers_fail_diagnostics():
    """Verify that failure across all providers produces rich diagnostics without unhandled exceptions."""
    service = EmailDeliveryService(
        smtp_host="smtp.gmail.com",
        smtp_port=465,
        cpanel_api_url="https://mailer.aivaratech.online/send"
    )
    service.pacer.wait_and_record = MagicMock(return_value=0.0)

    with patch("smtplib.SMTP_SSL", side_effect=smtplib.SMTPServerDisconnected("Server disconnected")), \
         patch("requests.post", side_effect=Exception("Connection timed out")):
        res = service.send_email(
            to="ain.sharma.abhinav@gmail.com",
            subject="Complete Failure Test",
            html_content="<p>Test</p>",
            dry_run=False
        )
        assert res.success is False
        assert res.provider == "failed"
        assert "Primary failed" in res.error
        assert "Fallbacks failed" in res.error
        assert "fallback_errors" in res.diagnostics


def test_email_pacer_timing_and_calculation():
    """Verify EmailPacer enforces minimum inter-message delays per recipient and globally."""
    pacer = EmailPacer(default_interval=0.1)
    recipient = "pacer.test@dbert.in"
    
    # First dispatch should require 0 delay
    d1 = pacer.calculate_delay(recipient)
    assert d1 == 0.0
    pacer.wait_and_record(recipient, dry_run=False)
    
    # Immediate subsequent dispatch should require approximately 0.1s delay
    d2 = pacer.calculate_delay(recipient)
    assert 0.0 < d2 <= 0.1
    
    # After waiting interval, delay returns to 0
    time.sleep(0.12)
    d3 = pacer.calculate_delay(recipient)
    assert d3 == 0.0


def test_rfc8058_unsubscribe_route_get_and_post(app_client):
    """Verify /unsubscribe endpoint handles both GET and POST (HTTP 200 on POST for RFC 8058)."""
    from app import app
    client = app_client[0] if isinstance(app_client, tuple) else app_client
    test_email = "unsubscribe.test@dbert.in"
    token = generate_unsubscribe_token(test_email, secret_key=app.secret_key)
    
    # 1. RFC 8058 One-Click POST request
    post_resp = client.post(f"/unsubscribe?e={test_email}&t={token}")
    assert post_resp.status_code == 200
    
    # 2. Browser GET request with valid token
    get_resp = client.get(f"/unsubscribe?e={test_email}&t={token}")
    assert get_resp.status_code == 200
    html_data = get_resp.data.decode("utf-8")
    assert "unsubscribed" in html_data.lower()
    
    # 3. Browser GET request with invalid token
    invalid_resp = client.get(f"/unsubscribe?e={test_email}&t=badtoken123")
    assert invalid_resp.status_code == 200
    invalid_html = invalid_resp.data.decode("utf-8")
    assert "invalid or expired" in invalid_html.lower()


def test_module_level_send_email_interface():
    """Verify SCOPE.md module-level contract: send_email(to, subject, html_content, ...) -> DeliveryResult."""
    with patch("smtplib.SMTP_SSL") as mock_ssl:
        res = send_email(
            to="test.user@dbert.in",
            subject="Module Interface Test",
            html_content="<p>Testing module function</p>",
            dry_run=True
        )
        assert isinstance(res, DeliveryResult)
        assert res.success is True
        assert res.provider == "dry_run"
        assert res.message_id
