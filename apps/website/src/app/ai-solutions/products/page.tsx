import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../ai-solutions.module.css';

export const metadata = pageMetadata('/ai-solutions/products');

export default function SaaSProductsCatalogPage() {
  const products = [
    { 
      title: 'DBERT Chat', 
      desc: 'Sovereign conversational AI chatbot engineered with dynamic token budgeting, custom dataset schema matching, and complete on-premise localized weight execution.', 
      slug: 'dbert-chat',
      tag: 'Enterprise NLP',
      price: '₹25,000/mo'
    },
    { 
      title: 'Document AI', 
      desc: 'Automated document processing pipeline that ingests financial balance sheets, complex PDF invoices, and handwritten logs into validated structured JSON schemas.', 
      slug: 'document-ai',
      tag: 'OCR & Vision RAG',
      price: '₹40,000/mo'
    },
    { 
      title: 'Certificate Verification API', 
      desc: 'Cryptographic RESTful API backend enabling academic institutions and edtech platforms to issue, verify, and audit tamper-proof digital credentials in real time.', 
      slug: 'certificate-verification-api',
      tag: 'Zero-Trust Security',
      price: '₹15,000/mo'
    },
    { 
      title: 'Hiring Automation Suite', 
      desc: 'Autonomous engineering candidate screening dashboard that directly parses GitHub code repositories and executes automated test cases to match developer competency.', 
      slug: 'hiring-automation-suite',
      tag: 'Talent & HR Tech',
      price: '₹35,000/mo'
    },
    { 
      title: 'Intern Management System', 
      desc: 'Industrial apprenticeship operational workspace that automates code task assignment, peer PR review grading, weekly stipend tracking, and mentor evaluations.', 
      slug: 'intern-management-system',
      tag: 'Workforce OS',
      price: '₹20,000/mo'
    }
  ];

  const faqs = [
    {
      question: 'Are DBERT AI software products deployed on public clouds or private local servers?',
      answer: 'All DBERT commercial software platforms are designed for mathematical operational privacy and zero external token dependency. We package our application modules as Dockerized containers capable of deploying directly onto your isolated AWS Virtual Private Cloud (VPC), bare-metal GPU server clusters, or local on-premises hardware arrays behind Nginx reverse proxies with zero-trust firewall boundaries.'
    },
    {
      question: 'How do DBERT products differ from traditional API wrappers built around commercial LLMs?',
      answer: 'Generic third-party AI SaaS wrappers transmit unencrypted enterprise customer prompts directly to external commercial API providers—exposing your sensitive corporate records to unintended training leakage, arbitrary latency throttling, and unpredictable token price escalation. Our product suite executes open-weights models (such as customized Llama-3, Qwen, and Mistral parameters) locally within your network via high-throughput vLLM and Ollama runtimes.'
    },
    {
      question: 'Can enterprise clients procure customized white-labeling or tailored proprietary fine-tuning?',
      answer: 'Yes. Every product module in our commercial suite can be customized via tailored engineering sprints. Our AI laboratory researchers can fine-tune weights on your internal historical domain data, integrate white-label corporate user interfaces, customize PostgreSQL pgvector semantic indexing pipelines, and implement specialized Single Sign-On (SAML/SSO) security gates.'
    },
    {
      question: 'What ongoing maintenance, SLA uptime guarantees, and security patch obligations are included?',
      answer: 'Commercial software subscriptions and enterprise deployments include 99.9% uptime Service Level Agreements (SLAs), automated daily encrypted database snapshots, real-time Prometheus/Grafana MLOps telemetry alerting, and continuous zero-day vulnerability patch distributions executed by our core studio engineering squads.'
    },
    {
      question: 'How do incubated portfolio startup founders access these enterprise product capabilities?',
      answer: 'Startup founders undergoing technical co-development within the DBERT Venture Studio gain native access to our entire proprietary product stack without incurring upfront enterprise software licensing fees. We embed modules like Document AI and DBERT Chat directly into incubated founder repositories under our standard services-against-equity exchange.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'CollectionPage',
        name: 'DBERT Commercial AI Products Suite & SaaS Systems',
        description: 'Deploy battle-tested, sovereign artificial intelligence software product platforms engineered for secure on-premise enterprise integration and local open-weights serving.',
        url: 'https://dbert.online/ai-solutions/products',
        mainEntity: {
          '@type': 'ItemList',
          itemListElement: products.map((p, index) => ({
            '@type': 'ListItem',
            position: index + 1,
            url: `https://dbert.online/ai-solutions/products/${p.slug}`,
            name: p.title,
            description: p.desc
          }))
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

      <div className="container pad-block">
        
        {/* Hero Header & Overview */}
        <div className="mb-10">
          <div className="doclabel">
            § 01 — AI PRODUCTS CATALOG <span className="rev">rev: 2026.2</span>
          </div>
          <h1 className="text-4xl font-mono font-bold text-white mb-3">
            Deploy Sovereign, Production-Ready AI Systems
          </h1>
          <p className="lede-wide text-muted max-w-3xl leading-relaxed">
            Battle-tested artificial intelligence software product platforms engineered by our venture studio to integrate seamlessly into your secure production IT infrastructure—guaranteeing data sovereignty, deterministic inference speeds, and zero external token dependency.
          </p>
        </div>

        {/* Product Philosophy */}
        <section className="section-breath border-t border-line">
          <div className="doclabel mb-2">§ 02 — ARCHITECTURAL INTEGRITY</div>
          <h2>Self-Hosted Enterprise Systems</h2>
          <p className="body-copy mb-6 max-w-3xl">
            We build tools that run directly inside your Virtual Private Cloud. By pairing local open-weights inference (Ollama / vLLM) with PostgreSQL pgvector, our products eliminate unpredictable token rate hikes and protect sensitive internal data.
          </p>
          <div className="card card-lift my-6">
            <span className="doclabel text-xs mb-1">§ PRODUCTION PEDIGREE</span>
            <h3 className="card-title mt-2">Tested at Scale on Live Workloads</h3>
            <p className="body-copy mt-2">
              Every platform in our catalog was originally built to solve computational, document parsing, or credential verification challenges inside our own venture studio and engineering cohorts before being packaged for enterprise licensing.
            </p>
          </div>
        </section>

        {/* Product Modules Grid */}
        <section className="section-breath border-t border-line">
          <div className="doclabel mb-4">§ 03 — DEPLOYABLE AI PRODUCT MODULES</div>
          <div className="bento-grid-3 stagger-grid">
            {products.map((prod, idx) => (
              <div key={idx} className="card card-lift flex flex-col justify-between h-full">
                <div>
                  <span className="tag-chip mb-3">{prod.tag}</span>
                  <h3 className="card-title my-2">{prod.title}</h3>
                  <div className="font-mono text-xs text-signal font-medium mb-3">Enterprise VPC License</div>
                  <p className="text-xs text-muted leading-relaxed mb-6">{prod.desc}</p>
                </div>
                <Link href={`/ai-solutions/products/${prod.slug}`} className="accent-link text-xs font-mono pt-4 border-t border-line stack-h justify-between align-center">
                  <span>Explore Specs &amp; SLA</span>
                  <span aria-hidden="true">&rarr;</span>
                </Link>
              </div>
            ))}
            <div className="card card-lift flex flex-col justify-between h-full text-center">
              <div>
                <span className="tag-chip mb-3">Custom Architecture</span>
                <h3 className="card-title my-2">Need Custom Domain Fine-Tuning?</h3>
                <p className="text-xs text-muted leading-relaxed mb-6">Our engineering team develops bespoke RAG search pipelines and fine-tuned open-weights models tailored strictly to your internal datasets.</p>
              </div>
              <Link href="/ai-solutions/consultation" className="btn btn-outline btn-sm w-full mt-auto">Book AI Consultation &rarr;</Link>
            </div>
          </div>
        </section>

        {/* Air-Gapped Deployment & Data Sovereignty Overview */}
        <section className="mb-14 pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 04 — ENTERPRISE DEPLOYMENT ARCHITECTURE</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-3">
            Air-Gapped Container Execution &amp; Mathematical Data Privacy
          </h2>
          <p className="prose-sm text-muted leading-relaxed mb-6 max-w-3xl">
            Every product within the DBERT suite is built on modular, containerized architectural principles. Whether you are an educational institution verifying student certificates or an industrial manufacturer processing technical compliance schematics, our systems integrate with rigorous defense-in-depth protocols.
          </p>

          <div className="grid gap-6 md:grid-cols-3 my-6">
            <div className="card p-6 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-2">1. Dockerized Container Run-Times</h4>
              <p className="text-xs text-muted leading-relaxed">
                Applications ship as self-contained Docker images incorporating optimized vLLM or Ollama local inference engines, pre-configured Nginx reverse proxy gates, and strict rate-limiting token bucket protections.
              </p>
            </div>
            <div className="card p-6 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-2">2. Hardened Vector Stores</h4>
              <p className="text-xs text-muted leading-relaxed">
                Semantic retrieval operates on localized PostgreSQL relational database clusters natively equipped with the pgvector extension and Hierarchical Navigable Small World (HNSW) indexing—ensuring sub-100ms vector query execution.
              </p>
            </div>
            <div className="card p-6 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-2">3. Zero-Trust Access Zoning</h4>
              <p className="text-xs text-muted leading-relaxed">
                Database storage volumes and GPU inference ports remain completely isolated within private network subnets, accessible strictly via SSH Bastion authentication gateways and mutual TLS encryption.
              </p>
            </div>
          </div>
        </section>

        {/* Commercial Licensing FAQ */}
        <section className="mb-14 pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 05 — COMMERCIAL LICENSING FAQ</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-4">Frequently Asked Product &amp; SLA Questions</h2>
          <div className="measure">
            <FAQAccordion items={faqs} />
          </div>
        </section>

        {/* Related Training & Infrastructure Mesh */}
        <section className="mb-12 pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 06 — RELATED ACADEMY &amp; INFRASTRUCTURE SERVICES</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-4">Explore Complementary Engineering Divisions</h2>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="card p-4 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-1">Cloud &amp; AI Infrastructure</h4>
              <p className="text-xs text-muted mb-3">Provision bare-metal GPU server clusters and design zero-trust Virtual Private Clouds for your enterprise.</p>
              <Link href="/startups/services/infrastructure" className="accent-link text-xs">View Infrastructure Service &rarr;</Link>
            </div>
            <div className="card p-4 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-1">AI Agent Course</h4>
              <p className="text-xs text-muted mb-3">Train your corporate software developers in constructing autonomous RAG workflows and local LangChain agents.</p>
              <Link href="/learners/courses/ai-agent-development" className="accent-link text-xs">Explore AI Agent Training &rarr;</Link>
            </div>
            <div className="card p-4 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-1">Venture Studio Incubation</h4>
              <p className="text-xs text-muted mb-3">Embed our proprietary product modules natively into your startup architecture under a services-against-equity structure.</p>
              <Link href="/startups/services" className="accent-link text-xs">Explore Venture Studio &rarr;</Link>
            </div>
          </div>
        </section>

        {/* Call to Action */}
        <section className="pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 07 — INITIATE DEPLOYMENT</div>
          <div className="bento-card callout p-8 bg-zinc-900 border border-line text-center rounded-lg">
            <h2 className="text-3xl font-mono font-bold text-white mb-2">Ready to Secure Your AI Operational Infrastructure?</h2>
            <p className="text-sm text-muted max-w-2xl mx-auto mb-6">
              Connect with our principal artificial intelligence researchers to schedule a technical architecture demo, request institutional SLA documentation, or procure containerized on-premise deployments.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link href="/ai-solutions/consultation" className="btn btn-primary btn-lg">Schedule Technical Demo &rarr;</Link>
              <Link href="/about/contact" className="btn btn-outline btn-lg">Contact Sales &amp; SLA Team &rarr;</Link>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}

