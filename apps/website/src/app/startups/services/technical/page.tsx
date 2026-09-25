import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import { Bot, Laptop, Zap, Shield, Database, Cpu, Workflow } from 'lucide-react';
import s from '../../startups.module.css';

export const metadata = pageMetadata('/startups/services/technical');

export default function TechnicalServicePage() {
  const steps = [
    { number: '01', title: 'Codebase Audit & Diagnostics', description: 'We inspect your repositories, database schemas, API routes, and compute budgets to locate latency bottlenecks and structural anti-patterns.' },
    { number: '02', title: 'Pipeline Architecture Blueprint', description: 'We draft custom engineering blueprints showing deterministic model mappings, vector index structures, and containerized hosting endpoints.' },
    { number: '03', title: 'Sprint Execution & Code Commits', description: 'Our venture engineering squad enters live two-week development sprints with you, committing tested production logic directly to your main git branch.' }
  ];

  const faqs = [
    {
      question: 'Do your engineers simply act as consultants or do they actively write and commit code?',
      answer: 'We are hands-on co-developers, not passive advisors. When you enter DBERT Technical Incubation, our senior software engineers and AI system specialists commit fully tested code directly into your GitHub or GitLab repository on a daily sprint cycle.'
    },
    {
      question: 'How do you prevent vendor lock-in and excessive cloud token escalation costs?',
      answer: 'We deploy open-weights models (such as Llama-3, Mistral, and Qwen) via localized inference runtimes like vLLM and Ollama running on private bare-metal or VPC instances. This insulates your product from third-party commercial API price hikes and arbitrary rate limiting.'
    },
    {
      question: 'What is your timeline for building a high-throughput Retrieval-Augmented Generation (RAG) pipeline?',
      answer: 'A hardened, production-ready RAG engine utilizing PostgreSQL pgvector indexing, semantic caching, and hybrid re-ranking typically transitions from initial architectural blueprint to live deployment within 14 to 21 operational days.'
    },
    {
      question: 'How does the technical squad collaborate with our existing in-house junior developers or CTO?',
      answer: 'We act as an integrated engineering multiplier. We set up automated linting pipelines, conduct rigorous Pull Request (PR) architectural reviews, and lead paired programming sprints to upskill your existing team while maintaining strict release velocity.'
    },
    {
      question: 'Who owns the underlying intellectual property (IP) and software repositories developed during incubation?',
      answer: '100% of all authored source code, database migrations, custom fine-tuned weights, and architectural documentation are exclusively assigned to and owned by your corporate entity upon milestone execution. DBERT retains zero proprietary claim over your core business IP.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Technical Architecture & AI MVP Co-Development',
        serviceType: 'AI Systems Engineering, Full-Stack Software Co-Development, RAG Architecture',
        description: 'Hands-on AI engineering squad that designs scalable system architectures, optimizes vector RAG databases, and commits production-ready code directly to startup repositories.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Venture Studio Technical Incubation',
          price: '45000',
          priceCurrency: 'INR',
          description: 'Monthly dedicated engineering co-development retainer or 2-6% equity incubation agreement',
          url: 'https://dbert.online/startups/services/technical'
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

      {/* Hero Header Section & What It Is */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — VENTURE TECHNICAL SERVICE <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Engineer Production-Grade AI Systems &amp; MVP Pipelines
        </h1>
        <p className="lede-wide">
          Avoid crippling technical debt and fragile API wrappers. We embed a dedicated team of DBERT venture studio engineers directly into your technical leadership, designing deterministic state machines, high-throughput pgvector search indices, and real-time streaming architectures.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Incubating Real Indian Tech Pioneers</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we enforce a definitive operational standard: <strong>we construct and run our technology in production before recommending it to founders</strong>. Our Technical Architecture service was born directly from our internal venture studio operations, where we observed brilliant Indian founders burning months of capital rebuilding fragile prototype chatbots that collapsed under production user load.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              Standard outsourcing agencies build brittle prototypes designed purely for investor demos, leaving founders with maintainability nightmares. We restructured our incubation model to provide battle-tested engineering squads that utilize our proprietary internal platforms—including Document AI and Private LLM Hosting—to construct resilient, carrier-grade software systems capable of handling hundreds of thousands of daily corporate transactions from day one.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs font-mono font-medium">Explore Private LLM Hosting Hardware &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Our MSME Corporate Credentials &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — PERFORMANCE &amp; EXECUTION BENCHMARKS</div>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Zap aria-hidden="true" /></span>
              <h3 className="accent-note">Sub-100ms Latency</h3>
              <p className="text-sm">Optimized semantic vector search query performance utilizing native PostgreSQL pgvector HNSW indexing structures.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Bot aria-hidden="true" /></span>
              <h3 className="accent-note">Ollama Local Serving</h3>
              <p className="text-sm">Bypass unencrypted public commercial LLM endpoints to ensure total mathematical customer data confidentiality.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Laptop aria-hidden="true" /></span>
              <h3 className="accent-note">Live Code Commits</h3>
              <p className="text-sm">Active senior full-stack engineers embedded in your daily sprint cycles writing production feature logic.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Architectural Deliverables (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — SYSTEM ARCHITECTURE DELIVERABLES</div>
        <h2 className="section-title mb-4">
          What Your Architecture Looks Like After DBERT
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. Framework &amp; Agent Design
            </h4>
            <p className="prose-sm text-muted">
              We construct clean state-machine communication patterns for your agent workflows, replacing non-deterministic prompt scripts with reliable type-safe orchestrators.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; LangGraph, CrewAI &amp; custom agent configurations</li>
              <li>&bull; Pydantic &amp; Zod strict structured output parsing</li>
              <li>&bull; Semantic prompt context token caching layers</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. Vector Index Optimization
            </h4>
            <p className="prose-sm text-muted">
              Guarantee your Retrieval-Augmented Generation (RAG) pipelines retrieve precise contextual documents in milliseconds under concurrent enterprise traffic.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Native PostgreSQL pgvector parameter adjustments</li>
              <li>&bull; Recursive character &amp; semantic overlapping chunking</li>
              <li>&bull; Hybrid BM25 &amp; cosine distance reranking pipelines</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. MLOps &amp; CI/CD Pipelines
            </h4>
            <p className="prose-sm text-muted">
              Ship updates safely without breaking production. We provision GPU hosting infrastructure, harden container environments, and execute simulated stress testing.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; AWS EC2, GCP &amp; RunPod bare-metal GPU clustering</li>
              <li>&bull; Rigid JWT bearer token &amp; CORS authentication</li>
              <li>&bull; Automated multi-point integration test suites</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Risk Mitigation */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY &amp; TECHNICAL RISK MITIGATION</div>
        <h2 className="section-title mb-2">Eliminating Single Point of Failures</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Early-stage technical decisions can permanently cripple a startup&apos;s enterprise valuation during future institutional funding rounds. We implement strict defense-in-depth protocols.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Zero Public Training Vulnerability</h4>
            <p className="text-xs text-muted">
              By routing analytical pipelines through hardened on-premise Ollama or vLLM container endpoints, we guarantee that zero corporate customer queries or proprietary databases ever inadvertently feed commercial third-party training datasets.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Automated Resilience Testing</h4>
            <p className="text-xs text-muted">
              We subject your backend API microservices and database read/write replicas to automated simulated load bursts—ensuring graceful degradation, predictive throttling, and zero memory exhaustion during abrupt traffic surges.
            </p>
          </div>
        </div>
      </div>

      {/* Pricing & Incubation Engagement Structures */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — INCUBATION &amp; COMMERCIAL STRUCTURES</div>
        <h2 className="section-title mb-2">Transparent Technical Incubation Models</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Select between equity-driven venture studio incubation designed to conserve early runway or dedicated fee-for-service technical engineering sprints.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Equity Incubation</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">2% &ndash; 6% <span className="text-xs text-muted font-normal">Equity</span></div>
              <p className="text-xs text-muted mt-2">Designed for pre-seed Indian AI startups requiring full technical co-development without draining seed capital reserves.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Dedicated senior full-stack AI engineering squad</li>
                <li>90-day comprehensive MVP production launch</li>
                <li>100% intellectual property (IP) assignment</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-outline w-full mt-4">Apply For Incubation &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Fastest Velocity</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Sprint Co-Development</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹95,000 <span className="text-xs text-muted font-normal">/ sprint</span></div>
              <p className="text-xs text-muted mt-2">Two-week intensive code execution sprints for established venture teams building specialized RAG or LLM integrations.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Dedicated paired engineering &amp; PR reviews</li>
                <li>PostgreSQL pgvector RAG database setup</li>
                <li>Direct GitHub code commit velocity</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-primary w-full mt-4">Schedule Sprint &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Architecture Audit</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹45,000 <span className="text-xs text-muted font-normal">flat fee</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive 7-day technical evaluation, database schema review, and latency remediation blueprint.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Complete repository AST &amp; schema audit</li>
                <li>Cloud token expenditure optimization guide</li>
                <li>Actionable engineering restructuring roadmap</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Book Tech Audit &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 07 — ONBOARDING WORKFLOW</div>
          <h2 className="subsection-title mb-4">
            Our Technical Onboarding Process
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — TECHNICAL KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED INCUBATION SERVICES &amp; PRODUCTS</div>
        <h2 className="section-title mb-4">Explore Complementary Venture Services</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Cloud &amp; AI Infrastructure</h4>
            <p className="text-xs text-muted mb-3">Provision private GPU clusters, local Ollama runtime registries, and secure virtual private network configurations.</p>
            <Link href="/startups/services/infrastructure" className="accent-link text-xs">View Infrastructure Service &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Hiring &amp; Team Support</h4>
            <p className="text-xs text-muted mb-3">Access DBERT Labs directory of 1,500+ vetted AI engineering fellows trained on real production codebases.</p>
            <Link href="/startups/services/hiring" className="accent-link text-xs">View Hiring Support &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">DBERT Chat Product</h4>
            <p className="text-xs text-muted mb-3">Deploy air-gapped conversational agent interfaces running over your proprietary operational database registers.</p>
            <Link href="/ai-solutions/products/dbert-chat" className="accent-link text-xs">View DBERT Chat &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Primary BG) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 10 — INITIATE CO-DEVELOPMENT</div>
        <div className="bento-card callout">
          <h2 className="card-title">Ship Faster with Battle-Tested Architecture</h2>
          <p className="page-lede">
            Ready to integrate advanced agent pipelines, configure optimized vector indices, and eliminate code inefficiencies? Apply for DBERT Technical Incubation today.
          </p>
          <Link href="/startups/register" className="btn btn-primary btn-lg mt-4">Register Your Startup &rarr;</Link>
        </div>
      </div>
    </div>
  );
}

