# DBERT Fellowship Remediation — Agent Session Log

## 2026-11-24 — Session 1 (Phase 0)

### Completed
- Created feature branch `fix/fellowship-landing-pages` from baseline commit `4bfa105a84ae468c1afbf7e72cf0f32f0208fcd1` (preserving uncommitted local work via stash/pop).
- Resolved 7 core policy/architecture decisions via `/grill-me` (`DEC-001` through `DEC-007`).
- Audited `apps/website` stack, routes, `next.config.js`, `pricing.config.ts`, `seo.config.ts`, `nav.config.json`, `sitemap.ts`, `src/app/page.tsx`, `src/app/courses/[domain]/page.tsx`, and all 11 `/learners/courses/*/page.tsx` files.
- Ran baseline `npm run build` (PASS, 357 routes), `npm run check:seo` (PASS, 81/81), and `npm run audit:headings` (10 missing `<h1>`, 1 multi-`<h1>`, 3 skipped levels).
- Created Phase 0 deliverables: `docs/audits/initial-audit.md`, `docs/audits/route-inventory.md`, `docs/audits/remediation-issues.md`, `docs/decisions/decision-log.md`, and `docs/audits/agent-session-log.md`.

### Files changed
- `docs/audits/initial-audit.md` (new)
- `docs/audits/route-inventory.md` (new)
- `docs/audits/remediation-issues.md` (new)
- `docs/decisions/decision-log.md` (new)
- `docs/audits/agent-session-log.md` (new)

### Commands/tests run
- `npm run build` -> PASS (357 pages)
- `npm run check:seo` -> PASS (81 entries)
- `npm run audit:headings` -> PASS with findings (10 missing h1, 1 multi-h1, 3 skipped)

### Decisions needed
- None for Phases 1–3; all policy decisions (`DEC-001`–`DEC-007`) are logged.

### Next actions
- Proceed to **Phase 1**: Repair route failures and navigation (redirect `/courses/[domain]` -> `/learners/courses/{slug}`, fix homepage `featuredTracks` and "View All" link, clean `sitemap.ts`, update `qa_knowledge_base.json`).

## 2026-11-24 — Session 2 (Phases 1–10)

### Completed
- **Phase 1:** Added permanent redirects `/courses` -> `/learners/courses` and `/courses/:slug` -> `/learners/courses/:slug` (plus `data-science` -> `data-analytics`) in `next.config.js` and `src/app/courses/[domain]/page.tsx`. Fixed homepage `featuredTracks` and "View All 11 Tracks" link, cleaned `sitemap.ts`, and fixed `qa_knowledge_base.json`.
- **Phase 2:** Created single source of truth `src/data/courses.types.ts`, `src/data/courses.core.ts`, `src/data/courses.specialized.ts`, and `src/data/courses.config.ts` (11 tracks, integrated with `pricing.config.ts` ₹1,999 fee). Wired `/`, `/learners`, `/learners/courses`, and `TrackLeadCaptureForm`. Added `scripts/check-catalogue.mjs`.
- **Phases 3–6:** Built `CurriculumAccordion.tsx` and `FellowshipTrackTemplate.tsx`; migrated all 11 `/learners/courses/*/page.tsx` routes; upgraded all 5 specialized tracks to full depth; removed unverified LPA/rating/scarcity claims; added `#placement-policy` on `/learners/fellowship` and `docs/content/claims-register.md`.
- **Phases 7–10:** Added accessible category/search filter (`CoursesCatalogueClient.tsx`) on `/learners/courses`; preserved all payment/application APIs; ran `check-catalogue.mjs`, `check:seo`, `audit:headings`, `lint`, and `build`; created `final-audit.md`, `regression-report.md`, and `rollback.md`.
