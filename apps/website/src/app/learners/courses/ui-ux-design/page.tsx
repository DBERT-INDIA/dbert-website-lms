import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import RegionalOpportunityBento from '@/components/ui/RegionalOpportunityBento';
import s from '../../learners.module.css';
import { Layers, Award, Sparkles } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/ui-ux-design');

export default function UiUxDesignCoursePage() {
  const faqs = [
    {
        "question": "Do I need graphic design or drawing skills to succeed in UI/UX design?",
        "answer": "No. Modern UI/UX design is rooted in information architecture, cognitive psychology, user problem solving, and systematic design tokens rather than freehand sketching."
    },
    {
        "question": "Which design tools are taught during the program?",
        "answer": "You achieve advanced mastery in Figma, covering Auto-Layout 5.0, component variants, interactive prototyping, variable design tokens, and developer handoff workflows."
    },
    {
        "question": "How are portfolio projects evaluated for industry recruiters?",
        "answer": "You craft end-to-end UX case studies detailing user personas, empathy maps, wireframes, iteration logs, and responsive Figma prototypes published to Behance and personal web portfolios."
    },
    {
        "question": "Can employers authenticate my DBERT UI/UX credentials?",
        "answer": "Yes. Upon completing design reviews and project approvals, your certificate is inscribed with a unique ID into our public verification portal at dbert.in/verify."
    },
    {
        "question": "What roles do graduates of this track pursue in India?",
        "answer": "Graduates secure roles as Junior UI/UX Designer, Product Design Intern, Interaction Designer, and Design Systems Specialist with starting packages of \u20b93.5\u2013\u20b97.5 LPA."
    }
];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Become a UI/UX & Product Design Specialist',
        description: 'Master Figma auto-layout, interactive design systems, qualitative user research, wireframing, and usability heuristics. Build production product prototypes ready for design review.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.in'
        },
        courseCode: 'DBERT-ENG-UIUX-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified Professional UI/UX & Product Design Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '28000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.in/learners/courses/ui-ux-design'
        }
      },
      {
        '@type': 'FAQPage',
        mainEntity: faqs.map((f: { question: string; answer: string }) => ({
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

  const tools = ["Figma", "Auto-Layout", "Design Systems", "FigJam", "Miro", "Wireframing", "Usability Testing", "Design Tokens", "Prototyping", "WCAG Accessibility", "Gutenberg Hierarchy", "User Flows"];

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
          Become a UI/UX & Product Design Specialist
        </h1>
        <p className={s.courseTagline}>
          ₹3,50,000 – ₹7,50,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master Figma auto-layout, interactive design systems, qualitative user research, wireframing, and usability heuristics. Build production product prototypes ready for design review.
        </p>
      </div>

      {/* Key Metrics Grid */}
      <div className="section-band">
        <div className="container">
          <h2 className="sr-only">Key Course Highlights</h2>
          <div className="bento-grid-3">
            <div className="bento-card center">
              <div className="bento-icon"><Layers className="w-5 h-5 text-accent" /></div>
              <h3 className="bento-title">Practical Project Sprints</h3>
              <p className="bento-text">
                8 intensive weekly sprints shipping real deliverables under senior engineering and design review.
              </p>
            </div>
            <div className="bento-card center">
              <div className="bento-icon"><Award className="w-5 h-5 text-accent" /></div>
              <h3 className="bento-title">Verifiable Credentials</h3>
              <p className="bento-text">
                Every completed certification is cryptographically registered and verifiable at dbert.in/verify.
              </p>
            </div>
            <div className="bento-card center">
              <div className="bento-icon"><Sparkles className="w-5 h-5 text-accent" /></div>
              <h3 className="bento-title">Direct Portal Referrals</h3>
              <p className="bento-text">
                Direct referral consideration to active corporate internships and startup venture pipelines.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Capstone Projects Section */}
      <div className="container pad-block">
        <div className="doclabel mb-2">§ 02 — PRODUCTION CAPSTONES</div>
        <h2 className="section-title mb-6">Real Systems Built and Shipped</h2>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="card p-6 bg-card border border-line">
            <h3 className="text-xl font-bold mb-3 text-white">Enterprise Design System & Token Architecture</h3>
            <p className="text-sm text-muted leading-relaxed">
              Architect a modular design system in Figma with 50+ auto-layout components, dark/light themes, typography scales, and accessible color tokens.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h3 className="text-xl font-bold mb-3 text-white">Fintech Mobile App UX & Usability Testing</h3>
            <p className="text-sm text-muted leading-relaxed">
              Conduct qualitative user interviews, design wireframes and high-fidelity interactive mobile flows for a personal budgeting application, validated through 5 moderated user tests.
            </p>
          </div>
        </div>
      </div>

      {/* Transparent Tuition & Zero-Cost EMI Table */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 03 — TUITION INVESTMENT &amp; EMI SCHEDULES</div>
        <h2 className="section-title mb-2">Transparent Indian Tuition &amp; Zero-Cost Financing</h2>
        <p className="prose-sm text-muted mb-6 max-w-2xl">
          We practice absolute financial transparency. Enroll directly with our straightforward upfront tuition or utilize flexible Zero-Cost EMI schedules through verified Indian educational lending partners.
        </p>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <div className="card p-6 bg-card border border-line">
            <span className="font-mono text-xs text-muted uppercase tracking-wider">One-Time Upfront Tuition</span>
            <div className="text-3xl font-mono font-bold text-white mt-2 mb-1">₹28,000 <span className="text-sm text-muted font-normal">INR (All Inclusive)</span></div>
            <p className="text-xs text-muted mb-4">Covers synchronous practical instruction, cloud lab access, comprehensive code and design reviews, and global certification database entry.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Permanent access to recorded architecture and design sessions</li>
              <li>Weekly 1-on-1 mentor optimization reviews</li>
              <li>Direct hiring referral recommendations for audited graduates</li>
            </ul>
            <Link href="/learners/launchpad?domain=ui-ux-design" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
          </div>

          <div className="card p-6 bg-card border-2 border-accent relative">
            <div className="absolute -top-3 right-4 bg-accent text-zinc-950 font-mono text-[10px] uppercase font-bold px-2 py-0.5 rounded">Zero-Cost EMI</div>
            <span className="font-mono text-xs text-accent uppercase tracking-wider">9-Month Installment Schedule</span>
            <div className="text-3xl font-mono font-bold text-emerald-400 mt-2 mb-1">₹3,111 <span className="text-sm text-muted font-normal">/ month (₹0 Interest)</span></div>
            <p className="text-xs text-muted mb-4">Available via authorized banking partnerships with zero processing surcharges or security deposit requirements for qualified candidates.</p>
            <ul className="list-disc pl-4 text-xs text-muted space-y-2 mb-6">
              <li>Expedited digital financial verification protocol</li>
              <li>Immediate course and lab access upon installment authorization</li>
              <li>Complete structural parity with lump-sum fee applicants</li>
            </ul>
            <Link href="/about/contact" className="btn btn-outline w-full">Inquire About EMI Financing</Link>
          </div>
        </div>
      </div>

      {/* Production Technologies Mastered */}
      <div className={`container ${s.techBlock} border-t border-line`}>
        <div className="doclabel mb-2">§ 04 — CORE TOOLING</div>
        <h2 className={s.techHeading}>Production Technologies Mastered</h2>
        <div className={s.techRow}>
          {tools.map((tool: string, idx: number) => (
            <span key={idx} className={s.techChip}>
              {tool}
            </span>
          ))}
        </div>
      </div>

      {/* Frequently Asked Questions */}
      <div className="container pad-block border-t border-line">
        <div className="doclabel mb-2">§ 05 — KNOWLEDGE BASE</div>
        <h2 className="section-title mb-4">Frequently Asked Questions</h2>
        <div className="measure">
          <FAQAccordion items={faqs} />
        </div>
      </div>

      {/* Live Regional Opportunities */}
      <RegionalOpportunityBento
        sectionNumber="§ 06"
        title="UI/UX Design Internships & Remote Roles"
        description="Connect directly to live product design sprints, mobile wireframing briefs, and enterprise design system projects across Bangalore, Pune, Delhi NCR, and Remote."
        domainName="Become a UI/UX & Product Design Specialist"
        hubHref="https://lms.dbert.in/internships/ui-ux-design"
        jobsHref="https://lms.dbert.in/jobs/ui-ux-design"
        opportunities={[
          {
            title: 'Become a UI/UX & Product Design Specialist Intern',
            roleDescription: 'Master Figma auto-layout, interactive design systems, qualitative user research, wireframing, and usability heuristics. Build production product prototypes ready for design review.',
            cityTag: 'Remote',
            location: 'India · Remote / Hybrid',
            stipend: '₹5,000 – ₹18,000 / mo',
            tags: ['Remote', 'Verified', 'Active Sprint'],
            href: 'https://lms.dbert.in/internships/ui-ux-design',
          }
        ]}
      />
    </div>
  );
}
