export interface InternRepoReference {
  name: string;
  url: string;
  role: string;
  badgeText?: string;
  description: string;
  keyModules: string[];
}

export interface LaunchpadDomain {
  id: string;
  name: string;
  shortName: string;
  tagline: string;
  price: string;
  duration: string;
  audience: string;
  outcome: string;
  githubRepos: InternRepoReference[];
  curriculum: {
    period: string;
    title: string;
    topics: string[];
  }[];
}

export const LAUNCHPAD_DOMAINS: Record<string, LaunchpadDomain> = {
  'data-analytics': {
    id: 'data-analytics',
    name: 'Data Analytics & Automated Business Intelligence',
    shortName: 'Data Analytics',
    tagline: 'Automated CSV Ingestion, Semantic Classification, Driver Decomposition & Executive Dashboards',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Aspiring data analysts, BI developers, and engineers seeking practical mastery in automated data ingestion, semantic column typing, variance decomposition, and dashboard generation.',
    outcome: 'Build an automated analytics platform modeled after Aivara Insight Lite: parse arbitrary CSVs, compute KPIs and driver decompositions in Pandas, integrate budget-capped LLM insights, and export offline PowerPoint decks.',
    githubRepos: [
      {
        name: 'Aivara-Technologies / aivara-insight-lite',
        url: 'https://github.com/Aivara-Technologies/aivara-insight-lite',
        role: 'Business Intelligence & Automated Analytics Engineer',
        badgeText: 'Aivara Technologies Cohort',
        description: 'A locally-hosted analytics application that takes arbitrary CSVs, infers structure, computes KPIs and driver decompositions in pandas, generates natural-language insights via OpenRouter, and exports offline PowerPoint (.pptx) slide decks.',
        keyModules: ['Robust CSV Sniffer & Loader', 'Semantic Column Classifier', 'Driver Decomposition Engine', 'python-pptx Deck Builder']
      },
      {
        name: 'Alkameinc / alkame-nifty-50-educational',
        url: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
        role: 'Quantitative Financial Analyst & Time-Series Engineer',
        badgeText: 'Alkame Quantitative Track',
        description: 'Quantitative market data analysis engine for the Nifty 50 index — real-time market data fetchers, feature engineering, statistical backtesting, risk indicators, and Plotly Dash visualizers.',
        keyModules: ['Time-Series Data Ingestion', 'Financial Feature Engineering', 'Strategy Backtesting Simulator', 'Interactive Risk Dashboards']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Robust Data Ingestion, Semantic Classification & Pandas Analytics Core',
        topics: [
          'Robust CSV ingestion: handling unknown delimiters with csv.Sniffer, encoding detection via charset-normalizer, header row inference, and error-tolerant row reading.',
          'Semantic column classification: rule-based typing for dates, continuous metrics, grouping dimensions, and unique IDs, with budget-aware LLM fallback for ambiguous schemas.',
          'Local analytics computation: automated summary KPI extraction, period-over-period delta calculation, rolling time-series aggregation, and ratio metrics.',
          'Driver & variance decomposition: computing categorical contribution shares ("what explains the lift"), dimension ranking by explanatory power, and top-contributor sorting.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Anomaly Detection, Dashboarding, LLM Fact Packets & Local PPTX Export',
        topics: [
          'Statistical anomaly detection: flagging risk signals using z-scores, interquartile range (IQR) spreads, and sudden period-over-period variance deviations.',
          'Interactive dashboard development: building multi-tab Streamlit / Plotly interfaces featuring KPI cards, trend line charts, and dimensional breakdown bar plots.',
          'LLM narrative insight layer & budget guardrails: constructing compact JSON facts packets, content-hash caching, and enforcing daily free-tier token ceilings.',
          'Capstone Shipment: Building and deploying an end-to-end automated analytics platform with offline PowerPoint (.pptx) deck generation using python-pptx and Plotly kaleido.'
        ]
      }
    ]
  },

  'ai-agent-development': {
    id: 'ai-agent-development',
    name: 'AI Agent Development',
    shortName: 'AI Agents',
    tagline: 'Multi-Agent State Machines, Local Inference & Tool Execution',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Beginners, college engineers, and developers wanting to architect autonomous agents that call tools, maintain vector memory, and run privacy-preserving local models.',
    outcome: 'Engineer autonomous multi-agent state machines, bind LLMs to strict Pydantic tool schemas, build local RAG pipelines, and ship an auditable agent assistant directly to GitHub.',
    githubRepos: [
      {
        name: 'DBERT-INDIA / dbert-agent',
        url: 'https://github.com/DBERT-INDIA/dbert-agent',
        role: 'Autonomous Agent & Tool Systems Engineer',
        badgeText: 'DBERT Core Agent Lab',
        description: 'A local-first, privacy-first AI assistant running on laptops — chat, document RAG, SQLite vector memory, deep research loops, voice I/O (Whisper/Piper), and MCP tool calling.',
        keyModules: ['Local LM Studio/Ollama Runtimes', 'Document Chunking & Vector RAG', 'Tool Calling Permission Layer', 'MCP External Tool Clients']
      },
      {
        name: 'Gayatri-Education / Gayatri-AI',
        url: 'https://github.com/Gayatri-Education/Gayatri-AI',
        role: 'Agentic Research & Coordinator Engineer',
        badgeText: 'Gayatri Agentic Squad',
        description: 'Multi-agent coordination topologies (planner/executor/critic), recursive search tree decomposition, cross-source web evidence verification, and real-time streaming interfaces.',
        keyModules: ['Multi-Agent Supervisor Routing', 'Recursive Web Scraping Trees', 'Citation Grounding Engine', 'Streaming Response Emitter']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Local Runtimes, Tool Calling & RAG Architecture',
        topics: [
          'Python development environment setup, managing virtual environments, and executing open-weights models locally via LM Studio & Ollama OpenAI-compatible endpoints.',
          'Function calling schemas: defining strict input/output validation models with Pydantic, structured JSON parsing, and building security permission gates for tool execution.',
          'Document RAG pipelines: ingesting PDFs and markdown files, chunking strategies, generating local vector embeddings, and persistent SQLite vector storage.',
          'Persistent conversational memory: storing conversation turns, semantic similarity retrieval across past chat histories, and prompt context window management.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Autonomous Research, Voice I/O & Production Deployment',
        topics: [
          'Multi-step autonomous deep research: building query decomposition loops, iterative web search scraping, source validation, and citation-grounded report synthesis.',
          'Voice integration: integrating offline speech-to-text (Whisper) and text-to-speech (Piper) for a hands-free, terminal-driven conversational loop.',
          'Model Context Protocol (MCP): connecting agent runtimes to external MCP tool servers, headless job automation, and URL monitoring scripts.',
          'Capstone Shipment: Architecting, testing, and shipping an auditable, local-first multi-agent desktop/CLI assistant to a public GitHub repository under senior review.'
        ]
      }
    ]
  },

  'generative-ai': {
    id: 'generative-ai',
    name: 'Generative AI',
    shortName: 'Generative AI',
    tagline: 'Multi-Model LLM Engineering, Deep Research & Knowledge Extraction',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Aspiring AI engineers, students, and software developers aiming to build commercial-grade GenAI pipelines, multi-provider LLM integrations, and context retrieval engines.',
    outcome: 'Master foundational prompt orchestration, multi-provider API integrations (OpenAI, Anthropic, Gemini), dynamic context window management, and deep web research agents.',
    githubRepos: [
      {
        name: 'Gayatri-Education / Gayatri-AI',
        url: 'https://github.com/Gayatri-Education/Gayatri-AI',
        role: 'Enterprise GenAI & RAG Systems Engineer',
        badgeText: 'Gayatri Core GenAI',
        description: 'Production Generative AI system featuring deep web research synthesis, multi-provider LLM abstraction, intelligent context pruning, SQLite session persistence, and real-time streaming UI.',
        keyModules: ['Multi-Provider LLM Clients', 'Context & Memory Management', 'Deep Research Engine', 'Real-time UI Streaming']
      },
      {
        name: 'DBERT-INDIA / dbert-agent',
        url: 'https://github.com/DBERT-INDIA/dbert-agent',
        role: 'Local-First & Private AI Assistant Engineer',
        badgeText: 'DBERT Privacy Lab',
        description: 'Privacy-first Generative AI stack running 100% air-gapped on personal workstations — document RAG chunking, persistent local embeddings, and permission-gated file operations.',
        keyModules: ['Local Document RAG', 'Zero-Data-Leakage Inference', 'Permission Safety Gates', 'Local Vector Embeddings']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'LLM Foundations, Multi-Provider Architecture & Context Management',
        topics: [
          'Generative AI system architecture: understanding tokens, temperature, context limits, and building a unified client interface for OpenAI, Anthropic, and Gemini models.',
          'Advanced prompt engineering & output guarantees: few-shot conditioning, chain-of-thought prompting, schema extraction, and JSON enforcement.',
          'Context window optimization: sliding window buffers, token trimming algorithms, semantic summarization of long chat histories, and SQLite session persistence.',
          'Multi-agent conversational topologies: structuring planner, executor, and critic agent workflows for multi-step reasoning tasks.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Live Web Grounding, Deep Research & Interactive Application',
        topics: [
          'Real-time web search integration: crawling search engines, extracting and sanitizing HTML content, and handling rate limits without blocking inference loops.',
          'Deep research synthesis engine: recursive search decomposition, multi-source cross-verification, and structured markdown report generation with inline citations.',
          'Interactive UI & token streaming: implementing Server-Sent Events (SSE) / streaming responses, token-by-token rendering, and real-time error handling.',
          'Capstone Shipment: Building and deploying a full-featured generative research assistant with persistent memory, multi-provider fallbacks, and live UI to GitHub.'
        ]
      }
    ]
  },

  'machine-learning': {
    id: 'machine-learning',
    name: 'Machine Learning & LLM Fine-Tuning',
    shortName: 'Machine Learning',
    tagline: 'Data Pipelines, Open-Weights LLM Fine-Tuning & Model Evaluation',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Developers, STEM students, and data practitioners seeking hands-on mastery in data preprocessing, supervised ML algorithms, and fine-tuning local open-weights LLMs (Llama-3).',
    outcome: 'Build end-to-end ML data pipelines, train supervised models, curate synthetic instruction datasets, fine-tune open-weights LLMs using LoRA/QLoRA, and benchmark model weights.',
    githubRepos: [
      {
        name: 'Gayatri-Education / Gayatri-Tutor-V3',
        url: 'https://github.com/Gayatri-Education/Gayatri-Tutor-V3',
        role: 'LLM Fine-Tuning & Synthetic Data Engineer',
        badgeText: 'Gayatri EdTech Track',
        description: 'End-to-end open-source pipeline for local Llama model fine-tuning, automated synthetic training data generation, patch validation, and model weight evaluation.',
        keyModules: ['Synthetic Dataset Generation', 'LoRA / QLoRA Fine-Tuning', 'Quantization (GGUF)', 'Model Evaluation & Benchmarking']
      },
      {
        name: 'Alkameinc / alkame-nifty-50-educational',
        url: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
        role: 'Statistical Modeling & Quantitative ML Engineer',
        badgeText: 'Quantitative Systems Track',
        description: 'Applied machine learning pipeline with supervised regression and ensemble classification (Random Forests, XGBoost), feature importance ranking, loss curve tracking, and algorithmic backtesting.',
        keyModules: ['Ensemble Model Trainer', 'Feature Selection Pipeline', 'Hyperparameter Optimization', 'Strategy Backtest Validator']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Data Engineering, Feature Pipelines & Applied Machine Learning',
        topics: [
          'Python for scientific computing: vectorized operations with NumPy, data cleansing and manipulation with Pandas, handling missing values and anomalies.',
          'Feature engineering & selection: categorical encodings, scaling transformations, rolling statistics, and correlation matrix analysis.',
          'Supervised model architectures: Linear/Logistic Regression, Decision Trees, Random Forests, XGBoost, and hyperparameter optimization with cross-validation.',
          'Model evaluation & validation: confusion matrices, Precision/Recall trade-offs, ROC-AUC curves, and building reproducible scikit-learn preprocessing pipelines.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Synthetic Data Curation, LLM Fine-Tuning & Model Deployment',
        topics: [
          'Dataset curation: generating synthetic instruction-response pairs, formatting training datasets (Alpaca/ShareGPT schemas), and programmatic quality filtering.',
          'Parameter-Efficient Fine-Tuning (PEFT): setting up LoRA & QLoRA configurations on open-weights models (Llama-3 / Mistral), tracking training loss curves.',
          'Model quantization & export: converting fine-tuned adapters into 4-bit/8-bit GGUF formats and running local inference using Ollama and vLLM.',
          'Capstone Shipment: Training, evaluating, and deploying a specialized domain-adapted model with benchmark metrics and a live inference API published to GitHub.'
        ]
      }
    ]
  },

  'python-automation': {
    id: 'python-automation',
    name: 'Python Automation',
    shortName: 'Python Automation',
    tagline: 'Dynamic Scraping, Scheduled Bots & Automated Workflows',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Beginners, career switchers, and operational professionals who want to automate real corporate tasks, parse business spreadsheets, and build background worker bots.',
    outcome: 'Master core Python programming, build web scrapers that bypass anti-bot challenges, orchestrate email automation workflows with Flask, and deploy scheduled cron jobs.',
    githubRepos: [
      {
        name: 'Gayatri-Education / gayatribot-Hr',
        url: 'https://github.com/Gayatri-Education/gayatribot-Hr',
        role: 'Business Process Automation & Email Systems Engineer',
        badgeText: 'Gayatri Enterprise Ops',
        description: 'Production HR automation bot featuring automated offer letter generation, applicant pipeline filtering, SMTP email delivery with logging, and a Flask control dashboard.',
        keyModules: ['Automated SMTP Email Dispatch', 'Flask Control Hub', 'SQLite Candidate Tracking', 'Scheduled Pipeline Automation']
      },
      {
        name: 'Alkameinc / alkame-nifty-50-educational',
        url: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
        role: 'Data Scraping & Scheduled Pipeline Engineer',
        badgeText: 'Data Pipeline Track',
        description: 'Automated market announcement fetchers, corporate event scraping pipelines, scheduled cron jobs, and automated webhook alerts for operational data extraction.',
        keyModules: ['Automated Web Fetchers', 'Dynamic Scraping & Throttling', 'Cron Task Scheduler', 'Webhook Alerting']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Python Fundamentals, Data Parsing & Email Automation',
        topics: [
          'Python programming essentials: data structures (lists, dicts, tuples), file I/O operations, robust exception handling, and standard logging configurations.',
          'Document & tabular data processing: reading, transforming, and writing Excel (.xlsx) and CSV files, JSON parsing, and validation using Pydantic.',
          'Automated communication services: SMTP and IMAP protocol integration, dynamic HTML email template rendering, and automated PDF attachment generation.',
          'Relational database logging: designing SQLite schemas, tracking workflow states, transaction auditing, and archiving processed records.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Web Scraping, Dashboard Control & Scheduled Bot Systems',
        topics: [
          'Web automation & data extraction: building scrapers with BeautifulSoup and Playwright, handling pagination, session cookies, and anti-bot retry logic.',
          'Control dashboard with Flask: developing lightweight REST endpoints, admin controls for starting/pausing pipelines, and status monitoring.',
          'Cron scheduling & error recovery: setting up background task execution, headless deployment, exponential backoff, and alerting webhooks (Discord/Slack).',
          'Capstone Shipment: Engineering an end-to-end candidate onboarding or data aggregation bot with a web dashboard, audit logs, and GitHub documentation.'
        ]
      }
    ]
  },

  'full-stack-development': {
    id: 'full-stack-development',
    name: 'Full Stack Development',
    shortName: 'Full Stack',
    tagline: 'Modern React/Next.js Frontends, Python APIs & Docker Deployments',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Beginners and aspiring software engineers wanting to learn complete end-to-end web engineering: from interactive UI components to backend APIs and databases.',
    outcome: 'Architect modern full-stack web applications with Next.js/React, build robust Python/Flask backends, manage relational databases, and containerize systems with Docker.',
    githubRepos: [
      {
        name: 'Gayatri-Education / Intern-workbench',
        url: 'https://github.com/Gayatri-Education/Intern-workbench',
        role: 'Frontend Architecture & Product UI Engineer',
        badgeText: 'Gayatri Frontend Track',
        description: 'Full-stack candidate and intern management workbench featuring a modern React frontend, Python API backend, database migrations, and Docker Compose orchestration.',
        keyModules: ['React/Next.js Interface', 'Role-Based Navigation', 'Client State Management', 'Modern Component System']
      },
      {
        name: 'DBERT-INDIA / Internshipportal',
        url: 'https://github.com/DBERT-INDIA/Internshipportal',
        role: 'Backend Systems & API Infrastructure Engineer',
        badgeText: 'DBERT Systems Lab',
        description: 'Full-scale enterprise internship portal with Python/Flask backend, relational database schema migrations with Alembic, session auth, automated test suites, and Docker deployment.',
        keyModules: ['Flask RESTful APIs', 'Alembic DB Migrations', 'Auth & Session Security', 'Docker Compose Infrastructure']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Modern Frontend Architecture & RESTful API Foundations',
        topics: [
          'Frontend fundamentals: TypeScript, modern React component lifecycles, hooks (useState, useEffect, useMemo), and modular CSS styling.',
          'Client-side state management, responsive UI design, accessible layouts, and seamless asynchronous API communication (Fetch/Axios).',
          'Backend engineering with Python: designing RESTful endpoints with Flask/FastAPI, routing, request validation, and error response formatting.',
          'Relational database architecture: modeling entities in PostgreSQL / SQLite, database migrations with Alembic, and writing efficient CRUD queries.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Authentication, Full-Stack Integration & Containerized Deployment',
        topics: [
          'User authentication & security: password hashing (bcrypt), JWT tokens, session cookies, and role-based access control (RBAC) middleware.',
          'Interactive dashboards: building multi-role management interfaces, file uploads, real-time status feeds, and data export features.',
          'Docker containerization: writing efficient multi-stage Dockerfiles, composing multi-service architectures (frontend, backend, database) with Docker Compose.',
          'Capstone Shipment: Building and deploying a complete multi-role web portal to a cloud platform, verified with automated tests and a production GitHub repo.'
        ]
      }
    ]
  }
};
