
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    rows = conn.execute("SELECT id, enrollment_id, subtopic_id, role, message, created_at FROM course_subtopic_chats ORDER BY id DESC LIMIT 10").fetchall()
    print("Recent chats count:", len(rows))
    for r in rows:
        print(f"[{r['id']}] Subtopic {r['subtopic_id']} | Role: {r['role']} | Time: {r['created_at']}")
        print(f"     Message: {r['message'][:200]}...")
