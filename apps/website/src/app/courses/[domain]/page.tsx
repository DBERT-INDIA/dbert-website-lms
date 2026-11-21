import React from 'react';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import CourseInteractiveShell, { type VerifiedAlum } from '@/components/courses/CourseInteractiveShell';
import directoryData from '@/data/directory_candidates.json';

interface PageProps {
  params: Promise<{ domain: string }>;
}

interface DomainCourseContent {
  slug: string;
  title: string;
  badge: string;
  headline: string;
  lede: string;
  salaryRange: string;
  stipend: string;
  skills: string[];
  tools: string[];
  partnerRepo: {
    name: string;
    repo: string;
    focus: string;
  };
  fellowshipWeeks: { period: string; title: string; tasks: string[] }[];
  courseWeeks: { period: string; title: string; topics: string[] }[];
  faqs: { question: string; answer: string }[];
}

const COURSES_DATA: Record<string, DomainCourseContent> = {
  'ai-agent-development': {
    slug: 'ai-agent-development',
    title: 'AI Agent & Multi-Agent Systems Engineering',
    badge: '🤖 Autonomous AI Systems',
    headline: 'Master Autonomous Multi-Agent State Machines & Local LLMs',
    lede: 'Engineer production-grade multi-agent architectures, deterministic tool-use pipelines, LangGraph state machines, and air-gapped local model serving via vLLM and Ollama.',
    salaryRange: '₹6,00,000 – ₹16,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['LangGraph', 'CrewAI', 'Ollama', 'vLLM', 'FastAPI', 'pgvector', 'Python Asyncio'],
    tools: ['Docker', 'Langfuse', 'Qdrant', 'Redis', 'GitHub Actions', 'GGUF'],
    partnerRepo: {
      name: 'Gayatri AI & DBERT Agent',
      repo: 'https://github.com/Gayatri-Education/Gayatri-AI',
      focus: 'Multi-agent supervisor routing networks, tool calling loops, and enterprise workflow execution.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'Architecture & Local Model Serving', tasks: ['Set up local Ollama & vLLM quantization', 'Build deterministic JSON function calling harness', 'First upstream PR review'] },
      { period: 'Weeks 3–6', title: 'Multi-Agent State Machine Sprints', tasks: ['Construct LangGraph cyclical state graphs', 'Implement CrewAI delegation loops with memory', 'Integrate vector RAG retrieval with hybrid reranking'] },
      { period: 'Weeks 7–8', title: 'System Hardening & Credential Release', tasks: ['End-to-end stress testing and token latency optimization', 'Submit audited capstone documentation (Turnitin < 5%)', 'Issue 3-document credential packet & ₹5,000 stipend release'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Foundational Systems & Async Python', topics: ['Python 3.12 async mechanics', 'FastAPI microservices', 'PostgreSQL pgvector schemas'] },
      { period: 'Weeks 5–8', title: 'Single & Multi-Agent Orchestration', topics: ['LangChain Expression Language (LCEL)', 'Hierarchical supervisor agents', 'Tool calling & error recovery'] },
      { period: 'Weeks 9–12', title: 'Enterprise Deployment & Production Capstone', topics: ['Air-gapped deployment with Docker', 'Streaming token WebSocket interfaces', 'Final defense & venture startup placement'] }
    ],
    faqs: [
      { question: 'What is the difference between the 2-Month Fellowship and 3-Month Course?', answer: 'The 2-Month Fellowship is an intensive sprint program for engineers with prior coding experience contributing directly to partner repositories (₹1,999 fee with ₹5,000 performance stipend). The 3-Month Course is a comprehensive end-to-end curriculum from foundational systems to enterprise production.' },
      { question: 'How is the credential verified by recruiters?', answer: 'Every graduate receives an official Certificate of Completion with a unique cryptographic UUID verifiable instantly at dbert.in/verify.' }
    ]
  },
  'generative-ai': {
    slug: 'generative-ai',
    title: 'Generative AI & LLM Systems Engineering',
    badge: '⚡ Foundation Models & RAG',
    headline: 'Fine-Tune Open-Weights LLMs & Architect Hybrid RAG Systems',
    lede: 'Learn parameter-efficient fine-tuning (LoRA/QLoRA), dense vector search, Reciprocal Rank Fusion, and production LLM orchestration on real venture codebases.',
    salaryRange: '₹6,50,000 – ₹18,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['PyTorch', 'Transformers', 'LoRA / QLoRA', 'LangChain', 'FastAPI', 'RAG'],
    tools: ['Hugging Face', 'ChromaDB', 'pgvector', 'vLLM', 'Docker', 'MLflow'],
    partnerRepo: {
      name: 'Alkame AI Market Intelligence',
      repo: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
      focus: 'Financial sentiment NLP with FinBERT, time-series embeddings, and streaming analysis.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'Tokenization & Vector Embedding Pipelines', tasks: ['Build dense vector search with cosine similarity', 'Implement hybrid BM25 + dense search', 'PR on Alkame data fetcher'] },
      { period: 'Weeks 3–6', title: 'Fine-Tuning & Evaluation Sprints', tasks: ['Fine-tune Mistral/Llama with QLoRA on domain datasets', 'Build RAG evaluation benchmark with Ragas', 'Deploy FastAPI streaming inference'] },
      { period: 'Weeks 7–8', title: 'Latency Benchmarking & Credential Release', tasks: ['Optimize KV-cache memory and GPU batching', 'Submit Turnitin-verified research dossier', 'Unlock ₹5,000 stipend release'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Transformers & Embedding Foundations', topics: ['Attention mechanisms', 'Sentence transformers', 'Vector database schemas'] },
      { period: 'Weeks 5–8', title: 'Advanced RAG & Prompt Chaining', topics: ['Reciprocal Rank Fusion', 'Context window pruning', 'Hallucination guardrails'] },
      { period: 'Weeks 9–12', title: 'PEFT Fine-Tuning & Enterprise Production', topics: ['LoRA/QLoRA pipelines', 'Model quantization (AWQ, GGUF)', 'Production deployment on AWS'] }
    ],
    faqs: [
      { question: 'Do I need access to an expensive GPU?', answer: 'No. DBERT provides cloud sandboxes and Google Colab Enterprise GPU runtimes for all fine-tuning and inference labs.' }
    ]
  },
  'full-stack-development': {
    slug: 'full-stack-development',
    title: 'Full Stack Web & AI Systems Engineering',
    badge: '💻 Production Web Architecture',
    headline: 'Build High-Scale Web Apps with Next.js 16, Node & Postgres',
    lede: 'Develop enterprise-grade full-stack architectures, implement pgvector similarity search, design responsive React 19 UIs, and deploy production microservices with active users.',
    salaryRange: '₹5,50,000 – ₹14,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['Next.js 16', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
    tools: ['Prisma', 'Docker', 'Redis', 'GitHub Actions', 'AWS EC2', 'Nginx'],
    partnerRepo: {
      name: 'DBERT Internship Portal & LMS',
      repo: 'https://github.com/DBERT-INDIA/Internshipportal',
      focus: 'Multi-tenant architecture, attendance heartbeats, verification APIs, and Next.js standalone SSR.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'App Router Architecture & DB Migrations', tasks: ['Set up Next.js 16 App Router standalone', 'Write Prisma / PostgreSQL migrations', 'First reviewed PR on portal repo'] },
      { period: 'Weeks 3–6', title: 'API Routes & Authentication Sprints', tasks: ['Build idempotent webhook processing', 'Implement streaming server actions', 'Deploy Redis cache-aside layer'] },
      { period: 'Weeks 7–8', title: 'Production Hardening & Verification', tasks: ['Audit Web Vitals (LCP < 1.2s)', 'Submit capstone code dossier', 'Receive verified credentials & ₹5,000 stipend'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Modern TypeScript & React 19 Core', topics: ['TypeScript strict mode', 'React Server Components', 'Component design systems'] },
      { period: 'Weeks 5–8', title: 'Next.js App Router & PostgreSQL Database', topics: ['Server actions', 'Relational database indexing', 'Authentication with JWT/NextAuth'] },
      { period: 'Weeks 9–12', title: 'Full Stack Microservices & Cloud Deployment', topics: ['Microservice communication', 'Docker containerization', 'Deploying to AWS EC2 with Nginx'] }
    ],
    faqs: [
      { question: 'What version of Next.js is taught?', answer: 'We teach the latest Next.js 16 App Router using React Server Components, standalone output mode, and Turbopack.' }
    ]
  },
  'data-analytics': {
    slug: 'data-analytics',
    title: 'Data Analytics & Automated Corporate BI',
    badge: '📊 Corporate Business Intelligence',
    headline: 'Transform Raw Data into Actionable Executive Intelligence',
    lede: 'Master SQL data modeling, Python Pandas variance decompositions, Power BI dashboards, and automated ETL pipelines worked through on real corporate financial datasets.',
    salaryRange: '₹5,00,000 – ₹13,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['SQL', 'Python Pandas', 'Power BI', 'Metabase', 'Data Modeling', 'ETL'],
    tools: ['PostgreSQL', 'DuckDB', 'Tableau', 'Excel Advanced', 'Git', 'Airflow'],
    partnerRepo: {
      name: 'Alkame Nifty 50 Financial Engine',
      repo: 'https://github.com/Alkameinc/alkame-nifty-50-educational',
      focus: 'NSE ticker ingestion, financial ratio variance, and automated BI reporting.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'SQL Aggregations & Schema Design', tasks: ['Write complex multi-table window functions', 'Clean corporate transaction logs with Pandas', 'PR on Alkame dataset pipeline'] },
      { period: 'Weeks 3–6', title: 'Automated BI & Cohort Decomposition', tasks: ['Construct live executive dashboards in Metabase', 'Engineer automated variance decomposition models', 'Build weekly email report automation'] },
      { period: 'Weeks 7–8', title: 'Data Audit & Credential Release', tasks: ['Submit verified portfolio analytical dossier', 'Turnitin originality review (< 5%)', 'Release ₹5,000 performance stipend'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Advanced SQL & Relational Databases', topics: ['Joins, subqueries, and CTEs', 'Window functions and ranking', 'Database query optimization'] },
      { period: 'Weeks 5–8', title: 'Python for Data Analysis & Pandas', topics: ['Data cleaning & wrangling', 'Statistical analysis & hypothesis testing', 'Time-series forecasting'] },
      { period: 'Weeks 9–12', title: 'Power BI, Metabase & Enterprise BI', topics: ['DAX calculations', 'Interactive executive dashboards', 'Automated corporate reporting'] }
    ],
    faqs: [
      { question: 'Is prior math or coding required for Data Analytics?', answer: 'Basic college math and logical reasoning are sufficient. We teach Python and SQL from foundational principles up to enterprise dashboards.' }
    ]
  },
  'cybersecurity': {
    slug: 'cybersecurity',
    title: 'Cybersecurity & Threat Defense Engineering',
    badge: '🛡️ Threat Defense & Infosec',
    headline: 'Defend Systems Against Exploitation & Pass Security Audits',
    lede: 'Learn ethical penetration testing, OWASP Top 10 vulnerabilities, packet capture with Wireshark, SIEM log correlation, and Linux defense-in-depth architecture.',
    salaryRange: '₹6,00,000 – ₹15,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['OWASP Top 10', 'Wireshark', 'Burp Suite', 'SIEM Logs', 'SOC Analysis', 'Linux'],
    tools: ['Nmap', 'Metasploit', 'Wazuh', 'Snort', 'Kali Linux', 'Docker'],
    partnerRepo: {
      name: 'DBERT Security Audit & Defense Suite',
      repo: 'https://github.com/DBERT-INDIA/Internshipportal',
      focus: 'Web security headers, CSP policies, rate limiting, and SQL injection mitigations.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'Reconnaissance & Vulnerability Scanning', tasks: ['Nmap port scanning & banner inspection', 'Wireshark network packet analysis', 'PR for security header hardening'] },
      { period: 'Weeks 3–6', title: 'Web App Penetration Testing', tasks: ['Burp Suite proxy intercept & repeater tests', 'Audit OWASP Top 10 web vulnerabilities', 'Formulate CVSS vulnerability remediation pull requests'] },
      { period: 'Weeks 7–8', title: 'Security Audit & Credential Release', tasks: ['Deliver comprehensive penetration test report', 'Turnitin originality check (< 5%)', 'Receive verified certificate & ₹5,000 stipend'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Network Security & Linux Hardening', topics: ['TCP/IP handshakes & Wireshark', 'Linux permissions & firewalls', 'SSH keys & cryptography'] },
      { period: 'Weeks 5–8', title: 'Application Security & OWASP Top 10', topics: ['SQL Injection & XSS exploitation', 'Broken Object Level Authorization (BOLA)', 'CSRF & SSRF defenses'] },
      { period: 'Weeks 9–12', title: 'SOC Operations, SIEM & Incident Response', topics: ['Log analysis with Wazuh/Splunk', 'Intrusion Detection Systems (IDS)', 'Remediation runbooks & compliance'] }
    ],
    faqs: [
      { question: 'Is this an ethical hacking course?', answer: 'Yes. All labs and penetration testing exercises are conducted strictly on isolated sandbox networks and authorized repositories.' }
    ]
  },
  'devops-cloud': {
    slug: 'devops-cloud',
    title: 'DevOps & Cloud Systems Engineering',
    badge: '☁️ Cloud Infrastructure',
    headline: 'Architect Automated CI/CD, Docker Clusters & AWS Cloud',
    lede: 'Master Docker containerization, Kubernetes orchestration, GitHub Actions CI/CD pipelines, AWS cloud VPCs, Terraform Infrastructure as Code, and production monitoring.',
    salaryRange: '₹6,50,000 – ₹16,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['Docker', 'Kubernetes', 'AWS EC2', 'GitHub Actions', 'Terraform', 'CI/CD'],
    tools: ['Prometheus', 'Grafana', 'Nginx', 'Linux Shell', 'Bash', 'Terraform'],
    partnerRepo: {
      name: 'DBERT Production Cloud Blueprints',
      repo: 'https://github.com/DBERT-INDIA/Internshipportal',
      focus: 'Zero-downtime releases, systemd service supervision, and automated DB backups.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'Containerization & Multi-Stage Docker', tasks: ['Build multi-stage Dockerfiles for Node & Python', 'Configure container networking and volume mounts', 'Submit PR on container build optimizations'] },
      { period: 'Weeks 3–6', title: 'CI/CD & Cloud Infrastructure Automation', tasks: ['Build automated GitHub Actions test & deploy pipeline', 'Provision AWS EC2 instances with Terraform', 'Configure Nginx SSL termination with Certbot'] },
      { period: 'Weeks 7–8', title: 'Cluster Monitoring & Credential Release', tasks: ['Deploy Prometheus & Grafana system telemetry', 'Submit audited cloud infrastructure documentation', 'Receive ₹5,000 performance stipend release'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Linux Administration & Shell Scripting', topics: ['Linux system commands & permissions', 'Bash automation scripts', 'Networking, DNS & SSH configuration'] },
      { period: 'Weeks 5–8', title: 'Docker Containers & CI/CD Pipelines', topics: ['Docker architecture & image optimization', 'Docker Compose microservices', 'GitHub Actions workflow automation'] },
      { period: 'Weeks 9–12', title: 'Kubernetes Orchestration & AWS Cloud', topics: ['K8s Pods, Deployments & Services', 'AWS VPC, EC2, S3 & IAM policies', 'Production zero-downtime deployments'] }
    ],
    faqs: [
      { question: 'Do candidates get experience with real AWS accounts?', answer: 'Yes. Candidates configure real AWS cloud resources, provision virtual private clouds, and automate systemd services.' }
    ]
  },
  'mobile-app-development': {
    slug: 'mobile-app-development',
    title: 'Mobile App Development (Flutter & React Native)',
    badge: '📱 Cross-Platform Mobile',
    headline: 'Build Cross-Platform iOS & Android Apps with Flutter',
    lede: 'Engineer production-ready mobile apps with Flutter/Dart and React Native, implementing offline SQLite caching, responsive UI layouts, and native device API bridges.',
    salaryRange: '₹5,50,000 – ₹14,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['Flutter', 'Dart', 'React Native', 'Mobile APIs', 'Offline SQLite', 'State Management'],
    tools: ['Firebase', 'Android Studio', 'Xcode', 'Postman', 'Git', 'Google Play Console'],
    partnerRepo: {
      name: 'Gayatri Tutor & Mobile Workbench',
      repo: 'https://github.com/Gayatri-Education/Gayatri-AI',
      focus: 'Cross-platform mobile UI, offline test caching, and real-time push notifications.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'Mobile Architecture & State Management', tasks: ['Set up cross-platform Flutter/React Native project', 'Implement Provider / BLoC state management', 'PR on mobile component library'] },
      { period: 'Weeks 3–6', title: 'Offline Database & REST API Sync', tasks: ['Configure local SQLite offline persistence', 'Connect to authenticated REST backend APIs', 'Implement Firebase Cloud Messaging push alerts'] },
      { period: 'Weeks 7–8', title: 'App Store Signing & Credential Release', tasks: ['Generate release APK / App Bundle', 'Submit audited capstone documentation (Turnitin < 5%)', 'Receive verified certificate & ₹5,000 stipend'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Dart Language & Flutter Fundamentals', topics: ['Dart OOP & async programming', 'Flutter widget tree & layout ergonomics', 'Form validation & user input'] },
      { period: 'Weeks 5–8', title: 'State Management & Offline Storage', topics: ['BLoC & Riverpod state patterns', 'SQLite database with Drift', 'REST API networking with Dio'] },
      { period: 'Weeks 9–12', title: 'Native Device Features & App Store Release', topics: ['Camera, location & biometrics APIs', 'Firebase authentication & analytics', 'Google Play Store publishing workflow'] }
    ],
    faqs: [
      { question: 'Can I test my code without a Mac?', answer: 'Yes. You can build and test Android APKs directly on Windows/Linux, and test iOS applications via cloud simulator harnesses.' }
    ]
  },
  'python-automation': {
    slug: 'python-automation',
    title: 'Python Automation & Web Extraction Engineering',
    badge: '⚙️ Autonomous Workflows',
    headline: 'Deploy Resilient Web Bots, Scrapers & Distributed Tasks',
    lede: 'Master Playwright and Selenium headless browser automation, Scrapy crawlers, Celery async distributed tasks, Redis queues, and resilient data synchronization workflows.',
    salaryRange: '₹5,00,000 – ₹13,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['Playwright', 'Scrapy', 'Celery', 'Redis', 'Python Async', 'PostgreSQL'],
    tools: ['Selenium', 'Beautiful Soup', 'Docker', 'FastAPI', 'Cron', 'Git'],
    partnerRepo: {
      name: 'DBERT Omnichannel Automation Daemons',
      repo: 'https://github.com/DBERT-INDIA/Internshipportal',
      focus: 'Playwright headless testing, automated candidate dispatching, and queue deduplication.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'Headless Browser Automation with Playwright', tasks: ['Write Playwright automated session scripts', 'Handle anti-bot challenges and session cookies', 'PR on portal automated testing harness'] },
      { period: 'Weeks 3–6', title: 'Distributed Task Queues with Celery & Redis', tasks: ['Configure asynchronous task workers with Celery', 'Build rate-limiting jitter algorithms', 'Implement idempotent SQLite/PostgreSQL deduplication'] },
      { period: 'Weeks 7–8', title: 'Pipeline Hardening & Credential Release', tasks: ['Stress test crawling pipelines under high concurrency', 'Submit audited capstone documentation (Turnitin < 5%)', 'Receive verified certificate & ₹5,000 stipend'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Advanced Python & Asyncio Architecture', topics: ['Asyncio event loops & coroutines', 'HTTP clients with httpx & aiohttp', 'Error handling & retry backoffs'] },
      { period: 'Weeks 5–8', title: 'Web Scraping & Headless Automation', topics: ['Playwright browser orchestration', 'DOM manipulation & shadow root selectors', 'Scrapy spiders & data pipelines'] },
      { period: 'Weeks 9–12', title: 'Distributed Workflows & Enterprise Automation', topics: ['Celery task queues with Redis', 'Dockerizing background worker daemons', 'Database synchronization & cron monitoring'] }
    ],
    faqs: [
      { question: 'Is Python automation useful for AI engineering?', answer: 'Crucial. Synthetic data generation, web knowledge retrieval, and LLM tool calling all rely fundamentally on Python automation pipelines.' }
    ]
  },
  'ui-ux-design': {
    slug: 'ui-ux-design',
    title: 'UI/UX Design & Venture Product Prototyping',
    badge: '🎨 Enterprise Design Systems',
    headline: 'Design High-Fidelity UI Systems & User Journey Flows',
    lede: 'Learn Figma component tokens, auto-layout, atomic design systems, interactive prototypes, user journey mapping, and WCAG accessibility standards for real venture products.',
    salaryRange: '₹5,00,000 – ₹13,00,000 LPA',
    stipend: '₹5,000 fixed + up to ₹18,000 performance incentive',
    skills: ['Figma', 'Auto-Layout', 'Design Systems', 'User Research', 'Wireframing', 'WCAG'],
    tools: ['Figma Tokens', 'FigJam', 'Notion', 'Tailwind Specs', 'Lottie', 'Git'],
    partnerRepo: {
      name: 'Gayatri AI & Aivara Design System',
      repo: 'https://github.com/Gayatri-Education/Gayatri-AI',
      focus: 'Component token libraries, responsive dark/light modes, and developer handoff specs.'
    },
    fellowshipWeeks: [
      { period: 'Weeks 1–2', title: 'Auto-Layout & Atomic Component Libraries', tasks: ['Design responsive auto-layout components in Figma', 'Build reusable atomic button & input tokens', 'PR on design system component review'] },
      { period: 'Weeks 3–6', title: 'High-Fidelity Interactive Prototyping', tasks: ['Create animated micro-interactions and screen transitions', 'Conduct qualitative user usability sessions', 'Formulate Tailwind CSS utility specifications'] },
      { period: 'Weeks 7–8', title: 'WCAG Accessibility Audit & Credential Release', tasks: ['Audit color contrast & keyboard navigation accessibility', 'Submit verified design portfolio dossier', 'Receive verified certificate & ₹5,000 stipend'] }
    ],
    courseWeeks: [
      { period: 'Weeks 1–4', title: 'Design Foundations & User Research', topics: ['Visual hierarchy, typography & color theory', 'User persona mapping & user interviews', 'Information architecture & wireframing'] },
      { period: 'Weeks 5–8', title: 'Figma Mastery & Advanced Auto-Layout', topics: ['Responsive auto-layout constraints', 'Component variants & interactive properties', 'Design system token architecture'] },
      { period: 'Weeks 9–12', title: 'Prototyping, Accessibility & Developer Handoff', topics: ['Smart animate & micro-interactions', 'WCAG 2.1 AA accessibility guidelines', 'Handoff documentation for React/Next.js'] }
    ],
    faqs: [
      { question: 'Do UI/UX designers need to write code?', answer: 'No coding is required. We focus on Figma, design systems, and preparing clean specs that engineers love building.' }
    ]
  }
};

export async function generateStaticParams() {
  return Object.keys(COURSES_DATA).map((domain) => ({ domain }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { domain } = await params;
  const course = COURSES_DATA[domain];

  if (!course) {
    return {
      title: 'Course Not Found | DBERT',
      description: 'The requested engineering course track was not found.'
    };
  }

  const title = `${course.title} (2026 Batch)`;
  const description = `Apply for the ${course.title} at DBERT. Master ${course.skills.slice(0, 4).join(', ')}, contribute to live venture codebases, and earn verifiable MSME credentials.`;

  return {
    title: `${title} | DBERT`,
    description,
    alternates: {
      canonical: `https://dbert.in/courses/${domain}`
    },
    openGraph: {
      title: `${title} | DBERT`,
      description,
      url: `https://dbert.in/courses/${domain}`,
      type: 'website'
    }
  };
}

export default async function DomainCoursePage({ params }: PageProps) {
  const { domain } = await params;
  const course = COURSES_DATA[domain];

  if (!course) {
    notFound();
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        '@id': `https://dbert.in/courses/${domain}#course`,
        name: course.title,
        description: course.lede,
        provider: {
          '@type': 'Organization',
          '@id': 'https://dbert.in/#organization',
          name: 'DBERT Technical Council & Venture Studio',
          url: 'https://dbert.in'
        },
        courseCode: `DBERT-${domain.toUpperCase().slice(0, 4)}-2026`,
        courseMode: 'Blended (Remote Sprint Labs & Mentorship)',
        educationalCredentialAwarded: 'DBERT Verified Systems Engineering Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '1999',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          url: `https://dbert.in/courses/${domain}`
        }
      },
      {
        '@type': 'EducationalOccupationalProgram',
        '@id': `https://dbert.in/courses/${domain}#program`,
        name: `DBERT ${course.title} Incubation Fellowship`,
        description: `2-Month high-velocity incubation sprint contributing to ${course.partnerRepo.name}. Includes ₹5,000 performance stipend and 3-document credential packet.`,
        provider: {
          '@type': 'Organization',
          name: 'DBERT',
          url: 'https://dbert.in'
        },
        timeToComplete: 'P2M',
        occupationalCategory: course.title
      },
      {
        '@type': 'BreadcrumbList',
        itemListElement: [
          { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://dbert.in' },
          { '@type': 'ListItem', position: 2, name: 'Courses', item: 'https://dbert.in/learners/courses' },
          { '@type': 'ListItem', position: 3, name: course.title, item: `https://dbert.in/courses/${domain}` }
        ]
      },
      {
        '@type': 'FAQPage',
        mainEntity: course.faqs.map((f) => ({
          '@type': 'Question',
          name: f.question,
          acceptedAnswer: { '@type': 'Answer', text: f.answer }
        }))
      }
    ]
  };

  const domainKeywords: Record<string, string[]> = {
    'ai-agent-development': ['intelligence', 'learning', 'agent'],
    'generative-ai': ['intelligence', 'learning'],
    'machine-learning': ['learning', 'intelligence'],
    'full-stack-development': ['full stack'],
    'data-analytics': ['data'],
    'python-automation': ['python'],
    'ui-ux-design': ['ui', 'ux', 'design'],
    'mobile-app-development': ['mobile'],
    'cybersecurity': ['security', 'python', 'cloud'],
    'devops-cloud': ['cloud', 'devops', 'python']
  };

  const kw = domainKeywords[domain] || [domain.split('-')[0]];
  const matchingAlumni: VerifiedAlum[] = (directoryData as any[])
    .filter((c) => kw.some((k) => (c.domain || '').toLowerCase().includes(k)))
    .sort((a, b) => (b.score || 0) - (a.score || 0))
    .slice(0, 6)
    .map((c) => ({
      certId: c.certId,
      holderName: c.holderName,
      domain: c.domain,
      score: c.score,
      grade: c.grade,
      verifyUrl: c.verifyUrl || `/verify/${c.certId}`
    }));

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <CourseInteractiveShell
        course={course}
        domain={domain}
        alumni={matchingAlumni}
      />
    </>
  );
}
