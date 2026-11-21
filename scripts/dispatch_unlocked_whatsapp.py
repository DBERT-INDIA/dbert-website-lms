import os
import sys
import json
import time
import random
import urllib.parse
import argparse
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
LOG_FILE = DATA_DIR / "whatsapp_unlocked_dispatch.log"
SENT_LOG_JSON = DATA_DIR / "whatsapp_unlocked_sent.json"

SESSION_PATHS = {
    1: AIVARA_DIR / ".chrome_session_account1" if (AIVARA_DIR / ".chrome_session_account1").exists() else PROJECT_ROOT / ".chrome_session_account1",
    2: AIVARA_DIR / ".chrome_session_account2" if (AIVARA_DIR / ".chrome_session_account2").exists() else PROJECT_ROOT / ".chrome_session_account2",
}

def log_message(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def record_dispatch(entry: dict):
    records = []
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []
    records.append(entry)
    with open(SENT_LOG_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

def send_whatsapp_single(page, item: dict, acc_num: int) -> tuple[bool, str]:
    if page.is_closed():
        return False, "BROWSER_CLOSED"

    phone = item["clean_phone"]
    msg = item["message"]
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=40000)
    except Exception as e_nav:
        err_msg = str(e_nav).lower()
        if "closed" in err_msg:
            return False, f"BROWSER_CLOSED: {str(e_nav)}"

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
                if any(term in txt for term in ["invalid", "not on whatsapp", "url is invalid", "couldn't find"]):
                    btn = d.query_selector("button")
                    if btn:
                        btn.click()
                    return False, "NOT_ON_WHATSAPP"
                elif any(term in txt for term in ["what's new", "calling is now available", "update"]):
                    c_btn = d.query_selector("button")
                    if c_btn:
                        c_btn.click()
                        time.sleep(1)
            except Exception:
                pass

        # Check send button
        send_btn = (
            page.query_selector('button[aria-label="Send"]') or
            page.query_selector('span[data-icon="send"]') or
            page.query_selector('span[data-icon="send-light"]')
        )
        if send_btn:
            try:
                time.sleep(1)
                tag = page.evaluate("(el) => el.tagName.toLowerCase()", send_btn)
                if tag != "button":
                    btn_parent = page.evaluate_handle("(el) => el.closest('button') || el", send_btn)
                    btn_parent.click()
                else:
                    send_btn.click()
                time.sleep(3)
                sent = True
                break
            except Exception:
                pass

        # Alternatively press Enter on chat box
        chat_input = page.query_selector('footer div[contenteditable="true"], div[role="textbox"], div[contenteditable="true"][data-tab="10"]')
        if chat_input:
            try:
                text_content = chat_input.inner_text().strip()
                if text_content:
                    chat_input.focus()
                    time.sleep(0.5)
                    page.keyboard.press("Enter")
                    time.sleep(3)
                    sent = True
                    break
            except Exception:
                pass

        time.sleep(1)

    if not sent:
        return False, "TIMEOUT_SEND_NOT_COMPLETED"

    return True, "SENT"

def run_account_worker(acc_num: int, queue_path: Path, dry_run: bool = False):
    session_dir = str(SESSION_PATHS[acc_num])
    log_message(f"=== STARTING UNLOCKED DOSSIER DISPATCH FOR ACCOUNT {acc_num} ===")
    log_message(f"Session Dir: {session_dir}")
    log_message(f"Queue File: {queue_path.name}")
    log_message(f"Dry Run: {dry_run}")

    if not queue_path.exists():
        log_message(f"[ERROR] Queue file not found: {queue_path}")
        return

    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)

    log_message(f"Loaded {len(queue)} items for Account {acc_num}.")

    # Load previously sent phones today
    today_str = datetime.now().strftime("%Y-%m-%d")
    already_sent_phones = set()
    if SENT_LOG_JSON.exists():
        try:
            with open(SENT_LOG_JSON, "r", encoding="utf-8") as f:
                for r in json.load(f):
                    if r.get("status") == "SENT" and r.get("timestamp", "").startswith(today_str):
                        already_sent_phones.add(r.get("phone"))
        except Exception:
            pass

    if dry_run:
        log_message(f"[DRY RUN] Simulating {len(queue)} messages for Account {acc_num}...")
        for idx, item in enumerate(queue, 1):
            log_message(f"\n--- Candidate #{idx} (Account {acc_num}) ---")
            log_message(f"To: {item['name']} (+{item['clean_phone']}) | Cert: {item['cert_id']}")
            log_message(f"Message Preview:\n{item['message']}\n")
        return

    launch_args = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-infobars",
        "--window-size=1280,800"
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=session_dir,
            headless=False,
            args=launch_args,
            viewport={"width": 1280, "height": 800}
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        log_message("Checking WhatsApp Web Session readiness...")
        try:
            page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=45000)
        except Exception as e_w:
            log_message(f"Warning on initial load: {e_w}")

        # Wait for chat list or QR code
        session_ready = False
        for _ in range(30):
            if page.query_selector("#pane-side") or page.query_selector('div[data-tab="3"]'):
                session_ready = True
                break
            time.sleep(1)

        if not session_ready:
            log_message(f"[WARNING] Account {acc_num} chat list not detected immediately. Checking page content...")

        success_count = 0
        failure_count = 0
        consecutive_failures = 0

        for idx, item in enumerate(queue, 1):
            phone = item["clean_phone"]
            name = item["name"]

            if phone in already_sent_phones:
                log_message(f"[{idx:2d}/{len(queue)}] Account {acc_num} | SKIP (Already sent): {name} ({phone})")
                continue

            log_message(f"[{idx:2d}/{len(queue)}] Account {acc_num} | Sending unlocked notice to {name} (+{phone})...")
            ok, reason = send_whatsapp_single(page, item, acc_num)

            result_entry = {
                "account": acc_num,
                "phone": phone,
                "name": name,
                "email": item.get("email"),
                "cert_id": item["cert_id"],
                "type": "unlocked_stipend_notice",
                "status": "SENT" if ok else reason,
                "timestamp": datetime.now().isoformat(),
            }
            record_dispatch(result_entry)

            if ok:
                success_count += 1
                consecutive_failures = 0
                already_sent_phones.add(phone)
                log_message(f"   [SUCCESS] Account {acc_num} -> {name} delivered successfully.")
            else:
                failure_count += 1
                consecutive_failures += 1
                log_message(f"   [FAILED] Account {acc_num} -> {name}: {reason}")

            if consecutive_failures >= 3:
                log_message(f"[CIRCUIT BREAKER] Account {acc_num} hit 3 consecutive failures ({reason}). Stopping worker.")
                break

            # Randomized 12s to 25s human break after confirming message has been sent
            if idx < len(queue):
                delay = random.uniform(12.0, 25.0)
                log_message(f"   ... Waiting {delay:.1f}s human break before next message...")
                time.sleep(delay)

        log_message(f"=== COMPLETED ACCOUNT {acc_num} DISPATCH: {success_count} Sent, {failure_count} Failed ===")
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run DBERT Unlocked Dossier WhatsApp Dispatcher")
    parser.add_argument("--account", type=int, choices=[1, 2], help="Run dispatch specifically for Account 1 or Account 2")
    parser.add_argument("--queue", type=str, help="Custom queue file path (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate queue without opening browser")
    args = parser.parse_args()

    q1 = Path(args.queue) if args.queue else DATA_DIR / "whatsapp_unlocked_queue_acc1.json"
    q2 = Path(args.queue) if args.queue else DATA_DIR / "whatsapp_unlocked_queue_acc2.json"

    if args.account == 1:
        run_account_worker(1, q1, dry_run=args.dry_run)
    elif args.account == 2:
        run_account_worker(2, q2, dry_run=args.dry_run)
    else:
        # Default run Account 1 then Account 2 sequentially
        run_account_worker(1, q1, dry_run=args.dry_run)
        time.sleep(5)
        run_account_worker(2, q2, dry_run=args.dry_run)
