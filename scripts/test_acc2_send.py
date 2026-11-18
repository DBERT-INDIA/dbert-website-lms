import urllib.parse
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

session = Path(r"C:\Users\user\Desktop\aivara\aivara\.chrome_session_account2")
cand = {'name': 'Mahesh Gowda S S', 'phone': '919740033372', 'domain': 'AI Agent Development'}

lines = [
    f"Hello {cand['name']},",
    "",
    "Congratulations on your selection for the DBERT AI Agent Development Fellowship!",
    "",
    "⚡ URGENT: Your Batch Orientation Kickoff begins TODAY at 05:00 PM IST.",
    "",
    "To confirm your seat, activate your LMS engineering workspace, and receive your live meeting credentials, please complete your ₹499 caution deposit reconciliation on the official form:",
    "",
    "👉 Official Registration & Payment Form:",
    "https://docs.google.com/forms/d/e/1FAIpQLSdFxi9bft4POk4b3eXmp4aH71LmeQrJ0WzXA1bsIm37MalSIw/viewform?usp=header",
    "",
    "(The ₹499 caution deposit is 100% refundable upon milestone completion as per institutional terms.)",
    "",
    "You can also view your official Letter of Offer anytime at:",
    "https://lms.dbert.in/portal/offer",
    "",
    "Merchant UPI VPA for direct transfer: Q652429146@ybl (DBERT Admissions)",
    "If you have already made the transfer, simply reply to this message with your 12-digit UTR number or payment screenshot for instant activation.",
    "",
    "See you at 05:00 PM IST!",
    "",
    "Warm regards,",
    "DBERT Admissions Desk",
    "Digital Blinc Education Research and Technology (dbert.in)"
]
msg = "\n".join(lines)
encoded_msg = urllib.parse.quote(msg)
url = f"https://web.whatsapp.com/send?phone={cand['phone']}&text={encoded_msg}"

launch_args = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-infobars",
]

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(session),
        channel="chrome",
        headless=False,
        ignore_default_args=["--enable-automation"],
        args=launch_args,
    )
    browser.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    page = browser.pages[0] if browser.pages else browser.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=40000)
    
    sent = False
    for sec in range(1, 30):
        time.sleep(1)
        # Check send button
        send_btn = page.query_selector('button[aria-label="Send"], button[data-testid="send"], button[data-testid="compose-btn-send"], span[data-icon="send"]')
        if send_btn:
            time.sleep(1)
            send_btn.click()
            time.sleep(2)
            sent = True
            print("Successfully clicked Send button on Account 2!")
            break
            
        chat_input = page.query_selector('footer div[contenteditable="true"], div[role="textbox"]')
        if chat_input and chat_input.inner_text().strip():
            chat_input.focus()
            page.keyboard.press("Enter")
            time.sleep(2)
            sent = True
            print("Successfully pressed Enter in chat input on Account 2!")
            break
            
    print("Result:", "SENT" if sent else "FAILED")
    time.sleep(3)
    browser.close()
