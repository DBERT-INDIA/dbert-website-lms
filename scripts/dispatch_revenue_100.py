import os
import sys
import json
import time
import smtplib
import random
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

TARGET_COHORT_PATH = "data/balanced_revenue_target_100.json"
TRACKING_PATH = "data/dispatch_tracking_revenue_100.json"
LOG_PATH = "data/dispatch_revenue_100.log"

ACCOUNTS = [
    {"user": "abhinav.sharma@dbert.in", "pass": "rsupmvvvvwrsuxuh", "name": "Abhinav Sharma | Admissions Director"},
    {"user": "manoj.kumar@dbert.in", "pass": "fnevtpseplwibckr", "name": "Manoj Kumar | Incubation Head"},
    {"user": "sandeep.bannu@dbert.in", "pass": "qtqzlmrynbcxvyjy", "name": "Sandeep Bannu | Engineering Lead"},
    {"user": "contactus@dbert.in", "pass": "llvmaajmrljpcwru", "name": "DBERT Admissions & Sprints Desk"},
    {"user": "pulkit.kunar@dbert.in", "pass": "vzefecwpggxuaztr", "name": "Pulkit Kumar | Fellowship Coordinator"}
]

REPORT_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

def get_smtp_connection(account):
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30)
    server.login(account["user"], account["pass"])
    return server

