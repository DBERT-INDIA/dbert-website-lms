import React from 'react';
import Link from 'next/link';
import { pageMetadata } from '@/lib/seo';
import HandNote from '@/components/ui/HandNote';
import TrackedLink from '@/components/ui/TrackedLink';
import StudioConsole, { type FeedLine } from '@/components/ui/StudioConsole';
import FactTicker from '@/components/ui/FactTicker';
import AudienceDoors, { type Door } from '@/components/ui/AudienceDoors';
import s from './labs.module.css';
import { BookOpen, Laptop, Microscope } from 'lucide-react';

export const metadata = pageMetadata('/labs');

export default function DBERTLabsLandingPage() {
  const preprints = [
    {
      title: 'Deterministic Conformal Prediction for Low-Latency Time Series in Emerging Markets',
      id: 'DBERT-TR-2026-04',
      date: 'Aug 2026',
      doi: 'doi:10.5281/zenodo.dbert.2026.04',
      abstract:
        'Empirical evaluation of non-exchangeable conformal prediction bounds over high-volatility tick data streams. Shipped to production under the Alkame quantitative risk engine.',
    },
    {
      title: 'Parameter-Efficient LoRA Quantization for Offline-First Edge Classrooms',
      id: 'DBERT-TR-2026-02',
      date: 'Jun 2026',
      doi: 'doi:10.5281/zenodo.dbert.2026.02',
      abstract:
        'Compression benchmarks for 3B–8B parameter models running on consumer hardware without external API connectivity. Powers Gayatri AI local school agent deployments.',
    },
  ];

  const labsTelemetryFeed: FeedLine[] = [
    {
      time: '11:02:14',
      tag: 'infer',
      message: 'DBERT-TR-2026-04 conformal risk bounds evaluated',
      detail: '· 99.1% coverage on tick streams',
    },
    {
      time: '11:05:42',
      tag: 'deploy',
      message: 'Gayatri AI v1.4 local classroom weights released',
      detail: '· 4-bit GGUF quantization',
    },
    {
      time: '11:09:03',
      tag: 'commit',
      message: 'dbert-rag-eval-harness merged to open repo',
      detail: '· automated synthetic QA test suite',
    },
    {
      time: '11:12:35',
      tag: 'audit',
      message: 'Sovereign Ollama cluster vulnerability audit passed',
      detail: '· zero external telemetry calls',
    },
    {
      time: '11:16:10',
      tag: 'grant',
      message: 'Zenodo open data archive DOI registration confirmed',
      detail: '· doi:10.5281/zenodo.dbert.2026.04',
    },
    {
      time: '11:20:48',
      tag: 'sprint',
      message: 'Distributed fine-tuning run completed',
      detail: '· 8x RTX 4090 cluster',
    },
  ];

  const labsFacts = [
    'open-weights models on Ollama & HuggingFace',
    'peer-audited arXiv-style technical preprints',
    'offline-first edge classroom LLMs',
    'empirical latency & token throughput benchmarks',
    '100% reproducible hyperparameters & datasets',
    'Delhi NCR applied AI engineering facility',
  ];

  const labsDoors: Door[] = [
    {
      kind: 'founder',
      who: 'Track 01 · Structural Investigations',
      title: 'Research Segments',
      description: 'Inspect active investigations into multi-agent systems, sovereign model compression, and hybrid vector RAG.',
      ctaLabel: 'Explore Research Tracks',
      href: '/labs/research',
    },
    {
      kind: 'enterprise',
      who: 'Track 02 · Peer-Audited Preprints',
      title: 'Technical Publications',
      description: 'Examine peer-reviewed style engineering briefs with DOI citations, empirical benchmarks, and code datasets.',
      ctaLabel: 'Browse Publications',
      href: '/labs/publications',
    },
    {
      kind: 'learner',
      who: 'Track 03 · Public Code & Weights',
      title: 'Open Source Repositories',
      description: 'Deploy open-weights models, local Ollama model cards, and offline classroom syntax parser libraries.',
      ctaLabel: 'Inspect Codebases',
      href: '/labs/opensource',
    },
  ];

  return (
    <>
      {/* ══════════ SECTION 1: HERO (2-COLUMN GRID) ══════════ */}
      <section className="section-subpage-hero">
        <div className="wrap subpage-hero-grid">
          <div>
            <div className="doclabel">
              § 01 — LABS ARCHIVES <span className="rev">rev: 2026.3</span>
            </div>
            <h1 className="relative inline-block">
              Where Breakthrough Systems Begin
              <HandNote className="absolute -right-12 -top-6 text-lg hidden md:block" tone="blue">
                peer-audited preprints ✍
              </HandNote>
            </h1>
            <p className="intro-copy">
              DBERT Labs is the dedicated applied artificial intelligence engineering facility and technical research division of DBERT based in Delhi NCR. 
              We investigate multi-agent orchestration architectures, local LLM edge quantization, custom RAG evaluation harnesses, and algorithmic financial intelligence—open-sourcing our findings and feeding validated systems directly into our incubation and learning ecosystems.
            </p>
            <div className="stack-h gap-3 mt-6 flex-wrap">
              <Link href="/labs/publications" className="btn btn-primary">
                Browse Preprints &rarr;
              </Link>
              <Link href="/labs/opensource" className="btn btn-outline">
                Open Source Repositories
              </Link>
            </div>
          </div>

          <div>
            <StudioConsole
              title="dbert-labs · active research telemetry"
              lines={labsTelemetryFeed}
              footLeft="applied AI research facility · Delhi NCR"
              footRight="● 6 active compute clusters"
            />
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 2: FULL-BLEED AMBIENT FACT TICKER ══════════ */}
      <div className="section-ticker-ribbon">
        <FactTicker facts={labsFacts} />
      </div>

      {/* ══════════ SECTION 3: 3-DOOR RESEARCH GATEWAY ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 02 — EXPLORE RESEARCH DIVISIONS</div>
            <h2>Applied Research Divisions</h2>
            <p>Peer-audited preprints, empirical latency benchmarks, and sovereign model weights.</p>
          </div>
          <AudienceDoors doors={labsDoors} />
        </div>
      </section>

      {/* ══════════ SECTION 4: ARXIV-STYLE PREPRINT HUD (BAND) ══════════ */}
      <section className="subpage-section band">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 03 — PEER-AUDITED PREPRINTS</div>
            <h2>arXiv-Style Technical Briefings</h2>
            <p>Empirical evaluation bounds, reproducible hyperparameters, and Zenodo open data archives.</p>
          </div>

          <div className={s.preprintSection}>
            <div className={s.preprintHeader}>
              <span className={s.preprintTag}>[ARXIV-STYLE PREPRINT REPOSITORY // PEER AUDITED]</span>
              <span className={s.preprintDoi}>OPEN ACCESS · REPRODUCIBLE HYPERPARAMETERS</span>
            </div>
            <div className={s.preprintList}>
              {preprints.map((paper) => (
                <div key={paper.id} className={s.preprintEntry}>
                  <h3 className={s.preprintEntryTitle}>{paper.title}</h3>
                  <div className={s.preprintMeta}>
                    <span>{paper.id}</span>
                    <span>·</span>
                    <span>{paper.date}</span>
                    <span>·</span>
                    <span className="text-accent">{paper.doi}</span>
                  </div>
                  <p className={s.preprintAbstract}>{paper.abstract}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 5: RESEARCH & OPEN DEVELOPMENT TRACKS ══════════ */}
      <section className="subpage-section">
        <div className="wrap">
          <div className="section-head-sub">
            <div className="doclabel">§ 04 — STRUCTURAL RESEARCH TRACKS</div>
            <h2>Technical Publications &amp; Codebases</h2>
            <p>Deploy our open-source weights and inspect reproducible benchmarks.</p>
          </div>

          <div className={s.hubGrid}>
            <div className={`card card-lift stack-between ${s.cardItem}`}>
              <div>
                <span className="icon-chip"><Microscope aria-hidden="true" /></span>
                <h3 className="card-heading-lg">Research Segments</h3>
                <p className="body-copy">
                  Inspect our active structural investigations: multi-agent system governance, sovereign LLM compression, hybrid vector RAG architectures, and automated evaluation toolboxes.
                </p>
              </div>
              <Link href="/labs/research" className="accent-label">Explore Technical Research &rarr;</Link>
            </div>

            <div className={`card card-lift stack-between ${s.cardItem}`}>
              <div>
                <span className="icon-chip"><BookOpen aria-hidden="true" /></span>
                <h3 className="card-heading-lg">Technical Publications</h3>
                <p className="body-copy">
                  Examine our peer-reviewed style engineering briefs, complete with academic citations (DOI/Scholar), reproducible hyperparameters, and empirical hardware latency benchmarks.
                </p>
              </div>
              <Link href="/labs/publications" className="accent-label">Explore Published Reports &rarr;</Link>
            </div>

            <div className={`card card-lift stack-between ${s.cardItem}`}>
              <div>
                <span className="icon-chip"><Laptop aria-hidden="true" /></span>
                <h3 className="card-heading-lg">Open Source Repositories</h3>
                <p className="body-copy">
                  Deploy DBERT&apos;s contributions to public open-weights registries (DBERT_AI custom LLM on Ollama) and educational systems (Gayatri AI syntax parsers).
                </p>
              </div>
              <Link href="/labs/opensource" className="accent-label">Explore Open-Source Code &rarr;</Link>
            </div>
          </div>
        </div>
      </section>

      {/* ══════════ SECTION 6: INSTITUTIONAL COLLABORATION (BAND-ALT) ══════════ */}
      <section className="subpage-section band-alt">
        <div className="wrap">
          <div className={`card card-lift ${s.ctaCard}`}>
            <div className="doclabel mb-2">§ 05 — INSTITUTIONAL COLLABORATION</div>
            <h2 className="card-title">Academic &amp; Institutional Collaboration</h2>
            <p className={s.ctaCopy}>
              Partner with DBERT Labs on custom engineering research sprints, sovereign AI cluster benchmarks, or specialized dataset alignment projects under verified legal frameworks.
            </p>
            <div className="stack-h gap-4 mt-6 justify-center">
              <TrackedLink
                href="/labs/collaborate"
                eventName="collaboration_click"
                eventParams={{ location: 'labs_landing', target: 'submit_proposal' }}
                className="btn btn-primary"
              >
                Submit Collaboration Proposal
              </TrackedLink>
              <Link href="/about/credentials" className="btn btn-outline">Inspect Institutional Verification</Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
