import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
import time

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_USER = "abhinav.sharma@dbert.in"
SMTP_PASS = "rsupmvvvvwrsuxuh"
FROM_EMAIL = "abhinav.sharma@dbert.in"
TARGET = "ajnatechrpa@gmail.com"

tests = [
    {
        "id": "Test 1",
        "subject": "Diagnostic Test 1: Plain text with dbert link",
        "type": "plain",
        "body": f"Hello,\n\nThis is Diagnostic Test 1. It is plain text containing the dbert link:\nhttps://dbert.in/verify?certid=CERT-DBERT-2026-DA-057\n\nSent at: {formatdate(localtime=True)}"
    },
    {
        "id": "Test 2",
        "subject": "Diagnostic Test 2: Simple HTML with zero links",
        "type": "html",
        "body": f"<html><body><p>Hello,</p><p>This is Diagnostic Test 2. It is <b>HTML formatting</b> with <u>zero links</u>.</p><p>Sent at: {formatdate(localtime=True)}</p></body></html>"
    },
    {
        "id": "Test 3",
        "subject": "Diagnostic Test 3: Plain text with Google link only",
        "type": "plain",
        "body": f"Hello,\n\nThis is Diagnostic Test 3. It is plain text containing a link to google:\nhttps://google.com\n\nSent at: {formatdate(localtime=True)}"
    }
]

context = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
    server.login(SMTP_USER, SMTP_PASS)
    for t in tests:
        msg = MIMEText(t["body"], t["type"], "utf-8")
        msg["Subject"] = t["subject"]
        msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
        msg["To"] = TARGET
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="dbert.in")

        res = server.sendmail(FROM_EMAIL, [TARGET], msg.as_string())
        print(f"Dispatched {t['id']} to {TARGET}: {res}")
        time.sleep(2)

print("All 3 diagnostic tests dispatched to ajnatechrpa@gmail.com!")
