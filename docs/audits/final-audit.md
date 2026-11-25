# DBERT Fellowship Landing Pages — Final Remediation Report

**Date:** 2026-11-24  
**Branch:** `fix/fellowship-landing-pages` (from `4bfa105a84ae468c1afbf7e72cf0f32f0208fcd1`)

## Executive Summary
All 10 phases of the DBERT Fellowship Landing Page Remediation Master Plan have been executed locally without altering backend APIs, database schemas, or deploying to production EC2. All 11 canonical fellowship tracks now share a single source of truth (`src/data/courses.config.ts`) and a unified, accessible landing-page template (`FellowshipTrackTemplate.tsx`), with broken homepage links and duplicate `/courses/*` routes resolved.

## Routes Repaired
- `/` (`src/app/page.tsx`): Replaced broken `/courses/machine-learning`, `/courses/data-science`, and `/courses/backend-engineering` links with the 6 canonical featured tracks from `getFeaturedTracks()`, linking to `/learners/courses/{slug}`. Updated "View All" CTA to `/learners/courses` ("View All 11 Tracks").
- `/courses/[domain]` (`next.config.js` & `src/app/courses/[domain]/page.tsx`): Added permanent redirects to `/learners/courses/{slug}` for all 11 canonical slugs (plus `/courses/data-science` -> `/learners/courses/data-analytics` and `/courses` -> `/learners/courses`). Unknown slugs return `404` (`notFound()`).
- `src/app/sitemap.ts`: Removed duplicate `/courses/*` URLs so only canonical `/learners/courses/*` routes are indexed.
- `src/data/qa_knowledge_base.json`: Updated `/courses/ai-agent-development` -> `/learners/courses/ai-agent-development`.

## Course Catalogue
- **Approved Tracks (11):** `ai-agent-development`, `generative-ai`, `machine-learning`, `full-stack-development`, `python-automation`, `data-analytics`, `ui-ux-design`, `devops-cloud`, `mobile-app-development`, `cybersecurity`, `digital-marketing`.
- **Canonical Routes:** `/learners/courses/{slug}` for all 11 tracks.
- **Single Source of Truth:** `src/data/courses.config.ts` (`courses.types.ts`, `courses.core.ts`, `courses.specialized.ts`) integrated with `src/config/pricing.config.ts` (`₹1,999` total fee, `₹499` caution deposit, `₹1,500` balance).
- **Consumers Unified:** `/`, `/learners`, `/learners/courses`, all 11 `/learners/courses/{slug}` pages, and `TrackLeadCaptureForm`.

## UX and Content Changes
- Created `FellowshipTrackTemplate.tsx` and `CurriculumAccordion.tsx` (accessible, keyboard-operable, non-PII `curriculum_expand` GA4 event).
- Added category filtering and keyword search (`CoursesCatalogueClient.tsx`) on `/learners/courses`.
- Upgraded the 5 thinner tracks (`ui-ux-design`, `devops-cloud`, `mobile-app-development`, `cybersecurity`, `digital-marketing`) to full curriculum, technology-role, capstone, evaluation, and FAQ parity.
- Removed unverified LPA salary taglines, stale ₹28,000–₹38,000 JSON-LD offers, and unverified rating/scarcity claims.

## Placement, Pricing, and Policy Changes
- Added `#placement-policy` anchor and explicit fee/refund/terms disclosure on `/learners/fellowship`.
- Linked `/learners/fellowship#placement-policy`, `/refund`, `/terms`, and `/enroll/1999` directly from every course page.
- Documented all public claims in `docs/content/claims-register.md`.

## Backend / Database Impact
- **No backend or database schema changes.**
- Preserved `/api/courses/enroll`, `/api/leads/capture`, `/api/enroll/lookup`, `/api/enroll/balance`, `/api/payments/*`, `/api/verify`, and `lms.dbert.in` links intact.

## Deployment Status
- **Local changes only** on branch `fix/fellowship-landing-pages` per `DEC-007`. Production EC2 has **not** been modified.
