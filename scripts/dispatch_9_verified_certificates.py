import os
import sys
import json
import time
from datetime import datetime
from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path("apps/portal").resolve()))

# Load .env
env_file = Path("apps/portal/.env")
if env_file.exists():
    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

from services.delivery_service import EmailDeliveryService

REGISTRY_PATH = Path("apps/website/src/data/certificates_registry.json")
TRACKING_PATH = Path("data/dispatch_tracking_9_verified.json")
LOG_PATH = Path("data/dispatch_9_verified.log")

TARGET_CERT_IDS = [
    "CERT-DBERT-2026-AIML-092",
    "CERT-DBERT-2026-DA-117",
    "CERT-DBERT-2026-FSD-070",
    "CERT-DBERT-2026-PA-023",
    "CERT-DBERT-2026-DA-124",
    "CERT-DBERT-2026-DA-077",
    "CERT-DBERT-2026-DA-183",
    "CERT-DBERT-2026-DA-109",
    "CERT-DBERT-2026-DA-184"
]

FROM_NAME = "Abhinav Sharma"
FROM_EMAIL = "abhinav.sharma@dbert.in"
REPLY_TO_EMAIL = "abhinav.sharma@dbert.in"


def log_message(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{ts}] {msg}"
    print(formatted)
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass


def build_verified_email(c_rec: dict):
    name = c_rec["holderName"]
    cert_id = c_rec["certId"]
    intern_id = c_rec.get("internId", "DBERT-INT")
    domain = c_rec.get("domain", "Data Analyst")
    project = c_rec.get("project", "Enterprise Incubation Project")
    duration = c_rec.get("duration", "2 Months")
    score = c_rec.get("score", 85)
    grade = c_rec.get("grade", "Grade A (Very Good)")
    verify_url = f"https://dbert.in/verify/{cert_id}"
    linkedin_url = (
        f"https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME"
        f"&name={domain}+Internship+Credential"
        f"&organizationName=DBERT"
        f"&issueYear=2026&issueMonth=11"
        f"&certUrl={verify_url}"
        f"&certId={cert_id}"
    )

    subject = f"Official Internship Credential Packet — {name} [{cert_id}]"

    plain_text = f"""Dear {name},

Congratulations! Your official DBERT Internship Credential Packet is now activated and verified on the sovereign technical registry.

Official Verification Record:
--------------------------------------------------------------------------------
- Candidate Name:        {name}
- Domain Track:          {domain}
- Program Tenure:        {duration}
- Core Project:          {project}
- Academic Evaluation:   {score}/100 ({grade})
- Certificate ID:        {cert_id}
- Permanent Intern ID:   {intern_id}
- Online Verification:   {verify_url}
- Add to LinkedIn:       {linkedin_url}
--------------------------------------------------------------------------------

Your credential contains 256-Bit cryptographic authentication and embedded micro-QR verification. You can view, share, and add your verified credential directly to your professional profiles at any time using the official link above.

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Official Sovereign Portal: https://dbert.in
Verification Registry: https://dbert.in/verify
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DBERT Official Credential</title>
</head>
<body style="margin:0;padding:0;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:10px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
    <!-- Header -->
    <div style="background-color:#0E1626;padding:26px 30px;text-align:center;border-bottom:2px solid #E2B96F;">
      <div style="color:#E2B96F;font-size:22px;font-weight:800;letter-spacing:3px;">D B E R T</div>
      <div style="color:#8A9AB5;font-size:12px;letter-spacing:1px;margin-top:4px;">SOVEREIGN TECHNICAL INCUBATION REGISTRY</div>
    </div>

    <!-- Content -->
    <div style="padding:32px 30px;">
      <div style="display:inline-block;background:rgba(16,185,129,0.15);color:#10B981;font-weight:700;font-size:11px;letter-spacing:1px;padding:4px 12px;border-radius:20px;border:1px solid rgba(16,185,129,0.3);margin-bottom:16px;">
        &#10003; OFFICIAL CREDENTIAL VERIFIED & ACTIVE
      </div>

      <h1 style="font-size:20px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;line-height:1.4;">
        Official Internship Credential Issued for {name}
      </h1>

      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 20px 0;">
        Dear <strong>{name}</strong>,<br><br>
        We are pleased to inform you that your official DBERT Internship Credential Packet has been generated, cryptographically signed, and registered on the permanent DBERT sovereign verification engine.
      </p>

      <!-- Credential Table -->
      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:20px;margin-bottom:24px;">
        <div style="font-size:11px;color:#E2B96F;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:12px;">
          AUTHENTICATED RECORD DOSSIER
        </div>
        <table style="width:100%;font-size:13px;border-collapse:collapse;">
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;width:40%;">Candidate Name:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{name}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Domain Track:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{domain}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Program Tenure:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{duration}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Core Project:</td>
            <td style="padding:6px 0;color:#F0F4F8;font-weight:600;">{project}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Academic Evaluation:</td>
            <td style="padding:6px 0;color:#10B981;font-weight:700;">{score}/100 ({grade})</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Certificate ID:</td>
            <td style="padding:6px 0;color:#38BDF8;font-family:monospace;font-weight:600;">{cert_id}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Permanent Intern ID:</td>
            <td style="padding:6px 0;color:#38BDF8;font-family:monospace;font-weight:600;">{intern_id}</td>
          </tr>
        </table>
      </div>

      <!-- Action Buttons -->
      <div style="text-align:center;margin:28px 0 20px 0;">
        <a href="{verify_url}" target="_blank" style="display:inline-block;background-color:#E2B96F;color:#0B0F17;font-weight:700;font-size:14px;text-decoration:none;padding:14px 28px;border-radius:6px;box-shadow:0 2px 10px rgba(226,185,111,0.3);margin-bottom:12px;">
          View Verified Credential Dossier &rarr;
        </a>
        <br>
        <a href="{linkedin_url}" target="_blank" style="display:inline-block;background-color:#0A66C2;color:#ffffff;font-weight:600;font-size:12px;text-decoration:none;padding:8px 18px;border-radius:4px;margin-top:6px;">
          Add to LinkedIn Profile ↗
        </a>
      </div>

      <!-- Signoff -->
      <div style="border-top:1px solid #1E2633;padding-top:18px;margin-top:24px;font-size:13px;line-height:1.6;color:#CBD5E1;">
        Sincerely,<br>
        <strong style="color:#F0F4F8;font-size:14px;">Abhinav Sharma</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">Program Head & Project Mentor<br>DBERT (Digital Blinc Education Research and Technology)</span>
      </div>
    </div>

    <!-- Footer -->
    <div style="background-color:#0E1626;padding:16px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11.5px;color:#8A9AB5;line-height:1.6;">
      Official Verification Portal: <a href="{verify_url}" style="color:#E2B96F;text-decoration:none;">dbert.in/verify</a> &nbsp;&bull;&nbsp;
      Support: <a href="mailto:support@dbert.in" style="color:#E2B96F;text-decoration:none;">support@dbert.in</a><br>
      &copy; 2026 DBERT &middot; Sovereign Technical Incubation Registry &middot; All Rights Reserved.
    </div>
  </div>
</body>
</html>"""

    return subject, plain_text, html_content


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dispatch official verified certificates to the 9 candidates.")
    parser.add_argument("--live", action="store_true", help="Execute live SMTP dispatch (default is dry run).")
    parser.add_argument("--delay", type=float, default=30.0, help="Inter-message pacing in seconds.")
    args = parser.parse_args()

    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    # Initialize tracking
    if TRACKING_PATH.exists():
        with open(TRACKING_PATH, "r", encoding="utf-8") as f:
            tracking = json.load(f)
    else:
        tracking = []
        for cid in TARGET_CERT_IDS:
            cand = registry.get(cid)
            if cand:
                tracking.append({
                    "certId": cid,
                    "holderName": cand["holderName"],
                    "email": cand["email"],
                    "domain": cand["domain"],
                    "status": "PENDING",
                    "sent_at": None,
                    "message_id": None,
                    "error": None
                })
        with open(TRACKING_PATH, "w", encoding="utf-8") as f:
            json.dump(tracking, f, indent=2)

    service = EmailDeliveryService(
        smtp_host=os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.environ.get("SMTP_PORT", "465")),
        smtp_user=os.environ.get("SMTP_USER", "abhinav.sharma@dbert.in"),
        smtp_pass=os.environ.get("SMTP_PASS", "rsupmvvvvwrsuxuh"),
        from_name=FROM_NAME,
        from_email=FROM_EMAIL,
        reply_to=REPLY_TO_EMAIL
    )

    log_message(f"Starting dispatch of {len(tracking)} verified certificates (Live: {args.live})...")

    for item in tracking:
        if item["status"] == "SENT":
            log_message(f"Skipping {item['holderName']} ({item['certId']}) - already SENT.")
            continue

        cid = item["certId"]
        cand = registry.get(cid)
        if not cand:
            continue

        subject, plain, html_body = build_verified_email(cand)
        log_message(f"\n>>> Dispatching to: {cand['holderName']} <{cand['email']}> [{cid}]")

        try:
            res = service.send_email(
                to=cand["email"],
                subject=subject,
                html_content=html_body,
                text_content=plain,
                dry_run=not args.live
            )

            if res.success:
                item["status"] = "SENT"
                item["sent_at"] = datetime.now().isoformat()
                item["message_id"] = res.message_id
                item["error"] = None
                log_message(f"  [SUCCESS] Sent! Message-ID: {res.message_id}")
            else:
                item["status"] = "PENDING"
                item["error"] = res.error
                log_message(f"  [FAILED/PENDING] {res.error}")
                if res.error and ("550 5.4.5" in res.error or "sending limit" in res.error.lower()):
                    log_message("  [CIRCUIT BREAKER] Google SMTP daily sending limit encountered. Halting dispatch gracefully.")
                    with open(TRACKING_PATH, "w", encoding="utf-8") as f:
                        json.dump(tracking, f, indent=2)
                    sys.exit(55)

        except Exception as e:
            item["status"] = "PENDING"
            item["error"] = str(e)
            log_message(f"  [EXCEPTION] {e}")

        with open(TRACKING_PATH, "w", encoding="utf-8") as f:
            json.dump(tracking, f, indent=2)

        if args.live:
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
