import imaplib
import email

IMAP_HOST = "imap.gmail.com"
IMAP_USER = "abhinav.sharma@dbert.in"
IMAP_PASS = "ckxnpudkapzgzbxl"

def read_bounce():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select('INBOX')

    typ, data = mail.search(None, 'ALL')
    msg_ids = data[0].split()
    print(f"Total inbox messages: {len(msg_ids)}")

    for msg_id in msg_ids:
        typ, msg_data = mail.fetch(msg_id, '(RFC822)')
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        subj = msg.get('Subject', '')
        from_hdr = msg.get('From', '')
        date_hdr = msg.get('Date', '')
        to_hdr = msg.get('To', '')
        print(f"\n--- Msg {msg_id.decode()} ---")
        print(f"From: {from_hdr}")
        print(f"To: {to_hdr}")
        print(f"Subject: {subj}")
        print(f"Date: {date_hdr}")
        
        # If mailer-daemon, print body
        if 'mailer-daemon' in from_hdr.lower() or 'failure' in subj.lower():
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        print("Body snippet:")
                        print(part.get_payload(decode=True).decode(errors='replace')[:1500])
            else:
                print("Body snippet:")
                print(msg.get_payload(decode=True).decode(errors='replace')[:1500])

    mail.logout()

if __name__ == '__main__':
    read_bounce()
