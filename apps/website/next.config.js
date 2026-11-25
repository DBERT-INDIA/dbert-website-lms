const withMDX = require('@next/mdx')({
  extension: /\.mdx?$/,
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
  // Standalone mode creates a minimal standalone Node.js server bundle for EC2
  output: 'standalone',
  images: {
    formats: ['image/avif', 'image/webp'],
    unoptimized: true,
  },
  async redirects() {
    return [
      {
        source: '/company/:slug/careers',
        destination: 'https://lms.dbert.in/company/:slug/careers',
        permanent: false,
      },
      {
        source: '/company/:slug/jobs',
        destination: 'https://lms.dbert.in/company/:slug/jobs',
        permanent: false,
      },
      {
        source: '/company/:slug',
        destination: 'https://lms.dbert.in/company/:slug/careers',
        permanent: false,
      },
      {
        source: '/insights/:slug*',
        destination: '/blog/:slug*',
        permanent: true,
      },
      {
        source: '/sitemap-lms.xml',
        destination: 'https://lms.dbert.in/sitemap.xml',
        permanent: true,
      },
      {
        source: '/verify/unlock',
        destination: '/enroll/1999',
        permanent: true,
      },
      {
        source: '/enroll/balance',
        destination: '/enroll/1999',
        permanent: true,
      },
      {
        source: '/eroll',
        destination: '/enroll/1999',
        permanent: true,
      },
      {
        source: '/courses',
        destination: '/learners/courses',
        permanent: true,
      },
      {
        source: '/courses/data-science',
        destination: '/learners/courses/data-analytics',
        permanent: true,
      },
      ...[
        'ai-agent-development',
        'generative-ai',
        'machine-learning',
        'python-automation',
        'full-stack-development',
        'data-analytics',
        'ui-ux-design',
        'devops-cloud',
        'mobile-app-development',
        'cybersecurity',
        'digital-marketing',
      ].map((slug) => ({
        source: `/courses/${slug}`,
        destination: `/learners/courses/${slug}`,
        permanent: true,
      })),
    ];
  },
};

module.exports = withMDX(nextConfig);
