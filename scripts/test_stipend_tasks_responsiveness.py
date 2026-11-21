import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

VIEWPORTS = [
    {"name": "iPhone SE", "width": 375, "height": 667, "is_mobile": True},
    {"name": "iPhone 14 / Pixel", "width": 390, "height": 844, "is_mobile": True},
    {"name": "iPad Mini", "width": 768, "height": 1024, "is_mobile": False},
    {"name": "iPad Pro", "width": 1024, "height": 1366, "is_mobile": False},
    {"name": "Desktop 1080p", "width": 1920, "height": 1080, "is_mobile": False},
    {"name": "Ultrawide 4K", "width": 2560, "height": 1440, "is_mobile": False},
]

AUTH_COOKIE = {
    "name": "dbert_auth",
    "value": "b21c99e7fd6143eb63648da7f7d5963fbba699c285ffbbd37b5b0aebcbfcfa1b",
    "domain": "lms.dbert.in",
    "path": "/",
}

out_dir = Path(r"C:\Users\user\.gemini\antigravity\brain\db340522-3de4-46ab-8736-005fb1623326\screenshots")
out_dir.mkdir(parents=True, exist_ok=True)

def run_responsive_tests():
    print("=" * 70)
    print("  STIPEND TASKS SCHEDULED DASHBOARD - RESPONSIVE AUDIT")
    print("=" * 70)

    total = 0
    passed = 0
    failed = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for vp in VIEWPORTS:
            total += 1
            w, h, name = vp["width"], vp["height"], vp["name"]
            print(f"\n--- Testing Viewport: {name} ({w}x{h}) ---")

            context = browser.new_context(
                viewport={"width": w, "height": h},
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15" if vp["is_mobile"] else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
            )
            context.add_cookies([AUTH_COOKIE])
            page = context.new_page()

            res = page.goto("https://lms.dbert.in/stipend/tasks", wait_until="domcontentloaded")
            page.wait_for_timeout(1000)

            # Check horizontal overflow
            overflow = page.evaluate("""() => {
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

            # Check CTA button heights on mobile
            btn_metrics = page.evaluate("""() => {
                const btns = Array.from(document.querySelectorAll('.dossier-btn-group .stipend-cta-btn'));
                return btns.map(b => {
                    const rect = b.getBoundingClientRect();
                    return {
                        text: b.innerText.trim().replace(/\\s+/g, ' '),
                        width: Math.round(rect.width),
                        height: Math.round(rect.height),
                        meetsTarget: rect.height >= 40
                    };
                });
            }""")

            scroll_w = overflow["scrollWidth"]
            inner_w = overflow["innerWidth"]
            has_overflow = overflow["hasOverflow"]

            if not has_overflow:
                print(f"  [PASS] Zero Overflow: {scroll_w}px / {inner_w}px")
                passed += 1
            else:
                print(f"  [FAIL] Overflow Detected: {scroll_w}px > {inner_w}px")
                failed.append(f"{name}: Overflow {scroll_w} > {inner_w}")

            print(f"  [INFO] Action Buttons ({len(btn_metrics)} found):")
            for b in btn_metrics:
                status = "PASS (>=40px)" if b["meetsTarget"] else "FAIL (<40px)"
                print(f"         - {b['text'][:30]:<32} | {b['width']}x{b['height']}px | {status}")

            # Capture screenshots for key representative devices
            if name == "iPhone 14 / Pixel":
                shot_path = out_dir / "6_stipend_tasks_scheduled_mobile_iphone14.png"
                page.screenshot(path=str(shot_path), full_page=True)
                print(f"  [SAVED] Mobile screenshot -> {shot_path.name}")
            elif name == "iPad Mini":
                shot_path = out_dir / "6_stipend_tasks_scheduled_tablet_ipad.png"
                page.screenshot(path=str(shot_path), full_page=True)
                print(f"  [SAVED] Tablet screenshot -> {shot_path.name}")
            elif name == "Desktop 1080p":
                shot_path = out_dir / "6_stipend_tasks_scheduled_desktop.png"
                page.screenshot(path=str(shot_path), full_page=False)
                print(f"  [SAVED] Desktop screenshot -> {shot_path.name}")

            context.close()

        browser.close()

    print("\n" + "=" * 70)
    print(f"SUMMARY: {passed}/{total} viewports passed zero-overflow validation.")
    if failed:
        print("FAILURES:")
        for f in failed:
            print(" -", f)
    print("=" * 70)

if __name__ == "__main__":
    run_responsive_tests()
