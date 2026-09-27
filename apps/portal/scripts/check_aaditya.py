import sqlite3
conn = sqlite3.connect('apps/portal/internship.db')
cur = conn.cursor()
cur.execute("SELECT id FROM intern_accounts WHERE email LIKE '%aadityakadam432%'")
print(cur.fetchone())
