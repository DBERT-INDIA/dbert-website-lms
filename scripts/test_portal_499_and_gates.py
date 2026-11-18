import os
import sys
import unittest
import json
from pathlib import Path

# Add portal to sys.path
sys.path.insert(0, str(Path("apps/portal").resolve()))

# Set test environment
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = ""

from app import app, get_db

class TestPortal499AndGates(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_admin_articles_review_publishing(self):
        """Verify approving an article transitions it to PUBLISHED with dbert.in/insights URL."""
        with get_db() as conn:
            existing = conn.execute("SELECT id FROM intern_accounts WHERE id=9999").fetchone()
            if not existing:
                conn.execute("INSERT INTO intern_accounts (id, name, email) VALUES (9999, 'Test Author', 'test_author_gate2@dbert.in')")
            art = conn.execute("SELECT id FROM intern_articles WHERE id=9999").fetchone()
            if art:
                conn.execute("UPDATE intern_articles SET status='PENDING_REVIEW', published_url=NULL WHERE id=9999")
            else:
                conn.execute("INSERT INTO intern_articles (id, intern_id, domain, title, content_markdown, status) VALUES (9999, 9999, 'Data Analyst', 'Scaling PostgreSQL for 10M Rows', 'Article body markdown...', 'PENDING_REVIEW')")
            conn.commit()

        from app import create_session
        token = create_session("admin@dbert.in", "admin")
        self.client.set_cookie(key="dbert_auth", value=token)

        res = self.client.post("/admin/articles/review", json={
            "id": 9999,
            "status": "APPROVED"
        }, headers={"Cookie": f"dbert_auth={token}"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["article_status"], "PUBLISHED")
        self.assertIn("https://dbert.in/insights/", data["published_url"])

        # Clean up
        with get_db() as conn:
            conn.execute("DELETE FROM intern_articles WHERE id=9999")
            conn.execute("DELETE FROM intern_accounts WHERE id=9999")
            conn.commit()
        print("✓ test_admin_articles_review_publishing passed!")

    def test_utr_regex_validation(self):
        """Test 12-digit UTR numeric constraint."""
        import re
        self.assertTrue(bool(re.match(r"^\d{12}$", "123456789012")))
        self.assertFalse(bool(re.match(r"^\d{12}$", "12345")))
        self.assertFalse(bool(re.match(r"^\d{12}$", "12345678901a")))
        self.assertFalse(bool(re.match(r"^\d{12}$", "")))
        print("✓ test_utr_regex_validation passed!")

if __name__ == "__main__":
    unittest.main()
