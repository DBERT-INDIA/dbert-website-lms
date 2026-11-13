"""
scripts/seed_mentor_slots.py
============================
Seeds active mentor staff accounts and upcoming Group Mentorship availability slots (14:00 – 20:15 IST)
with capacity of up to 30 interns per session across diverse domain tracks.
"""
import os
import sys
from datetime import datetime, timedelta

portal_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal"))
if portal_dir not in sys.path:
    sys.path.insert(0, portal_dir)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(portal_dir, ".env"))
except ImportError:
    pass

if "DATABASE_URL" not in os.environ:
    os.environ["TESTING"] = "1"
    os.environ["REQUIRE_POSTGRES"] = "false"

from app import app, get_db, set_password_hash

MENTORS = [
    {
        "name": "Abhinav Sharma",
        "email": "abhinav.sharma@dbert.in",
        "role": "staff",
        "specialty": "Principal AI Architect & Founder"
    },
    {
        "name": "Dr. Ananya Sen",
        "email": "ananya.sen@dbert.in",
        "role": "staff",
        "specialty": "Head of AI & Machine Learning"
    },
    {
        "name": "Rohan Kulkarni",
        "email": "rohan.kulkarni@dbert.in",
        "role": "staff",
        "specialty": "Senior Full-Stack & Systems Mentor"
    }
]

TOPICS_AND_TRACKS = [
    ("Data Analyst", "Capstone Project Architecture & Exploratory Data Analysis"),
    ("AI / Machine Learning", "Model Fine-Tuning, Embeddings & RAG Evaluation"),
    ("Full Stack Web Development", "Next.js SSR, Scalable API Design & Cloud Deployment"),
    ("Python Automation", "Production RPA, Playwright Automation & Workflow Reliability"),
    ("All Tracks", "Industry Technical Mentorship & Career Advisory"),
]

def seed_slots():
    with app.app_context():
        pwd_hash = set_password_hash("Password@123")
        with get_db() as conn:
            # 1. Seed Mentors into staff_accounts
            mentor_ids = []
            for m in MENTORS:
                conn.execute(
                    """
                    INSERT INTO staff_accounts (name, email, password_hash, is_active, role, created_at)
                    VALUES (?, ?, ?, 1, 'staff', datetime('now','localtime'))
                    ON CONFLICT(email) DO UPDATE SET
                        name = excluded.name,
                        password_hash = excluded.password_hash,
                        is_active = 1
                    """,
                    (m["name"], m["email"], pwd_hash)
                )
                m_row = conn.execute("SELECT id FROM staff_accounts WHERE email = ?", (m["email"],)).fetchone()
                mentor_ids.append((m_row["id"], m["name"]))

            print(f"[INFO] Mentors configured: {mentor_ids}")

            # 2. Ensure test interns have Accepted applications
            for em in ["kushal@dbert.in", "kushalagarwal27496@gmail.com", "deekshitha@dbert.in", "bhargavi13032007@gmail.com"]:
                app_exists = conn.execute("SELECT id FROM applications WHERE LOWER(email) = LOWER(?)", (em,)).fetchone()
                if app_exists:
                    conn.execute("UPDATE applications SET status = 'Accepted' WHERE id = ?", (app_exists["id"],))
                else:
                    conn.execute(
                        """
                        INSERT INTO applications (name, email, phone, city, college, course, semester, year_of_passing, domain, why_join, status, created_at)
                        VALUES (?, ?, '9876543201', 'New Delhi', 'Delhi University', 'B.Tech', '6', '2026', 'Data Analyst', 'Technical Excellence', 'Accepted', datetime('now','localtime'))
                        """,
                        ("Intern Student", em)
                    )

            # 3. Clean up unbooked slots
            conn.execute("DELETE FROM mentor_availability_slots WHERE seats_booked = 0")

            # 4. Generate slots spanning next 14 days (14:00 - 20:15 IST)
            base_date = datetime(2026, 11, 9).date()

            slot_times = [
                ("14:00", "14:45"),
                ("15:30", "16:15"),
                ("17:00", "17:45"),
                ("18:30", "19:15"),
                ("19:30", "20:15")
            ]

            created_count = 0
            for day_offset in range(0, 14):
                slot_date = base_date + timedelta(days=day_offset)
                date_str = slot_date.strftime("%Y-%m-%d")

                for i, (start_t, end_t) in enumerate(slot_times):
                    start_dt_str = f"{date_str} {start_t}:00"
                    end_dt_str = f"{date_str} {end_t}:00"

                    mentor_id, mentor_name = mentor_ids[(i + day_offset) % len(mentor_ids)]
                    domain, topic = TOPICS_AND_TRACKS[(i + day_offset * 2) % len(TOPICS_AND_TRACKS)]

                    # Seed varied seats_booked (e.g., 0, 8, 15, 28) for realistic capacity demonstration
                    simulated_seats = (i * 7 + day_offset * 3) % 25

                    conn.execute(
                        """
                        INSERT INTO mentor_availability_slots 
                        (mentor_staff_id, start_time, end_time, capacity, seats_booked, domain, topic, is_booked, created_at)
                        VALUES (?, ?, ?, 30, ?, ?, ?, 0, datetime('now','localtime'))
                        """,
                        (mentor_id, start_dt_str, end_dt_str, simulated_seats, domain, topic)
                    )
                    created_count += 1

            conn.commit()
            print(f"[SUCCESS] Seeded {created_count} active group mentor slots across {len(mentor_ids)} mentors over 14 days!")

if __name__ == "__main__":
    seed_slots()
