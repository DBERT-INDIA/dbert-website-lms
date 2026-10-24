import sqlite3
db = sqlite3.connect('apps/portal/internship.db')
db.row_factory = sqlite3.Row
c = db.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r['name'] for r in c.fetchall()]
print('Tables:', tables)
