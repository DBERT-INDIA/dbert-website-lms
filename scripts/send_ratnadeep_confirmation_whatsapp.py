#!/usr/bin/env python3
"""
================================================================================
DBERT — Dispatch Enrollment Confirmation WhatsApp to Ratnadeep (Account 2)
================================================================================
"""

import sys
import time
import json
import urllib.parse
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

SESSION_ACC2 = Path(r"C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2")
PHONE = "918591833879"
NAME = "Ratnadeep manojkumar bamane"
DOMAIN = "Data Analyst"
OFFER_ID = "DBERT-OFR-2026-DA-5278"

MESSAGE_LINES = [
    f"Hello {NAME},",
    "",
    "🎉 *Payment Reconciled & Enrollment Confirmed!*",
    "",
    f"Your ₹499 caution deposit has been successfully verified, and your admission to the DBERT {DOMAIN} Fellowship is officially confirmed.",
    "",
    "📄 *Download Your Official Counter-Signed Offer & Appointment Letter:*",
    "https://lms.dbert.in/portal/offer",
    "",
    "🚀 *Access Your Engineering LMS Workspace & Sprint Modules:*",
    "https://lms.dbert.in/courses",
    "",
    f"• Official Offer Letter ID: {OFFER_ID}",
    "• Batch Kickoff: Monday, 23 Nov 2026",
    f"• Program Track: {DOMAIN} Fellowship",
    "• Workstation & AI Tutor: Active and Unlocked",
    "• Milestone Performance Stipend: Up to ₹5,000 upon successful sprint & task milestones",
    "",
    "Your official digital payment verification voucher (SVG receipt) and 6-milestone lifecycle roadmap have also been dispatched to your registered email (ratnadeepratu737@gmail.com).",
    "",
    "We are thrilled to welcome you to the fellowship! If you need any assistance, reach out directly to the admissions team here.",
    "",
    "Warm regards,",
    "DBERT Admissions Directorate",
    "Digital Blinc Education Research and Technology (dbert.in)"
]

MESSAGE = "\n".join(MESSAGE_LINES)

print(f"Dispatching confirmation to {NAME} ({PHONE})...")
print(f"Line 8: {MESSAGE_LINES[7]}")
print(f"Line 11: {MESSAGE_LINES[10]}")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION_ACC2),
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-accelerated-2d-canvas",
            "--no-first-run",
            "--no-zygote",
            "--disable-gpu",
            "--mute-audio"
        ],
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    page = browser.pages[0] if browser.pages else browser.new_page()

    encoded_text = urllib.parse.quote(MESSAGE)
    target_url = f"https://web.whatsapp.com/send?phone={PHONE}&text={encoded_text}"
    
    page.goto(target_url, timeout=45000, wait_until="domcontentloaded")
    
    sent = False
    for attempt in range(35):
        dialogs = page.query_selector_all('div[role="dialog"], div[data-animate-modal-body="true"]')
        starting_chat = False
        for d in dialogs:
            try:
                txt = d.inner_text().lower()
                if "starting chat" in txt:
                    starting_chat = True
                elif any(term in txt for term in ["what's new", "calling is now available", "update", "privacy"]):
                    c_btn = d.query_selector("button")
                    if c_btn:
                        c_btn.click()
                        time.sleep(1)
            except Exception:
                pass

        cont_btn = page.query_selector("button:has-text('Continue'), button:has-text('OK'), button:has-text('Dismiss')")
        if cont_btn:
            try:
                cont_btn.click()
                time.sleep(1)
            except Exception:
                pass

        if starting_chat:
            time.sleep(1)
            continue

        send_btn = page.query_selector('button[aria-label="Send"], button[data-testid="send"], button[data-testid="compose-btn-send"], span[data-icon="send"]')
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
            except Exception as e:
                pass

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

    print(f"Dispatch Result: {sent}")
    page.screenshot(path="data/whatsapp_ratnadeep_confirmed.png")
    browser.close()

if sent:
    print("SUCCESS: Confirmation WhatsApp message delivered to Ratnadeep!")
else:
    print("FAILED: Message not delivered.")
    sys.exit(1)
