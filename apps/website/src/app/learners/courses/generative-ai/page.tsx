import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../learners.module.css';
import { Sparkles, Brain, Zap, Briefcase, GitBranch } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/generative-ai');

export default function GenerativeAICoursePage() {
  const faqs = [
    {
      question: 'What programming background is required to join the Generative AI course?',
      answer: 'Candidates should have foundational familiarity with Python syntax (variables, functions, loops, basic dictionary manipulation) and basic HTTP API concepts. If you are starting from zero, our 2-month Launchpad will establish all prerequisites.'
    },
    {
      question: 'Do we only use commercial APIs like OpenAI or also work with open-source models?',
      answer: 'You master both. The curriculum teaches multi-provider API abstraction (OpenAI, Anthropic Claude, Google Gemini) alongside local open-weights execution, intelligent context sliding windows, and deep search synthesis.'
    },
    {
      question: 'What real-world projects will I build during this track?',
      answer: 'You will build and deploy a production-grade Generative AI research assistant based on our active open-source intern repository (Gayatri-AI), complete with multi-provider fallbacks, streaming web search grounding, and persistent SQLite memory.'
    },
    {
      question: 'How is my final course credential verified by employers?',
      answer: 'Every credential issued by DBERT Labs contains a cryptographically signed UUID that HR managers and tech recruiters can verify in real-time at dbert.online/verify.'
    },
    {
      question: 'How does this connect to the DBERT Fellowship or Startup referrals?',
      answer: 'High-performing candidates who complete and push their reviewed code to GitHub become directly eligible for our competitive, paid DBERT Fellowship and expedited interviews across our venture studio startups.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Generative AI & LLM Systems Engineering Track',
        description: 'Professional engineering track teaching multi-provider LLM orchestration, intelligent context management, deep web research synthesis, and streaming UI applications.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        courseCode: 'DBERT-ENG-GENAI-2026',
        courseMode: 'Blended (Cohort Sprints & Production Lab Work)',
        educationalCredentialAwarded: 'Verified Generative AI Systems Professional Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '32000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.online/learners/courses/generative-ai'
        }
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
          § 01 — CAREER TRACK <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Become a Generative AI Systems Engineer
        </h1>
        <p className={s.courseTagline}>
          ₹5,50,000 – ₹14,00,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master commercial LLM multi-provider orchestration, sliding-window context compression, and deep web research agents. Ship production-grade software grounded in our open-source intern repository architecture.
        </p>
      </div>

      {/* Key Metrics Grid */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Brain aria-hidden="true" /></span>
              <h3 className="accent-note">Multi-Provider LLM Core</h3>
              <p className="text-sm">Architect unified interfaces orchestrating OpenAI, Anthropic, and Gemini models with intelligent fallback hierarchies.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Sparkles aria-hidden="true" /></span>
              <h3 className="accent-note">Deep Research Engines</h3>
              <p className="text-sm">Build autonomous recursive search agents that scrape web targets, cross-verify evidence, and synthesize cited reports.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
              <h3 className="accent-note">Live Intern Proof-of-Work</h3>
              <p className="text-sm">Contribute directly to production codebases modeled after Gayatri-AI, building an auditable GitHub portfolio.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Reference Repo Spotlight */}
      <div className="container pad-block">
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="badge badge-emerald text-xs font-mono">Reference Repository</span>
              <span className="font-mono text-sm text-white font-bold">Gayatri-Education / Gayatri-AI</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-4">
              Our curriculum is directly derived from what previous DBERT interns built: a full-scale GenAI system featuring deep research loops, memory managers, SQLite context storage, and streaming UI components.
            </p>
            <div className="flex flex-wrap gap-2">
              {['Multi-Provider LLMs', 'Context Sliding Window', 'Recursive Web Research', 'Streaming SSE'].map((tag, idx) => (
                <span key={idx} className="text-[11px] px-2 py-0.5 rounded bg-raise border border-line text-zinc-300 font-mono">
                  {tag}
                </span>
              ))}
            </div>
          </div>
          <a
            href="https://github.com/Gayatri-Education/Gayatri-AI"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-outline btn-sm font-mono text-xs inline-flex items-center gap-2 whitespace-nowrap self-start"
          >
            <GitBranch className="w-3.5 h-3.5" />
            Inspect Live GitHub Repo &rarr;
          </a>
        </div>
      </div>

      {/* Course Curriculum & Skills */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — TECHNICAL CURRICULUM ARCHITECTURE</div>
        <h2 className="section-title mb-4">
          What You&apos;ll Master
        </h2>
        <div className="bento-grid-2">
          <div className="bento-card">
            <h3 className="block-title">
              1. Context Management &amp; Memory Preserving Loops
            </h3>
            <p className="prose-sm text-muted">
              Solve the context window bottleneck. Build algorithms that selectively summarize conversation turns, dynamically prune irrelevant history, and persist structured vectors in SQLite.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Sliding window token compression &amp; dynamic context trimming</li>
              <li>&bull; Long-term conversational memory with SQLite transactional stores</li>
              <li>&bull; Deterministic structured extraction and JSON schema enforcement</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title">
              2. Deep Research Agents &amp; Real-Time Search Grounding
            </h3>
            <p className="prose-sm text-muted">
              Bind large models to live search engines. Design recursive search trees that query Google/Bing, scrape unstructured HTML targets, and generate cited analytical briefs.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Autonomous query decomposition &amp; multi-source web crawlers</li>
              <li>&bull; Cross-source verification pipelines &amp; citation attribution</li>
              <li>&bull; Real-time Server-Sent Events (SSE) token streaming to frontend UIs</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Capstone Projects Section */}
      <div className="section-band-lg border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — CAPSTONE PRODUCTION PROJECTS</div>
          <h2 className="section-title mb-4">
            Production Projects You&apos;ll Ship to Your Git Repository
          </h2>
          <div className="bento-grid-2">
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 1 &middot; Deep Research</span>
              <h3 className={s.projectTitle}>Autonomous Deep Research Synthesis Engine</h3>
              <p className="prose-sm text-muted">
                An industrial-grade research agent that accepts complex prompts, formulates multi-angle search queries, parallelizes web scraping, validates source veracity, and writes comprehensive cited briefs.
              </p>
            </div>
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 2 &middot; Multi-Modal &amp; Memory</span>
              <h3 className={s.projectTitle}>Enterprise GenAI Assistant with Persistent Memory</h3>
              <p className="prose-sm text-muted">
                A multi-provider generative AI assistant built with LiteLLM, persistent SQLite memory, sliding context management, and a real-time streaming web UI deployed to the cloud.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Tuition Card */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — TUITION &amp; ADMISSION</div>
        <h2 className="section-title mb-2">Transparent Indian Tuition &amp; Flexible EMI</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Complete upfront transparency without hidden fees. Access live cohort sprints, GitHub code reviews, and expedited venture studio placement referrals.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹32,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Includes full synchronous cohort sessions, API compute credit allocations, project audits, and permanent credential registration.</p>
            <Link href="/learners/launchpad?domain=generative-ai" className="btn btn-primary w-full">
              Explore Launchpad Track &rarr;
            </Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹3,555 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Structured through verified Indian banking partnerships with minimal documentation and zero interest surcharge.</p>
            <Link href="/about/contact" className="btn btn-outline w-full">Inquire About EMI Financing</Link>
          </div>
        </div>
      </div>

      {/* Technologies Mastered */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 05 — PRODUCTION TECHNOLOGIES</div>
        <h2 className={s.techHeading}>Production Technologies Mastered</h2>
        <div className={s.techRow}>
          {['OpenAI API', 'Anthropic Claude', 'Google Gemini', 'LiteLLM', 'SQLite', 'Python', 'FastAPI', 'BeautifulSoup', 'SSE Streaming', 'Git/GitHub', 'Docker'].map((tool, idx) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* FAQ Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* CTA */}
      <div className="container pb-block">
        <div className="bento-card callout-plain p-8 border border-line bg-card text-center">
          <div className="doclabel mb-1">§ 07 — ENROLL IN INDUSTRIAL TRAINING</div>
          <h2 className="card-title text-2xl font-bold text-white mb-2">Launch Your Generative AI Career</h2>
          <p className="page-lede text-sm text-muted max-w-xl mx-auto mb-6">
            Ready to build commercial GenAI systems, engineer context management loops, and ship live GitHub repositories? Enroll today in DBERT Industrial Training.
          </p>
          <div className="stack-h gap-4 justify-center">
            <Link href="/learners/launchpad?domain=generative-ai" className="btn btn-primary btn-lg">
              Start 2-Month Launchpad Track &rarr;
            </Link>
            <Link href="/learners/courses" className="btn btn-outline btn-lg">
              View All 6 Courses
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
