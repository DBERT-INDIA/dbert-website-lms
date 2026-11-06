import React from 'react';
import Link from 'next/link';
import HandNote from '@/components/ui/HandNote';
import { pageMetadata } from '@/lib/seo';
import { Briefcase, Sparkles, ArrowRight } from 'lucide-react';
import styles from '../about.module.css';

export const metadata = pageMetadata('/about/careers');

export default function CareersPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'JobPosting',
        title: 'AI Engineering Fellow & Technical Mentor',
        description: '<p>Join DBERT as an AI practitioner, researcher, or technical mentor. Guide incubation fellows across production LLM systems, code reviews, and applied AI ventures.</p><p><strong>Requirements:</strong> Hands-on experience with Python, PyTorch, modern LLM architectures, microservices, and student mentorship.</p>',
        datePosted: '2026-10-01T00:00:00+05:30',
        validThrough: '2027-06-30T23:59:59+05:30',
        employmentType: 'FULL_TIME',
        hiringOrganization: {
          '@type': 'Organization',
          name: 'DBERT (Applied AI Incubation & Research)',
          sameAs: 'https://dbert.in',
          logo: 'https://dbert.in/images/dbert_seal.png',
        },
        jobLocationType: 'TELECOMMUTE',
        applicantLocationRequirements: {
          '@type': 'Country',
          name: 'IN',
        },
        directApply: true,
      },
      {
        '@type': 'JobPosting',
        title: 'Aivara Technologies Hiring Cohort Fellow',
        description: '<p>Join our 3-month engineering sprint across 5 specialized domains: AI Agent Development, Full Stack, Python Automation, Data Analytics, and Data Engineering/ML.</p><p><strong>Requirements:</strong> Laptop with internet, 10 hours per week commitment, Python/JavaScript fundamentals.</p>',
        datePosted: '2026-10-01T00:00:00+05:30',
        validThrough: '2027-06-30T23:59:59+05:30',
        employmentType: 'INTERN',
        hiringOrganization: {
          '@type': 'Organization',
          name: 'Aivara Technologies & DBERT Labs',
          sameAs: 'https://dbert.in',
          logo: 'https://dbert.in/images/dbert_seal.png',
        },
        jobLocationType: 'TELECOMMUTE',
        applicantLocationRequirements: {
          '@type': 'Country',
          name: 'IN',
        },
        baseSalary: {
          '@type': 'MonetaryAmount',
          currency: 'INR',
          value: {
            '@type': 'QuantitativeValue',
            minValue: 10000,
            maxValue: 22000,
            unitText: 'MONTH',
          },
        },
        directApply: true,
      },
    ],
  };

  return (
    <div className="container pad-block">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="mb-lg">
        <div className="doclabel">
          § 01 — CAREERS &amp; RECRUITMENT <span className="rev">rev: 2026.2</span>
        </div>
        <div className="stack-h justify-start align-baseline gap-3 flex-wrap mb-2">
          <h1>Careers &amp; Hiring Cohorts</h1>
          <HandNote tone="blue">
            sprints · mentorship · placements ✍
          </HandNote>
        </div>
        <p>Build the future of AI education, research, and technical incubation.</p>
      </div>

      <div className={styles.centeredNarrow}>
        {/* Active Aivara Technologies Hiring Cohort Card */}
        <div className={`card card-lift ${styles.pad6} mb-6 border-accent`}>
          <div className="stack-h align-center gap-2 mb-2">
            <span className="icon-chip"><Sparkles size={18} aria-hidden="true" /></span>
            <span className="doclabel text-accent border-accent">
              NOW RECRUITING • APPLICATIONS OPEN
            </span>
          </div>
          <h2 className="card-title">Aivara Technologies Hiring Cohort (2026)</h2>
          <p className={styles.bodyMuted}>
            Join our 3-month engineering sprint across 5 specialized domains: AI Agent Development, Full Stack, Python Automation, Data Analytics, and Data Engineering/ML. Direct production repos, senior review rubrics, and placement tracks.
          </p>
          <div className="mt-4">
            <Link href="/cohorts/aivara" className="btn btn-primary inline-flex align-center gap-2">
              Apply for Cohort <ArrowRight size={16} />
            </Link>
          </div>
        </div>

        <div className={`card card-lift ${styles.pad6}`}>
          <span className="icon-chip"><Briefcase aria-hidden="true" /></span>
          <h2 className="card-title">General Talent Network</h2>
          <p className={styles.bodyMuted}>
            We are always looking for passionate AI practitioners, researchers, and technical mentors. Feel free to reach out to us with your portfolio.
          </p>
          <a href="mailto:contactus@dbert.in" className="btn btn-outline">Submit Your Portfolio</a>
        </div>
      </div>
    </div>
  );
}
