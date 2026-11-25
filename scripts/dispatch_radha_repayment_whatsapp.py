#!/usr/bin/env python3
"""
scripts/dispatch_radha_repayment_whatsapp.py
Dispatches official ₹299 verification fee repayment request to Radha Bhamodkar via WhatsApp Account 1.
"""

import sys
import os
import time
import json
import csv
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
TRACKING_CSV = DATA_DIR / "dispatch_tracking_radha_repayment.csv"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"

SESSION_ACC1 = (
    AIVARA_DIR / ".chrome_session_account1"
    if (AIVARA_DIR / ".chrome_session_account1").exists()
    else PROJECT_ROOT / ".chrome_session_account1"
)

CANDIDATE = {
    "name": "Radha Bhamodkar",
    "phone": "917385955836",
    "raw_phone": "7385955836",
    "email": "radhabhamodkar@gmail.com",
    "cert_id": "CERT-DBERT-2026-DA-019",
    "domain": "Data Analyst",
    "utr_failed": "956584485560",
    "candidate_id": "4979"
}

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def build_message(cand: dict) -> str:
    msg = (
        f"Official Notice: DBERT Project Credential Verification Audit\n"
        f"Candidate: {cand['name']} ({cand['cert_id']})\n"
        f"\n"
        f"Dear Radha,\n"
        f"\n"
        f"During our regular reconciliation of banking records against the verification ledger, your previously submitted transaction reference (UTR: {cand['utr_failed']}) for the ₹299 project verification fee could not be verified in our banking ledger.\n"
        f"\n"
        f"Repayment & Unlock Portal:\n"
        f"https://dbert.in/verify/unlock?certid={cand['cert_id']}\n"
        f"\n"
        f"Official Payment Details:\n"
        f"• Amount Payable: ₹299\n"
        f"• Official Merchant UPI ID: Q652429146@ybl (DBERT Admissions)\n"
        f"• Payee Name: DBERT Admissions\n"
        f"\n"
        f"To ensure your official credentials remain valid and to release Gate 1 stipend disbursement, repayment of the ₹299 verification fee is required.\n"
        f"\n"
        f"After completing the payment of ₹299, please submit your updated 12-digit UPI UTR on the portal link above or reply directly to this message with your payment receipt screenshot.\n"
        f"\n"
        f"Once verified, your official 3-document credential dossier (Certificate of Completion, Academic Evaluation Rubric, and Letter of Recommendation) will be fully reinstated on the public registry.\n"
        f"\n"
        f"DBERT Admissions & Verification Secretariat\n"
        f"Digital Blinc Education Research and Technology\n"
        f"Support: +91 81929 11360 | https://dbert.in"
    )
    return msg

