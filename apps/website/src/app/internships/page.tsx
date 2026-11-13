import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import Reveal from '@/components/ui/Reveal';
import HandNote from '@/components/ui/HandNote';

export const metadata = pageMetadata('/internships');

export default function InternshipsHubPage() {
  const domains = [
    {
      slug: 'full-stack-development',
      title: 'Full Stack Web Development',
      badge: 'Most Popular',
      desc: 'Build production web apps with React 19, Next.js App Router, TypeScript, and PostgreSQL with pgvector indexing.',
      openings: '1,420+ Live Openings',
      stipend: '₹8,000 – ₹18,000 / mo',
      cities: 'Remote · Bengaluru · Delhi NCR · Mumbai'
    },
    {
      slug: 'ai-agent-development',
      title: 'AI Agent & LLM Systems',
      badge: 'Trending #1',
      desc: 'Construct autonomous AI workflow agents with LangGraph, CrewAI tool-calling loops, and local vLLM / Ollama runtimes.',
      openings: '890+ Live Openings',
      stipend: '₹10,000 – ₹18,000 / mo',
      cities: 'Remote · Bengaluru · Pune · Hyderabad'
    },
    {
      slug: 'data-analytics',
      title: 'Data Analytics & Corporate BI',
      badge: 'High Demand',
      desc: 'Engineer SQL query pipelines, programmatically normalise datasets with Pandas, and construct interactive Metabase/Power BI dashboards.',
      openings: '1,150+ Live Openings',
      stipend: '₹6,000 – ₹15,000 / mo',
      cities: 'Remote · Delhi NCR · Mumbai · Bengaluru'
    },
    {
      slug: 'python-automation',
      title: 'Python Automation & Scraping',
      badge: 'Fast-Track',
      desc: 'Write concurrent Playwright scrapers, configure Celery/Redis task workers, and automate high-throughput data extraction.',
      openings: '740+ Live Openings',
      stipend: '₹7,000 – ₹15,000 / mo',
      cities: 'Remote · Pune · Hyderabad · Chennai'
    },
    {
      slug: 'devops-cloud',
      title: 'DevOps & Cloud Engineering',
      badge: 'Infrastructure',
      desc: 'Deploy Docker microservices, configure Kubernetes clusters, build automated GitHub Actions CI/CD pipelines, and manage AWS EC2/VPC.',
      openings: '620+ Live Openings',
      stipend: '₹8,000 – ₹16,000 / mo',
      cities: 'Remote · Bengaluru · Noida · Hyderabad'
    },
    {
      slug: 'ui-ux-design',
      title: 'UI/UX Design & Prototyping',
      badge: 'Design Track',
      desc: 'Design component libraries, auto-layout tokens, UX research journeys, and interactive high-fidelity prototypes in Figma.',
      openings: '580+ Live Openings',
      stipend: '₹6,000 – ₹14,000 / mo',
      cities: 'Remote · Mumbai · Delhi · Bengaluru'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: 'DBERT Remote Internships Across India',
    itemListElement: domains.map((d, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      name: `${d.title} Remote Internship`,
      url: `https://dbert.in/internships/${d.slug}/remote`
    }))
  };

  return (
    <div className="glow-wrapper">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="glow-spot"></div>

      {/* Hero Header */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — REMOTE INTERNSHIP DISCOVERY <span className="rev">rev: 2026.2</span>
        </div>
        <div className="stack-h justify-center align-baseline gap-3 flex-wrap">
          <h1 className="page-title">
            Remote Internships Across India
          </h1>
          <HandNote tone="amber">
            live client repos · real stipends ✎
          </HandNote>
        </div>
        <p className="lede-wide">
          Explore over 10,000 verified internship opportunities and startup engineering sprints. Build production software under senior review, earn performance stipends, and graduate with cryptographic MSME credentials.
        </p>

        <div className="flex justify-center gap-3 flex-wrap mt-4">
          <span className="proof-mark proof-mark-signal">
            <span>⚡ 6,700+ Internships on Portal</span>
          </span>
          <span className="proof-mark">
            <span>₹5,000–₹18,000 Stipends</span>
          </span>
          <span className="proof-mark">
            <span>✓ Turnitin Originality Rubrics</span>
          </span>
          <span className="proof-mark">
            <span>✓ Verified MSME Entity</span>
          </span>
        </div>
      </div>

      {/* Quick Launchpad to LMS */}
      <div className="section-band">
        <div className="container center">
          <div className="doclabel mb-2">§ 02 — LIVE SPRINT GATEWAY</div>
          <h2 className="section-title mb-2">Connect Directly to LMS Live Inventory</h2>
          <p className="band-lede mb-6">
            Looking for immediate placement? Our dedicated LMS portal hosts full applicant tracking, mentor evaluation, and live company openings updated daily.
          </p>
          <div className="flex justify-center gap-4 flex-wrap">
            <a
              href="https://lms.dbert.in/internships"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary btn-lg"
            >
              Browse 6,700+ Internships on LMS Portal ↗
            </a>
            <a
              href="https://lms.dbert.in/#signup"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-outline btn-lg"
            >
              Apply for Next Cohort (Starts Monday) ↗
            </a>
          </div>
        </div>
      </div>

      {/* Domain Tracks Grid */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — SPECIALIZED TECHNICAL DOMAINS</div>
        <h2 className="section-title">
          Explore Internships by Domain
        </h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 my-6">
          {domains.map((domain) => (
            <Reveal key={domain.slug} as="div">
              <div className="card p-6 bg-card border border-line flex flex-col justify-between h-full group hover:border-accent transition-colors">
                <div>
                  <div className="flex justify-between items-center mb-3">
                    <span className="tag-chip text-xs font-mono">{domain.badge}</span>
                    <span className="text-xs font-mono text-emerald-400 font-semibold">{domain.stipend}</span>
                  </div>
                  <h3 className="font-mono text-xl font-bold text-white group-hover:text-accent transition-colors mb-2">
                    {domain.title}
                  </h3>
                  <p className="text-xs leading-relaxed mb-4 text-[var(--text-secondary)]">
                    {domain.desc}
                  </p>
                </div>
                <div className="pt-4 border-t border-line/50 mt-auto">
                  <div className="text-[11px] font-mono text-muted mb-3">
                    📍 {domain.cities}
                  </div>
                  <div className="flex flex-col gap-2">
                    <a
                      href={`https://lms.dbert.in/#signup?domain=${domain.slug}&next=/internships/${domain.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-primary btn-sm text-center"
                    >
                      Apply on LMS (Domain Auto-Selected) ↗
                    </a>
                    <a
                      href={`https://lms.dbert.in/internships/${domain.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-outline btn-sm text-center"
                    >
                      View Live Postings on Portal ↗
                    </a>
                  </div>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>

      {/* Acceleration Callout */}
      <div className="band-top">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — INCUBATION FELLOWSHIP &amp; SEAT CONFIRMATION</div>
          <div className="bento-card cta-panel text-center">
            <h2 className="card-title">Join the Paid Applied AI Fellowship</h2>
            <p className="page-lede max-w-2xl mx-auto mb-6">
              Skip traditional queues and join an embedded venture sprint building live production systems for incubated startups. 2-month sprints, senior pull request code reviews, and guaranteed MSME credential issuance.
            </p>
            <div className="flex justify-center gap-3 flex-wrap">
              <Link href="/enroll/1999" className="btn btn-primary btn-lg">
                Complete Fellowship Enrollment (₹1,500 Balance) →
              </Link>
              <Link href="/learners/fellowship" className="btn btn-outline btn-lg">
                Inspect Fellowship Curriculum →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
