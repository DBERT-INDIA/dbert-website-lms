import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../learners.module.css';
import { ChartColumn, Database, TrendingUp, CheckCircle, ShieldCheck, GitBranch, ExternalLink } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/data-analytics');

export default function DataAnalyticsCoursePage() {
  const faqs = [
    {
      question: 'Do I require an advanced mathematical or computer science background to commence data analytics?',
      answer: 'No. While foundational analytical curiosity is beneficial, our curriculum explicitly teaches practical business statistics, SQL database logic, and Python Pandas syntax from the ground up without relying on complex theoretical calculus derivations.'
    },
    {
      question: 'Why does DBERT prioritize Python Pandas alongside SQL and Power BI over spreadsheet formulas alone?',
      answer: 'Standard business spreadsheets collapse under high-volume enterprise corporate transaction streams. By commanding programmatic Python Pandas arrays and optimized SQL database indexing, you can process millions of operational rows, automate repetitive reporting pipelines, and construct dynamic real-time Power BI executive dashboards seamlessly.'
    },
    {
      question: 'Can prospective employers independently authenticate my completed data analytics certification?',
      answer: 'Yes. Upon submitting validated database queries and dashboard repositories to our review faculty, your completed certificate is inscribed into our public verification portal at dbert.online/verify, enabling instant cryptographic HR checks.'
    },
    {
      question: 'How are technical data analysis projects integrated into real-world GitHub portfolios?',
      answer: 'You analyze complex, messy industrial datasets—including transactional retail logs, financial server metrics, and user engagement chronologies. All transformation scripts and schema normalizations are committed directly to your personal GitHub repository, providing concrete proof of competency.'
    },
    {
      question: 'What professional roles and starting remuneration packages do analytics graduates command in India?',
      answer: 'Graduates pursue high-impact commercial positions such as Data Analyst, BI Reporting Specialist, SQL Database Engineer, and Business Systems Analyst, attaining verified initial compensation structures ranging between ₹3.5 LPA and ₹9.0 LPA across established Indian corporate ecosystems.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Data Analytics, SQL Schemas & Executive Business Intelligence Track',
        description: 'Comprehensive data analytics engineering course in India teaching Python Pandas pipelines, advanced SQL JOINs, database normalization, and interactive Power BI executive dashboards.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        courseCode: 'DBERT-ENG-DATA-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified Professional Data Analytics & BI Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '28000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.online/learners/courses/data-analytics'
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

      {/* Hero Header Section */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — CAREER TRACK <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Become a Data Analytics &amp; BI Professional
        </h1>
        <p className={s.courseTagline}>
          ₹3,50,000 – ₹9,00,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master the analytical methods required to ingest, clean, normalize, and visualize large corporate enterprise data streams. Command programmatic Python Pandas pipelines, advanced SQL database query schemas, and interactive Power BI executive dashboards.
        </p>
      </div>

      {/* Key Metrics Grid (Secondary BG) */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><ChartColumn aria-hidden="true" /></span>
              <h3 className="accent-note">Data Modeling</h3>
              <p className="text-sm">Clean, merge, and aggregate large tabular business datasets programmatically using Python Pandas &amp; NumPy.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Database aria-hidden="true" /></span>
              <h3 className="accent-note">SQL Engineering</h3>
              <p className="text-sm">Write high-performance database queries: executing complex INNER/LEFT joins, nested subqueries, and indexes.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><TrendingUp aria-hidden="true" /></span>
              <h3 className="accent-note">Executive BI</h3>
              <p className="text-sm">Assemble interactive corporate analytical dashboards and key performance indicator (KPI) charts in Power BI.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Reference Repositories by Role Specialization */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — PRODUCTION REPOSITORIES BY INTERN ROLE</div>
        <h2 className="section-title mb-4">
          Open-Source Codebases You&apos;ll Build &amp; Contribute To
        </h2>
        <div className="grid gap-4 md:grid-cols-2">
          {/* Repo 1: Aivara Technologies */}
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="badge badge-emerald text-xs font-mono">Aivara Technologies Cohort</span>
                <span className="badge badge-cyan text-xs font-mono">BI &amp; Analytics Engineer</span>
              </div>
              <h3 className="font-mono text-base font-bold text-white mb-1">Aivara-Technologies / aivara-insight-lite</h3>
              <p className="text-xs text-muted leading-relaxed mb-4">
                Automated CSV ingestion, semantic column classification, KPI and driver/variance decomposition in Pandas, budget-capped LLM insights via OpenRouter, and offline PowerPoint (.pptx) deck generation.
              </p>
              <div className="flex flex-wrap gap-1.5 mb-4">
                {['CSV Sniffer', 'Semantic Classifier', 'Driver Decomposition', 'python-pptx Export'].map((mod, i) => (
                  <span key={i} className="text-[11px] px-2 py-0.5 rounded bg-raise border border-line text-zinc-300 font-mono">
                    {mod}
                  </span>
                ))}
              </div>
            </div>
            <a
              href="https://github.com/Aivara-Technologies/aivara-insight-lite"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-outline btn-sm font-mono text-xs inline-flex items-center gap-2 self-start"
            >
              <GitBranch className="w-3.5 h-3.5" />
              <span>Inspect Aivara Repo</span>
              <ExternalLink className="w-3 h-3 text-muted" />
            </a>
          </div>

          {/* Repo 2: Alkame Nifty-50 */}
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="badge badge-emerald text-xs font-mono">Alkame Capital Track</span>
                <span className="badge badge-cyan text-xs font-mono">Quantitative Market Analyst</span>
              </div>
              <h3 className="font-mono text-base font-bold text-white mb-1">Alkameinc / alkame-nifty-50-educational</h3>
              <p className="text-xs text-muted leading-relaxed mb-4">
                Quantitative market data engine for the Nifty 50 index — time-series market fetchers, statistical volatility modeling, backtesting engines, and Plotly Dash visualizers.
              </p>
              <div className="flex flex-wrap gap-1.5 mb-4">
                {['Market Data Ingestion', 'Feature Engineering', 'Backtesting Simulator', 'Plotly Dash'].map((mod, i) => (
                  <span key={i} className="text-[11px] px-2 py-0.5 rounded bg-raise border border-line text-zinc-300 font-mono">
                    {mod}
                  </span>
                ))}
              </div>
            </div>
            <a
              href="https://github.com/Alkameinc/alkame-nifty-50-educational"
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-outline btn-sm font-mono text-xs inline-flex items-center gap-2 self-start"
            >
              <GitBranch className="w-3.5 h-3.5" />
              <span>Inspect Alkame Repo</span>
              <ExternalLink className="w-3 h-3 text-muted" />
            </a>
          </div>
        </div>
      </div>

      {/* Course Curriculum & Skills (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 03 — TECHNICAL CURRICULUM ARCHITECTURE</div>
        <h2 className="section-title mb-4">
          What You&apos;ll Master
        </h2>
        <div className="bento-grid-2">
          <div className="bento-card">
            <h3 className="block-title">
              1. Automated Ingestion &amp; Semantic Classification
            </h3>
            <p className="prose-sm text-muted">
              Parse arbitrary enterprise CSVs without pre-cleaning. Implement robust delimiter sniffing, encoding detection, and rule-based semantic typing for dates, metrics, dimensions, and IDs.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Ingestion robustness: csv.Sniffer, charset-normalizer &amp; tolerant pandas loaders</li>
              <li>&bull; Semantic classification: dates, continuous metrics, grouping dimensions &amp; IDs</li>
              <li>&bull; Driver decomposition: computing categorical contribution shares &amp; variance lift</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title">
              2. Local Analytics, Budgeted LLMs &amp; Deck Export
            </h3>
            <p className="prose-sm text-muted">
              Compute KPIs, trends, and risk signals purely in Pandas. Package pre-computed facts for budget-capped LLM narration, and assemble offline PowerPoint (.pptx) decks with python-pptx and Plotly.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; KPI cards, period-over-period trend deltas &amp; statistical anomaly detection</li>
              <li>&bull; Facts packets JSON construction &amp; OpenRouter token budget ceilings</li>
              <li>&bull; Automated offline PowerPoint (.pptx) deck generation with python-pptx</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Instructor E-E-A-T & Leadership Profile Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 04 — INSTRUCTOR LEADERSHIP &amp; PROVENANCE</div>
        <h2 className="section-title mb-2">Taught by Experienced Enterprise Data Engineers</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We reject academic data science abstractions. Your SQL schemas and Pandas transformation pipelines are reviewed directly by industry data analysts who manage real corporate transaction indexing and enterprise dashboards across our incubated startup ecosystem.
        </p>
        
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <div className="flex align-center gap-2 mb-1">
              <span className="font-mono text-sm text-white font-bold">DBERT Data Analytics Leadership Team</span>
              <span className="badge badge-emerald text-xs">Active Industry Practitioners</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-4">
              Our faculty members supervise analytical database normalization and performance reporting for our venture studio portfolios and commercial enterprise products. You learn verified data modeling conventions from instructors who extract operational clarity from messy real-world databases daily.
            </p>
            <div className="stack-h gap-4">
              <Link href="/about/team" className="accent-link text-xs font-mono font-medium">Meet Our Data Systems Faculty &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify MSME Statutory Registrations &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Projects Section (Secondary BG) */}
      <div className="section-band-lg border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 05 — CAPSTONE PRODUCTION PROJECTS</div>
          <h2 className="section-title mb-4">
            Production Projects You&apos;ll Ship to Your Git Repository
          </h2>
          <div className="bento-grid-2">
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 1 &middot; Aivara Insight Lite</span>
              <h3 className={s.projectTitle}>Automated CSV Analytics &amp; PPTX Deck Generator</h3>
              <p className="prose-sm text-muted">
                Modeled after Aivara Technologies&apos; Aivara Insight Lite: automated arbitrary CSV parsing, semantic column typing, driver decomposition, Streamlit executive dashboard, budget-capped LLM insights via OpenRouter, and 100% offline PowerPoint (.pptx) deck generation with python-pptx and Plotly kaleido.
              </p>
            </div>
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 2 &middot; Quantitative Analytics</span>
              <h3 className={s.projectTitle}>Nifty 50 Market Indicator &amp; Backtesting Engine</h3>
              <p className="prose-sm text-muted">
                Consolidating high-frequency financial time series from the Alkame Nifty-50 codebase, calculating rolling technical indicators (RSI, Bollinger Bands, Sharpe ratio), simulating trade execution slippage, and serving interactive Plotly Dashboards.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Transparent Tuition & Zero-Cost EMI Table */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 05 — TUITION INVESTMENT &amp; EMI SCHEDULES</div>
        <h2 className="section-title mb-2">Transparent Indian Tuition &amp; Zero-Cost Financing</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We maintain rigorous fee disclosures without hidden enrollment surcharges or coercive post-placement wage deductions. Enrol with our upfront tuition model or utilize flexible Zero-Cost EMI schedules overseen by approved banking partners.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹28,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Includes synchronous interactive cohort instruction, database cloud laboratory access, personalized query reviews, and official credential registry entry.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Permanent access to all live training query scripts &amp; arrays</li>
              <li>Weekly personalized 1-on-1 analytical review discussions</li>
              <li>Expediated referral inclusion across enterprise hiring networks</li>
            </ul>
            <Link href="/learners/launchpad?domain=data-analytics" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹3,111 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Structured through authorized Indian institutional banking networks with zero processing charges or security deposit requirements for verified candidates.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Expediated digital financial eligibility validation</li>
              <li>Immediate course and lab activation upon installment signing</li>
              <li>Full structural equivalence to upfront tuition benefits</li>
            </ul>
            <Link href="/about/contact" className="btn btn-outline w-full">Inquire About EMI Financing</Link>
          </div>
        </div>
      </div>

      {/* Tools Section (Primary BG) */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 06 — CORE TECHNICAL TOOLING</div>
        <h2 className={s.techHeading}>Production Technologies Mastered</h2>
        <div className={s.techRow}>
          {["Python", "Pandas", "NumPy", "SQL", "PostgreSQL", "Power BI", "Excel", "Matplotlib", "Seaborn", "Git", "Jupyter", "SQLite"].map((tool, idx) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 07 — CAREER TRACK KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* CTA Block */}
      <div className="container pb-block">
        <div className="bento-card callout-plain p-8 border border-line bg-card text-center">
          <div className="doclabel mb-1">§ 08 — INITIALIZE CAREER ACCELERATION</div>
          <h2 className="card-title text-2xl font-bold text-white mb-2">Transform Corporate Data Into Your Career Advantage</h2>
          <p className="page-lede text-sm text-muted max-w-xl mx-auto mb-6">
            Ready to write optimized SQL queries, programmatically normalise enterprise datasets with Pandas, and construct interactive executive BI dashboards directly for your verified portfolio? Apply for DBERT Industrial Training today.
          </p>
          <div className="stack-h gap-4 justify-center">
            <Link href="/learners/launchpad" className="btn btn-primary btn-lg">Choose Your Career Path &rarr;</Link>
            <Link href="/blog/non-tech-to-ai-career" className="btn btn-outline btn-lg">Read Career Guide for Non-Tech Switchers</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

