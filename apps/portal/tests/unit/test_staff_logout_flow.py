import pytest
from app import app, get_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_staff_logout_get_clears_cookies_and_redirects(client):
    """Test GET /staff/logout clears auth cookies and redirects to /staff/login."""
    client.set_cookie("dbert_auth", "test-token-12345")
    client.set_cookie("dbert_session", "test-token-12345")
    with client.session_transaction() as sess:
        sess["staff_id"] = 1

    resp = client.get("/staff/logout", follow_redirects=False)
    assert resp.status_code == 302
    assert "/staff/login" in resp.headers.get("Location", "")

    cookies_header = resp.headers.getlist("Set-Cookie")
    auth_cleared = any("dbert_auth=;" in c or "Max-Age=0" in c for c in cookies_header)
    session_cleared = any("dbert_session=;" in c or "Max-Age=0" in c for c in cookies_header)
    assert auth_cleared or session_cleared

def test_staff_logout_invalidates_database_session(client):
    """Test /staff/logout deletes token from user_sessions table."""
    token = "test-staff-live-token-999"
    with get_db() as conn:
        conn.execute(
            "INSERT INTO user_sessions (session_token, user_id, email, role, created_at, expires_at) VALUES (?, ?, ?, ?, datetime('now'), datetime('now', '+1 day'))",
            (token, 1, "staff@dbert.test", "staff")
        )
        conn.commit()

    # Confirm token is inserted
    with get_db() as conn:
        row = conn.execute("SELECT 1 FROM user_sessions WHERE session_token = ?", (token,)).fetchone()
        assert row is not None

    # Call logout with cookie set
    client.set_cookie("dbert_auth", token)
    resp = client.get("/staff/logout", follow_redirects=False)
    assert resp.status_code == 302

    # Verify session is deleted from user_sessions
    with get_db() as conn:
        row = conn.execute("SELECT 1 FROM user_sessions WHERE session_token = ?", (token,)).fetchone()
        assert row is None

def test_staff_dashboard_redirects_unauthenticated(client):
    """Test unauthenticated request to /staff/dashboard redirects to /staff/login."""
    resp = client.get("/staff/dashboard", follow_redirects=False)
    assert resp.status_code == 302
    assert "/staff/login" in resp.headers.get("Location", "")
