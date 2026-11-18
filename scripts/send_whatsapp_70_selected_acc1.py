#!/usr/bin/env python3
"""
================================================================================
DBERT — WhatsApp Dispatch: Account 1 Dedicated Worker (34 Candidates)
================================================================================
Dedicated worker for Account 1 (+91 81929 11360) running in parallel with Account 2.
Logs deliveries to data/whatsapp_70_selected_sent_log_acc1.json to prevent race conditions.
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
MASTER_LOG_FILE = DATA_DIR / "whatsapp_70_selected_sent_log.json"
ACC1_LOG_FILE = DATA_DIR / "whatsapp_70_selected_sent_log_acc1.json"

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
SESSION_ACC1 = (
    AIVARA_DIR / ".chrome_session_account1"
    if (AIVARA_DIR / ".chrome_session_account1").exists()
    else ROOT_DIR / ".chrome_session_account1"
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

def load_acc1_sent_log() -> dict:
    sent = {}
    if MASTER_LOG_FILE.exists():
        try:
            with open(MASTER_LOG_FILE, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    if r.get("status") == "SENT":
                        sent[r["email"].lower()] = r
        except Exception:
            pass
    if ACC1_LOG_FILE.exists():
        try:
            with open(ACC1_LOG_FILE, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    sent[r["email"].lower()] = r
        except Exception:
            pass
    return sent

def save_acc1_record(record: dict):
    current = load_acc1_sent_log()
    current[record["email"].lower()] = record
    with open(ACC1_LOG_FILE, "w", encoding="utf-8") as f:
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

def main():
    parser = argparse.ArgumentParser(description="Account 1 WhatsApp Dispatcher")
    parser.add_argument("--live", action="store_true", help="Launch live dispatch")
    args = parser.parse_args()

    with open(COHORT_FILE, "r", encoding="utf-8") as f:
        candidates = json.load(f)

    # Shard: Account 1 gets odd indices (0, 2, 4...)
    acc1_candidates = [c for idx, c in enumerate(candidates) if idx % 2 == 0]

    sent_map = load_acc1_sent_log()
    pending = [c for c in acc1_candidates if sent_map.get(c["email"].lower(), {}).get("status") != "SENT"]

    print("=" * 76)
    print(f"  ACCOUNT 1 DISPATCH WORKER (+91 81929 11360)")
    print(f"  Allocated: {len(acc1_candidates)} | Already Sent: {len(acc1_candidates) - len(pending)} | Pending: {len(pending)}")
    print("=" * 76)

    if not args.live:
        print("[!] Safety check: Run with --live to dispatch.")
        return

    session_dir = str(SESSION_ACC1)
    acc_phone = "+91 81929 11360"

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
            print(f"[*] Chrome fallback: {e}")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()

        print("[*] Loading WhatsApp Web on Account 1...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)
        time.sleep(6)

        # Pre-flight check
        body_text = page.inner_text("body")
        if "Scan to log in" in body_text or "Link with phone number" in body_text:
            print("[!] ERROR: Account 1 is NOT logged in. Aborting.")
            browser.close()
            return

        print("[OK] Account 1 confirmed LOGGED IN and active.")

        success_count = 0
        fail_count = 0

        for idx, cand in enumerate(pending, 1):
            name = cand['name']
            email = cand['email']
            phone = clean_phone(cand.get('phone', ''))

            print(f"\n[Acc 1] [{idx}/{len(pending)}] Dispatching -> {name} ({phone}) <{email}>...")
            success, reason = send_whatsapp_single(page, cand)

            if success:
                success_count += 1
                print(f"[Acc 1] [SUCCESS] Delivered to {name} ({phone})")
                save_acc1_record({
                    "id": cand.get("id"),
                    "email": email,
                    "name": name,
                    "phone": phone,
                    "domain": cand.get("domain", ""),
                    "status": "SENT",
                    "account": 1,
                    "account_phone": acc_phone,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                fail_count += 1
                print(f"[Acc 1] [FAILED] {name} ({phone}) -> {reason}")
                save_acc1_record({
                    "id": cand.get("id"),
                    "email": email,
                    "name": name,
                    "phone": phone,
                    "domain": cand.get("domain", ""),
                    "status": "FAILED",
                    "reason": reason,
                    "account": 1,
                    "account_phone": acc_phone,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })

            if idx < len(pending):
                delay = round(random.uniform(18.0, 32.0), 2)
                print(f"[Acc 1] Pacing delay: {delay}s...")
                time.sleep(delay)

        time.sleep(3)
        browser.close()
        print(f"\n[OK] Account 1 completed: {success_count} sent, {fail_count} failed.")

if __name__ == "__main__":
    main()
