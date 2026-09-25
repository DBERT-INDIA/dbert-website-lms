import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import Reveal from '@/components/ui/Reveal';
import s from '../startups.module.css';

export const metadata = pageMetadata('/startups/services');

const services = [
  {
    href: '/startups/services/technical',
    title: 'Technical Architecture & MVP Build',
    description: 'Carrier-grade system design, PostgreSQL pgvector RAG indexes, localized Ollama serving, and the dedicated senior AI engineering squad that commits production code to your repo.',
    tag: 'Engineering Studio'
  },
  {
    href: '/startups/services/equity',
    title: 'Equity-Based Venture Incubation',
    description: 'How our bilateral co-development model works: exchange fair milestone-linked equity tranches (2-8%) for comprehensive 90-day software execution without burning seed cash.',
    tag: 'Core Incubation'
  },
  {
    href: '/startups/services/equity/term-sheets',
    title: 'Annotated Legal Term Sheets',
    description: 'Definitive Indian venture investment and co-development term sheet templates, featuring plain-language clause-by-clause annotations to eliminate legal deadlock.',
    tag: 'Legal Open Source'
  },
  {
    href: '/startups/services/funding',
    title: 'Funding Readiness & Micro-Grants',
    description: 'Access non-dilutive milestone micro-grants ranging from ₹50,000 to ₹5,00,000 to subsidize compute servers, optimize pitch narratives, and format institutional data rooms.',
    tag: 'Capital & Grants'
  },
  {
    href: '/startups/services/hiring',
    title: 'Venture Talent & Hiring Support',
    description: 'Audit our directory of 1,500+ pre-vetted AI developers and run zero-cost 15-day technical alignment sprints directly on your codebase with 0% recruitment commission fees.',
    tag: 'Zero Commission'
  },
  {
    href: '/startups/services/infrastructure',
    title: 'Cloud & AI Server Infrastructure',
    description: 'Hardened zero-trust Virtual Private Cloud (VPC) design, bare-metal GPU cluster provisioning, reverse proxy rate-limiting, and automated database backup scaling.',
    tag: 'Infrastructure'
  },
  {
    href: '/startups/services/legal',
    title: 'Legal & IP Compliance Advisory',
    description: 'End-to-end corporate structuring: execute SPICe+ Private Limited incorporations, deploy founder equity vesting contracts with cliffs, and register for DPIIT Startup India tax holidays.',
    tag: 'Statutory Defense'
  },
  {
    href: '/startups/investor-network',
    title: 'Venture Investor & Angel Network',
    description: 'Warm, direct intro referral pathways connecting validated portfolio founders with active Indian technology angel investors and early-stage institutional AI venture funds.',
    tag: 'Capital Syndicate'
  },
];

const faqs = [
  {
    question: 'What differentiates DBERT Incubation Services from traditional startup accelerators or dev agencies?',
    answer: 'Traditional startup accelerators provide generalist mentoring lectures, communal desk space, and networking while taking substantial equity. External outsourcing software agencies build fragile demonstration prototypes designed to burn billing hours without ongoing accountability. DBERT functions as an industrial venture studio: our senior full-stack AI engineers actually code, test, and commit resilient carrier-grade production software directly into your git repository under aligned equity or transparent milestone structures.'
  },
  {
    question: 'Can founders engage individual technical or legal services without entering full equity incubation?',
    answer: 'Yes. While active incubated startup ventures receive our complete suite of engineering, legal, hiring, and grant support natively bundled into an equity co-development structure (2-8%), independent tech founders can also procure standalone architectural audits, SPICe+ incorporations, VPC server deployments, or hiring alignment sprints via fixed, transparent commercial fee retainers.'
  },
  {
    question: 'How do DBERT non-dilutive micro-grants work alongside technical co-development?',
    answer: 'We deploy non-dilutive milestone micro-grants ranging from ₹50,000 to ₹5,00,000 to active portfolio startups. These grants take zero equity dilution and are directly allocated to cover essential operational technical overhead—such as AWS bare-metal GPU instances, domain registrations, and vector database hosting—preserving your liquid pre-seed cash reserves for operational runway.'
  },
  {
    question: 'What is the operational timeline for moving from initial application to live engineering code commits?',
    answer: 'Once a startup application passes our technical due diligence review and bilateral term sheets are executed, our venture engineering practice begins daily repository code commits and container provisioning within 7 working days. Comprehensive production MVP builds typically launch within a 90-day operational sprint cycle.'
  },
  {
    question: 'How do you guarantee total IP ownership and candidate developer competence during team expansion?',
    answer: '100% of all authored software code, algorithmic database schemas, custom fine-tuned weights, and legal documentation belong exclusively to your corporate entity upon milestone execution. Furthermore, startups access our audited pool of 1,500+ DBERT learners with 0% recruitment commission fees, verified via cryptographic SHA-256 achievement serial IDs.'
  }
];

