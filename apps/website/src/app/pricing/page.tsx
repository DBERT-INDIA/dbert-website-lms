import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from './pricing.module.css';

export const metadata = pageMetadata('/pricing');

export default function PricingPage() {
  const faqs = [
    {
      question: 'Why are DBERT industrial training fees significantly lower than traditional software bootcamps?',
      answer: ' Traditional IT bootcamps rely on aggressive external marketing budgets, costly third-party recruiters, or exploitative Income Share Agreements (ISAs) that take up to 15% of your future salary for years. Because DBERT operates an active engineering venture studio and internal software laboratory, our training academy functions primarily as our internal talent incubator. We pass these operational efficiencies directly to learners through affordable, transparent flat-rate course fees with zero future salary encumbrance.'
    },
    {
      question: 'How does the services-against-equity incubation model work for early-stage AI startups?',
      answer: 'For qualified pre-seed tech founders, paying ₹10,00,000 to an outsourcing development agency typically drains their operating runway before reaching market validation. Instead, DBERT executes a bilateral co-development agreement: we commit a dedicated senior AI engineering squad, provision private cloud GPU architecture, and build your production MVP over a 90-day sprint in exchange for a modest milestone-linked corporate equity stake typically ranging between 2% and 8%.'
    },
    {
      question: 'What is the refund and cancellation policy for upskilling program enrollments?',
      answer: 'We maintain an unconditional 7-day initial transparent evaluation window. If within the first 7 calendar days of starting a DBERT Launchpad or Accelerate cohort you determine that the intensive terminal engineering curriculum does not fit your learning style, you may request and receive a full 100% refund of your course fees without interrogation.'
    },
    {
      question: 'Can enterprises procure custom AI product fine-tuning and standalone GPU sprints on a fixed-fee retainer?',
      answer: 'Yes. While active portfolio startups operate under equity co-development, mature enterprises and non-incubated companies can engage our artificial intelligence researchers for targeted architectural audits, custom Llama/Qwen model quantization, pgvector RAG indexing, and high-availability AWS/RunPod infrastructure deployments via structured flat-fee commercial retainers.'
    },
    {
      question: 'Do you provide formal tax compliance invoicing and vendor documentation for corporate sponsorship?',
      answer: 'Every financial transaction executed with DBERT Labs includes statutory GST compliance invoicing, formal MSME verified vendor onboarding documentation, and electronic expense registers suitable for corporate tuition reimbursement audits and institutional due diligence data rooms.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'WebPage',
        name: 'DBERT Labs Transparent Pricing & Venture Commercials',
        description: 'Comprehensive pricing structures for industrial software upskilling programs, startup equity incubation tracks, micro-grants, and enterprise AI engineering sprints.',
        url: 'https://dbert.online/pricing'
      },
      {
        '@type': 'OfferCatalog',
        name: 'DBERT Upskilling Academy & Venture Programs',
        itemListElement: [
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Course',
              name: 'DBERT Launchpad Program',
              description: '3-Month foundational training in Python syntax, Git version controls, Bash commands, and Ollama local LLM execution.'
            },
            price: '7999',
            priceCurrency: 'INR'
          },
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Course',
              name: 'DBERT Accelerate Program',
              description: '3-Month advanced training building 3 production AI agent modules, relational database indexing, and API connectivity.'
            },
            price: '4999',
            priceCurrency: 'INR'
          },
          {
            '@type': 'Offer',
            itemOffered: {
              '@type': 'Course',
              name: 'DBERT Fellowship (Paid)',
              description: '3-Month immersive fellowship working directly on live client repositories under senior studio engineers.'
            },
            price: '1599',
            priceCurrency: 'INR'
          }
        ]
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
        <div className="measure-lg">
          
          {/* Page Header */}
          <div className="detail-header mb-8">
            <div className="doclabel">
              § 01 — COMMERCIAL STRUCTURES <span className="rev">rev: 2026.2</span>
            </div>
            <h1 className="page-title-sm">
              Transparent, Outcome-Focused Model
            </h1>
            <p className="page-intro">
              We reject hidden tuition markups, predatory lock-ins, and ambiguous hourly billing. Explore how we structure apprentice pathways, startup co-development equity tracks, and enterprise AI sprints.
            </p>
          </div>

          {/* Deep Overview & Educational Ethos Section */}
          <section className="section-breath border-t border-line">
            <div className="doclabel mb-2">§ 02 — THE VENTURE &amp; ACADEMY FLYWHEEL</div>
            <h2>
              Software We Build in Production Informs What We Teach
            </h2>
            <p className="body-copy mb-4">
              At DBERT, we build and operate production AI software before teaching it. Because our engineering team ships live products (such as DBERT Chat and Document AI) and incubates tech ventures, our educational programs focus purely on hands-on production code, pull-request reviews, and real-world deployment architectures.
            </p>
            <div className="card card-lift my-6">
              <span className="doclabel text-xs mb-1">§ COLLABORATIVE ECOSYSTEM</span>
              <h3 className="card-title mt-2">100% Remote, Live Git Repositories</h3>
              <p className="body-copy mt-2">
                All cohort members collaborate via remote pull requests, CI/CD pipelines, and dedicated sprint reviews. Top performers can advance into live client squad sprints without recruitment middleman barriers.
              </p>
              <div className="mt-4 pt-3 border-t border-line stack-h gap-4 flex-wrap">
                <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Our Credentials &rarr;</Link>
                <Link href="/startups/services/equity" className="accent-link text-xs font-mono font-medium">Explore Services-Against-Equity Incubation &rarr;</Link>
              </div>
            </div>
          </section>

          {/* Pricing / Program Grid */}
          <section className="section-breath border-t border-line">
            <div className="doclabel mb-2">§ 03 — UPSKILLING ACADEMY TRACKS</div>
            <h2 className="mb-6">
              Industrial Training Program Tracks
            </h2>
            
            <div className={s.tierGrid}>
              {[
                { 
                  title: 'DBERT Launchpad', 
                  feeLabel: 'Curriculum & Track Intake',
                  badge: 'Foundations',
                  duration: '2 Months (8 Sprints)', 
                  audience: 'Beginners & Career Switchers',
                  desc: 'Master Python fundamentals, Git collaboration, Linux terminal commands, and containerized local LLM tool chains.',
                  href: '/learners/launchpad',
                  cta: 'Request Track Curriculum &rarr;'
                },
                { 
                  title: 'DBERT Accelerate', 
                  feeLabel: 'Curriculum & Track Intake',
                  badge: 'Production Engineering',
                  duration: '2 Months (8 Sprints)', 
                  audience: 'Intermediate Developers & Students',
                  desc: 'Build and deploy 3 production AI agent workflows, pgvector semantic indexing, live REST API backends, and earn verifiable certs.',
                  href: '/learners/accelerate',
                  featured: true,
                  cta: 'Apply for Accelerate &rarr;'
                },
                { 
                  title: 'DBERT Fellowship', 
                  feeLabel: 'Selective Stipend Cohort',
                  badge: 'Live Squad Placement',
                  duration: '3 Months (Sprints)', 
                  audience: 'High-performing Contributors',
                  desc: 'Work directly on live client codebases under senior venture architects, submit evaluated PRs, and gain verifiable experience.',
                  href: '/learners/fellowship',
                  cta: 'Apply for Fellowship &rarr;'
                }
              ].map((tier, idx) => (
                <div key={idx} className={`card card-lift ${s.tierCard}${tier.featured ? ` ${s.tierCardFeatured}` : ''}`}>
                  <div>
                    <span className="tag-chip mb-2">{tier.audience}</span>
                    <h3 className={s.tierTitle}>{tier.title}</h3>
                    <div className="font-mono text-sm text-accent my-2 font-medium">{tier.feeLabel}</div>
                    <div className={s.tierDuration}>Duration: <strong>{tier.duration}</strong></div>
                    <p className={s.tierDesc}>{tier.desc}</p>
                  </div>
                  <Link href={tier.href} className={`btn btn-sm ${tier.featured ? 'btn-primary' : 'btn-outline'} ${s.tierBtn}`}>
                    {tier.cta}
                  </Link>
                </div>
              ))}
            </div>
          </section>

          {/* Startup & Enterprise Services */}
          <section className="section-breath border-t border-line">
            <div className="doclabel mb-2">§ 04 — STARTUP INCUBATION &amp; EQUITY TRACKS</div>
            <h2 className="mb-2">
              Venture Studio &amp; Enterprise AI Engagement Structures
            </h2>
            <p className="body-copy mb-6 measure">
              We align incentives directly with your long-term success. Rather than charging speculative hourly agency retainers, we work through dedicated co-development sprints and transparent equity agreements.
            </p>

            <div className="bento-grid-2 my-6">
              <div className="card card-lift flex flex-col justify-between">
                <div>
                  <span className="doclabel">§ VENTURE CO-BUILD</span>
                  <h3 className="card-title my-2">Services-Against-Equity Incubation</h3>
                  <div className="font-mono text-sm text-signal font-semibold mb-2">2% &ndash; 8% Milestone-Linked Equity</div>
                  <p className="body-copy text-sm">
                    For qualifying early-stage AI startups, we code and launch resilient production MVPs under an aligned equity exchange—bypassing cash-burn barriers and providing architecture reviews.
                  </p>
                  <ul className="feature-list mt-4 text-xs text-muted">
                    <li>Dedicated full-stack AI engineering squad</li>
                    <li>Zero out-of-pocket development retainers</li>
                    <li>Structured 90-day build to market deployment</li>
                  </ul>
                </div>
                <div className="mt-6">
                  <Link href="/startups/register" className="btn btn-primary btn-block">Apply For Incubation &rarr;</Link>
                </div>
              </div>

              <div className="card card-lift flex flex-col justify-between">
                <div>
                  <span className="doclabel">§ ENTERPRISE SPRINTS</span>
                  <h3 className="card-title my-2">Custom AI Architecture Engagements</h3>
                  <div className="font-mono text-sm text-signal font-semibold mb-2">Milestone / Scope Retainer</div>
                  <p className="body-copy text-sm">
                    For established organizations requiring isolated technical infrastructure upgrades, we deploy concentrated feature sprints with full IP transfer and strict NDA compliance.
                  </p>
                  <ul className="feature-list mt-4 text-xs text-muted">
                    <li>Private VPC deployment (AWS, GCP, or on-prem)</li>
                    <li>Localized open-weights serving via vLLM &amp; Ollama</li>
                    <li>Vector database clustering and retrieval pipelines</li>
                  </ul>
                </div>
                <div className="mt-6">
                  <Link href="/about/contact" className="btn btn-outline btn-block">Inquire About Sprints &rarr;</Link>
                </div>
              </div>
            </div>
          </section>

          {/* Commercial FAQ Section */}
          <section className="section-breath border-t border-line">
            <div className="doclabel mb-2">§ 05 — COMMERCIAL FAQ KNOWLEDGE BASE</div>
            <h2 className="mb-4">Frequently Asked Commercial Questions</h2>
            <div className="measure">
              <FAQAccordion items={faqs} />
            </div>
          </section>

          {/* Related Commercial & Legal Resources Mesh */}
          <section className="section-breath border-t border-line">
            <div className="doclabel mb-2">§ 06 — RELATED RESOURCES</div>
            <h2 className="mb-4">Explore Venture &amp; Legal Frameworks</h2>
            <div className="bento-grid-3">
              <div className="card card-lift">
                <h4 className="font-mono text-sm font-bold text-white mb-1">Annotated Term Sheets</h4>
                <p className="text-xs text-muted mb-3">Inspect standardized venture co-development term sheet templates with clause annotations.</p>
                <Link href="/startups/services/equity/term-sheets" className="accent-link text-xs">View Term Sheets &rarr;</Link>
              </div>
              <div className="card card-lift">
                <h4 className="font-mono text-sm font-bold text-white mb-1">Funding &amp; Equity</h4>
                <p className="text-xs text-muted mb-3">Discover how our co-development model helps founders reach market validation with zero agency debt.</p>
                <Link href="/startups/services/funding" className="accent-link text-xs">View Funding &rarr;</Link>
              </div>
              <div className="card card-lift">
                <h4 className="font-mono text-sm font-bold text-white mb-1">Legal &amp; IP Compliance</h4>
                <p className="text-xs text-muted mb-3">Review incorporation support, intellectual property assignments, and compliance guidelines.</p>
                <Link href="/startups/services/legal" className="accent-link text-xs">View Legal Details &rarr;</Link>
              </div>
            </div>
          </section>

          {/* Bottom Call to Action */}
          <section className="section-breath border-t border-line">
            <div className="doclabel mb-2">§ 07 — START YOUR JOURNEY</div>
            <div className="bento-card callout text-center">
              <h2>Ready to Build With DBERT?</h2>
              <p className="measure mx-auto my-4 text-muted">
                Whether applying for our hands-on engineering programs or exploring incubation co-development for your startup, our team is ready to connect.
              </p>
              <div className="stack-h justify-center gap-4 flex-wrap">
                <Link href="/learners" className="btn btn-primary btn-lg">Explore Learner Tracks &rarr;</Link>
                <Link href="/startups/register" className="btn btn-outline btn-lg">Register Your Startup &rarr;</Link>
              </div>
            </div>
          </section>

        </div>
      </div>
    </div>
  );
}

