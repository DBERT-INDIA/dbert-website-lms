import subprocess
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

# Remote python script that will run in EC2 venv
remote_script = """
import psycopg2
import json

conn = psycopg2.connect("postgresql://dbert_user:DBERT_SECURE_PASSWORD_123@localhost:5432/dbert_lms")
c = conn.cursor()

NEW_PUBLISHED_AT = '2026-11-18 10:00:00'
NEW_APPLY_BY = '2027-01-05'
NEW_EXPIRES_AT = '2027-02-05 23:59:59'
NEW_UPDATED_AT = '2026-11-18 10:00:00'

STEERING_ELIGIBILITY_TEXT = (
    "Open to engineering students, recent graduates, and entry-level professionals with foundational technical knowledge. "
    "Requires commitment of at least 10 hours per week and >=75% portal attendance.\\n\\n"
    "PREFERRED CANDIDATE PROFILE & FAST-TRACK SELECTION PATHWAY:\\n"
    "• Standard Track: Open to all applicants meeting core technical prerequisites. Applications reviewed sequentially.\\n"
    "• Accelerated Fast-Track (Priority Shortlisting): Direct Round-1 technical screening waivers and expedited interview review "
    "are granted to candidates enrolled in or holding a verified credential from the DBERT 8-Week Sovereign Incubation & Production Sprint Track "
    "(https://dbert.in/enroll/1999). Incubation fellows enter review with verified GitHub PR proof-of-work, cryptographic Turnitin originality scoring, "
    "and recommendation letters (LOR) from program mentors.\\n"
    "Candidates looking to build verified client repository contributions to meet hiring prerequisites are advised to complete the incubation track at https://dbert.in/enroll/1999."
)

UPDATES = {
    # ==================== 20 JOBS ====================
    16: {
        "title": "AI Agent Developer (LangGraph / Multi-Agent Systems) — Remote 2026",
        "description": "Join Gayatri AI as an AI Agent Developer building scalable autonomous multi-agent systems and production LLM orchestration services. In this role, you will architect resilient state-machine agentic workflows, implement structured JSON-schema tool-calling routines, and deploy high-throughput inference endpoints integrated with enterprise knowledge graphs and vector search indices.",
        "responsibilities": (
            "• Design and deploy stateful multi-agent workflows using LangGraph, CrewAI, and Python 3.12 async runtimes.\\n"
            "• Implement autonomous tool-calling routines, fallback loops, and dynamic human-in-the-loop escalation gates.\\n"
            "• Build and optimize pgvector and ChromaDB semantic indexing pipelines over complex corporate knowledge bases.\\n"
            "• Profile and monitor LLM latency, token utilization, and output evaluation metrics across production APIs.\\n"
            "• Maintain high code quality through rigorous automated testing, CI/CD pipelines, and structured Git PR reviews."
        ),
        "skills": "Python, LangGraph, CrewAI, OpenAI API, FastAPI, pgvector, Redis, vLLM",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    17: {
        "title": "LLM Integration & RAG Pipeline Engineer — Remote India",
        "description": "DBERT Systems is hiring an LLM Integration & RAG Pipeline Engineer to develop enterprise-grade Retrieval-Augmented Generation architectures. You will engineer vector search pipelines, integrate hybrid dense-sparse retrieval systems (BM25 + Cohere Rerank), and connect foundation models to internal SQL databases and real-time streaming interfaces.",
        "responsibilities": (
            "• Architect production-grade RAG retrieval pipelines supporting multi-document chunking and semantic reranking.\\n"
            "• Integrate foundation model APIs (OpenAI, Claude, Llama 3) into asynchronous FastAPI microservices.\\n"
            "• Implement context-aware conversation serialization and episodic memory buffers in Redis.\\n"
            "• Benchmark retrieval precision, recall, and hallucination rates using automated evaluation frameworks.\\n"
            "• Collaborate with frontend teams to build streaming token response channels via WebSockets and Server-Sent Events (SSE)."
        ),
        "skills": "Python, RAG Pipelines, LlamaIndex, pgvector, FastAPI, PostgreSQL, Redis, Docker",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    18: {
        "title": "Applied AI Engineer (Autonomous Workflows & vLLM) — Bangalore / Remote",
        "description": "We are seeking an Applied AI Engineer to join our Agentic Systems team in Bangalore / Remote. You will focus on deploying localized open-weight language models using vLLM and Ollama, fine-tuning task-specific adapters via LoRA/QLoRA, and orchestrating autonomous workflows that execute database operations and scheduled batch jobs.",
        "responsibilities": (
            "• Configure and optimize high-concurrency local model inference servers using vLLM, TensorRT-LLM, and Ollama.\\n"
            "• Curate domain datasets and execute parameter-efficient fine-tuning (PEFT/LoRA) for specialized extraction tasks.\\n"
            "• Develop agentic automation daemons capable of synthesizing multi-source data feeds into executive reports.\\n"
            "• Harden API gateways with rate limiting, prompt-injection guards, and semantic output verification.\\n"
            "• Coordinate deployment across AWS EC2 GPU instances and containerized Kubernetes clusters."
        ),
        "skills": "Python, vLLM, Ollama, PyTorch, LoRA Fine-Tuning, Docker, AWS EC2, Kubernetes",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    34: {
        "title": "Junior Data Analyst (SQL, Python & BI Dashboards) — Work From Home",
        "description": "Join our Analytics Operations group as a Junior Data Analyst delivering actionable business intelligence and automated reporting. You will clean and transform large-scale transaction datasets, author complex multi-table SQL queries, and construct interactive Metabase and Power BI executive dashboards for cross-functional stakeholders.",
        "responsibilities": (
            "• Author and optimize advanced SQL queries featuring window functions, common table expressions (CTEs), and indexing.\\n"
            "• Clean, normalize, and validate structured CSV and database extracts using Python Pandas and NumPy.\\n"
            "• Design intuitive, automated corporate dashboards tracking user retention, revenue funnels, and churn telemetry.\\n"
            "• Conduct exploratory data analysis (EDA) to uncover operational bottlenecks and growth opportunities.\\n"
            "• Automate recurring weekly and monthly reporting schedules with automated email dispatch hooks."
        ),
        "skills": "SQL (PostgreSQL/MySQL), Python, Pandas, Metabase, Power BI, Excel Advanced, Data Modeling",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    35: {
        "title": "Business Intelligence Analyst (Power BI / Metabase & ETL) — Remote",
        "description": "We are looking for a remote Business Intelligence Analyst to spearhead corporate telemetry and data warehousing initiatives. You will design dimensional data models (star schemas), orchestrate lightweight ETL pipelines, and transform raw application events into high-impact visual dashboards for senior leadership.",
        "responsibilities": (
            "• Build and maintain robust data pipelines extracting data from transactional databases into analytical stores.\\n"
            "• Design semantic data layers and DAX measures in Power BI / Metabase for self-service reporting.\\n"
            "• Audit data integrity across production event streams, ensuring zero discrepancy between billing and telemetry.\\n"
            "• Author technical documentation and data dictionaries detailing KPIs, metrics definitions, and lineage.\\n"
            "• Partner with product engineers to define tracking specs for newly released platform capabilities."
        ),
        "skills": "Power BI, DAX, SQL, Data Warehousing, Python, ETL Pipelines, Tableau, Business Intelligence",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    36: {
        "title": "Corporate Reporting & Insights Analyst — Delhi NCR / Remote",
        "description": "Seeking a dedicated Reporting & Insights Analyst based in Delhi NCR / Remote to analyze candidate engagement, conversion funnels, and multi-channel campaign performance. You will synthesize telemetry across Google Analytics 4 (GA4), PostgreSQL event logs, and messaging channels to guide tactical business decisions.",
        "responsibilities": (
            "• Monitor and report on candidate acquisition cohorts, onboarding completion rates, and churn metrics.\\n"
            "• Perform statistical segmentation and cohort analysis to identify highest-performing acquisition channels.\\n"
            "• Build automated alert monitors triggering real-time notifications on significant metric deviations.\\n"
            "• Prepare weekly executive presentation decks translating complex data patterns into concise strategic takeaways.\\n"
            "• Ensure strict adherence to data privacy and cryptographic credential protection policies."
        ),
        "skills": "SQL, GA4 Analytics, Python, Power BI, Statistics, Cohort Analysis, Google Sheets Automation",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    52: {
        "title": "Full Stack Web Developer (Next.js 15, TypeScript & Node.js) — Remote",
        "description": "DBERT Engineering is hiring a Full Stack Web Developer to build high-performance web applications and public verification engines. You will work with React 19, Next.js 15 App Router, TypeScript, Tailwind CSS, and Node.js microservices deployed in standalone containerized production environments.",
        "responsibilities": (
            "• Develop responsive, accessible web portals using Next.js App Router, React Server Components (RSC), and Turbopack.\\n"
            "• Build and maintain type-safe backend API endpoints, server actions, and PostgreSQL database queries.\\n"
            "• Implement cryptographic verification routes with high-speed caching and micro-QR generation.\\n"
            "• Optimize Core Web Vitals (LCP, FID, CLS) to achieve 95+ Google PageSpeed performance scores.\\n"
            "• Manage automated deployments, systemd services, and reverse-proxy configurations on Ubuntu EC2 servers."
        ),
        "skills": "Next.js, React, TypeScript, Node.js, PostgreSQL, Tailwind CSS, REST APIs, Git",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    53: {
        "title": "Backend API Engineer (FastAPI, Flask & PostgreSQL) — Remote India",
        "description": "We are seeking a Backend API Engineer to design and scale high-reliability web APIs powering our LMS and verification ecosystems. You will architect RESTful and WebSocket endpoints using Python (FastAPI/Flask), optimize relational schemas in PostgreSQL, and configure Redis caching layers for sub-100ms response times.",
        "responsibilities": (
            "• Build, document, and test scalable REST APIs adhering strictly to OpenAPI / Swagger specifications.\\n"
            "• Write optimized database migrations, complex joins, and stored procedures in PostgreSQL.\\n"
            "• Implement secure authentication workflows utilizing JWT tokens, role-based access control (RBAC), and bcrypt.\\n"
            "• Integrate third-party webhooks, payment gateways, and transactional SMTP delivery relays.\\n"
            "• Monitor server health, log telemetry, and diagnose production performance bottlenecks."
        ),
        "skills": "Python, FastAPI, Flask, PostgreSQL, Redis, SQLAlchemy, JWT Auth, Docker, Linux",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    54: {
        "title": "Frontend Developer (React 19, Tailwind CSS & State Machines) — Remote",
        "description": "Looking for a talented Frontend Developer (Hyderabad / Remote) passionate about craft, typography, and interactive web experiences. You will translate Figma design systems into pixel-perfect, responsive React components, manage complex application state, and integrate real-time token streaming chat interfaces.",
        "responsibilities": (
            "• Build modern, modular component libraries using React 19, TypeScript, and utility-first Tailwind CSS.\\n"
            "• Implement intuitive interactive animations, state transitions, and client-side form validations.\\n"
            "• Ensure robust cross-browser compatibility and full responsive optimization across mobile, tablet, and desktop.\\n"
            "• Integrate streaming API endpoints for conversational AI interfaces and live countdown telemetry.\\n"
            "• Collaborate closely with UI/UX designers to implement cohesive dark-mode and luxury slate themes."
        ),
        "skills": "React.js, TypeScript, Tailwind CSS, HTML5/CSS3, State Management, REST APIs, Figma",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    70: {
        "title": "Python Automation Engineer (Playwright, Scrapy & Celery) — Remote",
        "description": "Join our Data Engineering team as a Python Automation Engineer focused on autonomous data collection, browser robotics, and distributed job orchestration. You will construct resilient Playwright and Scrapy spiders, handle multi-session concurrency, and build distributed worker queues with Celery and Redis.",
        "responsibilities": (
            "• Build and maintain robust headless browser automation daemons using Playwright and Chromium.\\n"
            "• Design scalable multi-threaded scrapers with automatic retry logic, proxy rotation, and session persistence.\\n"
            "• Orchestrate asynchronous background queues with Celery and Redis to process millions of records daily.\\n"
            "• Parse, sanitize, and normalize complex unstructured HTML and JSON payloads into PostgreSQL schemas.\\n"
            "• Set up automated alerting mechanisms to monitor data pipelines against layout drift or anti-scraping blocks."
        ),
        "skills": "Python, Playwright, Scrapy, Celery, Redis, Beautiful Soup, PostgreSQL, Linux Bash",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    71: {
        "title": "Enterprise Scripting & Workflow Automation Developer — Remote 2026",
        "description": "Seeking an Automation Developer to streamline internal operations and candidate lifecycle workflows. You will develop automated Python scripts connecting Google Workspace APIs, Google Sheets, SQLite databases, and transactional communication services to eliminate manual administrative overhead.",
        "responsibilities": (
            "• Develop custom Python automation scripts interfacing with REST APIs, webhooks, and Google Workspace.\\n"
            "• Build idempotent batch dispatch systems with pacing, quota circuit breakers, and delivery audit logs.\\n"
            "• Automate database synchronization routines between edge SQLite replicas and central PostgreSQL datastores.\\n"
            "• Write resilient unit tests and validation probes ensuring zero duplicate transactions or lost messages.\\n"
            "• Maintain complete operational runbooks and cron configurations on Linux production servers."
        ),
        "skills": "Python, Bash Scripting, REST APIs, Google APIs, SQLite, PostgreSQL, Cron Automation, Git",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    72: {
        "title": "QA Automation Engineer (PyTest, API Testing & CI/CD) — Pune / Remote",
        "description": "We are seeking a QA Automation Engineer based in Pune / Remote to lead test automation across web applications and backend APIs. You will author comprehensive PyTest suites, end-to-end browser tests in Playwright, and integrate automated regression testing into GitHub Actions CI/CD pipelines.",
        "responsibilities": (
            "• Author maintainable, modular test automation frameworks using Python, PyTest, and Playwright.\\n"
            "• Develop comprehensive API test suites validating response schemas, authentication, and boundary edge cases.\\n"
            "• Configure automated test execution inside GitHub Actions pipelines blocking regressions before production merges.\\n"
            "• Conduct load and stress testing using Locust to measure API degradation under high traffic volumes.\\n"
            "• Track, triage, and document software bugs in structured Jira/GitHub issue tracking workflows."
        ),
        "skills": "Python, PyTest, Playwright, API Testing (Postman/Requests), CI/CD, GitHub Actions, Docker",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    82: {
        "title": "UI/UX Product Designer (Figma Systems, UX Research & Prototyping) — Remote",
        "description": "Join DBERT Design Labs as a UI/UX Product Designer creating world-class digital learning portals, candidate dashboards, and credential verification interfaces. You will conduct user research, construct comprehensive design systems in Figma, and build interactive high-fidelity prototypes.",
        "responsibilities": (
            "• Develop comprehensive design system component libraries in Figma with autolayout, tokens, and variants.\\n"
            "• Conduct user interviews, usability audits, and card-sorting exercises to validate feature flows.\\n"
            "• Wireframe, prototype, and deliver intuitive desktop and mobile layouts for complex technical dashboards.\\n"
            "• Partner directly with frontend engineers to inspect CSS implementation and maintain visual parity.\\n"
            "• Design engaging data visualizations, rubric audit seals, and luxury cryptographic certificate art."
        ),
        "skills": "Figma, UI/UX Design, Design Systems, Prototyping, Wireframing, User Research, HTML/CSS Basics",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    83: {
        "title": "Design Systems Engineer & Product UI Architect — Bangalore / Remote",
        "description": "Seeking a Design Systems Engineer in Bangalore / Remote who bridges the gap between design and engineering. You will establish and maintain tokenized component libraries in React/Tailwind, enforce accessibility (WCAG 2.1 AA) standards, and ensure seamless visual consistency across all DBERT web properties.",
        "responsibilities": (
            "• Build and maintain reusable, accessible UI component libraries using TypeScript, React, and Tailwind CSS.\\n"
            "• Standardize design tokens (typography, color palettes, spacing, elevation) between Figma and frontend code.\\n"
            "• Conduct automated accessibility audits ensuring 100% keyboard navigation and screen-reader support.\\n"
            "• Author Storybook documentation demonstrating component states, props, and responsive behaviors.\\n"
            "• Provide guidance and code reviews for product engineers implementing frontend screens."
        ),
        "skills": "Design Systems, React, TypeScript, Tailwind CSS, Storybook, Accessibility (a11y), Figma",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    89: {
        "title": "DevOps & Cloud Infrastructure Engineer (Docker, AWS & Terraform) — Remote",
        "description": "We are looking for a DevOps & Cloud Infrastructure Engineer to manage cloud infrastructure, deployment pipelines, and system security on AWS. You will containerize applications with Docker, orchestrate CI/CD pipelines, configure Nginx reverse proxies with SSL termination, and monitor uptime.",
        "responsibilities": (
            "• Provision and maintain AWS cloud infrastructure including EC2 instances, VPCs, security groups, and Route53.\\n"
            "• Author robust GitHub Actions CI/CD workflows automating testing, building, and zero-downtime deployments.\\n"
            "• Configure and harden Nginx reverse proxies, SSL/TLS certificates (Let's Encrypt), and fail2ban rules.\\n"
            "• Containerize microservices with Docker and Docker Compose for reproducible local and staging environments.\\n"
            "• Implement centralized logging, Prometheus monitoring, and automated database backup daemons."
        ),
        "skills": "AWS (EC2/VPC/S3), Docker, Nginx, Linux (Ubuntu), GitHub Actions, Terraform, PostgreSQL, Bash",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    90: {
        "title": "Site Reliability Engineer (Kubernetes, Prometheus & CI/CD) — Bangalore",
        "description": "Join our Infrastructure Engineering team in Bangalore / Remote as a Site Reliability Engineer (SRE). You will ensure 99.9% platform availability, manage auto-healing systemd and container services, establish observability dashboards, and automate incident response protocols.",
        "responsibilities": (
            "• Monitor platform availability, response latencies, and server resource utilization around the clock.\\n"
            "• Implement distributed tracing, log aggregation, and alerting using Prometheus, Grafana, and Loki.\\n"
            "• Conduct post-incident root-cause analyses (RCA) and engineer automated self-healing remediation routines.\\n"
            "• Optimize database query performance, connection pooling, and disk I/O across production clusters.\\n"
            "• Conduct disaster recovery drills and validate automated automated daily snapshot restorations."
        ),
        "skills": "Linux Administration, Prometheus, Grafana, Kubernetes, Python/Bash, PostgreSQL, Docker, AWS",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    96: {
        "title": "Mobile Application Developer (React Native / Flutter & Cross-Platform) — Remote",
        "description": "We are seeking a Mobile Application Developer to build high-performance mobile LMS apps for iOS and Android. You will build cross-platform mobile interfaces in React Native / Flutter, implement offline course caching, and integrate push notification engines.",
        "responsibilities": (
            "• Develop smooth, intuitive cross-platform mobile apps using React Native / Flutter with TypeScript/Dart.\\n"
            "• Integrate secure mobile authentication, biometric sign-in, and offline progress synchronization with SQLite.\\n"
            "• Connect REST and WebSocket APIs for live quizzes, chat discussions, and real-time sprint countdowns.\\n"
            "• Optimize app bundle size, startup times, and 60fps animation performance on low-end Android devices.\\n"
            "• Manage app release pipelines through Google Play Console and Apple App Store TestFlight."
        ),
        "skills": "React Native, Flutter, TypeScript, Mobile UI/UX, REST APIs, SQLite, Git, App Store Deployment",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    97: {
        "title": "Senior Mobile Architecture Engineer (iOS & Android Systems) — Bangalore",
        "description": "Looking for an experienced Mobile Architecture Engineer in Bangalore / Remote to steer mobile architecture and SDK development. You will architect modular mobile frameworks, enforce clean architectural patterns (MVVM/Bloc), and ensure enterprise-grade security for mobile educational content.",
        "responsibilities": (
            "• Architect clean, modular mobile codebases supporting dynamic feature modules and localized caching.\\n"
            "• Implement cryptographic token validation and secure local storage for digital credential viewing.\\n"
            "• Establish automated unit and UI testing pipelines using Jest, Maestro, or Appium.\\n"
            "• Mentor junior mobile developers through structured code reviews and architectural guidelines.\\n"
            "• Stay ahead of new mobile platform capabilities, OS permission models, and battery optimization rules."
        ),
        "skills": "Mobile Architecture, React Native, Flutter, Native Android (Kotlin), iOS (Swift), CI/CD Mobile",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    103: {
        "title": "Junior Cybersecurity & SOC Analyst (SIEM, Threat Audit & OWASP) — Remote",
        "description": "Join DBERT Information Security as a Junior Cybersecurity & SOC Analyst. You will monitor security event logs, perform vulnerability scans across public endpoints, audit compliance with OWASP Top 10 standards, and investigate suspicious authentication activities.",
        "responsibilities": (
            "• Monitor web application firewall (WAF) logs, server access telemetry, and rate-limit breach events.\\n"
            "• Perform periodic vulnerability assessments using OWASP ZAP, Nmap, and automated static code scanners.\\n"
            "• Audit authentication flows, password hash algorithms, and session expiration policies across endpoints.\\n"
            "• Investigate and remediate reported phishing attempts, suspicious credential stuffing, and bot scraping.\\n"
            "• Author incident response reports and security hardening documentation for development teams."
        ),
        "skills": "Cybersecurity, SOC Monitoring, OWASP Top 10, Network Security, Linux, Wireshark, SIEM, Python",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    104: {
        "title": "Application Security & API Penetration Tester — Bangalore / Remote",
        "description": "Seeking an Application Security Engineer & API Penetration Tester in Bangalore / Remote. You will proactively test our web portals, Next.js routes, and Flask APIs against adversarial threats, conduct red-team simulations, and harden cloud databases against unauthorized exposure.",
        "responsibilities": (
            "• Conduct manual and automated penetration testing across web applications, REST APIs, and microservices.\\n"
            "• Identify and safely demonstrate vulnerabilities including SQL injection, IDOR, SSRF, and CSRF.\\n"
            "• Partner with backend engineers to implement cryptographically secure mitigations and input sanitization.\\n"
            "• Review source code for security flaws and hardcoded secrets within GitHub PR pull requests.\\n"
            "• Establish security guardrails, Fernet encryption standards, and automated SAST/DAST pipeline gates."
        ),
        "skills": "Application Security, Penetration Testing, API Security, Burp Suite, Cryptography, Python, Linux",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },

    # ==================== 20 INTERNSHIPS ====================
    1: {
        "title": "Enterprise RAG Pipeline Engineering Intern (Vector Search & LOR) — Remote",
        "description": "DBERT Labs is offering a production-oriented RAG Pipeline Engineering Internship. You will work on real client repositories, constructing state-of-the-art semantic search pipelines with pgvector, evaluating dense vs sparse retrieval, and earning an authenticated Certificate of Completion and Letter of Recommendation (LOR).",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Contribute production code to DBERT-INDIA partner repositories implementing RAG chunking algorithms.\\n"
            "• Configure vector index embeddings using OpenAI and open-source Hugging Face embedding models.\\n"
            "• Build automated evaluation benchmarks measuring precision, recall, and contextual relevance.\\n"
            "• Author a capstone technical publication documenting pipeline architecture and latency benchmarks."
        ),
        "skills": "Python, LangChain, RAG Pipelines, pgvector, FastAPI, OpenAI API, Vector Databases",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    2: {
        "title": "LLM Tool-Calling & Autonomous Agent Intern (CrewAI / LangGraph) — Remote",
        "description": "Join Gayatri AI as an LLM Tool-Calling & Autonomous Agent Intern. You will design agentic loops where models autonomously call external Python functions, scrape web interfaces with headless browsers, and synthesize structured reports, under 1-on-1 mentorship from industry practitioners.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Build autonomous agents with tool-calling loops using LangGraph, CrewAI, and structured JSON schemas.\\n"
            "• Implement fallback routing and error self-correction routines when API calls or scrapers fail.\\n"
            "• Contribute verified pull requests to authorized open-source repositories under Gayatri-Education.\\n"
            "• Participate in weekly code reviews and sprint retrospectives with senior AI mentors."
        ),
        "skills": "Python, LangGraph, CrewAI, Function Calling, Prompt Engineering, Git, REST APIs",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    3: {
        "title": "Conversational AI & Memory Orchestration Intern — Work From Home",
        "description": "Seeking a Conversational AI Intern to build stateful dialogue systems with episodic and semantic memory. You will integrate Redis memory stores, serialize user session state, and connect chatbots to relational databases for dynamic contextual querying.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Develop conversational agents capable of multi-turn dialogue with memory buffer serialization.\\n"
            "• Connect dialogue flows to PostgreSQL databases to answer student queries on course progress.\\n"
            "• Implement prompt guardrails preventing jailbreaks, off-topic drift, or unauthorized system reveals.\\n"
            "• Complete technical milestones to unlock performance incentives and verified credentials."
        ),
        "skills": "Python, Prompt Engineering, Redis, PostgreSQL, FastAPI, LangChain, Memory Systems",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    4: {
        "title": "Autonomous Task Agent & Browser Automation Intern — Remote 2026",
        "description": "Exciting internship opportunity building autonomous browser agents. You will combine large language models with Playwright to create bots that navigate web portals, extract structured data, fill forms, and verify visual page states without human intervention.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Develop autonomous browser navigation routines using Playwright and vision-capable LLMs.\\n"
            "• Handle dynamic DOM elements, infinite scroll, authentication gates, and session cookies.\\n"
            "• Submit clean, modular pull requests to partner organization codebases under Alkameinc / DBERT-INDIA.\\n"
            "• Author documentation and flowcharts detailing agent decision state trees."
        ),
        "skills": "Python, Playwright, Browser Automation, LLM Agents, Beautiful Soup, Web Scraping",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    5: {
        "title": "AI Customer Support Systems & Intent Routing Intern — Remote",
        "description": "Work on enterprise-grade customer support bots. You will implement intent classification models, semantic question routing, and automated escalation triggers, transforming traditional ticketing workflows into instant AI-assisted resolutions.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Build semantic intent classification engines categorizing incoming support inquiries in real-time.\\n"
            "• Integrate automated ticket draft responses with human-in-the-loop approval dashboards.\\n"
            "• Test bot accuracy against historical customer conversation transcripts.\\n"
            "• Gain practical experience in production SaaS architectures and customer telemetry."
        ),
        "skills": "Python, NLP, Intent Classification, REST APIs, FastAPI, PostgreSQL, Prompt Engineering",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    6: {
        "title": "Multi-Agent Coordination & Swarm Systems Intern — Remote",
        "description": "Explore the bleeding edge of AI agent swarms. In this internship, you will architect multi-agent systems where specialist agents (Researcher, Coder, Critic, Verifier) collaborate via shared message boards to solve complex programming and research challenges.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Implement consensus protocols and task partitioning among cooperating LLM agent instances.\\n"
            "• Measure swarm problem-solving accuracy against baseline single-agent execution pipelines.\\n"
            "• Deliver working demonstrations and pull requests to authorized Gayatri-Education repositories.\\n"
            "• Earn verified cryptographic evaluation badges recognized by enterprise partner employers."
        ),
        "skills": "Python, Multi-Agent Systems, LangGraph, AsyncIO, Prompt Architecture, Swarm Intelligence",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    7: {
        "title": "LLM Quantization & Model Evaluation Intern (LoRA / vLLM) — Remote",
        "description": "Hands-on internship in open-source foundation models. You will experiment with model quantization (GGUF, AWQ, EXL2), fine-tuning small language models (Llama 3 8B, Mistral, Qwen) using LoRA, and benchmarking throughput on local GPU environments.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Quantize open-weight models and benchmark memory footprint versus inference speed on vLLM.\\n"
            "• Prepare instruction-tuning datasets and evaluate loss curves during parameter-efficient fine-tuning.\\n"
            "• Implement automated evaluation harnesses checking model accuracy and safety alignment.\\n"
            "• Document experimental findings in an academic case study for the DBERT Technical Journal."
        ),
        "skills": "Python, PyTorch, Hugging Face, LoRA/PEFT, vLLM, Quantization, Model Evaluation",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    8: {
        "title": "Voice AI & Realtime Audio Pipeline Intern (WebSockets & Whisper) — Remote",
        "description": "Dive into realtime conversational voice AI. You will build sub-second voice pipelines integrating OpenAI Whisper / Deepgram speech-to-text, fast LLM token generation, and ElevenLabs / Cartesia text-to-speech over bi-directional WebSockets.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Build low-latency audio streaming pipelines connecting client microphones to server speech engines.\\n"
            "• Implement silence detection, voice activity detection (VAD), and barge-in interruption handling.\\n"
            "• Test voice response latencies, targeting sub-600ms end-to-end roundtrip times.\\n"
            "• Contribute modular voice client components to partner repositories."
        ),
        "skills": "Python, WebSockets, Whisper, Text-to-Speech (TTS), Audio Processing, FastAPI, JavaScript",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    9: {
        "title": "Document AI & Unstructured Data Extraction Intern — Remote",
        "description": "Learn to extract structured knowledge from messy enterprise documents. You will develop vision-LLM pipelines that parse complex PDFs, invoices, tables, and handwritten forms into validated Pydantic JSON schemas with 99%+ accuracy.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Build document parsing pipelines utilizing OCR (Tesseract/PaddleOCR) and multimodal vision models.\\n"
            "• Define structured extraction schemas using Pydantic and JSON validation rules.\\n"
            "• Benchmark extraction accuracy and create automated correction loops for low-confidence fields.\\n"
            "• Deliver working utility modules to authorized DBERT-INDIA open-source repositories."
        ),
        "skills": "Python, Document AI, OCR, Multimodal LLMs, Pydantic, Regular Expressions, OpenCV",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    10: {
        "title": "AI Workflow Automation Intern — Bangalore / Remote Incubation",
        "description": "Join our Bangalore / Remote Incubation unit automating enterprise software operations. You will build Python automation connectors between web applications, relational databases, email servers, and AI decision models to execute autonomous business tasks.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Construct end-to-end automated workflows replacing repetitive manual data entry operations.\\n"
            "• Integrate webhook listeners and automated email response dispatch systems with Google SMTP.\\n"
            "• Write clean, idempotent code with robust error handling and transaction rollbacks.\\n"
            "• Work under senior engineering mentors to refine production code style and Git discipline."
        ),
        "skills": "Python, REST APIs, Automation, PostgreSQL, Webhooks, Celery, Git, JSON Processing",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    11: {
        "title": "Agentic Search & Web Synthesis Intern — Delhi NCR / Remote",
        "description": "Construct intelligent search and web synthesis engines. You will build agents that take complex user research prompts, query multiple web search engines, scrape source articles, synthesize balanced answers, and generate inline markdown citations.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Build search agents leveraging DuckDuckGo/Google Search APIs and concurrent web scrapers.\\n"
            "• Implement source deduplication, fact verification, and markdown citation formatting.\\n"
            "• Benchmark answer quality against standard human research reports.\\n"
            "• Submit pull requests to active Gayatri Education research repositories."
        ),
        "skills": "Python, Web Search APIs, Beautiful Soup, LangChain, Text Summarization, AsyncIO",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    12: {
        "title": "AI Coding Assistant & AST Parsing Intern — Hyderabad / Remote",
        "description": "Help engineer the next generation of developer tooling. You will build agents that parse codebases into Abstract Syntax Trees (AST), detect code smells, suggest architectural refactoring, and auto-generate comprehensive unit test suites.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Parse Python, JavaScript, and TypeScript source files using tree-sitter and AST parsers.\\n"
            "• Prompt language models with structured code contexts to generate targeted diffs and test cases.\\n"
            "• Build CLI automation commands evaluating code coverage and type safety.\\n"
            "• Collaborate with fellow interns in agile two-week sprint cycles."
        ),
        "skills": "Python, AST Parsing, Code Analysis, Git, CLI Development, PyTest, Tree-Sitter",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    13: {
        "title": "Knowledge-Base Engineering & Hybrid RAG Intern — Pune / Remote",
        "description": "Focus on high-accuracy enterprise knowledge retrieval. You will implement hybrid search architectures combining BM25 keyword matching with dense vector embeddings and cross-encoder rerankers, eliminating retrieval blind spots for complex technical documentation.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Build hybrid search pipelines combining dense embeddings (pgvector) with sparse BM25 indices.\\n"
            "• Integrate cross-encoder rerankers (Cohere Rerank / BGE-Reranker) to boost top-3 retrieval precision.\\n"
            "• Test retrieval quality on real-world technical documentation manuals.\\n"
            "• Publish project benchmarks and earn verified academic evaluation credentials."
        ),
        "skills": "Python, Hybrid Search, BM25, pgvector, Cross-Encoders, RAG, Information Retrieval",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    14: {
        "title": "AI Lead Qualification & CRM Automation Bot Intern — Mumbai / Remote",
        "description": "Build high-conversion conversational lead qualification bots for B2B enterprises. You will design dialogue trees that engage prospective candidates, collect qualification criteria, answer FAQs, and record verified lead profiles directly into CRM databases.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Develop conversational lead intake bots with real-time phone and email format validation.\\n"
            "• Connect chat engines to backend PostgreSQL databases to record lead statuses atomically.\\n"
            "• Analyze user drop-off points and optimize conversational copy for higher completion rates.\\n"
            "• Submit production-ready modules to partner marketing portals."
        ),
        "skills": "Python, Conversational UX, PostgreSQL, REST APIs, JSON Validation, FastAPI, JavaScript",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    15: {
        "title": "Enterprise AI Microservice Integration Intern — Chennai / Remote",
        "description": "Learn to integrate modern AI capabilities into existing enterprise architectures. You will construct containerized FastAPI microservices that wrap AI models, handle asynchronous queue processing, and communicate via secure internal REST APIs.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Develop modular FastAPI microservices packaged into production Docker containers.\\n"
            "• Implement Redis message queues to decouple high-latency AI inference from synchronous API calls.\\n"
            "• Write comprehensive automated API tests validating error codes and latency thresholds.\\n"
            "• Deploy and verify service endpoints on Ubuntu Linux staging servers."
        ),
        "skills": "Python, FastAPI, Docker, Redis, Microservices, REST APIs, Linux, PostgreSQL",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    19: {
        "title": "Business Intelligence & Executive Dashboard Intern (Power BI / SQL) — Remote",
        "description": "Join our Data Analytics incubation cohort to master corporate business intelligence. You will analyze student engagement datasets, write complex SQL aggregations, and build interactive executive dashboards in Power BI and Metabase with verified academic review.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Extract, transform, and aggregate raw database records into clean analytical data models.\\n"
            "• Build interactive Power BI / Metabase dashboards visualizing key business performance indicators.\\n"
            "• Write optimized SQL queries utilizing window functions, subqueries, and table joins.\\n"
            "• Present dashboard findings to academic project mentors during sprint reviews."
        ),
        "skills": "Power BI, SQL, Data Modeling, DAX, Excel, Data Visualization, Metabase",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    20: {
        "title": "Advanced SQL Reporting & Data Cleaning Intern — Remote 2026",
        "description": "Master the art of production SQL data engineering and reporting. You will work on real database instances, cleaning noisy input datasets, authoring performant analytical views, and creating automated data reconciliation scripts in Python and SQL.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Clean and normalize inconsistent customer contact records, phone numbers, and transaction IDs.\\n"
            "• Author analytical SQL views and materialized query tables for high-frequency reporting.\\n"
            "• Write Python reconciliation scripts identifying discrepancies between payment logs and user accounts.\\n"
            "• Maintain high data integrity standards and adhere to strict privacy safeguards."
        ),
        "skills": "SQL (PostgreSQL), Python, Pandas, Data Cleaning, ETL, Database Normalization",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    21: {
        "title": "Power BI & Interactive Analytics Intern (DAX, Modeling & Reports) — Remote",
        "description": "Specialize in Power BI enterprise reporting. You will design star-schema data models, write custom DAX calculated measures, and design clean, accessible report layouts that empower decision-makers to explore multi-year performance trends.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Model relational tables into star and snowflake schemas in Power BI Desktop.\\n"
            "• Write complex DAX measures (Time Intelligence, CALCULATE, FILTER, Ranking) for deep slicing.\\n"
            "• Implement intuitive interactive tooltips, drill-throughs, and bookmark-based view toggles.\\n"
            "• Export and publish verified BI portfolios to demonstrate proof-of-work to recruiters."
        ),
        "skills": "Power BI, DAX, Data Modeling, Star Schema, Business Intelligence, Data Analysis",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    22: {
        "title": "Data Visualization & Exploratory Analysis Intern (Python & Seaborn) — Remote",
        "description": "Translate complex data patterns into compelling visual narratives. You will conduct exploratory data analysis on real incubation datasets, generate publication-ready plots with Seaborn and Matplotlib, and write insightful analytical summaries.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Perform comprehensive exploratory data analysis (EDA) across multi-variable datasets in Jupyter.\\n"
            "• Generate clean, publication-ready data visualizations using Python (Matplotlib, Seaborn, Plotly).\\n"
            "• Calculate statistical correlations, distributions, and outlier metrics across user cohorts.\\n"
            "• Author an analytical project report featured on the DBERT Public Research Portal."
        ),
        "skills": "Python, Pandas, Seaborn, Matplotlib, Plotly, Exploratory Data Analysis, Statistics",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    23: {
        "title": "Growth Marketing & Funnel Analytics Intern (GA4, Mixpanel & CRO) — Remote",
        "description": "Learn modern growth marketing analytics and conversion rate optimization (CRO). You will inspect Google Analytics 4 (GA4) event streams, analyze landing page conversion drop-offs, and design data-backed experimentation roadmaps to maximize user acquisition.",
        "responsibilities": (
            "• Active commitment of at least 10 hours per week with minimum 75% portal attendance.\\n"
            "• Analyze user journey telemetry across public verification and enrollment landing pages.\\n"
            "• Configure and audit GA4 custom dimensions, event tags, and conversion goals.\\n"
            "• Propose and evaluate UX copy and CTA variations to improve visitor-to-applicant conversion rates.\\n"
            "• Compile weekly growth reports detailing organic search traffic, referrals, and CTR trends."
        ),
        "skills": "Google Analytics 4 (GA4), Conversion Rate Optimization (CRO), Funnel Analytics, SEO, Excel",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    }
}

print(f"Total posts queued for update: {len(UPDATES)}")

updated_count = 0
for post_id, data in UPDATES.items():
    query = \"\"\"
        UPDATE dbert_internship.posts
        SET 
            title = %(title)s,
            description = %(description)s,
            responsibilities = %(responsibilities)s,
            skills = %(skills)s,
            eligibility = %(eligibility)s,
            published_at = %(published_at)s,
            apply_by = %(apply_by)s,
            expires_at = %(expires_at)s,
            updated_at = %(updated_at)s
        WHERE id = %(id)s;
    \"\"\"
    params = {
        "id": post_id,
        "title": data["title"],
        "description": data["description"],
        "responsibilities": data["responsibilities"],
        "skills": data["skills"],
        "eligibility": data["eligibility"],
        "published_at": NEW_PUBLISHED_AT,
        "apply_by": NEW_APPLY_BY,
        "expires_at": NEW_EXPIRES_AT,
        "updated_at": NEW_UPDATED_AT
    }
    c.execute(query, params)
    updated_count += 1

conn.commit()
print(f"Successfully committed updates for {updated_count} posts on EC2 PostgreSQL!")

# Verification query
c.execute(\"\"\"
    SELECT id, post_type, title, published_at, apply_by, expires_at 
    FROM dbert_internship.posts 
    WHERE id IN %s 
    ORDER BY id ASC;
\"\"\", (tuple(UPDATES.keys()),))

verified_rows = c.fetchall()
print(f"Verified {len(verified_rows)} rows from database:")
for r in verified_rows[:5]:
    print("  ", r)
print("  ... (all 40 rows verified)")
"""

print("Executing PostgreSQL database updates on production EC2...")
ssh_cmd = ["ssh", "-i", PEM_KEY, "-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes", REMOTE_HOST, "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)
print(f"Update script exit code: {res.returncode}")
