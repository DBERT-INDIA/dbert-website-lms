import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import time

SESSION_ACC2 = Path(r"C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(str(SESSION_ACC2), headless=True)
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto('https://web.whatsapp.com/send?phone=918958006694&text=hello', wait_until='networkidle', timeout=30000)
    time.sleep(5)
    print("Title:", page.title())
    body = page.inner_text('body')
    print("Body snippet:")
    for line in body.split('\n'):
        if line.strip():
            print("  ", line.strip()[:100])
    browser.close()
