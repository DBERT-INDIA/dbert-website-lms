# DBERT Comprehensive 9-Domain Curriculum Architecture & Academic Operations Specification
================================================================================
Universal Framework for 2-Month Incubation Fellowships and 3-Month Paid Learner Courses
================================================================================

**Document Version:** 2.4.0  
**Effective Date:** 21 November 2026  
**Governing Authority:** DBERT Technical Council & Academic Operations Board  
**Target Applications:** `apps/website` (Next.js 16 Standalone), `apps/portal` (Flask LMS & Marketplace)  
**Production Server:** `ubuntu@3.26.237.171` (`/var/www/dbert-website-lms`)  
**Active Sovereign Domains:** `https://dbert.in`, `https://lms.dbert.in`, `https://api.dbert.in`  
**Retired Domain Redirection:** `dbert.online` (HTTP 301 Permanent Redirect)  
**GA4 Measurement ID:** Strictly `G-MN7ME9X518`  

---

## 1. Executive Summary & Academic Governance Framework

### 1.1. Pedagogical Mandate & Dual-Track Model
The DBERT engineering ecosystem operates on a fundamental principle: **Proof of Work supersedes credential speculation.** To serve both high-intent engineering fellows seeking verifiable industry pedigree and ambitious learners building foundational systems mastery, the DBERT Technical Council establishes two distinct, non-conflicting academic program structures:

```
                            ┌─────────────────────────────────────────┐
                            │        DBERT ACADEMIC COUNCIL           │
                            │        Curriculum Architecture          │
                            └────────────────────┬────────────────────┘
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼                                                           ▼
    ┌─────────────────────────────┐                             ┌─────────────────────────────┐
    │     STRUCTURE 1: FELLOWSHIP │                             │    STRUCTURE 2: PAID COURSE │
    │ 2 Months (8 Weeks / 56 Days)│                             │    3 Months (12 Weeks / 84) │
    ├─────────────────────────────┤                             ├─────────────────────────────┤
    │ • Target: Active Interns    │                             │ • Target: Career Pivoters   │
    │ • Fee: ₹499 dep + ₹1,500 bal│                             │ • Fee: ₹28,000–₹38,000      │
    │ • Payout: ₹5,000 Stipend    │                             │ • Zero-Cost EMI: 9 Months   │
    │ • 10 hrs/wk logged cadence  │                             │ • 12-15 hrs/wk live + labs  │
    │ • Upstream PR on 4 repos    │                             │ • 2 Production Capstones    │
    │ • 9-Dimension Rubric (100m) │                             │ • 12-Tool Stack Mastered    │
    │ • Turnitin < 5% Originality │                             │ • Verified Systems Diploma  │
    │ • 3-Doc Credential Packet   │                             │ • Direct Venture Placement  │
    └─────────────────────────────┘                             └─────────────────────────────┘
```

1. **Structure 1 — 2-Month Incubation Fellowship (8 Weeks / 56 Calendar Days):**
   - **Mission:** High-velocity sprint incubation. Fellows contribute production code to real-world open-source systems, resolve client issues, and graduate as pre-vetted engineers.
   - **Financial Architecture:** Caution deposit ₹499 (credited in full) + net balance ₹1,500 payable on `/enroll/1999` (Total program fee: ₹1,999).
   - **Stipend Eligibility:** ₹5,000 INR performance stipend released via the 5-Gate Milestone Engine upon verified completion.
   - **Attendance Mandate:** Mandatory 10.0 hours/week logged on the platform attendance daemon, strictly capped at 80.0 total hours for final grading.
   - **Core Deliverable:** Upstream Pull Request (PR) merged or approved on 1 of the 4 official partner repositories, plus a domain-specific production capstone.
   - **Graduation Asset:** 3-Document Credential Packet (Certificate of Completion, Academic Evaluation Dossier with 9-parameter score, and Official Letter of Recommendation) plus promotion to Tab 1 (Pre-Vetted Engineers) on `https://dbert.in/verify/directory`.

2. **Structure 2 — 3-Month Paid Learner Course (12 Weeks / 84 Calendar Days):**
   - **Mission:** Comprehensive systems engineering from fundamental theory to enterprise production. Learners transition from zero to industry-ready software engineers.
   - **Financial Architecture:** Tuition ₹28,000 to ₹38,000 upfront, or Zero-Cost EMI of ₹3,111 to ₹4,222/month across a 9-month tenure.
   - **Instructional Cadence:** 12 to 15 hours/week including synchronous architectural lectures, daily coding labs, and weekly faculty code reviews.
   - **Core Deliverables:** 2 comprehensive production capstone projects (Midterm Capstone at Week 8 and Flagship Capstone at Week 12).
   - **Technology Mastery:** Strictly 12 enterprise tools and frameworks mastered per domain.
   - **Graduation Asset:** DBERT Verified Professional Systems Diploma registered on `https://dbert.in/verify`, ATS-optimized portfolio, and expedited introductions to partner startups and venture funds.

---

### 1.2. Architectural Integration with Monorepo (`apps/website` & `apps/portal`)
The curriculum architecture interfaces seamlessly with existing monorepo components:
- **`apps/website` (Next.js 16 Standalone on Port 3000):**
  - Public catalogue at `/learners/courses` and specialized pages at `/learners/courses/[courseSlug]`.
  - Dynamic verification engine at `/verify/[certId]` rendering live credential packets and Turnitin verification stamps.
  - Pre-vetted talent directory at `/verify/directory` surfacing graduated fellows by 9-dimension rubric scores ($\ge 90$ Top Tier, $\ge 85$ High Merit, $\ge 80$ Proficient).
  - Balance completion gateway at `/enroll/1999` with instant candidate lookup via `/api/enroll/lookup`.
- **`apps/portal` (Flask LMS & Marketplace on Port 5001):**
  - Daily module delivery and multi-stage quiz engine (`apps/portal/config/courses_7day_catalog.py`).
  - Student attendance tracking daemon (`attendance-tracker.js` & `POST /attendance/ping`).
  - Milestone PR submission and validation pipeline (`scripts/audit_33_github_linkedin.py`).
  - Automated PDF credential generator (`apps/portal/services/certificate_packet_service.py`).
  - Candidate offer management and caution deposit ledger (`/portal/offer`).

---

### 1.3. Attendance Daemon, Heartbeat Protocol & Anti-Tamper Engine
To guarantee honest time investment and protect partner engineering integrity, both programs enforce strict telemetry rules:
- **Telemetry Heartbeat:** The LMS client executes `POST /attendance/ping` every 180 seconds while the student actively interacts with course material or task workspaces.
- **Anti-Tamper Gating:**
  - Pings received with $\Delta t < 170$ seconds are rejected with HTTP 429 to prevent bot automation.
  - Inactivity timeout: Heartbeat pauses automatically after 300 seconds of zero DOM mouse/keyboard events.
- **Fellowship Time Ledger:**
  - Standard weekly commitment: Exactly 10.0 hours (600 minutes) per week.
  - Aggregate tenure limit: 80.0 total hours (4,800 minutes) across the 8-week fellowship.
  - Capping Rule: Any time logged beyond 10 hours in a single calendar week rolls into bonus coin points for the Perks Store (`/tasks`) but is strictly capped at 10.0 hours towards the academic completion grade.

---

### 1.4. The 4 Official Partner Repositories & Upstream PR Gating Architecture
Every fellowship candidate must execute production code contributions against one of DBERT's 4 designated partner codebases. Personal forks without upstream PRs are rejected by the CI forensics engine:

| # | Partner Entity | Target Git Repository | Core Architectural Focus | Key Modules & Issue Scopes |
|---|---|---|---|---|
| **1** | **Alkame** | `https://github.com/Alkameinc/alkame-nifty-50-educational` | Quantitative financial modeling, Nifty 50 algorithmic indicators, backtesting engines, time-series anomaly detection. | Feature extraction pipelines, RSI/MACD vectorized indicators, risk dashboards, automated web fetchers. |
| **2** | **Gayatri AI** | `https://github.com/Gayatri-Education/Gayatri-AI` (and companion repos `Gayatri-Tutor-V3`, `gayatribot-Hr`, `Intern-workbench`) | Autonomous pedagogical agents, multi-agent supervisor loops, synthetic LLM fine-tuning data pipelines, HR automation bots. | Supervisor routing networks, LoRA instruction fine-tuning, automated SMTP email daemons, React workbench UI. |
| **3** | **DBERT Agent / Aivara** | `https://github.com/DBERT-INDIA/dbert-agent` (and `Aivara-Technologies/aivara-insight-lite`) | Local-first autonomous AI assistants, Model Context Protocol (MCP) tool clients, arbitrary CSV ingestion, automated PPTX generation. | Ollama/vLLM local runtimes, Pydantic schema validation, driver variance decomposition, python-pptx deck engines. |
| **4** | **Internship Portal** | `https://github.com/DBERT-INDIA/Internshipportal` (and `dbert-website-lms`, `cloud-infra-blueprints`, `secops-audit-suite`) | Production Flask LMS, Next.js App Router verification engines, RFC 8292 VAPID Web Push, Docker/K8s cloud infrastructure, security audits. | Alembic schema migrations, attendance heartbeats, OWASP Top 10 security mitigations, Terraform AWS modules. |

---

### 1.5. Authoritative 9-Dimension Assessment Rubric (100 Marks Total)
Extracted verbatim from production engine `apps/portal/services/certificate_packet_service.py:503`:

| # | Competency Dimension | Specific Evaluation Criteria | Max Marks | Passing Bar |
|---|---|---|:---:|:---:|
| **1** | **Technical Architecture & System Design** | Modular component decoupling, schema normalization, interface contracts, and clean separation of concerns. | **20** | $\ge 16$ |
| **2** | **Code Quality & PEP 8 / Clean Code** | Semantic naming, self-documenting code, type hinting, docstring coverage, and robust error trapping. | **10** | $\ge 8$ |
| **3** | **Core Algorithms & Implementation** | Correctness of domain logic, computational efficiency, algorithmic complexity ($O(n)$ analysis), and proper API usage. | **10** | $\ge 8$ |
| **4** | **Data Integrity, Security & Validation** | Boundary condition enforcement, defensive input sanitation, SQL injection / XSS prevention, and secret masking. | **10** | $\ge 8$ |
| **5** | **Testing & Verification Coverage** | Unit test completeness, mocked integration assertions, edge case coverage, and reproducible test suites ($\ge 80\%$). | **10** | $\ge 8$ |
| **6** | **Project Documentation & Deliverables** | Architecture decision records (ADRs), comprehensive README with local setup guides, API schemas, and sprint logs. | **10** | $\ge 8$ |
| **7** | **Problem Solving & Analytical Agility** | Autonomous debugging, incident mitigation, stack trace analysis, and creative architectural trade-off navigation. | **10** | $\ge 8$ |
| **8** | **Sprint Cadence & Delivery Rigor** | Punctual milestone submissions, consistent Git commit hygiene, honest attendance logging, and standup participation. | **10** | $\ge 8$ |
| **9** | **Code Review & Technical Viva** | Comprehension defense during technical viva with lead architects, live code walkthrough, and trade-off justification. | **10** | $\ge 8$ |
| **TOTAL** | **Cumulative Merit Score** | **Sum across all 9 technical and professional competency vectors** | **100** | **$\ge 80$ (Merit)** |

**Academic Performance Tiers:**
- **90–100 Marks (Grade A+):** Top Tier Distinction. Immediate candidate spotlight on `/hire/pre-vetted-engineers` and highest recommendation tier.
- **80–89 Marks (Grade A):** Merit Status. Verified credential issued; eligible for Gate 1-5 ₹5,000 stipend release; listed on Pre-Vetted Engineers Directory.
- **70–79 Marks (Grade B):** Proficient. Provisional credential awarded; candidate must complete an architectural patch or capstone revision to unlock stipend release.
- **< 70 Marks:** Incomplete / Changes Requested. Mandatory code refactoring and re-evaluation required.

---

### 1.6. 3-Document Credential Packet & Turnitin <5% Verification Architecture
Every graduating engineer is awarded a cryptographic 3-document credential packet:
1. **Document 1: Official Certificate of Completion:**
   - Features unique cryptographic identifier (e.g., `CERT-DBERT-2026-AGNT-042`).
   - Issued under the seal of Digital Blinc Education Research And Technology (DBERT), registered under the MSME Development Act.
   - Embedded QR code deep-linking directly to `https://dbert.in/verify/[certId]`.
2. **Document 2: Academic Evaluation Dossier:**
   - Detailed rubric breakdown displaying the candidate's exact marks across all 9 dimensions.
   - Turnitin Originality Verification Stamp certifying similarity $< 5.0\%$.
   - GitHub pull request verification metadata including commit hashes and target repository links.
3. **Document 3: Official Letter of Recommendation (LOR):**
   - Individualized narrative signed by Lead Architect & Founder Abhinav Sharma.
   - Highlights specific architectural contributions, problem-solving demonstrations, and professional conduct.

---

### 1.7. The 5-Gate ₹5,000 Stipend Release Pipeline
The ₹5,000 INR performance stipend is managed through a strict, auditable 5-gate pipeline:
1. **Gate 1 (Verified Credential Tier):** Candidate must hold a verified credential (`isProvisional: false`, `tier: 'verified'`). Any provisional status requires verification reconciliation.
2. **Gate 2 (Tenure Maturation Timeline):** Payout matures according to:
   $$\text{Maturation Date} = \max(\text{End Date} + 60\text{ days}, \text{2026-12-03})$$
3. **Gate 3 (Encrypted UPI Configuration):** Intern must verify their encrypted UPI Virtual Payment Address (VPA) in their account profile.
4. **Gate 4 (Capstone Deliverables Audit):** Staff and automated scripts verify:
   - Valid PR on 1 of the 4 official partner repositories.
   - Verified DBERT credential added to the candidate's LinkedIn profile under *Licenses & Certifications*.
5. **Gate 5 (Faculty Approval & Atomic Payout):** Upon 80+ rubric approval, 5,000 coins are credited to the candidate's withdrawal ledger $\rightarrow$ Candidate clicks "Request Payout" $\rightarrow$ Direct UPI settlement executed.

---

### 1.8. Paid Learner Course Financial, Diplomas & Talent Matching Framework
- **Master Pricing Table Across 9 Domains:**

| # | Technical Track | Course Code | Upfront Tuition | 9-Month Zero-Cost EMI | Salary Benchmark |
|---|---|---|:---:|:---:|:---:|
| 1 | AI Agent Development | `DBERT-ENG-AGNT-2026` | ₹35,000 | ₹3,888 / mo | ₹5.0 – ₹12.0 LPA |
| 2 | Generative AI & ML Engineering | `DBERT-ENG-GENAI-2026` | ₹34,000 | ₹3,777 / mo | ₹5.5 – ₹15.0 LPA |
| 3 | Full Stack AI Software Engineering | `DBERT-ENG-FSTCK-2026` | ₹38,000 | ₹4,222 / mo | ₹4.0 – ₹10.0 LPA |
| 4 | Data Analytics & Corporate BI | `DBERT-ENG-DATA-2026` | ₹28,000 | ₹3,111 / mo | ₹3.5 – ₹9.0 LPA |
| 5 | Cybersecurity & Threat Defense | `DBERT-ENG-CYBER-2026` | ₹28,000 | ₹3,111 / mo | ₹4.5 – ₹10.5 LPA |
| 6 | DevOps & Cloud Infrastructure | `DBERT-ENG-DEVOPS-2026` | ₹28,000 | ₹3,111 / mo | ₹4.5 – ₹11.0 LPA |
| 7 | Cross-Platform Mobile Engineering | `DBERT-ENG-MOBILE-2026` | ₹28,000 | ₹3,111 / mo | ₹4.0 – ₹9.0 LPA |
| 8 | Python Automation & Scraping | `DBERT-ENG-PYAUT-2026` | ₹28,000 | ₹3,111 / mo | ₹3.5 – ₹8.0 LPA |
| 9 | UI/UX & Product Design Systems | `DBERT-ENG-UIUX-2026` | ₹28,000 | ₹3,111 / mo | ₹3.5 – ₹7.5 LPA |

