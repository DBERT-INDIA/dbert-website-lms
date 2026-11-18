#!/usr/bin/env python3
"""
================================================================================
DBERT Urgent Batch Kickoff Multi-SMTP Dispatch Daemon
================================================================================
Dispatches urgent onboarding notifications across 5 Google Workspace SMTP
accounts in parallel with randomized 10s-30s anti-spam pacing.

Audience:
  - 64 Candidates with irregular/rejected payment proofs (Template B: Payment Re-verify)
  - 1,200 Latest Selected Candidates (Template A: Standard Kickoff)
  - Total Queue: 1,264 Candidates

Usage:
  # Check current campaign tracking status:
  python scripts/dispatch_urgent_batch_kickoff_multi_smtp.py --status

  # Dry-run inspection (previews sharding without sending):
  python scripts/dispatch_urgent_batch_kickoff_multi_smtp.py --dry-run

  # Dispatch 2 test emails (Template A & B) to personal inbox:
  python scripts/dispatch_urgent_batch_kickoff_multi_smtp.py --test-to ain.sharma.abhinav@gmail.com

  # Launch live parallel multi-threaded dispatch:
  python scripts/dispatch_urgent_batch_kickoff_multi_smtp.py --live
================================================================================
"""

import os
import sys
import json
import time
import ssl
import random
import smtplib
import argparse
import threading
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid
from pathlib import Path
from typing import Dict, List, Any

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"

COHORT_FILE = DATA_DIR / "urgent_kickoff_cohort_1265.json"
TRACKING_FILE = DATA_DIR / "dispatch_tracking_urgent_kickoff.json"
LOG_FILE = DATA_DIR / "dispatch_urgent_kickoff.log"

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

# 5 Authenticated Google Workspace SMTP Accounts
SMTP_ACCOUNTS = [
    {
        "id": "acc_1",
        "user": "abhinav.sharma@dbert.in",
        "pass": "rsupmvvvvwrsuxuh",
        "name": "Abhinav Sharma",
        "role": "Program Head & Project Mentor"
    },
    {
        "id": "acc_2",
        "user": "manoj.kumar@dbert.in",
        "pass": "fnevtpseplwibckr",
        "name": "Manoj Kumar",
        "role": "Academic Lead & Admissions"
    },
    {
        "id": "acc_3",
        "user": "sandeep.bannu@dbert.in",
        "pass": "qtqzlmrynbcxvyjy",
        "name": "Sandeep Bannu",
        "role": "Technical Program Operations"
    },
    {
        "id": "acc_4",
        "user": "contactus@dbert.in",
        "pass": "llvmaajmrljpcwru",
        "name": "DBERT Admissions & Verification",
        "role": "Admissions & Verification Concierge"
    },
    {
        "id": "acc_5",
        "user": "pulkit.kunar@dbert.in",
        "pass": "vzefecwpggxuaztr",
        "name": "Pulkit Kumar",
        "role": "Technical Mentorship & Verification"
    }
]

# Thread safety locks
tracking_lock = threading.Lock()
log_lock = threading.Lock()

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with log_lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

# ==============================================================================
# TEMPLATE BUILDERS (TEMPLATE A: STANDARD KICKOFF & TEMPLATE B: PAYMENT RE-VERIFY)
# ==============================================================================

