"""
test_push_modal_responsive.py
Tests the mobile-responsive bottom sheet transformation, high-contrast hardening,
iOS Safari PWA guidance state, and safe-area insets for the DBERT push modal.
"""
import re
import pytest

def test_push_modal_responsive_transformation_and_ios_state():
    with open('apps/portal/templates/portal.html', encoding='utf-8') as f:
        html = f.read()

    # 1. Verify Mobile Bottom-Sheet CSS media query
    assert '@media (max-width: 768px)' in html
    assert 'align-items: flex-end !important;' in html
    assert 'border-radius: 24px 24px 0 0 !important;' in html
    assert 'env(safe-area-inset-bottom)' in html
    assert 'dbertPushSlideUp' in html

    # 2. Verify Drag Handle for Mobile Bottom-Sheet
    assert 'class="dbert-push-drag-handle"' in html

    # 3. Verify iOS Safari Guidance State & Controls
    assert 'id="pushModalStateIOS"' in html
    assert 'id="dbertPushIOSDismissBtn"' in html
    assert 'iPhone / iPad Setup' in html
    assert 'Add to Home Screen' in html

    # 4. Verify High-Contrast Color Hardening
    assert 'color-scheme: dark;' in html
    assert '#F8FAFC !important;' in html
    assert '#CBD5E1 !important;' in html

    # 5. Verify Client JS handles iOS and standalone detection
    assert 'var isIOS = /iPhone|iPad|iPod/i.test(navigator.userAgent);' in html
    assert 'isStandalone' in html
    assert "setPushModalState('ios')" in html

    # 6. Verify zero inline onclick handlers
    modal_match = re.search(r'id="dbertPushPermissionModal".*?<\/div>\s*<\/div>\s*<\/div>', html, re.DOTALL)
    assert modal_match is not None
    assert 'onclick=' not in modal_match.group(0), "dbertPushPermissionModal must have zero inline onclick handlers"
