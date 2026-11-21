from playwright.sync_api import sync_playwright
import time
from pathlib import Path

out_path = Path(r"C:\Users\user\.gemini\antigravity\brain\db340522-3de4-46ab-8736-005fb1623326\screenshots\6_stipend_tasks_scheduled.png")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1280, "height": 1520})
    ctx.add_cookies([{
        "name": "dbert_auth",
        "value": "b21c99e7fd6143eb63648da7f7d5963fbba699c285ffbbd37b5b0aebcbfcfa1b",
        "domain": "lms.dbert.in",
        "path": "/"
    }])
    page = ctx.new_page()
    page.goto("https://lms.dbert.in/stipend/tasks", wait_until="domcontentloaded")
    time.sleep(3)
    
    # Check text
    found = page.locator("text='Thursday, 03 December 2026'").count()
    print(f"Matches for 'Thursday, 03 December 2026': {found}")
    
    page.screenshot(path=str(out_path))
    b.close()
    print("Screenshot saved to", out_path)
