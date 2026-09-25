import React from 'react';
import Link from 'next/link';
import DemoRequestForm from '@/components/ui/DemoRequestForm';
import PricingNotice from '@/components/ui/PricingNotice';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../ai-solutions.module.css';
import { Users, CheckCircle, GitPullRequest, Database, Shield, Award } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/products/intern-management-system');

export default function InternManagementPage() {
  const faqs = [
    {
      question: 'How does the portal connect with GitHub and Gitlab to audit intern pull requests?',
      answer: 'The system connects via explicit OAuth applications and webhook listeners to student Git repositories. When an engineering intern commits code or opens a pull request against a task milestone, the platform automatically parses commit velocity, tests test suite passing metrics, and logs the PR directly to the mentors review queue.'
    },
    {
      question: 'Can mentors issue cryptographically verifiable experience letters and diplomas upon completion?',
      answer: 'Yes. Upon satisfactory completion of designated internship sprints, authorized engineering mentors can generate signed digital Letters of Recommendation (LORs) and experience certificates embedded with unique SHA-256 validation IDs that link directly into our Certificate Verification API.'
    },
    {
      question: 'Is the underlying PostgreSQL and Prisma ORM schema customizable for custom institutional grading rules?',
      answer: 'Absolutely. The application utilizes structured Prisma ORM schema models that allow organizations to configure custom KPI milestones, weighted sprint rubrics, attendance tracking parameters, and specialized technical competency scorecards commensurate with internal engineering rubrics.'
    },
    {
      question: 'How do automated backup routines and encrypted registers protect student personal data?',
      answer: 'All academic transcripts, performance appraisals, and student personal identity parameters are secured at rest inside encrypted relational databases, augmented by daily encrypted snapshots and strict RBAC isolation to prevent unauthorized internal or external data access.'
    },
    {
      question: 'What deployment architectures are supported for universities and corporate upskilling programs?',
      answer: 'We deploy multi-tenant cloud instances hosted in reliable Indian data centers for scaling skill academies, as well as offline localized container deployments for corporate R&D divisions and universities requiring localized campus subnet operation.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareApplication',
        name: 'DBERT Intern Management System & Engineering Upskilling Portal',
        applicationCategory: 'BusinessApplication, EducationalApplication',
        operatingSystem: 'Cloud SaaS, Linux Subsystem, Docker Container, PostgreSQL',
        description: 'Comprehensive software portal designed to track student daily commit logs, supervise engineering mentor code reviews, and generate verifiable cryptographic completion letters.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Enterprise SaaS Licensing',
          price: '30000',
          priceCurrency: 'INR',
          description: 'Monthly SaaS licensing starting tier for technical universities and corporate internship programs',
          url: 'https://dbert.online/ai-solutions/products/intern-management-system'
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

      {/* Hero Header Section & What It Is */}
      <div className="container page-head">
        <div className="doclabel">
          § 01 — ENTERPRISE SAAS PRODUCT <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title">
          Accelerate Talent &mdash; From Apprentices to Production Engineers
        </h1>
        <p className="lede-wide">
          An end-to-end industrial training and internship management system that monitors student daily commit logs, audits sprint velocity, coordinates mentor code review queues, and automatically issues cryptographically verifiable project experience certificates.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Engineered to Power DBERT Industrial Training</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          We practice unwavering operational integrity: <strong>we build, deploy, and refine our enterprise software internally before licensing it commercially</strong>. The Intern Management System is the core operating system powering DBERT Labs Industrial Training programs and venture studio apprenticeships across India, coordinating rigorous daily technical evaluation for active learner cohorts.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              Managing hundreds of remote software engineering interns using scattered spreadsheets and ad-hoc email communications resulted in inconsistent mentor code feedback and unverified progress claims. We constructed a centralized, database-backed dashboard built over PostgreSQL and Prisma ORM that natively ties student sprint progress directly to GitHub pull request evaluations. Today, engineering organizations and educational bootcamps rely on our proven architecture to manage technical apprenticeship pipelines with precision.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/learners" className="accent-link text-xs font-mono font-medium">Explore DBERT Industrial Training &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Inspect Certificate Verification Registry &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Info Section (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container center">
          <div className="doclabel mb-2">§ 03 — ARCHITECTURAL ORCHESTRATION THESIS</div>
          <p className="band-lede max-w-3xl mx-auto text-white">
            Built on production PostgreSQL relational databases and type-safe Prisma ORM schemas, the portal delivers a responsive interface for engineering apprentices and senior technical mentors to collaborate on complex production software sprints without friction.
          </p>
        </div>
      </div>

      {/* Product Capabilities & How It Works (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — CORE ARCHITECTURAL SPECIFICATIONS</div>
        <h2 className="section-title mb-4">
          Engineered for Rigorous Technical Mentorship
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h3 className="block-title-sm">
              1. Automated Student Task Logging
            </h3>
            <p className="prose-sm text-muted">
              Track real-time student task chronologies, Git commit hashes, and weekly time-sprint goals within an intuitive visual progress dashboard.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Synchronized daily commit activity logs</li>
              <li>&bull; Automatic pull request submission checking</li>
              <li>&bull; Real-time Prisma database state transformations</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              2. Mentor Code Review Boards
            </h3>
            <p className="prose-sm text-muted">
              Empower engineering leaders to inspect student pull requests, document structural code critiques, and electronically authorize experience milestones.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Direct GitHub integration for repository audits</li>
              <li>&bull; Structured numerical scoring &amp; qualitative notes</li>
              <li>&bull; Automated issuance of digital graduation letters</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              3. Cryptographic Certificate Sync
            </h3>
            <p className="prose-sm text-muted">
              Synchronize student completion diplomas instantly with external employer lookup gateways, embedding unique cryptographic validation UUIDs.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Type-safe Prisma database relational adapters</li>
              <li>&bull; Instant JSON API endpoints for corporate lookups</li>
              <li>&bull; Encrypted daily database replication backups</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Compliance */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY &amp; COMPLIANCE RIGOR</div>
        <h2 className="section-title mb-2">Student Record Privacy &amp; Access Controls</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Academic transcripts and engineering appraisals demand absolute relational integrity. Our architecture guarantees multi-tenant data isolation and rigorous identity verification.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Multi-Tenant Data Isolation</h4>
            <p className="text-xs text-muted">
              Whether deployed for a single Indian technical university or a corporate training conglomerate, student identities and code review logs are strictly partitioned using schema-level tenant indexing, preventing cross-organization data leakage.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Cryptographic Audit Trails</h4>
            <p className="text-xs text-muted">
              Every mentor approval, score alteration, and certificate issuance triggers an immutable log entry stored within encrypted audit tables. This guarantees total transparency during statutory MSME or educational accreditation reviews.
            </p>
          </div>
        </div>
      </div>

      {/* Integrations Roster */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 06 — SYSTEM &amp; DATABASE INTEGRATIONS</div>
        <h2 className={s.techHeading}>Supported Enterprise Ecosystem Integrations</h2>
        <div className={s.techRow}>
          {["PostgreSQL", "Prisma ORM", "Next.js App Router", "GitHub Webhooks", "GitLab API", "REST / JSON", "Docker Container", "AWS / Azure", "SHA-256 Verification"].map((tool, idx) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Pricing & Commercial Licensing Tiers */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 07 — COMMERCIAL LICENSING &amp; DEPLOYMENT TIERS</div>
        <h2 className="section-title mb-2">Transparent Enterprise SaaS Licensing</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Configure structured monthly licensing bands tailored for Indian technical universities, startup skill bootcamps, and corporate internal developer training squads.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Academy Tier</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹30,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Designed for regional technical bootcamps and startup engineering apprenticeship intakes.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 100 active student accounts</li>
                <li>Automated GitHub PR commit tracking</li>
                <li>Standard business hour mentor onboarding</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-outline w-full mt-4">Select Academy Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">High Volume</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">University &amp; Enterprise</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹75,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive internship coordination for large corporate training arms and technical university networks.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 500 active student accounts</li>
                <li>Cryptographic certificate verification integration</li>
                <li>24/7 priority integration &amp; database support</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-primary w-full mt-4">Inquire Enterprise Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">On-Premise Custom</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Custom Scope</div>
              <p className="text-xs text-muted mt-2">Self-hosted Dockerized deployments engineered for corporate data center networks with zero telemetry.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Custom branding &amp; university subdomain</li>
                <li>Air-gapped local database execution</li>
                <li>Dedicated architectural engineering squad</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Discuss Custom Scope &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — PRODUCT TECHNICAL KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED AI SOLUTIONS &amp; INFRASTRUCTURE</div>
        <h2 className="section-title mb-4">Explore Complementary DBERT Platforms</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Certificate Verification API</h4>
            <p className="text-xs text-muted mb-3">Enable recruiters to instantly evaluate issued internship completion diplomas and LOR serial IDs.</p>
            <Link href="/ai-solutions/products/certificate-verification-api" className="accent-link text-xs">View Verification API &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Hiring Automation Suite</h4>
            <p className="text-xs text-muted mb-3">Streamline technical talent acquisition by auditing Git repositories and running automated resume scoring.</p>
            <Link href="/ai-solutions/products/hiring-automation-suite" className="accent-link text-xs">View Hiring Suite &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">DBERT Chat Console</h4>
            <p className="text-xs text-muted mb-3">Deploy secure RAG AI assistants over technical training documentation and enterprise Git codebases.</p>
            <Link href="/ai-solutions/products/dbert-chat" className="accent-link text-xs">View DBERT Chat &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Action Call & Demo Request */}
      <div className="container pb-block border-t border-line pt-12" id="demo-name">
        <div className="doclabel mb-2">§ 10 — SCHEDULE ENTERPRISE DEPLOYMENT</div>
        <PricingNotice />
        <DemoRequestForm productName="Intern Management System" />
      </div>
    </div>
  );
}
