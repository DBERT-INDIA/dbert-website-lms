import type { Metadata } from 'next';
import { seoConfig } from '@/data/seo.config';

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.online';

/**
 * Builds a page's Metadata from the central map in src/data/seo.config.ts.
 *
 * Pages call `export const metadata = pageMetadata('/learners')` rather than
 * hand-writing title and description, so every title and description on the
 * site lives in one file that `npm run check:seo` can validate in one pass.
 *
 * The title is returned as a plain string so layout.tsx's `%s | DBERT`
 * template appends the brand exactly once.
 */
export function pageMetadata(route: string): Metadata {
  const entry = seoConfig[route];

  if (!entry) {
    throw new Error(
      `No SEO entry for route "${route}". Add it to src/data/seo.config.ts.`
    );
  }

  const metadata: Metadata = {
    title: entry.title,
    description: entry.description,
    alternates: { canonical: `${SITE_URL}${route}` },
    openGraph: {
      title: `${entry.title} | DBERT`,
      description: entry.description,
      url: `${SITE_URL}${route}`,
    },
  };

  if (entry.noindex) {
    metadata.robots = { index: false, follow: false };
  }

  return metadata;
}
