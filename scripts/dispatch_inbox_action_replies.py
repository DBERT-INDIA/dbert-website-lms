#!/usr/bin/env python3
"""
================================================================================
DBERT AUTONOMOUS INBOX ACTION DISPATCHER
================================================================================
Processes and transmits tailored, verified responses to candidate inquiries 
across DBERT Google Workspace accounts (abhinav.sharma, manoj.kumar, sandeep.bannu).

Features:
- Thread-aware reply headers (In-Reply-To, References)
- Mobile-responsive, high-deliverability single-card HTML + clean UTF-8 plain text
- Multi-account SMTP pool rotation based on incoming inquiry ownership
- 15-second anti-spam rate control
- Atomic JSON state tracking and chronological audit logging
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

# SMTP Account Pool
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
    }
}

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [INBOX-ACTION] {msg}"
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

# 11 CANDIDATE DEFINITIONS & RESPONSES
CANDIDATE_RESPONSES = [
    {
        "id": "RESP-01-SURAJ",
        "email": "surajup5756@gmail.com",
        "name": "Suraj Upadhyay",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: DBERT Application Update: AI Agent Development Sprint Onboarding & Portal Access",
        "topic": "AI Agent Development Portal Access",
        "plain_content": """Thank you for reaching out regarding your selection confirmation for the AI Agent Development Fellowship (Application Ref: DBERT-APP-2026-S4627).

We are delighted to confirm that your seat reservation is approved for the upcoming sprint starting Monday, 16 November 2026 at 06:00 PM IST.

To log in and access your portal dashboard:
1. Visit the DBERT LMS portal: https://lms.dbert.in/portal (or https://lms.dbert.in/apply)
2. Enter your registered email: surajup5756@gmail.com
3. If this is your first time signing in, simply click "Forgot Password" or use your initial password to access your dedicated sprint roadmap and sandbox.

Regarding Seat Confirmation:
The ₹499 caution deposit secures your dedicated cloud compute sandbox (Ollama, LangGraph, CrewAI execution containers) and 1:1 mentor code reviews. It is 100% credited towards your fellowship ledger or refunded upon milestone completion.
Payment Link: https://dbert.in/enroll/1999 (UPI VPA: Q652429146@ybl)

Our Admissions Concierge is available on WhatsApp at +91 81929 11360 for any instant setup assistance.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reaching out regarding your selection confirmation for the <strong>AI Agent &amp; LLM Systems Fellowship</strong> (Application Ref: <code>DBERT-APP-2026-S4627</code>).
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          We are pleased to confirm that your seat reservation is officially approved for the sprint kickoff starting <strong>Monday, 16 November 2026 at 06:00 PM IST</strong>.
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:8px;">Portal Access &amp; Login Instructions:</div>
          <ol style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:20px;">
            <li>Visit the LMS portal: <a href="https://lms.dbert.in/portal" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal</a></li>
            <li>Login with your registered email: <strong>surajup5756@gmail.com</strong></li>
            <li>If you haven't set a password yet, click <strong>"Forgot Password"</strong> or use the activation link to set your secure password immediately.</li>
          </ol>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          <strong>Committed Seat Caution Deposit:</strong><br>
          The committed caution deposit (₹499) activates your dedicated cloud execution environment and mentor code reviews. It is <strong>100% credited against your fellowship ledger or refunded upon milestone completion</strong>.<br>
          Direct Enrollment &amp; UPI Link: <a href="https://dbert.in/enroll/1999" style="color:#E2B96F;font-weight:700;">https://dbert.in/enroll/1999</a> (UPI: <code>Q652429146@ybl</code>).
        </p>
        """
    },
    {
        "id": "RESP-02-VAISHNAVI",
        "email": "gundetivaishnavi634@gmail.com",
        "name": "Gundeti Vaishnavi",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: DBERT Application Update: Selection Confirmed for 16 Nov Sprint Cohort [DBERT-APP-2026-S4984]",
        "topic": "Full Stack Caution Deposit Clarification",
        "plain_content": """Thank you for reaching out regarding your selection for the Full Stack Development Fellowship (Reference: DBERT-APP-2026-S4984) starting Monday, 16 November 2026.

We are very happy to clarify the seat confirmation deposit:

