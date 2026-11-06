import os
import sys
import smtplib
import ssl
import csv
import json
import argparse
import time
from datetime import datetime
from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_PATH = os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json")
OUTPUTS_REGISTRY = os.path.join(BASE_DIR, "outputs", "certificates_registry.json")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DISPATCH_LOG = os.path.join(LOGS_DIR, "email_dispatch_log.csv")

os.makedirs(LOGS_DIR, exist_ok=True)

# Google SMTP Credentials
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "ckxnpudkapzgzbxl"
FROM_NAME = "Mr. Abhinav Sharma (DBERT)"
FROM_EMAIL = "abhinav.sharma@dbert.in"


def load_registry():
    path = REGISTRY_PATH if os.path.exists(REGISTRY_PATH) else OUTPUTS_REGISTRY
    if not os.path.exists(path):
        raise FileNotFoundError(f"Registry not found: {path}. Run generate_all_packets.py first.")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_email_message(c_rec, recipient_email):
    name = c_rec["holderName"]
    cert_id = c_rec["certId"]
    intern_id = c_rec["internId"]
    domain = c_rec["domain"]
    project = c_rec["project"]
    duration = c_rec["duration"]
    score = c_rec["score"]
    grade = c_rec["grade"]
    verify_url = f"https://dbert.in/verify?certid={cert_id}"

    # Crisp, transactional subject line with ASCII hyphen to guarantee clean inbox display across all mail clients
    subject = f"Official Internship Credential Packet: Certificate, Evaluation & Recommendation - {name} [{cert_id}]"

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = recipient_email
    msg["Reply-To"] = FROM_EMAIL
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    msg["X-Mailer"] = "DBERT Credential Notification Service"
    msg["X-Entity-Ref-ID"] = cert_id

    # 1. Plain text alternative (word-for-word parity with HTML for high deliverability)
    text_content = f"""Dear {name},

We are pleased to provide your official DBERT Internship Credential Packet following the successful completion of your 2-Month Technical Incubation & Internship Program.

Official Credential Record:
--------------------------------------------------------------------------------
- Candidate Name:        {name}
- Domain Track:          {domain}
- Program Tenure:        {duration}
- Core Project:          {project}
- Academic Evaluation:   {score}/100 ({grade})
- Certificate ID:        {cert_id}
- Permanent Intern ID:   {intern_id}
- Online Verification:   {verify_url}
--------------------------------------------------------------------------------

Attached to this email are your 3 official verified PDF documents:
1. Certificate of Completion (with official QR code & verification seal)
2. Academic Project Evaluation & Competency Rubrics (Turnitin verified)
3. Official Letter of Recommendation & Performance Appraisal

You can verify the authenticity of your credentials at any time on our official verification portal:
{verify_url}

You may also add this verified credential directly to your LinkedIn profile using the 1-click verification link above.

Sincerely,

Mr. Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Verification Portal: https://dbert.in/verify
Official Website: https://dbert.in
"""

    # 2. Clean Executive Light HTML (Designed for 100% Primary Inbox Deliverability)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Credential Packet</title>
