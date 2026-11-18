import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
SESSION_ACC1 = AIVARA_DIR / ".chrome_session_account1"
SESSION_ACC2 = AIVARA_DIR / ".chrome_session_account2"

def login_account(acc_num: int):
    session_dir = str(SESSION_ACC1 if acc_num == 1 else SESSION_ACC2)
    print("\n" + "=" * 76)
    print(f"  LAUNCHING VISIBLE CHROME WINDOW: ACCOUNT {acc_num}")
    print(f"  Session Directory: {session_dir}")
    print("  PLEASE SCAN THE WHATSAPP QR CODE IN THE OPENED CHROME WINDOW")
    print("=" * 76)

    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                viewport={"width": 1280, "height": 800},
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                ]
            )
        except Exception as e:
            print(f"[WARN] Failed with channel='chrome': {e}. Launching default Chromium...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                viewport={"width": 1280, "height": 800},
                ignore_default_args=["--enable-automation"],
            )

        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")

        print(f"\n[Account {acc_num}] WhatsApp Web loaded. Waiting for login...")
        print(f"[Account {acc_num}] Watching for active chat pane (#pane-side)...")

        # Poll until user scans QR code and chat pane appears (up to 3 minutes)
        logged_in = False
        start_time = time.time()
        timeout_seconds = 180

        while time.time() - start_time < timeout_seconds:
            try:
                if page.locator("#pane-side").count() > 0 or page.locator("div[role='grid']").count() > 0:
                    logged_in = True
                    break
            except Exception:
                pass
            time.sleep(2)

        if logged_in:
            print(f"\n✅ [ACCOUNT {acc_num}] LOGIN SUCCESSFUL! Session saved.")
            time.sleep(3)
        else:
            print(f"\n❌ [ACCOUNT {acc_num}] Login timed out after {timeout_seconds}s.")

        context.close()
        return logged_in

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=int, choices=[1, 2], help="Which account to log in (1 or 2)")
    args = parser.parse_args()

    if args.account:
        login_account(args.account)
    else:
        print("\nStep 1: Logging in Account 1...")
        success1 = login_account(1)
        if success1:
            print("\nStep 2: Logging in Account 2...")
            login_account(2)
        else:
            print("\nAccount 1 login was not completed. Run with --account 1 to retry.")