def build_email_content(candidate: Dict[str, Any], template_type: str, sender_account: Dict[str, str]):
    name = (candidate.get("name") or "Engineering Fellow").strip()
    domain = (candidate.get("domain") or "Applied Engineering").strip()
    email = candidate.get("email", "").strip()
    utr = candidate.get("utr", "").strip()
    admin_note = candidate.get("admin_note", "").strip()

    sender_name = sender_account["name"]
    sender_user = sender_account["user"]

    if template_type == "PAYMENT_REVERIFY":
        subject = f"[ACTION REQUIRED] Urgent Payment Re-Verification: Batch Kickoff in 5 Hours — DBERT Admissions"
        
        plain_text = f"""DBERT TECHNICAL COUNCIL — URGENT PAYMENT RE-VERIFICATION NOTICE
Digital Blinc Education Research and Technology (dbert.in)

URGENT: BATCH KICKOFF COMMENCES IN 5 HOURS
Orientation Schedule: Today, 16 November 2026 at 05:00 PM IST

Dear {name},

We are contacting you urgently regarding your incubation seat reservation for the 2-Month Remote Applied Engineering Fellowship ({domain}).

Your previous caution deposit submission (Recorded UTR: {utr or 'None/Pending'}) could not be reconciled by our finance desk due to:
"{admin_note or 'No valid transaction proof/UTR was attached'}"

To ensure you do not lose your assigned cloud development seat, your Candidate Portal has been RE-OPENED to SELECTED status for valid UTR re-submission.

================================================================================
4 STEPS TO SECURE YOUR SEAT BEFORE 05:00 PM IST:
================================================================================
Step 1: Open Your Offer Letter
Log in to your candidate portal:
https://lms.dbert.in/portal/offer

Step 2: Review Appointment Terms
Inspect your full appointment clauses, stipend structure (Fixed ₹5,000 + up to ₹18,000 incentive), and weekly 10 hrs engagement target in Terms Preview Mode.

Step 3: Complete ₹499 Caution Deposit
If you have already paid, ensure you have your correct 12-digit numeric bank UTR. If unpaid, complete ₹499 via UPI:
• UPI VPA: Q652429146@ybl (DBERT Admissions)
• 1-Tap UPI / QR available directly on https://lms.dbert.in/portal/offer

Step 4: Enter 12-Digit UTR
Submit your valid 12-digit UTR on the offer page or send proof directly to Admissions WhatsApp. Once reconciled, your digital signature section and official downloadable A4 PDF will unlock immediately.

================================================================================
IMMEDIATE ONBOARDING ASSISTANCE (DUAL WHATSAPP HELPLINES)
================================================================================
📱 Admissions & Payment Reconciliation Desk:
WhatsApp: +91 81929 11360
Direct Link: https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20{name}%20resubmitting%20my%20UTR%20for%20today%27s%20batch.

📱 Academic & Technical Mentorship Desk:
WhatsApp: +91 89580 06294
Direct Link: https://wa.me/918958006294?text=Hi%20Mentorship%20Desk%2C%20I%20am%20{name}%20inquiring%20about%20today%27s%20kickoff.

We look forward to confirming your credentials before the 05:00 PM IST orientation.

Sincerely,

{sender_name}
{sender_account['role']}
DBERT Technical Council
Portal: https://lms.dbert.in
Platform: https://dbert.in
"""

        html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DBERT Urgent Payment Re-Verification</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0B0F17; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; -webkit-font-smoothing: antialiased;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0B0F17; padding: 30px 15px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" style="max-width: 620px; background-color: #111827; border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 12px; overflow: hidden; box-shadow: 0 12px 35px rgba(0,0,0,0.6);" cellspacing="0" cellpadding="0" border="0">
          
          <!-- Urgent Alert Header -->
          <tr>
            <td style="background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 50%, #B91C1C 100%); padding: 14px 24px; text-align: center; border-bottom: 1px solid rgba(239, 68, 68, 0.4);">
              <span style="font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; color: #FEE2E2;">
                ⚠️ ACTION REQUIRED: URGENT PAYMENT RE-VERIFICATION · KICKOFF IN 5 HOURS
              </span>
            </td>
          </tr>

          <!-- Brand Header -->
          <tr>
            <td style="padding: 26px 32px 18px 32px; text-align: center; border-bottom: 1px solid #1F2937;">
              <span style="font-size: 26px; font-weight: 900; letter-spacing: 0.08em; color: #F8FAFC;">D B E R T</span>
              <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.2em; color: #E2B96F; font-weight: 700; margin-top: 4px;">Technical Council & Venture Studio</div>
            </td>
          </tr>

          <!-- Notice Body -->
          <tr>
            <td style="padding: 30px 32px 16px 32px;">
              <div style="display: inline-block; padding: 4px 12px; background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 9999px; color: #FBBF24; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 14px;">
                ● Action Required: Seat Confirmation Pending
              </div>
              <h1 style="margin: 0 0 12px 0; font-size: 21px; font-weight: 700; color: #FFFFFF; line-height: 1.35;">
                Dear {name},
              </h1>
              <p style="margin: 0 0 14px 0; font-size: 14px; line-height: 1.6; color: #94A3B8;">
                We are contacting you urgently regarding your seat reservation in the <strong style="color: #F1F5F9;">{domain}</strong> Fellowship (Batch Orientation starts in 5 hours at 05:00 PM IST).
              </p>
              
              <!-- Warning Card -->
              <div style="background-color: rgba(239, 68, 68, 0.08); border-left: 4px solid #EF4444; padding: 14px 16px; border-radius: 4px; margin-bottom: 20px;">
                <div style="font-size: 12px; font-weight: 700; color: #FCA5A5; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Finance Reconciliation Status:</div>
                <div style="font-size: 13px; color: #FEE2E2; line-height: 1.5;">
                  Your previous ₹499 transaction proof could not be verified: <em>"{admin_note or 'No valid transaction screenshot or 12-digit UTR was recorded.'}"</em>
                </div>
                <div style="font-size: 12px; color: #94A3B8; margin-top: 6px;">
                  Your candidate portal has been re-opened to <strong>Selected</strong> so you can enter your valid 12-digit UTR.
                </div>
              </div>
            </td>
          </tr>

          <!-- Primary CTA Button -->
          <tr>
            <td style="padding: 0 32px 24px 32px; text-align: center;">
              <a href="https://lms.dbert.in/portal/offer" style="display: inline-block; width: 100%; max-width: 360px; background: linear-gradient(135deg, #E2B96F 0%, #C49746 100%); color: #0B0F17; text-decoration: none; font-weight: 800; font-size: 15px; padding: 14px 28px; border-radius: 8px; box-shadow: 0 4px 20px rgba(226, 185, 111, 0.35); text-transform: uppercase; letter-spacing: 0.04em;">
                Re-Submit Valid UTR & Unlock Offer →
              </a>
              <div style="font-size: 12px; color: #64748B; margin-top: 10px;">
                Direct URL: <a href="https://lms.dbert.in/portal/offer" style="color: #94A3B8; text-decoration: underline;">https://lms.dbert.in/portal/offer</a>
              </div>
            </td>
          </tr>

          <!-- 4 Steps Guide -->
          <tr>
            <td style="padding: 22px 32px; background-color: #0A0F1A; border-top: 1px solid #1E293B; border-bottom: 1px solid #1E293B;">
              <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #E2B96F; margin-bottom: 14px;">
                How to Re-Verify Your Seat in 3 Minutes:
              </div>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="font-size: 13px; line-height: 1.55;">
                <tr>
                  <td style="padding-bottom: 10px; vertical-align: top; width: 26px; color: #E2B96F; font-weight: 700;">1.</td>
                  <td style="padding-bottom: 10px; color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Review Appointment Terms:</strong> Access your offer letter on LMS in Terms Preview Mode.
                  </td>
                </tr>
                <tr>
                  <td style="padding-bottom: 10px; vertical-align: top; color: #E2B96F; font-weight: 700;">2.</td>
                  <td style="padding-bottom: 10px; color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Get Your 12-Digit Bank UTR:</strong> Check your bank statement or UPI app receipt (GPay / PhonePe / Paytm) for the 12-digit numeric reference.
                  </td>
                </tr>
                <tr>
                  <td style="padding-bottom: 10px; vertical-align: top; color: #E2B96F; font-weight: 700;">3.</td>
                  <td style="padding-bottom: 10px; color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Submit on Portal:</strong> Enter the 12-digit UTR in the verification box on <a href="https://lms.dbert.in/portal/offer" style="color: #E2B96F;">/portal/offer</a>.
                  </td>
                </tr>
                <tr>
                  <td style="vertical-align: top; color: #E2B96F; font-weight: 700;">4.</td>
                  <td style="color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Admin Reconciliation:</strong> Our admissions team verifies your transaction; sign digitally and download your official signed PDF.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Dual WhatsApp Concierge -->
          <tr>
            <td style="padding: 24px 32px;">
              <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #94A3B8; margin-bottom: 14px; text-align: center;">
                Need Instant Help Reconciling Your Payment?
              </div>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                  <!-- WhatsApp 1: Admissions -->
                  <td style="padding-right: 8px; width: 50%;">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0F172A; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; text-align: center; padding: 14px 10px;">
                      <tr>
                        <td>
                          <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #10B981; font-weight: 700;">Admissions Desk</div>
                          <div style="font-size: 13px; font-weight: 700; color: #F1F5F9; margin: 4px 0;">+91 81929 11360</div>
                          <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20{name}%20resubmitting%20my%20UTR%20for%20today%27s%20batch." style="display: inline-block; background-color: #059669; color: #FFFFFF; font-size: 11px; font-weight: 700; text-decoration: none; padding: 6px 14px; border-radius: 6px; margin-top: 6px;">
                            Chat on WhatsApp →
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                  <!-- WhatsApp 2: Mentorship -->
                  <td style="padding-left: 8px; width: 50%;">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0F172A; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; text-align: center; padding: 14px 10px;">
                      <tr>
                        <td>
                          <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #60A5FA; font-weight: 700;">Mentorship Desk</div>
                          <div style="font-size: 13px; font-weight: 700; color: #F1F5F9; margin: 4px 0;">+91 89580 06294</div>
                          <a href="https://wa.me/918958006294?text=Hi%20Mentorship%20Desk%2C%20I%20am%20{name}%20inquiring%20about%20today%27s%20kickoff." style="display: inline-block; background-color: #2563EB; color: #FFFFFF; font-size: 11px; font-weight: 700; text-decoration: none; padding: 6px 14px; border-radius: 6px; margin-top: 6px;">
                            Chat on WhatsApp →
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Signatory Footer -->
          <tr>
            <td style="padding: 22px 32px 28px 32px; border-top: 1px solid #1E293B; background-color: #0B0F17; text-align: center;">
              <p style="margin: 0 0 4px 0; font-size: 13px; font-weight: 700; color: #F1F5F9;">{sender_name}</p>
              <p style="margin: 0 0 10px 0; font-size: 12px; color: #64748B;">{sender_account['role']} · DBERT Technical Council</p>
              <div style="font-size: 11px; color: #475569; line-height: 1.6;">
                Digital Blinc Education Research and Technology · New Delhi, India<br>
                Official Sovereign Portal: <a href="https://dbert.in" style="color: #64748B; text-decoration: underline;">https://dbert.in</a> · LMS: <a href="https://lms.dbert.in" style="color: #64748B; text-decoration: underline;">https://lms.dbert.in</a>
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    else:
        # TEMPLATE A: STANDARD SELECTED URGENT KICKOFF
        subject = f"[URGENT] Action Required: Batch Kickoff in 5 Hours — Review Offer Letter & Confirm Seat"
        
        plain_text = f"""DBERT TECHNICAL COUNCIL — APPOINTMENT & ENROLLMENT NOTICE
Digital Blinc Education Research and Technology (dbert.in)

URGENT: BATCH KICKOFF COMMENCES IN 5 HOURS
Orientation Schedule: Today, 16 November 2026 at 05:00 PM IST

Dear {name},

Congratulations! Following a comprehensive review of your technical application by the DBERT Admissions Council, you have been SELECTED for the 2-Month Remote Applied Engineering Internship & Incubation Fellowship ({domain}).

Your official Letter of Offer has been generated and is now accessible in your LMS Candidate Portal.

================================================================================
APPOINTMENT & COMPENSATION HIGHLIGHTS
================================================================================
• Position: Remote Engineering Fellow ({domain})
• Batch Kickoff: Today at 05:00 PM IST (Orientation in 5 Hours)
• Weekly Commitment: Minimum 10 Hours/Week platform engagement (aggregated across dbert.in & lms.dbert.in)
• Fixed Milestone Stipend: ₹5,000 (Earned upon completing sprint deliverables)
• Performance Incentive: Up to ₹18,000 (Based on milestone excellence)
• Total Potential Compensation: Up to ₹23,000
• Caution Deposit: ₹499 (100% Refundable / Credited per Section 5 of Offer Letter)
• Official Credentials: 2 Verifiable Cryptographic Certificates + Letter of Recommendation

================================================================================
ACTION REQUIRED: 4 STEPS TO CONFIRM SEAT BEFORE 05:00 PM IST
================================================================================
Due to strict sandbox server provisioning and compute capacity, unconfirmed seats will be released to waitlisted candidates at 04:30 PM IST.

Step 1: Open Your Offer Letter
Log in to your candidate portal:
https://lms.dbert.in/portal/offer

Step 2: Review Appointment Terms
Review your appointment clauses, stipend structure, and weekly 10 hrs commitment in Terms Preview Mode.

Step 3: Confirm Seat with ₹499 Caution Deposit
To activate your engineering sandbox and cloud workspace, complete the ₹499 caution deposit via UPI:
• UPI VPA: Q652429146@ybl (DBERT Admissions)
• 1-Tap UPI / QR available directly on your offer page: https://lms.dbert.in/portal/offer

Step 4: Enter 12-Digit UTR
Enter your 12-digit UPI Transaction Reference (UTR) directly on the portal page or forward it to Admissions WhatsApp. Once reconciled by our administrative team, your digital signature section and official downloadable A4 PDF will unlock immediately.

================================================================================
NEED ASSISTANCE? CONTACT OUR DUAL HELPLINES
================================================================================
Our team is online to assist with your onboarding and payment reconciliation:

📱 Admissions & Seat Confirmation:
WhatsApp: +91 81929 11360
Direct Link: https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20{name}%20confirming%20my%20seat.

📱 Academic & Technical Mentorship:
WhatsApp: +91 89580 06294
Direct Link: https://wa.me/918958006294?text=Hi%20Mentorship%20Desk%2C%20I%20am%20{name}%20inquiring%20about%20today%27s%20kickoff.

We look forward to welcoming you to the engineering cohort at 05:00 PM IST.

Sincerely,

{sender_name}
{sender_account['role']}
DBERT Technical Council
Portal: https://lms.dbert.in
Platform: https://dbert.in
"""

        html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DBERT Batch Kickoff in 5 Hours</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0B0F17; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; -webkit-font-smoothing: antialiased;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0B0F17; padding: 30px 15px;">
    <tr>
      <td align="center">
        <!-- Main Container -->
        <table role="presentation" width="100%" style="max-width: 620px; background-color: #111827; border: 1px solid rgba(226, 185, 111, 0.25); border-radius: 12px; overflow: hidden; box-shadow: 0 12px 35px rgba(0,0,0,0.6);" cellspacing="0" cellpadding="0" border="0">
          
          <!-- Urgent Alert Header -->
          <tr>
            <td style="background: linear-gradient(135deg, #7F1D1D 0%, #991B1B 50%, #B91C1C 100%); padding: 14px 24px; text-align: center; border-bottom: 1px solid rgba(239, 68, 68, 0.4);">
              <span style="font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.12em; color: #FEE2E2;">
                ⚡ URGENT: BATCH KICKOFF IN 5 HOURS · SEAT CONFIRMATION REQUIRED
              </span>
            </td>
          </tr>

          <!-- Brand Header -->
          <tr>
            <td style="padding: 26px 32px 18px 32px; text-align: center; border-bottom: 1px solid #1F2937;">
              <span style="font-size: 26px; font-weight: 900; letter-spacing: 0.08em; color: #F8FAFC;">D B E R T</span>
              <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.2em; color: #E2B96F; font-weight: 700; margin-top: 4px;">Technical Council & Venture Studio</div>
            </td>
          </tr>

          <!-- Hero Greeting -->
          <tr>
            <td style="padding: 30px 32px 16px 32px;">
              <div style="display: inline-block; padding: 4px 12px; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 9999px; color: #34D399; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 14px;">
                ● Application Status: Selected
              </div>
              <h1 style="margin: 0 0 12px 0; font-size: 22px; font-weight: 700; color: #FFFFFF; line-height: 1.35;">
                Congratulations, {name}!
              </h1>
              <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #94A3B8;">
                Following a technical review by the DBERT Admissions Council, you have been selected for the <strong style="color: #F1F5F9;">{domain}</strong> Fellowship (2 Months · Remote). Your formal Letter of Offer is ready in your portal.
              </p>
            </td>
          </tr>

          <!-- Appointment Summary Table -->
          <tr>
            <td style="padding: 0 32px 22px 32px;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0F172A; border: 1px solid #1E293B; border-radius: 8px; overflow: hidden; font-size: 13px;">
                <tr style="border-bottom: 1px solid #1E293B;">
                  <td style="padding: 10px 16px; color: #94A3B8; font-weight: 600; width: 42%;">Orientation Kickoff</td>
                  <td style="padding: 10px 16px; color: #F59E0B; font-weight: 700;">Today at 05:00 PM IST (In 5 Hours)</td>
                </tr>
                <tr style="border-bottom: 1px solid #1E293B; background: rgba(255,255,255,0.015);">
                  <td style="padding: 10px 16px; color: #94A3B8; font-weight: 600;">Fixed Stipend</td>
                  <td style="padding: 10px 16px; color: #10B981; font-weight: 700;">₹5,000 (Earned upon Milestone Release)</td>
                </tr>
                <tr style="border-bottom: 1px solid #1E293B;">
                  <td style="padding: 10px 16px; color: #94A3B8; font-weight: 600;">Performance Incentive</td>
                  <td style="padding: 10px 16px; color: #F1F5F9;">Up to ₹18,000 Variable</td>
                </tr>
                <tr style="border-bottom: 1px solid #1E293B; background: rgba(255,255,255,0.015);">
                  <td style="padding: 10px 16px; color: #94A3B8; font-weight: 600;">Weekly Commitment</td>
                  <td style="padding: 10px 16px; color: #F1F5F9;">10 Hours / Week Logged Platform Time</td>
                </tr>
                <tr>
                  <td style="padding: 10px 16px; color: #94A3B8; font-weight: 600;">Caution Deposit</td>
                  <td style="padding: 10px 16px; color: #E2B96F; font-weight: 700;">₹499 (100% Refundable / Reconciled)</td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Primary CTA Button -->
          <tr>
            <td style="padding: 0 32px 28px 32px; text-align: center;">
              <a href="https://lms.dbert.in/portal/offer" style="display: inline-block; width: 100%; max-width: 360px; background: linear-gradient(135deg, #E2B96F 0%, #C49746 100%); color: #0B0F17; text-decoration: none; font-weight: 800; font-size: 15px; padding: 14px 28px; border-radius: 8px; box-shadow: 0 4px 20px rgba(226, 185, 111, 0.35); text-transform: uppercase; letter-spacing: 0.04em;">
                Review Offer Letter & Confirm Seat →
              </a>
              <div style="font-size: 12px; color: #64748B; margin-top: 10px;">
                Direct URL: <a href="https://lms.dbert.in/portal/offer" style="color: #94A3B8; text-decoration: underline;">https://lms.dbert.in/portal/offer</a>
              </div>
            </td>
          </tr>

          <!-- 4-Step Onboarding Guide -->
          <tr>
            <td style="padding: 22px 32px; background-color: #0A0F1A; border-top: 1px solid #1E293B; border-bottom: 1px solid #1E293B;">
              <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #E2B96F; margin-bottom: 14px;">
                How to Confirm Your Seat in 4 Minutes:
              </div>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="font-size: 13px; line-height: 1.55;">
                <tr>
                  <td style="padding-bottom: 10px; vertical-align: top; width: 26px; color: #E2B96F; font-weight: 700;">1.</td>
                  <td style="padding-bottom: 10px; color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Review Appointment Terms:</strong> Access your offer letter on LMS in read-only preview mode.
                  </td>
                </tr>
                <tr>
                  <td style="padding-bottom: 10px; vertical-align: top; color: #E2B96F; font-weight: 700;">2.</td>
                  <td style="padding-bottom: 10px; color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Pay ₹499 Caution Deposit:</strong> Use 1-Tap UPI (GPay, PhonePe, Paytm) or scan the embedded QR code to VPA <code style="background: #1E293B; color: #E2B96F; padding: 2px 6px; border-radius: 4px;">Q652429146@ybl</code>.
                  </td>
                </tr>
                <tr>
                  <td style="padding-bottom: 10px; vertical-align: top; color: #E2B96F; font-weight: 700;">3.</td>
                  <td style="padding-bottom: 10px; color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Enter 12-Digit UTR:</strong> Submit your payment UTR on the offer page or send to Admissions WhatsApp.
                  </td>
                </tr>
                <tr>
                  <td style="vertical-align: top; color: #E2B96F; font-weight: 700;">4.</td>
                  <td style="color: #CBD5E1;">
                    <strong style="color: #FFFFFF;">Unlock & Download PDF:</strong> Admin verifies your deposit; sign digitally and download your executive A4 PDF before 05:00 PM IST.
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Dual WhatsApp Concierge Section -->
          <tr>
            <td style="padding: 24px 32px;">
              <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: #94A3B8; margin-bottom: 14px; text-align: center;">
                Need Immediate Setup or Verification Support?
              </div>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                <tr>
                  <!-- WhatsApp 1: Admissions -->
                  <td style="padding-right: 8px; width: 50%;">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0F172A; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; text-align: center; padding: 14px 10px;">
                      <tr>
                        <td>
                          <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #10B981; font-weight: 700;">Admissions Desk</div>
                          <div style="font-size: 13px; font-weight: 700; color: #F1F5F9; margin: 4px 0;">+91 81929 11360</div>
                          <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20{name}%20confirming%20my%20seat." style="display: inline-block; background-color: #059669; color: #FFFFFF; font-size: 11px; font-weight: 700; text-decoration: none; padding: 6px 14px; border-radius: 6px; margin-top: 6px;">
                            Chat on WhatsApp →
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                  <!-- WhatsApp 2: Mentorship -->
                  <td style="padding-left: 8px; width: 50%;">
                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #0F172A; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; text-align: center; padding: 14px 10px;">
                      <tr>
                        <td>
                          <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: #60A5FA; font-weight: 700;">Mentorship Desk</div>
                          <div style="font-size: 13px; font-weight: 700; color: #F1F5F9; margin: 4px 0;">+91 89580 06294</div>
                          <a href="https://wa.me/918958006294?text=Hi%20Mentorship%20Desk%2C%20I%20am%20{name}%20inquiring%20about%20today%27s%20kickoff." style="display: inline-block; background-color: #2563EB; color: #FFFFFF; font-size: 11px; font-weight: 700; text-decoration: none; padding: 6px 14px; border-radius: 6px; margin-top: 6px;">
                            Chat on WhatsApp →
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Signatory Footer -->
          <tr>
            <td style="padding: 22px 32px 28px 32px; border-top: 1px solid #1E293B; background-color: #0B0F17; text-align: center;">
              <p style="margin: 0 0 4px 0; font-size: 13px; font-weight: 700; color: #F1F5F9;">{sender_name}</p>
              <p style="margin: 0 0 10px 0; font-size: 12px; color: #64748B;">{sender_account['role']} · DBERT Technical Council</p>
              <div style="font-size: 11px; color: #475569; line-height: 1.6;">
                Digital Blinc Education Research and Technology · New Delhi, India<br>
                Official Sovereign Portal: <a href="https://dbert.in" style="color: #64748B; text-decoration: underline;">https://dbert.in</a> · LMS: <a href="https://lms.dbert.in" style="color: #64748B; text-decoration: underline;">https://lms.dbert.in</a>
              </div>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

    return subject, plain_text, html_body

