"""Unit tests for Phase 5: DBERT Mailer Architecture Enforcement."""

import os
import pytest
from unittest.mock import patch, MagicMock

def test_mailer_endpoint_default_configuration():
    from app import CPANEL_EMAIL_API_URL, EMAIL_PROVIDER
    assert CPANEL_EMAIL_API_URL == "https://mailer.aivaratech.online/send"
    assert EMAIL_PROVIDER == "cpanel_api"

@patch("requests.post")
def test_dbert_mailer_http_dispatch(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "success", "message": "Queued"}

    from app import _cpanel_api_send, _build_email_message
    msg = _build_email_message("test@example.com", "Test Subject", "<p>Test Body</p>", "transactional")
    _cpanel_api_send(msg, "test@example.com")

    assert mock_post.called
    call_args = mock_post.call_args
    assert call_args[0][0] == "https://mailer.aivaratech.online/send"
