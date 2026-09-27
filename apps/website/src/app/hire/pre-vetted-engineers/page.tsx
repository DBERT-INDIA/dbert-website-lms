import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import s from '@/app/learners/learners.module.css';
import { UserCheck, ShieldCheck, Cpu, Code2, ArrowRight, CheckCircle2 } from 'lucide-react';

export const metadata = {
  title: 'Hire Pre-Vetted AI & Full Stack Engineers | DBERT Labs',
  description: 'Hire pre-vetted AI, Full Stack, and Data engineers evaluated through live code reviews and system architecture benchmarks. Onboard proven tech talent in 48 hours.',
  keywords: ['Hire pre-vetted AI engineers', 'Hire full stack developers India', 'Pre-screened tech talent', 'Remote software engineers', 'Vetted developer platform'],
};

export default function HirePreVettedEngineersPage() {
  const faqs = [
    {
      question: 'How does DBERT vet candidate engineering competence?',
      answer: 'Our screening process goes beyond algorithmic LeetCode puzzles. Candidates are evaluated on actual production commits, system design architecture, clean git histories, and PR code reviews from our active open-source repositories and client builds.'
    },
    {
      question: 'What is the turnaround time for hiring a pre-vetted engineer?',
      answer: 'Because our talent pipeline continuously develops and ships code in active DBERT sprints, matched candidates can be interviewed and onboarded into your engineering team within 48 to 72 hours.'
    },
    {
      question: 'What specialization domains are available for hire?',
      answer: 'We provide pre-vetted engineers across Generative AI Systems (LLMs, RAG, AI Agents), Full Stack Web Development (Next.js, FastAPI, Node.js), Python Automation & Scraping, and Data Analytics (PostgreSQL, Power BI).'
    },
    {
      question: 'How do you guarantee candidate quality and commitment?',
      answer: 'Every engineer undergoes behavioral assessment, technical code audit, and security background verification. We provide a 14-day risk-free trial period for all full-time placement engagements.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'Hire Pre-Vetted Engineers Platform',
        serviceType: 'Technical Talent Acquisition & Staffing',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        description: 'B2B technical hiring platform delivering pre-vetted AI, Full Stack, and Data engineers to startups and enterprises.'
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqs.map((f) => ({
          '@type': 'Question',
          name: f.question,
          acceptedAnswer: {
            '@type': 'Answer',
            text: f.answer
          }
        }))
      }
    ]
  };

  return (
    <div className="glow-wrapper">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <div className="glow-spot"></div>

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § B2B HIRING — TALENT PLATFORM <span className="rev">rev: 2026.1</span>
        </div>
        <h1 className="page-title">
          Hire Pre-Vetted AI & Software Engineers in 48 Hours
        </h1>
        <p className={s.courseTagline}>
          Vetted through Live System Builds, Code Reviews, & Production Commit Histories — Not Resume Keywords.
        </p>
        <p className={s.courseLede}>
          Stop wasting hundreds of engineering hours interviewing unqualified candidates. DBERT pre-screens engineers through active production sprints so you receive proven, deployment-ready talent.
        </p>
        <div style={{ marginTop: '24px', display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <a href="#contact-hiring" className="btn btn-primary btn-lg">
            Request Candidate Profiles <ArrowRight className="inline-icon" />
          </a>
          <a href="#vetting-process" className="btn btn-outline btn-lg">
            Our Vetting Methodology
          </a>
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><UserCheck aria-hidden="true" /></span>
              <h3 className="accent-note">Top 3% Technical Screening</h3>
              <p>Only candidates who successfully pass code architecture evaluations, multi-tier security checks, and code reviews join our roster.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><ShieldCheck aria-hidden="true" /></span>
              <h3 className="accent-note">14-Day Risk-Free Trial</h3>
              <p>Evaluate your engineer in your actual codebase. If they aren’t the right fit, pay nothing during the trial period.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Cpu aria-hidden="true" /></span>
              <h3 className="accent-note">Production-Ready Engineers</h3>
              <p>Our engineers are fluent in modern stacks: Next.js, Python FastAPI, PostgreSQL, LangChain, PyTorch, and Docker containers.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Vetting Guide / Educational SEO Content */}
      <div className="container section-gap" id="vetting-process">
        <div className="prose-wrapper">
          <h2>How to Evaluate Engineering Talent Beyond Algorithmic LeetCode Puzzles</h2>
          <p>
            Traditional technical hiring processes often fail because they test candidates on synthetic puzzle-solving rather than practical software engineering skills. At DBERT Labs, we evaluate candidates against real-world engineering benchmarks:
          </p>
          
          <div className="grid-2-col" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', margin: '32px 0' }}>
            <div className="card-box" style={{ padding: '24px', background: 'var(--card-bg)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 color="#10b981" /> 1. Production Code Review
              </h3>
              <p>Candidates submit pull requests against live modular applications. We evaluate error handling, modularity, type hints, and automated test coverage.</p>
            </div>

            <div className="card-box" style={{ padding: '24px', background: 'var(--card-bg)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 color="#10b981" /> 2. System Architecture Design
              </h3>
              <p>Engineers design scalable REST/GraphQL backend architecture, configure database indexing, and implement JWT/OAuth security patterns.</p>
            </div>

            <div className="card-box" style={{ padding: '24px', background: 'var(--card-bg)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 color="#10b981" /> 3. Async Communication & Speed
              </h3>
              <p>We test async collaboration skills, Git branch discipline, dynamic debugging speed, and documentation thoroughness.</p>
            </div>

            <div className="card-box" style={{ padding: '24px', background: 'var(--card-bg)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 color="#10b981" /> 4. AI & LLM Engineering Competence
              </h3>
              <p>For AI engineers, we audit context window management, sliding buffer algorithms, RAG vector embeddings, and fallback resiliency.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Hiring Form / CTA */}
      <div className="section-band" id="contact-hiring">
        <div className="container center-text" style={{ maxWidth: '700px', margin: '0 auto', textAlign: 'center' }}>
          <h2>Scale Your Engineering Team Today</h2>
          <p style={{ margin: '16px 0 32px 0', color: 'var(--text-muted)' }}>
            Tell us about your technical requirements and timeline. Receive curated candidate profiles within 24 hours.
          </p>
          <a href="https://internship.dbert.online/apply" className="btn btn-primary btn-lg" style={{ padding: '16px 36px', fontSize: '1.1rem' }}>
            Schedule Talent Discovery Call
          </a>
        </div>
      </div>

      {/* FAQ Accordion */}
      <div className="container section-gap">
        <h2 className="center-text" style={{ marginBottom: '32px' }}>Frequently Asked Questions</h2>
        <FAQAccordion items={faqs} />
      </div>
    </div>
  );
}
