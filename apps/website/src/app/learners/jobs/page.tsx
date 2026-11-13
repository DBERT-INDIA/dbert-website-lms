import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import s from '../learners.module.css';

export const metadata = pageMetadata('/learners/jobs');

export default function JobBoardPage() {
  const jobs = [
    {
      id: 1,
      title: 'RAG Pipeline Engineering Intern',
      company: 'DBERT Labs',
      type: 'Remote / Internship',
      domain: 'AI Agent Development',
      domainSlug: 'ai-agent-development',
      salary: '₹5,000 – ₹18,000 / month performance stipend',
      requirements: 'Python 3.11+, LangChain or LlamaIndex, vector indexing (pgvector/Chroma), Git pull-request workflow.',
      desc: 'Architect and deploy production Retrieval-Augmented Generation retrieval pipelines over complex unstructured enterprise documents.',
      slug: 'rag-pipeline-engineering-intern-remote-1'
    },
    {
      id: 2,
      title: 'LLM Tool-Calling Agent Intern',
      company: 'Gayatri AI',
      type: 'Remote / Internship',
      domain: 'AI Agent Development',
      domainSlug: 'ai-agent-development',
      salary: '₹5,000 – ₹18,000 / month performance stipend',
      requirements: 'FastAPI, CrewAI or LangGraph, structured JSON schema tool-calling, headless browser automation.',
      desc: 'Build multi-agent state machines with tool use, fallback loops, and autonomous browser scraping nodes.',
      slug: 'llm-tool-calling-agent-intern-remote-2'
    },
    {
      id: 16,
      title: 'AI Agent Developer (Junior / Associate)',
      company: 'Gayatri AI',
      type: 'Remote / Full-time',
      domain: 'AI Agent Development',
      domainSlug: 'ai-agent-development',
      salary: '₹4,80,000 – ₹7,50,000 LPA starting package',
      requirements: 'Python async, vLLM / Ollama quantization runtime setups, prompt evaluation harnesses, Redis message queues.',
      desc: 'Engineer production autonomous agent services deployed across high-throughput enterprise APIs.',
      slug: 'ai-agent-developer-remote-16'
    },
    {
      id: 17,
      title: 'Full Stack AI Systems Engineer',
      company: 'DBERT Systems',
      type: 'Remote / Full-time',
      domain: 'Full Stack Development',
      domainSlug: 'full-stack-development',
      salary: '₹5,20,000 – ₹8,40,000 LPA starting package',
      requirements: 'Next.js App Router, TypeScript, PostgreSQL pgvector, server actions, and streaming token chat interfaces.',
      desc: 'Develop responsive client dashboards, vector search query indexes, and secure authentication pipelines.',
      slug: 'llm-integration-engineer-remote-17'
    },
    {
      id: 103,
      title: 'Cybersecurity & SOC Analyst',
      company: 'DBERT Security',
      type: 'Remote / Full-time',
      domain: 'Cybersecurity',
      domainSlug: 'cybersecurity',
      salary: '₹4,50,000 – ₹9,00,000 LPA starting package',
      requirements: 'OWASP Top 10 web app testing, Wireshark packet capture analysis, SIEM log monitoring, compliance reporting.',
      desc: 'Audit cloud infrastructure, analyze access telemetry, and harden API gateways against adversarial intrusion.',
      slug: 'cybersecurity-soc-analyst-remote-103'
    },
    {
      id: 3,
      title: 'Conversational AI Workflow Intern',
      company: 'DBERT Labs',
      type: 'Remote / Internship',
      domain: 'AI Agent Development',
      domainSlug: 'ai-agent-development',
      salary: '₹5,000 – ₹18,000 / month performance stipend',
      requirements: 'Python Pandas, prompt tuning, API orchestration, conversation memory state serialization.',
      desc: 'Develop interactive context-aware conversational bots connected to relational databases and live analytics feeds.',
      slug: 'conversational-ai-workflow-intern-remote-3'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': jobs.map((job) => {
      const isIntern = job.type.toLowerCase().includes('intern') || job.type.toLowerCase().includes('fellowship');
      const isLpa = job.salary.includes('LPA');
      let minValue = 5000;
      let maxValue = 18000;
      let unitText = 'MONTH';

      if (isLpa) {
        unitText = 'YEAR';
        if (job.title.includes('Cybersecurity')) {
          minValue = 450000;
          maxValue = 900000;
        } else if (job.title.includes('Full Stack')) {
          minValue = 520000;
          maxValue = 840000;
        } else {
          minValue = 480000;
          maxValue = 750000;
        }
      }

      return {
        '@type': 'JobPosting',
        title: job.title,
        description: `<p>${job.desc}</p><p><strong>Role Requirements:</strong> ${job.requirements}</p><p><strong>Employment Type:</strong> ${job.type}</p><p><strong>Compensation:</strong> ${job.salary}</p>`,
        datePosted: '2026-11-01T00:00:00+05:30',
        validThrough: '2027-06-30T23:59:59+05:30',
        employmentType: isIntern ? 'INTERN' : 'FULL_TIME',
        hiringOrganization: {
          '@type': 'Organization',
          name: `${job.company} (DBERT Network)`,
          sameAs: 'https://dbert.in',
          logo: 'https://dbert.in/logo.svg',
        },
        jobLocationType: 'TELECOMMUTE',
        applicantLocationRequirements: {
          '@type': 'Country',
          name: 'IN',
        },
        baseSalary: {
          '@type': 'MonetaryAmount',
          currency: 'INR',
          value: {
            '@type': 'QuantitativeValue',
            minValue,
            maxValue,
            unitText,
          },
        },
        directApply: true,
      };
    }),
  };

  return (
    <div className="glow-wrapper">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="glow-spot"></div>

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — CAREER &amp; INTERNSHIP HIRING PORTAL <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          10,000+ Live Jobs &amp; Remote Internships
        </h1>
        <p className="lede-wide">
          Access verified engineering roles and internship pathways posted directly by our venture portfolio startups, partner companies, and live industry scrapers across India.
        </p>
        <div className="flex justify-center gap-3 flex-wrap mt-4">
          <a href="https://lms.dbert.in/internships" target="_blank" rel="noopener noreferrer" className="proof-mark proof-mark-signal">
            <span>⚡ 6,700+ Active Internships</span>
          </a>
          <a href="https://lms.dbert.in/jobs" target="_blank" rel="noopener noreferrer" className="proof-mark">
            <span>💼 3,100+ Full-Time Tech Roles</span>
          </a>
          <a href="https://lms.dbert.in/#signup" target="_blank" rel="noopener noreferrer" className="proof-mark">
            <span>✓ ₹5,000–₹18,000 Sprints</span>
          </a>
        </div>
        <div style={{ marginTop: '20px' }}>
          <a
            href="/learners/resume-checker"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              padding: '8px 18px',
              borderRadius: '20px',
              background: 'rgba(217, 119, 6, 0.12)',
              border: '1px solid rgba(217, 119, 6, 0.35)',
              color: '#F59E0B',
              fontSize: '0.85rem',
              fontWeight: 600,
              textDecoration: 'none',
            }}
          >
            <span>🎯 Want to check if your resume clears ATS filters for these jobs?</span>
            <span style={{ textDecoration: 'underline' }}>Run Free AI ATS Audit →</span>
          </a>
        </div>
      </div>

      {/* Live Discovery Gateway (Secondary BG) */}
      <div className="section-band">
        <div className="container center">
          <div className="doclabel mb-2">§ 02 — EXPLORE LIVE DOMAIN CHANNELS ON LMS</div>
          <p className="band-lede mb-6">
            Explore live opportunities curated by technical domain. Every application is reviewed directly on our LMS portal with fast-track mentor screening.
          </p>

          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4 max-w-4xl mx-auto text-left">
            <a
              href="https://lms.dbert.in/internships/full-stack-development"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Full Stack Development ↗</div>
              <div className="text-[11px] text-muted">React, Next.js, Node.js, Remote Sprints</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/data-analyst"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Data Analytics ↗</div>
              <div className="text-[11px] text-muted">Python Pandas, SQL, Dashboard Engineering</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/ai-agent-development"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">AI Agent Development ↗</div>
              <div className="text-[11px] text-muted">LangGraph, RAG, Swarms, vLLM Systems</div>
            </a>
            <a
              href="https://lms.dbert.in/internships/python-automation"
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 bg-[var(--surface-base)] border border-line rounded hover:border-accent transition-colors block"
            >
              <div className="text-xs font-mono text-accent font-semibold mb-1">Python Automation ↗</div>
              <div className="text-[11px] text-muted">Playwright, Scraping, Task Pipelines</div>
            </a>
          </div>

          <div className="mt-6 flex justify-center gap-3 flex-wrap">
            <a
              href="https://lms.dbert.in/internships"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary btn-sm"
            >
              Browse All 6,700+ Internships on LMS ↗
            </a>
            <a
              href="https://lms.dbert.in/jobs"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-outline btn-sm"
            >
              Browse All 3,100+ Jobs on LMS ↗
            </a>
          </div>
        </div>
      </div>

      {/* Featured Production Openings (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — FEATURED VENTURE SPRINT ROLES</div>
        <h2 className="section-title">
          Featured Production Sprints
        </h2>
        <div className={s.jobList}>
          {jobs.map((job) => (
            <div key={job.id} className={`bento-card ${s.jobCard}`}>
              <div className={s.jobTop}>
                <span className={s.companyTag}>{job.company}</span>
                <span className={s.jobSalary}>{job.salary}</span>
              </div>
              <h3 className={s.jobTitle}>{job.title}</h3>
              <p className={s.jobDesc}>{job.desc}</p>
              <div className={s.reqBlock}>
                <strong className={s.reqLabel}>Role Requirements:</strong>
                <p className={s.reqBody}>{job.requirements}</p>
              </div>
              <div className={s.jobFoot}>
                <span className={s.jobType}>{job.type}</span>
                <div className="flex gap-2">
                  <a
                    href={`https://lms.dbert.in/apply/${job.id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn btn-primary btn-sm"
                  >
                    Apply Now on LMS ↗
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Call (Secondary BG) */}
      <div className="band-top">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — PLACEMENT ACCELERATION &amp; FELLOWSHIP</div>
          <div className="bento-card cta-panel">
            <h2 className="card-title">Fast-Track Your Technical Placement</h2>
            <p className="page-lede">
              Applications are reviewed and prioritized for DBERT Fellowship and course graduates. Pass technical evaluations or enter via selection screening to build live software systems.
            </p>
            <div className="flex justify-center gap-3 flex-wrap mt-4">
              <a
                href="https://lms.dbert.in/#signup"
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary btn-lg"
              >
                Apply for Remote Internship (Track Auto-Selected) ↗
              </a>
              <Link href="/enroll/1999" className="btn btn-outline btn-lg">
                Confirm Fellowship Seat (₹1,500 Balance) →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
