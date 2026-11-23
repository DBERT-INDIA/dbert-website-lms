#!/usr/bin/env python3
"""
================================================================================
DBERT — Interactive WhatsApp Web Login Helper
================================================================================
Launches a dedicated visible Chromium browser window using Playwright.
Avoids Chrome multi-process collision (0x80000003) on Windows.
Keeps the window open, renders the WhatsApp Web QR code, and automatically
detects when the QR code is scanned and the chat interface is loaded.
================================================================================
"""

import sys
import time
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")
AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")

SESSION_PATHS = {
    1: AIVARA_DIR / ".chrome_session_account1" if (AIVARA_DIR / ".chrome_session_account1").exists() else PROJECT_ROOT / ".chrome_session_account1",
    2: AIVARA_DIR / ".chrome_session_account2" if (AIVARA_DIR / ".chrome_session_account2").exists() else PROJECT_ROOT / ".chrome_session_account2",
}

def login_account(acc_num: int, timeout_sec: int = 300):
    session_dir = SESSION_PATHS.get(acc_num)
    print("=" * 76)
    print(f"      DBERT WHATSAPP WEB LOGIN HELPER — ACCOUNT {acc_num}")
    print("=" * 76)
    print(f"[*] Session Folder : {session_dir}")
    print(f"[*] Launching browser window for Account {acc_num}...")
    print("[*] Please keep this window open and scan the QR code with your phone.")
    print("=" * 76)

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
    ]

    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(session_dir),
                headless=False,
                args=launch_args,
                viewport={"width": 1100, "height": 800}
            )
        except Exception as e:
            print(f"[!] Error launching browser: {e}")
            return False

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()

        print("[*] Navigating to https://web.whatsapp.com...")
        try:
            page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)
        except Exception as e_nav:
            print(f"[!] Navigation notice: {e_nav}")

        print("\n[*] Waiting for you to scan the QR code...")
        print("[*] (If already logged in, the chat list will appear automatically.)\n")

        start_time = time.time()
        logged_in = False

        while time.time() - start_time < timeout_sec:
            if page.is_closed():
                print("[!] Browser window was closed by the user.")
                break

            # Check if chat interface is loaded
            chat_pane = page.query_selector("[aria-label='Chat list'], #side, #pane-side, [data-testid='chat-list']")
            if chat_pane:
                logged_in = True
                break

            # Print countdown pulse every 10s
            elapsed = int(time.time() - start_time)
            if elapsed > 0 and elapsed % 15 == 0:
                remaining = timeout_sec - elapsed
                print(f"    ... waiting for QR scan ({remaining}s remaining) ...")

            time.sleep(2)

        if logged_in:
            print("\n" + "=" * 76)
            print(f"  [✓] SUCCESS: ACCOUNT {acc_num} IS AUTHENTICATED AND LOGGED IN!")
            print(f"  [✓] Session permanently saved to: {session_dir.name}")
            print("=" * 76)
            time.sleep(3)
            try:
                browser.close()
            except Exception:
                pass
            return True
        else:
            print("\n[!] Login was not completed within the time limit.")
            try:
                browser.close()
            except Exception:
                pass
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp Web Login Helper")
    parser.add_argument("--account", type=int, choices=[1, 2], required=True, help="Account number (1 or 2)")
    parser.add_argument("--timeout", type=int, default=300, help="Max wait seconds for QR scan")
    args = parser.parse_args()

    success = login_account(args.account, args.timeout)
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
