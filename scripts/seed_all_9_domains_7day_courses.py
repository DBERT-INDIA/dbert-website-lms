"""
DBERT LMS - Seeding & Verification Daemon for All 9 Platform Domain 7-Day Courses
================================================================================
Idempotent script to seed complete 7-day courses (Days 1–7), chapters, subtopics,
and daily quizzes for all 9 official platform domains.
Compatible with both local SQLite and production EC2 PostgreSQL.
================================================================================
"""

import sys
import os
import json

# Ensure portal path is available
PORTAL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal"))
if PORTAL_PATH not in sys.path:
    sys.path.insert(0, PORTAL_PATH)

from app import get_db, VALID_DOMAINS
from config.courses_7day_catalog import ALL_9_DOMAIN_COURSES


def seed_all_courses():
    print(f"=== Starting 7-Day Course Seeding for All {len(ALL_9_DOMAIN_COURSES)} Domains ===")
    
    with get_db() as conn:
        courses_created = 0
        chapters_created = 0
        subtopics_created = 0
        quizzes_created = 0

        for dc in ALL_9_DOMAIN_COURSES:
            domain = dc["domain"]
            title = dc["title"]
            slug = dc["slug"]
            level = dc.get("level") or "Beginner"
            hours = dc.get("estimated_hours") or 14
            gradient = dc.get("banner_gradient") or "linear-gradient(135deg, #1e293b 0%, #334155 100%)"

            # Check if active course exists for domain
            course_row = conn.execute(
                "SELECT id, title FROM courses WHERE domain = ? AND is_active = 1 LIMIT 1",
                (domain,)
            ).fetchone()

            if course_row:
                cid = course_row["id"]
                print(f"[*] Found existing course for [{domain}]: ID {cid} - '{course_row['title']}'")
            else:
                conn.execute("""
                    INSERT INTO courses
                    (title, slug, domain, is_paid, price_inr, content_status, source, is_active,
                     level, estimated_hours, banner_gradient, created_at, updated_at)
                    VALUES (?, ?, ?, 0, 0, 'approved', 'custom', 1, ?, ?, ?, datetime('now','localtime'), datetime('now','localtime'))
                """, (title, slug, domain, level, hours, gradient))
                
                course_row = conn.execute(
                    "SELECT id, title FROM courses WHERE domain = ? AND is_active = 1 LIMIT 1",
                    (domain,)
                ).fetchone()
                cid = course_row["id"]
                courses_created += 1
                print(f"[+] Created NEW course for [{domain}]: ID {cid} - '{title}'")

            # Seed chapters (Days 1–7)
            for ch in dc["chapters"]:
                day_num = ch["day_number"]
                ch_title = ch["title"]

                ch_row = conn.execute(
                    "SELECT id, title FROM course_chapters WHERE course_id = ? AND day_number = ? LIMIT 1",
                    (cid, day_num)
                ).fetchone()

                if ch_row:
                    ch_id = ch_row["id"]
                else:
                    conn.execute(
                        "INSERT INTO course_chapters (course_id, day_number, title) VALUES (?, ?, ?)",
                        (cid, day_num, ch_title)
                    )
                    ch_row = conn.execute(
                        "SELECT id, title FROM course_chapters WHERE course_id = ? AND day_number = ? LIMIT 1",
                        (cid, day_num)
                    ).fetchone()
                    ch_id = ch_row["id"]
                    chapters_created += 1

                # Subtopics
                sub_count_row = conn.execute(
                    "SELECT COUNT(*) FROM course_subtopics WHERE chapter_id = ?",
                    (ch_id,)
                ).fetchone()
                sub_count = sub_count_row[0] if sub_count_row else 0

                if sub_count == 0:
                    for sort_idx, (st_title, st_brief, st_takeaways) in enumerate(ch["subtopics"], start=1):
                        takes_json = json.dumps(st_takeaways) if isinstance(st_takeaways, list) else str(st_takeaways)
                        conn.execute("""
                            INSERT INTO course_subtopics (chapter_id, sort_order, title, brief, key_takeaways_json)
                            VALUES (?, ?, ?, ?, ?)
                        """, (ch_id, sort_idx, st_title, st_brief, takes_json))
                        subtopics_created += 1

                # Quizzes
                quiz_row = conn.execute(
                    "SELECT id FROM course_day_quizzes WHERE course_id = ? AND day_number = ? LIMIT 1",
                    (cid, day_num)
                ).fetchone()

                if not quiz_row and ch.get("quiz"):
                    conn.execute("""
                        INSERT INTO course_day_quizzes (course_id, day_number, questions_json)
                        VALUES (?, ?, ?)
                    """, (cid, day_num, json.dumps(ch["quiz"])))
                    quizzes_created += 1

        conn.commit()

        print("\n=== Seeding Execution Summary ===")
        print(f"Courses Created:   {courses_created}")
        print(f"Chapters Created:  {chapters_created}")
        print(f"Subtopics Created: {subtopics_created}")
        print(f"Quizzes Created:   {quizzes_created}")

        # Verification Audit across all 9 VALID_DOMAINS
        print("\n=== Auditing All 9 Platform Domains ===")
        all_ok = True
        for vd in VALID_DOMAINS:
            c = conn.execute("SELECT id, title, domain FROM courses WHERE domain = ? AND is_active = 1 LIMIT 1", (vd,)).fetchone()
            if not c:
                print(f"[FAIL] Domain '{vd}' has NO active course!")
                all_ok = False
                continue
            
            chapters = conn.execute(
                "SELECT id, day_number, title FROM course_chapters WHERE course_id = ? ORDER BY day_number",
                (c["id"],)
            ).fetchall()
            day_nums = [row["day_number"] for row in chapters]
            
            sub_count = 0
            for row in chapters:
                sc = conn.execute("SELECT COUNT(*) FROM course_subtopics WHERE chapter_id = ?", (row["id"],)).fetchone()[0]
                sub_count += sc

            quizzes = conn.execute("SELECT day_number FROM course_day_quizzes WHERE course_id = ?", (c["id"],)).fetchall()
            q_days = [q["day_number"] for q in quizzes]

            status = "OK" if len(day_nums) == 7 and sub_count >= 14 and len(q_days) == 7 else "INCOMPLETE"
            if status != "OK":
                all_ok = False

            print(f"[{status}] [{vd}] Course ID {c['id']}: {len(day_nums)}/7 Days, {sub_count} Subtopics, {len(q_days)}/7 Quizzes")

        if all_ok:
            print("\n[SUCCESS] All 9 Platform Domains have 100% complete 7-Day Curricula!")
        else:
            print("\n[WARNING] Some domains are incomplete!")

    return all_ok


if __name__ == "__main__":
    success = seed_all_courses()
    sys.exit(0 if success else 1)
