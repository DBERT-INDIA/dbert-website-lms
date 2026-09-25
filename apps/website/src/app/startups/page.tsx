import React from 'react';
import CohortBanner from '@/components/ui/CohortBanner';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import HandNote from '@/components/ui/HandNote';
import HandDrawnArrow from '@/components/ui/HandDrawnArrow';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import s from './startups.module.css';

export const metadata = pageMetadata('/startups');

export default function StartupsLandingPage() {
  const selectionProcess = [
    { number: '01', title: 'Application Review & Repository Audit', description: 'Submit your pitch deck and MVP details outlining existing architectural bottlenecks, latency limitations, or talent gaps.' },
    { number: '02', title: 'Technical Architecture Deep-Dive', description: 'Our engineering leadership evaluates your vector DB indexing, inference token expenditures, team composition, and runway.' },
    { number: '03', title: 'Term Sheet & Alignment Interview', description: 'Discuss transparent equity exchange structures (FAST agreement) and incubation milestones with the DBERT technical advisory board.' },
    { number: '04', title: 'Onboarding & Dedicated Sprint Squads', description: 'Sign standardized term sheets and immediately launch active 2-week agile development sprints with your assigned engineering team.' }
  ];

  const faqs = [
    { question: 'How much equity does DBERT take?', answer: 'Our standard agreements range from 2% to 8% equity in the form of Advisory Shares (FAST agreements) or standard Common Stock, depending directly on the duration of engineering sprints and infrastructure support provided.' },
    { question: 'Who owns the Intellectual Property (IP)?', answer: 'You retain 100% ownership of your proprietary Intellectual Property. Every line of code written by DBERT senior engineers or fellowship contributors for your startup is fully legally assigned to your corporate entity upon completing agreed sprint milestones.' },
    { question: 'Do you require exclusivity or board seats?', answer: 'No. Our model is purely supportive and engineering-focused. You remain entirely free to raise independent capital, engage other traditional accelerators (such as Y Combinator or Peak XV), or recruit external CTOs without interference.' },
    { question: 'What happens if the startup fails or changes direction?', answer: 'If the venture pivots or ultimately fails, the granted advisory equity simply becomes worthless. We share the execution risk alongside you as true co-developers. There is never any retrospective cash clawback for engineering sprints rendered.' },
    { question: 'How quickly can your squads deliver our initial MVP?', answer: 'Depending on domain complexity and data pipelines, typical zero-to-MVP production sprints range between 4 to 8 weeks by leveraging our pre-tested RAG scaffolding, local model weight architectures, and proven React/Next.js client frameworks.' },
    { question: 'Do you provide direct financial seed grants?', answer: 'Yes. Qualifying incubated startups can receive non-dilutive infrastructure seed grants ranging from ₹50,000 to ₹5,00,000 specifically structured to cover initial GPU hosting clusters, commercial LLM token API expenditures, and secure vector database deployments.' },
    { question: 'Can we directly hire the developers working on our codebase?', answer: 'Absolutely. We actively encourage seamless talent transitions. Incubated startups can directly extend full-time offers to proven DBERT Applied AI Fellows who have consistently shipped production features on your actual codebase.' },
    { question: 'What is the application evaluation deadline?', answer: 'We evaluate proposals on a rolling monthly cohort cycle. Ensure your proposal is submitted prior to the cohort deadline listed in the notification bar to secure priority engineering squad matching.' }
  ];

  const startupServices = [
    { title: 'Technical Assistance & Co-Development', desc: 'Enterprise product architecture consulting, modular RAG framework selection, vector database indexing, security hardening, rigorous pull-request code reviews, and containerized MLOps pipelines.', slug: 'technical' },
    { title: 'Verified Engineering Hiring Support', desc: 'Recruit pre-vetted AI software engineers directly from DBERT’s audited fellowship graduate talent pool, eliminating traditional recruitment agency fees and technical interview screening friction.', slug: 'hiring' },
    { title: 'Infrastructure Seed Funding Support', desc: 'Direct technical seed grants from ₹50,000 to ₹5,00,000 to eliminate early startup financial friction across production cloud compute, database indexing, and external LLM API budgets.', slug: 'funding' },
    { title: 'Services Against Equity (2–8%)', desc: 'Accelerate enterprise AI product development without exhausting precious pre-seed cash runway. Exchange agile code sprints and infrastructure architectures for transparent advisory shares.', slug: 'equity' },
    { title: 'Startup Term Sheet Structuring', desc: 'Access standardized, founder-friendly India term sheet templates modeled on YC SAFE and FAST architectures, with open-source reference agreements tailored for Indian corporate governance.', slug: 'equity/term-sheets' },
    { title: 'Statutory Legal & IP Compliance', desc: 'End-to-end operational legal support covering statutory MCA filings, UDYAM/MSME entity recognition, contractor IP assignment agreements, and official Startup India recognition protocols.', slug: 'legal' },
    { title: 'Private AI Infrastructure Setup', desc: 'Deploy optimized private cloud GPU clusters, configure high-throughput local open-weights LLMs via Ollama & vLLM, and secure dedicated multi-tenant VPC environments.', slug: 'infrastructure' },
    { title: 'Angel Investor Network Access', desc: 'Directly introduce validated MVP milestones and proven user retention metrics to our active syndicates of Indian angel backers, seed tier venture funds, and technical AI advisors.', slug: 'investor-network' }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT AI Venture Studio Incubation & Technical Co-Development',
        description: 'Equity-based artificial intelligence startup incubation in Delhi NCR, providing dedicated software engineering squads, sovereign infrastructure seed grants (₹50K–₹5L), and audited AI developer recruitment without cash burn.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT (Digital Blinc Education Research And Technology)',
          url: 'https://dbert.online'
        },
        areaServed: {
          '@type': 'Country',
          name: 'India'
        },
        serviceType: 'AI Startup Incubation & Technical Consulting',
        url: 'https://dbert.online/startups'
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
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <CohortBanner deadlineDate="October 15th, 2026" />
      <div className="container pad-block">
        
        {/* Hero Banner Header */}
        <div className="mb-lg">
          <div className="doclabel">
            § 01 — VENTURE STUDIO INCUBATION <span className="rev">rev: 2026.2</span>
          </div>
          <h1 className="relative inline-block">
            An AI Startup Incubator That Builds With You, For Equity
            <HandNote className="absolute -right-12 -top-6 text-lg hidden md:block" tone="blue">
              Actual code!
            </HandNote>
          </h1>
          <p className="intro-copy">
            From initial concept commits to validated production scaling — DBERT powers early-stage Indian AI founders with dedicated software engineering squads, sovereign infrastructure seed grants, and verified developer pipelines without early cash dilution.
          </p>
        </div>

        {/* Honest Disclosure / Operational Thesis Section */}
        <section className={s.section}>
          <div className="doclabel mb-2">§ 02 — HONEST DISCLOSURE: WHO THIS IS FOR (AND NOT FOR)</div>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="card border-l-4 border-emerald-500">
              <h3 className="card-heading-lg mb-2 text-emerald-400">Who Incubation Is Built For:</h3>
              <ul className="list-disc pl-5 text-sm text-muted space-y-2">
                <li><strong>Technical founders needing agile execution squads:</strong> You understand systems architecture but require immediate, reliable engineering muscle to ship frontend interfaces, data pipelines, and testing suites.</li>
                <li><strong>Domain experts with validated proprietary datasets:</strong> You possess industry-specific training workflows or distribution channels (e.g., healthcare, fintech, legal) but lack an internal MLOps team to operationalize local LLMs.</li>
                <li><strong>Pre-seed teams optimizing cash runway:</strong> You prefer conserving valuable financial reserves for customer acquisition by deploying a verified <Link href="/blog/equity-for-services" className="ink-link">services-against-equity model (2–8%)</Link> for core product engineering.</li>
              </ul>
            </div>
            <div className="card border-l-4 border-amber-500">
              <h3 className="card-heading-lg mb-2 text-amber-400">Who Should Look Elsewhere:</h3>
              <ul className="list-disc pl-5 text-sm text-muted space-y-2">
                <li><strong>Founders seeking instant cash-only VC investment:</strong> We are hands-on software developers and operational co-builders, not passive financial venture funds or speculative institutional bankers.</li>
                <li><strong>Projects without core AI/ML technical leverage:</strong> If your startup is a simple e-commerce storefront or basic agency wrap without algorithmic value differentiation, our specialized MLOps infrastructure is not a match.</li>
                <li><strong>Teams looking to outsource responsibility:</strong> We co-develop alongside dedicated founders. If you cannot attend weekly code reviews or architectural sprint alignment demos, our squads cannot operate effectively.</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Full Service Roster (8 Services) */}
        <section className={s.section}>
          <div className="doclabel mb-3">§ 03 — SPECIALIZED INCUBATION SERVICES</div>
          <h2 className="section-title mb-4">Comprehensive Operational Infrastructure</h2>
          <div className={s.serviceGrid}>
            {startupServices.map((srv, idx) => {
              const href = srv.slug === 'investor-network' 
                ? '/startups/investor-network' 
                : `/startups/services/${srv.slug}`;
              return (
                <div key={idx} className={`card ${s.serviceCard}`}>
                  <div>
                    <h3 className="card-heading-lg">{srv.title}</h3>
                    <p className="body-copy">{srv.desc}</p>
                  </div>
                  <Link href={href} className="accent-label">Explore Service Specifications &rarr;</Link>
                </div>
              );
            })}
          </div>
        </section>

        {/* Incubation Model vs Traditional Bootstrapping Comparison Table */}
        <section className={s.section}>
          <div>
            <div className="doclabel mb-2">§ 04 — ECONOMIC ARCHITECTURE</div>
            <h2>Why DBERT Venture Studio vs. Traditional Bootstrapping?</h2>
            <p className="prose-sm text-muted mb-4">An objective comparison of capital preservation, execution latency, and technical debt risk across early startup stages.</p>
          </div>
          <div className={s.tableScroll}>
            <table className={s.compareTable}>
              <thead>
                <tr>
                  <th>Execution Metric</th>
                  <th className={s.colAccent}>DBERT Venture Incubation</th>
                  <th>Traditional Cash Bootstrapping</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Early Cash Burn Rate</td>
                  <td><strong>₹0 cash expenditure</strong> on technical development &amp; infrastructure setup.</td>
                  <td className={s.colMuted}>₹15L–₹35L+ upfront on freelance agency invoices or unverified junior hiring.</td>
                </tr>
                <tr>
                  <td>Time-to-MVP Production</td>
                  <td><strong>4 to 8 weeks</strong> leveraging pre-configured RAG libraries &amp; tested boilerplate modules.</td>
                  <td className={s.colMuted}>4 to 8 months attempting to architect auth, vector DBs, and LLM pipelines from scratch.</td>
                </tr>
                <tr>
                  <td>Developer Hiring Risk</td>
                  <td><strong>Zero friction.</strong> We supply cohesive squads who have previously contributed to <Link href="/learners/fellowship" className="ink-link">audited open-source repositories</Link>.</td>
                  <td className={s.colMuted}>Severe operational risk. Early mismatched technical hires often cause complete project stalling.</td>
                </tr>
                <tr>
                  <td>Technical Debt &amp; Scaling</td>
                  <td><strong>Minimal.</strong> Continuous architecture reviews led by seasoned industry practitioners.</td>
                  <td className={s.colMuted}>High risk of brittle prototypes requiring costly end-to-end rewrites post-Seed funding.</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="mt-4 pt-3 border-t border-line stack-h justify-between align-center">
            <span className="text-sm text-muted">Want to audit our standardized legal equity documents first?</span>
            <Link href="/startups/services/equity/term-sheets" className="btn btn-outline btn-sm">Inspect India Term Sheet Templates &rarr;</Link>
          </div>
        </section>

        {/* Incubated Portfolio Strip */}
        <section className={s.section}>
          <div className={s.sectionHead}>
            <div className="doclabel mb-1">§ 05 — PROVEN CASE STUDIES &amp; PORTFOLIO</div>
            <h2>Startups Co-Engineered in the DBERT Studio</h2>
            <p className="prose-sm text-muted">Explore verified technical architecture case studies and production metrics from early-stage AI ventures built by our engineering squads.</p>
          </div>
          <div className="grid gap-6 md:grid-cols-2 mb-6">
            <div className="card">
              <span className="pill mb-2">Fintech &amp; Trading AI</span>
              <h3 className="card-heading-lg">Alkame Inc.</h3>
              <p className="body-copy text-sm text-muted mb-4">Co-developed a high-throughput algorithmic prediction pipeline for Indian equity indices with sub-millisecond execution speeds and automated data scraping.</p>
              <Link href="/startups/portfolio/alkame" className="accent-label">Inspect Alkame Technical Case Study &rarr;</Link>
            </div>
            <div className="card">
              <span className="pill mb-2">EdTech Agent Framework</span>
              <h3 className="card-heading-lg">Gayatri AI</h3>
              <p className="body-copy text-sm text-muted mb-4">Built an offline-first multi-agent classroom learning engine utilizing local quantized model weights to completely eliminate recurring external token API costs.</p>
              <Link href="/startups/portfolio/gayatri-ai" className="accent-label">Inspect Gayatri AI Architecture &rarr;</Link>
            </div>
          </div>
          <div className="stack-h justify-center">
            <Link href="/startups/portfolio" className="btn btn-outline">View Complete Incubated Portfolio Hub &rarr;</Link>
          </div>
        </section>

        {/* Selection Process Timeline */}
        <section className={s.section}>
          <div className={s.sectionHead}>
            <div className="doclabel mb-1">§ 06 — EVALUATION PIPELINE</div>
            <h2>Four-Stage Incubation Onboarding</h2>
            <p className="prose-sm text-muted">A structured, deterministic selection process engineered to align operational culture before code execution.</p>
          </div>
          <div className="measure">
            <StepTimeline steps={selectionProcess} />
          </div>
        </section>

        {/* Founder Frequently Asked Questions */}
        <section className={s.section}>
          <div className={s.sectionHead}>
            <div className="doclabel mb-1">§ 07 — INCUBATION KNOWLEDGE BASE</div>
            <h2>Founder Frequently Asked Questions</h2>
            <p className="prose-sm text-muted">Transparent operational clarifications regarding equity agreements, intellectual property assignments, and seed grants.</p>
          </div>
          <div className="measure">
            <FAQAccordion items={faqs} />
          </div>
        </section>

        {/* Proprietary Enterprise Technology Stack */}
        <section className={s.section}>
          <div className={s.sectionHead}>
            <div className="doclabel mb-1">§ 08 — PROPRIETARY SAAS ADVANTAGE</div>
            <h2>The DBERT Enterprise Technology Stack</h2>
            <p className="prose-sm text-muted">We do not just advise; we engineer production software. Incubated startup founders receive immediate enterprise access to our sovereign SaaS suites and fine-tuned local models.</p>
          </div>
          <div className={s.productGrid}>
            {[
              { title: 'DBERT Chat Console', desc: 'Secure self-hosted multi-agent conversational interface with granular enterprise token budgeting.', href: '/ai-solutions/products/dbert-chat' },
              { title: 'Document AI Engine', desc: 'High-throughput optical parsing pipeline transforming complex unstructured legal PDFs into rigid JSON schemas.', href: '/ai-solutions/products/document-ai' },
              { title: 'Certificate Verification API', desc: 'Cryptographically auditable API endpoint verifying developer LORs, academic records, and corporate credentials.', href: '/ai-solutions/products/certificate-verification-api' },
              { title: 'Hiring Automation Suite', desc: 'Autonomous applicant evaluation interface auditing live Git pull requests and algorithmic syntax proficiency.', href: '/ai-solutions/products/hiring-automation-suite' },
              { title: 'Internship Manager', desc: 'Real-time contributor metrics dashboard monitoring pull request frequency and sprint task velocity.', href: '/ai-solutions/products/intern-management-system' }
            ].map((prod, idx) => (
              <div key={idx} className={`card ${s.productCard}`}>
                <div>
                  <h3 className={s.productTitle}>{prod.title}</h3>
                  <p className={s.productDesc}>{prod.desc}</p>
                </div>
                <Link href={prod.href} className={s.productLink}>Explore SaaS Specifications &rarr;</Link>
              </div>
            ))}
          </div>
          <div className="stack-h gap-4 mt-6 justify-center">
            <Link href="/ai-solutions" className="btn btn-outline">Explore All Enterprise AI Solutions</Link>
            <Link href="/labs/research" className="btn btn-outline">Inspect DBERT Research Briefings</Link>
          </div>
        </section>

        {/* Primary Call to Action Card */}
        <div className={`card ${s.ctaCard}`}>
          <div className="doclabel mb-2">§ 09 — SUBMIT VENTURE PROPOSAL</div>
          <h2 className="card-title">Turn Your AI Architecture into a Scalable Venture</h2>
          <p className={s.ctaCopy}>
            Evaluate your technical engineering bottlenecks, specify required GPU compute parameters, and submit your venture proposal directly to the DBERT engineering advisory board today.
          </p>
          <div className="stack-h gap-4 justify-center mt-6">
            <div className="relative inline-block">
              <Link href="/startups/register" className="btn btn-primary relative z-10">Apply for Incubation &rarr;</Link>
              <div className="absolute -right-12 -top-10 z-20 pointer-events-none transform rotate-12 hidden md:block">
                <HandDrawnArrow color="var(--signal)" width={55} height={55} className="transform rotate-90" />
              </div>
              <HandNote className="absolute -bottom-8 -right-4 whitespace-nowrap text-sm hidden md:block" tone="blue">
                Submit today!
              </HandNote>
            </div>
            <Link href="/about/team" className="btn btn-ghost">Meet Technical Leadership</Link>
          </div>
        </div>
      </div>
    </>
  );
}

