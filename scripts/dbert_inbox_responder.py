#!/usr/bin/env python3
"""
scripts/dbert_inbox_responder.py
Real-Time Autonomous Email Responder Daemon for DBERT Google Workspace Inboxes.

Scans all 5 pooled Google Workspace inboxes (abhinav.sharma, manoj.kumar, sandeep.bannu,
contactus, pulkit.kunar) via IMAP SSL, strips quoted threads, matches inquiry intent,
resolves candidate dossier, and dispatches verified institutional replies.
"""

import os
import sys
import time
import json
import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr, formataddr
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

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
RESPONDER_LOG_FILE = DATA_DIR / "inbox_responder.log"

SUPPRESSED_SENDERS = [
    "mailer-daemon", "postmaster", "no-reply", "noreply",
    "google.com", "accounts.google.com", "googlemail.com",
    "dbert.in", "ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"
]

def log_msg(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = f"[{ts}] {msg}"
    print(out, flush=True)
    with open(RESPONDER_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(out + "\n")

def load_replies_log() -> dict:
    if REPLIES_LOG_FILE.exists():
        try:
            with open(REPLIES_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_reply_log(msg_id: str, entry: dict):
    data = load_replies_log()
    data[msg_id] = entry
    with open(REPLIES_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def decode_mime_header(header_val: str) -> str:
    if not header_val:
        return ""
    decoded_parts = decode_header(header_val)
    res = []
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            res.append(part.decode(enc or "utf-8", errors="ignore"))
        else:
            res.append(str(part))
    return "".join(res)

def extract_body(msg) -> str:
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdisp = str(part.get("Content-Disposition", ""))
            if ctype == "text/plain" and "attachment" not in cdisp:
                payload = part.get_payload(decode=True)
                if payload:
                    body += payload.decode("utf-8", errors="ignore") + "\n"
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            body = payload.decode("utf-8", errors="ignore")
    return body

def strip_quoted_reply(body: str) -> str:
    """Strip RFC 2822 quoted replies, signatures, and previous email threads."""
    lines = body.splitlines()
    clean = []
    for line in lines:
        l_str = line.strip()
        # Common email quote markers
        if l_str.startswith(">"):
            continue
        if l_str.startswith("On ") and ("wrote:" in l_str or "wrote :" in l_str):
            break
        if "---------- Forwarded message ---------" in l_str:
            break
        if "________________________________" in l_str:
            break
        clean.append(line)
    return "\n".join(clean).strip()

def find_candidate_record(email_addr: str) -> dict:
    """Search known candidate databases by email address."""
    clean_em = email_addr.strip().lower()
    
    # 1. Sheet 1593 provisional registry
    sheet_path = DATA_DIR / "sheet_1593_provisional_registry.json"
    if sheet_path.exists():
        try:
            with open(sheet_path, "r", encoding="utf-8") as f:
                for cand in json.load(f):
                    if cand.get("email", "").strip().lower() == clean_em:
                        return cand
        except Exception:
            pass

    # 2. 409 Provisional Registry
    p409_path = DATA_DIR / "all_409_provisional_registry.json"
    if p409_path.exists():
        try:
            with open(p409_path, "r", encoding="utf-8") as f:
                for cand in json.load(f):
                    if cand.get("email", "").strip().lower() == clean_em:
                        return cand
        except Exception:
            pass

    # 3. Master directory
    dir_path = ROOT_DIR / "apps" / "website" / "src" / "data" / "directory_candidates.json"
    if dir_path.exists():
        try:
            with open(dir_path, "r", encoding="utf-8") as f:
                for cand in json.load(f):
                    if cand.get("email", "").strip().lower() == clean_em:
                        return cand
        except Exception:
            pass

    return {}

def classify_intent(subject: str, body: str) -> str:
    text = (subject + " " + body).lower()
    
    # Priority 1: Payment, Fees, QR, ₹299
    if any(k in text for k in ["299", "payment", "pay", "fee", "upi", "qr", "qr code", "cost", "charge", "refund", "how much", "amount", "paid"]):
        return "PAYMENT_AND_FEE_299"

    # Priority 2: Certificate download / LOR / Rubric claim
    if any(k in text for k in ["certificate", "cert", "download", "lor", "letter of recommendation", "rubric", "evaluation", "score", "pdf", "claim", "how to get"]):
        return "CERTIFICATE_AND_LOR_CLAIM"

    # Priority 3: Stipend / Coins / Payout
    if any(k in text for k in ["stipend", "coin", "coins", "5000", "payout", "task", "contribution", "money"]):
        return "STIPEND_AND_COINS"

    # Priority 4: College NOC / Internship Duration
    if any(k in text for k in ["noc", "college", "university", "duration", "tenure", "dates", "verification letter"]):
        return "COLLEGE_AND_TENURE_VERIFICATION"

    return "GENERAL_INQUIRY"

def build_automated_reply(
    intent: str,
    sender_name: str,
    sender_email: str,
    cand_record: dict,
    account_from_name: str,
    account_email: str
) -> tuple:
    first_name = cand_record.get("holderName") or sender_name or "Fellow Engineer"
    cert_id = cand_record.get("certId") or "CERT-DBERT-2026-PROV"
    domain = cand_record.get("domain") or "Technical Internship Track"
    unlock_url = f"https://dbert.in/verify/unlock?certid={cert_id}&email={sender_email}"
    verify_url = f"https://dbert.in/verify/{cert_id}"

    if intent == "PAYMENT_AND_FEE_299":
        subj = f"Re: Official Project Verification & Credential Unlock (Ref: {cert_id})"
        core_headline = "Project Verification & Credential Unlock Information"
        core_msg = f"""
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          Thank you for reaching out regarding your project verification.
        </p>
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          As part of the DBERT National Credential Standard, provisional credentials undergo formal academic evaluation. The <strong>₹299 Project Verification Fee</strong> covers:
        </p>
        <ul style="color:#94A3B8;font-size:13.5px;line-height:1.8;margin:0 0 18px 20px;padding:0;">
          <li><strong style="color:#F1F5F9;">Official 3-Document Credential Packet:</strong> Verifiable Certificate of Completion, US Letter Academic Project Evaluation (100-mark rubric), and Institutional LOR signed by Program Head Mr. Abhinav Sharma.</li>
          <li><strong style="color:#F1F5F9;">Turnitin Originality Rubric:</strong> Institutional plagiarism scan report and 9-dimension competency table.</li>
          <li><strong style="color:#F1F5F9;">Pre-Vetted Engineers Directory Listing:</strong> Published profile on <a href="https://dbert.in/verify/directory" style="color:#38BDF8;">dbert.in/verify/directory</a> for recruiter shortlisting.</li>
          <li><strong style="color:#F1F5F9;">Performance Stipend Unlock:</strong> Immediate eligibility to apply for 5,000 Coin (₹5,000) disbursement on <a href="https://lms.dbert.in/stipend/tasks" style="color:#38BDF8;">lms.dbert.in/stipend/tasks</a>.</li>
        </ul>
        <div style="background-color:#1E293B;border-left:4px solid #10B981;padding:14px 18px;border-radius:4px;margin-bottom:20px;">
          <p style="color:#F1F5F9;margin:0;font-size:14px;font-weight:600;">
            1-Click Verification Portal:
          </p>
          <p style="margin:6px 0 0 0;font-size:13px;">
            <a href="{unlock_url}" style="color:#38BDF8;word-break:break-all;">{unlock_url}</a>
          </p>
        </div>
        """
    elif intent == "CERTIFICATE_AND_LOR_CLAIM":
        subj = f"Re: How to Access Your Official Credentials & LOR (Ref: {cert_id})"
        core_headline = "Accessing Your Official 3-Document Credential Packet"
        core_msg = f"""
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          Your provisional certificate for <strong>{domain}</strong> is safely registered under Reference ID <strong>{cert_id}</strong>.
        </p>
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          To complete your project evaluation and unlock full high-resolution PDF downloads (Certificate, Academic Evaluation, and Letter of Recommendation), visit your personal verification dossier:
        </p>
        <div style="text-align:center;margin:22px 0;">
          <a href="{unlock_url}" style="background:linear-gradient(135deg,#10B981 0%,#059669 100%);color:#FFFFFF;text-decoration:none;font-weight:bold;font-size:14px;padding:12px 28px;border-radius:8px;display:inline-block;">
            Open Your Credential Dossier &rarr;
          </a>
        </div>
        """
    elif intent == "STIPEND_AND_COINS":
        subj = f"Re: Performance Stipend & 5,000 Coin Release Guidelines (Ref: {cert_id})"
        core_headline = "Performance Stipend (5,000 Coins / ₹5,000) Release"
        core_msg = f"""
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          DBERT Performance Stipends are released against technical code contributions reviewed under our audited rubrics.
        </p>
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          <strong>Steps to claim your stipend:</strong>
        </p>
        <ol style="color:#94A3B8;font-size:13.5px;line-height:1.8;margin:0 0 18px 20px;padding:0;">
          <li>Verify your credential dossier at <a href="{unlock_url}" style="color:#38BDF8;">dbert.in/verify/unlock</a>.</li>
          <li>Log in to your student dashboard at <a href="https://lms.dbert.in/stipend/tasks" style="color:#38BDF8;">lms.dbert.in/stipend/tasks</a>.</li>
          <li>Submit your domain capstone deliverables (GitHub repository, live demo, technical report).</li>
          <li>Upon mentor approval, <strong>5,000 Coins (₹5,000)</strong> are credited to your LMS wallet and disbursed via UPI.</li>
        </ol>
        """
    else:
        subj = f"Re: DBERT Credential & Admissions Directorate (Ref: {cert_id})"
        core_headline = "DBERT Support & Academic Directorate"
        core_msg = f"""
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          Thank you for contacting the DBERT Academic Directorate. We have logged your inquiry regarding your candidate record (<strong>{cert_id}</strong> &middot; <strong>{domain}</strong>).
        </p>
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          You can inspect your live candidate verification status and access your dossier anytime at:
        </p>
        <p style="margin:0 0 16px 0;font-size:13.5px;">
          <a href="{unlock_url}" style="color:#38BDF8;font-weight:600;">{unlock_url}</a>
        </p>
        <p style="color:#CBD5E1;font-size:14px;line-height:1.7;margin:0 0 16px 0;">
          For priority live WhatsApp assistance regarding fees, deadlines, or project submissions, reach out directly to our Admissions Concierge:
        </p>
        <p style="margin:0 0 16px 0;font-size:13.5px;">
          &bull; WhatsApp Support: <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20regarding%20{cert_id}" style="color:#10B981;font-weight:bold;">+91 81929 11360</a> &nbsp;|&nbsp;
          <a href="https://wa.me/918958006294?text=Hi%20Admissions%20Team%2C%20regarding%20{cert_id}" style="color:#10B981;font-weight:bold;">+91 89580 06294</a>
        </p>
        """

    html = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,Helvetica,sans-serif;background-color:#0B1120;color:#F1F5F9;padding:24px 12px;margin:0;">
  <div style="max-width:600px;margin:0 auto;background-color:#111827;border:1px solid #1F2937;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
    <!-- Top Header -->
    <div style="background:linear-gradient(135deg,#0E1626 0%,#182337 100%);padding:24px 28px;border-bottom:1px solid #1F2937;">
      <div style="color:#E2B96F;font-size:11px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;">
        DIGITAL BLINC EDUCATION RESEARCH &amp; TECHNOLOGY &middot; DBERT
      </div>
      <h2 style="color:#FFFFFF;margin:8px 0 0 0;font-size:20px;font-weight:700;">
        {core_headline}
      </h2>
    </div>

    <!-- Content -->
    <div style="padding:28px;">
      <p style="color:#F1F5F9;font-size:15px;margin:0 0 16px 0;">
        Dear <strong>{first_name}</strong>,
      </p>

      {core_msg}

      <!-- Candidate Snapshot -->
      <div style="background-color:#0E1626;border:1px solid #1F2937;border-radius:8px;padding:14px 18px;margin:22px 0;font-size:12.5px;">
        <table style="width:100%;border-collapse:collapse;color:#94A3B8;">
          <tr>
            <td style="padding:4px 0;">Candidate:</td>
            <td style="padding:4px 0;color:#F1F5F9;font-weight:600;text-align:right;">{first_name}</td>
          </tr>
          <tr>
            <td style="padding:4px 0;">Track:</td>
            <td style="padding:4px 0;color:#F1F5F9;text-align:right;">{domain}</td>
          </tr>
          <tr>
            <td style="padding:4px 0;">Credential ID:</td>
            <td style="padding:4px 0;color:#E2B96F;font-family:monospace;font-weight:bold;text-align:right;">{cert_id}</td>
          </tr>
        </table>
      </div>

      <p style="color:#94A3B8;font-size:13px;line-height:1.6;margin:20px 0 0 0;">
        Warm regards,<br/>
        <strong style="color:#F1F5F9;">{account_from_name}</strong><br/>
        <span style="color:#64748B;font-size:12px;">Credential &amp; Admissions Directorate &middot; DBERT</span>
      </p>
    </div>

    <!-- Official Disclaimers Footer -->
    <div style="background-color:#0B1120;padding:16px 24px;text-align:center;border-top:1px solid #1E2633;font-size:11px;color:#64748B;line-height:1.6;">
      <p style="margin:0 0 6px 0;">
        Official Sovereign Platform: <a href="https://dbert.in" style="color:#E2B96F;text-decoration:none;">dbert.in</a> &nbsp;|&nbsp; Verification: <a href="https://dbert.in/verify" style="color:#8A9AB5;text-decoration:none;">dbert.in/verify</a>
      </p>
      <p style="margin:0;">
        &copy; 2026 DBERT &middot; Sovereign Industrial Training &amp; Venture Studio &middot; MSME Registered
      </p>
    </div>
  </div>
</body>
</html>"""

    txt = f"""Dear {first_name},

{subj}

Candidate: {first_name}
Track: {domain}
Credential ID: {cert_id}

Personalized Credential Unlock Dossier:
{unlock_url}

For priority live WhatsApp assistance:
Admissions Concierge: +91 81929 11360 / +91 89580 06294

Warm regards,
{account_from_name}
Credential & Admissions Directorate · DBERT
https://dbert.in
"""

    return subj, txt, html

def process_inbox_account(service: EmailDeliveryService, acc) -> int:
    """Scan a single account's inbox and reply to new candidate inquiries."""
    replies_sent = 0
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=20)
        mail.login(acc.email, acc.app_password)
        mail.select("INBOX", readonly=False)

        # Search for UNSEEN messages
        status, search_res = mail.search(None, "UNSEEN")
        if status != "OK" or not search_res or not search_res[0]:
            mail.logout()
            return 0

        msg_ids = search_res[0].split()
        if not msg_ids:
            mail.logout()
            return 0

        log_msg(f"[{acc.email}] Found {len(msg_ids)} unread messages.")
        replies_log = load_replies_log()

        for mid in msg_ids:
            try:
                res, data = mail.fetch(mid, "(RFC822)")
                if res != "OK" or not data or not data[0]:
                    continue

                raw_email = data[0][1]
                msg = email.message_from_bytes(raw_email)

                message_id = msg.get("Message-ID", "").strip()
                from_header = decode_mime_header(msg.get("From", ""))
                sender_name, sender_email = parseaddr(from_header)
                sender_email = sender_email.strip().lower()
                subject = decode_mime_header(msg.get("Subject", ""))
                body = extract_body(msg)
                clean_body = strip_quoted_reply(body)

                # Suppression filter
                if any(sup in sender_email for sup in SUPPRESSED_SENDERS):
                    log_msg(f"[{acc.email}] Suppressed sender: {sender_email}")
                    mail.store(mid, "+FLAGS", "\\Seen")
                    continue

                # Deduplication check
                dedup_key = message_id or f"{sender_email}_{subject}"
                if dedup_key in replies_log:
                    log_msg(f"[{acc.email}] Already replied to {sender_email} (MsgID: {message_id})")
                    mail.store(mid, "+FLAGS", "\\Seen")
                    continue

                log_msg(f"[{acc.email}] Processing inquiry from: {sender_name} <{sender_email}> | Subj: {subject}")

                # Classify intent & candidate
                intent = classify_intent(subject, clean_body)
                cand_record = find_candidate_record(sender_email)
                log_msg(f"[{acc.email}] Matched Intent: {intent} | Candidate Record Found: {bool(cand_record)}")

                # Build reply
                reply_subj, reply_txt, reply_html = build_automated_reply(
                    intent=intent,
                    sender_name=sender_name,
                    sender_email=sender_email,
                    cand_record=cand_record,
                    account_from_name=acc.from_name,
                    account_email=acc.email
                )

                # Send reply via matching account
                res_delivery = service.send_email(
                    to=sender_email,
                    subject=reply_subj,
                    html_content=reply_html,
                    text_content=reply_txt,
                    tags={"type": "inbox_auto_reply", "intent": intent, "orig_msg_id": message_id},
                    dry_run=False
                )

                if res_delivery.success:
                    log_msg(f"[{acc.email}] ✓ Replied to {sender_email} (MsgID: {res_delivery.message_id}) [Intent: {intent}]")
                    save_reply_log(dedup_key, {
                        "replied_at": datetime.now().isoformat(),
                        "sender_email": sender_email,
                        "sender_name": sender_name,
                        "subject": subject,
                        "intent": intent,
                        "reply_account": acc.email,
                        "reply_msg_id": res_delivery.message_id
                    })
                    mail.store(mid, "+FLAGS", "\\Seen")
                    replies_sent += 1
                else:
                    log_msg(f"[{acc.email}] ✗ Delivery failed to {sender_email}: {res_delivery.error}")

            except Exception as e:
                log_msg(f"[{acc.email}] Error processing mid {mid}: {e}")

        mail.logout()
    except Exception as e:
        log_msg(f"[{acc.email}] IMAP check error: {e}")

    return replies_sent

def run_inbox_sweep() -> int:
    """Scan all 5 accounts once."""
    service = EmailDeliveryService()
    total_replies = 0
    for acc in service.pool.accounts:
        total_replies += process_inbox_account(service, acc)
    return total_replies

def run_daemon(poll_interval: int = 60):
    log_msg("=" * 70)
    log_msg(f"Starting DBERT Inbox Responder Daemon (Polling every {poll_interval}s across 5 inboxes)...")
    log_msg("=" * 70)
    service = EmailDeliveryService()

    while True:
        try:
            for acc in service.pool.accounts:
                process_inbox_account(service, acc)
        except Exception as e:
            log_msg(f"[DAEMON] Top-level error: {e}")
        time.sleep(poll_interval)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DBERT Autonomous Inbox Responder Daemon")
    parser.add_argument("--daemon", action="store_true", help="Run continuous background polling loop")
    parser.add_argument("--interval", type=int, default=60, help="Poll interval in seconds (default: 60)")
    parser.add_argument("--once", action="store_true", help="Execute single inbox sweep and exit")
    args = parser.parse_args()

    if args.daemon:
        run_daemon(args.interval)
    else:
        log_msg("Executing single inbox sweep...")
        sent = run_inbox_sweep()
        log_msg(f"Sweep complete. Total replies sent: {sent}")
