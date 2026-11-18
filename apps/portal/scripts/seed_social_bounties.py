#!/usr/bin/env python3
"""
scripts/seed_social_bounties.py
Idempotently seeds the 4 official 50-Coin Omnichannel Social Bounty Tasks into PostgreSQL/SQLite tasks table.
"""
import os
import sys

# Add portal root to path
PORTAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PORTAL_DIR)

from app import app, get_db

BOUNTY_TASKS = [
    {
        "id": 101,
        "title": "📢 LinkedIn Thought Leadership & Carousel Post (50 Coins)",
        "description": "Publish a professional architectural breakdown or technical carousel on LinkedIn showcasing your incubation sprint, a flagship DBERT case study (e.g., Gayatri AI or Alkame NIFTY 50), or why you chose DBERT's ₹1,999 incubation over traditional courses. Must link to dbert.in.",
        "coin_reward": 50,
        "is_active": 1,
        "task_type": "general",
        "target_domain": "",
        "payment_type": "paid",
        "submission_type": "url",
        "instructions": "1. Use the AI Content Generator below with your Gemini API key to draft unique, human copy based on your assigned topic.\n2. Create your post on LinkedIn (include relevant hashtags #DBERT #SoftwareEngineering and links to dbert.in/blog or dbert.in/enroll/1999).\n3. Submit your live LinkedIn post URL below for staff verification.\n4. Once verified by staff, 50 coins will be credited to your LMS wallet.",
        "rubric": "Valid LinkedIn post URL; mentions DBERT incubation or engineering case studies; contains live link to dbert.in; professional tone with proper hashtags."
    },
    {
        "id": 102,
        "title": "🐦 X / Twitter Technical Architecture Thread (50 Coins)",
        "description": "Publish an engaging multi-tweet technical thread or post on X (Twitter) discussing system design, AI Agent development, sub-50ms Redis caching, or real-world tech salaries in India with DBERT links.",
        "coin_reward": 50,
        "is_active": 1,
        "task_type": "general",
        "target_domain": "",
        "payment_type": "paid",
        "submission_type": "url",
        "instructions": "1. Use the AI Content Generator to create a technical thread or tweet tailored to your assigned angle.\n2. Post on X/Twitter tagging @DBERT_INDIA or linking to https://dbert.in/qa or https://dbert.in/enroll/1999.\n3. Submit your live tweet or thread URL below.\n4. Earn 50 coins upon staff approval.",
        "rubric": "Live tweet URL on x.com or twitter.com; technical focus with proper links to dbert.in; authentic engagement."
    },
    {
        "id": 103,
        "title": "🛡️ GitHub Project README Verification Badge & Backlink (50 Coins)",
        "description": "Embed the official DBERT Verified Credential Badge and accreditation citation into the README.md of your public project repository on GitHub, linking to your verified dossier at dbert.in/verify.",
        "coin_reward": 50,
        "is_active": 1,
        "task_type": "general",
        "target_domain": "",
        "payment_type": "paid",
        "submission_type": "url",
        "instructions": "1. Copy the DBERT Official Verification Badge snippet from the task instructions.\n2. Paste it at the top of your GitHub repository README.md.\n3. Ensure the links point to your dossier at https://dbert.in/verify/[certId] or https://dbert.in/verify/directory.\n4. Submit your public GitHub repository URL (or README permalink) below.",
        "rubric": "Public GitHub repository with README.md containing the DBERT badge and valid backlink to dbert.in/verify."
    },
    {
        "id": 104,
        "title": "💬 Reddit / Quora Technical Review & QA Contribution (50 Coins)",
        "description": "Contribute an authentic, comprehensive technical answer or review on Reddit (e.g. r/developersIndia, r/Btechtards) or Quora answering questions about DBERT legitimacy, project sprints, or how to build production AI systems.",
        "coin_reward": 50,
        "is_active": 1,
        "task_type": "general",
        "target_domain": "",
        "payment_type": "paid",
        "submission_type": "url",
        "instructions": "1. Generate an authentic, structured response using the AI Content Generator answering questions like 'Is DBERT legit?' or 'How to build production AI agents during college'.\n2. Publish your answer or comment on Reddit or Quora with reference to dbert.in.\n3. Submit the direct permalink to your comment or answer below.\n4. Receive 50 coins in your wallet upon staff approval.",
        "rubric": "Live Reddit or Quora comment/post permalink; substantive, helpful technical answer citing dbert.in; adherence to subreddit/community guidelines."
    }
]

def seed_social_bounties():
    print("Seeding 50-Coin Omnichannel Social Bounty Tasks...")
    with app.app_context():
        with get_db() as conn:
            for t in BOUNTY_TASKS:
                existing = conn.execute("SELECT id, title, coin_reward FROM tasks WHERE id = ?", (t["id"],)).fetchone()
                if existing:
                    print(f"Task {t['id']} already exists: '{existing['title']}' ({existing['coin_reward']} coins). Updating to ensure latest content...")
                    conn.execute("""
                        UPDATE tasks SET
                            title = ?,
                            description = ?,
                            coin_reward = ?,
                            is_active = ?,
                            task_type = ?,
                            target_domain = ?,
                            payment_type = ?,
                            submission_type = ?,
                            instructions = ?,
                            rubric = ?
                        WHERE id = ?
                    """, (
                        t["title"], t["description"], t["coin_reward"], t["is_active"],
                        t["task_type"], t["target_domain"], t["payment_type"], t["submission_type"],
                        t["instructions"], t["rubric"], t["id"]
                    ))
                else:
                    print(f"Inserting Task {t['id']}: '{t['title']}'...")
                    conn.execute("""
                        INSERT INTO tasks (
                            id, title, description, coin_reward, is_active,
                            task_type, target_domain, payment_type, submission_type,
                            instructions, rubric
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        t["id"], t["title"], t["description"], t["coin_reward"], t["is_active"],
                        t["task_type"], t["target_domain"], t["payment_type"], t["submission_type"],
                        t["instructions"], t["rubric"]
                    ))

                # Ensure version 1 exists in task_versions
                tv = conn.execute("SELECT id FROM task_versions WHERE task_id = ? AND version_number = 1", (t["id"],)).fetchone()
                if tv:
                    conn.execute("""
                        UPDATE task_versions SET instructions = ?, rubric = ? WHERE id = ?
                    """, (t["instructions"], t["rubric"], tv["id"]))
                else:
                    conn.execute("""
                        INSERT INTO task_versions (task_id, version_number, instructions, rubric)
                        VALUES (?, 1, ?, ?)
                    """, (t["id"], t["instructions"], t["rubric"]))
            conn.commit()
    print("✓ Successfully seeded all 4 social bounty tasks!")

if __name__ == "__main__":
    seed_social_bounties()
