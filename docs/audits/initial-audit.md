# DBERT Fellowship Landing Pages — Initial Audit Report (Phase 0)

**Date:** 2026-11-24  
**Branch:** `fix/fellowship-landing-pages`  
**Baseline Commit SHA:** `4bfa105a84ae468c1afbf7e72cf0f32f0208fcd1`  
**Audited Directory:** `apps/website/`

---

## 1. Repository & Stack Summary
- **Framework:** Next.js `16.3.4` (App Router, Turbopack, `output: 'standalone'`), React `19.2.7`, TypeScript `6.0.3`.
- **Styling:** CSS Modules (`*.module.css`) + global design tokens in `src/app/globals.css`, `lucide-react` icons, `clsx`.
- **Database / ORM:** Prisma `7.8.0` (`@prisma/adapter-pg`, `pg`), plus JSON data registries in `src/data/` and `data/`.
- **Payments & Auth:** `razorpay` (`^2.9.8`), `jsonwebtoken`, `bcryptjs`, UPI QR/UTR flow (`/api/enroll/balance`, `/api/courses/enroll`), external LMS sync (`https://lms.dbert.in`).
- **Analytics:** Google Analytics 4 (`G-MN7ME9X518`) + internal telemetry (`/api/telemetry/traffic`).
- **Baseline Build & Checks:**
  - `npm run build`: **PASS** (357 static/SSG pages compiled cleanly).
  - `npm run check:seo`: **PASS** (81 entries checked against 81 routed pages).
  - `npm run audit:headings`: **WARN/FAIL** (10 pages missing `<h1>`, 1 page with 2 `<h1>`, 3 skipped heading levels).
  - `npm run check:links`: Requires local server running on `:3000` (`ECONNREFUSED` when server is off).

## 2. Route Inventory Summary
See [`route-inventory.md`](./route-inventory.md) for the full table.
- **Canonical course pages:** 11 routes under `/learners/courses/{slug}`.
- **Competing duplicate route:** `/courses/[domain]` (9 hardcoded slugs in `COURSES_DATA`).

## 3. Broken Links & 404s
1. `src/app/page.tsx` (`featuredTracks`):
   - `/courses/machine-learning` -> **404** (missing from `COURSES_DATA` in `/courses/[domain]/page.tsx`).
   - `/courses/data-science` -> **404** (canonical slug is `data-analytics`).
   - `/courses/backend-engineering` -> **404** (track does not exist).
2. `src/app/page.tsx` line 435: "View All 9 Tracks & Cities" points to `/internships` instead of `/learners/courses`.

## 4. Duplicate or Conflicting Course Data
- Course definitions are duplicated independently across:
  1. `src/app/page.tsx` (`featuredTracks` array — 6 items, 2 invalid slugs)
  2. `src/app/learners/page.tsx` (inline array — 6 items, valid `/learners/courses/` slugs)
  3. `src/app/learners/courses/page.tsx` (`courses` array — 11 items, intro copy says "Six")
  4. `src/app/learners/courses/*/page.tsx` (11 separate files with hardcoded JSON-LD prices ₹28,000–₹38,000)
  5. `src/app/courses/[domain]/page.tsx` (`COURSES_DATA` — 9 items, price ₹1,999, unverified 4.9/5 rating)
  6. `src/components/forms/TrackLeadCaptureForm.tsx` (`DOMAIN_OPTIONS` — 10 items, missing `digital-marketing`)

## 5. CTA & Application Flow
- Primary external application portal: `https://lms.dbert.in` (and `lms.dbert.in/apply`).
- Lead capture form: `TrackLeadCaptureForm` -> `POST /api/leads/capture`.
- Deposit / balance payment endpoints: `POST /api/courses/enroll` (₹499), `POST /api/enroll/balance` (₹1,500), `GET /api/enroll/lookup`, `/api/payments/*` (Razorpay).

## 6. Content Inconsistencies
- **Pricing:** Course pages list ₹28,000–₹38,000 in JSON-LD `Offer`, while `/learners/fellowship`, `/courses/[domain]`, `/pricing`, and `pricing.config.ts` state **₹1,999** for the 2-month fellowship.
- **Salary claims:** All 11 `/learners/courses/*` pages display "Verified Average Starting Remuneration" (e.g., `₹5,00,000 – ₹12,00,000 LPA`) without an evidence source.
- **Scarcity/Ratings:** `CourseInteractiveShell.tsx` displays `Limited to 25 Vetted Fellows` and `⭐ 4.9/5 Rating from 465+ Fellows` without a verified rating dataset.
- **Depth gap:** 5 non-featured tracks (`cybersecurity`, `devops-cloud`, `digital-marketing`, `mobile-app-development`, `ui-ux-design`) are ~12KB vs 15–26KB for the 6 featured tracks.

## 7. Backend Dependencies
- `/api/courses/enroll`, `/api/leads/capture`, `/api/enroll/lookup`, `/api/enroll/balance`, `/api/payments/*`, `/api/verify`, and `lms.dbert.in` must remain **100% intact**.

## 8. Accessibility & SEO Observations
- `audit:headings` flagged missing `<h1>` on `/courses/[domain]`, `/enroll/1999`, `/fellows/verified`, `/verify/directory`, etc.
- `sitemap.ts` currently indexes `/courses/*` routes alongside `/learners/courses/*`.

## 9. Decisions Resolved via `/grill-me`
All mandatory policy questions were resolved and logged in [`docs/decisions/decision-log.md`](../decisions/decision-log.md) (`DEC-001` through `DEC-007`).

## 10. Prioritised Findings
- **P0:** Fix 3 broken homepage links (`DBERT-001`–`003`), eliminate `/courses/[domain]` duplication via permanent redirects (`DBERT-004`), fix stale ₹28k–₹38k JSON-LD pricing (`DBERT-005`), remove fabricated 4.9/5 rating & scarcity bar (`DBERT-006`).
- **P1:** Remove/qualify unverified LPA salary claims (`DBERT-007`), unify catalogue to 11 tracks (`DBERT-008`), upgrade 5 thinner tracks to shared template & depth (`DBERT-009`), fix homepage "View All" CTA (`DBERT-010`).
- **P2:** Fix `audit:headings` issues (`DBERT-011`) and add Phase 8–9 enhancements.
