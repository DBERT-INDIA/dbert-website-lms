import os
import sys
import smtplib
import ssl
import json
from email.utils import formatdate, make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REGISTRY_PATH = os.path.join(BASE_DIR, "apps", "website", "src", "data", "certificates_registry.json")

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_NAME = "Abhinav Sharma"
FROM_EMAIL = "abhinav.sharma@dbert.in"

RECIPIENTS = [
    "ain.sharma.abhinav@gmail.com",
    "ajnatechrpa@gmail.com"
]

def send_proper_mime_email():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    sample_id = "CERT-DBERT-2026-DA-057"
    rec = registry.get(sample_id)
    name = rec["holderName"]
    cert_id = rec["certId"]
    intern_id = rec["internId"]
    domain = rec["domain"]
    project = rec["project"]
    duration = rec["duration"]
    score = rec["score"]
    grade = rec["grade"]
    verify_url = f"https://dbert.in/verify?certid={cert_id}"

    subject = f"Official Internship Credential Record: {name} [{cert_id}]"

    text_content = f"""Dear {name},

We are pleased to provide your official DBERT Internship Credential Record following the completion of your 2-Month Technical Incubation & Internship Program.

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

You can verify the authenticity of your credentials on our official registry portal:
{verify_url}

Sincerely,

Abhinav Sharma
Program Head & Project Mentor
DBERT (Digital Blinc Education Research and Technology)
https://dbert.in
"""

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DBERT Credential Record</title>
<style>
  body {{
    margin: 0;
    padding: 0;
    background-color: #f1f5f9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
  }}
  .email-wrapper {{
    width: 100%;
    background-color: #f1f5f9;
    padding: 24px 12px;
  }}
  .email-card {{
    max-width: 600px;
    margin: 0 auto;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
  }}
  .header-bar {{
    background-color: #0F2942;
    padding: 24px;
    text-align: center;
    border-bottom: 3px solid #D4AF37;
  }}
  .header-title {{
    color: #ffffff;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0;
  }}
  .header-sub {{
    color: #cbd5e1;
    font-size: 11px;
    letter-spacing: 0.5px;
    margin: 4px 0 0 0;
    text-transform: uppercase;
  }}
  .body-content {{
    padding: 28px 24px;
  }}
  .greeting {{
    font-size: 16px;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 12px;
  }}
  .intro-text {{
    font-size: 14px;
    line-height: 1.6;
    color: #334155;
    margin-bottom: 20px;
  }}
  .record-box {{
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 16px 18px;
    margin-bottom: 22px;
  }}
  .record-title {{
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #0F2942;
    margin: 0 0 10px 0;
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
    width: 38%;
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
    font-family: monospace;
    font-size: 12.5px;
    color: #0284c7;
  }}
  .cta-section {{
    text-align: center;
    margin: 26px 0;
  }}
  .btn-verify {{
    display: inline-block;
    background-color: #0F2942;
    color: #ffffff !important;
    text-decoration: none;
    font-weight: 700;
    font-size: 14px;
    padding: 12px 28px;
    border-radius: 6px;
    border: 1px solid #D4AF37;
  }}
  .direct-url {{
    font-size: 12px;
    color: #64748b;
    margin-top: 10px;
    word-break: break-all;
  }}
  .sign-off-block {{
    border-top: 1px solid #e2e8f0;
    padding-top: 18px;
    margin-top: 22px;
    font-size: 13px;
    color: #334155;
    line-height: 1.5;
  }}
  .sign-name {{
    font-size: 14px;
    font-weight: 700;
    color: #0F2942;
    margin-top: 6px;
  }}
  .sign-role {{
    font-size: 12px;
    color: #64748b;
  }}
  .footer-bar {{
    background-color: #f8fafc;
    padding: 16px 24px;
    text-align: center;
    font-size: 11px;
    color: #64748b;
    border-top: 1px solid #e2e8f0;
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
        We are pleased to provide your official verified credential record following the completion of your <strong>2-Month Technical Incubation &amp; Internship Program</strong> with <strong>DBERT</strong>.
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
          View &amp; Verify Credential Online &rarr;
        </a>
        <div class="direct-url">
          Direct verification URL: <a href="{verify_url}" style="color: #0284c7;">{verify_url}</a>
        </div>
      </div>

      <div class="sign-off-block">
        Sincerely,<br>
        <div class="sign-name">{FROM_NAME}</div>
        <div class="sign-role">Program Head &amp; Project Mentor<br>DBERT (Digital Blinc Education Research and Technology)</div>
      </div>
    </div>

    <div class="footer-bar">
      Official Verification Portal: <a href="https://dbert.in/verify">dbert.in/verify</a> &nbsp;&bull;&nbsp; 
      Website: <a href="https://dbert.in">dbert.in</a><br>
      &copy; 2026 DBERT. All rights reserved. Official institutional notification.
    </div>
  </div>
</div>
</body>
</html>
"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        for target in RECIPIENTS:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
            msg["To"] = target
            msg["Reply-To"] = FROM_EMAIL
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain="dbert.in")

            msg.attach(MIMEText(text_content, "plain", "utf-8"))
            msg.attach(MIMEText(html_content, "html", "utf-8"))

            res = server.sendmail(FROM_EMAIL, [target], msg.as_string())
            print(f"Sent clean alternative email to {target}: {res}")

if __name__ == '__main__':
    send_proper_mime_email()
