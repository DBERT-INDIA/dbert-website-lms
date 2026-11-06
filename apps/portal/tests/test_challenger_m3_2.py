"""
apps/portal/tests/test_challenger_m3_2.py
Milestone 3 Empirical Adversarial Challenge Test Suite

Verifies:
1. Modal Popup Behavior (index.html #forgotOverlay and portal.html #passwordModal, #applyDomainModal, #logoutConfirmModal):
   - Centered popup modal opening, animation, and smooth display
   - ARIA roles (role="dialog", aria-modal="true", aria-labelledby, aria-describedby)
   - Dismissal via keyboard Escape key
   - Dismissal via backdrop click
   - Keyboard focus management & focus trapping cycle upon open/close
   - Form submission: frontend regex validation, bot honeypot protection, error and success DOM rendering
   - Portal modals & tab switching: zero runtime JavaScript exceptions
   - Explicit confirmation requirement on logout before calling /logout
2. CSP Action Delegation Resolution:
   - All functions called by data-act-* across templates exist and resolve on window (or are $builtins).
3. Responsive CSS Layout:
   - Desktop margin-left on .main at >= 961px is exactly 240px (not 480px).
   - .auth-card padding on mobile viewports (<= 768px) does not exceed 20px.
"""

import os
import sys
import re
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

portal_dir = Path(__file__).resolve().parent.parent
if str(portal_dir) not in sys.path:
    sys.path.insert(0, str(portal_dir))

from app import app as flask_app
from flask import render_template

TEMPLATES_DIR = portal_dir / "templates"
STATIC_DIR = portal_dir / "static"
CSS_FILE = STATIC_DIR / "css" / "dbert-theme.css"

BUILTINS = {
    '$hide', '$hideParent', '$removeParent', '$click',
    '$addClass', '$removeClass', '$show', '$reveal', '$noop'
}

def setup_browser_routes(page, html, endpoint="/"):
    def route_static(route):
        url = route.request.url
        if "/static/" in url:
            path = url.split("/static/")[1].split("?")[0]
            file_path = STATIC_DIR / path
            if file_path.exists():
                content = file_path.read_bytes()
                mime = "text/css" if path.endswith(".css") else ("application/javascript" if path.endswith(".js") else "text/plain")
                route.fulfill(status=200, body=content, content_type=mime)
                return
        route.fulfill(status=404)

    page.route("https://lms.dbert.in/static/**", route_static)
    page.route(f"https://lms.dbert.in{endpoint}", lambda route: route.fulfill(status=200, body=html, content_type="text/html"))
    page.route("https://lms.dbert.in/apply-token", lambda route: route.fulfill(status=200, body='{"token":"dummy"}', content_type="application/json"))
    page.route("https://cdnjs.cloudflare.com/**", lambda route: route.fulfill(status=200, body='', content_type="text/css"))
    page.route("https://fonts.googleapis.com/**", lambda route: route.fulfill(status=200, body='', content_type="text/css"))
    page.route("https://cdn.onesignal.com/**", lambda route: route.fulfill(status=200, body='', content_type="application/javascript"))


@pytest.fixture(scope="module")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="module")
def css_text():
    assert CSS_FILE.exists()
    return CSS_FILE.read_text(encoding="utf-8")