1. Why is the ₹499 Caution Deposit Required?
Because our engineering cohorts operate with dedicated mentor-intern ratios and provisioned cloud sandboxes, we require a nominal ₹499 caution deposit to confirm active commitment and prevent unutilized reservations.

2. 100% Credited / Refundable:
The ₹499 caution deposit is 100% credited towards your program ledger upon enrollment, or refunded upon successful completion of your fellowship milestones. There is zero hidden charge.

3. How to Confirm Your Seat:
- Pay ₹499 via UPI to VPA: Q652429146@ybl (DBERT Admissions)
- Or complete 1-tap verification at: https://dbert.in/enroll/1999
- Share your 12-digit UTR on Admissions WhatsApp: +91 81929 11360

We look forward to welcoming you to the 16 Nov sprint!""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for following up regarding your selection for the <strong>Full Stack Web Development Fellowship</strong> (Reference: <code>DBERT-APP-2026-S4984</code>) kicking off on <strong>Monday, 16 November 2026</strong>.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          We are pleased to provide full clarity regarding the committed seat caution deposit:
        </p>

        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:16px 20px;margin:18px 0;">
          <h4 style="margin:0 0 8px;color:#E2B96F;font-size:14px;">1. Purpose of the ₹499 Caution Deposit</h4>
          <p style="margin:0 0 12px;font-size:13px;color:#C8D3E0;line-height:1.5;">
            Our production sprints feature direct mentor reviews, live code inspection, and individual workspace infrastructure. The ₹499 deposit confirms your intent to actively participate and prevents reserved cohort slots from going unutilized.
          </p>

          <h4 style="margin:0 0 8px;color:#E2B96F;font-size:14px;">2. 100% Credited / Refundable Policy</h4>
          <p style="margin:0;font-size:13px;color:#C8D3E0;line-height:1.5;">
            The ₹499 is <strong>strictly a caution deposit</strong>. It is credited in full towards your program balance or refunded upon fellowship milestone completion.
          </p>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          <strong>Steps to Finalize Your Seat:</strong><br>
          1. Complete payment via UPI to merchant VPA: <code>Q652429146@ybl</code> (DBERT Admissions).<br>
          2. Submit your transaction UTR at: <a href="https://dbert.in/enroll/1999" style="color:#E2B96F;font-weight:700;">https://dbert.in/enroll/1999</a>.<br>
          3. Send your UTR to Admissions WhatsApp (<strong>+91 81929 11360</strong>) for instant confirmation.
        </p>
        """
    },
    {
        "id": "RESP-03-KAVANA",
        "email": "kavana200518@gmail.com",
        "name": "C S Kavana",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: DBERT Application Update: Selection Confirmed — Action Required to Confirm Seat [DBERT-APP-2026-S4861]",
        "topic": "SOC Analysis & Threat Defense Sprint Details",
        "plain_content": """Thank you for your interest in the SOC Analysis & Threat Monitoring Fellowship (Application Ref: DBERT-APP-2026-S4861).

Here are the details you requested regarding the sprint structure:

1. Commitment & Schedule:
The fellowship is structured for approximately 10 hours per week with flexible asynchronous task schedules, making it fully compatible with your college coursework. Live mentor reviews and walkthroughs take place on weekends.

2. Practical Curriculum:
You will work on real-world threat defense scenarios: network packet analysis with Wireshark, SIEM alert triage, log correlation, and vulnerability audits against the OWASP Top 10.

3. Seat Confirmation:
The ₹499 committed caution deposit reserves your seat in the 16 November cohort. It is 100% credited against your ledger or refunded upon milestone completion.
Payment portal: https://dbert.in/enroll/1999 (UPI VPA: Q652429146@ybl)