def build_email_payload(cand, sender_account):
    name = cand.get("name", "Fellow").strip()
    amount = cand.get("amount", 499)
    domain = cand.get("domain", "Applied Engineering")
    college = cand.get("college", "Engineering Institute")
    email = cand.get("email", "").strip()

    msg = MIMEMultipart("alternative")
    msg["Message-ID"] = f"<{uuid.uuid4()}@dbert.in>"
    msg["From"] = f"{sender_account['name']} <{sender_account['user']}>"
    msg["To"] = f"{name} <{email}>"
    msg["Reply-To"] = sender_account["user"]

    if amount == 499:
        # Caution deposit template
        priority_tier = cand.get("priority_tier", 2)
        if priority_tier == 1:
            subject = f"ACTION REQUIRED: Complete ₹499 Caution Deposit & Confirm Monday Incubation Seat — {name}"
            hero_badge = "RECONCILIATION & SEAT LOCK NOTICE"
            main_heading = "Finalize Your ₹499 Caution Deposit to Unlock Incubation & LMS"
            intro_p = f"We noticed your previous ₹499 caution deposit submission was flagged or pending verification. Your seat in the upcoming <strong>{domain}</strong> cohort is on hold until <strong>6:00 PM today</strong>."
        else:
            subject = f"CONFIRMATION: Lock Your Incubation Seat with ₹499 Caution Deposit (Refundable) — {name}"
            hero_badge = "INCUBATION SEAT RESERVATION"
            main_heading = "Confirm Your Incubation Seat with ₹499 Caution Deposit"
            intro_p = f"Congratulations on your selection for the <strong>{domain}</strong> Incubation Fellowship! To finalize your admission and activate your LMS workspace for Monday's kickoff, please complete your ₹499 caution deposit before <strong>6:00 PM today</strong>."

        body_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{subject}</title></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 24px 12px; color: #1e293b;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 640px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
    <!-- Header -->
    <tr>
      <td style="background-color: #0f172a; padding: 32px 28px; text-align: left; border-bottom: 3px solid #3b82f6;">
        <div style="color: #60a5fa; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">DBERT APPLIED RESEARCH & FELLOWSHIP</div>
        <div style="display: inline-block; background-color: #f59e0b; color: #000000; font-size: 10px; font-weight: 800; padding: 4px 10px; border-radius: 9999px; letter-spacing: 0.5px; margin-bottom: 12px;">{hero_badge}</div>
        <h1 style="color: #ffffff; font-size: 22px; margin: 0; font-weight: 700; line-height: 1.3;">{main_heading}</h1>
      </td>
    </tr>
    <!-- Content -->
    <tr>
      <td style="padding: 28px;">
        <p style="font-size: 15px; line-height: 1.6; margin-top: 0;">Dear <strong>{name}</strong>,</p>
        <p style="font-size: 14px; line-height: 1.6; color: #334155;">{intro_p}</p>

        <!-- Transparency Ledger Box -->
        <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px; margin: 24px 0;">
          <div style="font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Official Fee Structure & Benefits Breakdown</div>
          <table width="100%" style="font-size: 13px; color: #1e293b; border-collapse: collapse;">
            <tr>
              <td style="padding: 6px 0; border-bottom: 1px solid #e2e8f0;">Program Domain</td>
              <td style="padding: 6px 0; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 600;">{domain}</td>
            </tr>
            <tr>
              <td style="padding: 6px 0; border-bottom: 1px solid #e2e8f0;">Caution Deposit Payable</td>
              <td style="padding: 6px 0; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 700; color: #2563eb;">₹499 (100% Credited / Refundable)</td>
            </tr>
            <tr>
              <td style="padding: 6px 0; border-bottom: 1px solid #e2e8f0;">Batch Kickoff</td>
              <td style="padding: 6px 0; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 600;">Monday, 6:00 PM IST</td>
            </tr>
            <tr>
              <td style="padding: 6px 0;">Payment Cutoff</td>
              <td style="padding: 6px 0; text-align: right; font-weight: 700; color: #dc2626;">Today, 6:00 PM IST</td>
            </tr>
          </table>
        </div>

        <!-- Benefits Highlights -->
        <h3 style="font-size: 15px; font-weight: 700; color: #0f172a; margin: 20px 0 10px 0;">What Completing Your ₹499 Unlocks:</h3>
        <ul style="font-size: 13.5px; color: #334155; line-height: 1.6; padding-left: 20px; margin: 0 0 24px 0;">
          <li><strong>Production Sprint Workspace:</strong> Immediate access to LMS interactive coding lab, AI mentor tutor, and cohort repositories.</li>
          <li><strong>100% Credited or Refundable:</strong> The ₹499 is credited in full towards your incubation fee or refunded upon completing required milestone sprints.</li>
          <li><strong>₹5,000 Stipend Unlock:</strong> Eligibility to earn up to ₹5,000 in fellowship stipend across 4 verified contribution gates.</li>
          <li><strong>Official Letter of Selection:</strong> Verifiable offer letter and admission dossier hosted on sovereign domain <code>dbert.in</code>.</li>
        </ul>

        <!-- Primary Action CTA -->
        <div style="text-align: center; margin: 28px 0 20px 0;">
          <a href="https://lms.dbert.in/portal" style="display: inline-block; background-color: #2563eb; color: #ffffff; text-decoration: none; font-size: 15px; font-weight: 700; padding: 14px 32px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);">Access LMS & Pay ₹499 Fast-Pay →</a>
        </div>
        <p style="text-align: center; font-size: 12px; color: #64748b; margin-top: 8px;">Supports Google Pay, PhonePe, Paytm, and all UPI apps directly on your portal.</p>

        <!-- Fast Assistance / Proof Submission -->
        <div style="background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 16px; margin: 24px 0;">
          <div style="font-weight: 700; color: #065f46; font-size: 13px; margin-bottom: 6px;">Need Assistance or Already Paid?</div>
          <p style="font-size: 13px; color: #047857; margin: 0 0 10px 0; line-height: 1.5;">If you have completed payment or have a pending UTR, share your 12-digit transaction number directly with our Admissions Desk for instant 10-minute manual reconciliation.</p>
          <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20{name}%20({email}).%20Here%20is%20my%20%E2%82%B9499%20payment%20proof%2FUTR%3A%20" style="display: inline-block; background-color: #059669; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 700; padding: 8px 16px; border-radius: 6px;">Share Proof on WhatsApp (+91 81929 11360) →</a>
        </div>
      </td>
    </tr>
    <!-- Footer -->
    <tr>
      <td style="background-color: #f8fafc; padding: 20px 28px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b; line-height: 1.5;">
        <p style="margin: 0 0 4px 0;"><strong>DBERT Admissions & Incubation Governance</strong></p>
        <p style="margin: 0 0 8px 0;">Active Sovereign Domain: <a href="https://dbert.in" style="color: #2563eb; text-decoration: none;">dbert.in</a> | LMS Portal: <a href="https://lms.dbert.in" style="color: #2563eb; text-decoration: none;">lms.dbert.in</a></p>
        <p style="margin: 0; color: #94a3b8; font-size: 11px;">Notice: Legacy domain dbert.online is permanently retired. All official dispatches originate strictly from @dbert.in.</p>
      </td>
    </tr>
  </table>
