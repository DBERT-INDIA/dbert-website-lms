import sqlite3

db_path = r'C:\Users\user\Desktop\internship\internship.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check courses table
courses_cols = [r[1] for r in cursor.execute("PRAGMA table_info(courses)").fetchall()]
if 'program' not in courses_cols:
    print("Adding 'program' column to courses table...")
    cursor.execute("ALTER TABLE courses ADD COLUMN program TEXT DEFAULT 'fellowship'")
    print("Column added to courses.")
else:
    print("'program' column already exists in courses.")

# Check intern_accounts table
intern_cols = [r[1] for r in cursor.execute("PRAGMA table_info(intern_accounts)").fetchall()]
if 'program' not in intern_cols:
    print("Adding 'program' column to intern_accounts table...")
    cursor.execute("ALTER TABLE intern_accounts ADD COLUMN program TEXT DEFAULT 'fellowship'")
    print("Column added to intern_accounts.")
else:
    print("'program' column already exists in intern_accounts.")

conn.commit()
conn.close()
print("Migration completed successfully.")
