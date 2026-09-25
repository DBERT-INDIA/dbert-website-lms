import React from 'react';
import Link from 'next/link';
import InvestorForm from '@/components/ui/InvestorForm';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../startups.module.css';
import { ShieldCheck, Cpu, Briefcase, TrendingUp, CheckCircle } from 'lucide-react';

export const metadata = pageMetadata('/startups/investor-network');

export default function InvestorNetworkPage() {
  const faqs = [
    {
      question: 'How does DBERT Labs technical due diligence differ from traditional angel venture screening?',
      answer: 'Traditional angel syndicates and venture capital associates evaluate startups based almost entirely on pitch slide decks, subjective TAM forecasts, and founder rhetoric. Because DBERT Labs operates an active software laboratory and venture studio, our evaluation is fundamentally deterministic and architectural. We code-audit every portfolio founder’s actual Git repository, test their database RAG semantic indexing speeds, verify their Docker container scalability, and assess real computing unit economics before ever presenting deal flow to our network.'
    },
    {
      question: 'What is the corporate fee structure for accredited investors and VCs to access DBERT deal flow?',
      answer: 'Joining the DBERT Investor Network is completely fee-free for verified accredited angel investors, seed syndicates, and institutional venture capital partners. We do not charge subscription management retainers or introductory broker surcharges to inspect deal flow. Our economic alignment derives directly from holding equity stakes (2% to 8%) in the portfolio companies we technically co-develop, ensuring our incentives are identical to incoming coinvestors.'
    },
    {
      question: 'How does DBERT studio co-development eliminate early execution failure risk for seed investors?',
      answer: 'Statistical failure across pre-seed software startups occurs primarily when non-technical founders expend their cash seed capital contracting mediocre external outsourcing agencies—resulting in architectural collapse, security breaches, or exhausted operating runways before launching an MVP. DBERT eradicates execution risk by deploying our in-house senior full-stack AI engineering squads directly into portfolio ventures under a dilution-free services-against-equity exchange, guaranteeing carrier-grade MVP deployment within a 90-day sprint.'
    },
    {
      question: 'At what valuation stages and funding milestones do investors receive portfolio introductions?',
      answer: 'We introduce portfolio founders to our investor network at two strategic inflection points: immediately upon achieving verified production technical launch (Pre-Seed/Angel rounds seeking ₹25,00,000 to ₹1,00,00,000 in early expansion capital) and post-revenue scaling milestones (Seed/Series A expansion rounds). Network investors receive exclusive proprietary access to founders before public fundraising rounds commence.'
    },
    {
      question: 'Can institutional venture capital funds refer their non-technical portfolio companies into DBERT Incubation?',
      answer: 'Yes. Active VC partners frequently refer early-stage portfolio investments suffering from computational scaling bottlenecks or hiring delays directly into our venture studio. We perform technical intervention sprints, migrate public cloud API chat wrappers to cost-optimized bare-metal RunPod hardware, and stand up proprietary local open-weights inference engines.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Investor & Angel Syndicate Network',
        serviceType: 'AI Startup Deal Flow Curation, Technical Due Diligence Verification, Seed Co-Investment Introductions',
        description: 'Exclusive deal flow introductions to technical AI startup ventures co-developed, code-audited, and deployed by DBERT Labs Venture Studio engineers.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
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
        
        {/* Hero Header Section */}
        <div className="mb-10">
          <div className="doclabel">
            § 01 — INVESTOR DEAL FLOW NETWORK <span className="rev">rev: 2026.2</span>
          </div>
          <h1 className="text-4xl font-mono font-bold text-white mb-3">
            The DBERT Investor Network &mdash; Vetted Deal Flow
          </h1>
          <p className="intro-copy text-base text-muted max-w-3xl leading-relaxed">
            We do not just incubate theoretical ideas; we construct, stress-test, and ship carrier-grade production artificial intelligence systems. Join our global syndicate of seed, angel, and institutional venture capital investors to receive exclusive proprietary introductions to AI startups technically validated and co-developed within our venture studio.
          </p>
        </div>

        {/* Born-From Origin Section (Operational Provenance) */}
        <section className="mb-12 pt-6 border-t border-line">
          <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-3">
            Built to Eliminate Technical Blindness in Venture Investing
          </h2>
          <p className="prose-sm text-muted leading-relaxed mb-6 max-w-3xl">
            At DBERT Labs, we abide by a transparent operational principle: <strong>we only present startup deal flow to our network after our in-house engineers have physically inspected, architected, and built the company&apos;s production code</strong>. The DBERT Investor Network emerged directly from observing institutional investors consistently misallocate capital into artificial intelligence startups that relied on brittle third-party API wrappers or unsustainable token compute burning models.
          </p>
          <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center my-6">
            <div className="flex-1">
              <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Co-Development Advantage</span>
              <p className="text-xs text-muted leading-relaxed mt-2">
                By investing our own senior engineering hours and bare-metal GPU server compute directly into portfolio companies under a milestone services-against-equity structure (2% to 8% equity), we acquire deep, mathematically substantiated insight into every founder&apos;s architectural competence. When our investor partners receive a deal flow briefing from DBERT, they are reviewing an asset that has already survived months of rigorous repository vetting, vector database benchmark tests, and security audits inside our internal laboratory.
              </p>
              <div className="stack-h gap-4 mt-4 flex flex-wrap gap-4">
                <Link href="/startups/services/equity" className="accent-link text-xs font-mono font-medium">Inspect Our Services-Against-Equity Terms &rarr;</Link>
                <Link href="/startups/portfolio" className="accent-link text-xs font-mono font-medium">Browse Our Incubated Startup Portfolio &rarr;</Link>
              </div>
            </div>
          </div>
        </section>

        {/* Core Value Proposition & Deal Flow Form Grid */}
        <section className="mb-14 pt-8 border-t border-line">
          <div className="doclabel mb-4">§ 03 — SYNDICATE ACCESS &amp; BENEFITS</div>
          <div className="bento-grid-2">
            <div className={`card ${s.reasonsCard} bg-card border border-line p-8 flex flex-col justify-between`}>
              <div>
                <h2 className="display-heading text-2xl font-mono font-bold text-white mb-6">Why Source from DBERT?</h2>
                <ul className={`${s.reasonList} space-y-6`}>
                  <li className="border-b border-line/50 pb-4">
                    <strong className={`${s.reasonTitle} text-emerald-400 font-mono text-sm block mb-1`}>1. Exhaustive Technical Validation</strong>
                    <span className="text-xs text-muted leading-relaxed">Every single startup in our curated portfolio has had their core system architecture, local open-weights LLM pipelines, Docker containers, and PostgreSQL pgvector RAG database schemas built or rigorously audited by our senior venture engineers.</span>
                  </li>
                  <li className="border-b border-line/50 pb-4">
                    <strong className={`${s.reasonTitle} text-emerald-400 font-mono text-sm block mb-1`}>2. Execution Risk Mitigated</strong>
                    <span className="text-xs text-muted leading-relaxed">We provide the technical squad and architectural mentorship. Startups do not collapse due to developmental bottlenecks or exorbitant recruiting agency commissions because they directly leverage the DBERT developer ecosystem.</span>
                  </li>
                  <li>
                    <strong className={`${s.reasonTitle} text-emerald-400 font-mono text-sm block mb-1`}>3. Proprietary Early Access</strong>
                    <span className="text-xs text-muted leading-relaxed">Our accredited investor network receives first-look access to validated artificial intelligence MVPs operating with verified institutional customers before they are formally marketed to public VC forums or Demo Days.</span>
                  </li>
                </ul>
              </div>
              <div className="mt-8 pt-4 border-t border-line">
                <span className="text-xs font-mono text-muted">Verification Standard: 100% Code-Audited Repositories</span>
              </div>
            </div>
            
            <div id="booking-form" className={`card ${s.formCard} bg-zinc-900 border border-line p-8 rounded-lg`}>
              <h3 className="card-title-tight text-xl font-mono font-bold text-white mb-2">Request Deal Flow Access</h3>
              <p className={`${s.formCardCopy} text-xs text-muted mb-6`}>Detail your institution&apos;s funding stage preferences and AI investment thesis; our venture engineering directors will curate direct coinvestor introductions.</p>
              
              <InvestorForm />
            </div>
          </div>
        </section>

        {/* Security Rigor & Due Diligence Methodology */}
        <section className="mb-14 pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 04 — TECHNICAL DUE DILIGENCE RIGOR</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-3">
            Our Automated Architectural Due Diligence Standards
          </h2>
          <p className="prose-sm text-muted leading-relaxed mb-6 max-w-3xl">
            Before a portfolio startup is admitted to our syndicate deal flow registry, our engineering leaders subject their technology stack to a stringent technical audit across three foundational vectors.
          </p>

          <div className="grid gap-6 md:grid-cols-3 my-6">
            <div className="card p-6 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-2">1. Unit Compute Economics</h4>
              <p className="text-xs text-muted leading-relaxed">
                We verify that model inference velocities and token execution invoices scale linearly—rejecting startups reliant on unhedged public cloud commercial API billing that deteriorates structural operating margins.
              </p>
            </div>
            <div className="card p-6 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-2">2. IP &amp; Weight Ownership</h4>
              <p className="text-xs text-muted leading-relaxed">
                We confirm complete corporate legal and statutory ownership over compiled GGUF/AWQ model weight checkpoints, proprietary historical training datasets, and automated deployment scripts.
              </p>
            </div>
            <div className="card p-6 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-2">3. Zero-Trust Cyber Zoning</h4>
              <p className="text-xs text-muted leading-relaxed">
                We audit end-to-end security posture, verifying containerized Nginx rate-limiting proxy gateways, encrypted PostgreSQL storage buffers, and strict compliance with global digital personal data protection mandates.
              </p>
            </div>
          </div>
        </section>

        {/* Coinvestment Commercial Structures */}
        <section className="mb-14 pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 05 — COINVESTMENT &amp; SYNDICATE TIERS</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-2">
            Structured Venture Collaboration Models
          </h2>
          <p className="prose-sm text-muted leading-relaxed mb-6 max-w-3xl">
            We maintain structured coinvestment pathways designed for solo angel syndicates, micro-VC seed funds, and mature enterprise institutional partners.
          </p>
          <div className="grid gap-6 md:grid-cols-3 my-6">
            <div className="card p-6 bg-card border border-line flex flex-col justify-between">
              <div>
                <span className="font-mono text-xs text-accent uppercase font-bold">Angel &amp; Micro-Syndicates</span>
                <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹25L &ndash; ₹1Cr <span className="text-xs text-muted font-normal">ticket size</span></div>
                <p className="text-xs text-muted leading-relaxed mt-2">
                  Direct introductions to pre-seed founders immediately following our 90-day technical MVP co-development sprint and initial user deployment.
                </p>
                <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                  <li>Zero syndicate introductory or management fees</li>
                  <li>Direct access to live Git repository code audit</li>
                  <li>Annotated founder term sheet transparency</li>
                </ul>
              </div>
              <Link href="/startups/services/equity/term-sheets" className="btn btn-outline w-full mt-4">Inspect Term Sheets &rarr;</Link>
            </div>

            <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
              <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Strategic Coinvestor</div>
              <div>
                <span className="font-mono text-xs text-accent uppercase font-bold">Institutional Seed VC</span>
                <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹1Cr &ndash; ₹10Cr <span className="text-xs text-muted font-normal">expansion</span></div>
                <p className="text-xs text-muted leading-relaxed mt-2">
                  Curated deal flow briefings covering post-revenue AI portfolio scaling ventures requiring institutional expansion capital and private server hosting expansion.
                </p>
                <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                  <li>Full access to real-time Grafana MLOps metrics</li>
                  <li>Direct founder meeting coordination</li>
                  <li>Ongoing studio technical squad support guaranteed</li>
                </ul>
              </div>
              <a href="#booking-form" className="btn btn-primary w-full mt-4">Connect With Venture Director &rarr;</a>
            </div>

            <div className="card p-6 bg-card border border-line flex flex-col justify-between">
              <div>
                <span className="font-mono text-xs text-muted uppercase font-bold">VC Portfolio Referral</span>
                <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Intervention Sprint</div>
                <p className="text-xs text-muted leading-relaxed mt-2">
                  VC partners can refer non-technical portfolio companies into DBERT Incubation to optimize compute costs and build local AI infrastructure.
                </p>
                <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                  <li>Migration from cloud APIs to bare-metal GPUs</li>
                  <li>70% average per-token compute cost reduction</li>
                  <li>Executed under services-against-equity or retainers</li>
                </ul>
              </div>
              <Link href="/startups/services/technical" className="btn btn-outline w-full mt-4">Inquire Technical Intervention &rarr;</Link>
            </div>
          </div>
        </section>

        {/* FAQ Accordion Section */}
        <section className="mb-14 pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 06 — INVESTOR KNOWLEDGE BASE</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-4">Frequently Asked Investor Questions</h2>
          <div className="measure">
            <FAQAccordion items={faqs} />
          </div>
        </section>

        {/* Related Venture Studio Mesh */}
        <section className="mb-12 pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 07 — RELATED STUDIO DIVISIONS &amp; LEGAL FRAMEWORKS</div>
          <h2 className="text-2xl font-mono font-bold text-white mb-4">Explore Definitive Venture Resources</h2>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="card p-4 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-1">Services-Against-Equity Track</h4>
              <p className="text-xs text-muted mb-3">Review how we invest senior software engineering squads in exchange for milestone corporate equity.</p>
              <Link href="/startups/services/equity" className="accent-link text-xs">Explore Equity Model &rarr;</Link>
            </div>
            <div className="card p-4 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-1">Compute Funding &amp; Micro-Grants</h4>
              <p className="text-xs text-muted mb-3">Discover our non-dilutive milestone compute server grants up to ₹5,00,000 designed to preserve cash runway.</p>
              <Link href="/startups/services/funding" className="accent-link text-xs">View Compute Grants &rarr;</Link>
            </div>
            <div className="card p-4 bg-card border border-line">
              <h4 className="font-mono text-sm font-bold text-white mb-1">Active Venture Portfolio</h4>
              <p className="text-xs text-muted mb-3">Browse our active commercial startups operating inside the DBERT Labs incubator ecosystem.</p>
              <Link href="/startups/portfolio" className="accent-link text-xs">Browse Startup Portfolio &rarr;</Link>
            </div>
          </div>
        </section>

        {/* Bottom Call to Action */}
        <section className="pt-8 border-t border-line">
          <div className="doclabel mb-2">§ 08 — JOIN THE NETWORK</div>
          <div className="bento-card callout p-8 bg-zinc-900 border border-line text-center rounded-lg">
            <h2 className="text-3xl font-mono font-bold text-white mb-2">Ready to Gain Access to Technically Validated Deal Flow?</h2>
            <p className="text-sm text-muted max-w-2xl mx-auto mb-6">
              Partner with DBERT Labs to invest in resilient, sovereign artificial intelligence ventures backed by verified code repositories and dedicated industrial engineering squads.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <a href="#booking-form" className="btn btn-primary btn-lg">Submit Investor Credentials &rarr;</a>
              <Link href="/startups/portfolio" className="btn btn-outline btn-lg">Review Portfolio Ventures &rarr;</Link>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
}

