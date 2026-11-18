import sqlite3

conn = sqlite3.connect('data/dbert_revenue_whatsapp.db')
c = conn.cursor()

c.execute("SELECT count(*) FROM whatsapp_revenue_dispatch WHERE account_num = 1 AND whatsapp_status = 'PENDING'")
pending1 = c.fetchone()[0]
c.execute("SELECT count(*) FROM whatsapp_revenue_dispatch WHERE account_num = 1 AND whatsapp_status = 'FAILED'")
failed1 = c.fetchone()[0]

print(f"Account 1: {pending1} pending, {failed1} failed")

# Transfer all pending and failed from Account 1 to Account 2
c.execute("""
    UPDATE whatsapp_revenue_dispatch 
    SET account_num = 2, account_group = 'account2', whatsapp_status = 'PENDING', whatsapp_error = NULL 
    WHERE account_num = 1 AND whatsapp_status IN ('PENDING', 'FAILED')
""")
conn.commit()

c.execute("SELECT count(*) FROM whatsapp_revenue_dispatch WHERE account_num = 2 AND whatsapp_status = 'PENDING'")
pending2 = c.fetchone()[0]
c.execute("SELECT count(*) FROM whatsapp_revenue_dispatch WHERE whatsapp_status = 'SENT'")
total_sent = c.fetchone()[0]

print(f"Account 2 now has {pending2} pending candidates to send.")
print(f"Total Sent so far across all candidates: {total_sent}")
conn.close()
