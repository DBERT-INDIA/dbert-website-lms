#!/usr/bin/env python3
"""Check why Sabreen Saed and abhinand sagar timed out."""
import sys
import json
import time
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

SESSION_ACC2 = Path(r"C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2")

cands = [
    {"name": "Sabreen Saed", "phone": "918958006694", "offer_id": "DBERT-OFR-2026-CS-5252"},
    {"name": "abhinand sagar", "phone": "917975942091", "offer_id": "DBERT-OFR-2026-DM-5217"}
]

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_ACC2),
        headless=True,
        args=["--no-sandbox", "--disable-gpu"]
    )
    page = browser.pages[0] if browser.pages else browser.new_page()

    for cand in cands:
        phone = cand["phone"]
        name = cand["name"]
        print(f"\n--- Checking {name} ({phone}) ---")
        url = f"https://web.whatsapp.com/send?phone={phone}&text=test"
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        time.sleep(5)
        
        # Check dialogs
        dialogs = page.query_selector_all('div[role="dialog"]')
        print(f"Dialog count: {len(dialogs)}")
        for d in dialogs:
            try:
                print(f"Dialog text: {d.inner_text()}")
            except Exception as e:
                print(f"Dialog err: {e}")

        # Check send button or compose
        send_btn = page.query_selector('button[aria-label="Send"], button[data-testid="send"]')
        print(f"Send button found: {bool(send_btn)}")
        chat_box = page.query_selector('div[contenteditable="true"]')
        print(f"Chat box found: {bool(chat_box)}")

        page.screenshot(path=f"data/check_{phone}.png")
        print(f"Screenshot saved to data/check_{phone}.png")

    browser.close()
