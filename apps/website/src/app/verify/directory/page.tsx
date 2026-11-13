import React from 'react';
import type { Metadata } from 'next';
import Link from 'next/link';
import DirectoryClient, { type CandidateDirectoryItem } from './DirectoryClient';
import directoryData from '@/data/directory_candidates.json';
import { ArrowRight, ShieldCheck, UserCheck, CheckCircle2, HelpCircle } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Pre-Vetted Engineers Directory — Hire Proven AI & Tech Talent | DBERT',
  description:
    'Search the DBERT candidate directory for pre-vetted AI, Full Stack & Data engineers with verified Turnitin rubrics and code dossiers. Connect on LMS.',
  keywords: [
    'DBERT candidate directory',
    'Hire pre-vetted AI engineers',
    'Pre-vetted developers India',
    'Hire full stack engineers vetted',
    'Hire remote data analysts India',
    'Pre-screened tech talent directory',
    'Verified software engineers India',
    'Hire python developers with code proof'
  ],
  openGraph: {
    title: 'Pre-Vetted Engineers Directory — Hire Proven Tech Talent | DBERT',
    description:
      'Search and onboard pre-screened AI, Full Stack, Data, and Python engineers with verified production code reviews and 100-point evaluation rubrics.',
    url: 'https://dbert.in/verify/directory',
    siteName: 'DBERT',
    type: 'website',
  },
  alternates: {
    canonical: 'https://dbert.in/verify/directory',
  },
};

const recruiterFaqs = [
  {
    q: 'How does DBERT pre-vet candidates in this directory?',
    a: 'Unlike traditional resume boards, DBERT evaluates candidates through intensive 60-day engineering sprints on live client repositories. Candidates undergo 1:1 mentor code reviews, Turnitin originality audits, system architecture benchmarks, and 100-point rubric scoring before receiving verified hireability distinction.'
  },
  {
    q: 'What is included in each candidate\'s Proof Dossier?',
    a: 'Every verified engineer profile deep-links to their immutable cryptographic proof dossier at /verify/[certId]. The dossier includes their Turnitin originality report, 9-dimension rubric breakdown, mentor recommendation letter, verified production pull requests, and direct LMS employer connection.'
  },
  {
    q: 'How do recruiters and engineering managers connect with candidates?',
    a: 'Recruiters can click "Connect on LMS" on any candidate card to instantly register via our verified employer portal (lms.dbert.in/company/signup). From there, you can view the full candidate CV, send direct interview requests, and coordinate technical screening without third-party gatekeepers.'
  },
  {
    q: 'Are there any recruiter commissions or agency markup?',
    a: 'Zero. DBERT operates on an ethical open-access venture model with zero recruiter markup and zero placement commission for standard direct hires from our pre-vetted talent directory.'
  },
  {
    q: 'What is the turnaround time for onboarding a pre-vetted engineer?',
    a: 'Because candidates in the verified tier have already passed technical verification and active sprint milestones, matched engineers can typically interview and start in your sprint within 48 to 72 hours.'
  }
];

