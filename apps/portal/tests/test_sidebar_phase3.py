"""
Phase 3 LMS Sidebar 5-Group Restructuring Test Suite.
Verifies canonical 5-group navigation hierarchy, stage-based locks,
badge pulse animations, mobile CSS classes, and template syntax.
"""

import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup
import pytest

PORTAL_DIR = Path(__file__).resolve().parent.parent
if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

from app import app as flask_app
from flask import render_template

EXPECTED_GROUPS = [
    "Core Workspace",
    "Production Sprints",
    "Career & Outcomes",
    "Community & Rewards",
    "Account & Settings"
]

def render_sidebar(is_locked_pre_payment=True, is_graduated=False, is_selected_unpaid=False, active_page='portal'):
    with flask_app.test_request_context('/portal'):
        html = render_template(
            '_intern_sidebar.html',
            is_locked_pre_payment=is_locked_pre_payment,
            is_graduated=is_graduated,
            is_selected_unpaid=is_selected_unpaid,
            offer_badge='OFFICIAL',
            sprint_task_badge=None,
            active_page=active_page
        )
        return BeautifulSoup(html, 'html.parser')

def test_jinja2_template_syntax_all():
    """Verify all 82+ Jinja templates parse without syntax errors."""
    templates_dir = PORTAL_DIR / "templates"
    env = flask_app.jinja_env
    syntax_errors = []
    count = 0
    for root, _, files in os.walk(templates_dir):
        for f in files:
            if f.endswith(('.html', '.jinja2')):
                count += 1
                rel_path = Path(root, f).relative_to(templates_dir).as_posix()
                try:
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as fh:
                        env.parse(fh.read())
                except Exception as e:
                    syntax_errors.append((rel_path, str(e)))
    assert len(syntax_errors) == 0, f"Syntax errors in templates: {syntax_errors}"
    assert count >= 80, f"Expected at least 80 templates scanned, found {count}"

def test_five_nav_groups_order():
    """Verify all 5 nav groups appear in exact canonical order."""
    soup = render_sidebar()
    labels = [g.get_text().strip() for g in soup.select('.nav-group-label')]
    assert labels == EXPECTED_GROUPS, f"Nav group labels mismatch. Got: {labels}, Expected: {EXPECTED_GROUPS}"

def test_stage2_under_review_locks():
    """Stage 2 intern: Production sprints locked, no pulse on offer letter."""
    soup = render_sidebar(is_locked_pre_payment=True, is_graduated=False, is_selected_unpaid=False)
    
    # Sprint Tasks locked
    tasks_link = soup.find('a', href='/tasks')
    assert tasks_link is not None, "Missing /tasks link"
    assert 'nav-item-locked' in tasks_link.get('class', []), "/tasks link should have class nav-item-locked"
    assert tasks_link.get('data-locked') == 'true', "/tasks link should have data-locked='true'"
    assert tasks_link.find(class_='nav-lock-pill') is not None, "/tasks missing nav-lock-pill"
    assert "LOCKED" in tasks_link.find(class_='nav-lock-pill').text

    # 1:1 Architect Mentorship locked
    slots_link = soup.find('a', href='/mentors/slots')
    assert slots_link is not None, "Missing /mentors/slots link"
    assert 'nav-item-locked' in slots_link.get('class', [])
    assert slots_link.find(class_='nav-lock-pill') is not None

    # Stipend Milestone locked
    stipend_link = soup.find('a', href='/stipend/tasks')
    assert stipend_link is not None, "Missing /stipend/tasks link"
    assert 'nav-item-locked' in stipend_link.get('class', [])
    assert stipend_link.find(class_='nav-lock-pill') is not None

    # Offer letter badge should not pulse
    offer_link = soup.find('a', href='/portal/offer')
    assert offer_link is not None, "Missing /portal/offer link"
    pulse = offer_link.find(class_='nav-badge-pulse')
    assert pulse is None, "Offer letter badge should not pulse for Stage 2"

def test_stage3_selected_unpaid_pulse():
    """Stage 3 intern: Production sprints locked, Offer Letter badge pulses."""
    soup = render_sidebar(is_locked_pre_payment=True, is_graduated=False, is_selected_unpaid=True)
    
    # Offer letter badge must pulse
    offer_link = soup.find('a', href='/portal/offer')
    assert offer_link is not None
    pulse = offer_link.find(class_='nav-badge-pulse')
    assert pulse is not None, "Offer letter badge must have class nav-badge-pulse for Stage 3"
    assert "OFFICIAL" in pulse.text

    # Production sprints still locked
    tasks_link = soup.find('a', href='/tasks')
    assert 'nav-item-locked' in tasks_link.get('class', [])

def test_stage5_active_intern_unlocked():
    """Stage 5 confirmed intern: Production sprints unlocked, non-graduated certs locked."""
    soup = render_sidebar(is_locked_pre_payment=False, is_graduated=False, is_selected_unpaid=False)
    
    # Production sprints unlocked
    tasks_link = soup.find('a', href='/tasks')
    assert 'nav-item-locked' not in tasks_link.get('class', [])
    assert tasks_link.find(class_='nav-lock-pill') is None

    slots_link = soup.find('a', href='/mentors/slots')
    assert 'nav-item-locked' not in slots_link.get('class', [])
    assert slots_link.find(class_='nav-lock-pill') is None

    stipend_link = soup.find('a', href='/stipend/tasks')
    assert 'nav-item-locked' not in stipend_link.get('class', [])
    assert stipend_link.find(class_='nav-lock-pill') is None

    # Non-graduated intern certificates locked
    cert_link = soup.find('a', href='/certificates')
    assert cert_link is not None
    assert 'nav-item-locked' in cert_link.get('class', [])
    assert cert_link.find(class_='nav-lock-pill') is not None

def test_graduated_intern_unlocked():
    """Graduated intern: Certificates unlocked."""
    soup = render_sidebar(is_locked_pre_payment=False, is_graduated=True, is_selected_unpaid=False)
    
    cert_link = soup.find('a', href='/certificates')
    assert cert_link is not None
    assert 'nav-item-locked' not in cert_link.get('class', [])
    assert cert_link.find(class_='nav-lock-pill') is None

def test_css_classes_in_theme():
    """Verify Phase 3 CSS classes are present in dbert-theme.css."""
    css_path = PORTAL_DIR / "static" / "css" / "dbert-theme.css"
    assert css_path.exists(), "dbert-theme.css does not exist"
    css = css_path.read_text(encoding='utf-8')
    assert ".nav-lock-pill" in css, "Missing .nav-lock-pill in dbert-theme.css"
    assert ".nav-badge-pulse" in css, "Missing .nav-badge-pulse in dbert-theme.css"
    assert "badgePulse" in css, "Missing @keyframes badgePulse in dbert-theme.css"
    assert ".nav-item-locked" in css, "Missing .nav-item-locked in dbert-theme.css"
