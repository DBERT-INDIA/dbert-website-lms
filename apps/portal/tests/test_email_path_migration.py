"""Static assertion and deliverability tests for Email Subsystem & SMTP Integration."""

import os
import time
import pytest
from unittest.mock import patch, MagicMock

from app import (
    send_email_async,
    _build_email_message,
    send_password_reset_email,
    send_application_received_email,
    send_status_update_email,
    send_enrollment_reminder,
    send_otp_verification_email,
    notify_task_reviewed_email,
    notify_mentor_assigned_email,
)


def test_cpanel_api_is_fallback_transport_in_send_async(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "cpanel_api")
    with patch("app._cpanel_api_send") as mock_cpanel_send:
        send_email_async("user@test.dbert.in", "Test Subject", "<p>Body</p>")
        time.sleep(0.1)
        assert mock_cpanel_send.called


def test_smtp_is_dispatched_when_configured(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "smtp")
    with patch("app._smtp_send_raw") as mock_smtp_send:
        send_email_async("user@test.dbert.in", "Test SMTP", "<p>Body</p>")
        time.sleep(0.1)
        assert mock_smtp_send.called


def test_dummy_email_domains_intercepted_before_transport():
    with patch("app._smtp_send_raw") as mock_smtp_send, patch("app._cpanel_api_send") as mock_cpanel_send:
        send_email_async("candidate_delta@example.com", "Test Dummy", "<p>Body</p>")
        time.sleep(0.1)
        assert not mock_smtp_send.called
        assert not mock_cpanel_send.called


def test_email_disclaimer_and_footer():
    msg = _build_email_message("candidate@example.com", "Test Title", "<p>Hello World</p>", "test_campaign")
    
    # Extract plain and html parts
    plain_text = ""
    html_text = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            plain_text = part.get_payload(decode=True).decode("utf-8")
        elif part.get_content_type() == "text/html":
            html_text = part.get_payload(decode=True).decode("utf-8")

    # Assert Statutory Disclaimers in HTML
    assert "Digital Blinc Education Research and Technology (DBERT)" in html_text
    assert "MSME Registered" in html_text
    assert "Digital Personal Data Protection Act, 2023" in html_text
    assert "Security Notice:" in html_text
    assert "Unsubscribe" in html_text

    # Assert Statutory Disclaimers also in Plain Text part
    assert "Digital Blinc Education Research and Technology (DBERT)" in plain_text
    assert "Digital Personal Data Protection Act" in plain_text
    assert "Security Notice:" in plain_text


def test_otp_email_structure():
    with patch("app.send_email_async") as mock_send:
        send_otp_verification_email("user@example.com", "948271")
        assert mock_send.called
        args = mock_send.call_args[0]
        assert args[0] == "user@example.com"
        assert "948271" in args[1]  # Subject line
        assert "948271" in args[2]  # HTML body
        assert "expires in 10 minutes" in args[2]


def test_task_reviewed_and_mentor_assigned_emails():
    with patch("app.send_email_async") as mock_send:
        notify_task_reviewed_email("Alex Doe", "alex@example.com", "accepted", 50, "Excellent submission!")
        assert mock_send.called
        args = mock_send.call_args[0]
        assert "alex@example.com" == args[0]
        assert "+50 DBERT Coins" in args[2]
        assert "Excellent submission!" in args[2]

    with patch("app.send_email_async") as mock_send:
        notify_mentor_assigned_email("Alex Doe", "alex@example.com", "AI Agent Development")
        assert mock_send.called
        args = mock_send.call_args[0]
        assert "alex@example.com" == args[0]
        assert "AI Agent Development" in args[2]


def test_status_update_rejection_paid_program_fasttrack():
    with patch("app.send_email_async") as mock_send:
        send_status_update_email("Alex Doe", "alex@example.com", "Full Stack Development", "Rejected")
        assert mock_send.called
        args = mock_send.call_args[0]
        html_body = args[2]
        assert "Paid Program (₹1,999)" in html_body
        assert "guaranteed placement opportunity" in html_body