- **Talent Placement Guarantee:**
  - Candidates completing the 12-week program with score $\ge 85$ enter the DBERT Venture Roster.
  - Direct profile syndication to incubated startups, enterprise partners, and venture capital portfolios.
  - 3 guaranteed technical interviews within 60 days of graduation or 100% tuition refund.

---

## 2. Domain 1: AI Agent Development (`ai-agent-development`)

### 2.1. Domain Overview, Industry Benchmarks & Technical Competencies
AI Agent Development represents the cutting edge of applied artificial intelligence. Engineers in this domain design autonomous systems that combine large language models with persistent state machines, structured tool calling, memory retrieval, and multi-agent coordination.
- **Industry Relevancy:** Rapid transition from static chat interfaces to action-oriented agents executing multi-step business logic across APIs, databases, and operating systems.
- **Starting Salary Benchmark:** ₹5.0 LPA to ₹12.0 LPA (Median: ₹7.8 LPA).
- **Core Frameworks:** LangChain, LangGraph, CrewAI, Ollama, vLLM, OpenAI API, Anthropic Claude, HuggingFace, Pydantic, SQLite, Docker, Model Context Protocol (MCP).

---

### 2.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/DBERT-INDIA/dbert-agent` (Local-first autonomous AI assistant with MCP tool execution).
  - Secondary: `https://github.com/Gayatri-Education/Gayatri-AI` (Multi-agent supervisor routing and deep research).

#### Weekly Sprint Breakdown:
- **Week 1: Runtime Setup, Local LLM Inference & Environment Architecture**
  - *Sprint Goal:* Configure local-first inference runtimes and construct OpenAI-compatible abstraction wrappers.
  - *Deliverables:* Working Python 3.11 virtual environment; LM Studio / Ollama instance running `llama3.2:3b` or `qwen2.5:7b`; unified API client handling streaming responses and latency metrics.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Pass automated test asserting non-blocking local token generation with $<45$ms TTFT (Time To First Token).
- **Week 2: Pydantic Tool Schemas & Guarded Function Calling**
  - *Sprint Goal:* Implement deterministic function-calling pipelines with strict runtime input validation.
  - *Deliverables:* 4 custom tool definitions (Web Search, File System Reader, SQL Runner, Calculator) inheriting from `pydantic.BaseModel`; safety interceptor preventing arbitrary command execution.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Unit tests verifying that malformed tool call arguments trigger self-correcting validation prompts.
- **Week 3: Persistent Episodic Memory & Vector RAG with SQLite**
  - *Sprint Goal:* Architect a local vector memory store for semantic conversation recall.
  - *Deliverables:* Embedding ingestion pipeline using `all-MiniLM-L6-v2`; SQLite database storing chat messages, vector embeddings, and cosine similarity lookup queries.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Execute conversational retrieval test verifying accurate context injection across a 20-turn simulated dialogue.
- **Week 4: Omnichannel Growth & Agentic Evaluation Tasks**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish technical architecture case studies.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub explaining local agent memory architectures; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Multi-Agent State Machine Orchestration (LangGraph / CrewAI)**
  - *Sprint Goal:* Construct a hierarchical multi-agent coordination loop with state persistence.
  - *Deliverables:* State graph featuring Planner, Executor, and Critic nodes; conditional routing edges based on verification outputs; state checkpointing in SQLite.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Multi-turn benchmark where the agent decomposes a complex query, executes 3 tool calls, critiques output, and emits verified answer.
- **Week 6: Model Context Protocol (MCP) Client Integration**
  - *Sprint Goal:* Connect the agent system to standard Model Context Protocol servers for extended OS tool access.
  - *Deliverables:* MCP client adapter communicating over stdio/SSE; seamless invocation of external filesystem and browser tools.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Integration test proving autonomous tool discovery and execution via an external MCP server.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit, refine, and merge an enterprise feature or bugfix against `DBERT-INDIA/dbert-agent`.
  - *Deliverables:* Upstream PR addressing an approved backlog issue (e.g., token usage telemetry, custom tool permission confirmation modal, or Ollama fallback cascade); 100% test pass rate in partner CI.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Peer review sign-off and PR approval by DBERT lead maintainers.
- **Week 8: Capstone Shipment, Technical Viva & Credentialing**
  - *Sprint Goal:* Package the autonomous agent, undergo faculty evaluation, and release credentials.
  - *Deliverables:* Public GitHub repo with comprehensive README, Dockerfile, and architecture diagram; 15-minute live technical defense viva before faculty council.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Autonomous Local-First Multi-Agent System Auditor & Desktop Assistant*
- **Architecture:** Local Python CLI / FastAPI service orchestrating LangGraph state machines, SQLite vector storage, MCP stdio protocol client, and local Ollama inference.
- **Production Criteria:** Zero data leakage (100% local execution), sub-second tool dispatch, complete test suite with $\ge 85\%$ coverage, and clean Docker deployment.

---

### 2.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-AGNT-2026`
- **Tuition Fee:** ₹35,000 Upfront | Zero-Cost EMI: ₹3,888 / month (9 Months).
- **Career Benchmark:** ₹5.0 LPA – ₹12.0 LPA | Roles: AI Agent Engineer, Applied LLM Engineer, Autonomous Systems Developer.
- **Mastered 12-Tool Stack:**
  1. Python 3.11+
  2. LangChain
  3. LangGraph
  4. CrewAI
  5. Ollama
  6. vLLM
  7. OpenAI / Anthropic APIs
  8. Pydantic v2
  9. SQLite (sqlite-vec)
  10. Model Context Protocol (MCP)
  11. Docker
  12. FastAPI

#### 12-Week Comprehensive Syllabus:
- **Week 1: Fundamentals of Autonomous LLM Agents & Local Inference Runtimes**
  - *Concepts:* LLM tokenization, temperature, system prompts, reasoning loops (ReAct pattern), local open-weights models vs cloud APIs.
  - *Assignment:* Benchmark latency and throughput of `llama3.2` on CPU vs GPU using Ollama.
  - *Hands-on Lab:* Build a CLI chat assistant with session history and token count monitoring.
- **Week 2: Structured Outputs & Robust Pydantic Tool Calling**
  - *Concepts:* JSON schema generation, function calling semantics, handling hallucinated tool arguments, Pydantic data validation.
  - *Assignment:* Write a financial calculation tool schema with strict boundary validation and error handling.
  - *Hands-on Lab:* Build an agent that extracts structured tabular data from unstructured news articles into validated Pydantic models.
- **Week 3: Vector Embeddings & Local Retrieval-Augmented Generation (RAG)**
  - *Concepts:* Text chunking strategies (fixed vs recursive vs semantic), vector distance metrics (Cosine, L2, Dot Product), embeddings models.
  - *Assignment:* Build a markdown and PDF document chunker with metadata tagging.
  - *Hands-on Lab:* Implement an in-memory RAG pipeline querying technical documentation with source citation.
- **Week 4: Persistent Conversational Memory & Vector Storage**
  - *Concepts:* Episodic vs semantic memory, sliding window buffers, vector databases (sqlite-vec, Chroma), memory compaction algorithms.
  - *Assignment:* Design a SQLite schema storing chat sessions and vector representations of user preferences.
  - *Hands-on Lab:* Construct a customer support agent that remembers user details across multiple independent sessions.
- **Week 5: Agentic Reasoning Loops: ReAct, Reflexion & Self-Correction**
  - *Concepts:* Thought-Action-Observation loops, chain-of-verification, error analysis, self-reflection mechanisms.
  - *Assignment:* Implement an evaluation harness testing how often an agent detects and repairs its own coding mistakes.
  - *Hands-on Lab:* Build a Python code execution agent that writes, runs, catches syntax errors, and patches its own code.
- **Week 6: Multi-Agent State Machine Architecture with LangGraph**
  - *Concepts:* Directed Acyclic Graphs (DAGs), cyclic state machines, state channels, supervisor vs peer-to-peer topologies.
  - *Assignment:* Model an editorial workflow with Writer, Editor, and Fact-Checker nodes.
  - *Hands-on Lab:* Develop a LangGraph workflow that generates verified research summaries from live web searches.
- **Week 7: CrewAI Hierarchical Task Delegation & Role-Playing Agents**
  - *Concepts:* Agent personas, memory sharing, hierarchical task assignment, inter-agent delegation protocols.
  - *Assignment:* Configure a 3-agent software engineering crew (Product Manager, Coder, QA Engineer).
  - *Hands-on Lab:* Build an automated market research crew that analyzes competitor products and drafts SWOT analysis reports.
- **Week 8: Midterm Capstone Project 1: Enterprise Agentic RAG Platform**
  - *Focus:* Architect, test, and containerize a multi-format document analysis agent with vector search, persistent sessions, and citation validation.
  - *Evaluation:* Faculty code review and test suite execution against unseen edge documents.
- **Week 9: Model Context Protocol (MCP) & OS-Level Automation**
  - *Concepts:* Anthropic MCP architecture, JSON-RPC 2.0 transport over stdio and SSE, tool server development, security sandboxing.
  - *Assignment:* Author a custom MCP server exposing a PostgreSQL database schema and read-only query runner.
  - *Hands-on Lab:* Connect Claude Desktop or custom agent to the custom MCP server for natural language SQL queries.
- **Week 10: Human-in-the-Loop Controls, Safety Guardrails & Token Ceilings**
  - *Concepts:* Interrupt patterns, approval hooks, PII filtering with NeMo Guardrails, cost tracking and daily budget kill-switches.
  - *Assignment:* Implement an approval breakpoint intercepting dangerous operations (file deletion, outbound payment).
  - *Hands-on Lab:* Build a financial assistant that pauses and requests admin confirmation before executing simulated bank transfers.
- **Week 11: Production Deployment, Streaming Responses & Telemetry**
  - *Concepts:* FastAPI backend integration, Server-Sent Events (SSE) streaming, OpenTelemetry tracing for agent runs, Docker packaging.
  - *Assignment:* Instrument an agent workflow with OpenTelemetry to track execution time and token usage per step.
  - *Hands-on Lab:* Build a responsive web interface streaming agent reasoning steps and tool execution status in real time.
- **Week 12: Flagship Capstone Project 2: Distributed Autonomous Operations Platform**
  - *Focus:* Deploy a production-grade multi-agent operations platform capable of autonomous web scraping, data synthesis, report generation, and third-party webhook dispatch.
  - *Evaluation:* Live technical viva defense, comprehensive documentation, and direct interview matching.

---

## 3. Domain 2: Generative AI & Machine Learning Engineering (`generative-ai-ml`)

### 3.1. Domain Overview, Industry Benchmarks & Technical Competencies
Generative AI and Machine Learning engineering spans the entire lifecycle of modern predictive and generative intelligence: from exploratory data analysis and classic supervised algorithms to synthetic data curation, parameter-efficient fine-tuning (PEFT), model quantization, and production inference serving.
- **Industry Relevancy:** Explosive demand for engineers who can fine-tune small specialized language models (SLMs) and deploy private, cost-effective inference pipelines without relying solely on expensive closed-source APIs.
- **Starting Salary Benchmark:** ₹5.5 LPA to ₹15.0 LPA (Median: ₹8.4 LPA).
- **Core Frameworks:** PyTorch, Hugging Face (Transformers, PEFT, Datasets, TRL), Scikit-Learn, LoRA/QLoRA, GGUF, vLLM, LiteLLM, FastAPI, Weights & Biases, Docker.

---

### 3.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/Gayatri-Education/Gayatri-Tutor-V3` (LLM fine-tuning, synthetic data generation, and evaluation).
  - Secondary: `https://github.com/Alkameinc/alkame-nifty-50-educational` (Quantitative machine learning and time-series modeling).

#### Weekly Sprint Breakdown:
- **Week 1: Scientific Computing Core & Feature Pipeline Engineering**
  - *Sprint Goal:* Build reproducible tabular feature extraction pipelines using NumPy and Pandas.
  - *Deliverables:* Vectorized data cleaning scripts; automated handling of missing data, outliers, and categorical encodings; statistical feature correlation matrices.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Execution of data audit script asserting zero data leakage between train and validation splits.
- **Week 2: Classical Machine Learning & Cross-Validation Benchmarks**
  - *Sprint Goal:* Train and benchmark supervised ensemble models (Random Forest, XGBoost, LightGBM).
  - *Deliverables:* Model training pipeline with hyperparameter tuning via Optuna; ROC-AUC, Precision-Recall, and confusion matrix evaluation.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated test verifying that model validation metrics exceed baseline by $>15\%$.
- **Week 3: Deep Learning Foundations & PyTorch Tensor Computations**
  - *Sprint Goal:* Implement custom neural network layers and training loops in pure PyTorch.
  - *Deliverables:* Multi-layer perceptron (MLP) and custom loss functions with automatic differentiation; checkpoint saving and GPU acceleration verification.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Training loss convergence verification on a standard benchmark dataset within 20 epochs.
- **Week 4: Omnichannel Growth & ML Case Study Deliverables**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish open-source model evaluations.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub demonstrating ML model loss curve audits; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Synthetic Instruction Dataset Curation & Tokenization**
  - *Sprint Goal:* Curate and validate high-quality domain-specific instruction datasets for LLM fine-tuning.
  - *Deliverables:* Synthetic QA generation pipeline using structured LLM prompts; filtering heuristics removing low-diversity samples; Hugging Face `Dataset` formatting in Alpaca/ShareGPT schemas.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated dataset schema validation verifying $100\%$ compliance with tokenizer chat templates.
- **Week 6: Parameter-Efficient Fine-Tuning (LoRA & QLoRA)**
  - *Sprint Goal:* Execute a 4-bit quantized LoRA fine-tuning run on a 3B/7B open-weights model (e.g., Llama-3.2 or Qwen-2.5).
  - *Deliverables:* PEFT configuration script specifying target attention modules ($q, k, v, o$ projections); gradient checkpointing and memory optimization; Weights & Biases loss tracking.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of decreasing training loss and absence of catastrophic forgetting on general benchmarks.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit and merge an evaluation or data curation PR on `Gayatri-Education/Gayatri-Tutor-V3`.
  - *Deliverables:* Pull request implementing an automated benchmark evaluator (e.g., ROUGE, BLEU, or LLM-as-a-judge scoring harness) or synthetic dataset generator; partner CI passed.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Maintainer code review approval and PR integration.
- **Week 8: Model Quantization, Production Serving & Technical Viva**
  - *Sprint Goal:* Quantize model weights, build a FastAPI inference server, and defend capstone.
  - *Deliverables:* Conversion of fine-tuned adapter weights to 4-bit GGUF format; high-throughput vLLM/FastAPI serving endpoint; technical viva defense before faculty.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Domain-Adapted Educational SLM with LoRA Fine-Tuning & Quantized Inference API*
