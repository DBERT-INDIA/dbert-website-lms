import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import HandNote from '@/components/ui/HandNote';
import s from '@/app/learners/learners.module.css';
import { Bot, Database, Layers, ArrowRight, CheckCircle2 } from 'lucide-react';

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
        <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
          <h1 className="page-title mb-0">
            Enterprise AI Consulting &amp; Custom LLM Systems
          </h1>
          <HandNote tone="blue">
            senior architect review ✍
          </HandNote>
        </div>
        <p className={s.courseTagline}>
          From AI Readiness Audit to Production RAG Pipelines &amp; Private LLM Deployment.
        </p>
        <p className={s.courseLede}>
          Transform complex operational bottlenecks with production-grade Generative AI systems. We help enterprises architect secure, low-latency AI agents, custom vector databases, and multi-provider LLM infrastructure.
        </p>
        <div className="stack-h gap-4 mt-6 flex-wrap">
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
          <div className="section-head text-center mb-8">
            <div className="doclabel justify-center">§ 02 — SPECIALIZED ARCHITECTURE TRACKS</div>
            <h2>Core Engineering Capabilities</h2>
          </div>
          <div className="bento-grid-3">
            <div className="card card-lift text-center p-6">
              <span className="icon-chip"><Database aria-hidden="true" /></span>
              <h3 className="accent-note">Production RAG Architecture</h3>
              <p className="body-copy">Enterprise retrieval-augmented generation using hybrid vector-keyword search, semantic document chunking, and persistent storage.</p>
            </div>
            <div className="card card-lift text-center p-6">
              <span className="icon-chip"><Bot aria-hidden="true" /></span>
              <h3 className="accent-note">Autonomous AI Agents</h3>
              <p className="body-copy">Multi-step reasoning loops, tool-calling agents (MCP), and automated background pipeline execution with full audit logs.</p>
            </div>
            <div className="card card-lift text-center p-6">
              <span className="icon-chip"><Layers aria-hidden="true" /></span>
              <h3 className="accent-note">Private LLM Hosting</h3>
              <p className="body-copy">Domain-specific model fine-tuning (LoRA/QLoRA), air-gapped deployment, and zero-latency token streaming setups.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Human Educational / How-To SEO Section */}
      <div className="container section-gap">
        <div className="measure-lg">
          <h2>How to Successfully Integrate Enterprise Generative AI Without Security Risks</h2>
          <p className="body-copy">
            Deploying AI into enterprise workflows requires balancing model capabilities with data privacy, cost control, and latency SLAs. Here is our step-by-step engineering framework:
          </p>

          <div className="bento-grid-3 my-8">
            <div className="card card-lift p-6">
              <h3 className="card-heading-lg stack-h align-center gap-2 mb-3">
                <CheckCircle2 className="text-signal shrink-0" size={20} /> Phase 1: AI Readiness &amp; Data Audit
              </h3>
              <p className="body-copy">We audit internal data formats (PDFs, SQL schemas, unstructured logs) and evaluate security governance requirements before writing any code.</p>
            </div>

            <div className="card card-lift p-6">
              <h3 className="card-heading-lg stack-h align-center gap-2 mb-3">
                <CheckCircle2 className="text-signal shrink-0" size={20} /> Phase 2: Hybrid Prototype Architecture
              </h3>
              <p className="body-copy">We build a production proof-of-concept incorporating streaming UI components, multi-provider fallbacks (OpenAI, Claude, Gemini), and sliding context windows.</p>
            </div>

            <div className="card card-lift p-6">
              <h3 className="card-heading-lg stack-h align-center gap-2 mb-3">
                <CheckCircle2 className="text-signal shrink-0" size={20} /> Phase 3: MLOps &amp; Security Isolation
              </h3>
              <p className="body-copy">We deploy the model pipeline inside your private AWS/GCP cloud VPC with token rate limiting, cost caps, and real-time observability telemetry.</p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Band */}
      <div className="section-band" id="consulting-audit">
        <div className="container measure-sm text-center">
          <h2>Schedule an AI Architecture Consultation</h2>
          <p className="body-copy my-4 text-muted">
            Speak directly with a senior DBERT AI Systems Architect. Receive a tailored roadmap for your enterprise.
          </p>
          <Link href="/ai-solutions/consultation" className="btn btn-primary btn-lg">
            Book 30-Min AI Discovery Call
          </Link>
        </div>
      </div>

      {/* FAQ Accordion */}
      <div className="container section-gap">
        <h2 className="text-center mb-8">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>
    </div>
  );
}
