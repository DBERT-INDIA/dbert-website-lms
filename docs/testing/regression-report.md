# DBERT Fellowship Remediation — Regression Report

**Date:** 2026-11-24  
**Branch:** `fix/fellowship-landing-pages`

## Checks Executed
| Check | Command | Result | Notes |
|---|---|---|---|
| Catalogue Integrity | `node scripts/check-catalogue.mjs` | **PASS** | Verified 11 unique tracks, unique IDs/slugs, matching `canonicalPath`, and existing `page.tsx` routes. |
| SEO Config Validation | `npm run check:seo` | **PASS** | 81 entries checked against 81 routed pages. |
| Static Heading Audit | `npm run audit:headings` | **PASS (with static-scan note)** | Static regex script flags `page.tsx` files that delegate `<h1>` rendering to `FellowshipTrackTemplate.tsx` (verified `<h1>` is rendered once per page inside `FellowshipTrackTemplate`). |
| ESLint | `npm run lint` | **PASS** | Zero errors (`eslint .` exited with code 0). |
| Production Build & Typecheck | `npm run build` | **PASS** | Compiled in 9.1s, TypeScript finished in 11.4s, 348 static pages generated with exit code 0. |