- **Architecture:** PyTorch + Hugging Face TRL fine-tuning pipeline, GGUF 4-bit quantization, and high-performance FastAPI/vLLM streaming endpoint with request queuing.
- **Production Criteria:** Training loss curve documented in W&B, quantitative benchmark metrics demonstrating domain lift, sub-100ms latency, and Dockerized deployment.

---

### 3.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-GENAI-2026` / `DBERT-ENG-MLFT-2026`
- **Tuition Fee:** ₹34,000 Upfront | Zero-Cost EMI: ₹3,777 / month (9 Months).
- **Career Benchmark:** ₹5.5 LPA – ₹15.0 LPA | Roles: Generative AI Engineer, Machine Learning Engineer, NLP Engineer.
- **Mastered 12-Tool Stack:**
  1. Python & NumPy / Pandas
  2. PyTorch
  3. Scikit-Learn
  4. Hugging Face Transformers
  5. Hugging Face PEFT & TRL
  6. LoRA / QLoRA
  7. llama.cpp / GGUF
  8. vLLM / LiteLLM
  9. Weights & Biases (W&B)
  10. pgvector / PostgreSQL
  11. FastAPI
  12. Docker

#### 12-Week Comprehensive Syllabus:
- **Week 1: Applied Mathematics, Linear Algebra & Vectorized Data Pipelines**
  - *Concepts:* Matrix operations, eigenvectors, dot products, vector norms, probability distributions, data transformations with NumPy and Pandas.
  - *Assignment:* Implement PCA (Principal Component Analysis) from scratch using NumPy matrix decomposition.
  - *Hands-on Lab:* Build a high-throughput data cleaning pipeline that normalizes continuous metrics and encodes high-cardinality categorical variables.
- **Week 2: Classical Machine Learning & Predictive Modeling**
  - *Concepts:* Bias-variance tradeoff, regularization (L1/L2), decision trees, gradient boosting architectures (XGBoost, LightGBM), cross-validation strategies.
  - *Assignment:* Train and compare Random Forest vs XGBoost models on a customer churn dataset.
  - *Hands-on Lab:* Build a complete Scikit-Learn `Pipeline` with automated feature scaling, imputation, and hyperparameter tuning with GridSearchCV.
- **Week 3: Deep Learning Fundamentals with PyTorch**
  - *Concepts:* Computational graphs, forward/backward passes, gradient descent optimizers (SGD, AdamW), learning rate schedules, loss functions.
  - *Assignment:* Implement a multi-layer perceptron from scratch in PyTorch without using high-level `nn.Sequential`.
  - *Hands-on Lab:* Train a deep neural network on image or text classification with early stopping and model checkpointing.
- **Week 4: Transformer Architecture & Self-Attention Mechanics**
  - *Concepts:* Scaled dot-product attention, multi-head attention, positional encodings, encoder-decoder vs decoder-only models, tokenization.
  - *Assignment:* Write a PyTorch module implementing multi-head self-attention with tensor dimension assertions.
  - *Hands-on Lab:* Dissect and inspect token embeddings and attention weight heatmaps from a pre-trained BERT/GPT model.
- **Week 5: Modern LLM Foundations & Multi-Provider API Orchestration**
  - *Concepts:* Auto-regressive generation, temperature, top-$p$, top-$k$, repetition penalty, LiteLLM unified gateway across OpenAI, Anthropic, and Gemini.
  - *Assignment:* Build a model fallback router that redirects failed API calls across three distinct LLM providers.
  - *Hands-on Lab:* Develop a multi-model benchmarking script comparing latency, cost, and output quality across 5 LLM models.
- **Week 6: Advanced Retrieval-Augmented Generation (RAG) & Hybrid Search**
  - *Concepts:* Dense vector search vs sparse keyword search (BM25), reciprocal rank fusion (RRF), cross-encoder re-ranking, chunking optimizations.
  - *Assignment:* Implement a hybrid search pipeline combining BM25 and pgvector embeddings.
  - *Hands-on Lab:* Build an enterprise knowledge base assistant with document chunking, hybrid retrieval, and re-ranking using Cohere or BGE-Reranker.
- **Week 7: Evaluation Frameworks & LLM-as-a-Judge Metrics**
  - *Concepts:* RAG triad (Faithfulness, Answer Relevance, Context Precision), Ragas evaluation framework, synthetic evaluation dataset generation.
  - *Assignment:* Create a test suite evaluating 50 enterprise Q&A pairs using GPT-4 as an automated judge.
  - *Hands-on Lab:* Run an automated evaluation pipeline that computes precision and recall metrics for a production RAG system.
- **Week 8: Midterm Capstone Project 1: Enterprise Hybrid RAG Knowledge Engine**
  - *Focus:* Architect and deploy a complete enterprise knowledge retrieval engine with hybrid search, re-ranking, session memory, and streaming FastAPI UI.
  - *Evaluation:* Faculty code review and quantitative benchmark against standard retrieval datasets.
- **Week 9: Synthetic Data Generation & Instruction Dataset Engineering**
  - *Concepts:* Instruction-following paradigms, Alpaca vs ShareGPT formats, filtering synthetic data by perplexity and semantic diversity.
  - *Assignment:* Generate 1,000 synthetic technical QA pairs from raw API documentation using structured prompting.
  - *Hands-on Lab:* Build an automated data cleansing script removing duplicates, toxicity, and formatting inconsistencies from training datasets.
- **Week 10: Parameter-Efficient Fine-Tuning (LoRA, QLoRA & Unsloth)**
  - *Concepts:* Low-Rank Adaptation (LoRA) math, 4-bit NormalFloat (NF4) quantization, memory-efficient backpropagation, gradient accumulation.
  - *Assignment:* Configure a QLoRA fine-tuning run targeting Llama-3.2-3B on a single GPU with gradient checkpointing.
  - *Hands-on Lab:* Fine-tune an open-weights model on a proprietary domain dataset, tracking training and validation loss curves in W&B.
- **Week 11: Quantization (GGUF/AWQ) & High-Performance Serving (vLLM)**
  - *Concepts:* Post-training quantization (PTQ), GGUF conversion, PagedAttention, continuous batching, vLLM architecture, OpenAI-compatible servers.
  - *Assignment:* Quantize a fine-tuned model checkpoint into 4-bit and 8-bit GGUF files and benchmark inference memory footprint.
  - *Hands-on Lab:* Deploy a high-throughput vLLM inference server behind an Nginx reverse proxy with token streaming and latency metrics.
- **Week 12: Flagship Capstone Project 2: End-to-End Specialized SLM Fine-Tuning & Production Serving**
  - *Focus:* Deliver an end-to-end production machine learning system: from dataset curation and LoRA fine-tuning to GGUF quantization, vLLM serving, and a live web application.
  - *Evaluation:* Live technical defense viva, comprehensive architecture report, and portfolio review.


---

## 4. Domain 3: Full Stack Development (`full-stack-development`)

### 4.1. Domain Overview, Industry Benchmarks & Technical Competencies
Full Stack Development forms the computational backbone of modern web ecosystems. Engineers in this domain design and build end-to-end architectures: from responsive, server-rendered React/Next.js interfaces to scalable backend APIs, database schemas, authentication systems, and containerized deployments.
- **Industry Relevancy:** Relentless demand for engineers capable of bridging client interactivity, server components, relational databases, and cloud infrastructure without siloed boundaries.
- **Starting Salary Benchmark:** ₹4.0 LPA to ₹10.0 LPA (Median: ₹6.8 LPA).
- **Core Frameworks:** Next.js 16 (App Router), React 19, TypeScript, Node.js, Python (Flask/FastAPI), PostgreSQL, Prisma ORM, Tailwind CSS, Docker, Git, REST & GraphQL, Vercel/EC2.

---

### 4.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/DBERT-INDIA/Internshipportal` (Production Flask LMS, Alembic migrations, session auth, and company directory).
  - Secondary: `https://github.com/Gayatri-Education/Intern-workbench` (React/Next.js intern management workbench).

#### Weekly Sprint Breakdown:
- **Week 1: Modern Frontend Architecture & Next.js App Router Foundations**
  - *Sprint Goal:* Build modern modular user interfaces utilizing React 19 and Next.js 16 App Router.
  - *Deliverables:* TypeScript project setup; Server and Client Component hierarchy; responsive layouts using Tailwind CSS; modular UI component primitives (Button, Modal, Input, DataTable).
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated Lighthouse audit verifying $>90$ Performance and $100$ Accessibility on desktop and mobile viewports.
- **Week 2: Backend API Engineering & Request Validation Pipelines**
  - *Sprint Goal:* Implement RESTful microservices with strict schema validation and error wrapping.
  - *Deliverables:* Flask/FastAPI backend routes; Pydantic/Zod request validation; structured JSON error handlers returning RFC 7807 Problem Details; automated Swagger/OpenAPI documentation.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Integration test suite validating that malformed payloads return HTTP 422 with precise validation error paths.
- **Week 3: Relational Database Modeling & Migration Architecture**
  - *Sprint Goal:* Architect normalized PostgreSQL database schemas and automated migration scripts.
  - *Deliverables:* Entity-relationship modeling; Prisma schema or Alembic migration files; foreign key cascades, unique indexes, and seed scripts with realistic test records.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated migration test verifying error-free upgrade (`db push` / `alembic upgrade head`) and downgrade cycles.
- **Week 4: Omnichannel Growth & Full Stack Case Study Deliverables**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish architectural write-ups.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub demonstrating full-stack schema migrations and performance metrics; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Authentication, Session Security & Role-Based Access Control (RBAC)**
  - *Sprint Goal:* Implement enterprise authentication with JWTs, secure HTTP-only cookies, and RBAC guards.
  - *Deliverables:* Multi-role authentication flow (Candidate, Recruiter, Admin); bcrypt password hashing; JWT token refresh loops; protected route middleware.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Security test asserting that unauthorized requests to admin endpoints return HTTP 403 Forbidden.
- **Week 6: Real-Time Communication & Background Job Processing**
  - *Sprint Goal:* Integrate WebSockets / Server-Sent Events and asynchronous task processing.
  - *Deliverables:* Real-time event notifications using SSE; background task queuing with Celery/Redis for email notifications and PDF generation; live progress indicators in the UI.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* End-to-end test confirming background task execution and real-time status update delivery to the frontend client.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit and merge a production feature or architectural enhancement on `DBERT-INDIA/Internshipportal`.
  - *Deliverables:* Upstream PR addressing an approved portal backlog ticket (e.g., candidate application filtering, automated email notification triggers, or profile completeness checker); full CI pass.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Code review sign-off and merge confirmation by DBERT senior engineers.
- **Week 8: Containerized Deployment, Technical Viva & Credentialing**
  - *Sprint Goal:* Package application into multi-stage Docker images, deploy to cloud staging, and defend capstone.
  - *Deliverables:* Production Dockerfile and `docker-compose.yml`; live staging URL on cloud host; technical viva defense before faculty panel.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Multi-Tenant Enterprise Recruitment, Assessment & Candidate Verification Portal*
- **Architecture:** Next.js 16 App Router frontend + Python Flask REST backend + PostgreSQL database + Redis task queue + Docker Compose multi-service deployment.
- **Production Criteria:** Full CRUD operations across 5 entities, role-based authentication, sub-200ms API response time, $>80\%$ test coverage, and live cloud deployment.

---

### 4.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-FSTCK-2026`
- **Tuition Fee:** ₹38,000 Upfront | Zero-Cost EMI: ₹4,222 / month (9 Months).
- **Career Benchmark:** ₹4.0 LPA – ₹10.0 LPA | Roles: Full Stack Developer, Software Engineer, Frontend/Backend Engineer.
- **Mastered 12-Tool Stack:**
  1. Next.js 16 (App Router)
  2. React 19
  3. TypeScript
  4. Node.js
  5. Python & Flask / FastAPI
  6. PostgreSQL
  7. Prisma ORM / Alembic
  8. Redis & Celery
  9. Tailwind CSS
  10. Docker & Docker Compose
  11. Git & GitHub Actions
  12. Nginx & AWS EC2

#### 12-Week Comprehensive Syllabus:
- **Week 1: Modern Web Architecture, HTML5/CSS3 & TypeScript Foundations**
  - *Concepts:* Browser rendering lifecycle, DOM tree, CSS Flexbox & Grid, TypeScript type systems (interfaces, generics, utility types), modern ECMAScript features.
  - *Assignment:* Refactor a legacy JavaScript codebase into strictly typed TypeScript with zero `any` declarations.
  - *Hands-on Lab:* Build a responsive landing page layout using semantic HTML5, Tailwind CSS, and strict TypeScript interfaces.
- **Week 2: React 19 Core Mechanics, Hooks & Component State**
  - *Concepts:* Virtual DOM, unidirectional data flow, component lifecycle, hooks (`useState`, `useEffect`, `useCallback`, `useMemo`, `useRef`), custom hooks.
  - *Assignment:* Create a reusable custom hook `useDebounce` and `useLocalStorage` with comprehensive unit tests.
  - *Hands-on Lab:* Build an interactive multi-step registration wizard with client-side state persistence and field validation.
- **Week 3: Next.js 16 App Router & Server Components (RSC)**
  - *Concepts:* Server Components vs Client Components, nested layouts, loading skeletons, error boundaries, streaming with Suspense, Server Actions.
  - *Assignment:* Convert a traditional client-side data fetching page into a high-performance React Server Component.
  - *Hands-on Lab:* Build an e-commerce product catalog with instant search, category filtering, and server-side pagination.
- **Week 4: Backend API Engineering with Python (Flask & FastAPI)**
  - *Concepts:* Client-server architecture, REST principles, HTTP verbs, status codes, request routing, middleware, request validation with Pydantic.
  - *Assignment:* Write a complete RESTful API for an applicant tracking system with CRUD endpoints and custom error handling.
  - *Hands-on Lab:* Build an API gateway that routes requests, validates authorization headers, and logs response times.
- **Week 5: Relational Database Modeling with PostgreSQL & Prisma ORM**
  - *Concepts:* Relational schema design, primary/foreign keys, one-to-many, many-to-many relationships, database normalization, indexing strategies.
  - *Assignment:* Design a normalized PostgreSQL schema for a learning management system with course, student, quiz, and certificate tables.
  - *Hands-on Lab:* Execute Prisma schema migrations, write complex join queries, and benchmark query performance with `EXPLAIN ANALYZE`.
- **Week 6: Authentication, Authorization & Security Hardening**
  - *Concepts:* Session-based vs Token-based auth, JWT mechanics, refresh token rotation, bcrypt password hashing, CSRF/XSS protection, CSP headers.
  - *Assignment:* Implement a secure authentication service with email verification, password reset tokens, and rate-limiting.
  - *Hands-on Lab:* Build a role-based dashboard where Admin, Instructor, and Student roles access restricted endpoints and UI components.
- **Week 7: State Management & Complex Data Workflows**
  - *Concepts:* Global state management patterns, Zustand / Redux Toolkit, server state caching with TanStack React Query, optimistic UI updates.
  - *Assignment:* Implement optimistic UI mutations for an interactive task kanban board where items reorder before server confirmation.
  - *Hands-on Lab:* Build an interactive task board with drag-and-drop support, real-time server sync, and offline error recovery.
- **Week 8: Midterm Capstone Project 1: Microservices-Based SaaS API & Dashboard**
  - *Focus:* Architect, test, and containerize a full-stack SaaS administration portal with role-based auth, PostgreSQL storage, and responsive UI.
  - *Evaluation:* Faculty code review and automated test suite execution against functional requirements.
