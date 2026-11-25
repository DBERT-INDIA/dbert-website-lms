"""Regression tests for payment-state & stage-state UX across /stipend/tasks, /certificates, /portal/offer, and /portal."""

import os
import sys
from pathlib import Path
import pytest

PORTAL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PORTAL_DIR))

os.environ.setdefault("REQUIRE_POSTGRES", "false")
os.environ.setdefault("TESTING", "true")

import app as portal_app  # noqa: E402


@pytest.fixture()
def client():
    portal_app.app.config["TESTING"] = True
    with portal_app.app.test_client() as c:
        yield c


def _impersonate(client, email, target="/portal"):
    resp = client.get(f"/dev/impersonate?email={email}&target={target}", follow_redirects=True)
    assert resp.status_code == 200
    return resp.get_data(as_text=True)


def test_paid_1999_fellow_sees_no_upgrade_cta_on_stipend_tasks(client):
    html = _impersonate(client, "fellow_paid_1999@dbert.test", "/stipend/tasks")
    assert "₹1,999 Fellowship Settled" in html
    assert "Complete Sprint Milestones (/tasks)" in html
    assert "Upgrade to ₹1,999 Fellowship" not in html
    assert "Enroll in ₹1,999 Fellowship" not in html


def test_paid_1999_fellow_certificates_clean(client):
    html = _impersonate(client, "fellow_paid_1999@dbert.test", "/certificates")
    assert "Sprints Active" in html
    assert "Unlock for ₹299" not in html
    assert "₹1,500 Incubation Balance" not in html
    assert "Upgrade to ₹1,999 Fellowship" not in html


def test_paid_1999_fellow_offer_letter_no_redundant_1999_cta(client):
    html = _impersonate(client, "fellow_paid_1999@dbert.test", "/portal/offer")
    assert "Enroll in Incubation &amp; Paid Fellowship (₹1,999)" not in html


def test_paid_1999_fellow_portal_terms_copy(client):
    html = _impersonate(client, "fellow_paid_1999@dbert.test", "/portal")
    assert "5,000 Coins (60-Day)" in html
    assert "3-Doc Credential Packet" in html
    assert "₹5,000 / Sprint" not in html
    assert "2 Verifiable Certs" not in html


def test_deposit_499_fellow_sees_1999_upgrade_and_no_retired_299_1500(client):
    stipend_html = _impersonate(client, "stage5_enrolled@dbert.test", "/stipend/tasks")
    assert "Upgrade to ₹1,999 Fellowship" in stipend_html

    certs_html = _impersonate(client, "stage5_enrolled@dbert.test", "/certificates")
    assert "Unlock for ₹299" not in certs_html
    assert "₹1,500 Incubation Balance" not in certs_html


def test_stage0_rejected_hides_under_review_and_legacy_program_link(client):
    html = _impersonate(client, "rejected_user@dbert.test", "/portal")
    assert 'id="under-review-notice"' not in html
    assert 'Enroll in ₹1,999 Fellowship' in html
    assert 'source=portal_overview_rejected' in html or 'https://dbert.in/enroll/1999' in html
