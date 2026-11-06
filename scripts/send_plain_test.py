import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import time

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "ckxnpudkapzgzbxl"
FROM_NAME = "Abhinav Sharma"
FROM_EMAIL = "abhinav.sharma@dbert.in"
RECIPIENTS = [
    "ain.sharma.abhinav@gmail.com",
    "abhinav.sharma@dbert.in"
]

def send_plain():
    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20)
    server.login(SMTP_USER, SMTP_PASS)

    for rcpt in RECIPIENTS:
        msg = MIMEText(
            f"Hi Abhinav,\n\n"
            f"This is a direct plain-text verification test sent at {formatdate(localtime=True)}.\n\n"
            f"Verification Portal URL:\n"
            f"https://dbert.in/verify?certid=CERT-DBERT-2026-DA-057\n\n"
            f"Direct Dossier URL:\n"
            f"https://dbert.in/verify/CERT-DBERT-2026-DA-057\n\n"
            f"If you see this, please check if it landed in Primary, Promotions, Updates, or Spam.\n\n"
            f"Regards,\nAbhinav",
            "plain",
            "utf-8"
        )
        msg["Subject"] = f"Action Required: Credential Verification Link [CERT-DBERT-2026-DA-057]"
        msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
        msg["To"] = rcpt
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")
        msg["X-Priority"] = "1"
        msg["Importance"] = "High"

        res = server.sendmail(FROM_EMAIL, [rcpt], msg.as_string())
        print(f"Sent plain to {rcpt}: response={res}")

    server.quit()
    print("Done sending plain test emails!")

if __name__ == '__main__':
    send_plain()
