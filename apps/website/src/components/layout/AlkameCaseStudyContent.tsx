import React from 'react';
import Image from 'next/image';
import ContributorCards from '@/components/ui/ContributorCards';
import ContributorForm from '@/components/ui/ContributorForm';
import AlkameJumpNav from '@/components/ui/AlkameJumpNav';
import f from '../ui/forms.module.css';
import s from './alkame.module.css';

const architecturePillars = [
  {
    title: 'Model Layer',
    body: 'Per-symbol, per-horizon ensembles — logistic regression, random forest, gradient-boosted trees, and a stacking combiner — trained under strict no-lookahead discipline.',
  },
  {
    title: 'Calibration Layer',
    body: 'Split conformal prediction sits on top of every model output. A prediction is only surfaced once its prediction set collapses to a single label — a distribution-free coverage guarantee, not a raw softmax score.',
  },
  {
    title: 'Drift Detection & Retraining',
    body: 'Every prediction — shown or withheld — is logged with a resolvable outcome. A retrained model must re-clear the same validation gates before replacing production, never auto-promoted.',
  },
  {
    title: 'Validation Gate',
    body: 'Walk-forward backtesting across multiple non-overlapping windows, with explicit transaction-cost and slippage modeling, gates any promotion.',
  },
];

const technicalDifficulties = [
  {
    problem: 'Most retail-facing prediction tools report a point prediction with no validated measure of confidence.',
    approach: 'Split conformal prediction as a display gate — a call is only shown once its prediction set collapses to a single label, chosen over Platt scaling or isotonic regression for its distribution-free coverage guarantee.',
    cite: 'Kaya & Nguyen, 2025',
  },
  {
    problem: 'A single attractive backtest is a well-documented statistical trap — testing many configurations can make a strategy look strong purely by chance.',
    approach: 'Every candidate model clears a walk-forward, multi-window, cost-and-slippage-aware validation gate before promotion. One good backtest is necessary, never sufficient.',
    cite: 'Bailey, Borwein, López de Prado & Zhu, 2014',
  },
  {
    problem: 'Live markets drift, so a model validated last quarter can silently decay without anyone noticing.',
    approach: 'A Prediction Ledger logs every prediction against its eventual resolved outcome. Sustained degradation triggers retraining — the retrained model re-clears the same gates, no shortcuts.',
    cite: 'Gama et al., 2014',
  },
  {
    problem: 'Comparing a new architecture fairly against existing tooling, rather than a strawman.',
    approach: 'The evaluation protocol benchmarks against Qlib — Microsoft\u2019s open-source quant research platform — on identical data and time windows, plus a naive rule-based floor.',
    cite: 'Yang, Liu, Zhou, Bian & Liu, 2020',
  },
  {
    problem: 'India\u2019s regulatory footing for algorithmic and "black box" signal providers changed materially in 2025.',
    approach: 'Scope is deliberately restricted to signal-quality assessment, not automated order execution — staying on the lower-friction research/signal side of SEBI\u2019s new principal-agent framework.',
    cite: 'SEBI, Feb 2025',
  },
];

const timelineSteps = [
  { month: 'MAY 2026', body: 'Data infrastructure and feature-store setup across NIFTY 500 constituents; no-lookahead discipline established.' },
  { month: 'JUNE 2026', body: 'Model ensembles and the conformal calibration layer built out; Qlib and naive baselines prepared for matched comparison.' },
  { month: 'JULY 2026', body: 'Walk-forward validation protocol executed; Prediction Ledger begins logging live, resolvable outcomes.' },
  { month: 'AUGUST 2026', body: 'Live drift-monitoring window and program wrap-up; findings reported per the pre-registration commitments, in either direction.' },
];