- **Week 9: Asynchronous Background Tasks & Caching with Redis**
  - *Concepts:* In-memory data stores, Redis data structures (Strings, Hashes, Sets), caching strategies (cache-aside, write-through), Celery task workers.
  - *Assignment:* Implement a cache layer that reduces database load for heavy read queries by $>80\%$.
  - *Hands-on Lab:* Build a background job processing worker that queues PDF invoice generation and dispatches email notifications asynchronously.
- **Week 10: Containerization with Docker & Multi-Service Orchestration**
  - *Concepts:* Container virtualization, multi-stage Docker builds, layer caching, container networking, environment variable management, Docker Compose.
  - *Assignment:* Write an optimized multi-stage Dockerfile for Next.js reducing final image size below 150MB.
  - *Hands-on Lab:* Create a `docker-compose.yml` environment coordinating Next.js frontend, Flask backend, PostgreSQL database, and Redis cache.
- **Week 11: Production CI/CD Pipelines & Cloud Deployment (AWS EC2 & Nginx)**
  - *Concepts:* Continuous Integration/Continuous Deployment (CI/CD) with GitHub Actions, SSH automation, Nginx reverse proxy, SSL termination with Certbot.
  - *Assignment:* Build a GitHub Actions workflow that runs automated tests, builds Docker containers, and deploys to a remote server.
  - *Hands-on Lab:* Configure an Nginx reverse proxy on AWS EC2 routing domain traffic to frontend and backend container ports with SSL.
- **Week 12: Flagship Capstone Project 2: Next.js Enterprise LMS & Talent Marketplace**
  - *Focus:* Deliver a production-grade enterprise platform featuring live user authentication, dynamic course catalogs, candidate assessment tests, payment integration, and an administrative analytics portal.
  - *Evaluation:* Live technical defense viva, code quality audit, and direct interview scheduling.

---

## 5. Domain 4: Data Analytics & Corporate Business Intelligence (`data-analytics`)

### 5.1. Domain Overview, Industry Benchmarks & Technical Competencies
Data Analytics and Corporate Business Intelligence engineers transform raw, unstructured enterprise datasets into actionable business insights. Professionals in this track master automated data ingestion, semantic schema classification, driver and variance decomposition, KPI modeling, and executive report automation.
- **Industry Relevancy:** Organizations require automated analytics engines capable of parsing arbitrary enterprise CSVs, classifying business metrics, computing multi-dimensional variance lift, and generating offline executive decks without manual intervention.
- **Starting Salary Benchmark:** ₹3.5 LPA to ₹9.0 LPA (Median: ₹5.8 LPA).
- **Core Frameworks:** Python, Pandas, NumPy, SQL (PostgreSQL, SQLite), Power BI, Metabase, Matplotlib, Seaborn, Plotly, python-pptx, OpenRouter/LLM APIs, Jupyter.

---

### 5.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/Aivara-Technologies/aivara-insight-lite` (Automated CSV ingestion, semantic classification, driver decomposition, and python-pptx deck generation).
  - Secondary: `https://github.com/Alkameinc/alkame-nifty-50-educational` (Time-series analysis and financial metric visualization).

#### Weekly Sprint Breakdown:
- **Week 1: Robust Tabular Ingestion & Encoding Normalization**
  - *Sprint Goal:* Implement fault-tolerant file loaders handling arbitrary enterprise spreadsheets and CSVs.
  - *Deliverables:* Loader utilizing `csv.Sniffer` for automated delimiter detection (comma, tab, semicolon, pipe); charset detection with `charset-normalizer`; header row inference; robust handling of malformed and corrupted rows.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Pass ingestion test suite across 15 real-world messy CSV files with zero uncaught exceptions.
- **Week 2: Semantic Column Classification & Schema Inference Engine**
  - *Sprint Goal:* Build rule-based and LLM-assisted column typing algorithms.
  - *Deliverables:* Classifier identifying Dates, Continuous Metrics, Categorical Dimensions, and Unique Identifiers; fallback LLM classifier for ambiguous business column headers with prompt caching.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Accuracy assertion proving $>95\%$ classification accuracy across standard corporate ERP extracts.
- **Week 3: Local KPI Aggregation & Time-Series Variance Metrics**
  - *Sprint Goal:* Develop automated computation of period-over-period financial and operational KPIs.
  - *Deliverables:* Vectorized aggregation functions in Pandas computing Total Revenue, MoM Delta, YoY Growth, Rolling Averages, and margin ratios.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification that mathematical outputs match double-entry Excel accounting benchmarks within 0.001 tolerance.
- **Week 4: Omnichannel Growth & Analytics Case Study Deliverables**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish business intelligence case studies.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub demonstrating automated variance decomposition; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Driver Decomposition & Explanatory Variance Analysis**
  - *Sprint Goal:* Implement mathematical driver decomposition explaining top factors causing metric movements.
  - *Deliverables:* Algorithmic decomposition calculating categorical contribution shares ("which region/product caused the revenue drop?"); ranking dimensions by explanatory power.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Output validation verifying that cumulative component contributions sum to $100.0\%$ of total variance.
- **Week 6: Automated Executive Slide Deck Generation (python-pptx)**
  - *Sprint Goal:* Generate offline PowerPoint (`.pptx`) presentations populated with dynamic charts and narrative insights.
  - *Deliverables:* PPTX generator module using `python-pptx`; high-res chart rendering via Plotly/Kaleido; standardized corporate slide templates (Title, KPI Bento, Deep-Dive Breakdown, Appendix).
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated slide generation producing valid, uncorrupted `.pptx` files rendering properly in Microsoft PowerPoint.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit and merge an analytical module on `Aivara-Technologies/aivara-insight-lite`.
  - *Deliverables:* Upstream PR implementing an automated anomaly detection module (IQR / Z-score outliers) or chart rendering enhancement; partner CI passed.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Maintainer review approval and PR integration.
- **Week 8: Capstone Shipment, Technical Viva & Credentialing**
  - *Sprint Goal:* Deliver the complete automated analytics platform, defend architecture, and graduate.
  - *Deliverables:* Public GitHub repository with CLI/Web interface, sample dataset runs, unit tests, and comprehensive documentation; technical viva defense before faculty.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Aivara-Class Automated Enterprise CSV Ingestion, Driver Decomposition & Executive PPTX Generator*
- **Architecture:** Python 3.11 engine + Pandas analytics core + Plotly data visualizer + python-pptx slide builder + budget-capped LLM fact-packet insight generator.
- **Production Criteria:** Ingests arbitrary CSV in $<2$ seconds, automatically classifies columns, detects anomalies, generates a 6-slide executive deck, and requires zero external database dependencies.

---

### 5.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-DATA-2026`
- **Tuition Fee:** ₹28,000 Upfront | Zero-Cost EMI: ₹3,111 / month (9 Months).
- **Career Benchmark:** ₹3.5 LPA – ₹9.0 LPA | Roles: Data Analyst, BI Developer, Business Analytics Specialist.
- **Mastered 12-Tool Stack:**
  1. Python 3.11+
  2. Pandas
  3. NumPy
  4. SQL (PostgreSQL & SQLite)
  5. Microsoft Power BI
  6. Metabase
  7. Plotly & Seaborn
  8. python-pptx
  9. Excel Advanced (Power Query, DAX)
  10. Streamlit
  11. Git & GitHub
  12. Docker

#### 12-Week Comprehensive Syllabus:
- **Week 1: Advanced Business Excel, Data Modeling & Power Query**
  - *Concepts:* Keyboard shortcuts, structured tables, nested lookups (XLOOKUP, INDEX/MATCH), Power Query ETL transformations, data cleansing workflows.
  - *Assignment:* Clean, transform, and merge three disconnected multi-currency sales tables using Power Query.
  - *Hands-on Lab:* Build a financial balance sheet model with dynamic sensitivity tables and automated variance formulas.
- **Week 2: Relational Database Querying with SQL Fundamentals**
  - *Concepts:* SELECT queries, WHERE filters, ORDER BY, GROUP BY aggregations, HAVING clauses, string manipulation, date arithmetic.
  - *Assignment:* Write SQL queries calculating customer purchase frequency and average basket size from an orders database.
  - *Hands-on Lab:* Set up a local PostgreSQL database, seed enterprise tables, and solve 20 complex business data extraction problems.
- **Week 3: Advanced SQL: Joins, Subqueries & Window Functions**
  - *Concepts:* INNER/LEFT/FULL joins, correlated subqueries, Common Table Expressions (CTEs), Window functions (`ROW_NUMBER`, `RANK`, `LEAD`, `LAG`, `PARTITION BY`).
  - *Assignment:* Author a CTE pipeline calculating 30-day rolling customer retention and cohort churn rates.
  - *Hands-on Lab:* Build a sales leaderboard query ranking sales representatives within their respective geographical territories.
- **Week 4: Python for Data Analysis: NumPy & Pandas Foundations**
  - *Concepts:* NumPy arrays, vectorized calculations, Pandas Series and DataFrames, indexing, filtering, handling null values, merging and concatenating datasets.
  - *Assignment:* Vectorize an existing slow iterative loop in Python using NumPy and Pandas, demonstrating a $>50\times$ speedup.
  - *Hands-on Lab:* Ingest and clean a 100,000-row enterprise customer dataset, standardizing phone numbers, addresses, and transaction amounts.
- **Week 5: Exploratory Data Analysis (EDA) & Statistical Visualization**
  - *Concepts:* Summary statistics (mean, median, mode, IQR, standard deviation), distribution shapes, skewness, correlation matrices, Matplotlib, Seaborn.
  - *Assignment:* Conduct an end-to-end EDA on an e-commerce transactions dataset, identifying top buying behaviors and seasonal trends.
  - *Hands-on Lab:* Build an interactive exploratory visualization notebook featuring distribution histograms, box plots, and heatmaps.
- **Week 6: Interactive Dashboard Engineering with Power BI & DAX**
  - *Concepts:* Power BI data modeling (Star vs Snowflake schemas), DAX formulas (`CALCULATE`, `FILTER`, `ALL`, `DATESYTD`), interactive slicers, cross-filtering.
  - *Assignment:* Build a comprehensive executive sales performance dashboard in Power BI tracking revenue, gross margins, and customer acquisition costs.
  - *Hands-on Lab:* Configure row-level security (RLS) in Power BI restricting regional managers to their assigned territories.
- **Week 7: Open-Source BI with Metabase & Self-Hosted Analytics**
  - *Concepts:* Self-hosted business intelligence, Metabase setup with Docker, SQL query questions, pulse notifications, automated dashboard email delivery.
  - *Assignment:* Construct an automated daily revenue pulse that queries PostgreSQL and sends summary Slack/Email alerts.
  - *Hands-on Lab:* Deploy Metabase in a Docker container connected to PostgreSQL, creating a multi-card operational control dashboard.
- **Week 8: Midterm Capstone Project 1: High-Frequency Financial Market Analytics Platform**
  - *Focus:* Ingest historical financial time-series data, compute technical indicators (RSI, Moving Averages, Volatility), and build an interactive Plotly dashboard.
  - *Evaluation:* Faculty code review and quantitative validation against benchmark financial indices.
- **Week 9: Automated Tabular Ingestion & Semantic Classification**
  - *Concepts:* Automated format detection, delimiter inference (`csv.Sniffer`), encoding handling, rule-based column typing, regex pattern matching for IDs/Dates.
  - *Assignment:* Write an error-resilient CSV parser that handles unquoted delimiters, newline characters inside fields, and corrupted headers.
  - *Hands-on Lab:* Build a Python package that ingests an arbitrary tabular file and outputs a validated JSON schema specification.
- **Week 10: Statistical Driver & Variance Decomposition**
  - *Concepts:* Explanatory variance analysis, categorical contribution lift, baseline comparison, waterfall charts, dimension attribution modeling.
  - *Assignment:* Implement a driver decomposition function that identifies the exact products responsible for a $15\%$ drop in quarterly profit.
  - *Hands-on Lab:* Build an interactive Streamlit application that renders interactive Plotly waterfall charts explaining business variance.
- **Week 11: Programmatic Slide Deck Automation with python-pptx**
  - *Concepts:* Programmatic presentation construction, slide layout coordinates, shape positioning, embedding high-res charts, automated text formatting.
  - *Assignment:* Author a Python script that takes a Pandas DataFrame and exports a formatted 5-slide PowerPoint deck.
  - *Hands-on Lab:* Build an automated reporting pipeline that triggers weekly, pulls updated database numbers, and emails an executive `.pptx` deck.
- **Week 12: Flagship Capstone Project 2: Automated Enterprise BI & Executive Narrative Platform**
  - *Focus:* Deliver an enterprise analytics application that accepts arbitrary CSVs, classifies columns, detects anomalies, decomposes drivers, and outputs both an interactive Streamlit dashboard and an offline PowerPoint deck.
  - *Evaluation:* Live technical defense viva, code quality audit, and direct venture interview matching.

---

## 6. Domain 5: Cybersecurity & Threat Defense (`cybersecurity`)

### 6.1. Domain Overview, Industry Benchmarks & Technical Competencies
Cybersecurity and Threat Defense engineers protect computational infrastructure from malicious compromise. Professionals in this domain master vulnerability assessment, penetration testing, network traffic analysis, STRIDE threat modeling, OWASP Top 10 web vulnerabilities, Security Operations Center (SOC) incident response, and security compliance.
- **Industry Relevancy:** Escalating enterprise cyber threats demand engineers with practical offensive security auditing and defensive log analysis skills rather than abstract theoretical awareness.
- **Starting Salary Benchmark:** ₹4.5 LPA to ₹10.5 LPA (Median: ₹7.2 LPA).
- **Core Frameworks:** Wireshark, Nmap, Burp Suite Community/Pro, Metasploit, OWASP ZAP, Wazuh SIEM, Splunk, Linux Hardening, Python Scapy, CVSS Scoring.

---

### 6.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/DBERT-INDIA/secops-audit-suite` (Automated vulnerability scanning, SIEM log analysis, and OWASP playbooks).
  - Secondary: `https://github.com/DBERT-INDIA/Internshipportal` (Security subsystem audit and authentication hardening).

#### Weekly Sprint Breakdown:
- **Week 1: Threat Modeling & Defensive Linux Hardening**
  - *Sprint Goal:* Apply STRIDE threat modeling to modern web architectures and execute Linux server security hardening.
  - *Deliverables:* STRIDE threat matrix analyzing authentication and data flow vectors; Linux hardening script configuring SSH keys, disabling root login, configuring UFW firewall rules, and setting up Fail2ban.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Execution of automated Lynis security audit script demonstrating a security index $>80$.
- **Week 2: Network Reconnaissance & Port Enumeration with Nmap**
  - *Sprint Goal:* Conduct network surface discovery and service version enumeration.
  - *Deliverables:* Scripted Nmap scan templates (SYN stealth, version detection, NSE vulnerability scripts); network topology map identifying exposed attack vectors.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Successful identification and reporting of intentionally introduced vulnerable services on a controlled local lab target.
- **Week 3: Deep Packet Inspection & Traffic Analysis with Wireshark**
  - *Sprint Goal:* Analyze raw network PCAP files to identify malicious traffic patterns and credential leaks.
  - *Deliverables:* Wireshark display filter cheat sheet; analysis report identifying unencrypted credentials, ARP spoofing, and DNS exfiltration patterns from capture files.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Extraction of a simulated exfiltrated payload from a raw PCAP capture file.
