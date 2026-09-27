import sqlite3
conn = sqlite3.connect('apps/portal/internship.db')
print(conn.execute("SELECT email, COUNT(*) FROM intern_accounts GROUP BY email HAVING COUNT(*) > 1").fetchall())
