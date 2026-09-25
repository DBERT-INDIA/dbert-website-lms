import React from 'react';
import Link from 'next/link';
import DemoRequestForm from '@/components/ui/DemoRequestForm';
import PricingNotice from '@/components/ui/PricingNotice';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import s from '../../ai-solutions.module.css';
import { Code, CheckCircle, FileCheck, Shield, Users, Layers } from 'lucide-react';

export const metadata = pageMetadata('/ai-solutions/products/hiring-automation-suite');

export default function HiringAutomationPage() {
  const faqs = [
    {
      question: 'How does automated Git code auditing improve upon traditional algorithmic algorithmic coding tests?',
      answer: 'Standard timed puzzle tests fail to reflect real-world engineering proficiency and trigger candidate friction. Our platform analyzes candidates actual public or submitted Git repositories—evaluating structural commit frequency, pull-request documentation clarity, test suite coverage, and modular design consistency against real production standards.'
    },
    {
      question: 'Can the resume scoring engine handle messy unstructured PDFs across diverse format variations?',
      answer: 'Yes. Powered by our core Document AI optical ingestion pipeline, the talent evaluation engine ingests varied multi-page PDF CVs, personal portfolios, and project descriptions, mapping demonstrated tools and project architectures against your specific job requirement schemas.'
    },
    {
      question: 'How do you identify code plagiarism or superficial generative AI code generation in portfolios?',
      answer: 'Our repository evaluation heuristics inspect semantic AST (Abstract Syntax Tree) patterns, anomalous commit timing spikes (e.g., thousands of lines committed in a single unreviewed timestamp), and structural similarity against public tutorial boilerplate, flagging suspicious submissions for interviewer review.'
    },
    {
      question: 'Does the hiring suite integrate with existing Human Resource Information Systems (HRIS) or Slack?',
      answer: 'Yes. The suite natively furnishes bidirectional webhook connectors and REST APIs capable of updating interview scorecard registries in greenhouse, Workday, BambooHR, and automating interview scheduling status notifications across corporate Slack and Microsoft Teams channels.'
    },
    {
      question: 'Is candidate interview application data stored securely in compliance with privacy regulations?',
      answer: 'All candidate resumes, code evaluation outputs, and internal reviewer feedback scorecards are encrypted in transit and at rest within isolated database tables, strictly adhering to enterprise data retention schedules and Indian data privacy standards.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareApplication',
        name: 'DBERT AI Hiring Automation & Technical Talent Intelligence Suite',
        applicationCategory: 'BusinessApplication, HumanResourceApplication',
        operatingSystem: 'Cloud SaaS, Web Application, REST API Webhooks',
        description: 'AI-driven technical recruitment suite automating developer resume scoring, Git repository commit auditing, and centralized evaluation pipelines.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Enterprise SaaS Licensing',
          price: '40000',
          priceCurrency: 'INR',
          description: 'Monthly SaaS licensing starting tier for technical staffing teams and venture HR squads',
          url: 'https://dbert.online/ai-solutions/products/hiring-automation-suite'
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
          Hire Smarter &mdash; AI-Driven Technical Talent Intelligence
        </h1>
        <p className="lede-wide">
          Accelerate technical recruitment by replacing superficial buzzword filtering with concrete engineering proof. Automate unstructured resume evaluation, execute multi-point Git repository code audits, and synchronize interviewer feedback across a unified intelligence dashboard.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Built for Our Indian Venture Studio Recruitment</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, we enforce a definitive operational mandate: <strong>we construct and execute our solutions internally before offering them commercially</strong>. The Hiring Automation Suite was originally built to streamline recruitment for our incubated venture studio technology squads and advanced industrial fellowship intakes, where we evaluate hundreds of engineering applicants every month.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              Reviewing hundreds of developer portfolios manually created an intolerable bottleneck for our senior technical leads, while traditional recruitment software merely matched superficial keyword occurrences without inspecting repository quality. We constructed an automated auditing pipeline that directly links to applicant GitHub profiles, parses commit velocity, and flags superficial AI boilerplate. Today, engineering organizations across India deploy our suite to hire verified technical talent with unprecedented precision.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/startups" className="accent-link text-xs font-mono font-medium">Explore Our Incubated Startup Network &rarr;</Link>
              <Link href="/learners/fellowship" className="accent-link text-xs font-mono font-medium">Inspect AI Engineering Fellowship &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Product Image Placeholder Section (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container center">
          <div className="doclabel mb-2">§ 03 — ARCHITECTURAL EVALUATION THESIS</div>
          <p className="band-lede max-w-3xl mx-auto text-white">
            Reviewing hundreds of technical resumes by hand is a devastating bottleneck for engineering leaders. Our platform bypasses keyword spam by scanning actual candidate codebases, auditing pull request documentation, identifying code cloning patterns, and delivering scored technical recommendations directly to your hiring panel.
          </p>
        </div>
      </div>

      {/* Product Capabilities & How It Works (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — CORE ARCHITECTURAL SPECIFICATIONS</div>
        <h2 className="section-title mb-4">
          Engineered for Deep Technical Scaffolding
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h3 className="block-title-sm">
              1. Semantic Resume Scoring
            </h3>
            <p className="prose-sm text-muted">
              Score candidate profiles based on how accurately their demonstrated project architectures and system toolchains map to your exact job specifications.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Parsing complex unstructured PDF &amp; LaTeX profiles</li>
              <li>&bull; Matching architectural skills utilizing semantic logic</li>
              <li>&bull; Automatic flagging of chronological inconsistencies</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              2. Git Code Auditing Engine
            </h3>
            <p className="prose-sm text-muted">
              Audit candidate code portfolios automatically, inspecting structural commit frequency, unit test coverage, and documentation rigor across active repos.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Evaluating pull-request communication rigor</li>
              <li>&bull; Auditing repository Readme and architecture design</li>
              <li>&bull; Detecting cloned tutorial boilerplate &amp; plagiarism</li>
            </ul>
          </div>

          <div className="bento-card">
            <h3 className="block-title-sm">
              3. Collaborative Evaluation Hub
            </h3>
            <p className="prose-sm text-muted">
              Coordinate technical candidate interviews and synthesize scoring consensus across engineering panels in a secure centralized dashboard.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Unified scorecard &amp; architectural feedback forms</li>
              <li>&bull; Permanent technical interview transcript logs</li>
              <li>&bull; Automated status update webhook notifications</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Compliance */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY &amp; COMPLIANCE RIGOR</div>
        <h2 className="section-title mb-2">Candidate Data Protection &amp; RBAC</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          Technical hiring involves highly confidential corporate evaluations and personal candidate records. Our suite enforces strict architectural isolation and role-based clearance boundaries.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Role-Based Access Control (RBAC)</h4>
            <p className="text-xs text-muted">
              Configure fine-grained access boundaries between HR generalists, external technical interviewers, and VP of Engineering evaluators. External interviewers view relevant repository scorecards without accessing compensation metadata or historical hiring transcripts.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Encrypted Record Persistence</h4>
            <p className="text-xs text-muted">
              All parsed applicant profiles, GitHub personal authentication tokens, and algorithmic assessment scores are encrypted at rest via AES-256 within secure relational database schemas, ensuring compliance with Indian data privacy statutes.
            </p>
          </div>
        </div>
      </div>

      {/* Integrations Roster */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 06 — SYSTEM &amp; DATABASE INTEGRATIONS</div>
        <h2 className={s.techHeading}>Supported Enterprise Ecosystem Integrations</h2>
        <div className={s.techRow}>
          {["GitHub API", "GitLab SDK", "PostgreSQL", "Prisma ORM", "Greenhouse HR", "Workday API", "Slack / Teams", "Docker RunTime", "REST Webhooks"].map((tool, idx) => (
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
          Scale your technical evaluation velocity with predictable monthly software licenses tailored for Indian venture technology teams and enterprise recruitment organizations.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Startup Squad Tier</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹40,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Engineered for agile startup developer teams evaluating quarterly technical apprenticeship and engineering cohorts.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 250 candidate repository audits/mo</li>
                <li>Automated PDF semantic CV scoring</li>
                <li>Standard business hour engineering SLA</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-outline w-full mt-4">Select Startup Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">High Growth</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">Enterprise Recruiting</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹95,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Comprehensive hiring automation for scaling venture-backed corporations and high-volume talent platforms.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 1,500 candidate repository audits/mo</li>
                <li>Plagiarism &amp; generative boilerplate detection</li>
                <li>Dedicated HRIS &amp; Slack webhook integration</li>
              </ul>
            </div>
            <Link href="#demo-request" className="btn btn-primary w-full mt-4">Inquire Enterprise Tier &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Venture Studio Custom</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Custom Scope</div>
              <p className="text-xs text-muted mt-2">Tailored engineering recruitment architectures combined with direct talent pipeline access from DBERT Labs.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Custom repository code heuristic evaluation</li>
                <li>Direct pipeline integration with DBERT fellows</li>
                <li>Co-engineered interview technical challenges</li>
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
            <h4 className="font-mono text-sm font-bold text-white mb-1">Intern Management System</h4>
            <p className="text-xs text-muted mb-3">Manage hired technical apprentices, monitor daily sprint commits, and streamline review mentorship.</p>
            <Link href="/ai-solutions/products/intern-management-system" className="accent-link text-xs">View Intern Portal &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Certificate Verification API</h4>
            <p className="text-xs text-muted mb-3">Cryptographically authenticate candidate graduation diplomas and recommendation letters in real time.</p>
            <Link href="/ai-solutions/products/certificate-verification-api" className="accent-link text-xs">View Verification API &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Document AI Extraction</h4>
            <p className="text-xs text-muted mb-3">Convert unstructured PDF candidate portfolios and financial contracts into strict JSON schemas.</p>
            <Link href="/ai-solutions/products/document-ai" className="accent-link text-xs">View Document AI &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Action Call & Demo Request */}
      <div className="container pb-block border-t border-line pt-12" id="demo-request">
        <div className="doclabel mb-2">§ 10 — SCHEDULE ENTERPRISE DEPLOYMENT</div>
        <PricingNotice />
        <DemoRequestForm productName="Hiring Automation Suite" />
      </div>
    </div>
  );
}
