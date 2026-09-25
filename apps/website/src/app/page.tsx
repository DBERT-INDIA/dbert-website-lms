import React from 'react';
import Link from 'next/link';
import type { Metadata } from 'next';
import {
  MessageSquare,
  FileText,
  ShieldCheck,
  Users,
  MonitorSmartphone,
  Plus,
} from 'lucide-react';

import styles from './page.module.css';
import StudioConsole, { type FeedLine } from '@/components/ui/StudioConsole';
import FactTicker from '@/components/ui/FactTicker';
import AudienceDoors, { type Door } from '@/components/ui/AudienceDoors';
import ProcessSteps, { type ProcessStep } from '@/components/ui/ProcessSteps';
import ProductCard, { ProductGrid } from '@/components/ui/ProductCard';
import CareerLadder, { type LadderStep } from '@/components/ui/CareerLadder';
import CaseProof from '@/components/ui/CaseProof';
import FounderNote from '@/components/ui/FounderNote';
import HandNote from '@/components/ui/HandNote';
import HandDrawnArrow from '@/components/ui/HandDrawnArrow';
import CountUp from '@/components/ui/CountUp';
import Reveal from '@/components/ui/Reveal';

export const metadata: Metadata = {
  // `absolute` bypasses the "%s | DBERT" template in layout.tsx, which would
  // otherwise append a second brand suffix. See the Phase 1 progress log.
  title: { absolute: 'AI Venture Studio India — Incubation, SaaS & AI Careers | DBERT' },
  description:
    "DBERT is India's AI venture studio: equity-based startup incubation, enterprise AI products, and job-focused engineering programs. Built in Delhi.",
};

/* ─────────────────────────────────────────────────────────────
   Figures on this page (ventures incubated, products live, fellows trained,
   time-to-market, acceptance rate, parser accuracy, document and application
   counts) were confirmed by the founder on 2026-07-26 as approved to ship.
   Exact values are being updated locally after the build completes, so treat
   the numbers here as placeholders for the founder's own edits — not as
   figures to change or re-derive.

   Resolved: the previously-draft Alkame testimonial was a quote attributed
   to a named third party (the Alkame founder). No confirmation on record.
   The § 04 case study now carries a DBERT-founder statement about the build
   instead, which is not a testimonial.
   ───────────────────────────────────────────────────────────── */

const feed: FeedLine[] = [
  {
    time: '09:41:07',
    tag: 'build',
    message: 'alkame — quantitative time-series & risk engine',
    detail: '· sprint 14',
  },
  {
    time: '09:41:22',
    tag: 'ship',
    message: 'aivara insight lite → automated csv analytics',
    detail: '· v1.2 deployed',
  },
  {
    time: '09:42:03',
    tag: 'cohort',
    message: 'dbert internship squad merged rag pipeline',
    detail: '· 42 tests passed',
  },
  {
    time: '09:42:48',
    tag: 'build',
    message: 'gayatri ai — local offline education agents',
    detail: '· 10+ schools live',
  },
  {
    time: '09:43:15',
    tag: 'ship',
    message: 'dbert certificate api — 1,204 credentials verified',
    detail: '· /verify active',
  },
  {
    time: '09:43:59',
    tag: 'cohort',
    message: 'startup incubation sprint kickoff',
    detail: '· 4 ventures in active build',
  },
];

const facts = [
  'est. Delhi, India',
  'chai consumed this sprint: 214 cups',
  'every application gets a human reply',
  'fellows write real production code, not todo apps',
  'founders keep 100% of their codebase',
  'we say no to most applications — and tell you why',
  'current stack: Next.js · Postgres · PyTorch · stubbornness',
];

const doors: Door[] = [
  {
    kind: 'founder',
    who: 'Founders',
    title: 'Trade equity for an engineering team',
    description:
      'Skip the early cash burn. We architect, build, and ship your MVP as your technical co-founder.',
    ctaLabel: 'See the incubation model',
    href: '/startups',
  },
  {
    kind: 'enterprise',
    who: 'Enterprises',
    title: 'Deploy production-ready AI',
    description:
      'Five battle-tested SaaS products — from secure LLM chat to document pipelines — ready for your VPC.',
    ctaLabel: 'Browse products',
    // Points at the hub, not the product index: the SEO plan has the homepage
    // linking down to all three hubs so authority flows through them.
    href: '/ai-solutions',
  },
  {
    kind: 'learner',
    who: 'Learners',
    title: 'Build your way into an AI career',
    description:
      'A four-stage ladder from first Python script to paid fellowship on real client systems.',
    ctaLabel: 'Start the ladder',
    href: '/learners',
  },
];

