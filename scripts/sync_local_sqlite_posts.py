import sqlite3
import json
with open("scripts/refresh_oldest_40_jobs_internships.py", "r", encoding="utf-8") as f:
    full_content = f.read()

# Run local SQLite update to keep local DB in sync with EC2
conn = sqlite3.connect("apps/portal/internship.db")
c = conn.cursor()

exec_scope = {}
code_to_exec = full_content.split('remote_script = """')[1].split('print(f"Total posts queued for update:')[0]
code_to_exec = code_to_exec.replace("conn = psycopg2.connect", "# conn")
code_to_exec = code_to_exec.replace("c = conn.cursor()", "# c")
exec(code_to_exec, exec_scope)

UPDATES = exec_scope["UPDATES"]
NEW_PUBLISHED_AT = exec_scope["NEW_PUBLISHED_AT"]
NEW_APPLY_BY = exec_scope["NEW_APPLY_BY"]
NEW_EXPIRES_AT = exec_scope["NEW_EXPIRES_AT"]
NEW_UPDATED_AT = exec_scope["NEW_UPDATED_AT"]

updated = 0
for post_id, data in UPDATES.items():
    c.execute("""
        UPDATE posts
        SET 
            title = ?,
            description = ?,
            responsibilities = ?,
            skills = ?,
            eligibility = ?,
            published_at = ?,
            apply_by = ?,
            expires_at = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        data["title"],
        data["description"],
        data["responsibilities"],
        data["skills"],
        data["eligibility"],
        NEW_PUBLISHED_AT,
        NEW_APPLY_BY,
        NEW_EXPIRES_AT,
        NEW_UPDATED_AT,
        post_id
    ))
    updated += 1

conn.commit()
print(f"Updated {updated} records in local apps/portal/internship.db replica!")
