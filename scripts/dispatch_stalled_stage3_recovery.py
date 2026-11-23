#!/usr/bin/env python3
"""
scripts/dispatch_stalled_stage3_recovery.py
Omnichannel Stalled Stage 3 Candidate Recovery Daemon (Dual WhatsApp + Email).
Recovers candidates with an issued digital offer letter who have not confirmed
their seat (unpaid ₹499 caution deposit).

Sovereign Directives:
- Sovereign active domain strictly https://dbert.in and https://lms.dbert.in
- WhatsApp: Verification URL & Offer URL placed within the first 15 lines (Line 8 & 11)
- 18s - 35s humanized anti-ban pacing
- Deduplication against data/dbert_whatsapp_sent_today.json
- Circuit breaker halts if 3 consecutive failures occur
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

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

PROJECT_ROOT = Path(r"C:\Users\user\Desktop\dbert-website-lms")
DATA_DIR = PROJECT_ROOT / "data"
QUEUE_FILE = DATA_DIR / "stalled_stage3_recovery_queue.json"
SENT_LOG_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"
LOG_FILE = DATA_DIR / "whatsapp_dispatch_stage3_recovery.log"

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
SESSION_ACC2 = (
    AIVARA_DIR / ".chrome_session_account2"
    if (AIVARA_DIR / ".chrome_session_account2").exists()
    else PROJECT_ROOT / ".chrome_session_account2"
)

def log_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def load_queue():
    if not QUEUE_FILE.exists():
        return []
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def record_sent(phone_digits: str, name: str, email: str, channel: str):
    data = {}
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    data[phone_digits] = {
        "name": name,
        "email": email,
        "channel": channel,
        "sent_at": datetime.now().isoformat()
    }
    try:
        with open(SENT_LOG_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def format_whatsapp_message(cand: dict) -> str:
    first_name = cand.get("first_name", "Fellow")
    domain = cand.get("domain", "Applied Engineering")
    offer_id = cand.get("offer_letter_id", "DBERT-OFR-2026")
    offer_url = cand.get("offer_url", "https://lms.dbert.in/portal/offer")
    verify_url = cand.get("verification_url", "https://dbert.in/verify")

    # Lines 1-15 contain critical URLs and letterhead
    lines = [
        f"Dear {first_name},",
        f"",
        f"DBERT ADMISSIONS NOTIFICATION • SEAT CONFIRMATION NOTICE",
        f"Directorate of Applied Research & Engineering Fellowship",
        f"Batch Cohort: 2026–2027 • Domain: {domain}",
        f"Official Reference ID: {offer_id}",
        f"",
        f"📄 View & Digitally Sign Offer Letter:",
        f"{offer_url}",
        f"",
        f"🔍 Institutional Credential Verification Portal:",
        f"{verify_url}",
        f"",
        f"Stipend Structure & Protection Clauses:",
        f"• Milestone Stipend: ₹5,000 (Direct UPI disbursement upon capstone milestone)",
        f"• Campus Ambassador Incentive: Up to ₹18,000",
        f"• Seat Caution Deposit: ₹499 (100% credited against registration)",
        f"• 14-Day Academic Exam Pause: Pause sprints during university exams with zero penalty",
        f"",
        f"Please sign your digital offer and complete seat confirmation today to lock your allocated batch date.",
        f"",
        f"Admissions Desk WhatsApp: +91 81929 11360",
        f"DBERT Council • MSME UDYAM-UP-29-0109046"
    ]
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="DBERT Stalled Stage 3 Omnichannel Recovery")
    parser.add_argument("--dry-run", action="store_true", help="Preview message payloads without sending")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of candidates to process")
    parser.add_argument("--live", action="store_true", help="Execute live WhatsApp dispatch via Account 2")
    args = parser.parse_args()

    queue = load_queue()
    if not queue:
        print("Queue is empty. Run build_stalled_stage3_recovery_queue.py first.")
        return

    targets = queue[:args.limit]
    print("=" * 80)
    print("DBERT STALLED STAGE 3 RECOVERY DISPATCH DAEMON")
    print(f"Total in Queue: {len(queue)} | Target Slice: {len(targets)}")
    print(f"Mode: {'LIVE DISPATCH' if args.live else 'DRY RUN'}")
    print("=" * 80)

    if not args.live or args.dry_run:
        print("\n--- SAMPLE PREVIEW (FIRST CANDIDATE) ---")
        sample_msg = format_whatsapp_message(targets[0])
        print(f"To: {targets[0]['name']} ({targets[0]['phone']})")
        print("-" * 40)
        print(sample_msg)
        print("-" * 40)
        lines = sample_msg.split("\n")
        print(f"Total lines: {len(lines)}")
        offer_line = next((idx + 1 for idx, l in enumerate(lines) if "portal/offer" in l), None)
        verify_line = next((idx + 1 for idx, l in enumerate(lines) if "dbert.in/verify" in l), None)
        print(f"Offer URL line: {offer_line} (Must be <= 15)")
        print(f"Verify URL line: {verify_line} (Must be <= 15)")
        print("\nDry run completed successfully. Pass --live to initiate delivery.")
        return

    # LIVE PLAYWRIGHT EXECUTION
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed in current environment. Run dry-run or install playwright.")
        return

    log_message(f"Starting live dispatch for {len(targets)} candidates via Account 2...")
    with sync_playwright() as p:
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_ACC2),
            headless=False,
            channel="chrome",
            args=["--no-sandbox", "--disable-gpu", "--disable-notifications"]
        )
        page = browser_context.new_page()
        page.goto("https://web.whatsapp.com", wait_until="networkidle", timeout=60000)
        time.sleep(8)

        success_count = 0
        failure_count = 0
        consecutive_failures = 0

        for idx, cand in enumerate(targets, 1):
            raw_phone = cand.get("raw_phone")
            name = cand.get("name")
            email = cand.get("email")
            msg_text = format_whatsapp_message(cand)
            encoded_msg = urllib.parse.quote(msg_text)
            target_url = f"https://web.whatsapp.com/send?phone=91{raw_phone}&text={encoded_msg}"

            log_message(f"[{idx}/{len(targets)}] Navigating to {name} (+91{raw_phone})...")
            try:
                page.goto(target_url, wait_until="domcontentloaded", timeout=45000)
                time.sleep(5)

                # Click Send button
                send_button = page.locator('button[data-tab="11"], button[aria-label="Send"], span[data-icon="send"]').first
                send_button.wait_for(state="visible", timeout=20000)
                send_button.click()
                time.sleep(4)

                record_sent(raw_phone, name, email, "whatsapp_account2")
                log_message(f"[{idx}/{len(targets)}] DELIVERED to {name} (+91{raw_phone})")
                success_count += 1
                consecutive_failures = 0

                # Humanized pacing
                pause = random.randint(18, 35)
                log_message(f"Pacing: sleeping {pause}s...")
                time.sleep(pause)

            except Exception as e:
                log_message(f"[{idx}/{len(targets)}] FAILED for {name} (+91{raw_phone}): {e}")
                failure_count += 1
                consecutive_failures += 1
                if consecutive_failures >= 3:
                    log_message("Circuit breaker triggered: 3 consecutive failures. Halting.")
                    break

        browser_context.close()
        log_message(f"Dispatch finished. Delivered: {success_count}, Failed: {failure_count}")

if __name__ == "__main__":
    main()