</body>
</html>"""
        body_text = f"""DBERT INCUBATION SEAT CONFIRMATION (₹499)

Dear {name},

{intro_p.replace('<strong>', '').replace('</strong>', '')}

OFFICIAL DETAILS:
- Domain Track: {domain}
- Caution Deposit: ₹499 (100% Credited / Refundable upon milestone sprints)
- Batch Kickoff: Monday, 6:00 PM IST
- Payment Cutoff: Today, 6:00 PM IST

WHAT COMPOSING YOUR ₹499 UNLOCKS:
1. Immediate access to production LMS interactive sprint lab & mentor guidance.
2. 100% credited against your balance or refundable upon sprint milestones.
3. Eligibility to unlock up to ₹5,000 in stipend across verified progression gates.
4. Tamper-proof admission dossier hosted on dbert.in.

COMPLETE YOUR ₹499 PAYMENT HERE:
👉 https://lms.dbert.in/portal

NEED ASSISTANCE OR ALREADY PAID?
Share your 12-digit UTR on WhatsApp for instant manual verification:
👉 https://wa.me/918192911360

Admissions Desk: abhinav.sharma@dbert.in | dbert.in
"""
    else:
        # ₹299 Credential Verification & Gate 3 template
        subject = f"ACTION REQUIRED: Complete Gate 3 Credential Verification (₹299) to Unlock ₹5,000 Stipend — {name}"
        hero_badge = "GATE 3 MILESTONE AUDIT"
        main_heading = "Unlock Your ₹5,000 Fellowship Stipend Release"
        intro_p = f"You have demonstrated impressive technical progress in the <strong>{domain}</strong> Fellowship track! Our system indicates that you have active milestone submissions (LinkedIn / GitHub), but your <strong>Gate 3: Official Credential Verification</strong> is currently pending."

        body_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{subject}</title></head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f6f9; margin: 0; padding: 24px 12px; color: #1e293b;">
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width: 640px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);">
    <!-- Header -->
    <tr>
      <td style="background-color: #0f172a; padding: 32px 28px; text-align: left; border-bottom: 3px solid #10b981;">
        <div style="color: #34d399; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">DBERT FELLOWSHIP ADVANCEMENT ENGINE</div>
        <div style="display: inline-block; background-color: #10b981; color: #ffffff; font-size: 10px; font-weight: 800; padding: 4px 10px; border-radius: 9999px; letter-spacing: 0.5px; margin-bottom: 12px;">{hero_badge}</div>
        <h1 style="color: #ffffff; font-size: 22px; margin: 0; font-weight: 700; line-height: 1.3;">{main_heading}</h1>
      </td>
    </tr>
    <!-- Content -->
    <tr>
      <td style="padding: 28px;">
        <p style="font-size: 15px; line-height: 1.6; margin-top: 0;">Dear <strong>{name}</strong>,</p>
        <p style="font-size: 14px; line-height: 1.6; color: #334155;">{intro_p}</p>

        <!-- 4-Gate Progression Scorecard -->
        <div style="background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; padding: 18px; margin: 24px 0;">
          <div style="font-size: 12px; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">Your 4-Gate Fellowship Stipend Status</div>
          <table width="100%" style="font-size: 13px; color: #1e293b; border-collapse: collapse;">
            <tr>
              <td style="padding: 8px 0; border-bottom: 1px solid #e2e8f0;">Gate 1: Professional LinkedIn Profile</td>
              <td style="padding: 8px 0; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 700; color: #16a34a;">✓ Connected / Active</td>
            </tr>
            <tr>
              <td style="padding: 8px 0; border-bottom: 1px solid #e2e8f0;">Gate 2: Technical Case Study Article</td>
              <td style="padding: 8px 0; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 700; color: #2563eb;">Ready for Review / In Progress</td>
            </tr>
            <tr style="background-color: #fef2f2;">
              <td style="padding: 8px 6px; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #b91c1c;">Gate 3: Official Credential Verification (₹299)</td>
              <td style="padding: 8px 6px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: 800; color: #dc2626;">⏳ PENDING UNLOCK</td>
            </tr>
            <tr>
              <td style="padding: 8px 0;">Gate 4: Active Technical GitHub Repository</td>
              <td style="padding: 8px 0; text-align: right; font-weight: 700; color: #16a34a;">✓ Connected / Active</td>
            </tr>
          </table>
        </div>

        <!-- Benefits Highlights -->
        <h3 style="font-size: 15px; font-weight: 700; color: #0f172a; margin: 20px 0 10px 0;">Why Complete Gate 3 Credential Verification (₹299) Today:</h3>
        <ul style="font-size: 13.5px; color: #334155; line-height: 1.6; padding-left: 20px; margin: 0 0 24px 0;">
          <li><strong>Direct Stipend Release:</strong> Unlocks release eligibility for the <strong>₹5,000 cash stipend</strong> (credited as 5,000 withdrawable coins directly to your LMS UPI wallet).</li>
          <li><strong>Official 3-Document Executive Packet:</strong> Cryptographically verified Certificate of Completion, Academic Rubric Evaluation (Score/100), and Official Letter of Recommendation (LOR) signed by the Director.</li>
          <li><strong>Featured on Pre-Vetted Engineers Directory:</strong> Permanent public listing on <a href="https://dbert.in/verify/directory" style="color: #2563eb;">dbert.in/verify/directory</a> accessible to 60+ hiring partner companies.</li>
          <li><strong>Turnitin Plagiarism Seal:</strong> Formally verified authenticity rating eliminating credential fraud.</li>
        </ul>

        <!-- Primary Action CTA -->
        <div style="text-align: center; margin: 28px 0 20px 0;">
          <a href="https://dbert.in/enroll/1999" style="display: inline-block; background-color: #059669; color: #ffffff; text-decoration: none; font-size: 15px; font-weight: 700; padding: 14px 32px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.3);">Unlock Gate 3 Verification (₹299) →</a>
        </div>
        <p style="text-align: center; font-size: 12px; color: #64748b; margin-top: 8px;">Or fill out the official verification form at <a href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform" style="color: #2563eb;">Google Form Verification</a></p>

        <!-- Fast Assistance / Proof Submission -->
        <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 16px; margin: 24px 0;">
          <div style="font-weight: 700; color: #1e40af; font-size: 13px; margin-bottom: 6px;">Questions About Stipend Release?</div>
          <p style="font-size: 13px; color: #1d4ed8; margin: 0 0 10px 0; line-height: 1.5;">Connect directly with our Fellowship Governance Desk on WhatsApp to review your gate submissions and confirm instant verification clearance.</p>
          <a href="https://wa.me/918958006294?text=Hi%20Mentorship%20Desk%2C%20I%20am%20{name}%20({email}).%20I%20am%20ready%20to%20complete%20Gate%203%20Verification%20(%E2%82%B9299)%20to%20unlock%20my%20stipend.%20" style="display: inline-block; background-color: #2563eb; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 700; padding: 8px 16px; border-radius: 6px;">Contact Mentorship WhatsApp (+91 89580 06294) →</a>
        </div>
      </td>
    </tr>
    <!-- Footer -->
    <tr>
      <td style="background-color: #f8fafc; padding: 20px 28px; border-top: 1px solid #e2e8f0; font-size: 12px; color: #64748b; line-height: 1.5;">
        <p style="margin: 0 0 4px 0;"><strong>DBERT Fellowship & Credentials Authority</strong></p>
        <p style="margin: 0 0 8px 0;">Active Sovereign Domain: <a href="https://dbert.in" style="color: #2563eb; text-decoration: none;">dbert.in</a> | Stipend Tasks: <a href="https://lms.dbert.in/stipend/tasks" style="color: #2563eb; text-decoration: none;">lms.dbert.in/stipend/tasks</a></p>
        <p style="margin: 0; color: #94a3b8; font-size: 11px;">Notice: Legacy domain dbert.online is permanently retired. All official dispatches originate strictly from @dbert.in.</p>
      </td>
    </tr>
  </table>
</body>
</html>"""
        body_text = f"""DBERT FELLOWSHIP GATE 3 AUDIT & STIPEND UNLOCK (₹299)

Dear {name},

{intro_p.replace('<strong>', '').replace('</strong>', '')}

YOUR 4-GATE STIPEND PROGRESSION STATUS:
- Gate 1 (LinkedIn): ✓ Connected / Active
- Gate 2 (Case Study Article): Ready for Review / In Progress
- Gate 3 (₹299 Credential Verification): ⏳ PENDING UNLOCK
- Gate 4 (Technical GitHub Repository): ✓ Connected / Active

WHY COMPLETE GATE 3 (₹299) TODAY:
1. Direct Release of your ₹5,000 cash stipend (5,000 coins to your LMS UPI wallet).
2. Official 3-Document Executive Packet: Certificate, Project Rubric (Score/100), and signed Director LOR.
3. Permanent verified listing on the Pre-Vetted Engineers Directory (dbert.in/verify/directory) seen by 60+ hiring companies.
4. Cryptographically verifiable Turnitin originality seal.

UNLOCK GATE 3 VERIFICATION HERE:
👉 https://dbert.in/enroll/1999
Or fill out Google Form:
👉 https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform

QUESTIONS ABOUT STIPEND RELEASE?
WhatsApp Mentorship Desk directly:
👉 https://wa.me/918958006294

Fellowship Desk: abhinav.sharma@dbert.in | dbert.in
"""

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html", "utf-8"))
    return msg, subject

