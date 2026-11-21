#!/usr/bin/env python3
"""
================================================================================
DBERT Dual-Account WhatsApp Campaign Dispatcher (50 Messages)
- Account 1: 13 leads (₹499) + 13 leads (₹299) = 26 messages
- Account 2: 12 leads (₹499) + 12 leads (₹299) = 24 messages
- Anti-ban pacing: 18s - 30s randomized delays
- Deduplication & persistent logging: data/dbert_whatsapp_sent_today.json
================================================================================
"""

import sys
import os
import time
import json
import random
import argparse
import urllib.parse
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")
DATA_DIR = PROJECT_ROOT / "data"
AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")

LOG_FILE = DATA_DIR / "whatsapp_dispatch_today.log"
SENT_LOG_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"

SESSION_PATHS = {
    1: AIVARA_DIR / ".chrome_session_account1" if (AIVARA_DIR / ".chrome_session_account1").exists() else PROJECT_ROOT / ".chrome_session_account1",
    2: AIVARA_DIR / ".chrome_session_account2" if (AIVARA_DIR / ".chrome_session_account2").exists() else PROJECT_ROOT / ".chrome_session_account2",
}

def log_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def record_dispatch(entry: dict):
    records = []
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []
    records.append(entry)
    with open(SENT_LOG_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def send_whatsapp_single(page, item: dict, acc_num: int) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    phone = item["clean_phone"]
    msg = item["message"]
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
    except Exception as e_nav:
        err_msg = str(e_nav).lower()
        if "closed" in err_msg:
            return False, f"BROWSER_CLOSED: {str(e_nav)}"

    t_start = time.time()
    sent = False
    
    while time.time() - t_start < 40:
        if page.is_closed():
            return False, "BROWSER_CLOSED"

        dialogs = page.query_selector_all("[role='dialog']")
        starting_chat = False
        for d in dialogs:
            try:
                txt = d.inner_text().lower()
                if any(term in txt for term in ["invalid", "not on whatsapp", "url is invalid", "couldn't find"]):
                    btn = d.query_selector("button")
                    if btn:
                        btn.click()
                    return False, "NOT_ON_WHATSAPP"
                elif "starting chat" in txt:
                    starting_chat = True
            except Exception:
                pass

        if starting_chat:
            time.sleep(1)
            continue

        # Look for send button
        send_btn = page.query_selector('button[aria-label="Send"], button[data-testid="send"], button[data-testid="compose-btn-send"], span[data-icon="send"]')
        if send_btn:
            try:
                time.sleep(1)
                tag = page.evaluate("(el) => el.tagName.toLowerCase()", send_btn)
                if tag != "button":
                    btn_parent = page.evaluate_handle("(el) => el.closest('button') || el", send_btn)
                    btn_parent.click()
                else:
                    send_btn.click()
                time.sleep(3)
                sent = True
                break
            except Exception:
                pass

        # Alternatively press Enter on chat box
        chat_input = page.query_selector('footer div[contenteditable="true"], div[role="textbox"], div[contenteditable="true"][data-tab="10"]')
        if chat_input:
            try:
                text_content = chat_input.inner_text().strip()
                if text_content:
                    chat_input.focus()
                    time.sleep(0.5)
                    page.keyboard.press("Enter")
                    time.sleep(3)
                    sent = True
                    break
            except Exception:
                pass

        time.sleep(1)

    if not sent:
        return False, "TIMEOUT_SEND_NOT_COMPLETED"

    return True, "SENT"

def run_account_worker(acc_num: int, queue_path: Path):
    session_dir = str(SESSION_PATHS[acc_num])
    log_message(f"=== STARTING WORKER FOR ACCOUNT {acc_num} ===")
    log_message(f"Session Dir: {session_dir}")
    log_message(f"Queue File: {queue_path.name}")

    if not queue_path.exists():
        log_message(f"[ERROR] Queue file not found: {queue_path}")
        return

    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)

    log_message(f"Loaded {len(queue)} items for Account {acc_num}.")

    # Load previously sent phones today
    already_sent_phones = set()
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    if r.get("status") == "SENT":
                        already_sent_phones.add(r.get("phone"))
        except Exception:
            pass

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
        "--remote-debugging-port=0",
    ]

    with sync_playwright() as p:
        browser = None
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
        except Exception as e_ch:
            log_message(f"[*] Account {acc_num}: Launching bundled Chromium ({e_ch})...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.on("dialog", lambda d: d.accept())

        log_message(f"[*] Account {acc_num}: Navigating to WhatsApp Web home...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        # Wait for chat list to confirm authenticated state
        chat_loaded = False
        for _ in range(15):
            if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                chat_loaded = True
                break
            time.sleep(2)

        if not chat_loaded:
            log_message(f"[FATAL] Account {acc_num}: WhatsApp Web did not load chat list. Aborting worker.")
            browser.close()
            return

        log_message(f"[OK] Account {acc_num}: Confirmed authenticated. Beginning dispatch sequence...")

        consecutive_failures = 0
        success_count = 0
        failure_count = 0

        for idx, item in enumerate(queue, 1):
            phone = item["clean_phone"]
            name = item["name"]
            c_type = item["type"]

            if phone in already_sent_phones:
                log_message(f"[{idx}/{len(queue)}] Account {acc_num} | SKIP (Already sent): {name} ({phone})")
                continue

            log_message(f"[{idx}/{len(queue)}] Account {acc_num} | Sending {c_type} -> {name} (+{phone})...")
            ok, reason = send_whatsapp_single(page, item, acc_num)

            result_entry = {
                "account": acc_num,
                "phone": phone,
                "name": name,
                "email": item["email"],
                "type": c_type,
                "status": "SENT" if ok else reason,
                "timestamp": datetime.now().isoformat(),
            }
            record_dispatch(result_entry)

            if ok:
                success_count += 1
                consecutive_failures = 0
                already_sent_phones.add(phone)
                log_message(f"   [SUCCESS] Account {acc_num} -> {name} delivered successfully.")
            else:
                failure_count += 1
                consecutive_failures += 1
                log_message(f"   [FAILED] Account {acc_num} -> {name}: {reason}")

            if consecutive_failures >= 3:
                log_message(f"[CIRCUIT BREAKER] Account {acc_num} hit 3 consecutive failures ({reason}). Stopping worker.")
                break

            # Humanized delay before next message
            if idx < len(queue):
                delay = random.uniform(18.0, 28.0)
                log_message(f"   ... Waiting {delay:.1f}s human break before next message...")
                time.sleep(delay)

        log_message(f"=== COMPLETED ACCOUNT {acc_num} DISPATCH: {success_count} Sent, {failure_count} Failed ===")
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run DBERT WhatsApp Campaign Dispatcher")
    parser.add_argument("--account", type=int, choices=[1, 2], help="Run dispatch specifically for Account 1 or Account 2")
    args = parser.parse_args()

    if args.account == 1:
        run_account_worker(1, DATA_DIR / "campaign_dispatch_acc1.json")
    elif args.account == 2:
        run_account_worker(2, DATA_DIR / "campaign_dispatch_acc2.json")
    else:
        # Default run Account 1 then Account 2 sequentially
        run_account_worker(1, DATA_DIR / "campaign_dispatch_acc1.json")
        time.sleep(5)
        run_account_worker(2, DATA_DIR / "campaign_dispatch_acc2.json")