Admissions Helpline: +91 81929 11360
Technical Mentorship: +91 89580 06294""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for writing to us regarding the <strong>SOC Analysis &amp; Threat Defense Fellowship</strong> (Application Ref: <code>DBERT-APP-2026-S4861</code>).
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Here are the program details to help you prepare for the sprint kickoff:
        </p>

        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:16px 20px;margin:18px 0;">
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:18px;">
            <li><strong>Weekly Hours:</strong> 10 hours per week (Flexible &amp; asynchronous to accommodate college classes).</li>
            <li><strong>Practical Projects:</strong> Hands-on SIEM monitoring, Wireshark packet capture analysis, SOC alert triage, and application security auditing.</li>
            <li><strong>Mentorship &amp; Reviews:</strong> Senior security engineers conduct weekly code and report reviews.</li>
            <li><strong>Stipend &amp; Verification:</strong> Eligible for verified completion credentials, LOR, and performance milestones.</li>
          </ul>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          <strong>Seat Reservation:</strong> To lock your seat for the 16 Nov kickoff, complete your ₹499 committed deposit at <a href="https://dbert.in/enroll/1999" style="color:#E2B96F;font-weight:700;">https://dbert.in/enroll/1999</a> (UPI: <code>Q652429146@ybl</code>).
        </p>
        """
    },
    {
        "id": "RESP-04-SUMANJALI",
        "email": "chinnamgarisumanjali13@gmail.com",
        "name": "Chinnamgari Sumanjali",
        "sender_account": "sandeep.bannu@dbert.in",
        "subject": "Re: Clarification Required Regarding ₹499 Internship Seat Deposit",
        "topic": "Caution Deposit Clarification",
        "plain_content": """Dear Chinnamgari Sumanjali,

Thank you for contacting DBERT Operations regarding your selection for the Remote Internship cohort starting 16 November 2026.

We understand your question regarding the ₹499 caution deposit and are glad to clarify:

1. What is the ₹499 Deposit?
It is a refundable caution deposit that reserves your dedicated slot and sets up your personalized engineering workspace. It ensures that candidates who receive an offer actively attend, preventing batch spots from going unutilized.

2. Refund & Credit Policy:
The ₹499 is 100% credited towards your fellowship ledger upon enrollment, or refunded upon successful completion of your program milestones. It is not an uncredited administrative charge.

3. How to Complete Confirmation:
- UPI VPA: Q652429146@ybl (DBERT Admissions)
- Portal: https://dbert.in/enroll/1999
- WhatsApp: +91 81929 11360

We look forward to having you in the cohort!""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reaching out regarding your selection for the <strong>Remote Technical Fellowship</strong> starting <strong>16 November 2026</strong>.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          We are pleased to provide complete clarity on the ₹499 caution deposit:
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <p style="margin:0 0 8px;font-size:13px;color:#F0F4F8;font-weight:700;">Committed Caution Deposit Policy:</p>
          <p style="margin:0;font-size:13px;color:#C8D3E0;line-height:1.5;">
            The ₹499 deposit secures your reserved seat and provisions your LMS workspace. It is <strong>100% credited towards your program ledger or refunded upon milestone completion</strong>.
          </p>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          You can confirm your seat at: <a href="https://dbert.in/enroll/1999" style="color:#E2B96F;font-weight:700;">https://dbert.in/enroll/1999</a> or via UPI <code>Q652429146@ybl</code>, and share the UTR with Admissions WhatsApp at <strong>+91 81929 11360</strong>.
        </p>
        """
    },
    {
        "id": "RESP-05-NISHANT",
        "email": "nishantmakwane04@gmail.com",
        "name": "Nishant Makwane",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: DBERT Milestone Roadmap: Submission Assistance for ₹5,000 Stipend & Credentials",
        "topic": "Milestone Roadmap Submission Link",
        "plain_content": """Dear Nishant,

Thank you for bringing this to our attention. We noticed your message stating that your response was not recorded on the Google Form.

To ensure your submission is recorded without any issues, you have two guaranteed methods:

Method 1: Direct LMS Milestone Dashboard (Recommended)
Log in to your student portal at: https://lms.dbert.in/stipend/tasks
Here you can directly submit your:
- GitHub repository URL
- Live demo URL
- Technical contribution report

Method 2: Direct Google Form Link:
https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform

If you encounter any difficulty with either, you can reply directly to this email with your GitHub link and report, and our evaluation board will manually record your submission for your ₹5,000 stipend and verified credentials.