def send_telemetry(sent_count, total_count, note=""):
    try:
        sender = ACCOUNTS[0]
        server = get_smtp_connection(sender)
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"TELEMETRY: Revenue Dispatch Milestone — {sent_count}/{total_count} Delivered"
        msg["From"] = f"DBERT Telemetry <{sender['user']}>"
        msg["To"] = ", ".join(REPORT_EMAILS)

        content = f"""DBERT REVENUE TARGET COHORT DISPATCH TELEMETRY
======================================================
Progress: {sent_count}/{total_count} delivered ({round(sent_count/total_count*100, 1)}%)
Target Revenue Pool: ₹5,000 by 6:00 PM Today
Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")}
Note: {note}

Delivered via 5 authenticated Google Workspace accounts with anti-spam pacing.
Audit Log: {LOG_PATH}
"""
        msg.attach(MIMEText(content, "plain", "utf-8"))
        server.send_message(msg)
        server.quit()
        log(f"Telemetry report sent successfully to {REPORT_EMAILS}")
    except Exception as e:
        log(f"[WARN] Failed to send telemetry: {e}")

def run_test_suite(target_email):
    log(f"Executing Revenue Test Suite -> {target_email}")
    # 1 sample 499, 1 sample 299
    sample_499 = {
        "name": "Abhinav Sharma",
        "email": target_email,
        "amount": 499,
        "domain": "Artificial Intelligence & ML",
        "college": "IIT Kharagpur",
        "priority_tier": 1
    }
    sample_299 = {
        "name": "Abhinav Sharma",
        "email": target_email,
        "amount": 299,
        "domain": "Full Stack Web Development",
        "college": "IIT Kharagpur",
        "priority_tier": 3
    }

    # Send 499 sample
    acc1 = ACCOUNTS[0]
    log(f"Sending sample ₹499 via {acc1['user']}...")
    server = get_smtp_connection(acc1)
    msg, sub = build_email_payload(sample_499, acc1)
    server.send_message(msg)
    server.quit()
    log(f"  ✓ Sample ₹499 sent! MsgID: {msg['Message-ID']}")

    time.sleep(3)

    # Send 299 sample
    acc2 = ACCOUNTS[1]
    log(f"Sending sample ₹299 via {acc2['user']}...")
    server = get_smtp_connection(acc2)
    msg, sub = build_email_payload(sample_299, acc2)
    server.send_message(msg)
    server.quit()
    log(f"  ✓ Sample ₹299 sent! MsgID: {msg['Message-ID']}")

    log("Revenue Test Suite complete!")

