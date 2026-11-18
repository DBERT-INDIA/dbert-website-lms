#!/usr/bin/env python3
"""
scripts/dispatch_all_cohorts_pipeline.py

Unified multi-SMTP dispatch pipeline for:
- Cohort D: All Gates Verified & Scheduled Payout (6 candidates)
- Cohort B: Rejected Payment Resubmission (1 candidate)
- Cohort C: Missing Stipend Gates (38 candidates)
- Cohort A: Selected Offer Letter & 499 Seat Confirmation (63 candidates)

Total recipients: 108 candidates.
Rotating across 5 Google Workspace SMTP accounts with anti-spam pacing and atomic tracking.
"""

import os
import sys
import smtplib
import ssl
import time
import json
import argparse
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
DATA_DIR = ROOT_DIR / "data"
TRACKING_FILE = DATA_DIR / "cohort_dispatch_tracking.json"
LOG_FILE = DATA_DIR / "cohort_dispatch.log"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# SMTP Accounts Pool
SMTP_ACCOUNTS = [
    {
        "user": "abhinav.sharma@dbert.in",
        "pass": "rsupmvvvvwrsuxuh",
        "name": "Abhinav Sharma",
        "title": "Program Head & Project Mentor",
        "role": "DBERT Academic & Incubation Board"
    },
    {
        "user": "contactus@dbert.in",
        "pass": "llvmaajmrljpcwru",
        "name": "DBERT Admissions & Verification",
        "title": "Admissions & Verification Council",
        "role": "DBERT Academic Operations"
    },
    {
        "user": "manoj.kumar@dbert.in",
        "pass": "fnevtpseplwibckr",
        "name": "Manoj Kumar",
        "title": "Academic Lead & Admissions",
        "role": "DBERT Academic Operations"
    },
    {
        "user": "sandeep.bannu@dbert.in",
        "pass": "qtqzlmrynbcxvyjy",
        "name": "Sandeep Bannu",
        "title": "Technical Program Operations",
        "role": "DBERT Technical Fellowship Operations"
    },
    {
        "user": "pulkit.kunar@dbert.in",
        "pass": "vzefecwpggxuaztr",
        "name": "Pulkit Kumar",
        "title": "Admissions Desk & Candidate Support",
        "role": "DBERT Candidate Operations"
    }
]

TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [COHORT-DISPATCH] {msg}"
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

def get_smtp_connection(account: dict):
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=20)
    server.login(account["user"], account["pass"])
    return server

# ==============================================================================
# EMAIL TEMPLATE GENERATORS
# ==============================================================================

