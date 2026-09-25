import React from 'react';

interface ArticleSchemaProps {
  title: string;
  description: string;
  datePublished: string;
  authorName: string;
  authorUrl?: string;
  slug: string;
}

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.online';

/**
 * Server component injecting Google Rich Results compliant Article JSON-LD structured schema.
 */
export default function ArticleSchema({
  title,
  description,
  datePublished,
  authorName,
  authorUrl = `${SITE_URL}/about/team`,
  slug,
}: ArticleSchemaProps) {
  const articleUrl = `${SITE_URL}/blog/${slug}`;
  
  const json = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': articleUrl,
    },
    headline: title,
    description: description,
    image: `${SITE_URL}/alkame.png`, // Fallback high-res lab brand emblem
    datePublished: new Date(datePublished).toISOString(),
    dateModified: new Date(datePublished).toISOString(),
    author: {
      '@type': 'Person',
      name: authorName,
      url: authorUrl,
    },
    publisher: {
      '@type': 'Organization',
      name: 'DBERT Labs',
      url: SITE_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/alkame.png`,
      },
    },
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(json) }}
    />
  );
}