- **Week 4: Omnichannel Growth & Security Case Study Deliverables**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish security vulnerability assessments.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub demonstrating OWASP Top 10 remediation strategies; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Web Application Penetration Testing: Injection & Broken Access Control**
  - *Sprint Goal:* Audit web applications against OWASP Top 10 vulnerabilities (SQLi, XSS, IDOR/BOLA).
  - *Deliverables:* Burp Suite request/response logs demonstrating SQL injection bypass; exploitation proof-of-concept for IDOR vulnerability; corresponding remediation code patches.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Execution of unit assertions verifying that patched backend code rejects malicious payloads with HTTP 400/403.
- **Week 6: SIEM Log Analysis & SOC Incident Response Playbooks**
  - *Sprint Goal:* Configure centralized log aggregation and write detection rules for security incidents.
  - *Deliverables:* SIEM detection rules (Wazuh/Elastic) identifying brute-force SSH attacks, privilege escalation, and suspicious outbound connections; incident response triage playbook.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Live simulation verifying that triggering 5 failed login attempts raises an automated alert in the SIEM dashboard within 10 seconds.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit and merge a security patch or audit module on `DBERT-INDIA/secops-audit-suite`.
  - *Deliverables:* Upstream PR implementing an automated CVSS v3.1 calculator or an automated dependency vulnerability scanner; partner CI passed.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Maintainer security code review sign-off and PR merge.
- **Week 8: Capstone Shipment, Technical Viva & Credentialing**
  - *Sprint Goal:* Deliver the comprehensive penetration test report and vulnerability audit suite, defend findings in viva, and graduate.
  - *Deliverables:* Executive vulnerability remediation report with CVSS scoring and remediation code; public GitHub repository; technical viva defense before faculty.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Automated Web Application Vulnerability Scanner & CVSS Remediation Suite*
- **Architecture:** Python 3.11 CLI scanner + Burp Suite / OWASP ZAP API integration + Nmap wrapper + CVSS v3.1 scoring engine + automated Markdown/PDF executive report generator.
- **Production Criteria:** Scans target lab URLs safely, flags top OWASP vulnerabilities, assigns standardized CVSS scores, suggests patch code, and produces zero false crashes.

---

### 6.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-CYBER-2026`
- **Tuition Fee:** ₹28,000 Upfront | Zero-Cost EMI: ₹3,111 / month (9 Months).
- **Career Benchmark:** ₹4.5 LPA – ₹10.5 LPA | Roles: Security Analyst, SOC Analyst, Junior Penetration Tester, Cybersecurity Consultant.
- **Mastered 12-Tool Stack:**
  1. Linux (Kali / Ubuntu Server)
  2. Wireshark
  3. Nmap
  4. Burp Suite Community
  5. OWASP ZAP
  6. Metasploit Framework
  7. Wazuh SIEM
  8. Python (Scapy, Requests, Cryptography)
  9. SQLMap
  10. Hashcat & John the Ripper
  11. Git & GitHub
  12. Docker

#### 12-Week Comprehensive Syllabus:
- **Week 1: Information Security Principles, CIA Triad & Threat Modeling**
  - *Concepts:* Confidentiality, Integrity, Availability (CIA), Defense-in-depth, STRIDE threat modeling framework, attack surfaces, security policies.
  - *Assignment:* Perform a STRIDE threat model on a fintech payment gateway architecture diagram.
  - *Hands-on Lab:* Configure a virtualized security testing lab using VirtualBox/Docker with an attacking machine and a target server.
- **Week 2: Linux Operating System Security & System Administration**
  - *Concepts:* Linux file permissions (`chmod`, `chown`, SUID/SGID bits), systemd services, process monitoring, PAM authentication, auditing with `auditd`.
  - *Assignment:* Write a Bash script identifying all world-writable files and non-standard SUID binaries on a Linux host.
  - *Hands-on Lab:* Hardening a Linux server: disable insecure services, configure UFW firewall rules, and set up SSH public key authentication.
- **Week 3: Computer Networking & Packet Inspection with Wireshark**
  - *Concepts:* OSI model vs TCP/IP stack, IP addressing, subnetting, TCP 3-way handshake, DNS, DHCP, HTTP/HTTPS, ARP protocols.
  - *Assignment:* Capture and dissect a complete TCP handshake and TLS ClientHello packet in Wireshark.
  - *Hands-on Lab:* Analyze a network capture file containing a simulated Man-in-the-Middle (MitM) ARP poisoning attack.
- **Week 4: Network Reconnaissance, Port Scanning & Enumeration with Nmap**
  - *Concepts:* Host discovery techniques, TCP connect vs SYN stealth scans, UDP scanning, OS fingerprinting, Nmap Scripting Engine (NSE).
  - *Assignment:* Write a custom Nmap NSE script that checks for the presence of default HTTP administrative credentials.
  - *Hands-on Lab:* Execute comprehensive network scans against a target lab network, cataloging all active hosts, open ports, and service banners.
- **Week 5: Applied Cryptography, Hashing & Public Key Infrastructure (PKI)**
  - *Concepts:* Symmetric encryption (AES-256-GCM), asymmetric encryption (RSA, ECC), cryptographic hashing (SHA-256), HMACs, digital certificates, TLS/SSL.
  - *Assignment:* Implement an end-to-end encrypted file transfer script in Python using the `cryptography` library.
  - *Hands-on Lab:* Set up a private Certificate Authority (CA) using OpenSSL, issue SSL/TLS certificates, and configure HTTPS on a web server.
- **Week 6: Web Application Security: OWASP Top 10 Part 1 (Injections & Auth)**
  - *Concepts:* SQL Injection (in-band, blind, time-based), Command Injection, Cross-Site Scripting (Reflected, Stored, DOM-based), Broken Authentication.
  - *Assignment:* Exploit and subsequently patch a vulnerable login form susceptible to SQL injection and session fixation.
  - *Hands-on Lab:* Intercept and manipulate HTTP requests using Burp Suite to bypass client-side form validation and brute-force passwords.
- **Week 7: Web Application Security: OWASP Top 10 Part 2 (Access Control & SSRF)**
  - *Concepts:* Broken Object Level Authorization (BOLA/IDOR), Server-Side Request Forgery (SSRF), Cross-Site Request Forgery (CSRF), Security Misconfigurations.
  - *Assignment:* Demonstrate an IDOR vulnerability on an API endpoint by accessing another user's private data, then write the RBAC patch.
  - *Hands-on Lab:* Set up and exploit a simulated SSRF vulnerability that forces a backend server to query internal AWS metadata endpoints (`169.254.169.254`).
- **Week 8: Midterm Capstone Project 1: Automated Network Traffic & Intrusion Detection System**
  - *Focus:* Author a Python network monitoring script utilizing `scapy` that detects port scanning, ARP spoofing, and excessive SYN packets, issuing automated alerts.
  - *Evaluation:* Faculty code review and testing against simulated network attack vectors in a private lab.
- **Week 9: Vulnerability Assessment & Automated Scanning with OWASP ZAP**
  - *Concepts:* Active vs passive scanning, crawling dynamic web applications, false-positive filtering, integrating security scans into CI/CD pipelines.
  - *Assignment:* Configure OWASP ZAP to execute an automated security scan against a staging application and export findings.
  - *Hands-on Lab:* Build a GitHub Actions workflow that executes an automated OWASP ZAP baseline scan on every pull request.
- **Week 10: Endpoint Security, Malware Analysis Basics & Privilege Escalation**
  - *Concepts:* Common Windows/Linux privilege escalation vectors (unquoted service paths, cron jobs, sudo misconfigurations), static vs dynamic malware analysis.
  - *Assignment:* Audit a misconfigured Linux virtual machine to escalate privileges from a standard user to root.
  - *Hands-on Lab:* Analyze a suspicious binary in a sandbox environment: inspect strings, calculate hashes, and monitor system calls using `strace`.
- **Week 11: Security Operations Center (SOC) Log Monitoring with Wazuh SIEM**
  - *Concepts:* Centralized log management, syslog, Windows Event Logs, Security Information and Event Management (SIEM), alert correlation, incident response triage.
  - *Assignment:* Write custom Wazuh XML detection rules for detecting brute-force login attempts and privilege escalation events.
  - *Hands-on Lab:* Deploy Wazuh SIEM via Docker, install the Wazuh agent on an endpoint, and investigate simulated security incidents in the dashboard.
- **Week 12: Flagship Capstone Project 2: Enterprise SOC Incident Response & Vulnerability Remediation Platform**
  - *Focus:* Deliver an enterprise vulnerability audit and SOC response platform: perform a full penetration test on a multi-service web application, remediate vulnerabilities, and configure SIEM detection rules to alert on future exploit attempts.
  - *Evaluation:* Live technical defense viva, CVSS-formatted executive report presentation, and direct interview matching.


---

## 7. Domain 6: DevOps & Cloud Infrastructure Engineering (`devops-cloud`)

### 7.1. Domain Overview, Industry Benchmarks & Technical Competencies
DevOps and Cloud Infrastructure engineers automate and stabilize the bridge between application software and resilient production cloud platforms. Engineers in this domain architect infrastructure as code (IaC), containerize microservices, orchestrate Kubernetes clusters, build automated CI/CD pipelines, and maintain 24/7 observability with metrics and logging.
- **Industry Relevancy:** Rapid migration of enterprise workloads to containerized microservices and automated cloud environments demands engineers skilled in declarative infrastructure and automated delivery pipelines.
- **Starting Salary Benchmark:** ₹4.5 LPA to ₹11.0 LPA (Median: ₹7.5 LPA).
- **Core Frameworks:** Docker, Kubernetes (K8s), AWS (EC2, S3, RDS, VPC, IAM), Terraform, GitHub Actions, Linux/Bash, Nginx, Prometheus, Grafana, Helm, ArgoCD.

---

### 7.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/DBERT-INDIA/cloud-infra-blueprints` (Production-ready Terraform configurations, Kubernetes deployment manifests, and GitHub Actions CI/CD workflows).
  - Secondary: `https://github.com/DBERT-INDIA/Internshipportal` (Deployment infrastructure, Nginx configuration, and containerized services).

#### Weekly Sprint Breakdown:
- **Week 1: Linux Systems Administration, Shell Automation & Cloud Networking**
  - *Sprint Goal:* Configure enterprise Linux environments and architect secure cloud VPC topologies.
  - *Deliverables:* Bash automation scripts for server initialization; AWS VPC configuration featuring public/private subnets, Internet Gateways, NAT Gateways, and security groups.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification that instances in private subnets route outbound traffic via NAT while remaining inaccessible from external public IPs.
- **Week 2: Advanced Docker Containerization & Multi-Stage Image Optimization**
  - *Sprint Goal:* Author minimal, production-hardened Docker container images for polyglot applications.
  - *Deliverables:* Multi-stage Dockerfiles for Python/Flask and Node.js/Next.js services; non-root user execution enforcement; Alpine/Distroless base images; `.dockerignore` optimization.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Docker image vulnerability scan with Trivy showing zero Critical or High vulnerabilities and image size $<150$MB.
- **Week 3: Infrastructure as Code (IaC) with HashiCorp Terraform**
  - *Sprint Goal:* Provision modular cloud infrastructure declaratively using Terraform.
  - *Deliverables:* Modular Terraform project (`modules/vpc`, `modules/ec2`, `modules/rds`); remote state management with S3 and DynamoDB state locking; parameterized variables and output schemas.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Successful execution of `terraform plan` and `terraform apply` with zero configuration drift.
- **Week 4: Omnichannel Growth & DevOps Case Study Deliverables**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish cloud infrastructure architecture case studies.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub demonstrating Terraform IaC modularization; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Continuous Integration & Automated Delivery with GitHub Actions**
  - *Sprint Goal:* Construct end-to-end CI/CD pipelines executing tests, building images, and deploying to staging.
  - *Deliverables:* GitHub Actions workflow files (`.github/workflows/deploy.yml`); automated linting, test execution, Docker Hub/ECR image push, and SSH-based remote container restarts.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated pipeline trigger on Git push successfully executing all jobs and reporting green commit status within 5 minutes.
- **Week 6: Kubernetes Container Orchestration & Ingress Management**
  - *Sprint Goal:* Deploy containerized microservices to a local or cloud Kubernetes cluster.
  - *Deliverables:* Declarative Kubernetes manifests (`Deployment`, `Service`, `ConfigMap`, `Secret`, `Ingress`); rolling update deployment strategies; liveness and readiness probe configurations.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Zero-downtime rolling update test confirming continuous service availability during container image revision rollouts.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit and merge an infrastructure or CI/CD module on `DBERT-INDIA/cloud-infra-blueprints`.
  - *Deliverables:* Upstream PR implementing automated Prometheus metric exporters, Helm chart definitions, or Terraform security group audits; partner CI passed.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Maintainer code review approval and PR integration.
- **Week 8: Observability Stack, Technical Viva & Credentialing**
  - *Sprint Goal:* Deploy Prometheus and Grafana monitoring dashboards, defend infrastructure architecture, and graduate.
  - *Deliverables:* Prometheus server scraping container metrics; custom Grafana dashboard tracking CPU/Memory utilization, HTTP request rates, and 5xx error spikes; technical viva defense before faculty.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Production Multi-Tier Cloud Deployment with Terraform, Kubernetes & Prometheus Observability*
- **Architecture:** AWS VPC + EC2/EKS cluster provisioned via Terraform + Next.js frontend & Flask API containerized via Docker + Kubernetes Ingress routing + Prometheus & Grafana monitoring stack.
- **Production Criteria:** 100% reproducible via single command `terraform apply`, automated CI/CD pipeline, zero-downtime rolling updates, live metrics dashboard, and complete architecture documentation.

---

### 7.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-DEVOPS-2026`
- **Tuition Fee:** ₹28,000 Upfront | Zero-Cost EMI: ₹3,111 / month (9 Months).
- **Career Benchmark:** ₹4.5 LPA – ₹11.0 LPA | Roles: DevOps Engineer, Cloud Engineer, Site Reliability Engineer (SRE).
- **Mastered 12-Tool Stack:**
  1. Linux & Bash Shell Scripting
  2. Git & GitHub Actions
  3. Docker & Docker Compose
  4. Kubernetes (kubectl & Minikube/EKS)
  5. Helm Package Manager
  6. HashiCorp Terraform
  7. Amazon Web Services (AWS)
  8. Nginx Reverse Proxy
  9. Prometheus
  10. Grafana
  11. Ansible
  12. ArgoCD (GitOps)

#### 12-Week Comprehensive Syllabus:
- **Week 1: Linux Operating System Mastery & Shell Automation Scripting**
  - *Concepts:* Linux file system hierarchy, process management (`ps`, `top`, `kill`), disk management, networking utilities (`netstat`, `curl`, `ss`), Bash scripting syntax (loops, conditionals, functions).
  - *Assignment:* Author a Bash script that monitors disk usage and automatically cleans up old log files when capacity exceeds $85\%$.
  - *Hands-on Lab:* Build an automated server health audit script that collects CPU, RAM, and network statistics, exporting a structured JSON report.
- **Week 2: Version Control, Advanced Git Workflows & Branching Strategies**
  - *Concepts:* Git internals (blobs, trees, commits), branching models (GitFlow, Trunk-Based Development), rebasing vs merging, resolving conflicts, Git hooks.
  - *Assignment:* Configure pre-commit hooks that automatically run linters and block commits containing hardcoded API keys.
  - *Hands-on Lab:* Simulate a multi-developer merge conflict across 3 branches and execute a clean interactive rebase without losing commit history.