def record_dispatch(entry: dict):
    # 1. JSON
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
        log(f"[WARN] Failed to write to {SENT_LOG_JSON.name}: {e}")

    # 2. Tracking CSV
    file_exists = TRACKING_CSV.exists()
    fieldnames = ["candidate_id", "name", "email", "phone", "cert_id", "domain", "status", "timestamp", "account"]
    try:
        with open(TRACKING_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "candidate_id": entry.get("candidate_id"),
                "name": entry.get("name"),
                "email": entry.get("email"),
                "phone": entry.get("phone"),
                "cert_id": entry.get("cert_id"),
                "domain": entry.get("domain"),
                "status": entry.get("status"),
                "timestamp": entry.get("timestamp"),
                "account": "ACCOUNT_1"
            })
    except Exception as e:
        log(f"[WARN] Failed to write CSV: {e}")

    # 3. SQLite DB
    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO whatsapp_sent_log 
                (candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.get("candidate_id"),
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
            log("Logged dispatch to SQLite whatsapp_sent_log.")
        except Exception as e:
            log(f"[WARN] Failed to log to SQLite: {e}")

def send_whatsapp(page, cand: dict, msg: str) -> bool:
    phone = cand["phone"]
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

    log(f"Navigating to chat for {cand['name']} ({phone})...")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e_nav:
        if "closed" in str(e_nav).lower():
            log(f"Browser closed: {e_nav}")
            return False

    t_start = time.time()
    sent = False

    while time.time() - t_start < 45:
        if page.is_closed():
            log("Browser was closed.")
            return False

        try:
            # Check for invalid phone dialog
            dialogs = page.query_selector_all("[role='dialog']")
            for d in dialogs:
                try:
                    txt = d.inner_text().lower()
                    if any(term in txt for term in ["invalid", "not on whatsapp", "url is invalid", "couldn't find"]):
                        btn = d.query_selector("button")
                        if btn: btn.click()
                        log("[ERROR] Phone number not on WhatsApp.")
                        return False
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

            # Send button selectors
            send_btn = (
                page.query_selector("button[aria-label='Send']") or
                page.query_selector("span[data-icon='send']") or
                page.query_selector("button[data-tab='11']")
            )
            if send_btn:
                try:
                    send_btn.click()
                    log("Clicked Send button!")
                    time.sleep(4)
                    sent = True
                    break
                except Exception as e_click:
                    log(f"Click attempt note: {e_click}")

            # Fallback: Enter key
            inp = page.query_selector("div[contenteditable='true'][data-tab='10']") or page.query_selector("div[contenteditable='true']")
            if inp:
                try:
                    inp_text = inp.inner_text().strip()
                    if len(inp_text) > 10:
                        inp.press("Enter")
                        log("Pressed Enter in input box!")
                        time.sleep(4)
                        sent = True
                        break
                except Exception:
                    pass

        except Exception as e_poll:
            time.sleep(1)
            continue

        time.sleep(1)

    return sent

def main():
    parser = argparse.ArgumentParser(description="DBERT Radha Repayment WhatsApp Dispatcher")
    parser.add_argument("--live", action="store_true", help="Execute live message sending")
    parser.add_argument("--dry-run", action="store_true", help="Print message and validate configuration")
    args = parser.parse_args()

    msg = build_message(CANDIDATE)
    lines = msg.split("\n")
    log(f"Message length: {len(msg)} chars, {len(lines)} lines")

    if not args.live or args.dry_run:
        log("\n[DRY-RUN] Live dispatch not specified. Run with --live to dispatch.")
        return

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
    ]

    log("\n[LIVE] Launching WhatsApp Playwright Persistent Context with Account 1...")
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_ACC1),
                channel="chrome",
                headless=False,
                args=launch_args,
                viewport={"width": 1280, "height": 850}
            )
        except Exception as e_ch:
            log(f"[WARN] Chrome channel error ({e_ch}). Fallback to Chromium...")
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(SESSION_ACC1),
                headless=False,
                args=launch_args,
                viewport={"width": 1280, "height": 850}
            )

        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = context.pages[0] if context.pages else context.new_page()

        log("Loading WhatsApp Web...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        log("Verifying WhatsApp Web authentication...")
        logged_in = False
        for _ in range(60):
            if page.is_closed():
                log("[FATAL] Browser window closed during login check.")
                return
            if page.query_selector("[aria-label='Chat list'], #side, #pane-side, [data-testid='chat-list']"):
                logged_in = True
                break
            time.sleep(1)

        if not logged_in:
            log("[FATAL] Account 1 is NOT logged in or QR code is waiting. Aborting.")
            context.close()
            return

        log("[✓] Account 1 authenticated successfully! Dispatching repayment notice...")
        success = send_whatsapp(page, CANDIDATE, msg)

        if success:
            log(f"SUCCESS: WhatsApp repayment notice delivered to {CANDIDATE['name']} ({CANDIDATE['phone']})!")
            record_dispatch({
                "candidate_id": CANDIDATE["candidate_id"],
                "name": CANDIDATE["name"],
                "email": CANDIDATE["email"],
                "phone": CANDIDATE["phone"],
                "cert_id": CANDIDATE["cert_id"],
                "domain": CANDIDATE["domain"],
                "status": "DELIVERED",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            log(f"FAILED: Could not deliver message to {CANDIDATE['phone']}.")

        log("Waiting 5s before closing browser...")
        time.sleep(5)
        context.close()

if __name__ == "__main__":
    main()