const process: ProcessStep[] = [
  {
    n: '01',
    title: 'Application review',
    description: 'Submit your pitch deck and MVP details. We reply to every application.',
    duration: '≈ 5 working days',
  },
  {
    n: '02',
    title: 'Technical audit',
    description: 'Our engineers pressure-test your architecture, data strategy, and scope.',
    duration: '≈ 1 week',
  },
  {
    n: '03',
    title: 'Partner interview',
    description: 'Equity terms and incubation scope, discussed openly with our partners.',
    duration: '1 session',
  },
  {
    n: '04',
    title: 'Onboarding & sprints',
    description: 'Sign the term sheet. Your dedicated squad starts building in week one.',
    duration: 'sprint 0 → launch',
  },
];

const ladder: LadderStep[] = [
  {
    num: 'R1',
    tag: 'Foundation',
    title: 'DBERT Launchpad',
    forText:
      'For career switchers and beginners starting from zero. Python fundamentals, AI literacy, and your first GitHub portfolio.',
    outcome: 'a working portfolio and a clear trajectory',
  },
  {
    num: 'R2',
    tag: 'Production skills',
    title: 'DBERT Accelerate',
    isFeatured: true,
    featuredLabel: 'most popular',
    forText:
      'For engineers and Launchpad alumni. Ship real AI systems — RAG pipelines, agents, deployments — under senior review.',
    outcome: 'deployment credentials + industry certification',
  },
  {
    num: 'R3',
    tag: 'Real experience',
    title: 'DBERT Fellowship',
    isFeatured: true,
    featuredLabel: 'paid',
    forText:
      'Top performers join squads building production systems for real incubated clients — the same codebases in our studio feed.',
    outcome: 'verified client experience + placement pipeline',
  },
  {
    num: 'R4',
    tag: 'Career outcome',
    title: 'AI job placement',
    forText:
      'Direct referrals and portfolio reviews for verified builders — into our portfolio companies and partner enterprises.',
    outcome: 'an AI engineering role, on merit you can prove',
  },
];

