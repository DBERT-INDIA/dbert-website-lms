#!/usr/bin/env python3
"""
DBERT Selected Multi-Login (Last 10 Days, Unpaid ₹499) WhatsApp Dispatcher
- Queue: data/whatsapp_selected_10d_unpaid_queue.json (32 Candidates)
- Uses the logged-in WhatsApp Web session (.chrome_session_account2 / .chrome_session_account1)
- Anti-ban pacing: 18s - 35s randomized pause after each delivery
- Circuit breaker: Halts if 3 consecutive failures occur
- Deduplication: data/dispatch_tracking_selected_10d_unpaid.csv & data/dbert_whatsapp_sent_today.json
"""

import argparse
import csv
import json
import random
import sqlite3
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")
DATA_DIR = PROJECT_ROOT / "data"
AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")

QUEUE_FILE = DATA_DIR / "whatsapp_selected_10d_unpaid_queue.json"
LOG_FILE = DATA_DIR / "whatsapp_dispatch_selected_10d_unpaid.log"
SENT_LOG_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_selected_10d_unpaid.csv"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"


def resolve_session_dir(account: int) -> Path:
    name = f".chrome_session_account{account}"
    if (AIVARA_DIR / name).exists():
        return AIVARA_DIR / name
    return PROJECT_ROOT / name


