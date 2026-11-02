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
};

module.exports = withMDX(nextConfig);
