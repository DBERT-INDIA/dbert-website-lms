/**
 * cPanel Passenger / Phusion entry point.
 *
 * cPanel's "Setup Node.js App" feature uses Phusion Passenger to serve
 * Node.js apps. Passenger looks for `app.js` OR `server.js` in the
 * application root. This file bootstraps the standalone Next.js server
 * produced by `next build` when `output: 'standalone'` is set.
 *
 * How it works:
 *   1. `next build` with `output: 'standalone'` emits .next/standalone/server.js
 *   2. cPanel uploads the ENTIRE .next/standalone/ directory as the app root
 *   3. Passenger runs this server.js which calls Next.js' own minimal HTTP server
 *
 * Environment variables that MUST be set in cPanel before starting:
 *   PORT              (cPanel sets this automatically via Passenger)
 *   DATABASE_URL      postgresql://user:pass@host:5432/dbname
 *   JWT_SECRET        a long random string
 *   ADMIN_SETUP_TOKEN a one-time secret for /api/admin/setup
 *   NEXT_PUBLIC_SITE_URL  https://dbert.online
 *   RAZORPAY_KEY_ID        rzp_live_...
 *   RAZORPAY_KEY_SECRET    ...
 *   NEXT_PUBLIC_RAZORPAY_KEY_ID  rzp_live_...
 *   RAZORPAY_WEBHOOK_SECRET      ...
 *   NEXT_PUBLIC_GA_ID   G-XXXXXXXXXX
 */

// The standalone build's own server.js is already at this path after
// the .next/standalone directory is uploaded as the cPanel app root.
// Re-exporting it means Passenger's require('./server.js') resolves here.
process.env.PORT = process.env.PORT || '3000';
process.env.HOSTNAME = '0.0.0.0';

require('./server.js');
