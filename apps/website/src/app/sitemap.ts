import { MetadataRoute } from 'next';
import { seoConfig } from '@/data/seo.config';
import { getBlogSlugs } from '@/lib/blog';

/**
 * Derived from src/data/seo.config.ts rather than a second hand-maintained
 * list, so a route can never be added to the site and forgotten here.
 * `noindex` routes (admin) are excluded.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.online';
  const lastModified = new Date();

  const priorityFor = (route: string): number => {
    if (route === '') return 1.0;
    const depth = route.split('/').filter(Boolean).length;
    if (depth === 1) return 0.9; // hubs
    if (depth === 2) return 0.8;
    return 0.7;
  };

  const routes = [
    '',
    ...Object.entries(seoConfig)
      .filter(([, entry]) => !entry.noindex)
      .map(([route]) => route),
    ...getBlogSlugs().map((slug) => `/blog/${slug}`),
  ];

  return routes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified,
    changeFrequency: route === '' ? 'weekly' : 'monthly',
    priority: priorityFor(route),
  }));
}