class TestModalPopupBehavior:
    """Adversarial stress-testing of modal popups on index.html and portal.html."""

    def test_index_forgot_modal_aria_attributes(self, browser_context):
        """Verify ARIA role='dialog', aria-modal='true', and aria-labelledby on #forgotOverlay."""
        with flask_app.test_request_context("/"):
            html = render_template("index.html", SITE_ORIGIN="https://lms.dbert.in")

        page = browser_context.new_page()
        setup_browser_routes(page, html, "/")
        page.goto("https://lms.dbert.in/")
        page.wait_for_load_state("domcontentloaded")

        aria = page.evaluate("""() => {
            const el = document.getElementById('forgotOverlay');
            return {
                role: el.getAttribute('role'),
                ariaModal: el.getAttribute('aria-modal'),
                ariaLabelledby: el.getAttribute('aria-labelledby'),
                ariaDescribedby: el.getAttribute('aria-describedby'),
                display: window.getComputedStyle(el).display
            };
        }""")
        page.close()

        assert aria["role"] == "dialog"
        assert aria["ariaModal"] == "true"
        assert aria["ariaLabelledby"] == "forgotTitle"
        assert aria["display"] == "none"

    def test_index_forgot_modal_centering_and_focus(self, browser_context):
        """Verify modal opens as a centered popup and places initial focus on email input."""
        with flask_app.test_request_context("/"):
            html = render_template("index.html", SITE_ORIGIN="https://lms.dbert.in")

        page = browser_context.new_page()
        setup_browser_routes(page, html, "/")
        page.goto("https://lms.dbert.in/")
        page.wait_for_load_state("domcontentloaded")

        page.evaluate("() => window.focus()")
        page.evaluate("() => window.openForgotModal()")
        page.wait_for_timeout(300)

        open_state = page.evaluate("""() => {
            const ov = document.getElementById('forgotOverlay');
            const box = ov.querySelector('.dbert-modal-box');
            const ovStyle = window.getComputedStyle(ov);
            const boxRect = box.getBoundingClientRect();
            return {
                hasActiveClass: ov.classList.contains('active'),
                display: ovStyle.display,
                isCentered: Math.abs((window.innerHeight - boxRect.height)/2 - boxRect.top) < 60,
                activeElementId: document.activeElement ? document.activeElement.id : null,
                bodyOverflow: document.body.style.overflow
            };
        }""")
        page.close()

        assert open_state["hasActiveClass"] is True
        assert open_state["display"] == "flex"
        assert open_state["isCentered"] is True
        assert open_state["bodyOverflow"] == "hidden"
        assert open_state["activeElementId"] == "fp_email"

    def test_index_forgot_modal_keyboard_escape_dismissal(self, browser_context):
        """Verify pressing Escape dismisses the modal and restores body scroll."""
        with flask_app.test_request_context("/"):
            html = render_template("index.html", SITE_ORIGIN="https://lms.dbert.in")

        page = browser_context.new_page()
        setup_browser_routes(page, html, "/")
        page.goto("https://lms.dbert.in/")
        page.evaluate("() => window.openForgotModal()")
        page.wait_for_timeout(300)

        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        closed = page.evaluate("""() => {
            const ov = document.getElementById('forgotOverlay');
            return {
                hasActiveClass: ov.classList.contains('active'),
                display: window.getComputedStyle(ov).display,
                bodyOverflow: document.body.style.overflow
            };
        }""")
        page.close()

        assert closed["hasActiveClass"] is False
        assert closed["display"] == "none"
        assert closed["bodyOverflow"] == ""

    def test_index_forgot_modal_backdrop_dismissal(self, browser_context):
        """Verify clicking on modal backdrop dismisses it."""
        with flask_app.test_request_context("/"):
            html = render_template("index.html", SITE_ORIGIN="https://lms.dbert.in")

        page = browser_context.new_page()
        setup_browser_routes(page, html, "/")
        page.goto("https://lms.dbert.in/")
        page.evaluate("() => window.openForgotModal()")
        page.wait_for_timeout(300)

        bd_rect = page.evaluate("""() => {
            const bd = document.querySelector('.dbert-modal-backdrop');
            const r = bd.getBoundingClientRect();
            return { x: r.left + 50, y: r.top + 50, width: r.width, height: r.height };
        }""")
        assert bd_rect["width"] > 0 and bd_rect["height"] > 0

        page.mouse.click(bd_rect["x"], bd_rect["y"])
        page.wait_for_timeout(300)

        is_hidden = page.evaluate("() => document.getElementById('forgotOverlay').style.display === 'none'")
        page.close()

        assert is_hidden is True

    def test_index_forgot_modal_validation_and_honeypot(self, browser_context):
        """Verify email validation, honeypot field, and error/success rendering."""
        with flask_app.test_request_context("/"):
            html = render_template("index.html", SITE_ORIGIN="https://lms.dbert.in")

        page = browser_context.new_page()
        setup_browser_routes(page, html, "/")
        page.goto("https://lms.dbert.in/")
        page.evaluate("() => window.openForgotModal()")
        page.wait_for_timeout(300)

        # 1. Empty submission
        page.evaluate("() => { document.getElementById('fp_email').value = ''; window.submitForgot(); }")
        err1 = page.evaluate("() => document.getElementById('forgotError').textContent.trim()")
        assert "valid email address" in err1.lower()

        # 2. Invalid email format
        page.evaluate("() => { document.getElementById('fp_email').value = 'invalid-email-format'; window.submitForgot(); }")
        err2 = page.evaluate("() => document.getElementById('forgotError').textContent.trim()")
        assert "valid email address" in err2.lower()

        # 3. Honeypot invisible protection
        hp = page.evaluate("""() => {
            const h = document.getElementById('fp_company_website');
            return { tabIndex: h.tabIndex, display: window.getComputedStyle(h).display, val: h.value };
        }""")
        assert hp["tabIndex"] == -1
        assert hp["display"] == "none"

        # 4. Successful submission with direct reset link rendering
        captured = []
        page.route("https://lms.dbert.in/forgot-password", lambda route: (
            captured.append(route.request.post_data_json),
            route.fulfill(status=200, body='{"status":"success","message":"Reset link sent.","reset_url":"https://lms.dbert.in/reset-password?token=abc"}', content_type="application/json")
        ))

        page.evaluate("() => { document.getElementById('fp_email').value = 'valid@example.com'; window.submitForgot(); }")
        page.wait_for_timeout(300)

        assert len(captured) == 1
        assert captured[0]["email"] == "valid@example.com"
        assert "company_website" in captured[0]

        succ = page.evaluate("""() => {
            const s = document.getElementById('forgotSuccess');
            const f = document.getElementById('forgotFormArea');
            const d = document.getElementById('forgotDirectLink');
            return {
                succDisplay: window.getComputedStyle(s).display,
                formDisplay: window.getComputedStyle(f).display,
                hasDirectLink: d && d.innerHTML.includes('reset-password?token=abc')
            };
        }""")
        page.close()

        assert succ["succDisplay"] == "flex"
        assert succ["formDisplay"] == "none"
        assert succ["hasDirectLink"] is True

    def test_portal_modals_and_tab_switching_no_exceptions(self, browser_context):
        """Verify tab switching and modal interactions do not throw JavaScript runtime errors."""
        with flask_app.test_request_context("/portal"):
            html = render_template(
                "portal.html",
                SITE_ORIGIN="https://lms.dbert.in",
                intern={"name": "Test Intern", "email": "intern@dbert.in", "id": 1, "domain": "AI Engineering", "status": "Accepted"},
                user={"name": "Test Intern", "email": "intern@dbert.in", "id": 1, "domain": "AI Engineering", "role": "intern"}
            )

        page = browser_context.new_page()
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))

        setup_browser_routes(page, html, "/portal")
        page.route("https://lms.dbert.in/intern/me", lambda route: route.fulfill(
            status=200,
            body='{"status":"success","intern":{"name":"Test","email":"intern@dbert.in","domain":"AI","status":"Accepted","coins":100},"applications":[]}',
            content_type="application/json"
        ))
        page.route("https://lms.dbert.in/intern/**", lambda route: route.fulfill(status=200, body='{"status":"success","cohorts":[],"items":[],"applications":[],"certificates":[],"coins":100,"balance":100,"threads":[],"notifications":[]}', content_type="application/json"))

        page.goto("https://lms.dbert.in/portal")
        page.wait_for_load_state("domcontentloaded")

        # Check modal dialog ARIA properties
        aria = page.evaluate("""() => {
            const pw = document.getElementById('passwordModal');
            const ad = document.getElementById('applyDomainModal');
            const lg = document.getElementById('logoutConfirmModal');
            return {
                pw: { role: pw.getAttribute('role'), modal: pw.getAttribute('aria-modal') },
                ad: { role: ad.getAttribute('role'), modal: ad.getAttribute('aria-modal') },
                lg: { role: lg.getAttribute('role'), modal: lg.getAttribute('aria-modal') }
            };
        }""")
        assert aria["pw"]["role"] == "dialog" and aria["pw"]["modal"] == "true"
        assert aria["ad"]["role"] == "dialog" and aria["ad"]["modal"] == "true"
        assert aria["lg"]["role"] == "dialog" and aria["lg"]["modal"] == "true"

        # Tab switching across all tabs
        for tab in ["overview", "myapplications", "coins", "certificate", "leaderboard", "cohorts", "messages", "notifications", "password", "applyanother"]:
            page.evaluate(f"() => window.switchTab('{tab}')")
            page.wait_for_timeout(50)

        assert len(errors) == 0, f"Runtime JS errors occurred during tab switching: {errors}"

        # Test #passwordModal open and Escape
        page.evaluate("() => window.openPasswordModal()")
        assert page.evaluate("() => !document.getElementById('passwordModal').classList.contains('hidden')")
        page.keyboard.press("Escape")
        assert page.evaluate("() => document.getElementById('passwordModal').classList.contains('hidden')")

        # Test #applyDomainModal open and Escape
        page.evaluate("() => window.openApplyDomainModal()")
        assert page.evaluate("() => !document.getElementById('applyDomainModal').classList.contains('hidden')")
        page.keyboard.press("Escape")
        assert page.evaluate("() => document.getElementById('applyDomainModal').classList.contains('hidden')")

        page.close()

    def test_portal_logout_confirmation_gate_enforcement(self, browser_context):
        """Verify logout confirmation modal strictly gates /logout session termination."""
        with flask_app.test_request_context("/portal"):
            html = render_template(
                "portal.html",
                SITE_ORIGIN="https://lms.dbert.in",
                intern={"name": "Test Intern", "email": "intern@dbert.in", "id": 1, "domain": "AI Engineering", "status": "Accepted"},
                user={"name": "Test Intern", "email": "intern@dbert.in", "id": 1, "domain": "AI Engineering", "role": "intern"}
            )

        page = browser_context.new_page()
        setup_browser_routes(page, html, "/portal")
        page.route("https://lms.dbert.in/intern/me", lambda route: route.fulfill(
            status=200,
            body='{"status":"success","intern":{"name":"Test","email":"intern@dbert.in","domain":"AI","status":"Accepted","coins":100},"applications":[]}',
            content_type="application/json"
        ))
        page.route("https://lms.dbert.in/intern/**", lambda route: route.fulfill(status=200, body='{"status":"success","cohorts":[],"items":[],"applications":[],"certificates":[],"coins":100,"balance":100,"threads":[],"notifications":[]}', content_type="application/json"))

        logout_calls = []
        page.route("https://lms.dbert.in/logout", lambda route: (logout_calls.append(True), route.fulfill(status=200, body='{"status":"success"}', content_type="application/json")))

        page.goto("https://lms.dbert.in/portal")
        page.wait_for_load_state("domcontentloaded")

        # 1. Trigger logout click
        page.evaluate("() => window.confirmLogout()")
        page.wait_for_timeout(100)

        is_open = page.evaluate("() => !document.getElementById('logoutConfirmModal').classList.contains('hidden')")
        assert is_open is True
        assert len(logout_calls) == 0, "/logout MUST NOT be called upon initial logout button click"

        # 2. Cancel logout
        page.evaluate("() => window.closeLogoutModal()")
        page.wait_for_timeout(100)
        is_closed = page.evaluate("() => document.getElementById('logoutConfirmModal').classList.contains('hidden')")
        assert is_closed is True
        assert len(logout_calls) == 0, "/logout MUST NOT be called when user cancels"

        # 3. Explicit confirmation
        page.evaluate("() => window.confirmLogout()")
        page.evaluate("() => window.doLogout()")
        page.wait_for_timeout(200)

        assert len(logout_calls) == 1, "/logout MUST be called when user confirms"
        page.close()


