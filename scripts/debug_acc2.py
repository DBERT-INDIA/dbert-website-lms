import time
from pathlib import Path
from playwright.sync_api import sync_playwright

session = Path(r"C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2")

launch_args = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-infobars",
]

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(session),
        channel="chrome",
        headless=False,
        ignore_default_args=["--enable-automation"],
        args=launch_args,
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=40000)
    time.sleep(10)
    text = page.inner_text("body")
    print("Account 2 Page inner text:\n", text[:300])
    browser.close()
