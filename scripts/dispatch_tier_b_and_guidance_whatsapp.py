#!/usr/bin/env python3
"""
================================================================================
DBERT Stipend Tier B (3 Candidates) & PR Guidance (4 Candidates) WhatsApp Dispatch
- Sender: Account 2 (.chrome_session_account2) - Verified LOGGED IN
- Anti-ban pacing: 18s - 35s randomized human pause after delivery
- Tracking & Deduplication: data/dbert_whatsapp_sent_today.json & data/whatsapp_tier_b_guidance.log
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

LOG_FILE = DATA_DIR / "whatsapp_tier_b_guidance.log"
SENT_LOG_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"
QUEUE_FILE = DATA_DIR / "whatsapp_tier_b_and_guidance_queue.json"

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

def load_sent_phones():
    if not SENT_LOG_JSON.exists():
        return set()
    try:
        with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data) if isinstance(data, list) else set(data.keys())
    except Exception:
        return set()

def record_sent_phone(phone: str, meta: dict):
    sent_set = set()
    data = {}
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                raw = json.load(f)
                if isinstance(raw, dict):
                    data = raw
                elif isinstance(raw, list):
                    data = {p: {} for p in raw}
        except Exception:
            data = {}
    
    data[phone] = {
        "timestamp": datetime.now().isoformat(),
        "account": "account2",
        "intern_id": meta.get("intern_id"),
        "name": meta.get("name"),
        "type": meta.get("type")
    }
    with open(SENT_LOG_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description="Dispatch Tier B and PR Guidance WhatsApp messages")
    parser.add_argument("--live", action="store_true", help="Execute real sending via Playwright Account 2")
    parser.add_argument("--force", action="store_true", help="Bypass sent_today check")
    args = parser.parse_args()

    if not QUEUE_FILE.exists():
        log_message(f"Queue file {QUEUE_FILE} does not exist!")
        return

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    sent_phones = load_sent_phones()
    pending = []
    for item in queue:
        p = item["phone"].strip()
        if not args.force and p in sent_phones:
            log_message(f"[SKIP] Phone {p} ({item['name']}) already contacted today.")
            continue
        pending.append(item)

    log_message(f"Total candidates in queue: {len(queue)}, Pending dispatch: {len(pending)}")
    if not pending:
        log_message("All candidates already contacted! Exiting cleanly.")
        return

    if not args.live:
        log_message("=== DRY RUN MODE ===")
        for idx, item in enumerate(pending, 1):
            log_message(f"[{idx}/{len(pending)}] Would send to {item['name']} ({item['phone']}) - Type: {item['type']}")
            print(f"Message preview:\n{item['message']}\n" + "-"*50)
        log_message("To send live, run: python scripts/dispatch_tier_b_and_guidance_whatsapp.py --live")
        return

    # LIVE EXECUTION
    log_message("=== LIVE DISPATCH LAUNCHING via Account 2 ===")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_ACC2),
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )
        page = browser.new_page()
        page.goto("https://web.whatsapp.com", wait_until="networkidle", timeout=60000)
        log_message("Waiting for WhatsApp Web main chat interface...")
        page.wait_for_selector("#side", timeout=45000)
        log_message("✓ Account 2 logged in and authenticated!")

        success_count = 0
        for idx, item in enumerate(pending, 1):
            name = item['name']
            phone = item['phone']
            msg = item['message']
            log_message(f"[{idx}/{len(pending)}] Sending to {name} ({phone})...")

            encoded_msg = urllib.parse.quote(msg)
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
            page.goto(url, wait_until="domcontentloaded", timeout=45000)

            # Wait for send button or invalid number alert
            try:
                page.wait_for_selector("button[aria-label='Send'], span[data-icon='send']", timeout=25000)
                time.sleep(2)
                page.click("button[aria-label='Send'], span[data-icon='send']")
                time.sleep(3)
                record_sent_phone(phone, item)
                log_message(f"✓ DELIVERED to {name} ({phone})")
                success_count += 1
            except Exception as e:
                log_message(f"✗ FAILED to send to {name} ({phone}): {e}")

            if idx < len(pending):
                delay = random.randint(18, 32)
                log_message(f"Human pause: {delay}s before next message...")
                time.sleep(delay)

        log_message(f"Batch completed: {success_count}/{len(pending)} sent successfully.")
        browser.close()

if __name__ == "__main__":
    main()
