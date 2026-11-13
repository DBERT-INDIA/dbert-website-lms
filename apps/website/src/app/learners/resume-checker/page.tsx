import React from 'react';
import { pageMetadata } from '@/lib/seo';
import ResumeCheckerClient from './ResumeCheckerClient';
import s from './resume-checker.module.css';

export const metadata = pageMetadata('/learners/resume-checker');

export default function ResumeCheckerPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'WebApplication',
    name: 'DBERT Free AI Resume & ATS Scanner',
    url: 'https://dbert.in/learners/resume-checker',
    description: 'Audit your tech resume with our free AI ATS scanner. Get instant keyword gap analysis, score ratings, and match with verified remote developer jobs today.',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'All',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'INR',
    },
    creator: {
      '@type': 'Organization',
      name: 'DBERT',
      url: 'https://dbert.in',
    },
  };

  const breadcrumbsLd = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: 'https://dbert.in',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Learners',
        item: 'https://dbert.in/learners',
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: 'AI Resume Checker',
        item: 'https://dbert.in/learners/resume-checker',
      },
    ],
  };

  return (
    <div className="glow-wrapper">
      <div className="glow-spot" />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbsLd) }}
      />

      <div className={s.container}>
        <div className={s.hero}>
          <div className={s.docLabel}>§ 01 — AUTOMATED APPLICANT TRACKING AUDIT</div>
          <h1 className={s.pageTitle}>Free AI Resume &amp; ATS Scanner 2026</h1>
          <p className={s.lede}>
            Test your resume against modern automated hiring filters. Identify missing tech stack keywords,
            measure quantifiable impact density, and optimize your profile for verified partner roles.
          </p>
        </div>

        <ResumeCheckerClient />
      </div>
    </div>
  );
}