def build_cohort_d_email(c: dict, sender: dict) -> tuple:
    name = c.get("name", "Fellow")
    email = c.get("email")
    cert_id = c.get("cert_id", "CERT-DBERT-2026")
    domain = c.get("domain", "Applied Engineering")
    release_date_display = c.get("stipend_release_date_display", "Upcoming Cycle")
    release_date = c.get("stipend_release_date", "")
    org = c.get("verified_github_org", "Approved Organization")
    repo = c.get("verified_github_repo", org)
    amount = c.get("amount", 5499)

    subject = f"[APPROVED] ₹{amount:,} Stipend Disbursement Scheduled — Ref: {cert_id}"

    plain = f"""Dear {name},

We are pleased to inform you that all four eligibility and milestone gates for your DBERT Internship have been reviewed and approved by the DBERT Engineering Evaluation Committee.

MILESTONE & DISBURSEMENT SUMMARY:
--------------------------------------------------------------------------------
- Candidate Name: {name}
- Domain Track: {domain}
- Credential Reference: {cert_id}
- Public LinkedIn Experience: Verified & Featured
- Authorized GitHub Organization: {org}
- Repository Deliverable: {repo}
- Approved Payout Amount: ₹{amount:,} /- (₹5,000 Milestone Stipend + ₹499 Refundable Caution Deposit)
- Scheduled Disbursement Date: {release_date_display} (60 days following internship end date)
- Disbursement Channel: Registered Fernet-encrypted UPI ID on file
--------------------------------------------------------------------------------

Your stipend dashboard on the DBERT LMS has been updated to reflect your verified status:
https://lms.dbert.in/stipend/tasks

No further action is required from your side. The automated disbursement engine will execute the direct UPI transfer of ₹{amount:,} on {release_date_display}.

For any queries, please reach out via WhatsApp Admissions Concierge:
https://wa.me/918192911360?text={quote(f'Hi Team, my stipend is approved for release on {release_date} (Ref: {cert_id})')}

Warm regards,

{sender['name']}
{sender['title']}
DBERT Academic & Technical Fellowship Board
Digital Blinc Education Research and Technology
Official Portal: https://dbert.in | LMS: https://lms.dbert.in
"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; background-color: #07090E; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; }}
.wrapper {{ max-width: 620px; margin: 0 auto; background-color: #0E131F; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; }}
.header {{ background: linear-gradient(135deg, #064E3B 0%, #065F46 100%); padding: 36px 32px; border-bottom: 2px solid #10B981; text-align: left; }}
.badge {{ display: inline-block; background: rgba(52, 211, 153, 0.2); border: 1px solid rgba(52, 211, 153, 0.4); padding: 5px 14px; border-radius: 9999px; font-size: 11px; font-weight: 700; color: #34D399; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 12px; }}
.header h1 {{ margin: 0 0 8px; font-size: 22px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em; }}
.header p {{ margin: 0; font-size: 14px; color: #A7F3D0; }}
.body {{ padding: 32px; }}
.payout-box {{ background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1.5px solid rgba(52, 211, 153, 0.45); border-radius: 12px; padding: 22px; margin: 24px 0; text-align: center; }}
.payout-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: #94A3B8; font-weight: 700; }}
.payout-val {{ font-size: 32px; font-weight: 800; color: #34D399; margin: 8px 0 4px; }}
.payout-sub {{ font-size: 12px; color: #64748B; }}
.grid {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
.grid td {{ padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 13px; }}
.grid td.label {{ color: #94A3B8; font-weight: 600; width: 40%; }}
.grid td.val {{ color: #F8FAFC; font-weight: 700; text-align: right; }}
.btn {{ display: inline-block; background: #10B981; color: #FFFFFF !important; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-weight: 700; font-size: 14px; text-align: center; margin-top: 10px; }}
.footer {{ padding: 24px 32px; background: #07090E; border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; color: #64748B; line-height: 1.6; text-align: center; }}
</style>
</head>
<body>
<div style="padding: 24px 12px;">
  <div class="wrapper">
    <div class="header">
      <div class="badge">✓ All 4 Gates Verified &amp; Approved</div>
      <h1>Stipend Milestone Approved &amp; Scheduled</h1>
      <p>Official notification from DBERT Academic &amp; Incubation Council</p>
    </div>
    <div class="body">
      <p style="font-size: 15px; line-height: 1.6; margin-top: 0;">Dear <strong>{name}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        We are pleased to inform you that your complete credential dossier, professional LinkedIn experience, and open-source technical contribution on GitHub have been verified and approved by the DBERT Engineering Evaluation Committee.
      </p>

      <div class="payout-box">
        <div class="payout-label">Total Approved Disbursement</div>
        <div class="payout-val">₹{amount:,} /-</div>
        <div class="payout-sub">₹5,000 Milestone Grant + ₹499 Caution Deposit Refund</div>
      </div>

      <table class="grid">
        <tr>
          <td class="label">Candidate Name</td>
          <td class="val">{name}</td>
        </tr>
        <tr>
          <td class="label">Domain Track</td>
          <td class="val">{domain}</td>
        </tr>
        <tr>
          <td class="label">Credential Reference</td>
          <td class="val"><code style="color:#38BDF8;">{cert_id}</code></td>
        </tr>
        <tr>
          <td class="label">Verified GitHub Org</td>
          <td class="val"><strong style="color:#FCD34D;">{org}</strong></td>
        </tr>
        <tr>
          <td class="label">Scheduled Payout Date</td>
          <td class="val" style="color:#34D399;">{release_date_display}</td>
        </tr>
        <tr>
          <td class="label">Payout Channel</td>
          <td class="val">Registered UPI ID (Direct Transfer)</td>
        </tr>
      </table>

      <div style="text-align: center; margin: 28px 0 16px;">
        <a href="https://lms.dbert.in/stipend/tasks" class="btn">View Verified Stipend Dossier &rarr;</a>
      </div>

      <p style="font-size: 13px; color: #94A3B8; line-height: 1.6; text-align: center;">
        No further action required. The automated payout engine will credit ₹{amount:,}/- directly to your registered UPI account on <strong>{release_date_display}</strong>.
      </p>
    </div>
    <div class="footer">
      <strong>DBERT (Digital Blinc Education Research and Technology)</strong><br>
      Admissions &amp; Academic Board &bull; WhatsApp Support: +91 81929 11360<br>
      Sovereign Domain: <a href="https://dbert.in" style="color: #38BDF8; text-decoration: none;">https://dbert.in</a> &bull; LMS: <a href="https://lms.dbert.in" style="color: #38BDF8; text-decoration: none;">https://lms.dbert.in</a>
    </div>
  </div>
</div>
</body>
</html>
"""
    return subject, plain, html


