import imaplib
import email

IMAP_HOST = "imap.gmail.com"
IMAP_USER = "abhinav.sharma@dbert.in"
IMAP_PASS = "ckxnpudkapzgzbxl"

def inspect_sent_headers():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select('"[Gmail]/Sent Mail"')

    typ, data = mail.search(None, 'ALL')
    msg_ids = data[0].split()

    if msg_ids:
        # Check the last sent message
        last_id = msg_ids[-1]
        typ, msg_data = mail.fetch(last_id, '(RFC822)')
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        
        print(f"=== Headers for Sent Msg {last_id.decode()} ===")
        for k, v in msg.items():
            if k.lower() in ['from', 'to', 'subject', 'date', 'message-id', 'dkim-signature', 'received', 'authentication-results']:
                print(f"{k}: {v[:100] if len(v) > 100 else v}")

    mail.logout()

if __name__ == '__main__':
    inspect_sent_headers()
