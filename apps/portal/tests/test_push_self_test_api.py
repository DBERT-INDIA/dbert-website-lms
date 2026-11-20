"""
test_push_self_test_api.py
Tests for the Web Push Self-Test Endpoint (/api/push/test and /api/push/broadcast alias)
and frontend markup compliance in account_notifications.html.
"""
import os
import sys
import unittest
from unittest.mock import patch

PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)

if "DATABASE_URL" not in os.environ:
    os.environ["DATABASE_URL"] = ""
os.environ["SECRET_KEY"] = "test-secret-key-push-12345"

from app import app, get_db, create_session, AUTH_COOKIE


class TestPushSelfTestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SESSION_COOKIE_DOMAIN"] = None
        app.config["SESSION_COOKIE_SECURE"] = False

    def setUp(self):
        self.app = app
        self.app.config["TESTING"] = True
        self.app.config["SESSION_COOKIE_DOMAIN"] = None
        self.app.config["SESSION_COOKIE_SECURE"] = False
        self.client = app.test_client()

        # Ensure a test intern account exists in DB (portable across SQLite and Postgres)
        with get_db() as conn:
            existing = conn.execute("SELECT id FROM intern_accounts WHERE LOWER(email) = ?", ('test_push_intern@dbert.test',)).fetchone()
            if not existing:
                try:
                    conn.execute("""
                        INSERT INTO intern_accounts (id, email, name, domain, is_active)
                        VALUES (999, 'test_push_intern@dbert.test', 'Test Push Intern', 'Data Analytics', 1)
                    """)
                    conn.commit()
                except Exception:
                    pass

    def test_push_test_unauthenticated_returns_401(self):
        """Unauthenticated POST /api/push/test with valid CSRF must return 401 JSON."""
        with self.client.session_transaction() as sess:
            sess["_csrf"] = "csrf-token-123"

        res = self.client.post(
            "/api/push/test",
            json={"title": "Test", "body": "Hello"},
            headers={"X-CSRF-Token": "csrf-token-123"}
        )
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertEqual(data.get("status"), "error")
        self.assertIn("Authentication required", data.get("message", ""))

    def test_push_broadcast_unauthenticated_returns_401(self):
        """Unauthenticated POST /api/push/broadcast with valid CSRF must also return 401 JSON (not 404)."""
        with self.client.session_transaction() as sess:
            sess["_csrf"] = "csrf-token-123"

        res = self.client.post(
            "/api/push/broadcast",
            json={"title": "Test", "body": "Hello"},
            headers={"X-CSRF-Token": "csrf-token-123"}
        )
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertEqual(data.get("status"), "error")

    @patch("services.notifications.web_push_service.dispatch_lifecycle_push")
    def test_push_test_authenticated_dispatches_push(self, mock_dispatch):
        """Authenticated intern calling /api/push/test dispatches self_test push and returns 200."""
        token = create_session("test_push_intern@dbert.test", role="intern")
        self.client.set_cookie(AUTH_COOKIE, token)

        with self.client.session_transaction() as sess:
            sess["_csrf"] = "csrf-token-123"

        res = self.client.post(
            "/api/push/test",
            json={
                "title": "🔔 DBERT Push Test",
                "body": "Custom test message",
                "url": "/account/notifications"
            },
            headers={"X-CSRF-Token": "csrf-token-123"}
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        self.assertIn("dispatched", data.get("message", "").lower())

        # Verify dispatch_lifecycle_push was invoked with self_test event and intern email
        mock_dispatch.assert_called_once()
        kwargs = mock_dispatch.call_args[1]
        self.assertEqual(kwargs.get("event_name"), "self_test")
        self.assertEqual(kwargs.get("target_email"), "test_push_intern@dbert.test")
        self.assertEqual(kwargs.get("intern_id"), 999)
        self.assertTrue(kwargs.get("sync_inapp"))

    @patch("services.notifications.web_push_service.dispatch_lifecycle_push")
    def test_push_broadcast_alias_authenticated(self, mock_dispatch):
        """Authenticated caller using legacy /api/push/broadcast alias safely dispatches self_test."""
        token = create_session("test_push_intern@dbert.test", role="intern")
        self.client.set_cookie(AUTH_COOKIE, token)

        with self.client.session_transaction() as sess:
            sess["_csrf"] = "csrf-token-123"

        res = self.client.post(
            "/api/push/broadcast",
            json={"title": "Test Alias"},
            headers={"X-CSRF-Token": "csrf-token-123"}
        )
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data.get("status"), "success")
        mock_dispatch.assert_called_once()
        self.assertEqual(mock_dispatch.call_args[1].get("event_name"), "self_test")

    def test_account_notifications_markup_and_csp(self):
        """Ensure account_notifications.html has correct endpoint, CSRF headers, and zero inline onclicks."""
        template_path = os.path.join(PORTAL_DIR, "templates", "account_notifications.html")
        with open(template_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Check button exists
        self.assertIn('id="btnTestPush"', html)
        self.assertIn('Send Test Alert', html)

        # Check JS uses /api/push/test
        self.assertIn('/api/push/test', html)
        self.assertIn('X-CSRF-Token', html)

        # Check zero inline onclick handlers on the button
        self.assertNotIn('onclick="sendTestPush', html)
        self.assertNotIn('onclick="', html[html.find('id="btnTestPush"'):html.find('id="btnTestPush"') + 150])


if __name__ == "__main__":
    unittest.main()
