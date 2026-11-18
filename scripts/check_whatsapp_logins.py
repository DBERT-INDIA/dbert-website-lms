import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
SESSION_ACC1 = AIVARA_DIR / ".chrome_session_account1"
SESSION_ACC2 = AIVARA_DIR / ".chrome_session_account2"

def check_account_session(acc_num: int):
    session_dir = str(SESSION_ACC1 if acc_num == 1 else SESSION_ACC2)
    print("=" * 70)
    print(f"CHECKING WHATSAPP LOGIN STATUS: ACCOUNT {acc_num}")
    print(f"Session Dir: {session_dir}")
    print("=" * 70)

    with sync_playwright() as p:
        try:
            # Launch headless to verify without interrupting user
            context = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                ]
            )
        except Exception as e:
            print(f"[WARN] Failed to launch with channel='chrome': {e}. Retrying default chromium...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=True,
                ignore_default_args=["--enable-automation"],
            )

        page = context.pages[0] if context.pages else context.new_page()

        try:
            print(f"[Account {acc_num}] Navigating to https://web.whatsapp.com...")
            page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=45000)

            # Wait for either chat list (logged in) or QR code (logged out)
            chat_list_sel = "#pane-side, [data-testid='chat-list'], div[role='grid']"
            qr_sel = "canvas[aria-label='Scan this QR code to use WhatsApp Web'], div[data-ref]"

            print(f"[Account {acc_num}] Checking page elements (waiting up to 15s)...")
            try:
                elem = page.wait_for_selector(f"{chat_list_sel}, {qr_sel}", timeout=15000)
                tag = elem.evaluate("el => el.tagName.toLowerCase()")
                is_qr = "canvas" in tag or elem.get_attribute("data-ref") is not None
                if is_qr:
                    print(f"❌ [ACCOUNT {acc_num}] NOT LOGGED IN — QR code is present!")
                    logged_in = False
                else:
                    print(f"✅ [ACCOUNT {acc_num}] LOGGED IN SUCCESSFULLY — Chat list is active!")
                    logged_in = True
            except Exception:
                # Check current URL or page title
                title = page.title()
                print(f"[Account {acc_num}] Timeout waiting for primary selector. Page title: '{title}'")
                # Look deeper for chat list
                if page.locator("#pane-side").count() > 0 or page.locator("div[role='grid']").count() > 0:
                    print(f"✅ [ACCOUNT {acc_num}] LOGGED IN — Found chat pane container.")
                    logged_in = True
                elif page.locator("canvas").count() > 0:
                    print(f"❌ [ACCOUNT {acc_num}] NOT LOGGED IN — Found QR canvas.")
                    logged_in = False
                else:
                    print(f"⚠️ [ACCOUNT {acc_num}] UNKNOWN / LOADING STATE — Neither chat pane nor QR canvas found.")
                    logged_in = False

            context.close()
            return logged_in

        except Exception as e:
            print(f"[ERROR] Error checking Account {acc_num}: {e}")
            try: context.close()
            except Exception: pass
            return False

if __name__ == "__main__":
    acc1_status = check_account_session(1)
    acc2_status = check_account_session(2)

    print("\n" + "=" * 70)
    print("WHATSAPP SESSIONS AUDIT RESULT:")
    print(f"  Account 1: {'LOGGED IN (Ready to send)' if acc1_status else 'LOGGED OUT (Needs QR Scan)'}")
    print(f"  Account 2: {'LOGGED IN (Ready to send)' if acc2_status else 'LOGGED OUT (Needs QR Scan)'}")
    print("=" * 70)
