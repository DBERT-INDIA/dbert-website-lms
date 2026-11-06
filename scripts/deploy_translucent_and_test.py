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
    print("1. SCP TRANSLUCENT LOCK & IMAGE FIX TO EC2")
    print("=" * 80)

    files_to_scp = [
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
            os.path.join(BASE_DIR, "apps", "website", "src", "app", "api", "verify", "route.ts"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/app/api/verify/route.ts"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/data/certificates_registry.json"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "src", "lib", "verification.ts"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/src/lib/verification.ts"
        ),
        (
            os.path.join(BASE_DIR, "apps", "website", "public", "certificates", "previews", "sample_certificate_locked.png"),
            f"{SERVER}:{REMOTE_BASE}/apps/website/public/certificates/previews/sample_certificate_locked.png"
        ),
    ]

    for local_p, remote_p in files_to_scp:
        print(f"Uploading: {os.path.basename(local_p)} -> {remote_p}")
        subprocess.run(
            ["scp", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", local_p, remote_p],
            check=True
        )

def build_and_restart():
    print("\n" + "=" * 80)
    print("2. BUILDING NEXT.JS ON EC2 AND RESTARTING SERVICE")
    print("=" * 80)

    remote_script = """
    set -e
    cd /var/www/dbert-website-lms/apps/website
    rm -f .next/trace* 2>/dev/null || true
    export NODE_ENV=production
    npm run build
    cp -r public .next/standalone/ 2>/dev/null || true
    cp -r public .next/standalone/apps/website/ 2>/dev/null || true
    sudo chmod -R 755 public/
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

def test_live():
    print("\n" + "=" * 80)
    print("3. VERIFYING LIVE PRODUCTION ENDPOINTS")
    print("=" * 80)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # 1. Active Verified
    url_act = "https://dbert.in/verify/CERT-DBERT-2026-DA-001"
    r1 = requests.get(url_act, headers=headers)
    print(f"Active Verified: {url_act} -> HTTP {r1.status_code}")
    print(f"  - Has verified seal: {'YES' if 'Cryptographically Verified Credential' in r1.text else 'NO'}")

    # 2. Provisional Locked
    url_prov = "https://dbert.in/verify/CERT-DBERT-2026-DA-057"
    r2 = requests.get(url_prov, headers=headers)
    print(f"Provisional Locked: {url_prov} -> HTTP {r2.status_code}")
    print(f"  - Has translucent lock pill: {'YES' if 'RECORD ON FILE' in r2.text else 'NO'}")
    print(f"  - Has candidate name (Badugu venkata rajesh): {'YES' if 'Badugu venkata rajesh' in r2.text else 'NO'}")
    print(f"  - Has college (Vishnu institute of technology): {'YES' if 'Vishnu institute of technology' in r2.text else 'NO'}")
    print(f"  - Has Urgent Action Banner: {'YES' if 'Action Required: Your credential authentication and stipend release' in r2.text else 'NO'}")
    print(f"  - Has Google Form CTA: {'YES' if 'docs.google.com/forms' in r2.text else 'NO'}")

def send_targeted_test_email():
    print("\n" + "=" * 80)
    print("4. DISPATCHING TEST EMAIL TO", TEST_RECIPIENT)
    print("=" * 80)

    with open(os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json"), "r", encoding="utf-8") as f:
        registry = json.load(f)

    rec = registry.get("CERT-DBERT-2026-DA-057")
    name = rec["holderName"]
    cert_id = rec["certId"]
    domain = rec["domain"]
    duration = rec["duration"]
    project = rec["project"]
    score = rec["score"]
    grade = rec["grade"]
    intern_id = rec["internId"]
    verify_url = f"https://dbert.in/verify?certid={cert_id}"
    ssr_url = f"https://dbert.in/verify/{cert_id}"

    # Clear subject with no spam triggers
    subject = f"DBERT Official Credential Record - {name} [{cert_id}]"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = TEST_RECIPIENT
    msg["Reply-To"] = FROM_EMAIL
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")

    text_body = f"""Dear {name},

Your official credential record following the completion of your 2-Month Technical Incubation & Internship Program with DBERT is on record:

- Candidate Name: {name}
- Domain Track: {domain}
- Program Tenure: {duration}
- Core Project: {project}
- Academic Score: {score}/100 ({grade})
- Certificate ID: {cert_id}
- Permanent Intern ID: {intern_id}

Direct Verification Link:
{verify_url}

Direct SSR Route:
{ssr_url}

Please review your dossier on the official portal above.

Sincerely,
Mr. Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
https://dbert.in
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 20px; color: #1e293b;">
  <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <div style="background-color: #0F2942; padding: 24px; text-align: center; border-bottom: 3px solid #D4AF37;">
      <h2 style="color: #ffffff; margin: 0; font-size: 22px; letter-spacing: 1.5px;">DBERT</h2>
      <p style="color: #cbd5e1; margin: 4px 0 0 0; font-size: 11px; text-transform: uppercase;">Digital Blinc Education Research and Technology</p>
    </div>
    <div style="padding: 28px;">
      <p style="font-size: 16px; font-weight: bold; margin-top: 0;">Dear {name},</p>
      <p style="font-size: 14px; line-height: 1.6; color: #334155;">
        Your official credential record following the completion of your <strong>2-Month Technical Incubation &amp; Internship Program</strong> is now recorded on the sovereign registry:
      </p>

      <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; margin: 20px 0;">
        <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
          <tr><td style="padding: 5px 0; color: #64748b; width: 40%;">Candidate Name:</td><td style="font-weight: bold; color: #0f172a;">{name}</td></tr>
          <tr><td style="padding: 5px 0; color: #64748b;">Domain Track:</td><td style="font-weight: bold; color: #0F2942;">{domain}</td></tr>
          <tr><td style="padding: 5px 0; color: #64748b;">Program Tenure:</td><td style="color: #0f172a;">{duration}</td></tr>
          <tr><td style="padding: 5px 0; color: #64748b;">Core Project:</td><td style="color: #0f172a;">{project}</td></tr>
          <tr><td style="padding: 5px 0; color: #64748b;">Academic Score:</td><td style="font-weight: bold; color: #059669;">{score}/100 ({grade})</td></tr>
          <tr><td style="padding: 5px 0; color: #64748b;">Certificate ID:</td><td style="font-family: monospace; color: #0284c7; font-weight: bold;">{cert_id}</td></tr>
          <tr><td style="padding: 5px 0; color: #64748b;">Permanent Intern ID:</td><td style="font-family: monospace; color: #64748b;">{intern_id}</td></tr>
        </table>
      </div>

      <div style="text-align: center; margin: 28px 0;">
        <a href="{verify_url}" style="display: inline-block; background-color: #0F2942; color: #ffffff !important; text-decoration: none; font-weight: bold; font-size: 14px; padding: 13px 30px; border-radius: 6px; border: 1px solid #D4AF37;">
          View &amp; Verify Dossier Online &rarr;
        </a>
        <p style="font-size: 12px; color: #64748b; margin-top: 10px;">
          Direct URL: <a href="{verify_url}" style="color: #0284c7;">{verify_url}</a>
        </p>
      </div>

      <div style="border-top: 1px solid #e2e8f0; padding-top: 18px; margin-top: 24px; font-size: 13px; color: #475569;">
        Sincerely,<br>
        <strong>Mr. Abhinav Sharma</strong><br>
        Program Head &amp; Project Mentor<br>
        DBERT (Digital Blinc Education Research and Technology)
      </div>
    </div>
  </div>
</body>
</html>
"""

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
    server.login(SMTP_USER, SMTP_PASS)
    errs = server.sendmail(FROM_EMAIL, [TEST_RECIPIENT], msg.as_string())
    server.quit()
    print("SMTP result:", errs)
    print(f"Test email successfully dispatched to {TEST_RECIPIENT}!")

def main():
    scp_files()
    build_and_restart()
    test_live()
    send_targeted_test_email()

if __name__ == '__main__':
    main()
