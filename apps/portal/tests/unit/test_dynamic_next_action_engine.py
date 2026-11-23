import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app import build_intern_next_action, STAGE_CONFIRMED


class TestDynamicNextActionEngine(unittest.TestCase):
    def setUp(self):
        self.flow_state = {
            "stage_num": 5,
            "stage": STAGE_CONFIRMED,
            "domain": "Artificial Intelligence & ML",
            "has_paid_balance": False,
            "days_since_joining": 14,
        }

    def test_case_1_active_coursework_progression(self):
        """Active enrolled course with pending days should recommend resume sprint lesson."""
        sprint_ctx = {
            "course_active": {
                "course_id": 7,
                "course_title": "AI & Prompt Engineering Sprints",
                "current_day": 3,
                "total_days": 10,
                "completed_at": None,
            },
            "g1_linkedin": False,
            "g2_article": False,
            "g3_verified": False,
            "g4_github": False,
            "unlocked_gates_count": 0,
            "top_bounty": {"id": 101, "title": "Model Evaluation Benchmark", "coin_reward": 50},
        }
        res = build_intern_next_action(self.flow_state, hours_logged=4.5, sprint_ctx=sprint_ctx)
        self.assertEqual(res["stage_badge"], "Stage 5: Sprint Day 3 of 10")
        self.assertIn("Resume Sprint: AI & Prompt Engineering Sprints (Day 3)", res["heading"])
        self.assertEqual(res["primary_cta_url"], "/courses/7")
        self.assertEqual(res["primary_cta_label"], "Resume Day 3 Sprint Lesson →")
        self.assertNotIn("1,500", res["primary_cta_label"])
        self.assertNotIn("1,500", res["description"])
        self.assertNotIn("1,500", str(res.get("secondary_cta_label", "")))
        self.assertNotIn("1,500", str(res.get("tertiary_cta_label", "")))

    def test_case_2_gate_1_linkedin_recommendation(self):
        """When course is completed/idle and LinkedIn missing, recommends Gate 1."""
        sprint_ctx = {
            "course_active": None,
            "g1_linkedin": False,
            "g2_article": False,
            "g3_verified": False,
            "g4_github": False,
            "unlocked_gates_count": 0,
        }
        res = build_intern_next_action(self.flow_state, hours_logged=10.0, sprint_ctx=sprint_ctx)
        self.assertIn("Stipend Gate 1", res["stage_badge"])
        self.assertIn("LinkedIn", res["heading"])
        self.assertEqual(res["primary_cta_url"], "/account")
        self.assertNotIn("1,500", str(res))

    def test_case_3_gate_2_case_study_article(self):
        """When Gate 1 done, missing article, recommends Gate 2."""
        sprint_ctx = {
            "course_active": None,
            "g1_linkedin": True,
            "g2_article": False,
            "g3_verified": False,
            "g4_github": False,
            "unlocked_gates_count": 1,
        }
        res = build_intern_next_action(self.flow_state, hours_logged=10.0, sprint_ctx=sprint_ctx)
        self.assertIn("Stipend Gate 2", res["stage_badge"])
        self.assertIn("Technical Case Study", res["heading"])
        self.assertEqual(res["primary_cta_url"], "/portal")
        self.assertNotIn("1,500", str(res))

    def test_case_4_gate_3_credential_verification(self):
        """When Gate 1 & 2 done, missing verified credential, recommends Gate 3."""
        sprint_ctx = {
            "course_active": None,
            "g1_linkedin": True,
            "g2_article": True,
            "g3_verified": False,
            "g4_github": False,
            "unlocked_gates_count": 2,
        }
        res = build_intern_next_action(self.flow_state, hours_logged=10.0, sprint_ctx=sprint_ctx)
        self.assertIn("Stipend Gate 3", res["stage_badge"])
        self.assertIn("Verify Official Credential", res["heading"])
        self.assertEqual(res["primary_cta_url"], "/verify/unlock")
        self.assertNotIn("1,500", str(res))

    def test_case_5_gate_4_github_capstone_pr(self):
        """When Gate 1, 2, 3 done, missing GitHub capstone, recommends Gate 4."""
        sprint_ctx = {
            "course_active": None,
            "g1_linkedin": True,
            "g2_article": True,
            "g3_verified": True,
            "g4_github": False,
            "unlocked_gates_count": 3,
        }
        res = build_intern_next_action(self.flow_state, hours_logged=10.0, sprint_ctx=sprint_ctx)
        self.assertIn("Stipend Gate 4", res["stage_badge"])
        self.assertIn("GitHub Capstone", res["heading"])
        self.assertEqual(res["primary_cta_url"], "/tasks")
        self.assertNotIn("1,500", str(res))

    def test_case_6_all_gates_completed_stipend_ready(self):
        """When all 4 gates complete, surfaces ₹5,000 stipend release ready."""
        sprint_ctx = {
            "course_active": None,
            "g1_linkedin": True,
            "g2_article": True,
            "g3_verified": True,
            "g4_github": True,
            "unlocked_gates_count": 4,
        }
        res = build_intern_next_action(self.flow_state, hours_logged=12.0, sprint_ctx=sprint_ctx)
        self.assertIn("All 4 Gates Verified", res["stage_badge"])
        self.assertIn("₹5,000 Milestone Stipend Ready", res["heading"])
        self.assertEqual(res["primary_cta_url"], "/tasks")
        self.assertNotIn("1,500", str(res))


if __name__ == "__main__":
    unittest.main()
