import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")

acc2_dir = str(AIVARA_DIR / ".chrome_session_account2" if (AIVARA_DIR / ".chrome_session_account2").exists() else PROJECT_ROOT / ".chrome_session_account2")

launch_args = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-infobars",
    "--remote-debugging-port=0",
]

print("Attempting official WhatsApp Web UI logout for Account 2...")

with sync_playwright() as p:
    browser = None
    try:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=acc2_dir,
            channel="chrome",
            headless=False,
            ignore_default_args=["--enable-automation"],
            args=launch_args,
        )
    except Exception as e:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=acc2_dir,
            headless=False,
            ignore_default_args=["--enable-automation"],
            args=launch_args,
        )

    browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=45000)

    time.sleep(5)
    
    # Check if logged in
    chat_list = page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header")
    if chat_list:
        print("[*] Logged in state detected. Clicking Menu -> Log out...")
        
        # Try finding menu button
        menu_btn = page.query_selector("[data-testid='menu-bar-menu'], button[aria-label='Menu'], span[data-icon='menu'], header [data-icon='more-vert'], span[data-icon='more-vert']")
        if menu_btn:
            menu_btn.click()
            time.sleep(2)
            logout_option = page.query_selector("div[role='button']:has-text('Log out'), span:has-text('Log out'), div:has-text('Log out')")
            if logout_option:
                logout_option.click()
                time.sleep(2)
                confirm_btn = page.query_selector("button:has-text('Log out'), div[role='button']:has-text('Log out')")
                if confirm_btn:
                    confirm_btn.click()
                    print("[OK] Clicked confirm Log out in WhatsApp Web UI.")
                    time.sleep(5)
            else:
                print("[!] Logout option in dropdown not found.")
        else:
            print("[!] Menu button not found.")
    else:
        print("[*] Account 2 is not in chat list, already logged out or at QR code.")

    browser.close()
    time.sleep(2)

print("Account 2 UI logout process finished.")