const positioningRows = [
  { work: 'Kaya & Nguyen (2025)', contribution: 'Conformal prediction achieves error rates tracking nominal significance levels, on 764 US large/mid-cap stocks, Jan 2022\u2013Jan 2024.', gap: 'Small-scale, US-only proof of concept — not India-specific, not integrated into a production pipeline with drift detection.' },
  { work: 'Bailey et al. (2014)', contribution: 'Formal proof that backtest overfitting is a near-inevitable statistical artifact of testing many configurations.', gap: 'Diagnoses the problem rigorously, but is a methodology paper — no live architecture for continuously re-validating deployed models.' },
  { work: 'Gama et al. (2014)', contribution: 'Establishes the standard taxonomy of concept drift (sudden, gradual, incremental, recurring) in ML broadly.', gap: 'General-purpose survey, not applied to retail financial signal generation or tied to audit/regulatory requirements.' },
];

// Sticky left column paired with a right column of variable height.
// The left column pins near the top of the viewport as the user scrolls
// past a taller right column, instead of leaving dead space beneath it.
function StickyRow({
  index,
  eyebrow,
  title,
  left,
  right,
  id,
}: {
  index: string;
  eyebrow: string;
  title: string;
  left: React.ReactNode;
  right: React.ReactNode;
  id: string;
}) {
  return (
    <div id={id} className={s.row}>
      <div className={`container ${s.rowBody}`}>
        <div className={s.stickyGrid}>
          <div className={s.stickyCol}>
            <p className={s.rowIndex}>{index}</p>
            <div className="doclabel">§ {index.replace(/[^0-9]/g, '').padStart(2, '0') || '02'} — {eyebrow.toUpperCase()}</div>
            <h2 className={s.rowTitle}>{title}</h2>
            {left}
          </div>
          <div>{right}</div>
        </div>
      </div>
    </div>
  );
}

