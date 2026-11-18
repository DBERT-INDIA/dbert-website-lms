#!/usr/bin/env python3
"""
scripts/dispatch_inbox_responses.py
Dispatches tailored, professional responses to candidate inbox inquiries
via Google Workspace SMTP and updates IMAP read state.
"""

import os
import sys
import json
import time
import imaplib
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid, parseaddr

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
DATA_DIR = ROOT_DIR / "data"

if str(PORTAL_DIR) not in sys.path:
    sys.path.insert(0, str(PORTAL_DIR))

# Load .env
env_file = PORTAL_DIR / ".env"
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k not in os.environ:
                    os.environ[k] = v

from services.delivery_service import EmailDeliveryService

REPLIES_LOG_FILE = DATA_DIR / "inbox_replies_log.json"

def get_account_by_email(service: EmailDeliveryService, email_addr: str):
    clean = email_addr.strip().lower()
    for acc in service.pool.accounts:
        if acc.email.lower() == clean:
            return acc
    return service.pool.accounts[0]

def send_threaded_email(
    acc,
    to_email: str,
    subject: str,
    html_body: str,
    text_body: str,
    in_reply_to: str = "",
    references: str = ""
) -> tuple:
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{acc.from_name} <{acc.email}>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    msg["Reply-To"] = acc.email

    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references
    elif in_reply_to:
        msg["References"] = in_reply_to

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=20)
        server.login(acc.email, acc.app_password)
        server.sendmail(acc.email, [to_email], msg.as_string())
        server.quit()
        return True, msg["Message-ID"]
    except Exception as e:
        return False, str(e)

def mark_imap_seen(acc, mid_str: str):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=15)
        mail.login(acc.email, acc.app_password)
        mail.select("INBOX", readonly=False)
        mail.store(mid_str.encode(), "+FLAGS", "\\Seen")
        mail.logout()
    except Exception as e:
        print(f"  [WARN] Failed to mark mid {mid_str} as seen on {acc.email}: {e}")

