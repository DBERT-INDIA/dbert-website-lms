#!/usr/bin/env python3
"""
================================================================================
DBERT — WhatsApp Dispatch: 70 Selected Unpaid Candidates (Google Form CTA)
================================================================================
Dispatches personalized WhatsApp messages to the last 70 selected interns
who have not yet completed their ₹499 caution deposit reconciliation, informing
them that their batch starts today (05:00 PM IST) and directing them to complete
their submission on the official Google Form.

Strict Constraints:
  - Form URL MUST appear within the first 15 lines.
  - Dual accounts:
      * Account 1 (+91 81929 11360): 35 candidates
      * Account 2 (+91 89580 06294): 35 candidates
  - Anti-ban pacing: 18.0s - 32.0s randomized delay between messages.
  - Idempotent tracking: data/whatsapp_70_selected_sent_log.json.

Usage:
  python scripts/send_whatsapp_70_selected_google_form.py --dry-run
  python scripts/send_whatsapp_70_selected_google_form.py --live
  python scripts/send_whatsapp_70_selected_google_form.py --live --account 2
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

COHORT_FILE = DATA_DIR / "whatsapp_last_70_selected_unpaid.json"
SENT_LOG_FILE = DATA_DIR / "whatsapp_70_selected_sent_log.json"

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

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdFxi9bft4POk4b3eXmp4aH71LmeQrJ0WzXA1bsIm37MalSIw/viewform?usp=header"

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

    # Constraint Check: GOOGLE_FORM_URL is strictly on Line 10 (within first 15 lines)
    lines = [
        f"Hello {name},",
        "",
        f"Congratulations on your selection for the DBERT {domain} Fellowship!",
        "",
        "⚡ URGENT: Your Batch Orientation Kickoff begins TODAY at 05:00 PM IST.",
        "",
        "To confirm your seat, activate your LMS engineering workspace, and receive your live meeting credentials, please complete your ₹499 caution deposit reconciliation on the official form:",
        "",
        "👉 Official Registration & Payment Form:",
        GOOGLE_FORM_URL,
        "",
        "(The ₹499 caution deposit is 100% refundable upon milestone completion as per institutional terms.)",
        "",
        "You can also view your official Letter of Offer anytime at:",
        "https://lms.dbert.in/portal/offer",
        "",
        "Merchant UPI VPA for direct transfer: Q652429146@ybl (DBERT Admissions)",
        "If you have already made the transfer, simply reply to this message with your 12-digit UTR number or payment screenshot for instant activation.",
        "",
        "See you at 05:00 PM IST!",
        "",
        "Warm regards,",
        "DBERT Admissions Desk",
        "Digital Blinc Education Research and Technology (dbert.in)"
    ]
    return "\n".join(lines)

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

        # Check for invalid phone dialog
        dialogs = page.query_selector_all("[role='dialog']")
        for d in dialogs:
            try:
                txt = d.inner_text().lower()
                if any(k in txt for k in ["invalid", "not on whatsapp", "couldn't find"]):
                    btn = d.query_selector("button")
                    if btn:
                        btn.click()
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

        # Try Enter in chat input if text is staged
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
            print(f"[*] Chrome launch fallback ({e}). Using Chromium engine...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()

        print(f"[*] Loading WhatsApp Web on Account {acc_num}...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)

        # Pre-flight Authentication Check
        body_text = page.inner_text("body")
        if "Scan to log in" in body_text or "Link with phone number" in body_text:
            print(f"\n[!] ALERT: Account {acc_num} ({acc_phone}) is NOT logged in (QR code detected)!")
            print(f"[!] Skipping Account {acc_num} to prevent queue timeouts.")
            print(f"[!] Run login_whatsapp_account{acc_num}.bat to log in.")
            browser.close()
            return False

        print(f"[OK] Account {acc_num} verified LOGGED IN and active.")

        success_count = 0
        fail_count = 0

        for idx, cand in enumerate(candidates, 1):
            name = cand['name']
            email = cand['email']
            phone = clean_phone(cand.get('phone', ''))

            print(f"\n[Acc {acc_num}] [{idx}/{len(candidates)}] Dispatching -> {name} ({phone}) <{email}>...")
            success, reason = send_whatsapp_single(page, cand)

            if success:
                success_count += 1
                print(f"[Acc {acc_num}] [SUCCESS] Delivered to {name} ({phone})")
                save_sent_record({
                    "id": cand.get("id"),
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
                fail_count += 1
                print(f"[Acc {acc_num}] [FAILED] {name} ({phone}) -> {reason}")
                save_sent_record({
                    "id": cand.get("id"),
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
                print(f"[Acc {acc_num}] Pacing delay: {delay}s...")
                time.sleep(delay)

        time.sleep(3)
        browser.close()
        print(f"\n[OK] Worker for Account {acc_num} completed: {success_count} sent, {fail_count} failed.")
        return True

def main():
    parser = argparse.ArgumentParser(description="DBERT WhatsApp Dispatch to 70 Selected Unpaid Candidates")
    parser.add_argument("--dry-run", action="store_true", help="Preview message content, line count, and queue split")
    parser.add_argument("--live", action="store_true", help="Execute live WhatsApp dispatch")
    parser.add_argument("--account", type=int, choices=[1, 2], help="Run only specific account (1 or 2)")
    args = parser.parse_args()

    if not COHORT_FILE.exists():
        print(f"Error: Cohort file not found at {COHORT_FILE}")
        sys.exit(1)

    with open(COHORT_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    # Filter out already sent
    sent_map = load_sent_log()
    pending = [c for c in candidates if sent_map.get(c["email"].lower(), {}).get("status") != "SENT"]

    print(f"Loaded {len(candidates)} candidates from cohort.")
    print(f"Already sent: {len(candidates) - len(pending)} | Pending: {len(pending)}")

    # Shard into Account 1 (odd index) and Account 2 (even index)
    q1 = []
    q2 = []
    for idx, c in enumerate(candidates):
        # Only assign if pending
        if sent_map.get(c["email"].lower(), {}).get("status") == "SENT":
            continue
        if idx % 2 == 0:
            q1.append(c)
        else:
            q2.append(c)

    print(f"\nPending Queue Allocation:")
    print(f"  Account 1 (+91 81929 11360): {len(q1)} candidates")
    print(f"  Account 2 (+91 89580 06294): {len(q2)} candidates")

    # Template Line Validation
    sample_cand = candidates[0]
    sample_msg = format_message(sample_cand)
    lines = sample_msg.split("\n")
    form_line_idx = None
    for i, line in enumerate(lines, 1):
        if GOOGLE_FORM_URL in line:
            form_line_idx = i
            break

    print(f"\nTemplate Validation:")
    print(f"  Total Lines: {len(lines)}")
    print(f"  Google Form URL Position: Line {form_line_idx} (Constraint: <= 15 -> {'PASSED' if form_line_idx and form_line_idx <= 15 else 'FAILED'})")

    if args.dry_run:
        print("\n=== SAMPLE WHATSAPP MESSAGE PREVIEW ===")
        for i, line in enumerate(lines, 1):
            prefix = f"{i:2d} | "
            if GOOGLE_FORM_URL in line:
                prefix = f"{i:2d} | >>> "
            print(f"{prefix}{line}")
        print("\n[DRY RUN COMPLETE] Zero messages sent. Run with --live to dispatch.")
        return

    if not args.live:
        print("\nSafety Confirmation: Run with --live to start dispatch.")
        return

    # Execute
    if args.account:
        if args.account == 1 and q1:
            process_queue_for_account(1, q1)
        elif args.account == 2 and q2:
            process_queue_for_account(2, q2)
    else:
        if q1:
            process_queue_for_account(1, q1)
        if q2:
            process_queue_for_account(2, q2)

    # Final summary
    final_sent = load_sent_log()
    success_total = sum(1 for c in candidates if final_sent.get(c["email"].lower(), {}).get("status") == "SENT")
    fail_total = sum(1 for c in candidates if final_sent.get(c["email"].lower(), {}).get("status") == "FAILED")
    print("\n" + "=" * 76)
    print(f"  DISPATCH MISSION REPORT: 70 SELECTED CANDIDATES")
    print(f"  Total Candidates: {len(candidates)}")
    print(f"  Successfully Delivered: {success_total}")
    print(f"  Failed / Invalid: {fail_total}")
    print(f"  Audit Log: {SENT_LOG_FILE}")
    print("=" * 76)

if __name__ == "__main__":
    main()
