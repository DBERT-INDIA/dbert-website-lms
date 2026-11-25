"""Exercise the résumé checker with a browser-enforced script policy."""

from collections import deque
from email import policy
from email.parser import BytesParser
from pathlib import Path
from secrets import token_urlsafe
from urllib.parse import urlsplit

import pytest
from flask import Flask, render_template
from playwright.sync_api import expect, sync_playwright


PORTAL = Path(__file__).resolve().parents[2]
ORIGIN = "https://resume-checker.test"
ENDPOINT = "/api/tools/ats-checker"
FULL_STACK = "Full Stack Development"
AI_AGENT = "AI Agent Development"
BASELINE_TEXT = "Built a synthetic inventory app and documented the REST API."
REVISION_TEXT = "Built and tested a synthetic inventory app with REST and PostgreSQL."


@pytest.fixture(scope="module")
def chromium():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=["--host-resolver-rules=MAP * ~NOTFOUND"],
        )
        yield browser
        browser.close()


def multipart_fields(request):
    content_type = request.headers["content-type"]
    headers = f"Content-Type: {content_type}\r\n\r\n".encode()
    message = BytesParser(policy=policy.default).parsebytes(headers + request.post_data_buffer)
    return {
        part.get_param("name", header="content-disposition"): (
            part.get_filename() or part.get_payload(decode=True).decode("utf-8")
        )
        for part in message.iter_parts()
    }


@pytest.fixture
def checker(chromium):
    app = Flask(__name__, template_folder=str(PORTAL / "templates"))
    nonce = token_urlsafe(16)
    with app.test_request_context():
        html = render_template(
            "resume_checker.html",
            csp_nonce=lambda: nonce,
            csrf_token=lambda: "test-csrf-token",
            SITE_ORIGIN=ORIGIN,
        )

    headers = {
        "Content-Security-Policy": (
            f"default-src 'self'; script-src 'self' 'nonce-{nonce}'; "
            "style-src 'self' 'unsafe-inline'; object-src 'none'"
        )
    }
    responses = deque()
    requests = []
    context = chromium.new_context(service_workers="block")
    static_dir = PORTAL / "static"

    def handle_route(route):
        request = route.request
        url = urlsplit(request.url)
        if url.netloc != "resume-checker.test":
            route.abort()
        elif url.path == "/resume-checker":
            route.fulfill(headers=headers, content_type="text/html", body=html)
        elif url.path == ENDPOINT and request.method == "POST":
            requests.append(multipart_fields(request))
            if responses:
                status, data = responses.popleft()
                route.fulfill(status=status, json=data)
            else:
                route.fulfill(status=500, json={"status": "error", "message": "Unexpected scan"})
        elif url.path.startswith("/static/"):
            asset = (static_dir / url.path.removeprefix("/static/")).resolve()
            if asset.is_relative_to(static_dir) and asset.is_file():
                route.fulfill(path=asset)
            else:
                route.fulfill(status=404)
        else:
            route.abort()

    context.route("**/*", handle_route)
    try:
        page = context.new_page()
        page.set_default_timeout(5_000)
        page.goto(f"{ORIGIN}/resume-checker")
        yield page, responses, requests
    finally:
        context.close()


