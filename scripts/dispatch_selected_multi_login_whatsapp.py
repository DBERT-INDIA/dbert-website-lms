#!/usr/bin/env python3
"""
================================================================================
DBERT Multi-Login Selected Cohort WhatsApp Dispatch Daemon (Account 2 Only)
- Queue: data/whatsapp_selected_multi_login_queue.json (9 Candidates)
- Sender: Account 2 (.chrome_session_account2) - Verified LOGGED IN
- Anti-ban pacing: 18s - 35s randomized human pause after delivery
- Multi-layer deduplication & tracking:
  * data/whatsapp_dispatch_selected_multi_login.log
  * data/dbert_whatsapp_sent_today.json
  * data/dbert_whatsapp.db (whatsapp_sent_log)
  * data/dispatch_tracking_selected_multi_login.csv
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

LOG_FILE = DATA_DIR / "whatsapp_dispatch_selected_multi_login.log"
SENT_LOG_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_selected_multi_login.csv"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"

QUEUE_FILE = DATA_DIR / "whatsapp_selected_multi_login_queue.json"
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

def init_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS whatsapp_sent_log (
                phone TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                account TEXT,
                status TEXT,
                sent_at TEXT,
                details TEXT
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        log_message(f"[DB Warning] init_db: {e}")

def record_delivery_all_stores(cand: dict, status: str, details: str = ""):
    now_iso = datetime.now().isoformat()
    phone = cand.get("phone", "")
    name = cand.get("name", "")
    email = cand.get("email", "")

    # 1. Update SQLite
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO whatsapp_sent_log (phone, name, email, account, status, sent_at, details)
            VALUES (?, ?, ?, 'Account 2', ?, ?, ?)
        """, (phone, name, email, status, now_iso, details))
        conn.commit()
        conn.close()
    except Exception as e:
        log_message(f"[DB Error] record_delivery_all_stores: {e}")

    # 2. Update SENT_LOG_JSON
    try:
        sent_entries = []
        if SENT_LOG_JSON.exists():
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                sent_entries = json.load(f)
        sent_entries.append({
            "phone": phone,
            "name": name,
            "email": email,
            "account": "Account 2",
            "campaign": "selected_multi_login_offer",
            "status": status,
            "timestamp": now_iso,
            "details": details
        })
        with open(SENT_LOG_JSON, "w", encoding="utf-8") as f:
            json.dump(sent_entries, f, indent=2)
    except Exception as e:
        log_message(f"[JSON Error] record_delivery_all_stores: {e}")

    # 3. Update CSV
    try:
        file_exists = TRACKING_CSV.exists()
        with open(TRACKING_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "app_id", "name", "phone", "email", "domain", "offer_id", "status", "details"])
            writer.writerow([
                now_iso,
                cand.get("app_id", ""),
                name,
                phone,
                email,
                cand.get("domain", ""),
                cand.get("offer_letter_id", ""),
                status,
                details
            ])
    except Exception as e:
        log_message(f"[CSV Error] record_delivery_all_stores: {e}")

def check_login(page) -> bool:
    log_message("Checking WhatsApp Web login state for Account 2...")
    try:
        page.goto("https://web.whatsapp.com", timeout=60000, wait_until="domcontentloaded")
    except Exception as e:
        log_message(f"[WARN] Error loading web.whatsapp.com: {e}")

    for sec in range(45):
        if page.query_selector('canvas[aria-label="Scan this QR code to use WhatsApp Web"]') or page.query_selector('div[data-ref]'):
            log_message("[FATAL] Account 2 session has expired or requires QR scan!")
            return False
        if page.query_selector('div[contenteditable="true"][data-tab="3"]') or \
           page.query_selector('#side') or \
           page.query_selector('header[data-testid="chatlist-header"]') or \
           page.query_selector('div[aria-label="Chat list"]'):
            log_message("[SUCCESS] Account 2 is authenticated and ready.")
            return True
        time.sleep(1)

    log_message("[WARN] Timed out waiting for chatlist. Inspecting current DOM...")
    page.screenshot(path=str(DATA_DIR / "whatsapp_acc2_status.png"))
    return False