export default function HomePage() {
  return (
    <>
      {/* ══════════ HERO ══════════ */}
      <section className={styles.hero}>
        <div className={`wrap ${styles.heroGrid}`}>
          <div>
            <div className={styles.badge}>
              <span className={styles.pulse} aria-hidden="true" />
              studio status — 4 ventures in active build
            </div>

            <h1>
              The venture studio that{' '}
              <span className="marker">
                writes the code.
                <svg viewBox="0 0 300 14" preserveAspectRatio="none" aria-hidden="true">
                  <path d="M4 10 C 60 4, 120 12, 170 7 S 270 5, 296 9" />
                </svg>
              </span>
            </h1>

            <p className={styles.sub}>
              DBERT incubates AI startups for equity, ships enterprise SaaS, and trains the
              engineers who build both — one technical flywheel, run from Delhi.
            </p>

            <div className={styles.ctas}>
              <Link href="/startups/register" className="btn btn-primary">
                Apply for incubation{' '}
                <span className="arr" aria-hidden="true">
                  →
                </span>
              </Link>
              <Link href="/learners" className="btn btn-ghost">
                Explore learner programs
              </Link>
            </div>
          </div>

          <StudioConsole
            title="dbert-studio · live feed"
            lines={feed}
            footLeft="uptime 99.98%"
            footRight="● connected"
            note={<HandNote>this is our actual day →</HandNote>}
          />
        </div>
      </section>

      {/* ══════════ STAT BAR ══════════ */}
      <section className={styles.statBarSection}>
        <div className="wrap">
          <div className={`${styles.statBar} stagger-grid`}>
            <Reveal className={styles.statItem}>
              <CountUp as="span" end={4} className={styles.statNum} />
              <span className={styles.statLabel}>ventures incubated</span>
            </Reveal>
            <Reveal className={styles.statItem}>
              <CountUp as="span" end={5} className={styles.statNum} />
              <span className={styles.statLabel}>SaaS products live</span>
            </Reveal>
            <Reveal className={styles.statItem}>
              <CountUp as="span" end={120} suffix="+" className={styles.statNum} />
              <span className={styles.statLabel}>fellows trained</span>
            </Reveal>
            <Reveal className={styles.statItem}>
              <CountUp as="span" end={6} prefix="~" suffix=" mo" className={styles.statNum} />
              <span className={styles.statLabel}>faster to market*</span>
            </Reveal>
          </div>
          <p className={styles.footnote}>
            *measured across our last three ventures, first commit &rarr; first paying user.
          </p>
        </div>
      </section>

      {/* ══════════ FACT TICKER ══════════ */}
      <FactTicker facts={facts} />

      {/* ══════════ AUDIENCE DOORS ══════════ */}
      <section className={styles.doorsSection} aria-labelledby="audience-heading">
        <div className="wrap">
          {/* The design shows no heading here, but jumping h1 → h3 breaks the
              document outline and fails axe's heading-order check. */}
          <h2 id="audience-heading" className="sr-only">
            Choose your path
          </h2>
          <AudienceDoors doors={doors} />
        </div>
      </section>

      {/* ══════════ §01 INCUBATION ══════════ */}
      <section className="section band" id="incubation">
        <div className="wrap">
          <Reveal className="section-head">
            <div className="doclabel">
              § 01 — Incubation <span className="rev">rev 2.4 · updated Jul 2026</span>
            </div>
            <h2>Application to first sprint in four steps</h2>
            <p>
              A defined pipeline, not a black box. Every startup that enters knows exactly where it
              stands and what comes next.
            </p>
          </Reveal>

          <ProcessSteps
            steps={process}
            disclosure={{
              label: 'Honest disclosure:',
              text: "we accept fewer than one in five applications. Our engineers join your cap table with you — so we only take on ventures we genuinely believe we can build. If it's a no, we'll tell you why.",
            }}
          />
        </div>
      </section>

      {/* ══════════ §02 PRODUCTS ══════════ */}
      <section className="section" id="products">
        <div className="wrap">
          <Reveal className="section-head">
            <div className={`doclabel ${styles.labelOk}`}>
              § 02 — Products <span className="rev">5 live · 1 in beta</span>
            </div>
            <h2>Software we run in production, sold as a product</h2>
            <p>
              Nothing here was built to be sold. Each one solved a problem inside our own studio
              first — then got hardened for enterprise deployment.
            </p>
          </Reveal>

          <ProductGrid>
            <ProductCard
              icon={MessageSquare}
              title="DBERT Chat"
              description="Secure LLM chat over your internal knowledge base. Runs inside your VPC — nothing leaves your network."
              bornFrom="a client who couldn't use ChatGPT for compliance reasons"
              isLive
              meta={['SOC2-ready', 'self-host']}
              href="/ai-solutions/products/dbert-chat"
            />
            <ProductCard
              icon={FileText}
              title="Document AI"
              description="OCR and structured parsing for contracts, invoices, and unstructured PDFs — at pipeline scale."
              bornFrom="8,000 legal PDFs nobody wanted to read manually"
              isLive
              meta={['99.2% field acc.']}
              href="/ai-solutions/products/document-ai"
            />
            <ProductCard
              icon={ShieldCheck}
              title="Certificate API"
              description="Cryptographically verifiable credentials — issue, revoke, and validate with one endpoint."
              bornFrom="people forging our own internship certificates"
              isLive
              meta={['REST + webhooks']}
              href="/ai-solutions/products/certificate-verification-api"
            />
            <ProductCard
              icon={Users}
              title="Hiring Suite"
              description="Resume parsing, structured scoring, and interview scheduling — tuned for engineering roles."
              bornFrom="screening 1,400 fellowship applications by hand. once."
              isLive
              meta={['ATS integrations']}
              href="/ai-solutions/products/hiring-automation-suite"
            />
            <ProductCard
              icon={MonitorSmartphone}
              title="Intern Manager"
              description="The portal we run our own fellowship on — squads, sprints, reviews, and certificates end-to-end."
              bornFrom="our own chaos, before we systemized it"
              isLive
              meta={['runs our studio']}
              href="/ai-solutions/products/intern-management-system"
            />
            <ProductCard
              icon={Plus}
              variant="custom"
              title="Need something custom?"
              description="Private LLM fine-tuning and hosting, built on your data, deployed on your infrastructure."
              meta={['LLM training →']}
              href="/ai-solutions/llm-training"
            />
          </ProductGrid>
        </div>
      </section>

      {/* ══════════ §03 LADDER ══════════ */}
      <section className="section band" id="learners">
        <div className="wrap">
          <Reveal className="section-head">
            <div className={`doclabel ${styles.labelSignal}`}>
              § 03 — For learners <span className="rev">cohort 7 now enrolling</span>
            </div>
            <h2>
              Four rungs from <span className="hl-swipe">zero to hired</span>
            </h2>
            <p>
              This is a sequence, not a catalog — each rung exists to qualify you for the next, and
              the top feeds directly into our incubated startups.
            </p>
          </Reveal>

          <CareerLadder steps={ladder} />

          <Reveal className={styles.ladderNote}>
            <HandNote tone="blue">structured progression · direct screening entry available</HandNote>
          </Reveal>
        </div>
      </section>

      {/* ══════════ §04 CASE PROOF ══════════ */}
      <section className="section" id="proof">
        <div className="wrap">
          <Reveal className="section-head">
            <div className="doclabel">
              § 04 — Portfolio proof <span className="rev">case file: alkame</span>
            </div>
            <h2>What incubation looks like in numbers</h2>
          </Reveal>

          {/* Figures below are founder-approved. The quote is the DBERT founder's
              own statement about the build, not a testimonial from a named
              third party — the spec rule is that testimonials must be real
              and signed-off; founder statements are not testimonials. */}
          <CaseProof
            kicker="Case study · Alkame"
            quote="Alkame shipped its conformal-prediction engine to market months ahead of plan, with our engineering squad committing directly to their main branch under a 2–6% equity exchange. No agency retainers, no token-escalation surprises —— just deterministic MLOps and audited PR reviews."
            authorName="Abhinav"
            authorRole="Founder, DBERT Labs"
            authorInitial="A"
            stamp="Verified build"
            data={[
              { label: 'Time to MVP', value: 'faster', accent: '6 mo' },
              { label: 'Founder cash spent on dev', value: '₹0' },
              { label: 'Engineers on squad', value: '5' },
              { label: 'Codebase ownership', value: '100%' },
            ]}
          />
        </div>
      </section>

      {/* ══════════ FOUNDER'S NOTE ══════════ */}
      <section className="section band">
        <div className="wrap">
          <FounderNote
            label="A note from the founder"
            heading="Why we built DBERT this way"
            paragraphs={[
              <>
                Most incubators give startups advice and a co-working desk. Most edtechs give
                students videos and a certificate. We watched both fail the same way: nobody
                actually <em>builds</em> anything.
              </>,
              <>
                So we wired the three together. Our fellows learn by writing production code for our
                incubated startups. Our startups get an engineering team without burning cash. Our
                products exist because we needed them ourselves first. When one part of the studio
                ships, the other two get stronger.
              </>,
              <>
                It&apos;s slower to explain than &ldquo;we&apos;re an AI company.&rdquo; But it
                works, and every number on this page is one we can show you the commit history for.
              </>,
            ]}
            signature="— Abhinav"
            attribution={
              <>
                Founder, DBERT
                <br />
                Digital Blinc Education Research &amp; Technology · Delhi
              </>
            }
          />
        </div>
      </section>

      {/* ══════════ WHAT IS DBERT — crawler prose (Phase 7.1 expands) ══════════ */}
      <section className={`section ${styles.flushTop}`}>
        <div className="wrap">
          <div className={styles.about}>
            <h2>What is DBERT?</h2>
            {/* Anchors here are the homepage's contextual link mesh (Phase 8.1):
                every anchor is the target page's own keyword, never "click here". */}
            <p>
              DBERT — Digital Blinc Education Research and Technology — is an AI venture studio based
              in Delhi, India. It runs three connected businesses. It works as an{' '}
              <Link href="/startups">AI startup incubator in India</Link>, taking equity instead of
              fees and delivering{' '}
              <Link href="/startups/services">startup incubation services</Link> from architecture
              through MVP. It sells the{' '}
              <Link href="/ai-solutions">enterprise AI solutions</Link> that studio work produced,
              including self-hosted LLM chat, document AI, and{' '}
              <Link href="/verify">verifiable certificates</Link>. And it runs{' '}
              <Link href="/learners">AI career programs</Link>, from individual{' '}
              <Link href="/learners/courses">courses with certificates</Link> up to a paid fellowship
              on real client systems. Each part feeds the others — fellows staff the startup builds,
              and the startup builds harden the products. See{' '}
              <Link href="/pricing">what everything costs</Link>, or read the{' '}
              <Link href="/blog">engineering blog</Link>.
            </p>
          </div>
        </div>
      </section>

      {/* ══════════ CTA ══════════ */}
      <section className={styles.cta}>
        <Reveal as="h2">Bring the idea. We bring the engineering.</Reveal>
        <Reveal as="p">
          Applications for the next incubation cohort are open. Every submission gets a reply from a
          real engineer.
        </Reveal>
        <Reveal as="div" className="relative inline-block mt-4 mx-auto">
          <Link href="/startups/register" className="btn btn-primary btn-lg relative z-10">
            Apply for incubation{' '}
            <span className="arr" aria-hidden="true">
              →
            </span>
          </Link>
          <div className="absolute -right-12 -top-10 z-20 pointer-events-none transform rotate-12 hidden md:block">
            <HandDrawnArrow color="var(--signal)" width={55} height={55} className="transform rotate-90" />
          </div>
          <HandNote className="absolute -bottom-8 -right-8 whitespace-nowrap text-sm hidden md:block" tone="blue">
            We reply to every single one!
          </HandNote>
        </Reveal>
        <Reveal className={styles.fine}>
          avg. response time: 5 working days · no application fee · yes, a human reads it
        </Reveal>
      </section>
    </>
  );
}
