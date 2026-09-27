import pytest
from unittest.mock import patch, MagicMock
from services.ai.gemini_provider import GeminiProvider
from services.ai.exceptions import GeminiAuthError, GeminiModelRetiredError, GeminiRateLimitError, GeminiTimeoutError

@patch('services.ai.gemini_provider.requests.post')
def test_gemini_provider_valid_key(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Hello world"}]}}],
        "usageMetadata": {"promptTokenCount": 5, "candidatesTokenCount": 2}
    }
    mock_post.return_value = mock_resp
    
    provider = GeminiProvider("fake_key")
    resp = provider.generate_content("Hi")
    
    assert resp.text == "Hello world"
    assert resp.input_tokens == 5
    assert resp.output_tokens == 2

@patch('services.ai.gemini_provider.requests.post')
def test_gemini_provider_invalid_key(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 401
    mock_post.return_value = mock_resp
    
    provider = GeminiProvider("fake_key")
    with pytest.raises(GeminiAuthError):
        provider.generate_content("Hi")

@patch('services.ai.gemini_provider.requests.post')
def test_gemini_provider_model_404(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_post.return_value = mock_resp
    
    provider = GeminiProvider("fake_key")
    with pytest.raises(GeminiModelRetiredError):
        provider.generate_content("Hi")

@patch('services.ai.gemini_provider.requests.post')
def test_gemini_provider_fallback_on_429(mock_post):
    # First model 429s, second model succeeds
    mock_429 = MagicMock()
    mock_429.status_code = 429
    
    mock_200 = MagicMock()
    mock_200.status_code = 200
    mock_200.json.return_value = {"candidates": [{"content": {"parts": [{"text": "Success on fallback"}]}}]}
    
    mock_post.side_effect = [mock_429, mock_200]
    
    provider = GeminiProvider("fake_key")
    resp = provider.generate_content("Hi")
    assert resp.text == "Success on fallback"

@patch('services.ai.gemini_provider.requests.post')
def test_gemini_provider_timeout(mock_post):
    import requests
    mock_post.side_effect = requests.Timeout("Connection timed out")
    
    provider = GeminiProvider("fake_key")
    resp = provider.generate_content("Hi")
    assert resp.text is None
    assert "Timeout reaching" in resp.error

@patch('services.ai.gemini_provider.requests.post')
def test_gemini_provider_empty_response(mock_post):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {} # Empty JSON
    mock_post.return_value = mock_resp
    
    provider = GeminiProvider("fake_key")
    resp = provider.generate_content("Hi")
    
    assert resp.text == ""

