import subprocess
import os
import smtplib
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import requests

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
SERVER = "ubuntu@3.26.237.171"
REMOTE_BASE = "/var/www/dbert-website-lms"
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "ckxnpudkapzgzbxl"
FROM_NAME = "Mr. Abhinav Sharma (DBERT)"
FROM_EMAIL = "abhinav.sharma@dbert.in"
TEST_RECIPIENT = "ain.sharma.abhinav@gmail.com"

def scp_files():
    print("=" * 80)
    print("1. SCP MODIFIED COMPONENTS & PROVISIONAL REGISTRY TO EC2")
    print("=" * 80)

    files_to_scp = [
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "app", "api", "verify", "route.ts"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/app/api/verify/route.ts"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "CertificatePreviewFrame.tsx"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/app/verify/CertificatePreviewFrame.tsx"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "verify.module.css"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/app/verify/verify.module.css"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "page.tsx"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/app/verify/page.tsx"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "app", "verify", "[certId]", "page.tsx"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/app/verify/[certId]/page.tsx"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/data/certificates_registry.json"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews", "sample_certificate_locked.png"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/public/certificates/previews/sample_certificate_locked.png"
        ),
    ]

    for local_p, remote_p in files_to_scp:
        if os.path.exists(local_p):
            print(f"Uploading: {os.path.basename(local_p)} -> {remote_p}")
            subprocess.run(
                ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", local_p, remote_p],
                check=True
            )
        else:
            print(f"WARNING: File not found locally: {local_p}")

def build_and_restart():
    print("\n" + "=" * 80)
    print("2. BUILDING NEXT.JS ON EC2 AND RESTARTING SERVICE")
    print("=" * 80)

    remote_script = """
    set -e
    cd /var/www/dbert-website-lms/apps/website
    export NODE_ENV=production
    npm run build
    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true
    sudo systemctl restart dbert-website.service
    sleep 3
    systemctl is-active dbert-website.service
    """

    res = subprocess.run(
        ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", SERVER, remote_script],
        capture_output=True
    )

    out = res.stdout.decode("utf-8", errors="replace")
    safe_out = out[-1000:].encode("ascii", errors="ignore").decode("ascii")
    print("Remote build stdout tail:\n", safe_out)
    if res.returncode != 0:
        err = res.stderr.decode("utf-8", errors="replace").encode("ascii", errors="ignore").decode("ascii")
        print("Remote build stderr:\n", err)
        raise RuntimeError("EC2 Build failed.")

def test_live_pages():
    print("\n" + "=" * 80)
    print("3. VERIFYING LIVE PRODUCTION ENDPOINTS")
    print("=" * 80)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # 1. Active Verified Certificate
    print("\n[A] Testing Active Verified Certificate (CERT-DBERT-2026-DA-001)...")
    url_active = "https://dbert.in/verify/CERT-DBERT-2026-DA-001"
    r_act = requests.get(url_active, headers=headers, timeout=15)
    print(f"URL: {url_active} -> HTTP {r_act.status_code}")
    has_active_seal = "Cryptographically Verified Credential" in r_act.text
    has_provisional_banner = "Action Required: Your credential authentication and stipend release" in r_act.text
    print(f"  - Green Active Seal: {'YES (PASS)' if has_active_seal else 'NO (FAIL)'}")
    print(f"  - Provisional Banner Absent: {'YES (PASS)' if not has_provisional_banner else 'NO (FAIL)'}")

    # 2. Provisional Locked Certificate
    print("\n[B] Testing Provisional Locked Certificate (CERT-DBERT-2026-DA-057)...")
    url_prov = "https://dbert.in/verify/CERT-DBERT-2026-DA-057"
    r_prov = requests.get(url_prov, headers=headers, timeout=15)
    print(f"URL: {url_prov} -> HTTP {r_prov.status_code}")
    has_amber_pill = "Provisional Record · Action Required" in r_prov.text
    has_action_banner = "Action Required: Your credential authentication and stipend release" in r_prov.text
    has_form_cta = "https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform" in r_prov.text
    has_lock_overlay = "CERTIFICATE INACTIVE — ACTION REQUIRED" in r_prov.text
    print(f"  - Amber Provisional Pill: {'YES (PASS)' if has_amber_pill else 'NO (FAIL)'}")
    print(f"  - Urgent Action Banner: {'YES (PASS)' if has_action_banner else 'NO (FAIL)'}")
    print(f"  - Google Form Button: {'YES (PASS)' if has_form_cta else 'NO (FAIL)'}")
    print(f"  - Locked Frame Overlay: {'YES (PASS)' if has_lock_overlay else 'NO (FAIL)'}")