Admissions WhatsApp: +91 81929 11360""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for letting us know about the form recording issue regarding your <strong>Data Analyst Milestone Roadmap</strong>.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          To ensure your project deliverables are recorded immediately for your <strong>₹5,000 performance stipend and verified credential</strong>, please use either of the options below:
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:6px;">Option 1: Native LMS Submission Dashboard (Instant)</div>
          <p style="margin:0 0 10px;font-size:13px;color:#C8D3E0;line-height:1.5;">
            Visit: <a href="https://lms.dbert.in/stipend/tasks" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/stipend/tasks</a> to submit your GitHub repository and technical report.
          </p>
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:6px;">Option 2: Direct Google Form</div>
          <p style="margin:0;font-size:13px;color:#C8D3E0;line-height:1.5;">
            <a href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform" style="color:#E2B96F;font-weight:700;">Open Direct Google Form →</a>
          </p>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Alternatively, you can reply directly to this email with your GitHub repository link, and our operations team will manually log your submission.
        </p>
        """
    },
    {
        "id": "RESP-06-HARIOM",
        "email": "imhariom25@gmail.com",
        "name": "Hariom Yadav",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: DBERT Milestone Roadmap: Clarification on Free Evaluation vs Optional Hard Copy",
        "topic": "Zero Fee Clarification for Milestone Evaluation",
        "plain_content": """Dear Hariom,

We received your message stating that you are unable to pay ₹299.

Please be completely assured: YOU DO NOT NEED TO PAY ₹299!

We want to make this 100% clear:
1. The ₹299 fee is STRICTLY OPTIONAL for candidates who want a physical printed certificate and frame couriered to their home address.
2. Academic evaluation, LMS grading, cryptographic certificate verification on https://dbert.in/verify, and eligibility for the ₹5,000 performance stipend are 100% FREE!
3. You do not have to pay a single rupee to complete your fellowship evaluation.

Please proceed to submit your project deliverables on the student portal:
https://lms.dbert.in/stipend/tasks

If you need any guidance, our team is available on WhatsApp at +91 81929 11360.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          We received your reply stating that you are unable to pay ₹299.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#F0F4F8;font-weight:700;">
          Please be completely reassured: You do NOT have to pay ₹299!
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <h4 style="margin:0 0 6px;color:#E2B96F;font-size:14px;">100% Free Standard Evaluation Policy:</h4>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:18px;">
            <li>The ₹299 is <strong>strictly optional</strong> for candidates who request a physical printed certificate and hard-copy courier delivery.</li>
            <li>Your official academic project evaluation, digital credentials, cryptographically signed verification dossier on <a href="https://dbert.in/verify" style="color:#E2B96F;">dbert.in/verify</a>, and <strong>eligibility for the ₹5,000 performance stipend are 100% FREE</strong>.</li>
          </ul>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Please submit your technical deliverables directly on the student portal at <a href="https://lms.dbert.in/stipend/tasks" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/stipend/tasks</a> without any payment.
        </p>
        """
    },
    {
        "id": "RESP-07-PRAKASH",
        "email": "prakash.a2878@gmail.com",
        "name": "Prakash A",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: Application Status Update & Next Mandatory Steps [CERT-DBERT-2026-AIML-378]",
        "topic": "Onboarding Verification Next Steps",
        "plain_content": """Dear Prakash,

Thank you for your update regarding your application (Ref: CERT-DBERT-2026-AIML-378).

Here are your mandatory next steps to finalize onboarding:

1. Access Your LMS Dashboard:
Log in to: https://lms.dbert.in/portal using your registered email: prakash.a2878@gmail.com.

2. Complete Track Verification:
Confirm your track details under the AI & Machine Learning program and review the Week 1 milestone brief.

3. Admissions Support:
If you require immediate verification assistance or have specific document upload questions, connect directly with our Admissions Desk on WhatsApp at +91 81929 11360.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for following up regarding your application (Ref: <code>CERT-DBERT-2026-AIML-378</code>).
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Here are your confirmed next steps:
        </p>

        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:16px 20px;margin:18px 0;">
          <ol style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:18px;">
            <li>Log in to your LMS profile: <a href="https://lms.dbert.in/portal" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal</a></li>
            <li>Verify your track registration under the <strong>AI &amp; Machine Learning</strong> domain.</li>
            <li>Review your Week 1 sprint task brief and setup instructions.</li>
          </ol>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          If you need any document verification assistance, reach out directly to Admissions on WhatsApp: <strong>+91 81929 11360</strong>.
        </p>
        """
    },
    {
        "id": "RESP-08-ASTHA",
        "email": "asthaarya42@gmail.com",
        "name": "Astha Arya",
        "sender_account": "manoj.kumar@dbert.in",
        "subject": "Re: Unable to Complete Onboarding Verification – Server Error Resolved",
        "topic": "Onboarding Server Error Resolution",
        "plain_content": """Dear Astha,

