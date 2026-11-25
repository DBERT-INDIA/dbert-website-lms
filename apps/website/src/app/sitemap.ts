import { MetadataRoute } from 'next';
import fs from 'fs';
import path from 'path';
export const revalidate = 3600;
import { seoConfig } from '@/data/seo.config';
import { getBlogSlugs } from '@/lib/blog';
import { getAllDomainSlugs } from '@/data/domains.config';
import { getAllGeoInternshipRoutes } from '@/data/geo_domains.config';
import certificatesRegistry from '@/data/certificates_registry.json';

/**
 * High-authority dynamic sitemap generator for dbert.in
 * Categorizes priorities and change frequencies across hubs, courses, products, careers, domain directories, and verified certificates.
 * Strictly preserves historical indexed routes while adding all current/new domains, courses, and verified certificates.
 */
export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://dbert.in';
  const lastModified = new Date();

  const getPriority = (route: string): number => {
    if (route === '') return 1.0;
    if (['/startups', '/ai-solutions', '/learners', '/labs', '/learners/courses', '/learners/fellowship', '/learners/jobs', '/internships', '/cohorts/aivara', '/verify/directory', '/hire/pre-vetted-engineers', '/fellows/verified', '/qa', '/about/team'].includes(route)) return 0.95;
    if (route.startsWith('/verify/directory/')) return 0.90;
    if (['/verify', '/about/careers', '/labs/opensource', '/learners/accelerate', '/learners/launchpad'].includes(route)) return 0.9;
    if (route.startsWith('/learners/courses/') || route.startsWith('/courses/')) return 0.9;
    if (route.startsWith('/internships/')) return 0.85;
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
    if (['/learners/jobs', '/learners/fellowship', '/cohorts/aivara', '/verify/directory', '/hire/pre-vetted-engineers', '/fellows/verified', '/qa', '/about/team'].includes(route) || route.startsWith('/verify/directory/')) return 'daily';
    if (route.startsWith('/learners/courses') || route.startsWith('/courses/') || route.startsWith('/internships/') || route.startsWith('/blog/') || route.startsWith('/verify/')) return 'weekly';
    if (['/startups', '/ai-solutions', '/learners', '/verify', '/enroll/1999', '/about/careers', '/labs/opensource'].includes(route)) return 'weekly';
    if (['/privacy', '/terms', '/refund'].includes(route)) return 'yearly';
    return 'monthly';
  };

  // 1. Get verified certificates from registry (all verified = true)
  const verifiedCertRoutes = Object.entries(certificatesRegistry as Record<string, { verified?: boolean }>)
    .filter(([, cert]) => cert.verified === true)
    .map(([certId]) => `/verify/${certId}`);

  // 2. Get specialized 9 canonical domain directories
  const domainDirectoryRoutes = getAllDomainSlugs().map(
    (slug) => `/verify/directory/${slug}`
  );

  // 3. Get programmatic geo-internship combinations across all 18 tech hubs
  const geoInternshipRoutes = getAllGeoInternshipRoutes();

  // 4. Get 9 canonical domain course routes
  const courseDomainRoutes = [
    'ai-agent-development',
    'generative-ai',
    'full-stack-development',
    'data-analytics',
    'cybersecurity',
    'devops-cloud',
    'mobile-app-development',
    'python-automation',
    'ui-ux-design',
  ].map((slug) => `/courses/${slug}`);

  // 5. Preserve all previously indexed routes from existing public/sitemap.xml
  const historicalRoutes: string[] = [];
  try {
    const publicSitemapPath = path.join(process.cwd(), 'public/sitemap.xml');
    if (fs.existsSync(publicSitemapPath)) {
      const xml = fs.readFileSync(publicSitemapPath, 'utf-8');
      const locMatches = xml.match(/<loc>(.*?)<\/loc>/g);
      if (locMatches) {
        locMatches.forEach((m) => {
          const u = m.replace(/<\/?loc>/g, '').trim();
          const route = u.replace(baseUrl, '').replace('https://dbert.in', '');
          if (route || route === '') {
            historicalRoutes.push(route);
          }
        });
      }
    }
  } catch {
    // Graceful fallback
  }

  // 6. Combine and deduplicate all routes (previous + current)
  const routes = [
    '',
    ...historicalRoutes.filter((route) => !seoConfig[route]?.noindex),
    ...Object.entries(seoConfig)
      .filter(([, entry]) => !entry.noindex)
      .map(([route]) => route),
    ...getBlogSlugs().map((slug) => `/blog/${slug}`),
    ...domainDirectoryRoutes,
    ...courseDomainRoutes,
    ...geoInternshipRoutes,
    ...verifiedCertRoutes,
  ];

  const uniqueRoutes = Array.from(new Set(routes));

  return uniqueRoutes.map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified,
    changeFrequency: getChangeFrequency(route),
    priority: getPriority(route),
  }));
}
