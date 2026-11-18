import sqlite3

conn = sqlite3.connect("apps/portal/internship.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("--- All intern_offer_letters rows ---")
for r in cur.execute("SELECT id, offer_letter_id, intern_id, email, name, domain, caution_deposit_status, accepted_at, pdf_unlocked FROM intern_offer_letters").fetchall():
    print(dict(r))

print("\n--- All dev/test intern_accounts ---")
for r in cur.execute("SELECT id, name, email, domain FROM intern_accounts WHERE email LIKE '%dbert.test%' OR id BETWEEN 9000 AND 9999").fetchall():
    print(dict(r))

print("\n--- Dev impersonate routes in app.py ---")
