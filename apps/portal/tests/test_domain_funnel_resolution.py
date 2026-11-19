import unittest
import os
import sys

# Ensure apps/portal is on sys.path
PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)

from app import (
    app,
    get_db,
    VALID_DOMAINS,
    CANONICAL_DOMAIN_MAP,
    normalize_domain_string,
    get_intern_flow_state,
    STAGE_CONFIRMED,
    STAGE_APP_REQUIRED,
)


class TestDomainFunnelResolution(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_canonical_normalization(self):
        """Tests that various raw strings, slugs, and synonyms normalize to canonical VALID_DOMAINS."""
        # 1. Exact matches
        for vd in VALID_DOMAINS:
            self.assertEqual(normalize_domain_string(vd), vd)

        # 2. Data Analyst synonyms & variations
        self.assertEqual(normalize_domain_string("Data Analytics"), "Data Analyst")
        self.assertEqual(normalize_domain_string("data-analytics"), "Data Analyst")
        self.assertEqual(normalize_domain_string("data science"), "Data Analyst")
        self.assertEqual(normalize_domain_string("data-science"), "Data Analyst")
        self.assertEqual(normalize_domain_string("da"), "Data Analyst")

        # 3. Full Stack Development variations
        self.assertEqual(normalize_domain_string("Full Stack Web Development"), "Full Stack Development")
        self.assertEqual(normalize_domain_string("full-stack-development"), "Full Stack Development")
        self.assertEqual(normalize_domain_string("web development"), "Full Stack Development")
        self.assertEqual(normalize_domain_string("fsd"), "Full Stack Development")

        # 4. AI & ML variations
        self.assertEqual(normalize_domain_string("AI & Machine Learning"), "AI Agent Development")
        self.assertEqual(normalize_domain_string("ai and machine learning"), "AI Agent Development")
        self.assertEqual(normalize_domain_string("aiml"), "AI Agent Development")
        self.assertEqual(normalize_domain_string("ai-agent"), "AI Agent Development")

        # 5. Python Automation
        self.assertEqual(normalize_domain_string("python developer"), "Python Automation")
        self.assertEqual(normalize_domain_string("python-automation"), "Python Automation")
        self.assertEqual(normalize_domain_string("python"), "Python Automation")

        # 6. UI/UX
        self.assertEqual(normalize_domain_string("ui/ux"), "UI/UX Design")
        self.assertEqual(normalize_domain_string("ui design"), "UI/UX Design")
        self.assertEqual(normalize_domain_string("ui-ux-design"), "UI/UX Design")

        # 7. DevOps & Cloud
        self.assertEqual(normalize_domain_string("devops"), "DevOps & Cloud")
        self.assertEqual(normalize_domain_string("cloud computing"), "DevOps & Cloud")

        # 8. Mobile App Development
        self.assertEqual(normalize_domain_string("android app development"), "Mobile App Development")
        self.assertEqual(normalize_domain_string("flutter"), "Mobile App Development")

        # 9. Invalid / unrecognized
        self.assertIsNone(normalize_domain_string(None))
        self.assertIsNone(normalize_domain_string(""))
        self.assertIsNone(normalize_domain_string("Quantum Astrophysics"))

    def test_flow_state_auto_healing(self):
        """Tests that get_intern_flow_state normalizes domain from linked records and updates intern_accounts."""
        test_email = "test_funnel_heal@dbert.test"
        with get_db() as conn:
            # Clean up previous test runs
            conn.execute("DELETE FROM intern_accounts WHERE LOWER(email)=?", (test_email,))
            conn.execute("DELETE FROM applications WHERE LOWER(email)=?", (test_email,))
            conn.execute("DELETE FROM enrollments WHERE LOWER(email)=?", (test_email,))
            conn.execute("DELETE FROM intern_offer_letters WHERE LOWER(email)=?", (test_email,))
            if hasattr(conn, "commit"):
                conn.commit()

            # Insert intern with non-canonical domain 'Data Analytics'
            conn.execute(
                """
                INSERT INTO intern_accounts (name, email, phone, password_hash, domain, college, course, is_active, signup_stage)
                VALUES ('Test User', ?, '9999999999', 'hash', 'Data Analytics', 'Test College', 'B.Tech', 1, 3)
                """,
                (test_email,)
            )
            # Insert application with 'Accepted' status to reach Stage 5
            conn.execute(
                """
                INSERT INTO applications (name, email, phone, city, domain, college, course, semester, year_of_passing, status)
                VALUES ('Test User', ?, '9999999999', 'Delhi', 'data analytics', 'Test College', 'B.Tech', '6th Semester', '2026', 'Accepted')
                """,
                (test_email,)
            )
            if hasattr(conn, "commit"):
                conn.commit()

            # Run flow state
            st = get_intern_flow_state(conn, test_email)
            self.assertEqual(st["stage_num"], 5)
            self.assertEqual(st["stage"], STAGE_CONFIRMED)
            # Must be healed to canonical 'Data Analyst'
            self.assertEqual(st["domain"], "Data Analyst")

            # Check that intern_accounts.domain was auto-updated in database
            acct = conn.execute("SELECT domain FROM intern_accounts WHERE LOWER(email)=?", (test_email,)).fetchone()
            self.assertEqual(acct["domain"], "Data Analyst")

            # Clean up
            conn.execute("DELETE FROM intern_accounts WHERE LOWER(email)=?", (test_email,))
            conn.execute("DELETE FROM applications WHERE LOWER(email)=?", (test_email,))
            if hasattr(conn, "commit"):
                conn.commit()

    def test_portal_html_hierarchy(self):
        """Tests that portal.html places #nextActionMissionCard before #academicProfileBanner,
        and contains the domain fallback selection modal."""
        template_path = os.path.join(PORTAL_DIR, "templates", "portal.html")
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check DOM ordering
        mission_pos = content.find('id="nextActionMissionCard"')
        banner_pos = content.find('id="academicProfileBanner"')
        stepbar_pos = content.find('id="overviewStepBar"')
        accepted_pos = content.find('id="ovAccepted"')

        self.assertNotEqual(mission_pos, -1, "nextActionMissionCard not found")
        self.assertNotEqual(banner_pos, -1, "academicProfileBanner not found")
        self.assertNotEqual(stepbar_pos, -1, "overviewStepBar not found")
        self.assertNotEqual(accepted_pos, -1, "ovAccepted not found")

        # mission card comes before academic banner
        self.assertLess(mission_pos, banner_pos, "Mission card must be placed BEFORE academicProfileBanner")
        # academic banner comes before stepbar
        self.assertLess(banner_pos, stepbar_pos, "Academic profile banner must be placed before overviewStepBar")
        # stepbar comes before ovAccepted
        self.assertLess(stepbar_pos, accepted_pos, "overviewStepBar must be placed before ovAccepted")

        # Check fallback domain selection modal exists
        self.assertIn('id="domainSelectionModal"', content)
        self.assertIn("confirmDomainSelection('Data Analyst')", content)
        self.assertIn("confirmDomainSelection('AI Agent Development')", content)
        self.assertIn("showDomainSelectionModal", content)


if __name__ == "__main__":
    unittest.main()
