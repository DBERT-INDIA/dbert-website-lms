"""Exercise the production quiz template and CSP handlers in Chromium."""

from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, render_template
from playwright.sync_api import expect, sync_playwright


PORTAL = Path(__file__).resolve().parents[2]


def test_quiz_moves_one_question_and_restores_the_draft():
    app = Flask(__name__, template_folder=str(PORTAL / "templates"))
    origin = "https://course-quiz.test"
    quiz = "/courses/1/quiz/3"
    attempt = "c" * 32
    submissions = []

    def handle(route):
        url = urlsplit(route.request.url)
        if url.netloc != "course-quiz.test":
            route.abort()
        elif url.path == quiz:
            with app.test_request_context(quiz):
                html = render_template(
                    "course_quiz.html", csp_nonce=lambda: "sample", csrf_token=lambda: "test-token",
                    course={"id": 1, "title": "Data handling", "requires_project": True},
                    chapter={"title": "Reading records"}, day_number=3, attempt_key=attempt, elapsed_seconds=12,
                    questions=[{"id": i, "question": f"Practice question {i}", "options": ["Keep", "Discard"]}
                               for i in range(1, 4)],
                )
            route.fulfill(
                body=html, content_type="text/html; charset=utf-8",
                headers={"Content-Security-Policy": "default-src 'self'; script-src 'self' 'nonce-sample'; style-src 'self' 'unsafe-inline'"},
            )
        elif url.path == quiz + "/submit":
            assert route.request.headers["x-csrf-token"] == "test-token"
            submissions.append(route.request.post_data_json)
            route.fulfill(json={"status": "success", "score": 3, "max_score": 3, "passed": True,
                                "course_completed": True, "certificate_issued": True,
                                "cert_url": "/portal/certificate/sample"})
        elif url.path.startswith("/static/"):
            asset = PORTAL / url.path.removeprefix("/")
            if asset.is_file():
                route.fulfill(path=asset)
            else:
                route.fulfill(status=404)
        else:
            route.fulfill(status=404)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, args=["--host-resolver-rules=MAP * ~NOTFOUND"])
        page = browser.new_page(service_workers="block")
        page.route("**/*", handle)
        page.goto(origin + quiz)
        page.get_by_role("button", name="Next").click()
        expect(page.get_by_role("heading", name="Q1. Practice question 1")).to_be_visible()
        page.get_by_role("radio", name="Keep").check()
        page.get_by_role("button", name="Next").click()
        expect(page.get_by_role("heading", name="Q2. Practice question 2")).to_be_visible()

        page.reload()
        expect(page.get_by_role("heading", name="Q2. Practice question 2")).to_be_visible()
        page.get_by_role("button", name="Back").click()
        expect(page.get_by_role("radio", name="Keep")).to_be_checked()
        page.get_by_role("button", name="Next").click()
        page.get_by_role("radio", name="Discard").check()
        page.get_by_role("button", name="Next").click()
        page.get_by_role("radio", name="Keep").check()
        page.get_by_role("button", name="Submit Quiz").click()
        expect(page.get_by_role("dialog", name="Course quizzes completed")).to_be_visible()
        expect(page.get_by_role("heading", name="Course quizzes completed")).to_be_focused()
        expect(page.get_by_role("link", name="Open required capstone")).to_have_attribute("href", "/courses/1/submit-project")
        expect(page.get_by_text("Final quiz score 3 / 3")).to_be_visible()
        assert len(submissions) == 1
        assert submissions[0]["attempt_key"] == attempt
        assert submissions[0]["answers"] == {"1": 0, "2": 1, "3": 0}
        browser.close()
