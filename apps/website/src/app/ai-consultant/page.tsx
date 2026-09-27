import React from 'react';
import FAQAccordion from '@/components/ui/FAQAccordion';
import s from '@/app/learners/learners.module.css';
import { Bot, Sparkles, Database, Layers, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';

export const metadata = {
  title: 'Enterprise AI Strategy & Consultant Services | DBERT Labs',
  description: 'Enterprise AI consulting and custom LLM integration services. Architect production RAG systems, multi-provider AI workflows, and fine-tuned domain models with DBERT Labs.',
  keywords: ['Enterprise AI consultant', 'Generative AI consulting company', 'Custom LLM development', 'AI strategy consulting', 'RAG pipeline setup'],
};

export default function AIConsultantPage() {
  const faqs = [
    {
      question: 'How do DBERT AI consulting services differ from traditional IT consultancies?',
      answer: 'We don’t just deliver PowerPoint slide decks or generic advice. Our AI engineering consultants build, benchmark, and deploy custom production software models directly into your secure cloud infrastructure.'
    },
    {
      question: 'What security measures guarantee our corporate data remains private during AI integration?',
      answer: 'We enforce zero-data-retention compliance policies, establish localized private vector stores, and deploy air-gapped or VPC-isolated open-weights LLMs (such as Llama 3 or Mistral) to prevent sensitive corporate IP from leaking to commercial public models.'
    },
    {
      question: 'How do you determine whether a business process should use commercial APIs or fine-tuned local models?',
      answer: 'We execute a comprehensive AI Readiness Audit comparing query latency, operational cost per 1M tokens, security governance, and domain accuracy before recommending an architecture.'
    },
    {
      question: 'What is the typical timeframe for an enterprise AI proof-of-concept deployment?',
      answer: 'Our sprint-based delivery model delivers functional MVP prototypes within 2 to 4 weeks, followed by iterative enterprise scaling and automated MLOps monitoring.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'Enterprise AI Consulting & Custom LLM Architecture',
        serviceType: 'AI Engineering & Technological Advisory',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        description: 'End-to-end enterprise AI consulting services specializing in RAG architectures, custom LLM fine-tuning, and automated workflows.'
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
          § ENTERPRISE CONSULTING — AI STRATEGY <span className="rev">rev: 2026.1</span>
        </div>
        <h1 className="page-title">
          Enterprise AI Consulting & Custom LLM Systems
        </h1>
        <p className={s.courseTagline}>
          From AI Readiness Audit to Production RAG Pipelines & Private LLM Deployment.
        </p>
        <p className={s.courseLede}>
          Transform complex operational bottlenecks with production-grade Generative AI systems. We help enterprises architect secure, low-latency AI agents, custom vector databases, and multi-provider LLM infrastructure.
        </p>
        <div style={{ marginTop: '24px', display: 'flex', gap: '16px', flexWrap: 'wrap' }}>
          <a href="#consulting-audit" className="btn btn-primary btn-lg">
            Request AI Readiness Audit <ArrowRight className="inline-icon" />
          </a>
          <a href="#services-overview" className="btn btn-outline btn-lg">
            Explore Services
          </a>
        </div>
      </div>

      {/* Services Grid */}
      <div className="section-band" id="services-overview">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Database aria-hidden="true" /></span>
              <h3 className="accent-note">Production RAG Architecture</h3>
              <p>Enterprise retrieval-augmented generation using hybrid vector-keyword search, semantic document chunking, and persistent storage.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Bot aria-hidden="true" /></span>
              <h3 className="accent-note">Autonomous AI Agents</h3>
              <p>Multi-step reasoning loops, tool-calling agents (MCP), and automated background pipeline execution with full audit logs.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Layers aria-hidden="true" /></span>
              <h3 className="accent-note">Private LLM Hosting</h3>
              <p>Domain-specific model fine-tuning (LoRA/QLoRA), air-gapped deployment, and zero-latency token streaming setups.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Human Educational / How-To SEO Section */}
      <div className="container section-gap">
        <div className="prose-wrapper">
          <h2>How to Successfully Integrate Enterprise Generative AI Without Security Risks</h2>
          <p>
            Deploying AI into enterprise workflows requires balancing model capabilities with data privacy, cost control, and latency SLAs. Here is our step-by-step engineering framework:
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', margin: '32px 0' }}>
            <div className="card-box" style={{ padding: '24px', background: 'var(--card-bg)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 color="#10b981" /> Phase 1: AI Readiness & Data Audit
              </h3>
              <p>We audit internal data formats (PDFs, SQL schemas, unstructured logs) and evaluate security governance requirements before writing any code.</p>
            </div>

            <div className="card-box" style={{ padding: '24px', background: 'var(--card-bg)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 color="#10b981" /> Phase 2: Hybrid Prototype Architecture
              </h3>
              <p>We build a production proof-of-concept incorporating streaming UI components, multi-provider fallbacks (OpenAI, Claude, Gemini), and sliding context windows.</p>
            </div>

            <div className="card-box" style={{ padding: '24px', background: 'var(--card-bg)', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
              <h3 style={{ fontSize: '1.25rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <CheckCircle2 color="#10b981" /> Phase 3: MLOps & Security Isolation
              </h3>
              <p>We deploy the model pipeline inside your private AWS/GCP cloud VPC with token rate limiting, cost caps, and real-time observability telemetry.</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Band */}
      <div className="section-band" id="consulting-audit">
        <div className="container center-text" style={{ maxWidth: '700px', margin: '0 auto', textAlign: 'center' }}>
          <h2>Schedule an AI Architecture Consultation</h2>
          <p style={{ margin: '16px 0 32px 0', color: 'var(--text-muted)' }}>
            Speak directly with a senior DBERT AI Systems Architect. Receive a tailored roadmap for your enterprise.
          </p>
          <a href="https://internship.dbert.online/apply" className="btn btn-primary btn-lg" style={{ padding: '16px 36px', fontSize: '1.1rem' }}>
            Book 30-Min AI Discovery Call
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
