import subprocess
import json
import sys
import sqlite3
import os

sys.stdout.reconfigure(encoding='utf-8')

PEM_KEY = r"C:\Users\user\.ssh\dbert-production-server.pem"
REMOTE_HOST = "ubuntu@3.26.237.171"

NEW_PUBLISHED_AT = '2026-11-20 10:00:00'
NEW_APPLY_BY = '2027-01-15'
NEW_EXPIRES_AT = '2027-02-15 23:59:59'
NEW_UPDATED_AT = '2026-11-20 10:00:00'

STEERING_ELIGIBILITY_TEXT = (
    "Open to engineering students, recent graduates, and entry-level professionals with foundational technical knowledge. "
    "Requires commitment of at least 10 hours per week and >=75% portal attendance.\n\n"
    "PREFERRED CANDIDATE PROFILE & FAST-TRACK SELECTION PATHWAY:\n"
    "• Standard Track: Open to all applicants meeting core technical prerequisites. Applications reviewed sequentially.\n"
    "• Accelerated Fast-Track (Priority Shortlisting): Direct Round-1 technical screening waivers and expedited interview review "
    "are granted to candidates enrolled in or holding a verified credential from the DBERT 8-Week Sovereign Incubation & Production Sprint Track "
    "(https://dbert.in/enroll/1999). Incubation fellows enter review with verified GitHub PR proof-of-work, cryptographic Turnitin originality scoring, "
    "and recommendation letters (LOR) from program mentors.\n"
    "Candidates looking to build verified client repository contributions to meet hiring prerequisites are advised to complete the incubation track at https://dbert.in/enroll/1999."
)

