import React from 'react';
import Link from 'next/link';
import DemoRequestForm from '@/components/ui/DemoRequestForm';
import PricingNotice from '@/components/ui/PricingNotice';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../ai-solutions.module.css';
import { FileText, CheckCircle, Database, Shield, Webhook, Layers } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/products/document-ai');

export default function DocumentAIPage() {
  const faqs = [
    {
      question: 'What document formats and layout variations can the Document AI pipeline ingest?',
      answer: 'Our parsing engine ingests complex unstructured PDF reports, scanned multi-page invoices, MSME audit sheets, structured CSV logs, and raw optical image captures (PNG/JPG). It handles rotating alignments, low-resolution scans, and multi-column document layouts without needing fragile OCR template rules.'
    },
    {
      question: 'How does automatic accuracy verification prevent false or hallucinated parameter outputs?',
      answer: 'The pipeline incorporates bilateral semantic checking algorithms that mathematically audit extracted financial quantities against supporting table sub-calculations (e.g., verifying invoice subtotal + tax = total billable balance). Any value inconsistency triggers an automatic human-in-the-loop audit flag.'
    },
    {
      question: 'Can extracted structured JSON data be transmitted directly to custom SQL databases or ERP platforms?',
      answer: 'Yes. Upon successful schema extraction, our event dispatcher triggers authenticated HTTP webhook payloads to write formatted records directly into PostgreSQL tables, Salesforce Salesforce CRM records, SAP financial ledgers, or custom internal enterprise cloud REST endpoints.'
    },
    {
      question: 'Is customer document data stored or utilized to train future AI image or parsing models?',
      answer: 'Never. Document payloads are processed entirely inside volatile RAM sandbox workers within secure cloud or on-premise container environments. Once extracted JSON strings are confirmed delivered via webhook, source files and temporary buffer scans are irrevocably purged.'
    },
    {
      question: 'What is the standard processing speed and API latency per document extraction query?',
      answer: 'Standard single-page invoices and financial tabular sheets complete extraction and schema validation within 800ms to 1.5 seconds. Multi-page legal contractual dossiers complete within 3 to 5 seconds depending on OCR preprocessing resolution.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareApplication',
        name: 'DBERT Document AI & Automated JSON Schema Extraction Suite',
        applicationCategory: 'BusinessApplication, DataEngineeringApplication',
        operatingSystem: 'Cloud REST API, Docker Container, Linux Subsystem',
        description: 'Industrial document intelligence pipeline transforming unstructured invoices, PDFs, and legal contracts into validated JSON schemas with zero token training leaks.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Enterprise SaaS Licensing',
          price: '35000',
          priceCurrency: 'INR',
          description: 'Monthly license starting tier for automated document parsing & verification webhooks',
          url: 'https://dbert.online/ai-solutions/products/document-ai'
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
          Transform Unstructured Data Into Actionable JSON Intelligence
        </h1>
        <p className="lede-wide">
          An enterprise document parsing architecture that continuously ingests unstructured invoices, PDF corporate contracts, MSME tax registers, and operational logs, converting them directly into predictable, type-safe JSON schema structures with automatic mathematical validation.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Incubating Indian Venture Startups</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          We categorically refuse to sell unchecked software wrapper abstractions. <strong>DBERT Document AI was born out of our venture studio operations</strong>, where our technical audits required analyzing thousands of unstructured supplier invoices, bank ledger statements, and complex Indian MSME incorporation certificates across portfolio startups.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              Traditional optical character recognition (OCR) systems failed whenever a vendor slightly altered an invoice border or table format, forcing engineering squads into constant regex rule patching. We designed Document AI to utilize localized vision-language models and Pydantic schema validation. It parses document meaning semantically rather than relying on strict pixel coordinate templates, eliminating breaking data parsing bugs.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/startups/services/technical" className="accent-link text-xs font-mono font-medium">Explore Technical Services &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Our MSME Corporate Registration &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Code Simulator Block (Secondary BG) - How It Works */}
      <div className="section-band border-t border-b border-line">
        <div className={`container ${s.codeWrap}`}>
          <div className="doclabel mb-2">§ 03 — ARCHITECTURAL INTEGRATION COMMAND</div>
          <h2 className="subsection-title">Automated API Extraction Command</h2>
          <p className="prose-sm text-muted mb-4 max-w-2xl">
            Submit document file URLs or Base64 binary payloads alongside your desired output parameter schema using a single REST POST request.
          </p>
          <div className={`bento-card ${s.codeCard}`}>
            <pre className={s.code}>
{`curl -X POST "https://api.dbert.online/v1/extract" \\
  -H "Authorization: Bearer YOUR_ENTERPRISE_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "document_url": "https://secure-storage.dbert.online/client_invoices/inv_9981.pdf",
    "schema_definition": {
      "invoice_number": "string",
      "total_tax_inr": "number",
      "vendor_pan": "string_regex_[A-Z]{5}[0-9]{4}[A-Z]{1}",
      "line_items": "array_of_objects"
    },
    "enforce_math_audit": true
  }'`}
            </pre>
          </div>
        </div>
      </div>

      {/* Product Capabilities & How It Works (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — CORE ARCHITECTURAL SPECIFICATIONS</div>
        <h2 className="section-title mb-4">
          Engineered for Document Parsing Integrity
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h3 className="block-title-sm">
              1. Unstructured to JSON Schemas
            </h3>
            <p className="prose-sm text-muted">
              Extract targeted key-value properties and nested tabular arrays from diverse PDF forms, invoices, and legal filings, converting them directly to strict JSON structures.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Autonomous document orientation &amp; type recognition</li>
              <li>&bull; Strict parameter normalizations (ISO dates &amp; currency)</li>
              <li>&bull; Multi-language visual image &amp; scan preprocessing</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              2. Accuracy Verification &amp; Audit
            </h3>
            <p className="prose-sm text-muted">
              Configure deterministic arithmetic validation rules (such as debit/credit total balance cross-checks) to flag questionable or low-confidence OCR reads immediately.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Bilateral value-audit arithmetic checksum calculations</li>
              <li>&bull; Automatic anomaly alerts for missing required keys</li>
              <li>&bull; Granular 0-100 reliability confidence index scorecards</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              3. Automated Database Webhooks
            </h3>
            <p className="prose-sm text-muted">
              Establish hardened HTTPS webhook event callbacks to deposit verified extracted operational records directly into your database relational tables or accounting suites.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; HMAC signed authenticated HTTPS webhook payloads</li>
              <li>&bull; Instant ingestion adapters for PostgreSQL &amp; Salesforce</li>
              <li>&bull; Batch extraction exports formatted as CSV or XLSX arrays</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Compliance */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY &amp; COMPLIANCE RIGOR</div>
        <h2 className="section-title mb-2">Zero-Retention Document Privacy</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Enterprise finance and legal document analysis demands rigid data isolation. Our processing containers operate under strict zero-retention guidelines and cryptographic transit encryption.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Volatile Memory Sandboxing</h4>
            <p className="text-xs text-muted">
              Invoices and contracts are parsed within ephemeral RAM sandboxes. Once extracted schema values are acknowledged by your client server via webhook, temporary processing images are purged from operational buffers immediately.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Air-Gapped On-Premise Execution</h4>
            <p className="text-xs text-muted">
              For financial auditors and government compliance operations, Document AI can be instantiated wholly entirely offline within your localized Docker or Kubernetes clusters, guaranteeing zero public cloud exposure.
            </p>
          </div>
        </div>
      </div>

      {/* Integrations Roster */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 06 — SYSTEM &amp; DATABASE INTEGRATIONS</div>
        <h2 className={s.techHeading}>Supported Enterprise Ecosystem Integrations</h2>
        <div className={s.techRow}>
          {["PostgreSQL", "Prisma ORM", "Salesforce CRM", "SAP ERP", "Python Requests", "Node.js SDK", "Docker Container", "REST / Webhooks", "AWS S3 / Azure Blob"].map((tool, idx) => (
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
          Scale your enterprise document throughput with structured monthly licensing bands designed for high-volume Indian accounting teams, MSME platforms, and developer squads.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Growth API Tier</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹35,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Designed for high-growth startups automating vendor invoice processing and document onboarding.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 15,000 document extractions/mo</li>
                <li>Pydantic schema validation rules</li>
                <li>Standard webhook callback architectures</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-outline w-full mt-4">Select Growth Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">High Throughput</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Enterprise Scale</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹95,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Dedicated high-speed extraction processing lines with prioritized SLA and custom mathematical audit logic.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 75,000 document extractions/mo</li>
                <li>Custom business rules &amp; tax math validation</li>
                <li>24/7 priority integration troubleshooting</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-primary w-full mt-4">Inquire Enterprise Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">On-Premise Container</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Custom Scope</div>
              <p className="text-xs text-muted mt-2">Deploy self-contained offline Docker extraction bundles within localized high-security data centers.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Air-gapped zero-internet runtime operation</li>
                <li>Unlimited on-premise extraction volume</li>
                <li>Dedicated architectural maintenance squad</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Discuss On-Premise Scope &rarr;</Link>
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
            <h4 className="font-mono text-sm font-bold text-white mb-1">DBERT Chat Console</h4>
            <p className="text-xs text-muted mb-3">Deploy conversational chat interfaces over extracted corporate document archives with pgvector RAG.</p>
            <Link href="/ai-solutions/products/dbert-chat" className="accent-link text-xs">View DBERT Chat &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Certificate Verification API</h4>
            <p className="text-xs text-muted mb-3">Cryptographically check employee completion credentials and training diplomas via ultra-fast API.</p>
            <Link href="/ai-solutions/products/certificate-verification-api" className="accent-link text-xs">View Verification API &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Technical Architecture Review</h4>
            <p className="text-xs text-muted mb-3">Audit startup technology stacks, codebase repositories, and architectural debt before venture rounds.</p>
            <Link href="/startups/services/technical" className="accent-link text-xs">View Technical Services &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Action Call & Demo Request */}
      <div className="container pb-block border-t border-line pt-12" id="demo-request">
        <div className="doclabel mb-2">§ 10 — SCHEDULE ENTERPRISE DEPLOYMENT</div>
        <PricingNotice />
        <DemoRequestForm productName="Document AI Pipeline" />
      </div>
    </div>
  );
}

