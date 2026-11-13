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
    ];
  },
};

module.exports = withMDX(nextConfig);
