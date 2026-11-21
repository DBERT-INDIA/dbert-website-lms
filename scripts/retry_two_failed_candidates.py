#!/usr/bin/env python3
import sys
import os
import time
import json
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

SESSION_ACC2 = Path(r"C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2")
QUEUE_FILE = Path(r"C:\Users\user\Desktop\dbert-website-lms\data\whatsapp_selected_multi_login_queue.json")

with open(QUEUE_FILE, "r", encoding="utf-8") as f:
    queue = json.load(f)

targets = [q for q in queue if q["app_id"] in (5252, 5217)]
print(f"Retrying {len(targets)} candidates...")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_ACC2),
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-accelerated-2d-canvas",
            "--no-first-run",
            "--no-zygote",
            "--disable-gpu",
            "--mute-audio"
        ],
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    page = browser.pages[0] if browser.pages else browser.new_page()

    page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
    time.sleep(10)

    for cand in targets:
        phone = cand["phone"]
        name = cand["name"]
        print(f"\n--- Retrying {name} ({phone}) ---")
        encoded_text = urllib.parse.quote(cand["message"])
        target_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_text}"
        
        page.goto(target_url, wait_until="domcontentloaded")
        
        sent = False
        for attempt in range(40):
            # Check for invalid number or not on whatsapp modal
            dialogs = page.query_selector_all('div[role="dialog"], div[data-animate-modal-body="true"]')
            starting_chat = False
            for d in dialogs:
                try:
                    txt = d.inner_text()
                    print(f"  Attempt {attempt} modal dialog text: {txt[:100]}")
                    if any(term in txt.lower() for term in ["invalid", "not on whatsapp", "couldn't find"]):
                        btn = d.query_selector("button")
                        if btn: btn.click()
                        print(f"  RESULT: NOT_ON_WHATSAPP / INVALID")
                        sent = "NOT_ON_WHATSAPP"
                        break
                    elif "starting chat" in txt.lower():
                        starting_chat = True
                except Exception as e:
                    pass
            if sent == "NOT_ON_WHATSAPP":
                break

            if starting_chat:
                time.sleep(1)
                continue

            send_btn = page.query_selector('button[aria-label="Send"], button[data-testid="send"], span[data-icon="send"]')
            if send_btn:
                print(f"  Found send button on attempt {attempt}! Clicking...")
                try:
                    tag = page.evaluate("(el) => el.tagName.toLowerCase()", send_btn)
                    if tag != "button":
                        btn_parent = page.evaluate_handle("(el) => el.closest('button') || el", send_btn)
                        btn_parent.click()
                    else:
                        send_btn.click()
                    time.sleep(3)
                    sent = True
                    break
                except Exception as e:
                    print(f"  Click error: {e}")

            chat_input = page.query_selector('footer div[contenteditable="true"], div[role="textbox"]')
            if chat_input:
                try:
                    text_content = chat_input.inner_text().strip()
                    if text_content:
                        print(f"  Found chatbox text! Pressing Enter on attempt {attempt}...")
                        chat_input.focus()
                        time.sleep(0.5)
                        page.keyboard.press("Enter")
                        time.sleep(3)
                        sent = True
                        break
                except Exception as e:
                    print(f"  Enter error: {e}")

            time.sleep(1)

        print(f"Final status for {name} ({phone}): {sent}")
        page.screenshot(path=f"data/retry_{phone}.png")
        if sent is True:
            time.sleep(20)

    browser.close()