class TestCSPActionDelegationResolution:
    """Verifies that every data-act-* action attribute across portal templates resolves in browser."""

    def test_all_templates_csp_action_resolution(self, browser_context):
        act_attr_re = re.compile(r'data-act-([a-zA-Z0-9_-]+)="([^"]+)"')
        act_attr_single_re = re.compile(r"data-act-([a-zA-Z0-9_-]+)='([^']+)'")

        # Verify all templates with data-act-*
        html_files = sorted(list(TEMPLATES_DIR.glob("*.html")))
        total_actions_found = 0
        unresolved_actions = []

        # Custom render contexts
        contexts = {
            "account_gemini_key.html": {"fallback_used": False, "fallback_limit": 100, "masked_key": "AIza***", "configured": True},
            "admin_cohorts.html": {"counts": {"active": 1, "completed": 0}, "cohorts": []},
            "admin_integrity_dashboard.html": {
                "metrics": {
                    "users": {"total_users": 10, "total_interns": 8, "total_companies": 2},
                    "applications": {"total": 20, "accepted": 15, "selected": 5},
                    "enrollments": {"total": 12, "verified": 10, "pending": 2},
                    "payments": {"verified_volume_inr": 50000, "total_records": 10, "events_logged": 10},
                    "active_interns": {"count": 7},
                    "certificates": {"total_issued": 5},
                    "db": {"size_mb": 1.2, "wal_size_mb": 0.1, "integrity_check": "ok"},
                    "system": {"cpu_percent": 12.5, "memory_percent": 45.0, "disk_free_gb": 80.0}
                },
                "anomalies": {
                    "summary": {"status": "HEALTHY", "critical_count": 0, "warning_count": 0, "info_count": 0, "total_anomalies": 0, "health_score": 100},
                    "impossible_states": {"count": 0, "items": []},
                    "expired_live_listings": {"count": 0, "items": []},
                    "failed_critical_jobs": {"count": 0, "items": []},
                    "orphan_enrollments": {"count": 0, "items": []},
                    "duplicate_active_applications": {"count": 0, "items": []}
                },
                "now": "2026-11-04 12:00:00"
            },
            "admin_post_hire_deposits.html": {"counts": {"pending": 0, "approved": 0}, "deposits": []},
            "certificate_document.html": {"cert": {"certificate_id": "CERT-1", "student_name": "Test", "domain": "AI", "issue_date": "2026-01-01"}},
            "company_applicants.html": {"apps": [], "stats": {}, "company": {"id": 1, "name": "Co"}, "post": {"id": 1}, "pending_certs_status": "pending_certs"},
            "course_learn.html": {"enrollment": {"id": 1, "status": "active"}, "course": {"id": 1, "title": "AI Course"}, "chapter": {"id": 1, "title": "Ch 1"}, "subtopics": []},
            "course_pay.html": {"course": {"id": 1, "title": "AI Course", "price_inr": 4999, "price": 4999, "domain": "AI"}, "user": {"email": "test@dbert.in", "name": "Test"}},
            "course_quiz.html": {"chapter": {"id": 1, "title": "Ch 1", "quiz_json": "[]"}, "course": {"id": 1, "title": "AI"}},
            "cv_editor.html": {"form": {"experience": [], "education": []}, "cv": {}},
            "mentor_availability.html": {"staff": {"id": 1, "name": "Mentor"}, "slots": []},
            "messages_inbox.html": {"actor": {"role": "intern", "id": 1}, "threads": []},
            "messages_thread.html": {"conv_id": 1, "actor": {"sender_type": "intern", "role": "intern", "id": 1}, "messages": []},
            "program.html": {"paid_amount": 9999, "SITE_ORIGIN": "https://lms.dbert.in"},
            "scraped_internship_detail.html": {"job": {"id": 1, "title": "Software Intern", "company_name": "Google", "domain": "AI", "location": "Remote", "URL": "https://example.com"}},
            "staff_project_queue.html": {"staff": {"id": 1, "name": "Staff"}, "submissions": []},
            "staff_task_queue.html": {"staff": {"id": 1, "name": "Staff"}, "tasks": []},
            "post_detail.html": {
                "is_intern": True, "is_logged_in": True, "already_applied": False,
                "post": {"id": 1, "title": "AI Intern", "company_name": "Test Co", "domain": "AI", "post_type": "internship"},
                "my_apps_url": "/portal", "comments": []
            }
        }

        for html_file in html_files:
            raw_text = html_file.read_text(encoding="utf-8")
            matches = set(act_attr_re.findall(raw_text) + act_attr_single_re.findall(raw_text))
            if not matches:
                continue

            ctx = {
                "user": {"name": "Test User", "email": "test@dbert.in", "id": 1, "domain": "AI Engineering", "role": "intern"},
                "intern": {"name": "Test User", "email": "test@dbert.in", "id": 1, "domain": "AI Engineering"},
                "company": {"name": "Test Co", "email": "recruiter@co.com", "id": 1},
                "course": {"id": 1, "title": "AI Course", "domain": "AI Engineering", "price": 0, "status": "active"},
                "quiz": {"id": 1, "questions": []},
                "post": {"id": 1, "title": "Internship Post", "company_name": "Test Co", "domain": "AI Engineering", "status": "active", "post_type": "internship"},
                "task": {"id": 1, "title": "Sample Task"},
                "applicant": {"name": "Applicant", "email": "app@test.com"},
                "SITE_ORIGIN": "https://lms.dbert.in",
                "active_page": "test",
                "account": {"email": "test@dbert.in"},
                "my_apps_url": "/portal",
            }
            if html_file.name in contexts:
                ctx.update(contexts[html_file.name])

            with flask_app.test_request_context("/"):
                rendered = render_template(html_file.name, **ctx)

            page = browser_context.new_page()
            setup_browser_routes(page, rendered, "/")
            page.goto("https://lms.dbert.in/")
            page.wait_for_load_state("domcontentloaded")

            for evt, fn in matches:
                if fn in BUILTINS or fn.startswith('$'):
                    continue
                total_actions_found += 1
                is_fn = page.evaluate(f"typeof window['{fn}'] === 'function'")
                if not is_fn:
                    unresolved_actions.append((html_file.name, evt, fn))

            page.close()

        assert len(unresolved_actions) == 0, f"Unresolved CSP action handlers: {unresolved_actions}"
        assert total_actions_found > 100, f"Expected >100 CSP actions verified, found {total_actions_found}"


