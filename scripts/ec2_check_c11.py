
import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db

with get_db() as conn:
    c = conn.execute("SELECT id, title, domain FROM courses WHERE id = 11").fetchone()
    print("Course 11:", dict(c) if c else "None")
    if c:
        chaps = conn.execute("SELECT id, day_number, title FROM course_chapters WHERE course_id = 11 ORDER BY day_number").fetchall()
        print("Chapters count:", len(chaps))
        for ch in chaps[:3]:
            subs = conn.execute("SELECT id, sort_order, title, brief FROM course_subtopics WHERE chapter_id = ? ORDER BY sort_order", (ch['id'],)).fetchall()
            print(f"  Day {ch['day_number']}: {ch['title']}")
            for s in subs:
                print(f"    - Subtopic ID {s['id']}: {s['title']}")
