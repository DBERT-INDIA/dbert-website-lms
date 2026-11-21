import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(line_buffering=True)

ARTIFACT_DIR = Path(r"C:\Users\user\.gemini\antigravity\brain\db340522-3de4-46ab-8736-005fb1623326\screenshots")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

TOKENS = {
    "scheduled": "b21c99e7fd6143eb63648da7f7d5963fbba699c285ffbbd37b5b0aebcbfcfa1b",
    "countdown": "8235a62a69e82cc7260f63277739201984bc468acde862e25fc52d2724efdfea",
    "admin": "3d4e50f2dbd803a76cb8d1f729c2ddbe86885069e9bd55b72049cccb21dd46dc"
}

def capture_all():
    print(f"[START] Saving screenshots to: {ARTIFACT_DIR}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. PUBLIC VIEWS (Unauthenticated context)
        pub_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        pub_page = pub_ctx.new_page()

        # View 1: Directory Tab 1 (Pre-Vetted Engineers)
        try:
            print("1. Capturing Pre-Vetted Engineers Directory (Tab 1)...")
            pub_page.goto("https://dbert.in/verify/directory", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            pub_page.screenshot(path=str(ARTIFACT_DIR / "1_directory_tab1_engineers.png"), full_page=False)
            print("   -> Done 1")
        except Exception as e:
            print(f"   -> Err 1: {e}")

        # View 2: Directory Tab 2 (Incubation Fellows)
        try:
            print("2. Capturing Directory Tab 2 (Incubation Fellows)...")
            tab2_btn = pub_page.locator("text='Incubation Fellows'")
            if tab2_btn.count() > 0:
                tab2_btn.first.click()
                time.sleep(2)
                pub_page.screenshot(path=str(ARTIFACT_DIR / "2_directory_tab2_fellows.png"), full_page=False)
                print("   -> Done 2")
            else:
                print("   -> Tab 2 btn not found")
        except Exception as e:
            print(f"   -> Err 2: {e}")

        # View 3: Unlocked Proof Dossier
        try:
            print("3. Capturing Unlocked Proof Dossier (Yasharth Poddar)...")
            pub_page.goto("https://dbert.in/verify/CERT-DBERT-2026-FSD-046", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            pub_page.screenshot(path=str(ARTIFACT_DIR / "3_proof_dossier_unlocked.png"), full_page=False)
            print("   -> Done 3")
        except Exception as e:
            print(f"   -> Err 3: {e}")

        # View 4: LMS Home / Signin
        try:
            print("4. Capturing LMS Portal Home / Sign-in...")
            pub_page.goto("https://lms.dbert.in/#signin", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            pub_page.screenshot(path=str(ARTIFACT_DIR / "4_lms_portal_signin.png"), full_page=False)
            print("   -> Done 4")
        except Exception as e:
            print(f"   -> Err 4: {e}")

        # View 5: 3-Document Printable Credential Dossier
        try:
            print("5. Capturing 3-Doc Printable Credential Dossier...")
            pub_page.goto("https://lms.dbert.in/portal/certificate/CERT-DBERT-2026-FSD-156/print", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            pub_page.screenshot(path=str(ARTIFACT_DIR / "5_printable_3doc_credential.png"), full_page=False)
            print("   -> Done 5")
        except Exception as e:
            print(f"   -> Err 5: {e}")

        pub_ctx.close()

        # 2. AUTHENTICATED CONTEXT: SCHEDULED INTERN (Gurka Vinay Kumar Reddy)
        sched_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        sched_ctx.add_cookies([{
            "name": "dbert_auth",
            "value": TOKENS["scheduled"],
            "domain": "lms.dbert.in",
            "path": "/"
        }])
        sched_page = sched_ctx.new_page()

        try:
            print("6. Capturing Stipend Tasks Dashboard (Scheduled Payout View)...")
            sched_page.goto("https://lms.dbert.in/stipend/tasks", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            sched_page.screenshot(path=str(ARTIFACT_DIR / "6_stipend_tasks_scheduled.png"), full_page=False)
            print("   -> Done 6")
        except Exception as e:
            print(f"   -> Err 6: {e}")

        try:
            print("7. Capturing Intern Ambassador / Wallet Withdraw View...")
            sched_page.goto("https://lms.dbert.in/intern/ambassador/withdraw", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            sched_page.screenshot(path=str(ARTIFACT_DIR / "7_ambassador_wallet_withdraw.png"), full_page=False)
            print("   -> Done 7")
        except Exception as e:
            print(f"   -> Err 7: {e}")

        sched_ctx.close()

        # 3. AUTHENTICATED CONTEXT: IN-SPRINT COUNTDOWN INTERN (Deepanshu)
        count_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        count_ctx.add_cookies([{
            "name": "dbert_auth",
            "value": TOKENS["countdown"],
            "domain": "lms.dbert.in",
            "path": "/"
        }])
        count_page = count_ctx.new_page()

        try:
            print("8. Capturing Stipend Tasks Dashboard (Active Sprint Countdown View)...")
            count_page.goto("https://lms.dbert.in/stipend/tasks", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            count_page.screenshot(path=str(ARTIFACT_DIR / "8_stipend_tasks_countdown.png"), full_page=False)
            print("   -> Done 8")
        except Exception as e:
            print(f"   -> Err 8: {e}")

        count_ctx.close()

        # 4. AUTHENTICATED CONTEXT: ADMIN REVIEW FUNNEL
        admin_ctx = browser.new_context(viewport={"width": 1280, "height": 800})
        admin_ctx.add_cookies([{
            "name": "dbert_auth",
            "value": TOKENS["admin"],
            "domain": "lms.dbert.in",
            "path": "/"
        }])
        admin_page = admin_ctx.new_page()

        try:
            print("9. Capturing Admin / Staff Stipend Review Funnel...")
            admin_page.goto("https://lms.dbert.in/admin/stipend-funnel", wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)
            admin_page.screenshot(path=str(ARTIFACT_DIR / "9_admin_stipend_funnel.png"), full_page=False)
            print("   -> Done 9")
        except Exception as e:
            print(f"   -> Err 9: {e}")

        admin_ctx.close()
        browser.close()
        print("=== ALL SCREENSHOTS CAPTURED SUCCESSFULLY ===")

if __name__ == "__main__":
    capture_all()