def build_cohort_b_email(c: dict, sender: dict) -> tuple:
    name = c.get("name", "Candidate")
    email = c.get("email")
    domain = c.get("domain", "Applied Engineering")
    amount = c.get("amount", 499)
    admin_note = c.get("admin_note", "Complete with current receipt")
    utr = c.get("utr", "")

    subject = f"[ACTION REQUIRED] Update Payment Receipt for DBERT Offer Acceptance ({domain})"

    plain = f"""Dear {name},

This is an official update regarding your DBERT Internship enrollment for the {domain} track.

Our admissions accounts team reviewed your submitted ₹{amount} seat confirmation payment record (UTR: {utr or 'Pending'}). The record could not be reconciled.

REASON / ADVISORY:
"{admin_note}"

To secure your seat and prevent release to waitlisted candidates, please log in to the portal and upload your valid UPI transaction screenshot / enter the current 12-digit UTR:

https://lms.dbert.in/portal/offer

PAYMENT DETAILS FOR RE-SUBMISSION:
- Amount: ₹{amount} (Refundable caution deposit)
- Admissions Merchant VPA: Q652429146@ybl (DBERT Admissions)
- WhatsApp Support: +91 81929 11360

Once updated, your offer letter will be activated and confirmed within 2 business hours.

Warm regards,

{sender['name']}
{sender['title']}
DBERT Admissions Desk
"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; background-color: #07090E; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; }}
.wrapper {{ max-width: 600px; margin: 0 auto; background-color: #0E131F; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; }}
.header {{ background: linear-gradient(135deg, #7C2D12 0%, #9A3412 100%); padding: 32px 28px; border-bottom: 2px solid #EA580C; text-align: left; }}
.badge {{ display: inline-block; background: rgba(251, 146, 60, 0.2); border: 1px solid rgba(251, 146, 60, 0.4); padding: 5px 14px; border-radius: 9999px; font-size: 11px; font-weight: 700; color: #FB923C; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 12px; }}
.header h1 {{ margin: 0 0 6px; font-size: 20px; font-weight: 800; color: #FFFFFF; }}
.body {{ padding: 28px; }}
.note-box {{ background: rgba(234, 88, 12, 0.1); border-left: 4px solid #EA580C; padding: 14px 18px; border-radius: 0 8px 8px 0; margin: 20px 0; font-size: 14px; color: #FED7AA; }}
.btn {{ display: inline-block; background: #EA580C; color: #FFFFFF !important; text-decoration: none; padding: 13px 26px; border-radius: 8px; font-weight: 700; font-size: 14px; text-align: center; margin: 20px 0; }}
.footer {{ padding: 20px 28px; background: #07090E; border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; color: #64748B; text-align: center; }}
</style>
</head>
<body>
<div style="padding: 20px 12px;">
  <div class="wrapper">
    <div class="header">
      <div class="badge">Action Required &bull; Payment Update</div>
      <h1>Transaction Receipt Re-Verification Needed</h1>
    </div>
    <div class="body">
      <p style="font-size: 15px; margin-top: 0;">Dear <strong>{name}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        Our admissions accounts team reviewed your submitted ₹{amount} seat confirmation payment record for the <strong>{domain}</strong> track. The record could not be reconciled.
      </p>

      <div class="note-box">
        <strong>Admissions Review Note:</strong><br>
        <em>"{admin_note}"</em>
      </div>

      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        To ensure your seat is locked and prevent release to waitlisted applicants, please visit the offer portal to re-enter your current 12-digit UTR or upload the correct transaction proof:
      </p>

      <div style="text-align: center;">
        <a href="https://lms.dbert.in/portal/offer" class="btn">Update Payment Details on Portal &rarr;</a>
      </div>

      <p style="font-size: 13px; color: #94A3B8; line-height: 1.6;">
        For instant assistance, you can also share your payment receipt directly with our admissions desk on WhatsApp at <a href="https://wa.me/918192911360" style="color: #38BDF8; text-decoration: none;">+91 81929 11360</a>.
      </p>
    </div>
    <div class="footer">
      <strong>DBERT Admissions &amp; Verification Desk</strong> &bull; https://dbert.in
    </div>
  </div>
</div>
</body>
</html>
"""
    return subject, plain, html