- **Week 3: Containerization Fundamentals with Docker**
  - *Concepts:* Virtual machines vs containers, Linux namespaces and cgroups, Docker architecture, Dockerfile instructions (`FROM`, `RUN`, `COPY`, `CMD`, `ENTRYPOINT`), image layers.
  - *Assignment:* Build a Docker image for a legacy application, optimizing build cache usage to reduce rebuild time from 5 minutes to 15 seconds.
  - *Hands-on Lab:* Containerize a Python web application, run it in a detached container, and test port forwarding and volume persistence.
- **Week 4: Advanced Docker, Multi-Stage Builds & Compose Orchestration**
  - *Concepts:* Multi-stage builds, minimal base images (Alpine, Distroless), non-root container security, Docker Compose service definitions, container networking.
  - *Assignment:* Author a `docker-compose.yml` that coordinates an application frontend, backend API, PostgreSQL database, and Redis cache on an isolated bridge network.
  - *Hands-on Lab:* Execute performance and vulnerability auditing on custom Docker images using Trivy and Docker Slim.
- **Week 5: Continuous Integration (CI) with GitHub Actions**
  - *Concepts:* CI principles, GitHub Actions runners, workflows, jobs, steps, environment secrets, caching dependencies, matrix builds across operating systems.
  - *Assignment:* Build a CI pipeline that runs unit tests across Python 3.10, 3.11, and 3.12, failing if test coverage falls below $80\%$.
  - *Hands-on Lab:* Create an automated pipeline that builds, tags, and pushes multi-architecture Docker images to GitHub Container Registry (GHCR).
- **Week 6: Cloud Computing Foundations with Amazon Web Services (AWS)**
  - *Concepts:* Cloud shared responsibility model, AWS Global Infrastructure (Regions, Availability Zones), IAM users, roles, and policies, EC2 instance types, EBS volumes, S3 storage classes.
  - *Assignment:* Configure an IAM policy enforcing least-privilege access for an automated deployment bot.
  - *Hands-on Lab:* Launch and configure an Ubuntu EC2 instance in AWS, attach an Elastic IP, configure Security Groups, and deploy a secure Nginx web server.
- **Week 7: Cloud Networking, VPCs & High Availability Architecture**
  - *Concepts:* Virtual Private Clouds (VPCs), CIDR subnetting, Public vs Private subnets, Route Tables, Internet Gateways, NAT Gateways, Application Load Balancers (ALB).
  - *Assignment:* Design a multi-AZ VPC architecture accommodating public web servers and isolated private database instances.
  - *Hands-on Lab:* Provision an AWS Application Load Balancer that distributes incoming HTTP traffic across two EC2 instances with health checks.
- **Week 8: Midterm Capstone Project 1: Automated CI/CD Deployment Pipeline to AWS**
  - *Focus:* Architect an automated GitHub Actions pipeline that tests, builds, pushes Docker containers, and deploys to an AWS EC2 instance behind an Nginx reverse proxy with automated SSL.
  - *Evaluation:* Faculty code review and live deployment verification.
- **Week 9: Infrastructure as Code (IaC) with HashiCorp Terraform**
  - *Concepts:* Declarative vs imperative infrastructure, Terraform providers, resources, data sources, state files (`terraform.tfstate`), remote state storage in S3 with DynamoDB locking.
  - *Assignment:* Write Terraform configurations provisioning a complete AWS VPC with subnets and routing tables.
  - *Hands-on Lab:* Refactor monolithic Terraform scripts into reusable modules (`modules/vpc`, `modules/security_groups`, `modules/compute`).
- **Week 10: Container Orchestration with Kubernetes (K8s) Fundamentals**
  - *Concepts:* Kubernetes architecture (Control Plane, Worker Nodes, etcd, kubelet), Pods, Deployments, ReplicaSets, Services (ClusterIP, NodePort, LoadBalancer), Namespaces.
  - *Assignment:* Write Kubernetes YAML manifests deploying a scalable 3-replica web application with health probes.
  - *Hands-on Lab:* Set up a local Minikube/Kind cluster, deploy application pods, simulate pod failures, and observe Kubernetes automated self-healing.
- **Week 11: Advanced Kubernetes: Ingress, ConfigMaps, Secrets & Helm Packaging**
  - *Concepts:* Kubernetes Ingress controllers (Nginx Ingress), ConfigMaps, Secrets management, Helm charts (templates, values.yaml), package publishing.
  - *Assignment:* Create a reusable Helm chart for a microservice with configurable replicas, environment variables, and ingress hosts.
  - *Hands-on Lab:* Deploy an Nginx Ingress Controller routing multiple domain paths to distinct backend Kubernetes services.
- **Week 12: Flagship Capstone Project 2: High-Availability GitOps Kubernetes Cluster on AWS with Full Observability**
  - *Focus:* Deliver a production-grade cloud infrastructure: provision an EKS/K8s cluster via Terraform, configure automated GitOps delivery using ArgoCD, and deploy Prometheus & Grafana dashboards tracking infrastructure metrics.
  - *Evaluation:* Live technical defense viva, failover test execution, and direct interview matching.

---

## 8. Domain 7: Mobile App Development (`mobile-app-development`)

### 8.1. Domain Overview, Industry Benchmarks & Technical Competencies
Mobile Application engineers design, build, and deploy performant cross-platform mobile experiences for iOS and Android devices. Professionals in this domain master reactive UI layouts, client state management, device hardware integration, offline-first data caching, and app store release management.
- **Industry Relevancy:** Consumer and enterprise digital engagement happens predominantly on mobile devices. Companies prioritize cross-platform engineering (Flutter, React Native) to achieve rapid, unified feature delivery across operating systems.
- **Starting Salary Benchmark:** ₹4.0 LPA to ₹9.0 LPA (Median: ₹6.2 LPA).
- **Core Frameworks:** React Native, Flutter & Dart, TypeScript, Firebase (Auth, Firestore, Cloud Messaging), SQLite Mobile, Redux Toolkit / Bloc, REST APIs, Xcode & Android Studio.

---

### 8.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/DBERT-INDIA/mobile-app-workbench` (Cross-platform candidate companion app featuring offline state, camera integration, and push notifications).
  - Secondary: `https://github.com/DBERT-INDIA/Internshipportal` (Mobile API endpoints and student task integration).

#### Weekly Sprint Breakdown:
- **Week 1: Cross-Platform Environment Setup & Mobile UI Layout Mechanics**
  - *Sprint Goal:* Configure mobile development toolchains and implement responsive mobile layouts.
  - *Deliverables:* Configured development environment (React Native CLI or Flutter SDK) with Android Studio emulator; responsive screen layouts implementing Flexbox grid, safe-area viewports, and custom typography scales.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Pixel-perfect verification across multiple screen densities (hdpi, xhdpi, xxhdpi) and aspect ratios.
- **Week 2: Navigation Architectures & Deep Linking Protocols**
  - *Sprint Goal:* Implement multi-tier mobile navigation patterns and URL deep linking.
  - *Deliverables:* Navigation hierarchy combining Native Stack, Bottom Tabs, and Drawer navigators; deep linking configuration allowing external URLs to open specific application screens.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification that tapping an external `dbert://verify/[certId]` link opens the verification screen directly.
- **Week 3: Asynchronous State Management & REST API Data Fetching**
  - *Sprint Goal:* Architect predictable application state management and robust network interaction.
  - *Deliverables:* State store (Redux Toolkit or Bloc/Riverpod); asynchronous API middleware handling pagination, pull-to-refresh, loading states, and network timeouts.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Unit tests proving that failed API calls trigger graceful retry logic and user-friendly error banners without crashing the app.
- **Week 4: Omnichannel Growth & Mobile Engineering Case Studies**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish mobile architecture case studies.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub demonstrating mobile state management and offline synchronization; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Native Device Hardware APIs & Camera Integration**
  - *Sprint Goal:* Integrate native device sensors, camera hardware, and biometric authentication.
  - *Deliverables:* Camera integration allowing image capture and local compression; photo picker with runtime permission handling (Android 14+ / iOS); biometric fingerprint/FaceID login.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Functional verification that capturing an image compresses file size below 500KB before uploading.
- **Week 6: Offline-First Persistence & Background Synchronization**
  - *Sprint Goal:* Implement local SQLite/WatermelonDB storage and background task synchronization.
  - *Deliverables:* Local relational database schema; offline mutation queue caching user actions when disconnected; background synchronization daemon reconciling state upon network reconnection.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Offline test: submit task while in Airplane Mode $\rightarrow$ toggle network on $\rightarrow$ verify automatic background submission to server.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit and merge a mobile module on `DBERT-INDIA/mobile-app-workbench`.
  - *Deliverables:* Upstream PR implementing an offline certificate caching module, biometric auth screen, or push notification listener; partner CI passed.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Maintainer review approval and PR merge.
- **Week 8: Release Bundling, Technical Viva & Credentialing**
  - *Sprint Goal:* Generate production-signed release bundles (AAB / IPA), defend mobile architecture in viva, and graduate.
  - *Deliverables:* Signed Android App Bundle (AAB); release configuration with ProGuard/R8 code shrinking; public GitHub repository; technical viva defense before faculty.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Offline-First Cross-Platform LMS Companion App & Task Submission Engine*
- **Architecture:** React Native / Flutter mobile app + SQLite local database + REST API client + Firebase Cloud Messaging (FCM) + biometric authentication + background sync worker.
- **Production Criteria:** Runs smoothly at 60 FPS, functions completely offline for cached courses, syncs data upon reconnect, signed release bundle $<25$MB, and zero unhandled exceptions.

---

### 8.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-MOBILE-2026`
- **Tuition Fee:** ₹28,000 Upfront | Zero-Cost EMI: ₹3,111 / month (9 Months).
- **Career Benchmark:** ₹4.0 LPA – ₹9.0 LPA | Roles: Mobile App Developer, React Native Developer, Flutter Developer, iOS/Android Engineer.
- **Mastered 12-Tool Stack:**
  1. React Native / Flutter SDK
  2. TypeScript / Dart
  3. Android Studio & Xcode
  4. React Navigation / Flutter Navigator
  5. Redux Toolkit / Bloc State Management
  6. SQLite Mobile / WatermelonDB
  7. Firebase Authentication
  8. Firebase Cloud Messaging (FCM)
  9. Axios / Dio HTTP Client
  10. Jest & React Native Testing Library
  11. Git & GitHub
  12. Fastlane & Google Play Console

#### 12-Week Comprehensive Syllabus:
- **Week 1: Mobile Ecosystem Architecture & Development Toolchains**
  - *Concepts:* Mobile app architecture, native vs hybrid vs cross-platform, bridge architecture vs Flutter engine, Android SDK, Gradle build system, iOS CocoaPods.
  - *Assignment:* Set up a local development environment with Android Studio emulator and configure a new TypeScript/Dart project.
  - *Hands-on Lab:* Build a multi-screen welcome and onboarding UI with responsive SVG illustrations and platform-specific styling.
- **Week 2: Core UI Components, Flexbox & Responsive Layouts**
  - *Concepts:* Layout primitives (View, Text, Image, ScrollView), Flexbox layout algorithm (flexDirection, justifyContent, alignItems), Safe Area Insets, platform-specific code.
  - *Assignment:* Implement a responsive profile screen adapting seamlessly between compact smartphones and large tablets.
  - *Hands-on Lab:* Build an interactive settings screen with toggle switches, grouped list sections, and custom modal dialogs.
- **Week 3: Navigation Systems & Deep Linking Architecture**
  - *Concepts:* Navigation paradigms, Stack navigation, Bottom Tab bars, Modal screens, passing parameters between screens, URI schemes and Universal Links.
  - *Assignment:* Configure a nested navigation structure containing an authentication stack and an authenticated main tab stack.
  - *Hands-on Lab:* Implement deep link routing allowing push notifications or web links to navigate users directly to specific course detail screens.
- **Week 4: Complex Lists, FlatList Virtualization & 60 FPS Performance**
  - *Concepts:* List virtualization, FlatList vs SectionList, windowing algorithms, `keyExtractor`, `getItemLayout`, image caching and lazy loading, memory profiling.
  - *Assignment:* Optimize a slow, lagging list of 5,000 items to scroll smoothly at constant 60 FPS without memory leaks.
  - *Hands-on Lab:* Build an infinite-scrolling social feed featuring pull-to-refresh, skeleton placeholder loaders, and cached network images.
- **Week 5: State Management Architecture (Redux Toolkit / Bloc)**
  - *Concepts:* Application state vs component state, unidirectional data flow, slices, reducers, asynchronous thunks/events, state selectors and memoization.
  - *Assignment:* Build a global shopping cart state store managing item quantities, pricing totals, and coupon code discounts.
  - *Hands-on Lab:* Refactor a prop-drilling application into a clean centralized state store with persistent storage using AsyncStorage / HydratedBloc.
- **Week 6: Networking, REST APIs & Asynchronous Error Handling**
  - *Concepts:* HTTP client configuration, base URLs, interceptors for JWT injection, handling HTTP error codes (401, 403, 500), exponential backoff retries.
  - *Assignment:* Implement an API client interceptor that automatically attempts token refresh upon receiving an HTTP 401 response before re-executing failed requests.
  - *Hands-on Lab:* Connect the mobile app to a live RESTful LMS API, fetching course catalogs, student task lists, and submitting form data.
- **Week 7: Native Device Hardware: Camera, Media & Geolocation**
  - *Concepts:* Mobile permissions model (runtime permissions), camera access, photo compression, file system operations, geolocation coordinates, map rendering.
  - *Assignment:* Build a camera capture component that allows users to capture document photos and compress images before transmission.
  - *Hands-on Lab:* Create an interactive location picker screen displaying nearby tech meetups on a dynamic Google Maps / Mapbox view.
- **Week 8: Midterm Capstone Project 1: Real-Time Chat & Geolocation Native Mobile Application**
  - *Focus:* Architect and deploy a real-time mobile application featuring user authentication, WebSocket chat messaging, camera photo attachments, and interactive maps.
  - *Evaluation:* Faculty code review and testing on both physical mobile devices and emulators.
- **Week 9: Offline-First Data Persistence with SQLite Mobile**
  - *Concepts:* Offline-first design principles, embedded SQLite databases, relational tables, schema migrations, optimistic UI updates, conflict resolution strategies.
  - *Assignment:* Create an offline task manager that allows users to create, edit, and delete tasks while offline, persisting state in SQLite.
  - *Hands-on Lab:* Build an automated synchronization queue that detects network reconnection and syncs local SQLite changes with the backend API.
- **Week 10: Push Notifications with Firebase Cloud Messaging (FCM)**
  - *Concepts:* APNs (Apple Push Notification service), FCM architecture, device registration tokens, foreground vs background notification handlers, notification channels.
  - *Assignment:* Configure Firebase in the mobile project and handle incoming push notifications with custom sound and icon payloads.
  - *Hands-on Lab:* Implement interactive push notifications that display actionable buttons (e.g., "Accept Offer", "Dismiss") directly on the device lock screen.
- **Week 11: Automated Mobile Testing & Fastlane Deployment Automation**
  - *Concepts:* Unit testing with Jest, UI component testing with React Native Testing Library, End-to-End testing with Detox/Maestro, Fastlane release automation.
  - *Assignment:* Write unit tests covering state reducers and integration tests verifying user login form flows.
  - *Hands-on Lab:* Set up Fastlane lanes that automate version bumping, building signed release binaries, and capturing automated app store screenshots.
