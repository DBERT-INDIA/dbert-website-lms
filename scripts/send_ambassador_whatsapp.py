#!/usr/bin/env python3
"""
scripts/send_ambassador_whatsapp.py
================================================================================
DBERT — Ambassador & Referred Leads WhatsApp Outreach Dispatcher
================================================================================
Dispatches official WhatsApp lead updates to Ambassadors and seat conversion
notices to Referred Leads using Playwright with persistent Chrome sessions.

Features:
- Reads from data/ambassador_whatsapp_queue.json
- Dual-Account distribution:
    * Account 1: Odd records (.chrome_session_account1)
    * Account 2: Even records (.chrome_session_account2)
- Interactive and Auto-dispatch modes
- Human pacing: 18s - 30s randomized delays
- Permanent tracking in data/ambassador_whatsapp_tracking.json & .csv
- Idempotent: Skips already sent recipients automatically
================================================================================
"""

import os
import sys
import time
import json
import csv
import random
import argparse
import urllib.parse
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

QUEUE_FILE = DATA_DIR / "ambassador_whatsapp_queue.json"
TRACKING_FILE = DATA_DIR / "ambassador_whatsapp_tracking.json"
TRACKING_CSV = DATA_DIR / "ambassador_whatsapp_tracking.csv"
LOG_FILE = DATA_DIR / "ambassador_whatsapp_dispatch.log"

AIVARA_SESSIONS_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
LOCAL_SESSIONS_DIR = ROOT_DIR

SESSION_ACC1 = (
    AIVARA_SESSIONS_DIR / ".chrome_session_account1"
    if (AIVARA_SESSIONS_DIR / ".chrome_session_account1").exists()
    else LOCAL_SESSIONS_DIR / ".chrome_session_account1"
)

SESSION_ACC2 = (
    AIVARA_SESSIONS_DIR / ".chrome_session_account2"
    if (AIVARA_SESSIONS_DIR / ".chrome_session_account2").exists()
    else LOCAL_SESSIONS_DIR / ".chrome_session_account2"
)


