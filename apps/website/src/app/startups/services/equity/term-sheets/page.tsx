import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../../startups.module.css';

export const metadata = pageMetadata('/startups/services/equity/term-sheets');

export default function TermSheetsPage() {
  const faqs = [
    {
      question: 'Why does DBERT prefer advisory shares (FAST) over early priced equity rounds?',
      answer: 'Executing a formal priced equity valuation or shareholder formalization across Indian corporate legal jurisdictions (MCA/FDI compliance) can consume months of costly operational overhead. Founder Advisor Standard Template (FAST) agreements simply execute a milestone-driven advisory grant that instantly aligns engineering deliverables without complicating your early capitalization table or holding up ongoing engineering sprint velocity.'
    },
    {
      question: 'What happens to the assigned intellectual property (IP) if engineering milestones are missed?',
      answer: 'Our standardized legal contracts contain strict milestone-gated equity tranches. Every individual sprint deliverable (e.g., custom RAG pipeline deployment, vector indexing optimization, UI/UX client release) must formally pass rigorous integration criteria on your Git repository before the associated equity tranche vests. If milestones remain unfulfilled, zero equity vests and you retain complete legal rights to all contributed codebase commits up to that point.'
    },
    {
      question: 'Are DBERT term sheets legally compliant with Indian Ministry of Corporate Affairs (MCA) guidelines?',
      answer: 'Yes. Our reference frameworks are adapted specifically for Indian entities incorporated under the Companies Act (2013), seamlessly integrating with official Udyam/MSME recognition parameters, standard shareholder agreement (SHA) protection clauses, and statutory sweat equity or ESOP pool allocations.'
    },
    {
      question: 'Can we alter or modify these reference term sheet clauses with our corporate legal counsel?',
      answer: 'Absolutely. We actively encourage founders to review every section of our standardized open-source templates alongside independent corporate legal advisors. Our aim is total transparency and mutual execution speed, not rigid or predatory contractual entrapment.'
    },
    {
      question: 'How does this equity model interact with subsequent institutional VC funding rounds?',
      answer: 'DBERT advisory equity grants act as lightweight common or advisory allocations that sit alongside standard founder equity. When you transition into formal Seed or Series A financing rounds led by institutional venture funds (such as Y Combinator, Peak XV, or Blume Ventures), our equity simply converts or dilutes alongside founding shareholders according to standard industry pro-rata practices.'
    },
    {
      question: 'Is there any retrospective cash financial obligation if our enterprise pivots or shuts down?',
      answer: 'Never. We act as genuine engineering co-builders who intentionally share venture execution risk alongside you. If your startup undergoes a commercial pivot or ultimately ceases operations, the granted equity simply dissolves without any retrospective cash clawback or financial indebtedness for technical sprints performed.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Services-Against-Equity Startup Term Sheets & FAST Frameworks',
        description: 'Transparent 2%–8% services-against-equity AI startup co-development term sheet templates for Indian founders. Annotated legal clauses, milestone-gated vesting schedules, and verified FAST agreement structures.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT (Digital Blinc Education Research And Technology)',
          url: 'https://dbert.online'
        },
        areaServed: {
          '@type': 'Country',
          name: 'India'
        },
        serviceType: 'Startup Legal Agreements & Equity Venture Studio Co-Development',
        url: 'https://dbert.online/startups/services/equity/term-sheets'
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
    <div className="container pad-block">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <div className="measure-lg">
        
        {/* Header Section */}
        <div className={s.sectionHead}>
          <div className="doclabel">
            § 01 — EQUITY ARCHITECTURE <span className="rev">rev: 2026.2</span>
          </div>
          <h1 className="display-heading">Services-Against-Equity Term Sheets &amp; Legal Frameworks</h1>
          <p className={s.termsLede}>
            We reject hidden fees, opaque incubation covenants, and predatory early dilution. For qualifying AI startups across India, DBERT deploys dedicated software engineering squads, sovereign infrastructure, and validated hiring pipelines in exchange for transparent, milestone-gated equity—preserving 100% of your critical early cash runway.
          </p>
        </div>

        {/* Disclaimer Warning Card */}
        <div className={`card ${s.disclaimerCard} mb-6 border-l-4 border-amber-500`}>
          <strong className={`${s.disclaimerTitle} text-amber-400 font-mono text-xs uppercase block mb-1`}>Statutory Legal Disclaimer &amp; Notice</strong>
          <p className={`${s.disclaimerCopy} text-sm text-muted`}>
            The technical equity specifications, annotated contractual clauses, and downloadable reference term sheet templates published below are curated for structural transparency, educational analysis, and startup collaboration modeling. They do not constitute formal binding legal advice. Startup founders must independently consult qualified Indian corporate legal counsel before formally incorporating agreements or legally modifying share capital tables under the Companies Act (2013).
          </p>
        </div>

        {/* The 2% - 8% Co-Development Tier Breakdown */}
        <section className="mb-lg">
          <div className="doclabel mb-2">§ 02 — CO-DEVELOPMENT EQUITY TIERS</div>
          <h2 className="section-title mb-3">The 2% – 8% Standardized Co-Development Model</h2>
          <p className="prose-lg mb-4 text-muted">
            Our advisory equity engagements are explicitly categorized into three rigid structural tiers based directly upon engineering labor volume, compute infrastructure complexity, and dedicated sprint team duration. Every level utilizes standardized Founder Advisor Standard Template (FAST) or sweat equity shareholder structures designed to integrate without friction into subsequent institutional fundraising due diligence.
          </p>
          <div className="grid gap-4 md:grid-cols-3 my-6">
            <div className="card p-5 bg-card border border-line flex flex-col justify-between">
              <div>
                <span className="font-mono text-xs text-accent uppercase tracking-wider">Tier 1 &middot; Advisory Level</span>
                <h3 className="card-heading-lg mt-1 mb-2 text-white">2% &ndash; 3% Advisory Equity</h3>
                <p className="text-xs text-muted leading-relaxed mb-4">
                  Targeted at technical founders who possess active internal code execution squads but require experienced senior enterprise systems architecture oversite to avoid scaling bottlenecks and infrastructure security misconfigurations.
                </p>
                <ul className="list-disc pl-4 text-xs text-muted space-y-1">
                  <li>Weekly architectural codebase pull-request reviews</li>
                  <li>Vector database indexing &amp; RAG schema optimization</li>
                  <li>Direct access to our audited <Link href="/startups/services/hiring" className="ink-link">1,500+ developer hiring pool</Link></li>
                  <li>Official Udyam/MSME corporate technical audits</li>
                </ul>
              </div>
              <div className="mt-4 pt-3 border-t border-line text-right font-mono text-xs text-muted">Vesting: 2-Year (6-Month Cliff)</div>
            </div>
            
            <div className="card p-5 bg-card border-2 border-accent flex flex-col justify-between relative">
              <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Most Deployed</div>
              <div>
                <span className="font-mono text-xs text-accent uppercase tracking-wider">Tier 2 &middot; Co-Development</span>
                <h3 className="card-heading-lg mt-1 mb-2 text-white">4% &ndash; 5% Sprint Equity</h3>
                <p className="text-xs text-muted leading-relaxed mb-4">
                  Designed for pre-seed founders and domain experts who need complete zero-to-production execution of their initial minimum viable commercial AI product without spending capital on external software development agency invoices.
                </p>
                <ul className="list-disc pl-4 text-xs text-muted space-y-1">
                  <li><strong>4 to 8 week agile code engineering sprints</strong></li>
                  <li>Dedicated full-stack React/Next.js UI/UX production</li>
                  <li>Containerized MLOps server orchestration setup</li>
                  <li>Non-dilutive cloud compute seed grant eligibility</li>
                </ul>
              </div>
              <div className="mt-4 pt-3 border-t border-line text-right font-mono text-xs text-muted">Vesting: Milestone-Gated Tranches</div>
            </div>

            <div className="card p-5 bg-card border border-line flex flex-col justify-between">
              <div>
                <span className="font-mono text-xs text-accent uppercase tracking-wider">Tier 3 &middot; Venture Partner</span>
                <h3 className="card-heading-lg mt-1 mb-2 text-white">6% &ndash; 8% Venture Equity</h3>
                <p className="text-xs text-muted leading-relaxed mb-4">
                  A deeply integrated structural co-founding partnership. DBERT embeds an elite, specialized applied engineering squad managed directly by senior technical leadership to operate as your acting external AI technology organization.
                </p>
                <ul className="list-disc pl-4 text-xs text-muted space-y-1">
                  <li>Dedicated engineering squad (Applied AI Fellowship leads)</li>
                  <li>Custom LLM parameter fine-tuning on domain data</li>
                  <li>Continuous ongoing operational SLAs &amp; DevOps</li>
                  <li>Direct institutional angel investor introductions</li>
                </ul>
              </div>
              <div className="mt-4 pt-3 border-t border-line text-right font-mono text-xs text-muted">Vesting: 3-Year Strategic Alignment</div>
            </div>
          </div>
        </section>

        {/* Annotated Legal Clause Book (Magnet Resource Expansion) */}
        <section className="mb-lg">
          <div className="doclabel mb-2">§ 03 — ANNOTATED LEGAL CLAUSE BOOK</div>
          <h2 className="section-title mb-3">Critical Structural Term Sheet Clauses Explained</h2>
          <p className="prose-sm text-muted mb-6">
            Traditional venture studio covenants frequently obscure restrictive clauses within complex legal legalese. Below, we publish our core architectural clauses complete with explicit translation notes explaining why each term exists and how it actively safeguards founder rights.
          </p>
          
          <div className="space-y-6">
            
            {/* Clause 1 */}
            <div className="p-5 bg-zinc-900/60 rounded-lg border border-line">
              <div className="flex justify-between align-start mb-2">
                <h4 className="font-mono text-sm text-white font-bold">Clause 1: Milestone-Gated IP &amp; Code Assignment</h4>
                <span className="badge badge-accent font-mono text-xs">Founder Protection</span>
              </div>
              <p className="font-mono text-xs text-zinc-400 bg-zinc-950 p-3 rounded border border-zinc-800 mb-3 leading-relaxed">
                &quot;All intellectual property, proprietary source code commits, custom model weight embeddings, and algorithmic documentation authored by DBERT technical squads under this agreement shall be automatically, irrevocably, and exclusively assigned to the Startup corporate entity immediately upon validation and integration of each designated sprint milestone deliverable into the official main source control branch.&quot;
              </p>
              <p className="text-xs text-muted leading-relaxed">
                <strong>Why we structure it this way:</strong> Most traditional software agencies withhold intellectual property ownership until full financial completion invoices are settled. In an equity co-development relationship, you must hold unimpeded legal ownership over your source code at every progressive stage of growth to satisfy external investor legal due diligence and maintain technical self-reliance.
              </p>
            </div>

            {/* Clause 2 */}
            <div className="p-5 bg-zinc-900/60 rounded-lg border border-line">
              <div className="flex justify-between align-start mb-2">
                <h4 className="font-mono text-sm text-white font-bold">Clause 2: Anti-Clawback &amp; Shared Execution Risk</h4>
                <span className="badge badge-emerald font-mono text-xs">Zero Financial Risk</span>
              </div>
              <p className="font-mono text-xs text-zinc-400 bg-zinc-950 p-3 rounded border border-zinc-800 mb-3 leading-relaxed">
                &quot;In the event that the Startup commercial venture is formally concluded, restructured, or commercially unsuccessful prior to the realization of a liquidity event or public offering, DBERT expressly waives any right, option, or claim to financial recovery, retrospective labor fee conversion, or cash reimbursement for engineering development sprints rendered.&quot;
              </p>
              <p className="text-xs text-muted leading-relaxed">
                <strong>Why we structure it this way:</strong> Building innovative artificial intelligence software carries inherent algorithmic and commercial adoption risks. When we sign an incubation term sheet, we step onto your cap table as authentic co-builders—we consciously assume execution risk alongside you rather than functioning as speculative debt collectors.
              </p>
            </div>

            {/* Clause 3 */}
            <div className="p-5 bg-zinc-900/60 rounded-lg border border-line">
              <div className="flex justify-between align-start mb-2">
                <h4 className="font-mono text-sm text-white font-bold">Clause 3: Non-Interfering Governance &amp; Pro-Rata Dilution</h4>
                <span className="badge badge-blue font-mono text-xs">Cap Table Cleanliness</span>
              </div>
              <p className="font-mono text-xs text-zinc-400 bg-zinc-950 p-3 rounded border border-zinc-800 mb-3 leading-relaxed">
                &quot;Advisory Shares issued under this agreement shall constitute standard voting or non-voting common stock equivalents carrying zero blocking rights, veto authority, or preferred operational governance mandates over executive corporate decision-making. Upon the execution of subsequent priced financing rounds, DBERT equity shall subject itself to proportional pro-rata dilution identical to founding common shareholders.&quot;
              </p>
              <p className="text-xs text-muted leading-relaxed">
                <strong>Why we structure it this way:</strong> Institutional venture capital investors intensely dislike bloated early advisory covenants that attempt to preserve unrealistic anti-dilution ratchets or disruptive operational board voting vetoes. Our framework ensures your cap table remains perfectly clean, streamlined, and highly attractive for subsequent Series A lead term sheet negotiations.
              </p>
            </div>

          </div>
        </section>

        {/* Downloadable Reference Asset Section */}
        <section className={`card ${s.downloadCard} mb-lg bg-zinc-900 border-2 border-line p-6 text-center`}>
          <div className="doclabel mb-1">§ 04 — OPEN REFERENCE RESOURCE</div>
          <h3 className="card-title text-xl font-bold text-white mb-2">Download Standard India FAST Term Sheet (.PDF)</h3>
          <p className={`${s.downloadCopy} text-sm text-muted max-w-xl mx-auto mb-6`}>
            Access our open-source, non-binding reference template containing explicit vesting schedules (2-year vesting with a standard 6-month cliff), IP assignment schedules, and statutory corporate Indian definitions.
          </p>
          
          <div className="stack-h justify-center gap-4 flex-wrap">
            <Link 
              href="/startups/services/equity" 
              className={`btn btn-primary ${s.downloadBtn} stack-h align-center gap-2`}
            >
              <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              View Model Clauses Online
            </Link>
            <Link href="/blog/equity-for-services" className="btn btn-outline">
              Read Equity Engineering Deep-Dive &rarr;
            </Link>
          </div>
        </section>

        {/* Founder FAQ Section */}
        <section className="mb-lg">
          <div className="doclabel mb-2">§ 05 — LEGAL KNOWLEDGE BASE</div>
          <h2 className="section-title mb-4">Founder Term Sheet FAQ</h2>
          <div className="measure">
            <FAQAccordion items={faqs} />
          </div>
        </section>

        {/* Call to Action Footer */}
        <div className="card bg-card p-8 rounded-lg border border-line text-center">
          <div className="doclabel mb-1">§ 06 — INITIALIZE COLLABORATION</div>
          <h2 className="card-title text-xl font-bold text-white mb-2">Ready to Build With Aligned Technical Leadership?</h2>
          <p className="text-sm text-muted max-w-lg mx-auto mb-6">
            Submit your pitch deck and architecture summary today. Our senior engineering leadership evaluates incoming proposals on a weekly rolling basis.
          </p>
          <div className="stack-h gap-4 justify-center">
            <Link href="/startups/register" className="btn btn-primary">Submit Incubation Proposal &rarr;</Link>
            <Link href="/startups" className="btn btn-outline">Return to Startups Hub</Link>
          </div>
        </div>

      </div>
    </div>
  );
}