export default function AlkameCaseStudyContent() {
  return (
    <div>
      {/* Hero */}
      <div className={`container ${s.hero}`}>
        <div className={s.heroGrid}>
          <div>
            <div className={s.logoRow}>
              <div className={s.logoFrame}>
                <Image src="/alkame.png" alt="Alkame Inc. Logo" fill className={s.logoImg} />
              </div>
              <div className="doclabel">§ 01 — FINTECH CASE STUDY <span className="rev">rev: 2026.2</span></div>
            </div>
            <h1 className={s.heroTitle}>
              Alkame Inc.
            </h1>
            <p className={s.heroLede}>
              Calibrated, conformal-prediction market intelligence across the NIFTY 500 &mdash; an applied
              research program DBERT incubates in exchange for equity.
            </p>
            <div className={s.btnRow}>
              <a href="https://alkameinc.info/" target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-sm">Visit Alkame ↗</a>
              <a href="https://github.com/Alkameinc/alkame-nifty-50-educational/" target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-sm">View GitHub Repo ↗</a>
            </div>
          </div>

          {/* Quick-facts panel */}
          <div className={`card ${s.facts}`}>
            <p className={s.factsLabel}>
              At a Glance
            </p>
            <div className={s.factsList}>
              <div>
                <p className={s.factValue}>&#8377;1.2Cr</p>
                <p className={s.factNote}>Research contribution &mdash; DBERT services delivered in exchange for equity</p>
              </div>
              <div>
                <p className={s.factValue}>4 Months</p>
                <p className={s.factNote}>May &ndash; August 2026 applied research program</p>
              </div>
              <div>
                <p className={s.factValue}>6,300+ Stocks</p>
                <p className={s.factNote}>NIFTY 500 universe, sub-100ms ingestion latency</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sticky jump-nav — stays visible while scrolling, highlights the active section */}
      <AlkameJumpNav />

      {/* 01 — Research Question */}
      <StickyRow
        id="research-question"
        index="01"
          eyebrow="The Research Question"
          title="Why Calibrated Confidence Matters"
          left={
            <p className={s.rowNote}>
              A documented gap between unregulated retail-facing signals and validated confidence &mdash;
              grounded in SEBI&rsquo;s own regulatory data.
            </p>
          }
          right={
            <div className={s.stack3}>
              <div className={s.statGrid}>
                <div className={`card ${f.errorTint}`}>
                  <p className={f.figure}>+41%</p>
                  <p className={f.metaLine}>YoY rise in aggregate retail derivative losses &mdash; &#8377;1,05,603cr in FY25</p>
                </div>
                <div className={`card ${f.errorTint}`}>
                  <p className={f.figure}>~91%</p>
                  <p className={f.metaLine}>of individual traders ended FY25 in loss, averaging ~&#8377;1.1 lakh each</p>
                </div>
                <div className={`card ${f.errorTint}`}>
                  <p className={f.figure}>~20%</p>
                  <p className={f.metaLine}>YoY decline in unique traders even as losses rose &mdash; a structural, not cyclical, pattern</p>
                </div>
                <div className={`card ${f.errorTint}`}>
                  <p className={f.figure}>~2%</p>
                  <p className={f.metaLine}>of financial &ldquo;finfluencers&rdquo; are SEBI-registered, yet 82% of investors act on their advice anyway</p>
                </div>
              </div>
              <p className={s.source}>
                Sources: SEBI, Jul 2025; CFA Institute, 2025.
              </p>
              <p className={s.question}>
                Alkame-Nifty50 tests one falsifiable question: does enforcing calibrated confidence as a
                display gate &mdash; via split conformal prediction &mdash; and walk-forward, cost-aware
                validation as a promotion gate, produce lower calibration error and comparable-or-better
                risk-adjusted edge than Microsoft&rsquo;s Qlib and a naive rule-based baseline?
              </p>
              <div className={`card ${s.accentCard}`}>
                <p className={s.disclaimer}>
                  This is a pre-registered study design. No empirical results are claimed here &mdash; the
                  research team has committed in advance to report the outcome whichever direction it points.
                </p>
              </div>
            </div>
          }
        />

      {/* 02 — Where This Sits vs. Existing Research */}
      <StickyRow
        id="positioning"
        index="02"
        eyebrow="Grounded in Research"
        title="Where This Sits vs. Existing Work"
        left={
          <p className={s.rowNote}>
            Alkame-Nifty50&rsquo;s contribution is architectural and applied, not a new algorithm &mdash; it
            integrates findings that, on their own, stop short of a production system.
          </p>
        }
        right={
          <div className={f.stack2}>
            {positioningRows.map((row) => (
              <div key={row.work} className={`card ${s.compactCard}`}>
                <p className={s.priorWork}>{row.work}</p>
                <p className={s.priorContribution}>{row.contribution}</p>
                <p className={s.priorGap}>
                  <span className={s.strong}>Gap this project addresses: </span>{row.gap}
                </p>
              </div>
            ))}
          </div>
        }
      />

      {/* 03 — System Architecture */}
      <StickyRow
        id="architecture"
        index="03"
          eyebrow="System Architecture"
          title="How Alkame-Nifty50 Is Built"
          left={
            <p className={s.rowNote}>
              Four layers, each built to resist a specific, documented failure mode in retail-facing
              quantitative trading tools.
            </p>
          }
          right={
            <div className={s.pillarGrid}>
              {architecturePillars.map((pillar) => (
                <div key={pillar.title} className="card">
                  <h3 className={s.pillarTitle}>{pillar.title}</h3>
                  <p className={s.pillarBody}>{pillar.body}</p>
                </div>
              ))}
            </div>
          }
        />

      {/* 04 — Technical Difficulties */}
      <StickyRow
        id="challenges"
        index="04"
        eyebrow="Engineering Challenges"
        title="Technical Difficulties & How We Approached Them"
        left={
          <p className={s.rowNote}>
            Five specific, well-documented failure modes shaped this design &mdash; each paired with the
            concrete choice made to address it, and the research it draws on.
          </p>
        }
        right={
          <div className={f.stack2}>
            {technicalDifficulties.map((item, idx) => (
              <div key={idx} className={`card ${s.compactCard}`}>
                <p className={s.problem}>
                  <span className={s.problemLabel}>Problem — </span>{item.problem}
                </p>
                <p className={s.approach}>
                  <span className={s.approachLabel}>Approach — </span>{item.approach}
                </p>
                <p className={s.cite}>{item.cite}</p>
              </div>
            ))}
          </div>
        }
      />

      {/* 05 — Regulatory Reality */}
      <StickyRow
        id="regulatory"
        index="05"
          eyebrow="Compliance by Design"
          title="Built Against a Moving Regulatory Target"
          left={
            <p className={s.rowNote}>
              SEBI&rsquo;s February 2025 circular introduced India&rsquo;s first governance framework for
              retail algo trading &mdash; this changes how a system like Alkame must be classified.
            </p>
          }
          right={
            <div className="card">
              <p className={`${s.regBody} ${s.regBodySpaced}`}>
                Under SEBI Circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013 (Feb 2025), stockbrokers are
                the <span className={s.strongText}>principal</span>,
                and any algo provider acts as their{' '}
                <span className={s.strongText}>agent</span>. Algorithms
                are classified as disclosed or{' '}
                <span className={s.strongText}>undisclosed
                (&ldquo;black box&rdquo;)</span> — Alkame&rsquo;s ML ensemble falls in the latter category by
                construction.
              </p>
              <p className={s.regBody}>
                The project stays on the research/signal side of this line rather than automated execution
                &mdash; the compliance layer hard-blocks any output that reads as personalized advice or
                unauthorized order placement, avoiding the higher-friction execution regulatory bracket.
              </p>
              <p className={`${s.cite} ${s.citeSpaced}`}>SEBI, Feb 2025</p>
            </div>
          }
        />

      {/* 06 — Timeline */}
      <StickyRow
        id="timeline"
        index="06"
        eyebrow="Research Timeline"
        title="A 4-Month Applied Research Program"
        left={
          <p className={s.rowNote}>
            May through August 2026, moving from infrastructure and model-building through live validation
            and drift monitoring.
          </p>
        }
        right={
          <div className={s.timeline}>
            <div className={s.timelineRail} />
            <div className="stack">
              {timelineSteps.map((step) => (
                <div key={step.month} className={s.timelineItem}>
                  <div className={s.timelineDot} />
                  <p className={s.timelineMonth}>{step.month}</p>
                  <p className={s.timelineBody}>{step.body}</p>
                </div>
              ))}
            </div>
          </div>
        }
      />

      {/* Contributors — full width, needs the grid space */}
      <div id="team" className={s.teamBand}>
        <div className="container">
          <div className={s.teamHeader}>
            <div className="doclabel mb-2">§ 05 — CONTRIBUTING RESEARCH TEAM</div>
            <h2 className={s.teamTitle}>Interns Currently Working on Alkame</h2>
            <p className={s.teamLede}>
              Meet the DBERT interns actively contributing to this research program.
            </p>
          </div>
          <ContributorCards />
          <ContributorForm />
        </div>
      </div>

      {/* CTA */}
      <div className="container pad-block">
        <div className="bento-card callout">
          <h2 className="card-title">Want to Work on Projects Like This?</h2>
          <p className="page-lede">
            DBERT interns get hands-on placement on real, funded research programs like Alkame-Nifty50 &mdash;
            not simulated coursework. Apply through the internship platform to get matched to a live project.
          </p>
          <div className={s.ctaRow}>
            <a href="https://internship.dbert.online" target="_blank" rel="noopener noreferrer" className="btn btn-primary btn-lg">Apply on internship.dbert.online</a>
            <a href="/startups/register" className="btn btn-outline btn-lg">Get Similar Support for Your Startup</a>
          </div>
        </div>
      </div>
    </div>
  );
}
