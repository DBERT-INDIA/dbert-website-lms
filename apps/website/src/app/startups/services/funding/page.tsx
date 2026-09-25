import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import { ChartColumn, Handshake, Wallet, ShieldCheck, TrendingUp, Award } from 'lucide-react';

export const metadata = pageMetadata('/startups/services/funding');

export default function FundingServicePage() {
  const steps = [
    { number: '01', title: 'Milestone Definition & Audit', description: 'We partner with startup founders to map verifiable engineering milestones (RAG deployment, live user load, beta metrics) aligned with non-equity micro-grant distribution tranches.' },
    { number: '02', title: 'Pitch Deck & Valuation Prep', description: 'We refine your investment narrative, construct defensible cap-table dilution models, and format institutional technical data rooms.' },
    { number: '03', title: 'Venture & Angel Referrals', description: 'Upon milestone verification, we execute warm introductory referrals directly to active Indian tech angel syndicates and early-stage AI venture funds.' }
  ];

  const faqs = [
    {
      question: 'Do we have to give up corporate equity in exchange for DBERT non-equity micro-grants?',
      answer: 'Zero equity is taken for our micro-grant disbursements. DBERT micro-grants ranging from ₹50,000 to ₹5,00,000 are purely non-dilutive capital allocations designed to subsidize initial GPU compute rentals, domain setups, and production hosting costs for qualified incubated startups.'
    },
    {
      question: 'What qualifies a portfolio startup to unlock progressive micro-grant payment tranches?',
      answer: 'Micro-grants are linked to verifiable technical execution rather than theoretical business projections. Tranches open as our co-development engineering squads meet defined architectural milestones—such as deploying a live pgvector indexing register, achieving sub-100ms API inference latency, or onboarding your first 100 enterprise trial users.'
    },
    {
      question: 'How do you structure warm referrals to active technology angel investors and venture capitalists?',
      answer: 'We reject bulk mail merges and blind LinkedIn blasting. When your AI product reaches verified deployment stability, DBERT engineering partners conduct direct introduction calls with curated active tech investors from our proprietary venture network who understand technical AI architecture.'
    },
    {
      question: 'Can you assist founders in preparing financial projections and dilution cap table scenarios?',
      answer: 'Yes. Our financial modeling mentors work directly with you to construct mathematically rigorous pro-forma financial models, burn-rate runway forecasts, and SAFE note cap-table dilution scenarios that survive scrutiny from tier-1 institutional due diligence teams.'
    },
    {
      question: 'What items belong in a complete institutional technical data room prior to raising pre-seed capital?',
      answer: 'An institutional-grade AI technical data room must include GitHub codebase architecture diagrams, executed founder IP assignment NDAs, open-source model license compliance schedules (MIT, Apache 2.0), historical database latency benchmarks, and verified third-party cloud hosting vulnerability assessments.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Venture Funding Readiness & Non-Dilutive Micro-Grants',
        serviceType: 'Startup Grants, Pitch Deck Optimization, Angel & VC Introductions, Cap Table Advisory',
        description: 'Access non-equity micro-grants up to ₹5,00,000, institutional pitch deck formatting, technical data room curation, and direct referrals to Indian tech angel syndicates.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Venture Studio Capital Support',
          price: '0',
          priceCurrency: 'INR',
          description: 'Non-dilutive micro-grants from ₹50,000 to ₹5,00,000 and zero fee capital referral assistance for incubated portfolio ventures',
          url: 'https://dbert.online/startups/services/funding'
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
          § 01 — VENTURE FUNDING SERVICE <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Fuel Your AI Growth from Day One &mdash; Dilution-Free
        </h1>
        <p className="lede-wide">
          De-risk your earliest product development sprints without surrendering early equity to predatory pre-seed syndicates. Access DBERT&apos;s non-dilutive milestone micro-grants ranging from ₹50,000 to ₹5,00,000, assemble bulletproof technical data rooms, and connect directly with active tech angel networks.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Funding Real Industrial Research &amp; AI Builds</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we stand by a stringent operational tenet: <strong>we allocate our own venture reserves and test operational financing models internally before presenting them to founders</strong>. Our Funding Readiness practice was born from our direct experiences financing scalable internal product lines like DBERT Chat and Document AI through sustainable bootstrap engineering rather than premature venture dilution.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              We repeatedly witnessed promising AI entrepreneurs compromising 30% of their enterprise valuation to early informal syndicates simply to pay for AWS GPU compute credits and initial server infrastructure. By establishing non-dilutive micro-grants directly linked to engineering production commits within our incubation studio, we provide the essential bridge capital required to achieve working product prototypes prior to institutional pitch valuation meetings.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/startups/investor-network" className="accent-link text-xs font-mono font-medium">Explore Investor &amp; Angel Network &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Our Corporate Grant Legitimacy &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — CAPITAL BENCHMARKS &amp; ASSURANCES</div>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Wallet aria-hidden="true" /></span>
              <h3 className="accent-note">₹5,00,000 Grants</h3>
              <p className="text-sm">Access milestone-based non-dilutive micro-grants to offset server infrastructure, GPU VRAM rentals, and cloud database bills.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Handshake aria-hidden="true" /></span>
              <h3 className="accent-note">Direct Angel Access</h3>
              <p className="text-sm">Warm introductory referrals to active technology angel networks, family offices, and early-stage VC funds focused on AI.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><ChartColumn aria-hidden="true" /></span>
              <h3 className="accent-note">Valuation Advisory</h3>
              <p className="text-sm">Specialist guidance in shaping cap tables, drafting Indian SAFE note structures, and financial runway modeling.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Core Deliverables (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — FUNDING READINESS DELIVERABLES</div>
        <h2 className="section-title mb-4">
          The Capital Runway &amp; Narrative You Need to Scale
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. Non-Dilutive Micro-Grants
            </h4>
            <p className="prose-sm text-muted">
              DBERT allocates targeted non-equity micro-grants to incubated portfolio companies to directly absorb initial development expenses and compute hosting invoices.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Non-equity grants ranging from ₹50,000 to ₹5,00,000</li>
              <li>&bull; Milestone tranches tied directly to software deployments</li>
              <li>&bull; 100% focused on compute hosting &amp; database expenses</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. Technical Pitch Optimization
            </h4>
            <p className="prose-sm text-muted">
              We refine your investor communications. We transform technical jargon into clear value metrics, mapping architecture summaries and target user unit economics to investor standards.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; RAG pipeline &amp; AI system architecture diagrams</li>
              <li>&bull; Unit economic profit model &amp; CAC/LTV auditing</li>
              <li>&bull; Professional institutional deck &amp; Executive Summary formatting</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. Institutional Data Rooms
            </h4>
            <p className="prose-sm text-muted">
              Bypass prolonged due diligence delays. We establish complete electronic data rooms containing clean Git histories, corporate filings, IP assignments, and SAFE agreements.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Pre-curated technical &amp; architectural audit records</li>
              <li>&bull; Cap table modeling with dilution scenario forecasts</li>
              <li>&bull; Verified DPIIT Startup India &amp; statutory compliance proofs</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Risk Mitigation */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — CAPITAL &amp; DILUTION RISK MITIGATION</div>
        <h2 className="section-title mb-2">Immunizing Against Early Financing Pitfalls</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Accepting early seed capital under unstructured convertible notes or predatory preference covenants can severely limit your future Series A institutional options. We build financial defenses.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Anti-Dilution Cap Protection</h4>
            <p className="text-xs text-muted">
              We simulate subsequent investment rounds using advanced cap-table modeling software—identifying potential dilution traps, unratcheted liquidation preferences, and board seat imbalances before you sign binding terms.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Audit-Proof Expense Registers</h4>
            <p className="text-xs text-muted">
              Micro-grant accounting is maintained within transparent, auditable expense registers. When external funds perform corporate forensic reviews, every rupee spent on servers and compute architecture is cleanly verified against vendor receipts.
            </p>
          </div>
        </div>
      </div>

      {/* Pricing & Incubation Engagement Structures */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — CAPITAL SUPPORT PACKAGES &amp; TIERING</div>
        <h2 className="section-title mb-2">Transparent Venture Funding Tracks</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Select between non-dilutive grant tracks bundled within DBERT technical incubation or specialized standalone advisory engagements for external pitching.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Incubated Venture</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹5,00,000 <span className="text-xs text-muted font-normal">max grant</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive non-equity micro-grants bundled natively into active DBERT equity-based venture studio incubation.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>0% corporate equity dilution for grant sums</li>
                <li>Milestone-linked server infrastructure subsidies</li>
                <li>Full electronic due diligence data room creation</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-primary w-full mt-4">Apply For Incubation &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Standalone Prep</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Pitch &amp; Data Room Audit</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹35,000 <span className="text-xs text-muted font-normal">flat fee</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive 10-day audit of your investment presentation, financial projections, and technical architecture documentation.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Complete rewrite &amp; visual design of 15-slide deck</li>
                <li>Institutional cap table dilution scenario model</li>
                <li>Preparation for technical angel interrogation</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Book Pitch Audit &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Venture Syndicate</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Invite Only</div>
              <p className="text-xs text-muted mt-2">Direct warm investor introductions for vetted AI founders exhibiting documented user traction and robust unit economics.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Curated intros to active Indian angel networks</li>
                <li>Representation during valuation negotiation rounds</li>
                <li>Co-investment evaluation by DBERT venture fund</li>
              </ul>
            </div>
            <Link href="/startups/investor-network" className="btn btn-outline w-full mt-4">Explore Syndicate &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 07 — FUNDING WORKFLOW</div>
          <h2 className="subsection-title mb-4">
            Our Capital Referral &amp; Grant Pipeline
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — FUNDING KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED INCUBATION SERVICES &amp; PRODUCTS</div>
        <h2 className="section-title mb-4">Explore Complementary Venture Services</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Investor Network Hub</h4>
            <p className="text-xs text-muted mb-3">Discover our direct referral pathways to technology angel syndicates and institutional venture capital funds.</p>
            <Link href="/startups/investor-network" className="accent-link text-xs">View Investor Network &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Annotated Term Sheets</h4>
            <p className="text-xs text-muted mb-3">Review standardized venture investment term sheet templates with transparent plain-language explanations.</p>
            <Link href="/startups/services/equity/term-sheets" className="accent-link text-xs">View Term Sheets &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Legal &amp; IP Compliance</h4>
            <p className="text-xs text-muted mb-3">Secure Private Limited incorporations, execute founder vesting schedules, and register with DPIIT Startup India.</p>
            <Link href="/startups/services/legal" className="accent-link text-xs">View Legal Service &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Primary BG) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 10 — SUBMIT FUNDING APPLICATION</div>
        <div className="bento-card callout">
          <h2 className="card-title">Turn Your Vision into a Funded Reality</h2>
          <p className="page-lede">
            Ready to secure dilution-free milestone micro-grants, structure bulletproof technical data rooms, and connect with active VC networks? Apply for DBERT Incubation today.
          </p>
          <Link href="/startups/register" className="btn btn-primary btn-lg mt-4">Register Your Startup &rarr;</Link>
        </div>
      </div>
    </div>
  );
}

