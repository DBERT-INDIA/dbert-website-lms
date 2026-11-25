import subprocess
import time
import os
import sys
import requests
from playwright.sync_api import sync_playwright

def run_tests():
    test_port = '3010'
    env = os.environ.copy()
    env['PORT'] = test_port
    env['HOSTNAME'] = '127.0.0.1'
    env['NODE_ENV'] = 'production'
    cwd = os.path.abspath('apps/website/.next/standalone')

    print(f"Starting standalone server from {cwd} on port {test_port}...")
    proc = subprocess.Popen(['node', 'server.js'], cwd=cwd, env=env)
    time.sleep(3)

    try:
        base_url = f'http://127.0.0.1:{test_port}'

        # 1. Test Redirect: /verify/unlock
        print("\n--- Testing Redirect: /verify/unlock ---")
        r1 = requests.get(f'{base_url}/verify/unlock?certid=CERT-DBERT-2026-DA-057', allow_redirects=False)
        print(f"Status: {r1.status_code}")
        print(f"Location header: {r1.headers.get('Location')}")
        assert r1.status_code == 308, f"Expected 308, got {r1.status_code}"
        assert r1.headers.get('Location') == '/enroll/1999?certid=CERT-DBERT-2026-DA-057', f"Unexpected Location: {r1.headers.get('Location')}"
        print("✓ /verify/unlock redirect verified")

        # 2. Test Redirect: /enroll/balance
        print("\n--- Testing Redirect: /enroll/balance ---")
        r2 = requests.get(f'{base_url}/enroll/balance', allow_redirects=False)
        print(f"Status: {r2.status_code}")
        print(f"Location header: {r2.headers.get('Location')}")
        assert r2.status_code == 308, f"Expected 308, got {r2.status_code}"
        assert r2.headers.get('Location') == '/enroll/1999', f"Unexpected Location: {r2.headers.get('Location')}"
        print("✓ /enroll/balance redirect verified")

        # 3. Test Redirect: /eroll
        print("\n--- Testing Redirect: /eroll ---")
        r3 = requests.get(f'{base_url}/eroll?certid=CERT-DBERT-2026-DA-057', allow_redirects=False)
        print(f"Status: {r3.status_code}")
        print(f"Location header: {r3.headers.get('Location')}")
        assert r3.status_code == 308, f"Expected 308, got {r3.status_code}"
        assert r3.headers.get('Location') == '/enroll/1999?certid=CERT-DBERT-2026-DA-057', f"Unexpected Location: {r3.headers.get('Location')}"
        print("✓ /eroll redirect verified")

        # 4. Test API Isolation: POST /api/enroll/balance
        print("\n--- Testing API Route Isolation: POST /api/enroll/balance ---")
        r4 = requests.post(f'{base_url}/api/enroll/balance', json={}, allow_redirects=False)
        print(f"Status: {r4.status_code}")
        print(f"Response: {r4.text}")
        assert r4.status_code == 400, f"Expected 400 from API validation, got {r4.status_code}"
        assert 'Full Legal Name is required' in r4.text, f"Unexpected body: {r4.text}"
        assert 'Location' not in r4.headers, f"API route should NOT redirect! Found Location header: {r4.headers.get('Location')}"
        print("✓ POST /api/enroll/balance route isolation confirmed (0 redirection, API handler hit directly)")

        # 5. Test API Isolation: GET /api/enroll/balance
        print("\n--- Testing API Route Isolation: GET /api/enroll/balance ---")
        r5 = requests.get(f'{base_url}/api/enroll/balance', allow_redirects=False)
        print(f"Status: {r5.status_code}")
        assert r5.status_code in [405, 404], f"Expected 405/404 for GET /api/enroll/balance, got {r5.status_code}"
        assert 'Location' not in r5.headers, f"GET /api/enroll/balance should NOT redirect to /enroll/1999! Location: {r5.headers.get('Location')}"
        print("✓ GET /api/enroll/balance does not redirect to /enroll/1999")

        # 6. Playwright Browser Tests: Banner Conditional Rendering and Viewport Responsiveness
        print("\n--- Testing Banner Rendering & Viewport Responsiveness in Playwright ---")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # Test A: Desktop with certid -> Banner visible
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(f'{base_url}/enroll/1999?certid=CERT-DBERT-2026-DA-057', wait_until='domcontentloaded')
            page.wait_for_timeout(2000)
            content = page.content()
            notice_text = "Standalone ₹299 verification fees have been discontinued"
            assert notice_text in content, "Notice banner text not found when certid present!"
            print("✓ Banner rendered with ?certid=CERT-DBERT-2026-DA-057 (Desktop 1280px)")

            # Test B: Desktop without certid -> Banner NOT visible
            page.goto(f'{base_url}/enroll/1999', wait_until='domcontentloaded')
            page.wait_for_timeout(2000)
            content_no_cert = page.content()
            assert notice_text not in content_no_cert, "Notice banner should NOT be rendered when certid is absent!"
            print("✓ Banner NOT rendered without certid (Desktop 1280px)")

            # Test C: Empty certid query param: ?certid= -> Banner NOT visible
            page.goto(f'{base_url}/enroll/1999?certid=', wait_until='domcontentloaded')
            page.wait_for_timeout(2000)
            content_empty = page.content()
            assert notice_text not in content_empty, "Notice banner should NOT be rendered when certid is empty string!"
            print("✓ Banner NOT rendered with ?certid= (empty param)")

            # Test D: Query param with certId (camelCase): ?certId=CERT-DBERT-2026-DA-057 -> Banner visible
            page.goto(f'{base_url}/enroll/1999?certId=CERT-DBERT-2026-DA-057', wait_until='domcontentloaded')
            page.wait_for_timeout(2000)
            content_camel = page.content()
            assert notice_text in content_camel, "Notice banner should be rendered with camelCase certId!"
            print("✓ Banner rendered with ?certId= (camelCase)")

            # Test E: Mobile Viewport 390px (iPhone 12/13/14)
            page_mobile_390 = browser.new_page(viewport={"width": 390, "height": 844})
            page_mobile_390.goto(f'{base_url}/enroll/1999?certid=CERT-DBERT-2026-DA-057', wait_until='domcontentloaded')
            page_mobile_390.wait_for_timeout(2000)
            assert notice_text in page_mobile_390.content()
            
            scroll_width_390 = page_mobile_390.evaluate("document.documentElement.scrollWidth")
            client_width_390 = page_mobile_390.evaluate("document.documentElement.clientWidth")
            body_scroll_390 = page_mobile_390.evaluate("document.body.scrollWidth")
            print(f"Mobile 390px - scrollWidth: {scroll_width_390}, clientWidth: {client_width_390}, bodyScrollWidth: {body_scroll_390}")
            assert scroll_width_390 <= 390, f"Horizontal overflow detected on 390px viewport! scrollWidth={scroll_width_390}"
            print("✓ Mobile 390px: Banner visible, ZERO horizontal overflow (exact 390px width)")

            # Test F: Mobile Viewport 320px (iPhone SE small)
            page_mobile_320 = browser.new_page(viewport={"width": 320, "height": 568})
            page_mobile_320.goto(f'{base_url}/enroll/1999?certid=CERT-DBERT-2026-DA-057', wait_until='domcontentloaded')
            page_mobile_320.wait_for_timeout(2000)
            assert notice_text in page_mobile_320.content()
            
            scroll_width_320 = page_mobile_320.evaluate("document.documentElement.scrollWidth")
            client_width_320 = page_mobile_320.evaluate("document.documentElement.clientWidth")
            print(f"Mobile 320px - scrollWidth: {scroll_width_320}, clientWidth: {client_width_320}")
            # Note: check if banner itself exceeds 320px
            banner_box = page_mobile_320.evaluate("""() => {
                const els = Array.from(document.querySelectorAll('div')).filter(el => el.textContent.includes('Standalone ₹299'));
                if (els.length > 0) {
                    const rect = els[0].getBoundingClientRect();
                    return { width: rect.width, left: rect.left, right: rect.right };
                }
                return null;
            }""")
            print(f"Banner bounding rect on 320px: {banner_box}")
            assert banner_box is not None, "Banner element bounding box not found"
            assert banner_box['width'] <= 320, f"Banner exceeds 320px viewport! width={banner_box['width']}"
            assert banner_box['right'] <= 320, f"Banner right edge clips out of 320px viewport! right={banner_box['right']}"
            print("✓ Mobile 320px: Banner cleanly contained within viewport without overflow")

            browser.close()

        print("\nALL 6 INDEPENDENT VERIFICATION TESTS PASSED SUCCESSFULLY!")

    finally:
        print("Shutting down standalone test server...")
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    run_tests()
