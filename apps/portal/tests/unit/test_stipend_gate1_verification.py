import sys
import os
import unittest
import requests

class TestStipendGate1Verification(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5001"

    def setUp(self):
        self.session = requests.Session()
        # Impersonate Gate 1 locked candidate holding Provisional CERT-DBERT-2026-FSD-901
        res = self.session.get(
            f"{self.BASE_URL}/dev/impersonate?email=stipend_gate1_locked@dbert.test",
            allow_redirects=False
        )
        self.assertIn(res.status_code, (200, 302))

    def test_gate1_renders_299_verification_and_no_1500_balance(self):
        """Verifies Gate 1 displays ₹299 official verification gateway and removes ₹1,500 balance."""
        res = self.session.get(f"{self.BASE_URL}/stipend/tasks")
        self.assertEqual(res.status_code, 200)
        html = res.text

        # 1. Provisional cert should be identified
        self.assertIn("CERT-DBERT-2026-FSD-901", html)

        # 2. Gate 1 text must mention ₹299 official credential verification
        self.assertIn("₹299 official credential verification", html)
        self.assertIn("OPTION A: COMPLETE ₹299 VERIFICATION &amp; UNLOCK STIPEND", html)
        self.assertIn("Complete official <strong>₹299 project verification</strong>", html)
        self.assertIn("Complete ₹299 Verification &amp; Unlock Stipend", html)

        # 3. URL must deep link to /verify/unlock with certid and email
        expected_unlock_url = "https://dbert.in/verify/unlock?certid=CERT-DBERT-2026-FSD-901&amp;email=stipend_gate1_locked@dbert.test"
        self.assertIn(expected_unlock_url, html)

        # 4. Must NOT mention ₹1,500 balance or /enroll/1999 anywhere on Gate 1
        self.assertNotIn("₹1,500", html)
        self.assertNotIn("1,500 balance", html)
        self.assertNotIn("enroll/1999", html)


if __name__ == "__main__":
    unittest.main()