def report(score, *, domain=FULL_STACK, locked=True):
    breakdown = {
        name: {"percentage": score, "score": score * maximum // 100, "max": maximum}
        for name, maximum in (
            ("keywords", 30),
            ("impact_verbs", 25),
            ("structure", 20),
            ("length_hygiene", 15),
            ("domain_alignment", 10),
        )
    }
    return 200, {
        "status": "success",
        "score": score,
        "tier": "Developing",
        "color": "#10B981",
        "pass_probability": "Moderate",
        "domain": domain,
        "breakdown": breakdown,
        "stats": {"found_keywords": [], "missing_keywords_count": 1},
        "strengths": ["Contains synthetic project experience."],
        "locked": locked,
        "critical_missing_keywords": [] if locked else ["PostgreSQL"],
        "recommendations": {"bullet_rewrites": []},
        "matched_jobs": [],
    }


def scan_text(page, text, score):
    page.locator("#resumeText").fill(text)
    page.locator("#btnScan").click()
    expect(page.locator("#scoreNum")).to_have_text(str(score))


def expect_comparison(page, baseline, revision, delta):
    row = page.locator("#comparisonTable tr").filter(has_text="ATS score")
    expect(row.locator("th, td")).to_have_text(
        ["ATS score", str(baseline), str(revision), delta]
    )


def test_baseline_compares_only_completed_scans_for_the_same_domain(checker):
    page, responses, requests = checker
    responses.extend([report(60), report(75), report(82, domain=AI_AGENT), report(56)])

    page.locator("#tabPasteBtn").press("Enter")
    expect(page.locator("#resumeText")).to_be_visible()
    scan_text(page, BASELINE_TEXT, 60)
    page.get_by_role("button", name="Set as baseline").click()
    expect(page.locator("#comparisonTable")).to_be_hidden()

    scan_text(page, REVISION_TEXT, 75)
    expect_comparison(page, 60, 75, "+15")

    page.locator(f'[data-domain="{AI_AGENT}"]').click()
    scan_text(page, REVISION_TEXT, 82)
    expect(page.locator("#comparisonTable")).to_be_hidden()
    expect(page.locator("#comparisonStatus")).not_to_be_empty()

    page.locator(f'[data-domain="{FULL_STACK}"]').click()
    scan_text(page, REVISION_TEXT, 56)
    expect_comparison(page, 60, 56, "−4")

    page.get_by_role("button", name="Clear baseline").click()
    expect(page.locator("#comparisonTable")).to_be_hidden()
    expect(page.locator("#scoreNum")).to_have_text("56")
    assert requests == [
        {"domain": FULL_STACK, "text": BASELINE_TEXT},
        {"domain": FULL_STACK, "text": REVISION_TEXT},
        {"domain": AI_AGENT, "text": REVISION_TEXT},
        {"domain": FULL_STACK, "text": REVISION_TEXT},
    ]


def test_failed_scan_and_report_unlock_preserve_revision(checker):
    page, responses, requests = checker
    responses.extend(
        [
            report(60),
            report(75),
            (400, {"status": "error", "message": "Synthetic scan failed"}),
            report(75, locked=False),
        ]
    )
    page.locator("#tabPasteBtn").click()
    scan_text(page, BASELINE_TEXT, 60)
    page.locator("#saveBaseline").click()
    scan_text(page, REVISION_TEXT, 75)

    page.locator("#resumeText").fill("An unfinished edit that was never accepted.")
    page.locator("#btnScan").click()
    expect(page.locator("#scanError")).to_contain_text("Synthetic scan failed")
    expect(page.locator("#scoreNum")).to_have_text("75")
    expect_comparison(page, 60, 75, "+15")

    page.locator(f'[data-domain="{AI_AGENT}"]').click()
    page.get_by_label("Full name").fill("Synthetic Candidate")
    page.get_by_label("Email address").fill("candidate@example.test")
    page.get_by_label("Email address").press("Enter")
    expect(page.locator("#unlockedContent")).to_be_visible()
    expect_comparison(page, 60, 75, "+15")
    assert len(requests) == 4
    assert requests[-1]["text"] == REVISION_TEXT
    assert requests[-1]["domain"] == FULL_STACK
    assert requests[-1]["email"] == "candidate@example.test"


def test_pdf_picker_and_scan_work_from_the_keyboard(checker):
    page, responses, requests = checker
    responses.append(report(60))
    with page.expect_file_chooser() as event:
        page.locator("#dropZone").press("Enter")
    event.value.set_files(
        {"name": "synthetic.pdf", "mimeType": "application/pdf", "buffer": b"%PDF-1.4\n"}
    )
    expect(page.locator("#dropLabel")).to_contain_text("synthetic.pdf")

    page.locator("#btnScan").press("Enter")
    expect(page.locator("#scoreNum")).to_have_text("60")
    assert requests == [{"domain": FULL_STACK, "file": "synthetic.pdf"}]


def test_job_description_evidence_uses_the_audited_inputs(checker):
    page, responses, requests = checker
    _, sample = report(74)
    sample["job_fit"] = {
        "matched": ["React"], "missing": ["PostgreSQL"],
        "next_steps": [{"label": "Find DBERT resources for PostgreSQL", "href": "/search?q=PostgreSQL"}],
    }
    responses.append((200, sample))
    page.locator("#tabPasteBtn").click()
    page.get_by_text("Compare with a job description", exact=True).click()
    page.locator("#atsJobDescription").fill("Experience with React and PostgreSQL.")
    scan_text(page, REVISION_TEXT, 74)
    expect(page.locator("#atsJobFit")).to_be_visible()
    expect(page.locator("#atsJobFitSkills")).to_contain_text("React — Mentioned")
    expect(page.locator("#atsJobFitSkills")).to_contain_text("PostgreSQL — Needs evidence")
    expect(page.get_by_role("link", name="Find DBERT resources for PostgreSQL")).to_have_attribute("href", "/search?q=PostgreSQL")
    assert requests[-1]["job_description"] == "Experience with React and PostgreSQL."
