"""
scripts/migrate_stipend_schema_and_tasks.py
Idempotent database migration script for Stipend Contribution and AI Pre-screening schema.
Ensures columns on task_submissions and seeds 4 standard domain stipend milestone tasks (5,000 coins).
"""
import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "portal")))

from app import get_db, ensure_column

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("stipend_migration")

STIPEND_TASKS = [
    {
        "title": "AI & Machine Learning Capstone Contribution",
        "description": "Submit your completed AI Agent pipeline, production model deployment, or enterprise LLM integration along with GitHub source repository, live deployment URL, and comprehensive Technical Report PDF.",
        "target_domain": "AI & Machine Learning",
        "coin_reward": 5000,
        "instructions": "Ensure your repository includes requirements.txt/Dockerfile, README with deployment steps, model evaluation metrics, and sample inference logs.",
        "rubric": "Code Architecture (25pts), Documentation & Metrics (25pts), Deployment/Inference (25pts), Originality & Domain Impact (25pts)"
    },
    {
        "title": "Data Analytics & Enterprise BI Dossier",
        "description": "Submit your end-to-end data pipeline, interactive BI dashboard, and analytical findings report along with GitHub repository, live dashboard link, and technical documentation PDF.",
        "target_domain": "Data Analyst",
        "coin_reward": 5000,
        "instructions": "Include SQL scripts or Jupyter notebooks, interactive PowerBI/Tableau/Streamlit dashboard link, and executive business summary PDF.",
        "rubric": "Data Wrangling & Pipeline (25pts), Visual Analytics & UI (25pts), Statistical Rigor & Insights (25pts), Technical Dossier Completeness (25pts)"
    },
    {
        "title": "Full Stack Production Web Application",
        "description": "Submit your production full stack web application featuring responsive frontend, RESTful/GraphQL APIs, database integration, and cloud deployment along with GitHub repo, live demo URL, and architectural PDF.",
        "target_domain": "Full Stack Web Development",
        "coin_reward": 5000,
        "instructions": "Repository must contain frontend and backend directories, clear environment setup guide, live deployed application URL, and architecture overview.",
        "rubric": "Frontend Quality & UX (25pts), Backend API & Database (25pts), Security & Authentication (25pts), Cloud Deployment & Demo (25pts)"
    },
    {
        "title": "Python Enterprise Automation Suite",
        "description": "Submit your enterprise RPA script, headless automation daemon, or robust data pipeline accompanied by GitHub repository, live execution demo / cloud log, and technical execution report PDF.",
        "target_domain": "Python Automation",
        "coin_reward": 5000,
        "instructions": "Demonstrate scheduled execution, robust exception recovery, logging, and an executive runbook outlining enterprise utility.",
        "rubric": "Automation Logic & Resilience (25pts), Error Recovery & Logging (25pts), Clean Code Architecture (25pts), Production Readiness & Runbook (25pts)"
    }
]


def run_migration():
    logger.info("Starting Stipend Schema Migration...")
    with get_db() as conn:
        # 1. Ensure platform_config table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS platform_config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TEXT
            )
        """)

        # 2. Ensure columns on task_submissions
        for col, defn in [
            ("github_repo_url", "TEXT DEFAULT ''"),
            ("live_demo_url", "TEXT DEFAULT ''"),
            ("report_file_url", "TEXT DEFAULT ''"),
            ("ai_evaluation_score", "INTEGER DEFAULT 0"),
            ("ai_evaluation_status", "TEXT DEFAULT 'pending'"),
            ("ai_evaluation_notes", "TEXT DEFAULT ''"),
            ("ai_evaluated_at", "TEXT DEFAULT ''"),
            ("task_category", "TEXT DEFAULT 'general'")
        ]:
            ensure_column(conn, "task_submissions", col, defn)
            logger.info(f"Ensured column task_submissions.{col}")

        # 3. Ensure columns on tasks
        for col, defn in [
            ("instructions", "TEXT DEFAULT ''"),
            ("rubric", "TEXT DEFAULT ''")
        ]:
            ensure_column(conn, "tasks", col, defn)
            logger.info(f"Ensured column tasks.{col}")

        # 4. Seed the 4 official domain stipend milestone tasks
        for task in STIPEND_TASKS:
            existing = conn.execute(
                "SELECT id FROM tasks WHERE task_type = 'stipend_milestone' AND LOWER(title) = LOWER(?)",
                (task["title"],)
            ).fetchone()

            if existing:
                conn.execute(
                    """
                    UPDATE tasks SET
                        description = ?,
                        target_domain = ?,
                        coin_reward = ?,
                        instructions = ?,
                        rubric = ?,
                        payment_type = 'paid',
                        is_active = 1
                    WHERE id = ?
                    """,
                    (task["description"], task["target_domain"], task["coin_reward"], task["instructions"], task["rubric"], existing["id"])
                )
                logger.info(f"Updated existing task: {task['title']} (ID: {existing['id']})")
            else:
                conn.execute(
                    """
                    INSERT INTO tasks (
                        title, description, coin_reward, is_active, author_type,
                        created_at, task_type, target_domain, payment_type, submission_type,
                        instructions, rubric
                    ) VALUES (
                        ?, ?, ?, 1, 'admin', datetime('now','localtime'),
                        'stipend_milestone', ?, 'paid', 'url', ?, ?
                    )
                    """,
                    (task["title"], task["description"], task["coin_reward"], task["target_domain"], task["instructions"], task["rubric"])
                )
                logger.info(f"Seeded new stipend milestone task: {task['title']}")

        conn.commit()

    logger.info("Stipend Schema Migration and Task Seeding completed successfully!")
    return True


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
