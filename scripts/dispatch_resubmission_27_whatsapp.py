#!/usr/bin/env python3
"""
================================================================================
DBERT Capstone Revision (27 Candidates) WhatsApp Dispatch Daemon (Account 2 Only)
- Queue: data/phones_27_resubmission.json (27 Submissions -> 25 Unique Phone Numbers)
- Sender: Account 2 (.chrome_session_account2) - Verified LOGGED IN
- Anti-ban pacing: 18s - 35s randomized human pause after delivery
- Multi-layer deduplication & tracking:
  * data/whatsapp_dispatch_299.log
  * data/dbert_whatsapp_sent_today.json
  * data/dbert_whatsapp.db (whatsapp_sent_log)
  * data/dispatch_tracking_resubmit_27.csv
  * EC2 PostgreSQL dbert_internship.notifications dual-write
- Circuit breaker: Halts if 3 consecutive failures occur
================================================================================
"""

import sys
import os
import time
import json
import csv
import random
import argparse
import urllib.parse
import sqlite3
import subprocess
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
TRACKING_CSV = DATA_DIR / "dispatch_tracking_resubmit_27.csv"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"
QUEUE_FILE = DATA_DIR / "phones_27_resubmission.json"

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"

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

def sync_notification_to_ec2(intern_id, title, body, link):
    """Inserts in-app notification to EC2 PostgreSQL dbert_internship.notifications."""
    if not intern_id:
        return
    py_script = f'''
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    conn.execute(
        """
        INSERT INTO notifications (intern_id, kind, title, body, link) 
        VALUES (?, ?, ?, ?, ?);
        """,
        ({int(intern_id)}, "whatsapp_outreach", {json.dumps(title)}, {json.dumps(body)}, {json.dumps(link)})
    )
    if hasattr(conn, "commit"):
        conn.commit()
    print("Notification synced to EC2 for intern #{intern_id}")
'''
    try:
        subprocess.run(
            ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"],
            input=py_script,
            text=True,
            capture_output=True,
            encoding="utf-8",
            timeout=10
        )
    except Exception as e:
        log_message(f"[WARN] Failed to dual-write notification to EC2: {e}")

def record_dispatch(entry: dict):
    # 1. Update JSON
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
        log_message(f"[WARN] Failed to write to {SENT_LOG_JSON.name}: {e}")

    # 2. Update CSV
    fieldnames = ["serial_no", "intern_id", "name", "email", "clean_phone", "cert_id", "domain", "status", "timestamp", "account"]
    file_exists = TRACKING_CSV.exists()
    try:
        with open(TRACKING_CSV, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "serial_no": entry.get("serial_no"),
                "intern_id": entry.get("intern_id"),
                "name": entry.get("name"),
                "email": entry.get("email"),
                "clean_phone": entry.get("clean_phone"),
                "cert_id": entry.get("cert_id"),
                "domain": entry.get("domain"),
                "status": entry.get("status"),
                "timestamp": entry.get("timestamp"),
                "account": entry.get("account")
            })
    except Exception as e:
        log_message(f"[WARN] Failed to write to CSV: {e}")

    # 3. Update SQLite DB
    if DB_PATH.exists() and entry.get("status") == "SENT":
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                INSERT OR IGNORE INTO whatsapp_sent_log 
                (candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.get("intern_id"),
                entry.get("name"),
                entry.get("email"),
                entry.get("clean_phone"),
                entry.get("cert_id"),
                entry.get("domain"),
                "ACCOUNT_2",
                entry.get("timestamp")
            ))
            conn.commit()
            conn.close()
        except Exception as e:
            log_message(f"[WARN] Failed to write to SQLite: {e}")