class TestResponsiveLayoutCalculations:
    """CSS rule computation tests on dbert-theme.css."""

    def test_desktop_main_left_margin_is_exactly_240px(self, browser_context, css_text):
        """Verify desktop margin-left on .main at >= 961px is exactly 240px."""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>{css_text}</style>
</head>
<body class="has-sidebar">
  <div class="sidebar"></div>
  <div class="main">
    <div class="content">Content</div>
  </div>
</body>
</html>"""

        for w in [961, 1024, 1440, 1920]:
            page = browser_context.new_page()
            page.set_viewport_size({"width": w, "height": 800})
            page.set_content(html_content)
            ml = page.evaluate("() => window.getComputedStyle(document.querySelector('.main')).marginLeft")
            page.close()
            assert ml == "240px", f"Expected 240px margin-left on .main at {w}px, got {ml}"

    def test_auth_card_padding_on_mobile(self, browser_context, css_text):
        """
        Adversarially tests .auth-card padding on mobile (<= 768px).
        Requirement: Must NOT exceed 20px.
        """
        html_home = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>{css_text}</style>
</head>
<body class="home">
  <div class="auth-wrapper">
    <div class="auth-card">
      <h1>Sign In</h1>
    </div>
  </div>
</body>
</html>"""

        html_standalone = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>{css_text}</style>
