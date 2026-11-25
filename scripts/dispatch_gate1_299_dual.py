#!/usr/bin/env python3
"""
Dual-Account WhatsApp Dispatcher for Gate 1 (₹299) Today 6:00 PM Deadline.
- Account 1: C:\\Users\\user\\Desktop\\aivara\\aivara\\.chrome_session_account1 (50 candidates)
- Account 2: C:\\Users\\user\\Desktop\\aivara\\aivara\\.chrome_session_account2 (50 candidates)
- Pacing: 18s-35s randomized delay + 3-consecutive-failure circuit breaker.
"""

import argparse
import csv
import json
import random
import sqlite3
import subprocess
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

QUEUE_ACC1 = DATA_DIR / "whatsapp_gate1_299_acc1.json"
QUEUE_ACC2 = DATA_DIR / "whatsapp_gate1_299_acc2.json"
TRACKING_CSV = DATA_DIR / "dispatch_tracking_gate1_299_nov25.csv"
LOG_FILE = DATA_DIR / "whatsapp_dispatch_299.log"
SENT_TODAY_JSON = DATA_DIR / "dbert_whatsapp_sent_today.json"
DB_PATH = DATA_DIR / "dbert_whatsapp.db"


def log_msg(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def build_message(item: dict) -> str:
    first_name = (item.get("name") or "Intern").strip().split()[0]
    cert_id = (item.get("cert_id") or "").strip()
    unlock_url = (
        f"https://dbert.in/verify/unlock?certid={cert_id}"
        if cert_id
        else "https://dbert.in/verify/unlock"
    )
    return (
        f"⚠️ *FINAL REMINDER: Gate 1 Action Required Today by 6:00 PM*\n\n"
        f"Hi {first_name},\n\n"
        f"Your *₹299 Gate 1 verification deposit* is still pending. Without completing Gate 1, you will *not* be able to unlock upcoming tasks or submit any new tasks for stipend release.\n\n"
        f"🔓 *Unlock Gate 1 Now:*\n"
        f"{unlock_url}\n\n"
        f"📢 *Real-Time Updates Group:*\n"
        f"https://chat.whatsapp.com/Kn6o6hMoFfc7rIVx0wgZt3\n\n"
        f"📅 *₹5,499 Stipend Release Date:* 03 Dec 2026\n"
        f"⏰ *Deadline:* *Today, 6:00 PM*\n\n"
        f"Complete before *6:00 PM today* to keep your task portal unlocked for the *03 Dec 2026* release.\n\n"
        f"— *DBERT Admissions & Stipend Desk*"
    )


def load_already_sent_today() -> set[str]:
    sent = set()
    if TRACKING_CSV.exists():
        try:
            with open(TRACKING_CSV, encoding="utf-8", newline="") as f:
                for row in csv.DictReader(f):
                    if row.get("status") == "SENT":
                        sent.add(row.get("clean_phone", ""))
        except Exception:
            pass
    return sent


def record_result(item: dict, status: str, account_label: str):
    ts = datetime.now().isoformat(timespec="seconds")
    fieldnames = [
        "serial_no", "candidate_id", "name", "email", "clean_phone",
        "cert_id", "domain", "status", "timestamp", "account",
    ]
    file_exists = TRACKING_CSV.exists()
    with open(TRACKING_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            w.writeheader()
        w.writerow({
            "serial_no": item.get("serial_no"),
            "candidate_id": item.get("candidate_id"),
            "name": item.get("name"),
            "email": item.get("email"),
            "clean_phone": item.get("clean_phone"),
            "cert_id": item.get("cert_id"),
            "domain": item.get("domain"),
            "status": status,
            "timestamp": ts,
            "account": account_label,
        })

    if status == "SENT":
        # Append to dbert_whatsapp_sent_today.json
        records = []
        if SENT_TODAY_JSON.exists():
            try:
                records = json.loads(SENT_TODAY_JSON.read_text(encoding="utf-8"))
            except Exception:
                records = []
        records.append({
            "candidate_id": item.get("candidate_id"),
            "name": item.get("name"),
            "email": item.get("email"),
            "phone": item.get("clean_phone"),
            "cert_id": item.get("cert_id"),
            "status": "SENT",
            "timestamp": ts,
            "account": account_label,
        })
        SENT_TODAY_JSON.write_text(json.dumps(records, indent=2), encoding="utf-8")

        # Update SQLite whatsapp_sent_log
        if DB_PATH.exists():
            try:
                conn = sqlite3.connect(DB_PATH, timeout=15)
                conn.execute(
                    """
                    INSERT OR IGNORE INTO whatsapp_sent_log
                    (candidate_id, holder_name, user_email, clean_phone, cert_id, domain_track, account_group, whatsapp_sent_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item.get("candidate_id"),
                        item.get("name"),
                        item.get("email"),
                        item.get("clean_phone"),
                        item.get("cert_id"),
                        item.get("domain"),
                        account_label,
                        ts,
                    ),
                )
                conn.commit()
                conn.close()
            except Exception as e:
                log_msg(f"[WARN] SQLite log error: {e}")


def open_context(p, session_dir: str):
    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-infobars",
        "--remote-debugging-port=0",
    ]
    try:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            channel="chrome",
            headless=False,
            ignore_default_args=["--enable-automation"],
            args=launch_args,
        )
    except Exception:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=False,
            ignore_default_args=["--enable-automation"],
            args=launch_args,
        )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return ctx


def verify_account(acc_num: int, wait_secs: int = 180) -> bool:
    session_dir = str(SESSION_ACC1 if acc_num == 1 else SESSION_ACC2)
    log_msg(f"[PREFLIGHT] Checking Account {acc_num} ({session_dir})...")
    with sync_playwright() as p:
        ctx = open_context(p, session_dir)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        logged_in = False
        qr_notice = False
        for _ in range(wait_secs // 2):
            if page.is_closed():
                log_msg(f"[PREFLIGHT] Account {acc_num} window closed.")
                return False
            try:
                if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                    logged_in = True
                    break
                if not qr_notice and page.query_selector("canvas, [data-testid='qrcode']"):
                    log_msg(f"[ACTION REQUIRED] Account {acc_num} needs QR scan! Scan in the open Chrome window.")
                    qr_notice = True
            except Exception:
                pass
            time.sleep(2)

        time.sleep(2)
        ctx.close()
        if logged_in:
            log_msg(f"[PREFLIGHT] Account {acc_num} VERIFIED & LOGGED IN.")
        else:
            log_msg(f"[PREFLIGHT] Account {acc_num} login timed out.")
        return logged_in


def send_one(page, phone: str, message: str) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"
    url = f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(message)}"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e:
        if "closed" in str(e).lower():
            return False, "BROWSER_CLOSED"

    t0 = time.time()
    while time.time() - t0 < 45:
        if page.is_closed():
            return False, "BROWSER_CLOSED"

        for d in page.query_selector_all("[role='dialog']"):
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
                time.sleep(2)
                return True, "SENT"
            except Exception:
                pass

        # Fallback: press Enter in message box
        box = page.query_selector('div[contenteditable="true"][data-tab="10"], footer div[contenteditable="true"]')
        if box:
            try:
                box.focus()
                page.keyboard.press("Enter")
                time.sleep(2)
                return True, "SENT"
            except Exception:
                pass

        time.sleep(1)
    return False, "TIMEOUT"


def run_worker(acc_num: int):
    queue_file = QUEUE_ACC1 if acc_num == 1 else QUEUE_ACC2
    session_dir = str(SESSION_ACC1 if acc_num == 1 else SESSION_ACC2)
    account_label = f"ACCOUNT_{acc_num}"

    items = json.loads(queue_file.read_text(encoding="utf-8"))
    already = load_already_sent_today()
    pending = [x for x in items if x["clean_phone"] not in already]
    log_msg(f"[{account_label}] Starting worker: {len(pending)} pending (of {len(items)})")
    if not pending:
        return

    sent_cnt = 0
    fail_streak = 0
    with sync_playwright() as p:
        ctx = open_context(p, session_dir)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.on("dialog", lambda d: d.accept())
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        # Wait up to 45s for chat list
        ready = False
        for _ in range(22):
            if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list'], header"):
                ready = True
                break
            time.sleep(2)
        if not ready:
            log_msg(f"[{account_label}] Not logged in! Aborting worker.")
            ctx.close()
            return

        for idx, item in enumerate(pending, start=1):
            msg = build_message(item)
            ok, status = send_one(page, item["clean_phone"], msg)
            record_result(item, status, account_label)
            if ok:
                sent_cnt += 1
                fail_streak = 0
                log_msg(f"[{account_label}] ({idx}/{len(pending)}) SENT -> {item['name']} ({item['clean_phone']})")
            else:
                log_msg(f"[{account_label}] ({idx}/{len(pending)}) {status} -> {item['name']} ({item['clean_phone']})")
                if status == "BROWSER_CLOSED":
                    break
                if status != "NOT_ON_WHATSAPP":
                    fail_streak += 1
                    if fail_streak >= 3:
                        log_msg(f"[{account_label}] Circuit breaker tripped after 3 consecutive failures.")
                        break

            if idx < len(pending):
                delay = random.uniform(18.0, 35.0)
                time.sleep(delay)

        ctx.close()
    log_msg(f"[{account_label}] Finished. Sent={sent_cnt}/{len(pending)}")


def dry_run():
    q1 = json.loads(QUEUE_ACC1.read_text(encoding="utf-8"))
    q2 = json.loads(QUEUE_ACC2.read_text(encoding="utf-8"))
    already = load_already_sent_today()
    p1 = [x for x in q1 if x["clean_phone"] not in already]
    p2 = [x for x in q2 if x["clean_phone"] not in already]
    print(f"DRY RUN: Account 1 pending={len(p1)}/{len(q1)}, Account 2 pending={len(p2)}/{len(q2)}, Total={len(p1)+len(p2)}")
    sample = (p1 or q1)[0]
    msg = build_message(sample)
    lines = msg.splitlines()
    url_lines = [i + 1 for i, ln in enumerate(lines) if "https://dbert.in" in ln]
    print(f"Unlock URL line(s): {url_lines} (must be <= 15)")
    print("--- Sample Message ---")
    print(msg)
    print("----------------------")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--worker", type=int, choices=[1, 2])
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        dry_run()
        return

    if args.verify_only:
        ok1 = verify_account(1)
        ok2 = verify_account(2)
        print(f"Verification Summary: Account 1={'OK' if ok1 else 'FAILED'}, Account 2={'OK' if ok2 else 'FAILED'}")
        sys.exit(0 if (ok1 and ok2) else 1)

    if args.worker:
        run_worker(args.worker)
        return

    if args.live:
        if not verify_account(1):
            sys.exit(1)
        if not verify_account(2):
            sys.exit(1)
        log_msg("[LAUNCHER] Both accounts verified! Launching Worker 1 & Worker 2 in parallel...")
        p1 = subprocess.Popen([sys.executable, __file__, "--worker", "1"])
        time.sleep(3)
        p2 = subprocess.Popen([sys.executable, __file__, "--worker", "2"])
        p1.wait()
        p2.wait()
        log_msg("[LAUNCHER] Dual-account dispatch complete.")


if __name__ == "__main__":
    main()
