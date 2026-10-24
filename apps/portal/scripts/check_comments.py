import sqlite3
db = sqlite3.connect('apps/portal/internship.db')
db.row_factory = sqlite3.Row
c = db.cursor()
c.execute("SELECT sql FROM sqlite_master WHERE name='post_comments'")
print(c.fetchone()[0])
print("---")
c.execute("SELECT * FROM post_comments LIMIT 3")
for r in c.fetchall():
    print(dict(r))
