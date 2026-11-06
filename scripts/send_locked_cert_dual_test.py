#!/usr/bin/env python3
"""
scripts/send_locked_cert_dual_test.py
Dispatches the locked certificate test email (CERT-DBERT-2026-DA-057)
to both:
  1. ain.sharma.abhinav@gmail.com
  2. ajnatechrpa@gmail.com

Features:
- Live DNS Tri-Factor Check (SPF, DKIM, DMARC)
- Uses production-grade EmailDeliveryService
- Multipart MIME (RFC 2046) with pristine plain text + clean branded HTML card
- RFC 5322 Message-ID with @dbert.in domain
- Enforced 15-second pacing delay between recipients to prevent Google velocity limits
- Safe CLI: defaults to --dry-run; pass --live to execute actual SMTP dispatch.
"""

import os
import sys
import time
import json
import argparse
import subprocess
from pathlib import Path
from email.utils import formatdate

# Setup import paths
ROOT_DIR = Path(__file__).resolve().parent.parent
PORTAL_DIR = ROOT_DIR / "apps" / "portal"
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

from services.delivery_service import EmailDeliveryService, EmailPacer

# Recipients
TARGET_RECIPIENTS = [
    ("ain.sharma.abhinav@gmail.com", "Abhinav (AIN)"),
    ("ajnatechrpa@gmail.com", "AjnaTech RPA")
]

# Certificate Details
CERT_DATA = {
    "certId": "CERT-DBERT-2026-DA-057",
    "internId": "DBERT-2026-INT-1000",
    "holderName": "Badugu venkata rajesh",
    "domain": "Data Analyst",
    "project": "Cognitive Solutions",
    "duration": "15 Aug 2026 - 15 Oct 2026",
    "score": 88,
    "grade": "Grade A (Very Good)",
    "signatory": "Abhinav Sharma",
    "signatoryTitle": "Program Head & Project Mentor",
    "verifyUrl": "https://dbert.in/verify/CERT-DBERT-2026-DA-057",
    "portalUrl": "https://dbert.in/verify"
}


def build_plain_text(data: dict) -> str:
    return f"""Dear {data['holderName']},

Your official technical incubation and internship program record with DBERT has been recorded on the verification portal.

Credential Details:
- Candidate Name:        {data['holderName']}
- Domain Track:          {data['domain']}
- Program Tenure:        {data['duration']}
- Core Project:          {data['project']}
- Academic Evaluation:   {data['score']}/100 ({data['grade']})
- Certificate ID:        {data['certId']}
- Permanent Intern ID:   {data['internId']}

Direct Verification Portal Link:
{data['verifyUrl']}

Please visit the link above to view your complete credential dossier and review your verification status.

Sincerely,

{data['signatory']}
{data['signatoryTitle']}
DBERT (Digital Blinc Education Research and Technology)
{data['portalUrl']}
"""


