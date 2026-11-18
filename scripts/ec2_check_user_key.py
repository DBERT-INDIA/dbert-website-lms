
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    chat = conn.execute("SELECT * FROM course_subtopic_chats WHERE id = 3220").fetchone()
    print("Chat 3220:", dict(chat))
    enr = conn.execute("SELECT * FROM course_enrollments WHERE id = ?", (chat['enrollment_id'],)).fetchone()
    print("Enrollment:", dict(enr))
    intern = conn.execute("SELECT id, name, email, domain FROM intern_accounts WHERE id = ?", (enr['intern_id'],)).fetchone()
    print("Intern:", dict(intern))
    key_row = conn.execute("SELECT id, available_models_json FROM user_api_keys WHERE intern_id = ?", (intern['id'],)).fetchone()
    print("Key row:", dict(key_row) if key_row else "NO KEY")
