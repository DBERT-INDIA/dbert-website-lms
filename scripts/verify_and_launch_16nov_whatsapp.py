#!/usr/bin/env python3
"""
================================================================================
DBERT — Automated Pre-Flight Verifier & Dual-Account WhatsApp Launcher
================================================================================
Target: 16 Nov Selected Interns (94 Candidates)
Steps:
  1. Verifies WhatsApp Web Login for Account 1 (.chrome_session_account1).
     If QR scan needed, opens visible Chrome and waits until scanned.
  2. Verifies WhatsApp Web Login for Account 2 (.chrome_session_account2).
     If QR scan needed, opens visible Chrome and waits until scanned.
  3. Once BOTH accounts are 100% verified, launches Worker 1 (Odd Serials: 47)
     and Worker 2 (Even Serials: 47) in parallel side-by-side terminal windows.
================================================================================
"""

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DISPATCH_SCRIPT = SCRIPT_DIR / "send_16nov_selected_whatsapp.py"

AIVARA_DIR = Path(r"C:\Users\user\Desktop\aivara\aivara")
DEFAULT_SESSION_ACC1 = (
    AIVARA_DIR / ".chrome_session_account1"
    if (AIVARA_DIR / ".chrome_session_account1").exists()
    else PROJECT_ROOT / ".chrome_session_account1"
)
DEFAULT_SESSION_ACC2 = (
    AIVARA_DIR / ".chrome_session_account2"
    if (AIVARA_DIR / ".chrome_session_account2").exists()
    else PROJECT_ROOT / ".chrome_session_account2"
)


def verify_account_login(acc_num: int, max_wait_seconds: int = 600) -> bool:
    """
    Verifies if the specified account is logged into WhatsApp Web.
    If not, keeps a visible Chrome browser open and waits for the user to scan the QR code.
    """
    session_dir = str(DEFAULT_SESSION_ACC1 if acc_num == 1 else DEFAULT_SESSION_ACC2)
    print("\n" + "=" * 76)
    print(f"  PRE-FLIGHT VERIFICATION: ACCOUNT {acc_num}")
    print(f"  Session Folder: {session_dir}")
    print("=" * 76)

    with sync_playwright() as p:
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-infobars",
            "--remote-debugging-port=0",
        ]
        browser = None
        try:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                channel="chrome",
                headless=False,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )
        except Exception as e_chrome:
            print(f"[*] System Chrome failed ({e_chrome}). Launching bundled Chromium...")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=session_dir,
                headless=False,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                ignore_default_args=["--enable-automation"],
                args=launch_args,
            )

        browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.on("dialog", lambda d: d.accept())

        print(f"[*] Opening WhatsApp Web for Account {acc_num}...")
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded", timeout=60000)

        print(f"[*] Checking login state for Account {acc_num}...")
        logged_in = False
        qr_printed = False

        ticks = max_wait_seconds // 2
        for _ in range(ticks):
            if page.is_closed():
                print(f"[!] Browser window was closed for Account {acc_num}!")
                return False

            # Check if chat interface is loaded
            if page.query_selector("[aria-label='Chat list'], #pane-side, [data-testid='chat-list']"):
                logged_in = True
                break

            # Check if QR code is displayed
            qr_node = page.query_selector("canvas, [data-testid='qrcode']")
            if qr_node:
                try:
                    qr_img_path = PROJECT_ROOT / "data" / f"qr_account{acc_num}.png"
                    qr_node.screenshot(path=str(qr_img_path))
                except Exception:
                    pass
                if not qr_printed:
                    print("\n" + "!" * 76)
                    print(f"  [ACTION REQUIRED] Account {acc_num} is NOT logged in!")
                    print(f"  >>> Please scan the QR code in the opened Chrome window on your phone.")
                    print(f"  >>> (QR image also saved to data/qr_account{acc_num}.png)")
                    print("!" * 76 + "\n")
                    qr_printed = True

            time.sleep(2)

        time.sleep(2)  # Short cooldown to persist tokens
        browser.close()

        if logged_in:
            print(f"[OK] Account {acc_num} is VERIFIED and LOGGED IN!\n")
            return True
        else:
            print(f"[FAILED] Account {acc_num} verification timed out after {max_wait_seconds}s.\n")
            return False


