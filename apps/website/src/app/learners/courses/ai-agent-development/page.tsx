import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../learners.module.css';
import { Bot, Briefcase, Zap, CheckCircle, ShieldCheck } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/ai-agent-development');

export default function AIAgentCoursePage() {
  const faqs = [
    {
      question: 'What prior programming proficiency is required before commencing the AI Agent Development course?',
      answer: 'Incoming candidates must possess demonstrated working fluency in core Python syntax (functions, classes, dictionaries, exception handling) and basic REST API interaction. Candidates without foundational syntax experience should begin directly in our introductory Launchpad programming curriculum.'
    },
    {
      question: 'How do fine-tuned local models differ from generic calling of OpenAI or Anthropic commercial APIs?',
      answer: 'While our technical curriculum thoroughly covers external API function calling, we place rigorous engineering emphasis on configuring localized open-weights inference (Ollama and vLLM runtimes). Serving weights locally guarantees total corporate data privacy, zero recurrent token API billing, and complete algorithmic customization.'
    },
    {
      question: 'Can I independently verify my final training certificate with potential Indian startup employers?',
      answer: 'Yes. Every issued engineering credential contains a unique cryptographic validation UUID that HR managers and technical team leads can verify instantly by accessing our open institutional portal at dbert.online/verify.'
    },
    {
      question: 'How are technical capstone sprint projects evaluated and integrated into developer Git portfolios?',
      answer: 'You do not submit static toy academic homework files. Capstones are evaluated through live GitHub pull requests reviewed by our senior practice instructors against real corporate software acceptance criteria, ensuring an auditable production contribution log.'
    },
    {
      question: 'Do you facilitate direct recruitment introductions upon cohort completion?',
      answer: 'Yes. Successful graduates who demonstrate consistently high code quality metrics during capstone evaluations are admitted directly into our audited talent roster, gaining expedited referral access to engineering squads across our incubated Indian AI venture studio startups.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'AI Agent Development & Multi-Agent Systems Engineering Track',
        description: 'Professional engineering program in India teaching autonomous multi-agent state machines, LangGraph, CrewAI, local GGUF weight quantization, and robust function calling pipelines.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        courseCode: 'DBERT-ENG-AGNT-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified AI Agent Systems Professional Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '35000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.online/learners/courses/ai-agent-development'
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
          Become an AI Agent Development Engineer
        </h1>
        <p className={s.courseTagline}>
          ₹5,00,000 – ₹12,00,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Acquire the production engineering proficiency required to architect, quantize, and orchestrate autonomous multi-agent systems. Master hierarchical state machines, deterministic tool calling schemas, and air-gapped local model serving.
        </p>
      </div>

      {/* Key Metrics Grid (Secondary BG) */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Bot aria-hidden="true" /></span>
              <h3 className="accent-note">Autonomous Agents</h3>
              <p className="text-sm">Engineer resilient LangGraph and CrewAI conversational loops, supervisor routers, and hierarchal memory states.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Zap aria-hidden="true" /></span>
              <h3 className="accent-note">Quantized Inference</h3>
              <p className="text-sm">Serve fine-tuned open-weights models locally on physical workstation GPUs using optimized Ollama &amp; vLLM engines.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
              <h3 className="accent-note">Audited Placement</h3>
              <p className="text-sm">Graduates gain direct talent roster recognition and referral interviews across active incubated Indian startup developer squads.</p>
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
              1. Multi-Agent Systems Orchestration
            </h3>
            <p className="prose-sm text-muted">
              Design collaborative worker agent topologies utilizing hierarchical, sequential, and conversational supervisory routing patterns. Build robust stateful memory preservation loops.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Stateful cyclic graph definitions using modern LangGraph &amp; CrewAI</li>
              <li>&bull; Dynamic supervisor routing loops and autonomous task delegation</li>
              <li>&bull; Advanced context window compression, pruning &amp; summarization</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title">
              2. Tool Integration &amp; Function Calling Schemas
            </h3>
            <p className="prose-sm text-muted">
              Bind large language models deterministically to external production APIs, internal relational databases, and secure Docker execution sandboxes with rigid validation.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Writing strict input/output validation tool schemas using Pydantic</li>
              <li>&bull; Executing arbitrary shell scripts inside isolated container environments</li>
              <li>&bull; Bypassing LLM JSON parsing bugs via deterministic structured formatting</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Instructor E-E-A-T & Leadership Profile Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 03 — INSTRUCTOR LEADERSHIP &amp; PROVENANCE</div>
        <h2 className="section-title mb-2">Taught by Active AI Systems Architects</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We categorically reject passive academic lecturing by theorizing non-practitioners. Your training sprints are evaluated directly by senior software engineers who actively maintain open-source AI repositories and engineer commercial production systems across our venture studio.
        </p>
        
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <div className="flex align-center gap-2 mb-1">
              <span className="font-mono text-sm text-white font-bold">DBERT Technical Leadership Squad</span>
              <span className="badge badge-emerald text-xs">Active Industry Practitioners</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-4">
              Our instructors operate dual operational mandates: conducting weekly technical audits for incubated venture studio startups and leading our technical apprenticeship cohorts. You learn production code conventions from practitioners who battle active computational bottlenecks, GPU out-of-memory errors, and vector indexing latency daily.
            </p>
            <div className="stack-h gap-4">
              <Link href="/about/team" className="accent-link text-xs font-mono font-medium">Inspect Instructor Credentials &amp; Biographies &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Institutional Accreditation &amp; MSME Registrations &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Projects Section (Secondary BG) */}
      <div className="section-band-lg border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — CAPSTONE PRODUCTION PROJECTS</div>
          <h2 className="section-title mb-4">
            Production Projects You&apos;ll Ship to Your Git Repository
          </h2>
          <div className="bento-grid-2">
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 1 &middot; Production Systems</span>
              <h3 className={s.projectTitle}>Autonomous Multi-Agent Support Desk</h3>
              <p className="prose-sm text-muted">
                An industrial-strength automated helpdesk architecture using LangGraph to classify incoming customer support threads, query live PostgreSQL schemas, perform hybrid vector context lookups, and execute authenticated API remediation actions to resolve client tickets without human operator intervention.
              </p>
            </div>
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 2 &middot; Financial Intelligence</span>
              <h3 className={s.projectTitle}>Market Signal Extractor &amp; Parser</h3>
              <p className="prose-sm text-muted">
                An autonomous researcher worker team using CrewAI to monitor unstructured online corporate announcements, parse extensive financial PDFs, analyze sentiment divergence dynamics, and format rigorous JSON intelligence signals directly into PostgreSQL database analytical tables.
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
          We maintain absolute pricing transparency without hidden enrollment fees or inflated post-placement income share agreements. View our direct upfront tuition or structure flexible Zero-Cost EMI schedules through verified Indian financial institutions.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹35,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Includes full synchronous cohort sessions, GPU lab compute allocation, project review audits, and permanent credential validation registry listings.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Immediate lifetime access to recorded sprint architectures</li>
              <li>Dedicated weekly 1-on-1 code review feedback sessions</li>
              <li>Direct entry into our vetted startup engineering recruitment pipeline</li>
            </ul>
            <Link href="/learners/launchpad?domain=ai-agent-development" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹3,888 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Structured through authorized banking partnerships without processing charges or collateral demands for verified Indian engineering candidates.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Instant eligibility evaluation with minimal paperwork</li>
              <li>No upfront downpayment required to initiate technical lab access</li>
              <li>Full equivalence to upfront tuition benefits without discrimination</li>
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
          {["LangChain", "CrewAI", "LangGraph", "Ollama", "vLLM", "OpenAI API", "HuggingFace", "Python", "Docker", "Git", "PostgreSQL", "Pydantic"].map((tool, idx) => (
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
          <h2 className="card-title text-2xl font-bold text-white mb-2">Launch Your AI Agent Engineering Career</h2>
          <p className="page-lede text-sm text-muted max-w-xl mx-auto mb-6">
            Ready to design resilient multi-agent state machines, serve open-weights models locally, and deploy auditable software to your personal Git repository? Enrol in DBERT Industrial Training today.
          </p>
          <div className="stack-h gap-4 justify-center">
            <Link href="/learners/launchpad" className="btn btn-primary btn-lg">Choose Your Career Path &rarr;</Link>
            <Link href="/blog/paid-ai-internship-india-guide-2026" className="btn btn-outline btn-lg">Read Guide to Paid AI Internships</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

