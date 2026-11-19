"""
test_push_notification_remediation.py
Tests the Web Push Notification blocked state detection, unblocking guidance,
dashboard alert banner, and CSP nonce compliance in portal.html.
"""
import re
import pytest

def test_push_notification_modal_and_banner_markup():
    with open('apps/portal/templates/portal.html', encoding='utf-8') as f:
        html = f.read()

    # 1. Verify dashboard blocked alert banner is present
    assert 'id="pushBlockedBanner"' in html, "pushBlockedBanner must exist in portal.html"
    assert 'Browser Push Notifications Are Blocked' in html
    assert 'id="btnOpenPushHelp"' in html
    assert 'id="btnDismissPushBanner"' in html

    # 2. Verify dual-state modal architecture
    assert 'id="dbertPushPermissionModal"' in html
    assert 'id="pushModalStateDefault"' in html
    assert 'id="pushModalStateBlocked"' in html

    # 3. Verify step guide elements
    assert 'push-guide-step' in html
    assert 'How to Unblock Notifications' in html
    assert 'id="dbertPushReloadBtn"' in html
    assert "I've Enabled It" in html
    assert 'id="dbertPushBlockedDismissBtn"' in html

    # 4. Verify CSS classes
    assert '.push-blocked-banner' in html
    assert '.dbert-push-modal-overlay' in html
    assert 'z-index: 100001;' in html
    assert 'padding-left: calc(var(--portal-sidebar, 260px) + 24px);' in html

    # 5. Verify Permissions API observer & live change handler
    assert "permissions.query({ name: 'notifications' })" in html
    assert "pStatus.onchange" in html

    # 6. Verify zero inline onclick handlers on push modal or banner elements
    banner_match = re.search(r'id="pushBlockedBanner".*?<\/div>\s*<\/div>\s*<\/div>', html, re.DOTALL)
    assert banner_match is not None
    assert 'onclick=' not in banner_match.group(0), "pushBlockedBanner must have zero inline onclick handlers"

    modal_match = re.search(r'id="dbertPushPermissionModal".*?<\/div>\s*<\/div>\s*<\/div>', html, re.DOTALL)
    assert modal_match is not None
    assert 'onclick=' not in modal_match.group(0), "dbertPushPermissionModal must have zero inline onclick handlers"
