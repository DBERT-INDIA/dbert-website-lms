import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import { Scale, Shield, Timer, Handshake, Cpu, CheckCircle } from 'lucide-react';

export const metadata = pageMetadata('/startups/services/equity');

export default function EquityServicePage() {
  const steps = [
    { number: '01', title: 'Scope Definition & Estimate', description: 'We analyze your target MVP architecture parameters, estimate active developer sprint requirements, and align mutually fair equity fractions.' },
    { number: '02', title: 'Bilateral Agreement Execution', description: 'We draft and execute transparent incubation agreement frameworks, establishing explicit development milestones and vesting locks.' },
    { number: '03', title: 'Sprint Execution & Launch', description: 'Our engineering squad writes, tests, and commits tested logic directly to your repositories, deploying a production MVP in 90 days.' }
  ];

  const faqs = [
    {
      question: 'How do you determine the exact equity percentage required for technical co-development?',
      answer: 'Our equity incubation scope spans between 2% and 8% depending on the complexity of the required architecture, developer sprint volume, and stage of current product maturity. Lightweight prototype refactoring lands closer to 2%, while comprehensive ground-up RAG and enterprise multi-agent application builds scale toward 6-8%.'
    },
    {
      question: 'Are there any hidden cash development retainers or consulting fees alongside the equity fraction?',
      answer: 'Zero. Under our pure equity incubation track, founders pay ₹0 in software developer sourcing, system design consulting, or architectural management fees during the defined 90-day build window. Your operating cash is wholly preserved for marketing, legal, and operational runway.'
    },
    {
      question: 'What happens if DBERT fails to deliver the committed production MVP within the 90-day window?',
      answer: 'Our equity agreements incorporate strict milestone-based vesting conditions. If our engineering practice fails to achieve agreed-upon technical release criteria or deployment specifications, our equity entitlement remains unvested and reverts to your company cap table.'
    },
    {
      question: 'Do we receive ongoing maintenance and MLOps monitoring support after the initial 90-day launch?',
      answer: 'Yes. Every equity incubation package natively bundles an additional 3 months of comprehensive post-launch MLOps optimization, server throughput monitoring, bug resolutions, and database scaling to ensure stability during initial user onboarding.'
    },
    {
      question: 'How does DBERT differ from traditional startup incubators or university entrepreneurship cells?',
      answer: 'Traditional incubators offer generalized mentoring lectures, desk space, and surface-level networking while taking substantial equity. We function as an active venture software studio: we supply senior engineering squads that actually write, test, and ship your production AI codebase.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Equity-Based AI Incubation & Technical Co-Development',
        serviceType: 'Venture Studio Incubation, Equity Co-Development, MVP Software Sprint',
        description: 'Exchange 2% to 8% equity for dedicated senior software engineering squads that design, build, and deploy production AI products in 90 days without cash burn.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Venture Incubation Equity Exchange',
          price: '0',
          priceCurrency: 'INR',
          description: 'Zero out-of-pocket development cash fees in exchange for agreed milestone-based 2% to 8% equity fraction',
          url: 'https://dbert.online/startups/services/equity'
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
          § 01 — VENTURE EQUITY SERVICE <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Launch Your AI MVP Without Burning Operating Cash
        </h1>
        <p className="lede-wide">
          Stop draining your pre-seed capital reserves on expensive dev agencies or unverified contract freelancers. We assign senior DBERT software engineering squads to design, build, and deploy your proprietary AI application in exchange for clear milestone equity fractions (2% to 8%).
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Bridging Indian Engineering to Venture Value</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we stand by a clear industrial commitment: <strong>we put our engineering labor and venture equity on the line before asking founders for trust</strong>. Our equity incubation model was created to solve a massive structural inefficiency across the Indian startup ecosystem—exceptional founders with deep domain vision often fail because early software agency development costs drain 100% of their initial operating cash before achieving product-market fit.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              We realized that as an operational industrial training academy and software studio, we possess an unprecedented advantage: direct access to India&apos;s sharpest, verified AI engineers and battle-tested infrastructure platforms. By aligning our engineering capacity with early startup equity, we create a truly win-win venture architecture—you retain your precious liquid runway, while our technical squads execute with the pride and precision of dedicated co-founders.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/startups/services/equity/term-sheets" className="accent-link text-xs font-mono font-medium">Inspect Annotated Term Sheet Templates &rarr;</Link>
              <Link href="/learners" className="accent-link text-xs font-mono font-medium">Explore Engineering Fellowships &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — INCUBATION BENCHMARKS &amp; ASSURANCES</div>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Scale aria-hidden="true" /></span>
              <h3 className="accent-note">2% &ndash; 8% Equity</h3>
              <p className="text-sm">Preserve precious pre-seed capital reserves. Exchange small, fair equity percentages for dedicated senior engineering execution.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Timer aria-hidden="true" /></span>
              <h3 className="accent-note">90-Day MVP Launch</h3>
              <p className="text-sm">Move from database designs and Figma mockups to a live production software deployment in under 3 operational months.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Shield aria-hidden="true" /></span>
              <h3 className="accent-note">3-Month MLOps Support</h3>
              <p className="text-sm">Post-launch technical assistance covers server monitoring, database index optimizations, security patches, and API scaling.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Core Deliverables (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — CO-DEVELOPMENT SCOPE &amp; DELIVERABLES</div>
        <h2 className="section-title mb-4">
          From Blueprint to Live Enterprise Product in 90 Days
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. Full-Stack AI MVP Development
            </h4>
            <p className="prose-sm text-muted">
              Our dedicated software squads architect your primary production features—developing clean modern dashboards, establishing relational databases, and writing custom AI logic.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Next.js 16 &amp; React responsive interface layouts</li>
              <li>&bull; Node.js API servers &amp; PostgreSQL pgvector schemas</li>
              <li>&bull; LangGraph, Ollama &amp; vLLM orchestration workflows</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. Hardened Legal Protections
            </h4>
            <p className="prose-sm text-muted">
              We eliminate legal ambiguity. Our incubation packages incorporate transparent standardized agreements, milestone-backed vesting schedules, and 100% IP transfer covenants.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Milestone-based vesting tied to software performance</li>
              <li>&bull; 100% immediate IP assignment upon milestone delivery</li>
              <li>&bull; Standard Indian SAFE note &amp; cap-table equity structure</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. Post-Launch MLOps Scaling
            </h4>
            <p className="prose-sm text-muted">
              We stand by our code post-launch. For 90 days after going live, DBERT system engineers monitor runtime containers, tune database queries, and manage infrastructure capacity.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Bare-metal GPU container &amp; uptime latency surveillance</li>
              <li>&bull; Algorithmic RAG token budget efficiency tuning</li>
              <li>&bull; Dedicated weekly engineering code reviews &amp; bug resolutions</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Risk Mitigation */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — TECHNICAL &amp; CORPORATE RISK MITIGATION</div>
        <h2 className="section-title mb-2">De-Risking Early Technical Execution</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Handing critical core technology creation to an external agency often leads to proprietary knowledge loss and unmaintainable code spaghetti. We operate as an aligned technical partner.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Codebase Continuity Assurance</h4>
            <p className="text-xs text-muted">
              Every feature is documented within exhaustive Git README logs, architectural ADR diagrams, and structured modular folders. If you later hire full-time internal engineering leads, handoff execution occurs without operational friction.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Milestone Performance Locks</h4>
            <p className="text-xs text-muted">
              Our equity entitlement remains legally linked to verifiable deployment milestones. You do not cede unreserved equity upfront; our ownership vests precisely as we deploy functional software features to production servers.
            </p>
          </div>
        </div>
      </div>

      {/* Pricing & Incubation Engagement Structures */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — INCUBATION TIERING &amp; EQUITY EXCHANGE</div>
        <h2 className="section-title mb-2">Transparent Equity Exchange Structures</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We tailor equity exchange percentages and milestone schedules directly to your startup&apos;s product complexity and development timeline.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Light MVP Sprint</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">2% &ndash; 4% <span className="text-xs text-muted font-normal">Equity</span></div>
              <p className="text-xs text-muted mt-2">Designed for agile AI web applicatons, automated parsing dashboards, and focused RAG search engines.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>60-day concentrated MVP delivery cycle</li>
                <li>Next.js 16 frontend &amp; PostgreSQL setup</li>
                <li>Standard 30-day post-launch support</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-outline w-full mt-4">Apply Light Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Core Track</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Full Technical Studio</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">5% &ndash; 8% <span className="text-xs text-muted font-normal">Equity</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive 90-day co-development for enterprise SaaS systems and multi-agent industrial automation platforms.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Dedicated multi-developer engineering squad</li>
                <li>90-day full-stack production architecture build</li>
                <li>90-day post-launch MLOps &amp; CI/CD support</li>
              </ul>
            </div>
            <Link href="/startups/register" className="btn btn-primary w-full mt-4">Apply Core Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Hybrid Cash + Equity</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Custom Scope</div>
              <p className="text-xs text-muted mt-2">Tailored structures combining minor operational cost retainers with reduced equity exposure (1-2%).</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Preserve cap table equity limits</li>
                <li>Cost-basis monthly engineering retainer</li>
                <li>Full venture studio team accessibility</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Discuss Hybrid Scope &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 07 — CO-DEVELOPMENT PIPELINE</div>
          <h2 className="subsection-title mb-4">
            Our Co-Development Pipeline
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — INCUBATION KNOWLEDGE BASE</div>
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
            <p className="text-xs text-muted mb-3">Review annotated legal term sheet templates with plain-language clause breakdowns for Indian startup founders.</p>
            <Link href="/startups/services/equity/term-sheets" className="accent-link text-xs">View Term Sheets &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Funding Readiness &amp; Grants</h4>
            <p className="text-xs text-muted mb-3">Access DBERT micro-grants ranging up to ₹5,00,000 to offset server costs and connect with active tech angel networks.</p>
            <Link href="/startups/services/funding" className="accent-link text-xs">View Funding Support &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Hiring &amp; Alignment Sprints</h4>
            <p className="text-xs text-muted mb-3">Filter our directory of 1,500+ DBERT learners and execute 15-day technical alignment sprints before making formal team hires.</p>
            <Link href="/startups/services/hiring" className="accent-link text-xs">View Hiring Support &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Primary BG) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 10 — SUBMIT INCUBATION APPLICATION</div>
        <div className="bento-card callout">
          <h2 className="card-title">Build Together. Launch Faster. Own the Outcome.</h2>
          <p className="page-lede">
            Ready to exchange equity for production software co-development, bypass cash-burn barriers, and launch a live MVP in 90 days? Apply for DBERT Incubation today.
          </p>
          <Link href="/startups/register" className="btn btn-primary btn-lg mt-4">Register Your Startup &rarr;</Link>
        </div>
      </div>
    </div>
  );
}

