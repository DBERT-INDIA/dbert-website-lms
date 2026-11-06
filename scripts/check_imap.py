import imaplib
import email

IMAP_HOST = "imap.gmail.com"
IMAP_USER = "abhinav.sharma@dbert.in"
IMAP_PASS = "ckxnpudkapzgzbxl"

def check_sent():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(IMAP_USER, IMAP_PASS)
        print("IMAP Login SUCCESS!")

        # List folders
        typ, folders = mail.list()
        print("Folders available:")
        for f in folders:
            print("  ", f.decode())

        # Select Sent Mail
        mail.select('"[Gmail]/Sent Mail"')
        typ, data = mail.search(None, 'ALL')
        msg_ids = data[0].split()
        print(f"\nTotal messages in Sent Mail: {len(msg_ids)}")

        if msg_ids:
            # Check last 5 messages
            for msg_id in msg_ids[-5:]:
                typ, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT TO DATE FROM)])')
                header_text = msg_data[0][1].decode(errors='replace').strip()
                print(f"\nMsg ID {msg_id.decode()}:\n{header_text}")

        # Also check Inbox
        mail.select('INBOX')
        typ, data_in = mail.search(None, 'ALL')
        in_ids = data_in[0].split()
        print(f"\nTotal messages in INBOX of abhinav.sharma@dbert.in: {len(in_ids)}")
        if in_ids:
            for msg_id in in_ids[-3:]:
                typ, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT TO DATE FROM)])')
                header_text = msg_data[0][1].decode(errors='replace').strip()
                print(f"\nInbox Msg ID {msg_id.decode()}:\n{header_text}")

        mail.logout()
    except Exception as e:
        print("IMAP Error:", e)

if __name__ == '__main__':
    check_sent()
