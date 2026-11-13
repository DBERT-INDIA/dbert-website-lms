import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import Faq from '@/components/seo/Faq';
import HandNote from '@/components/ui/HandNote';
import { pageMetadata } from '@/lib/seo';
import { seoConfig } from '@/data/seo.config';
import s from '../learners.module.css';
import { Banknote, Laptop, Scroll } from 'lucide-react';


export const metadata = pageMetadata('/learners/fellowship');

const steps = [
  {
    number: '01',
    title: 'Technical Onboarding & Architecture Setup (Weeks 1–2)',
    description:
      'You are assigned to an active venture squad under a senior engineer, granted direct repository access, and set up locally against production database schemas. Weeks 1–2 focus on architecture orientation, CI/CD pipelines, and your first reviewed pull request.',
  },
  {
    number: '02',
    title: 'Active Contribution Sprints & Senior Code Reviews (Weeks 3–6)',
    description:
      'You build REST and streaming API routes, configure vector indexes, write migrations, and submit pull requests directly to live venture repositories. Every PR is rigorously reviewed, commented, and graded by senior engineering staff before merging.',
  },
  {
    number: '03',
    title: 'System Hardening, Verifiable Credentials & Stipend Handoff (Weeks 7–8)',
    description:
      'Final system hardening, integration tests, and documentation. You receive your official 3-document credential packet (verifiable on /verify and directory), audited performance stipend disbursement, and referrals to hiring partner startups.',
  },
];

const faqs = [
  {
    question: 'Is the DBERT fellowship really a paid AI internship?',
    answer:
      'Yes, with an audited performance structure. The stipend ranges from ₹5,000 to ₹18,000 across milestone deliverables, evaluated against 4 objective engineering criteria: code quality, architecture & security, test coverage, and documentation. Approved stipends are credited atomically and disbursed directly to the fellow\'s verified UPI ID via the LMS portal.',
  },
  {
    question: 'Do I have to complete DBERT Accelerate first?',
    answer:
      'No. There are two entry routes. The first is completing DBERT Accelerate, where mentors have evaluated your foundational code. The second is passing our external code screening challenge, open to any engineer regardless of academic background. Technical screening is 100% free with zero application fees.',
  },
  {
    question: 'Do you guarantee permanent corporate employment or jobs at the end?',
    answer:
      'No, and you should be sceptical of any programme in India that claims a 100% unconditional job guarantee. What we guarantee is real: guaranteed assignment to an active client repository, senior engineering code review on every PR, an independently verifiable Certificate UUID at dbert.in/verify, and an official experience letter. Partner startups review fellow performance logs when hiring, but a referral is an earned introduction, not an unconditional offer.',
  },
  {
    question: 'What kind of work do fellows actually do?',
    answer:
      'Production engineering on live venture codebases with active users. Recent fellows have built REST and token-streaming APIs, Postgres schema migrations, vector RAG retrieval pipelines, and responsive React interfaces across venture projects such as Alkame, Gayatri AI, Aivara Insight Lite, and DBERT Systems.',
  },
  {
    question: 'How long is the fellowship and what does the ₹1,999 fee cover?',
    answer:
      'The programme runs 2 months (8 weeks). The one-time fee of ₹1,999 covers 1-on-1 mentorship, senior code reviews, guaranteed assignment to an active production repository, and issuance of the 3-document verifiable credential packet. Performance stipends (₹5,000–₹18,000) are earned separately based on milestone deliverables.',
  },
  {
    question: 'Is this remote, and does it work alongside a degree or a job?',
    answer:
      'It is fully remote and squad-based. Sprints are structured around delivery milestones rather than fixed office hours, making it workable alongside final-year college coursework. It involves real production deadlines, requiring approximately 12–15 focused hours per week.',
  },
  {
    question: 'How is the credential verified by recruiters and employers?',
    answer:
      'Every graduate receives an official Certificate of Completion, Academic Project Evaluation, and Letter of Recommendation with a unique UUID. Recruiters can verify the credential instantly at dbert.in/verify or explore all graduates in our public Alphabetical Credential Directory at dbert.in/verify/directory.',
  },
  {
    question: 'Where do I apply, and are there any application fees?',
    answer:
      'Applications run through the DBERT portal at lms.dbert.in. There is strictly ZERO application fee. Selection is based purely on technical code review of your GitHub repositories or screening task submission.',
  },
];

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'Course',
      name: 'DBERT Fellowship — paid AI internship',
      description: seoConfig['/learners/fellowship'].description,
      provider: {
        '@type': 'Organization',
        name: 'Digital Blinc Education Research And Technology',
        alternateName: 'DBERT',
        url: 'https://dbert.in',
      },
      url: 'https://dbert.in/learners/fellowship',
      hasCourseInstance: {
        '@type': 'CourseInstance',
        courseMode: 'online',
        courseWorkload: 'P2M',
      },
      offers: {
        '@type': 'Offer',
        category: 'Paid',
        price: '1999',
        priceCurrency: 'INR',
        availability: 'https://schema.org/InStock',
        url: 'https://lms.dbert.in/',
      },
    },
    {
      '@type': 'FAQPage',
      mainEntity: faqs.map((f) => ({
        '@type': 'Question',
        name: f.question,
        acceptedAnswer: {
          '@type': 'Answer',
          text: f.answer,
        },
      })),
    },
  ],
};

