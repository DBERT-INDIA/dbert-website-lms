import pytest
from unittest.mock import patch, MagicMock
from services.ai.gemini_discovery import (
    discover_gemini_models,
    get_dynamic_fallback_chain,
    _rank_models,
    clear_model_cache
)

def setup_function():
    clear_model_cache()


def test_rank_models_prioritizes_flash_over_pro_and_orders_by_version():
    raw_models = [
        "models/gemini-1.5-pro",
        "models/gemini-2.0-flash",
        "models/gemini-1.5-flash",
        "models/gemini-1.0-pro",  # should be excluded (1.0)
        "models/gemini-2.0-pro-exp",
        "models/gemini-2.5-flash",
        "models/imagen-3.0-generate", # non-text
    ]
    best_default, ordered = _rank_models(raw_models)
    
    # 2.5 flash is highest version flash
    assert best_default == "gemini-2.5-flash"
    
    # Flash models should precede pro models, and versions descending
    assert ordered[0] == "gemini-2.5-flash"
    assert ordered[1] == "gemini-2.0-flash"
    assert ordered[2] == "gemini-1.5-flash"
    assert "gemini-2.0-pro-exp" in ordered
    assert "gemini-1.5-pro" in ordered
    # Ensure 1.0 is excluded
    assert "gemini-1.0-pro" not in ordered


def test_discover_gemini_models_success():
    fake_api_response = {
        "models": [
            {
                "name": "models/gemini-1.5-flash",
                "supportedGenerationMethods": ["generateContent"]
            },
            {
                "name": "models/gemini-2.0-flash",
                "supportedGenerationMethods": ["generateContent"]
            },
            {
                "name": "models/gemini-1.5-pro",
                "supportedGenerationMethods": ["generateContent"]
            },
            {
                "name": "models/text-embedding-004",
                "supportedGenerationMethods": ["embedContent"]
            },
            {
                "name": "models/gemini-tts-1",
                "supportedGenerationMethods": ["generateContent"]
            }
        ]
    }
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = fake_api_response
    
    with patch("requests.get", return_value=mock_resp):
        best_default, models, err = discover_gemini_models(api_key="AIzaSyFakeKeyForTesting123456789")
        assert err is None
        assert best_default == "gemini-2.0-flash"
        assert "gemini-1.5-flash" in models
        assert "gemini-1.5-pro" in models
        # Embedding and TTS should be filtered out
        assert not any("embedding" in m for m in models)
        assert not any("tts" in m for m in models)


def test_discover_gemini_models_caching():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "models": [
            {"name": "models/gemini-2.0-flash", "supportedGenerationMethods": ["generateContent"]}
        ]
    }
    
    with patch("requests.get", return_value=mock_resp) as mock_get:
        # First call hits network
        best1, _, _ = discover_gemini_models(api_key="AIzaSyFakeKeyForTesting123456789")
        assert mock_get.call_count == 1
        
        # Second call hits in-memory cache
        best2, _, _ = discover_gemini_models(api_key="AIzaSyFakeKeyForTesting123456789")
        assert mock_get.call_count == 1
        assert best1 == best2 == "gemini-2.0-flash"


def test_get_dynamic_fallback_chain_with_user_models():
    user_models = [
        "models/gemini-1.5-pro",
        "models/gemini-2.0-flash",
        "models/audio-model",
    ]
    chain = get_dynamic_fallback_chain(user_models=user_models)
    assert chain[0] == "gemini-2.0-flash"
    assert chain[1] == "gemini-1.5-pro"
    assert not any("audio" in m for m in chain)
