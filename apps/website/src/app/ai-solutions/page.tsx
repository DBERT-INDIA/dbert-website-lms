import React from 'react';
import Link from 'next/link';
import StudioConsole, { type FeedLine } from '@/components/ui/StudioConsole';
import FactTicker from '@/components/ui/FactTicker';
import AudienceDoors, { type Door } from '@/components/ui/AudienceDoors';
import FAQAccordion from '@/components/ui/FAQAccordion';
import HandNote from '@/components/ui/HandNote';
import TrackedLink from '@/components/ui/TrackedLink';
import { pageMetadata } from '@/lib/seo';
import s from './ai-solutions.module.css';
import { Bot, Briefcase, Monitor, ShieldCheck, Cpu } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions');

export default function AISolutionsLandingPage() {
  const faqs = [
    {
      question: 'Can your SaaS tools and local LLM architectures run entirely inside our corporate VPC?',
      answer: 'Yes. Every enterprise solution built by DBERT—including DBERT Chat and Document AI—is specifically designed for sovereign containerized deployment within your private AWS, GCP, Azure, or on-premises physical datacenter infrastructure. No sensitive proprietary payload is ever routed to external third-party servers.'
    },
    {
      question: 'How do custom fine-tuned weights compare to generic commercial LLM APIs?',
      answer: 'Generic commercial models charge recurrent token fees and introduce unpredictable network latency while carrying significant third-party data privacy exposure. Our fine-tuned local models (such as DBERT_AI) are optimized specifically on your domain data, delivering faster deterministic JSON parsing at zero recurring API token expense.'
    },
    {
      question: 'What is the "we run it before we sell it" engineering thesis?',
      answer: 'Unlike traditional software vendors who assemble speculative software wrappers, every enterprise product in our catalog originated as an internal tool built to solve real operational scale challenges across our startup venture incubator and 1,500+ developer training ecosystem before being commercialized.'
    },
    {
      question: 'What is your typical enterprise implementation and integration timeline?',
      answer: 'A standard deployment sprint—from database architectural audit and VPC container ingestion to custom IAM role provisioning and load testing—typically requires between 2 to 6 weeks, overseen directly by our senior active engineering leads.'
    },
    {
      question: 'How do you guarantee Intellectual Property (IP) and security compliance?',
      answer: 'DBERT operates under strict statutory MSME Government of India compliance standards. All fine-tuned parameter weights, custom embeddings, and application codebases remain your legally audited corporate property under explicit end-to-end encryption agreements.'
    },
    {
      question: 'Do you offer ongoing operational MLOps and infrastructure maintenance?',
      answer: 'Yes. Through our Strategic AI Consultation and continuous DevOps packages, our engineering team manages live cluster auto-scaling, model drift evaluation, periodic parameter retraining, and security vulnerability patching.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Enterprise AI Solutions, SaaS & Custom LLM Fine-Tuning',
        description: 'Production-ready sovereign enterprise AI architectures in India: self-hosted LLM chat consoles, high-throughput document OCR parsing pipelines, credential verification APIs, and private LLM cluster hosting.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT (Digital Blinc Education Research And Technology)',
          url: 'https://dbert.online'
        },
        areaServed: {
          '@type': 'Country',
          name: 'India'
        },
        serviceType: 'Enterprise Artificial Intelligence & Sovereign Cloud Deployment',
        url: 'https://dbert.online/ai-solutions'
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

  const enterpriseTelemetryFeed: FeedLine[] = [
    {
      time: '11:02:14',
      tag: 'infer',
      message: 'dbert-chat vLLM cluster',
      detail: '· 42ms p99 token latency',
    },
    {
      time: '11:04:30',
      tag: 'parse',
      message: 'document-ai parsed 1,420 invoice PDFs',
      detail: '· 99.4% schema accuracy',
    },
    {
      time: '11:07:05',
      tag: 'vpc',
      message: 'air-gapped AWS GovCloud cluster deployed',
      detail: '· 0 external API calls',
    },
    {
      time: '11:09:50',
      tag: 'verify',
      message: 'credential API answered 82 verification queries',
      detail: '· SLA 18ms',
    },
    {
      time: '11:12:22',
      tag: 'deploy',
      message: 'custom fine-tuned LLaMA-3.3 70B quantized for Indian banking',
      detail: '· 4x lower vCPU cost',
    },
  ];

  const enterpriseFacts = [
    '100% VPC air-gapped deployment',
    'zero third-party API token dependencies or recurring egress fees',
    'deterministic JSON schema outputs with strict Pydantic validation',
    'complete corporate ownership of fine-tuned weights & embeddings',
    '99.98% production uptime SLA guaranteed in enterprise MSAs',
    'Delhi NCR dedicated systems architects & on-site integration support',
    'audited compliance with RBI data localisation & MeitY standards',
  ];

  const enterpriseDoors: Door[] = [
    {
      kind: 'enterprise',
      who: 'Product 01 · Conversational AI',
      title: 'DBERT Chat Console',
      description: 'Private, self-hosted LLM chat interface with enterprise RAG indexing and granular token budgeting.',
      ctaLabel: 'Inspect Chat Specs',
      href: '/ai-solutions/products/dbert-chat',
    },
    {
      kind: 'founder',
      who: 'Product 02 · OCR & Extraction',
      title: 'Document AI Pipeline',
      description: 'High-throughput document extraction processing thousands of unstructured PDFs directly into relational schemas.',
      ctaLabel: 'Inspect Pipeline',
      href: '/ai-solutions/products/document-ai',
    },
    {
      kind: 'learner',
      who: 'Product 03 · Enterprise Talent',
      title: 'Hiring Automation Suite',
      description: 'Resume parsing, structured scoring, and automated candidate routing built for engineering recruitment.',
      ctaLabel: 'View Hiring Suite',
      href: '/ai-solutions/products/hiring-automation-suite',
    },
  ];

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      {/* ══════════ SECTION 1: HERO (2-COLUMN GRID) ══════════ */}
      <section className="section-subpage-hero">
        <div className="wrap subpage-hero-grid">
          <div>
            <div className="doclabel">
              § 01 — ENTERPRISE AI SOLUTIONS <span className="rev">rev: 2026.2</span>
            </div>
            <h1 className="relative inline-block">
              Production-Grade AI That Powers Sovereign Business Scale
              <HandNote className="absolute -right-12 -top-6 text-lg hidden md:block" tone="blue">
                zero third-party token leaks ✎
              </HandNote>
            </h1>
            <p className="intro-copy">
              From experimental lab prototypes to deterministic enterprise deployment. We engineer custom-tuned model parameter weights, zero-leakage document ingestion pipelines, and resilient VPC hosting architectures that transform industrial operations across India.
            </p>
            <div className="stack-h gap-3 mt-6 flex-wrap">
              <Link href="/ai-solutions/consultation" className="btn btn-primary">
                Schedule VPC Architecture Audit →
              </Link>
              <Link href="#products" className="btn btn-outline">
                Explore Sovereign SaaS Products
              </Link>
            </div>
          </div>

          <div>
            <StudioConsole
              title="dbert-vpc · sovereign inference cluster telemetry"
              lines={enterpriseTelemetryFeed}
              footLeft="model: dbert-ai-7b · vLLM backend"
              footRight="● 99.98% uptime SLA"
              note={
                <HandNote tone="blue">
                  zero third-party token leaks ✎
                </HandNote>
              }
            />
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 2: FULL-BLEED AMBIENT FACT TICKER ══════════ */}
      <div className="section-ticker-ribbon">
        <FactTicker facts={enterpriseFacts} />
      </div>

      {/* ══════════ SECTION 3: ENTERPRISE SAAS GATEWAY DOORS ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 02 — BROWSE PRODUCTION SAAS SUITES</div>
            <h2>Sovereign Enterprise Products</h2>
            <p>Pre-built, auditable SaaS modules ready for private VPC deployment with zero third-party API dependencies.</p>
          </div>
          <AudienceDoors doors={enterpriseDoors} />
        </div>
      </section>

      {/* ══════════ SECTION 4: PRODUCTION GAP & SOVEREIGN VPC BLUEPRINT (BAND) ══════════ */}
      <section className="subpage-section band" id="products">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 03 — THE PRODUCTION GAP &amp; SOVEREIGN ARCHITECTURE</div>
            <h2>Moving Beyond Generic API Wrappers</h2>
            <p>
              Most commercial AI initiatives hit a hard operational ceiling when scaling: unpredictable per-token pricing, network latency spikes, and severe third-party compliance exposure (RBI, MeitY, GDPR).
            </p>
          </div>

          {/* Sovereign VPC Topology Blueprint */}
          <div className={s.vpcTopology}>
            <div className={s.vpcHeader}>
              <span className="font-mono text-xs text-text font-bold">SOVEREIGN VPC TOPOLOGY // ZERO EXTERNAL EGRESS</span>
              <span className={s.vpcTag}>[RBI / MEITY COMPLIANT · 0.00 KB LEAKAGE]</span>
            </div>
            <div className={s.vpcFlow}>
              <div className={s.vpcNode}>
                <div className={s.vpcNodeTitle}>1. Ingestion &amp; Sanitization</div>
                <p className={s.vpcNodeDesc}>
                  Unstructured contracts, PDFs &amp; database records pass through internal parsing. PII is scrubbed before embeddings.
                </p>
              </div>
              <div className={s.vpcNode}>
                <div className={s.vpcNodeTitle}>2. Vector Index &amp; HNSW</div>
                <p className={s.vpcNodeDesc}>
                  PostgreSQL pgvector / Milvus cluster indexes embeddings locally with sub-10ms similarity queries behind internal firewall.
                </p>
              </div>
              <div className={s.vpcNode}>
                <div className={s.vpcNodeTitle}>3. Local Model Inference</div>
                <p className={s.vpcNodeDesc}>
                  DBERT_AI &amp; open-weight LLMs served via vLLM / Ollama clusters on your private GPUs. Zero external API calls.
                </p>
              </div>
            </div>
          </div>

          {/* Token Economics Deck */}
          <div className={`${s.economicsDeck} my-10`}>
            <div className={`${s.econCard} ${s.econCardCloud}`}>
              <div className={s.econTitle}>Third-Party Cloud APIs</div>
              <div className={`${s.econFigure} ${s.cloudFig}`}>₹12.4L+ / mo</div>
              <p className="text-xs text-muted">Estimated at 10M tokens/day on commercial proprietary APIs</p>
              <ul className={s.econList}>
                <li>✖ Recurring per-token pricing escalations</li>
                <li>✖ High latency spikes during peak commercial hours</li>
                <li>✖ Data egress to external commercial servers</li>
                <li>✖ Zero ownership of underlying intelligence</li>
              </ul>
            </div>

            <div className={`${s.econCard} ${s.econCardSovereign}`}>
              <div className={s.econTitle}>DBERT Sovereign VPC Cluster</div>
              <div className={`${s.econFigure} ${s.sovereignFig}`}>₹0 / token</div>
              <p className="text-xs text-muted">Fixed GPU cluster hosting with unlimited deterministic inferences</p>
              <ul className={s.econList}>
                <li>✔ 100% fixed compute cost regardless of query volume</li>
                <li>✔ Sub-50ms deterministic local inference speeds</li>
                <li>✔ Complete data sovereignty (0 bytes leave VPC)</li>
                <li>✔ Perpetual ownership of fine-tuned model weights</li>
              </ul>
            </div>
          </div>

          <div className="card card-lift disclosure my-6">
            <h3 className="card-heading-lg mb-2">Why Our Tools Are Production-Tested</h3>
            <p className="prose-sm text-muted">
              Every tool we offer—from our Document AI OCR parser to our Certificate Verification API—was created to solve operational bottlenecks within our own venture studio and engineering cohorts before being packaged for enterprise use.
            </p>
          </div>
          <div className="stack-h gap-4 mt-6 flex-wrap">
            <Link href="/ai-solutions/llm-training/private-hosting" className="btn btn-outline btn-sm">Explore Private VPC Hosting Specs &rarr;</Link>
            <Link href="/ai-solutions/products" className="btn btn-outline btn-sm">Browse All 5 Enterprise Products &rarr;</Link>
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 5: CAPABILITY PILLARS ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 04 — CAPABILITY PILLARS</div>
            <h2>How We Partner With Engineering Teams</h2>
            <p>Direct architectural engagement from lead systems builders.</p>
          </div>
          <div className={`${s.capabilityGrid} stagger-grid`}>
            
            <div className={`card card-lift ${s.capabilityCard}`}>
              <div>
                <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
                <h3 className={s.capabilityTitle}>Strategic AI Consultation</h3>
                <p className="body-copy">
                  Architecture audits, vector retrieval optimization, and structured roadmap planning. We help technical teams design realistic AI pipelines without over-engineering.
                </p>
              </div>
              <Link href="/ai-solutions/consultation" className="accent-label">Explore Consultation &rarr;</Link>
            </div>

            <div className={`card card-lift ${s.capabilityCard}`}>
              <div>
                <span className="icon-chip"><Bot aria-hidden="true" /></span>
                <h3 className={s.capabilityTitle}>Custom LLM Fine-Tuning</h3>
                <p className="body-copy">
                  Domain-specific model tuning using curated datasets, LoRA adapters, and localized inference servers (Ollama / vLLM) that operate entirely within your firewall.
                </p>
              </div>
              <Link href="/ai-solutions/llm-training" className="accent-label">Explore Fine-Tuning Pipelines &rarr;</Link>
            </div>

            <div className={`card card-lift ${s.capabilityCard}`}>
              <div>
                <span className="icon-chip"><Monitor aria-hidden="true" /></span>
                <h3 className={s.capabilityTitle}>Deployable SaaS Products</h3>
                <p className="body-copy">
                  Pre-built systems ready for direct integration: internal document parsing, enterprise RAG knowledge chat, verifiable credentials, and intern workflow portals.
                </p>
              </div>
              <Link href="/ai-solutions/products" className="accent-label">Explore SaaS Catalog &rarr;</Link>
            </div>

          </div>
        </div>
      </section>

      {/* ══════════ SECTION 6: OPEN-WEIGHTS DEPLOYMENT (BAND-ALT) ══════════ */}
      <section className="subpage-section band-alt">
        <div className="wrap">
          <div className="card callout">
            <div className="doclabel mb-1">§ 05 — OPEN-WEIGHTS DEPLOYMENT</div>
            <h2 className="card-title">The DBERT_AI Sovereign Open-Weights Model</h2>
            <p className="page-lede mb-4">
              We publish custom fine-tuned parameter weights directly onto the verified global Ollama model registry. Download, run local low-latency inference queries, and host private customized models within your corporate datacenter to achieve total enterprise data privacy while eliminating ongoing API token expenditure.
            </p>
            <div className="stack-h gap-4 align-center justify-center">
              <Link href="/ai-solutions/llm-training/dbert-ai" className="btn btn-primary">Inspect Model Specifications</Link>
              <a
                href="https://ollama.com/DBERT/DBERT_AI"
                target="_blank"
                rel="noopener noreferrer"
                className="font-mono text-xs accent-link"
              >
                ollama run DBERT/DBERT_AI &rarr;
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 7: ENTERPRISE FAQ ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub text-center">
            <div className="doclabel justify-center">§ 06 — ENTERPRISE KNOWLEDGE BASE</div>
            <h2>Enterprise Architecture &amp; Security FAQ</h2>
            <p className="mx-auto">Detailed architectural clarifications on VPC hosting, compliance certifications, and air-gapped deployments.</p>
          </div>
          <div className="measure">
            <FAQAccordion items={faqs} />
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 8: BOTTOM CTA PANEL (BAND) ══════════ */}
      <section className="subpage-section band">
        <div className="wrap">
          <div className="card callout-plain text-center">
            <h3 className="card-heading-lg mb-2">Ready to Transition from Prototype to Sovereign AI Production?</h3>
            <p className="prose-sm text-muted mb-4 max-w-xl mx-auto">
              Engage directly with our active systems architects for an objective infrastructure feasibility audit or customized VPC software demonstration.
            </p>
            <div className="stack-h gap-4 justify-center">
              <TrackedLink
                href="/ai-solutions/consultation"
                eventName="consultation_click"
                eventParams={{ location: 'ai_solutions_bottom', target: 'book_consultation' }}
                className="btn btn-primary"
              >
                Book Technical Consultation
              </TrackedLink>
              <Link href="/startups" className="btn btn-outline">View Startup Incubation Model</Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

