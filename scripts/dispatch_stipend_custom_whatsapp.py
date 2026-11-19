#!/usr/bin/env python3
"""
================================================================================
DBERT — Custom Stipend Milestone & ₹299 Gate WhatsApp Dispatcher
================================================================================
Dispatches personalized WhatsApp messages to candidates who have added LinkedIn
and need to complete their ₹299 project evaluation to release:
  1. Official 3-doc verified credential packet (Certificate, Evaluation, LOR)
  2. ₹499 Security Caution Deposit refund
  3. ₹5,000 Milestone Stipend disbursement

Constraints:
  - Both Google Form URL & Website ₹299 Payment URL in lines 1-15
  - Warning: ₹499 security deposit and ₹5,000 stipend withheld if not completed
  - Sender: Logged-in Account 2 (.chrome_session_account2)
  - Anti-ban pacing: 18s–35s randomized human breaks
  - Circuit breaker: Halts if 3 consecutive failures occur
================================================================================
"""

import os
import sys
import time
import json
import csv
import random
import sqlite3
import argparse
import urllib.parse
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
SESSION_ACC1 = (
    AIVARA_DIR / ".chrome_session_account1"
    if (AIVARA_DIR / ".chrome_session_account1").exists()
    else PROJECT_ROOT / ".chrome_session_account1"
)
SESSION_ACC2 = (
    AIVARA_DIR / ".chrome_session_account2"
    if (AIVARA_DIR / ".chrome_session_account2").exists()
    else PROJECT_ROOT / ".chrome_session_account2"
)

DB_PATH = DATA_DIR / "dbert_whatsapp.db"
INPUT_QUEUE_JSON = DATA_DIR / "whatsapp_stipend_299_pending.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_stipend_299.csv"

GOOGLE_FORM_URL = (
    "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header"
)


def format_stipend_message(cand: dict) -> str:
    name = (cand.get("name") or "Candidate").strip()
    cert_id = cand.get("cert_id") or ""
    email = (cand.get("email") or "").strip().lower()

    if cert_id:
        verify_url = f"https://dbert.in/verify?certid={cert_id}"
        payment_url = f"https://dbert.in/enroll/1999?certid={cert_id}&fee=299"
    else:
        verify_url = "https://dbert.in/verify"
        payment_url = f"https://dbert.in/enroll/1999?email={email}&fee=299"

    # Strictly adheres to first 15 lines placement
    return (
        f"🎓 *Official DBERT Credential & Stipend Notice*\n"
        f"\n"
        f"Dear {name},\n"
        f"\n"
        f"Congratulations! Your DBERT internship tenure and LinkedIn profile are recorded on LMS.\n"
        f"\n"
        f"🔗 *Direct Verification & Dossier URL:*\n"
        f"👉 {verify_url}\n"
        f"\n"
        f"📝 *Mandatory Claim & Verification Form:*\n"
        f"👉 {GOOGLE_FORM_URL}\n"
        f"\n"
        f"💳 *Instant ₹299 Verification & Payment Link:*\n"
        f"👉 {payment_url}\n"
        f"\n"
        f"⚠️ *IMPORTANT SETTLEMENT NOTICE:*\n"
        f"Completion of the ₹299 official project evaluation is mandatory. Please note that if this verification is not completed, your *₹499 security caution deposit* and your *₹5,000 milestone stipend* will *NOT be released*.\n"
        f"\n"
        f"📌 *Required Action Steps:*\n"
        f"1️⃣ Complete your ₹299 project verification via UPI at: {payment_url}\n"
        f"2️⃣ Confirm your transaction details on the Google Form above.\n"
        f"3️⃣ Your official 3-document credential packet (Certificate, Academic Rubric, LOR) will unlock, and your ₹5,000 milestone stipend will be processed to your verified UPI account.\n"
        f"\n"
        f"Best regards,\n"
        f"*Abhinav Sharma*\n"
        f"Program Head & Project Mentor\n"
        f"*DBERT — Digital Blinc Education Research And Technology*\n"
        f"🌐 https://dbert.in"
    )


def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stipend_dispatch_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_id INTEGER,
            name TEXT,
            email TEXT,
            phone TEXT,
            cert_id TEXT,
            account_used INTEGER,
            status TEXT,
            error_message TEXT,
            sent_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def get_sent_phones():
    if not DB_PATH.exists():
        return set()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT phone FROM stipend_dispatch_log WHERE status = 'SENT'")
    sent = {r[0] for r in cur.fetchall()}
    conn.close()
    return sent


