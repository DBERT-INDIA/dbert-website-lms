"""Static assertion tests for Phase 6: Email Path Migration."""

import os
import pytest
from unittest.mock import patch, MagicMock

def test_cpanel_api_is_default_transport_in_send_async(monkeypatch):
    monkeypatch.setenv("EMAIL_PROVIDER", "")
    with patch("app._cpanel_api_send") as mock_cpanel_send:
        from app import send_email_async
        # Trigger async send
        send_email_async("user@example.com", "Test Subject", "<p>Body</p>")
        # Allow thread to execute
        import time
        time.sleep(0.1)
        assert mock_cpanel_send.called
