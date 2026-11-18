import subprocess
import json

SSH_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
HOST = "ubuntu@3.26.237.171"

remote_script = """
import os, sys, json
from datetime import datetime
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import get_db, _sync_published_articles_registry, _post_slugify

# 1. IDs to delete from queue (Duplicates & Invalid raw diffs)
DELETE_IDS = [6, 9, 42, 43, 44, 45]

# 2. Articles to publish with correct formatting
PUBLISH_SPECS = [
    {
        "id": 2,
        "title": "Exploratory Data Analysis: Understanding Data Before Making Decisions",
        "domain": "Data Analyst",
        "slug": "exploratory-data-analysis-understanding-data-before-making-d",
        "feedback": "Approved by Editorial Board & Technical Council. Live on dbert.in/blog."
    },
    {
        "id": 3,
        "title": "AI in Engineering: From Design Tools to Autonomous Systems",
        "domain": "AI Agent Development",
        "slug": "ai-in-engineering-from-design-tools-to-autonomous-systems",
        "feedback": "Approved by Editorial Board & Technical Council. Live on dbert.in/blog."
    },
    {
        "id": 5,
        "title": "The Importance of Data Cleaning in Data Analytics Pipelines",
        "domain": "Data Analyst",
        "slug": "importance-of-data-cleaning-in-data-analytics-pipelines",
        "feedback": "Approved by Editorial Board & Technical Council. Live on dbert.in/blog."
    },
    {
        "id": 7,
        "title": "Physical AI: When Artificial Intelligence Enters the Physical World",
        "domain": "AI Agent Development",
        "slug": "physical-ai-when-artificial-intelligence-enters-the-physical",
        "feedback": "Approved by Editorial Board & Technical Council. Live on dbert.in/blog."
    },
    {
        "id": 8,
        "title": "The Strategic Role of Data Analytics in Modern Enterprise",
        "domain": "Data Analyst",
        "slug": "strategic-role-of-data-analytics-in-modern-enterprise",
        "feedback": "Approved by Editorial Board & Technical Council. Live on dbert.in/blog."
    },
    {
        "id": 10,
        "title": "How Hadoop MapReduce Actually Works: An Engineering Architecture Breakdown",
        "domain": "Data Analyst",
        "slug": "how-hadoop-mapreduce-actually-works-engineering-breakdown",
        "feedback": "Approved by Editorial Board & Technical Council. Live on dbert.in/blog."
    },
    {
        "id": 40,
        "title": "Alkame NIFTY 50: Quantitative Market Intelligence & Educational Analytics Platform",
        "domain": "Data Analyst",
        "slug": "alkame-nifty-50-quantitative-market-intelligence-platform",
        "feedback": "Capstone Project Case Study verified & approved. Live on dbert.in/blog."
    },
    {
        "id": 46,
        "title": "Building a NEET Question Ingestion and Semantic Validation Pipeline: From Raw CSVs to Model-Ready MCQs",
        "domain": "Data Analyst",
        "slug": "building-a-neet-question-ingestion-and-semantic-validation-p",
        "feedback": "High-merit technical research paper approved by Editorial Council. Live on dbert.in/blog."
    },
    {
        "id": 47,
        "title": "Architecting Alkame: A Multi-Agent AI Quantitative Market Intelligence Platform",
        "domain": "AI Agent Development",
        "slug": "architecting-alkame-a-multi-agent-ai-quantitative-market-inte",
        "feedback": "Capstone Project Case Study verified & approved. Live on dbert.in/blog."
    }
]

with get_db() as conn:
    print("=== 1. DELETING DUPLICATE & INVALID ARTICLES FROM QUEUE ===")
    for del_id in DELETE_IDS:
        cur = conn.execute("SELECT id, title, intern_id, status FROM intern_articles WHERE id = ?", (del_id,)).fetchone()
        if cur:
            conn.execute("DELETE FROM intern_articles WHERE id = ?", (del_id,))
            print(f"  ✓ Deleted Article ID {del_id}: '{cur['title'][:50]}' (Status: {cur['status']})")
        else:
            print(f"  - Article ID {del_id} not found (already deleted)")

    print("\\n=== 2. FORMATTING & PUBLISHING APPROVED NON-DUPLICATE ARTICLES ===")
    now_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for spec in PUBLISH_SPECS:
        aid = spec["id"]
        title = spec["title"]
        domain = spec["domain"]
        slug = spec["slug"]
        pub_url = f"https://dbert.in/blog/{slug}"
        feedback = spec["feedback"]

        cur = conn.execute("SELECT id, title, content_markdown FROM intern_articles WHERE id = ?", (aid,)).fetchone()
        if cur:
            # Clean content markdown headings if needed
            content = cur["content_markdown"] or ""
            if not content.startswith("#"):
                content = f"# {title}\\n\\n" + content
            
            conn.execute(
                "UPDATE intern_articles SET title = ?, domain = ?, status = 'PUBLISHED', published_url = ?, mentor_feedback = ?, content_markdown = ?, updated_at = ? WHERE id = ?",
                (title, domain, pub_url, feedback, content, now_ts, aid)
            )
            print(f"  ✓ Published ID {aid}: '{title[:55]}...' -> {pub_url}")
        else:
            print(f"  ! Article ID {aid} not found")

    conn.commit()

    print("\\n=== 3. SYNCHRONIZING PUBLISHED ARTICLES REGISTRY ===")
    _sync_published_articles_registry(conn)
    print("  ✓ Synced published articles to data/published_articles.json and apps/website/src/data/published_articles.json")

    # Audit final state
    rem_pending = conn.execute("SELECT COUNT(*) as c FROM intern_articles WHERE status = 'PENDING_REVIEW'").fetchone()["c"]
    total_pub = conn.execute("SELECT COUNT(*) as c FROM intern_articles WHERE status = 'PUBLISHED'").fetchone()["c"]
    print(f"\\n=== FINAL AUDIT: Remaining in Queue: {rem_pending} | Total Published: {total_pub} ===")
"""

print("Executing article review, deduplication and publication on EC2...")
cmd = ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", HOST, f"cat << 'EOF' > /tmp/process_articles.py\n{remote_script}\nEOF\n/var/www/dbert-website-lms/apps/portal/.venv/bin/python /tmp/process_articles.py"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("STDOUT:\n", res.stdout)
if res.stderr:
    print("STDERR:\n", res.stderr)
