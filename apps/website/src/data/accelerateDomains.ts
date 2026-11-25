import type { InternRepoReference } from './launchpadDomains';

export interface AccelerateDomain {
  id: string;
  name: string;
  shortName: string;
  tagline: string;
  price: string;
  duration: string;
  scopeSummary: string;
  audience: string;
  outcome: string;
  githubRepos: InternRepoReference[];
  curriculum: {
    period: string;
    title: string;
    topics: string[];
  }[];
}

export const ACCELERATE_DOMAINS: Record<string, AccelerateDomain> = {
  'ai-agent-development': {
    id: 'ai-agent-development',
    name: 'AI Agent Systems & Orchestration Sprints',
    shortName: 'AI Agents',
    tagline: 'Applied Multi-Agent State Graphs, Tool Calling, Memory Persistence & Production Evaluation',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Build 3 standalone multi-agent services (vs. Launchpad basics or Fellowship live client PRs).',
    audience: 'CS graduates, Python developers, and Launchpad alumni moving from basic scripts to fault-tolerant multi-agent APIs.',
    outcome: 'Ship 3 evaluated AI agent microservices with LangGraph state recovery, PostgreSQL pgvector memory, and sub-2s local Ollama streaming.',
    githubRepos: [
      {
        name: 'DBERT-INDIA / dbert-agent',
        url: 'https://github.com/DBERT-INDIA/dbert-agent',
        role: 'Applied Agent Architecture Builder',
        badgeText: 'Accelerate Sprint Track',
        description: 'Multi-step planning loops, schema-validated tool adapters, and human-in-the-loop approval checkpoints.',
        keyModules: ['LangGraph State Machine', 'Pydantic Tool Contracts', 'FastAPI SSE Streaming', 'Agent Trace Evaluator']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Deterministic Tool Calling & Async FastAPI Gateway',
        topics: [
          'Converting brittle prompt chains into schema-validated Pydantic tool schemas.',
          'Async streaming SSE endpoints in FastAPI with strict timeout and fallback handlers.',
          'Local open-weights serving benchmarks via Ollama and vLLM.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Hybrid RAG Memory & Pgvector Indexing',
        topics: [
          'BM25 sparse + pgvector HNSW dense hybrid retrieval pipelines.',
          'Cross-encoder re-ranking and persistent conversation checkpointing in PostgreSQL.',
          'Evaluating citation grounding and hallucination rates with automated test suites.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Multi-Agent Delegation & Human-in-the-Loop Controls',
        topics: [
          'Planner/Executor/Reviewer graph handoffs in LangGraph & CrewAI.',
          'Role-based permission guards before mutating external databases or APIs.',
          'Containerizing agent workers with Docker Compose and Redis queues.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Telemetry, Load Benchmarking & Readiness Audit',
        topics: [
          'Structured JSONL telemetry logging, token cost ceilings, and retry backoff.',
          'Senior PR walkthrough covering architecture trade-offs and edge-case recovery.',
          'Direct qualification pathway into the ₹1,999 client-production Fellowship.'
        ]
      }
    ]
  },
  'generative-ai': {
    id: 'generative-ai',
    name: 'Generative AI, RAG & Fine-Tuning Sprints',
    shortName: 'Generative AI',
    tagline: 'Applied Retrieval-Augmented Generation, Document OCR, Reranking & Guardrails',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · End-to-end multimodal & RAG pipelines under weekly code review.',
    audience: 'Developers with Python fundamentals seeking applied mastery in production RAG, OCR ingestion, and semantic search.',
    outcome: 'Architect and benchmark an enterprise knowledge engine handling scanned PDFs, hybrid chunking, and strict citation checks.',
    githubRepos: [
      {
        name: 'Gayatri-Education / Gayatri-AI',
        url: 'https://github.com/Gayatri-Education/Gayatri-AI',
        role: 'Applied GenAI & RAG Engineer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Document OCR extraction, semantic retrieval, Redis query caching, and strict grounded generation.',
        keyModules: ['Layout-Aware PDF OCR', 'Semantic Chunking', 'Redis Semantic Cache', 'Citation Verifier']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Multi-Format Ingestion & Document Parsing',
        topics: [
          'Parsing complex tables and scanned PDFs with PyMuPDF and Tesseract OCR.',
          'Structure-aware markdown/section chunking vs. fixed token sliding windows.',
          'Metadata enrichment for access-controlled multi-tenant knowledge bases.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Hybrid Retrieval, Caching & Reranking',
        topics: [
          'Dense + lexical RRF fusion inside PostgreSQL pgvector and FAISS.',
          'Redis semantic caching strategies reducing LLM inference cost by >60%.',
          'Prompt injection defense and output JSON schema enforcement.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Domain Adaptation & Retrieval Evaluation',
        topics: [
          'Creating golden QA evaluation sets for Precision@K and faithfulness.',
          'Comparing quantized GGUF open-weights models vs. hosted API fallbacks.',
          'Streaming citations cleanly to React/Next.js frontend clients.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Deployment Hardening & Senior Architecture Review',
        topics: [
          'Rate limiting, latency profiling, and Docker packaging for VPS deployment.',
          'Final evaluated sprint demo and technical architecture write-up.',
          'Accelerate credential issuance + Fellowship client placement readiness.'
        ]
      }
    ]
  },
  'machine-learning': {
    id: 'machine-learning',
    name: 'Applied Machine Learning & MLOps Sprints',
    shortName: 'Machine Learning',
    tagline: 'Feature Engineering, Model Calibration, Experiment Tracking & Inference Serving',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Tabular/time-series modeling & MLOps serving APIs.',
    audience: 'Students and engineers with Python & NumPy familiarity building production ML services beyond static notebooks.',
    outcome: 'Deliver reproducible training pipelines, MLflow/DVC tracking, drift monitors, and containerized FastAPI inference servers.',
    githubRepos: [
      {
        name: 'Alkameinc / alkame-nifty-50-educational',
        url: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
        role: 'Applied ML & Forecasting Engineer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Quantitative time-series feature pipelines, walk-forward validation, and calibration benchmarks.',
        keyModules: ['Walk-Forward Splits', 'XGBoost & PyTorch Pipelines', 'Model Registry', 'FastAPI Serving']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Leak-Free Validation & Feature Engineering',
        topics: [
          'Time-series walk-forward cross-validation and group-aware splits.',
          'Scikit-learn custom transformers and reproducible preprocessing pipelines.',
          'Class imbalance handling, threshold tuning, and ROC/PR calibration.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Gradient Boosting, PyTorch & Experiment Tracking',
        topics: [
          'Hyperparameter tuning with Optuna across LightGBM, XGBoost, and PyTorch.',
          'Tracking metrics, feature importance, and model artifacts reproducibly.',
          'SHAP explainability outputs for regulated domain stakeholders.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Production Inference APIs & Batch Scoring',
        topics: [
          'Low-latency ONNX / FastAPI model serving with Pydantic input validation.',
          'Scheduled feature computation and data drift detection alerts.',
          'Writing automated unit tests around feature parity and edge inputs.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Containerized Deployment & Senior Model Review',
        topics: [
          'Multi-stage Docker builds, health probes, and memory-bounded workers.',
          'Final 1:1 engineering audit and verified benchmark report.',
          'Fast-track eligibility for client ML production squads.'
        ]
      }
    ]
  },
  'data-analytics': {
    id: 'data-analytics',
    name: 'Data Analytics & Automated BI Sprints',
    shortName: 'Data Analytics',
    tagline: 'Advanced SQL Modeling, Python Pandas/NumPy Automation, Power BI & Executive Reporting',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Automated multi-source SQL/Python ETL & BI dashboards.',
    audience: 'Analysts who already know basic Excel/SQL and want applied mastery in PostgreSQL analytics, Python automation, and Power BI.',
    outcome: 'Build automated KPI ETL pipelines, interactive Power BI/Metabase dashboards, and Python-driven executive slide generators.',
    githubRepos: [
      {
        name: 'Aivara-Technologies / aivara-insight-lite',
        url: 'https://github.com/Aivara-Technologies/aivara-insight-lite',
        role: 'Applied BI & Analytics Engineer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Automated CSV/SQL ingestion, driver variance decomposition, and executive deck generation.',
        keyModules: ['PostgreSQL Window Analytics', 'Pandas/NumPy Decomposition', 'Power BI Data Modeling', 'Matplotlib/Seaborn Automation']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'PostgreSQL Window Functions & Dimensional Modeling',
        topics: [
          'Multi-table funnel joins, cohort retention queries, and rolling aggregations.',
          'Star-schema views separating analytical marts from operational tables.',
          'Indexing and EXPLAIN ANALYZE query latency tuning.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Automated Python, Pandas, NumPy & Jupyter Pipelines',
        topics: [
          'Schema validation assertions and messy Excel/CSV reconciliation in Pandas.',
          'Revenue/KPI driver variance decomposition using vectorized NumPy logic.',
          'Publication-grade Matplotlib & Seaborn charts exported cleanly from Jupyter.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Power BI Semantic Models & Executive Storytelling',
        topics: [
          'DAX measures, YoY/MoM variance cards, and drill-through Power BI reports.',
          'Automating executive PowerPoint decks directly from cleaned data frames.',
          'Designing honest visualizations with confidence intervals and caveats.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Git-Versioned BI Suite & Senior Analyst Review',
        topics: [
          'Structuring Git repositories with reproducible SQL, notebooks, and data dictionaries.',
          'Senior code & metric review to verify zero silent row drops.',
          'Readiness audit for client Data Analytics Fellowship engagements.'
        ]
      }
    ]
  },
  'full-stack-development': {
    id: 'full-stack-development',
    name: 'Full Stack Web Systems & SaaS Architecture Sprints',
    shortName: 'Full Stack',
    tagline: 'Next.js App Router, FastAPI/Node Backends, PostgreSQL Auth, Redis & Production Deployments',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Multi-tenant SaaS systems with auth, caching & CI.',
    audience: 'Developers familiar with React/JS or backend basics ready to ship full-stack production architectures.',
    outcome: 'Architect a multi-tenant web application with role-based JWT/OAuth2 auth, PostgreSQL migrations, Redis caching, and automated Playwright E2E checks.',
    githubRepos: [
      {
        name: 'DBERT-INDIA / Internshipportal',
        url: 'https://github.com/DBERT-INDIA/Internshipportal',
        role: 'Applied Full Stack Architect',
        badgeText: 'Accelerate Sprint Track',
        description: 'High-concurrency web portal, relational schemas, idempotent payments, and modular services.',
        keyModules: ['Next.js + TypeScript', 'PostgreSQL & Indexing', 'RBAC Auth & OWASP', 'Redis + Nginx Deploy']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Relational Schema Design & Backend API Contracts',
        topics: [
          'Normalized PostgreSQL schemas, foreign keys, migrations, and composite indexes.',
          'Type-safe REST/JSON contracts in Next.js Route Handlers and FastAPI.',
          'Idempotent write patterns and server-side validation.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Frontend State, SSR/ISR & Responsive Design Systems',
        topics: [
          'Next.js Server vs. Client Components, streaming Suspense, and SEO metadata.',
          'Accessible form UX, optimistic updates, and mobile-first CSS architecture.',
          'Eliminating N+1 API waterfalls with batched queries.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Auth, Security Hardening & Redis Caching',
        topics: [
          'HTTP-only session cookies, RBAC middleware, CSRF & XSS mitigation.',
          'Redis response caching and background task queues for heavy webhooks.',
          'Rate limiting and structured audit logging.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'End-to-End QA, Standalone Build & Production Release',
        topics: [
          'Playwright E2E regression tests + systemd/Docker zero-downtime restarts.',
          'Final senior code review across backend and frontend PRs.',
          'Direct readiness pathway to client Full Stack Fellowship squads.'
        ]
      }
    ]
  },
  'python-automation': {
    id: 'python-automation',
    name: 'Python Automation, Scraping & Workflow Bots Sprints',
    shortName: 'Python Automation',
    tagline: 'Async Playwright Scrapers, Webhook Workers, Retry Queues & Telegram/WhatsApp Integrations',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Resilient scraping, OCR & event-driven bots.',
    audience: 'Developers with Python syntax fluency building fault-tolerant automation workers and bot pipelines.',
    outcome: 'Ship resilient async scrapers, Celery/SQLite task queues, and automated notification/reporting bots with zero silent drops.',
    githubRepos: [
      {
        name: 'Gayatri-Education / gayatribot-Hr',
        url: 'https://github.com/Gayatri-Education/gayatribot-Hr',
        role: 'Applied Automation Engineer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Automated candidate ingestion, scheduled dispatch pipelines, and resilient browser workers.',
        keyModules: ['Async Playwright', 'Idempotent State Queues', 'Retry Circuit Breakers', 'Bot Webhook Handlers']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Async Python HTTP, Rate Limiting & Parsing',
        topics: [
          'High-throughput httpx/asyncio scraping with exponential backoff.',
          'Structuring deterministic data parsers with Pydantic & regex sanity guards.',
          'Resumable checkpoints using SQLite WAL / PostgreSQL.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Playwright Browser Automation & Document Extraction',
        topics: [
          'Headless browser orchestration, resource blocking, and DOM state waits.',
          'Tesseract OCR / PDF extraction workflows for unstructured invoices and resumes.',
          'Automated screenshot diagnostics on worker failure.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Scheduled Daemons & Bot Dispatch Engines',
        topics: [
          'Building Telegram/WhatsApp/Email webhook alerts and daily digest jobs.',
          'Deduplication ledgers and circuit-breaker health alarms.',
          'Writing PyTest mocks for third-party APIs.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Systemd Deployment, Logging & Sprint Audit',
        topics: [
          'Packaging CLI/daemon automation with rotating structured logs.',
          'Senior PR walkthrough covering idempotency and error handling.',
          'Seamless progression into DBERT Fellowship live automation queues.'
        ]
      }
    ]
  },
  'ui-ux-design': {
    id: 'ui-ux-design',
    name: 'UI/UX Design Systems & Product Prototyping Sprints',
    shortName: 'UI/UX Design',
    tagline: 'Tokenized Figma Design Systems, WCAG AA Accessibility, Interactive Prototypes & Dev Handoff',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · End-to-end SaaS design system & audited UX flows.',
    audience: 'Designers who know basic Figma frames and want real SaaS component libraries, accessibility audits, and developer handoff.',
    outcome: 'Produce a responsive token-driven Figma design system, usability test findings, and developer-ready CSS specs.',
    githubRepos: [
      {
        name: 'DBERT-Design / dbert-design-system',
        url: 'https://github.com/DBERT-Design/dbert-design-system',
        role: 'Applied Product & UX Designer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Unified dark/light component tokens, responsive dashboards, and conversion-focused onboarding flows.',
        keyModules: ['Figma Variables & Tokens', 'WCAG AA Contrast', 'Mobile-First Flows', 'Inspectable Dev Specs']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Information Architecture & User Funnel Mapping',
        topics: [
          'Auditing onboarding drop-offs and multi-step enrollment user journeys.',
          'Low-fidelity task flows covering empty, loading, error, and success states.',
          'Heuristic evaluation against Nielsen usability benchmarks.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Design Tokens & Auto-Layout Component Libraries',
        topics: [
          'Semantic spacing, typography, elevation, and color tokens in Figma.',
          'Variant-rich interactive tables, forms, modals, and mobile drawers.',
          'WCAG 2.1 AA contrast & keyboard focus validation.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'High-Fidelity Prototyping & Usability Testing',
        topics: [
          'Interactive prototypes across desktop (1440px) and mobile (375px) viewports.',
          'Conducting structured 5-user usability sessions and iterating friction points.',
          'Micro-copy and form validation clarity.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Engineering Handoff & Portfolio Case Study',
        topics: [
          'CSS variable mapping and responsive breakpoint documentation for engineers.',
          'Senior design & engineering review critique.',
          'Portfolio publication + Fellowship product squad eligibility.'
        ]
      }
    ]
  },
  'devops-cloud': {
    id: 'devops-cloud',
    name: 'Cloud Infrastructure, Docker & CI/CD Sprints',
    shortName: 'DevOps & Cloud',
    tagline: 'Nginx Reverse Proxies, Multi-Stage Docker, GitHub Actions, TLS & Zero-Downtime Linux Ops',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Production VPS hardening, CI/CD & observability.',
    audience: 'Engineers comfortable with Linux commands building automated CI/CD, reverse proxies, and monitored cloud deployments.',
    outcome: 'Provision hardened Ubuntu EC2/VPS stacks with Nginx TLS, multi-stage Docker builds, GitHub Actions CI/CD, and alerting.',
    githubRepos: [
      {
        name: 'DBERT-Cloud / infrastructure-blueprints',
        url: 'https://github.com/DBERT-Cloud/infrastructure-blueprints',
        role: 'Applied Cloud & DevOps Engineer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Reproducible reverse proxy configs, systemd service supervision, automated SSL, and CI pipelines.',
        keyModules: ['Docker Multi-Stage', 'Nginx & Certbot TLS', 'GitHub Actions CI/CD', 'Prometheus/Logs']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Linux Hardening, Systemd & Nginx Reverse Proxying',
        topics: [
          'UFW firewall rules, SSH key hardening, and non-root service accounts.',
          'Nginx upstream routing, gzip/Brotli, TLS certificates, and HTTP/2 headers.',
          'Writing reliable systemd unit files with clean restart policies.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Containerization & Multi-Service Orchestration',
        topics: [
          'Multi-stage Dockerfiles shrinking Next.js and Python image footprints.',
          'Docker Compose networks, healthchecks, and PostgreSQL volume backups.',
          'Secrets management across staging and production environments.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'GitHub Actions CI/CD & Rollback Automation',
        topics: [
          'Automated lint, test, build, and artifact promotion pipelines.',
          'Zero-downtime deploy scripts and automated post-deploy smoke checks.',
          'Database backup verification and point-in-time recovery drills.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Observability, Incident Drills & Senior Infra Review',
        topics: [
          'Log aggregation, disk/RAM threshold alerts, and latency SLO dashboards.',
          'Live outage triage simulation and post-mortem documentation.',
          'Qualification for Fellowship infrastructure & deployment tracks.'
        ]
      }
    ]
  },
  'mobile-app-development': {
    id: 'mobile-app-development',
    name: 'Cross-Platform Mobile Engineering Sprints',
    shortName: 'Mobile Apps',
    tagline: 'React Native / Flutter State Architecture, Offline Caching, Push Alerts & Store Packaging',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Offline-first mobile apps connected to live APIs.',
    audience: 'Developers with JS/Dart/Web knowledge shipping production-grade iOS/Android mobile workflows.',
    outcome: 'Ship an offline-capable cross-platform mobile client featuring secure token storage, deep linking, push alerts, and CI release builds.',
    githubRepos: [
      {
        name: 'DBERT-Mobile / cross-platform-app-workbench',
        url: 'https://github.com/DBERT-Mobile/cross-platform-app-workbench',
        role: 'Applied Mobile App Engineer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Modular mobile navigation, encrypted local persistence, and REST/WebSocket synchronization.',
        keyModules: ['Typed Navigation', 'Offline Sync Queue', 'Biometric/Secure Auth', 'EAS / APK Release']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Mobile Architecture, Typed Routing & Design Fidelity',
        topics: [
          'Deep linking, guarded auth stacks, and accessible gesture patterns.',
          'Smooth 60fps FlatList virtualization and skeleton loading states.',
          'Adaptive layouts across small Android viewports and tablets.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'API Integration, Offline Queueing & Local Persistence',
        topics: [
          'TanStack Query / Riverpod caching with optimistic mutations.',
          'Secure Keychain/Keystore JWT refresh token rotation.',
          'Offline action outbox syncing cleanly on reconnect.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Native Capabilities, Push Notifications & Profiling',
        topics: [
          'Push notification channels, deep-link routing, and camera/file uploads.',
          'Eliminating UI thread jank and bundle bloat via profiling.',
          'Automated component tests for critical checkout/onboarding screens.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Signed Release Builds & Senior Mobile Audit',
        topics: [
          'Environment flavors, crash reporting, and signed AAB/IPA packaging.',
          'Senior PR walkthrough and performance checklist.',
          'Direct route into live mobile Fellowship product squads.'
        ]
      }
    ]
  },
  'cybersecurity': {
    id: 'cybersecurity',
    name: 'Application Security, OWASP & SOC Defense Sprints',
    shortName: 'Cybersecurity',
    tagline: 'OWASP Top 10 Pentesting, Auth/API Hardening, SIEM Telemetry & Incident Response',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Defensive & offensive auditing across real web APIs.',
    audience: 'CS/IT learners with networking & Linux basics ready to execute vulnerability audits, exploit reproduction, and remediation patches.',
    outcome: 'Deliver formal CVSS vulnerability reports, reproducible PoCs, patched API security controls, and SOC detection rules.',
    githubRepos: [
      {
        name: 'DBERT-Security / secops-audit-suite',
        url: 'https://github.com/DBERT-Security/secops-audit-suite',
        role: 'Applied Security & AppSec Engineer',
        badgeText: 'Accelerate Sprint Track',
        description: 'Automated OWASP scanners, IDOR/SSRF verification harnesses, and hardened middleware templates.',
        keyModules: ['OWASP API Audit', 'Burp & Nuclei Harnesses', 'JWT/RBAC Fixes', 'SIEM Alert Rules']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Threat Modeling & Reconnaissance Foundations',
        topics: [
          'Attack surface enumeration, HTTP proxy inspection, and TLS misconfiguration checks.',
          'Reading application routes to identify broken object-level authorization (BOLA/IDOR).',
          'Documenting attack trees and CVSS severity scoring.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'Exploitation & Remediation of OWASP API Risks',
        topics: [
          'Testing SQLi, XSS, SSRF, CSRF, and rate-limit bypasses in isolated labs.',
          'Auditing JWT signature validation, session fixation, and file upload sanitization.',
          'Writing remediation pull requests rather than report-only findings.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Container Security, Secrets Scanning & SOC Rules',
        topics: [
          'Integrating automated SAST/DAST & secret scanners into GitHub Actions.',
          'Parsing Nginx/auth logs for credential-stuffing anomalies and IP throttling.',
          'Building reproducible incident response playbooks.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Capstone Audit Dossier & Senior Security Review',
        topics: [
          'Delivering an executive vulnerability audit report + verified patch suite.',
          '1:1 security walkthrough with senior engineering reviewers.',
          'Eligibility for DBERT Fellowship SecOps & AppSec audits.'
        ]
      }
    ]
  },
  'digital-marketing': {
    id: 'digital-marketing',
    name: 'Technical SEO, Analytics Attribution & Growth Sprints',
    shortName: 'Digital Marketing',
    tagline: 'Schema JSON-LD, GA4 Funnel Attribution, Programmatic SEO & Performance Campaigns',
    price: '₹4,999',
    duration: '2 Months (8 Weeks)',
    scopeSummary: 'Applied Intermediate Track · Technical SEO, GA4 events & ROI attribution.',
    audience: 'Marketers and growth analysts moving from surface-level posts to technical SEO, GA4 funnel engineering, and CAC/LTV optimization.',
    outcome: 'Audit crawl architectures, ship Schema.org JSON-LD + GA4 conversion telemetry, and optimize full-funnel acquisition experiments.',
    githubRepos: [
      {
        name: 'DBERT-Growth / performance-marketing-suite',
        url: 'https://github.com/DBERT-Growth/performance-marketing-suite',
        role: 'Applied Growth & Technical SEO Analyst',
        badgeText: 'Accelerate Sprint Track',
        description: 'Programmatic landing page audits, GA4 event schemas, and multi-channel attribution calculators.',
        keyModules: ['Technical SEO & Sitemaps', 'GA4 Conversion Events', 'Landing Page CRO', 'CAC/ROAS Modeling']
      }
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Technical SEO, Crawlability & Structured Data',
        topics: [
          'Canonical tags, XML sitemaps, Core Web Vitals, and robots.txt architecture.',
          'Designing FAQPage, Course, JobPosting, and BreadcrumbList JSON-LD.',
          'Eliminating keyword cannibalization across multi-city landing pages.'
        ]
      },
      {
        period: 'Weeks 3–4',
        title: 'GA4 Telemetry, UTM Taxonomy & Funnel Attribution',
        topics: [
          'Strict UTM governance across email, WhatsApp, organic search, and paid ads.',
          'Instrumenting micro-conversion events and diagnosing checkout drop-offs.',
          'Building cohort payback and CAC/LTV sheets.'
        ]
      },
      {
        period: 'Weeks 5–6',
        title: 'Conversion Rate Optimization & Content Engines',
        topics: [
          'Above-the-fold clarity, trust proof placement, and A/B test hypotheses.',
          'Distributing technical case studies across LinkedIn, organic search, and newsletters.',
          'Structuring LLM discovery (`llms.txt`) and high-intent comparison pages.'
        ]
      },
      {
        period: 'Weeks 7–8',
        title: 'Growth Audit Portfolio & Senior Funnel Review',
        topics: [
          'Presenting a live acquisition + SEO audit backed by verifiable metrics.',
          '1:1 mentor review covering channel economics and reporting clarity.',
          'Direct entry path into DBERT Fellowship growth & analytics squads.'
        ]
      }
    ]
  }
};
