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

sessions = {
    1: AIVARA_DIR / ".chrome_session_account1" if (AIVARA_DIR / ".chrome_session_account1").exists() else PROJECT_ROOT / ".chrome_session_account1",
    2: AIVARA_DIR / ".chrome_session_account2" if (AIVARA_DIR / ".chrome_session_account2").exists() else PROJECT_ROOT / ".chrome_session_account2",
}

results = {}

launch_args = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-infobars",
    "--remote-debugging-port=0",
]

with sync_playwright() as p:
    for acc_num in [1, 2]:
        session_dir = str(sessions[acc_num])
        print(f"\n{'='*60}")
        print(f"Checking WhatsApp Web Status for Account {acc_num}...")
        print(f"Session Dir: {session_dir}")
        print(f"{'='*60}")
        
        browser = None
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
        except Exception as e:
            print(f"System Chrome launch failed ({e}), trying bundled Chromium...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
            
        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.on("dialog", lambda d: d.accept())
        
        status = "UNKNOWN"
        details = ""
        
        try:
            print(f"[*] Navigating to https://web.whatsapp.com for Account {acc_num}...")
            page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=45000)
            
            # Wait and poll for up to 25 seconds
            for i in range(12):
                time.sleep(2)
                
                # Check for Chat List (Logged In)
                chat_list = page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header, [data-testid='chatlist-header']")
                if chat_list:
                    status = "LOGGED_IN"
                    details = "Chat list found (active session verified)"
                    break
                    
                # Check for QR Code (Not Logged In)
                qr = page.query_selector("canvas, [data-testid='qrcode'], div[data-ref]")
                if qr:
                    status = "NOT_LOGGED_IN_QR_REQUIRED"
                    details = "QR Code is displayed; phone pairing required"
                    break
                
                # Check for Phone Logged Out / Syncing message
                retry_btn = page.query_selector("button:has-text('Log out'), button:has-text('Retry')")
                text_content = page.content().lower()
                if "log in to whatsapp" in text_content or "to use whatsapp on your computer" in text_content:
                    if page.query_selector("canvas"):
                        status = "NOT_LOGGED_IN_QR_REQUIRED"
                        details = "QR Code prompt active on login page"
                        break
                        
                print(f"    ... waiting for WhatsApp Web to render state ({i*2 + 2}s)")
            
            # Save screenshot for audit
            screenshot_path = PROJECT_ROOT / f"data/whatsapp_acc{acc_num}_status.png"
            page.screenshot(path=str(screenshot_path))
            print(f"[*] Saved screenshot to: {screenshot_path}")
            
        except Exception as ex:
            status = "ERROR"
            details = str(ex)
            print(f"[!] Error during check: {ex}")
            
        finally:
            browser.close()
            time.sleep(2)
            
        results[acc_num] = {
            "status": status,
            "details": details,
            "session_dir": session_dir
        }

print("\n" + "#"*60)
print("FINAL WHATSAPP LOGIN AUDIT REPORT")
print("#"*60)
for acc_num, res in results.items():
    print(f"Account {acc_num}: {res['status']} | {res['details']}")
