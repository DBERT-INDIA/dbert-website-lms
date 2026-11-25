"""Renew expiring/2026 posts to 2027 targets, unify /enroll/1999 funnel steering across all posts,
and seed 20 fresh 2027 multi-city posts across underrepresented & ML/GenAI tracks in PostgreSQL.

Designed to run on EC2 inside /var/www/dbert-website-lms/apps/portal (with .env loaded),
or triggered remotely by scripts/renew_posts_and_deploy_2027.py.
"""

import os
import re
import sys
import datetime
import psycopg2
from dotenv import load_dotenv

ENV_PATHS = [
    "/var/www/dbert-website-lms/apps/portal/.env",
    os.path.join(os.path.dirname(__file__), "..", "apps", "portal", ".env"),
]
for p in ENV_PATHS:
    if os.path.exists(p):
        load_dotenv(p)
        break

TARGET_PUBLISHED_AT = "2026-11-25 10:00:00"
TARGET_APPLY_BY = "2027-01-15"
TARGET_EXPIRES_AT = "2027-02-15 23:59:59"
TARGET_UPDATED_AT = "2026-11-25 22:55:00"

STEERING_ELIGIBILITY_BLOCK = (
    "TIERED FAST-TRACK PATHWAY (Certificate -> Stipend -> Placement):\n"
    "• Standard Track: Open to all applicants meeting core technical prerequisites.\n"
    "• Accelerated Fast-Track (Priority Shortlisting): Direct Round-1 screening waivers and expedited review "
    "are granted to fellows enrolled in the DBERT 8-Week Technical Incubation & Production Sprint Track "
    "(https://dbert.in/enroll/1999 — ₹1,999 total fee; ₹499 caution deposit credited in full, ₹1,500 net balance).\n"
    "• Value Ladder: (1) Cryptographic Turnitin-verified 3-Document Credential Packet -> "
    "(2) ₹5,000+ Stipend Unlock at Gate 1 (3 approved PRs + >=75% attendance) -> "
    "(3) 100% Guaranteed Production Internship & Dedicated Placement Assistance."
)