def build_provisional_email(c_rec, recipient_email):
    name = c_rec["holderName"]
    cert_id = c_rec["certId"]
    intern_id = c_rec["internId"]
    domain = c_rec["domain"]
    project = c_rec["project"]
    duration = c_rec["duration"]
    score = c_rec["score"]
    grade = c_rec["grade"]
    verify_url = f"https://dbert.in/verify?certid={cert_id}"

    subject = f"Official Internship Credential Packet: Certificate, Evaluation & Recommendation - {name} [{cert_id}]"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = recipient_email
    msg["Reply-To"] = FROM_EMAIL
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")
    msg["X-Mailer"] = "DBERT Credential Notification Service"
    msg["X-Entity-Ref-ID"] = cert_id

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

Your official credential records (Certificate, Evaluation Rubrics & Letter of Recommendation) are hosted on our sovereign verification portal.

Access and verify your official credentials at:
{verify_url}

Sincerely,

Mr. Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
Verification Portal: https://dbert.in/verify
Official Website: https://dbert.in
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Credential Packet</title>
<style>
  body {{
    margin: 0; padding: 0; background-color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b; -webkit-font-smoothing: antialiased;
  }}
  .email-wrapper {{ width: 100%; background-color: #f1f5f9; padding: 30px 10px; }}
  .email-card {{
    max-width: 620px; margin: 0 auto; background-color: #ffffff;
    border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }}
  .header-bar {{
    background-color: #0F2942; padding: 26px 30px; text-align: center; border-bottom: 3px solid #D4AF37;
  }}
  .header-title {{ color: #ffffff; font-size: 22px; font-weight: 800; letter-spacing: 2px; margin: 0 0 4px 0; }}
  .header-sub {{ color: #cbd5e1; font-size: 11px; letter-spacing: 0.5px; margin: 0; text-transform: uppercase; }}
  .body-content {{ padding: 32px 30px 24px 30px; }}
  .greeting {{ font-size: 17px; font-weight: 700; color: #0f172a; margin-bottom: 12px; }}
  .intro-text {{ font-size: 14px; line-height: 1.6; color: #334155; margin-bottom: 22px; }}
  .record-box {{
    background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 18px 20px; margin-bottom: 24px;
  }}
  .record-title {{
    font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #0F2942;
    margin: 0 0 12px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;
  }}
  .record-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .record-table td {{ padding: 6px 0; vertical-align: top; }}
  .label-col {{ color: #64748b; width: 36%; font-weight: 500; }}
  .value-col {{ color: #0f172a; font-weight: 600; }}
  .highlight-value {{ color: #0F2942; font-weight: 700; }}
  .code-font {{ font-family: Menlo, Monaco, Consolas, monospace; font-size: 12.5px; color: #0284c7; }}
  .cta-section {{ text-align: center; margin: 28px 0; }}
  .btn-verify {{
    display: inline-block; background-color: #0F2942; color: #ffffff !important;
    text-decoration: none; font-weight: 700; font-size: 14px; padding: 13px 32px;
    border-radius: 6px; border: 1px solid #D4AF37;
  }}
  .direct-url {{ font-size: 11.5px; color: #64748b; margin-top: 10px; word-break: break-all; }}
  .direct-url a {{ color: #0284c7; text-decoration: none; }}
  .docs-box {{
    background-color: #f8fafc; border-left: 3px solid #0F2942; padding: 14px 18px; margin-bottom: 24px; border-radius: 0 6px 6px 0;
  }}
  .docs-box-title {{ font-size: 13px; font-weight: 700; color: #0F2942; margin: 0 0 8px 0; }}
  .docs-item {{ font-size: 12.5px; line-height: 1.55; color: #475569; margin-bottom: 6px; }}
  .docs-item strong {{ color: #0f172a; }}
  .sign-off-block {{
    border-top: 1px solid #e2e8f0; padding-top: 20px; margin-top: 24px; font-size: 13.5px; color: #334155; line-height: 1.5;
  }}
  .sign-name {{ font-size: 15px; font-weight: 700; color: #0F2942; margin-top: 8px; }}
  .sign-role {{ font-size: 12px; color: #64748b; margin-top: 2px; }}
  .footer-bar {{
    background-color: #f8fafc; padding: 16px 30px; text-align: center; font-size: 11px; color: #94a3b8; border-top: 1px solid #e2e8f0;
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
        We are pleased to provide your official verified credential packet following the successful completion of your <strong>2-Month Technical Incubation &amp; Internship Program</strong> with <strong>DBERT</strong>.
      </p>

      <div class="record-box">
        <div class="record-title">Official Credential Record</div>
        <table class="record-table">
          <tr><td class="label-col">Candidate Name:</td><td class="value-col">{name}</td></tr>
          <tr><td class="label-col">Domain Track:</td><td class="value-col highlight-value">{domain}</td></tr>
          <tr><td class="label-col">Program Tenure:</td><td class="value-col">{duration}</td></tr>
          <tr><td class="label-col">Core Project:</td><td class="value-col">{project}</td></tr>
          <tr><td class="label-col">Academic Evaluation:</td><td class="value-col highlight-value">{score}/100 ({grade})</td></tr>
          <tr><td class="label-col">Certificate ID:</td><td class="value-col code-font">{cert_id}</td></tr>
          <tr><td class="label-col">Permanent Intern ID:</td><td class="value-col code-font">{intern_id}</td></tr>
        </table>
      </div>

      <div class="cta-section">
        <a href="{verify_url}" target="_blank" class="btn-verify">
          Access &amp; Verify Credential Online &rarr;
        </a>
        <div class="direct-url">
          Direct registry URL: <a href="{verify_url}">{verify_url}</a>
        </div>
      </div>

      <div class="docs-box">
        <div class="docs-box-title">Hosted Sovereign Documents (Official Records on File):</div>
        <div class="docs-item">
          &bull; <strong>1. Certificate of Completion:</strong> High-resolution credential featuring verification seal and quick-response authenticity code.
        </div>
        <div class="docs-item">
          &bull; <strong>2. Academic Project Evaluation:</strong> Comprehensive 9-dimension competency rubrics with academic clearance stamp.
        </div>
        <div class="docs-item">
          &bull; <strong>3. Official Letter of Recommendation:</strong> Executive institutional endorsement and performance appraisal.
        </div>
        <div style="font-size: 11.5px; color: #64748b; margin-top: 10px; font-style: italic;">
          * All official records are hosted directly on the DBERT sovereign registry at the link above.
        </div>
      </div>

      <div class="sign-off-block">
        Sincerely,<br>
        <div class="sign-name">Mr. Abhinav Sharma</div>
        <div class="sign-role">Program Head &amp; Project Mentor</div>
        <div class="sign-role">DBERT (Digital Blinc Education Research and Technology)</div>
      </div>
    </div>
    <div class="footer-bar">
      &copy; 2026 DBERT &middot; dbert.in &middot; All rights reserved &middot; Tamper-Proof Sovereign Registry
    </div>
  </div>
</div>
</body>
</html>
"""

    part1 = MIMEText(text_content, "plain", "utf-8")
    part2 = MIMEText(html_content, "html", "utf-8")
    msg.attach(part1)
    msg.attach(part2)

    return msg

def send_test_email():
    print("\n" + "=" * 80)
    print("4. SENDING TEST EMAIL TO", TEST_RECIPIENT)
    print("=" * 80)

    with open(os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"), "r", encoding="utf-8") as f:
        registry = json.load(f)

    sample_cert_id = "CERT-DBERT-2026-DA-057"
    sample_rec = registry.get(sample_cert_id)
    if not sample_rec:
        raise ValueError(f"Sample record not found: {sample_cert_id}")

    msg = build_provisional_email(sample_rec, TEST_RECIPIENT)

    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(FROM_EMAIL, [TEST_RECIPIENT], msg.as_string())
    server.quit()

    print(f"Test email successfully dispatched to {TEST_RECIPIENT}!")
    print(f"Subject: {msg['Subject']}")
    print(f"Sample Provisional ID: {sample_cert_id}")
    print(f"Sample Provisional Verification URL: https://dbert.in/verify?certid={sample_cert_id}")
    print(f"SSR Direct URL: https://dbert.in/verify/{sample_cert_id}")

def main():
    scp_files()
    build_and_restart()
    test_live_pages()
    send_test_email()

if __name__ == "__main__":
    main()
