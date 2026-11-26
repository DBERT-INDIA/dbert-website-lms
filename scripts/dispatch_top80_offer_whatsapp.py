#!/usr/bin/env python3
"""
DBERT Top-80 Selected Cohort Offer Letter & Group Invite WhatsApp Dispatcher
- Queue: data/top80_offer_queue_nov26.json (80 candidates)
- Account 1 (.chrome_session_account1): Odd serials (40 candidates)
- Account 2 (.chrome_session_account2): Even serials (40 candidates)
- Pacing: 18s - 35s randomized human pause; circuit breaker at 3 consecutive failures.
"""

import sys
import time
import json
import csv
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
QUEUE_FILE = DATA_DIR / "top80_offer_queue_nov26.json"
TRACKING_CSV = DATA_DIR / "whatsapp_dispatch_top80_nov26.csv"
LOG_FILE = DATA_DIR / "whatsapp_dispatch_top80_nov26.log"
GROUP_URL = "https://chat.whatsapp.com/Kn6o6hMoFfc7rIVx0wgZt3"


def log_msg(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_sent_phones() -> set[str]:
    sent = set()
    if TRACKING_CSV.exists():
        with open(TRACKING_CSV, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("status") == "SENT" and row.get("phone"):
                    sent.add(row["phone"].strip())
    return sent


def record_status(cand: dict, account_label: str, status: str, details: str = ""):
    file_exists = TRACKING_CSV.exists()
    with open(TRACKING_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["timestamp", "serial", "account", "phone", "name", "email", "domain", "offer_letter_id", "status", "details"],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "serial": cand["serial"],
            "account": account_label,
            "phone": cand["phone"],
            "name": cand["name"],
            "email": cand["email"],
            "domain": cand["domain"],
            "offer_letter_id": cand["offer_letter_id"],
            "status": status,
            "details": details,
        })


def build_message(cand: dict) -> str:
    name = cand["name"]
    domain = cand["domain"]
    email = cand["email"]
    offer_id = cand["offer_letter_id"]
    tenure = cand.get("tenure_months", 3)
    stipend = cand.get("stipend_amount", 5000)
    hours = cand.get("login_hours_per_week", 10)
    b_start = cand.get("batch_start_date", "2026-12-01")
    b_end = cand.get("batch_end_date", "2027-02-28")

    return (
        f"Hi {name},\n\n"
        f"Congratulations! Your DBERT Internship Application has been *APPROVED (Selected)* for *{domain}*.\n"
        f"Offer ID: *{offer_id}*\n\n"
        f"*1. View & Sign Your Offer Letter:*\n"
        f"https://lms.dbert.in/portal/offer\n"
        f"(Log in with your registered email: {email})\n\n"
        f"*2. Join the Official Interns WhatsApp Group:*\n"
        f"{GROUP_URL}\n\n"
        f"*Internship Terms Summary:*\n"
        f"- *Domain:* {domain}\n"
        f"- *Tenure:* {tenure} Months ({b_start} to {b_end})\n"
        f"- *Stipend:* Rs.{stipend}/month (milestone-linked)\n"
        f"- *Remote Login Hours:* {hours} hrs/week (flexible remote)\n\n"
        f"*How to Complete Your Enrollment:*\n"
        f"1) Open https://lms.dbert.in/portal/offer and review all offer terms\n"
        f"2) Digitally sign the Offer Letter\n"
        f"3) Complete enrollment (Rs.499 refundable caution deposit) to unlock your batch & tasks\n"
        f"4) Join the WhatsApp group above for onboarding updates.\n\n"
        f"Need help? Reply here or contact DBERT Admissions."
    )


def send_whatsapp_message(page, phone: str, text: str) -> tuple[bool, str]:
    encoded = urllib.parse.quote(text)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
        for _ in range(30):
            # Invalid number popup
            invalid = page.locator("div[data-animate-modal-popup='true']:has-text('invalid'), div:has-text('Phone number shared via url is invalid')").first
            if invalid.count() > 0 and invalid.is_visible():
                return False, "Invalid WhatsApp number"

            send_btn = page.locator("button[aria-label='Send'], span[data-icon='send'], span[data-icon='wds-ic-send-filled']").first
            if send_btn.count() > 0 and send_btn.is_visible():
                time.sleep(random.uniform(0.8, 1.5))
                send_btn.click()
                time.sleep(random.uniform(2.0, 3.5))
                return True, "Delivered"

            time.sleep(1.5)
        return False, "Timed out waiting for Send button"
    except Exception as e:
        return False, str(e)[:180]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=int, choices=[1, 2], required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    mine = [c for c in queue if (c["serial"] % 2 == 1 if args.account == 1 else c["serial"] % 2 == 0)]
    already_sent = load_sent_phones()
    pending = [c for c in mine if c["phone"] not in already_sent]

    acc_label = f"Account {args.account}"
    session_dir = str(PROJECT_ROOT / (".chrome_session_account1" if args.account == 1 else ".chrome_session_account2"))
    log_msg(f"[{acc_label}] Loaded {len(mine)} assigned, {len(pending)} pending (session={session_dir})")

    if args.dry_run:
        if pending:
            print("\n--- SAMPLE MESSAGE ---")
            print(build_message(pending[0]))
            print("--- END SAMPLE ---")
        return

    if not pending:
        log_msg(f"[{acc_label}] Nothing pending.")
        return

    consecutive_failures = 0
    sent_count = 0
    failed_count = 0

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=False,
            ignore_default_args=["--enable-automation"],
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox", "--disable-infobars"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=45000)

        logged_in = False
        for _ in range(20):
            time.sleep(2)
            if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                logged_in = True
                break
        if not logged_in:
            log_msg(f"[{acc_label}] ERROR: Not logged in! Aborting.")
            ctx.close()
            sys.exit(1)

        for idx, cand in enumerate(pending, 1):
            msg = build_message(cand)
            ok, details = send_whatsapp_message(page, cand["phone"], msg)
            if ok:
                sent_count += 1
                consecutive_failures = 0
                record_status(cand, acc_label, "SENT", details)
                log_msg(f"[{acc_label}] ({idx}/{len(pending)}) SENT -> {cand['name']} ({cand['phone']})")
            else:
                failed_count += 1
                consecutive_failures += 1
                record_status(cand, acc_label, "FAILED", details)
                log_msg(f"[{acc_label}] ({idx}/{len(pending)}) FAILED -> {cand['name']} ({cand['phone']}): {details}")
                if consecutive_failures >= 3:
                    log_msg(f"[{acc_label}] CIRCUIT BREAKER TRIGGERED (3 consecutive failures). Stopping.")
                    break

            if idx < len(pending):
                pause = random.uniform(18, 35)
                time.sleep(pause)

        ctx.close()

    log_msg(f"[{acc_label}] Finished: sent={sent_count}, failed={failed_count}")


if __name__ == "__main__":
    main()
