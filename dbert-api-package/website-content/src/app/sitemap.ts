import { MetadataRoute } from 'next';
export const dynamic = 'force-static';
import { seoConfig } from '@/data/seo.config';
import { getBlogSlugs } from '@/lib/blog';

/**
 * High-authority dynamic sitemap generator for dbert.online
 * Categorizes priorities and change frequencies across hubs, courses, products, and articles.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.online';
  const lastModified = new Date();

  const getPriority = (route: string): number => {
    if (route === '') return 1.0;
    if (['/startups', '/ai-solutions', '/learners', '/labs', '/learners/courses'].includes(route)) return 0.95;
    if (route.startsWith('/learners/courses/')) return 0.9;
    if (route.startsWith('/ai-solutions/products/')) return 0.9;
    if (route.startsWith('/startups/services/')) return 0.85;
    if (route.startsWith('/blog/')) return 0.85;
    if (['/privacy', '/terms', '/refund'].includes(route)) return 0.5;
    const depth = route.split('/').filter(Boolean).length;
    if (depth <= 2) return 0.8;
    return 0.7;
  };

  const getChangeFrequency = (route: string): 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' => {
    if (route === '') return 'daily';
    if (route.startsWith('/learners/courses') || route.startsWith('/blog/')) return 'weekly';
    if (['/startups', '/ai-solutions', '/learners', '/verify'].includes(route)) return 'weekly';
    if (['/privacy', '/terms', '/refund'].includes(route)) return 'yearly';
    return 'monthly';
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
    changeFrequency: getChangeFrequency(route),
    priority: getPriority(route),
  }));
}
