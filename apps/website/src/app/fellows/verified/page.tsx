import React from 'react';
import type { Metadata } from 'next';
import { pageMetadata } from '@/lib/seo';
import FellowsClient, { type VerifiedFellowItem } from './FellowsClient';
import rawFellowsData from '@/data/verified_fellows_showcase.json';

const verifiedFellowsMetadata = pageMetadata('/fellows/verified');

export const metadata: Metadata = {
  ...verifiedFellowsMetadata,
  keywords: [
    'DBERT verified fellows',
    'DBERT student reviews',
    'DBERT certificates on LinkedIn',
    'DBERT alumni proof',
    'Verified AI engineers India',
    'DBERT published articles',
    'DBERT evaluation rubrics',
    'DBERT legitimate internship proof'
  ],
  openGraph: {
    ...verifiedFellowsMetadata.openGraph,
    siteName: 'DBERT',
    type: 'website',
  },
};

export default function VerifiedFellowsPage() {
  const fellows = rawFellowsData as unknown as VerifiedFellowItem[];

  // JSON-LD Structured Data
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'DBERT Verified Fellows & Published Case Studies',
    description:
      'Directory of verified fellows from DBERT Technical Incubation with authenticated certificates, LinkedIn credentials, and published engineering articles.',
    url: 'https://dbert.in/fellows/verified',
    provider: {
      '@type': 'Organization',
      name: 'DBERT (Digital Blinc Education Research and Technology)',
      url: 'https://dbert.in',
      sameAs: [
        'https://www.linkedin.com/company/dbert',
        'https://github.com/DBERT-INDIA'
      ]
    },
    mainEntity: {
      '@type': 'ItemList',
      numberOfItems: fellows.length,
      itemListElement: fellows.slice(0, 30).map((fellow, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        item: {
          '@type': 'EducationalOccupationalCredential',
          name: `${fellow.name} — ${fellow.domain} Fellowship Credential`,
          credentialCategory: 'Technical Incubation Certificate',
          url: fellow.verificationUrl,
          recognizedBy: {
            '@type': 'Organization',
            name: 'DBERT Technical Council'
          }
        }
      }))
    }
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <FellowsClient fellows={fellows} />
    </>
  );
}
