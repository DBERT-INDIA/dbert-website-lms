import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import sys

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "ckxnpudkapzgzbxl"
FROM_NAME = "Abhinav Sharma"
FROM_EMAIL = "abhinav.sharma@dbert.in"
TEST_RECIPIENTS = [
    "ain.sharma.abhinav@gmail.com",
    "abhinav.sharma@dbert.in"
]

def send_test():
    print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} via SSL...")
    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        server.set_debuglevel(2)
        print("Connected. Logging in...")
        server.login(SMTP_USER, SMTP_PASS)
        print("Logged in successfully!")

        for recipient in TEST_RECIPIENTS:
            print(f"\n--- Sending test email to: {recipient} ---")
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"DBERT Diagnostic Test Email - {formatdate(localtime=True)}"
            msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
            msg["To"] = recipient
            msg["Date"] = formatdate(localtime=True)
            msg["Message-ID"] = make_msgid(domain="dbert.in")

            text_body = f"""Hello Abhinav,

This is a direct diagnostic test email from DBERT Technical Incubation.

Verification Link:
https://dbert.in/verify?certid=CERT-DBERT-2026-DA-057

Direct Dossier Link:
https://dbert.in/verify/CERT-DBERT-2026-DA-057

Sent at: {formatdate(localtime=True)}
"""
            html_body = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif; padding: 20px;">
  <h2>DBERT Verification Portal Test</h2>
  <p>Hello Abhinav,</p>
  <p>This is a direct diagnostic test from <code>abhinav.sharma@dbert.in</code> to verify inbox delivery.</p>
  <p>
    <a href="https://dbert.in/verify?certid=CERT-DBERT-2026-DA-057" style="background: #0F2942; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
      View CERT-DBERT-2026-DA-057 Online &rarr;
    </a>
  </p>
  <p>Timestamp: {formatdate(localtime=True)}</p>
</body>
</html>
"""
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            res = server.sendmail(FROM_EMAIL, [recipient], msg.as_string())
            print(f"Sendmail result for {recipient}: {res}")

        server.quit()
        print("\nAll diagnostic emails sent successfully!")
    except Exception as e:
        print(f"SMTP Diagnostic Error: {e}", file=sys.stderr)

if __name__ == '__main__':
    send_test()