Thank you for reporting the server error you encountered while completing onboarding verification for the Data Analytics track.

We have resolved the server connectivity issue and verified that the portal is operating normally.

Please try accessing your onboarding dashboard now:
Portal URL: https://lms.dbert.in/portal
Registered Email: asthaarya42@gmail.com

If your browser shows a cached error, please do a quick refresh (Ctrl+F5) or open in an Incognito window.

Alternatively, you can message our Admissions Concierge on WhatsApp at +91 81929 11360 and we will verify your onboarding manually within minutes.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reporting the server error you experienced while completing your onboarding for the <strong>Data Analytics</strong> track.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Our engineering team has resolved the underlying database lock, and the portal is now operating smoothly.
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <div style="font-size:13px;font-weight:700;color:#E2B96F;margin-bottom:6px;">Direct Verification Link:</div>
          <p style="margin:0;font-size:13px;color:#C8D3E0;line-height:1.5;">
            Please visit <a href="https://lms.dbert.in/portal" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/portal</a> and proceed with your onboarding.
          </p>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          If you encounter any difficulty, our Admissions Concierge is available on WhatsApp at <strong>+91 81929 11360</strong> to verify your account manually.
        </p>
        """
    },
    {
        "id": "RESP-09-VINAY",
        "email": "gurkavinay22@gmail.com",
        "name": "Gurka Vinay Kumar Reddy",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: Official Internship Credential Packet — Payout Setup Confirmed [CERT-DBERT-2026-AIML-169]",
        "topic": "UPI Payout Setup & Capstone Submission Confirmed",
        "plain_content": """Dear Vinay,

Thank you for your update.

We have officially recorded your UPI ID (9014147134@upi) into your candidate ledger for credential CERT-DBERT-2026-AIML-169.

Status Update:
1. Payout Configuration: Your UPI ID (9014147134@upi) is now locked in for direct disbursement upon milestone release.
2. Technical Contribution: Your AI & Machine Learning Capstone project submission has been queued for evaluation rubric sign-off.
3. Verified Credentials: Your official credentials remain verified and publicly verifiable at:
https://dbert.in/verify?certid=CERT-DBERT-2026-AIML-169 (Grade A, Score: 80/100).

Once our evaluation board signs off on the technical review, your milestone stipend will be credited directly to your UPI ID.""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for following up with your payout details.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          We are pleased to confirm that your UPI ID <code>9014147134@upi</code> has been successfully recorded into our disbursement ledger for credential <code>CERT-DBERT-2026-AIML-169</code>.
        </p>

        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:16px 20px;margin:18px 0;">
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:18px;">
            <li><strong>Payout Method:</strong> Recorded as <code>9014147134@upi</code>.</li>
            <li><strong>Capstone Review:</strong> Your technical contribution is in the final evaluation queue.</li>
            <li><strong>Verified Credentials:</strong> Live and verified at <a href="https://dbert.in/verify?certid=CERT-DBERT-2026-AIML-169" style="color:#E2B96F;font-weight:700;">dbert.in/verify/CERT-DBERT-2026-AIML-169</a> (Grade A, Score: 80/100).</li>
          </ul>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Upon completion of the final evaluation sign-off, your performance stipend will be disbursed directly to your confirmed UPI address.
        </p>
        """
    },
    {
        "id": "RESP-10-SHANU",
        "email": "shanusrigowtham17@gmail.com",
        "name": "Shanu Sri Gowtham",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: Official Internship Credential Packet: Stipend Milestone Status [CERT-DBERT-2026-AIML-013]",
        "topic": "Stipend Milestone Roadmap & Capstone Requirements",
        "plain_content": """Dear Shanu Sri Gowtham,

Thank you for contacting us regarding your stipend milestone status.

We want to reassure you that your academic achievements are fully recognized and in outstanding standing:
- Credential ID: CERT-DBERT-2026-AIML-013
- Grade: A+ (Outstanding Performance, Score: 87/100)
- Public Verification Dossier: https://dbert.in/verify?certid=CERT-DBERT-2026-AIML-013

Regarding Performance Stipend Release:
Under DBERT academic guidelines, performance stipends are released through the LMS Milestone Portal once the technical contribution criteria are validated:
1. Verify that your UPI ID is configured on your portal profile: https://lms.dbert.in/profile
2. Submit your technical project repository and report on the milestone dashboard: https://lms.dbert.in/stipend/tasks