# 20 fresh 2027-targeted multi-city posts (5 each across AI Agent/ML, Mobile App, DevOps & Cloud, Cybersecurity/UI-UX)
# Strictly uses VALID_DOMAINS from apps/portal/app.py so every listing resolves cleanly on lms.dbert.in.
NEW_2027_POSTS = [
    # --- AI Agent Development (including ML / RAG / LoRA / vLLM roles across 5 hubs) ---
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "AI Agent Development",
        "title": "LangGraph Multi-Agent Orchestration Intern (Python / FastAPI) — Bengaluru 2027",
        "slug": "langgraph-multi-agent-orchestration-intern-bengaluru-2027",
        "location": "Bangalore",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "LangGraph, Python, FastAPI, Pydantic, PostgreSQL, pgvector, Docker",
        "description": (
            "Join DBERT Labs in Bengaluru / Remote to engineer stateful multi-agent orchestration workflows using LangGraph, "
            "deterministic tool-calling schemas, and human-in-the-loop approval checkpoints on live venture repositories. "
            "Fellows progress through our Certificate -> Stipend -> Placement ladder with senior PR reviews."
        ),
        "responsibilities": (
            "• Commit at least 10 hours/week with >=75% portal attendance and weekly sprint velocity.\n"
            "• Implement cyclical LangGraph state graphs with PostgreSQL checkpointing and fallback retries.\n"
            "• Enforce Pydantic tool-call validation and write automated PyTest integration harnesses.\n"
            "• Contribute 3+ approved pull requests to qualify for Gate 1 ₹5,000+ milestone stipend."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "AI Agent Development",
        "title": "PyTorch & QLoRA LLM Fine-Tuning Intern (ML / vLLM) — Mumbai 2027",
        "slug": "pytorch-qlora-llm-fine-tuning-intern-mumbai-2027",
        "location": "Mumbai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "PyTorch, Transformers, LoRA, QLoRA, vLLM, MLflow, Python, FastAPI",
        "description": (
            "Work with DBERT's applied ML engineering squad in Mumbai / Remote to prepare domain instruction datasets, "
            "execute QLoRA parameter-efficient fine-tuning on open-weights LLMs, and benchmark vLLM serving latency."
        ),
        "responsibilities": (
            "• Curate leakage-free evaluation datasets and benchmark baseline vs. fine-tuned perplexity.\n"
            "• Track training runs and quantized GGUF/AWQ artifacts reproducibly in MLflow.\n"
            "• Containerize FastAPI/vLLM inference endpoints with latency and drift checks.\n"
            "• Maintain >=75% attendance and ship 3+ approved production PRs."
        ),
    },
    {
        "company_id": 3,
        "post_type": "internship",
        "domain": "AI Agent Development",
        "title": "Hybrid RAG & Vector Search Intern (BM25 / pgvector / Reranking) — Delhi NCR 2027",
        "slug": "hybrid-rag-vector-search-intern-delhi-ncr-2027",
        "location": "Delhi NCR",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "RAG, pgvector, BM25, LangChain, FastAPI, Cross-Encoder, Python, PostgreSQL",
        "description": (
            "Join Gayatri AI in Delhi NCR / Remote to build production Hybrid RAG retrieval pipelines combining "
            "PostgreSQL tsvector BM25 search, pgvector dense embeddings, Reciprocal Rank Fusion, and cross-encoder reranking."
        ),
        "responsibilities": (
            "• Build deterministic PDF/document chunking and metadata ingestion pipelines.\n"
            "• Implement Reciprocal Rank Fusion (RRF) and faithfulness evaluation harnesses.\n"
            "• Ship grounded citation endpoints in FastAPI with Turnitin-audited documentation."
        ),
    },
    {
        "company_id": 5,
        "post_type": "internship",
        "domain": "AI Agent Development",
        "title": "CrewAI Tool-Calling & Autonomous Workflow Intern — Hyderabad 2027",
        "slug": "crewai-tool-calling-autonomous-workflow-intern-hyderabad-2027",
        "location": "Hyderabad",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "CrewAI, Ollama, Python, FastAPI, Redis, JSON Schema, Git",
        "description": (
            "Join Aivara Technologies in Hyderabad / Remote to build role-based multi-agent pipelines using CrewAI and "
            "local Ollama runtimes for automated business intelligence and document synthesis."
        ),
        "responsibilities": (
            "• Engineer structured JSON tool-calling connectors with token-budget monitoring.\n"
            "• Implement Redis caching and fallback recovery for multi-step agent delegations.\n"
            "• Deliver 3+ senior-reviewed pull requests on live Aivara repositories."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "AI Agent Development",
        "title": "Machine Learning Inference & MLOps Intern (Docker / FastAPI) — Pune 2027",
        "slug": "machine-learning-inference-mlops-intern-pune-2027",
        "location": "Pune",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Python, scikit-learn, PyTorch, MLflow, Docker, FastAPI, GitHub Actions",
        "description": (
            "Join DBERT Engineering in Pune / Remote to containerize predictive ML models, automate CI validation gates, "
            "and monitor inference drift across production venture APIs."
        ),
        "responsibilities": (
            "• Build reproducible scikit-learn and PyTorch training pipelines with MLflow tracking.\n"
            "• Package inference services in non-root Docker containers with automated smoke tests.\n"
            "• Complete >=75% portal attendance and 3+ approved repository PRs."
        ),
    },

    # --- DevOps & Cloud (5 multi-city 2027 posts) ---
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "DevOps & Cloud",
        "title": "Docker & Multi-Stage Container Engineering Intern — Mumbai 2027",
        "slug": "docker-multi-stage-container-engineering-intern-mumbai-2027",
        "location": "Mumbai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Docker, Docker Compose, Linux, Nginx, PostgreSQL, Redis, Bash",
        "description": (
            "Join DBERT Infrastructure in Mumbai / Remote to optimize multi-stage Docker builds, harden non-root containers, "
            "and orchestrate isolated Next.js + FastAPI + PostgreSQL stacks."
        ),
        "responsibilities": (
            "• Author lean multi-stage Dockerfiles with healthchecks and secret-free environment hygiene.\n"
            "• Configure Nginx reverse-proxy compression, security headers, and TLS termination.\n"
            "• Ship verified infrastructure PRs under senior systems architect review."
        ),
    },
    {
        "company_id": 2,
        "post_type": "internship",
        "domain": "DevOps & Cloud",
        "title": "GitHub Actions CI/CD & Release Automation Intern — Hyderabad 2027",
        "slug": "github-actions-cicd-release-automation-intern-hyderabad-2027",
        "location": "Hyderabad",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "GitHub Actions, CI/CD, Docker, PyTest, ESLint, Linux, Git",
        "description": (
            "Cognitive Solutions is hiring a CI/CD Automation Intern in Hyderabad / Remote to build deterministic GitHub Actions "
            "workflows enforcing lint, typecheck, PyTest, and build gates across monorepo apps."
        ),
        "responsibilities": (
            "• Design fast cached GitHub Actions pipelines for Next.js and Python Flask services.\n"
            "• Automate zero-downtime systemd verification and rollback runbooks.\n"
            "• Ship 3+ reviewed infrastructure PRs with >=75% sprint attendance."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "DevOps & Cloud",
        "title": "Terraform & AWS Cloud Infrastructure Intern — Noida 2027",
        "slug": "terraform-aws-cloud-infrastructure-intern-noida-2027",
        "location": "Noida",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Terraform, AWS EC2, VPC, IAM, Nginx, Linux, Bash",
        "description": (
            "Join DBERT Cloud Ops in Noida / Remote to author modular Terraform IaC templates, harden AWS VPC security groups, "
            "and automate PostgreSQL backup & health telemetry."
        ),
        "responsibilities": (
            "• Write declarative Terraform modules with least-privilege IAM policies.\n"
            "• Implement automated disk, memory, and systemd health diagnostics.\n"
            "• Complete weekly mentor check-ins and 3+ approved PRs."
        ),
    },
    {
        "company_id": 4,
        "post_type": "internship",
        "domain": "DevOps & Cloud",
        "title": "Kubernetes & Microservices Reliability Intern — Chennai 2027",
        "slug": "kubernetes-microservices-reliability-intern-chennai-2027",
        "location": "Chennai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Kubernetes, Docker, Prometheus, Grafana, Linux, Nginx, YAML",
        "description": (
            "Join Alkame Inc in Chennai / Remote to manage containerized deployment manifests, readiness probes, "
            "and observability dashboards for quantitative microservices."
        ),
        "responsibilities": (
            "• Author Kubernetes deployment, service, and liveness/readiness probe manifests.\n"
            "• Configure Prometheus/Grafana latency alerts and structured log inspection.\n"
            "• Ship 3+ reviewed pull requests during the 8-week sprint."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "DevOps & Cloud",
        "title": "Linux Systems & Production Deployment Intern — Kolkata 2027",
        "slug": "linux-systems-production-deployment-intern-kolkata-2027",
        "location": "Kolkata",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Linux, Systemd, Nginx, PostgreSQL, Bash, SSL/TLS, Git",
        "description": (
            "Join DBERT Engineering in Kolkata / Remote to harden Ubuntu production nodes, configure systemd workers, "
            "and maintain SSL/TLS reverse proxy reliability."
        ),
        "responsibilities": (
            "• Maintain systemd service units, SSH hardening, and automated backup scripts.\n"
            "• Troubleshoot port bindings, Nginx upstream routing, and database connection pools.\n"
            "• Complete >=75% attendance and 3+ approved pull requests."
        ),
    },

    # --- Mobile App Development (5 multi-city 2027 posts) ---
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "Mobile App Development",
        "title": "Flutter Cross-Platform App Developer Intern (Dart / Riverpod) — Mumbai 2027",
        "slug": "flutter-cross-platform-app-developer-intern-mumbai-2027",
        "location": "Mumbai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Flutter, Dart, Riverpod, REST APIs, SQLite, JWT Auth, Git",
        "description": (
            "Join DBERT Mobile Labs in Mumbai / Remote to build responsive Flutter Android/iOS interfaces, "
            "authenticated REST API clients, and clean Riverpod state management flows."
        ),
        "responsibilities": (
            "• Build modular Flutter screens with responsive breakpoints and accessible form validation.\n"
            "• Integrate JWT-authenticated REST APIs with retry and offline error states.\n"
            "• Ship 3+ mentor-reviewed pull requests to qualify for Gate 1 stipend."
        ),
    },
    {
        "company_id": 2,
        "post_type": "internship",
        "domain": "Mobile App Development",
        "title": "React Native & TypeScript Mobile Intern — Delhi NCR 2027",
        "slug": "react-native-typescript-mobile-intern-delhi-ncr-2027",
        "location": "Delhi NCR",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "React Native, TypeScript, REST APIs, AsyncStorage, SQLite, Git",
        "description": (
            "Cognitive Solutions is seeking a React Native Mobile Intern in Delhi NCR / Remote to engineer typed mobile navigation, "
            "real-time notifications, and offline-tolerant data syncing."
        ),
        "responsibilities": (
            "• Architect clean TypeScript React Native components and typed navigation stacks.\n"
            "• Implement offline caching queues and optimistic UI updates.\n"
            "• Maintain >=75% attendance and ship 3+ approved repository PRs."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "Mobile App Development",
        "title": "Offline-First SQLite Mobile Sync Intern (Flutter / Android) — Chennai 2027",
        "slug": "offline-first-sqlite-mobile-sync-intern-chennai-2027",
        "location": "Chennai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Flutter, SQLite, Offline Sync, Dart, REST APIs, Unit Testing",
        "description": (
            "Join DBERT Engineering in Chennai / Remote to implement resilient SQLite local persistence, "
            "background sync queues, and conflict-free reconnect flows for mobile LMS clients."
        ),
        "responsibilities": (
            "• Design local SQLite schemas and deterministic sync queues for intermittent networks.\n"
            "• Write widget and unit tests verifying offline-to-online recovery.\n"
            "• Package reproducible Android APK release builds under mentor review."
        ),
    },
    {
        "company_id": 3,
        "post_type": "internship",
        "domain": "Mobile App Development",
        "title": "Mobile UI Performance & Push Notification Intern — Noida 2027",
        "slug": "mobile-ui-performance-push-notification-intern-noida-2027",
        "location": "Noida",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Flutter, React Native, Deep Linking, Push Notifications, Profiling",
        "description": (
            "Gayatri AI is hiring a Mobile Performance Intern in Noida / Remote to eliminate frame drops, "
            "implement deep linking, and integrate real-time learner push notifications."
        ),
        "responsibilities": (
            "• Profile list virtualization, image caching, and 60fps UI transitions.\n"
            "• Wire deep-link routes and permission prompts cleanly across Android devices.\n"
            "• Deliver 3+ reviewed PRs with Turnitin-verified documentation."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "Mobile App Development",
        "title": "Mobile API Security & Release Engineering Intern — Gurgaon 2027",
        "slug": "mobile-api-security-release-engineering-intern-gurgaon-2027",
        "location": "Gurgaon",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Flutter, Secure Storage, JWT Refresh, Android SDK, CI/CD, Git",
        "description": (
            "Join DBERT Mobile Systems in Gurgaon / Remote to harden mobile token storage, automate Android AAB builds, "
            "and enforce API contract validation."
        ),
        "responsibilities": (
            "• Implement secure encrypted token storage and automatic refresh-token rotation.\n"
            "• Automate Android release signing and smoke-test CI pipelines.\n"
            "• Complete weekly sprint reviews and 3+ approved pull requests."
        ),
    },

    # --- Cybersecurity & UI/UX Design (5 multi-city 2027 posts) ---
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "Cybersecurity",
        "title": "OWASP Top 10 AppSec & API Pentesting Intern — Mumbai 2027",
        "slug": "owasp-top10-appsec-api-pentesting-intern-mumbai-2027",
        "location": "Mumbai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "OWASP Top 10, Burp Suite, Python, JWT Security, SQLi/XSS Defense, Linux",
        "description": (
            "Join DBERT Security Suite in Mumbai / Remote to conduct authorized sandbox OWASP Top 10 audits, "
            "detect BOLA/IDOR and injection risks, and author code-level remediation PRs."
        ),
        "responsibilities": (
            "• Audit FastAPI/Flask and Next.js endpoints against OWASP Top 10 risks.\n"
            "• Submit parameterized-query, CSP, and rate-limiting remediation pull requests.\n"
            "• Author CVSS-scored vulnerability dossiers with <3% Turnitin similarity."
        ),
    },
    {
        "company_id": 2,
        "post_type": "internship",
        "domain": "Cybersecurity",
        "title": "SOC Threat Triage & SIEM Log Forensics Intern — Delhi NCR 2027",
        "slug": "soc-threat-triage-siem-log-forensics-intern-delhi-ncr-2027",
        "location": "Delhi NCR",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Wazuh, SIEM Logs, Wireshark, Linux Hardening, Python, SOC Analysis",
        "description": (
            "Cognitive Solutions is hiring a SOC & SIEM Analysis Intern in Delhi NCR / Remote to correlate authentication logs, "
            "analyze packet captures in Wireshark, and automate brute-force containment rules."
        ),
        "responsibilities": (
            "• Inspect Linux auth, Nginx, and API rate-limit telemetry for anomaly patterns.\n"
            "• Write Python log-parsing alerts and SSH/firewall hardening checklists.\n"
            "• Ship 3+ verified security engineering PRs during the 8-week sprint."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "Cybersecurity",
        "title": "Cloud IAM & Zero-Trust Auth Hardening Intern — Chennai 2027",
        "slug": "cloud-iam-zero-trust-auth-hardening-intern-chennai-2027",
        "location": "Chennai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "OAuth2 PKCE, JWT Rotation, CSP, HSTS, Linux, Python, Cryptography",
        "description": (
            "Join DBERT Security in Chennai / Remote to harden OAuth2 PKCE login flows, CSRF protections, "
            "and strict HTTP security header policies across production web portals."
        ),
        "responsibilities": (
            "• Validate OAuth2 state/PKCE flows and HttpOnly/SameSite cookie policies.\n"
            "• Automate secret-scanning and dependency vulnerability checks in CI.\n"
            "• Maintain >=75% attendance and ship 3+ approved PRs."
        ),
    },
    {
        "company_id": 1,
        "post_type": "internship",
        "domain": "UI/UX Design",
        "title": "Figma Design Systems & WCAG Accessibility Intern — Mumbai 2027",
        "slug": "figma-design-systems-wcag-accessibility-intern-mumbai-2027",
        "location": "Mumbai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Figma, Auto-Layout, Design Tokens, WCAG 2.2 AA, Tailwind CSS Specs",
        "description": (
            "Join DBERT Design Labs in Mumbai / Remote to build responsive Figma component libraries, "
            "verify WCAG 2.2 AA contrast/touch targets, and deliver developer-ready Tailwind specs."
        ),
        "responsibilities": (
            "• Design responsive Auto-Layout component variants across 320px–1440px breakpoints.\n"
            "• Audit multi-step enrollment and LMS flows for accessibility and conversion clarity.\n"
            "• Collaborate with frontend engineers on live UI QA pull requests."
        ),
    },
    {
        "company_id": 2,
        "post_type": "internship",
        "domain": "UI/UX Design",
        "title": "Product UX Research & Conversion Prototyping Intern — Chennai 2027",
        "slug": "product-ux-research-conversion-prototyping-intern-chennai-2027",
        "location": "Chennai",
        "work_mode": "Remote",
        "stipend_min": 5000,
        "stipend_max": 18000,
        "skills": "Figma Prototyping, UX Research, User Journeys, Wireframing, CRO",
        "description": (
            "Cognitive Solutions is seeking a Product UX Intern in Chennai / Remote to conduct usability teardowns, "
            "prototype onboarding journeys, and reduce mobile friction across SaaS dashboards."
        ),
        "responsibilities": (
            "• Map end-to-end user journeys with explicit loading, empty, and error states.\n"
            "• Deliver interactive Figma prototypes and developer handoff specs.\n"
            "• Complete >=75% sprint attendance and verified capstone review."
        ),
    },
]


def main():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not set in environment or .env")

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SET search_path TO dbert_internship")

    # 1. Renew all posts expiring in next 15d (apply_by <= 2026-12-10) OR expires_at < 2027-02-10
    cur.execute(
        "SELECT id, post_type, domain, title, apply_by, expires_at, eligibility "
        "FROM posts WHERE status='published' ORDER BY id"
    )
    rows = cur.fetchall()
    print(f"Loaded {len(rows)} published posts from PostgreSQL.")

    renewed_28 = 0
    fixed_2027_dates = 0
    steered_1999 = 0

    for pid, ptype, domain, title, apply_by, expires_at, elig in rows:
        exp_str = str(expires_at or "")[:10]
        app_str = str(apply_by or "")[:10]
        elig_str = elig or ""

        needs_date_renewal = (
            not exp_str
            or exp_str < "2027-02-10"
            or not app_str
            or app_str <= "2026-12-10"
        )
        needs_1999 = "enroll/1999" not in elig_str

        if not needs_date_renewal and not needs_1999:
            continue

        new_title = title
        if needs_date_renewal and exp_str < "2027-01-01":
            if "2027" not in new_title:
                new_title = f"{new_title} (2026/2027)"
            renewed_28 += 1
        elif needs_date_renewal:
            fixed_2027_dates += 1

        if needs_1999:
            if elig_str.strip():
                new_elig = elig_str.strip() + "\n\n" + STEERING_ELIGIBILITY_BLOCK
            else:
                new_elig = STEERING_ELIGIBILITY_BLOCK
            steered_1999 += 1
        else:
            new_elig = elig_str

        if needs_date_renewal:
            new_apply = TARGET_APPLY_BY
            new_exp = TARGET_EXPIRES_AT
            cur.execute(
                """
                UPDATE posts
                SET title = %s,
                    apply_by = %s,
                    expires_at = %s,
                    published_at = CASE WHEN published_at < '2026-11-20' THEN %s ELSE published_at END,
                    updated_at = %s,
                    eligibility = %s,
                    status = 'published'
                WHERE id = %s
                """,
                (new_title, new_apply, new_exp, TARGET_PUBLISHED_AT, TARGET_UPDATED_AT, new_elig, pid),
            )
        else:
            cur.execute(
                "UPDATE posts SET eligibility = %s, updated_at = %s WHERE id = %s",
                (new_elig, TARGET_UPDATED_AT, pid),
            )

    # 2. Insert 20 new 2027 multi-city posts idempotently by slug
    inserted = 0
    for p in NEW_2027_POSTS:
        cur.execute("SELECT id FROM posts WHERE slug = %s", (p["slug"],))
        if cur.fetchone():
            continue
        cur.execute(
            """
            INSERT INTO posts (
                company_id, post_type, domain, title, slug, description, responsibilities,
                skills, location, work_mode, stipend_min, stipend_max, pay_period, is_unpaid,
                duration, openings, apply_by, certifications_json, eligibility, status,
                published_at, expires_at, views, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, 'month', 0,
                '2 Months', 5, %s, '[]', %s, 'published',
                %s, %s, 0, %s, %s
            )
            """,
            (
                p["company_id"],
                p["post_type"],
                p["domain"],
                p["title"],
                p["slug"],
                p["description"],
                p["responsibilities"],
                p["skills"],
                p["location"],
                p["work_mode"],
                p["stipend_min"],
                p["stipend_max"],
                TARGET_APPLY_BY,
                STEERING_ELIGIBILITY_BLOCK,
                TARGET_PUBLISHED_AT,
                TARGET_EXPIRES_AT,
                TARGET_UPDATED_AT,
                TARGET_UPDATED_AT,
            ),
        )
        inserted += 1

    conn.commit()

    # Post-verification summary
    cur.execute("SELECT COUNT(*) FROM posts WHERE status='published'")
    total_pub = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM posts WHERE status='published' AND expires_at >= '2027-01-01'")
    total_2027 = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM posts WHERE status='published' AND apply_by <= '2026-12-10'")
    still_expiring = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM posts WHERE status='published' AND eligibility LIKE '%enroll/1999%'")
    total_steered = cur.fetchone()[0]

    print(f"Summary:")
    print(f"  Renewed <2027 expiring posts: {renewed_28}")
    print(f"  Aligned 2027 dates (apply_by <= expires_at): {fixed_2027_dates}")
    print(f"  Added /enroll/1999 steering to posts: {steered_1999}")
    print(f"  Inserted new 2027 multi-city posts: {inserted}")
    print(f"Post-check:")
    print(f"  Total published posts: {total_pub}")
    print(f"  Posts with 2027+ expiry: {total_2027}")
    print(f"  Posts with apply_by <= 2026-12-10: {still_expiring}")
    print(f"  Posts with /enroll/1999 eligibility steering: {total_steered}/{total_pub}")

    conn.close()


if __name__ == "__main__":
    main()
