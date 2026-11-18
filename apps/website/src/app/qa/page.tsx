import React from 'react';
import type { Metadata } from 'next';
import Script from 'next/script';
import QAClient, { type QAItem } from './QAClient';
import qaKnowledgeBase from '@/data/qa_knowledge_base.json';

export const metadata: Metadata = {
  title: 'Technical Knowledge & Career Q&A Hub | DBERT',
  description:
    'Peer-reviewed architectural case studies, production AI agent blueprints, financial data pipelines, and career guidance for DBERT Incubation Fellows and software engineers.',
  keywords: [
    'DBERT QA Hub',
    'AI agent developer questions',
    'FastAPI enterprise architecture',
    'Streamlit NIFTY 50 analytics',
    'Redis caching latency',
    'RAG pipeline best practices',
    'DBERT incubation fellowship 1999',
    'DBERT certificate verification',
    'Is DBERT legit'
  ],
  openGraph: {
    title: 'Technical Knowledge & Career Q&A Hub | DBERT',
    description:
      'Peer-reviewed architectural case studies, production AI agent blueprints, financial data pipelines, and career guidance for DBERT Incubation Fellows.',
    url: 'https://dbert.in/qa',
    siteName: 'DBERT',
    type: 'website',
  },
  alternates: {
    canonical: 'https://dbert.in/qa',
  },
};

export default function QAPage() {
  const items = qaKnowledgeBase as QAItem[];

  // Construct Google FAQPage JSON-LD Schema
  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map(item => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: `${item.shortAnswer} ${item.detailedMarkdown.replace(/\n\n/g, ' ').replace(/\[.*?\]\(.*?\)/g, '')}`
      }
    }))
  };

  return (
    <>
      <Script
        id="qa-faqpage-schema"
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      <QAClient initialItems={items} />
    </>
  );
}
