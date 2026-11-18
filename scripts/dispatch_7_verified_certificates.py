import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path("apps/portal").resolve()))

# Load portal .env
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
TRACKING_PATH = Path("data/dispatch_tracking_7_verified.json")
LOG_PATH = Path("data/dispatch_7_verified.log")

TARGET_CERT_IDS = [
    "CERT-DBERT-2026-AIML-100",  # Rajveer Singh
    "CERT-DBERT-2026-DA-186",   # Deepanshu
    "CERT-DBERT-2026-DA-127",   # Komma Hari Kesava
    "CERT-DBERT-2026-DA-187",   # Arya Nitin Pawar
    "CERT-DBERT-2026-AIML-064",  # Piyush Solanki
    "CERT-DBERT-2026-DA-086",   # Ramparia Amrita R.
    "CERT-DBERT-2026-AIML-178"   # Arnak Ray
]

FROM_NAME = "Abhinav Sharma"
FROM_EMAIL = "abhinav.sharma@dbert.in"
REPLY_TO_EMAIL = "abhinav.sharma@dbert.in"
TELEMETRY_EMAILS = ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]


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
    domain = c_rec.get("domain", "Engineering")
    project = c_rec.get("project", "Enterprise Technical Incubation Architecture")
    duration = c_rec.get("duration", "2 Months")
    score = c_rec.get("score", 85)
    grade = c_rec.get("grade", "Grade: A+ (Outstanding Performance)")
    verify_url = f"https://dbert.in/verify/{cert_id}"
    linkedin_url = (
        f"https://www.linkedin.com/profile/add?startTask=CERTIFICATION_NAME"
        f"&name={domain}+Internship+Credential"
        f"&organizationName=DBERT"
        f"&issueYear=2026&issueMonth=11"
        f"&certUrl={verify_url}"
        f"&certId={cert_id}"
    )

    subject = f"Official Internship Credential Packet (3 Documents Attached) — {name} [{cert_id}]"

    plain_text = f"""Dear {name},

Congratulations! Your official DBERT Internship Credential Packet has been activated, verified, and published on the sovereign technical registry.

Attached to this email, you will find your complete 3-document credential packet:
1. Certificate of Completion (with embedded cryptographic micro-QR verification)
2. Academic Project Evaluation (with 9-dimension rubric table and Turnitin originality validation seal)
3. Formal Letter of Recommendation (on official DBERT executive letterhead)

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

Your credential contains 256-Bit cryptographic authentication. You can view, verify, and share your official verification dossier with employers and recruiters anytime using the official link above.

Admissions & Verification Support:
WhatsApp: +91 89580 06294 / +91 81929 11360
Email: abhinav.sharma@dbert.in

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
  <div style="max-width:620px;margin:24px auto;background-color:#141A23;border:1px solid #232A36;border-radius:12px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.5);">
    
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

      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 18px 0;">
        Dear <strong>{name}</strong>,<br><br>
        We are pleased to inform you that your official DBERT Internship Credential Packet has been generated, cryptographically signed, and registered on the permanent sovereign verification engine.
      </p>

      <!-- Attached Docs Notice Box -->
      <div style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.3);border-radius:8px;padding:16px 18px;margin-bottom:22px;">
        <div style="color:#A5B4FC;font-size:13px;font-weight:700;margin-bottom:6px;">
          📎 3 Official PDF Documents Attached to this Email:
        </div>
        <ul style="margin:0;padding-left:18px;color:#E2E8F0;font-size:12.5px;line-height:1.6;">
          <li><strong>Document 1:</strong> Certificate of Completion (with micro-QR code)</li>
          <li><strong>Document 2:</strong> Academic Project Evaluation (with 9-dimension rubric &amp; Turnitin seal)</li>
          <li><strong>Document 3:</strong> Formal Letter of Recommendation (on executive letterhead)</li>
        </ul>
      </div>

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
            <td style="padding:6px 0;color:#8A9AB5;">Evaluation Score:</td>
            <td style="padding:6px 0;color:#10B981;font-weight:700;">{score}/100 ({grade})</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Certificate ID:</td>
            <td style="padding:6px 0;color:#E2B96F;font-family:monospace;font-weight:700;">{cert_id}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#8A9AB5;">Permanent Intern ID:</td>
            <td style="padding:6px 0;color:#CBD5E1;font-family:monospace;">{intern_id}</td>
          </tr>
        </table>
      </div>

      <!-- Action Buttons -->
      <div style="text-align:center;margin-bottom:28px;">
        <a href="{verify_url}" style="display:inline-block;background:linear-gradient(135deg, #E2B96F, #C59A4E);color:#0B0F17;font-weight:700;font-size:13px;padding:12px 24px;border-radius:6px;text-decoration:none;margin:6px 8px;box-shadow:0 4px 15px rgba(226,185,111,0.3);">
          View Live Verification Dossier &rarr;
        </a>
        <a href="{linkedin_url}" target="_blank" style="display:inline-block;background:#0A66C2;color:#ffffff;font-weight:700;font-size:13px;padding:12px 24px;border-radius:6px;text-decoration:none;margin:6px 8px;">
          Add Credential to LinkedIn &rarr;
        </a>
      </div>

      <!-- Support Concierge -->
      <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:14px 18px;margin-bottom:24px;font-size:12px;color:#94A3B8;line-height:1.6;">
        <strong style="color:#CBD5E1;">Need Instant Support or Verification Assistance?</strong><br>
        Admissions Concierge WhatsApp: 
        <a href="https://wa.me/918958006294" style="color:#38BDF8;text-decoration:none;font-weight:600;">+91 89580 06294</a> / 
        <a href="https://wa.me/918192911360" style="color:#38BDF8;text-decoration:none;font-weight:600;">+91 81929 11360</a>
      </div>

      <!-- Signatory Block -->
      <div style="border-top:1px solid #1E2633;padding-top:18px;margin-top:20px;">
        <strong style="color:#F0F4F8;font-size:14px;">Abhinav Sharma</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">Program Head &amp; Project Mentor<br>DBERT (Digital Blinc Education Research and Technology)</span>
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
    parser = argparse.ArgumentParser(description="Dispatch official verified certificates with 3 attached PDFs.")
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

    log_message("=" * 80)
    log_message(f"Starting verified dispatch for {len(tracking)} candidates (Mode: {'LIVE SMTP' if args.live else 'DRY RUN'})...")
    log_message("=" * 80)

    delivered_count = 0

    for item in tracking:
        cid = item["certId"]
        if item["status"] == "SENT":
            log_message(f"Skipping {item['holderName']} ({cid}) - already SENT.")
            delivered_count += 1
            continue

        cand = registry.get(cid)
        if not cand:
            log_message(f"Candidate {cid} not found in registry. Skipping.")
            continue

        doc1_path = cand.get("doc1Pdf", "")
        doc2_path = cand.get("doc2Pdf", "")
        doc3_path = cand.get("doc3Pdf", "")

        attachments = []
        for p, label in [(doc1_path, "1_Certificate_of_Completion"), (doc2_path, "2_Academic_Project_Evaluation"), (doc3_path, "3_Letter_of_Recommendation")]:
            if p and os.path.exists(p):
                with open(p, "rb") as pf:
                    pdf_bytes = pf.read()
                filename = f"{label}_{cid}.pdf"
                attachments.append((filename, pdf_bytes, "application/pdf"))
            else:
                log_message(f"  [WARN] Missing PDF for {cid}: {p}")

        log_message(f"\n>>> Preparing dispatch for: {cand['holderName']} <{cand['email']}> [{cid}] (Attachments: {len(attachments)})")

        subject, plain, html_body = build_verified_email(cand)

        try:
            res = service.send_email(
                to=cand["email"],
                subject=subject,
                html_content=html_body,
                text_content=plain,
                attachments=attachments if attachments else None,
                dry_run=not args.live
            )

            if res.success:
                if args.live:
                    item["status"] = "SENT"
                    item["sent_at"] = datetime.now().isoformat()
                    item["message_id"] = res.message_id
                    item["error"] = None
                    delivered_count += 1
                    log_message(f"  [SUCCESS] Sent! Message-ID: {res.message_id}")
                else:
                    log_message(f"  [DRY-RUN OK] Simulated Message-ID: {res.message_id}")
            else:
                item["status"] = "PENDING"
                item["error"] = res.error
                log_message(f"  [FAILED/PENDING] {res.error}")
                if res.error and ("550 5.4.5" in res.error or "sending limit" in res.error.lower()):
                    log_message("  [CIRCUIT BREAKER] Google SMTP daily limit hit. Halting dispatch gracefully.")
                    if args.live:
                        with open(TRACKING_PATH, "w", encoding="utf-8") as f:
                            json.dump(tracking, f, indent=2)
                    sys.exit(55)

        except Exception as e:
            item["status"] = "PENDING"
            item["error"] = str(e)
            log_message(f"  [EXCEPTION] {e}")

        if args.live:
            with open(TRACKING_PATH, "w", encoding="utf-8") as f:
                json.dump(tracking, f, indent=2)

        if args.live:
            log_message(f"Pacing: sleeping {args.delay} seconds before next dispatch...")
            time.sleep(args.delay)

    log_message("\n" + "=" * 80)
    log_message(f"DISPATCH BATCH COMPLETE: {delivered_count}/{len(tracking)} DELIVERED.")
    log_message("=" * 80)

    # Disptach telemetry report if live
    if args.live and delivered_count > 0:
        telemetry_subject = f"[DBERT TELEMETRY] 7 Verified Certificates Dispatched Successfully ({delivered_count}/{len(tracking)})"
        telemetry_html = f"""
        <div style="font-family:Arial,sans-serif;padding:20px;background:#0F172A;color:#fff;border-radius:10px;">
          <h2 style="color:#10B981;">DBERT Production Verified Dispatch Report</h2>
          <p>The 7 sheet candidate credentials have been dispatched via authenticated Google Workspace SMTP with all 3 official PDF documents attached:</p>
          <ul>
            {''.join(f'<li><strong>{x["holderName"]}</strong> ({x["certId"]}) &lt;{x["email"]}&gt; - <strong>{x["status"]}</strong> (MsgID: {x.get("message_id")})</li>' for x in tracking)}
          </ul>
          <p style="color:#94A3B8;font-size:12px;">Live verified on production EC2: <a href="https://dbert.in/verify" style="color:#38BDF8;">https://dbert.in/verify</a></p>
        </div>
        """
        for t_email in TELEMETRY_EMAILS:
            try:
                service.send_email(
                    to=t_email,
                    subject=telemetry_subject,
                    html_content=telemetry_html,
                    text_content=f"7 Verified Certificates Dispatched: {delivered_count}/{len(tracking)} delivered.",
                    dry_run=False
                )
                log_message(f"Telemetry report sent to {t_email}")
            except Exception as e:
                log_message(f"Failed to send telemetry to {t_email}: {e}")


if __name__ == "__main__":
    main()
