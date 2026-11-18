import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SESSION_ACC1 = (
    AIVARA_DIR / ".chrome_session_account1"
    if (AIVARA_DIR / ".chrome_session_account1").exists()
    else PROJECT_ROOT / ".chrome_session_account1"
)
SESSION_ACC2 = (
    AIVARA_DIR / ".chrome_session_account2"
    if (AIVARA_DIR / ".chrome_session_account2").exists()
    else PROJECT_ROOT / ".chrome_session_account2"
)

def check_account(acc_num: int):
    session_dir = str(SESSION_ACC1 if acc_num == 1 else SESSION_ACC2)
    print(f"\n==================================================")
    print(f"Checking WhatsApp Account {acc_num}")
    print(f"Session Dir: {session_dir}")
    print(f"==================================================")

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
    ]

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
        except Exception as e:
            print(f"Error launching system Chrome: {e}. Trying bundled Chromium...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()

        print(f"Navigating to web.whatsapp.com for Account {acc_num}...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        # Wait up to 20 seconds to see if chat list or QR code appears
        start_t = time.time()
        logged_in = False
        qr_detected = False

        while time.time() - start_t < 25:
            if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                logged_in = True
                break
            if page.query_selector("canvas, [data-testid='qrcode']"):
                qr_detected = True
                break
            time.sleep(1)

        print(f"Account {acc_num} Result:")
        if logged_in:
            print(f"  --> LOGGED IN: YES! (Chat list detected)")
        elif qr_detected:
            print(f"  --> LOGGED IN: NO! (QR Code detected on screen)")
        else:
            print(f"  --> UNKNOWN / TIMEOUT (Neither chat list nor QR code appeared within 25s)")

        # Keep browser open a bit or close
        browser.close()
        return logged_in, qr_detected

if __name__ == "__main__":
    acc = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    check_account(acc)
