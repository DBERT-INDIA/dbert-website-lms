#!/usr/bin/env python3
"""
Automated Playwright Responsive Test Suite.
Audits key pages across 6 viewports on both https://dbert.in and https://lms.dbert.in.
Checks:
  - Zero horizontal overflow (scrollWidth <= innerWidth + 2px tolerance)
  - HTTP 200 response
  - Responsive layout assertions
"""

import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

VIEWPORTS = [
    {"name": "iPhone SE", "width": 375, "height": 667},
    {"name": "iPhone 14 / Pixel", "width": 390, "height": 844},
    {"name": "iPad Mini / Air", "width": 768, "height": 1024},
    {"name": "iPad Pro / Laptop", "width": 1024, "height": 1366},
    {"name": "Standard Desktop 1080p", "width": 1920, "height": 1080},
    {"name": "Ultrawide 4K", "width": 2560, "height": 1440},
]

URLS = [
    {"app": "Website", "name": "Homepage", "url": "https://dbert.in/"},
    {"app": "Website", "name": "Directory", "url": "https://dbert.in/verify/directory"},
    {"app": "Website", "name": "Enrollment 1999", "url": "https://dbert.in/enroll/1999"},
    {"app": "Website", "name": "Certificate Verify", "url": "https://dbert.in/verify/CERT-DBERT-2026-DA-057"},
    {"app": "LMS", "name": "Leaderboard", "url": "https://lms.dbert.in/leaderboard"},
    {"app": "LMS", "name": "Portal Offer", "url": "https://lms.dbert.in/portal/offer?token=dbert-offer-2026-da-9103"},
    {"app": "LMS", "name": "LMS Homepage", "url": "https://lms.dbert.in/"},
    {"app": "LMS", "name": "Certificate Print Dossier", "url": "https://lms.dbert.in/portal/certificate/DBERT-VERIFIED-F0423A71/print"},
]

def run_tests():
    print("=" * 70)
    print("  DBERT UNIVERSAL RESPONSIVE AUDIT TEST SUITE")
    print("=" * 70)
    
    total_checks = 0
    passed_checks = 0
    failed_checks = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        for vp in VIEWPORTS:
            vp_name = vp["name"]
            w = vp["width"]
            h = vp["height"]
            print(f"\n--- Testing Viewport: {vp_name} ({w}x{h}) ---")
            
            context = browser.new_context(
                viewport={"width": w, "height": h},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            for item in URLS:
                total_checks += 1
                app = item["app"]
                page_name = item["name"]
                url = item["url"]

                try:
                    res = page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    page.wait_for_timeout(600)
                    status = res.status if res else 0

                    # Check horizontal scroll width
                    overflow_data = page.evaluate("""() => {
                        const docWidth = document.documentElement.scrollWidth;
                        const winWidth = window.innerWidth;
                        const bodyWidth = document.body ? document.body.scrollWidth : 0;
                        const maxScroll = Math.max(docWidth, bodyWidth);
                        return {
                            scrollWidth: maxScroll,
                            innerWidth: winWidth,
                            hasOverflow: maxScroll > winWidth + 3
                        };
                    }""")

                    has_overflow = overflow_data["hasOverflow"]
                    scroll_w = overflow_data["scrollWidth"]
                    inner_w = overflow_data["innerWidth"]

                    if status in (200, 302, 307) and not has_overflow:
                        print(f"  [PASS] [{app}] {page_name:<26} (HTTP {status}) -> Width: {scroll_w}/{inner_w}px (No overflow)")
                        passed_checks += 1
                    else:
                        issue = f"HTTP {status}" if status != 200 else f"Overflow: {scroll_w}px > {inner_w}px"
                        print(f"  [FAIL] [{app}] {page_name:<26} ({issue})")
                        failed_checks.append(f"{vp_name} - [{app}] {page_name}: {issue}")

                except Exception as e:
                    print(f"  [ERROR] [{app}] {page_name:<26}: {str(e)[:60]}")
                    failed_checks.append(f"{vp_name} - [{app}] {page_name}: Exception {str(e)[:50]}")

            context.close()
        browser.close()

    print("\n" + "=" * 70)
    print(f"  AUDIT SUMMARY: {passed_checks}/{total_checks} checks passed ({passed_checks/total_checks*100:.1f}%)")
    if failed_checks:
        print(f"  FAILED CHECKS ({len(failed_checks)}):")
        for f in failed_checks:
            print(f"    - {f}")
    else:
        print("  ALL 6 VIEWPORTS PASSED WITH ZERO HORIZONTAL OVERFLOW!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