def log_message(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def build_message(cand: dict) -> str:
    first_name = (cand.get("name") or "Candidate").strip().split()[0]
    domain = cand.get("domain") or "AI & Software Engineering"
    return (
        f"Hi {first_name}, congratulations on being *Selected* for the DBERT Internship Cohort! 🎉\n"
        f"\n"
        f"We noticed you logged into the LMS multiple times recently (Domain: *{domain}*), but haven't completed your seat confirmation yet.\n"
        f"\n"
        f"🔗 *Get Your Offer Letter & Confirm Seat:*\n"
        f"https://lms.dbert.in/portal/offer\n"
        f"\n"
        f"🔗 *Verify DBERT Credentials:*\n"
        f"https://dbert.in/verify\n"
        f"\n"
        f"*Key Internship Details:*\n"
        f"• *Domain:* {domain}\n"
        f"• *Tenure:* 2 Months (8 Weeks) from your selected Monday batch start date (+ 5-day grace window)\n"
        f"• *Stipend & Rewards:* Performance-indexed ₹5,000 milestone stipend (5,000 coins on /stipend/tasks after meeting sprint & credential gates)\n"
        f"• *How to Get Your Offer Letter:*\n"
        f"  1. Log in at https://lms.dbert.in/portal/offer\n"
        f"  2. Review & digitally sign your Offer Letter\n"
        f"  3. Select your Monday batch start date & submit the ₹499 refundable caution deposit (refunded upon milestone clearance)\n"
        f"\n"
        f"Need help? Reply here or message Admissions at +91 81929 11360."
    )


def load_already_sent_campaign() -> set[str]:
    sent = set()
    if TRACKING_CSV.exists():
        try:
            with open(TRACKING_CSV, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if row.get("status") == "SENT":
                        sent.add((row.get("phone") or "").strip())
        except Exception:
            pass
    return sent


def record_delivery(cand: dict, account_label: str, status: str, details: str = ""):
    now_iso = datetime.now().isoformat()
    phone = cand.get("phone", "")
    name = cand.get("name", "")
    email = cand.get("email", "")

    # 1. CSV
    file_exists = TRACKING_CSV.exists()
    with open(TRACKING_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["timestamp", "app_id", "name", "email", "phone", "domain", "account", "status", "details"])
        w.writerow([now_iso, cand.get("app_id"), name, email, phone, cand.get("domain"), account_label, status, details])

    # 2. JSON log
    try:
        entries = json.loads(SENT_LOG_JSON.read_text(encoding="utf-8")) if SENT_LOG_JSON.exists() else []
        entries.append({
            "phone": phone,
            "name": name,
            "email": email,
            "account": account_label,
            "campaign": "selected_10d_unpaid",
            "status": status,
            "timestamp": now_iso,
            "details": details,
        })
        SENT_LOG_JSON.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    except Exception as e:
        log_message(f"[JSON Error] {e}")

    # 3. SQLite whatsapp_sent_log
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR REPLACE INTO whatsapp_sent_log (phone, name, email, account, status, sent_at, details) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (phone, name, email, account_label, status, now_iso, details),
        )
        conn.commit()
        conn.close()
    except Exception as e:
        log_message(f"[DB Error] {e}")


def check_login(page, label: str, wait_qr_seconds: int = 120) -> bool:
    log_message(f"Checking WhatsApp Web login state for {label}...")
    page.goto("https://web.whatsapp.com", timeout=60000, wait_until="domcontentloaded")
    for sec in range(wait_qr_seconds):
        if (
            page.query_selector('div[contenteditable="true"][data-tab="3"]')
            or page.query_selector("#side")
            or page.query_selector('header[data-testid="chatlist-header"]')
            or page.query_selector('div[aria-label="Chat list"]')
        ):
            log_message(f"[SUCCESS] {label} is authenticated and ready.")
            return True
        if sec == 5 and (page.query_selector('canvas[aria-label="Scan this QR code to use WhatsApp Web"]') or page.query_selector("div[data-ref]")):
            log_message(f"[ACTION REQUIRED] {label} needs QR scan in the open Chromium window (waiting up to {wait_qr_seconds}s)...")
        time.sleep(1)
    log_message(f"[FATAL] {label} timed out waiting for WhatsApp Web login.")
    return False


def send_single(page, phone: str, message: str) -> tuple[bool, str]:
    encoded = urllib.parse.quote(message)
    page.goto(f"https://web.whatsapp.com/send?phone={phone}&text={encoded}", timeout=45000, wait_until="domcontentloaded")

    for _ in range(40):
        for d in page.query_selector_all('div[role="dialog"], div[data-animate-modal-body="true"]'):
            try:
                txt = d.inner_text().lower()
                if any(k in txt for k in ("invalid", "not on whatsapp", "url is invalid", "couldn't find")):
                    btn = d.query_selector("button")
                    if btn:
                        btn.click()
                    return False, "NOT_ON_WHATSAPP"
                if any(k in txt for k in ("what's new", "calling is now available", "update", "privacy")):
                    btn = d.query_selector("button")
                    if btn:
                        btn.click()
                        time.sleep(1)
            except Exception:
                pass

        send_btn = page.query_selector(
            'button[aria-label="Send"], button[data-testid="send"], button[data-testid="compose-btn-send"], span[data-icon="send"]'
        )
        if send_btn:
            try:
                time.sleep(1)
                tag = page.evaluate("(el) => el.tagName.toLowerCase()", send_btn)
                if tag != "button":
                    page.evaluate_handle("(el) => el.closest('button') || el", send_btn).click()
                else:
                    send_btn.click()
                time.sleep(3)
                return True, "SENT"
            except Exception:
                pass

        box = page.query_selector('footer div[contenteditable="true"], div[role="textbox"], div[contenteditable="true"][data-tab="10"]')
        if box:
            try:
                if box.inner_text().strip():
                    box.focus()
                    time.sleep(0.5)
                    page.keyboard.press("Enter")
                    time.sleep(3)
                    return True, "SENT"
            except Exception:
                pass
        time.sleep(1)

    return False, "TIMEOUT_SEND_NOT_COMPLETED"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--account", type=int, default=2, choices=[1, 2])
    parser.add_argument("--wait-qr", type=int, default=120)
    args = parser.parse_args()

    queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    already_sent = load_already_sent_campaign()
    pending = [c for c in queue if c["phone"] not in already_sent]

    log_message(f"Loaded {len(queue)} total candidates; {len(already_sent)} already sent; {len(pending)} pending.")

    if args.dry_run:
        if pending:
            sample = build_message(pending[0])
            lines = sample.splitlines()
            print("\n--- SAMPLE MESSAGE (First 15 Lines Check) ---")
            for idx, ln in enumerate(lines[:15], 1):
                print(f"{idx:02d}: {ln}")
            print(f"Total lines: {len(lines)}")
        return

    if not pending:
        log_message("Nothing pending to send.")
        return

    session_dir = resolve_session_dir(args.account)
    label = f"Account {args.account}"
    log_message(f"Launching Playwright with session: {session_dir}")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"],
            viewport={"width": 1280, "height": 850},
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        if not check_login(page, label, wait_qr_seconds=args.wait_qr):
            ctx.close()
            sys.exit(2)

        consec_failures = 0
        sent_count = 0
        for idx, cand in enumerate(pending, 1):
            msg = build_message(cand)
            log_message(f"[{idx}/{len(pending)}] Sending to {cand['name']} ({cand['phone']}) [{cand['domain']}]...")
            ok, status = send_single(page, cand["phone"], msg)
            record_delivery(cand, label, "SENT" if ok else "FAILED", status)
            if ok:
                sent_count += 1
                consec_failures = 0
                log_message(f"  -> SENT ({sent_count}/{len(pending)})")
            else:
                consec_failures += 1
                log_message(f"  -> FAILED: {status} (consec={consec_failures})")
                if consec_failures >= 3:
                    log_message("[CIRCUIT BREAKER] 3 consecutive failures. Halting dispatch.")
                    break
            if idx < len(pending):
                delay = random.randint(18, 35)
                log_message(f"  -> Sleeping {delay}s...")
                time.sleep(delay)

        ctx.close()
        log_message(f"Dispatch complete. Sent={sent_count}/{len(pending)}")


if __name__ == "__main__":
    main()