export default function DirectoryPage() {
  const candidates = directoryData as CandidateDirectoryItem[];

  // 1. ItemList Schema for Candidate Dossiers
  const itemListSchema = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: 'DBERT Pre-Vetted Software & AI Engineers Directory',
    description: 'Official registry of pre-screened technical engineers evaluated on live production pull requests, system design, and 100-point academic rubrics.',
    url: 'https://dbert.in/verify/directory',
    numberOfItems: candidates.length,
    itemListElement: candidates.slice(0, 35).map((cand, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      item: {
        '@type': 'Person',
        name: cand.holderName,
        jobTitle: `${cand.domain} Engineer`,
        identifier: cand.certId,
        url: `https://dbert.in/verify/${cand.certId}`,
        knowsAbout: [cand.domain, 'Software Engineering', 'Production Code Review'],
        award: `${cand.score}/100 Evaluation Grade ${cand.grade}`
      }
    }))
  };

  // 2. BreadcrumbList Schema
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: 'https://dbert.in'
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Talent',
        item: 'https://dbert.in/hire/pre-vetted-engineers'
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: 'Pre-Vetted Engineers Directory',
        item: 'https://dbert.in/verify/directory'
      }
    ]
  };

  // 3. Recruiter FAQPage Schema
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: recruiterFaqs.map((faq) => ({
      '@type': 'Question',
      name: faq.q,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.a
      }
    }))
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(itemListSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />

      <DirectoryClient candidates={candidates} />

      {/* Recruiter Hiring & FAQ Add-On Section */}
      <section className="container pad-block" style={{ borderTop: '1px solid var(--border-subtle, #1E293B)', marginTop: '40px' }}>
        <div className="measure-lg" style={{ maxWidth: '1100px', margin: '0 auto' }}>
          
          {/* Executive B2B Banner */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%)',
            border: '1px solid rgba(200, 153, 69, 0.25)',
            borderRadius: '16px',
            padding: '28px 32px',
            marginBottom: '48px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '24px',
            flexWrap: 'wrap'
          }}>
            <div>
              <span style={{ fontSize: '12px', fontWeight: 800, color: 'var(--gold, #C89945)', textTransform: 'uppercase', letterSpacing: '0.08em', display: 'block', marginBottom: '6px' }}>
                ⭐ Need A Dedicated Engineering Squad?
              </span>
              <h2 style={{ fontSize: '22px', fontWeight: 800, color: '#FFFFFF', margin: '0 0 8px 0', lineHeight: 1.25 }}>
                Deploy pre-vetted AI &amp; Full Stack engineers in 48 hours
              </h2>
              <p style={{ fontSize: '14.5px', color: '#94A3B8', margin: 0, maxWidth: '650px', lineHeight: 1.5 }}>
                Skip months of screening. Our engineers are pre-evaluated on production pull requests, Turnitin originality, and live system architectures with a 14-day risk-free trial.
              </p>
            </div>
            <Link
              href="/hire/pre-vetted-engineers"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '8px',
                background: 'linear-gradient(135deg, #C89945 0%, #D4AF37 100%)',
                color: '#0F172A',
                fontWeight: 800,
                fontSize: '14.5px',
                padding: '12px 24px',
                borderRadius: '10px',
                textDecoration: 'none',
                boxShadow: '0 4px 14px rgba(200, 153, 69, 0.35)',
                whiteSpace: 'nowrap'
              }}
            >
              Explore B2B Hiring &amp; Retainers <ArrowRight style={{ width: '16px', height: '16px' }} />
            </Link>
          </div>

          {/* Recruiter FAQ Accordion */}
          <div>
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              <span style={{ fontSize: '12px', fontWeight: 800, color: '#38BDF8', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                Hiring Intelligence &amp; Verification
              </span>
              <h2 style={{ fontSize: '24px', fontWeight: 800, color: '#FFFFFF', marginTop: '6px', marginBottom: '8px' }}>
                Frequently Asked Questions by Technical Recruiters
              </h2>
              <p style={{ fontSize: '14.5px', color: '#94A3B8', maxWidth: '680px', margin: '0 auto' }}>
                Everything you need to know about candidate evaluation rubrics, code dossiers, and LMS direct messaging.
              </p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {recruiterFaqs.map((faq, i) => (
                <div
                  key={i}
                  style={{
                    background: 'rgba(15, 23, 42, 0.6)',
                    border: '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '12px',
                    padding: '20px 24px'
                  }}
                >
                  <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#F8FAFC', margin: '0 0 8px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <HelpCircle style={{ width: '18px', height: '18px', color: 'var(--gold, #C89945)', flexShrink: 0 }} />
                    {faq.q}
                  </h3>
                  <p style={{ fontSize: '14px', color: '#94A3B8', margin: 0, lineHeight: 1.6, paddingLeft: '26px' }}>
                    {faq.a}
                  </p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </section>
    </>
  );
}
