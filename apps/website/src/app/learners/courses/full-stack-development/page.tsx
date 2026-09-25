import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../learners.module.css';
import { Laptop, Rocket, Workflow, CheckCircle, ShieldCheck } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/full-stack-development');

export default function FullStackCoursePage() {
  const faqs = [
    {
      question: 'How does this full-stack curriculum differentiate itself from traditional MERN bootcamp programs?',
      answer: 'Standard coding bootcamps isolate frontend and backend instruction from artificial intelligence architectures. Our program embeds enterprise AI directly into your stack from day one: you master PostgreSQL with pgvector semantic similarity distance indexing, implement real-time Server-Sent Events (SSE) token streaming, and build full RAG production pipelines directly inside modern Next.js App Router applications.'
    },
    {
      question: 'What level of proficiency in web technologies is required prior to enrollment?',
      answer: 'Incoming students should possess functional familiarity with core HTML5, vanilla CSS styling, and JavaScript fundamental syntax (ES6 arrow functions, promises, and async/await structures). Candidates completely new to programming should complete our Launchpad introductory modules prior to tackling server components and Prisma ORM migrations.'
    },
    {
      question: 'Will I deploy my completed web applications to accessible live server environments?',
      answer: 'Absolutely. Every production capstone project is continuously integrated and deployed across active Vercel serverless domains, connected to managed cloud PostgreSQL databases (Supabase / Neon), and monitored via containerized telemetry—giving you live, public URLs for technical recruiters to evaluate.'
    },
    {
      question: 'How does DBERT institutional certification validation operate for aspiring software developers?',
      answer: 'Upon satisfactory completion of all repository pull requests and live technical interviews, your verified graduation credentials and project links are logged into our public authentication registry at dbert.online/verify, eliminating verification friction during enterprise hiring audits.'
    },
    {
      question: 'What career compensation tiers do full-stack AI developers typically command in India?',
      answer: 'Graduates equipped with dual full-stack and vector database engineering proficiency represent highly sought-after candidates across Indian venture-backed startups and consulting firms, commanding verified starting compensation packages spanning ₹4.0 LPA to ₹10.0 LPA depending on interview performance.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Full Stack AI & Modern Web Development Track',
        description: 'Comprehensive engineering Bootcamp in India teaching Next.js App Router, React, Node.js, Express, PostgreSQL, Prisma ORM, and integrated vector search RAG pipelines.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        courseCode: 'DBERT-ENG-FSTCK-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified Full Stack AI Software Engineering Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '38000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.online/learners/courses/full-stack-development'
        }
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqs.map(f => ({
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
          § 01 — CAREER TRACK <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Become a Full Stack AI Software Developer
        </h1>
        <p className={s.courseTagline}>
          ₹4,00,000 – ₹10,00,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master modern full-stack engineering across interactive React interfaces and Next.js server components, backed by scalable Node.js microservices and embedded PostgreSQL pgvector semantic indexing pipelines.
        </p>
      </div>

      {/* Key Metrics Grid (Secondary BG) */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Laptop aria-hidden="true" /></span>
              <h3 className="accent-note">Modern Tech Stack</h3>
              <p className="text-sm">Master Next.js App Router conventions, React server components, Node.js REST servers, and strict Prisma ORM schemas.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Workflow aria-hidden="true" /></span>
              <h3 className="accent-note">RAG Integrations</h3>
              <p className="text-sm">Configure semantic document search distance indexes directly within PostgreSQL databases utilizing optimized pgvector extensions.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Rocket aria-hidden="true" /></span>
              <h3 className="accent-note">Live Deployments</h3>
              <p className="text-sm">Deploy high-availability serverless production domains via Vercel, Supabase cloud databases, and Docker container infrastructures.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Course Curriculum & Skills (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — TECHNICAL CURRICULUM ARCHITECTURE</div>
        <h2 className="section-title mb-4">
          What You&apos;ll Master
        </h2>
        <div className="bento-grid-2">
          <div className="bento-card">
            <h3 className="block-title">
              1. Frontend Architectures &amp; Next.js Frameworks
            </h3>
            <p className="prose-sm text-muted">
              Build high-performance interactive user interfaces employing Server-Side Rendering (SSR), React Server Components (RSC), and robust declarative state patterns.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Next.js App Router: nested layouts, streaming boundaries &amp; server actions</li>
              <li>&bull; Advanced state synchronization via modern hooks and context architectures</li>
              <li>&bull; Designing semantic v2 design tokens with responsive CSS module layouts</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title">
              2. Backend REST Microservices &amp; Vector Indexing
            </h3>
            <p className="prose-sm text-muted">
              Design secure API server backends and configure high-speed relational databases optimized for both tabular business records and high-dimensional AI embedding search.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Node.js &amp; Express routing, custom middleware, CORS, and JWT authentication</li>
              <li>&bull; Relational data modeling &amp; automated type-safe migrations with Prisma ORM</li>
              <li>&bull; Vector embedding generation and cosine similarity matching with pgvector</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Instructor E-E-A-T & Leadership Profile Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 03 — INSTRUCTOR LEADERSHIP &amp; PROVENANCE</div>
        <h2 className="section-title mb-2">Taught by Active Full Stack AI Practitioners</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Learn modern full-stack AI development directly from systems architects who actively lead development across our proprietary SaaS catalog (including DBERT Chat and Intern Management System) and venture studio client repositories.
        </p>
        
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <div className="flex align-center gap-2 mb-1">
              <span className="font-mono text-sm text-white font-bold">DBERT Full Stack Leadership Team</span>
              <span className="badge badge-emerald text-xs">Active Industry Practitioners</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-4">
              We eliminate obsolete MERN boilerplate. Your code evaluations are conducted directly by senior full-stack developers who actively balance rendering performance, database connection pooling, and token streaming latency across commercial user volumes daily.
            </p>
            <div className="stack-h gap-4">
              <Link href="/about/team" className="accent-link text-xs font-mono font-medium">Inspect Engineering Faculty Credentials &rarr;</Link>
              <Link href="/ai-solutions/products" className="accent-link text-xs font-mono font-medium">Audit Proprietary DBERT SaaS Products &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Projects Section (Secondary BG) */}
      <div className="section-band-lg border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — CAPSTONE PRODUCTION PROJECTS</div>
          <h2 className="section-title mb-4">
            Production Projects You&apos;ll Ship to Live URLs
          </h2>
          <div className="bento-grid-2">
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 1 &middot; Hybrid RAG System</span>
              <h3 className={s.projectTitle}>Semantic Enterprise Document Search Engine</h3>
              <p className="prose-sm text-muted">
                An end-to-end Next.js application that autonomously ingests corporate PDF libraries, partitions complex content into semantic overlapping chunks, calculates embedding vectors via local models, persists payloads to PostgreSQL pgvector databases, and renders sub-100ms similarity results.
              </p>
            </div>
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 2 &middot; Token Streaming UI</span>
              <h3 className={s.projectTitle}>Real-Time Token Streaming Console &amp; Auth Portal</h3>
              <p className="prose-sm text-muted">
                Build an authenticated production chat dashboard that implements real-time Server-Sent Events (SSE) token streaming from custom open-weights endpoints, logging complete encrypted session transcripts and user usage parameters to Prisma relational tables.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Transparent Tuition & Zero-Cost EMI Table */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 05 — TUITION INVESTMENT &amp; EMI SCHEDULES</div>
        <h2 className="section-title mb-2">Transparent Indian Tuition &amp; Zero-Cost Financing</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Review our simple upfront tuition schedules or select adaptable Zero-Cost EMI installment models managed through verified Indian banking networks without hidden costs or restrictive post-placement income percentages.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹38,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Includes intensive live training sprints, serverless cloud database test credits, rigorous 1-on-1 code reviews, and lifetime institutional certification registry verification.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Immediate permanent access to repository architectural boilerplate</li>
              <li>Dedicated weekly 1-on-1 engineering debugging sessions</li>
              <li>Priority introduction to active Indian AI venture hiring squads</li>
            </ul>
            <Link href="/learners/launchpad?domain=full-stack-development" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹4,222 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Facilitated via authorized retail financial partners with zero documentation surcharges or early repayment penalties for qualified engineering candidates.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Expediated paperless loan authorization procedures</li>
              <li>Instant access to production servers upon installment activation</li>
              <li>Complete structural parity with upfront payment enrollments</li>
            </ul>
            <Link href="/about/contact" className="btn btn-outline w-full">Inquire About EMI Financing</Link>
          </div>
        </div>
      </div>

      {/* Tools Section (Primary BG) */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 06 — CORE TECHNICAL TOOLING</div>
        <h2 className={s.techHeading}>Production Technologies Mastered</h2>
        <div className={s.techRow}>
          {["Next.js 16", "React 19", "TypeScript", "Node.js", "Express", "PostgreSQL", "Prisma ORM", "pgvector", "Docker", "Git", "Vercel", "Tailwind / CSS"].map((tool, idx) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 07 — CAREER TRACK KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* CTA Block */}
      <div className="container pb-block">
        <div className="bento-card callout-plain p-8 border border-line bg-card text-center">
          <div className="doclabel mb-1">§ 08 — INITIALIZE CAREER ACCELERATION</div>
          <h2 className="card-title text-2xl font-bold text-white mb-2">Ship Full Stack AI Production Apps From Day One</h2>
          <p className="page-lede text-sm text-muted max-w-xl mx-auto mb-6">
            Ready to architect interactive Next.js consoles, configure high-throughput PostgreSQL vector indexes, and deploy real-time RAG applications to verified public endpoints? Enrol in DBERT Industrial Training today.
          </p>
          <div className="stack-h gap-4 justify-center">
            <Link href="/learners/launchpad" className="btn btn-primary btn-lg">Choose Your Career Path &rarr;</Link>
            <Link href="/blog/rag-pipeline-tutorial-from-scratch" className="btn btn-outline btn-lg">Read Tutorial on Production RAG</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

