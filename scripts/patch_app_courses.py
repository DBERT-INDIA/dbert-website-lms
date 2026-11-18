with open("apps/portal/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Replace the hardcoded course dictionaries with imports from config.courses_7day_catalog
start_marker = "PLATFORM_DOMAIN_COURSES = ["
end_marker = "ALL_DOMAIN_COURSES = PLATFORM_DOMAIN_COURSES + DOMAIN_COURSES_METADATA"

s_idx = content.find(start_marker)
e_idx = content.find(end_marker)
assert s_idx != -1 and e_idx != -1, "Course dictionary markers not found in app.py"
e_idx += len(end_marker)

catalog_import_block = """from config.courses_7day_catalog import (
    EXISTING_4_DOMAIN_COURSES,
    NEW_7DAY_DOMAIN_COURSES,
    ALL_9_DOMAIN_COURSES,
)

PLATFORM_DOMAIN_COURSES = EXISTING_4_DOMAIN_COURSES
DOMAIN_COURSES_METADATA = NEW_7DAY_DOMAIN_COURSES
ALL_DOMAIN_COURSES = ALL_9_DOMAIN_COURSES"""

content = content[:s_idx] + catalog_import_block + content[e_idx:]

# 2. Update the seeding loop in init_db to seed ALL_DOMAIN_COURSES and avoid relying on cur.lastrowid
old_loop = """        # ── Seed 4 Platform Domain Courses, Chapters, Subtopics, and Quizzes ──
        for dc in PLATFORM_DOMAIN_COURSES:
            existing_course = conn.execute(
                "SELECT id FROM courses WHERE domain=? AND is_active=1 LIMIT 1", (dc["domain"],)
            ).fetchone()
            if existing_course:
                cid = existing_course["id"]
            else:
                cur = conn.execute(\"\"\"
                    INSERT INTO courses
                    (title, slug, domain, is_paid, price_inr, content_status, source, is_active,
                     level, estimated_hours, banner_gradient, created_at, updated_at)
                    VALUES (?, ?, ?, 0, 0, 'approved', 'custom', 1, ?, ?, ?, datetime('now','localtime'), datetime('now','localtime'))
                \"\"\", (dc["title"], dc["slug"], dc["domain"], dc["level"], dc["estimated_hours"], dc["banner_gradient"]))
                cid = cur.lastrowid

            # Seed chapters, subtopics, and quizzes for this domain course
            for ch in dc["chapters"]:
                day_num = ch["day_number"]
                ch_row = conn.execute(
                    "SELECT id FROM course_chapters WHERE course_id=? AND day_number=? LIMIT 1",
                    (cid, day_num)
                ).fetchone()
                if ch_row:
                    ch_id = ch_row["id"]
                else:
                    cur_ch = conn.execute(
                        "INSERT INTO course_chapters (course_id, day_number, title) VALUES (?, ?, ?)",
                        (cid, day_num, ch["title"])
                    )
                    ch_id = cur_ch.lastrowid

                # Subtopics
                subtopic_count = conn.execute(
                    "SELECT COUNT(*) FROM course_subtopics WHERE chapter_id=?", (ch_id,)
                ).fetchone()[0]
                if subtopic_count == 0:
                    for sort_idx, (st_title, st_brief, st_takeaways) in enumerate(ch["subtopics"], start=1):
                        conn.execute(\"\"\"
                            INSERT INTO course_subtopics (chapter_id, sort_order, title, brief, key_takeaways_json)
                            VALUES (?, ?, ?, ?, ?)
                        \"\"\", (ch_id, sort_idx, st_title, st_brief, json.dumps(st_takeaways)))

                # Quizzes
                quiz_row = conn.execute(
                    "SELECT id FROM course_day_quizzes WHERE course_id=? AND day_number=? LIMIT 1",
                    (cid, day_num)
                ).fetchone()
                if not quiz_row and ch.get("quiz"):
                    conn.execute(\"\"\"
                        INSERT INTO course_day_quizzes (course_id, day_number, questions_json)
                        VALUES (?, ?, ?)
                    \"\"\", (cid, day_num, json.dumps(ch["quiz"])))\n"""

new_loop = """        # ── Seed All 9 Platform Domain Courses, Chapters, Subtopics, and Quizzes ──
        for dc in ALL_DOMAIN_COURSES:
            existing_course = conn.execute(
                "SELECT id FROM courses WHERE domain=? AND is_active=1 LIMIT 1", (dc["domain"],)
            ).fetchone()
            if existing_course:
                cid = existing_course["id"]
            else:
                conn.execute(\"\"\"
                    INSERT INTO courses
                    (title, slug, domain, is_paid, price_inr, content_status, source, is_active,
                     level, estimated_hours, banner_gradient, created_at, updated_at)
                    VALUES (?, ?, ?, 0, 0, 'approved', 'custom', 1, ?, ?, ?, datetime('now','localtime'), datetime('now','localtime'))
                \"\"\", (dc["title"], dc["slug"], dc["domain"], dc["level"], dc["estimated_hours"], dc["banner_gradient"]))
                course_row = conn.execute(
                    "SELECT id FROM courses WHERE domain=? AND is_active=1 LIMIT 1", (dc["domain"],)
                ).fetchone()
                cid = course_row["id"] if course_row else None

            if not cid:
                continue

            # Seed chapters, subtopics, and quizzes for this domain course
            for ch in dc["chapters"]:
                day_num = ch["day_number"]
                ch_row = conn.execute(
                    "SELECT id FROM course_chapters WHERE course_id=? AND day_number=? LIMIT 1",
                    (cid, day_num)
                ).fetchone()
                if ch_row:
                    ch_id = ch_row["id"]
                else:
                    conn.execute(
                        "INSERT INTO course_chapters (course_id, day_number, title) VALUES (?, ?, ?)",
                        (cid, day_num, ch["title"])
                    )
                    new_ch = conn.execute(
                        "SELECT id FROM course_chapters WHERE course_id=? AND day_number=? LIMIT 1",
                        (cid, day_num)
                    ).fetchone()
                    ch_id = new_ch["id"] if new_ch else None

                if not ch_id:
                    continue

                # Subtopics
                subtopic_count = conn.execute(
                    "SELECT COUNT(*) FROM course_subtopics WHERE chapter_id=?", (ch_id,)
                ).fetchone()[0]
                if subtopic_count == 0:
                    for sort_idx, (st_title, st_brief, st_takeaways) in enumerate(ch["subtopics"], start=1):
                        conn.execute(\"\"\"
                            INSERT INTO course_subtopics (chapter_id, sort_order, title, brief, key_takeaways_json)
                            VALUES (?, ?, ?, ?, ?)
                        \"\"\", (ch_id, sort_idx, st_title, st_brief, json.dumps(st_takeaways)))

                # Quizzes
                quiz_row = conn.execute(
                    "SELECT id FROM course_day_quizzes WHERE course_id=? AND day_number=? LIMIT 1",
                    (cid, day_num)
                ).fetchone()
                if not quiz_row and ch.get("quiz"):
                    conn.execute(\"\"\"
                        INSERT INTO course_day_quizzes (course_id, day_number, questions_json)
                        VALUES (?, ?, ?)
                    \"\"\", (cid, day_num, json.dumps(ch["quiz"])))\n"""

assert old_loop in content, "old_loop not found in content"
content = content.replace(old_loop, new_loop, 1)

with open("apps/portal/app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully patched apps/portal/app.py!")