export default function FellowshipProgramPage() {
  return (
    <div className="glow-wrapper">
      <div className="glow-spot"></div>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      {/* Hero */}
      <div className="container page-head">
        <div className="doclabel">
          § 03 — FELLOWSHIP PROGRAMME <span className="rev">cohort track</span>
        </div>
        <div className="stack-h justify-center align-baseline gap-3 flex-wrap">
          <h1 className="page-title">
            A paid AI internship where the code ships
          </h1>
          <HandNote tone="blue">
            live client repos · real stipends ✎
          </HandNote>
        </div>
        <p className="lede-wide">
          The DBERT Fellowship places you on a real client codebase under senior review — production
          systems for incubated startups, not practice projects. You leave with merged commits, a
          performance stipend, and an experience letter a recruiter can verify.
        </p>
        <div className="flex justify-center gap-3 flex-wrap mt-4">
          <Link href="/verify" className="proof-mark">
            <span>✓ Verifiable Credential UUID</span>
          </Link>
          <Link href="/verify/directory" className="proof-mark">
            <span>✓ 465+ Certified Fellows Directory</span>
          </Link>
          <span className="proof-mark proof-mark-signal">
            <span>₹5,000–₹18,000 Performance Stipend</span>
          </span>
          <Link href="/about/credentials" className="proof-mark">
            <span>✓ MSME Registered Entity</span>
          </Link>
        </div>
      </div>

      {/* Key facts */}
      <div className="section-band">
        <div className="container">
          {/* The three cards are h3s, so this h2 keeps the outline from jumping
              h1 → h3 and failing axe's heading-order check. Same pattern the
              homepage uses above the audience doors. Promoting the cards to h2
              instead would inherit the global h2 scale (up to 2.7rem) and
              dwarf the page title. */}
          <h2 className="sr-only">What the fellowship gives you</h2>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <span className="icon-chip"><Laptop aria-hidden="true" /></span>
              <h3 className="accent-note">Real client codebases</h3>
              <p className="text-sm">Write secure API routes, configure databases, and deploy model pipelines for incubated startups.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Banknote aria-hidden="true" /></span>
              <h3 className="accent-note">Performance stipends</h3>
              <p className="text-sm">₹5,000 to ₹18,000, paid against delivery milestones and code quality rather than hours logged.</p>
            </div>
            <div className="bento-card center">
              <span className="icon-chip"><Scroll aria-hidden="true" /></span>
              <h3 className="accent-note">Verifiable letters</h3>
              <p className="text-sm">Experience letters and LORs signed by the DBERT engineers who reviewed your pull requests.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Long-form body */}
      <div className="container pad-block">
        <div className="article">
          <h2>What a paid AI internship in India usually gets wrong</h2>
          <p>
            Search for a paid AI internship in India and most of what comes back is a course with an
            internship label stapled to it. The work is a sandbox: a to-do app, a chatbot against a
            public API, a notebook that runs once and is never opened again. The certificate at the end
            certifies attendance. Recruiters have learned to read straight past it, which is why so
            many candidates with three internships on a CV still cannot answer a question about
            production incidents, migrations, or code review.
          </p>

          <div className="card p-6 bg-card border border-line my-6">
            <div className="doclabel mb-2">THE HONEST COMPARISON</div>
            <div className="space-y-3 font-mono text-sm">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-line/50 pb-2">
                <span className="redline-del">Unpaid prompt engineering on toy notebooks</span>
                <span className="text-ok font-semibold">&rarr; Merged commits on live venture repos</span>
              </div>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-line/50 pb-2">
                <span className="redline-del">Certificate of online video attendance</span>
                <span className="text-ok font-semibold">&rarr; Verifiable UUID credential on /verify</span>
              </div>
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
                <span className="redline-del">Paying ₹1.5L upfront with empty job guarantees</span>
                <span className="text-ok font-semibold">&rarr; Performance stipend up to ₹18,000</span>
              </div>
            </div>
          </div>

          <p>
            The gap is not knowledge. It is evidence. An engineer who has shipped to a repository with
            users on the other end has a different set of habits — they write migrations that can be
            rolled back, they read a stack trace before they read Stack Overflow, and they can explain
            why a pull request was rejected. Those habits are visible in an interview within about ten
            minutes, and no amount of coursework simulates them. For deeper strategic guidance on separating legitimate technical engagements from marketing sandboxes, review our <Link href="/blog/paid-ai-internship-india-guide-2026">2026 Guide to Paid AI Internships in India</Link>.
          </p>

          <h2>What the DBERT Fellowship actually is</h2>
          <p>
            The fellowship is a 2-month (8-week), selection-based technical incubation programme that places you inside a
            development squad building software for DBERT&apos;s own incubated startups and enterprise
            clients. It sits at the top of the{' '}
            <Link href="/learners">AI career programs</Link> ladder, after{' '}
            <Link href="/learners/accelerate">the Accelerate engineering programme</Link>, and it is
            the rung where the work stops being ours and starts being a client&apos;s.
          </p>
          <p>
            That distinction drives everything else about the programme. Because a client is waiting
            on the output, your pull requests are reviewed by senior engineers against the same bar as
            any other contributor&apos;s, and rejected on the same grounds. Because the systems are
            live, the work is unglamorous in the specific way real work is unglamorous — schema
            changes, retrieval quality, error handling, the long tail of things that only matter when
            someone is actually using the software.
          </p>

          <h3>Live venture repositories &amp; client deployments</h3>
          <p>
            Fellows work directly on production codebases rather than sandboxes or tutorial rebuilds. Recent squads have contributed directly to:
          </p>
          <ul>
            <li><strong>Alkame:</strong> Quantitative financial market intelligence platform featuring real-time signal processing, streaming news feeds, and vector-similarity retrieval pipelines.</li>
            <li><strong>Gayatri AI:</strong> Conversational AI and agent reasoning system with localized embeddings and specialized function-calling loops.</li>
            <li><strong>Aivara Insight Lite:</strong> High-throughput document intelligence and automated pipeline extraction for enterprise records.</li>
            <li><strong>DBERT Systems:</strong> Open-weights custom LLMs (e.g. <code>ollama run DBERT/DBERT_AI</code>) and developer infrastructure for reproducible agent workflows.</li>
          </ul>

          <h3>Selection: merit-based with zero application fees</h3>
          <p>
            The first route is completing{' '}
            <Link href="/learners/accelerate">DBERT Accelerate</Link>, which is how most fellows
            arrive — by then we have evaluated weeks of their code.
            The second is the external code screening challenge, open to anyone regardless of academic background.
            There is strictly <strong>zero application fee</strong> for applying, screening, or interview evaluation.
          </p>
          <p>
            Either way, the application asks for code — a GitHub repository, a deployed application, or a screening
            submission. That is what the selection decision is made on.
          </p>

          <h3>How the performance stipend works: 4-dimension engineering rubric</h3>
          <p>
            The stipend ranges from <strong>₹5,000 to ₹18,000</strong> across delivery milestones. It is performance-based,
            not an hourly wage. Submissions are made through our LMS technical task engine and audited by senior staff against 4 objective engineering dimensions:
          </p>
          <ul>
            <li><strong>Code Quality &amp; Cleanliness:</strong> Adherence to strict linting (PEP8/ESLint), TypeScript or Python typing, modular architecture, and proper error boundaries.</li>
            <li><strong>Architecture &amp; Security:</strong> Secure parameterization, database migrations, clean API route structures, and zero hardcoded secrets.</li>
            <li><strong>Practical Feasibility &amp; Testing:</strong> Passing unit and integration tests, reproducible Docker/local setups, and live deployment verification.</li>
            <li><strong>Technical Documentation:</strong> Clear READMEs, architecture decision records, and endpoint documentation.</li>
          </ul>
          <p>
            Approved milestone stipends are released atomically and disbursed via UPI directly to the fellow&apos;s verified account.
          </p>
          <p>
            The programme fee is <strong>₹1,999</strong> for the 2 months of technical incubation, covering 1-on-1 mentorship,
            senior pull request reviews, guaranteed assignment to an active client repository, and official verifiable credential issuance.
          </p>

          <h2>What you leave with</h2>
          <p>
            Three things, in descending order of how much they matter in an interview:
          </p>
          <ol>
            <li>
              <strong>Merged commits on a system with users.</strong> Public on GitHub where the client permits
              it, describable in detail where they do not. This is the tangible evidence that transforms technical interviews.
            </li>
            <li>
              <strong>An official 3-document credential packet:</strong> Certificate of Completion, Academic Project Evaluation, and Letter of Recommendation naming the engineer who reviewed your work. Each document carries a unique UUID that anyone can verify independently at{' '}
              <Link href="/verify">dbert.in/verify</Link> or in our public{' '}
              <Link href="/verify/directory">Alphabetical Credential Directory</Link>.
            </li>
            <li>
              <strong>Visibility to partner startups.</strong> Hiring partners review fellow sprint logs
              when hiring, and{' '}
              <Link href="/learners/jobs">the AI jobs board for verified builders</Link> is reserved
              for fellows with that verified record.
            </li>
          </ol>

          <h2>What we guarantee vs what we do not claim</h2>
          <div className="disclosure">
            <p>
              <strong>✓ What we guarantee:</strong> We guarantee active technical assignment to live venture repositories under senior engineer code review, 1-on-1 technical mentorship, and an independently verifiable credential packet upon milestone completion.
            </p>
            <p>
              <strong>✗ We do not promise unconditional jobs or corporate hiring:</strong> Any programme in India claiming a 100% placement guarantee is either selecting so hard that the guarantee is meaningless or misleading applicants. A startup referral is an earned introduction, not an employment contract.
            </p>
            <p>
              <strong>✗ We do not promise the top of the stipend band:</strong> Stipends are earned against the 4-dimension engineering rubric. Fellows who consistently ship high-quality code across all milestones achieve the upper band.
            </p>
            <p>
              <strong>✓ Zero application fees:</strong> DBERT never charges application, registration, or interview screening fees.
            </p>
          </div>
        </div>
      </div>

      {/* Timeline */}
      <div className="band-top">
        <div className="container-sm">
          <h2 className="subsection-title">
            How the 2-Month Incubation is Structured
          </h2>
          <StepTimeline steps={steps} />
        </div>
      </div>

      {/* Why unique + FAQ */}
      <div className="container pad-block">
        <div className={`bento-grid-2 ${s.gridCentered}`}>
          <div className="article">
            <h2>Why this is structured as a fellowship, not a course</h2>
            <p>
              A course can be run at any scale — the marginal cost of one more student is close to
              zero. Client work cannot. Every fellow consumes senior engineering review time on a
              repository with a deadline, which is the scarcest thing DBERT has. That constraint is
              why the programme is selective, why squads are small, and why we cannot simply admit
              everyone who applies.
            </p>
            <p>
              It is also why the stipend is performance-based rather than flat. The programme only
              works if fellows ship: a squad carrying someone who does not is a squad missing a client
              deadline.
            </p>
          </div>
          <div className={`bento-card ${s.accentPanel}`}>
            <h3 className={s.accentPanelTitle}>What makes the fellowship different</h3>
            <ul className={s.accentList}>
              <li><strong>Not sandbox toys</strong> — production databases and live API pipelines, on the client repository.</li>
              <li><strong>Senior code review</strong> — every pull request reviewed and graded before it merges.</li>
              <li><strong>Independently verifiable</strong> — the letter carries an ID a recruiter can check without asking us.</li>
              <li><strong>Direct hiring visibility</strong> — partner startups read performance logs when they hire.</li>
            </ul>
          </div>
        </div>

        <div className="article">
          <Faq items={faqs} heading="Paid AI internship — common questions" />
        </div>
      </div>

      {/* CTA */}
      <div className="container pb-block">
        <div className="bento-card callout-plain">
          <h2 className="card-title">Applications open for the next cohort</h2>
          <p className="page-lede">
            Entry is by completing{' '}
            <Link href="/learners/accelerate">DBERT Accelerate</Link> or by passing the external code
            screening challenge. Bring code, not a CV.
          </p>
          <a
            href="https://lms.dbert.in"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary btn-lg"
          >
            Apply for the AI Fellowship
          </a>
        </div>
      </div>
    </div>
  );
}
