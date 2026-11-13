/**
 * Canonical Technical Domains Configuration for DBERT Pre-Vetted Talent Directory
 * Maps raw candidate domain strings to standardized slugs, display titles,
 * curated skill taxonomies, and high-intent SEO metadata.
 */

export interface DomainMeta {
  slug: string;
  name: string;
  shortName: string;
  badge: string;
  headline: string;
  description: string;
  rawMatches: string[];
  primarySkills: string[];
  secondarySkills: string[];
  seoTitle: string;
  seoDescription: string;
  keywords: string[];
  faqs: { question: string; answer: string }[];
}

export const CANONICAL_DOMAINS: Record<string, DomainMeta> = {
  'full-stack-development': {
    slug: 'full-stack-development',
    name: 'Full Stack Web Development',
    shortName: 'Full Stack',
    badge: '⚡ Production Web Squads',
    headline: 'Pre-Vetted Full Stack Developers (Next.js, Node & Postgres)',
    description: 'Browse pre-screened Full Stack engineers evaluated on multi-tenant SaaS architectures, REST/GraphQL APIs, clean Git histories, and Turnitin-audited capstones. Onboard in 48 hours.',
    rawMatches: [
      'Full Stack Development',
      'Full Stack Web Development'
    ],
    primarySkills: ['Next.js', 'React 19', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
    secondarySkills: ['Prisma', 'REST APIs', 'GraphQL', 'Docker', 'JWT Auth', 'Redis', 'Zod', 'Express'],
    seoTitle: 'Pre-Vetted Full Stack Developers | DBERT Roster',
    seoDescription: 'Hire pre-vetted Full Stack developers evaluated on Next.js, Node & PostgreSQL with Turnitin rubrics and verified pull requests. Onboard in 48 hours.',
    keywords: [
      'Hire pre-vetted full stack developers',
      'Next.js engineers India',
      'React TypeScript software developers',
      'PostgreSQL full stack candidates',
      'Vetted full stack talent directory'
    ],
    faqs: [
      {
        question: 'How does DBERT screen Full Stack developers?',
        answer: 'Candidates are evaluated on actual SaaS feature implementations, clean component hierarchies, PostgreSQL schema migrations, and authenticated REST/GraphQL API endpoints. Code is audited for Turnitin originality and git hygiene.'
      },
      {
        question: 'What frameworks and databases do our Full Stack engineers master?',
        answer: 'Core competency covers Next.js 14/15/16 App Router, React 19, TypeScript, Node.js runtime, PostgreSQL, Prisma ORM, Tailwind CSS, Redis caching, and Docker containerization.'
      },
      {
        question: 'What is the turnaround time to onboard a Full Stack developer?',
        answer: 'Because candidates have already completed active sprints and peer-reviewed PRs, hiring managers can interview and onboard candidates within 48 to 72 hours with a 14-day risk-free trial.'
      },
      {
        question: 'Can we hire Full Stack developers for remote or on-site roles?',
        answer: 'Yes. All candidates are evaluated for asynchronous remote collaboration, git branching conventions, and daily standup communication, and are available for remote, hybrid, or on-site roles.'
      }
    ]
  },
  'ai-machine-learning': {
    slug: 'ai-machine-learning',
    name: 'AI & Machine Learning',
    shortName: 'AI & ML',
    badge: '🤖 Sovereign AI & LLM Systems',
    headline: 'Pre-Vetted AI & Machine Learning Engineers (PyTorch & LLMs)',
    description: 'Deploy pre-vetted AI & Machine Learning engineers with verified benchmarks in PyTorch, LangChain, RAG architectures, and fine-tuned sovereign models. Zero recruiter markup.',
    rawMatches: [
      'Artificial Intelligence & Machine Learning',
      'Artificial Intelligence (AI) & Machine Learning (ML)',
      'Artificial Intelligence (AI) and Machine Learning (ML)'
    ],
    primarySkills: ['PyTorch', 'LangChain', 'FastAPI', 'RAG Pipelines', 'Transformers', 'OpenCV'],
    secondarySkills: ['CrewAI', 'Hugging Face', 'Vector DBs', 'ChromaDB', 'Python', 'MLOps', 'Scikit-Learn', 'vLLM'],
    seoTitle: 'Pre-Vetted AI & ML Engineers | DBERT Directory',
    seoDescription: 'Browse pre-vetted AI & Machine Learning engineers evaluated on PyTorch, LangChain & LLM APIs with audited code dossiers and 14-day risk-free trials.',
    keywords: [
      'Hire AI engineers India',
      'Pre-vetted machine learning developers',
      'PyTorch LangChain engineers',
      'RAG pipeline developers',
      'LLM fine-tuning specialists'
    ],
    faqs: [
      {
        question: 'How are AI & Machine Learning engineers evaluated?',
        answer: 'Engineers build and benchmark production AI systems including Retrieval-Augmented Generation (RAG) pipelines, embedding vector search, model fine-tuning with LoRA/QLoRA, and FastAPI model inference endpoints.'
      },
      {
        question: 'Do candidates understand production model deployment?',
        answer: 'Yes. Candidates are evaluated on token latency optimization, vector indexing with Chroma/pgvector, prompt chaining with LangChain/CrewAI, and containerized deployment with Docker.'
      },
      {
        question: 'What is the difference between verified and provisional AI candidates?',
        answer: 'Verified candidates have completed full academic evaluations (scores 80-100), verified Turnitin capstones, and cryptographic credentials. Provisional candidates are actively completing their milestone sprints.'
      },
      {
        question: 'Are intellectual property (IP) assignments included?',
        answer: 'Yes, 100% IP rights transfer to your company upon placement. Candidates sign standard contractor NDAs and IP assignment agreements.'
      }
    ]
  },
  'data-analytics': {
    slug: 'data-analytics',
    name: 'Data Analytics & Business Intelligence',
    shortName: 'Data Analytics',
    badge: '📊 Quantitative Intelligence',
    headline: 'Pre-Vetted Data Analysts & BI Engineers (SQL & Power BI)',
    description: 'Onboard pre-vetted Data Analysts and BI engineers proficient in advanced SQL window functions, Python Pandas data modeling, automated ETL pipelines, and executive Power BI dashboards.',
    rawMatches: [
      'Data Analyst',
      'Data Analytics'
    ],
    primarySkills: ['SQL', 'Python Pandas', 'Power BI', 'Data Modeling', 'ETL Pipelines', 'Excel DAX'],
    secondarySkills: ['Tableau', 'PostgreSQL', 'NumPy', 'Seaborn', 'Statistical Testing', 'Data Warehousing', 'BigQuery'],
    seoTitle: 'Pre-Vetted Data Analysts & BI Engineers | DBERT',
    seoDescription: 'Hire pre-vetted Data Analysts with proven SQL, Python Pandas & Power BI portfolios evaluated on real business datasets. Onboard in 48 hours.',
    keywords: [
      'Hire pre-vetted data analysts',
      'SQL Power BI engineers India',
      'Python data analytics candidates',
      'Business intelligence developer directory',
      'Remote data analyst talent'
    ],
    faqs: [
      {
        question: 'What analytical tools are tested during candidate vetting?',
        answer: 'Candidates are evaluated on complex SQL multi-table joins, subqueries, CTEs, Python data transformation with Pandas, statistical modeling, and interactive Power BI/Tableau dashboard design.'
      },
      {
        question: 'Can DBERT Data Analysts build production ETL workflows?',
        answer: 'Yes. Fellows design automated extraction and loading pipelines, normalize relational data schemas, and generate actionable executive summaries.'
      },
      {
        question: 'How can hiring companies review a candidate’s work?',
        answer: 'Every candidate card features a "View Proof Dossier" link to their public evaluation rubric, capstone summary, Turnitin originality seal, and academic recommendation letter.'
      },
      {
        question: 'Is there a trial period for hiring data analysts?',
        answer: 'Yes. DBERT provides a 14-day risk-free evaluation period on your actual internal datasets and reporting queries.'
      }
    ]
  },
  'python-automation': {
    slug: 'python-automation',
    name: 'Python Automation & Web Scraping',
    shortName: 'Python Automation',
    badge: '⚙️ Autonomous Infrastructure',
    headline: 'Pre-Vetted Python Automation & Scraping Engineers',
    description: 'Hire pre-vetted Python engineers specialized in Playwright/Selenium browser automation, asynchronous Celery task queues, Redis caching, and resilient high-scale web crawlers.',
    rawMatches: [
      'Python Automation'
    ],
    primarySkills: ['Playwright', 'Selenium', 'Celery', 'Redis', 'Web Scraping', 'Python Asyncio'],
    secondarySkills: ['Beautiful Soup', 'FastAPI', 'Docker', 'Cron Scheduling', 'Anti-Bot Bypass', 'PostgreSQL'],
    seoTitle: 'Pre-Vetted Python Automation Engineers | DBERT',
    seoDescription: 'Hire pre-vetted Python automation engineers evaluated on Playwright, Celery, Redis & data scraping pipelines. Onboard in 48 hours risk-free.',
    keywords: [
      'Hire Python automation engineers',
      'Playwright web scraping developers',
      'Celery Redis workflow engineers',
      'Python script automation candidates',
      'Pre-vetted Python talent India'
    ],
    faqs: [
      {
        question: 'What automation frameworks do candidates master?',
        answer: 'Candidates build headful and headless web bots with Playwright and Selenium, distributed job processing with Celery and Redis, and automated data pipelines with asyncio.'
      },
      {
        question: 'Are candidates trained on anti-scraping countermeasures?',
        answer: 'Yes. Candidates understand user-agent rotation, proxy orchestration, rate-limiting jitter, DOM traversal, and session persistence.'
      },
      {
        question: 'How fast can a Python Automation engineer start?',
        answer: 'Pre-vetted candidates with verified credentials can be onboarded to your repository in 48 to 72 hours.'
      },
      {
        question: 'Do you charge recruitment or placement markup?',
        answer: 'No. DBERT charges zero recruiter markup or agency commissions on direct placements.'
      }
    ]
  },
  'ui-ux-design': {
    slug: 'ui-ux-design',
    name: 'UI/UX Product Design',
    shortName: 'UI/UX Design',
    badge: '🎨 Enterprise Interface Design',
    headline: 'Pre-Vetted UI/UX Product Designers (Figma & Systems)',
    description: 'Hire pre-screened UI/UX product designers proficient in Figma auto-layout, atomic design systems, interactive prototypes, user journey mapping, and WCAG accessibility standards.',
    rawMatches: [
      'UI/UX Design',
      'UI and UX Internship',
      'UI & UX Design'
    ],
    primarySkills: ['Figma', 'Auto-Layout', 'Design Systems', 'Wireframing', 'WCAG', 'User Journeys'],
    secondarySkills: ['Interactive Prototyping', 'Component Tokens', 'Design Tokens', 'Usability Testing', 'Mobile UI'],
    seoTitle: 'Pre-Vetted UI/UX Designers | DBERT Directory',
    seoDescription: 'Browse pre-vetted UI/UX designers evaluated on Figma auto-layout, design systems & WCAG accessibility with audited portfolios. Onboard in 48 hours.',
    keywords: [
      'Hire UI UX designers India',
      'Pre-vetted Figma product designers',
      'Design system specialists',
      'Mobile app UX UI talent',
      'Vetted designer directory'
    ],
    faqs: [
      {
        question: 'What design deliverables do DBERT UI/UX candidates produce?',
        answer: 'Candidates deliver Figma component libraries with responsive auto-layout, interactive state variants, atomic design tokens, user wireframes, and developer handoff specs.'
      },
      {
        question: 'Are designs tested for accessibility?',
        answer: 'Yes. All candidates are evaluated for WCAG 2.1 AA contrast compliance, keyboard focus readability, and mobile touch target ergonomics.'
      },
      {
        question: 'Can designers work directly with frontend developers?',
        answer: 'Yes. Candidates are trained to deliver clean CSS token definitions and Tailwind-compatible utility specs for seamless engineering handoffs.'
      },
      {
        question: 'How are design portfolios evaluated?',
        answer: 'Senior product designers review every candidate dossier for visual hierarchy, interaction fidelity, design system hygiene, and user research depth.'
      }
    ]
  },
  'devops-cloud': {
    slug: 'devops-cloud',
    name: 'DevOps & Cloud Engineering',
    shortName: 'DevOps & Cloud',
    badge: '☁️ Cloud Architecture',
    headline: 'Pre-Vetted DevOps & Cloud Engineers (AWS & Docker)',
    description: 'Access pre-vetted DevOps and Cloud engineers evaluated on Docker containerization, Kubernetes clusters, GitHub Actions CI/CD automation, Linux system administration, and AWS cloud VPCs.',
    rawMatches: [
      'DevOps & Cloud'
    ],
    primarySkills: ['Docker', 'Kubernetes', 'AWS', 'CI/CD Actions', 'Linux Shell', 'Nginx'],
    secondarySkills: ['Terraform', 'Prometheus', 'Grafana', 'PostgreSQL Admin', 'SSL/TLS', 'Bash Automation'],
    seoTitle: 'Pre-Vetted DevOps & Cloud Engineers | DBERT Roster',
    seoDescription: 'Hire pre-vetted DevOps & Cloud engineers evaluated on Docker, Kubernetes & AWS CI/CD pipelines with audited system builds. Onboard in 48 hours.',
    keywords: [
      'Hire DevOps engineers India',
      'Docker Kubernetes cloud developers',
      'AWS infrastructure specialists',
      'CI CD pipeline automation candidates',
      'Pre-vetted cloud talent'
    ],
    faqs: [
      {
        question: 'What cloud infrastructure competencies are evaluated?',
        answer: 'Engineers configure Docker multi-stage builds, container orchestration, automated GitHub Actions pipelines, Linux system hardening, and Nginx reverse proxy routing.'
      },
      {
        question: 'Do candidates have experience with production AWS deployments?',
        answer: 'Yes. Candidates manage EC2 instances, S3 storage policies, RDS PostgreSQL setups, and SSL/TLS certificate renewal automation.'
      },
      {
        question: 'Can DevOps engineers manage zero-downtime releases?',
        answer: 'Yes. Candidates are trained in green/blue deployments, systemd service supervision, and automated database backups.'
      },
      {
        question: 'Is there a risk-free trial for DevOps hires?',
        answer: 'Yes. All placements include a 14-day evaluation trial on your infrastructure.'
      }
    ]
  },
  'mobile-app-development': {
    slug: 'mobile-app-development',
    name: 'Mobile App Development',
    shortName: 'Mobile Apps',
    badge: '📱 Cross-Platform Apps',
    headline: 'Pre-Vetted Mobile App Developers (Flutter & React Native)',
    description: 'Deploy pre-vetted mobile app developers proficient in Flutter/Dart, React Native, Firebase integration, offline SQLite caching, state management, and responsive native UI architectures.',
    rawMatches: [
      'Mobile App Development'
    ],
    primarySkills: ['Flutter', 'Dart', 'React Native', 'Firebase', 'REST APIs', 'Android SDK'],
    secondarySkills: ['State Management', 'Provider / Bloc', 'Offline Storage', 'Push Notifications', 'iOS Xcode', 'SQLite'],
    seoTitle: 'Pre-Vetted Mobile App Developers | DBERT Directory',
    seoDescription: 'Hire pre-vetted mobile developers in Flutter, React Native & Firebase evaluated on live mobile builds and audited codebases. Onboard in 48 hours.',
    keywords: [
      'Hire Flutter developers India',
      'React Native mobile engineers',
      'Cross-platform app developers',
      'Firebase mobile app candidates',
      'Pre-vetted mobile talent directory'
    ],
    faqs: [
      {
        question: 'What mobile app frameworks do candidates specialize in?',
        answer: 'Candidates build cross-platform applications in Flutter/Dart and React Native, with native bridging, push notification services, and offline caching.'
      },
      {
        question: 'Are mobile applications tested on real physical devices?',
        answer: 'Yes. Deliverables are tested on real Android and iOS devices for performance, touch responsiveness, battery efficiency, and layout scaling.'
      },
      {
        question: 'Do candidates know how to publish to app stores?',
        answer: 'Yes. Candidates are trained on Google Play Console and Apple App Store signing, bundle optimization, and release track management.'
      },
      {
        question: 'How quickly can a mobile developer join our team?',
        answer: 'Verified mobile developers are ready to integrate into your existing Git workflows within 48 to 72 hours.'
      }
    ]
  }
};

/**
 * Returns canonical domain metadata by slug, or undefined.
 */
export function getDomainBySlug(slug: string): DomainMeta | undefined {
  return CANONICAL_DOMAINS[slug];
}

/**
 * Normalizes any raw domain string into its canonical slug.
 */
export function normalizeDomainToSlug(rawDomain: string): string {
  const trimmed = (rawDomain || '').trim();
  for (const domain of Object.values(CANONICAL_DOMAINS)) {
    if (domain.rawMatches.some((m) => m.toLowerCase() === trimmed.toLowerCase())) {
      return domain.slug;
    }
  }
  return '';
}

/**
 * Returns all canonical slugs.
 */
export function getAllDomainSlugs(): string[] {
  return Object.keys(CANONICAL_DOMAINS);
}
