import os
import time
from playwright.sync_api import sync_playwright

artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\9e76c80f-9681-4f52-a13d-330f08edd6f5"
os.makedirs(artifact_dir, exist_ok=True)

targets = [
    {
        "name": "santosh",
        "email": "turlapatisantosh@gmail.com",
        "token": "3a48660648309d1a63174658aeb707d6d18968453c8e1a9d419cb0ecf5d9d033",
    },
    {
        "name": "ratnadeep",
        "email": "ratnadeepratu737@gmail.com",
        "token": "f5eb19ac5ff7d7b66d0a18c7c108af2d4050f1fc0bdcd9e59e89379ec437baf0",
    }
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for tgt in targets:
        print(f"--- Processing {tgt['name']} ({tgt['email']}) ---")
        context = browser.new_context(
            viewport={"width": 1440, "height": 960},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        context.add_init_script("""
            const cd = String(Date.now() + 24 * 3600 * 1000);
            localStorage.setItem('dbert_push_modal_dismissed_until', cd);
            localStorage.setItem('dbert_push_blocked_dismissed_until', cd);
        """)
        context.add_cookies([
            {
                "name": "dbert_auth",
                "value": tgt["token"],
                "domain": "lms.dbert.in",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax"
            },
            {
                "name": "dbert_session",
                "value": tgt["token"],
                "domain": "lms.dbert.in",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax"
            }
        ])

        page = context.new_page()
        page.goto("https://lms.dbert.in/portal", wait_until="networkidle", timeout=30000)
        time.sleep(3)

        # Force hide push modal overlays
        page.evaluate("""() => {
            const m = document.getElementById('dbertPushModal');
            if (m) m.style.display = 'none';
            document.querySelectorAll('#dbertPushModal, #dbertPushBlockedModal, .scrim, .modal-backdrop').forEach(el => el.remove());
        }""")
        time.sleep(1)

        # 1. Hero / Top Screen
        hero_file = os.path.join(artifact_dir, f"dashboard_{tgt['name']}_hero.png")
        page.screenshot(path=hero_file)
        print(f"Saved: {hero_file}")

        # 2. Scroll to Attendance Hub
        page.evaluate("""() => {
            const el = document.getElementById('ovAccepted') || document.querySelector('.dash-grid');
            if (el) {
                el.scrollIntoView({ behavior: 'instant', block: 'start' });
            }
        }""")
        time.sleep(1)
        att_file = os.path.join(artifact_dir, f"dashboard_{tgt['name']}_attendance.png")
        page.screenshot(path=att_file)
        print(f"Saved: {att_file}")

        # 3. Full Page
        full_file = os.path.join(artifact_dir, f"dashboard_{tgt['name']}_full.png")
        page.screenshot(path=full_file, full_page=True)
        print(f"Saved: {full_file}")

        context.close()

    browser.close()

print("All screenshots successfully captured!")
