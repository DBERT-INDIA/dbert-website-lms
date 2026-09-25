const withMDX = require('@next/mdx')({
  extension: /\.mdx?$/,
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
  async redirects() {
    return [
      {
        source: '/learners/incubation/:path*',
        destination: '/learners/launchpad/:path*',
        permanent: true,
      },
      {
        source: '/learners/training/:path*',
        destination: '/learners/accelerate/:path*',
        permanent: true,
      },
      {
        source: '/learners/internship/:path*',
        destination: '/learners/fellowship/:path*',
        permanent: true,
      }
    ];
  }
};

module.exports = withMDX(nextConfig);
