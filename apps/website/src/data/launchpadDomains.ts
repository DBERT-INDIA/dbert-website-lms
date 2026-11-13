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
  },

  'ui-ux-design': {
    id: 'ui-ux-design',
    name: 'UI/UX Design & Product Experience Systems',
    shortName: 'UI/UX Design',
    tagline: 'Figma Auto-Layout, Design Tokens, User Research & Clickable Prototypes',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Aspiring UI/UX designers, product thinkers, and frontend engineers who want to master design systems, user flows, and Figma prototyping.',
    outcome: 'Architect complete design systems in Figma, conduct user research, build interactive high-fidelity prototypes, and package specs for production engineering handoff.',
    githubRepos: [
      {
        name: 'DBERT-Design / dbert-design-system',
        url: 'https://github.com/DBERT-INDIA/dbert-design-tokens',
        role: 'Lead UI/UX & Design Systems Engineer',
        badgeText: 'DBERT Experience Lab',
        description: 'Comprehensive Figma design tokens, WCAG AA/AAA accessible components, typography scales, and responsive interaction prototypes.',
        keyModules: ['Figma Auto-Layout Matrices', 'Design Tokens Schema', 'WCAG Contrast Audits', 'Interactive Prototype Specs']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'User Research, Information Architecture & Figma Foundations',
        topics: [
          'Qualitative user research: conducting user interviews, building empathy maps, and drafting user personas.',
          'Information architecture: card sorting, sitemap design, and user journey flow diagramming.',
          'Figma interface mastery: vectors, constraints, Auto-Layout flex properties, and responsive resizing.',
          'Low-fidelity wireframing: visual hierarchy, Gutenberg diagram, and rapid grayscale prototype testing.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Design Systems, Tokens, Usability Testing & Developer Handoff',
        topics: [
          'Design tokens: establishing semantic color palettes, modular typography scales, and WCAG AA contrast compliance.',
          'Component architecture: variant matrices, boolean properties, and interactive component state animations.',
          'Usability audits: Nielsen Norman heuristics, moderated walkthroughs, and error recovery analysis.',
          'Capstone Shipment: Delivering an end-to-end clickable mobile or web SaaS prototype with developer handoff specs.'
        ]
      }
    ]
  },

  'devops-cloud': {
    id: 'devops-cloud',
    name: 'Cloud Infrastructure & DevOps Engineering',
    shortName: 'DevOps & Cloud',
    tagline: 'Docker Multi-Stage Builds, Kubernetes Clusters, AWS Architecture & CI/CD Pipelines',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Backend developers and systems engineers aiming to master container orchestration, automated cloud infrastructure, and CI/CD pipelines.',
    outcome: 'Deploy resilient containerized microservices to cloud environments using Docker, Kubernetes, GitHub Actions, and Terraform with Prometheus observability.',
    githubRepos: [
      {
        name: 'DBERT-Cloud / infrastructure-blueprints',
        url: 'https://github.com/DBERT-INDIA/cloud-infra-blueprints',
        role: 'DevOps & Site Reliability Engineer',
        badgeText: 'DBERT Cloud Lab',
        description: 'Production-ready Terraform configurations, Kubernetes deployment manifests, and GitHub Actions CI/CD workflows for containerized applications.',
        keyModules: ['Multi-Stage Dockerfiles', 'Kubernetes Ingress & Secrets', 'GitHub Actions CI/CD', 'Prometheus & Grafana Monitoring']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Linux Systems, Cloud Networks & Docker Containerization',
        topics: [
          'Linux systems administration: file permissions, systemd daemon management, and shell automation scripts.',
          'Cloud networking: AWS VPC topology, CIDR subnets, security groups, and IAM least-privilege security.',
          'Docker containerization: writing efficient multi-stage Dockerfiles, non-root user policies, and layer caching.',
          'Multi-container environments: orchestration with Docker Compose, volume mounts, and network isolation.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Kubernetes Orchestration, CI/CD Automation & Observability',
        topics: [
          'Kubernetes fundamentals: Pods, Deployments, ReplicaSets, ClusterIP, and Ingress routing controllers.',
          'CI/CD automation: building automated build, test, and container release pipelines with GitHub Actions.',
          'Infrastructure monitoring: metric collection with Prometheus, Grafana visualization dashboards, and alerting rules.',
          'Capstone Shipment: Building and deploying a zero-downtime containerized application with automated CI/CD and metrics.'
        ]
      }
    ]
  },

  'mobile-app-development': {
    id: 'mobile-app-development',
    name: 'Cross-Platform Mobile App Engineering',
    shortName: 'Mobile Apps',
    tagline: 'React Native & Flutter, Device Hardware APIs, Offline State & Store Deployment',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Frontend and full-stack developers looking to build high-performance native iOS and Android applications with modern cross-platform tech.',
    outcome: 'Build, optimize, and ship production-ready mobile apps featuring offline caching, push notifications, native hardware integration, and store bundles.',
    githubRepos: [
      {
        name: 'DBERT-Mobile / cross-platform-app-workbench',
        url: 'https://github.com/DBERT-INDIA/mobile-app-workbench',
        role: 'Mobile Application Engineer',
        badgeText: 'DBERT Mobile Lab',
        description: 'Full-featured cross-platform mobile application with offline-first synchronization, native camera integration, and background push notifications.',
        keyModules: ['React Native Navigation', 'AsyncStorage Local Cache', 'Camera & Hardware APIs', 'AAB Release Builds']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Mobile Architecture, Responsive Layouts & Navigation',
        topics: [
          'Mobile UI foundations: React Native core components (View, Text, ScrollView), flexbox styling, and safe-area insets.',
          'Navigation patterns: configuring Native Stack, Bottom Tabs, and Drawer navigation with deep linking.',
          'State management: managing asynchronous application state with Context API, Redux Toolkit, or Zustand.',
          'Hardware integrations: camera capture, image picker, device geolocation, and runtime permission handling.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Offline Storage, Performance Optimization & App Store Builds',
        topics: [
          'Offline-first architecture: local persistent storage with AsyncStorage/SQLite, optimistic UI updates, and synchronization.',
          'Performance profiling: 60fps list virtualization with FlatList/FlashList, memory optimization, and Hermes engine tuning.',
          'Push notifications: integrating Firebase Cloud Messaging (FCM) on iOS and Android devices.',
          'Capstone Shipment: Generating production signed Android App Bundles (AAB) and deploying an interactive mobile app capstone.'
        ]
      }
    ]
  },

  'cybersecurity': {
    id: 'cybersecurity',
    name: 'Cybersecurity, SOC Analysis & Ethical Hacking',
    shortName: 'Cybersecurity',
    tagline: 'STRIDE Threat Modeling, OWASP Top 10, Penetration Testing & SIEM Log Analysis',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Engineers, IT professionals, and security enthusiasts seeking practical skills in vulnerability assessment, threat analysis, and security operations.',
    outcome: 'Execute structured web penetration tests, analyze SIEM security events, audit systems against OWASP Top 10, and draft executive remediation reports.',
    githubRepos: [
      {
        name: 'DBERT-Security / secops-audit-suite',
        url: 'https://github.com/DBERT-INDIA/secops-audit-suite',
        role: 'Information Security & SOC Analyst',
        badgeText: 'DBERT Security Operations',
        description: 'Applied security assessment suite featuring automated vulnerability scanners, SIEM log analyzers, and OWASP remediation playbooks.',
        keyModules: ['OWASP Top 10 Auditing', 'Wireshark Packet Analysis', 'Burp Suite Testing Playbooks', 'CVSS Risk Scoring Engine']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'Threat Modeling, Network Analysis & Cryptography',
        topics: [
          'Information security foundations: CIA triad, defense-in-depth architecture, and STRIDE threat modeling.',
          'Network packet inspection: analyzing TCP/IP, DNS, and TLS handshakes with Wireshark to detect network anomalies.',
          'Applied cryptography: symmetric/asymmetric ciphers, hashing algorithms, digital signatures, and public key infrastructure (PKI).',
          'Vulnerability scanning: host discovery, port scanning, and service version enumeration using Nmap.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Web Application Penetration Testing & SOC Operations',
        topics: [
          'OWASP Top 10: exploiting and remediating SQL Injection, Cross-Site Scripting (XSS), BOLA/IDOR, and SSRF flaws.',
          'Proxy intercept tools: auditing HTTP traffic, fuzzing parameters, and testing authentication flows with Burp Suite.',
          'SOC monitoring: triaging alerts, analyzing security logs in SIEM (Splunk/Elastic), and following incident response playbooks.',
          'Capstone Shipment: Conducting a full-scope penetration test on a test environment and drafting a CVSS-scored remediation report.'
        ]
      }
    ]
  },

  'digital-marketing': {
    id: 'digital-marketing',
    name: 'Growth Engineering & Digital Performance Marketing',
    shortName: 'Digital Marketing',
    tagline: 'Technical SEO, Meta & Google Ads, Google Analytics 4 & Conversion Funnels',
    price: '₹7,999',
    duration: '2 months',
    audience: 'Marketers, founders, and growth enthusiasts looking to engineer scalable customer acquisition funnels using data-driven marketing tools.',
    outcome: 'Execute technical SEO audits, manage high-ROI Google & Meta ad campaigns, instrument GA4 custom event tracking, and optimize conversion funnels.',
    githubRepos: [
      {
        name: 'DBERT-Growth / performance-marketing-suite',
        url: 'https://github.com/DBERT-INDIA/growth-marketing-suite',
        role: 'Growth Marketing & Funnel Optimization Engineer',
        badgeText: 'DBERT Growth Lab',
        description: 'Comprehensive performance marketing toolkit: technical SEO audit scripts, conversion event tracking blueprints, and ad attribution models.',
        keyModules: ['Technical SEO Auditing', 'GA4 Custom Event Setup', 'Google/Meta Campaign Blueprints', 'LTV/CAC Financial Modeling']
      }
    ],
    curriculum: [
      {
        period: 'Month 1 (Weeks 1–4)',
        title: 'SEO Foundations, Technical Auditing & On-Page Optimization',
        topics: [
          'Keyword research: search intent mapping, search volume analysis, and semantic content gap identification.',
          'On-page SEO: optimizing title tags, meta descriptions, semantic heading hierarchies, and internal linking structures.',
          'Technical SEO: Core Web Vitals (LCP, INP, CLS), crawl budgets, XML sitemaps, robots.txt, and Schema.org JSON-LD markup.',
          'Content marketing: developing high-converting educational content briefs, distribution strategies, and lead magnets.'
        ]
      },
      {
        period: 'Month 2 (Weeks 5–8)',
        title: 'Paid Acquisition, Conversion Analytics & Growth Funnels',
        topics: [
          'Google Ads: search campaign structure, keyword match types, Quality Score optimization, and negative keyword lists.',
          'Meta Ads: audience segmentation, custom & lookalike audiences, Meta Pixel / CAPI setup, and creative testing frameworks.',
          'Web analytics: Google Analytics 4 custom event tracking, conversion funnels, multi-touch attribution, and cohort retention.',
          'Capstone Shipment: Building and presenting an end-to-end multi-channel acquisition funnel with forecasted ROAS and budget allocation.'
        ]
      }
    ]
  }

};
