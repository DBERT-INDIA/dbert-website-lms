import React from 'react';
import Link from 'next/link';
import StepTimeline from '@/components/ui/StepTimeline';
import Faq from '@/components/seo/Faq';
import { pageMetadata } from '@/lib/seo';
import { seoConfig } from '@/data/seo.config';
import s from '../learners.module.css';
import { Banknote, Laptop, Scroll } from 'lucide-react';


export const metadata = pageMetadata('/learners/fellowship');

const steps = [
  {
    number: '01',
    title: 'Technical onboarding and squad assignment',
    description:
      'You are assigned to a development squad under an engineering mentor, given repository access, and set up locally against the real database schema. Week one is environment, codebase tour, and your first reviewed pull request.',
  },
  {
    number: '02',
    title: 'Active contribution sprints',
    description:
      'You design interfaces, configure vector indexes, build API routes, and take part in code review — on the client repository, not a fork. Every pull request is reviewed and graded by a senior engineer before it merges.',
  },
  {
    number: '03',
    title: 'Evaluation and career handoff',
    description:
      'Final module hardening, then the paperwork that makes the work legible to a recruiter: an experience letter tied to a verifiable certificate ID, your performance-based stipend, and introductions where a partner startup is hiring.',
  },
];

const faqs = [
  {
    question: 'Is the DBERT fellowship really a paid AI internship?',
    answer:
      'Yes, with a specific structure worth understanding before you apply. The stipend is performance-based and ranges from ₹5,000 to ₹18,000, paid against delivery milestones and code quality rather than hours logged. It is not a salary and it is not guaranteed at the top of the band — a fellow who ships reviewed, merged work across the full programme earns more than one who does not.',
  },
  {
    question: 'Do I have to complete DBERT Accelerate first?',
    answer:
      'No. There are two routes in. The first is completing DBERT Accelerate, which is how most fellows arrive. The second is passing our external code screening challenge, which is open to anyone regardless of where they learned to code. The screening exists precisely so that self-taught engineers and graduates of other programmes are not locked out.',
  },
  {
    question: 'Do you guarantee placement at the end?',
    answer:
      'No, and you should be sceptical of any programme in India that does. What we actually provide is a verifiable record: an experience letter signed by the engineers who reviewed your code, a certificate ID anyone can check at dbert.online/verify, and commits on a real client repository. Partner startups review fellow performance logs when they hire, so the pipeline is real, but a referral is not an offer and we will not describe it as one.',
  },
  {
    question: 'What kind of work do fellows actually do?',
    answer:
      'Production work on systems that have users. That has meant REST and streaming API routes, database and vector-index configuration, retrieval pipelines, front-end interfaces, and deployment plumbing for incubated startups and enterprise clients. It does not mean tutorial rebuilds, sandbox exercises, or a capstone that nobody runs after you leave.',
  },
  {
    question: 'How long is the fellowship and how much does it cost?',
    answer:
      'The programme runs three months and the fee is ₹1,599. The fee covers mentorship, code review, and the certification and letter issuance at the end; the stipend is separate and flows to you. Fees are reviewed each cohort, so treat the figure on this page as current rather than permanent.',
  },
  {
    question: 'Is this remote, and does it work alongside a degree or a job?',
    answer:
      'It is remote and squad-based. Sprints are structured around delivery milestones rather than fixed office hours, which is what makes it workable alongside a final-year course load. It is still real client work with real deadlines, so it is not a zero-effort add-on — fellows who treat it as one tend to finish at the bottom of the stipend band.',
  },
  {
    question: 'How is the experience letter different from a normal internship certificate?',
    answer:
      'Two ways. It names the engineer who reviewed your work and the system you contributed to, rather than certifying attendance; and it carries a certificate ID that a recruiter can verify independently at dbert.online/verify without contacting us. A letter nobody can check is worth roughly what it costs to print.',
  },
  {
    question: 'Where do I apply?',
    answer:
      'Applications run through the DBERT internship platform at internship.dbert.online. The application asks for your code — a repository, a deployed project, or your screening submission — rather than a CV of coursework, because that is what the selection is actually based on.',
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
        url: 'https://dbert.online',
      },
      url: 'https://dbert.online/learners/fellowship',
      hasCourseInstance: {
        '@type': 'CourseInstance',
        courseMode: 'online',
        courseWorkload: 'P3M',
      },
      offers: {
        '@type': 'Offer',
        category: 'Paid',
        price: '1599',
        priceCurrency: 'INR',
        availability: 'https://schema.org/InStock',
        url: 'https://internship.dbert.online/',
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
        <h1 className="page-title">
          A paid AI internship where the code ships
        </h1>
        <p className="lede-wide">
          The DBERT Fellowship places you on a real client codebase under senior review — production
          systems for incubated startups, not practice projects. You leave with merged commits, a
          performance stipend, and an experience letter a recruiter can verify.
        </p>
        <div className="flex justify-center gap-3 flex-wrap mt-4">
          <Link href="/verify" className="proof-mark">
            <span>✓ Verifiable Credential UUID</span>
          </Link>
          <span className="proof-mark proof-mark-signal">
            <span>₹5,000–₹18,000 Monthly Performance Stipend</span>
          </span>
          <Link href="/about" className="proof-mark">
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
            The fellowship is a three-month, selection-based programme that places you inside a
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

          <h3>The work itself</h3>
          <p>
            Squads are assigned to a system rather than a curriculum, so the exact stack depends on
            the client. Across recent squads that has meant:
          </p>
          <ul>
            <li>REST and token-streaming API routes, including auth and rate limiting</li>
            <li>Postgres schema design and migrations, plus vector-index configuration for retrieval</li>
            <li>Retrieval-augmented generation pipelines — chunking, embedding, evaluation of answer quality</li>
            <li>Front-end interfaces against those APIs, built to the client&apos;s design</li>
            <li>Deployment, environment configuration, and the observability needed to debug it later</li>
          </ul>
          <p>
            You will not touch all of it. Squads specialise, and a fellow who spends three months
            getting a retrieval pipeline genuinely good has a better story than one who touched
            everything shallowly. Explore how these production vector components come together in our technical workshop on <Link href="/blog/rag-pipeline-tutorial-from-scratch">Production RAG Architecture from Scratch</Link>.
          </p>

          <h3>Selection: two ways in</h3>
          <p>
            The first route is completing{' '}
            <Link href="/learners/accelerate">DBERT Accelerate</Link>, which is how most fellows
            arrive — by then we have seen months of their code and know what they can be trusted with.
            The second is the external code screening challenge, open to anyone regardless of where
            they learned. The screening exists so that self-taught engineers and graduates of other
            programmes are not locked out of the pipeline by not having bought our course first.
          </p>
          <p>
            Either way, the application asks for code — a repository, a deployed project, a screening
            submission — rather than a list of coursework. That is what the decision is made on.
          </p>

          <h3>The stipend, stated plainly</h3>
          <p>
            The stipend ranges from <strong>₹5,000 to ₹18,000</strong> and is performance-based: it is
            paid against delivery milestones and code quality, not hours logged. Nobody starts at the
            top of the band. A fellow who ships reviewed, merged work across the full three months
            earns materially more than one who does not, and we would rather say that here than have
            you discover it in month two. To see how intermediate and advanced performance directly scales into full-time compensation across Indian technology hubs, inspect our analysis of <Link href="/blog/ai-agent-developer-salary-2026">2026 AI Developer Salaries in India</Link>.
          </p>
          <p>
            The programme fee is <strong>₹1,599</strong> for the three months, covering mentorship,
            code review, and certificate and letter issuance. Fees are reviewed each cohort, so treat
            that as the current figure rather than a permanent one.
          </p>

          <h2>What you leave with</h2>
          <p>
            Three things, in descending order of how much they matter in an interview:
          </p>
          <ol>
            <li>
              <strong>Merged commits on a system with users.</strong> Public where the client permits
              it, describable in detail where they do not. This is the part that changes how the
              interview goes.
            </li>
            <li>
              <strong>An experience letter naming the engineer who reviewed your work</strong> and the
              system you contributed to — not a certificate of attendance. It carries a certificate ID
              a recruiter can check independently at{' '}
              <Link href="/verify">the DBERT certificate verification page</Link> without contacting
              us. A letter nobody can verify is worth what it costs to print.
            </li>
            <li>
              <strong>Visibility to partner startups.</strong> They review fellow performance logs
              when hiring, and{' '}
              <Link href="/learners/jobs">the AI jobs board for verified builders</Link> is restricted
              to people with that record.
            </li>
          </ol>

          <h2>What we do not claim</h2>
          <div className="disclosure">
            <p>
              <strong>We do not guarantee placement.</strong> Any programme in India promising a job
              at the end is either selecting so hard that the guarantee is meaningless or is going to
              disappoint someone. A referral is not an offer, and we will not describe it as one.
            </p>
            <p>
              <strong>We do not publish a placement percentage or an acceptance rate.</strong> We
              would rather publish nothing than publish a number we cannot substantiate to a
              prospective fellow who asks how it was calculated. When the cohort history is long
              enough to state honestly, it will appear on{' '}
              <Link href="/learners/jobs">the jobs page</Link> with its method attached.
            </p>
            <p>
              <strong>We do not promise the top of the stipend band.</strong> It is performance-based
              and most fellows land in the middle of it.
            </p>
          </div>
        </div>
      </div>

      {/* Timeline */}
      <div className="band-top">
        <div className="container-sm">
          <h2 className="subsection-title">
            How three months are structured
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
            href="https://internship.dbert.online/"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary btn-lg"
          >
            Apply for the paid AI fellowship
          </a>
        </div>
      </div>
    </div>
  );
}
