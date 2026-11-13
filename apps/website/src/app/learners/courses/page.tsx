import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import HandNote from '@/components/ui/HandNote';
import s from '../learners.module.css';
import Reveal from '@/components/ui/Reveal';

export const metadata = pageMetadata('/learners/courses');

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'ItemList',
      name: 'DBERT Production AI & Engineering Skill Tracks',
      itemListElement: [
        {
          '@type': 'Course',
          position: 1,
          name: 'AI Agent Development',
          description: 'Orchestration frameworks, tool use, LangGraph, CrewAI and deployment.',
          url: 'https://dbert.in/learners/courses/ai-agent-development',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 2,
          name: 'Generative AI Systems',
          description: 'Multi-provider LLMs, intelligent context pruning, live web research engines and streaming UIs.',
          url: 'https://dbert.in/learners/courses/generative-ai',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 3,
          name: 'Machine Learning & Fine-Tuning',
          description: 'Data preprocessing, feature engineering, and fine-tuning open-weights LLMs with LoRA/QLoRA.',
          url: 'https://dbert.in/learners/courses/machine-learning',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 4,
          name: 'Python System Automation',
          description: 'Scraping, scheduling, APIs and data pipelines taught through production automation.',
          url: 'https://dbert.in/learners/courses/python-automation',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 5,
          name: 'Full Stack AI Development',
          description: 'React, Next.js, Node.js, vector databases and streaming models deployed to production.',
          url: 'https://dbert.in/learners/courses/full-stack-development',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 6,
          name: 'Data Analytics & Automated BI',
          description: 'SQL, Python, Pandas and automated dashboards worked through on real corporate datasets.',
          url: 'https://dbert.in/learners/courses/data-analytics',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 7,
          name: 'UI/UX Design & Product Prototyping',
          description: 'Figma auto-layout, design systems, user flows, and interactive prototyping.',
          url: 'https://dbert.in/learners/courses/ui-ux-design',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 8,
          name: 'DevOps & Cloud Infrastructure',
          description: 'Docker containerization, Kubernetes orchestration, CI/CD pipelines, and AWS deployment.',
          url: 'https://dbert.in/learners/courses/devops-cloud',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 9,
          name: 'Mobile App Development',
          description: 'Cross-platform iOS and Android app engineering with Flutter, Dart, and React Native.',
          url: 'https://dbert.in/learners/courses/mobile-app-development',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 10,
          name: 'Cybersecurity & Threat Defense',
          description: 'Ethical hacking, OWASP Top 10 vulnerabilities, Wireshark, SOC analysis, and SIEM monitoring.',
          url: 'https://dbert.in/learners/courses/cybersecurity',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
        {
          '@type': 'Course',
          position: 11,
          name: 'Digital Marketing & Growth Engineering',
          description: 'Technical SEO, Google & Meta Ads performance marketing, conversion optimization, and GA4 analytics.',
          url: 'https://dbert.in/learners/courses/digital-marketing',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.in' },
        },
      ],
    },
  ],
};

const courses = [
  {
    href: '/learners/courses/ai-agent-development',
    title: 'AI Agent Development',
    badge: 'Trending #1',
    duration: '2 Months • 8 Sprints',
    tech: 'LangGraph, CrewAI, Ollama',
    description:
      'Autonomous multi-agent state machines, tool use and local LLM runtime deployment, ending in a functional agent you demo.',
  },
  {
    href: '/learners/courses/generative-ai',
    title: 'Generative AI Systems',
    badge: 'High Impact',
    duration: '2 Months • 8 Sprints',
    tech: 'Llama-3, vLLM, pgvector',
    description:
      'Multi-provider LLM orchestration, intelligent context pruning, live web research engines, and streaming token front-ends.',
  },
  {
    href: '/learners/courses/machine-learning',
    title: 'Machine Learning & Fine-Tuning',
    badge: 'Deep Tech',
    duration: '2 Months • 8 Sprints',
    tech: 'PyTorch, LoRA, HuggingFace',
    description:
      'Data preprocessing pipelines, synthetic dataset curation, and parameter-efficient fine-tuning on open-weights foundation models.',
  },
  {
    href: '/learners/courses/python-automation',
    title: 'Python Automation',
    badge: 'High Demand',
    duration: '2 Months • 8 Sprints',
    tech: 'Playwright, Celery, Redis',
    description:
      'High-throughput web scraping, headless browser automation, background task queues, and automated reporting scripts.',
  },
  {
    href: '/learners/courses/full-stack-development',
    title: 'Full Stack AI Development',
    badge: 'Most Popular',
    duration: '2 Months • 8 Sprints',
    tech: 'Next.js, TypeScript, PostgreSQL',
    description:
      'Production web engineering covering React 19, TypeScript, API route architecture, vector search, and containerized deployment.',
  },
  {
    href: '/learners/courses/data-analytics',
    title: 'Data Analytics & BI',
    badge: 'Evergreen',
    duration: '2 Months • 8 Sprints',
    tech: 'Pandas, SQL, Metabase',
    description:
      'SQL query optimization, Python Pandas ETL pipelines, automated reporting dashboards, and statistical signal extraction.',
  },
  {
    href: '/learners/courses/ui-ux-design',
    title: 'UI/UX Design & Prototyping',
    badge: 'Design Track',
    duration: '2 Months • 8 Sprints',
    tech: 'Figma, Auto-Layout, Design Systems',
    description:
      'User journey mapping, wireframing, component design tokens, and interactive mobile/web prototypes built in Figma.',
  },
  {
    href: '/learners/courses/devops-cloud',
    title: 'DevOps & Cloud Engineering',
    badge: 'High Demand',
    duration: '2 Months • 8 Sprints',
    tech: 'Docker, Kubernetes, AWS, CI/CD',
    description:
      'Containerization, cluster orchestration, automated GitHub Actions pipelines, and scalable cloud deployment architectures.',
  },
  {
    href: '/learners/courses/mobile-app-development',
    title: 'Mobile App Development',
    badge: 'Mobile Track',
    duration: '2 Months • 8 Sprints',
    tech: 'Flutter, Dart, React Native',
    description:
      'Cross-platform native iOS & Android applications, reactive state management, offline persistence, and mobile APIs.',
  },
  {
    href: '/learners/courses/cybersecurity',
    title: 'Cybersecurity & Defense',
    badge: 'Security Track',
    duration: '2 Months • 8 Sprints',
    tech: 'Wireshark, Burp Suite, SOC, SIEM',
    description:
      'Ethical hacking methodologies, OWASP web application auditing, network packet analysis, and security telemetry monitoring.',
  },
  {
    href: '/learners/courses/digital-marketing',
    title: 'Digital Marketing & Growth',
    badge: 'Growth Track',
    duration: '2 Months • 8 Sprints',
    tech: 'GA4, Google Ads, Meta Ads, SEO',
    description:
      'Technical SEO architecture, performance acquisition funnels, conversion rate optimization (CRO), and growth analytics.',
  },
];