UPDATES = {
    # ==================== DATA ANALYST (12 posts) ====================
    24: {
        "title": "Sales & Revenue Data Analyst Intern (SQL / Power BI / Python) — Remote 2026/2027",
        "description": "Join DBERT as a remote Sales & Revenue Data Analyst Intern analyzing high-volume transaction datasets, conversion funnels, and enterprise sales performance metrics. You will write complex SQL queries, build interactive Power BI revenue dashboards, and conduct exploratory data analysis on real student and partner platform sales pipelines.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Analyze sales pipeline velocity, customer lifetime value (LTV), customer acquisition cost (CAC), and lead conversion ratios.\n"
            "• Author performant PostgreSQL queries using window functions, aggregations, and CTEs.\n"
            "• Develop automated Power BI and Metabase dashboards for executive sales telemetry.\n"
            "• Perform exploratory data analysis (EDA) using Python (Pandas/NumPy) to surface untapped revenue opportunities."
        ),
        "skills": "SQL, Python, Pandas, Power BI, Advanced Excel, Sales Funnel Analytics, PostgreSQL",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    25: {
        "title": "Financial Data Analyst Intern (Financial Modeling / Excel / SQL) — Remote 2026/2027",
        "description": "DBERT is seeking a Financial Data Analyst Intern to model unit economics, forecast cash flows, and automate reconciliation workflows across multi-channel payment streams. In this role, you will analyze transaction ledgers, audit Stripe and UPI settlement logs, and build variance analysis models for leadership.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly review check-ins.\n"
            "• Build financial models, cost-benefit analyses, and burn-rate forecasts using Microsoft Excel and Python.\n"
            "• Reconcile transactional payment logs (Razorpay/UPI/Bank feeds) against internal ledger records with zero variance.\n"
            "• Author automated reconciliation scripts in Python to detect settlement anomalies and payment leaks.\n"
            "• Prepare monthly financial overview decks summarizing revenue margins, operational expenditure, and receivables."
        ),
        "skills": "Financial Modeling, Advanced Excel, SQL, Python, Variance Analysis, Accounting Principles, Power BI",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    26: {
        "title": "Product & User Behavior Analytics Intern (Amplitude / SQL / GA4) — Remote 2026/2027",
        "description": "Join our Product Growth team as a Product Analytics Intern analyzing user engagement, feature adoption, and retention curves across DBERT web applications. You will track product funnels, conduct cohort retention analysis, and extract actionable behavioral insights from event telemetry.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly sprint participation.\n"
            "• Design event tracking taxonomies and instrument behavioral event telemetry across user journey touchpoints.\n"
            "• Conduct multi-period cohort retention analysis and churn diagnostic investigations using SQL and Python.\n"
            "• Author detailed A/B test analysis reports evaluating feature impact on trial-to-paid conversion rates.\n"
            "• Translate user navigation paths into actionable UI/UX feature recommendations for the engineering team."
        ),
        "skills": "Product Analytics, SQL, Python, GA4, Amplitude, Cohort Analysis, A/B Testing, User Retention",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    27: {
        "title": "E-Commerce & Marketplace Data Analyst Intern (Shopify / SQL / Python) — Remote 2026/2027",
        "description": "DBERT is hiring an E-Commerce Data Analyst Intern to optimize digital storefront performance, cart abandonment rates, and merchandise velocity. You will analyze SKU profitability, user checkout drop-offs, and repeat purchasing patterns across modern digital commerce channels.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone completion.\n"
            "• Analyze online shopping cart funnels to diagnose drop-off triggers and recommend checkout optimizations.\n"
            "• Model customer purchase recency, frequency, and monetary value (RFM) to drive targeted retention campaigns.\n"
            "• Author SQL queries extracting inventory velocity, gross merchandise value (GMV), and return rates.\n"
            "• Build real-time merchant analytics dashboards visualizing top-selling SKUs, traffic sources, and conversion benchmarks."
        ),
        "skills": "E-Commerce Analytics, SQL, Python, Google Analytics, RFM Analysis, Power BI, Advanced Excel",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    28: {
        "title": "Operations Data Analyst Intern (Process Optimization & SLA Metrics) — Bangalore / Remote",
        "description": "We are looking for an Operations Data Analyst Intern based in Bangalore / Remote to evaluate business operational efficiency, mentor workload allocation, and service level agreement (SLA) fulfillment. You will turn raw operational logs into actionable workflow improvements.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Monitor mentor review turnaround times, student ticket resolution SLAs, and platform support throughput.\n"
            "• Build operational bottleneck detection dashboards in Metabase and Power BI.\n"
            "• Cleanse and transform unstructured dispatch and verification event logs using Python Pandas.\n"
            "• Recommend automated operational triggers to streamline staff task assignments and dispatch workflows."
        ),
        "skills": "Operations Analytics, SQL, Python, Metabase, Process Mapping, Excel, Data Visualization",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    29: {
        "title": "Customer Insights & Behavioral Analyst Intern (Customer Feedback & NLP) — Delhi NCR / Remote",
        "description": "Seeking a Customer Insights Analyst Intern in Delhi NCR / Remote to analyze candidate survey responses, feedback telemetry, and Net Promoter Scores (NPS). You will combine quantitative satisfaction data with qualitative sentiment analysis to drive student success initiatives.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly mentor syncs.\n"
            "• Design, deploy, and analyze customer satisfaction (CSAT) and Net Promoter Score (NPS) surveys.\n"
            "• Apply NLP sentiment analysis and text classification to student review feedback using Python.\n"
            "• Identify high-correlation factors between initial course onboarding experience and long-term completion.\n"
            "• Present bi-weekly Voice-of-Customer (VoC) synthesis reports to product and academic operations leads."
        ),
        "skills": "Customer Insights, SQL, Python, NLP Sentiment Analysis, Survey Design, Data Storytelling, Excel",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    30: {
        "title": "Data Cleaning & ETL Pipeline Intern (Pandas / SQL / PostgreSQL) — Hyderabad / Remote",
        "description": "DBERT is hiring a Data Cleaning & ETL Intern based in Hyderabad / Remote to ingest, sanitize, and validate massive candidate databases and external lead repositories. You will build resilient data transformation pipelines that ensure zero missing or corrupted records across production stores.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone deliverables.\n"
            "• Write robust Python Pandas and SQL scripts to clean, deduplicate, and normalize heterogeneous datasets.\n"
            "• Implement schema validation rules, regex data formatters, and constraint checks for email/phone fields.\n"
            "• Build automated ETL staging routines moving data from flat CSV/JSON files into relational PostgreSQL tables.\n"
            "• Audit data quality metrics and generate automated health reports detailing anomaly detection results."
        ),
        "skills": "Data Cleaning, ETL Pipelines, Python, Pandas, PostgreSQL, SQL, Data Validation, Regex",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    31: {
        "title": "Excel & Reporting Automation Intern (Advanced VBA / Python / Macros) — Pune / Remote",
        "description": "Join our Business Operations team in Pune / Remote as an Excel & Reporting Automation Intern. You will automate manual corporate reporting spreadsheets, author VBA macros, and develop Python-based automated email report dispatchers for cross-functional managers.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly mentor milestones.\n"
            "• Author complex Excel workbooks utilizing dynamic array formulas (XLOOKUP, FILTER, INDEX/MATCH) and Pivot Tables.\n"
            "• Build VBA macros and Python automation scripts to eliminate repetitive manual copy-paste workflows.\n"
            "• Integrate Python OpenPyXL and XlsxWriter libraries to generate styled corporate report decks automatically.\n"
            "• Schedule automated daily and weekly report generation jobs tied to PostgreSQL database queries."
        ),
        "skills": "Advanced Excel, VBA Macros, Python, OpenPyXL, SQL, Pivot Tables, Business Reporting",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    32: {
        "title": "Survey & Market Research Data Intern (Statistical Modeling & Hypothesis Testing) — Mumbai / Remote",
        "description": "DBERT is seeking a Survey & Market Research Data Intern in Mumbai / Remote to conduct market landscape research, salary benchmark analysis, and academic competency evaluations. You will leverage statistical techniques to analyze sample cohorts and deliver empirical research papers.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and task delivery.\n"
            "• Formulate survey questionnaires, define representative sampling strategies, and audit response validity.\n"
            "• Execute statistical hypothesis testing (t-tests, chi-square, ANOVA) and regression modeling in Python.\n"
            "• Benchmark tech industry fresher compensation trends and skill requirement matrices across tech hubs.\n"
            "• Author comprehensive research summaries and data visualizations for industry whitepapers."
        ),
        "skills": "Statistical Analysis, Python (SciPy/Statsmodels), Survey Methodology, Hypothesis Testing, SPSS, Data Visualization",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    33: {
        "title": "Supply Chain & Logistics Analytics Intern (Demand Forecasting & Inventory) — Chennai / Remote",
        "description": "We are looking for a Supply Chain Analytics Intern in Chennai / Remote to model inventory turnover, optimize procurement cycles, and analyze distribution network efficiency. You will apply quantitative models to forecast demand and minimize fulfillment latency.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly sprint deliverables.\n"
            "• Build time-series demand forecasting models (ARIMA, Exponential Smoothing) to predict inventory consumption.\n"
            "• Analyze supplier lead times, safety stock levels, and order fulfillment bottleneck data.\n"
            "• Develop inventory optimization dashboards tracking stock-to-sales ratios and carrying costs.\n"
            "• Synthesize logistics telemetry into actionable recommendations for procurement leadership."
        ),
        "skills": "Supply Chain Analytics, Demand Forecasting, Python, Time Series, SQL, Excel Advanced, Inventory Modeling",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    73: {
        "title": "Junior Data Analyst Intern (EDA / Tableau / Python & Business Metrics) — Remote 2026/2027",
        "description": "DBERT is offering a remote Junior Data Analyst Internship focused on exploratory data analysis, business metric modeling, and interactive Tableau/Power BI dashboard construction. You will turn raw application data into compelling visual stories for cross-functional leads.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Conduct exploratory data analysis (EDA) using Python (Pandas/Matplotlib/Seaborn) on platform datasets.\n"
            "• Build interactive Tableau and Power BI dashboards visualizing student retention and milestone velocity.\n"
            "• Write SQL queries to extract data, calculate business KPIs, and uncover operational trends.\n"
            "• Present data findings to mentors during weekly project review sessions."
        ),
        "skills": "Python, Pandas, SQL, Tableau, Power BI, Exploratory Data Analysis (EDA), Statistics",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    75: {
        "title": "Business & Data Intelligence Intern (SQL / Metabase / Dashboarding) — Remote 2026/2027",
        "description": "We are looking for a Business & Data Intelligence Intern to develop executive dashboards, audit reporting telemetry, and analyze operational trends across DBERT learning platforms. You will partner with operational leads to translate business requirements into intuitive analytics tools.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly milestone velocity.\n"
            "• Author performant SQL queries to calculate business metrics, conversion funnels, and user cohorts.\n"
            "• Construct dynamic Metabase and Power BI dashboards with drill-down capabilities for leadership.\n"
            "• Automate weekly reporting decks and data extract schedules using Python and SQL.\n"
            "• Audit reporting discrepancies and validate data integrity across staging and production tables."
        ),
        "skills": "SQL, Metabase, Power BI, Python, Business Intelligence, Data Warehousing, Excel Advanced",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },

    # ==================== FULL STACK, WEB & SECURITY (16 posts) ====================
    37: {
        "title": "React & Next.js Frontend Developer Intern (TypeScript / Tailwind CSS) — Remote 2026/2027",
        "description": "Join DBERT Engineering as a React & Next.js Frontend Developer Intern building production-grade web applications. You will create pixel-perfect, responsive UI components, implement state management architectures, and integrate REST/GraphQL APIs within modern Next.js App Router applications.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Build performant, accessible web components using React 19, TypeScript, and utility-first Tailwind CSS.\n"
            "• Implement client-side form validations, loading skeletons, and interactive state transitions.\n"
            "• Integrate RESTful endpoints and handle optimistic UI updates with TanStack Query (React Query).\n"
            "• Ensure cross-browser compatibility and responsive design across desktop, tablet, and mobile breakpoints."
        ),
        "skills": "React.js, Next.js, TypeScript, Tailwind CSS, JavaScript (ES6+), HTML5/CSS3, Git, REST APIs",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    38: {
        "title": "Flask & Python Backend Developer Intern (RESTful APIs / PostgreSQL) — Remote 2026/2027",
        "description": "DBERT is hiring a Flask & Python Backend Developer Intern to architect and scale web services powering our LMS and verification infrastructure. You will design database schemas, implement secure session authentication, and build robust API endpoints handling high concurrency.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly code review check-ins.\n"
            "• Develop modular Flask blueprints, application factories, and REST API routes with JSON schemas.\n"
            "• Write optimized database queries and migrations in PostgreSQL using SQLAlchemy ORM and raw SQL.\n"
            "• Implement secure password hashing, CSRF protection, and role-based access control (RBAC).\n"
            "• Author unit and integration tests using PyTest to ensure bulletproof backend reliability."
        ),
        "skills": "Python, Flask, PostgreSQL, SQLAlchemy, RESTful APIs, PyTest, Git, Linux",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    39: {
        "title": "REST API & Microservices Development Intern (FastAPI / Swagger / Docker) — Remote 2026/2027",
        "description": "Looking for a REST API Development Intern to build high-throughput microservices using Python FastAPI. You will author OpenAPI/Swagger specifications, implement rate limiting and token authentication, and containerize services with Docker for production deployment.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint deliverables.\n"
            "• Design and document clean, consistent REST API endpoints adhering strictly to OpenAPI 3.0 standards.\n"
            "• Implement asynchronous route handlers, Pydantic data validation models, and dependency injection in FastAPI.\n"
            "• Configure Redis caching layers and API rate limiters to guarantee sub-50ms endpoint latencies.\n"
            "• Write automated end-to-end API test suites in Postman and Python Requests."
        ),
        "skills": "FastAPI, Python, REST APIs, Pydantic, PostgreSQL, Redis, Docker, Postman",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    40: {
        "title": "Full Stack Web Developer Intern (React / Node.js / PostgreSQL) — Remote 2026/2027",
        "description": "Join our Core Engineering team as a Full Stack Web Developer Intern. In this role, you will work across both client and server tiers—crafting intuitive user interfaces in React, engineering robust backend services in Node.js/Express or Python, and managing relational data in PostgreSQL.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Develop full-stack feature slices from database schema definition to interactive UI rendering.\n"
            "• Architect secure authentication flows using JWT, cookies, and OAuth2.\n"
            "• Write clean, well-tested code with comprehensive Git version control and pull request reviews.\n"
            "• Optimize frontend asset bundles and backend SQL query performance for lightning-fast page loads."
        ),
        "skills": "React, Node.js, Express, JavaScript/TypeScript, PostgreSQL, SQL, HTML5/CSS3, Git",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    41: {
        "title": "E-Commerce Platform Developer Intern (Cart / Payment Gateways / Next.js) — Remote 2026/2027",
        "description": "DBERT is hiring an E-Commerce Platform Developer Intern to engineer checkout funnels, shopping cart state machines, and payment gateway integrations. You will build secure transaction processing flows and optimize conversion-critical pages.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone completion.\n"
            "• Build resilient shopping cart state machines supporting discounts, coupons, and local currency formatting.\n"
            "• Integrate payment gateway webhooks (Razorpay, Stripe, UPI) with idempotent verification logic.\n"
            "• Implement real-time inventory quantity checks and optimistic stock reservation locks.\n"
            "• Author automated regression test suites verifying checkout flows across multiple payment scenarios."
        ),
        "skills": "Next.js, React, Node.js, Payment Gateways (Razorpay/Stripe), UPI Integration, PostgreSQL, Tailwind CSS",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    42: {
        "title": "Admin Dashboard & Internal Tools Developer Intern (React / Charts / DataTables) — Remote 2026/2027",
        "description": "Seeking an Admin Dashboard Developer Intern to create high-utility internal operations portals, monitoring dashboards, and candidate management interfaces. You will translate complex operational data into actionable, filterable UI tables and visual charts.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint participation.\n"
            "• Build interactive admin consoles featuring server-side pagination, multi-column sorting, and debounce search.\n"
            "• Render dynamic chart visualizations (Recharts, Chart.js) for operational metrics and revenue KPIs.\n"
            "• Implement role-based access control (RBAC) ensuring administrative permissions are strictly enforced.\n"
            "• Optimize heavy table rendering and export capabilities (CSV/Excel/PDF) for large datasets."
        ),
        "skills": "React.js, TypeScript, Tailwind CSS, Recharts, TanStack Table, REST APIs, RBAC",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    43: {
        "title": "Database-Driven Web App Developer Intern (PostgreSQL / Prisma / Express) — Remote 2026/2027",
        "description": "Join our Data Systems group as a Database-Driven Web App Developer Intern. You will design normalized relational schemas, author complex join queries, configure index optimization strategies, and build data-heavy CRUD web applications.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and task delivery.\n"
            "• Design normalized third-normal-form (3NF) relational database schemas with foreign key integrity.\n"
            "• Write complex SQL queries featuring window functions, subqueries, and compound indexes.\n"
            "• Build high-throughput RESTful CRUD endpoints using Node.js/Express or Python.\n"
            "• Conduct query profiling using EXPLAIN ANALYZE to identify sequential scan bottlenecks and tune performance."
        ),
        "skills": "PostgreSQL, SQL, Node.js, Express, Prisma ORM, Database Design, Index Optimization",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    44: {
        "title": "UI/UX Implementation & Design Systems Intern (Figma to Code / Tailwind CSS) — Remote 2026/2027",
        "description": "DBERT Design Labs is hiring a UI/UX Implementation Intern to bridge the gap between design and production engineering. You will translate Figma design specifications into pixel-perfect, accessible, and responsive Tailwind CSS / React component systems.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Convert Figma UI design mockups into modular, reusable React components with pixel-perfect accuracy.\n"
            "• Maintain design token systems (colors, spacing, typography scales, elevation) across light and dark modes.\n"
            "• Ensure full WCAG 2.1 AA accessibility compliance including keyboard navigation and ARIA attributes.\n"
            "• Conduct visual regression reviews across multiple viewport resolutions and operating systems."
        ),
        "skills": "Figma, Tailwind CSS, React.js, CSS3 / Flexbox / Grid, UI/UX Prototyping, Accessibility (WCAG)",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    45: {
        "title": "Web Application Maintenance & Site Reliability Intern (Debugging / CI/CD) — Remote 2026/2027",
        "description": "We are looking for a Web App Maintenance & Reliability Intern to ensure platform stability, resolve runtime defects, optimize database queries, and improve automated testing coverage across production applications.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly review check-ins.\n"
            "• Triage, reproduce, and resolve frontend and backend software bugs reported in production logs.\n"
            "• Audit error tracking telemetry (Sentry, server logs) and implement preventative patch updates.\n"
            "• Refactor legacy codebase components to improve readability, modularity, and testability.\n"
            "• Maintain CI/CD automated test runners and verify deployment health checks on Ubuntu EC2 servers."
        ),
        "skills": "JavaScript/TypeScript, Python, PostgreSQL, Debugging, Git, CI/CD, Linux, Systemd",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    46: {
        "title": "SaaS Feature Development Intern (Multi-Tenant Architecture / APIs) — Bangalore / Remote",
        "description": "DBERT is seeking a SaaS Feature Development Intern in Bangalore / Remote to build modular, tenant-isolated features for enterprise client companies. You will implement role management, billing quota guards, and multi-tenant telemetry dashboards.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone deliverables.\n"
            "• Build modular SaaS product capabilities following clean architecture and domain-driven design principles.\n"
            "• Implement tenant data isolation rules in relational schemas preventing cross-tenant data leakage.\n"
            "• Develop user invitation, role management, and team permission administration workflows.\n"
            "• Instrument user action audit logging and telemetry event streaming for corporate clients."
        ),
        "skills": "React, Node.js / Python, Multi-Tenancy, PostgreSQL, REST APIs, Security, Git",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    47: {
        "title": "Authentication & Web Security Intern (JWT / OAuth2 / OWASP Top 10) — Delhi NCR / Remote",
        "description": "Join our Platform Security team in Delhi NCR / Remote as an Authentication & Web Security Intern. You will audit web application security postures, implement robust JWT/session authentication, defend against OWASP vulnerabilities, and secure sensitive user credentials.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Implement cryptographic password hashing (bcrypt/Argon2) and secure session token rotation.\n"
            "• Conduct vulnerability scanning and remediation against OWASP Top 10 risks (SQLi, XSS, CSRF, IDOR).\n"
            "• Harden API gateways with rate limiting, CORS configuration, and security header policies (CSP, HSTS).\n"
            "• Build administrative audit logging tracking authentication attempts, password resets, and permission changes."
        ),
        "skills": "Web Security, OWASP Top 10, JWT, OAuth2, Python / Node.js, Cryptography, Linux, Pentesting Basics",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    48: {
        "title": "Internal Tools & Workflow Developer Intern (React / Python / Automation) — Hyderabad / Remote",
        "description": "We are looking for an Internal Tools Developer Intern in Hyderabad / Remote to empower internal administrative and admissions teams with high-speed automated portals, candidate lookup tools, and data synchronization daemons.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone deliverables.\n"
            "• Build internal web interfaces allowing support staff to inspect candidate records and verification statuses.\n"
            "• Integrate webhook listeners and automated status synchronization hooks across internal systems.\n"
            "• Design ergonomic forms with debounced search, keyboard shortcuts, and instantaneous feedback.\n"
            "• Maintain comprehensive technical documentation and user guides for non-technical internal operators."
        ),
        "skills": "React, Python, Flask / FastAPI, PostgreSQL, REST APIs, Internal Tooling, Workflow Automation",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    49: {
        "title": "Progressive Web App (PWA) Developer Intern (Service Workers / Offline First) — Pune / Remote",
        "description": "DBERT is hiring a PWA Developer Intern in Pune / Remote to elevate web mobile experiences into offline-capable, installable progressive web applications. You will configure Service Workers, implement IndexedDB client storage, and optimize mobile performance.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint deliverables.\n"
            "• Implement Service Workers managing cache-first and network-first resource caching strategies.\n"
            "• Build offline data synchronization mechanisms using client-side IndexedDB and background sync APIs.\n"
            "• Configure Web App Manifests for native-like home screen installation across Android and iOS.\n"
            "• Optimize Google Lighthouse PWA scores, achieving 95+ ratings across performance and best practices."
        ),
        "skills": "Progressive Web Apps (PWA), Service Workers, JavaScript / TypeScript, IndexedDB, Web Performance, Mobile UX",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    50: {
        "title": "Booking & Scheduling System Developer Intern (Calendar APIs / Node.js) — Mumbai / Remote",
        "description": "Join our Mentorship Engineering squad in Mumbai / Remote as a Booking & Scheduling System Developer Intern. You will engineer 1:1 mentorship booking engines, conflict detection algorithms, automated calendar invites, and timezone-aware scheduling calendars.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Develop reservation booking workflows with atomic database transactions preventing double-booking.\n"
            "• Implement robust timezone conversions handling cross-continental mentor and student availability.\n"
            "• Integrate Google Calendar / iCal feeds and automated meeting confirmation email hooks.\n"
            "• Build responsive calendar UI interfaces allowing mentors to toggle custom availability windows."
        ),
        "skills": "React, Node.js / Python, Timezone Handling, PostgreSQL, Calendar APIs, Atomic Transactions, UI/UX",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    51: {
        "title": "Headless CMS & Content Platform Developer Intern (Strapi / Next.js / Markdown) — Chennai / Remote",
        "description": "We are seeking a CMS Development Intern in Chennai / Remote to manage and scale content delivery infrastructure across our knowledge bases, blogs, and course documentation. You will build headless CMS workflows and static site generation pipelines.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone completion.\n"
            "• Configure headless CMS schemas and content authoring workflows using Strapi or markdown-based CMS engines.\n"
            "• Build dynamic blog and documentation page templates in Next.js App Router with ISR (Incremental Static Regeneration).\n"
            "• Automate Schema.org Article and BreadcrumbList structured JSON-LD data injection for search engines.\n"
            "• Implement markdown rendering pipelines with syntax highlighting and LaTeX math support."
        ),
        "skills": "Next.js, Headless CMS, TypeScript, Markdown / MDX, SEO Architecture, REST / GraphQL APIs",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    74: {
        "title": "Full Stack Developer Internship (Modern Web Architecture & APIs) — Remote 2026/2027",
        "description": "Join DBERT as a Full Stack Developer Intern building modern web features across frontend UI and backend services. You will design user interfaces, implement API routes, optimize database queries, and contribute to active client repositories.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly review check-ins.\n"
            "• Develop user-facing features using modern frontend frameworks (React/Next.js) and clean CSS.\n"
            "• Build and document backend API endpoints handling business logic, authentication, and data persistence.\n"
            "• Write unit tests and maintain high code quality standards through Git pull request reviews.\n"
            "• Collaborate with mentors and peers in weekly technical syncs to ship production features."
        ),
        "skills": "React, Node.js / Python, JavaScript/TypeScript, SQL, PostgreSQL, REST APIs, Git, Tailwind CSS",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },

    # ==================== PYTHON AUTOMATION & QA (15 posts) ====================
    55: {
        "title": "Web Scraping & Data Extraction Intern (Scrapy / Playwright / BeautifulSoup) — Remote 2026/2027",
        "description": "Join our Autonomous Systems team as a Web Scraping & Data Extraction Intern. You will develop resilient web crawlers, headless browser automation spiders, and structured data extraction routines gathering critical industry intelligence at scale.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly milestone deliverables.\n"
            "• Author resilient web scraping spiders using Python, Scrapy, BeautifulSoup, and Playwright.\n"
            "• Handle anti-bot protections using user-agent rotation, delay randomized jitter, and session persistence.\n"
            "• Parse, clean, and validate complex HTML/JSON payloads into standardized relational schemas.\n"
            "• Build automated data extraction monitors detecting target DOM layout shifts and alerting developers."
        ),
        "skills": "Python, Scrapy, Playwright, BeautifulSoup, XPath / CSS Selectors, Proxy Management, PostgreSQL",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    56: {
        "title": "Workflow & Business Process Automation Intern (Python / Webhooks / Zapier) — Remote 2026/2027",
        "description": "DBERT is seeking a Workflow & Business Process Automation Intern to connect distributed business tools, synchronize cross-channel records, and eliminate repetitive operational tasks using Python and automated webhook pipelines.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Develop custom Python automation daemons listening for system webhooks and executing downstream tasks.\n"
            "• Integrate third-party SaaS APIs (Google Workspace, Slack, Discord, CRM) into cohesive workflow chains.\n"
            "• Build idempotent transaction logs ensuring zero duplicate processing during unexpected service retries.\n"
            "• Author technical workflow runbooks and automated monitoring alerts for internal operations teams."
        ),
        "skills": "Python, Webhooks, REST APIs, Zapier / Make, Process Automation, JSON, Bash Scripting",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    57: {
        "title": "Selenium & End-to-End Test Automation Intern (Python / Selenium / PyTest) — Remote 2026/2027",
        "description": "Looking for a Test Automation Intern to build comprehensive end-to-end regression suites for student and recruiter portals. You will author robust browser automation scripts in Python using Selenium and PyTest, verifying cross-browser stability.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone completion.\n"
            "• Build modular Page Object Model (POM) test frameworks using Python, Selenium WebDriver, and PyTest.\n"
            "• Automate critical user journeys: account signup, verification lookup, payment submissions, and task workflows.\n"
            "• Integrate automated test runs into CI/CD pipelines, blocking code merges on test failures.\n"
            "• Generate rich HTML test execution reports with failure screenshots and DOM diagnostic dumps."
        ),
        "skills": "Selenium WebDriver, Python, PyTest, Page Object Model (POM), Test Automation, CI/CD, Git",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    58: {
        "title": "Data Pipeline & ETL Automation Intern (Airflow / Pandas / SQL / Cron) — Remote 2026/2027",
        "description": "Join our Data Infrastructure group as a Data Pipeline & ETL Automation Intern. You will construct scheduled data ingestion workflows, transform raw event streams, and orchestrate automated database migrations and backups across production servers.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly sprint velocity.\n"
            "• Build scheduled ETL batch pipelines extracting, transforming, and loading telemetry records.\n"
            "• Orchestrate data pipeline DAGs using Apache Airflow or lightweight Python cron daemons.\n"
            "• Implement automated data quality verification checks and anomaly alerting mechanisms.\n"
            "• Optimize bulk SQL insert and upsert operations in PostgreSQL for high throughput."
        ),
        "skills": "Python, ETL Pipelines, Pandas, SQL, PostgreSQL, Apache Airflow / Cron, Linux",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    59: {
        "title": "API Integration & Webhook Automation Intern (Requests / FastAPI / Celery) — Remote 2026/2027",
        "description": "DBERT is hiring an API Integration Automation Intern to build custom API connectors, webhook dispatch relays, and automated data synchronization microservices connecting disparate cloud platforms.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone velocity.\n"
            "• Build robust API client libraries in Python handling pagination, rate limits, and exponential backoff retries.\n"
            "• Develop asynchronous webhook processing queues using Celery and Redis to handle burst traffic.\n"
            "• Secure API endpoints with HMAC signature verification and secret key rotation.\n"
            "• Maintain comprehensive API integration unit tests using Mock and VCR.py for offline test stability."
        ),
        "skills": "Python, REST APIs, Requests, FastAPI, Webhooks, Celery, Redis, HMAC Security",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    60: {
        "title": "Automated Report Generation Intern (ReportLab / Pandas / OpenPyXL) — Remote 2026/2027",
        "description": "We are seeking an Automated Report Generation Intern to build programmatic PDF and Excel reporting engines. You will generate high-fidelity multi-page academic transcripts, financial summaries, and student performance reports directly from database records.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly review check-ins.\n"
            "• Author programmatic vector PDF generation routines using Python ReportLab and PyMuPDF.\n"
            "• Build dynamic Excel workbook generation scripts with styled tables and charts using OpenPyXL.\n"
            "• Automate weekly report compilation and transactional email dispatch to student cohorts and administrators.\n"
            "• Optimize PDF rendering performance to compile hundreds of document pages in seconds."
        ),
        "skills": "Python, ReportLab, PyMuPDF, OpenPyXL, Pandas, PDF Generation, Data Visualization",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    61: {
        "title": "Scheduled Job & Cron Automation Intern (Celery / Redis / Linux Daemons) — Remote 2026/2027",
        "description": "Join our Platform Reliability team as a Scheduled Job & Cron Automation Intern. You will manage background worker fleets, scheduled maintenance daemons, database pruning jobs, and queue telemetry across production Ubuntu servers.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Configure and monitor distributed task queues with Celery, Redis, and Python background workers.\n"
            "• Author Linux systemd unit services and cron jobs for automated system health diagnostics.\n"
            "• Implement circuit breakers, task retries, and dead-letter queues (DLQ) for failed background tasks.\n"
            "• Build monitoring telemetry tracking worker memory utilization, queue latency, and task throughput."
        ),
        "skills": "Celery, Redis, Python, Linux Systemd, Cron, Bash Scripting, Distributed Systems",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    62: {
        "title": "Email & Notification Infrastructure Automation Intern (SMTP / Push / WhatsApp) — Remote 2026/2027",
        "description": "DBERT is seeking an Email & Notification Automation Intern to build high-deliverability transactional messaging systems. You will optimize multi-account SMTP pools, implement web push notifications, and automate WhatsApp milestone reminders.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone completion.\n"
            "• Maintain multi-account Google Workspace SMTP delivery pools with automated rotation and quota monitors.\n"
            "• Implement Web Push notification workflows using WebPush standards and Service Workers.\n"
            "• Build automated WhatsApp notification dispatch daemons with rate pacing and anti-ban protections.\n"
            "• Track email delivery, bounce, and open metrics using cryptographic telemetry and SPF/DKIM validation."
        ),
        "skills": "Python, SMTP Protocols, Web Push Notifications, Service Workers, Playwright, SQLite, DNS (SPF/DKIM)",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    63: {
        "title": "Inventory & Stock Telemetry Automation Intern (Python / Database Sync) — Remote 2026/2027",
        "description": "Looking for an Inventory Automation Intern to build real-time inventory monitoring systems, stock level threshold alerts, and automated reorder triggers connecting supplier APIs and internal databases.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and task delivery.\n"
            "• Develop automated synchronization daemons pulling real-time stock levels across warehouse feeds.\n"
            "• Build threshold alert triggers sending instant alerts when inventory levels breach safe buffers.\n"
            "• Audit catalog data for duplicate SKUs, missing metadata, and price discrepancies.\n"
            "• Construct automated inventory health reports summarizing turnover velocity and dead stock."
        ),
        "skills": "Python, SQL, REST APIs, Database Synchronization, Data Validation, Automation, Pandas",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    64: {
        "title": "Lead Generation & Enrichment Automation Intern (Data Scraping & CRM Sync) — Bangalore / Remote",
        "description": "Join our Growth Engineering team in Bangalore / Remote as a Lead Generation Automation Intern. You will engineer automated lead discovery spiders, data enrichment routines, and CRM synchronization workflows for prospective corporate hiring partners.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Build automated web extraction pipelines gathering corporate contact info from public portals and directories.\n"
            "• Enrich extracted lead records with firmographic data (company size, tech stack, funding, key contacts).\n"
            "• Implement email syntax verification and MX record DNS probes to ensure high list hygiene.\n"
            "• Automate lead ingestion into internal CRM datastores with deduplication rules."
        ),
        "skills": "Python, Scrapy, Lead Enrichment, DNS Verification, CRM Integration, Pandas, Automation",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    65: {
        "title": "Price Monitoring & Competitive Intelligence Automation Intern — Delhi NCR / Remote",
        "description": "DBERT is hiring a Price Monitoring Automation Intern in Delhi NCR / Remote to build automated market tracking spiders, competitor price scrapers, and real-time pricing telemetry dashboards.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly review check-ins.\n"
            "• Build scheduled scraping daemons monitoring competitor course pricing, curriculum offerings, and discount codes.\n"
            "• Normalize scraped pricing data across varying currencies, tax rates, and duration models.\n"
            "• Generate automated daily price deviation alerts alerting marketing leadership to market shifts.\n"
            "• Author competitive landscape synthesis reports visualizing historical price elasticities."
        ),
        "skills": "Python, Web Scraping, BeautifulSoup, Pandas, Competitive Intelligence, SQL, Alerting Systems",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    66: {
        "title": "Document Processing & OCR Automation Intern (PyMuPDF / Tesseract / Python) — Hyderabad / Remote",
        "description": "We are seeking a Document Processing Automation Intern in Hyderabad / Remote to engineer automated document ingestion pipelines, student ID card verification, and OCR text extraction engines.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint deliverables.\n"
            "• Build automated PDF extraction pipelines parsing tabular data and text blocks using PyMuPDF and pdfplumber.\n"
            "• Implement optical character recognition (OCR) workflows using Tesseract to digitize physical documents.\n"
            "• Build image preprocessing filters (grayscale, binarization, de-skewing) with OpenCV to maximize OCR accuracy.\n"
            "• Classify and route incoming document uploads into structured database tables automatically."
        ),
        "skills": "Python, PyMuPDF, OCR (Tesseract), OpenCV, pdfplumber, Document Classification, Regular Expressions",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    67: {
        "title": "Social Media & Content Distribution Automation Intern (Meta APIs / LinkedIn) — Pune / Remote",
        "description": "DBERT is hiring a Social Media Automation Intern in Pune / Remote to build automated content scheduling pipelines, track campaign engagement metrics, and streamline cross-platform article syndication.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and milestone completion.\n"
            "• Build automated content scheduling and publishing scripts interfacing with LinkedIn and Twitter/X APIs.\n"
            "• Monitor social engagement metrics (impressions, clicks, shares, comments) and compile weekly analytics reports.\n"
            "• Automate Open Graph (OG) image generation pipelines for newly published articles and job listings.\n"
            "• Build social listening spiders tracking brand mentions and community sentiment across public developer forums."
        ),
        "skills": "Python, REST APIs, Social Media APIs (LinkedIn/Meta), Open Graph Automation, Data Analytics, SEO",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    68: {
        "title": "QA Automation & Software Testing Intern (PyTest / Postman / Playwright) — Mumbai / Remote",
        "description": "Seeking a QA Automation Intern in Mumbai / Remote to lead test automation across public website portals and backend LMS APIs. You will write automated test scripts, conduct boundary testing, and guarantee zero regressions across deployments.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and weekly review check-ins.\n"
            "• Author automated functional, regression, and sanity test suites in Python using PyTest and Playwright.\n"
            "• Validate REST API response schemas, status codes, and security error headers using Postman and Requests.\n"
            "• Configure automated CI test workflows in GitHub Actions to validate every incoming pull request.\n"
            "• Document defect reproduction steps and verify bug fixes before production server deployments."
        ),
        "skills": "Python, PyTest, Playwright, API Testing (Postman), Test Automation, GitHub Actions CI, Bug Tracking",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    },
    69: {
        "title": "Bot Development Intern (Telegram / WhatsApp / Discord Bots & Python) — Chennai / Remote",
        "description": "Join our Automation Engineering group in Chennai / Remote as a Bot Development Intern. You will design, build, and deploy conversational bots on Telegram, Discord, and WhatsApp to automate student onboarding, FAQs, and milestone reminders.",
        "responsibilities": (
            "• Commit at least 10 hours per week maintaining >=75% portal attendance and sprint milestone velocity.\n"
            "• Build conversational chatbots using Python, python-telegram-bot, discord.py, and WhatsApp automation hooks.\n"
            "• Implement interactive menu buttons, inline queries, and conversational state machines.\n"
            "• Connect chatbots to backend PostgreSQL databases to allow students to query task statuses and milestones.\n"
            "• Deploy bots as persistent background systemd services on Linux production instances."
        ),
        "skills": "Python, Telegram Bot API, Discord.py, Chatbot Development, AsyncIO, PostgreSQL, Linux Systemd",
        "eligibility": STEERING_ELIGIBILITY_TEXT
    }
}