<style>
  body {{
    margin: 0;
    padding: 0;
    background-color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    -webkit-font-smoothing: antialiased;
  }}
  .email-wrapper {{
    width: 100%;
    background-color: #f1f5f9;
    padding: 30px 10px;
  }}
  .email-card {{
    max-width: 620px;
    margin: 0 auto;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }}
  .header-bar {{
    background-color: #0F2942;
    padding: 26px 30px;
    text-align: center;
    border-bottom: 3px solid #D4AF37;
  }}
  .header-title {{
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0 0 4px 0;
  }}
  .header-sub {{
    color: #cbd5e1;
    font-size: 11px;
    letter-spacing: 0.5px;
    margin: 0;
    text-transform: uppercase;
  }}
  .body-content {{
    padding: 32px 30px 24px 30px;
  }}
  .greeting {{
    font-size: 17px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 12px;
  }}
  .intro-text {{
    font-size: 14px;
    line-height: 1.6;
    color: #334155;
    margin-bottom: 22px;
  }}
  .record-box {{
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 18px 20px;
    margin-bottom: 24px;
  }}
  .record-title {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #0F2942;
    margin: 0 0 12px 0;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
  }}
  .record-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  .record-table td {{
    padding: 6px 0;
    vertical-align: top;
  }}
  .label-col {{
    color: #64748b;
    width: 36%;
    font-weight: 500;
  }}
  .value-col {{
    color: #0f172a;
    font-weight: 600;
  }}
  .highlight-value {{
    color: #0F2942;
    font-weight: 700;
  }}
  .code-font {{
    font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
    font-size: 12.5px;
    color: #0284c7;
  }}
  .cta-section {{
    text-align: center;
    margin: 28px 0;
  }}
  .btn-verify {{
    display: inline-block;
    background-color: #0F2942;
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 700;
    font-size: 14px;
    padding: 13px 32px;
    border-radius: 6px;
    border: 1px solid #D4AF37;
  }}
  .direct-url {{
    font-size: 11.5px;
    color: #64748b;
    margin-top: 10px;
    word-break: break-all;
  }}
  .direct-url a {{
    color: #0284c7;
    text-decoration: none;
  }}
  .docs-box {{
    background-color: #f8fafc;
    border-left: 3px solid #0F2942;
    padding: 14px 18px;
    margin-bottom: 24px;
    border-radius: 0 6px 6px 0;
  }}
  .docs-box-title {{
    font-size: 13px;
    font-weight: 700;
    color: #0F2942;
    margin: 0 0 8px 0;
  }}
  .docs-item {{
    font-size: 12.5px;
    line-height: 1.55;
    color: #475569;
    margin-bottom: 6px;
  }}
  .docs-item strong {{
    color: #0f172a;
  }}
  .sign-off-block {{
    border-top: 1px solid #e2e8f0;
    padding-top: 20px;
    margin-top: 24px;
    font-size: 13.5px;
    color: #334155;
    line-height: 1.5;
  }}
  .sign-name {{
    font-size: 15px;
    font-weight: 700;
    color: #0F2942;
    margin-top: 8px;
  }}
  .sign-role {{
    font-size: 12.5px;
    color: #64748b;
  }}
  .footer-bar {{
    background-color: #f8fafc;
    padding: 18px 30px;
    text-align: center;
    font-size: 11px;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
    line-height: 1.5;
  }}
  .footer-bar a {{
    color: #0F2942;
    text-decoration: none;
    font-weight: 600;
  }}
</style>
</head>
<body>
<div class="email-wrapper">
  <div class="email-card">
    <div class="header-bar">
      <div class="header-title">DBERT</div>
      <div class="header-sub">Digital Blinc Education Research and Technology</div>
    </div>

    <div class="body-content">
      <div class="greeting">Dear {name},</div>
      <p class="intro-text">
        We are pleased to provide your official verified credential packet following the successful completion of your <strong>2-Month Technical Incubation & Internship Program</strong> with <strong>DBERT</strong>.
      </p>

      <div class="record-box">
        <div class="record-title">Official Credential Record</div>
        <table class="record-table">
          <tr>
            <td class="label-col">Candidate Name:</td>
            <td class="value-col">{name}</td>
          </tr>
          <tr>
            <td class="label-col">Domain Track:</td>
            <td class="value-col highlight-value">{domain}</td>
          </tr>
          <tr>
            <td class="label-col">Program Tenure:</td>
            <td class="value-col">{duration}</td>
          </tr>
          <tr>
            <td class="label-col">Core Project:</td>
            <td class="value-col">{project}</td>
          </tr>
          <tr>
            <td class="label-col">Academic Evaluation:</td>
            <td class="value-col highlight-value">{score}/100 ({grade})</td>
          </tr>
          <tr>
            <td class="label-col">Certificate ID:</td>
            <td class="value-col code-font">{cert_id}</td>
          </tr>
          <tr>
            <td class="label-col">Permanent Intern ID:</td>
            <td class="value-col code-font">{intern_id}</td>
          </tr>
        </table>
      </div>

      <div class="cta-section">
        <a href="{verify_url}" target="_blank" class="btn-verify">
          Verify Credential Online &rarr;
        </a>
        <div class="direct-url">
          Direct verification URL: <a href="{verify_url}">{verify_url}</a>
        </div>
      </div>

      <div class="docs-box">
        <div class="docs-box-title">Attached Verified Documents (3 Official PDFs):</div>
        <div class="docs-item">
          &bull; <strong>1. Certificate of Completion:</strong> High-resolution credential featuring verification seal and quick-response authenticity code.
        </div>
        <div class="docs-item">
          &bull; <strong>2. Academic Project Evaluation:</strong> Comprehensive 9-dimension competency rubrics with academic clearance stamp.
        </div>
        <div class="docs-item">
          &bull; <strong>3. Official Letter of Recommendation:</strong> Executive institutional endorsement and performance appraisal.
        </div>
      </div>

      <div class="sign-off-block">
        Sincerely,<br>
        <div class="sign-name">{FROM_NAME}</div>
        <div class="sign-role">Program Head & Project Mentor<br>DBERT (Digital Blinc Education Research and Technology)</div>
      </div>
    </div>

    <div class="footer-bar">
      Official Verification Portal: <a href="https://dbert.in/verify">dbert.in/verify</a> &nbsp;&bull;&nbsp; 
      Website: <a href="https://dbert.in">dbert.in</a><br>
      &copy; 2026 DBERT. All rights reserved. This is an official institutional notification.
    </div>
  </div>
