import os
import sys

PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PORTAL_DIR not in sys.path:
    sys.path.insert(0, PORTAL_DIR)

import app as portal_app


def test_lms_program_page_publishes_full_syllabi_and_1999_parity():
    portal_app.app.testing = True
    with portal_app.app.test_client() as client:
        resp = client.get("/program")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)

        assert "1,999" in html
        assert "2 Months" in html
        assert "Data Analytics" in html
        for keyword in [
            "Excel",
            "PostgreSQL",
            "Pandas",
            "NumPy",
            "Power BI",
            "Matplotlib",
            "Seaborn",
            "Jupyter",
            "Aivara",
            "Alkame",
            "https://dbert.in/learners/courses/data-analytics",
        ]:
            assert keyword in html, f"Missing '{keyword}' on /program"

        for forbidden in ["3 Months", "3-Month", "28,000", "9,999", "9999"]:
            assert forbidden not in html, f"Forbidden stale string '{forbidden}' found on /program"


def test_lms_launchpad_and_accelerate_enforce_canonical_2month_prices():
    portal_app.app.testing = True
    with portal_app.app.test_client() as client:
        lp = client.get("/launchpad")
        assert lp.status_code == 200
        lp_html = lp.get_data(as_text=True)
        assert "7,999" in lp_html
        assert "2 Months" in lp_html
        assert "DBERT Launchpad" in lp_html
        assert "3 Months" not in lp_html
        assert "28,000" not in lp_html

        acc = client.get("/accelerate")
        assert acc.status_code == 200
        acc_html = acc.get_data(as_text=True)
        assert "4,999" in acc_html
        assert "2 Months" in acc_html
        assert "DBERT Accelerate" in acc_html
        assert "3 Months" not in acc_html
        assert "28,000" not in acc_html


def test_city_slugify_normalizes_accents_and_sitemap_excludes_umlaut_noise():
    assert portal_app._city_slugify("Zürich") == "zurich"
    assert portal_app._city_slugify("München") == "munchen"
    assert portal_app._city_slugify("Bangalore, India") == "bangalore-india"

    portal_app.app.testing = True
    with portal_app.app.test_client() as client:
        resp = client.get("/sitemap.xml")
        assert resp.status_code == 200
        xml = resp.get_data(as_text=True)
        for bad_slug in ["/internships/zrich", "/internships/mnchen", "/jobs/zrich", "/jobs/mnchen"]:
            assert bad_slug not in xml