def build_cohort_c_email(c: dict, sender: dict) -> tuple:
    name = c.get("name", "Fellow")
    email = c.get("email")
    domain = c.get("domain", "Applied Engineering")
    missing_gates = c.get("missing_gates", [])
    missing_count = len(missing_gates)
    completed_count = 4 - missing_count
    pct = int((completed_count / 4) * 100)

    subject = f"[UPDATE] {name}, complete {missing_count} remaining step(s) to unlock your ₹5,000 Stipend"

    plain_missing = "\n".join([f"- Step {g['gate_num']}: {g['gate_name']} -> {g['action']}" for g in missing_gates])

    plain = f"""Dear {name},

Here is your current DBERT Stipend Milestone Progression update for the {domain} track.

CURRENT STATUS: {completed_count} of 4 Gates Unlocked ({pct}% Complete)

You are just {missing_count} step(s) away from unlocking your ₹5,000 Technical Milestone Stipend!

REMAINING ACTION ITEMS:
{plain_missing}

To complete your remaining requirements and submit your capstone deliverables, visit your Stipend Milestone Dashboard:
https://lms.dbert.in/stipend/tasks

Once all 4 gates are complete, your submission will be routed to the DBERT Engineering Evaluation Committee for review and scheduled disbursement.

Warm regards,

{sender['name']}
{sender['title']}
DBERT Academic & Incubation Council
"""

    html_items = ""
    for g in missing_gates:
        html_items += f"""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;">
          <div style="font-size: 11px; color: #F59E0B; font-weight: 700; text-transform: uppercase;">Step {g['gate_num']}: {g['gate_name']}</div>
          <div style="font-size: 13px; color: #F1F5F9; margin-top: 4px; line-height: 1.5;">{g['action']}</div>
          <div style="margin-top: 8px;">
            <a href="{g['cta_url']}" style="color: #38BDF8; font-size: 12px; font-weight: 700; text-decoration: none;">Complete Step &rarr;</a>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; background-color: #07090E; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; }}
.wrapper {{ max-width: 600px; margin: 0 auto; background-color: #0E131F; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; }}
.header {{ background: linear-gradient(135deg, #1E1B4B 0%, #312E81 100%); padding: 32px 28px; border-bottom: 2px solid #6366F1; text-align: left; }}
.badge {{ display: inline-block; background: rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.4); padding: 5px 14px; border-radius: 9999px; font-size: 11px; font-weight: 700; color: #A5B4FC; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 12px; }}
.header h1 {{ margin: 0 0 6px; font-size: 20px; font-weight: 800; color: #FFFFFF; }}
.header p {{ margin: 0; font-size: 13px; color: #C7D2FE; }}
.body {{ padding: 28px; }}
.progress-box {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 16px 20px; margin: 20px 0; }}
.btn {{ display: inline-block; background: #6366F1; color: #FFFFFF !important; text-decoration: none; padding: 13px 26px; border-radius: 8px; font-weight: 700; font-size: 14px; text-align: center; margin: 16px 0; }}
.footer {{ padding: 20px 28px; background: #07090E; border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; color: #64748B; text-align: center; }}
</style>
</head>
<body>
<div style="padding: 20px 12px;">
  <div class="wrapper">
    <div class="header">
      <div class="badge">Stipend Progression Update</div>
      <h1>{completed_count} of 4 Gates Unlocked ({pct}% Complete)</h1>
      <p>Only {missing_count} step(s) remaining to unlock your ₹5,000 Stipend</p>
    </div>
    <div class="body">
      <p style="font-size: 15px; margin-top: 0;">Dear <strong>{name}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        Thank you for your active participation in the <strong>{domain}</strong> track. You have successfully cleared {completed_count} pre-flight requirements.
      </p>

      <div style="margin: 22px 0;">
        <div style="font-size: 12px; font-weight: 800; color: #94A3B8; text-transform: uppercase; margin-bottom: 10px;">Remaining Action Items:</div>
        {html_items}
      </div>

      <div style="text-align: center;">
        <a href="https://lms.dbert.in/stipend/tasks" class="btn">Open Stipend Dashboard &rarr;</a>
      </div>

      <p style="font-size: 13px; color: #94A3B8; line-height: 1.6; text-align: center; margin-top: 20px;">
        Once all gates are satisfied, your submission is routed to the DBERT Evaluation Committee for final sign-off and payout scheduling.
      </p>
    </div>
    <div class="footer">
      <strong>DBERT Academic &amp; Incubation Council</strong> &bull; https://dbert.in
    </div>
  </div>
</div>
</body>
</html>
"""
    return subject, plain, html


