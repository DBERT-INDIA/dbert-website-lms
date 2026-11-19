import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, get_db

class TestLeaderboardAndCertificates(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_leaderboard_public_access(self):
        res = self.client.get('/leaderboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Cohort Engineering Leaderboard", res.data)
        self.assertIn(b"Leaderboard Standings", res.data)

    def test_leaderboard_domain_filter(self):
        res = self.client.get('/leaderboard?domain=Data+Analyst')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Data Analyst", res.data)

    def test_certificates_unauthenticated_redirect(self):
        res = self.client.get('/certificates')
        self.assertIn(res.status_code, (301, 302))
        self.assertIn("/#signin", res.headers.get("Location", ""))

    def test_sitemap_includes_leaderboard(self):
        res = self.client.get('/sitemap.xml')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"/leaderboard", res.data)

if __name__ == '__main__':
    unittest.main()
