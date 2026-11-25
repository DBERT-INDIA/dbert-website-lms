"""Browser checks for the real classroom template and synthetic study data."""

from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from flask import Flask, render_template
from playwright.sync_api import expect, sync_playwright


PORTAL = Path(__file__).resolve().parents[2]
ORIGIN = "https://study-classroom.test"
CLASSROOM = "/courses/7/study"
API = "/api/study-classroom/7"
LESSONS = {
    11: {
        "id": 11,
        "title": "Filtering input",
        "day_number": 1,
        "sections": [{"id": "filter-step", "title": "Choose valid rows", "text": "Retain valid rows before processing."}],
    },
    22: {
        "id": 22,
        "title": "Grouping output",
        "day_number": 2,
        "sections": [
            {"id": "source-intro", "title": "Grouping basics", "text": "Collect rows with the same key."},
            {"id": "flow", "title": "Build grouped output", "text": "Return one record per key."},
        ],
    },
}
QUESTION = "What happens after filtering?"


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as playwright:
        active = playwright.chromium.launch(headless=True, args=["--host-resolver-rules=MAP * ~NOTFOUND"])
        yield active
        active.close()


@pytest.fixture
def classroom(browser):
    app = Flask(__name__, template_folder=str(PORTAL / "templates"))
    records = {
        "entries": {},
        "notes": {11: {"text": "Saved draft", "version": 1}},
        "failed_asks": 0,
        "older_entry": None,
        "requests": [],
    }
    context = browser.new_context(viewport={"width": 1280, "height": 850}, service_workers="block")
    errors = []

    def handle(route):
        request = route.request
        url = urlsplit(request.url)
        if url.netloc != "study-classroom.test":
            route.abort()
            return
        if url.path == CLASSROOM:
            lesson_id = int(parse_qs(url.query).get("lesson_id", ["11"])[0])
            with app.test_request_context():
                html = render_template(
                    "study_classroom.html",
                    csrf_token=lambda: "synthetic-csrf",
                    study_course={"id": 7, "title": "Data pipeline basics"},
                    study_lessons=list(LESSONS.values()),
                    study_active_lesson=lesson_id,
                )
            route.fulfill(
                body=html,
                content_type="text/html; charset=utf-8",
                headers={"Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"},
            )
            return
        if url.path.startswith("/static/"):
            asset = PORTAL / url.path.removeprefix("/")
            route.fulfill(path=asset)
            return
        if url.path.startswith(API):
            path = url.path.removeprefix(API)
            data = request.post_data_json if request.method != "GET" else None
            records["requests"].append((request.method, path, data))
            if data is not None:
                assert request.headers["x-csrf-token"] == "synthetic-csrf"
            if path == "/state":
                params = parse_qs(url.query)
                lesson = LESSONS[int(params["lesson_id"][0])]
                entries = list(records["entries"].values())
                older = records["older_entry"]
                if older and params.get("entry_id") == [str(older["id"])]:
                    entries.append(older)
                route.fulfill(json={
                    "lesson": lesson,
                    "trail": entries,
                    "notes": records["notes"].get(lesson["id"], {"text": "", "version": 0}),
                    "followups": [{
                        "title": "Practice grouping", "message": "Revisit grouped output.",
                        "due_on": "2026-12-01", "lesson_id": 22, "practice_url": "/courses/7/quiz/2",
                    }],
                })
            elif path == "/ask":
                if records["failed_asks"]:
                    records["failed_asks"] -= 1
                    route.fulfill(status=503, json={"error": "Tutor temporarily unavailable."})
                    return
                entry = sample_entry(data["question"], data["lesson_id"])
                records["entries"][entry["id"]] = entry
                route.fulfill(json={"entry": entry})
            elif path == "/trail/31":
                entry = records["entries"][31]
                entry["status"] = data["status"]
                route.fulfill(json={"entry": entry})
            elif path == "/notes/11":
                saved = records["notes"][11]
                if data["version"] != saved["version"]:
                    route.fulfill(status=409, json={"error": "Version conflict"})
                else:
                    records["notes"][11] = {"text": data["text"], "version": saved["version"] + 1}
                    route.fulfill(json={"notes": records["notes"][11]})
            else:
                route.fulfill(status=404, json={"error": "Unexpected test request"})
            return
        route.abort()

    def open_page():
        page = context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.set_default_timeout(5000)
        return page

    context.route("**/*", handle)
    try:
        yield open_page(), records
        assert not errors, errors
    finally:
        context.close()


def sample_entry(question=QUESTION, lesson_id=11):
    return {
        "id": 31,
        "lesson_id": lesson_id,
        "question": question,
        "answer": "Build groups for valid rows. The literal <Example> stays visible.\n\n```python\nreturn rows\n```",
        "citations": [{"lesson_id": 22, "section_id": "flow", "title": "Grouped output source", "excerpt": "Return one record per key."}],
        "status": "explored",
        "created_at": "2026-11-24",
        "practice_url": "/courses/7/study/review/31",
    }


