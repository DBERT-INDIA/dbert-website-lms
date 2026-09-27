#!/usr/bin/env python3
import os
import json
import psycopg2

def main():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        print("Please export DATABASE_URL first.")
        return
        
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    schema = os.environ.get("POSTGRES_SCHEMA", "dbert_internship")
    cur.execute(f"SET search_path TO {schema}, public")

    cur.execute("SELECT id, title FROM courses")
    courses = {row[1]: row[0] for row in cur.fetchall()}
    
    if not courses:
        print("No courses found!")
        return

    # Curriculum definitions
    curricula = {
        "Data Analytics Accelerated: Practical EDA, SQL & Business Intelligence": [
            ("Day 1: SQL Foundations & Data Extraction", [
                ("Advanced SELECT & Filtering", "Master complex WHERE clauses and text matching.", ["Write complex filters", "Handle NULLs"]),
                ("Joins & Aggregations", "Combine tables and group data effectively.", ["Master INNER/LEFT/OUTER JOINs", "Use GROUP BY & HAVING"])
            ]),
            ("Day 2: Exploratory Data Analysis (EDA) in Python", [
                ("Pandas Basics", "Load, clean, and inspect dataframes.", ["Import CSV/SQL data", "Handle missing values"]),
                ("Data Visualization", "Create charts with Matplotlib & Seaborn.", ["Plot distributions", "Visualize correlations"])
            ]),
            ("Day 3: Business Intelligence & Dashboards", [
                ("Dashboard Design", "Principles of effective BI reporting.", ["Define KPIs", "Design layout"]),
                ("Capstone: Final Report", "Build an interactive dashboard.", ["Connect data source", "Publish dashboard"])
            ])
        ],
        "Applied AI Agents: Production RAG, Tool Calling & Multi-Agent Orchestration": [
            ("Day 1: LLM Fundamentals & Prompt Engineering", [
                ("API Integration", "Connect to OpenAI/Anthropic APIs.", ["Manage API keys", "Format requests/responses"]),
                ("Advanced Prompting", "Zero-shot, few-shot, and Chain of Thought.", ["Design robust prompts", "Control outputs"])
            ]),
            ("Day 2: Retrieval-Augmented Generation (RAG)", [
                ("Vector Databases", "Store and query embeddings.", ["Generate embeddings", "Perform similarity search"]),
                ("Building RAG", "Combine retrieval with generation.", ["Chunk documents", "Inject context into prompts"])
            ]),
            ("Day 3: Agents & Tool Calling", [
                ("Function Calling", "Allow LLMs to execute code.", ["Define JSON schemas", "Handle tool execution"]),
                ("Multi-Agent Systems", "Orchestrate multiple agents.", ["Define agent roles", "Manage agent memory"])
            ])
        ],
        "Full Stack Web Application Engineering": [
             ("Day 1: Frontend Fundamentals (React/Vue)", [
                ("Component Architecture", "Build reusable UI components.", ["Manage state", "Pass props"]),
                ("Routing & Navigation", "Implement single-page routing.", ["Set up router", "Handle URL parameters"])
            ]),
            ("Day 2: Backend API Development (Node/Python)", [
                ("RESTful Design", "Create structured API endpoints.", ["Handle GET/POST/PUT/DELETE", "Validate inputs"]),
                ("Database Integration", "Connect API to Postgres/MongoDB.", ["Write queries/ORM", "Manage migrations"])
            ]),
            ("Day 3: Authentication & Deployment", [
                ("JWT & Security", "Secure your application.", ["Implement login/signup", "Protect routes"]),
                ("Cloud Deployment", "Host your full stack app.", ["Deploy frontend", "Provision backend & DB"])
            ])
        ],
        "Python Automation, Scripting & ETL Pipelines": [
            ("Day 1: Core Scripting & OS Interactions", [
                ("File System Automation", "Read, write, and organize files.", ["Use pathlib/os", "Parse JSON/CSV"]),
                ("Task Scheduling", "Run scripts automatically.", ["Use cron/Task Scheduler", "Handle logging"])
            ]),
            ("Day 2: Web Scraping & API Consumption", [
                ("Requests & BeautifulSoup", "Extract data from the web.", ["Send HTTP requests", "Parse HTML DOM"]),
                ("Handling APIs", "Consume REST and GraphQL APIs.", ["Handle authentication", "Parse complex JSON"])
            ]),
            ("Day 3: Building ETL Pipelines", [
                ("Extract & Transform", "Cleanse and shape data.", ["Standardize formats", "Handle edge cases"]),
                ("Load & Notify", "Push data to DB and send alerts.", ["Bulk insert to SQL", "Send email/Slack alerts"])
            ])
        ],
        "Full Stack Web Development: Modern Architecture, REST APIs & Cloud Deployment": [
             ("Day 1: Frontend Fundamentals (React/Vue)", [
                ("Component Architecture", "Build reusable UI components.", ["Manage state", "Pass props"]),
                ("Routing & Navigation", "Implement single-page routing.", ["Set up router", "Handle URL parameters"])
            ]),
            ("Day 2: Backend API Development (Node/Python)", [
                ("RESTful Design", "Create structured API endpoints.", ["Handle GET/POST/PUT/DELETE", "Validate inputs"]),
                ("Database Integration", "Connect API to Postgres/MongoDB.", ["Write queries/ORM", "Manage migrations"])
            ]),
            ("Day 3: Authentication & Deployment", [
                ("JWT & Security", "Secure your application.", ["Implement login/signup", "Protect routes"]),
                ("Cloud Deployment", "Host your full stack app.", ["Deploy frontend", "Provision backend & DB"])
            ])
        ],
        "Python Automation & Web Scraping: Production Pipelines & Cloud Daemons": [
             ("Day 1: Core Scripting & OS Interactions", [
                ("File System Automation", "Read, write, and organize files.", ["Use pathlib/os", "Parse JSON/CSV"]),
                ("Task Scheduling", "Run scripts automatically.", ["Use cron/Task Scheduler", "Handle logging"])
            ]),
            ("Day 2: Web Scraping & API Consumption", [
                ("Requests & BeautifulSoup", "Extract data from the web.", ["Send HTTP requests", "Parse HTML DOM"]),
                ("Handling APIs", "Consume REST and GraphQL APIs.", ["Handle authentication", "Parse complex JSON"])
            ]),
            ("Day 3: Building ETL Pipelines", [
                ("Extract & Transform", "Cleanse and shape data.", ["Standardize formats", "Handle edge cases"]),
                ("Load & Notify", "Push data to DB and send alerts.", ["Bulk insert to SQL", "Send email/Slack alerts"])
            ])
        ],
        "Test Course": [
             ("Day 1: Introduction", [
                ("Welcome", "Getting started with the course.", ["Login", "Navigate portal"]),
            ]),
            ("Day 2: Advanced Topics", [
                ("Deep Dive", "Exploring complex subjects.", ["Read docs", "Take quiz"]),
            ])
        ]
    }

    # Clear existing to be safe
    cur.execute("DELETE FROM course_subtopics")
    cur.execute("DELETE FROM course_chapters")
    
    total_chapters = 0
    total_subtopics = 0
    
    for title, course_id in courses.items():
        if title in curricula:
            chapters = curricula[title]
            for day_idx, (chapter_title, subtopics) in enumerate(chapters, 1):
                cur.execute(
                    "INSERT INTO course_chapters (course_id, day_number, title) VALUES (%s, %s, %s) RETURNING id",
                    (course_id, day_idx, chapter_title)
                )
                chapter_id = cur.fetchone()[0]
                total_chapters += 1
                
                for sub_idx, (sub_title, sub_brief, takeaways) in enumerate(subtopics, 1):
                    cur.execute(
                        "INSERT INTO course_subtopics (chapter_id, sort_order, title, brief, key_takeaways_json) VALUES (%s, %s, %s, %s, %s)",
                        (chapter_id, sub_idx, sub_title, sub_brief, json.dumps(takeaways))
                    )
                    total_subtopics += 1

    conn.commit()
    print(f"Successfully seeded {total_chapters} chapters and {total_subtopics} subtopics!")

if __name__ == "__main__":
    main()
