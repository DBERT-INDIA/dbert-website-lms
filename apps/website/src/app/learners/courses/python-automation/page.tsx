import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../learners.module.css';
import { Bot, Bug, Settings, CheckCircle, ShieldCheck } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/python-automation');

export default function PythonAutomationCoursePage() {
  const faqs = [
    {
      question: 'Is prior experience with Python required to succeed in the automation engineering track?',
      answer: 'This track assumes introductory familiarity with variables, loops, and conditional statements. Beginners without prior exposure to terminal environments are encouraged to complete our foundational Launchpad prep modules before beginning advanced Selenium and asynchronous scraping pipelines.'
    },
    {
      question: 'How do you address dynamic scraping limitations and anti-bot rate defenses in modern web systems?',
      answer: 'Our curriculum goes far beyond simple static BeautifulSoup requests. You master production browser automation utilizing headless Selenium, Playwright, and Puppeteer, alongside robust residential proxy rotation, custom HTTP header forgery, and automated session cookie persistence.'
    },
    {
      question: 'Can I autonomously schedule and deploy these scraping pipelines in cloud container environments?',
      answer: 'Yes. You receive hands-on instruction in deploying distributed Celery worker queues backed by Redis data stores, setting up reliable Linux cron job scheduling schedules inside reproducible Docker container infrastructures.'
    },
    {
      question: 'How does DBERT verify my automation engineering credentials for potential corporate recruiters?',
      answer: 'Upon passing our technical code review milestones, your completion certificate is entered directly into our global institutional validation database. Employers can inspect your credential authenticity directly by inputting your unique serial code at dbert.online/verify.'
    },
    {
      question: 'What types of roles and compensation ranges do graduates of this track target in India?',
      answer: 'Graduates actively recruit for specialized engineering roles including QA Automation Engineer, Python Scraping Developer, Backend Tooling Specialist, and Data Pipeline Analyst, commanding verified starting compensation tiers ranging from ₹3.5 LPA to ₹8.0 LPA across emerging technology firms.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Python Automation, Web Scraping & Bot Engineering Track',
        description: 'Professional automation engineering course in India teaching scalable data extraction, dynamic browser scripting, Selenium, Playwright, Celery task scheduling, and anti-scraping bypass architectures.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        courseCode: 'DBERT-ENG-PYAUT-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified Python Automation Systems Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '28000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.online/learners/courses/python-automation'
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
          Become a Python Automation &amp; Scraping Engineer
        </h1>
        <p className={s.courseTagline}>
          ₹3,50,000 – ₹8,00,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Acquire the programming proficiency to automate industrial workflows, harvest high-frequency web data, configure concurrent asynchronous worker queues, and engineer resilient browser bots utilizing Python, Selenium, Playwright, and Celery.
        </p>
      </div>

      {/* Key Metrics Grid (Secondary BG) */}
      <div className="section-band">
        <div className="container">
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Bug aria-hidden="true" /></span>
              <h3 className="accent-note">Advanced Scraping</h3>
              <p className="text-sm">Master dynamic residential proxy rotation arrays, browser header customization, and anti-bot bypass protocols.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Settings aria-hidden="true" /></span>
              <h3 className="accent-note">Task Schedulers</h3>
              <p className="text-sm">Configure continuous cron jobs, webhook event listeners, and concurrent distributed asynchronous task queues with Celery.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Bot aria-hidden="true" /></span>
              <h3 className="accent-note">Browser Scripting</h3>
              <p className="text-sm">Automate complex JavaScript-heavy web layouts and authentication forms utilizing Selenium and Playwright.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Course Curriculum & Skills (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — TECHNICAL CURRICULUM ARCHITECTURE</div>
        <h2 className="section-title mb-4">
          What You&apos;ll Master
        </h2>
        <div className="bento-grid-2">
          <div className="bento-card">
            <h3 className="block-title">
              1. Web Scraping &amp; Data Extraction Pipelines
            </h3>
            <p className="prose-sm text-muted">
              Extract high-integrity enterprise records from challenging target architectures. Master HTML DOM tree navigation, unauthorized JSON API endpoint interrogation, and payload normalizations.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Advanced DOM traversals via reliable CSS selectors and XPath regex</li>
              <li>&bull; Executing persistent authenticated connections with Python Requests sessions</li>
              <li>&bull; Parsing raw response blocks and serializing tabular data feeds systematically</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title">
              2. Browser Automation &amp; Asynchronous Task Scheduling
            </h3>
            <p className="prose-sm text-muted">
              Interact deterministically with single-page web applications. Automate human interaction patterns including element clicking, secure form inputs, DOM scrolling, and CAPTCHA handling solutions.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Configuring headless WebDriver binaries, explicit waits &amp; exception traps</li>
              <li>&bull; Dynamic SPA scraping using modern Playwright &amp; Selenium architectures</li>
              <li>&bull; Orchestrating concurrent background execution loops via Celery &amp; Redis</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Instructor E-E-A-T & Leadership Profile Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 03 — INSTRUCTOR LEADERSHIP &amp; PROVENANCE</div>
        <h2 className="section-title mb-2">Taught by Active Software Test &amp; Data Engineers</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Learn automation engineering from industry practitioners who actively design corporate web scraping infrastructures and data mining pipelines across our venture studio portfolio and commercial SaaS deployments.
        </p>
        
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <div className="flex align-center gap-2 mb-1">
              <span className="font-mono text-sm text-white font-bold">DBERT Systems Engineering Leadership</span>
              <span className="badge badge-emerald text-xs">Active Industry Practitioners</span>
            </div>
            <p className="text-xs text-muted leading-relaxed mb-4">
              Our engineering mentors supervise ongoing technical audits across our incubated startups and actively engineer our enterprise data ingestion tools (such as our Document AI optical parser). You master resilient programming idioms from mentors who overcome IP blacklists and structural DOM mutations daily.
            </p>
            <div className="stack-h gap-4">
              <Link href="/about/team" className="accent-link text-xs font-mono font-medium">Meet Our Engineering Faculty &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify MSME Institutional Accreditation &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Projects Section (Secondary BG) */}
      <div className="section-band-lg border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 04 — CAPSTONE PRODUCTION PROJECTS</div>
          <h2 className="section-title mb-4">
            Production Projects You&apos;ll Ship to Your Git Repository
          </h2>
          <div className="bento-grid-2">
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 1 &middot; Automated Intelligence</span>
              <h3 className={s.projectTitle}>High-Frequency Retail Valuation Monitor</h3>
              <p className="prose-sm text-muted">
                An automated concurrent scraping pipeline utilizing Python and Playwright to harvest pricing inventories across major Indian e-commerce marketplaces, structure SQLite transactional tables, and trigger real-time markdown alerts via Twilio and WhatsApp REST endpoints.
              </p>
            </div>
            <div className="bento-card on-ink">
              <span className="pill">Capstone Project 2 &middot; Asynchronous Workers</span>
              <h3 className={s.projectTitle}>Autonomous Social Media Analytics Engine</h3>
              <p className="prose-sm text-muted">
                An industrial backend scheduler utilizing Celery and Redis to dispatch automated social engagement queries, parse dynamic public profiling metrics, extract sentiment markers, and deposit cleaned time-series arrays into PostgreSQL monitoring databases.
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
          We practice absolute financial transparency. Enroll directly with our straightforward upfront tuition or utilize flexible Zero-Cost EMI schedules through verified Indian educational lending partners.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹28,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Covers synchronous practical instruction, Docker simulation lab access, comprehensive pull-request reviews, and global certification database entry.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Permanent access to recorded automation code architectures</li>
              <li>Weekly 1-on-1 code review optimization sessions</li>
              <li>Direct hiring referral recommendations for audited graduates</li>
            </ul>
            <Link href="/learners/launchpad?domain=python-automation" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹3,111 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Available via authorized banking partnerships with zero processing surcharges or security deposit requirements for qualified candidates.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Expediated digital financial verification protocol</li>
              <li>Immediate course and lab access upon installment authorization</li>
              <li>Complete structural parity with lump-sum fee applicants</li>
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
          {["Python", "Selenium", "Playwright", "BeautifulSoup", "Requests", "Celery", "Redis", "cron", "Docker", "Git", "SQLite", "XPath"].map((tool, idx) => (
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
          <h2 className="card-title text-2xl font-bold text-white mb-2">Automate Industrial Systems &mdash; Launch Your Career</h2>
          <p className="page-lede text-sm text-muted max-w-xl mx-auto mb-6">
            Ready to write scalable scraping scripts, configure automated concurrent tasks, and deploy proxy rotation architectures directly to your professional portfolio? Apply for DBERT Industrial Training today.
          </p>
          <div className="stack-h gap-4 justify-center">
            <Link href="/learners/launchpad" className="btn btn-primary btn-lg">Choose Your Career Path &rarr;</Link>
            <Link href="/blog/non-tech-to-ai-career" className="btn btn-outline btn-lg">Read Pathway Guide for Switchers</Link>
          </div>
        </div>
      </div>
    </div>
  );
}

