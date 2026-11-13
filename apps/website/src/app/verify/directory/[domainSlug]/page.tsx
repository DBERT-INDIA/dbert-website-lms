import React from 'react';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import DirectoryClient, { type CandidateDirectoryItem } from '../DirectoryClient';
import directoryData from '@/data/directory_candidates.json';
import {
  CANONICAL_DOMAINS,
  getDomainBySlug,
  normalizeDomainToSlug,
} from '@/data/domains.config';
import { ArrowRight, ShieldCheck, UserCheck, HelpCircle } from 'lucide-react';

interface DomainPageProps {
  params: Promise<{
    domainSlug: string;
  }>;
}

/**
 * Pre-render all 7 canonical technical domain directory pages statically at build time.
 */
export async function generateStaticParams() {
  return Object.keys(CANONICAL_DOMAINS).map((slug) => ({
    domainSlug: slug,
  }));
}

/**
 * Generate domain-specific SEO metadata compliant with Next.js strict bounds (<=52 title, 140-155 desc).
 */
export async function generateMetadata({ params }: DomainPageProps): Promise<Metadata> {
  const { domainSlug } = await params;
  const domain = getDomainBySlug(domainSlug);
  if (!domain) {
    return {
      title: 'Domain Directory | DBERT Pre-Vetted Talent',
      description: 'Search DBERT verified software engineers and AI developers with audited production code and evaluation dossiers.',
    };
  }

  const pageUrl = `https://dbert.in/verify/directory/${domain.slug}`;

  return {
    title: domain.seoTitle,
    description: domain.seoDescription,
    keywords: domain.keywords,
    openGraph: {
      title: `${domain.seoTitle} | DBERT Labs`,
      description: domain.seoDescription,
      url: pageUrl,
      siteName: 'DBERT',
      type: 'website',
    },
    alternates: {
      canonical: pageUrl,
    },
  };
}

export default async function DomainDirectoryPage({ params }: DomainPageProps) {
  const { domainSlug } = await params;
  const domain = getDomainBySlug(domainSlug);

  if (!domain) {
    notFound();
  }

  const allCandidates = directoryData as CandidateDirectoryItem[];
  const domainCandidates = allCandidates.filter(
    (c) => normalizeDomainToSlug(c.domain) === domain.slug
  );

  const pageUrl = `https://dbert.in/verify/directory/${domain.slug}`;

  // 1. ItemList Schema for Domain Candidates
  const itemListSchema = {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: `DBERT Pre-Vetted ${domain.name} Directory`,
    description: domain.description,
    url: pageUrl,
    numberOfItems: domainCandidates.length,
    itemListElement: domainCandidates.slice(0, 30).map((cand, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      item: {
        '@type': 'Person',
        name: cand.holderName,
        jobTitle: `${cand.domain} Engineer`,
        identifier: cand.certId,
        url: `https://dbert.in/verify/${cand.certId}`,
        knowsAbout: [...domain.primarySkills, 'Production Code Review'],
        award: `${cand.score}/100 Evaluation Grade ${cand.grade}`,
      },
    })),
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
        item: 'https://dbert.in',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Pre-Vetted Directory',
        item: 'https://dbert.in/verify/directory',
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: `${domain.shortName} Engineers`,
        item: pageUrl,
      },
    ],
  };

  // 3. FAQPage Schema
  const faqPageSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: domain.faqs.map((f) => ({
      '@type': 'Question',
      name: f.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: f.answer,
      },
    })),
  };

  return (
    <>
      {/* Structured Data Scripts */}
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
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqPageSchema) }}
      />

      {/* Main Interactive Directory Client */}
      <DirectoryClient
        candidates={allCandidates}
        currentDomainSlug={domain.slug}
        customHeadline={domain.headline}
        customDescription={domain.description}
        customBadge={domain.badge}
      />

      {/* Domain Recruiter Callout Banner */}
      <section style={{ maxWidth: '1200px', margin: '48px auto 64px', padding: '0 16px' }}>
        <div
          style={{
            background: 'linear-gradient(135deg, #0F172A 0%, #1E293B 100%)',
            border: '1px solid #334155',
            borderRadius: '14px',
            padding: '28px 32px',
            marginBottom: '48px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '24px',
            flexWrap: 'wrap',
          }}
        >
          <div>
            <span
              style={{
                fontSize: '12px',
                fontWeight: 800,
                color: 'var(--gold, #C89945)',
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                display: 'block',
                marginBottom: '6px',
              }}
            >
              ⭐ Hiring {domain.shortName} Talent?
            </span>
            <h2
              style={{
                fontSize: '22px',
                fontWeight: 800,
                color: '#FFFFFF',
                margin: '0 0 8px 0',
                lineHeight: 1.25,
              }}
            >
              Deploy pre-vetted {domain.shortName} engineers in 48 hours
            </h2>
            <p
              style={{
                fontSize: '14.5px',
                color: '#94A3B8',
                margin: 0,
                maxWidth: '650px',
                lineHeight: 1.5,
              }}
            >
              Skip weeks of screening. Our {domain.shortName} engineers are pre-evaluated on
              production pull requests, system design, and verified capstones with a 14-day
              risk-free trial.
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
              whiteSpace: 'nowrap',
            }}
          >
            Explore B2B Hiring &amp; Retainers{' '}
            <ArrowRight style={{ width: '16px', height: '16px' }} />
          </Link>
        </div>

        {/* Domain Recruiter FAQ Section */}
        <div>
          <div style={{ textAlign: 'center', marginBottom: '32px' }}>
            <span
              style={{
                fontSize: '12px',
                fontWeight: 800,
                color: '#38BDF8',
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
              }}
            >
              {domain.shortName} Hiring Intelligence &amp; Vetting
            </span>
            <h2
              style={{
                fontSize: '24px',
                fontWeight: 800,
                color: '#FFFFFF',
                margin: '6px 0 0 0',
              }}
            >
              Frequently Asked Questions by Technical Hiring Managers
            </h2>
          </div>

          <div
            style={{
              display: 'grid',
              gap: '16px',
              maxWidth: '900px',
              margin: '0 auto',
            }}
          >
            {domain.faqs.map((faq, idx) => (
              <div
                key={idx}
                style={{
                  background: '#0F172A',
                  border: '1px solid #1E293B',
                  borderRadius: '12px',
                  padding: '20px 24px',
                }}
              >
                <h3
                  style={{
                    fontSize: '16px',
                    fontWeight: 700,
                    color: '#F8FAFC',
                    margin: '0 0 8px 0',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                  }}
                >
                  <span style={{ color: 'var(--gold, #C89945)', fontSize: '18px' }}>Q:</span>
                  {faq.question}
                </h3>
                <p
                  style={{
                    fontSize: '14px',
                    color: '#94A3B8',
                    lineHeight: 1.6,
                    margin: 0,
                    paddingLeft: '28px',
                  }}
                >
                  {faq.answer}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
