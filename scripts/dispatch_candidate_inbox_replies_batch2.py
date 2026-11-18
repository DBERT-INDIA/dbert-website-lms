#!/usr/bin/env python3
"""
================================================================================
DBERT AUTONOMOUS CANDIDATE INBOX DISPATCHER (BATCH 2)
================================================================================
Processes and transmits tailored, verified responses to candidate inquiries 
across all DBERT Google Workspace accounts.
================================================================================
"""

import os
import sys
import smtplib
import ssl
import time
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from pathlib import Path
from urllib.parse import quote

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
DATA_DIR = ROOT_DIR / "data"
TRACKING_FILE = DATA_DIR / "inbox_action_dispatch_tracking.json"
LOG_FILE = DATA_DIR / "inbox_action_dispatch.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# SMTP Accounts Pool
SMTP_ACCOUNTS = {
    "abhinav.sharma@dbert.in": {
        "user": "abhinav.sharma@dbert.in",
        "pass": "rsupmvvvvwrsuxuh",
        "name": "Abhinav Sharma",
        "title": "Program Head & Project Mentor",
        "role": "DBERT Academic & Incubation Board"
    },
    "manoj.kumar@dbert.in": {
        "user": "manoj.kumar@dbert.in",
        "pass": "fnevtpseplwibckr",
        "name": "Manoj Kumar",
        "title": "Academic Lead & Admissions",
        "role": "DBERT Academic Operations"
    },
    "sandeep.bannu@dbert.in": {
        "user": "sandeep.bannu@dbert.in",
        "pass": "qtqzlmrynbcxvyjy",
        "name": "Sandeep Bannu",
        "title": "Technical Program Operations",
        "role": "DBERT Technical Fellowship Operations"
    },
    "contactus@dbert.in": {
        "user": "contactus@dbert.in",
        "pass": "llvmaajmrljpcwru",
        "name": "DBERT Admissions & Verification",
        "title": "Admissions & Candidate Verification Council",
        "role": "DBERT Academic Operations"
    },
    "pulkit.kunar@dbert.in": {
        "user": "pulkit.kunar@dbert.in",
        "pass": "vzefecwpggxuaztr",
        "name": "Pulkit Kumar",
        "title": "Admissions Desk & Candidate Support",
        "role": "DBERT Candidate Operations"
    }
}

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [INBOX-REPLY-B2] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def load_tracking() -> dict:
    if TRACKING_FILE.exists():
        try:
            with open(TRACKING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_tracking(state: dict):
    with open(TRACKING_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def build_whatsapp_buttons(cand_name: str, email: str, topic: str) -> str:
    adm_text = quote(f"Hi DBERT Admissions, I am {cand_name} ({email}). Query regarding: {topic}.")
    men_text = quote(f"Hi DBERT Mentorship, I am {cand_name} ({email}). Query regarding technical sprints for {topic}.")

    return f"""
    <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:16px 20px;margin:24px 0 20px;">
      <div style="font-size:11px;font-weight:700;color:#E2B96F;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;">
        1-Tap Dedicated WhatsApp Concierge
      </div>
      <div style="display:flex;gap:12px;flex-wrap:wrap;">
        <a href="https://wa.me/918192911360?text={adm_text}" target="_blank" rel="noopener" style="flex:1;min-width:200px;background:#25D366;color:#0B0F17;font-weight:700;font-size:12px;padding:10px 16px;border-radius:8px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;box-shadow:0 3px 10px rgba(37,211,102,0.25);">
          Admissions &amp; Payments (+91 81929 11360)
        </a>
        <a href="https://wa.me/918958006294?text={men_text}" target="_blank" rel="noopener" style="flex:1;min-width:200px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);color:#F0F4F8;font-weight:700;font-size:12px;padding:10px 16px;border-radius:8px;text-decoration:none;display:inline-flex;align-items:center;justify-content:center;gap:6px;">
          Sprints &amp; Mentorship (+91 89580 06294)
        </a>
      </div>
      <p style="font-size:11px;color:#8A9AB5;margin:8px 0 0;line-height:1.4;">
        Available Mon–Sat, 10:00 AM – 8:00 PM IST for instant verification, UTR confirmation, and technical mentorship.
      </p>
    </div>
    """

def wrap_email_html(sender: dict, recipient_name: str, content_html: str, wa_block: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
    <!-- Header -->
    <div style="background-color:#0E1626;padding:24px;text-align:center;border-bottom:2px solid #E2B96F;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:11px;letter-spacing:1px;margin-top:4px;text-transform:uppercase;">Sovereign Technical Incubation &amp; Research Platform</div>
    </div>

    <!-- Body -->
    <div style="padding:28px 26px;">
      <p style="font-size:15px;color:#F0F4F8;margin-top:0;">Dear <strong>{recipient_name}</strong>,</p>
      
      {content_html}

      {wa_block}

      <!-- Signoff -->
      <div style="margin-top:28px;padding-top:20px;border-top:1px solid rgba(255,255,255,0.08);">
        <p style="font-size:14px;color:#F0F4F8;margin:0 0 4px;font-weight:700;">Sincerely,</p>
        <p style="font-size:14px;color:#E2B96F;margin:0 0 2px;font-weight:800;">{sender['name']}</p>
        <p style="font-size:12px;color:#8A9AB5;margin:0 0 2px;">{sender['title']}</p>
        <p style="font-size:12px;color:#8A9AB5;margin:0 0 2px;">{sender['role']}</p>
        <p style="font-size:12px;color:#52627A;margin:4px 0 0;">DBERT (Digital Blinc Education Research and Technology) · <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a></p>
      </div>
    </div>

    <!-- Footer -->
    <div style="background-color:#0A0E14;padding:16px 24px;text-align:center;border-top:1px solid #1E2530;font-size:11px;color:#52627A;">
      DBERT Academic Board · Active Domain: <a href="https://dbert.in" style="color:#8A9AB5;text-decoration:none;">https://dbert.in</a><br>
      Admissions Helpline: +91 81929 11360 · Technical Mentorship: +91 89580 06294
    </div>
  </div>
 </body>
</html>
"""

# BATCH 2 CANDIDATE RESPONSES
CANDIDATE_RESPONSES = [
    {
        "id": "RESP-12-CHANCHAL",
        "email": "chanchalkumari728@gmail.com",
        "name": "Chanchal Kumari",
        "sender_account": "contactus@dbert.in",
        "subject": "Re: [URGENT] Action Required: Batch Kickoff — Review Offer Letter & Confirm Seat",
        "topic": "Offer Acceptance & Seat Confirmation",
        "plain_content": """Thank you for accepting the selection offer for the DBERT Technical Fellowship! We are thrilled to welcome you to the cohort.

To complete your seat confirmation and access your sprint sandbox:
1. Review and digitally sign your formal Letter of Offer:
   https://lms.dbert.in/portal/offer
2. Confirm your seat with the ₹499 refundable caution deposit:
   The ₹499 caution deposit reserves your dedicated compute sandbox and 1:1 mentor code reviews. It is 100% credited against your fellowship ledger or refunded upon milestone completion.
   Direct Payment: UPI VPA Q652429146@ybl (DBERT Admissions) or https://dbert.in/enroll/1999
3. Submit your 12-digit UPI UTR on the portal or share it with Admissions on WhatsApp (+91 81929 11360) for instant verification.

Once confirmed, your LMS dashboard will unlock your project roadmap and mentor details.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for confirming your acceptance of the <strong>DBERT Technical Fellowship Offer</strong>! We are thrilled to welcome you to the cohort.
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Mandatory Steps to Finalize Onboarding:</div>
          <ol style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>Review &amp; Sign Letter of Offer:</strong> Access your formal offer letter at <a href="https://lms.dbert.in/portal/offer" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal/offer</a></li>
            <li><strong>Seat Confirmation Deposit (₹499):</strong> Activate your dedicated cloud execution environment and mentor code reviews. This deposit is <strong>100% credited or refunded upon milestone completion</strong>.<br>
            UPI ID: <code>Q652429146@ybl</code> (DBERT Admissions) · Quick Link: <a href="https://dbert.in/enroll/1999" style="color:#E2B96F;font-weight:700;">https://dbert.in/enroll/1999</a></li>
            <li><strong>Instant UTR Verification:</strong> Submit your 12-digit UPI UTR on the portal or message Admissions via WhatsApp (+91 81929 11360).</li>
          </ol>
        </div>
        """
    },
    {
        "id": "RESP-13-TRISHAM",
        "email": "trishamgupta43@gmail.com",
        "name": "Trisham Gupta",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: [URGENT] Action Required: Batch Kickoff — Review Offer Letter & Confirm Seat",
        "topic": "Seat Confirmation & Payment Steps",
        "plain_content": """Thank you for your update regarding your offer review and seat confirmation!

Here are the direct instructions to finalize your registration:
1. Seat Confirmation Payment:
   Amount: ₹499 (100% refundable upon milestone delivery)
   UPI VPA: Q652429146@ybl (DBERT Admissions)
   Online Portal: https://dbert.in/enroll/1999
2. Record Your Submission:
   Once the transaction is complete, please record the 12-digit UPI UTR on your offer dashboard (https://lms.dbert.in/portal/offer) or send the screenshot directly to our WhatsApp Admissions Desk at +91 81929 11360.

Your LMS learning dashboard, sprint roadmap, and GitHub access will be activated immediately upon confirmation.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for confirming that you have reviewed your offer and are completing the seat confirmation!
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Instant Seat Confirmation Details:</div>
          <p style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0 0 10px;">
            <strong>Caution Deposit:</strong> ₹499 (100% refundable upon project delivery)<br>
            <strong>Official UPI VPA:</strong> <code>Q652429146@ybl</code> (DBERT Admissions)<br>
            <strong>Portal Link:</strong> <a href="https://dbert.in/enroll/1999" style="color:#E2B96F;font-weight:700;">https://dbert.in/enroll/1999</a>
          </p>
          <p style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;">
            After completing payment, submit your 12-digit UTR at <a href="https://lms.dbert.in/portal/offer" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal/offer</a> or route it to Admissions on WhatsApp (+91 81929 11360).
          </p>
        </div>
        """
    },
    {
        "id": "RESP-14-SANJAI",
        "email": "sanjaikumar.p.k2006@gmail.com",
        "name": "Sanjai Kumar",
        "sender_account": "contactus@dbert.in",
        "subject": "Re: Requesting info about the internship — Caution Deposit & Offer Letter Details",
        "topic": "AI Agent Caution Deposit Clarification",
        "plain_content": """Thank you for reaching out regarding your selection for the AI Agent Development Fellowship! We are delighted to clarify your questions:

1. Why is the ₹499 Caution Deposit Required?
DBERT does NOT charge any tuition or course fees for the fellowship track. The ₹499 caution deposit is an operational commitment to reserve dedicated cloud sandbox compute (Ollama, LangGraph, and GPU containers) and eliminate inactive ghost registrations.

2. Is the Deposit Refundable?
Yes, 100%. Upon completion and submission of your sprint milestone deliverables, the entire ₹499 is refunded back to your source account or credited to your fellowship wallet.

3. Viewing Your Offer Letter First:
You can review your complete, formal Letter of Offer in preview mode right now BEFORE making any payment.
Simply visit: https://lms.dbert.in/portal/offer

4. ₹5,000 Technical Contribution Stipend:
Upon completing your project capstone and technical contributions, you remain fully eligible for the ₹5,000 production milestone stipend.

Feel free to connect directly with Admissions on WhatsApp at +91 81929 11360 for any further questions.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reaching out regarding your selection for the <strong>AI Agent Development Fellowship</strong>. We are very glad to clarify the financial and onboarding terms:
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Clarification on Program Terms &amp; Deposit:</div>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>Zero Tuition:</strong> DBERT does not charge tuition fees for the fellowship program.</li>
            <li><strong>Purpose of ₹499 Deposit:</strong> The refundable caution deposit secures dedicated cloud GPU sandboxes (Ollama, LangChain, CrewAI) and prevents ghost seat reservations.</li>
            <li><strong>100% Refundable:</strong> The deposit is fully refunded or credited to your wallet upon submitting your sprint deliverables.</li>
            <li><strong>Review Offer Letter First:</strong> You can read your full, formal Letter of Offer in preview mode before making any payment: <a href="https://lms.dbert.in/portal/offer" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal/offer</a></li>
            <li><strong>₹5,000 Stipend Rights:</strong> You remain fully eligible to unlock the ₹5,000 production contribution stipend upon project completion.</li>
          </ul>
        </div>
        """
    },
    {
        "id": "RESP-15-SIVA",
        "email": "svsk798@gmail.com",
        "name": "Siva Mandapati",
        "sender_account": "contactus@dbert.in",
        "subject": "Re: DBERT Application Update: Full Stack Development Fellowship Selection & Offer Terms",
        "topic": "Full Stack Caution Deposit & Offer Access",
        "plain_content": """Thank you for contacting the DBERT Admissions Council regarding your selection for the Full Stack Development Fellowship.

We confirm that your selection is 100% genuine and verified on our sovereign platform (https://dbert.in).

Regarding your questions:
1. Reviewing Your Formal Offer Letter:
You can review and read your full, formal Letter of Offer in preview mode right now BEFORE making any payment:
Visit: https://lms.dbert.in/portal/offer
Login with your registered email: svsk798@gmail.com

2. Clarification on the ₹499 Caution Deposit:
DBERT does not charge any tuition or course fees. The ₹499 caution deposit is an operational commitment to reserve cloud deployment servers (Docker, PostgreSQL, and AWS sandboxes) for your projects. This deposit is 100% REFUNDABLE upon completing your sprint milestones.

3. Next Steps:
Review your appointment terms at https://lms.dbert.in/portal/offer. When you are ready to confirm your seat, you can submit the ₹499 deposit via UPI (VPA: Q652429146@ybl) and enter the 12-digit UTR on the portal.

Admissions Helpline: +91 81929 11360 (WhatsApp).""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for contacting the DBERT Admissions Council regarding your selection for the <strong>Full Stack Development Fellowship</strong>.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          We confirm that your application and selection are <strong>100% genuine and verified</strong> on our sovereign platform (<a href="https://dbert.in" style="color:#E2B96F;">https://dbert.in</a>).
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Offer Letter Access &amp; Deposit Clarification:</div>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>Read Offer Letter First:</strong> You can view and inspect your full, formal Letter of Offer in preview mode before paying anything: <a href="https://lms.dbert.in/portal/offer" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal/offer</a></li>
            <li><strong>Caution Deposit Purpose:</strong> The ₹499 deposit secures cloud server sandboxes and prevents seat wastage. It is <strong>100% refundable</strong> upon project milestone delivery.</li>
            <li><strong>Seat Confirmation:</strong> Once reviewed, finalize your seat confirmation on the portal or via UPI VPA <code>Q652429146@ybl</code>.</li>
          </ul>
        </div>
        """
    },
    {
        "id": "RESP-16-ARYAN",
        "email": "aryanbhakuni2006@gmail.com",
        "name": "Aryan Bhakuni",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: DBERT Milestone Roadmap: Technical Contribution Approved & Published — ₹5,000 Stipend Release",
        "topic": "Article Published & Stipend Release Procedure",
        "plain_content": """Dear Aryan,

Congratulations! We have excellent news regarding your technical contribution.

Your comprehensive engineering and market intelligence project has been formally reviewed, approved, and PUBLISHED on the DBERT sovereign platform:
Title: Alkame NIFTY 50: Quantitative Market Intelligence & Educational Analytics Platform
Live Sovereign URL: https://dbert.in/blog/alkame-nifty-50-quantitative-market-intelligence-platform

To complete the release of your ₹5,000 technical contribution stipend:
1. Ensure your payout UPI ID is linked and verified on your LMS profile:
   https://lms.dbert.in/stipend/tasks
2. The Academic & Review Board has verified your GitHub repository and live deployment. The stipend disbursement queue will credit your wallet/linked account in the current payment cycle.

Thank you for your high-caliber contribution to the DBERT engineering ecosystem!""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Congratulations, <strong>Aryan</strong>! We have fantastic news regarding your technical contribution.
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">★ Technical Contribution Formally Published:</div>
          <p style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0 0 10px;">
            <strong>Title:</strong> Alkame NIFTY 50: Quantitative Market Intelligence &amp; Educational Analytics Platform<br>
            <strong>Live Canonical Article:</strong> <a href="https://dbert.in/blog/alkame-nifty-50-quantitative-market-intelligence-platform" style="color:#E2B96F;font-weight:700;">https://dbert.in/blog/alkame-nifty-50-quantitative-market-intelligence-platform</a>
          </p>
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:6px;">Next Step for ₹5,000 Stipend Release:</div>
          <ol style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li>Confirm your registered UPI ID at <a href="https://lms.dbert.in/stipend/tasks" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/stipend/tasks</a></li>
            <li>Your milestone submission has been reconciled by the evaluation board, and your payout is queued for processing in this cycle.</li>
          </ol>
        </div>
        """
    },
    {
        "id": "RESP-17-VINAY",
        "email": "gurkavinay22@gmail.com",
        "name": "Gurka Vinay Kumar Reddy",
        "sender_account": "contactus@dbert.in",
        "subject": "Re: Missing ₹5,000 Stipend Disbursement – Credential ID: CERT-DBERT-2026-AIML-169",
        "topic": "₹5,000 Stipend Payout Reconciliation Update",
        "plain_content": """Dear Gurka Vinay Kumar Reddy,

Thank you for your follow-up message regarding your ₹5,000 production milestone stipend for Credential ID: CERT-DBERT-2026-AIML-169.

We would like to reassure you that your contribution and credentials are fully recognized and secure:
1. Your credential is authenticated on our sovereign platform:
   https://dbert.in/verify/CERT-DBERT-2026-AIML-169
2. Your linked UPI ID (9014147134@upi) is registered in our accounting ledger.
3. The Finance Council executes verified stipend disbursements in bi-weekly automated batches. Your file is in the active reconciliation batch for processing.

You will receive an automated transaction notification with the 12-digit banking UTR number as soon as the bank relay confirms execution.

If you have any urgent queries, our Admissions & Accounts Desk is available at +91 81929 11360 (WhatsApp).""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Dear <strong>Gurka Vinay Kumar Reddy</strong>,
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for following up regarding your <strong>₹5,000 production milestone stipend</strong> for Credential ID: <code>CERT-DBERT-2026-AIML-169</code>.
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Payout Reconciliation Status:</div>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>Verified Credential:</strong> Confirmed on sovereign registry (<a href="https://dbert.in/verify/CERT-DBERT-2026-AIML-169" style="color:#E2B96F;font-weight:700;">dbert.in/verify/CERT-DBERT-2026-AIML-169</a>).</li>
            <li><strong>Linked UPI ID:</strong> <code>9014147134@upi</code> is validated and securely encrypted in the ledger.</li>
            <li><strong>Batch Processing:</strong> Finance releases disbursements in scheduled cycles. Your file is queued in the current payment release. The banking UTR will be emailed immediately upon execution.</li>
          </ul>
        </div>
        """
    },
    {
        "id": "RESP-18-BHARGAVI",
        "email": "bhargavi13032007@gmail.com",
        "name": "Bhargavi Poola",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: Clarification Regarding LinkedIn Profile Linking and Domain Specialization – Cohort 2026",
        "topic": "Domain Confirmation & Incubation Seat Confirmed",
        "plain_content": """Dear Bhargavi Poola,

Thank you for reaching out regarding your domain specialization and LinkedIn profile linking!

We are pleased to provide you with complete clarity:
1. Domain Specialization Confirmed:
Your track is officially registered as Full Stack Web Development (Credential ID: CERT-DBERT-2026-FSD-156). Any earlier automated email referencing Data Analyst was an automated system template placeholder; your permanent record is 100% Full Stack Web Development.

2. Seat & Enrollment Fully Confirmed:
Your incubation balance (₹1,500) has been verified and reconciled with UTR 679862090077 (Ref: DBERT-ENR-703685-TYN6).
Your live batch countdown is running at:
https://dbert.in/enroll/1999?email=bhargavi13032007@gmail.com

3. LinkedIn Profile Linking:
To add your credential to LinkedIn:
- Open your LinkedIn profile -> Add Profile Section -> Recommended -> Add Licenses & Certifications
- Name: Full Stack Web Development Fellow
- Issuing Organization: DBERT (Digital Blinc Education Research and Technology)
- Credential URL: https://dbert.in/verify/CERT-DBERT-2026-FSD-156
- Credential ID: CERT-DBERT-2026-FSD-156

Our Mentorship team (+91 89580 06294) will support you throughout your sprints!""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Dear <strong>Bhargavi Poola</strong>,
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reaching out! We are delighted to confirm your domain details and enrollment status:
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">★ Your Confirmed Enrollment Dossier:</div>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>Domain Track:</strong> Confirmed as <strong>Full Stack Web Development</strong> (Credential ID: <code>CERT-DBERT-2026-FSD-156</code>).</li>
            <li><strong>Seat Confirmed:</strong> Your enrollment fee is reconciled in full (UTR: <code>679862090077</code>). Check your live countdown at <a href="https://dbert.in/enroll/1999?email=bhargavi13032007@gmail.com" style="color:#E2B96F;font-weight:700;">dbert.in/enroll/1999</a></li>
            <li><strong>LinkedIn 1-Click Verification:</strong> Add your credential to your LinkedIn profile with Credential URL: <a href="https://dbert.in/verify/CERT-DBERT-2026-FSD-156" style="color:#E2B96F;font-weight:700;">https://dbert.in/verify/CERT-DBERT-2026-FSD-156</a></li>
          </ul>
        </div>
        """
    },
    {
        "id": "RESP-19-OM",
        "email": "omvinayak94@gmail.com",
        "name": "Om Vinayak",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: payment done - Certificate & LOR Application Form 299",
        "topic": "₹299 Verification Payment Confirmed",
        "plain_content": """Dear Om Vinayak,

Thank you for confirming your payment submission for the Certificate & Letter of Recommendation (LOR) Verification Form!

Our Academic Operations & Verification Council has received your transaction details. The credential review process consists of:
1. Turnitin Originality Scan & Plagiarism Check
2. Academic 9-Dimension Rubric Evaluation Scoring
3. Generation of official cryptographically signed 3-document credential packet:
   - Certificate of Completion
   - Academic Project Evaluation
   - Executive Letter of Recommendation (LOR) signed by Program Head

Your verified credential packet will be delivered directly to your inbox and registered on the sovereign verification engine (https://dbert.in/verify).

Admissions Desk: +91 81929 11360 (WhatsApp).""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Dear <strong>Om Vinayak</strong>,
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for confirming your payment submission for the <strong>Certificate &amp; LOR Verification Form</strong>!
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Credential Processing Status:</div>
          <p style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0 0 8px;">
            Your transaction proof has been submitted to the Academic Operations Council. The evaluation team is finalizing your:
          </p>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li>Turnitin Originality &amp; Similarity Validation Seal</li>
            <li>9-Dimension Academic Evaluation Rubric</li>
            <li>Executive Letter of Recommendation (LOR) signed by Program Head</li>
          </ul>
          <p style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:8px 0 0;">
            The complete 3-document credential packet will be delivered to your email and permanently verified at <a href="https://dbert.in/verify" style="color:#E2B96F;font-weight:700;">https://dbert.in/verify</a>.
          </p>
        </div>
        """
    },
    {
        "id": "RESP-20-KUNDAN",
        "email": "kundankumhar966@gmail.com",
        "name": "Kundan Kumhar",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: Official Internship Credential Packet: Session Materials & Curriculum Access [CERT-DBERT-2026-FSD-056]",
        "topic": "Session PDF & Curriculum Materials",
        "plain_content": """Dear Kundan Kumhar,

Thank you for reaching out regarding the session materials for Full Stack Web Development (Credential ID: CERT-DBERT-2026-FSD-056).

You can access all session notes, curriculum modules, and architecture guides directly on the LMS portal:
1. Course Curriculum & Notes:
   https://lms.dbert.in/courses
2. Your Verified Credential Dossier:
   https://dbert.in/verify/CERT-DBERT-2026-FSD-056

If you need any specific technical handbook or project repository access, please let us know or message Mentorship on WhatsApp at +91 89580 06294.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Dear <strong>Kundan Kumhar</strong>,
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reaching out regarding session materials for your <strong>Full Stack Web Development</strong> credential (<code>CERT-DBERT-2026-FSD-056</code>).
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Curriculum &amp; Session Access:</div>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>LMS Course Curriculum &amp; Modules:</strong> <a href="https://lms.dbert.in/courses" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/courses</a></li>
            <li><strong>Verified Public Credential:</strong> <a href="https://dbert.in/verify/CERT-DBERT-2026-FSD-056" style="color:#E2B96F;font-weight:700;">dbert.in/verify/CERT-DBERT-2026-FSD-056</a></li>
          </ul>
        </div>
        """
    },
    {
        "id": "RESP-21-ABHISHEK",
        "email": "abhirapolu08@gmail.com",
        "name": "Rapolu Abhishek",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: Official Internship Credential Packet: Stipend Milestone Status [CERT-DBERT-2026-AIML-014]",
        "topic": "Certificate ID Alignment & Stipend Milestone",
        "plain_content": """Dear Rapolu Abhishek,

Thank you for reaching out regarding your credential packet and stipend procedure.

We are glad to clarify both questions:
1. Certificate ID Alignment:
Your permanent cryptographic credential ID is CERT-DBERT-2026-AIML-014. It is officially verified on our sovereign registry:
https://dbert.in/verify/CERT-DBERT-2026-AIML-014
Any temporary provisional ID previously generated has been superseded by this official credential. You can use CERT-DBERT-2026-AIML-014 for all employer verifications and LinkedIn certifications.

2. ₹5,000 Stipend Qualification:
The Google Form you submitted registered your initial payout intent. To complete the automated stipend release, ensure you have completed your 4 milestone gates and verified your UPI ID on LMS:
https://lms.dbert.in/stipend/tasks

Our team is reviewing the active cohort submissions and will update your dossier accordingly.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Dear <strong>Rapolu Abhishek</strong>,
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reaching out! We are glad to clarify your credential ID and stipend status:
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Credential Alignment &amp; Stipend Roadmap:</div>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>Official Credential ID:</strong> Your active cryptographic credential is <code>CERT-DBERT-2026-AIML-014</code> (<a href="https://dbert.in/verify/CERT-DBERT-2026-AIML-014" style="color:#E2B96F;font-weight:700;">dbert.in/verify/CERT-DBERT-2026-AIML-014</a>). This supersedes any earlier temporary ID.</li>
            <li><strong>₹5,000 Stipend Release:</strong> Ensure your UPI payout details are verified at <a href="https://lms.dbert.in/stipend/tasks" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/stipend/tasks</a> to receive your milestone disbursement.</li>
          </ul>
        </div>
        """
    },
    {
        "id": "RESP-22-AMAN",
        "email": "aman.garg1861@gmail.com",
        "name": "Aman Garg",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: DBERT Internship Verification: Next Steps for Verified Credential [CERT-DBERT-2026-FSD-117]",
        "topic": "Certificate Next Steps & Recruiter Visibility",
        "plain_content": """Dear Aman Garg,

Thank you for reaching out! Since you already have your Certificate of Completion (CERT-DBERT-2026-FSD-117), here are the most valuable next steps to maximize your career impact:

1. 1-Click LinkedIn Credential Integration:
Add your verified credential to your LinkedIn profile under "Licenses & Certifications":
- Name: Full Stack Web Development Fellow
- Issuing Organization: DBERT (Digital Blinc Education Research and Technology)
- Credential URL: https://dbert.in/verify/CERT-DBERT-2026-FSD-117

2. Pre-Vetted Engineers Directory:
Your profile is featured on our sovereign talent directory accessed by hiring partners:
https://dbert.in/verify/directory

3. Technical Contribution & ₹5,000 Stipend:
If you would like to contribute technical articles, code repositories, or mentor junior fellows, you can unlock our ₹5,000 production contribution stipend at:
https://lms.dbert.in/stipend/tasks

Admissions Helpline: +91 81929 11360 (WhatsApp).""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Dear <strong>Aman Garg</strong>,
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Since you already hold your official <strong>Certificate of Completion</strong> (<code>CERT-DBERT-2026-FSD-117</code>), here are the recommended next steps:
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Next Actions for Your Credential:</div>
          <ol style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>LinkedIn Showcase:</strong> Add your verified badge to LinkedIn using your public link: <a href="https://dbert.in/verify/CERT-DBERT-2026-FSD-117" style="color:#E2B96F;font-weight:700;">dbert.in/verify/CERT-DBERT-2026-FSD-117</a></li>
            <li><strong>Recruiter Directory:</strong> View your listing on the Pre-Vetted Talent Directory: <a href="https://dbert.in/verify/directory" style="color:#E2B96F;font-weight:700;">dbert.in/verify/directory</a></li>
            <li><strong>₹5,000 Stipend Contributions:</strong> Submit advanced open-source technical projects on <a href="https://lms.dbert.in/stipend/tasks" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/stipend/tasks</a> to earn production stipends.</li>
          </ol>
        </div>
        """
    },
    {
        "id": "RESP-23-GOUTHAMI",
        "email": "gouthamigouthu06@gmail.com",
        "name": "Gouthami N A",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: [URGENT] Action Required: Batch Kickoff — Program Structure & Caution Deposit Clarification",
        "topic": "Caution Deposit vs Stipend Structure Clarification",
        "plain_content": """Dear Gouthami N A,

We understand your question and are happy to clarify how the DBERT Fellowship structure works:

1. Zero Tuition:
DBERT never charges tuition fees for this internship fellowship. The training and mentorship are free.

2. Why the ₹499 Caution Deposit?
In previous batches, many candidates reserved seats but never attended sprints, blocking server GPU sandboxes and mentor slots from serious students. The ₹499 caution deposit is an operational commitment deposit that is 100% REFUNDABLE upon completing your sprint deliverables.

3. The ₹5,000 Stipend:
Stipends are performance-based compensation awarded to fellows for delivering genuine software projects and technical contributions during the fellowship.

4. Inspect Your Offer Letter First:
You can read the entire formal Letter of Offer before making any decision:
https://lms.dbert.in/portal/offer

If you have any doubts, feel free to chat with our Admissions team on WhatsApp at +91 81929 11360.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Dear <strong>Gouthami N A</strong>,
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          We understand your question and want to ensure complete transparency regarding the fellowship model:
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Fellowship Model &amp; Refund Guarantee:</div>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li><strong>Zero Tuition:</strong> DBERT does not charge tuition fees for the fellowship track.</li>
            <li><strong>Caution Deposit Purpose:</strong> The ₹499 caution deposit reserves your cloud sandbox and eliminates inactive ghost registrations. It is <strong>100% refunded</strong> upon project submission.</li>
            <li><strong>₹5,000 Contribution Stipend:</strong> Awarded upon delivery of technical projects and milestones.</li>
            <li><strong>Inspect Offer Letter:</strong> You can read your full appointment terms before deciding: <a href="https://lms.dbert.in/portal/offer" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal/offer</a></li>
          </ul>
        </div>
        """
    }
]

def send_reply(cand: dict, live: bool = False):
    sender = SMTP_ACCOUNTS.get(cand["sender_account"])
    if not sender:
        log(f"Sender account {cand['sender_account']} not found in pool!")
        return False

    wa_block = build_whatsapp_buttons(cand["name"], cand["email"], cand["topic"])
    html_body = wrap_email_html(sender, cand["name"], cand["html_content"], wa_block)

    msg = MIMEMultipart("alternative")
    msg["From"] = f"{sender['name']} <{sender['user']}>"
    msg["To"] = cand["email"]
    msg["Subject"] = cand["subject"]
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    msg["Reply-To"] = sender["user"]

    part_text = MIMEText(cand["plain_content"], "plain", "utf-8")
    part_html = MIMEText(html_body, "html", "utf-8")
    msg.attach(part_text)
    msg.attach(part_html)

    if not live:
        log(f"[DRY-RUN] Would send reply to {cand['name']} <{cand['email']}> via {sender['user']}")
        return True

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=20) as server:
            server.login(sender["user"], sender["pass"])
            server.sendmail(sender["user"], [cand["email"]], msg.as_string())
        log(f"SENT -> {cand['name']} <{cand['email']}> via {sender['user']}")
        return True
    except Exception as e:
        log(f"FAILED -> {cand['name']} <{cand['email']}> via {sender['user']}: {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="DBERT Candidate Inbox Reply Dispatcher (Batch 2)")
    parser.add_argument("--live", action="store_true", help="Execute real live sending")
    parser.add_argument("--delay", type=int, default=15, help="Delay between dispatches in seconds")
    args = parser.parse_args()

    state = load_tracking()

    print("=" * 76)
    print("  DBERT AUTONOMOUS INBOX ACTION DISPATCHER (BATCH 2)")
    print(f"  Mode: {'LIVE DISPATCH' if args.live else 'DRY RUN'}")
    print(f"  Candidates in Queue: {len(CANDIDATE_RESPONSES)}")
    print("=" * 76)

    dispatched = 0
    for idx, cand in enumerate(CANDIDATE_RESPONSES, 1):
        cand_id = cand["id"]
        if cand_id in state and state[cand_id].get("status") == "SENT":
            print(f"[{idx}/{len(CANDIDATE_RESPONSES)}] ALREADY SENT -> {cand['name']} <{cand['email']}> (Skipping)")
            continue

        print(f"\n[{idx}/{len(CANDIDATE_RESPONSES)}] Processing -> {cand['name']} <{cand['email']}> ({cand['topic']})")
        success = send_reply(cand, live=args.live)
        if success and args.live:
            state[cand_id] = {
                "name": cand["name"],
                "email": cand["email"],
                "sender": cand["sender_account"],
                "subject": cand["subject"],
                "topic": cand["topic"],
                "status": "SENT",
                "dispatched_at": datetime.now().isoformat()
            }
            save_tracking(state)
            dispatched += 1
            if idx < len(CANDIDATE_RESPONSES):
                time.sleep(args.delay)
        elif not args.live:
            dispatched += 1

    print("\n" + "=" * 76)
    print(f"  BATCH 2 DISPATCH COMPLETE: {dispatched} replies processed.")
    print("=" * 76)

if __name__ == "__main__":
    main()
