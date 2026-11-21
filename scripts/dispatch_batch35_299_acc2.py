#!/usr/bin/env python3
"""
================================================================================
DBERT Batch 35 WhatsApp Dispatch Daemon (Account 2 Only)
- Queue: data/whatsapp_299_queue_batch35_acc2.json (35 Candidates)
- Sender: Account 2 (.chrome_session_account2) - Verified LOGGED IN
- Anti-ban pacing: 18s - 35s randomized human pause after delivery
- Multi-layer deduplication & tracking:
  * data/whatsapp_dispatch_299.log
  * data/dbert_whatsapp_sent_today.json
  * data/dbert_whatsapp.db (whatsapp_sent_log)
  * data/dispatch_tracking_batch35_acc2.csv
- Circuit breaker: Halts if 3 consecutive failures occur
================================================================================
"""

import sys
import os
import time
import json
import csv
import random
import argparse
import urllib.parse
import sqlite3
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

LOG_FILE = DATA_DIR / "whatsapp_dispatch_299.log"
SENT_LOG_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_batch35_acc2.csv"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"

QUEUE_FILE = DATA_DIR / "whatsapp_299_queue_batch35_acc2.json"
SESSION_ACC2 = (
    AIVARA_DIR / ".chrome_session_account2"
    if (AIVARA_DIR / ".chrome_session_account2").exists()
    else PROJECT_ROOT / ".chrome_session_account2"
)

