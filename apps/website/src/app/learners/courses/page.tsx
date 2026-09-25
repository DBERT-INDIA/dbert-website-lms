import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
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
          url: 'https://dbert.online/learners/courses/ai-agent-development',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },
        },
        {
          '@type': 'Course',
          position: 2,
          name: 'Generative AI Systems',
          description: 'Multi-provider LLMs, intelligent context pruning, live web research engines and streaming UIs.',
          url: 'https://dbert.online/learners/courses/generative-ai',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },
        },
        {
          '@type': 'Course',
          position: 3,
          name: 'Machine Learning & Fine-Tuning',
          description: 'Data preprocessing, feature engineering, and fine-tuning open-weights LLMs with LoRA/QLoRA.',
          url: 'https://dbert.online/learners/courses/machine-learning',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },
        },
        {
          '@type': 'Course',
          position: 4,
          name: 'Python System Automation',
          description: 'Scraping, scheduling, APIs and data pipelines taught through production automation.',
          url: 'https://dbert.online/learners/courses/python-automation',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },
        },
        {
          '@type': 'Course',
          position: 5,
          name: 'Full Stack AI Development',
          description: 'React, Next.js, Node.js, vector databases and streaming models deployed to production.',
          url: 'https://dbert.online/learners/courses/full-stack-development',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },
        },
        {
          '@type': 'Course',
          position: 6,
          name: 'Data Analytics & Automated BI',
          description: 'SQL, Python, Pandas and automated dashboards worked through on real corporate datasets.',
          url: 'https://dbert.online/learners/courses/data-analytics',
          provider: { '@type': 'Organization', name: 'DBERT', url: 'https://dbert.online' },
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
          <h1>AI and engineering courses with verifiable certificates</h1>
          <p>
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
                  <p className="text-xs text-muted leading-relaxed mb-4">
                    {course.description}
                  </p>
                </div>
                <div className="pt-4 border-t border-line/50 mt-auto">
                  <div className="text-[11px] font-mono text-accent mb-2">
                    {course.tech}
                  </div>
                  <div className="text-xs font-mono font-medium text-white flex items-center justify-between">
                    <span>Inspect Track Syllabus</span>
                    <span className="group-hover:translate-x-1 transition-transform">&rarr;</span>
                  </div>
                </div>
              </Link>
            </Reveal>
          ))}
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