def build_cohort_a_email(c: dict, sender: dict) -> tuple:
    name = c.get("name", "Candidate")
    email = c.get("email")
    domain = c.get("domain", "Applied Engineering")

    subject = f"[OFFER LETTER AVAILABLE] Congratulations {name} — DBERT Internship Offer Selected"

    plain = f"""Dear {name},

Congratulations! We are delighted to inform you that your application for the DBERT Technical Internship in {domain} has been reviewed and officially SELECTED by the DBERT Academic Selection Board.

YOUR NEXT CTA:
1. Review your Letter of Offer & Term Details online at:
   https://lms.dbert.in/portal/offer
2. Confirm your seat by completing the ₹499 refundable caution deposit.
   (The ₹499 deposit is credited in full towards your program ledger and is refundable upon milestone completion).

OFFER HIGHLIGHTS:
- Domain Track: {domain}
- Program Head: Mr. Abhinav Sharma
- Caution Deposit: ₹499 (100% refundable upon project completion)
- Stipend Opportunity: Up to ₹5,000 on capstone milestone delivery
- Offer Access Link: https://lms.dbert.in/portal/offer

Please complete your acceptance within 48 hours to ensure your incubation seat is reserved.

For any assistance or payment questions, reach out via WhatsApp Admissions:
https://wa.me/918192911360?text={quote(f'Hi Admissions, I received my offer for {domain} and need assistance.')}

Warm regards,

{sender['name']}
{sender['title']}
DBERT Academic Admissions
Digital Blinc Education Research and Technology
Portal: https://dbert.in | LMS: https://lms.dbert.in
"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ margin: 0; padding: 0; background-color: #07090E; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #E2E8F0; }}
.wrapper {{ max-width: 600px; margin: 0 auto; background-color: #0E131F; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; overflow: hidden; }}
.header {{ background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%); padding: 36px 30px; border-bottom: 2px solid #3B82F6; text-align: left; }}
.badge {{ display: inline-block; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); padding: 5px 14px; border-radius: 9999px; font-size: 11px; font-weight: 700; color: #93C5FD; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 12px; }}
.header h1 {{ margin: 0 0 6px; font-size: 22px; font-weight: 800; color: #FFFFFF; }}
.header p {{ margin: 0; font-size: 14px; color: #BFDBFE; }}
.body {{ padding: 30px; }}
.card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 18px 22px; margin: 20px 0; }}
.btn {{ display: inline-block; background: #2563EB; color: #FFFFFF !important; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-weight: 700; font-size: 14px; text-align: center; margin: 18px 0; }}
.footer {{ padding: 22px 30px; background: #07090E; border-top: 1px solid rgba(255,255,255,0.06); font-size: 12px; color: #64748B; text-align: center; }}
</style>
</head>
<body>
<div style="padding: 20px 12px;">
  <div class="wrapper">
    <div class="header">
      <div class="badge">Official Selection &bull; Incubation Cohort</div>
      <h1>Letter of Offer Ready for Review</h1>
      <p>Congratulations on your selection to the DBERT Technical Fellowship</p>
    </div>
    <div class="body">
      <p style="font-size: 15px; margin-top: 0;">Dear <strong>{name}</strong>,</p>
      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        We are delighted to confirm that your application for the <strong>{domain}</strong> track has been selected. Your digital Letter of Offer is now available for review and acceptance.
      </p>

      <div class="card">
        <div style="font-size: 11px; color: #94A3B8; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Offer Details</div>
        <div style="font-size: 16px; font-weight: 800; color: #F8FAFC; margin-top: 6px;">{domain} Track</div>
        <div style="font-size: 13px; color: #38BDF8; margin-top: 4px;">Milestone Stipend Eligibility: Up to ₹5,000</div>
        <div style="font-size: 12px; color: #94A3B8; margin-top: 6px;">Refundable Seat Deposit: ₹499 (credited in full)</div>
      </div>

      <p style="font-size: 14px; line-height: 1.6; color: #CBD5E1;">
        Please review your offer terms and complete your ₹499 seat confirmation within 48 hours to secure your placement:
      </p>

      <div style="text-align: center;">
        <a href="https://lms.dbert.in/portal/offer" class="btn">Review Offer &amp; Confirm Seat &rarr;</a>
      </div>

      <p style="font-size: 13px; color: #94A3B8; line-height: 1.6; text-align: center; margin-top: 18px;">
        Questions? Connect with our Admissions Concierge on WhatsApp at <a href="https://wa.me/918192911360" style="color: #38BDF8; text-decoration: none;">+91 81929 11360</a>.
      </p>
    </div>
    <div class="footer">
      <strong>DBERT Admissions &amp; Incubation Desk</strong> &bull; https://dbert.in &bull; https://lms.dbert.in
    </div>
  </div>
</div>
</body>
</html>
"""
    return subject, plain, html

