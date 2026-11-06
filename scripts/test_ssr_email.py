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
    msg = MIMEText(f"Hello Abhinav,\n\nThis is Diagnostic Test 4 testing the clean SSR URL format without query parameters:\nhttps://dbert.in/verify/CERT-DBERT-2026-DA-057\n\nSent at: {formatdate(localtime=True)}", "plain", "utf-8")
    msg["Subject"] = f"Diagnostic Test 4: SSR URL format"
    msg["From"] = f"Abhinav Sharma <{FROM_EMAIL}>"
    msg["To"] = target
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="dbert.in")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASS)
        res = server.sendmail(FROM_EMAIL, [target], msg.as_string())
        print(f"Dispatched Test 4 to {target}: {res}")
