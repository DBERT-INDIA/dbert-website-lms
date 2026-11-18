import sys
import time
import random
import sqlite3
import urllib.parse
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

DB_PATH = Path("data/dbert_revenue_whatsapp.db")
LOG_PATH = Path("data/dispatch_revenue_whatsapp.log")
AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
SESSION_ACC1 = AIVARA_DIR / ".chrome_session_account1"
SESSION_ACC2 = AIVARA_DIR / ".chrome_session_account2"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def get_db():
    conn = sqlite3.connect(str(DB_PATH), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def send_whatsapp_single(page, row: dict) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    clean_phone = row["clean_phone"]
    if not clean_phone or len(clean_phone) < 10:
        return False, "INVALID_PHONE"

    message = row["whatsapp_message"]
    encoded_msg = urllib.parse.quote(message)
    target_url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_msg}"

    try:
        page.goto(target_url, wait_until="domcontentloaded", timeout=45000)
    except Exception as e:
        return False, f"NAV_TIMEOUT: {e}"

    # Check for invalid phone popup or not on WhatsApp popup
    time.sleep(3)
    try:
        invalid_popup = page.locator("div[role='dialog']:has-text('Phone number shared via url is invalid'), div[role='dialog']:has-text('not on WhatsApp')")
        if invalid_popup.count() > 0:
            ok_btn = invalid_popup.locator("button:has-text('OK')")
            if ok_btn.count() > 0:
                ok_btn.first.click()
            return False, "PHONE_NOT_ON_WHATSAPP"
    except Exception:
        pass

    send_selectors = [
        "span[data-icon='send']",
        "button[aria-label='Send']",
        "button[data-tab='11']",
        "footer button:has(span[data-icon='send'])"
    ]

    button_found = None
    for _ in range(25):
        if page.is_closed():
            return False, "BROWSER_CLOSED"
        for sel in send_selectors:
            try:
                locator = page.locator(sel)
                if locator.count() > 0 and locator.first.is_visible():
                    button_found = locator.first
                    break
            except Exception:
                continue
        if button_found:
            break
        # Also check for popup mid-wait
        try:
            if page.locator("div[role='dialog']:has-text('invalid'), div[role='dialog']:has-text('not on WhatsApp')").count() > 0:
                ok_btn = page.locator("div[role='dialog'] button:has-text('OK')")
                if ok_btn.count() > 0:
                    ok_btn.first.click()
                return False, "PHONE_NOT_ON_WHATSAPP"
        except Exception:
            pass
        time.sleep(1)

    if not button_found:
        try:
            composer = page.locator("footer div[contenteditable='true']")
            if composer.count() > 0:
                composer.first.press("Enter")
                time.sleep(2)
                return True, "SENT_VIA_ENTER"
        except Exception:
            pass
        return False, "SEND_BTN_TIMEOUT"

    try:
        button_found.click()
        time.sleep(2)
        return True, "SENT_VIA_CLICK"
    except Exception as e:
        return False, f"CLICK_FAILED: {e}"

def run_revenue_worker(account_num: int, delay_min: float = 18.0, delay_max: float = 28.0):
    session_dir = str(SESSION_ACC1 if account_num == 1 else SESSION_ACC2)
    acc_label = f"Account {account_num}"

    log(f"Starting Revenue WhatsApp Worker for {acc_label} using {session_dir}")

    conn = get_db()
    pending_rows = conn.execute(
        "SELECT * FROM whatsapp_revenue_dispatch WHERE account_num = ? AND whatsapp_status = 'PENDING' ORDER BY serial_no ASC",
        (account_num,)
    ).fetchall()
    conn.close()

    total_pending = len(pending_rows)
    log(f"[{acc_label}] Total pending candidates to process: {total_pending}")

    if total_pending == 0:
        log(f"[{acc_label}] No pending candidates in queue. Exiting.")
        return

    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                ]
            )
        except Exception:
            context = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=True,
                ignore_default_args=["--enable-automation"],
            )

        page = context.pages[0] if context.pages else context.new_page()

        log(f"[{acc_label}] Initializing WhatsApp Web...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
        time.sleep(8)

        consecutive_failures = 0

        for i, row_data in enumerate(pending_rows, start=1):
            row = dict(row_data)
            serial = row["serial_no"]
            name = row["name"]
            phone = row["clean_phone"]
            amount = row["amount"]

            log(f"[{acc_label}] [{i}/{total_pending}] (Serial #{serial}) Sending to {name} ({phone}) [₹{amount}]...")

            success, detail = send_whatsapp_single(page, row)
            now_str = datetime.now().isoformat()

            conn = get_db()
            if success:
                conn.execute(
                    "UPDATE whatsapp_revenue_dispatch SET whatsapp_status = 'SENT', sent_at = ?, whatsapp_error = NULL WHERE serial_no = ?",
                    (now_str, serial)
                )
                conn.commit()
                consecutive_failures = 0
                log(f"  ✓ [{acc_label}] SENT to {name}! Method: {detail}")
            else:
                conn.execute(
                    "UPDATE whatsapp_revenue_dispatch SET whatsapp_status = 'FAILED', whatsapp_error = ? WHERE serial_no = ?",
                    (detail, serial)
                )
                conn.commit()
                # Only count towards circuit breaker if it's NOT an invalid phone number
                if detail != "PHONE_NOT_ON_WHATSAPP":
                    consecutive_failures += 1
                log(f"  ❌ [{acc_label}] FAILED for {name}: {detail}")

            conn.close()

            # Circuit breaker: pause only if 8 consecutive non-phone failures occur
            if consecutive_failures >= 8:
                log(f"⚠️ [{acc_label}] CIRCUIT BREAKER TRIGGERED: 8 consecutive system failures. Halting worker.")
                break

            # Anti-ban randomized delay
            if i < total_pending:
                delay = random.uniform(delay_min, delay_max)
                log(f"  [{acc_label}] Sleeping {delay:.1f}s before next candidate...")
                time.sleep(delay)

        context.close()
        log(f"[{acc_label}] Worker run finished.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=int, required=True, choices=[1, 2], help="Account number (1 or 2)")
    parser.add_argument("--delay-min", type=float, default=18.0)
    parser.add_argument("--delay-max", type=float, default=28.0)
    args = parser.parse_args()

    run_revenue_worker(args.account, args.delay_min, args.delay_max)