def run_dispatch(live=False, delay_min=18.0, delay_max=26.0):
    with open(TARGET_COHORT_PATH, "r", encoding="utf-8") as f:
        cohort = json.load(f)

    total = len(cohort)
    log("="*80)
    log(f"Starting Revenue Cohort Dispatch for {total} candidates (Mode: {'LIVE' if live else 'DRY RUN'})")
    log("="*80)

    # Load existing tracking
    tracking = {}
    if os.path.exists(TRACKING_PATH):
        try:
            with open(TRACKING_PATH, "r", encoding="utf-8") as f:
                for row in json.load(f):
                    tracking[row["email"].lower()] = row
        except Exception:
            pass

    sent_this_session = 0
    server = None
    current_account_idx = -1

    for idx, cand in enumerate(cohort, start=1):
        email = cand["email"].strip().lower()
        amount = cand.get("amount", 499)

        if tracking.get(email, {}).get("status") == "SENT":
            log(f"[{idx}/{total}] Skipping already SENT candidate: {cand.get('name')} <{email}>")
            continue

        target_acc_idx = (idx - 1) % len(ACCOUNTS)
        account = ACCOUNTS[target_acc_idx]

        log(f">>> [{idx}/{total}] Dispatching to: {cand.get('name')} <{email}> [₹{amount}] via {account['user']}")

        if not live:
            time.sleep(0.01)
            msg_id = f"<dry-run-{uuid.uuid4()}@dbert.in>"
            tracking[email] = {
                "email": email,
                "name": cand.get("name"),
                "amount": amount,
                "status": "SENT",
                "sent_at": datetime.now().isoformat(),
                "sender": account["user"],
                "message_id": msg_id
            }
            log(f"  ✓ [DRY RUN OK] Sim MsgID: {msg_id}")
            continue

        # Live dispatch
        if server is None or current_account_idx != target_acc_idx:
            if server is not None:
                try: server.quit()
                except Exception: pass
            current_account_idx = target_acc_idx
            server = get_smtp_connection(account)

        msg, sub = build_email_payload(cand, account)
        server.send_message(msg)
        msg_id = msg["Message-ID"]

        tracking[email] = {
            "email": email,
            "name": cand.get("name"),
            "amount": amount,
            "status": "SENT",
            "sent_at": datetime.now().isoformat(),
            "sender": account["user"],
            "message_id": msg_id
        }
        sent_this_session += 1
        log(f"  ✓ [SUCCESS] MsgID: {msg_id}")

        # Persist atomic tracking
        with open(TRACKING_PATH, "w", encoding="utf-8") as f:
            json.dump(list(tracking.values()), f, indent=2)

        # Milestone telemetry
        if sent_this_session % 25 == 0:
            send_telemetry(sent_this_session, total, note=f"Completed {sent_this_session} dispatches")

        # Anti-spam delay
        if idx < total:
            delay = random.uniform(delay_min, delay_max)
            log(f"  Sleeping {delay:.1f}s before next dispatch (anti-spam pacing)...")
            time.sleep(delay)

    if server is not None:
        try: server.quit()
        except Exception: pass

    # Persist final state
    with open(TRACKING_PATH, "w", encoding="utf-8") as f:
        json.dump(list(tracking.values()), f, indent=2)

    log("="*80)
    log(f"REVENUE COHORT DISPATCH COMPLETE: {sent_this_session}/{total} DELIVERED.")
    log("="*80)

    if live:
        send_telemetry(sent_this_session, total, note="BATCH 100% COMPLETED")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Revenue Target Cohort Dispatcher (₹5000 Target)")
    parser.add_argument("--live", action="store_true", help="Execute live SMTP sending")
    parser.add_argument("--dry-run", action="store_true", help="Simulate batch rendering and state tracking")
    parser.add_argument("--test-suite", type=str, metavar="EMAIL", help="Send sample ₹499 and ₹299 templates to target email")
    parser.add_argument("--delay-min", type=float, default=18.0, help="Min delay between dispatches (seconds)")
    parser.add_argument("--delay-max", type=float, default=26.0, help="Max delay between dispatches (seconds)")

    args = parser.parse_args()

    if args.test_suite:
        run_test_suite(args.test_suite)
    elif args.live:
        run_dispatch(live=True, delay_min=args.delay_min, delay_max=args.delay_max)
    else:
        run_dispatch(live=False)
