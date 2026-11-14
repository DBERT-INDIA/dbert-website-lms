import React from 'react';

interface ArticleSchemaProps {
  title: string;
  description: string;
  datePublished: string;
  authorName: string;
  authorUrl?: string;
  slug: string;
  certId?: string;
  domain?: string;
}

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in';

/**
 * Server component injecting Google Rich Results compliant Article & BreadcrumbList JSON-LD structured schema.
 */
export default function ArticleSchema({
  title,
  description,
  datePublished,
  authorName,
  authorUrl,
  slug,
  certId,
  domain,
}: ArticleSchemaProps) {
  const articleUrl = `${SITE_URL}/blog/${slug}`;
  const resolvedAuthorUrl = authorUrl || (certId ? `${SITE_URL}/verify/${certId}` : `${SITE_URL}/verify/directory`);
  
  const articleJson = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': articleUrl,
    },
    headline: title,
    description: description,
    image: `${SITE_URL}/alkame.png`,
    datePublished: new Date(datePublished).toISOString(),
    dateModified: new Date(datePublished).toISOString(),
    inLanguage: 'en-US',
    proficiencyLevel: 'Professional',
    about: domain || 'Software Engineering & Artificial Intelligence',
    author: {
      '@type': 'Person',
      name: authorName,
      url: resolvedAuthorUrl,
      jobTitle: `${domain || 'AI & Full Stack'} Engineering Fellow`,
      ...(certId ? {
        hasCredential: {
          '@type': 'EducationalOccupationalCredential',
          name: 'DBERT Verified Engineering Credential',
          credentialCategory: 'Professional Fellowship & Capstone Evaluation',
          recognizedBy: {
            '@type': 'Organization',
            name: 'DBERT India',
            url: SITE_URL,
          },
        },
      } : {}),
    },
    publisher: {
      '@type': 'Organization',
      name: 'DBERT Labs',
      url: SITE_URL,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/alkame.png`,
      },
      sameAs: [
        'https://www.linkedin.com/company/dbert-india/',
      ],
    },
  };

  const breadcrumbJson = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: SITE_URL,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Engineering Blog',
        item: `${SITE_URL}/blog`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: title,
        item: articleUrl,
      },
    ],
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleJson) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbJson) }}
      />
    </>
  );
}
