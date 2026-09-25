import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import styles from './about.module.css';

export const metadata = pageMetadata('/about');

const pillars = [
  {
    label: '1. For Startups:',
    body: 'Providing product architecture consultation, developer matching resources, seed grants, co-development models (services-against-equity at 2-8%), and containerized AI setup support.',
    href: '/startups'
  },
  {
    label: '2. For Learners:',
    body: 'Offering structured engineering ladders, production developer courses, mock technical interview boards, resume scoring audits, and paid remote fellowship placements.',
    href: '/learners'
  },
  {
    label: '3. AI Solutions & SaaS Products:',
    body: 'Building custom fine-tuned weights configurations, secure document-ingest pipelines, validator APIs, and our local sovereign in-house LLM architecture (DBERT_AI).',
    href: '/ai-solutions'
  },
  {
    label: '4. DBERT Labs Research:',
    body: 'Advancing artificial intelligence frontiers in multi-agent orchestration libraries, local model weight edge optimizations, open-source commits, and academic institutional collaborations.',
    href: '/labs'
  },
];

export default function AboutPage() {
  return (
    <div className="container pad-block">
      <div className="mb-lg">
        <div className="doclabel">
          § 05 — INSTITUTIONAL ARCHITECTURE <span className="rev">rev: 2026.2</span>
        </div>
        <h1>Applied AI Incubation &amp; Research</h1>
        <p className="page-intro">
          Digital Blinc Education Research And Technology (DBERT) — Engineering live systems, incubating venture cohorts, and training production software engineers.
        </p>
      </div>

      <div className="measure-lg">
        {/* Origin & Operational Thesis */}
        <section className="section-breath border-t border-line">
          <div className="doclabel mb-2">§ 01 — THE DBERT MODEL</div>
          <h2>Bridging Research to Production Code</h2>
          <p className="body-copy mb-4">
            DBERT (parent entity: Digital Blinc Education Research And Technology, registered MSME) operates as an engineering-driven AI venture studio and talent incubator. We are headquartered in NCR (Ghaziabad), India, and operate as a fully remote, cloud-distributed technical collective.
          </p>
          <p className="body-copy mb-6">
            Our founding thesis addresses a critical industry failure: traditional education teaches academic theory separated from production realities, while early-stage startups bleed seed capital paying dev agencies for prototypes that crash under load. At DBERT, our engineering squads write live production code for portfolio startups, publish open-weights research, and mentor apprentice developers directly on live pull requests.
          </p>

          <div className="card card-lift my-6">
            <span className="doclabel text-xs mb-1">§ VERIFIED LEGITIMACY</span>
            <h3 className="card-title mt-2">Authentic Credentials &amp; Transparent Frameworks</h3>
            <p className="body-copy mt-2">
              We operate under statutory Indian MSME guidelines. All cohort completions, fellowship experience letters, and milestone deliverables carry verifiable cryptographic hashes authenticated on-chain.
            </p>
            <div className="mt-4 pt-3 border-t border-line stack-h gap-4 flex-wrap">
              <Link href="/about/team" className="btn btn-outline btn-sm">Inspect Team &amp; Mentors</Link>
              <Link href="/about/credentials" className="btn btn-outline btn-sm">Audit MSME Credentials</Link>
              <Link href="/verify" className="accent-link text-sm font-medium">Verify Certificate ID &rarr;</Link>
            </div>
          </div>
        </section>

        {/* Milestone Timeline */}
        <section className="section-breath border-t border-line">
          <div className="doclabel mb-2">§ 02 — STUDIO EVOLUTION</div>
          <h2>Our Execution Timeline</h2>
          <div className="bento-grid-3 stagger-grid my-6">
            <div className="card card-lift">
              <span className="tag-chip mb-2">Phase 1</span>
              <h3 className="card-title text-base my-1">Inception &amp; Open Models</h3>
              <p className="text-xs text-muted">Launched DBERT Labs research focus, fine-tuning sovereign models and publishing open-weights Ollama packages (DBERT_AI).</p>
            </div>
            <div className="card card-lift">
              <span className="tag-chip mb-2">Phase 2</span>
              <h3 className="card-title text-base my-1">Venture Incubation</h3>
              <p className="text-xs text-muted">Initiated our services-against-equity incubation track, partnering with technical founders to build MVPs with 100% code ownership.</p>
            </div>
            <div className="card card-lift">
              <span className="tag-chip mb-2">Phase 3</span>
              <h3 className="card-title text-base my-1">Scale &amp; Fellowship</h3>
              <p className="text-xs text-muted">Scaled the Applied AI Fellowship to over 1,500 candidates across India, matching vetted talent to live engineering repositories.</p>
            </div>
          </div>
        </section>

        {/* The 4 Operational Pillars */}
        <section className="section-breath border-t border-line">
          <div className="doclabel mb-2">§ 03 — OPERATIONAL PILLARS</div>
          <h2>Four Interconnected Pillars</h2>
          <div className="bento-grid-2 stagger-grid my-6">
            {pillars.map((pillar) => (
              <div key={pillar.label} className="card card-lift flex flex-col justify-between">
                <div>
                  <span className="doclabel mb-2">{pillar.label}</span>
                  <p className="body-copy text-sm my-3">{pillar.body}</p>
                </div>
                <div className="pt-3 border-t border-line">
                  <Link href={pillar.href} className="accent-link text-xs font-semibold uppercase tracking-wider">
                    Explore Ecosystem &rarr;
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