- **Week 12: Flagship Capstone Project 2: Offline-First Cross-Platform Production App with Background Sync & Store Release Bundle**
  - *Focus:* Deliver an enterprise-grade mobile application: complete offline functionality, camera upload, push notifications, biometric authentication, and a signed Android App Bundle (AAB) ready for Google Play release.
  - *Evaluation:* Live technical defense viva, app store bundle audit, and direct venture interview matching.

---

## 9. Domain 8: Python Automation & Web Scraping (`python-automation`)

### 9.1. Domain Overview, Industry Benchmarks & Technical Competencies
Python Automation and Web Scraping engineers eliminate manual corporate drudgery by building robust background bots, scheduled daemons, automated web crawlers, and asynchronous task pipelines. Professionals in this domain master web automation tools, anti-bot challenge bypassing, headless browser orchestration, email dispatch engines, and tabular data synthesis.
- **Industry Relevancy:** Enterprise demand for automated robotic process automation (RPA), data ingestion crawlers, competitor price monitoring bots, and backend workflow daemons continues to outpace manual development.
- **Starting Salary Benchmark:** ₹3.5 LPA to ₹8.0 LPA (Median: ₹5.5 LPA).
- **Core Frameworks:** Python 3.11+, Playwright, Selenium, BeautifulSoup4, Scrapy, Requests/HTTPX, Celery & Redis, APScheduler / Cron, SQLite, python-dotenv, Docker.

---

### 9.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/Gayatri-Education/gayatribot-Hr` (Production HR automation bot featuring automated offer letter generation, applicant pipeline filtering, SMTP email delivery, and Flask control hub).
  - Secondary: `https://github.com/Alkameinc/alkame-nifty-50-educational` (Automated market announcement fetchers and scheduled scrapers).

#### Weekly Sprint Breakdown:
- **Week 1: Python Advanced Automation Constructs & Data Processing**
  - *Sprint Goal:* Master advanced Python data manipulation, file handling, and regex text processing.
  - *Deliverables:* Scripts utilizing `openpyxl`, `csv`, and `json` for automated spreadsheet ingestion; regex extraction engines parsing unstructured text; structured exception logging.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification that automated scripts process a 10,000-row spreadsheet in $<3$ seconds without memory bloat.
- **Week 2: Static Web Scraping & HTML Parsing with BeautifulSoup4**
  - *Sprint Goal:* Build high-speed static web crawlers handling pagination, sessions, and headers.
  - *Deliverables:* Scraper utilizing `requests` and `BeautifulSoup4` with custom User-Agent rotation; robust CSS selector and XPath queries; automated retry loops with exponential backoff.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Execution of scraper extracting 500 catalog items from an e-commerce site with zero 429 Too Many Requests errors.
- **Week 3: Headless Browser Automation with Playwright**
  - *Sprint Goal:* Automate dynamic, JavaScript-heavy single-page applications using Playwright.
  - *Deliverables:* Playwright Python script executing automated form submissions, clicking dynamic elements, waiting for network idle states, and capturing full-page screenshots.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated test confirming successful login and data extraction from an SPA requiring dynamic client rendering.
- **Week 4: Omnichannel Growth & Automation Case Studies**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish automation engineering case studies.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and GitHub demonstrating Playwright automation and anti-bot mitigation; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Automated Email Dispatch & Document Generation**
  - *Sprint Goal:* Build programmatic email communication pipelines with dynamic PDF attachment generation.
  - *Deliverables:* SMTP email delivery client with Jinja2 HTML email template rendering; dynamic PDF generation using ReportLab/WeasyPrint; delivery audit logging in SQLite.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification that generated PDFs render perfectly and emails pass SPF/DKIM verification during delivery testing.
- **Week 6: Scheduled Daemons, Task Queues & Cron Automation**
  - *Sprint Goal:* Deploy background worker daemons with task scheduling and webhook alerts.
  - *Deliverables:* Scheduler utilizing `APScheduler` or Celery with Redis broker; background task worker executing recurring scraping jobs; automated Discord/Slack alerting webhooks on job failures.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Simulation verifying that an injected synthetic error triggers a Slack alert webhook within 5 seconds.
- **Week 7: Upstream Pull Request on Partner Repository**
  - *Sprint Goal:* Submit and merge an automation module on `Gayatri-Education/gayatribot-Hr`.
  - *Deliverables:* Upstream PR implementing automated candidate application filtering, SMTP rate pacing, or a Flask admin status dashboard; partner CI passed.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Maintainer code review approval and PR integration.
- **Week 8: Capstone Shipment, Technical Viva & Credentialing**
  - *Sprint Goal:* Deliver the complete end-to-end automation bot, defend architecture in viva, and graduate.
  - *Deliverables:* Public GitHub repository with Dockerfile, SQLite database, web dashboard, and complete documentation; technical viva defense before faculty.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Distributed Headless Scraping & Automated HR Candidate Pipeline Daemon*
- **Architecture:** Python 3.11 + Playwright headless engine + SQLite task ledger + Flask admin monitoring dashboard + Celery background worker + SMTP delivery engine.
- **Production Criteria:** Runs autonomously as a background daemon, handles rate limiting, extracts and parses resume PDFs, sends personalized emails, and logs full audit trails.

---

### 9.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-PYAUT-2026`
- **Tuition Fee:** ₹28,000 Upfront | Zero-Cost EMI: ₹3,111 / month (9 Months).
- **Career Benchmark:** ₹3.5 LPA – ₹8.0 LPA | Roles: Python Developer, Automation Engineer, Web Scraping Specialist, RPA Developer.
- **Mastered 12-Tool Stack:**
  1. Python 3.11+
  2. Requests & HTTPX
  3. BeautifulSoup4 & lxml
  4. Playwright Python
  5. Selenium WebDriver
  6. Scrapy Framework
  7. Celery & Redis
  8. APScheduler & Cron
  9. SQLite & SQLAlchemy
  10. Flask (Control Dashboards)
  11. Git & GitHub
  12. Docker

#### 12-Week Comprehensive Syllabus:
- **Week 1: Advanced Python Constructs & System Automation Scripting**
  - *Concepts:* Python idioms, list/dict comprehensions, generator functions, context managers (`with` statements), OS and FileSystem APIs (`os`, `pathlib`, `shutil`), logging modules.
  - *Assignment:* Write a script that recursively traverses a directory, organizes files by extension, and archives files older than 30 days into a compressed ZIP.
  - *Hands-on Lab:* Build a system automation script that monitors folder changes in real time using `watchdog` and triggers processing pipelines.
- **Week 2: Tabular Data Automation with Excel, CSV & JSON**
  - *Concepts:* Reading and writing Excel spreadsheets with `openpyxl`, formula injection, CSV dialect handling, JSON schema parsing, serialization and deserialization.
  - *Assignment:* Automate the monthly reconciliation of two disparate billing spreadsheets, generating an error report of mismatched invoices.
  - *Hands-on Lab:* Build a command-line tool that accepts messy JSON data exports and normalizes them into formatted Excel tables with auto-fitted column widths.
- **Week 3: Web Protocols, HTTP APIs & REST Automation**
  - *Concepts:* Client-server architecture, HTTP headers, request methods (GET, POST, PUT, DELETE), status codes, authentication schemes (API Keys, Bearer Tokens, Basic Auth), HTTPX async.
  - *Assignment:* Write a Python client library wrapping a public REST API with automatic rate-limiting and pagination handling.
  - *Hands-on Lab:* Build a multi-threaded API data harvester utilizing `concurrent.futures` that fetches 1,000 API records in parallel.
- **Week 4: Static Web Scraping with BeautifulSoup4 & lxml**
  - *Concepts:* HTML document object model (DOM), CSS selectors, XPath expressions, parsing tables, handling cookies and session state with `requests.Session`.
  - *Assignment:* Author a web scraper extracting real estate listings (price, location, square footage) across 20 paginated result pages.
  - *Hands-on Lab:* Build a scraper that monitors news websites for target keyword mentions and outputs structured records to a SQLite database.
- **Week 5: Dynamic Web Scraping with Selenium WebDriver**
  - *Concepts:* Browser automation architecture, WebDriver protocol, explicit vs implicit waits (`WebDriverWait`, `expected_conditions`), handling alert popups, scrolling dynamic pages.
  - *Assignment:* Automate the complete end-to-end checkout flow of an e-commerce test website using Selenium.
  - *Hands-on Lab:* Build a bot that logs into a password-protected web portal, downloads monthly PDF statements, and saves them locally.
- **Week 6: Modern Headless Automation with Playwright Python**
  - *Concepts:* Playwright vs Selenium architecture, async API, auto-waiting mechanics, network request interception, browser contexts, mobile device emulation.
  - *Assignment:* Write an automated Playwright script that intercepts network responses to capture raw JSON API payloads directly without parsing DOM elements.
  - *Hands-on Lab:* Build a cross-browser regression test script that captures and compares visual screenshots of web pages across Chromium, Firefox, and WebKit.
- **Week 7: Anti-Bot Challenge Mitigation & Stealth Scraping**
  - *Concepts:* Bot detection mechanisms (Cloudflare, Akamai, PerimeterX), browser fingerprinting (Canvas, WebGL, User-Agent, navigator.webdriver), proxy rotation, CAPTCHA handling.
  - *Assignment:* Configure Playwright with stealth plugins and rotating residential proxies to successfully access protected web pages.
  - *Hands-on Lab:* Build an automated monitor that tracks competitor pricing changes on dynamic retail websites without getting blocked.
- **Week 8: Midterm Capstone Project 1: Resilient Headless Scraping Daemon with SQLite Storage**
  - *Focus:* Architect and deploy a headless Playwright scraper that monitors an active job board, extracts new listings, filters duplicates, and stores records in SQLite with full error logging.
  - *Evaluation:* Faculty code review and 48-hour live runtime resilience evaluation.
- **Week 9: Large-Scale Web Crawling with Scrapy Framework**
  - *Concepts:* Scrapy architecture (Spiders, Item Pipelines, Downloader Middlewares), asynchronous architecture via Twisted, Scrapy Shell, item exports (JSON, CSV).
  - *Assignment:* Author a multi-page Scrapy spider crawling an entire technical blog archive, following internal links, and parsing article content.
  - *Hands-on Lab:* Build a Scrapy pipeline that automatically validates scraped item fields and inserts clean records into a PostgreSQL database.
- **Week 10: Automated Email & Document Generation Pipelines**
  - *Concepts:* SMTP and IMAP protocols, MIME multipart messages, dynamic HTML template rendering with Jinja2, automated PDF generation with WeasyPrint.
  - *Assignment:* Build an automated onboarding bot that generates custom PDF welcome packets and sends personalized emails with attachments.
  - *Hands-on Lab:* Create an email monitoring daemon that polls an IMAP inbox, extracts attached spreadsheets, processes data, and sends an automated reply.
- **Week 11: Asynchronous Task Queuing with Celery & Redis**
  - *Concepts:* Distributed task queues, message brokers (Redis), Celery worker architecture, periodic tasks with Celery Beat, task retry policies, task monitoring with Flower.
  - *Assignment:* Configure a Celery task queue that processes heavy image resizing and document conversion tasks in the background.
  - *Hands-on Lab:* Build an automated batch processing system with a lightweight Flask web dashboard showing real-time task progress and worker health.
- **Week 12: Flagship Capstone Project 2: Enterprise Automated Candidate Pipeline & Webhook Dispatch Daemon**
  - *Focus:* Deliver a production-grade enterprise automation system: headless web scraper that collects industry leads, filters candidates via automated criteria, generates PDF dossiers, dispatches email notifications, and provides a web control dashboard.
  - *Evaluation:* Live technical defense viva, code quality audit, and direct venture interview matching.


---

## 10. Domain 9: UI/UX Design & Product Experience Systems (`ui-ux-design`)

### 10.1. Domain Overview, Industry Benchmarks & Technical Competencies
UI/UX Design and Product Experience engineers architect the visual, structural, and behavioral interfaces of modern software products. Professionals in this domain master qualitative user research, information architecture, wireframing, high-fidelity Figma prototyping, design token standardization, WCAG accessibility compliance, and developer design system handoff.
- **Industry Relevancy:** With software becoming increasingly complex, companies prioritize product designers who understand engineering constraints, atomic design systems, and design tokens rather than purely decorative art.
- **Starting Salary Benchmark:** ₹3.5 LPA to ₹7.5 LPA (Median: ₹5.2 LPA).
- **Core Frameworks:** Figma, Auto-Layout, Design Tokens (Style Dictionary), FigJam, Miro, Whimsical, Zeroheight, Zeplin, UserTesting, WCAG 2.1 AA/AAA Audits, Storybook, HTML/CSS basics.

---

### 10.2. Structure 1: 2-Month Fellowship Program (8 Weeks / 56 Days)
- **Program Metrics:** 8 Weeks (56 Calendar Days) | 10 Hours/Week (80 Hours Capped) | Caution Deposit ₹499 + ₹1,500 Balance | ₹5,000 Performance Stipend.
- **Assigned Partner Repositories:**
  - Primary: `https://github.com/DBERT-INDIA/dbert-design-tokens` (Comprehensive Figma design tokens, WCAG accessible component library, typography scales, and interactive prototypes).
  - Secondary: `https://github.com/Gayatri-Education/Intern-workbench` (User experience workflows, candidate dashboard interactions, and design token integration).

#### Weekly Sprint Breakdown:
- **Week 1: Qualitative User Research, Empathy Mapping & Personas**
  - *Sprint Goal:* Conduct user problem discovery and synthesize findings into actionable research artifacts.
  - *Deliverables:* User interview script; 5 recorded user interviews; empathy maps; 2 detailed user persona profiles identifying pain points, goals, and technical comfort levels.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Faculty review verifying that persona pain points map directly to observable interview evidence.
- **Week 2: Information Architecture & User Journey Flow Mapping**
  - *Sprint Goal:* Structure complex application workflows into intuitive, low-friction information architectures.
  - *Deliverables:* Card sorting results; application sitemap hierarchy; end-to-end user journey flowcharts diagramming happy paths and error states in FigJam/Miro.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification that every primary user goal can be completed in $\le 3$ distinct navigation actions.
- **Week 3: Figma Core Mastery: Vectors, Constraints & Auto-Layout 5.0**
  - *Sprint Goal:* Construct modular, responsive layout frames using advanced Figma layout mechanics.
  - *Deliverables:* Responsive screen layouts utilizing nested Auto-Layout (horizontal/vertical directions, gap, padding, wrap properties); fill vs hug constraints; min/max width bounds.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Stress test: resizing parent frames between 320px (mobile) and 1440px (desktop) without text truncation or element breakage.
- **Week 4: Omnichannel Growth & Product Design Case Studies**
  - *Sprint Goal:* Complete enterprise micro-bounties and publish design systems case studies.
  - *Deliverables:* Omnichannel Social Bounties (Tasks 101–104) published on LinkedIn and Behance/Dribbble demonstrating Auto-Layout and design token matrices; 50 task coins earned.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Verification of live URL submissions on LMS portal.
- **Week 5: Design Tokens & Atomic Component Architecture**
  - *Sprint Goal:* Architect a scalable design system using standardized design tokens and atomic components.
  - *Deliverables:* Semantic color palette (primary, neutral, semantic alerts); modular typography scale; spacing scale (4px/8px grid); atomic component library (Buttons, Inputs, Badges, Cards) with variant matrices and boolean properties.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Automated Figma plugin audit confirming zero hardcoded hex colors or detached styles.
