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

    def test_leaderboard_expandable_scoring_methodology(self):
        res = self.client.get('/leaderboard')
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)

        # Card and toggle elements
        self.assertIn('id="rubricCard"', html)
        self.assertIn('id="rubricHeader"', html)
        self.assertIn('id="toggleRubricBtn"', html)
        self.assertIn('View Scoring Rules', html)
        self.assertIn('id="rubricExpandableContent"', html)
        self.assertIn('style="display: none;"', html)

        # 7 scoring metrics
        self.assertIn('Verified Certification', html)
        self.assertIn('+100 pts', html)
        self.assertIn('Approved Bounty Task', html)
        self.assertIn('+50 pts', html)
        self.assertIn('Completed Sprint Lesson', html)
        self.assertIn('+25 pts', html)
        self.assertIn('Platform Sprint Attendance', html)
        self.assertIn('+5 pts/hr', html)
        self.assertIn('Published Engineering Article', html)
        self.assertIn('100% Score on Daily Quiz', html)
        self.assertIn('+5 pts', html)
        self.assertIn('Mastered Technical Concept', html)

        # CSP compliance: zero inline onclick
        self.assertNotIn('onclick=', html)
        self.assertIn('header.addEventListener(\'click\', toggleRubric);', html)

if __name__ == '__main__':
    unittest.main()