def build_message(cand: dict) -> str:
    name = (cand.get("name") or "Fellow").strip()
    domain = cand.get("domain") or "Technical Incubation"
    cert_id = cand.get("cert_id") or "DBERT Fellowship"
    gh_reason = cand.get("github_reason") or "Personal fork or standalone repository without an open PR."
    li_reason = cand.get("linkedin_reason") or "DBERT credential not yet verified under Licenses & Certifications."
    
    # Strict first-15-lines placement of both URLs
    lines = [
        f"Dear {name},",
        "",
        "Greetings from DBERT Academic Admissions & Technical Review Board.",
        f"This is an official update regarding your ₹5,000 Milestone Stipend Capstone for your {domain} Fellowship.",
        "",
        "Your submission has been reviewed, and REVISIONS ARE REQUIRED before your release can be approved:",
        "1. Resubmit Deliverables: https://lms.dbert.in/stipend/tasks",
        f"2. Your Credential Dossier: https://dbert.in/verify/{cert_id}",
        "",
        "REQUIRED ACTION ITEMS TO UNLOCK APPROVAL:",
        f"1. GitHub Deliverable (Gate 4):",
        f"   Issue Flagged: {gh_reason}",
        "   Requirement: DBERT milestone policy strictly requires an active Pull Request (PR) on one of our 4 official partner repositories:",
        "   • Alkame Platform: https://github.com/Alkameinc/alkame-nifty-50-educational",
        "   • Gayatri AI: https://github.com/Gayatri-Education/Gayatri-Demo",
        "   • DBERT Agent / Aivara: https://github.com/DBERT-INDIA/dbert-agent",
        "   • Internship Portal: https://github.com/DBERT-INDIA/Internshipportal",
        "   Please open a Pull Request against the upstream repository and submit your PR link (e.g. github.com/Alkameinc/.../pull/123).",
        "",
        f"2. LinkedIn Credential (Gate 1):",
        f"   Issue Flagged: {li_reason}",
        "   Requirement: Add DBERT to your LinkedIn profile under 'Licenses & Certifications' using the 1-Click launcher on your stipend dashboard.",
        "",
        "Your submission form on https://lms.dbert.in/stipend/tasks has been unlocked for resubmission. Please update your deliverables as soon as possible for the upcoming 03 December 2026 payout release.",
        "",
        "DBERT Admissions & Engineering Office",
        "https://dbert.in | admissions@dbert.in"
    ]
    return "\n".join(lines)

def load_queue():
    if not QUEUE_FILE.exists():
        log_message(f"[ERROR] Queue file {QUEUE_FILE} not found!")
        sys.exit(1)
        
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Deduplicate by phone
    seen_phones = set()
    unique_candidates = []
    for c in data:
        ph = c.get("clean_phone")
        if not ph or len(ph) != 12:
            continue
        if ph in seen_phones:
            continue
        seen_phones.add(ph)
        unique_candidates.append(c)
        
    return unique_candidates

