import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import ConsultationForm from '@/components/ui/ConsultationForm';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import { Bot, Briefcase, TrendingUp, ShieldCheck, Database, Cpu } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/consultation');

export default function ConsultationPage() {
  const steps = [
    { number: '01', title: 'Discovery & Bottleneck Audit', description: 'We analyze your active operational workflows to identify high-yield AI opportunities, determine context window requirements, and calculate expected return on investment (ROI).' },
    { number: '02', title: 'System Architecture Blueprinting', description: 'We design custom blueprints showing data models, vector databases, API gateways, and model serving registries (evaluating local open-weights vs cloud-hosted structures).' },
    { number: '03', title: 'Pipeline Implementation & MLOps Setup', description: 'Our engineering team builds working integrations, deploys fine-tuned weights, configures containerized servers, and sets up GPU cluster monitoring dashboards.' }
  ];

  const faqs = [
    {
      question: 'How does an AI system architecture audit differ from high-level management consulting?',
      answer: 'High-level management consultancies typically deliver theoretical slide decks with generalized AI buzzwords without touching your repository. At DBERT Labs, our architectural audits are executed by veteran full-stack AI engineers and researchers. We inspect your actual Git codebases, database indexing structures, latency logs, and compute invoices to deliver deterministic engineering schematics, precise parameter calculations, and containerized proof-of-concept pull requests.'
    },
    {
      question: 'What is the standard duration and commercial fee structure for an engineering consultation sprint?',
      answer: 'Our foundational Technical Architecture & Bottleneck Audit is a structured 10-day sprint priced at a flat commercial fee of ₹35,000. For comprehensive end-to-end system implementations—such as building enterprise RAG retrieval engines or deploying local open-weights container arrays—we formulate transparent milestone project proposals or transition eligible startups into our services-against-equity co-development track.'
    },
    {
      question: 'How do you determine whether to recommend private local model hosting over external public APIs?',
      answer: 'We analyze three mathematical variables: daily concurrent query volume, token generation latency thresholds, and regulatory data privacy obligations. If your application processes confidential medical, legal, or proprietary enterprise data, or if your projected monthly per-token cloud billing exceeds bare-metal GPU rental costs, we design airtight Virtual Private Cloud (VPC) deployments using vLLM and Ollama serving runtimes.'
    },
    {
      question: 'What intellectual property agreements and confidentiality protocols govern consultation engagements?',
      answer: 'Prior to inspecting any proprietary workflows or database log archives, DBERT Labs executes reciprocal bilateral Non-Disclosure Agreements (NDAs). Upon engagement completion, 100% of all authored architecture schematics, algorithmic data pipeline diagrams, fine-tuned weight weights, and custom code modules belong exclusively to your business entity.'
    },
    {
      question: 'Can your consultation team oversee the implementation of MLOps observability dashboards?',
      answer: 'Yes. Every enterprise architecture blueprint includes complete MLOps infrastructure design. We integrate Prometheus and Grafana telemetry monitoring directly into your model serving pipelines—tracking graphics memory (VRAM) consumption, time-to-first-token (TTFT), inference throughput velocities, and semantic drift in real time.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT AI System Architecture & Engineering Consultation',
        serviceType: 'AI Workflow Audit, RAG System Architecture Blueprinting, Local LLM Deployment Consultation, MLOps Design',
        description: 'Carrier-grade artificial intelligence consulting: audit business workflows, engineer private RAG pipeline schematics, optimize GPU infrastructure, and design resilient MLOps telemetry.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          price: '35000',
          priceCurrency: 'INR',
          description: '10-day foundational technical architecture and bottleneck audit sprint or customized milestone retainers'
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
          § 01 — AI ENGINEERING CONSULTATION <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Architect Your AI-Powered Future &mdash; Deterministically
        </h1>
        <p className="lede-wide">
          Move from operational conjecture to hardened production deployment. We audit enterprise business workflows, engineer custom RAG pipeline schematics, provision cost-optimized GPU servers, and deploy autonomous MLOps observatories.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Operating Private Server Laboratories &amp; Studio MVPs</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we abide by a non-negotiable engineering tenet: <strong>we design, stress-test, and run AI architectures on our own physical server clusters before advising enterprises</strong>. Our AI Consultation practice evolved naturally from designing our proprietary product line (including DBERT Chat and Document AI) and deploying bare-metal hardware hosting arrays across our industrial training network.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">Why Technical Precision Matters</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              We frequently observed mid-sized organizations burning millions of rupees deploying fragile API chat wrappers that collapsed under production user volume or violated consumer data compliance laws. By bridging real industrial research to corporate strategy, our engineering partners help you bypass costly experimental cycles—equipping your IT architecture with battle-tested open-weights serving runtimes and zero-trust data firewalls.
            </p>
            <div className="stack-h gap-4 mt-4 flex flex-wrap gap-4">
              <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs font-mono font-medium">Inspect Our Bare-Metal Hardware Infrastructure &rarr;</Link>
              <Link href="/ai-solutions/products" className="accent-link text-xs font-mono font-medium">Explore Our Battle-Tested Commercial AI Suite &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid (Secondary BG) */}
      <div className="section-band border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — ARCHITECTURAL BENCHMARKS</div>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
              <h3 className="accent-note">Custom Schemas</h3>
              <p className="text-sm">Tailored RESTful API structures and structured JSON extraction rules mapped directly to your historical database log archives.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Bot aria-hidden="true" /></span>
              <h3 className="accent-note">Model Selection</h3>
              <p className="text-sm">Mathematical evaluation of open-weights local models (Llama-3, Qwen) versus cloud commercial APIs to balance unit cost and latency.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><TrendingUp aria-hidden="true" /></span>
              <h3 className="accent-note">MLOps Observability</h3>
              <p className="text-sm">Continuous Prometheus and Grafana dashboards monitoring GPU temperatures, VRAM capacities, and query latency distributions.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Core Consulting Pillars (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — CONSULTING SCOPE &amp; DELIVERABLES</div>
        <h2 className="section-title mb-4">
          Our Core Engineering Workstreams
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. Discovery &amp; Bottleneck Audit
            </h4>
            <p className="prose-sm text-muted">
              We dissect your active operational workflows to pinpoint high-yield artificial intelligence automation opportunities and compile rigorous financial ROI projections.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Auditing manual human text &amp; document redundancies</li>
              <li>&bull; Calculating context window memory parameter bounds</li>
              <li>&bull; Delivering comprehensive unit economic savings forecasts</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. System Architecture Blueprint
            </h4>
            <p className="prose-sm text-muted">
              We draft definitive schematics detailing semantic vector databases, reverse proxy rate limits, isolated subnet firewalls, and model serving container topologies.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Designing PostgreSQL pgvector RAG semantic indexing</li>
              <li>&bull; Zero-trust AWS/RunPod Virtual Private Cloud boundaries</li>
              <li>&bull; Selecting between Ollama, vLLM &amp; commercial inference</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. Pipeline Execution &amp; MLOps
            </h4>
            <p className="prose-sm text-muted">
              Our studio engineering squads build production integrations, configure containerized bare-metal GPU nodes, and execute simulated concurrent high-load tests.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Deploying stateful multi-agent networks via CrewAI</li>
              <li>&bull; Dockerized localized serving engine registries (Ollama)</li>
              <li>&bull; Automated Grafana VRAM and token velocity alerting</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Security Rigor & Defense Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — DATA SECURITY &amp; RISK MITIGATION</div>
        <h2 className="section-title mb-2">Hardening Enterprise AI Implementations</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          An unguided artificial intelligence integration can expose internal corporate networks to prompt injection vulnerabilities, data leakage through external model training, and catastrophic cloud billing loops. We build impregnable technical defenses.
        </p>
        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Zero-Leakage Model Serving</h4>
            <p className="text-xs text-muted">
              We design air-gapped localized model inference architectures where sensitive business data never exits your Virtual Private Cloud. Open-weights models process documents completely inside private RAM, protecting corporate attorney-client privileges and customer confidentiality.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Ingress Rate-Limiting &amp; Proxy Shields</h4>
            <p className="text-xs text-muted">
              All client request endpoints reside behind containerized Nginx reverse proxies utilizing token bucket algorithms and SSL mutual TLS termination—preventing automated Distributed Denial-of-Service (DDoS) exploitation and unauthorized token consumption attacks.
            </p>
          </div>
        </div>
      </div>

      {/* Commercial Consulting Packages */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — CONSULTATION RETAINERS &amp; TRACKS</div>
        <h2 className="section-title mb-2">Transparent Commercial Consulting Tiers</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Select between targeted technical discovery sprints, end-to-end implementation retainers, or transition into dilution-free technical co-development.
        </p>
        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">High Demand</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase font-bold">Architecture Audit Sprint</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹35,000 <span className="text-xs text-muted font-normal">flat fee</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive 10-day engineering sprint to inspect your codebase, audit cloud compute costs, and draft definitive RAG schematics.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Complete operational bottleneck &amp; ROI report</li>
                <li>Database RAG indexing &amp; VPC security design</li>
                <li>Actionable Docker and model selection roadmap</li>
              </ul>
            </div>
            <a href="#booking-form" className="btn btn-primary w-full mt-4">Book Audit Sprint &rarr;</a>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase font-bold">Full Implementation Suite</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹1,50,000+ <span className="text-xs text-muted font-normal">custom</span></div>
              <p className="text-xs text-muted mt-2">End-to-end software engineering delivery where our senior AI squad stands up high-throughput bare-metal containers and MLOps observatories.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>AWS/RunPod multi-node GPU cluster setup</li>
                <li>Ollama &amp; vLLM localized production serving</li>
                <li>Prometheus MLOps telemetry alerting dashboard</li>
              </ul>
            </div>
            <a href="#booking-form" className="btn btn-outline w-full mt-4">Inquire Full Suite &rarr;</a>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase font-bold">Venture Studio Track</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Equity Bundling</div>
              <p className="text-xs text-muted mt-2">Early-stage AI startup pioneers can access full technical consulting and software execution under our services-against-equity exchange.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>0% upfront cash development or consulting fees</li>
                <li>90-day comprehensive production MVP sprint</li>
                <li>Bundled micro-grants for initial GPU hosting</li>
              </ul>
            </div>
            <Link href="/startups/services/technical" className="btn btn-outline w-full mt-4">Explore Venture Studio &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 07 — STRATEGY EXECUTION ROADMAP</div>
          <h2 className="subsection-title mb-4">
            Our Strategy Execution Process
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* FAQ Accordion Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — CONSULTATION KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED AI SYSTEMS &amp; ACADEMY TRACKS</div>
        <h2 className="section-title mb-4">Explore Complementary Capabilities</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Custom LLM Training</h4>
            <p className="text-xs text-muted mb-3">Audit our 5-stage fine-tuning lifecycle and explore custom neural network weights compiled for enterprise domains.</p>
            <Link href="/ai-solutions/llm-training" className="accent-link text-xs">View Custom LLM Suite &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Private Hardware Hosting</h4>
            <p className="text-xs text-muted mb-3">Inspect our physical bare-metal hardware server arrays designed for sovereign AI operational secrecy.</p>
            <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs">View Private Hosting &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Cloud Infrastructure Service</h4>
            <p className="text-xs text-muted mb-3">Deploy cost-optimized AWS and RunPod Virtual Private Clouds equipped with containerized pgvector clusters.</p>
            <Link href="/startups/services/infrastructure" className="accent-link text-xs">View Infrastructure Service &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Primary BG) */}
      <div className="container pad-block border-t border-line" id="booking-form">
        <div className="doclabel mb-4">§ 10 — INITIATE CONSULTATION BOOKING</div>
        <ConsultationForm />
      </div>
    </div>
  );
}