def send_completion_telemetry(sent_count: int, failed_count: int, skipped_count: int, total_count: int, elapsed_sec: float, tracking: dict):
    subject = f"[TELEMETRY] DBERT Cohort Dispatch Completed: {sent_count}/{total_count} Delivered ({len(SMTP_ACCOUNTS)} SMTP Accounts)"
    
    elapsed_min = round(elapsed_sec / 60, 1)
    cohort_breakdown = {"A": 0, "B": 0, "C": 0, "D": 0}
    for k, v in tracking.items():
        if v.get("status") == "SENT":
            c = v.get("cohort", "Unknown")
            cohort_breakdown[c] = cohort_breakdown.get(c, 0) + 1

    body = f"""DBERT OPERATIONAL DISPATCH TELEMETRY REPORT
================================================================================
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Targets: {total_count}
Successfully Delivered: {sent_count}
Skipped (Already Sent): {skipped_count}
Failed: {failed_count}
Elapsed Time: {elapsed_min} minutes
SMTP Node Pool: 5 Google Workspace relay accounts rotated

COHORT DELIVERY BREAKDOWN:
- Cohort D (Stipend Approved & Scheduled Payout): {cohort_breakdown.get('D', 0)}
- Cohort B (Rejected Payments Re-Submission): {cohort_breakdown.get('B', 0)}
- Cohort C (Pending Gates Guidance): {cohort_breakdown.get('C', 0)}
- Cohort A (Selected Offer Letter & 499 Deposit): {cohort_breakdown.get('A', 0)}

Live Tracking File: data/cohort_dispatch_tracking.json
Audit Log: data/cohort_dispatch.log
================================================================================
"""
    log("Sending completion telemetry...")
    sender = SMTP_ACCOUNTS[0]
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=20) as s:
            s.login(sender["user"], sender["pass"])
            for rcpt in TELEMETRY_EMAILS:
                msg = MIMEMultipart("plain")
                msg["Subject"] = subject
                msg["From"] = f"{sender['name']} <{sender['user']}>"
                msg["To"] = rcpt
                msg["Date"] = formatdate(localtime=True)
                msg.attach(MIMEText(body, "plain", "utf-8"))
                s.sendmail(sender["user"], [rcpt], msg.as_string())
                log(f"   -> Telemetry sent to {rcpt}")
    except Exception as e:
        log(f"   -> Failed to send telemetry: {e}")

