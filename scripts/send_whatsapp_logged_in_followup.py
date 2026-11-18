#!/usr/bin/env python3
"""
================================================================================
DBERT — WhatsApp Concierge Outreach to Logged-in Unpaid Candidates
================================================================================
Dispatches personalized WhatsApp messages to candidates who logged into the
portal today following their email notification, offering 1-on-1 concierge
assistance before the 05:00 PM IST kickoff.

Dual Accounts:
  - Account 1 (Odd Candidates): .chrome_session_account1 (+91 81929 11360)
  - Account 2 (Even Candidates): .chrome_session_account2 (+91 89580 06294)

Usage:
  # Dry-run inspection:
  python scripts/send_whatsapp_logged_in_followup.py --dry-run

  # Launch live dispatch:
  python scripts/send_whatsapp_logged_in_followup.py --live
================================================================================
"""

import os
import sys
import re
import json
import time
import random
import urllib.parse
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

COHORT_FILE = DATA_DIR / "whatsapp_followup_logged_in_unpaid.json"
SENT_LOG_FILE = DATA_DIR / "whatsapp_followup_sent_log.json"

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
SESSION_ACC1 = (
    AIVARA_DIR / ".chrome_session_account1"
    if (AIVARA_DIR / ".chrome_session_account1").exists()
    else ROOT_DIR / ".chrome_session_account1"
)
SESSION_ACC2 = (
    AIVARA_DIR / ".chrome_session_account2"
    if (AIVARA_DIR / ".chrome_session_account2").exists()
    else ROOT_DIR / ".chrome_session_account2"
)

def clean_phone(raw_phone: str) -> str:
    if not raw_phone:
        return ""
    digits = re.sub(r"\D", "", str(raw_phone))
    if digits.startswith("91") and len(digits) == 12:
        return digits
    if len(digits) == 10:
        return f"91{digits}"
    if len(digits) > 10 and digits.startswith("0"):
        digits = digits.lstrip("0")
        if len(digits) == 10:
            return f"91{digits}"
    return digits

def format_message(cand: dict) -> str:
    name = (cand.get("name") or "there").strip()
    domain = (cand.get("domain") or "Applied Engineering").strip()

    # Compliance: Line 8 has direct offer link (within first 15 lines)
    msg = f"""Hello {name},

This is Admissions & Student Concierge from DBERT Technical Council.

We noticed that you logged into your candidate portal today following your appointment notice for the {domain} Fellowship.

We wanted to check in personally — are you encountering any issues reviewing your Letter of Offer or completing the ₹499 caution deposit reconciliation?

👉 Direct Offer Link:
https://lms.dbert.in/portal/offer

⚡ Batch Kickoff Reminder:
Our live Batch Orientation Kickoff begins today at 05:00 PM IST (in ~3 hours). We want to ensure your engineering cloud workspace and LMS access are fully active before the session starts.

How we can help you right now:
1. Direct UPI: If your app is having issues, you can transfer ₹499 directly to our merchant VPA: Q652429146@ybl (DBERT Admissions).
2. Instant WhatsApp Confirmation: If already paid, simply reply to this message with your 12-digit UTR or payment screenshot, and we will verify and activate your seat immediately.
3. Questions on terms or schedule: Feel free to ask any questions right here.

Are you available for today's 05:00 PM IST orientation?

Warm regards,
DBERT Admissions Desk
Digital Blinc Education Research and Technology (dbert.in)"""
    return msg

def load_sent_log() -> dict:
    if not SENT_LOG_FILE.exists():
        return {}
    try:
        with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {r["email"].lower(): r for r in data}
    except Exception:
        return {}