def log_message(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass


def load_tracking() -> dict:
    if TRACKING_FILE.exists():
        try:
            with open(TRACKING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_tracking(tracking: dict):
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump(tracking, f, indent=2, ensure_ascii=False)
    
    rows = list(tracking.values())
    if rows:
        fieldnames = ["key", "type", "name", "phone", "email", "status", "sent_at", "account_used", "error"]
        with open(TRACKING_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for r in rows:
                writer.writerow(r)


def send_whatsapp_message(page, phone: str, message: str) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    if not phone or len(phone) < 10:
        return False, "INVALID_PHONE"

    encoded_msg = urllib.parse.quote(message)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
    except Exception as e_nav:
        err_msg = str(e_nav).lower()
        if "closed" in err_msg:
            return False, f"BROWSER_CLOSED: {str(e_nav)}"

    t_start = time.time()
    while time.time() - t_start < 35:
        if page.is_closed():
            return False, "BROWSER_CLOSED"

        # Check for invalid number dialog
        dialogs = page.query_selector_all("[role='dialog']")
        for d in dialogs:
            try:
                txt = d.inner_text().lower()
                if any(term in txt for term in ["invalid", "not on whatsapp", "couldn't find"]):
                    btn = d.query_selector("button")
                    if btn:
                        btn.click()
                    return False, "NOT_ON_WHATSAPP"
            except Exception:
                pass

        # Try to find Send button
        send_btn = page.query_selector('button[aria-label="Send"], button[data-testid="send"], button[data-testid="compose-btn-send"], span[data-icon="send"]')
        if send_btn:
            try:
                time.sleep(0.8)
                tag = page.evaluate("(el) => el.tagName.toLowerCase()", send_btn)
                if tag != "button":
                    btn_parent = page.evaluate_handle("(el) => el.closest('button') || el", send_btn)
                    btn_parent.click()
                else:
                    send_btn.click()
                time.sleep(2.5)
                return True, "SENT"
            except Exception as e_click:
                pass

        time.sleep(1)

    return False, "SEND_BUTTON_TIMEOUT"


def run_worker(account_num: int, queue_items: list, auto_start: bool = True, delay_min: float = 18.0, delay_max: float = 28.0):
    session_dir = str(SESSION_ACC1 if account_num == 1 else SESSION_ACC2)
    log_message(f"Starting WhatsApp Worker Account {account_num} with {len(queue_items)} items...")
    log_message(f"Session directory: {session_dir}")

    from playwright.sync_api import sync_playwright

    tracking = load_tracking()

    with sync_playwright() as p:
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--remote-debugging-port=0",
        ]

        browser = None
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
        except Exception as e_chrome:
            log_message(f"Chrome channel launch fallback ({e_chrome}). Launching bundled Chromium...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.on("dialog", lambda d: d.accept())

        log_message(f"Navigating to WhatsApp Web (Account {account_num})...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        logged_in = False
        for _ in range(30):
            if page.is_closed():
                break
            if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                logged_in = True
                break
            time.sleep(1)

        if not logged_in:
            log_message(f"Account {account_num} is not logged in. Waiting for QR scan (up to 120s)...")
            for _ in range(60):
                if page.is_closed():
                    log_message(f"Browser closed for Account {account_num}.")
                    return
                if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                    logged_in = True
                    break
                time.sleep(2)

        if not logged_in:
            log_message(f"Account {account_num} login timed out. Aborting.")
            return

        log_message(f"Account {account_num} is ACTIVE! Starting dispatch in 3s...")
        time.sleep(3)

        success_count = 0
        fail_count = 0

        for i, item in enumerate(queue_items, 1):
            phone = item.get("phone", "")
            name = item.get("name", "")
            itype = item.get("type", "")
            key = f"{itype}_{phone}"

            if key in tracking and tracking[key].get("status") == "SENT":
                log_message(f"[{i}/{len(queue_items)}] SKIP (Already sent): {name} (+{phone})")
                continue

            log_message(f"[{i}/{len(queue_items)}] Sending to {name} (+{phone}) [{itype}]...")
            ok, detail = send_whatsapp_message(page, phone, item["message"])

            if ok:
                success_count += 1
                tracking[key] = {
                    "key": key,
                    "type": itype,
                    "name": name,
                    "phone": phone,
                    "email": item.get("email"),
                    "status": "SENT",
                    "sent_at": datetime.now().isoformat(),
                    "account_used": f"Account {account_num}"
                }
                save_tracking(tracking)
                log_message(f"[{i}/{len(queue_items)}] SUCCESS: Delivered to {name} (+{phone})")
            else:
                fail_count += 1
                tracking[key] = {
                    "key": key,
                    "type": itype,
                    "name": name,
                    "phone": phone,
                    "email": item.get("email"),
                    "status": "FAILED",
                    "failed_at": datetime.now().isoformat(),
                    "account_used": f"Account {account_num}",
                    "error": detail
                }
                save_tracking(tracking)
                log_message(f"[{i}/{len(queue_items)}] FAILED: {name} (+{phone}) | {detail}")

            if "BROWSER_CLOSED" in detail:
                break

            if i < len(queue_items):
                delay = random.uniform(delay_min, delay_max)
                log_message(f"Pacing cooldown: {delay:.1f}s...")
                time.sleep(delay)

        log_message(f"Worker Account {account_num} completed. Sent: {success_count}, Failed: {fail_count}")


def main():
    parser = argparse.ArgumentParser(description="DBERT Ambassador & Lead WhatsApp Dispatcher")
    parser.add_argument("--account", type=int, choices=[1, 2], default=1, help="Chrome account session to use (1 or 2)")
    parser.add_argument("--all-accounts", action="store_true", help="Split queue across both accounts sequentially")
    parser.add_argument("--status", action="store_true", help="Show dispatch progress and status")
    args = parser.parse_args()

    if args.status:
        tracking = load_tracking()
        print(f"Total tracked WhatsApp dispatches: {len(tracking)}")
        sent = sum(1 for v in tracking.values() if v.get("status") == "SENT")
        failed = sum(1 for v in tracking.values() if v.get("status") == "FAILED")
        print(f"Sent: {sent} | Failed: {failed}")
        for k, v in tracking.items():
            print(f"  {v.get('type')}: {v.get('name')} (+{v.get('phone')}) -> {v.get('status')} [{v.get('account_used')}]")
        return

    if not QUEUE_FILE.exists():
        log_message(f"Queue file not found: {QUEUE_FILE}. Please run dispatch_ambassador_outreach.py --whatsapp-export first.")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    log_message(f"Loaded {len(queue)} items from {QUEUE_FILE}")

    if args.all_accounts:
        # Split odd/even
        acc1_items = [item for i, item in enumerate(queue) if i % 2 == 0]
        acc2_items = [item for i, item in enumerate(queue) if i % 2 == 1]
        log_message(f"Partitioned queue: Account 1 ({len(acc1_items)} items), Account 2 ({len(acc2_items)} items)")
        
        if acc1_items:
            log_message("Launching Account 1 batch...")
            run_worker(1, acc1_items)
        if acc2_items:
            log_message("Launching Account 2 batch...")
            run_worker(2, acc2_items)
    else:
        run_worker(args.account, queue)


if __name__ == "__main__":
    main()