- **Week 6: WCAG 2.1 Accessibility Auditing & Micro-Interactions**
  - *Sprint Goal:* Ensure universal accessibility and build interactive component state prototypes.
  - *Deliverables:* Color contrast audit report certifying WCAG 2.1 AA/AAA compliance across all text and UI elements; interactive components with hover, active, focused, and disabled states; micro-interaction animations.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Stark / Contrast plugin verification proving $100\%$ AA compliance across light and dark modes.
- **Week 7: Upstream Pull Request / Design Tokens Contribution on Partner Repo**
  - *Sprint Goal:* Submit and merge a design token export or component specification on `DBERT-INDIA/dbert-design-tokens`.
  - *Deliverables:* Pull request exporting validated JSON design tokens (using Style Dictionary format) and Markdown design specs for engineering implementation; partner review passed.
  - *Logged Attendance:* 10.0 Hours.
  - *Validation Checkpoint:* Design system lead review approval and token schema validation.
- **Week 8: Capstone Shipment, Technical Viva & Credentialing**
  - *Sprint Goal:* Deliver the complete clickable prototype and developer handoff specification, defend design rationale in viva, and graduate.
  - *Deliverables:* Public Figma community link with interactive clickable prototype; developer handoff documentation with CSS properties, spacing guidelines, and responsive rules; technical viva defense before faculty.
  - *Logged Attendance:* 10.0 Hours (Cumulative: 80.0 Hours).
  - *Validation Checkpoint:* Faculty score $\ge 80/100$, Turnitin score $< 5\%$, credential generation, Gate 1-5 stipend unlock.

#### Capstone Project Specification:
- **Title:** *Enterprise B2B SaaS Design System & Interactive Developer Handoff Prototype*
- **Architecture:** Figma atomic design system + semantic design tokens (JSON) + WCAG 2.1 AA/AAA compliance audit + clickable prototype covering 15+ responsive screens + developer handoff documentation.
- **Production Criteria:** 100% Auto-Layout compliance, zero detached components, interactive state animations, complete edge case coverage (empty states, errors), and ready for engineering implementation.

---

### 10.3. Structure 2: 3-Month Paid Learner Course (12 Weeks)
- **Course Code:** `DBERT-ENG-UIUX-2026`
- **Tuition Fee:** ₹28,000 Upfront | Zero-Cost EMI: ₹3,111 / month (9 Months).
- **Career Benchmark:** ₹3.5 LPA – ₹7.5 LPA | Roles: UI/UX Designer, Product Designer, Interaction Designer, Design Systems Specialist.
- **Mastered 12-Tool Stack:**
  1. Figma
  2. FigJam
  3. Miro
  4. Auto-Layout & Component Variants
  5. Design Tokens (Style Dictionary)
  6. Stark (Accessibility & Contrast Checker)
  7. Maze / Useberry (Usability Testing)
  8. Notion (Product Requirement Docs)
  9. Whimsical (Sitemaps & Flows)
  10. Storybook Basics
  11. Git & GitHub (for Design Tokens)
  12. Zeroheight (Design System Documentation)

#### 12-Week Comprehensive Syllabus:
- **Week 1: Fundamentals of User-Centered Design & Design Thinking**
  - *Concepts:* Design thinking process (Empathize, Define, Ideate, Prototype, Test), cognitive psychology in UI (Hick's Law, Fitts's Law, Miller's Law), UI vs UX vs Product Design.
  - *Assignment:* Audit an existing popular mobile application, identifying 5 usability violations based on Nielsen Norman 10 Usability Heuristics.
  - *Hands-on Lab:* Set up Figma workspace, configure project files, and practice keyboard shortcuts for accelerated UI drafting.
- **Week 2: Qualitative & Quantitative User Research Methodologies**
  - *Concepts:* Generative vs evaluative research, user interviews, surveys, empathy mapping, user personas, problem statement formulation (How Might We statements).
  - *Assignment:* Conduct 3 user interviews regarding online learning experiences and synthesize responses into an empathy map.
  - *Hands-on Lab:* Build a comprehensive user persona in Figma detailing motivations, frustrations, tech stack familiarity, and quotes.
- **Week 3: Information Architecture, Sitemaps & User Flows**
  - *Concepts:* Information hierarchy, mental models, open vs closed card sorting, sitemap taxonomies, task flows vs user journey maps.
  - *Assignment:* Create an application sitemap for a multi-tenant healthcare scheduling platform.
  - *Hands-on Lab:* Diagram a complete user onboarding flow in FigJam detailing decisions, notifications, error paths, and success confirmations.
- **Week 4: Low-Fidelity Wireframing & Rapid Paper Prototyping**
  - *Concepts:* Low-fidelity vs high-fidelity, visual hierarchy, Gutenberg diagram, F-pattern vs Z-pattern scanning, grayscale layout constraints.
  - *Assignment:* Sketch 10 diverse layout variations for a dashboard homepage using paper wireframing techniques.
  - *Hands-on Lab:* Convert paper sketches into digital grayscale wireframes in Figma, testing basic content hierarchy without colors or images.
- **Week 5: Visual Design Foundations: Typography, Color Theory & Grids**
  - *Concepts:* Font pairings, type scales (modular scales), line-height/letter-spacing, color psychology, 60-30-10 color rule, 8pt spatial grid system.
  - *Assignment:* Construct a harmonious corporate color palette with primary, secondary, neutral, and alert tints/shades.
  - *Hands-on Lab:* Build a responsive typography stylesheet in Figma defining desktop, tablet, and mobile heading/body text styles.
- **Week 6: Figma Mastery: Constraints, Nested Auto-Layout & Smart Resizing**
  - *Concepts:* Horizontal/vertical directions, space between vs packed, padding, hug contents vs fill container, fixed widths, absolute positioning inside Auto-Layout.
  - *Assignment:* Build a responsive navigation navbar that adjusts elements dynamically from desktop widescreen down to mobile hamburger view.
  - *Hands-on Lab:* Create a complex responsive pricing card matrix that expands and reorganizes contents smoothly across viewport widths.
- **Week 7: Component Properties, Variants & Interactive Component States**
  - *Concepts:* Component architecture, master components vs instances, component variants, boolean properties, text properties, instance swap properties.
  - *Assignment:* Build a comprehensive button component featuring 4 variants (Primary, Secondary, Ghost, Destructive), 3 sizes, and leading/trailing icon toggles.
  - *Hands-on Lab:* Create an interactive form input component with hover, active typing, validation error, and disabled states.
- **Week 8: Midterm Capstone Project 1: Mobile Fintech Application Design & User Journey Flow**
  - *Focus:* Architect an end-to-end mobile fintech wallet experience (Sign Up, KYC verification, Send Money, Transaction History) with low-to-high fidelity screens and interactive flows.
  - *Evaluation:* Faculty design review and peer heuristic evaluation.
- **Week 9: Design Tokens & Scalable Design System Architecture**
  - *Concepts:* Atomic design methodology (Atoms, Molecules, Organisms, Templates, Pages), design tokens (Global, Alias, Component tokens), token naming conventions (BEM/CUBE).
  - *Assignment:* Author a standardized JSON design token file representing the color, typography, and spacing tokens of a SaaS platform.
  - *Hands-on Lab:* Build a complete design system library in Figma and publish it as an accessible team library.
- **Week 10: Web Accessibility (WCAG 2.1) & Inclusive Design**
  - *Concepts:* Web Content Accessibility Guidelines (WCAG 2.1 AA/AAA), color contrast ratios (4.5:1 text, 3:1 UI), focus states, screen reader considerations, accessible forms.
  - *Assignment:* Audit an existing landing page using Stark or Contrast plugins and resolve all failing contrast ratios.
  - *Hands-on Lab:* Design an accessible dark mode theme for a complex data visualization dashboard, ensuring compliant contrast across all charts.
- **Week 11: Advanced Prototyping, Micro-Interactions & Usability Testing**
  - *Concepts:* Smart Animate, interactive drag triggers, scroll overflows, modal overlays, conducting unmoderated usability tests with Maze, calculating System Usability Scale (SUS).
  - *Assignment:* Prototype a micro-interaction animation (e.g., swipe-to-delete or animated success confetti) using Smart Animate.
  - *Hands-on Lab:* Set up a live usability test in Maze, recruit 5 test users, and analyze click heatmaps and drop-off rates.
- **Week 12: Flagship Capstone Project 2: Comprehensive Enterprise B2B SaaS Design System with Clickable Prototypes & Developer Handoff**
  - *Focus:* Deliver an enterprise-grade product design package: complete Figma design system, WCAG AA audited components, interactive clickable prototype covering 15+ responsive screens, and developer handoff documentation with spacing tokens and CSS snippets.
  - *Evaluation:* Live technical design defense viva, portfolio walkthrough, and direct venture interview matching.

---

## 11. Cross-Domain Comparative Matrix & Operational Playbook

### 11.1. Master Comparative Matrix Across All 9 Domains

| # | Technical Domain | Course Code | Fellowship Partner Repos | Fellowship Capstone | Course Tuition (EMI) | Course Salary Benchmark | Flagship Course Capstone |
|---|---|---|---|---|:---:|:---:|---|
| **1** | **AI Agent Development** | `DBERT-ENG-AGNT-2026` | `DBERT-INDIA/dbert-agent`, `Gayatri-AI` | Local-First Multi-Agent Assistant | ₹35,000 (₹3,888/mo) | ₹5.0 – ₹12.0 LPA | Distributed Multi-Agent Operations Platform |
| **2** | **Generative AI & ML** | `DBERT-ENG-GENAI-2026` | `Gayatri-Tutor-V3`, `alkame-nifty-50` | Domain-Adapted Fine-Tuned SLM | ₹34,000 (₹3,777/mo) | ₹5.5 – ₹15.0 LPA | Specialized SLM Fine-Tuning & vLLM Serving |
| **3** | **Full Stack Development** | `DBERT-ENG-FSTCK-2026` | `DBERT-INDIA/Internshipportal`, `Intern-workbench` | Enterprise Assessment Portal | ₹38,000 (₹4,222/mo) | ₹4.0 – ₹10.0 LPA | Next.js Enterprise LMS & Talent Marketplace |
| **4** | **Data Analytics & BI** | `DBERT-ENG-DATA-2026` | `aivara-insight-lite`, `alkame-nifty-50` | Automated CSV Driver Decomposer | ₹28,000 (₹3,111/mo) | ₹3.5 – ₹9.0 LPA | Automated Enterprise BI & Narrative Deck Platform |
| **5** | **Cybersecurity & Threat** | `DBERT-ENG-CYBER-2026` | `secops-audit-suite`, `Internshipportal` | Web Vulnerability Scanner & CVSS Suite | ₹28,000 (₹3,111/mo) | ₹4.5 – ₹10.5 LPA | Enterprise SOC Incident Response & Auditing |
| **6** | **DevOps & Cloud** | `DBERT-ENG-DEVOPS-2026` | `cloud-infra-blueprints`, `Internshipportal` | Multi-Tier Terraform/K8s Cloud Deploy | ₹28,000 (₹3,111/mo) | ₹4.5 – ₹11.0 LPA | High-Availability GitOps Kubernetes Cluster |
| **7** | **Mobile App Development** | `DBERT-ENG-MOBILE-2026` | `mobile-app-workbench`, `Internshipportal` | Offline-First LMS Companion Mobile App | ₹28,000 (₹3,111/mo) | ₹4.0 – ₹9.0 LPA | Offline-First Cross-Platform Production App |
| **8** | **Python Automation** | `DBERT-ENG-PYAUT-2026` | `gayatribot-Hr`, `alkame-nifty-50` | Headless Scraper & HR Pipeline Daemon | ₹28,000 (₹3,111/mo) | ₹3.5 – ₹8.0 LPA | Enterprise Candidate Pipeline & Webhook Daemon |
| **9** | **UI/UX Product Design** | `DBERT-ENG-UIUX-2026` | `dbert-design-tokens`, `Intern-workbench` | B2B SaaS Design System & Prototype | ₹28,000 (₹3,111/mo) | ₹3.5 – ₹7.5 LPA | Enterprise Design System with Handoff Specs |

---

### 11.2. Upstream PR Verification Workflow & Anti-Plagiarism Engine (Turnitin <5%)
All code and written deliverables undergo programmatic verification prior to faculty scoring:
1. **Automated GitHub Forensics Scan (`scripts/audit_33_github_linkedin.py`):**
   - The candidate's submitted Pull Request URL is parsed.
   - The target repository is verified to belong to one of the 4 official partner namespaces (`Alkameinc`, `Gayatri-Education`, `DBERT-INDIA`, `Aivara-Technologies`).
   - Merged or opened commit diffs are evaluated for originality, non-trivial line count changes ($>50$ lines of actual logic), and absence of copied facade code.
2. **Turnitin Academic Originality Check:**
   - Architecture documentation, technical reports, and code comments are submitted to the Turnitin integration endpoint.
   - Any deliverable exhibiting $\ge 5.0\%$ similarity against indexed academic papers, previous student cohorts, or public tutorials is flagged as `CHANGES_REQUESTED`.
   - The candidate is given exactly 72 hours to refactor the flagged sections and resubmit.

---

### 11.3. Faculty Evaluation Board & Technical Viva Protocol
The final 10 marks of the 100-mark rubric are awarded through a synchronous technical viva:
- **Evaluation Committee:** Composed of 1 Lead Architect (Abhinav Sharma or designated senior staff) and 1 Domain Specialist.
- **Viva Structure (15 Minutes):**
  - *Minutes 0–5 (System Architecture Walkthrough):* Candidate screenshares and explains high-level design decisions, schema normalizations, and concurrency management.
  - *Minutes 5–10 (Live Code Inspection & Defense):* Evaluators select 2 random subroutines in the candidate's codebase and ask them to explain edge case handling and $O(n)$ time/space complexity.
  - *Minutes 10–15 (Adversarial Trade-Off Q&A):* Candidate defends why they chose specific libraries, patterns, or data structures over alternatives.
- **Scoring Minimum:** A minimum score of 8/10 in the Technical Viva and an aggregate score of $\ge 80/100$ across all 9 dimensions is mandatory for Merit / Verified status.

---

### 11.4. Monorepo Integration & Production EC2 Deployment Protocol
Upon updating curriculum files or related Next.js pages:
1. **Source Code Modifications:**
   - Updates to curriculum data reside in `apps/website/src/data/` (`launchpadDomains.ts`, `domains.config.ts`, `pricing.config.ts`).
   - Route implementations reside in `apps/website/src/app/learners/courses/` and `/verify/directory/`.
2. **Standalone Build & Deployment:**
   - Files are synchronized to production EC2:
     ```powershell
     scp -i "C:\Users\user\.ssh\dbert-production-server.pem" -o StrictHostKeyChecking=no -o BatchMode=yes <local_file> ubuntu@3.26.237.171:/var/www/dbert-website-lms/apps/website/<target_path>
     ```
   - Remote build execution on EC2:
     ```bash
     cd /var/www/dbert-website-lms/apps/website
     export NODE_ENV=production
     npm run build
     cp -r public .next/standalone/ 2>/dev/null || true
     cp -r public .next/standalone/apps/website/ 2>/dev/null || true
     sudo systemctl restart dbert-website.service
     systemctl is-active dbert-website.service
     ```
3. **Verification:** Live endpoints return `HTTP 200 OK` on `https://dbert.in`.
