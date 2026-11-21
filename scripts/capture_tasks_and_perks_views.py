from playwright.sync_api import sync_playwright
import time
from pathlib import Path

out_dir = Path(r"C:\Users\user\.gemini\antigravity\brain\db340522-3de4-46ab-8736-005fb1623326\screenshots")
out_dir.mkdir(parents=True, exist_ok=True)

AUTH_TOKEN = "b21c99e7fd6143eb63648da7f7d5963fbba699c285ffbbd37b5b0aebcbfcfa1b"

views = [
    {
        "name": "11_tasks_open_bounties_desktop.png",
        "url": "https://lms.dbert.in/tasks#available",
        "viewport": {"width": 1280, "height": 1050},
        "tab": "available"
    },
    {
        "name": "12_tasks_coin_perks_desktop.png",
        "url": "https://lms.dbert.in/tasks#perks",
        "viewport": {"width": 1280, "height": 1050},
        "tab": "perks"
    },
    {
        "name": "13_tasks_open_bounties_tablet.png",
        "url": "https://lms.dbert.in/tasks#available",
        "viewport": {"width": 820, "height": 1180},
        "tab": "available"
    },
    {
        "name": "14_tasks_open_bounties_mobile.png",
        "url": "https://lms.dbert.in/tasks#available",
        "viewport": {"width": 390, "height": 844},
        "tab": "available"
    },
    {
        "name": "15_tasks_coin_perks_mobile.png",
        "url": "https://lms.dbert.in/tasks#perks",
        "viewport": {"width": 390, "height": 844},
        "tab": "perks"
    },
    {
        "name": "16_coins_ledger_with_perks_cta.png",
        "url": "https://lms.dbert.in/account/coins",
        "viewport": {"width": 1280, "height": 950},
        "tab": None
    }
]

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    for v in views:
        ctx = b.new_context(viewport=v["viewport"])
        ctx.add_cookies([
            {
                "name": "dbert_auth",
                "value": AUTH_TOKEN,
                "domain": ".dbert.in",
                "path": "/"
            },
            {
                "name": "dbert_auth",
                "value": AUTH_TOKEN,
                "domain": "lms.dbert.in",
                "path": "/"
            }
        ])
        page = ctx.new_page()
        page.goto(v["url"], wait_until="domcontentloaded")
        time.sleep(3)

        if v["tab"]:
            page.evaluate(f"window.switchTab && window.switchTab('{v['tab']}')")
            time.sleep(1)

        dest = out_dir / v["name"]
        page.screenshot(path=str(dest))
        print(f"Captured {v['name']} at {v['viewport']}")
        ctx.close()
    b.close()
print("All screenshots captured successfully!")