def save_sent_record(record: dict):
    current = load_sent_log()
    current[record["email"].lower()] = record
    with open(SENT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(list(current.values()), f, indent=2, ensure_ascii=False)

def send_whatsapp_single(page, cand: dict) -> tuple:
    raw_phone = cand.get("phone", "")
    phone = clean_phone(raw_phone)
    if not phone or len(phone) < 12:
        return False, f"INVALID_PHONE ({raw_phone})"

    msg = format_message(cand)
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
    except Exception as e:
        if "closed" in str(e).lower():
            return False, "BROWSER_CLOSED"

    t_start = time.time()
    sent = False

    while time.time() - t_start < 40:
        if page.is_closed():
            return False, "BROWSER_CLOSED"

        # Check for invalid phone popup dialog
        dialogs = page.query_selector_all("[role='dialog']")
        for d in dialogs:
            try:
                txt = d.inner_text().lower()
                if any(k in txt for k in ["invalid", "not on whatsapp", "couldn't find"]):
                    btn = d.query_selector("button")
                    if btn: btn.click()
                    return False, "PHONE_NOT_ON_WHATSAPP"
            except Exception:
                pass

        # Check send button
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
                time.sleep(2)
                sent = True
                break
            except Exception:
                pass

        # Try Enter in chat input
        chat_input = page.query_selector('footer div[contenteditable="true"], div[role="textbox"]')
        if chat_input:
            try:
                text_content = chat_input.inner_text().strip()
                if text_content:
                    chat_input.focus()
                    time.sleep(0.5)
                    page.keyboard.press("Enter")
                    time.sleep(2)
                    sent = True
                    break
            except Exception:
                pass

        time.sleep(1)

    return sent, "SENT" if sent else "TIMEOUT"

def process_queue_for_account(acc_num: int, candidates: list):
    session_dir = str(SESSION_ACC1 if acc_num == 1 else SESSION_ACC2)
    acc_phone = "+91 81929 11360" if acc_num == 1 else "+91 89580 06294"

    print("\n" + "=" * 76)
    print(f"  LAUNCHING DISPATCH WORKER: ACCOUNT {acc_num} ({acc_phone})")
    print(f"  Queue Size: {len(candidates)} candidates | Session: {session_dir}")
    print("=" * 76)

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
    ]

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
        except Exception as e:
            print(f"[*] Chrome failed ({e}). Using Chromium...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()

        # Check login
        print(f"[*] Loading WhatsApp Web on Account {acc_num}...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)
        time.sleep(5)

        for idx, cand in enumerate(candidates, 1):
            name = cand['name']
            email = cand['email']
            phone = clean_phone(cand.get('phone', ''))

            print(f"\n[{acc_num}] [{idx}/{len(candidates)}] Sending -> {name} ({phone}) <{email}>...")
            success, reason = send_whatsapp_single(page, cand)

            if success:
                print(f"[{acc_num}] [SUCCESS] Delivered to {name} ({phone})")
                save_sent_record({
                    "email": email,
                    "name": name,
                    "phone": phone,
                    "domain": cand.get("domain", ""),
                    "status": "SENT",
                    "account": acc_num,
                    "account_phone": acc_phone,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                print(f"[{acc_num}] [FAILED] {name} ({phone}) -> {reason}")
                save_sent_record({
                    "email": email,
                    "name": name,
                    "phone": phone,
                    "domain": cand.get("domain", ""),
                    "status": "FAILED",
                    "reason": reason,
                    "account": acc_num,
                    "account_phone": acc_phone,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })

            if idx < len(candidates):
                delay = round(random.uniform(18.0, 32.0), 2)
                print(f"[{acc_num}] Human anti-ban pacing: sleeping {delay}s...")
                time.sleep(delay)

        time.sleep(3)
        browser.close()
        print(f"\n[OK] Worker for Account {acc_num} completed all assigned candidates.")

def main():
    parser = argparse.ArgumentParser(description="DBERT WhatsApp Follow-up to Logged-in Unpaid Candidates")
    parser.add_argument("--dry-run", action="store_true", help="Preview message content and queue distribution")
    parser.add_argument("--live", action="store_true", help="Execute live WhatsApp dispatch")
    args = parser.parse_args()

    if not COHORT_FILE.exists():
        print(f"Error: Cohort file not found at {COHORT_FILE}")
        sys.exit(1)

    with open(COHORT_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    # Filter already sent
    sent_map = load_sent_log()
    pending = [c for c in candidates if sent_map.get(c["email"].lower(), {}).get("status") != "SENT"]

    print(f"Loaded {len(candidates)} total candidates.")
    print(f"Already sent: {len(candidates) - len(pending)} | Pending: {len(pending)}")

    # Shard: Odd indexes -> Account 1, Even indexes -> Account 2
    q1 = []
    q2 = []
    for idx, c in enumerate(pending):
        if idx % 2 == 0:
            q1.append(c)
        else:
            q2.append(c)

    print(f"\nQueue Sharding:")
    print(f"  Account 1 (+91 81929 11360): {len(q1)} candidates")
    print(f"  Account 2 (+91 89580 06294): {len(q2)} candidates")

    if args.dry_run:
        print("\n=== SAMPLE WHATSAPP MESSAGE PREVIEW ===")
        if pending:
            print(format_message(pending[0]))
        print("\n[DRY RUN COMPLETE] Zero messages sent. Run with --live to dispatch.")
        return

    if not args.live:
        print("\nSafety Confirmation: Run with --live to start dispatch.")
        return

    # Execute sequentially: Account 1, then Account 2
    if q1:
        process_queue_for_account(1, q1)
    if q2:
        process_queue_for_account(2, q2)

    print("\n==============================================================================")
    print("  ALL WHATSAPP FOLLOW-UP OUTREACH SESSIONS COMPLETE!")
    print("==============================================================================")

if __name__ == "__main__":
    main()
