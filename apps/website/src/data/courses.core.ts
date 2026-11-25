import type { FellowshipTrack } from './courses.types';

export const CORE_FELLOWSHIP_TRACKS: FellowshipTrack[] = [
  {
    id: 'ai-agent-development',
    slug: 'ai-agent-development',
    canonicalPath: '/learners/courses/ai-agent-development',
    name: 'AI Agent Development',
    shortName: 'AI Agent Engineering',
    badge: 'Trending #1',
    category: 'AI & Data',
    featured: true,
    displayOrder: 1,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Build and evaluate tool-using AI agents that plan, execute, recover from errors, and request human approval on real venture codebases.',
    shortDescription:
      'Autonomous multi-agent state machines, tool calling loops, and local LLM runtime deployment ending in a reviewed production agent.',
    fullDescription:
      'The AI Agent Development track focuses on deterministic agent orchestration, state persistence, permission boundaries, and structured tool execution. Rather than building single-prompt wrappers, fellows contribute pull requests to active DBERT agent workflows using LangGraph, CrewAI, FastAPI, and local Ollama/vLLM runtimes.',
    whoShouldApply: [
      'Final-year CS/IT students and working developers who already write clean Python.',
      'Engineers who want verifiable pull-request experience on multi-agent orchestration rather than toy chatbot notebooks.',
      'Builders interested in local open-weights inference, tool calling, and reliable agent evaluation.',
    ],
    prerequisites: [
      'Working fluency in Python (functions, classes, async/await, JSON parsing, exception handling).',
      'Basic familiarity with Git branching, pull requests, and REST APIs.',
      'If you are new to Python or Git, start with DBERT Launchpad or Accelerate first.',
    ],
    outcomes: [
      'Design cyclical agent state graphs with explicit memory, retries, and human-in-the-loop approval checkpoints.',
      'Implement schema-validated tool/function calling with strict permission boundaries and failure recovery.',
      'Serve open-weights models locally via Ollama/vLLM and benchmark token latency.',
      'Ship reviewed pull requests and earn a verifiable 3-document credential packet.',
    ],
    technologies: [
      { name: 'LangGraph', role: 'Cyclical multi-agent state machines and human-in-the-loop checkpoints' },
      { name: 'CrewAI', role: 'Role-based agent delegation and structured task handoffs' },
      { name: 'Ollama & vLLM', role: 'Local and self-hosted open-weights LLM inference' },
      { name: 'FastAPI', role: 'Async streaming APIs and Pydantic-validated tool endpoints' },
      { name: 'PostgreSQL + pgvector', role: 'Persistent agent state and hybrid vector memory' },
      { name: 'Docker & Git', role: 'Reproducible sprint environments and reviewed PR workflows' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Agent Loops, State & Local Model Runtimes',
        topics: [
          'Deterministic JSON tool calling and Pydantic schema validation',
          'Local open-weights serving with Ollama and vLLM',
          'Git workflow, environment setup, and first reviewed PR',
        ],
        deliverable: 'Schema-validated tool-calling agent running against a local model endpoint.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Stateful Orchestration with LangGraph & CrewAI',
        topics: [
          'State graphs, conditional routing, and retry/backoff policies',
          'Role-based delegation trade-offs (LangGraph vs CrewAI)',
          'Short-term and persistent PostgreSQL/pgvector memory',
        ],
        deliverable: 'Multi-step research/task agent with persistent state and fallback handling.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Human-in-the-Loop, Security & Tracing',
        topics: [
          'Permission boundaries and approval gates for side-effecting tools',
          'Prompt-injection defenses and output guardrails',
          'Execution tracing, token budgets, and regression benchmarks',
        ],
        deliverable: 'Audited PR adding approval gates and evaluation traces to an active squad repo.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Capstone Hardening & Credential Release',
        topics: [
          'Integration testing and latency optimization',
          'Architecture decision records (ADRs) and Turnitin originality check',
          'Final senior engineer review and credential packet issuance',
        ],
        deliverable: 'Production capstone PR, technical dossier, and 3-document verifiable credential.',
      },
    ],
    capstone: {
      title: 'Multi-Agent Research & Support Workflow',
      description:
        'Contribute an evaluated tool-using agent workflow to Gayatri AI or an approved internal DBERT squad repository, complete with permission gates, structured citations, and failure recovery.',
      status: 'active',
      ventureName: 'Gayatri AI',
      repositoryUrl: 'https://github.com/Gayatri-Education/Gayatri-AI',
      acceptanceCriteria: [
        'All tool schemas validated via Pydantic with zero unhandled exceptions.',
        'Human-in-the-loop gate enforced before any state-mutating action.',
        'Unit and integration tests passing in CI with Turnitin < 5% on documentation.',
      ],
    },
    evaluation: [
      'Code Quality & Typing: Strict Python typing, modular architecture, and clean linting.',
      'Architecture & Security: Safe tool permissions, zero hardcoded secrets, clean DB migrations.',
      'Practical Testing: Reproducible Docker/local setup and passing integration tests.',
      'Documentation: Clear README, architecture notes, and PR walkthrough.',
    ],
    faqs: [
      {
        question: 'What prior Python experience do I need?',
        answer:
          'You should be comfortable with Python functions, classes, dictionaries, async/await, and basic REST API calls. Beginners should start with DBERT Launchpad.',
      },
      {
        question: 'Do I need paid OpenAI/Anthropic API credits?',
        answer:
          'No. We emphasize local open-weights inference with Ollama and vLLM so you can build and test without recurring token bills.',
      },
      {
        question: 'What does the ₹1,999 fee cover?',
        answer:
          'It is the total program fee for the 2-month fellowship, covering 1-on-1 mentorship, senior PR reviews, active repository assignment, and verifiable 3-document credential issuance.',
      },
    ],
    relatedSlugs: ['generative-ai', 'machine-learning', 'python-automation'],
    regionalOpportunities: [
      {
        title: 'AI Workflow Automation & Agent Orchestrator Intern',
        roleDescription: 'Orchestrate multi-step LLM task graphs and human-in-the-loop review nodes.',
        cityTag: 'Bengaluru',
        location: 'Bengaluru · Hybrid / Remote',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/ai-workflow-automation-intern-bangalore-remote-10',
        tags: ['LangGraph', 'CrewAI', 'Redis', 'Python'],
      },
      {
        title: 'Agentic Search & Retrieval Intern',
        roleDescription: 'Design hybrid dense-sparse retrievers and citation validation nodes.',
        cityTag: 'Delhi NCR',
        location: 'Delhi NCR · Remote',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/agentic-search-systems-intern-delhi-ncr-remote-11',
        tags: ['RAG', 'pgvector', 'FastAPI'],
      },
      {
        title: 'Production RAG Pipeline Remote Intern',
        roleDescription: 'Build end-to-end question-answering systems with semantic cache layers.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/rag-pipeline-engineering-intern-remote-1',
        tags: ['RAG', 'Ollama', 'FastAPI', 'LangGraph'],
      },
    ],
  },
  {
    id: 'generative-ai',
    slug: 'generative-ai',
    canonicalPath: '/learners/courses/generative-ai',
    name: 'Generative AI Systems',
    shortName: 'Generative AI & LLMs',
    badge: 'High Impact',
    category: 'AI & Data',
    featured: true,
    displayOrder: 2,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Build an evaluated LLM application using document ingestion, hybrid retrieval, reranking, and reliable inference serving.',
    shortDescription:
      'Document chunking, embeddings, hybrid BM25 + vector retrieval, RAG evaluation harnesses, and streaming LLM backends.',
    fullDescription:
      'The Generative AI Systems track teaches the engineering behind reliable retrieval-augmented generation and LLM serving. Fellows build ingestion pipelines, hybrid search with pgvector/ChromaDB, automated RAG evaluation benchmarks, and streaming FastAPI endpoints.',
    whoShouldApply: [
      'Python developers and CS graduates aiming to build production RAG and LLM systems.',
      'Engineers tired of fragile prompt demos who want measurable retrieval and generation quality.',
    ],
    prerequisites: [
      'Solid Python fundamentals and familiarity with HTTP/JSON APIs.',
      'Basic SQL knowledge and Git workflow comfort.',
    ],
    outcomes: [
      'Build document ingestion and chunking pipelines for PDFs, markdown, and structured records.',
      'Implement hybrid retrieval (dense embeddings + BM25) with reranking.',
      'Measure faithfulness and context recall using structured RAG evaluation.',
      'Deploy streaming inference endpoints with prompt/model routing and guardrails.',
    ],
    technologies: [
      { name: 'Python & FastAPI', role: 'Async ingestion workers and token-streaming inference APIs' },
      { name: 'pgvector & ChromaDB', role: 'Dense vector indexing and metadata-filtered retrieval' },
      { name: 'PyTorch & HuggingFace', role: 'Embeddings, cross-encoder rerankers, and PEFT basics' },
      { name: 'vLLM & Ollama', role: 'High-throughput and local LLM serving' },
      { name: 'Ragas / Eval Harnesses', role: 'Automated retrieval and faithfulness benchmarking' },
      { name: 'Docker', role: 'Reproducible containerized service deployment' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Data Ingestion, Chunking & Embeddings',
        topics: [
          'Document parsing, semantic chunking, and metadata schemas',
          'Embedding model selection and pgvector/ChromaDB indexing',
          'First reviewed PR on venture ingestion pipeline',
        ],
        deliverable: 'Reproducible document ingestion and vector indexing pipeline.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Hybrid Retrieval, Reranking & Citations',
        topics: [
          'Combining BM25 lexical search with dense vector search (RRF)',
          'Cross-encoder reranking and context window budgeting',
          'Grounded citation formatting and hallucination checks',
        ],
        deliverable: 'Hybrid retriever endpoint with verifiable source citations.',
      },
      {
        period: 'Weeks 5–6',
        title: 'RAG Evaluation, Routing & Fine-Tuning Limits',
        topics: [
          'Building golden evaluation datasets and measuring recall/faithfulness',
          'Prompt/model routing and semantic caching',
          'When to use RAG vs QLoRA fine-tuning (prerequisites and trade-offs)',
        ],
        deliverable: 'Evaluation report comparing baseline vs hybrid+reranked RAG.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Inference Serving & Capstone Defense',
        topics: [
          'Streaming SSE/WebSocket responses and latency profiling',
          'Security guardrails and Turnitin originality audit',
          'Final PR merge and 3-document credential issuance',
        ],
        deliverable: 'Evaluated knowledge assistant capstone and verified credential packet.',
      },
    ],
    capstone: {
      title: 'Evaluated Enterprise Knowledge Assistant',
      description:
        'Build an end-to-end knowledge assistant with document ingestion, hybrid retrieval, reranking, grounded citations, and a quantitative evaluation report for Alkame or Aivara.',
      status: 'active',
      ventureName: 'Alkame & Aivara',
      repositoryUrl: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
      acceptanceCriteria: [
        'Hybrid retrieval outperforms dense-only baseline on test query set.',
        'Every generated answer includes traceable source citations.',
        'Streaming API handles concurrent requests without blocking.',
      ],
    },
    evaluation: [
      'Retrieval Quality: Documented evaluation metrics before and after reranking.',
      'Code & API Design: Clean async FastAPI routes and typed schemas.',
      'Security & Privacy: Input sanitization and zero leaked credentials.',
      'Documentation: Clear architecture notes and reproducible setup.',
    ],
    faqs: [
      {
        question: 'Do I need an expensive local GPU?',
        answer:
          'No. Retrieval, evaluation, and quantized local inference labs run on standard developer machines or provided cloud notebooks.',
      },
      {
        question: 'How is this different from AI Agent Development?',
        answer:
          'Generative AI Systems focuses deeply on RAG, embeddings, reranking, evaluation, and LLM serving; AI Agent Development focuses on multi-step tool-using state machines and delegation.',
      },
    ],
    relatedSlugs: ['ai-agent-development', 'machine-learning', 'full-stack-development'],
    regionalOpportunities: [
      {
        title: 'GenAI & RAG Systems Intern',
        roleDescription: 'Build hybrid retrieval pipelines and citation-backed LLM APIs.',
        cityTag: 'Bengaluru',
        location: 'Bengaluru · Hybrid / Remote',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/generative-ai',
        tags: ['RAG', 'pgvector', 'FastAPI', 'vLLM'],
      },
      {
        title: 'Document Intelligence NLP Intern',
        roleDescription: 'Extract structured records from PDFs using LLM pipelines and validation.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/rag-pipeline-engineering-intern-remote-1',
        tags: ['Python', 'Embeddings', 'Docker'],
      },
    ],
  },
  {
    id: 'machine-learning',
    slug: 'machine-learning',
    canonicalPath: '/learners/courses/machine-learning',
    name: 'Machine Learning & Fine-Tuning',
    shortName: 'ML & MLOps',
    badge: 'Deep Tech',
    category: 'AI & Data',
    featured: true,
    displayOrder: 3,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Train, evaluate, deploy, and monitor a reproducible machine-learning or fine-tuned model with tracked experiments.',
    shortDescription:
      'Data validation, feature engineering, baseline modeling, experiment tracking, containerized serving, and drift monitoring.',
    fullDescription:
      'This track separates classical ML, parameter-efficient fine-tuning, and MLOps clearly. Fellows learn how to validate datasets, establish strong baselines, track experiments reproducibly, package models in Docker, and monitor inference drift.',
    whoShouldApply: [
      'Developers and data practitioners who want to move models from notebooks into reproducible production services.',
      'Graduates who want hands-on MLOps, evaluation, and fine-tuning discipline.',
    ],
    prerequisites: [
      'Python programming comfort and basic familiarity with NumPy/Pandas.',
      'Foundational understanding of statistics or linear algebra.',
    ],
    outcomes: [
      'Build reproducible data validation and feature engineering pipelines.',
      'Compare classical ML baselines against fine-tuned models using proper validation splits.',
      'Track experiments, parameters, and model artifacts with a model registry.',
      'Serve models in Docker containers with basic drift and latency monitoring.',
    ],
    technologies: [
      { name: 'Python & scikit-learn', role: 'Tabular baselines, pipelines, and cross-validation' },
      { name: 'PyTorch & HuggingFace', role: 'Model training and parameter-efficient fine-tuning (LoRA)' },
      { name: 'MLflow', role: 'Experiment tracking, metrics logging, and model registry' },
      { name: 'Pandas & Great Expectations', role: 'Data cleaning and schema/distribution validation' },
      { name: 'FastAPI & Docker', role: 'Reproducible containerized model inference serving' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Data Validation & Strong Baselines',
        topics: [
          'Train/val/test leakage prevention and data quality checks',
          'Feature engineering pipelines with scikit-learn',
          'Establishing interpretable baseline metrics',
        ],
        deliverable: 'Validated dataset pipeline and documented baseline benchmark.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Experiment Tracking & Model Training',
        topics: [
          'Logging runs, hyperparameters, and artifacts in MLflow',
          'Classical ML vs neural/LoRA fine-tuning trade-offs',
          'Error analysis and calibration',
        ],
        deliverable: 'Tracked experiment suite with registered candidate model.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Containerized Serving & Inference APIs',
        topics: [
          'Packaging model weights and preprocessing into Docker',
          'FastAPI prediction endpoints with input validation',
          'Batch vs real-time inference patterns',
        ],
        deliverable: 'Containerized inference service with automated smoke tests.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Monitoring, Drift & Capstone Audit',
        topics: [
          'Tracking prediction distributions and data drift',
          'Retraining triggers and rollback procedures',
          'Final code review and credential packet release',
        ],
        deliverable: 'Reproducible deployed model with monitoring and evaluation report.',
      },
    ],
    capstone: {
      title: 'Reproducible Predictive Model & Inference Service',
      description:
        'Train, track, containerize, and deploy a predictive model (such as financial signal classification or churn/demand forecasting) with documented evaluation and drift checks.',
      status: 'active',
      ventureName: 'Alkame',
      repositoryUrl: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
      acceptanceCriteria: [
        'Zero data leakage between training and evaluation splits.',
        'All experiments reproducible from pinned configs and tracked in MLflow.',
        'Inference container builds cleanly and passes API contract tests.',
      ],
    },
    evaluation: [
      'Experimental Rigor: Leakage-free splits and honest baseline comparisons.',
      'Reproducibility: Pinned dependencies, seed control, and clean Dockerfiles.',
      'Code Quality: Modular pipeline code outside monolithic notebooks.',
      'Documentation: Model card, limitations, and evaluation summary.',
    ],
    faqs: [
      {
        question: 'Does this cover both classical ML and LLM fine-tuning?',
        answer:
          'Yes, and we explicitly distinguish when classical tabular ML (scikit-learn/gradient boosting) outperforms deep learning or LoRA fine-tuning.',
      },
    ],
    relatedSlugs: ['generative-ai', 'data-analytics', 'ai-agent-development'],
    regionalOpportunities: [
      {
        title: 'Machine Learning & MLOps Intern',
        roleDescription: 'Build reproducible training pipelines and containerized inference APIs.',
        cityTag: 'Bengaluru',
        location: 'Bengaluru · Hybrid / Remote',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/machine-learning',
        tags: ['PyTorch', 'MLflow', 'Docker', 'FastAPI'],
      },
    ],
  },
  {
    id: 'full-stack-development',
    slug: 'full-stack-development',
    canonicalPath: '/learners/courses/full-stack-development',
    name: 'Full Stack Web Development',
    shortName: 'Full Stack Web',
    badge: 'Most Popular',
    category: 'Software & Cloud',
    featured: true,
    displayOrder: 4,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Build, test, and deploy a complete web application with React/Next.js, TypeScript, PostgreSQL, authentication, and operational basics.',
    shortDescription:
      'Next.js App Router, TypeScript component architecture, PostgreSQL migrations, role-based auth, testing, and deployment.',
    fullDescription:
      'Full Stack Web Development trains fellows on real production web codebases. You will work across TypeScript, React/Next.js, REST/server-action APIs, PostgreSQL schemas, authentication, and automated testing under senior PR review.',
    whoShouldApply: [
      'Students and junior developers who know basic HTML/CSS/JS and want real full-stack production experience.',
      'Frontend or backend learners who want to own features end-to-end from DB migration to UI.',
    ],
    prerequisites: [
      'Working knowledge of JavaScript/TypeScript fundamentals and basic React.',
      'Familiarity with Git and relational database concepts.',
    ],
    outcomes: [
      'Architect type-safe React and Next.js App Router pages and reusable components.',
      'Design normalized PostgreSQL schemas, migrations, and authenticated API endpoints.',
      'Implement role-based access control, validation, and error boundaries.',
      'Write integration tests and ship production-ready pull requests.',
    ],
    technologies: [
      { name: 'Next.js & React 19', role: 'App Router, Server Components, and responsive UI' },
      { name: 'TypeScript', role: 'End-to-end type safety across UI and APIs' },
      { name: 'PostgreSQL & Prisma', role: 'Relational data modeling, indexing, and migrations' },
      { name: 'Node.js / REST APIs', role: 'Server-side validation, auth, and webhook handling' },
      { name: 'Docker & GitHub Actions', role: 'CI checks, build verification, and deployment' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'TypeScript, Next.js Architecture & DB Setup',
        topics: [
          'Next.js App Router server vs client component boundaries',
          'PostgreSQL schema design and migrations',
          'First reviewed PR on venture web repository',
        ],
        deliverable: 'Type-safe feature route backed by a migrated PostgreSQL table.',
      },
      {
        period: 'Weeks 3–4',
        title: 'APIs, Authentication & Role-Based Access',
        topics: [
          'Input validation, idempotent API handlers, and error states',
          'Session/JWT authentication and role-based permissions',
          'Responsive form UX and accessibility',
        ],
        deliverable: 'Authenticated CRUD workflow with server-side validation.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Testing, Caching & Observability',
        topics: [
          'Unit and API integration testing',
          'Performance profiling, Core Web Vitals, and query optimization',
          'Structured logging and error handling',
        ],
        deliverable: 'Tested feature module with documented API contracts.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Production Hardening & Credential Release',
        topics: [
          'Security review (XSS, CSRF, auth checks, secret hygiene)',
          'Deployment verification and technical documentation',
          'Final PR audit and 3-document credential issuance',
        ],
        deliverable: 'Deployed SaaS workflow capstone and verified credential packet.',
      },
    ],
    capstone: {
      title: 'Role-Based SaaS Workflow & Portal Module',
      description:
        'Ship a complete full-stack workflow (authentication, role-based dashboard, validated APIs, and PostgreSQL persistence) for the DBERT Portal or an incubated venture app.',
      status: 'active',
      ventureName: 'DBERT Internship Portal',
      repositoryUrl: 'https://github.com/DBERT-INDIA/Internshipportal',
      acceptanceCriteria: [
        'Zero TypeScript or ESLint errors in production build.',
        'All API routes validate inputs and enforce authorization.',
        'Responsive across mobile (375px) and desktop (1440px).',
      ],
    },
    evaluation: [
      'Code Quality: Clean TypeScript, modular components, and zero lint errors.',
      'Security & Data Integrity: Parameterized queries, auth checks, no leaked secrets.',
      'UX & Accessibility: Keyboard navigation, clear error states, responsive layout.',
      'Documentation: Clear PR description and schema/API notes.',
    ],
    faqs: [
      {
        question: 'Do I need to know Next.js before joining?',
        answer:
          'Basic React and JavaScript/TypeScript knowledge is expected. You will learn Next.js App Router patterns during Weeks 1–2.',
      },
    ],
    relatedSlugs: ['python-automation', 'devops-cloud', 'ui-ux-design'],
    regionalOpportunities: [
      {
        title: 'Full Stack Next.js & Postgres Intern',
        roleDescription: 'Build authenticated web dashboards, APIs, and database migrations.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/full-stack-development',
        tags: ['Next.js', 'TypeScript', 'PostgreSQL'],
      },
    ],
  },
  {
    id: 'python-automation',
    slug: 'python-automation',
    canonicalPath: '/learners/courses/python-automation',
    name: 'Python Automation',
    shortName: 'Python Automation',
    badge: 'High Demand',
    category: 'Software & Cloud',
    featured: true,
    displayOrder: 5,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Engineer resilient Python automation pipelines, headless browser workflows, and distributed background task queues.',
    shortDescription:
      'Playwright headless automation, structured data extraction, Celery/Redis task queues, and idempotent database syncing.',
    fullDescription:
      'Python Automation focuses on reliable operational engineering: writing maintainable async Python workers, Playwright browser test/automation suites, rate-limited API/web sync pipelines, and deduplicated database ingestion.',
    whoShouldApply: [
      'Python developers interested in backend automation, QA engineering, and data pipeline orchestration.',
      'Builders who want to automate complex multi-step workflows reliably.',
    ],
    prerequisites: [
      'Core Python syntax fluency (lists, dicts, functions, file I/O, basic OOP).',
      'Basic familiarity with command line and Git.',
    ],
    outcomes: [
      'Build resilient Playwright browser automation and end-to-end test harnesses.',
      'Design idempotent background workers with Celery, Redis, and retry backoffs.',
      'Parse, validate, and sync structured data into SQLite/PostgreSQL.',
      'Package and monitor scheduled automation daemons safely.',
    ],
    technologies: [
      { name: 'Python 3.12 (Asyncio)', role: 'Concurrent I/O workers and resilient retry logic' },
      { name: 'Playwright', role: 'Headless browser automation and E2E verification' },
      { name: 'Celery & Redis', role: 'Distributed background task queues and scheduling' },
      { name: 'PostgreSQL / SQLite', role: 'Idempotent state tracking and deduplication' },
      { name: 'Docker', role: 'Isolated worker execution environments' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Async Python & Structured Extraction',
        topics: [
          'Asyncio coroutines, httpx clients, and exponential backoff',
          'Schema validation with Pydantic and structured logging',
          'First reviewed PR on automation repository',
        ],
        deliverable: 'Resilient async API/data ingestion script with retry handling.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Headless Browser Workflows with Playwright',
        topics: [
          'Reliable locators, network interception, and session state',
          'Automated E2E UI regression suites',
          'Handling timeouts, artifacts, and failure screenshots',
        ],
        deliverable: 'Automated Playwright test and workflow suite.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Task Queues, Deduplication & Scheduling',
        topics: [
          'Celery task queues backed by Redis',
          'Idempotent database writes and circuit breakers',
          'Rate limiting and ethical automation practices',
        ],
        deliverable: 'Deduplicated background worker queue with health checks.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Hardening, Testing & Credential Release',
        topics: [
          'Containerizing workers with Docker',
          'Runbooks, alerting, and Turnitin originality audit',
          'Final PR review and credential packet issuance',
        ],
        deliverable: 'Production automation daemon capstone and verified credential.',
      },
    ],
    capstone: {
      title: 'Distributed Automation & E2E Verification Suite',
      description:
        'Deliver a fault-tolerant Python worker and Playwright verification pipeline with idempotent PostgreSQL/SQLite state tracking for DBERT Portal operations.',
      status: 'active',
      ventureName: 'DBERT Internship Portal',
      repositoryUrl: 'https://github.com/DBERT-INDIA/Internshipportal',
      acceptanceCriteria: [
        'Zero duplicate records on repeated worker runs (idempotency verified).',
        'Graceful failure handling with structured logs.',
        'All automated Playwright checks pass deterministically.',
      ],
    },
    evaluation: [
      'Reliability: Proper timeouts, retries, and idempotency guards.',
      'Code Quality: Clean Python typing, PEP8 linting, modular helpers.',
      'Testing: Automated unit and E2E test coverage.',
      'Documentation: Clear runbooks and environment variable specs.',
    ],
    faqs: [
      {
        question: 'Is this track suitable for QA automation engineers?',
        answer:
          'Yes. Playwright E2E testing, CI integration, and backend worker verification are core parts of this track.',
      },
    ],
    relatedSlugs: ['full-stack-development', 'devops-cloud', 'ai-agent-development'],
    regionalOpportunities: [
      {
        title: 'Python Automation & QA Systems Intern',
        roleDescription: 'Build Playwright E2E suites and async backend data sync workers.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/python-automation',
        tags: ['Python', 'Playwright', 'Celery', 'Redis'],
      },
    ],
  },
  {
    id: 'data-analytics',
    slug: 'data-analytics',
    canonicalPath: '/learners/courses/data-analytics',
    name: 'Data Analytics & BI',
    shortName: 'Data Analytics & BI',
    badge: 'Evergreen',
    category: 'AI & Data',
    featured: true,
    displayOrder: 6,
    status: 'published',
    duration: '2 Months (8 Weeks)',
    weeklyCommitment: '12–15 hours / week (remote, milestone-driven)',
    heroOutcome:
      'Turn raw operational data into defensible SQL analyses, predictive metrics, and decision-ready BI dashboards.',
    shortDescription:
      'Advanced SQL window functions, Python Pandas cleaning, exploratory statistics, and automated Power BI / Metabase dashboards.',
    fullDescription:
      'Data Analytics & BI bridges raw SQL/Python data engineering and executive decision-making. Fellows clean real datasets, write optimized analytical SQL queries, perform variance and cohort analysis, and publish clear, honest dashboards.',
    whoShouldApply: [
      'Graduates and analysts who want hands-on SQL, Python Pandas, and BI dashboarding on real business datasets.',
      'Candidates who want to move beyond spreadsheet-only reporting into reproducible analytics.',
    ],
    prerequisites: [
      'Comfort with basic spreadsheets, college-level math, and logical reasoning.',
      'Basic familiarity with SQL or Python is helpful; foundational refreshers are included in Week 1.',
    ],
    outcomes: [
      'Write complex analytical SQL using CTEs, window functions, and query optimization.',
      'Clean, validate, and transform messy datasets using Python Pandas.',
      'Perform exploratory data analysis, cohort retention, and basic forecasting.',
      'Build executive dashboards in Power BI or Metabase while communicating uncertainty clearly.',
    ],
    technologies: [
      { name: 'PostgreSQL / SQL', role: 'CTEs, window functions, and analytical data modeling' },
      { name: 'Python & Pandas', role: 'Data cleaning, variance decomposition, and EDA' },
      { name: 'Power BI & Metabase', role: 'Interactive executive dashboards and KPI tracking' },
      { name: 'DuckDB', role: 'Fast local analytical queries over CSV/Parquet files' },
      { name: 'Git', role: 'Version-controlled SQL scripts and reproducible notebooks' },
    ],
    curriculum: [
      {
        period: 'Weeks 1–2',
        title: 'Analytical SQL & Data Extraction',
        topics: [
          'Joins, CTEs, window functions, and cohort queries',
          'Schema normalization for analytics vs OLTP',
          'First reviewed SQL/data PR',
        ],
        deliverable: 'Versioned SQL analytical query pack with documented KPI definitions.',
      },
      {
        period: 'Weeks 3–4',
        title: 'Data Cleaning, Validation & EDA in Python',
        topics: [
          'Handling missing values, outliers, and schema drift with Pandas',
          'Descriptive statistics and hypothesis testing basics',
          'Automated data quality assertions',
        ],
        deliverable: 'Reproducible Python cleaning and EDA pipeline.',
      },
      {
        period: 'Weeks 5–6',
        title: 'Forecasting & Executive BI Dashboards',
        topics: [
          'Time-series trend decomposition and baseline forecasting',
          'Designing clear Metabase / Power BI dashboards',
          'Communicating uncertainty and metric caveats',
        ],
        deliverable: 'Interactive BI dashboard with drill-down filters.',
      },
      {
        period: 'Weeks 7–8',
        title: 'Business Interpretation & Capstone Audit',
        topics: [
          'Writing executive decision memos backed by reproducible queries',
          'Turnitin originality check and peer/senior review',
          'Final credential packet issuance',
        ],
        deliverable: 'Business dataset analysis, dashboard, and verified credential packet.',
      },
    ],
    capstone: {
      title: 'Corporate Financial & Cohort Analytics Suite',
      description:
        'Analyze an approved Alkame or operational dataset to produce an automated SQL/Pandas cleaning pipeline, a predictive trend component, and an interactive BI dashboard.',
      status: 'active',
      ventureName: 'Alkame',
      repositoryUrl: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
      acceptanceCriteria: [
        'All KPI calculations reproducible directly from documented SQL/Python scripts.',
        'Dashboard visualizations avoid misleading scales and state data limitations.',
        'Clean Git commit history and Turnitin < 5% on analytical report.',
      ],
    },
    evaluation: [
      'Analytical Accuracy: Reproducible numbers with zero silent data drops.',
      'SQL & Python Quality: Readable, indexed queries and clean Pandas transforms.',
      'Communication: Clear executive summary explaining what the data does and does not prove.',
      'Documentation: Data dictionary and reproducible run instructions.',
    ],
    faqs: [
      {
        question: 'Do I need to be a software engineer before joining Data Analytics?',
        answer:
          'No. Logical reasoning and comfort with basic math/spreadsheets are enough to start; we guide you through analytical SQL and Pandas.',
      },
    ],
    relatedSlugs: ['machine-learning', 'python-automation', 'digital-marketing'],
    regionalOpportunities: [
      {
        title: 'Data Analyst & BI Engineering Intern',
        roleDescription: 'Build SQL cohort queries, Pandas ETL scripts, and Metabase dashboards.',
        cityTag: 'Remote',
        location: 'Virtual · Anywhere India',
        placement: '100% Guaranteed Production Internship with Dedicated Placement Assistance',
        href: 'https://lms.dbert.in/internships/data-analytics',
        tags: ['SQL', 'Pandas', 'Power BI', 'Metabase'],
      },
    ],
  },
];
