import imaplib
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('abhinav.sharma@dbert.in', 'rsupmvvvvwrsuxuh')
mail.select('"[Gmail]/Sent Mail"')
typ, data = mail.search(None, 'ALL')
msg_ids = data[0].split()
print('Total in Sent Mail now:', len(msg_ids))
for msg_id in msg_ids[-2:]:
    typ, m = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (SUBJECT TO DATE)])')
    print('---')
    print(m[0][1].decode(errors='replace').strip())
mail.logout()