# ==============================================================================
# STATE & TRACKING MANAGEMENT
# ==============================================================================

def load_tracking() -> Dict[str, Dict[str, Any]]:
    with tracking_lock:
        if not TRACKING_FILE.exists():
            return {}
        try:
            with open(TRACKING_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {row["email"].lower(): row for row in data}
        except Exception as e:
            log(f"Error loading tracking file: {e}")
            return {}

def save_tracking_record(record: Dict[str, Any]):
    with tracking_lock:
        current = {}
        if TRACKING_FILE.exists():
            try:
                with open(TRACKING_FILE, "r", encoding="utf-8") as f:
                    rows = json.load(f)
                    current = {r["email"].lower(): r for r in rows}
            except Exception:
                current = {}
        current[record["email"].lower()] = record
        with open(TRACKING_FILE, "w", encoding="utf-8") as f:
            json.dump(list(current.values()), f, indent=2, ensure_ascii=False)

def get_stats():
    if not TRACKING_FILE.exists():
        print("Tracking file does not exist yet.")
        return
    with open(TRACKING_FILE, "r", encoding="utf-8") as f:
        rows = json.load(f)
    sent_count = sum(1 for r in rows if r.get("status") == "SENT")
    failed_count = sum(1 for r in rows if r.get("status") == "FAILED")
    print(f"=== DISPATCH STATS ===")
    print(f"Total Logged Records: {len(rows)}")
    print(f"Successfully Sent:    {sent_count}")
    print(f"Failed / Bounced:     {failed_count}")
    by_account = {}
    for r in rows:
        acc = r.get("account", "unknown")
        by_account[acc] = by_account.get(acc, 0) + (1 if r.get("status") == "SENT" else 0)
    print("Sent by Account:")
    for acc, count in by_account.items():
        print(f"  {acc}: {count}")

# ==============================================================================
# TELEMETRY DISPATCHER
# ==============================================================================

def send_telemetry(subject: str, summary_html: str):
    sender = SMTP_ACCOUNTS[0]
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[TELEMETRY] {subject}"
    msg["From"] = formataddr((f"{sender['name']} (Telemetry)", sender["user"]))
    msg["To"] = ", ".join(TELEMETRY_EMAILS)
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    msg.attach(MIMEText(summary_html, "html", "utf-8"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=15) as server:
            server.login(sender["user"], sender["pass"])
            server.sendmail(sender["user"], TELEMETRY_EMAILS, msg.as_string())
        log(f"Telemetry dispatched: {subject}")
    except Exception as e:
        log(f"Failed to dispatch telemetry: {e}")

# ==============================================================================
# WORKER THREAD FUNCTION
# ==============================================================================

def worker_thread(account: Dict[str, str], queue: List[Dict[str, Any]], sent_counter: Dict[str, int], stop_event: threading.Event):
    acc_id = account["id"]
    user = account["user"]
    pwd = account["pass"]
    name = account["name"]
    
    log(f"[{acc_id}] Worker thread started for {user} with {len(queue)} assigned candidates.")
    
    server = None
    ssl_context = ssl.create_default_context()

    def get_server():
        s = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context, timeout=20)
        s.login(user, pwd)
        return s

    for idx, candidate in enumerate(queue, 1):
        if stop_event.is_set():
            log(f"[{acc_id}] Stop event detected. Exiting worker.")
            break

        email = candidate["email"].strip().lower()
        cand_name = candidate["name"]
        tmpl_type = candidate.get("template_type", "STANDARD_KICKOFF")

        subject, plain_text, html_body = build_email_content(candidate, tmpl_type, account)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr((name, user))
        msg["To"] = formataddr((cand_name, email))
        msg["Reply-To"] = user
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")

        msg.attach(MIMEText(plain_text, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        delivered = False
        attempts = 0

        while attempts < 2 and not delivered:
            attempts += 1
            try:
                if server is None:
                    server = get_server()
                server.sendmail(user, [email], msg.as_string())
                delivered = True
            except Exception as e:
                err_msg = str(e)
                log(f"[{acc_id}] Error sending to {email} (attempt {attempts}): {err_msg}")
                try:
                    if server:
                        server.quit()
                except Exception:
                    pass
                server = None
                
                # Check for daily limit quota circuit breaker
                if "550 5.4.5" in err_msg or "Daily user sending limit" in err_msg:
                    log(f"[{acc_id}] CRITICAL: Google daily user quota reached on {user}. Halting worker {acc_id}.")
                    save_tracking_record({
                        "email": email,
                        "name": cand_name,
                        "status": "QUOTA_HALTED",
                        "account": user,
                        "error": err_msg,
                        "timestamp": datetime.now().isoformat()
                    })
                    return

                time.sleep(5)

        if delivered:
            with tracking_lock:
                sent_counter["total"] += 1
                curr_total = sent_counter["total"]

            save_tracking_record({
                "email": email,
                "name": cand_name,
                "domain": candidate.get("domain", ""),
                "template": tmpl_type,
                "status": "SENT",
                "account": user,
                "timestamp": datetime.now().isoformat()
            })
            log(f"[{acc_id}] [{idx}/{len(queue)}] SENT -> {cand_name} <{email}> ({tmpl_type}) | Global Total: {curr_total}")

            # Milestone telemetry every 100 emails
            if curr_total % 100 == 0:
                telemetry_body = f"""<h3>DBERT Urgent Kickoff Dispatch Milestone</h3>
<p>Delivered: <strong>{curr_total}</strong> emails successfully across 5 accounts.</p>
<p>Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>
"""
                send_telemetry(f"Milestone: {curr_total} Urgent Emails Delivered", telemetry_body)

        else:
            save_tracking_record({
                "email": email,
                "name": cand_name,
                "template": tmpl_type,
                "status": "FAILED",
                "account": user,
                "timestamp": datetime.now().isoformat()
            })

        # USER INSTRUCTION: 10 to 30 random seconds pacing between every email
        delay = round(random.uniform(10.0, 30.0), 2)
        log(f"[{acc_id}] Pacing pause {delay}s before next recipient...")
        time.sleep(delay)

    if server:
        try:
            server.quit()
        except Exception:
            pass
    log(f"[{acc_id}] Worker finished all assigned queue tasks.")

# ==============================================================================
# MAIN ORCHESTRATOR
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="DBERT Urgent Batch Kickoff Multi-SMTP Dispatch Daemon")
    parser.add_argument("--dry-run", action="store_true", help="Preview sharded queues without sending emails")
    parser.add_argument("--live", action="store_true", help="Execute live multi-threaded dispatch")
    parser.add_argument("--test-to", type=str, help="Send 1 sample of Template A & Template B to test email")
    parser.add_argument("--status", action="store_true", help="Display dispatch metrics from tracking file")

    args = parser.parse_args()

    if args.status:
        get_stats()
        return

    if not COHORT_FILE.exists():
        print(f"Error: Cohort file not found at {COHORT_FILE}")
        sys.exit(1)

    with open(COHORT_FILE, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)

    log(f"Loaded {len(all_candidates)} total candidates from {COHORT_FILE}")

    # Handle test mode
    if args.test_to:
        test_email = args.test_to.strip()
        log(f"Executing pre-flight test dispatch to {test_email} across accounts...")
        context = ssl.create_default_context()
        
        # Test Template A
        sample_cand_a = {
            "name": "Abhinav Sharma (Test)",
            "domain": "Full Stack Development",
            "email": test_email,
            "template_type": "STANDARD_KICKOFF"
        }
        acc_a = SMTP_ACCOUNTS[0]
        subj_a, txt_a, html_a = build_email_content(sample_cand_a, "STANDARD_KICKOFF", acc_a)
        msg_a = MIMEMultipart("alternative")
        msg_a["Subject"] = f"[TEST TEMPLATE A] {subj_a}"
        msg_a["From"] = formataddr((acc_a["name"], acc_a["user"]))
        msg_a["To"] = test_email
        msg_a.attach(MIMEText(txt_a, "plain", "utf-8"))
        msg_a.attach(MIMEText(html_a, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=15) as s:
            s.login(acc_a["user"], acc_a["pass"])
            s.sendmail(acc_a["user"], [test_email], msg_a.as_string())
        log(f"Test Template A sent via {acc_a['user']} -> {test_email}")

        # Test Template B
        sample_cand_b = {
            "name": "Abhinav Sharma (Test Payment Re-verify)",
            "domain": "Data Analytics",
            "email": test_email,
            "utr": "None / Unattached",
            "admin_note": "No payment screenshot or receipt was attached.",
            "template_type": "PAYMENT_REVERIFY"
        }
        acc_b = SMTP_ACCOUNTS[1]
        subj_b, txt_b, html_b = build_email_content(sample_cand_b, "PAYMENT_REVERIFY", acc_b)
        msg_b = MIMEMultipart("alternative")
        msg_b["Subject"] = f"[TEST TEMPLATE B] {subj_b}"
        msg_b["From"] = formataddr((acc_b["name"], acc_b["user"]))
        msg_b["To"] = test_email
        msg_b.attach(MIMEText(txt_b, "plain", "utf-8"))
        msg_b.attach(MIMEText(html_b, "html", "utf-8"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=15) as s:
            s.login(acc_b["user"], acc_b["pass"])
            s.sendmail(acc_b["user"], [test_email], msg_b.as_string())
        log(f"Test Template B sent via {acc_b['user']} -> {test_email}")

        print("Test emails successfully delivered! Inspect your inbox.")
        return

    # Check already sent
    tracking = load_tracking()
    pending = [c for c in all_candidates if tracking.get(c["email"].lower(), {}).get("status") != "SENT"]

    log(f"Total candidates: {len(all_candidates)} | Already Sent: {len(all_candidates) - len(pending)} | Pending: {len(pending)}")

    # Separate Priority 1 (Payment Re-verify) and Priority 2 (Standard Kickoff)
    p1 = [c for c in pending if c.get("template_type") == "PAYMENT_REVERIFY"]
    p2 = [c for c in pending if c.get("template_type") != "PAYMENT_REVERIFY"]

    # Shard round-robin into 5 queues
    num_accounts = len(SMTP_ACCOUNTS)
    shards: List[List[Dict[str, Any]]] = [[] for _ in range(num_accounts)]

    # Distribute Priority 1 first
    for idx, c in enumerate(p1):
        shards[idx % num_accounts].append(c)

    # Distribute Priority 2
    offset = len(p1) % num_accounts
    for idx, c in enumerate(p2):
        shards[(idx + offset) % num_accounts].append(c)

    print("\n=== QUEUE SHARDING BREAKDOWN ===")
    for i, acc in enumerate(SMTP_ACCOUNTS):
        p1_count = sum(1 for c in shards[i] if c.get("template_type") == "PAYMENT_REVERIFY")
        p2_count = sum(1 for c in shards[i] if c.get("template_type") != "PAYMENT_REVERIFY")
        print(f"Worker {acc['id']} ({acc['user']}): {len(shards[i])} total (P1 Re-verify: {p1_count}, P2 Standard: {p2_count})")

    if args.dry_run:
        print("\n[DRY RUN COMPLETE] Zero emails were sent. Use --live to launch parallel dispatch.")
        return

    if not args.live:
        print("\nSafety Confirmation: Run with --live to launch the 5 parallel dispatch workers.")
        return

    log("LAUNCHING 5 PARALLEL DISPATCH WORKERS (Pacing: 10s-30s random pauses)...")
    stop_event = threading.Event()
    sent_counter = {"total": 0}
    threads = []

    for i, acc in enumerate(SMTP_ACCOUNTS):
        t = threading.Thread(
            target=worker_thread,
            args=(acc, shards[i], sent_counter, stop_event),
            name=f"Worker-{acc['id']}"
        )
        t.daemon = True
        threads.append(t)
        t.start()

    try:
        while any(t.is_alive() for t in threads):
            time.sleep(2)
    except KeyboardInterrupt:
        log("\nCaught interrupt signal! Signaling workers to stop gracefully...")
        stop_event.set()
        for t in threads:
            t.join(timeout=5)
        log("Workers stopped.")

    final_total = sent_counter["total"]
    log(f"All workers finished. Total emails sent in this session: {final_total}")
    send_telemetry(
        f"Urgent Batch Dispatch Complete: {final_total} Delivered",
        f"<h3>Dispatch Session Complete</h3><p>Total Emails Dispatched: <strong>{final_total}</strong></p><p>Completed At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}</p>"
    )

if __name__ == "__main__":
    main()
