import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import RegionalOpportunityBento from '@/components/ui/RegionalOpportunityBento';
import s from '../../learners.module.css';
import { Layers, Award, Sparkles } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/digital-marketing');

export default function DigitalMarketingCoursePage() {
  const faqs = [
    {
        "question": "How does DBERT's marketing track differ from traditional social media courses?",
        "answer": "We focus on technical, measurable growth engineering: GA4 event schemas, Google Tag Manager server tagging, search intent keyword modeling, and conversion rate optimization (CRO)."
    },
    {
        "question": "Will I manage real advertising campaigns and analytics budgets?",
        "answer": "Yes. You design live campaign structures, optimize cost-per-click (CPC) bidding strategies, conduct A/B ad creative split tests, and interpret real-time GA4 conversion funnels."
    },
    {
        "question": "Is technical coding required for digital marketing?",
        "answer": "No deep software coding is required. We teach practical technical skills including HTML meta tag structuring, schema JSON-LD generation, UTM parameters, and regex filtering."
    },
    {
        "question": "Can prospective employers authenticate my digital marketing credentials?",
        "answer": "Yes. Every credential is permanently inscribed with a unique ID into our institutional database at dbert.in/verify for instant employer verification."
    },
    {
        "question": "What starting salaries do digital marketing specialists command in India?",
        "answer": "Graduates step into roles including SEO Specialist, Performance Marketing Associate, Digital Growth Analyst, and Social Media Automation Lead, earning \u20b93.5\u2013\u20b97.5 LPA."
    }
];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Become a Digital Marketing & Growth Specialist',
        description: 'Master data-driven digital growth: technical on-page and off-page SEO, Google Ads PPC search campaigns, Meta Ads performance acquisition, and Google Analytics 4 (GA4) funnel tracking.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.in'
        },
        courseCode: 'DBERT-ENG-MKTG-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified Digital Marketing & Growth Systems Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '28000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.in/learners/courses/digital-marketing'
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

  const tools = ["Google Analytics 4 (GA4)", "Google Search Console", "Google Ads", "Meta Ads Manager", "Technical SEO", "Ahrefs/Semrush", "Content Strategy", "Email Automation", "Conversion Optimization (CRO)", "Copywriting", "Tag Manager", "Zapier"];

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
          Become a Digital Marketing & Growth Specialist
        </h1>
        <p className={s.courseTagline}>
          ₹3,50,000 – ₹7,50,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master data-driven digital growth: technical on-page and off-page SEO, Google Ads PPC search campaigns, Meta Ads performance acquisition, and Google Analytics 4 (GA4) funnel tracking.
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
            <h3 className="text-xl font-bold mb-3 text-white">Comprehensive Technical SEO & Content Optimization Audit</h3>
            <p className="text-sm text-muted leading-relaxed">
              Perform an end-to-end technical audit on a multi-page web platform, resolving Core Web Vitals issues, broken redirects, schema markup errors, and mapping high-intent keyword silos.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h3 className="text-xl font-bold mb-3 text-white">High-ROAS Google & Meta Performance Acquisition Funnel</h3>
            <p className="text-sm text-muted leading-relaxed">
              Architect a multi-stage advertising funnel across Google Search and Meta Ads, configuring custom GA4 event tracking, audience retargeting pixels, and high-converting landing pages.
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
            <Link href="/learners/launchpad?domain=digital-marketing" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
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
        title="Digital Marketing & Growth Internships"
        description="Connect directly to live digital acquisition campaigns, technical SEO audits, and content automation sprints across Delhi NCR, Mumbai, Bangalore, and Remote."
        domainName="Become a Digital Marketing & Growth Specialist"
        hubHref="https://lms.dbert.in/internships/digital-marketing"
        jobsHref="https://lms.dbert.in/jobs/digital-marketing"
        opportunities={[
          {
            title: 'Become a Digital Marketing & Growth Specialist Intern',
            roleDescription: 'Master data-driven digital growth: technical on-page and off-page SEO, Google Ads PPC search campaigns, Meta Ads performance acquisition, and Google Analytics 4 (GA4) funnel tracking.',
            cityTag: 'Remote',
            location: 'India · Remote / Hybrid',
            stipend: '₹5,000 – ₹18,000 / mo',
            tags: ['Remote', 'Verified', 'Active Sprint'],
            href: 'https://lms.dbert.in/internships/digital-marketing',
          }
        ]}
      />
    </div>
  );
}
