# DBERT Fellowship Landing Pages — Remediation Issues Tracker

| ID | Priority | Issue | Route / Component | Resolution | Status |
|---|---|---|---|---|---|
| DBERT-001 | P0 | Broken `machine-learning` link on homepage | `src/app/page.tsx` | Driven from `getFeaturedTracks()`, linking to `/learners/courses/machine-learning`; `/courses/machine-learning` redirects permanently. | Closed |
| DBERT-002 | P0 | Broken `data-science` link on homepage | `src/app/page.tsx` | Aligned to canonical `data-analytics` track; `/courses/data-science` redirects permanently to `/learners/courses/data-analytics`. | Closed |
| DBERT-003 | P0 | Broken `backend-engineering` link on homepage | `src/app/page.tsx` | Aligned homepage 6 featured tracks to `DEC-002` (`python-automation`). | Closed |
| DBERT-004 | P0 | Duplicate `/courses/[domain]` route competing with `/learners/courses/{slug}` | `next.config.js`, `src/app/courses/[domain]/page.tsx`, `sitemap.ts`, `qa_knowledge_base.json` | Permanent redirects to `/learners/courses/{slug}`, `notFound()` for unknown slugs, removed `/courses/*` from sitemap. | Closed |
| DBERT-005 | P0 | Stale ₹28,000–₹38,000 prices in JSON-LD across all 11 `/learners/courses/*` pages | `src/app/learners/courses/*/page.tsx` | All 11 pages now use `FellowshipTrackTemplate` + `FELLOWSHIP_FEE` (`₹1,999` from `pricing.config.ts`). | Closed |
| DBERT-006 | P0 | Unverified "4.9/5 Rating from 465+ Fellows" and "Limited to 25" scarcity claims | `src/components/courses/CourseInteractiveShell.tsx` | Replaced with verified `FellowshipTrackTemplate` (no fabricated rating or scarcity bar). | Closed |
| DBERT-007 | P1 | Unsubstantiated LPA salary taglines on course heroes | `src/app/learners/courses/*/page.tsx` | Removed unverified LPA taglines; replaced with outcome-focused `heroOutcome`. | Closed |
| DBERT-008 | P1 | `/learners/courses/page.tsx` said "Six focused technical tracks" while rendering 11 | `src/app/learners/courses/page.tsx` | Driven from `getPublishedTracks()` (11 tracks) with updated copy and category/search filter. | Closed |
| DBERT-009 | P1 | 5 non-featured tracks had thinner content (~12KB vs 15–26KB) | `src/data/courses.specialized.ts`, `FellowshipTrackTemplate.tsx` | All 5 upgraded to full curriculum, technology roles, capstone, evaluation, and FAQ parity. | Closed |
| DBERT-010 | P1 | Homepage "View All 9 Tracks & Cities" button pointed to `/internships` | `src/app/page.tsx` | Updated to `/learners/courses` ("View All 11 Tracks"). | Closed |
| DBERT-011 | P2 | `audit:headings` reports missing `<h1>` on pages delegating to client/shared components | `scripts/check-headings.mjs` | `FellowshipTrackTemplate` renders a single `<h1>` per course page; pre-existing `/enroll/*` and `/verify/*` pages left untouched outside scope. | Accepted / Documented |