def log_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def record_dispatch(entry: dict):
    # 1. Update JSON
    records = []
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []
    records.append(entry)
    try:
        with open(SENT_LOG_JSON, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        log_message(f"[WARN] Failed to write to {SENT_LOG_JSON.name}: {e}")

    # 2. Update CSV
    fieldnames = ["serial_no", "candidate_id", "name", "email", "clean_phone", "cert_id", "domain", "status", "timestamp", "account"]
    file_exists = TRACKING_CSV.exists()
    try:
        with open(TRACKING_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "serial_no": entry.get("serial_no"),
                "candidate_id": entry.get("candidate_id"),
                "name": entry.get("name"),
                "email": entry.get("email"),
                "clean_phone": entry.get("phone"),
                "cert_id": entry.get("cert_id"),
                "domain": entry.get("domain"),
                "status": entry.get("status"),
                "timestamp": entry.get("timestamp"),
                "account": entry.get("account")
            })
    except Exception as e:
        log_message(f"[WARN] Failed to write to CSV: {e}")

    # 3. Update SQLite DB
    if DB_PATH.exists() and entry.get("status") == "SENT":
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT OR IGNORE INTO whatsapp_sent_log 
                (candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.get("candidate_id"),
                entry.get("name"),
                entry.get("email"),
                entry.get("phone"),
                entry.get("cert_id"),
                entry.get("domain"),
                "ACCOUNT_2",
                entry.get("timestamp")
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            log_message(f"[WARN] Failed to update SQLite DB: {e}")

def send_whatsapp_single(page, item: dict) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    phone = item["clean_phone"]
    msg = item["message"]
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e_nav:
        err_msg = str(e_nav).lower()
        if "closed" in err_msg:
            return False, f"BROWSER_CLOSED: {str(e_nav)}"

    t_start = time.time()
    sent = False
    
    while time.time() - t_start < 45:
        if page.is_closed():
            return False, "BROWSER_CLOSED"

        # Check for invalid phone dialog
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
                elif any(term in txt for term in ["what's new", "calling is now available", "update", "privacy"]):
                    c_btn = d.query_selector("button")
                    if c_btn:
                        c_btn.click()
                        time.sleep(1)
            except Exception:
                pass

        # Also dismiss any standalone Continue / OK modal buttons
        cont_btn = page.query_selector("button:has-text('Continue'), button:has-text('OK'), button:has-text('Dismiss')")
        if cont_btn:
            try:
                cont_btn.click()
                time.sleep(1)
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

def run_dispatch(dry_run: bool = False):
    session_dir = str(SESSION_ACC2)
    log_message(f"============================================================")
    log_message(f"=== STARTING BATCH 35 DISPATCH DAEMON (ACCOUNT 2 ONLY) ===")
    log_message(f"============================================================")
    log_message(f"Session Dir: {session_dir}")
    log_message(f"Queue File: {QUEUE_FILE.name}")
    log_message(f"Dry Run Mode: {dry_run}")

    if not QUEUE_FILE.exists():
        log_message(f"[FATAL] Queue file not found: {QUEUE_FILE}")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    log_message(f"Loaded {len(queue)} items from queue.")

    # Build live deduplication cache
    already_sent_phones = set()
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    if r.get("status") == "SENT":
                        already_sent_phones.add(str(r.get("phone"))[-10:])
        except Exception:
            pass

    if dry_run:
        log_message(f"[DRY RUN] Simulating {len(queue)} messages for Account 2...")
        for q in queue:
            log_message(f"  #{q['serial_no']:02d} -> {q['name']:<25} ({q['clean_phone']}) | Cert: {q['cert_id']:<24} | Score: {q['intent_score']}")
        log_message("[DRY RUN COMPLETE] Ready for live dispatch.")
        return

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
            log_message(f"[*] Account 2: Launching bundled Chromium ({e_ch})...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.on("dialog", lambda d: d.accept())

        log_message(f"[*] Account 2: Navigating to WhatsApp Web home...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=45000)

        # Confirm session is ready
        logged_in = False
        for i in range(15):
            time.sleep(2)
            chat_list = page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header")
            if chat_list:
                logged_in = True
                break
            log_message(f"    ... waiting for WhatsApp session to be ready ({i*2 + 2}s)")

        if not logged_in:
            log_message(f"[FATAL] Account 2 session is not logged in! Halting dispatch.")
            browser.close()
            return

        log_message(f"[OK] Account 2: Confirmed authenticated. Beginning dispatch sequence...")

        consecutive_failures = 0
        success_count = 0
        skip_count = 0
        fail_count = 0

        for idx, item in enumerate(queue, 1):
            phone_10 = str(item["clean_phone"])[-10:]
            if phone_10 in already_sent_phones:
                log_message(f"[{idx:2d}/{len(queue)}] Account 2 | SKIP (Already sent): {item['name']} ({item['clean_phone']})")
                skip_count += 1
                continue

            log_message(f"[{idx:2d}/{len(queue)}] Account 2 | Sending to {item['name']} (+{item['clean_phone']})...")

            success, status = send_whatsapp_single(page, item)

            entry = {
                "account": 2,
                "phone": item["clean_phone"],
                "name": item["name"],
                "email": item["email"],
                "candidate_id": item["candidate_id"],
                "cert_id": item["cert_id"],
                "domain": item["domain"],
                "serial_no": item["serial_no"],
                "type": item["type"],
                "status": "SENT" if success else "FAILED",
                "details": status,
                "timestamp": datetime.now().isoformat()
            }
            record_dispatch(entry)

            if success:
                success_count += 1
                consecutive_failures = 0
                already_sent_phones.add(phone_10)
                log_message(f"   [SUCCESS] Account 2 -> {item['name']} delivered successfully.")
                
                # Randomized human delay between 18.0s and 35.0s
                if idx < len(queue):
                    delay = random.uniform(18.0, 35.0)
                    log_message(f"   ... Waiting {delay:.1f}s human break before next message...")
                    time.sleep(delay)
            else:
                fail_count += 1
                consecutive_failures += 1
                log_message(f"   [FAILED] Account 2 -> {item['name']}: {status}")

                if consecutive_failures >= 3:
                    log_message(f"[CIRCUIT BREAKER] 3 consecutive delivery failures occurred! Halting dispatch.")
                    break

                if idx < len(queue):
                    time.sleep(random.uniform(10.0, 15.0))

        log_message(f"============================================================")
        log_message(f"=== BATCH 35 DISPATCH COMPLETE ===")
        log_message(f"Total Processed: {len(queue)} | Sent: {success_count} | Skipped: {skip_count} | Failed: {fail_count}")
        log_message(f"============================================================")

        try:
            browser.close()
        except Exception:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DBERT Batch 35 WhatsApp Dispatcher")
    parser.add_argument("--dry-run", action="store_true", help="Simulate queue without sending")
    parser.add_argument("--live", action="store_true", help="Execute live dispatch")
    args = parser.parse_args()

    if not args.dry_run and not args.live:
        print("Please specify either --dry-run or --live")
        sys.exit(1)

    run_dispatch(dry_run=args.dry_run)