def log_send_result(cand, account_num, status, error_msg=""):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO stipend_dispatch_log (intern_id, name, email, phone, cert_id, account_used, status, error_message, sent_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cand.get("intern_id"),
        cand.get("name"),
        cand.get("email"),
        cand.get("raw_phone") or cand.get("phone"),
        cand.get("cert_id"),
        account_num,
        status,
        error_msg,
        now_iso
    ))
    conn.commit()
    conn.close()


def send_whatsapp_message(page, cand: dict) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    raw_phone = cand.get("raw_phone")
    if not raw_phone:
        p = cand.get("phone", "")
        raw_phone = "".join(c for c in p if c.isdigit())[-10:]

    if not raw_phone or len(raw_phone) < 10:
        return False, "INVALID_PHONE"

    msg = format_stipend_message(cand)
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone=91{raw_phone}&text={encoded_msg}"

    try:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
        except Exception as e_nav:
            if "Target closed" in str(e_nav) or page.is_closed():
                return False, "BROWSER_CLOSED"

        time.sleep(3)

        # Check for invalid phone dialog
        invalid_dialog = page.query_selector(
            "div[data-animate-modal-popup='true'], [data-testid='popup-contents'], div[role='dialog']"
        )
        if invalid_dialog:
            body_text = invalid_dialog.inner_text().lower()
            if "phone number shared via url is invalid" in body_text or "invalid" in body_text:
                ok_btn = page.query_selector("button:has-text('OK'), [data-testid='popup-controls-ok']")
                if ok_btn:
                    try:
                        ok_btn.click()
                    except Exception:
                        pass
                return False, "INVALID_PHONE_NUMBER"

        # Locate send button or compose box
        time.sleep(2)
        send_btn_selectors = [
            "button[aria-label='Send']",
            "span[data-icon='send']",
            "[data-testid='send']",
            "button[data-tab='11']",
        ]

        send_button = None
        for sel in send_btn_selectors:
            try:
                el = page.wait_for_selector(sel, state="visible", timeout=12000)
                if el:
                    send_button = el
                    break
            except Exception:
                continue

        if send_button:
            time.sleep(random.uniform(0.8, 1.5))
            send_button.click()
            time.sleep(random.uniform(2.5, 4.0))
            return True, "SENT"

        # Fallback Enter in message box
        box_selectors = [
            "footer div[contenteditable='true']",
            "div[data-testid='conversation-compose-box-input']",
            "div[role='textbox']",
        ]
        for sel in box_selectors:
            msg_box = page.query_selector(sel)
            if msg_box:
                msg_box.focus()
                time.sleep(0.5)
                page.keyboard.press("Enter")
                time.sleep(3.5)
                return True, "SENT"

        return False, "SEND_BUTTON_NOT_FOUND"

    except Exception as e:
        return False, f"EXCEPTION: {str(e)}"


