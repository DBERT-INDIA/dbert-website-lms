import pytest
from app import app, get_db, create_session, AUTH_COOKIE, _validate_gemini_key_live

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as c:
        yield c

def test_course_learn_chat_prompt_query_passed_to_template(client):
    """Verify that visiting /courses/<id>/learn?chat_prompt_query=... passes the query to template context."""
    with get_db() as conn:
        intern = conn.execute("SELECT id, email FROM intern_accounts WHERE email = 'test_cybersecurity@dbert.in'").fetchone()
        assert intern is not None
        
        # Ensure enrollment in course 11
        conn.execute("""
            INSERT OR IGNORE INTO course_enrollments (intern_id, course_id, enrolled_at, current_day, email)
            VALUES (?, 11, datetime('now'), 1, ?)
        """, (intern["id"], intern["email"]))
        
        # Ensure enrollments row with payment_status 'Verified' so gate passes
        conn.execute("""
            INSERT OR IGNORE INTO enrollments (name, email, phone, college, domain, payment_status, created_at)
            VALUES ('Test Cyber', ?, '9876543210', 'Engineering College', 'Cybersecurity', 'Verified', datetime('now'))
        """, (intern["email"],))
        
        # Ensure API key exists so gate passes
        conn.execute("""
            INSERT OR IGNORE INTO user_api_keys (intern_id, encrypted_key, validated_at, created_at)
            VALUES (?, 'dummy_key', datetime('now'), datetime('now'))
        """, (intern["id"],))
        conn.commit()

        token = create_session(intern["email"], "intern")
        client.set_cookie(AUTH_COOKIE, token)

        with client.session_transaction() as sess:
            sess["intern_id"] = intern["id"]
            sess["email"] = intern["email"]
            sess["role"] = "intern"

        res = client.get("/courses/11/learn?chat_prompt_query=Explain+the+CIA+Triad")
        assert res.status_code == 200
        html = res.data.decode("utf-8")
        
        # Check that chat_prompt_query is embedded in the JS initialization
        assert 'Explain the CIA Triad' in html
        assert 'data-prevent-submit' in html
        assert 'data-prevent-keydown' in html
        # Ensure input name="chat_prompt_query" is NOT present (prevents browser GET submission)
        assert 'name="chat_prompt_query"' not in html
        # Ensure markdown parser and styling are embedded for rich bold, code, and list rendering
        assert 'renderMarkdown' in html
        assert '.chat-bubble.assistant strong' in html
        assert '.chat-inline-code' in html
        assert '.chat-code-block' in html


def test_validate_gemini_key_live_rejects_empty_or_short():
    """Verify that _validate_gemini_key_live rejects empty or short keys."""
    is_valid, models, err = _validate_gemini_key_live("")
    assert not is_valid
    assert "empty" in err.lower()

    is_valid, models, err = _validate_gemini_key_live("short_key_123")
    assert not is_valid
    assert "too short" in err.lower()


def test_validate_gemini_key_live_uses_dynamic_models_and_selects_best_fitted(monkeypatch):
    """Verify that _validate_gemini_key_live strictly uses dynamically discovered models and tests them."""
    from unittest.mock import MagicMock
    import requests

    # Mock discover_gemini_models to return a modern list where gemini-1.5-flash does NOT exist
    discovered = ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.5-pro"]
    monkeypatch.setattr("app.discover_gemini_models", lambda api_key, force_refresh=True: ("gemini-2.5-flash", discovered, None))

    tested_urls = []

    def mock_post(url, *args, **kwargs):
        tested_urls.append(url)
        mock_resp = MagicMock()
        # Suppose the first model returns 200
        if "gemini-2.5-flash" in url:
            mock_resp.status_code = 200
            mock_resp.json.return_value = {"candidates": [{"content": {"parts": [{"text": "pong"}]}}]}
        else:
            mock_resp.status_code = 404
        return mock_resp

    monkeypatch.setattr(requests, "post", mock_post)

    is_valid, models, err = _validate_gemini_key_live("AIzaSyTestDynamicKey123456789")
    assert is_valid is True
    assert err is None
    assert models[0] == "gemini-2.5-flash"
    # Verify gemini-1.5-flash was NEVER tested
    assert not any("gemini-1.5-flash" in u for u in tested_urls)
    assert any("gemini-2.5-flash" in u for u in tested_urls)