def launch_dual_workers():
    """Launches Account 1 and Account 2 dispatch workers in separate visible command windows."""
    print("=" * 76)
    print("  LAUNCHING DUAL WHATSAPP WORKERS (ACCOUNT 1 & ACCOUNT 2)")
    print("=" * 76)

    # 1. Launch Account 1 (Odd Serials: 47 candidates)
    cmd1 = f'start "DBERT WA Worker - Account 1 (Odd 1..93)" cmd /k "cd /d {PROJECT_ROOT} && python scripts/send_16nov_selected_whatsapp.py --worker account1 --auto-start"'
    subprocess.Popen(cmd1, shell=True)
    print("[*] Worker 1 launched: Account 1 (47 Odd Candidates)")

    time.sleep(4)  # Small stagger between launches

    # 2. Launch Account 2 (Even Serials: 47 candidates)
    cmd2 = f'start "DBERT WA Worker - Account 2 (Even 2..94)" cmd /k "cd /d {PROJECT_ROOT} && python scripts/send_16nov_selected_whatsapp.py --worker account2 --auto-start"'
    subprocess.Popen(cmd2, shell=True)
    print("[*] Worker 2 launched: Account 2 (47 Even Candidates)")

    print("\n" + "=" * 76)
    print("  BOTH WORKERS RUNNING IN PARALLEL SIDE-BY-SIDE WINDOWS")
    print("  Monitor progress with: python scripts/send_16nov_selected_whatsapp.py --status")
    print("=" * 76 + "\n")


def main():
    parser = argparse.ArgumentParser(description="DBERT 16 Nov WhatsApp Pre-Flight & Dual Launcher")
    parser.add_argument("--verify-only", action="store_true", help="Only verify login sessions without launching workers")
    parser.add_argument("--account", type=int, choices=[1, 2], help="Verify specific account only (1 or 2)")
    parser.add_argument("--skip-verify", action="store_true", help="Directly launch workers without pre-flight check")
    args = parser.parse_args()

    # Ensure queue is initialized
    subprocess.run([sys.executable, str(DISPATCH_SCRIPT), "--init-queue"], check=True)

    if args.skip_verify:
        launch_dual_workers()
        return

    if args.account:
        print("=" * 76)
        print(f"  DBERT 16 NOV SELECTED WHATSAPP LOGIN CHECK: ACCOUNT {args.account}")
        print("=" * 76)
        ok = verify_account_login(args.account)
        if ok:
            print(f"[OK] Account {args.account} is ready for dispatch!")
        else:
            print(f"[FAILED] Account {args.account} is not logged in.")
        return

    print("=" * 76)
    print("  DBERT 16 NOV SELECTED WHATSAPP DUAL-ACCOUNT PRE-FLIGHT VERIFIER")
    print("=" * 76)

    # Step 1: Verify Account 1
    acc1_ok = verify_account_login(1)
    if not acc1_ok:
        print("[ABORT] Account 1 is not verified. Please scan the QR code and re-run.")
        sys.exit(1)

    # Step 2: Verify Account 2
    acc2_ok = verify_account_login(2)
    if not acc2_ok:
        print("[ABORT] Account 2 is not verified. Please scan the QR code and re-run.")
        sys.exit(1)

    print("=" * 76)
    print("  ✓ ALL PRE-FLIGHT CHECKS PASSED: BOTH ACCOUNT 1 & 2 ARE AUTHENTICATED")
    print("=" * 76)

    if args.verify_only:
        print("[*] --verify-only specified. Exiting without launching workers.")
        return

    # Step 3: Launch both workers in parallel
    launch_dual_workers()


if __name__ == "__main__":
    main()
