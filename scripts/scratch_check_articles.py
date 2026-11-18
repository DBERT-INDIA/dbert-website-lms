import sqlite3
import glob

print("--- Checking SQLite databases ---")
for db in glob.glob("apps/portal/**/*.db", recursive=True) + ["dbert.db", "data/portal.db"]:
    try:
        conn = sqlite3.connect(db)
        tables = [t[0] for t in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        article_tables = [t for t in tables if 'article' in t.lower()]
        if article_tables:
            print(f"Database {db} has article tables: {article_tables}")
            for at in article_tables:
                cols = [c[1] for c in conn.execute(f"PRAGMA table_info({at})").fetchall()]
                count = conn.execute(f"SELECT COUNT(*) FROM {at}").fetchone()[0]
                print(f"  Table {at} (rows: {count}): cols = {cols}")
                if count > 0:
                    rows = conn.execute(f"SELECT * FROM {at} LIMIT 3").fetchall()
                    print(f"    Sample row: {rows[0]}")
    except Exception as e:
        print(f"Error checking {db}: {e}")
