'use client';

import { usePathname } from 'next/navigation';
import { seoConfig } from '@/data/seo.config';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.online';

/** Fallback label for a path segment with no SEO entry (e.g. blog slugs). */
function labelFromSegment(segment: string): string {
  return segment
    .split('-')
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

/**
 * Emits BreadcrumbList JSON-LD on every route below the homepage.
 *
 * Mounted once in the root layout rather than added to 56 pages. It is a client
 * component because Next.js does not expose the pathname to server layouts —
 * the alternatives were middleware plus `headers()`, which would opt the entire
 * app out of static rendering, or editing every page. Google renders JavaScript
 * and reads structured data injected this way.
 *
 * Crumb names reuse the titles in src/data/seo.config.ts so breadcrumb labels
 * and page titles can never drift apart.
 */
export default function Breadcrumbs() {
  const pathname = usePathname();

  if (!pathname || pathname === '/') return null;

  const segments = pathname.split('/').filter(Boolean);

  const items = [
    {
      '@type': 'ListItem',
      position: 1,
      name: 'Home',
      item: SITE_URL,
    },
    ...segments.map((segment, index) => {
      const route = '/' + segments.slice(0, index + 1).join('/');
      return {
        '@type': 'ListItem',
        position: index + 2,
        name: seoConfig[route]?.title ?? labelFromSegment(segment),
        item: `${SITE_URL}${route}`,
      };
    }),
  ];

  const json = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items,
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(json) }}
    />
  );
}
