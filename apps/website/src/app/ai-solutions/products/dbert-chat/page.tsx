import React from 'react';
import Link from 'next/link';
import DemoRequestForm from '@/components/ui/DemoRequestForm';
import PricingNotice from '@/components/ui/PricingNotice';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../ai-solutions.module.css';
import { Shield, Cpu, Lock, Workflow, Terminal, Layers } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/products/dbert-chat');

export default function DBERTChatPage() {
  const faqs = [
    {
      question: 'How does DBERT Chat guarantee data confidentiality against third-party training leaks?',
      answer: 'DBERT Chat operates entirely within your private containerized environment or isolated cloud virtual private cloud (VPC). Zero customer prompt queries or database completions are transmitted to public commercial aggregators (such as OpenAI or Anthropic public training pipelines). Your sensitive enterprise know-how remains cryptographically bounded within your domain.'
    },
    {
      question: 'What is the maximum embedding context window supported by your pgvector RAG indexing?',
      answer: 'Our embedding pipelines support configurable context windows extending up to 128,000 tokens per single interactive thread, utilizing hybrid recursive character chunk partitioning and re-ranking algorithms in PostgreSQL pgvector to retrieve semantic matches with sub-100ms latency.'
    },
    {
      question: 'Can we self-host DBERT Chat directly on our internal enterprise workstation hardware?',
      answer: 'Yes. For Indian enterprises operating under strict data localization and compliance governance (including defense, fintech, and biomedical sectors), we distribute Dockerized runtime bundles pre-configured for localized weights serving via Ollama and vLLM on enterprise NVIDIA GPU hardware.'
    },
    {
      question: 'How does bilateral rate limiting protect internal servers from concurrent traffic bursts?',
      answer: 'The messaging gateway implements distributed Redis token buckets and dynamic queues, capping user requests and output token budgets per department or individual seat. This eliminates server memory exhaustion and maintains predictable operational computational costs.'
    },
    {
      question: 'What onboarding support and Service Level Agreements (SLAs) do you provide for enterprise tier clients?',
      answer: 'Enterprise subscription tiers receive dedicated Slack/WhatsApp support channels, custom SQL database adapter integration assistance from our venture studio engineers, and a backed 99.9% uptime Service Level Agreement for managed cloud deployments.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareApplication',
        name: 'DBERT Chat Enterprise Console & Private RAG Gateway',
        applicationCategory: 'BusinessApplication, DeveloperApplication',
        operatingSystem: 'Linux, Docker, Cloud SaaS, Windows Server',
        description: 'Private, localized chatbot architecture supporting enterprise PostgreSQL pgvector matching, real-time SSE token streaming, and zero token training leaks.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Enterprise SaaS Licensing',
          price: '45000',
          priceCurrency: 'INR',
          description: 'Monthly license starting fee for verified private cloud deployment with SLA',
          url: 'https://dbert.online/ai-solutions/products/dbert-chat'
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
          § 01 — ENTERPRISE SAAS PRODUCT <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Enterprise Conversations &mdash; Private, Intelligent, Secure
        </h1>
        <p className="lede-wide">
          Deploy localized conversational agent interfaces running over your proprietary enterprise databases and operational document logs. Maintain absolute cryptographic data confidentiality, enforce department token rate budgets, and eliminate commercial training leaks.
        </p>
        <div className="flex justify-center gap-3 flex-wrap mt-4">
          <span className="proof-mark">
            <span>✓ 100% DPDP Act 2023 Compliant</span>
          </span>
          <span className="proof-mark proof-mark-signal">
            <span>Customer VPC or On-Premise Air-Gapped</span>
          </span>
          <span className="proof-mark">
            <span>Zero Data Ingestion by Third-Party APIs</span>
          </span>
        </div>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Our Own Production Requirements</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we enforce a strict engineering standard: <strong>we build and operate our tools internally before commercializing them</strong>. DBERT Chat was originally engineered to replace insecure public LLM wrappers across our technical training venture studio, where hundreds of engineering fellows interact daily with internal codebase repositories, proprietary legal term-sheet archives, and MSME evaluation reports.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              Off-the-shelf commercial APIs exposed our proprietary venture studio client data to external third-party telemetry and incurred unpredictable token escalation billing during heavy code generation sprints. We constructed DBERT Chat as a hardened, localized retrieval gateway leveraging PostgreSQL pgvector distance indexes and Server-Sent Events (SSE). Today, this identical battle-tested architecture empowers external enterprises requiring air-gapped conversational intelligence.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs font-mono font-medium">Explore Hardware &amp; Hosting Architecture &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Our MSME Corporate Registration &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Code Simulator Block (Secondary BG) - How It Works */}
      <div className="section-band border-t border-b border-line">
        <div className={`container ${s.codeWrap}`}>
          <div className="doclabel mb-2">§ 03 — ARCHITECTURAL INTEGRATION COMMAND</div>
          <h2 className="subsection-title">Developer API Gateway Command</h2>
          <p className="prose-sm text-muted mb-4 max-w-2xl">
            Integrate DBERT Chat into existing corporate portals, ERP software, or backend microservices in minutes via standard REST and streaming endpoints.
          </p>
          <div className={`bento-card ${s.codeCard}`}>
            <pre className={s.code}>
{`curl -X POST "https://api.dbert.online/v1/chat" \\
  -H "Authorization: Bearer YOUR_ENTERPRISE_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "dbert-chat-v2-quantized",
    "messages": [{"role": "user", "content": "Query internal audit logs for Q4 expenditure"}],
    "vector_collection": "finance_records_2026",
    "stream_tokens": true,
    "enforce_privacy": true
  }'`}
            </pre>
          </div>
        </div>
      </div>

      {/* Product Capabilities & How It Works (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — CORE ARCHITECTURAL SPECIFICATIONS</div>
        <h2 className="section-title mb-4">
          Engineered for Enterprise Throughput &amp; Reliability
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h3 className="block-title-sm">
              1. RAG Vector Storage Engine
            </h3>
            <p className="prose-sm text-muted">
              Query corporate document repositories, institutional databases, and historical transaction logs utilizing high-throughput PostgreSQL pgvector distance indexing parameters.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Sub-100ms cosine similarity vector matching</li>
              <li>&bull; Recursive character &amp; semantic overlapping chunking</li>
              <li>&bull; Native PostgreSQL pgvector schema normalization</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              2. Token Budgeting &amp; Governors
            </h3>
            <p className="prose-sm text-muted">
              Define explicit departmental usage quotas and token consumption thresholds to eliminate server overload and enforce rigorous monthly computing cost boundaries.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Configurable seat-level input/output token caps</li>
              <li>&bull; Distributed bilateral rate-limiting &amp; FIFO queues</li>
              <li>&bull; Real-time GPU runtime throughput analytical logs</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              3. Interactive Console UI &amp; SSE
            </h3>
            <p className="prose-sm text-muted">
              Deliver zero-latency responsive operator interfaces supporting secure real-time Server-Sent Events (SSE) streaming without websocket disconnect overhead.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Asynchronous SSE real-time token streaming pathways</li>
              <li>&bull; AES-256 encrypted relational session storage tables</li>
              <li>&bull; Responsive Next.js 16 modular console layouts</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Compliance */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY &amp; COMPLIANCE RIGOR</div>
        <h2 className="section-title mb-2">Enterprise Security &amp; Data Isolation</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Designed for regulated Indian operating environments, DBERT Chat implements strict zero-trust boundaries, eliminating data exfiltration risks common in cloud consumer generative chatbots.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Zero Token Training Leaks</h4>
            <p className="text-xs text-muted">
              We contractually and technically enforce that zero incoming operational prompts, document payloads, or generated completion summaries are ever routed to model training clusters or third-party behavioral aggregation algorithms.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Role-Based Access Control (RBAC)</h4>
            <p className="text-xs text-muted">
              Integrate directly with enterprise Single Sign-On (SSO) and LDAP identity providers. Enforce strict collection-level read and write permissions ensuring interns and executives only retrieve documentation commensurate with their security clearance.
            </p>
          </div>
        </div>
      </div>

      {/* Integrations Roster */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 06 — SYSTEM &amp; DATABASE INTEGRATIONS</div>
        <h2 className={s.techHeading}>Supported Enterprise Ecosystem Integrations</h2>
        <div className={s.techRow}>
          {["PostgreSQL pgvector", "Next.js App Router", "Ollama RunTime", "vLLM Engine", "Docker / Kubernetes", "Prisma ORM", "AWS / GCP / Azure", "Redis Cache", "REST / Webhooks"].map((tool, idx) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Pricing & Commercial Licensing Tiers */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 07 — COMMERCIAL LICENSING &amp; DEPLOYMENT TIERS</div>
        <h2 className="section-title mb-2">Transparent Enterprise SaaS Licensing</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Select between managed high-availability cloud deployments or fully offline on-premise container licensing tailored to your Indian organization&apos;s governance and computing scale.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Startup Managed Cloud</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹45,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Hosted inside dedicated Indian region VPCs with automated backups and 50 team seat licenses.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 500,000 document embedding queries/mo</li>
                <li>Managed PostgreSQL pgvector cluster</li>
                <li>Standard business hour engineering SLA</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-outline w-full mt-4">Select Startup Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Popular Choice</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Enterprise Air-Gapped</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹1,20,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Deployed directly to your corporate bare-metal servers or secure local cloud hardware with zero telemetry.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Unlimited local inference &amp; embedding volume</li>
                <li>Ollama &amp; vLLM open-weights optimization</li>
                <li>24/7 dedicated engineering practice support</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-primary w-full mt-4">Inquire Enterprise Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Venture Studio Custom</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Custom Scope</div>
              <p className="text-xs text-muted mt-2">Tailored multi-agent operational orchestration and custom domain fine-tuning for specialized industrial workflows.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Custom model fine-tuning on domain corpora</li>
                <li>Full source-code adapter access &amp; training</li>
                <li>Co-development engineering apprenticeship squads</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Discuss Custom Scope &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — PRODUCT TECHNICAL KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED AI SOLUTIONS &amp; INFRASTRUCTURE</div>
        <h2 className="section-title mb-4">Explore Complementary DBERT Platforms</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Document AI Extraction</h4>
            <p className="text-xs text-muted mb-3">Convert messy corporate PDFs, scanned invoices, and forms directly into structured JSON schemas.</p>
            <Link href="/ai-solutions/products/document-ai" className="accent-link text-xs">View Document AI &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Private LLM Hosting</h4>
            <p className="text-xs text-muted mb-3">Review transparent hardware architecture and bare-metal server infrastructure in Indian datacenters.</p>
            <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs">View Private Hosting &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Hiring Automation Suite</h4>
            <p className="text-xs text-muted mb-3">Audit candidate codebases, run resume scoring pipelines, and streamline technical recruiting.</p>
            <Link href="/ai-solutions/products/hiring-automation-suite" className="accent-link text-xs">View Hiring Suite &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Action Call & Demo Request */}
      <div className="container pb-block border-t border-line pt-12" id="demo-request">
        <div className="doclabel mb-2">§ 10 — SCHEDULE ENTERPRISE DEPLOYMENT</div>
        <PricingNotice />
        <DemoRequestForm productName="DBERT Chat" />
      </div>
    </div>
  );
}