def run_dispatch(account_num=2, delay_min=18.0, delay_max=35.0, dry_run=False, test_to=None):
    init_db()

    with open(INPUT_QUEUE_JSON, "r", encoding="utf-8") as f:
        queue = json.load(f)

    if test_to:
        clean_target = "".join(c for c in test_to if c.isdigit())[-10:]
        test_cand = {
            "intern_id": 9999,
            "name": "DBERT Test Candidate",
            "email": "test@dbert.in",
            "phone": f"+91{clean_target}",
            "raw_phone": clean_target,
            "domain": "Artificial Intelligence",
            "cert_id": "CERT-DBERT-2026-AIML-001",
        }
        queue = [test_cand]

    sent_phones = get_sent_phones()
    pending = [c for c in queue if (c.get("raw_phone") or c.get("phone", "")[-10:]) not in sent_phones]

    print("\n" + "=" * 76)
    print("      DBERT — STIPEND MILESTONE & ₹299 GATE WHATSAPP DISPATCHER      ")
    print("=" * 76)
    print(f"  Target Candidates Total  : {len(queue)}")
    print(f"  Already Sent Previously   : {len(sent_phones)}")
    print(f"  Pending in This Batch    : {len(pending)}")
    print(f"  Active Sender Account    : Account {account_num} (Session: {SESSION_ACC2})")
    print(f"  Anti-Ban Human Delay     : {delay_min}s – {delay_max}s randomized breaks")
    print("=" * 76 + "\n")

    if dry_run:
        print("[DRY RUN PREVIEW] Showing first 3 messages:\n")
        for i, c in enumerate(pending[:3], 1):
            print(f"--- CANDIDATE {i}: {c['name']} (+91 {c['raw_phone']}) ---")
            print(format_stipend_message(c))
            print("-" * 76 + "\n")
        print(f"[OK] Dry run complete for {len(pending)} pending candidates. Ready for live dispatch.")
        return

    if not pending:
        print("[OK] All candidates have already been dispatched. Queue is empty!")
        return

    from playwright.sync_api import sync_playwright

    session_dir = str(SESSION_ACC2 if account_num == 2 else SESSION_ACC1)
    consecutive_failures = 0
    max_consecutive_failures = 3

    success_count = 0
    fail_count = 0

    with sync_playwright() as p:
        print(f"[*] Launching Chrome for Account {account_num} from {session_dir}...")
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--remote-debugging-port=0",
        ]
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
        except Exception as e_chrome:
            print(f"[*] Native Chrome launch failed ({e_chrome}). Launching bundled Chromium...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()

        print("[*] Navigating to WhatsApp Web...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=45000)

        # Verify login
        logged_in = False
        for _ in range(15):
            if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                logged_in = True
                break
            time.sleep(2)

        if not logged_in:
            print(f"[FATAL] Account {account_num} is not logged in! Please scan QR code first.")
            browser.close()
            return

        print(f"[PASS] Account {account_num} is verified and active! Beginning dispatch...\n")

        for idx, cand in enumerate(pending, start=1):
            cand_name = cand.get("name", "Candidate")
            cand_phone = cand.get("raw_phone") or cand.get("phone", "")[-10:]
            cert = cand.get("cert_id") or "N/A"

            print(f"[{idx}/{len(pending)}] Sending to {cand_name} (+91 {cand_phone}) | Cert: {cert} ...")

            ok, detail = send_whatsapp_message(page, cand)

            if ok:
                success_count += 1
                consecutive_failures = 0
                log_send_result(cand, account_num, "SENT")
                print(f"  >>> [SENT] Successfully delivered to +91 {cand_phone}")
            else:
                fail_count += 1
                consecutive_failures += 1
                log_send_result(cand, account_num, "FAILED", detail)
                print(f"  >>> [FAILED] Could not send to +91 {cand_phone}: {detail}")

                if consecutive_failures >= max_consecutive_failures:
                    print("\n" + "!" * 76)
                    print(f"[CIRCUIT BREAKER] {consecutive_failures} consecutive failures encountered!")
                    print("Pausing dispatch to protect account safety.")
                    print("!" * 76 + "\n")
                    break

            # Pacing delay
            if idx < len(pending):
                delay = random.uniform(delay_min, delay_max)
                print(f"  >>> Human pause: {delay:.1f}s ...\n")
                time.sleep(delay)

        browser.close()

    print("\n" + "=" * 76)
    print("      DISPATCH SESSION COMPLETED      ")
    print(f"  Successfully Sent  : {success_count}")
    print(f"  Failed Deliveries  : {fail_count}")
    print(f"  Database Updated   : {DB_PATH}")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DBERT Stipend Milestone WhatsApp Dispatcher")
    parser.add_argument("--dry-run", action="store_true", help="Preview queue and formatted messages without sending")
    parser.add_argument("--live", action="store_true", help="Execute live dispatch")
    parser.add_argument("--test-to", type=str, help="Send 1 test message to specified phone number")
    parser.add_argument("--account", type=int, default=2, help="Sender account (default: 2)")
    parser.add_argument("--delay-min", type=float, default=18.0, help="Minimum human delay in seconds")
    parser.add_argument("--delay-max", type=float, default=35.0, help="Maximum human delay in seconds")

    args = parser.parse_args()

    if args.dry_run or args.test_to or args.live:
        run_dispatch(
            account_num=args.account,
            delay_min=args.delay_min,
            delay_max=args.delay_max,
            dry_run=args.dry_run,
            test_to=args.test_to
        )
    else:
        print("Please specify --dry-run, --test-to <phone>, or --live to execute.")