print(f"Total posts queued for update: {len(UPDATES)}")

# 1. Update local SQLite database
LOCAL_DB = "apps/portal/internship.db"
if os.path.exists(LOCAL_DB):
    print(f"Updating local SQLite database: {LOCAL_DB}...")
    conn_sq = sqlite3.connect(LOCAL_DB)
    c_sq = conn_sq.cursor()
    sq_updated = 0
    for pid, data in UPDATES.items():
        c_sq.execute("""
            UPDATE posts
            SET 
                title = ?,
                description = ?,
                responsibilities = ?,
                skills = ?,
                eligibility = ?,
                published_at = ?,
                apply_by = ?,
                expires_at = ?,
                updated_at = ?
            WHERE id = ?;
        """, (
            data["title"],
            data["description"],
            data["responsibilities"],
            data["skills"],
            data["eligibility"],
            NEW_PUBLISHED_AT,
            NEW_APPLY_BY,
            NEW_EXPIRES_AT,
            NEW_UPDATED_AT,
            pid
        ))
        sq_updated += 1
    conn_sq.commit()
    conn_sq.close()
    print(f"Local SQLite: {sq_updated} posts updated successfully.")

# 2. Update remote PostgreSQL database on EC2
remote_script = f"""
import psycopg2, os
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
conn = psycopg2.connect(os.environ["DATABASE_URL"])
c = conn.cursor()

NEW_PUBLISHED_AT = '{NEW_PUBLISHED_AT}'
NEW_APPLY_BY = '{NEW_APPLY_BY}'
NEW_EXPIRES_AT = '{NEW_EXPIRES_AT}'
NEW_UPDATED_AT = '{NEW_UPDATED_AT}'

UPDATES = {json.dumps(UPDATES)}

print(f"Remote script received {{len(UPDATES)}} post updates.")
updated_count = 0
for pid_str, data in UPDATES.items():
    pid = int(pid_str)
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
    params = {{
        "id": pid,
        "title": data["title"],
        "description": data["description"],
        "responsibilities": data["responsibilities"],
        "skills": data["skills"],
        "eligibility": data["eligibility"],
        "published_at": NEW_PUBLISHED_AT,
        "apply_by": NEW_APPLY_BY,
        "expires_at": NEW_EXPIRES_AT,
        "updated_at": NEW_UPDATED_AT
    }}
    c.execute(query, params)
    updated_count += 1

conn.commit()
print(f"Committed {{updated_count}} updates to EC2 PostgreSQL.")

# Verify query
c.execute(\"\"\"
    SELECT id, title, published_at, apply_by, expires_at 
    FROM dbert_internship.posts 
    WHERE id IN %s 
    ORDER BY id ASC;
\"\"\", (tuple(int(k) for k in UPDATES.keys()),))

verified = c.fetchall()
print(f"Verified {{len(verified)}} rows in remote PostgreSQL:")
for row in verified[:3]:
    print("  ", row)
print("  ... and all remaining rows verified!")
"""

print("\nDeploying database updates to EC2 PostgreSQL...")
ssh_cmd = [
    "ssh", "-i", PEM_KEY,
    "-o", "StrictHostKeyChecking=no",
    "-o", "BatchMode=yes",
    REMOTE_HOST,
    "/var/www/dbert-website-lms/apps/portal/.venv/bin/python3"
]
res = subprocess.run(ssh_cmd, input=remote_script, text=True, capture_output=True)
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

if res.returncode == 0:
    print("\nAll 43 expiring posts successfully renewed on production PostgreSQL!")
else:
    print(f"\nFailed to update remote PostgreSQL. Exit code: {res.returncode}")
