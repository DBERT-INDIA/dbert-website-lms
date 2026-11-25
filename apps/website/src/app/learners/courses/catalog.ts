export const courseCategories = {
  'ai-data': 'AI & data',
  software: 'Software & infrastructure',
  'design-growth': 'Design & growth',
} as const;

type Course = {
  href: string;
  title: string;
  category: keyof typeof courseCategories;
  duration: string;
  tech: string;
  description: string;
};

export const courses = [
  {
    href: '/learners/courses/ai-agent-development',
    title: 'AI Agent Development',
    category: 'ai-data',
    duration: '2 months · 8 sprints',
    tech: 'LangGraph, CrewAI, Ollama',
    description:
      'Autonomous multi-agent state machines, tool use and local LLM runtime deployment, ending in a functional agent you demo.',
  },
  {
    href: '/learners/courses/generative-ai',
    title: 'Generative AI Systems',
    category: 'ai-data',
    duration: '2 months · 8 sprints',
    tech: 'Llama-3, vLLM, pgvector',
    description:
      'Multi-provider LLM orchestration, intelligent context pruning, live web research engines, and streaming token front-ends.',
  },
  {
    href: '/learners/courses/machine-learning',
    title: 'Machine Learning & Fine-Tuning',
    category: 'ai-data',
    duration: '2 months · 8 sprints',
    tech: 'PyTorch, LoRA, HuggingFace',
    description:
      'Data preprocessing pipelines, synthetic dataset curation, and parameter-efficient fine-tuning on open-weights foundation models.',
  },
  {
    href: '/learners/courses/python-automation',
    title: 'Python Automation',
    category: 'software',
    duration: '2 months · 8 sprints',
    tech: 'Playwright, Celery, Redis',
    description:
      'High-throughput web scraping, headless browser automation, background task queues, and automated reporting scripts.',
  },
  {
    href: '/learners/courses/full-stack-development',
    title: 'Full Stack AI Development',
    category: 'software',
    duration: '2 months · 8 sprints',
    tech: 'Next.js, TypeScript, PostgreSQL',
    description:
      'Production web engineering covering React 19, TypeScript, API route architecture, vector search, and containerized deployment.',
  },
  {
    href: '/learners/courses/data-analytics',
    title: 'Data Analytics & BI',
    category: 'ai-data',
    duration: '2 months · 8 sprints',
    tech: 'Pandas, SQL, Metabase',
    description:
      'SQL query optimization, Python Pandas ETL pipelines, automated reporting dashboards, and statistical signal extraction.',
  },
  {
    href: '/learners/courses/ui-ux-design',
    title: 'UI/UX Design & Prototyping',
    category: 'design-growth',
    duration: '2 months · 8 sprints',
    tech: 'Figma, Auto-Layout, Design Systems',
    description:
      'User journey mapping, wireframing, component design tokens, and interactive mobile/web prototypes built in Figma.',
  },
  {
    href: '/learners/courses/devops-cloud',
    title: 'DevOps & Cloud Engineering',
    category: 'software',
    duration: '2 months · 8 sprints',
    tech: 'Docker, Kubernetes, AWS, CI/CD',
    description:
      'Containerization, cluster orchestration, automated GitHub Actions pipelines, and scalable cloud deployment architectures.',
  },
  {
    href: '/learners/courses/mobile-app-development',
    title: 'Mobile App Development',
    category: 'software',
    duration: '2 months · 8 sprints',
    tech: 'Flutter, Dart, React Native',
    description:
      'Cross-platform native iOS & Android applications, reactive state management, offline persistence, and mobile APIs.',
  },
  {
    href: '/learners/courses/cybersecurity',
    title: 'Cybersecurity & Defense',
    category: 'software',
    duration: '2 months · 8 sprints',
    tech: 'Wireshark, Burp Suite, SOC, SIEM',
    description:
      'Ethical hacking methodologies, OWASP web application auditing, network packet analysis, and security telemetry monitoring.',
  },
  {
    href: '/learners/courses/digital-marketing',
    title: 'Digital Marketing & Growth',
    category: 'design-growth',
    duration: '2 months · 8 sprints',
    tech: 'GA4, Google Ads, Meta Ads, SEO',
    description:
      'Technical SEO architecture, performance acquisition funnels, conversion rate optimization (CRO), and growth analytics.',
  },
] satisfies Course[];
