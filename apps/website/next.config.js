const withMDX = require('@next/mdx')({
  extension: /\.mdx?$/,
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
  // Standalone mode bundles the Node.js server so cPanel Passenger can
  // run it without a globally-installed Next.js.
  output: 'standalone',
  images: {
    formats: ['image/avif', 'image/webp'],
    // On cPanel shared hosting, the built-in Next.js image optimiser
    // requires sharp which may not compile. Setting unoptimized:true
    // serves images as-is from the public/ directory.
    // Remove this line if your host successfully installs sharp.
    unoptimized: true,
  },
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
