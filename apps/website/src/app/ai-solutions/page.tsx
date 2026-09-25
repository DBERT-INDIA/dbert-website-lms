import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from './ai-solutions.module.css';
import { Bot, Briefcase, Monitor } from 'lucide-react';

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

  return (
    <div className="glow-wrapper">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <div className="glow-spot"></div>

        <header className="page-hero">
          <div className="doclabel">
            § 01 — ENTERPRISE AI SOLUTIONS <span className="rev">rev: 2026.2</span>
          </div>
          <h1 className="page-title-sm">
            Production-Grade AI That Powers Sovereign Business Scale
          </h1>
          <p className="page-intro">
            From experimental lab prototypes to deterministic enterprise deployment. We engineer custom-tuned model parameter weights, zero-leakage document ingestion pipelines, and resilient VPC hosting architectures that transform industrial operations across India.
          </p>
        </header>

        <section className="page-band alt">
          <div className="doclabel mb-2">§ 02 — THE PRODUCTION GAP</div>
          <h2 className="section-heading">
            Moving Beyond Generic API Wrappers
          </h2>
          <p className="prose-lg max-w-3xl">
            Most commercial AI initiatives run into issues when scaling to real workloads: unpredictable per-token pricing, network latency, and third-party data compliance exposure.
          </p>
          <p className="prose-lg mb-4 max-w-3xl">
            We focus on self-hosted model deployments, specialized vector indexing with PostgreSQL pgvector, and automated document parsers that run entirely within your private cloud environment.
          </p>
          <div className="card card-lift disclosure my-6">
            <h3 className="card-heading-lg mb-2">Why Our Tools Are Production-Tested</h3>
            <p className="prose-sm text-muted">
              Every tool we offer—from our Document AI OCR parser to our Certificate Verification API—was created to solve operational bottlenecks within our own venture studio and engineering cohorts before being packaged for enterprise use.
            </p>
          </div>
          <div className="stack-h gap-4 mt-6 flex-wrap">
            <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link font-medium">Explore Private VPC Hosting Specs &rarr;</Link>
            <Link href="/ai-solutions/products" className="accent-link font-medium">Browse All 5 Enterprise Products &rarr;</Link>
          </div>
        </section>

        <section className="page-band">
          <div className="doclabel mb-2">§ 03 — CAPABILITY PILLARS</div>
          <h2 className="section-heading-4">
            How We Partner With Engineering Teams
          </h2>
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
        </section>

        <section className="page-band alt">
          <div className="card callout">
            <div className="doclabel mb-1">§ 04 — OPEN-WEIGHTS DEPLOYMENT</div>
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
        </section>

        <section className="page-band">
          <div className="doclabel mb-1">§ 05 — ENTERPRISE KNOWLEDGE BASE</div>
          <h2 className="section-heading-4 mb-4">Enterprise Architecture &amp; Security FAQ</h2>
          <div className="measure">
            <FAQAccordion items={faqs} />
          </div>
        </section>

        <section className="page-band page-cta">
          <div className="card callout-plain text-center">
            <h3 className="card-heading-lg mb-2">Ready to Transition from Prototype to Sovereign AI Production?</h3>
            <p className="prose-sm text-muted mb-4 max-w-xl mx-auto">
              Engage directly with our active systems architects for an objective infrastructure feasibility audit or customized VPC software demonstration.
            </p>
            <div className="stack-h gap-4 justify-center">
              <Link href="/ai-solutions/consultation" className="btn btn-primary">Book Technical Consultation</Link>
              <Link href="/startups" className="btn btn-outline">View Startup Incubation Model</Link>
            </div>
          </div>
        </section>
    </div>
  );
}