# ==============================================================================
# HTML TEMPLATE BUILDER
# ==============================================================================
def wrap_dbert_email(title: str, recipient_name: str, core_html: str, sender_name: str, sender_title: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body style="margin:0;padding:24px 12px;background-color:#0B1120;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F1F5F9;">
  <div style="max-width:600px;margin:0 auto;background-color:#111827;border:1px solid #1E293B;border-radius:12px;overflow:hidden;box-shadow:0 10px 25px rgba(0,0,0,0.5);">
    
    <!-- Top Bar -->
    <div style="background:linear-gradient(135deg, #0E1626 0%, #1E293B 100%);padding:22px 28px;border-bottom:1px solid #1E293B;">
      <div style="color:#E2B96F;font-size:11px;font-weight:800;letter-spacing:1px;text-transform:uppercase;">
        DIGITAL BLINC EDUCATION RESEARCH &amp; TECHNOLOGY &middot; DBERT
      </div>
      <h2 style="color:#FFFFFF;margin:6px 0 0 0;font-size:19px;font-weight:700;">
        {title}
      </h2>
    </div>

    <!-- Body -->
    <div style="padding:26px 28px;">
      <p style="color:#F1F5F9;font-size:15px;margin:0 0 16px 0;">
        Dear <strong>{recipient_name}</strong>,
      </p>

      {core_html}

      <div style="margin-top:28px;padding-top:18px;border-top:1px solid #1E293B;font-size:13px;color:#94A3B8;">
        Warm regards,<br/>
        <strong style="color:#F1F5F9;font-size:14px;">{sender_name}</strong><br/>
        <span style="color:#64748B;">{sender_title} &middot; DBERT Technical Council</span><br/>
        <span style="color:#64748B;">Official Web: <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a> | LMS: <a href="https://lms.dbert.in" style="color:#38BDF8;text-decoration:none;">lms.dbert.in</a></span>
      </div>
    </div>

    <!-- Footer -->
    <div style="background-color:#0B1120;padding:14px 24px;text-align:center;border-top:1px solid #1E293B;font-size:11px;color:#64748B;">
      &copy; 2026 DBERT &middot; Sovereign Industrial Training &amp; Venture Studio &middot; MSME Registered
    </div>
  </div>
</body>
</html>"""

def main():
    service = EmailDeliveryService()
    inbox_file = Path("data/active_unseen_inquiries.json")
    if not inbox_file.exists():
        print("No active inquiries file found.")
        return

    with open(inbox_file, "r", encoding="utf-8") as f:
        inquiries = json.load(f)

    print("=" * 76)
    print(f"  PROCESSING {len(inquiries)} INBOX INQUIRIES")
    print("=" * 76)

    dispatched = 0

    for inq in inquiries:
        sender_email = inq["sender_email"].lower()
        sender_name = inq["sender_name"]
        subject = inq["subject"]
        acc_email = inq["account"]
        acc = get_account_by_email(service, acc_email)
        mid = inq["mid"]
        orig_msg_id = inq["message_id"]

        print(f"\nEvaluating: {sender_name} <{sender_email}> (Mid: {mid}) on {acc.email}")

        # ----------------------------------------------------------------------
        # Case 1: Nishant Makwane (GitHub Milestone Submission)
        # ----------------------------------------------------------------------
        if "nishantmakwane04@gmail.com" in sender_email:
            reply_subj = "Re: DBERT Milestone Roadmap: Submission Assistance for ₹5,000 Stipend & Credentials"
            core_html = """
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Thank you for providing your GitHub repository link: 
              <a href="https://github.com/nishantmak04/Gayatri-AI-Bug-Fixes" style="color:#38BDF8;font-weight:600;">https://github.com/nishantmak04/Gayatri-AI-Bug-Fixes</a>.
            </p>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              We have officially logged your repository for the <strong>Data Analyst Milestone Roadmap</strong>. Here are the simple remaining steps to finalize your ₹5,000 stipend and verified credentials:
            </p>
            <div style="background-color:#0E1626;border:1px solid #1E293B;border-radius:8px;padding:16px;margin:18px 0;font-size:13px;line-height:1.7;color:#94A3B8;">
              <strong style="color:#F1F5F9;display:block;margin-bottom:8px;">📌 4-Step Stipend Release Checklist:</strong>
              1. <strong>Portal Submission:</strong> Please submit your GitHub repository link along with any live demo or summary report directly on your stipend dashboard: 
              <br/><a href="https://lms.dbert.in/stipend/tasks" style="color:#38BDF8;">https://lms.dbert.in/stipend/tasks</a><br/><br/>
              2. <strong>UPI Payout Account:</strong> Ensure your verified UPI ID is saved in your LMS profile at <a href="https://lms.dbert.in/profile" style="color:#38BDF8;">lms.dbert.in/profile</a> so our automated disbursement engine can transfer your funds.<br/><br/>
              3. <strong>Council Review:</strong> Our academic team and automated AI evaluation will review your commits against the domain rubric.<br/><br/>
              4. <strong>₹5,000 Wallet Credit:</strong> Once approved, 5,000 Coins (₹5,000) will be credited to your wallet for 1-click withdrawal.
            </div>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              If you have any questions or require real-time support, feel free to reply to this email or contact Admissions WhatsApp at <strong>+91 81929 11360</strong>.
            </p>
            """
            text_body = f"""Dear Nishant,

Thank you for providing your GitHub repository link (https://github.com/nishantmak04/Gayatri-AI-Bug-Fixes).

We have logged your repository for the Data Analyst Milestone Roadmap. To finalize your ₹5,000 performance stipend and verified credential release:

1. Submit your GitHub link and project report on your portal dashboard: https://lms.dbert.in/stipend/tasks
2. Save your payout UPI ID in your profile: https://lms.dbert.in/profile
3. Once reviewed by the Council, 5,000 Coins (₹5,000) will be credited to your wallet for instant withdrawal.

Feel free to reply if you need any assistance!

Warm regards,
Manoj Kumar
DBERT Academic Operations & Council
https://dbert.in | https://lms.dbert.in
"""
            html_body = wrap_dbert_email("Milestone Submission Received · Verification Next Steps", sender_name, core_html, acc.from_name, "Academic Operations")
            ok, res_id = send_threaded_email(acc, sender_email, reply_subj, html_body, text_body, orig_msg_id)
            print(f"  [DISPATCHED] Sent to {sender_email} (MsgID: {res_id}) -> Success: {ok}")
            mark_imap_seen(acc, mid)
            dispatched += 1

        # ----------------------------------------------------------------------
        # Case 2: Aryan Bhakuni (Milestone Review & Stipend Release)
        # ----------------------------------------------------------------------
        elif "aryanbhakuni2006@gmail.com" in sender_email:
            reply_subj = "Re: DBERT Milestone Roadmap: Your Path to ₹5,000 Stipend & Verified Credentials — Aryan [11 May 2026]"
            core_html = """
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Congratulations on completing your milestones! We have queued your project deliverables for formal review by the DBERT Technical Council.
            </p>
            <div style="background-color:#0E1626;border:1px solid #1E293B;border-radius:8px;padding:16px;margin:18px 0;font-size:13px;line-height:1.7;color:#94A3B8;">
              <strong style="color:#F1F5F9;display:block;margin-bottom:8px;">⚡ Payout Verification Steps:</strong>
              &bull; <strong>Dashboard Tracking:</strong> You can track your milestone evaluation status live at <a href="https://lms.dbert.in/stipend/tasks" style="color:#38BDF8;">https://lms.dbert.in/stipend/tasks</a>.<br/>
              &bull; <strong>Payout Setup:</strong> Please make sure your active UPI ID is configured in your profile at <a href="https://lms.dbert.in/profile" style="color:#38BDF8;">https://lms.dbert.in/profile</a>.<br/>
              &bull; <strong>Release Timeline:</strong> Academic Council audits are completed within 24–48 hours. Once approved, 5,000 Coins (₹5,000) will appear in your LMS wallet ready to withdraw.
            </div>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Thank you for your active participation and technical contributions to DBERT.
            </p>
            """
            text_body = f"""Dear Aryan,

Congratulations on completing your milestones! We have queued your deliverables for formal review by the Technical Council.

Next Steps:
1. Track your review status at: https://lms.dbert.in/stipend/tasks
2. Ensure your UPI ID is saved at: https://lms.dbert.in/profile
3. Once approved (within 24-48 hours), 5,000 Coins (₹5,000) will be released to your wallet for 1-click withdrawal.

Thank you for your great work!

Warm regards,
Manoj Kumar
DBERT Academic Operations
https://dbert.in | https://lms.dbert.in
"""
            html_body = wrap_dbert_email("Milestone Review In Progress · Stipend Release Update", sender_name, core_html, acc.from_name, "Academic Operations")
            ok, res_id = send_threaded_email(acc, sender_email, reply_subj, html_body, text_body, orig_msg_id)
            print(f"  [DISPATCHED] Sent to {sender_email} (MsgID: {res_id}) -> Success: {ok}")
            mark_imap_seen(acc, mid)
            dispatched += 1

        # ----------------------------------------------------------------------
        # Case 3: CH.Anjali Chidaraboyana (Application Withdrawal / Opt-out)
        # ----------------------------------------------------------------------
        elif "chanjalichidaraboyana@gmail.com" in sender_email:
            reply_subj = "Re: Application Profile Closure — DBERT Sprint Cohort [DBERT-APP-2026-N5008]"
            core_html = """
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Thank you for letting us know. As per your request, we have officially closed your application profile (<strong>DBERT-APP-2026-N5008</strong>) and removed your contact from our active batch notifications.
            </p>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              You will not receive any further automated reminders regarding this cohort. We wish you the very best in your academic studies and future career endeavors!
            </p>
            """
            text_body = f"""Dear Chidaraboyana,

Thank you for letting us know. As requested, we have closed your application profile (DBERT-APP-2026-N5008) and removed your contact from active batch notifications.

You will not receive any further automated reminders regarding this cohort. We wish you all the best in your studies and future endeavors!

Warm regards,
Manoj Kumar
DBERT Admissions Desk
https://dbert.in
"""
            html_body = wrap_dbert_email("Application Closure Confirmation", sender_name, core_html, acc.from_name, "Admissions Directorate")
            ok, res_id = send_threaded_email(acc, sender_email, reply_subj, html_body, text_body, orig_msg_id)
            print(f"  [DISPATCHED] Sent to {sender_email} (MsgID: {res_id}) -> Success: {ok}")
            mark_imap_seen(acc, mid)
            dispatched += 1

        # ----------------------------------------------------------------------
        # Case 4: Trisham Gupta (Seat Confirmation & Payment In Progress)
        # ----------------------------------------------------------------------
        elif "trishamgupta43@gmail.com" in sender_email:
            reply_subj = "Re: [URGENT] Action Required: Batch Kickoff in 5 Hours — Review Offer Letter & Confirm Seat"
            core_html = """
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Thank you for confirming! We are thrilled to welcome you to the DBERT Engineering Fellowship.
            </p>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Here are the quick links to finalize your ₹499 caution deposit reconciliation before today's live orientation kickoff:
            </p>
            <div style="background-color:#0E1626;border:1px solid #1E293B;border-radius:8px;padding:16px;margin:18px 0;font-size:13.5px;line-height:1.8;color:#94A3B8;">
              &bull; <strong>Official Seat & Payment Form:</strong><br/>
              <a href="https://docs.google.com/forms/d/e/1FAIpQLSdFxi9bft4POk4b3eXmp4aH71LmeQrJ0WzXA1bsIm37MalSIw/viewform?usp=header" style="color:#38BDF8;font-weight:bold;">https://docs.google.com/forms/d/e/1FAIpQLSdFxi9bft4POk4b3eXmp4aH71LmeQrJ0WzXA1bsIm37MalSIw/viewform?usp=header</a><br/><br/>
              &bull; <strong>Direct Merchant UPI VPA:</strong> <code style="color:#E2B96F;font-size:14px;font-weight:bold;">Q652429146@ybl</code> (DBERT Admissions)<br/>
              &bull; <strong>Portal Offer Letter:</strong> <a href="https://lms.dbert.in/portal/offer" style="color:#38BDF8;">https://lms.dbert.in/portal/offer</a>
            </div>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Once completed, simply reply here or share your 12-digit UPI UTR on WhatsApp at <strong>+91 81929 11360</strong> for instant seat confirmation and orientation credentials.
            </p>
            """
            text_body = f"""Dear Trisham,

Thank you for confirming! We are excited to welcome you to the DBERT Engineering Fellowship.

To finalize your seat confirmation and ₹499 caution deposit reconciliation before the live orientation:

1. Official Form: https://docs.google.com/forms/d/e/1FAIpQLSdFxi9bft4POk4b3eXmp4aH71LmeQrJ0WzXA1bsIm37MalSIw/viewform?usp=header
2. Merchant UPI VPA: Q652429146@ybl (DBERT Admissions)
3. Portal Offer: https://lms.dbert.in/portal/offer

Reply here or message Admissions WhatsApp (+91 81929 11360) with your UTR for instant seat activation.

Warm regards,
Manoj Kumar
DBERT Admissions Desk
https://dbert.in | https://lms.dbert.in
"""
            html_body = wrap_dbert_email("Seat Confirmation Acknowledgment & Kickoff Access", sender_name, core_html, acc.from_name, "Admissions Directorate")
            ok, res_id = send_threaded_email(acc, sender_email, reply_subj, html_body, text_body, orig_msg_id)
            print(f"  [DISPATCHED] Sent to {sender_email} (MsgID: {res_id}) -> Success: {ok}")
            mark_imap_seen(acc, mid)
            dispatched += 1

        # ----------------------------------------------------------------------
        # Case 5: Gurka Vinay Kumar Reddy (Stipend Payout Verification)
        # ----------------------------------------------------------------------
        elif "gurkavinay22@gmail.com" in sender_email:
            reply_subj = "Re: Missing ₹5,000 Stipend Disbursement – Credential ID: CERT-DBERT-2026-AIML-169"
            core_html = """
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Thank you for contacting the DBERT Central Support Desk regarding your ₹5,000 production milestone stipend for the AI Agent Development Fellowship.
            </p>
            <div style="background-color:#0E1626;border:1px solid #1E293B;border-radius:8px;padding:16px;margin:18px 0;font-size:13px;line-height:1.7;color:#94A3B8;">
              <strong style="color:#F1F5F9;display:block;margin-bottom:8px;">📌 Reconciled Record Details:</strong>
              &bull; <strong>Candidate:</strong> Gurka Vinay Kumar Reddy<br/>
              &bull; <strong>Domain:</strong> AI Agent Development Fellow<br/>
              &bull; <strong>Credential ID:</strong> <code style="color:#E2B96F;">CERT-DBERT-2026-AIML-169</code><br/>
              &bull; <strong>Evaluation Score:</strong> 80/100<br/>
              &bull; <strong>Registered UPI ID:</strong> <code style="color:#38BDF8;">9014147134@upi</code>
            </div>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              We have escalated your payout record directly to the Finance &amp; Disbursement Desk to pull the banking UTR (Unique Transaction Reference) from our institutional clearing partner.
            </p>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              Our finance team will verify the payment gateway settlement log and transmit the bank UTR to your email within <strong>12–24 business hours</strong> so you can confirm receipt directly with your bank branch.
            </p>
            <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
              For immediate tracking or expedited WhatsApp coordination, you can also reach out to our dedicated Admissions Concierge at <strong>+91 81929 11360</strong>.
            </p>
            """
            text_body = f"""Dear Gurka Vinay Kumar Reddy,

Thank you for contacting the DBERT Support Desk regarding your ₹5,000 production milestone stipend (Credential ID: CERT-DBERT-2026-AIML-169).

We have escalated your payout inquiry directly to the Finance & Disbursement Desk to verify the bank transaction settlement log for your registered UPI ID (9014147134@upi).

Our team will share the exact banking UTR (Unique Transaction Reference) with you within 12–24 hours so you can confirm with your bank.

For live assistance, you can also connect directly with Admissions WhatsApp at +91 81929 11360.

Warm regards,
DBERT Admissions & Finance Directorate
https://dbert.in | https://lms.dbert.in
"""
            html_body = wrap_dbert_email("Stipend Payout Status Investigation · Escalation Ticket", sender_name, core_html, "DBERT Support & Admissions Desk", "Finance Directorate")
            ok, res_id = send_threaded_email(acc, sender_email, reply_subj, html_body, text_body, orig_msg_id)
            print(f"  [DISPATCHED] Sent to {sender_email} (MsgID: {res_id}) -> Success: {ok}")
            mark_imap_seen(acc, mid)
            dispatched += 1

        # ----------------------------------------------------------------------
        # Case 6 & 7: Abusive / Profanity Senders (Suppress & Mark Seen)
        # ----------------------------------------------------------------------
        elif any(bad in sender_email for bad in ["ajmalashrafi2016@gmail.com", "htootayza14@gmail.com"]):
            print(f"  [SUPPRESSED] Abusive message from {sender_email}. Marking seen and closing ticket.")
            mark_imap_seen(acc, mid)

        else:
            print(f"  [SKIPPED] Unhandled or general sender: {sender_email}")
            mark_imap_seen(acc, mid)

    print("\n" + "=" * 76)
    print(f"  INBOX RESPONSE MISSION COMPLETE: {dispatched} REPLIES DELIVERED")
    print("=" * 76)

if __name__ == "__main__":
    main()
