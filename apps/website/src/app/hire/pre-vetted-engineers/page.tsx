import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import HandNote from '@/components/ui/HandNote';
import StudioConsole, { type FeedLine } from '@/components/ui/StudioConsole';
import FactTicker from '@/components/ui/FactTicker';
import s from '@/app/learners/learners.module.css';
import { UserCheck, ShieldCheck, Cpu, ArrowRight, CheckCircle2 } from 'lucide-react';

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

  const hiringTelemetryFeed: FeedLine[] = [
    {
      time: '10:04:12',
      tag: 'review',
      message: 'Full Stack Fellow PR audited for venture client',
      detail: '· Next.js 15 & Postgres multi-tenant schema',
    },
    {
      time: '10:14:45',
      tag: 'verify',
      message: 'Cryptographic LOR & commit history verified',
      detail: '· 42 commits merged on client production repo',
    },
    {
      time: '10:28:30',
      tag: 'deploy',
      message: 'Applied AI Fellow onboarded to pre-seed startup',
      detail: '· 48h match turnaround · zero recruiter fee',
    },
    {
      time: '10:35:18',
      tag: 'audit',
      message: 'System architecture benchmark completed',
      detail: '· 99.8% test coverage · JWT + OAuth auth',
    },
    {
      time: '10:49:02',
      tag: 'stipend',
      message: 'Trial period completed with 100% satisfaction',
      detail: '· permanent full-time offer extended',
    },
  ];

  const hiringFacts = [
    'top 3% technical screening bar',
    'zero recruiter commissions or markup',
    '14-day risk-free trial on your actual repo',
    'evaluated on live Git pull requests & system design',
    'onboard pre-vetted talent in 48-72 hours',
    'full IP assignment and contractor legal compliance',
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
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      {/* ══════════ SECTION 1: HERO (2-COLUMN GRID) ══════════ */}
      <section className="section-subpage-hero">
        <div className="wrap subpage-hero-grid">
          <div>
            <div className="doclabel">
              § B2B HIRING — TALENT PLATFORM <span className="rev">rev: 2026.1</span>
            </div>
            <h1 className="relative inline-block">
              Hire Pre-Vetted AI &amp; Software Engineers in 48 Hours
              <HandNote className="absolute -right-8 -top-6 text-lg hidden md:block" tone="blue">
                top 1% cohort fellows ✎
              </HandNote>
            </h1>
            <p className="intro-copy">
              Vetted through live system builds, code reviews, and production commit histories — not resume keywords. Onboard deployment-ready engineering squads without agency recruitment markups.
            </p>
            <div className="stack-h gap-4 mt-6 flex-wrap">
              <a href="#contact-hiring" className="btn btn-primary">
                Request Candidate Profiles <ArrowRight className="inline-icon" />
              </a>
              <a href="#vetting-process" className="btn btn-outline">
                Our Vetting Methodology
              </a>
            </div>
          </div>

          <div>
            <StudioConsole
              title="dbert-talent · candidate vetting & dispatch telemetry"
              lines={hiringTelemetryFeed}
              footLeft="industrial talent verification"
              footRight="● 48h turnaround"
            />
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 2: FULL-BLEED AMBIENT FACT TICKER ══════════ */}
      <div className="section-ticker-ribbon">
        <FactTicker facts={hiringFacts} />
      </div>

      {/* ══════════ SECTION 3: KEY METRICS GRID ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub text-center">
            <div className="doclabel justify-center">§ 02 — VETTING CRITERIA &amp; PROCESS</div>
            <h2>Industrial Vetting Standards</h2>
            <p className="mx-auto">Audited on live pull requests and distributed systems rather than algorithmic puzzles.</p>
          </div>
          <div className="bento-grid-3">
            <div className="card card-lift text-center p-6">
              <span className="icon-chip"><UserCheck aria-hidden="true" /></span>
              <h3 className="accent-note">Top 3% Technical Screening</h3>
              <p className="body-copy">Only candidates who successfully pass code architecture evaluations, multi-tier security checks, and code reviews join our roster.</p>
            </div>
            <div className="card card-lift text-center p-6">
              <span className="icon-chip"><ShieldCheck aria-hidden="true" /></span>
              <h3 className="accent-note">14-Day Risk-Free Trial</h3>
              <p className="body-copy">Evaluate your engineer in your actual codebase. If they aren’t the right fit, pay nothing during the trial period.</p>
            </div>
            <div className="card card-lift text-center p-6">
              <span className="icon-chip"><Cpu aria-hidden="true" /></span>
              <h3 className="accent-note">Production-Ready Engineers</h3>
              <p className="body-copy">Our engineers are fluent in modern stacks: Next.js, Python FastAPI, PostgreSQL, LangChain, PyTorch, and Docker containers.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 4: VETTING METHODOLOGY (BAND) ══════════ */}
      <section className="subpage-section band" id="vetting-process">
        <div className="wrap measure-lg">
          <div className="section-head-sub">
            <div className="doclabel">§ 03 — PRACTICAL EVALUATION METHODOLOGY</div>
            <h2>How to Evaluate Engineering Talent Beyond Algorithmic LeetCode Puzzles</h2>
            <p>
              Traditional technical hiring processes often fail because they test candidates on synthetic puzzle-solving rather than practical software engineering skills. At DBERT Labs, we evaluate candidates against real-world engineering benchmarks:
            </p>
          </div>
          
          <div className="bento-grid-2 my-8">
            <div className="card card-lift p-6">
              <h3 className="card-heading-lg stack-h align-center gap-2 mb-3">
                <CheckCircle2 className="text-signal shrink-0" size={20} /> 1. Production Code Review
              </h3>
              <p className="body-copy">Candidates submit pull requests against live modular applications. We evaluate error handling, modularity, type hints, and automated test coverage.</p>
            </div>

            <div className="card card-lift p-6">
              <h3 className="card-heading-lg stack-h align-center gap-2 mb-3">
                <CheckCircle2 className="text-signal shrink-0" size={20} /> 2. System Architecture Design
              </h3>
              <p className="body-copy">Engineers design scalable REST/GraphQL backend architecture, configure database indexing, and implement JWT/OAuth security patterns.</p>
            </div>

            <div className="card card-lift p-6">
              <h3 className="card-heading-lg stack-h align-center gap-2 mb-3">
                <CheckCircle2 className="text-signal shrink-0" size={20} /> 3. Async Communication &amp; Speed
              </h3>
              <p className="body-copy">We test async collaboration skills, Git branch discipline, dynamic debugging speed, and documentation thoroughness.</p>
            </div>

            <div className="card card-lift p-6">
              <h3 className="card-heading-lg stack-h align-center gap-2 mb-3">
                <CheckCircle2 className="text-signal shrink-0" size={20} /> 4. AI &amp; LLM Engineering Competence
              </h3>
              <p className="body-copy">For AI engineers, we audit context window management, sliding buffer algorithms, RAG vector embeddings, and fallback resiliency.</p>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 5: CONTACT & DISCOVERY CTA ══════════ */}
      <section className="subpage-section" id="contact-hiring">
        <div className="wrap measure-sm text-center">
          <div className="doclabel justify-center mb-2">§ 04 — TALENT DISCOVERY</div>
          <h2>Scale Your Engineering Team Today</h2>
          <p className="body-copy my-4 text-muted">
            Tell us about your technical requirements and timeline. Receive curated candidate profiles within 24 hours.
          </p>
          <Link href="/startups/services/hiring" className="btn btn-primary btn-lg">
            Schedule Talent Discovery Call
          </Link>
        </div>
      </section>

      {/* ══════════ SECTION 6: FAQS (BAND-ALT) ══════════ */}
      <section className="subpage-section band-alt">
        <div className="wrap measure">
          <div className="section-head-sub text-center">
            <div className="doclabel justify-center">§ 05 — FREQUENTLY ASKED QUESTIONS</div>
            <h2>Candidate Screening &amp; Engagement FAQs</h2>
          </div>
          <FAQAccordion items={faqs} />
        </div>
      </section>
    </>
  );
}