def main():
    parser = argparse.ArgumentParser(description="DBERT Capstone Revision (27 Candidates) WhatsApp Dispatch")
    parser.add_argument("--dry-run", action="store_true", help="Print messages without dispatching")
    parser.add_argument("--live", action="store_true", help="Execute live WhatsApp dispatch")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of candidates to process")
    args = parser.parse_args()

    candidates = load_queue()
    if args.limit > 0:
        candidates = candidates[:args.limit]

    log_message("=" * 80)
    log_message(f"STARTING DBERT CAPSTONE REVISION WHATSAPP DISPATCH")
    log_message(f"Total Unique Candidates to Contact: {len(candidates)}")
    log_message(f"Session Account: {SESSION_ACC2}")
    log_message(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE DISPATCH'}")
    log_message("=" * 80)

    if args.dry_run:
        for idx, cand in enumerate(candidates, 1):
            msg = build_message(cand)
            print(f"\n[{idx}/{len(candidates)}] --- CANDIDATE: {cand['name']} ({cand['clean_phone']}) ---")
            print(msg[:400] + "\n... [TRUNCATED] ...\n")
            lines = msg.split("\n")
            print(f"Line 7: {lines[6] if len(lines) > 6 else 'N/A'}")
            print(f"Line 8: {lines[7] if len(lines) > 7 else 'N/A'}")
        log_message("[DRY RUN COMPLETE] Zero messages sent.")
        return

    if not args.live:
        print("Please specify either --dry-run or --live.")
        return

    # Check Session
    if not SESSION_ACC2.exists():
        log_message(f"[FATAL] Account 2 session dir {SESSION_ACC2} does not exist!")
        sys.exit(1)

    log_message(f"[INIT] Launching Playwright Chromium with persistent context...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_ACC2),
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            viewport=None
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        log_message("[INIT] Navigating to WhatsApp Web to verify authentication...")
        page.goto("https://web.whatsapp.com", wait_until="load", timeout=60000)
        
        # Wait for chat list or search bar
        try:
            page.wait_for_selector("div[contenteditable='true'][data-tab='3'], #side", timeout=35000)
            log_message("[AUTH SUCCESS] WhatsApp Web session is ACTIVE and authenticated!")
        except Exception:
            log_message("[FATAL] WhatsApp Web is not authenticated or QR code is showing! Aborting.")
            browser.close()
            sys.exit(1)

        consecutive_failures = 0
        sent_count = 0
        failed_count = 0

        for idx, cand in enumerate(candidates, 1):
            phone = cand["clean_phone"]
            name = cand["name"]
            email = cand["email"]
            intern_id = cand.get("intern_id")
            cert_id = cand.get("cert_id")
            domain = cand.get("domain")

            log_message(f"\n[{idx}/{len(candidates)}] Processing {name} ({phone})...")
            message_text = build_message(cand)
            encoded_msg = urllib.parse.quote(message_text)
            direct_url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

            success = False
            try:
                page.goto(direct_url, wait_until="load", timeout=45000)
                
                # Wait for send button or invalid number alert
                send_btn_selector = "button[aria-label='Send'], span[data-icon='send']"
                
                # Check for invalid phone popup
                try:
                    invalid_alert = page.wait_for_selector(
                        "div[data-animate-modal-popup='true']",
                        timeout=8000
                    )
                    if invalid_alert and ("phone number shared via url is invalid" in invalid_alert.inner_text().lower() or "not on whatsapp" in invalid_alert.inner_text().lower()):
                        log_message(f"[SKIP] Phone number {phone} is not on WhatsApp or invalid.")
                        record_dispatch({
                            "serial_no": idx,
                            "intern_id": intern_id,
                            "name": name,
                            "email": email,
                            "clean_phone": phone,
                            "cert_id": cert_id,
                            "domain": domain,
                            "status": "INVALID_PHONE",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "account": "ACCOUNT_2"
                        })
                        continue
                except Exception:
                    pass

                # Locate send button
                send_btn = page.wait_for_selector(send_btn_selector, timeout=25000)
                if send_btn:
                    time.sleep(random.uniform(1.5, 3.0))
                    send_btn.click()
                    log_message(f"[SUCCESS] Message dispatched to {name} ({phone})!")
                    success = True
                    consecutive_failures = 0
                    sent_count += 1

                    # Record dispatch
                    record_dispatch({
                        "serial_no": idx,
                        "intern_id": intern_id,
                        "name": name,
                        "email": email,
                        "clean_phone": phone,
                        "cert_id": cert_id,
                        "domain": domain,
                        "status": "SENT",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "account": "ACCOUNT_2"
                    })

                    # Dual-write in-app notification to EC2
                    notif_body = (
                        f"Your capstone deliverable requires revisions: {cand.get('github_reason')}. "
                        "Please open a Pull Request on an official partner repo and add DBERT to LinkedIn."
                    )
                    sync_notification_to_ec2(
                        intern_id=intern_id,
                        title="Action Required: Milestone Revision & PR Submission",
                        body=notif_body,
                        link="/stipend/tasks"
                    )

                    # Pacing
                    delay = random.uniform(18.0, 35.0)
                    log_message(f"[PACING] Sleeping for {delay:.1f}s...")
                    time.sleep(delay)
                else:
                    log_message(f"[FAIL] Send button not found for {phone}.")
                    consecutive_failures += 1
                    failed_count += 1
            except Exception as e:
                log_message(f"[ERROR] Failed delivering to {phone}: {e}")
                consecutive_failures += 1
                failed_count += 1

            if consecutive_failures >= 3:
                log_message("[CIRCUIT BREAKER] 3 consecutive failures encountered! Halting dispatch.")
                break

        browser.close()
        log_message("\n" + "=" * 80)
        log_message(f"DISPATCH COMPLETED: {sent_count} sent, {failed_count} failed out of {len(candidates)}.")
        log_message("=" * 80)

if __name__ == "__main__":
    main()
