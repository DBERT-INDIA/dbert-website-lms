import React from 'react';
import Link from 'next/link';
import DemoRequestForm from '@/components/ui/DemoRequestForm';
import PricingNotice from '@/components/ui/PricingNotice';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../ai-solutions.module.css';
import { ShieldCheck, Database, Lock, Key, CheckCircle, Terminal } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/products/certificate-verification-api');

export default function CertificateVerificationAPIPage() {
  const faqs = [
    {
      question: 'How does cryptographic certification authentication prevent fraudulent diploma claims?',
      answer: 'Every credential issued through our industrial engineering cohorts or registered enterprise client platforms is encoded with a unique SHA-256 digital hash and cryptographic UUID. When an employer queries the API, our backend matches the cryptographic token against immutable relational database registers, preventing altered PDF diplomas from passing validation.'
    },
    {
      question: 'Can we embed verification lookup controls directly inside our corporate HR talent dashboard?',
      answer: 'Yes. Our platform supplies zero-dependency HTML lookup widget embed snippets and React interface adapters. Human Resource departments and technical staffing partners can verify candidates natively within their internal portals without redirecting out to external sites.'
    },
    {
      question: 'What protections exist to prevent automated unauthorized bulk credential scraping via the API?',
      answer: 'The API gateway mandates encrypted JWT bearer token authentication, dynamic IP-based rate throttling, and algorithmic anomaly detection. Requests attempting sequential or dictionary enumeration of certificate serial numbers are automatically blacklisted by our firewall rules.'
    },
    {
      question: 'What response formats and parameters are returned during a successful credential evaluation?',
      answer: 'A successful GET interrogation returns a cleanly structured JSON payload containing verified attributes: candidate complete legal name, completed program concentration, capstone repository URL hashes, issuance timestamp, and active Letter of Recommendation (LOR) authorization status.'
    },
    {
      question: 'Can educational institutes or startup training programs license this API for their own credential issuance?',
      answer: 'Yes. Authorized Indian skill academies, technical university departments, and venture developer bootcamps can license our secure verification API to issue, track, and independently authenticate their own student certificates using our managed backend architecture.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareApplication',
        name: 'DBERT Cryptographic Certificate & Credential Verification API',
        applicationCategory: 'SecurityApplication, BusinessApplication',
        operatingSystem: 'Cloud REST API, Node.js, Web Widget Embed',
        description: 'Secure enterprise API backend and cryptographic verification gateway enabling instant validation of developer credentials, diplomas, and MSME LOR completion records.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Enterprise API Licensing',
          price: '25000',
          priceCurrency: 'INR',
          description: 'Monthly API access licensing starting tier for enterprise HR platforms and academic institutions',
          url: 'https://dbert.online/ai-solutions/products/certificate-verification-api'
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
          Instant Trust &mdash; Cryptographic Credential Verification API
        </h1>
        <p className="lede-wide">
          An enterprise-grade API gateway and cryptographic validation engine allowing hiring platforms, corporate HR squads, and educational institutions to audit candidate credentials, MSME completion registers, and Letter of Recommendation (LOR) authenticity in milliseconds.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Built to Eliminate Indian Technical Resumes Fraud</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we enforce rigorous operational authenticity: <strong>we construct and run our technology in production before licensing it</strong>. This verification API was engineered to solve a rampant bottleneck across our Indian venture studio hiring pipelines—the prevalence of altered PDF internship certificates and fabricated reference credentials submitted during startup hiring rounds.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              Manual email and phone background verification consumed dozens of hours per engineering hire across our portfolio startups. To automate trust, we engineered a high-speed cryptographic API backend connecting directly to our immutable graduation and project repository databases. Today, enterprise staffing partners and academic organizations leverage this exact verification infrastructure to evaluate candidate authenticity instantly.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Test Live Credential Verification Portal &rarr;</Link>
              <Link href="/learners" className="accent-link text-xs font-mono font-medium">Inspect Industrial Training Tracks &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Code Simulator Block (Secondary BG) - How It Works */}
      <div className="section-band border-t border-b border-line">
        <div className={`container ${s.codeWrap}`}>
          <div className="doclabel mb-2">§ 03 — ARCHITECTURAL INTEGRATION COMMAND</div>
          <h2 className="subsection-title">Instant HTTP Verification Command</h2>
          <p className="prose-sm text-muted mb-4 max-w-2xl">
            Execute a single authenticated REST query passing the target certificate serial UUID to receive an immediate cryptographic verification confirmation.
          </p>
          <div className={`bento-card ${s.codeCard}`}>
            <pre className={s.code}>
{`curl -X GET "https://api.dbert.online/v1/verify?certId=DBERT-ENG-2026-8894" \\
  -H "Authorization: Bearer YOUR_ENTERPRISE_API_KEY" \\
  -H "Accept: application/json"

# Example JSON Response:
# { "status": "VERIFIED", "candidate": "Aditya Verma", "track": "AI Agent Systems", "lor_valid": true }`}
            </pre>
          </div>
        </div>
      </div>

      {/* Product Capabilities & How It Works (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — CORE ARCHITECTURAL SPECIFICATIONS</div>
        <h2 className="section-title mb-4">
          Engineered for High-Speed Authentication
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h3 className="block-title-sm">
              1. High-Speed JSON Query Endpoints
            </h3>
            <p className="prose-sm text-muted">
              Query candidate educational and internship achievements using secure HTTP GET parameters, returning verified structured attributes instantly.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Ultra-fast sub-50ms lookup response performance</li>
              <li>&bull; Granular Boolean status variables &amp; timestamp return</li>
              <li>&bull; Rigid JWT API gateway authorization token checks</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              2. Encrypted Database Lookups
            </h3>
            <p className="prose-sm text-muted">
              Maintain absolute candidate data isolation. All academic registers and employment letters are secured via encrypted PostgreSQL indexing.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Rate-throttling shields against automated bulk scraping</li>
              <li>&bull; Comprehensive auditing of API interrogation logs</li>
              <li>&bull; Multi-region encrypted relational database backups</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              3. Embeddable UI &amp; Web Widgets
            </h3>
            <p className="prose-sm text-muted">
              Embed responsive verification lookup forms and interactive status badges directly into your corporate portals or recruitment software.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Lightweight HTML &amp; JavaScript widget embed scripts</li>
              <li>&bull; Direct CRM synchronization for HR background audits</li>
              <li>&bull; Batch verification processing via CSV upload endpoints</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Compliance */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY &amp; COMPLIANCE RIGOR</div>
        <h2 className="section-title mb-2">Cryptographic Hardening &amp; Privacy</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We treat credential verification as mission-critical enterprise security. Our architecture guarantees tamper-proof record persistence and defensive anti-scraping controls.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Immutable Relational Indexes</h4>
            <p className="text-xs text-muted">
              Once an engineered completion record or Letter of Recommendation is cryptographically committed to our relational ledger, modifying historical records requires multi-signature administrative authorization, rendering fraudulent credential injection impossible.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Defensive Anti-Enumeration</h4>
            <p className="text-xs text-muted">
              To protect candidate privacy against uninvited marketing aggregators, our gateway monitors access patterns. Sequential serial enumeration attempts are instantly trapped, ensuring only valid corporate recruiters access achievement verification data.
            </p>
          </div>
        </div>
      </div>

      {/* Integrations Roster */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 06 — SYSTEM &amp; DATABASE INTEGRATIONS</div>
        <h2 className={s.techHeading}>Supported Enterprise Ecosystem Integrations</h2>
        <div className={s.techRow}>
          {["PostgreSQL", "Prisma ORM", "REST / JSON API", "Next.js / React Widget", "Node.js SDK", "Salesforce / HRIS", "Docker Container", "Redis Rate-Limit", "SHA-256 Crypto"].map((tool, idx) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Pricing & Commercial Licensing Tiers */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 07 — COMMERCIAL LICENSING &amp; DEPLOYMENT TIERS</div>
        <h2 className="section-title mb-2">Transparent Enterprise API Licensing</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Deploy high-speed credential verification across your staffing platforms or educational institutions with predictable monthly API lookup bands.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Corporate HR Tier</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹25,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Designed for startup HR departments and regional staffing agencies automating developer background audits.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 5,000 API verification checks/mo</li>
                <li>HTML embeddable lookup widgets</li>
                <li>Standard business hour engineering SLA</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-outline w-full mt-4">Select HR Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">High Volume</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Platform Partner</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹65,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Engineered for large employment portals and enterprise recruiters conducting batch candidate onboarding.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 50,000 API verification checks/mo</li>
                <li>Batch CSV automated upload endpoints</li>
                <li>24/7 dedicated integration support SLA</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-primary w-full mt-4">Inquire Platform Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Institutional Issuer</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Custom Scope</div>
              <p className="text-xs text-muted mt-2">For universities and technical academies requiring custom database tables to host and authenticate student records.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Custom institutional issuer branding</li>
                <li>Dedicated cloud PostgreSQL schema</li>
                <li>Co-engineered administration portals</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Discuss Institutional Scope &rarr;</Link>
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
            <h4 className="font-mono text-sm font-bold text-white mb-1">Hiring Automation Suite</h4>
            <p className="text-xs text-muted mb-3">Integrate credential validation with automated git repository code audits and technical resume scoring.</p>
            <Link href="/ai-solutions/products/hiring-automation-suite" className="accent-link text-xs">View Hiring Suite &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Intern Management System</h4>
            <p className="text-xs text-muted mb-3">Track student task logs, supervise mentor pull-request code reviews, and issue verified completion LORs.</p>
            <Link href="/ai-solutions/products/intern-management-system" className="accent-link text-xs">View Intern Portal &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Document AI Extraction</h4>
            <p className="text-xs text-muted mb-3">Convert unstructured PDF invoices and complex legal contracts directly into validated JSON schemas.</p>
            <Link href="/ai-solutions/products/document-ai" className="accent-link text-xs">View Document AI &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Action Call & Demo Request */}
      <div className="container pb-block border-t border-line pt-12" id="demo-request">
        <div className="doclabel mb-2">§ 10 — SCHEDULE ENTERPRISE DEPLOYMENT</div>
        <PricingNotice />
        <DemoRequestForm productName="Certificate Verification API" />
      </div>
    </div>
  );
}

