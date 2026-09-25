import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import { Building2, FileText, BadgeCheck, ShieldCheck, Scale, Lock } from 'lucide-react';

export const metadata = pageMetadata('/startups/services/legal');

export default function LegalServicePage() {
  const steps = [
    { number: '01', title: 'Entity Selection & Name Approval', description: 'We evaluate your startup capitalization scale to select between Private Limited or LLP structures and submit MCA RUN name validation requests.' },
    { number: '02', title: 'Corporate Registration Filings', description: 'We draft company incorporation MOA/AOA instruments, configure cap tables, and submit integrated SPICe+ MCA/PAN/GST registers.' },
    { number: '03', title: 'Startup India & MSME Onboarding', description: 'We execute filings to secure official DPIIT Startup India recognition and MSME Udyam certificates to unlock statutory tax benefits.' }
  ];

  const faqs = [
    {
      question: 'Should an artificial intelligence technology startup register as a Private Limited Company or an LLP in India?',
      answer: 'For technology startups seeking institutional venture capital funding or planning to issue Employee Stock Ownership Plans (ESOPs), a Private Limited Company is universally required by angel networks and VC funds. Limited Liability Partnerships (LLPs) are better suited for closely held bootstrapped professional service firms.'
    },
    {
      question: 'How long does the complete SPICe+ incorporation and DPIIT recognition timeline typically take?',
      answer: 'Standard MCA SPICe+ entity incorporation—including Digital Signature Certificates (DSC), Director Identification Numbers (DIN), PAN, and GST allocation—typically completes within 7 to 10 working days. Subsequent DPIIT Startup India recognition completes within 2 to 3 weeks upon submission of technical validation proofs.'
    },
    {
      question: 'What are the core income tax exemptions and capital benefits unlocked by DPIIT Startup India registration?',
      answer: 'Recognized startups gain access to Section 80-IAC income tax exemptions for 3 consecutive years out of their initial 10 years, exemption from angel tax under Section 56(2)(viib), self-certification under labor laws, and fast-tracked patent application facilitation with up to an 80% government fee rebate.'
    },
    {
      question: 'How do your standardized agreements protect founder equity from early departed co-founders or developers?',
      answer: 'We deploy strict 4-year founder equity vesting schedules incorporating a mandatory 1-year cliff and robust Good Reason/Cause definitions. If a co-founder departs during the first 12 months, unvested equity is automatically absorbed back into the corporate equity reserve without disputational deadlock.'
    },
    {
      question: 'Do you provide specialized AI model legal terms and intellectual property assignment contracts?',
      answer: 'Yes. Standard commercial software agreements fail to address AI training dataset rights and model weight ownership. Our contracts embed specific clauses ensuring all employee and apprentice contributions to neural model weights and vector training datasets belong 100% exclusively to the startup entity.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Legal & Intellectual Property Compliance Advisory',
        serviceType: 'Startup Incorporation, Commercial Contract Drafting, DPIIT Recognition Advisory',
        description: 'Comprehensive legal structuring, SPICe+ Private Limited incorporation, AI intellectual property assignment contracts, and DPIIT Startup India tax onboarding.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Venture Studio Legal Incubation',
          price: '25000',
          priceCurrency: 'INR',
          description: 'Flat fee incorporation and standardized contract suite or included within equity incubation scope',
          url: 'https://dbert.online/startups/services/legal'
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
          § 01 — VENTURE LEGAL SERVICE <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Protect Your Corporate Entity &amp; IP from Day One
        </h1>
        <p className="lede-wide">
          Secure your statutory Indian legal foundations before writing a single line of production code. We coordinate rigorous Private Limited and LLP incorporations, execute AI intellectual property assignment covenants, draft SAFE contracts, and facilitate official Startup India DPIIT recognition.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Navigating Indian Startup Realities</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we believe in radical operational reality: <strong>we construct and validate our frameworks in our own corporate affairs before advising founders</strong>. Our Legal &amp; IP service originated directly from managing our own MSME registration (DBERT Labs under Govt of India Udyam portal) and negotiating bilateral incubation term sheets across dozens of venture investments.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              Many promising Indian AI ventures fail during technical due diligence simply because their founding developers never executed formal intellectual property (IP) assignment contracts, leaving critical algorithm ownership ambiguous. We synthesized our battle-tested operational documents into a standardized legal framework that immunizes startups against cap-table paralysis, IP disputes, and costly statutory filing penalties.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Inspect DBERT Corporate Registration &rarr;</Link>
              <Link href="/startups/services/equity/term-sheets" className="accent-link text-xs font-mono font-medium">Review Annotated Venture Term Sheets &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — CORPORATE &amp; STATUTORY MILESTONES</div>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Building2 aria-hidden="true" /></span>
              <h3 className="accent-note">Incorporation Mastery</h3>
              <p className="text-sm">Complete end-to-end management of SPICe+ Private Limited or LLP establishment, MCA compliance, and tax registers.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><BadgeCheck aria-hidden="true" /></span>
              <h3 className="accent-note">Startup India Recognition</h3>
              <p className="text-sm">Onboard with DPIIT registry and MSME portals to secure official startup recognition and income tax exemptions.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><FileText aria-hidden="true" /></span>
              <h3 className="accent-note">Hardened IP Contracts</h3>
              <p className="text-sm">Access standardized AI developer NDAs, 4-year founder vesting agreements, and recognized SAFE note contracts.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Core Deliverables (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — LEGAL FRAMEWORK DELIVERABLES</div>
        <h2 className="section-title mb-4">
          The Legal Foundation That Scales with Your Growth
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. Business Incorporation
            </h4>
            <p className="prose-sm text-muted">
              We assist with drafting strict MOA/AOA charter instruments, executing integrated SPICe+ MCA filings, securing DIN and DSC tokens, and registering local PAN and GST numbers.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Private Limited Company &amp; LLP incorporations</li>
              <li>&bull; DIN &amp; DSC Class-3 digital token generation</li>
              <li>&bull; Integrated PAN, TAN &amp; GST tax registration filings</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. Statutory Benefit Registrations
            </h4>
            <p className="prose-sm text-muted">
              We navigate complex Government of India programs, executing DPIIT registration to secure official Startup India status, 3-year income tax holidays, and MSME Udyam benefits.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Official DPIIT Startup India recognition applications</li>
              <li>&bull; MSME Udyam certificate incorporation records</li>
              <li>&bull; Section 80-IAC tax holiday &amp; patent rebate guidance</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. AI Contract &amp; IP Drafting
            </h4>
            <p className="prose-sm text-muted">
              Protect your neural models and datasets. We draft explicit founder vesting agreements, employee NDAs, proprietary software licensing terms, and convertible SAFE structures.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; 4-year founder equity vesting agreements with cliffs</li>
              <li>&bull; Customized AI weights &amp; dataset IP assignment NDAs</li>
              <li>&bull; Standard Indian SAFE note &amp; valuation agreements</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Risk Mitigation */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — LEGAL RISK MITIGATION &amp; AUDITABILITY</div>
        <h2 className="section-title mb-2">Immunizing Against Early Legal Fatalities</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Unforced legal errors—from undefined co-founder equity splits to unlicensed third-party scraping scripts—can kill multi-million dollar acquisitions. We build defensible legal bulkheads.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Cap Table Integrity Defense</h4>
            <p className="text-xs text-muted">
              By enforcing clear equity cliff thresholds and milestone-contingent share issuances, we ensure your cap table remains clean, transparent, and institutionally investable throughout subsequent seed and Series A valuation rounds.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">AI Dataset Copyright Compliance</h4>
            <p className="text-xs text-muted">
              We conduct preemptive procedural reviews of your web data pipelines and open-source model licenses (MIT, Apache 2.0, Llama Community) to ensure your deployed conversational systems remain safe from copyright infringement litigation.
            </p>
          </div>
        </div>
      </div>

      {/* Pricing & Incubation Engagement Structures */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — COMMERCIAL LEGAL PACKAGES &amp; TIERING</div>
        <h2 className="section-title mb-2">Transparent Legal Structuring Fees</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Access specialized startup legal execution through affordable flat-fee service packages or fully bundled within our equity-based venture studio incubation agreements.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Core Incorporation</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹25,000 <span className="text-xs text-muted font-normal">flat fee</span></div>
              <p className="text-xs text-muted mt-2">Complete end-to-end Private Limited or LLP company incorporation including government statutory filing charges.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>SPICe+ MCA forms, DIN, DSC &amp; PAN/GST</li>
                <li>Standardized MOA &amp; AOA charter creation</li>
                <li>Free MSME Udyam registration assistance</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Request Incorporation &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Complete Protection</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Venture Legal Suite</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹60,000 <span className="text-xs text-muted font-normal">package</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive legal scaffolding for high-growth AI startups preparing for external investor pitching.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>DPIIT Startup India tax recognition onboarding</li>
                <li>Custom 4-year founder equity vesting agreements</li>
                <li>AI developer IP assignment NDAs &amp; SAFE notes</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-primary w-full mt-4">Inquire Legal Suite &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Incubated Venture</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Included</div>
              <p className="text-xs text-muted mt-2">Full corporate entity formation and continuous contractual guidance bundled directly into DBERT equity incubation.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>0% out-of-pocket professional service fees</li>
                <li>Continuous investor term sheet auditing</li>
                <li>Co-development engineering &amp; legal harmony</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-outline w-full mt-4">Apply For Incubation &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 07 — REGISTRATION PIPELINE WORKFLOW</div>
          <h2 className="subsection-title mb-4">
            Our Corporate Registration Pipeline
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — LEGAL KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED INCUBATION SERVICES &amp; HUBS</div>
        <h2 className="section-title mb-4">Explore Complementary Venture Services</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Annotated Term Sheets</h4>
            <p className="text-xs text-muted mb-3">Inspect detailed venture capital term sheet templates for Indian founders with clause-by-clause breakdowns.</p>
            <Link href="/startups/services/equity/term-sheets" className="accent-link text-xs">View Term Sheets &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Equity-Based Incubation</h4>
            <p className="text-xs text-muted mb-3">Learn how our bilateral software co-development model works—what we deliver, what we take, and what you keep.</p>
            <Link href="/startups/services/equity" className="accent-link text-xs">View Equity Incubation &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Technical Architecture Build</h4>
            <p className="text-xs text-muted mb-3">Connect legal protection directly to production engineering squads writing code for your core AI product.</p>
            <Link href="/startups/services/technical" className="accent-link text-xs">View Technical Service &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Primary BG) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 10 — INITIATE CORPORATE ONBOARDING</div>
        <div className="bento-card callout">
          <h2 className="card-title">Build on a Rock-Solid Legal Foundation</h2>
          <p className="page-lede">
            Ready to secure Private Limited incorporations, register with Startup India, and draft IP protection agreements? Apply for DBERT Incubation today.
          </p>
          <Link href="/startups/register" className="btn btn-primary btn-lg mt-4">Register Your Startup &rarr;</Link>
        </div>
      </div>
    </div>
  );
}

