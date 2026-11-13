import React from 'react';
import Link from 'next/link';
import FAQAccordion from '@/components/ui/FAQAccordion';
import { pageMetadata } from '@/lib/seo';
import RegionalOpportunityBento from '@/components/ui/RegionalOpportunityBento';
import s from '../../learners.module.css';
import { Layers, Award, Sparkles } from 'lucide-react';

export const metadata = pageMetadata('/learners/courses/devops-cloud');

export default function DevopsCloudCoursePage() {
  const faqs = [
    {
        "question": "Is Linux terminal experience required before beginning this track?",
        "answer": "Foundational comfort with computer networks is helpful, but our curriculum teaches Linux shell navigation, permissions, process management, and SSH from the ground up."
    },
    {
        "question": "Will I work on live cloud infrastructure during the course?",
        "answer": "Yes. You deploy containerized services to live Linux virtual machines, configure Nginx reverse proxies with SSL, and automate GitHub Actions workflows deploying to AWS EC2."
    },
    {
        "question": "How does this course address container orchestration?",
        "answer": "You build multi-container applications with Docker Compose, progress to writing Kubernetes manifests (Deployments, Services, ConfigMaps, Ingress), and monitor clusters with Prometheus."
    },
    {
        "question": "Can employers independently verify my DevOps credentials?",
        "answer": "Yes. Every certificate is cryptographically recorded in our registry at dbert.in/verify, allowing HR and DevOps managers to authenticate candidate capabilities instantly."
    },
    {
        "question": "What career paths are available for DevOps engineers in India?",
        "answer": "Graduates step into roles including DevOps Engineer, Cloud Support Associate, Site Reliability Engineering (SRE) Intern, and Platform Engineer, earning \u20b94.5\u2013\u20b911.0 LPA."
    }
];

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Course',
        name: 'Become a DevOps & Cloud Infrastructure Engineer',
        description: 'Master Docker containerization, Kubernetes orchestration, CI/CD automated deployment pipelines, Linux server administration, and AWS cloud infrastructure through live terminal labs.',
        provider: {
          '@type': 'Organization',
          name: 'DBERT Labs Industrial Training & Venture Studio',
          url: 'https://dbert.in'
        },
        courseCode: 'DBERT-ENG-DEVOPS-2026',
        courseMode: 'Blended (Synchronous Cohort & Remote Production Lab Sprints)',
        educationalCredentialAwarded: 'Verified DevOps & Cloud Infrastructure Systems Diploma',
        offers: {
          '@type': 'Offer',
          category: 'Tuition Fee',
          price: '28000',
          priceCurrency: 'INR',
          availability: 'https://schema.org/InStock',
          validFrom: '2026-01-01',
          url: 'https://dbert.in/learners/courses/devops-cloud'
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

  const tools = ["Docker", "Kubernetes", "AWS", "GitHub Actions", "Terraform", "Linux / Bash", "Nginx", "Prometheus", "Grafana", "CI/CD", "Helm", "GitOps"];

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
          Become a DevOps & Cloud Infrastructure Engineer
        </h1>
        <p className={s.courseTagline}>
          ₹4,50,000 – ₹11,00,000 LPA Verified Average Starting Remuneration
        </p>
        <p className={s.courseLede}>
          Master Docker containerization, Kubernetes orchestration, CI/CD automated deployment pipelines, Linux server administration, and AWS cloud infrastructure through live terminal labs.
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
            <h3 className="text-xl font-bold mb-3 text-white">Multi-Tier Container Deployment with Kubernetes & Helm</h3>
            <p className="text-sm text-muted leading-relaxed">
              Containerize a microservice application with Docker, package it with Helm charts, and configure self-healing rolling deployments across a Kubernetes cluster.
            </p>
          </div>
          <div className="card p-6 bg-card border border-line">
            <h3 className="text-xl font-bold mb-3 text-white">Automated Zero-Downtime CI/CD Pipeline on AWS</h3>
            <p className="text-sm text-muted leading-relaxed">
              Construct an end-to-end GitHub Actions pipeline with automated linting, test suites, Docker image registry pushes, and zero-downtime blue/green deployment to AWS EC2.
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
            <Link href="/learners/launchpad?domain=devops-cloud" className="btn btn-primary w-full">Explore Launchpad Track &rarr;</Link>
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
        title="DevOps & Cloud Internships across Tech Corridors"
        description="Connect directly to real-world cloud migrations, Kubernetes cluster maintenance, and automated deployment pipelines across Bangalore, Hyderabad, Pune, and Remote."
        domainName="Become a DevOps & Cloud Infrastructure Engineer"
        hubHref="https://lms.dbert.in/internships/devops-cloud"
        jobsHref="https://lms.dbert.in/jobs/devops-cloud"
        opportunities={[
          {
            title: 'Become a DevOps & Cloud Infrastructure Engineer Intern',
            roleDescription: 'Master Docker containerization, Kubernetes orchestration, CI/CD automated deployment pipelines, Linux server administration, and AWS cloud infrastructure through live terminal labs.',
            cityTag: 'Remote',
            location: 'India · Remote / Hybrid',
            stipend: '₹5,000 – ₹18,000 / mo',
            tags: ['Remote', 'Verified', 'Active Sprint'],
            href: 'https://lms.dbert.in/internships/devops-cloud',
          }
        ]}
      />
    </div>
  );
}
