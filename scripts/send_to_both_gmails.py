import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "ckxnpudkapzgzbxl"
FROM_NAME = "DBERT Credential Registry"
FROM_EMAIL = "abhinav.sharma@dbert.in"

RECIPIENTS = [
    "ain.sharma.abhinav@gmail.com",
    "ain.sharma.abhinav2@gmail.com",
    "abhinav.sharma@dbert.in"
]

def send_to_all():
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
    server.login(SMTP_USER, SMTP_PASS)

    for rcpt in RECIPIENTS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"DBERT Credential Record - Test [CERT-DBERT-2026-DA-057]"
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = rcpt
        msg["Reply-To"] = FROM_EMAIL
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")
        msg["X-Priority"] = "1"
        msg["Importance"] = "high"

        text = f"""DBERT Credential Verification Test

Verification URL:
https://dbert.in/verify?certid=CERT-DBERT-2026-DA-057

Direct URL:
https://dbert.in/verify/CERT-DBERT-2026-DA-057

Candidate: Badugu venkata rajesh
Certificate ID: CERT-DBERT-2026-DA-057
Score: 88/100 (Grade A)
Domain: Data Analyst
Batch: August to October 2026
"""

        html = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 20px;">
  <div style="max-width: 580px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px;">
    <h3 style="color: #0F2942; margin-top: 0;">DBERT Official Credential Record</h3>
    <p>This is a test notification for <strong>Badugu venkata rajesh</strong> [<code>CERT-DBERT-2026-DA-057</code>].</p>
    <div style="margin: 20px 0; text-align: center;">
      <a href="https://dbert.in/verify?certid=CERT-DBERT-2026-DA-057" style="background: #0F2942; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
        View &amp; Verify Dossier Online &rarr;
      </a>
    </div>
    <p style="font-size: 13px; color: #64748b;">
      Direct link: <a href="https://dbert.in/verify?certid=CERT-DBERT-2026-DA-057">https://dbert.in/verify?certid=CERT-DBERT-2026-DA-057</a>
    </p>
  </div>
</body>
</html>
"""
        msg.attach(MIMEText(text, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))

        res = server.sendmail(FROM_EMAIL, [rcpt], msg.as_string())
        print(f"Sent to {rcpt}: res={res}")

    server.quit()
    print("All sent!")

if __name__ == '__main__':
    send_to_all()