export default function StartupServicesHubPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Labs Venture Studio & Incubation Services Suite',
        serviceType: 'AI Venture Incubation, Software Co-Development, Cloud GPU Infrastructure, Startup Legal Structuring',
        description: 'Comprehensive technical, legal, financial, and talent incubation services for high-growth Indian AI startup founders. Senior engineering squads commit production code directly to founder repositories.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'AggregateOffer',
          priceCurrency: 'INR',
          lowPrice: '0',
          highPrice: '125000',
          offerCount: services.length,
          description: 'Available via milestone equity exchange (2% to 8% equity) or flat-fee specialized venture sprints'
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

      <section className="section">
        <div className="wrap">
          <Reveal className="section-head">
            <div className="doclabel">
              § 01 — VENTURE SERVICES HUB <span className="rev">rev: 2026.2</span>
            </div>
            <h1>What an Incubated Startup Actually Gets</h1>
            <p className="lede-wide text-muted">
              Incubation at DBERT Labs is a concrete engineering and operational engagement—never an ambiguous consulting arrangement. These are the mandatory professional workstreams we execute for portfolio pioneers, each commanded by the identical AI engineering leaders and researchers who build and run our internal enterprise platforms.
            </p>
          </Reveal>

          {/* How We Partner With Founders */}
          <Reveal className="section-breath border-t border-line" as="div">
            <div className="doclabel mb-2">§ 02 — THE CO-DEVELOPMENT APPROACH</div>
            <h2>Built For Founders Who Need Real Engineering</h2>
            <p className="body-copy mb-6 max-w-3xl">
              Many early-stage founders lose precious runway paying outsourced agencies for brittle prototypes that fail under real customer traffic. We operate as an aligned technical partner: our engineering squad writes, reviews, and deploys production software in exchange for a milestone-linked equity stake.
            </p>
            <div className="card card-lift my-6">
              <span className="doclabel text-xs mb-1">§ CODEBASE INTEGRITY</span>
              <h3 className="card-title mt-2">100% Code Ownership · Direct Git Commits</h3>
              <p className="body-copy mt-2">
                We commit directly to your company repositories. Every pull request is reviewed and documented, ensuring your team has full intellectual property rights, zero vendor lock-in, and audit-ready architectures for future institutional diligence.
              </p>
              <div className="mt-4 pt-3 border-t border-line stack-h gap-4 flex-wrap">
                <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Our Credentials &rarr;</Link>
                <Link href="/startups/services/equity/term-sheets" className="accent-link text-xs font-mono font-medium">Inspect Open-Source Term Sheets &rarr;</Link>
              </div>
            </div>
          </Reveal>

          {/* Services Grid Section */}
          <div className="section-breath border-t border-line">
            <div className="doclabel mb-4">§ 03 — INCUBATION WORKSTREAM CATALOG</div>
            <div className={`${s.serviceIndexGrid} stagger-grid`}>
              {services.map((service) => (
                <Reveal key={service.href} as="div">
                  <Link href={service.href} className="card card-lift flex flex-col justify-between h-full">
                    <div>
                      <span className="tag-chip mb-3">{service.tag}</span>
                      <h3 className="card-title my-2">{service.title}</h3>
                      <p className="text-xs text-muted leading-relaxed">{service.description}</p>
                    </div>
                    <div className="mt-6 pt-4 border-t border-line stack-h justify-between align-center text-xs font-mono text-accent">
                      <span>Inspect Scope</span>
                      <span aria-hidden="true">&rarr;</span>
                    </div>
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>

          {/* Commercial & Engagement Structures Overview */}
          <Reveal className="section-breath border-t border-line" as="div">
            <div className="doclabel mb-2">§ 04 — ENGAGEMENT TRACKS</div>
            <h2>Transparent Partnership Paths</h2>
            <p className="body-copy mb-6 max-w-2xl">
              Choose between comprehensive equity co-development structured to preserve cash or targeted standalone engineering sprints for defined deliverables.
            </p>
            <div className="bento-grid-3 my-6">
              <div className="card card-lift flex flex-col justify-between">
                <div>
                  <span className="doclabel">§ EQUITY TRACK</span>
                  <h3 className="card-title my-2">Venture Incubation</h3>
                  <div className="font-mono text-sm text-signal font-semibold mb-2">2% &ndash; 8% Milestone Equity</div>
                  <p className="text-xs text-muted mt-2">Production software co-development, architectural audits, and MLOps maintenance without out-of-pocket development retainers.</p>
                  <ul className="feature-list mt-4 text-xs text-muted">
                    <li>Dedicated full-stack AI engineering squad</li>
                    <li>Structured 90-day build to production launch</li>
                    <li>Direct access to senior architecture review</li>
                  </ul>
                </div>
                <div className="mt-6">
                  <Link href="/startups/register" className="btn btn-primary btn-block">Apply For Incubation &rarr;</Link>
                </div>
              </div>

              <div className="card card-lift flex flex-col justify-between">
                <div>
                  <span className="doclabel">§ STANDALONE SPRINTS</span>
                  <h3 className="card-title my-2">Feature &amp; VPC Hardening</h3>
                  <div className="font-mono text-sm text-signal font-semibold mb-2">Scope-Based Retainer</div>
                  <p className="text-xs text-muted mt-2">Targeted engineering and architecture execution packages for operating tech ventures requiring dedicated assistance.</p>
                  <ul className="feature-list mt-4 text-xs text-muted">
                    <li>pgvector retrieval &amp; semantic RAG setups</li>
                    <li>Sovereign localized model containers (Ollama/vLLM)</li>
                    <li>IAM role security &amp; private VPC integration</li>
                  </ul>
                </div>
                <div className="mt-6">
                  <Link href="/about/contact" className="btn btn-outline btn-block">Inquire About Sprints &rarr;</Link>
                </div>
              </div>

              <div className="card card-lift flex flex-col justify-between">
                <div>
                  <span className="doclabel">§ TALENT PLACEMENT</span>
                  <h3 className="card-title my-2">Venture Talent Onboarding</h3>
                  <div className="font-mono text-sm text-signal font-semibold mb-2">Zero Recruitment Commission</div>
                  <p className="text-xs text-muted mt-2">Access our verified AI developer talent directory for active incubated ventures with verified code portfolios.</p>
                  <ul className="feature-list mt-4 text-xs text-muted">
                    <li>Direct candidate code inspection on GitHub</li>
                    <li>Evaluated PR history from live sprint codebases</li>
                    <li>Cryptographically verifiable SHA-256 credentials</li>
                  </ul>
                </div>
                <div className="mt-6">
                  <Link href="/startups/services/hiring" className="btn btn-outline btn-block">Explore Venture Talent &rarr;</Link>
                </div>
              </div>
            </div>
          </Reveal>

          {/* Frequently Asked Questions Section */}
          <Reveal className="my-12 pt-8 border-t border-line" as="div">
            <div className="doclabel mb-2">§ 05 — INCUBATION KNOWLEDGE BASE</div>
            <h2 className="text-2xl font-mono font-bold text-white mb-4">Frequently Asked Questions</h2>
            <div className="measure">
              <FAQAccordion items={faqs} />
            </div>
          </Reveal>

          {/* Related Solutions Mesh */}
          <Reveal className="my-12 pt-8 border-t border-line" as="div">
            <div className="doclabel mb-2">§ 06 — RELATED ACADEMY SOLUTIONS &amp; HUBS</div>
            <h2 className="text-2xl font-mono font-bold text-white mb-4">Explore Complementary DBERT Divisions</h2>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="card p-4 bg-card border border-line">
                <h4 className="font-mono text-sm font-bold text-white mb-1">Industrial AI Training</h4>
                <p className="text-xs text-muted mb-3">Explore our core apprentice training cohorts where engineers construct production RAG and LLM infrastructures.</p>
                <Link href="/learners" className="accent-link text-xs">Explore Learners Hub &rarr;</Link>
              </div>
              <div className="card p-4 bg-card border border-line">
                <h4 className="font-mono text-sm font-bold text-white mb-1">Commercial AI Solutions</h4>
                <p className="text-xs text-muted mb-3">Deploy air-gapped enterprise product tools including DBERT Chat, Document AI, and Hiring Automation Suite.</p>
                <Link href="/ai-solutions/products" className="accent-link text-xs">View Products Suite &rarr;</Link>
              </div>
              <div className="card p-4 bg-card border border-line">
                <h4 className="font-mono text-sm font-bold text-white mb-1">Private LLM Hosting</h4>
                <p className="text-xs text-muted mb-3">Inspect physical bare-metal hardware enterprise arrays designed for mathematical customer operational secrecy.</p>
                <Link href="/ai-solutions/llm-training/private-hosting" className="accent-link text-xs">View Private Hosting &rarr;</Link>
              </div>
            </div>
          </Reveal>

          {/* CTA Block */}
          <Reveal className="mt-12 pt-8 border-t border-line">
            <div className="doclabel mb-2">§ 07 — INITIATE INCUBATION APPLICATION</div>
            <div className="bento-card callout p-8 bg-zinc-900 border border-line text-center rounded-lg">
              <h2 className="text-3xl font-mono font-bold text-white mb-3">Build Together. Launch Faster. Own the Outcome.</h2>
              <p className="text-sm text-muted max-w-2xl mx-auto mb-6">
                Ready to partner with senior AI engineering squads, bypass early cash-burn barriers, unlock non-dilutive compute grants, and ship a production MVP in 90 days? Apply for DBERT Venture Incubation today.
              </p>
              <Link href="/startups/register" className="btn btn-primary btn-lg inline-flex align-center gap-2">
                Apply for Incubation{' '}
                <span className="arr" aria-hidden="true">
                  →
                </span>
              </Link>
            </div>
          </Reveal>
        </div>
      </section>
    </div>
  );
}

