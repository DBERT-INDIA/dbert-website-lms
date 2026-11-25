import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
SESSION_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2")

print("=" * 70)
print("  DBERT WHATSAPP WEB LOGIN HELPER (ACCOUNT 2)")
print("=" * 70)
print(f"Session Folder: {SESSION_DIR}")
print("Opening visible browser window for WhatsApp Web login...")
print("Please scan the QR code using WhatsApp on your phone (Linked Devices).")
print("Once you see your chats loaded, keep the browser open or close it when done.")
print("=" * 70)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_DIR),
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ],
        user_agent=USER_AGENT
    )
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

    logged_in = False
    # Poll until login detected or window closed
    while True:
        if page.is_closed():
            print("\nBrowser window closed.")
            break
        
        chat_pane = page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header, div[role='textbox']")
        if chat_pane and not logged_in:
            logged_in = True
            print("\n" + "*" * 70)
            print("  SUCCESS: WhatsApp Web logged in successfully!")
            print("  Session credentials have been saved to .chrome_session_account2.")
            print("  You can now close the browser window and return to chat.")
            print("*" * 70 + "\n")
        
        time.sleep(2)

    browser.close()
