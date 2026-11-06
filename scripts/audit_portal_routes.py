import os
import sys
import unittest

sys.path.insert(0, os.path.abspath("apps/portal"))
from app import app, get_db

class PortalAuditTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_database_connection(self):
        with app.app_context():
            with get_db() as conn:
                res = conn.execute("SELECT 1").fetchone()
                self.assertIsNotNone(res)
                print(" [PASS] Database connection check")

    def test_core_public_routes(self):
        public_routes = [
            ("/", 200),
            ("/program", 200),
            ("/jobs", 200),
            ("/internships", 200),
            ("/internships?tab=all", 200),
            ("/sitemap.xml", 200),
            ("/robots.txt", 200),
            ("/terms", 200),
            ("/privacy", 200),
            ("/health", 200),
            ("/cert/verify", 200),
        ]
        for route, expected_code in public_routes:
            with self.subTest(route=route):
                res = self.client.get(route)
                self.assertEqual(res.status_code, expected_code, f"Route {route} returned {res.status_code}")
                print(f" [PASS] {route} -> HTTP {res.status_code}")

    def test_seo_programmatic_routes(self):
        seo_routes = [
            "/internships/ai-agent-development",
            "/internships/full-stack-development",
            "/internships/data-analyst",
            "/internships/python-automation",
            "/jobs/ai-agent-development",
            "/jobs/full-stack-development",
            "/internships/ai-agent-development/bangalore",
            "/internships/data-analyst/pune",
            "/jobs/python-automation/hyderabad",
            "/internships/work-from-home/ai-agent-development",
            "/internships/paid/data-analyst",
            "/jobs/work-from-home/full-stack-development",
            "/jobs/paid/python-automation",
            "/internships/virtual-remote-internships",
            "/internships/paid-internships",
        ]
        for route in seo_routes:
            with self.subTest(route=route):
                res = self.client.get(route)
                self.assertEqual(res.status_code, 200, f"SEO route {route} returned {res.status_code}")
                print(f" [PASS] SEO {route} -> HTTP {res.status_code}")

    def test_lead_detail_routes(self):
        # Fetch one scraped internship and one scraped job from DB
        with app.app_context():
            with get_db() as conn:
                s_intern = conn.execute("SELECT id, Role, Company FROM scraped_internships LIMIT 1").fetchone()
                s_job = conn.execute("SELECT id, Role, Company FROM scraped_jobs LIMIT 1").fetchone()

        if s_intern:
            url = f"/internship/lead/{s_intern['id']}"
            res = self.client.get(url, follow_redirects=True)
            self.assertEqual(res.status_code, 200, f"Internship lead detail {url} failed with {res.status_code}")
            print(f" [PASS] Scraped lead detail {url} -> HTTP {res.status_code}")

        if s_job:
            url = f"/job/lead/{s_job['id']}"
            res = self.client.get(url, follow_redirects=True)
            self.assertEqual(res.status_code, 200, f"Job lead detail {url} failed with {res.status_code}")
            print(f" [PASS] Scraped job detail {url} -> HTTP {res.status_code}")

    def test_auth_protection_and_redirects(self):
        protected_routes = [
            ("/admin", (302, 303)),
            ("/portal", (302, 303)),
            ("/intern/tutor", (302, 303)),
            ("/intern/coins", (302, 401)),
            ("/intern/certificates", (302, 401)),
        ]
        for route, expected_codes in protected_routes:
            with self.subTest(route=route):
                res = self.client.get(route)
                if isinstance(expected_codes, int):
                    expected_codes = (expected_codes,)
                self.assertIn(res.status_code, expected_codes, f"Protected route {route} status {res.status_code}")
                print(f" [PASS] Protected route {route} -> HTTP {res.status_code}")

if __name__ == "__main__":
    unittest.main()