# ==============================================================================
# MAIN DISPATCH LOOP
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Dispatch emails across all 4 cohorts.")
    parser.add_argument("--live", action="store_true", help="Execute live SMTP delivery (default: dry-run)")
    parser.add_argument("--cohort", choices=["A", "B", "C", "D", "all"], default="all", help="Target cohort (default: all)")
    parser.add_argument("--delay", type=float, default=12.0, help="Delay in seconds between sends (default: 12s)")
    args = parser.parse_args()

    tracking = load_tracking()

    print("=" * 80)
    print("DBERT MULTI-SMTP COHORT DISPATCH PIPELINE")
    print(f"Mode: {'LIVE DISPATCH' if args.live else 'DRY RUN (Preview Only)'} | Cohort: {args.cohort.upper()}")
    print("=" * 80)

    # Load cohorts
    data_dir = ROOT_DIR / "data"
    cohort_a = json.load(open(data_dir / "cohort_a_final.json", encoding="utf-8")) if (args.cohort in ["A", "all"]) else []
    cohort_b = json.load(open(data_dir / "cohort_b_final.json", encoding="utf-8")) if (args.cohort in ["B", "all"]) else []
    cohort_c = json.load(open(data_dir / "cohort_c_final.json", encoding="utf-8")) if (args.cohort in ["C", "all"]) else []
    cohort_d = json.load(open(data_dir / "cohort_d_final.json", encoding="utf-8")) if (args.cohort in ["D", "all"]) else []

    # Tag records with cohort
    queue = []
    # Highest priority: Cohort D (Stipend Approved) -> B (Rejected) -> C (Pending Gates) -> A (Offer Unpaid)
    for c in cohort_d: queue.append(("D", c))
    for c in cohort_b: queue.append(("B", c))
    for c in cohort_c: queue.append(("C", c))
    for c in cohort_a: queue.append(("A", c))

    log(f"Queue loaded: {len(queue)} total recipients across targeted cohorts.")
    print(f"Cohort Breakdown -> D: {len(cohort_d)}, B: {len(cohort_b)}, C: {len(cohort_c)}, A: {len(cohort_a)}")

    smtp_index = 0
    active_smtp = None
    server = None

    sent_count = 0
    skipped_count = 0
    failed_count = 0
    start_time = time.time()

    try:
        for idx, (cohort_name, cand) in enumerate(queue, 1):
            email = cand["email"].strip().lower()
            key = f"COHORT_{cohort_name}_{email}"

            if tracking.get(key, {}).get("status") == "SENT":
                skipped_count += 1
                continue

            # Rotate SMTP account
            active_smtp = SMTP_ACCOUNTS[smtp_index % len(SMTP_ACCOUNTS)]
            smtp_index += 1

            if cohort_name == "D":
                subject, plain, html = build_cohort_d_email(cand, active_smtp)
            elif cohort_name == "B":
                subject, plain, html = build_cohort_b_email(cand, active_smtp)
            elif cohort_name == "C":
                subject, plain, html = build_cohort_c_email(cand, active_smtp)
            else:
                subject, plain, html = build_cohort_a_email(cand, active_smtp)

            if not args.live:
                log(f"[DRY-RUN] #{idx}/{len(queue)} [Cohort {cohort_name}] -> {email} ({cand.get('name')}) via {active_smtp['user']}: {subject[:55]}...")
                sent_count += 1
                continue

            # Live Send
            try:
                if server is None:
                    server = get_smtp_connection(active_smtp)

                msg = MIMEMultipart("alternative")
                msg["Subject"] = subject
                msg["From"] = f"{active_smtp['name']} <{active_smtp['user']}>"
                msg["To"] = email
                msg["Date"] = formatdate(localtime=True)
                msg["Message-ID"] = make_msgid(domain="dbert.in")
                msg["Reply-To"] = active_smtp["user"]
                msg["X-Entity-Ref-ID"] = key

                msg.attach(MIMEText(plain, "plain", "utf-8"))
                msg.attach(MIMEText(html, "html", "utf-8"))

                server.sendmail(active_smtp["user"], [email], msg.as_string())
                log(f"[LIVE-SENT] #{idx}/{len(queue)} [Cohort {cohort_name}] -> {email} via {active_smtp['user']}")

                tracking[key] = {
                    "cohort": cohort_name,
                    "email": email,
                    "name": cand.get("name"),
                    "status": "SENT",
                    "sender": active_smtp["user"],
                    "sent_at": datetime.now().isoformat(),
                    "subject": subject
                }
                save_tracking(tracking)
                sent_count += 1

                time.sleep(args.delay)

            except Exception as e:
                log(f"[ERROR] #{idx} [Cohort {cohort_name}] -> {email} failed via {active_smtp['user']}: {e}")
                failed_count += 1
                # Close server so next iteration reconnects
                try:
                    if server: server.quit()
                except Exception:
                    pass
                server = None
                time.sleep(5)

    finally:
        if server:
            try: server.quit()
            except Exception: pass

    log(f"Pipeline completed: Sent: {sent_count}, Skipped (Already Sent): {skipped_count}, Failed: {failed_count}")
    if args.live:
        elapsed_sec = time.time() - start_time
        send_completion_telemetry(sent_count, failed_count, skipped_count, len(queue), elapsed_sec, tracking)

if __name__ == "__main__":
    main()
