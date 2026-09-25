/**
 * Per-route SEO metadata — the single source of truth for Phase 6.1–6.4.
 *
 * Rules enforced by scripts/check-seo.mjs (run via `npm run check:seo`):
 *  · title ≤ 52 chars — layout.tsx appends " | DBERT" (8), keeping it under 60
 *  · description 140–155 chars, contains the primary keyword, ends on an action
 *  · one primary keyword per route, never reused across routes
 *
 * Titles follow docs/seo-content-plan.md Part 2 where that document specifies
 * one. Descriptions are written here.
 *
 * Descriptions deliberately carry no statistics. Not because the figures are
 * unverified — they are founder-approved — but because meta descriptions are
 * the worst place to hardcode a number that changes: it is the copy least
 * likely to be revisited when the underlying figure moves.
 */

export type SeoEntry = {
  /** ≤52 chars. The "| DBERT" suffix is appended by the layout template. */
  title: string;
  /** 140–155 chars. */
  description: string;
  /** Primary keyword this route owns. Must be unique across the map. */
  keyword: string;
  /** Excluded from the sitemap and marked noindex. */
  noindex?: boolean;
};

export const seoConfig: Record<string, SeoEntry> = {
  // ── Core ────────────────────────────────────────────────────────────────
  '/pricing': {
    keyword: 'DBERT pricing',
    title: 'Pricing — Programs, Products & Incubation Terms',
    description:
      'Transparent DBERT pricing for learner programs, enterprise AI products and equity-based incubation. No hidden fees — see exactly what everything costs.',
  },
  '/verify': {
    keyword: 'verify DBERT certificate',
    title: 'Verify a DBERT Certificate',
    description:
      'Verify a DBERT certificate in seconds. Enter the certificate ID to confirm its issue date, programme and holder, and spot forged credentials instantly.',
  },
  '/privacy': {
    keyword: 'DBERT privacy policy',
    title: 'Privacy Policy',
    description:
      'How DBERT collects, stores and uses your personal data across our programmes, products and application forms — in plain language. Read the full policy.',
  },
  '/terms': {
    keyword: 'DBERT terms and conditions',
    title: 'Terms & Conditions',
    description:
      'The terms governing use of DBERT services, programmes and software products, including enrolment, payment and acceptable use. Read them before applying.',
  },
  '/refund': {
    keyword: 'DBERT refund policy',
    title: 'Refund Policy',
    description:
      'When DBERT course and programme fees can be refunded, how long refunds take, and exactly how to request one. Read the policy before you enrol.',
  },

  // ── Startups ────────────────────────────────────────────────────────────
  '/startups': {
    keyword: 'AI startup incubator India',
    title: 'AI Startup Incubator in India — Equity-Based',
    description:
      'An AI startup incubator in India that builds for equity: architecture, MVP development and hiring from one engineering team. See the model and apply.',
  },
  '/startups/register': {
    keyword: 'apply startup incubator India',
    title: 'Apply for Incubation — Startup Application',
    description:
      'Apply to the DBERT startup incubator. See what we evaluate, how long a decision takes, and what happens next — then submit your venture for review.',
  },
  '/startups/portfolio': {
    keyword: 'DBERT portfolio startups',
    title: 'Portfolio — Startups We Built and Backed',
    description:
      'The startups DBERT has incubated, with the problem each one solves and the systems we built for them. Browse the portfolio and read the case studies.',
  },
  '/startups/portfolio/alkame': {
    keyword: 'AI stock prediction startup India',
    title: 'Alkame — Conformal Prediction for Markets',
    description:
      'How DBERT built Alkame, an AI stock prediction engine using conformal prediction, against a moving Indian regulatory target. Read the case study.',
  },
  '/startups/portfolio/cognitive-solutions': {
    keyword: 'Cognitive Solutions DBERT case study',
    title: 'Cognitive Solutions — Incubation Case Study',
    description:
      'How DBERT took Cognitive Solutions from concept to a shipped product: the architecture chosen, the squad that built it, and what launched. Read the study.',
  },
  '/startups/portfolio/digital-blaize': {
    keyword: 'Digital Blaize DBERT case study',
    title: 'Digital Blaize — Incubation Case Study',
    description:
      'How DBERT built Digital Blaize as its technical co-founder: the stack, the sprint plan and the product that reached users. Read the full engineering story.',
  },
  '/startups/portfolio/gayatri-ai': {
    keyword: 'Gayatri AI DBERT case study',
    title: 'Gayatri AI — Incubation Case Study',
    description:
      'How DBERT designed and shipped Gayatri AI, from data strategy through deployment, in exchange for equity rather than fees. Read the engineering case study.',
  },
  '/startups/services': {
    keyword: 'startup incubation services India',
    title: 'Startup Incubation Services — What You Get',
    description:
      'The startup incubation services DBERT delivers in India: architecture, MVP build, hiring, infrastructure, legal and funding prep. See the full scope.',
  },
  '/startups/services/technical': {
    keyword: 'technical co-founder as a service',
    title: 'Technical Co-Founder as a Service',
    description:
      'Get a technical co-founder as a service: system architecture, MVP build and senior engineering review, paid in equity rather than cash. See how it works.',
  },
  '/startups/services/equity': {
    keyword: 'equity-based startup services',
    title: 'Equity-Based Startup Services — How It Works',
    description:
      'How equity-based startup services work at DBERT: what we deliver, what we take, and what you keep. Understand the model before you apply for incubation.',
  },
  '/startups/services/equity/term-sheets': {
    keyword: 'startup term sheet template India',
    title: 'Startup Term Sheet Templates (India) — Free',
    description:
      'Free annotated startup term sheet templates for Indian founders, with every clause explained in plain language. Download them and read before you sign.',
  },
  '/startups/services/funding': {
    keyword: 'startup funding support India',
    title: 'Funding Readiness & Investor Prep',
    description:
      'Startup funding support in India: get your metrics, data room and pitch investor-ready with engineers who have built the product. Start preparing today.',
  },
  '/startups/services/hiring': {
    keyword: 'startup hiring India engineers',
    title: 'Hire Vetted AI Engineers for Your Startup',
    description:
      'Hire vetted AI engineers for your startup in India, screened on production work rather than interviews alone. See how DBERT hiring support works.',
  },
  '/startups/services/infrastructure': {
    keyword: 'startup cloud infrastructure setup',
    title: 'Cloud & AI Infrastructure for Startups',
    description:
      'Cloud and AI infrastructure setup for startups: VPC design, GPU capacity, vector stores and CI, built to scale without rewrites. See what we set up.',
  },
  '/startups/services/legal': {
    keyword: 'startup legal compliance India',
    title: 'Startup Legal & IP Compliance Support',
    description:
      'Startup legal and compliance support in India: entity setup, IP assignment, contracts and data obligations, handled alongside the build. See what we cover.',
  },
  '/startups/investor-network': {
    keyword: 'angel investor network India AI',
    title: 'AI Investor Network — Connect With Backers',
    description:
      'An AI investor network for Indian founders: warm introductions to angels and funds who already understand technical products. See how introductions work.',
  },

  // ── AI solutions ────────────────────────────────────────────────────────
  '/ai-solutions': {
    keyword: 'enterprise AI solutions India',
    title: 'Enterprise AI Solutions & Products — India',
    description:
      'Production-ready enterprise AI from an Indian venture studio: self-hosted LLM chat, document AI, hiring automation and custom model training. Explore them.',
  },
  '/ai-solutions/products': {
    keyword: 'AI software products India',
    title: 'AI Software Products Built in Production',
    description:
      'Every DBERT product solved a problem inside our own studio before it was sold. Browse the AI software we run in production and deploy for enterprises.',
  },
  '/ai-solutions/products/dbert-chat': {
    keyword: 'self-hosted enterprise LLM chat',
    title: 'Self-Hosted Enterprise LLM Chat — Your VPC',
    description:
      'Self-hosted enterprise LLM chat over your internal knowledge base, running inside your own VPC so no data leaves your network. See the architecture.',
  },
  '/ai-solutions/products/document-ai': {
    keyword: 'document AI OCR India',
    title: 'Document AI — OCR & Contract Parsing',
    description:
      'Document AI for Indian enterprises: OCR and structured parsing for contracts, invoices and unstructured PDFs at pipeline scale. See how it handles yours.',
  },
  '/ai-solutions/products/certificate-verification-api': {
    keyword: 'certificate verification API',
    title: 'Certificate Verification API — Issue & Verify',
    description:
      'A certificate verification API for issuing, revoking and validating tamper-evident credentials from one endpoint. Read the docs and start integrating.',
  },
  '/ai-solutions/products/hiring-automation-suite': {
    keyword: 'AI hiring automation software India',
    title: 'AI Hiring Automation — Parsing & Scoring',
    description:
      'AI hiring automation software for Indian teams: resume parsing, structured scoring and interview scheduling tuned for engineering roles. Book a demo.',
  },
  '/ai-solutions/products/intern-management-system': {
    keyword: 'intern management system software',
    title: 'Intern Management System — Squads to Certs',
    description:
      'The intern management system DBERT runs its own fellowship on: squads, sprints, reviews and verifiable certificates end to end. See it in action.',
  },
  '/ai-solutions/llm-training': {
    keyword: 'custom LLM training services India',
    title: 'Custom LLM Training Services — India',
    description:
      'Custom LLM training services in India: fine-tune open models on your own data and deploy them on infrastructure you control. Discuss your use case.',
  },
  '/ai-solutions/llm-training/pipeline': {
    keyword: 'fine-tune LLM on company data',
    title: 'Fine-Tune an LLM on Your Company Data',
    description:
      'How to fine-tune an LLM on company data: dataset preparation, training runs, evaluation and rollout, handled end to end by DBERT. See the pipeline.',
  },
  '/ai-solutions/llm-training/private-hosting': {
    keyword: 'private LLM hosting India',
    title: 'Private LLM Hosting in India — Costs & Specs',
    description:
      'Private LLM hosting in India: the hardware, the rupee costs and the compliance questions nobody publishes, set out plainly. Plan your deployment.',
  },
  '/ai-solutions/llm-training/dbert-ai': {
    keyword: 'DBERT AI model',
    title: 'DBERT AI — Our In-House Language Model',
    description:
      'DBERT AI is the in-house language model we train and run for studio and client workloads. See what it is built on and where it is deployed today.',
  },
  '/ai-solutions/consultation': {
    keyword: 'AI consultation services India',
    title: 'AI Consultation for Enterprises — Book a Session',
    description:
      'AI consultation services in India, run by the engineers who ship the systems. See what a session covers and what you walk away with, then book one.',
  },

  // ── Learners ────────────────────────────────────────────────────────────
  '/learners': {
    keyword: 'AI career programs India',
    title: 'AI Career Programs — Zero to Hired',
    description:
      'AI career programs in India built as a ladder, not a catalogue: from your first Python script to a paid fellowship on real client systems. Find your rung.',
  },
  '/learners/launchpad': {
    keyword: 'AI course for beginners India 2 months',
    title: '2-Month AI & Engineering Launchpad Across 6 Domains',
    description:
      'A 2-month AI and engineering launchpad in India across 6 domains with live GitHub repos: AI Agents, GenAI, Machine Learning, Automation & Analytics.',
  },
  '/learners/accelerate': {
    keyword: 'AI engineering bootcamp India',
    title: 'AI Engineering Program — RAG, Agents, Deploy',
    description:
      'An AI engineering program in India where you ship RAG pipelines, agents and deployments under senior review. See the projects you will build and apply.',
  },
  '/learners/fellowship': {
    keyword: 'paid AI internship India',
    title: 'Paid AI Fellowship — Real Client Systems',
    description:
      'A paid AI internship in India where you write production code for real incubated startups, not practice projects. See selection criteria and how to apply.',
  },
  '/learners/interview-prep': {
    keyword: 'AI engineer interview preparation',
    title: 'AI Engineer Interview Prep — Mock Interviews',
    description:
      'AI engineer interview preparation with mock technical interviews, a question bank and feedback from working engineers. Start practising for your round.',
  },
  '/learners/jobs': {
    keyword: 'AI jobs India freshers',
    title: 'AI Jobs & Placement for Verified Builders',
    description:
      'AI jobs in India for freshers who can prove what they built. Direct referrals and portfolio reviews for verified DBERT builders. Browse open roles today.',
  },
  '/learners/courses': {
    keyword: 'AI courses with certificate India',
    title: 'AI & Engineering Courses with Certificates',
    description:
      'AI and engineering courses in India with verifiable certificates across 6 domains: AI Agents, Generative AI, Machine Learning, Automation, and Analytics.',
  },
  '/learners/courses/ai-agent-development': {
    keyword: 'AI agent development course',
    title: 'AI Agent Development Course — Build & Deploy',
    description:
      'An AI agent development course covering orchestration frameworks, tool use and deployment, ending in an agent you can show. See the full syllabus.',
  },
  '/learners/courses/generative-ai': {
    keyword: 'Generative AI course India',
    title: 'Generative AI Systems Course — Multi-LLMs',
    description:
      'A Generative AI systems course covering multi-provider LLMs, intelligent context compression, deep web research tools, and streaming UI development.',
  },
  '/learners/courses/machine-learning': {
    keyword: 'Machine learning course fine-tuning India',
    title: 'Machine Learning & LLM Fine-Tuning Course — India',
    description:
      'Applied machine learning course covering feature engineering, classical ML models, synthetic datasets, and parameter-efficient fine-tuning on Llama-3.',
  },
  '/learners/courses/python-automation': {
    keyword: 'Python automation course India',
    title: 'Python Automation Course — Scripts to Pipelines',
    description:
      'A Python automation course in India: scraping, scheduling, APIs and data pipelines, taught through work you would actually be paid to do. See the syllabus.',
  },
  '/learners/courses/full-stack-development': {
    keyword: 'full stack AI development course India',
    title: 'Full Stack AI Development Course — India',
    description:
      'A full stack AI development course India covering React, Next.js, APIs and databases through projects you deploy to production. See the syllabus now.',
  },
  '/learners/courses/data-analytics': {
    keyword: 'data analytics course India certificate',
    title: 'Data Analytics Course with Certificate — India',
    description:
      'A data analytics course in India with a verifiable certificate, covering SQL, Python, Pandas and dashboards through real datasets. See the full plan.',
  },

  // ── Labs ────────────────────────────────────────────────────────────────
  '/labs': {
    keyword: 'DBERT Labs AI research',
    title: 'DBERT Labs — Applied AI Research',
    description:
      'DBERT Labs is where our applied AI research happens, from conformal prediction to document understanding. See current research areas and publications.',
  },
  '/labs/research': {
    keyword: 'AI research India applied',
    title: 'Applied AI Research Projects — India',
    description:
      'Applied AI research projects running at DBERT Labs in India, each with its current status and the problem it addresses. Browse the research index.',
  },
  '/labs/publications': {
    keyword: 'DBERT publications',
    title: 'Publications & Papers — DBERT Labs',
    description:
      'Papers published by DBERT Labs, with full citations, abstracts and PDFs where available. Read the research behind the systems we build and ship.',
  },
  '/labs/opensource': {
    keyword: 'DBERT open source',
    title: 'Open Source Projects — DBERT Labs',
    description:
      'Open source projects released by DBERT Labs, with repositories, licences and contribution guides. Browse the code and open your first pull request.',
  },
  '/labs/collaborate': {
    keyword: 'AI research collaboration India',
    title: 'AI Research Collaboration — Work With Labs',
    description:
      'Partner with DBERT Labs on applied AI research in India, whether you are a university group, a lab or an industry team. Tell us what you want to build.',
  },

  // ── About ───────────────────────────────────────────────────────────────
  '/about': {
    keyword: 'about DBERT',
    title: 'About DBERT — India’s AI Venture Studio',
    description:
      'About DBERT: how Digital Blinc Education Research and Technology grew into an AI venture studio wiring incubation, products and training together in Delhi.',
  },
  '/about/team': {
    keyword: 'DBERT team',
    title: 'Team — The Engineers Behind DBERT',
    description:
      'Meet the DBERT team: the engineers, mentors and partners who architect the products, run the squads and review every line of fellowship code we ship.',
  },
  '/about/credentials': {
    keyword: 'DBERT credentials verified',
    title: 'Credentials, Registrations & Verification',
    description:
      'DBERT credentials and registrations, with documentation you can check yourself, plus how to verify any certificate we issue. Review the proofs here.',
  },
  '/about/careers': {
    keyword: 'careers at DBERT',
    title: 'Careers at DBERT — Build With Us',
    description:
      'Careers at DBERT for engineers who would rather ship production systems than sit in planning meetings. See how we work and which roles are open now.',
  },
  '/about/contact': {
    keyword: 'contact DBERT',
    title: 'Contact DBERT — Delhi, India',
    description:
      'Contact DBERT in Delhi, India by email or phone, or send a message about incubation, products or programmes. Every enquiry gets a reply from a human.',
  },

  // ── Blog ────────────────────────────────────────────────────────────────
  '/blog': {
    keyword: 'AI engineering blog India',
    title: 'AI Engineering Blog — Notes From the Studio',
    description:
      'An AI engineering blog from an Indian venture studio: build logs, career guides and honest write-ups of what worked and what did not. Read the latest.',
  },

  // ── Admin (never indexed) ───────────────────────────────────────────────
  '/admin/login': {
    keyword: '',
    title: 'Admin Sign In',
    description: 'Internal DBERT administration sign-in.',
    noindex: true,
  },
  '/admin/leads': {
    keyword: '',
    title: 'Admin Dashboard',
    description: 'Internal DBERT lead tracking dashboard.',
    noindex: true,
  },
  '/admin/alkame-contributors': {
    keyword: '',
    title: 'Alkame Contributors',
    description: 'Internal moderation queue for Alkame contributor submissions.',
    noindex: true,
  },
  '/admin/cohort-applications': {
    keyword: '',
    title: 'Cohort Applications',
    description: 'Internal review portal for Aivara Technologies cohort submissions.',
    noindex: true,
  },

  // ── Cohorts ─────────────────────────────────────────────────────────────
  '/cohorts/aivara': {
    keyword: 'Aivara Technologies hiring cohort',
    title: 'Aivara Technologies Hiring Cohort 2026',
    description:
      'Join the Aivara Technologies hiring cohort with DBERT Labs. Choose from 5 engineering tracks, build production systems, and submit your application today.',
  },
};

export const seoRoutes = Object.keys(seoConfig);