def test_desktop_retry_and_review_persist_in_the_trail(classroom):
    page, records = classroom
    records["failed_asks"] = 1
    page.goto(ORIGIN + CLASSROOM)
    expect(page.get_by_role("region", name="Study trail")).to_be_visible()
    expect(page.get_by_role("region", name="Tutor chat")).to_be_visible()
    expect(page.get_by_role("region", name="Lecture")).to_be_visible()
    expect(page.get_by_role("heading", name="Filtering input")).to_be_visible()

    separator = page.get_by_role("separator", name="Study trail width")
    width = int(separator.get_attribute("aria-valuenow"))
    separator.press("ArrowRight")
    expect(separator).to_have_attribute("aria-valuenow", str(width + 24))
    point = separator.bounding_box()
    page.mouse.move(point["x"] + point["width"] / 2, point["y"] + 32)
    page.mouse.down()
    page.mouse.move(point["x"] + point["width"] / 2 + 20, point["y"] + 32)
    page.mouse.up()
    expect(separator).to_have_attribute("aria-valuenow", str(width + 44))

    question = page.get_by_label("Your question")
    question.fill(QUESTION)
    page.get_by_role("button", name="Ask tutor").click()
    expect(page.get_by_text("Tutor temporarily unavailable.")).to_be_visible()
    expect(question).to_have_value(QUESTION)
    page.get_by_role("button", name="Ask tutor").click()
    expect(page.get_by_text("Build groups for valid rows.", exact=False)).to_be_visible()
    expect(page.locator("pre code")).to_have_text("return rows")
    expect(page.locator("example")).to_have_count(0)
    practice = page.get_by_role("link", name="Practice this topic")
    expect(practice).to_have_count(0)
    asks = [data for _, path, data in records["requests"] if path == "/ask"]
    assert asks[0] == asks[1]

    page.get_by_role("button", name="Mark for review").click()
    expect(page.get_by_role("button", name="Mark explored")).to_be_visible()
    expect(practice).to_have_attribute("href", "/courses/7/study/review/31")
    page.reload()
    page.get_by_role("button", name="Needs review 1").click()
    expect(page.get_by_role("region", name="Study trail").get_by_text(QUESTION)).to_be_visible()
    expect(page.get_by_role("heading", name="Mentor follow-ups")).to_be_visible()
    expect(page.get_by_role("link", name="Practice grouping")).to_be_visible()
    expect(page.get_by_role("link", name="Practice this lesson")).to_have_attribute("href", "/courses/7/quiz/2")


def test_mobile_tabs_and_exact_citation_restore_on_reload(classroom):
    page, records = classroom
    records["entries"][31] = sample_entry()
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(ORIGIN + CLASSROOM)
    chat = page.get_by_role("tab", name="Tutor chat")
    trail = page.get_by_role("tab", name="Study trail")
    lecture = page.get_by_role("tab", name="Lecture")
    expect(chat).to_have_attribute("aria-selected", "true")
    chat.press("ArrowLeft")
    expect(trail).to_be_focused()
    expect(chat).to_have_attribute("aria-selected", "false")
    page.get_by_role("link", name=QUESTION, exact=False).click()
    expect(chat).to_have_attribute("aria-selected", "true")
    expect(page.locator("#study-entry-31")).to_be_focused()

    page.get_by_role("link", name="Grouped output source", exact=False).press("Enter")
    expect(lecture).to_have_attribute("aria-selected", "true")
    expect(page.get_by_role("heading", name="Grouping output")).to_be_visible()
    focus = page.locator(".study-source-highlight")
    expect(focus).to_be_focused()
    expect(focus.get_by_role("heading", name="Build grouped output")).to_be_visible()
    assert parse_qs(urlsplit(page.url).query) == {"lesson_id": ["22"], "section_id": ["flow"]}
    page.reload()
    expect(focus).to_be_focused()
    assert page.locator("html").evaluate("(node) => node.scrollWidth === node.clientWidth")

    records["older_entry"] = records["entries"].pop(31)
    page.goto(ORIGIN + CLASSROOM + "?lesson_id=11&entry_id=31")
    expect(chat).to_have_attribute("aria-selected", "true")
    expect(page.locator("#study-entry-31")).to_be_focused()

    trail.click()
    page.get_by_role("link", name="Practice grouping").click()
    expect(lecture).to_have_attribute("aria-selected", "true")
    page.reload()
    expect(lecture).to_have_attribute("aria-selected", "true")
    expect(page.get_by_role("heading", name="Grouping output")).to_be_visible()


def test_notes_keep_a_draft_and_handle_conflicting_saves(classroom):
    page, records = classroom
    page.goto(ORIGIN + CLASSROOM)
    notes = page.get_by_label("Your notes for this lesson")
    expect(notes).to_have_value("Saved draft")
    notes.fill("Unsaved notes about the filter")
    course = page.get_by_label("Current lesson")
    course.select_option("22")
    expect(page.get_by_role("heading", name="Grouping output")).to_be_visible()
    course.select_option("11")
    expect(notes).to_have_value("Unsaved notes about the filter")

    records["notes"][11] = {"text": "Another tab saved these notes", "version": 2}
    page.get_by_role("button", name="Save notes").click()
    expect(page.get_by_text("Saved notes changed in another tab.", exact=False)).to_be_visible()
    expect(notes).to_have_value("Unsaved notes about the filter")
    page.get_by_role("button", name="Load saved notes").click()
    expect(notes).to_have_value("Another tab saved these notes")
    notes.fill("New saved notes")
    page.get_by_role("button", name="Save notes").click()
    expect(page.get_by_text("Notes saved.", exact=True)).to_be_visible()
    page.reload()
    expect(notes).to_have_value("New saved notes")