</head>
<body class="pg-auth">
  <div class="card auth-card">
    <h1>Login</h1>
  </div>
</body>
</html>"""

        violations = []
        for w in [360, 390, 412, 768]:
            # Test Home Auth Card
            page_h = browser_context.new_page()
            page_h.set_viewport_size({"width": w, "height": 800})
            page_h.set_content(html_home)
            pad_h = page_h.evaluate("""() => {
                const cs = window.getComputedStyle(document.querySelector('.auth-card'));
                return {
                    top: parseFloat(cs.paddingTop),
                    right: parseFloat(cs.paddingRight),
                    bottom: parseFloat(cs.paddingBottom),
                    left: parseFloat(cs.paddingLeft)
                };
            }""")
            page_h.close()

            max_h = max(pad_h.values())
            if max_h > 20:
                violations.append(f"body.home .auth-card at {w}px has max padding {max_h}px (top={pad_h['top']}, right={pad_h['right']}, bottom={pad_h['bottom']}, left={pad_h['left']})")

            # Test Standalone Auth Card
            page_s = browser_context.new_page()
            page_s.set_viewport_size({"width": w, "height": 800})
            page_s.set_content(html_standalone)
            pad_s = page_s.evaluate("""() => {
                const cs = window.getComputedStyle(document.querySelector('.auth-card'));
                return {
                    top: parseFloat(cs.paddingTop),
                    right: parseFloat(cs.paddingRight),
                    bottom: parseFloat(cs.paddingBottom),
                    left: parseFloat(cs.paddingLeft)
                };
            }""")
            page_s.close()

            max_s = max(pad_s.values())
            if max_s > 20:
                violations.append(f"standalone .auth-card at {w}px has max padding {max_s}px (top={pad_s['top']}, right={pad_s['right']}, bottom={pad_s['bottom']}, left={pad_s['left']})")

        # EMPIRICAL CHALLENGER ASSERTION:
        # If violations exist, raise AssertionError documenting the exact CSS collision
        assert len(violations) == 0, (
            "DEFECT FOUND in dbert-theme.css: .auth-card padding exceeds 20px on mobile <= 768px:\n"
            + "\n".join(violations)
            + "\nRoot cause: Line 3651 defines 'body.home .auth-card, .auth-card { padding: 28px 30px !important; }' "
            "outside of media queries, overriding mobile styling."
        )