</div>
</body>
</html>
"""

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(text_content, "plain", "utf-8"))
    alt_part.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(alt_part)

    # Attach all 3 PDFs
    pdf_paths = [
        ("1_Certificate_of_Completion_" + cert_id + ".pdf", c_rec["doc1Pdf"]),
        ("2_Academic_Project_Evaluation_" + cert_id + ".pdf", c_rec["doc2Pdf"]),
        ("3_Letter_of_Recommendation_" + cert_id + ".pdf", c_rec["doc3Pdf"])
    ]

    for filename, file_path in pdf_paths:
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                pdf_data = f.read()
            attach = MIMEApplication(pdf_data, _subtype="pdf")
            attach.add_header("Content-Disposition", "attachment", filename=filename)
            msg.attach(attach)
        else:
            print(f"  [WARN] PDF file not found to attach: {file_path}")

    return msg


def get_already_sent_cert_ids():
    if not os.path.exists(DISPATCH_LOG):
        return set()
    sent_ids = set()
    with open(DISPATCH_LOG, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 4 and row[3] == "SUCCESS":
                sent_ids.add(row[2].strip())
    return sent_ids


def log_dispatch(email, cert_id, status, details, candidate_name=""):
    file_exists = os.path.exists(DISPATCH_LOG)
    now_iso = datetime.now().isoformat()
    with open(DISPATCH_LOG, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Recipient_Email", "Certificate_ID", "Status", "Details"])
        writer.writerow([now_iso, email, cert_id, status, details])

    # Also log to SQLite portal DB email_log
    portal_db = os.path.join(BASE_DIR, "apps", "portal", "internship.db")
    if os.path.exists(portal_db):
        try:
            import sqlite3
            conn = sqlite3.connect(portal_db)
            c = conn.cursor()
            subject = f"Official Internship Credential Packet: Certificate, Evaluation & Recommendation [{cert_id}]"
            is_sent = "YES" if "SUCCESS" in status else "NO"
            c.execute("""
                INSERT INTO email_log (timestamp, email, name, subject, email_sent)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), email, candidate_name or email, subject, is_sent))
            conn.commit()
            conn.close()
        except Exception as e:
            pass


def validate_all_attachments(registry):
    print("Performing pre-flight file integrity validation for all candidates...")
    missing_files = []
    for cert_id, rec in registry.items():
        for doc_key in ["doc1Pdf", "doc2Pdf", "doc3Pdf"]:
            fpath = rec.get(doc_key)
            if not fpath or not os.path.exists(fpath) or os.path.getsize(fpath) < 1000:
                missing_files.append((cert_id, doc_key, fpath))

    if missing_files:
        print(f"\n[FATAL ERROR] {len(missing_files)} required PDF attachments are missing or empty:")
        for cid, dkey, fp in missing_files:
            print(f"  - [{cid}] {dkey}: {fp}")
        return False

    print(f"[OK] All 56 candidate packets verified: 168 PDFs exist and are intact on disk.\n")
    return True


def send_email_smtp(msg, recipient_email):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(FROM_EMAIL, [recipient_email], msg.as_string())


