#!/usr/bin/env python3
"""
================================================================================
DBERT Batch 50 Untouched Candidates WhatsApp Dispatch Daemon (Account 1 Only)
================================================================================
- Target Queue: data/whatsapp_299_queue_untouched_50.json (50 Candidates)
- Sender: Account 1 (.chrome_session_account1) - Verified LOGGED IN
- Anti-ban pacing: 18s - 35s randomized human pause after delivery
- Multi-layer deduplication & tracking:
    * data/whatsapp_dispatch_299.log
    * data/dbert_whatsapp_sent_today.json
    * data/dbert_whatsapp.db (whatsapp_sent_log)
    * data/dispatch_tracking_batch50_acc1.csv
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
TRACKING_CSV = DATA_DIR / "dispatch_tracking_batch50_acc1.csv"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"

QUEUE_FILE = DATA_DIR / "whatsapp_299_queue_untouched_50.json"
SESSION_ACC1 = (
    AIVARA_DIR / ".chrome_session_account1"
    if (AIVARA_DIR / ".chrome_session_account1").exists()
    else PROJECT_ROOT / ".chrome_session_account1"
)

def log_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted, flush=True)
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
                "candidate_id": entry.get("cert_id"),
                "name": entry.get("name"),
                "email": entry.get("email"),
                "clean_phone": entry.get("phone"),
                "cert_id": entry.get("cert_id"),
                "domain": entry.get("domain"),
                "status": entry.get("status"),
                "timestamp": entry.get("timestamp"),
                "account": "ACCOUNT_1"
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
                entry.get("cert_id"),
                entry.get("name"),
                entry.get("email"),
                entry.get("phone"),
                entry.get("cert_id"),
                entry.get("domain"),
                "ACCOUNT_1",
                entry.get("timestamp")
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            log_message(f"[WARN] Failed to update SQLite DB: {e}")

def send_whatsapp_single(page, item: dict) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    phone = item["phone"]
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

        # Standalone Continue / OK modal buttons
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

def run_dispatch(dry_run: bool = False, delay_min: int = 18, delay_max: int = 35):
    log_message("=" * 70)
    log_message("=== STARTING DBERT BATCH 50 UNTOUCHED INTERNS DISPATCH (ACC 1) ===")
    log_message("=" * 70)
    log_message(f"Session Dir : {SESSION_ACC1}")
    log_message(f"Queue File  : {QUEUE_FILE.name}")
    log_message(f"Dry Run     : {dry_run}")
    log_message(f"Pacing      : {delay_min}s - {delay_max}s")

    if not QUEUE_FILE.exists():
        log_message(f"[FATAL] Queue file not found: {QUEUE_FILE}")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    log_message(f"Loaded {len(queue)} untouched candidates for Account 1.")

    # Deduplication cache
    already_sent = set()
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    if r.get("status") == "SENT":
                        p = str(r.get("phone", ""))[-10:]
                        if p: already_sent.add(p)
                        c = str(r.get("cert_id", "")).strip()
                        if c: already_sent.add(c)
        except Exception:
            pass

    if dry_run:
        log_message(f"[DRY RUN] Simulating {len(queue)} messages for Account 1:")
        for q in queue:
            log_message(f"  #{q['serial_no']:02d} -> {q['name']:<25} ({q['phone']}) | Cert: {q['cert_id']:<24} | Score: {q['score']}")
        log_message("[DRY RUN COMPLETE] Ready for live dispatch.")
        return

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
    ]

    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_ACC1),
                channel="chrome",
                headless=False,
                args=launch_args,
                viewport={"width": 1280, "height": 800}
            )
        except Exception as e_ch:
            log_message(f"[WARN] Chrome channel error ({e_ch}). Fallback to Chromium...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_ACC1),
                headless=False,
                args=launch_args,
                viewport={"width": 1280, "height": 800}
            )

        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = context.pages[0] if context.pages else context.new_page()

        log_message("[Account 1] Loading WhatsApp Web...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        log_message("[Account 1] Verifying WhatsApp Web authentication...")
        logged_in = False
        for _ in range(60):
            if page.is_closed():
                log_message("[FATAL] Browser window closed during login check.")
                return
            if page.query_selector("[aria-label='Chat list'], #side, #pane-side, [data-testid='chat-list']"):
                logged_in = True
                break
            time.sleep(1)

        if not logged_in:
            log_message("[FATAL] Account 1 is NOT logged in or QR code is waiting. Aborting.")
            context.close()
            return

        log_message("[✓] Account 1 authenticated successfully! Starting dispatch loop.")

        consecutive_failures = 0
        sent_count = 0

        for idx, item in enumerate(queue, 1):
            phone_clean = item["clean_phone"]
            cert_id = item["cert_id"]

            if phone_clean in already_sent or cert_id in already_sent:
                log_message(f"[{idx}/{len(queue)}] [SKIP] Already sent: {item['name']} ({phone_clean})")
                continue

            log_message(f"[{idx}/{len(queue)}] Sending to {item['name']} ({item['phone']}) | Cert: {cert_id} | Score: {item['score']}...")

            success, status_msg = send_whatsapp_single(page, item)
            now_str = datetime.now().isoformat()

            entry = {
                "serial_no": item["serial_no"],
                "name": item["name"],
                "phone": item["clean_phone"],
                "email": item["email"],
                "cert_id": cert_id,
                "domain": item["domain"],
                "score": item["score"],
                "status": status_msg,
                "timestamp": now_str,
                "account": "ACCOUNT_1"
            }

            record_dispatch(entry)

            if success:
                consecutive_failures = 0
                sent_count += 1
                already_sent.add(phone_clean)
                already_sent.add(cert_id)
                delay = random.uniform(delay_min, delay_max)
                log_message(f"  [✓] DELIVERED! Status: {status_msg} | Pausing {delay:.1f}s anti-ban break...")
                time.sleep(delay)
            else:
                consecutive_failures += 1
                log_message(f"  [✗] FAILED! Reason: {status_msg} (Failures in a row: {consecutive_failures})")
                time.sleep(5)

            if consecutive_failures >= 3:
                log_message("[CIRCUIT BREAKER] 3 consecutive failures encountered on Account 1. Halting dispatch.")
                break

        log_message("=" * 70)
        log_message("=== DISPATCH COMPLETE FOR BATCH 50 UNTOUCHED INTERNS ===")
        log_message(f"Total Sent: {sent_count}/{len(queue)}")
        log_message("=" * 70)
        context.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DBERT Batch 50 Untouched Interns WhatsApp Dispatcher")
    parser.add_argument("--dry-run", action="store_true", help="Simulate queue without sending")
    parser.add_argument("--live", action="store_true", help="Execute real live sending")
    parser.add_argument("--delay-min", type=int, default=18, help="Minimum pause seconds")
    parser.add_argument("--delay-max", type=int, default=35, help="Maximum pause seconds")
    args = parser.parse_args()

    if not args.live and not args.dry_run:
        print("[!] Specify either --dry-run or --live. Defaulting to --dry-run for safety.")
        args.dry_run = True

    run_dispatch(dry_run=args.dry_run, delay_min=args.delay_min, delay_max=args.delay_max)
