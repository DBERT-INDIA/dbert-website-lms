import React from 'react';
import Link from 'next/link';
import StudioConsole, { type FeedLine } from '@/components/ui/StudioConsole';
import FactTicker from '@/components/ui/FactTicker';
import AudienceDoors, { type Door } from '@/components/ui/AudienceDoors';
import HandNote from '@/components/ui/HandNote';
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

const studioTelemetryFeed: FeedLine[] = [
  {
    time: '09:30:10',
    tag: 'chai',
    message: 'morning chai ritual completed',
    detail: '· 214 cups consumed this sprint',
  },
  {
    time: '09:35:44',
    tag: 'commit',
    message: 'studio monorepo merged 14 pull requests across 4 ventures',
    detail: '· 0 regression',
  },
  {
    time: '09:40:02',
    tag: 'review',
    message: 'systems architecture audit with 2 pre-seed founder teams',
    detail: '· terms aligned',
  },
  {
    time: '09:44:18',
    tag: 'build',
    message: 'custom vLLM inference engine optimized for Indian languages',
    detail: '· Hindi & Tamil ready',
  },
  {
    time: '09:48:02',
    tag: 'verify',
    message: '1,204 cryptographic certificate IDs verified on /verify',
    detail: '· 100% authenticity SLA',
  },
];

const studioFacts = [
  'est. Delhi NCR, India',
  'chai consumed this sprint: 214 cups',
  'every application gets a human reply',
  'fellows write real production code, not todo apps',
  'founders keep 100% of their codebase',
  'current stack: Next.js · Postgres · PyTorch · stubbornness',
  'registered MSME Government of India recognized entity',
];

const aboutDoors: Door[] = [
  {
    kind: 'founder',
    who: 'Pillar 01 · Venture Studio',
    title: 'Incubate Startups',
    description: 'We partner with technical founders, write the core code, and take equity risk together.',
    ctaLabel: 'See Incubation Model',
    href: '/startups',
  },
  {
    kind: 'enterprise',
    who: 'Pillar 02 · Sovereign AI',
    title: 'Enterprise SaaS',
    description: 'Battle-tested software tools born out of our own internal operational scale challenges.',
    ctaLabel: 'Browse Products',
    href: '/ai-solutions',
  },
  {
    kind: 'learner',
    who: 'Pillar 03 · Engineering Ladder',
    title: 'Train Engineers',
    description: 'A 4-stage progression turning curious students into verified production builders.',
    ctaLabel: 'Explore Ladder',
    href: '/learners',
  },
];

export default function AboutPage() {
  return (
    <>
      {/* ══════════ SECTION 1: HERO (2-COLUMN GRID) ══════════ */}
      <section className="section-subpage-hero">
        <div className="wrap subpage-hero-grid">
          <div>
            <div className="doclabel">
              § 01 — INSTITUTIONAL ARCHITECTURE <span className="rev">rev: 2026.2</span>
            </div>
            <h1 className="relative inline-block">
              Applied AI Incubation &amp; Research
              <HandNote className="absolute -right-8 -top-6 text-lg hidden md:block" tone="blue">
                registered MSME ✎
              </HandNote>
            </h1>
            <p className="intro-copy">
              Digital Blinc Education Research And Technology (DBERT) — Engineering live systems, incubating venture cohorts, and training production software engineers from Delhi NCR.
            </p>
            <div className="stack-h gap-3 mt-6 flex-wrap">
              <Link href="/about/team" className="btn btn-primary">
                Meet Technical Leadership →
              </Link>
              <Link href="/about/credentials" className="btn btn-outline">
                Audit MSME Credentials
              </Link>
            </div>
          </div>

          <div>
            <StudioConsole
              title="dbert-studio · delhi ncr operations telemetry"
              lines={studioTelemetryFeed}
              footLeft="delhi studio · sector 62"
              footRight="● studio active"
              note={
                <HandNote tone="amber">
                  the venture studio that writes the code ✎
                </HandNote>
              }
            />
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 2: FULL-BLEED AMBIENT FACT TICKER ══════════ */}
      <div className="section-ticker-ribbon">
        <FactTicker facts={studioFacts} />
      </div>

      {/* ══════════ SECTION 3: THE 3 CORE PILLARS GATEWAY ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 02 — THE DBERT TECHNICAL FLYWHEEL</div>
            <h2>Three Integrated Foundry Pillars</h2>
            <p>One unified technical engine powering startups, enterprise SaaS, and engineering careers.</p>
          </div>
          <AudienceDoors doors={aboutDoors} />
        </div>
      </section>

      {/* ══════════ SECTION 4: THE DBERT MODEL (BAND) ══════════ */}
      <section className="subpage-section band">
        <div className="wrap measure-lg">
          <div className="section-head-sub">
            <div className="doclabel">§ 03 — THE DBERT MODEL</div>
            <h2>Bridging Research to Production Code</h2>
            <p>
              DBERT (parent entity: Digital Blinc Education Research And Technology, registered MSME) operates as an engineering-driven AI venture studio and talent incubator. We are headquartered in NCR (Ghaziabad), India, and operate as a fully remote, cloud-distributed technical collective.
            </p>
          </div>
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
              <Link href="/dbert-online" className="accent-link text-sm font-medium">dbert.online Migration Notice &rarr;</Link>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 5: STUDIO EVOLUTION (BAND-ALT) ══════════ */}
      <section className="subpage-section band-alt">
        <div className="wrap measure-lg">
          <div className="section-head-sub">
            <div className="doclabel">§ 04 — STUDIO EVOLUTION</div>
            <h2>Our Execution Timeline</h2>
            <p>Key developmental milestones from inception to institutional scale.</p>
          </div>
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
        </div>
      </section>

      {/* ══════════ SECTION 6: OPERATIONAL PILLARS ══════════ */}
      <section className="subpage-section">
        <div className="wrap measure-lg">
          <div className="section-head-sub">
            <div className="doclabel">§ 05 — OPERATIONAL PILLARS</div>
            <h2>Four Interconnected Pillars</h2>
            <p>Architectural divisions ensuring sustainable execution across our studio flywheel.</p>
          </div>
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
        </div>
      </section>
    </>
  );
}

