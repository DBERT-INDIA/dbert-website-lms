import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_EMAIL = "abhinav.sharma@dbert.in"

for target in ["ain.sharma.abhinav@gmail.com", "ajnatechrpa@gmail.com"]:
    msg = MIMEText(f"Hello,\n\nThis is a simple plain text test message with no links sent at {formatdate(localtime=True)}.\n\nBest,\nAbhinav", "plain", "utf-8")
    msg["Subject"] = f"Test message {formatdate(localtime=True)}"
    msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
    msg["To"] = target
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        res = server.sendmail(FROM_EMAIL, [target], msg.as_string())
        print(f"Sent zero-link plain text to {target}: {res}")
