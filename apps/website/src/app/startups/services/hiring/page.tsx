import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import { Briefcase, Timer, Users, ShieldCheck, CheckCircle, Code } from 'lucide-react';
import HandNote from '@/components/ui/HandNote';
import HandDrawnArrow from '@/components/ui/HandDrawnArrow';

export const metadata = pageMetadata('/startups/services/hiring');

export default function HiringServicePage() {
  const steps = [
    { number: '01', title: 'Talent Pool Filtration', description: 'We filter through our verified talent directory of 1,500+ DBERT learners, evaluating actual commit velocities and GitHub repository architectures.' },
    { number: '02', title: '15-Day Stack Alignment Sprint', description: 'Selected candidates complete a zero-cost 15-day alignment sprint matching your precise database models, API routing frameworks, and codebase structure.' },
    { number: '03', title: 'Onboarding & Contract Execution', description: 'We facilitate NDA execution, verify cryptographic credential serial IDs, and support continuous technical integration without agency commissions.' }
  ];

  const faqs = [
    {
      question: 'Why do incubated startups pay 0% hiring commissions or recruiter placement fees?',
      answer: 'Our venture studio mission is to ensure incubated portfolio companies succeed technically and operationally. As an industrial training pioneer, our economic value is generated through engineering skill development and early startup equity—not by charging startups exploitative recruitment finder commissions or talent brokerage fees.'
    },
    {
      question: 'How does the free 15-day technical alignment sprint work before formal full-time onboarding?',
      answer: 'Before a startup formally extends an employment contract or internship offer, selected DBERT learners spend 15 operational days paired with your technical leadership in a supervised trial sprint. They configure your localized dev environment, inspect your schema, and resolve real introductory repository tasks to prove cultural and architectural alignment.'
    },
    {
      question: 'What specific technologies and architectural paradigms are DBERT candidate developers vetted on?',
      answer: 'Our developer talent pool undergoes intensive hands-on verification across cutting-edge AI systems and modern full-stack frameworks: Next.js App Router, TypeScript, React 19, PostgreSQL pgvector RAG indexes, Python FastAPI, Ollama localized weights serving, Docker containerization, and strict Git PR review rubrics.'
    },
    {
      question: 'Can we utilize your automated hiring suite to audit candidates sourced outside the DBERT network?',
      answer: 'Yes. While incubated companies gain priority access to our pre-vetted learner directory, startups can also license our AI Hiring Automation Suite to run semantic resume scoring and GitHub code plagiarism checks against external candidate pools.'
    },
    {
      question: 'How do you guarantee candidate credential authenticity and verify past project training records?',
      answer: 'Every candidate diploma, internship experience letter, and capstone GitHub project history is encoded within our cryptographic Certificate Verification API. You can instantly audit SHA-256 validation tokens directly through our online verification gateway.'
    }
  ];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Service',
        name: 'DBERT Venture Talent & AI Engineering Hiring Support',
        serviceType: 'Technical Recruitment, Developer Alignment Sprints, Engineering Talent Directory',
        description: 'Access 1,500+ pre-vetted AI developers and full-stack engineers with 0% recruitment commission fees and a 15-day pre-onboarding technical alignment sprint.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.online'
        },
        offers: {
          '@type': 'Offer',
          category: 'Venture Studio Talent Onboarding',
          price: '0',
          priceCurrency: 'INR',
          description: '0% sourcing commission fees for incubated startups utilizing our vetted developer directory',
          url: 'https://dbert.online/startups/services/hiring'
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
          § 01 — VENTURE HIRING SERVICE <span className="rev">rev: 2026.2</span>
        </div>
        <h1 className="page-title relative inline-block">
          Assemble the AI Engineering Team That Ships
          <HandNote className="absolute -right-12 -top-6 text-lg hidden md:block" tone="blue">
            Zero risk!
          </HandNote>
        </h1>
        <p className="lede-wide">
          Stop relying on generic recruitment boards and superficial whiteboard algorithmic puzzle tests. Access DBERT&apos;s exclusive directory of 1,500+ pre-vetted AI engineers and execute a zero-risk 15-day technical alignment sprint directly on your codebase before making formal hiring commitments.
        </p>
      </div>

      {/* Born-From Origin Section (Operational Provenance) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 02 — OPERATIONAL PROVENANCE &amp; ORIGIN</div>
        <h2 className="section-title mb-2">Born From Training India&apos;s Next Engineering Cohort</h2>
        <p className="prose-sm text-muted mb-6 max-w-3xl">
          At DBERT Labs, our venture talent practice is founded on absolute operational synergy: <strong>we recruit and test our developers inside real production environments before connecting them to startups</strong>. Our Hiring Support service originated directly from our flagship Industrial Training cohorts, where hundreds of Indian engineering fellows undergo exhaustive mentorship across RAG pipelines, MLOps, and scalable full-stack development.
        </p>
        <div className="card p-6 bg-card border border-line flex flex-col md:flex-row gap-6 align-center">
          <div className="flex-1">
            <span className="font-mono text-xs text-accent uppercase font-bold tracking-wider">The Engineering Motivation</span>
            <p className="text-xs text-muted leading-relaxed mt-2">
              We witnessed portfolio startup founders spending 30% of their seed capital on recruiter headhunter commissions, only to spend months terminating candidates whose real-world coding abilities failed to match their interview bravado. By bridging our validated engineering fellowship graduates directly with incubated startups, we eliminate recruiting agency fees entirely and replace theoretical guesswork with documented commit histories.
            </p>
            <div className="stack-h gap-4 mt-4">
              <Link href="/ai-solutions/products/hiring-automation-suite" className="accent-link text-xs font-mono font-medium">Inspect AI Hiring Automation Suite &rarr;</Link>
              <Link href="/verify" className="accent-link text-xs font-mono font-medium">Verify Candidate Cryptographic Credentials &rarr;</Link>
            </div>
          </div>
        </div>
      </div>

      {/* Key Metrics Grid (Secondary BG) - Why It Matters */}
      <div className="section-band border-t border-b border-line">
        <div className="container">
          <div className="doclabel mb-2">§ 03 — TALENT METRICS &amp; COMMERCIAL ADVANTAGES</div>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Users aria-hidden="true" /></span>
              <h3 className="accent-note">1,500+ Vetted Engineers</h3>
              <p className="text-sm">Access our audited candidate directory specializing in modern AI agent orchestration, PostgreSQL pgvector, and full-stack systems.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Timer aria-hidden="true" /></span>
              <h3 className="accent-note">15-Day Alignment Sprint</h3>
              <p className="text-sm">Pre-train selected developers directly on your specific API routing frameworks and database schemas before signing contracts.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
              <h3 className="accent-note">0% Sourcing Commissions</h3>
              <p className="text-sm">Incubated portfolio startups pay zero recruiter commissions, brokerage finding fees, or staffing agency retainers for team hires.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Core Deliverables (Primary BG) */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 04 — TALENT ONBOARDING DELIVERABLES</div>
        <h2 className="section-title mb-4">
          How We Build Your High-Performance Engineering Squad
        </h2>
        <div className="bento-grid-3">
          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              1. Audited Candidate Directory
            </h4>
            <p className="prose-sm text-muted">
              Access engineering fellows who have mastered our industrial training tracks—developing live RAG systems, managing Docker container microservices, and passing real architecture reviews.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Detailed hands-on coding &amp; commit quality scorecards</li>
              <li>&bull; GitHub repository AST validation and architecture reports</li>
              <li>&bull; Direct reference evaluations from senior DBERT engineering leaders</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              2. Custom Alignment Sprints
            </h4>
            <p className="prose-sm text-muted">
              We design and coordinate a free 15-day pre-onboarding alignment program. Selected candidate developers familiarize themselves with your exact Git workflows before formal signing.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Framework-specific technical task modules &amp; tutorials</li>
              <li>&bull; Mentor-supervised codebase repository walkthroughs</li>
              <li>&bull; Introductory feature code commits prior to contract execution</li>
            </ul>
          </div>

          <div className="bento-card">
            <h4 className="block-title font-mono text-sm uppercase text-white mb-2">
              3. Operational Handoff Support
            </h4>
            <p className="prose-sm text-muted">
              Ensure strict statutory and legal compliance. We facilitate standard NDA agreements, audit recommendation letters via cryptographic verification, and support team integration.
            </p>
            <ul className="feature-list text-xs space-y-1 mt-3">
              <li>&bull; Automated drafting of employee NDAs &amp; IP assignment terms</li>
              <li>&bull; Remote developer activity tracking and Git sprint metrics</li>
              <li>&bull; Cryptographic registration of graduation achievement serial IDs</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Enterprise Security & Risk Mitigation */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — SECURITY &amp; RECRUITMENT RISK MITIGATION</div>
        <h2 className="section-title mb-2">Eliminating Technical Resume Hallucinations</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          The proliferation of generative AI tools has rendered standard resume screening and remote take-home coding assessments obsolete. We institute structural defensive verification.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-4">
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Anti-Plagiarism Repo Inspection</h4>
            <p className="text-xs text-muted">
              Before presenting any engineering candidate, our algorithms audit their submitted project repositories for synthetic generated boilerplate, anomalous timestamp spikes, and cloned tutorial code—ensuring authentic engineering proficiency.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-2">Cryptographic Diploma Authentication</h4>
            <p className="text-xs text-muted">
              Every learner achievement record in our directory is permanently embedded within an immutable relational database indexed by a SHA-256 cryptographic hash, completely eliminating fraudulent certificate submissions.
            </p>
          </div>
        </div>
      </div>

      {/* Pricing & Incubation Engagement Structures */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 06 — TALENT ONBOARDING &amp; SOURCING MODELS</div>
        <h2 className="section-title mb-2">Zero Commission Fee Structure</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We reject the traditional recruitment agency percentage fee model. Our talent network is accessible through transparent venture engagement paths.
        </p>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Incubated Venture</span>
              <div className="text-2xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹0 <span className="text-xs text-muted font-normal">commission fee</span></div>
              <p className="text-xs text-muted mt-2">Full unrestricted access to our pre-vetted AI developer talent directory for active DBERT incubated startups.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>0% agency placement or finder commissions</li>
                <li>Free 15-day technical alignment sprint cycles</li>
                <li>Full cryptographic background achievement audit</li>
              </ul>
            </div>
            <div className="relative mt-4">
              <Link href="/startups/register" className="btn btn-primary w-full relative z-10">Apply For Incubation &rarr;</Link>
              <div className="absolute -right-8 -top-8 z-20 pointer-events-none transform -rotate-12">
                <HandDrawnArrow color="var(--signal)" width={50} height={50} className="transform rotate-45" />
              </div>
              <HandNote className="absolute -bottom-6 right-0 whitespace-nowrap text-xs" tone="amber">
                Free for incubated!
              </HandNote>
            </div>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative flex flex-col justify-between">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Standalone Partner</div>
            <div>
              <span className="font-mono text-xs text-accent uppercase">External Tech Partner</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">₹35,000 <span className="text-xs text-muted font-normal">/ month</span></div>
              <p className="text-xs text-muted mt-2">Subscription access for external tech corporations seeking direct pipeline introductions to vetted engineering graduates.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Up to 10 verified technical introductions/mo</li>
                <li>Access to GitHub commit quality audit scorecards</li>
                <li>Standard business hour placement coordination</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Become Tech Partner &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border border-line flex flex-col justify-between">
            <div>
              <span className="font-mono text-xs text-muted uppercase">Custom Squad Build</span>
              <div className="text-2xl font-mono font-bold text-white mt-2 mb-1">Custom Scope</div>
              <p className="text-xs text-muted mt-2">Dedicated training and custom fellowship curriculum alignment designed specifically around your proprietary tech stack.</p>
              <ul className="list-disc pl-4 text-xs text-muted space-y-1 my-4">
                <li>Custom industrial training capstone track</li>
                <li>Dedicated cohort recruitment &amp; hackathons</li>
                <li>Direct campus &amp; bootcamp pipeline integration</li>
              </ul>
            </div>
            <Link href="/about/contact" className="btn btn-outline w-full mt-4">Discuss Custom Squad &rarr;</Link>
          </div>
        </div>
      </div>

      {/* Timeline Section (Secondary BG) */}
      <div className="band-top border-t border-line">
        <div className="container-sm">
          <div className="doclabel mb-2">§ 07 — TEAM INTEGRATION PIPELINE</div>
          <h2 className="subsection-title mb-4">
            Our Team Integration Pipeline
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Frequently Asked Questions Section */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 08 — TALENT KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Related Solutions Mesh */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 09 — RELATED INCUBATION SERVICES &amp; PRODUCTS</div>
        <h2 className="section-title mb-4">Explore Complementary Venture Services</h2>
        <div className="grid gap-4 md:grid-cols-3">
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Hiring Automation Suite</h4>
            <p className="text-xs text-muted mb-3">License our autonomous Git code auditing and resume scoring pipeline to evaluate external developer applicants.</p>
            <Link href="/ai-solutions/products/hiring-automation-suite" className="accent-link text-xs">View Hiring Suite &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Intern Management System</h4>
            <p className="text-xs text-muted mb-3">Manage hired developer fellows, monitor daily sprint commits, and streamline PR code reviews with our dedicated portal.</p>
            <Link href="/ai-solutions/products/intern-management-system" className="accent-link text-xs">View Intern Portal &rarr;</Link>
          </div>
          <div className="card p-4 bg-card border border-line">
            <h4 className="font-mono text-sm font-bold text-white mb-1">Technical Architecture Build</h4>
            <p className="text-xs text-muted mb-3">Pair hired developer fellows directly with senior DBERT venture engineering squads to launch your production AI MVP.</p>
            <Link href="/startups/services/technical" className="accent-link text-xs">View Technical Service &rarr;</Link>
          </div>
        </div>
      </div>

      {/* CTA Block (Primary BG) */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 10 — INITIATE TEAM INTEGRATION</div>
        <div className="bento-card callout">
          <h2 className="card-title">Stop Searching. Start Shipping.</h2>
          <p className="page-lede">
            Ready to access our pre-vetted AI developer directory, run zero-risk 15-day technical alignment sprints, and integrate qualified engineers without commission fees? Apply for DBERT Incubation today.
          </p>
          <Link href="/startups/register" className="btn btn-primary btn-lg mt-4">Register Your Startup &rarr;</Link>
        </div>
      </div>
    </div>
  );
}

