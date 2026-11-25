#!/usr/bin/env python3
"""
================================================================================
DBERT Batch 35 (Wave 1) Single-Account WhatsApp Dispatch Daemon
- Target Queue: data/whatsapp_299_queue_batch35_live.json (35 Candidates)
- Sender: Single Account (.chrome_session_account2 default or --account 1)
- Pacing: 18s - 32s randomized human delay
- Multi-layer tracking & deduplication:
  * data/whatsapp_dispatch_299.log
  * data/dbert_whatsapp_sent_today.json
  * data/dispatch_tracking_batch35_wave1.csv
  * data/dbert_whatsapp.db (whatsapp_sent_log)
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

QUEUE_FILE = DATA_DIR / "whatsapp_299_queue_batch35_live.json"
LOG_FILE = DATA_DIR / "whatsapp_dispatch_299.log"
SENT_LOG_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_batch35_wave1.csv"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

def log_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def record_dispatch(entry: dict, account_name: str):
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

    # 2. Update Tracking CSV
    file_exists = TRACKING_CSV.exists()
    fieldnames = [
        "serial_no", "candidate_id", "name", "email", "clean_phone",
        "cert_id", "domain", "status", "timestamp", "account"
    ]
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
                "account": account_name
            })
    except Exception as e:
        log_message(f"[WARN] Failed to write to CSV: {e}")

    # 3. Update SQLite
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
                account_name.upper(),
                entry.get("timestamp")
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            log_message(f"[WARN] Failed to write to SQLite: {e}")

def wait_for_chat_ui(page, max_wait: int = 300):
    log_message(f"Checking WhatsApp Web authentication (waiting up to {max_wait}s for QR scan / chat UI)...")
    ticks = max_wait // 2
    for i in range(ticks):
        if page.is_closed():
            return False
        
        # Check if chat UI loaded (any recognized pane/header)
        chat_pane = page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header, div[role='textbox']")
        if chat_pane:
            log_message("✓ WhatsApp Web authenticated successfully! Chat interface is active.")
            return True
        
        # Check if QR code is visible
        if i % 5 == 0:
            remaining = max_wait - i * 2
            log_message(f"Waiting for QR code scan... ({remaining}s remaining). Please scan in the opened browser window.")
        time.sleep(2)
    return False

def send_single_message(page, phone: str, text: str):
    encoded_text = urllib.parse.quote(text)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_text}"
    
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e_nav:
        if "closed" in str(e_nav).lower():
            return False, f"BROWSER_CLOSED: {e_nav}"

    sent = False
    for attempt in range(25):
        if page.is_closed():
            return False, "PAGE_CLOSED"

        try:
            # Check for invalid phone popup
            dialogs = page.query_selector_all("div[role='dialog'], div[data-animate-modal-popup='true']")
            starting_chat = False
            for d in dialogs:
                try:
                    txt = d.inner_text().lower()
                    if any(term in txt for term in ["invalid", "not on whatsapp", "url is invalid", "couldn't find"]):
                        btn = d.query_selector("button")
                        if btn: btn.click()
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
        except Exception as e_step:
            if "closed" in str(e_step).lower():
                return False, "PAGE_CLOSED"
            time.sleep(1)
            continue

        time.sleep(1)

    if not sent:
        return False, "TIMEOUT_SEND_NOT_COMPLETED"

    return True, "SENT"

def main():
    parser = argparse.ArgumentParser(description="DBERT Batch 35 Single-Account WhatsApp Dispatch")
    parser.add_argument("--account", type=int, default=2, choices=[1, 2], help="WhatsApp account to use (default: 2)")
    parser.add_argument("--dry-run", action="store_true", help="Print messages without sending")
    parser.add_argument("--live", action="store_true", help="Execute live WhatsApp dispatch")
    parser.add_argument("--limit", type=int, default=35, help="Number of messages to send (default: 35)")
    parser.add_argument("--wait-auth", type=int, default=300, help="Seconds to wait for QR authentication (default: 300)")
    args = parser.parse_args()

    session_dir = AIVARA_DIR / f".chrome_session_account{args.account}"
    account_name = f"account{args.account}"

    if not QUEUE_FILE.exists():
        log_message(f"Queue file {QUEUE_FILE} not found!")
        sys.exit(1)

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    queue = queue[:args.limit]
    log_message("=" * 70)
    log_message(f"DBERT BATCH 35 (WAVE 1) SINGLE-ACCOUNT DISPATCH")
    log_message(f"Selected Account : {account_name.upper()} ({session_dir})")
    log_message(f"Target Count     : {len(queue)} candidates")
    log_message(f"Mode             : {'DRY RUN' if not args.live else 'LIVE DISPATCH'}")
    log_message("=" * 70)

    if not args.live or args.dry_run:
        log_message("=== DRY RUN PREVIEW (FIRST 3 CANDIDATES) ===")
        for idx, item in enumerate(queue[:3], 1):
            log_message(f"[{idx}/{len(queue)}] To: {item['name']} ({item['phone']}) - Track: {item['domain']}")
            print(f"Message:\n{item['message']}\n" + "-"*50)
        log_message(f"Dry run complete for {len(queue)} items.")
        log_message("To send live, execute with --live flag.")
        return

    # Deduplication cache
    already_sent_phones = set()
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    if r.get("status") == "SENT":
                        already_sent_phones.add(str(r.get("phone"))[-10:])
        except Exception:
            pass

    # LIVE DISPATCH
    log_message("[INIT] Launching Playwright browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ],
            user_agent=USER_AGENT
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        try:
            page.goto("https://web.whatsapp.com", wait_until="commit", timeout=90000)
        except Exception as e_initial:
            log_message(f"[WARN] Initial goto notice: {e_initial}")

        # Authenticate
        is_ready = wait_for_chat_ui(page, max_wait=args.wait_auth)
        if not is_ready:
            log_message("[FATAL] WhatsApp Web was not authenticated in time. Aborting dispatch.")
            browser.close()
            sys.exit(1)

        sent_count = 0
        failed_count = 0
        skip_count = 0
        consecutive_failures = 0

        for idx, item in enumerate(queue, 1):
            phone = str(item["phone"]).strip()
            name = item["name"]
            msg = item["message"]

            if phone[-10:] in already_sent_phones:
                log_message(f"[{idx}/{len(queue)}] [SKIP] {name} (+{phone}) already received message today.")
                skip_count += 1
                continue

            log_message(f"\n[{idx}/{len(queue)}] Dispatching to {name} (+{phone})...")
            success, reason = send_single_message(page, phone, msg)

            now_ts = datetime.now().isoformat()
            record_entry = {
                "serial_no": idx,
                "candidate_id": item.get("candidate_id", f"WAVE1-{idx:03d}"),
                "name": name,
                "email": item.get("email"),
                "phone": phone,
                "cert_id": item.get("cert_id"),
                "domain": item.get("domain"),
                "status": "SENT" if success else "FAILED",
                "reason": reason,
                "timestamp": now_ts,
                "account": account_name
            }
            record_dispatch(record_entry, account_name)

            if success:
                sent_count += 1
                consecutive_failures = 0
                already_sent_phones.add(phone[-10:])
                log_message(f"  ✓ SUCCESS ({sent_count}/{len(queue)}) - Message delivered to {name}")
                delay = random.uniform(18.0, 32.0)
                log_message(f"  [HUMAN BREAK] Pausing {delay:.1f}s before next contact...")
                time.sleep(delay)
            else:
                failed_count += 1
                consecutive_failures += 1
                log_message(f"  ✗ FAILED ({reason}) - To: {name} (+{phone})")
                if consecutive_failures >= 3:
                    log_message("[CIRCUIT BREAKER] 3 consecutive delivery failures! Halting dispatch to protect session.")
                    break
                time.sleep(5)

        log_message("=" * 70)
        log_message(f"DISPATCH RUN COMPLETE")
        log_message(f"Total Sent   : {sent_count}")
        log_message(f"Total Skipped: {skip_count}")
        log_message(f"Total Failed : {failed_count}")
        log_message("=" * 70)
        browser.close()

if __name__ == "__main__":
    main()