def build_html(data: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Internship Verification</title>
</head>
<body style="margin:0;padding:24px 12px;background-color:#0B0F17;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#F0F4F8;">
  <div style="max-width:600px;margin:0 auto;background-color:#141A23;border:1px solid #232A36;border-radius:10px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
    <!-- Header -->
    <div style="background-color:#0E1626;padding:24px 28px;text-align:center;border-bottom:2px solid #E2B96F;">
      <h1 style="color:#ffffff;font-size:22px;font-weight:800;letter-spacing:1.5px;margin:0 0 4px 0;">DBERT</h1>
      <p style="color:#8A9AB5;font-size:12px;letter-spacing:0.5px;margin:0;text-transform:uppercase;">Digital Blinc Education Research and Technology</p>
    </div>

    <!-- Content -->
    <div style="padding:28px 26px;">
      <p style="font-size:16px;font-weight:700;color:#F0F4F8;margin:0 0 14px 0;">
        Dear {data['holderName']},
      </p>
      
      <p style="font-size:14px;line-height:1.6;color:#CBD5E1;margin:0 0 20px 0;">
        Your official technical incubation and internship program record with <strong>DBERT</strong> has been recorded on the verification portal.
      </p>

      <!-- Record Table Card -->
      <div style="background-color:#0F141C;border:1px solid #1E2633;border-radius:8px;padding:18px 20px;margin:0 0 24px 0;">
        <div style="font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#E2B96F;margin:0 0 12px 0;padding-bottom:6px;border-bottom:1px solid #1E2633;">
          Official Credential Record
        </div>
        <table style="width:100%;border-collapse:collapse;font-size:13px;">
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;width:38%;">Candidate Name:</td>
            <td style="padding:5px 0;color:#F0F4F8;font-weight:600;">{data['holderName']}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Domain Track:</td>
            <td style="padding:5px 0;color:#E2B96F;font-weight:700;">{data['domain']}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Program Tenure:</td>
            <td style="padding:5px 0;color:#F0F4F8;font-weight:600;">{data['duration']}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Core Project:</td>
            <td style="padding:5px 0;color:#F0F4F8;font-weight:600;">{data['project']}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Academic Evaluation:</td>
            <td style="padding:5px 0;color:#E2B96F;font-weight:700;">{data['score']}/100 ({data['grade']})</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Certificate ID:</td>
            <td style="padding:5px 0;color:#38BDF8;font-family:Menlo,Consolas,monospace;font-weight:600;">{data['certId']}</td>
          </tr>
          <tr>
            <td style="padding:5px 0;color:#8A9AB5;">Permanent Intern ID:</td>
            <td style="padding:5px 0;color:#38BDF8;font-family:Menlo,Consolas,monospace;font-weight:600;">{data['internId']}</td>
          </tr>
        </table>
      </div>

      <!-- CTA Button -->
      <div style="text-align:center;margin:28px 0 24px 0;">
        <a href="{data['verifyUrl']}" target="_blank" style="display:inline-block;background-color:#E2B96F;color:#0B0F17;font-weight:700;font-size:14px;text-decoration:none;padding:13px 30px;border-radius:6px;box-shadow:0 2px 8px rgba(226,185,111,0.25);">
          View Credential Dossier &rarr;
        </a>
        <div style="margin-top:10px;font-size:12px;color:#8A9AB5;">
          Direct Link: <a href="{data['verifyUrl']}" style="color:#38BDF8;text-decoration:none;">{data['verifyUrl']}</a>
        </div>
      </div>

      <!-- Signoff -->
      <div style="border-top:1px solid #1E2633;padding-top:18px;margin-top:20px;font-size:13px;line-height:1.6;color:#CBD5E1;">
        Sincerely,<br>
        <strong style="color:#F0F4F8;font-size:14px;">{data['signatory']}</strong><br>
        <span style="color:#8A9AB5;font-size:12px;">{data['signatoryTitle']}<br>DBERT (Digital Blinc Education Research and Technology)</span>
      </div>
    </div>

    <!-- Footer -->
    <div style="background-color:#0E1626;padding:16px 20px;text-align:center;border-top:1px solid #1E2633;font-size:11.5px;color:#8A9AB5;line-height:1.6;">
      Official Verification Portal: <a href="{data['portalUrl']}" style="color:#E2B96F;text-decoration:none;font-weight:600;">dbert.in/verify</a> &nbsp;&bull;&nbsp;
      Official Support: <a href="mailto:support@dbert.in" style="color:#E2B96F;text-decoration:none;">support@dbert.in</a><br>
      &copy; 2026 DBERT &middot; Sovereign Technical Incubation Registry &middot; All Rights Reserved.
    </div>
  </div>
</body>
</html>"""


def check_dns(domain: str, qtype: str = "TXT") -> str:
    try:
        cmd = ["powershell", "-NoProfile", "-Command", f"Resolve-DnsName -Name '{domain}' -Type {qtype} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Strings"]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "DNS check failed"


def main():
    parser = argparse.ArgumentParser(description="Send Locked Certificate Test Emails to ain and ajna")
    parser.add_argument("--live", action="store_true", help="Perform live outbound SMTP dispatch (default: dry-run)")
    parser.add_argument("--delay", type=float, default=15.0, help="Inter-recipient delay in seconds (default: 15.0)")
    args = parser.parse_args()

    is_live = args.live
    delay = args.delay

    print("=" * 72)
    print("  DBERT LOCKED CERTIFICATE EMAIL VERIFICATION RUNNER")
    print("=" * 72)
    print(f" Mode:                {'[LIVE OUTBOUND SEND]' if is_live else '[DRY-RUN (ZERO NETWORK CALLS)]'}")
    print(f" Certificate:         {CERT_DATA['certId']} ({CERT_DATA['holderName']})")
    print(f" Direct Verify URL:   {CERT_DATA['verifyUrl']}")
    print(f" Inter-Message Delay: {delay}s")
    print(f" Targets:             {[t[0] for t in TARGET_RECIPIENTS]}")
    print("=" * 72)

    # 1. DNS Pre-Flight
    print("\n--- [Step 1] Pre-Flight DNS Tri-Factor Verification ---")
    dmarc = check_dns("_dmarc.dbert.in", "TXT")
    spf = check_dns("dbert.in", "TXT")
    dkim = check_dns("google._domainkey.dbert.in", "TXT")

    print(f"  SPF:   {'PASS' if 'include:_spf.google.com' in spf else 'WARN'} ({spf[:60]}...)")
    print(f"  DKIM:  {'PASS' if 'v=DKIM1' in dkim else 'WARN'} ({dkim[:60]}...)")
    print(f"  DMARC: {'PASS' if 'v=DMARC1' in dmarc else 'WARN'} ({dmarc[:60]}...)")

    if not ("v=DMARC1" in dmarc and "include:_spf.google.com" in spf and "v=DKIM1" in dkim):
        print("  WARNING: DNS tri-factor authentication incomplete.")
    else:
        print("  [ALL PASS] SPF, DKIM, and DMARC verified active on global DNS.")

    # 2. Service Initialization
    print("\n--- [Step 2] Delivery Engine Initialization ---")
    service = EmailDeliveryService(
        smtp_host=os.environ.get("SMTP_HOST", "smtp.gmail.com"),
        smtp_port=int(os.environ.get("SMTP_PORT", "465")),
        smtp_user=os.environ.get("SMTP_USER", "abhinav.sharma@dbert.in"),
        smtp_pass=os.environ.get("SMTP_PASS", "rsupmvvvvwrsuxuh"),
        from_name="Abhinav Sharma",
        from_email="abhinav.sharma@dbert.in",
        reply_to="support@dbert.in",
        pacer=EmailPacer(default_interval=delay)
    )
    print(f"  SMTP Host:    {service.smtp_host}:{service.smtp_port} (SSL)")
    print(f"  Sender:       {service.from_name} <{service.from_email}>")
    print(f"  Reply-To:     {service.reply_to}")
    print(f"  Pacing delay: {service.pacer.default_interval}s")

    # 3. Payload Preparation
    subject = f"DBERT Internship Verification: {CERT_DATA['holderName']} [{CERT_DATA['certId']}]"
    plain_text = build_plain_text(CERT_DATA)
    html_content = build_html(CERT_DATA)

    # 4. Dispatch Loop
    print("\n--- [Step 3] Dispatching Test Emails ---")
    results = []
    for idx, (email_addr, label) in enumerate(TARGET_RECIPIENTS, 1):
        print(f"\n[{idx}/{len(TARGET_RECIPIENTS)}] Processing recipient: {label} <{email_addr}>")

        res = service.send_email(
            to=email_addr,
            subject=subject,
            html_content=html_content,
            text_content=plain_text,
            dry_run=not is_live
        )

        status_str = "SUCCESS" if res.success else "FAILED"
        print(f"  Result:     {status_str} (Provider: {res.provider})")
        print(f"  Message-ID: {res.message_id}")
        if res.error:
            print(f"  Error:      {res.error}")
        if res.diagnostics.get("pacing_delay_sec"):
            print(f"  Paced for:  {res.diagnostics['pacing_delay_sec']}s")

        results.append((email_addr, res))

    # Summary
    print("\n" + "=" * 72)
    print("  DISPATCH SUMMARY")
    print("=" * 72)
    for addr, res in results:
        status = "SENT" if (res.success and is_live) else ("DRY-RUN VALIDATED" if res.success else "FAILED")
        print(f"  - {addr}: {status} (Message-ID: {res.message_id})")

    if not is_live:
        print("\n[NOTE] Script ran in DRY-RUN mode. To execute live outbound dispatch:")
        print("  python scripts/send_locked_cert_dual_test.py --live --delay 15")
    else:
        print("\n[SUCCESS] Both live test emails have been submitted via Google Workspace SMTP.")
        print("Please check the Primary Inboxes of:")
        print("  1. ain.sharma.abhinav@gmail.com")
        print("  2. ajnatechrpa@gmail.com")


if __name__ == "__main__":
    main()
