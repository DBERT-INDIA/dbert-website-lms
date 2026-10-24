const withMDX = require('@next/mdx')({
  extension: /\.mdx?$/,
});

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
  // Export mode generates static HTML/CSS/JS for basic shared hosting
  output: 'export',
  trailingSlash: true,
  images: {
    formats: ['image/avif', 'image/webp'],
    // On cPanel shared hosting, the built-in Next.js image optimiser
    // requires sharp which may not compile. Setting unoptimized:true
    // serves images as-is from the public/ directory.
    // Remove this line if your host successfully installs sharp.
    unoptimized: true,
  },
};

module.exports = withMDX(nextConfig);
