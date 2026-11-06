import { MetadataRoute } from 'next';
export const dynamic = 'force-static';
import { seoConfig } from '@/data/seo.config';
import { getBlogSlugs } from '@/lib/blog';
import certificatesRegistry from '@/data/certificates_registry.json';

/**
 * High-authority dynamic sitemap generator for dbert.in
 * Categorizes priorities and change frequencies across hubs, courses, products, careers, and verified certificates.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in';
  const lastModified = new Date();

  const getPriority = (route: string): number => {
    if (route === '') return 1.0;
    if (['/startups', '/ai-solutions', '/learners', '/labs', '/learners/courses', '/learners/jobs', '/cohorts/aivara', '/verify/directory'].includes(route)) return 0.95;
    if (['/verify', '/about/careers', '/hire/pre-vetted-engineers'].includes(route)) return 0.9;
    if (route.startsWith('/learners/courses/')) return 0.9;
    if (route.startsWith('/ai-solutions/products/')) return 0.9;
    if (route.startsWith('/startups/services/')) return 0.85;
    if (['/enroll/1999', '/about/credentials', '/pricing'].includes(route)) return 0.85;
    if (route.startsWith('/blog/')) return 0.85;
    if (route.startsWith('/verify/')) return 0.8;
    if (['/privacy', '/terms', '/refund'].includes(route)) return 0.5;
    const depth = route.split('/').filter(Boolean).length;
    if (depth <= 2) return 0.8;
    return 0.7;
  };

  const getChangeFrequency = (route: string): 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' => {
    if (route === '') return 'daily';
    if (['/learners/jobs', '/cohorts/aivara', '/verify/directory'].includes(route)) return 'daily';
    if (route.startsWith('/learners/courses') || route.startsWith('/blog/') || route.startsWith('/verify/')) return 'weekly';
    if (['/startups', '/ai-solutions', '/learners', '/verify', '/enroll/1999', '/about/careers'].includes(route)) return 'weekly';
    if (['/privacy', '/terms', '/refund'].includes(route)) return 'yearly';
    return 'monthly';
  };

  // Get verified certificates from registry
  const verifiedCertRoutes = Object.entries(certificatesRegistry as Record<string, { verified?: boolean }>)
    .filter(([, cert]) => cert.verified === true)
    .map(([certId]) => `/verify/${certId}`);

  const routes = [
    '',
    ...Object.entries(seoConfig)
      .filter(([, entry]) => !entry.noindex)
      .map(([route]) => route),
    ...getBlogSlugs().map((slug) => `/blog/${slug}`),
    ...verifiedCertRoutes,
  ];

  return routes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified,
    changeFrequency: getChangeFrequency(route),
    priority: getPriority(route),
  }));
}