Once your submission clears the milestone check, your 5,000 coin stipend will be released to your wallet for instant payout.

Admissions Helpline: +91 81929 11360""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Thank you for reaching out regarding your performance stipend milestone.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          First, please be reassured that your academic credentials are fully verified and in outstanding standing:<br>
          <strong>Dossier:</strong> <a href="https://dbert.in/verify?certid=CERT-DBERT-2026-AIML-013" style="color:#E2B96F;font-weight:700;">CERT-DBERT-2026-AIML-013</a> (Grade A+, Score: 87/100).
        </p>

        <div style="background:rgba(226,185,111,0.06);border-left:3px solid #E2B96F;border-radius:6px;padding:14px 18px;margin:20px 0;">
          <h4 style="margin:0 0 6px;color:#E2B96F;font-size:14px;">Stipend Disbursement Procedure:</h4>
          <ol style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:18px;">
            <li>Ensure your UPI ID is configured under your profile on <a href="https://lms.dbert.in/profile" style="color:#E2B96F;">lms.dbert.in/profile</a>.</li>
            <li>Submit your technical capstone deliverables (GitHub link and report) at <a href="https://lms.dbert.in/stipend/tasks" style="color:#E2B96F;font-weight:700;">https://lms.dbert.in/stipend/tasks</a>.</li>
            <li>Upon milestone approval, your ₹5,000 performance stipend is released directly to your wallet and disbursed via UPI.</li>
          </ol>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          For any expedited assistance, our Admissions Concierge is available on WhatsApp at <strong>+91 81929 11360</strong>.
        </p>
        """
    },
    {
        "id": "RESP-11-ROSMI",
        "email": "rosmireji556@gmail.com",
        "name": "Rosmi Reji",
        "sender_account": "abhinav.sharma@dbert.in",
        "subject": "Re: DBERT Internship Verification & Official Work Reference [CERT-DBERT-2026-FSD-103]",
        "topic": "Official Work Reference & Employer Verification",
        "plain_content": """Dear Rosmi Reji,

Congratulations on your upcoming job opportunity! We are very happy to provide full employment reference and verification support.

You may provide the following details to prospective employers:

1. Cryptographic Verification Dossier:
Employers can instantly verify your internship completion and performance online:
https://dbert.in/verify?certid=CERT-DBERT-2026-FSD-103

2. Official Verification Contacts for Background Checks:
- Organization: DBERT (Digital Blinc Education Research and Technology)
- Verification Email: admissions@dbert.in / support@dbert.in
- Program Head & Mentor: Mr. Abhinav Sharma (abhinav.sharma@dbert.in)
- Institutional Website: https://dbert.in

Whenever an employer requires written verification or background check forms completed, they can email admissions@dbert.in directly, and our HR team will confirm your tenure and project deliverables within 24 hours.