def send_single_message(page, phone: str, message: str) -> tuple[bool, str]:
    encoded_text = urllib.parse.quote(message)
    target_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_text}"
    
    try:
        page.goto(target_url, timeout=45000, wait_until="domcontentloaded")
    except Exception as e:
        return False, f"NAV_ERROR: {e}"

    sent = False
    for attempt in range(35):
        dialogs = page.query_selector_all('div[role="dialog"], div[data-animate-modal-body="true"]')
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
    log_message("============================================================")
    log_message("=== STARTING MULTI-LOGIN SELECTED DISPATCH (ACCOUNT 2) ===")
    log_message("============================================================")
    log_message(f"Session Dir: {session_dir}")
    log_message(f"Queue File: {QUEUE_FILE.name}")
    log_message(f"Dry Run Mode: {dry_run}")

    if not QUEUE_FILE.exists():
        log_message(f"[FATAL] Queue file not found: {QUEUE_FILE}")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    log_message(f"Loaded {len(queue)} items from queue.")

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
        log_message("=== DRY RUN PREVIEW ===")
        for i, cand in enumerate(queue, 1):
            p10 = str(cand.get("phone"))[-10:]
            status_prev = "ALREADY_SENT" if p10 in already_sent_phones else "PENDING_DELIVERY"
            log_message(f"[{i}/{len(queue)}] {cand['name']} | {cand['phone']} | {cand['domain']} | {status_prev}")
            log_message(f"Offer ID: {cand.get('offer_letter_id')}")
            lines = cand['message'].split('\n')
            log_message(f"Line 8: {lines[7]}")
            log_message(f"Line 11: {lines[10]}")
            log_message("-" * 50)
        log_message("Dry run finished successfully. No messages were dispatched.")
        return

    init_db()

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
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

        if not check_login(page):
            log_message("[FATAL] WhatsApp Web login check failed. Aborting dispatch.")
            browser.close()
            return

        consecutive_failures = 0
        sent_count = 0
        fail_count = 0
        skip_count = 0

        for i, cand in enumerate(queue, 1):
            phone = cand["phone"]
            name = cand["name"]
            p10 = str(phone)[-10:]

            if p10 in already_sent_phones:
                log_message(f"[{i}/{len(queue)}] SKIP: {name} ({phone}) already contacted today.")
                skip_count += 1
                continue

            log_message(f"[{i}/{len(queue)}] Dispatching to: {name} ({phone}) | Domain: {cand.get('domain')}...")
            success, result_detail = send_single_message(page, phone, cand["message"])

            if success:
                consecutive_failures = 0
                sent_count += 1
                already_sent_phones.add(p10)
                record_delivery_all_stores(cand, "SENT", "Delivered via Account 2")
                log_message(f"[{i}/{len(queue)}] SUCCESS -> Delivered to {name} ({phone})")
                
                # Human Anti-ban delay: 18s - 35s
                if i < len(queue):
                    pause = random.randint(18, 35)
                    log_message(f"Pacing cooldown: sleeping {pause}s...")
                    time.sleep(pause)
            else:
                consecutive_failures += 1
                fail_count += 1
                record_delivery_all_stores(cand, "FAILED", result_detail)
                log_message(f"[{i}/{len(queue)}] FAILED -> {name} ({phone}) Reason: {result_detail}")

                if consecutive_failures >= 3:
                    log_message("[CIRCUIT BREAKER] 3 consecutive failures encountered! Halting dispatch.")
                    page.screenshot(path=str(DATA_DIR / "whatsapp_acc2_circuit_breaker.png"))
                    break

        log_message("============================================================")
        log_message(f"=== DISPATCH SUMMARY ===")
        log_message(f"Total: {len(queue)} | Sent: {sent_count} | Failed: {fail_count} | Skipped: {skip_count}")
        log_message("============================================================")

        try:
            browser.close()
        except Exception:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DBERT Multi-Login Selected WhatsApp Dispatch Daemon")
    parser.add_argument("--dry-run", action="store_true", help="Preview queue and exit without sending")
    parser.add_argument("--live", action="store_true", help="Execute live dispatch")
    args = parser.parse_args()

    if not args.live and not args.dry_run:
        print("Please specify --live or --dry-run.")
        sys.exit(1)

    run_dispatch(dry_run=args.dry_run)