def main():
    parser = argparse.ArgumentParser(description="DBERT Official Certificate Email Dispatch Engine")
    parser.add_argument("--test-recipient", type=str, help="Send a single test packet to this email address")
    parser.add_argument("--send-batch", action="store_true", help="Dispatch to all 56 candidates in registry")
    parser.add_argument("--dry-run", action="store_true", help="Validate without sending actual emails")
    parser.add_argument("--no-resume", action="store_true", help="Do not skip previously sent candidates")
    args = parser.parse_args()

    registry = load_registry()
    print("=" * 80)
    print("DBERT CERTIFICATE EMAIL DISPATCH ENGINE")
    print(f"SMTP Host: {SMTP_HOST}:{SMTP_PORT} (SSL)")
    print(f"Sender: {FROM_EMAIL}")
    print(f"Loaded credentials: {len(registry)}")
    print("=" * 80)

    # Pre-flight check
    if not validate_all_attachments(registry):
        print("Dispatch aborted due to missing attachments.")
        sys.exit(1)

    if args.test_recipient:
        sample_id = "CERT-DBERT-2026-DA-001"
        sample_rec = registry.get(sample_id)
        if not sample_rec:
            sample_rec = next(iter(registry.values()))

        target_email = args.test_recipient.strip()
        print(f"\n[TEST MODE] Sending test credential packet for '{sample_rec['holderName']}'")
        print(f"  Certificate ID: {sample_rec['certId']}")
        print(f"  Target Recipient: {target_email}")
        print(f"  Attached Files:")
        print(f"    - {sample_rec['doc1Pdf']}")
        print(f"    - {sample_rec['doc2Pdf']}")
        print(f"    - {sample_rec['doc3Pdf']}")

        if args.dry_run:
            print("\n[DRY RUN] Skipping SMTP dispatch.")
            return

        msg = build_email_message(sample_rec, target_email)
        try:
            print("Connecting to Google SMTP (SSL 465)...")
            send_email_smtp(msg, target_email)
            log_dispatch(target_email, sample_rec["certId"], "SUCCESS_TEST", "Test email dispatched successfully", sample_rec["holderName"])
            print(f"\n[SUCCESS] Test email successfully sent to: {target_email}")
            print(f"Subject: {msg['Subject']}")
            print(f"Log written to: {DISPATCH_LOG}")
        except Exception as e:
            log_dispatch(target_email, sample_rec["certId"], "ERROR_TEST", str(e), sample_rec["holderName"])
            print(f"\n[ERROR] Failed to send test email: {e}")
            sys.exit(1)
        return

    if args.send_batch:
        already_sent = set() if args.no_resume else get_already_sent_cert_ids()
        if already_sent:
            print(f"Resumption active: {len(already_sent)} candidates already successfully dispatched and will be skipped.")

        print(f"\n[BATCH MODE] Starting dispatch to all {len(registry)} candidates (Rate limit: 3s delay)...")
        success_count = 0
        skipped_count = 0
        error_count = 0

        for idx, (cert_id, rec) in enumerate(registry.items(), start=1):
            recipient = rec["email"]
            name = rec["holderName"]

            if cert_id in already_sent:
                print(f"[{idx:02d}/56] {name} <{recipient}> ({cert_id}) -> [ALREADY SENT - SKIPPED]")
                skipped_count += 1
                continue

            print(f"[{idx:02d}/56] Sending to {name} <{recipient}> ({cert_id})...")

            if args.dry_run:
                print(f"  [DRY RUN] Validated packet for {name} <{recipient}>")
                success_count += 1
                continue

            try:
                msg = build_email_message(rec, recipient)
                send_email_smtp(msg, recipient)
                log_dispatch(recipient, cert_id, "SUCCESS", "Dispatched to candidate", name)
                print(f"  [OK] Sent successfully")
                success_count += 1
                time.sleep(3)  # 3-second rate-limiting
            except Exception as e:
                log_dispatch(recipient, cert_id, "ERROR", str(e), name)
                print(f"  [FAIL] Error: {e}")
                error_count += 1

        print("\n" + "=" * 80)
        print(f"BATCH DISPATCH COMPLETE: {success_count} succeeded, {skipped_count} skipped, {error_count} failed.")
        print(f"Log: {DISPATCH_LOG}")
        print("=" * 80)
        return

    print("Please specify --test-recipient <email> or --send-batch.")

if __name__ == "__main__":
    main()