We wish you every success in your career!""",
        "html_content": """
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Congratulations on your prospective career opportunity! We are delighted to support you with full employment and academic reference verification.
        </p>
        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          You can share the following official verification credentials with employers:
        </p>

        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:16px 20px;margin:18px 0;">
          <h4 style="margin:0 0 6px;color:#E2B96F;font-size:14px;">Official Employer Verification Details:</h4>
          <ul style="font-size:13px;color:#C8D3E0;line-height:1.6;margin:0;padding-left:18px;">
            <li><strong>Direct Verification Dossier:</strong> <a href="https://dbert.in/verify?certid=CERT-DBERT-2026-FSD-103" style="color:#E2B96F;font-weight:700;">dbert.in/verify?certid=CERT-DBERT-2026-FSD-103</a></li>
            <li><strong>Official HR Email for BGV:</strong> <code>admissions@dbert.in</code> / <code>support@dbert.in</code></li>
            <li><strong>Program Mentor:</strong> Mr. Abhinav Sharma (<code>abhinav.sharma@dbert.in</code>)</li>
            <li><strong>Organization:</strong> DBERT (Digital Blinc Education Research and Technology)</li>
          </ul>
        </div>

        <p style="font-size:14px;line-height:1.6;color:#C8D3E0;">
          Whenever a prospective employer reaches out for formal written verification, our HR verification desk will confirm your project deliverables within 24 hours.
        </p>
        """
    }
]

def send_smtp_email(sender_info: dict, recipient_email: str, recipient_name: str, subject: str, plain_text: str, html_body: str) -> str:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{sender_info['name']} · DBERT <{sender_info['user']}>"
    msg["To"] = f"{recipient_name} <{recipient_email}>"
    msg["Reply-To"] = sender_info['user']
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")

    part1 = MIMEText(plain_text, "plain", "utf-8")
    part2 = MIMEText(html_body, "html", "utf-8")
    msg.attach(part1)
    msg.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=20) as server:
        server.login(sender_info["user"], sender_info["pass"])
        server.send_message(msg)

    return msg["Message-ID"]

def main():
    log("=" * 76)
    log("STARTING DIRECT AUTONOMOUS INBOX ACTION DISPATCH")
    log("=" * 76)

    tracking = load_tracking()
    sent_count = 0

    for idx, cand in enumerate(CANDIDATE_RESPONSES, 1):
        cand_id = cand["id"]
        recipient = cand["email"]
        sender_acc = cand["sender_account"]
        sender_info = SMTP_ACCOUNTS[sender_acc]

        if cand_id in tracking and tracking[cand_id].get("status") == "SENT":
            log(f"[{idx}/{len(CANDIDATE_RESPONSES)}] ALREADY SENT to {cand['name']} ({recipient}) — Skipping.")
            continue

        log(f"[{idx}/{len(CANDIDATE_RESPONSES)}] Dispatching reply to {cand['name']} ({recipient}) from {sender_acc}...")

        wa_block = build_whatsapp_buttons(cand["name"], recipient, cand["topic"])
        html_email = wrap_email_html(sender_info, cand["name"], cand["html_content"], wa_block)

        try:
            msg_id = send_smtp_email(
                sender_info=sender_info,
                recipient_email=recipient,
                recipient_name=cand["name"],
                subject=cand["subject"],
                plain_text=cand["plain_content"],
                html_body=html_email
            )

            tracking[cand_id] = {
                "name": cand["name"],
                "email": recipient,
                "sender": sender_acc,
                "subject": cand["subject"],
                "topic": cand["topic"],
                "status": "SENT",
                "message_id": msg_id,
                "dispatched_at": datetime.now().isoformat()
            }
            save_tracking(tracking)
            sent_count += 1
            log(f"  ✓ SUCCESS: Delivered Message-ID: {msg_id}")

            # Pacing delay
            if idx < len(CANDIDATE_RESPONSES):
                log("  Pacing 15 seconds before next candidate delivery...")
                time.sleep(15)

        except Exception as e:
            log(f"  ✗ FAILED to send to {recipient}: {e}")
            tracking[cand_id] = {
                "name": cand["name"],
                "email": recipient,
                "sender": sender_acc,
                "status": "FAILED",
                "error": str(e),
                "attempted_at": datetime.now().isoformat()
            }
            save_tracking(tracking)

    log("=" * 76)
    log(f"MISSION COMPLETE: {sent_count} REPLIES DISPATCHED.")
    log("=" * 76)

    # Telemetry report to admins
    try:
        telemetry_html = f"""<h3>DBERT Autonomous Email Dispatch Telemetry</h3>
        <p>Total Replies Dispatched: <strong>{sent_count}</strong></p>
        <ul>
        """
        for cid, record in tracking.items():
            if record.get("status") == "SENT":
                telemetry_html += f"<li><strong>{record['name']}</strong> ({record['email']}) — Sent from {record['sender']} | Topic: {record['topic']}</li>"
        telemetry_html += "</ul>"

        admin_sender = SMTP_ACCOUNTS["abhinav.sharma@dbert.in"]
        for admin_email in TELEMETRY_EMAILS:
            send_smtp_email(
                sender_info=admin_sender,
                recipient_email=admin_email,
                recipient_name="DBERT Operations",
                subject=f"Telemetry: DBERT Autonomous Inbox Dispatch Complete ({sent_count} Candidate Replies)",
                plain_text=f"DBERT Autonomous Email Dispatch Complete: {sent_count} candidate replies sent.",
                html_body=telemetry_html
            )
            log(f"Telemetry notification delivered to {admin_email}")
    except Exception as e:
        log(f"Telemetry notification warning: {e}")

if __name__ == "__main__":
    main()
