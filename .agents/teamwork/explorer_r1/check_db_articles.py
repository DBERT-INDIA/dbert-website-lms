import sqlite3
import os

root = r'c:\Users\user\Desktop\dbert-website-lms'
for db_rel in ['internship.db', 'apps/portal/internship.db']:
    db_path = os.path.join(root, db_rel)
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, title, published_url FROM intern_articles WHERE published_url LIKE '%dbert.online%'")
            rows = cur.fetchall()
            print(f"{db_rel}: found {len(rows)} articles with dbert.online:")
            for r in rows:
                print(f"  ID {r[0]}: {r[1]} -> {r[2]}")
        except Exception as e:
            print(f"{db_rel} error: {e}")
        conn.close()