export default function CoursesHubPage() {
  return (
    <section className="section">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="wrap">
        <Reveal className="section-head">
          <div className="doclabel">
            § 01 — COURSES <span className="rev">skill tracks</span>
          </div>
          <div className="stack-h align-baseline gap-3 flex-wrap">
            <h1>AI and engineering courses with verifiable certificates</h1>
            <HandNote tone="amber">
              production code · real pull requests ✍
            </HandNote>
          </div>
          <p className="body-copy">
            Six focused technical tracks built around production engineering practices. Complete them through guided sprints, merge pull requests against real codebases, and verify your credentials on-chain. If you want the full sequence from beginner to paid fellowship, explore the{' '}
            <Link href="/learners" className={s.backLink}>
              career ladder
            </Link>{' '}
            first.
          </p>
        </Reveal>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 my-8">
          {courses.map((course) => (
            <Reveal key={course.href} as="div">
              <Link href={course.href} className="card card-lift p-6 bg-card border border-line flex flex-col justify-between h-full group">
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="tag-chip text-xs font-mono">{course.badge}</span>
                    <span className="text-xs font-mono text-muted">{course.duration}</span>
                  </div>
                  <h2 className="font-mono text-xl font-bold text-white group-hover:text-accent transition-colors mb-2">
                    {course.title}
                  </h2>
                  <p className="text-xs leading-relaxed mb-4 text-[var(--text-secondary)]">
                    {course.description}
                  </p>
                </div>
                <div className="pt-4 border-t border-line/50 mt-auto">
                  <div className="text-[11px] font-mono text-accent mb-2">
                    {course.tech}
                  </div>
                  <div className="text-xs font-mono font-medium text-[var(--text-primary)] flex items-center justify-between">
                    <span>Inspect Track Syllabus</span>
                    <span className="group-hover:translate-x-1 transition-transform">&rarr;</span>
                  </div>
                </div>
              </Link>
            </Reveal>
          ))}
        </div>

        {/* Live Regional Opportunities Discovery Hub */}
        <div className="card p-6 bg-card border border-line mt-12 mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
            <div>
              <span className="doclabel text-xs">§ 02 — LIVE SPRINT DISCOVERY PORTAL</span>
              <h2 className="text-xl font-bold font-mono text-white mt-1">
                Explore 3,200+ Live Industry Internships &amp; Placements
              </h2>
              <p className="text-xs text-muted max-w-2xl mt-1">
                Looking for immediate hands-on startup sprints with stipends? Our live portal matches candidates across Mumbai, Bengaluru, Delhi NCR, Pune, and remote teams.
              </p>
            </div>
            <a
              href="https://lms.dbert.in/"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary text-xs shrink-0"
            >
              Launch Internship Portal ↗
            </a>
          </div>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4 pt-4 border-t border-line">
            <a
              href="https://lms.dbert.in/internships/full-stack-development"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Full Stack AI Track ↗</div>
              <div className="text-[11px] text-muted">Mumbai, Bengaluru, Remote Sprints</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/data-analyst"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Data Analytics Track ↗</div>
              <div className="text-[11px] text-muted">SQL, Power BI, Corporate Reporting</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/python-automation"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Python Automation Track ↗</div>
              <div className="text-[11px] text-muted">Scraping, QA Testing, Orchestration</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/ai-agent-development"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block text-left"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">AI Agent Systems Track ↗</div>
              <div className="text-[11px] text-muted">LangGraph, RAG, Swarms, vLLM</div>
            </a>
          </div>
        </div>

        <Reveal className="hub-cta-row text-center mt-10">
          <Link href="/learners" className="btn btn-outline">
            &larr; Return to Progressive Career Ladder
          </Link>
        </Reveal>
      </div>
    </section>
  );
}
