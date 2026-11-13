#!/usr/bin/env python3
"""
scripts/send_rejected_payments_whatsapp.py
================================================================================
DBERT — Rejected Payments WhatsApp Notification Dispatcher
================================================================================
Dispatches official WhatsApp resubmission notices to candidates whose payment
receipts (₹499 deposit or ₹1,500 balance) were rejected, providing explicit
guidelines and direct resubmission links.

Features:
- Reads from data/rejected_payments_whatsapp_queue.json
- Dual-Account distribution:
    * Account 1: Odd records (.chrome_session_account1)
    * Account 2: Even records (.chrome_session_account2)
- Human pacing: 18s - 32s randomized delays
- Deduplication & atomic tracking in data/rejected_payments_whatsapp_tracking.json
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

QUEUE_FILE = DATA_DIR / "rejected_payments_whatsapp_queue.json"
TRACKING_FILE = DATA_DIR / "rejected_payments_whatsapp_tracking.json"
TRACKING_CSV = DATA_DIR / "rejected_payments_whatsapp_tracking.csv"
LOG_FILE = DATA_DIR / "rejected_payments_whatsapp_dispatch.log"

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
            return {}
    return {}


def save_tracking(tracking: dict):
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump(tracking, f, indent=2, ensure_ascii=False)

    rows = list(tracking.values())
    if rows:
        fieldnames = ["key", "type", "name", "phone", "email", "status", "sent_at", "account_used", "error"]
        with open(TRACKING_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)


def load_queue(account: int = None) -> list:
    if not QUEUE_FILE.exists():
        log_message(f"Queue file missing: {QUEUE_FILE}")
        return []
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    if account == 1:
        return [item for idx, item in enumerate(queue) if idx % 2 == 0]
    elif account == 2:
        return [item for idx, item in enumerate(queue) if idx % 2 != 0]
    return queue


def send_whatsapp_messages(account: int, headless: bool = False, delay: float = 20.0, dry_run: bool = False):
    from playwright.sync_api import sync_playwright

    session_path = SESSION_ACC1 if account == 1 else SESSION_ACC2
    log_message(f"Starting WhatsApp Dispatcher for Account {account}")
    log_message(f"Session path: {session_path}")

    queue = load_queue(account=account)
    tracking = load_tracking()
    log_message(f"Total candidates in Account {account} queue: {len(queue)}")

    if dry_run:
        print("\n" + "=" * 80)
        print(f"DRY RUN: WHATSAPP ACCOUNT {account} PREVIEW ({len(queue)} recipients)")
        print("=" * 80)
        for idx, item in enumerate(queue, 1):
            key = f"{item['type']}_{item['email']}"
            status = tracking.get(key, {}).get("status", "PENDING")
            print(f"\n[{idx}/{len(queue)}] {item['name']} | Phone: +{item['phone']} | Status: {status}")
            print(f"Resubmit URL: {item['resubmit_url']}")
            print("Message:")
            print(item["message"][:200] + "...")
        print("\n" + "=" * 80)
        return

    # Check session
    if not session_path.exists():
        log_message(f"ERROR: Session directory does not exist: {session_path}")
        return

    sent_count = 0
    skip_count = 0
    fail_count = 0
    consecutive_fails = 0

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(session_path),
            headless=headless,
            viewport={"width": 1280, "height": 800},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
        )

        page = context.new_page()
        log_message("Navigating to web.whatsapp.com to verify active session...")
        page.goto("https://web.whatsapp.com", wait_until="networkidle", timeout=60000)

        # Wait for chat list or search bar
        try:
            page.wait_for_selector(
                "div[contenteditable='true'][data-tab='3'], div[aria-label='Chat list']",
                timeout=30000,
            )
            log_message("WhatsApp Web session active and ready!")
        except Exception:
            log_message("WARNING: Chat list not detected within 30s. Checking for QR code...")
            qr = page.query_selector("canvas[aria-label='Scan this QR code to link a device']")
            if qr:
                log_message("CRITICAL: QR Code detected. Session is logged out! Please log in first.")
                context.close()
                return

        for idx, item in enumerate(queue, 1):
            key = f"{item['type']}_{item['email']}"
            if key in tracking and tracking[key].get("status") == "SENT":
                log_message(f"[{idx}/{len(queue)}] SKIP (Already sent): {item['name']} (+{item['phone']})")
                skip_count += 1
                continue

            phone = item["phone"]
            message_text = item["message"]
            encoded_text = urllib.parse.quote(message_text)
            send_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_text}"

            log_message(f"[{idx}/{len(queue)}] Navigating to chat for {item['name']} (+{phone})...")

            try:
                page.goto(send_url, wait_until="networkidle", timeout=45000)

                # Look for send button or invalid number popup
                send_button_selector = (
                    "button[aria-label='Send'], span[data-icon='send'], button[data-testid='compose-btn-send']"
                )
                invalid_popup_selector = (
                    "div[data-animate-modal-body='true']:has-text('Phone number shared via url is invalid')"
                )

                # Wait for send button or invalid modal
                for _ in range(25):
                    if page.query_selector(send_button_selector):
                        break
                    if page.query_selector(invalid_popup_selector):
                        break
                    time.sleep(1)

                if page.query_selector(invalid_popup_selector):
                    log_message(f"[{idx}/{len(queue)}] FAILED: Phone number +{phone} is not on WhatsApp.")
                    tracking[key] = {
                        "key": key,
                        "type": item["type"],
                        "name": item["name"],
                        "phone": phone,
                        "email": item["email"],
                        "status": "INVALID_PHONE",
                        "sent_at": None,
                        "account_used": f"Account_{account}",
                        "error": "Phone number not registered on WhatsApp",
                    }
                    save_tracking(tracking)
                    fail_count += 1
                    consecutive_fails += 1
                    continue

                send_btn = page.query_selector(send_button_selector)
                if send_btn:
                    time.sleep(random.uniform(1.0, 2.5))
                    send_btn.click()
                    time.sleep(2.0)

                    log_message(f"[{idx}/{len(queue)}] SUCCESS: WhatsApp sent to {item['name']} (+{phone})")
                    sent_count += 1
                    consecutive_fails = 0

                    tracking[key] = {
                        "key": key,
                        "type": item["type"],
                        "name": item["name"],
                        "phone": phone,
                        "email": item["email"],
                        "status": "SENT",
                        "sent_at": datetime.now().isoformat(),
                        "account_used": f"Account_{account}",
                        "error": None,
                    }
                    save_tracking(tracking)
                else:
                    raise Exception("Send button did not appear within timeout")

            except Exception as e:
                log_message(f"[{idx}/{len(queue)}] ERROR sending to {item['name']} (+{phone}): {e}")
                tracking[key] = {
                    "key": key,
                    "type": item["type"],
                    "name": item["name"],
                    "phone": phone,
                    "email": item["email"],
                    "status": "FAILED",
                    "sent_at": None,
                    "account_used": f"Account_{account}",
                    "error": str(e),
                }
                save_tracking(tracking)
                fail_count += 1
                consecutive_fails += 1

            if consecutive_fails >= 3:
                log_message("CIRCUIT BREAKER: 3 consecutive failures. Pausing worker for safety.")
                break

            if idx < len(queue):
                cooldown = delay + random.uniform(2.0, 7.0)
                log_message(f"Human pacing cooldown: sleeping {cooldown:.1f}s...")
                time.sleep(cooldown)

        context.close()
        log_message(
            f"Account {account} Finished: Sent={sent_count}, Skipped={skip_count}, Failed={fail_count}, Total={len(queue)}"
        )


def main():
    parser = argparse.ArgumentParser(description="DBERT Rejected Payments WhatsApp Outreach")
    parser.add_argument("--account", type=int, choices=[1, 2], default=1, help="Which WhatsApp account to run (1 or 2)")
    parser.add_argument("--all", action="store_true", help="Run both accounts sequentially")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--delay", type=float, default=20.0, help="Base delay between messages")
    parser.add_argument("--dry-run", action="store_true", help="Preview recipients without sending")
    parser.add_argument("--status", action="store_true", help="Show current campaign status")
    args = parser.parse_args()

    if args.status:
        tracking = load_tracking()
        sent = sum(1 for v in tracking.values() if v.get("status") == "SENT")
        failed = sum(1 for v in tracking.values() if v.get("status") in ("FAILED", "INVALID_PHONE"))
        print(f"Rejected Payments WhatsApp Status: Sent={sent}, Failed={failed}, Total Tracked={len(tracking)}")
        return

    if args.all:
        send_whatsapp_messages(account=1, headless=args.headless, delay=args.delay, dry_run=args.dry_run)
        send_whatsapp_messages(account=2, headless=args.headless, delay=args.delay, dry_run=args.dry_run)
    else:
        send_whatsapp_messages(account=args.account, headless=args.headless, delay=args.delay, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
