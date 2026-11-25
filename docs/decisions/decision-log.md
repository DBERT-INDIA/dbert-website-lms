# DBERT Fellowship Remediation — Decision Log

## DEC-001 — Canonical eleven fellowship tracks
- **Date:** 2026-11-24
- **Decision owner:** DBERT Product Owner (via `/grill-me`)
- **Decision:** All **11** existing tracks under `/learners/courses/{slug}` are approved and form the canonical catalogue (the earlier plan reference to "nine" tracks is superseded).
  1. `ai-agent-development` — AI Agent Development
  2. `generative-ai` — Generative AI Systems
  3. `machine-learning` — Machine Learning & Fine-Tuning
  4. `python-automation` — Python Automation
  5. `full-stack-development` — Full Stack Web Development
  6. `data-analytics` — Data Analytics & BI
  7. `ui-ux-design` — UI/UX Design
  8. `devops-cloud` — DevOps & Cloud Engineering
  9. `mobile-app-development` — Mobile App Development
  10. `cybersecurity` — Cybersecurity & Threat Defense
  11. `digital-marketing` — Digital Marketing & Growth
- **Alternatives:** Restricting to 6 featured tracks or 9 tracks.
- **Reason:** All 11 tracks already have active pages and SEO entries, and all 11 feed into the fellowship pathway.
- **Affected routes/data:** `src/data/courses.config.ts` (to be created), `src/app/learners/courses/*`, `src/app/learners/page.tsx`, `src/app/page.tsx`, `src/app/sitemap.ts`.
- **Approved by:** User (2026-11-24 `/grill-me`)

## DEC-002 — Homepage featured subset (6 of 11)
- **Date:** 2026-11-24
- **Decision owner:** DBERT Product Owner (via `/grill-me`)
- **Decision:** Keep the 6 currently featured tracks (`ai-agent-development`, `generative-ai`, `machine-learning`, `full-stack-development`, `python-automation`, `data-analytics`) as the featured homepage/learners subset, with "View all tracks" linking to `/learners/courses` showing all 11 published tracks.
- **Affected routes/data:** `src/app/page.tsx` (currently links to broken `data-science` and `backend-engineering` slugs — must be aligned to these 6), `src/app/learners/page.tsx`, `src/app/learners/courses/page.tsx`.
- **Approved by:** User (2026-11-24 `/grill-me`)

## DEC-003 — Canonical course route pattern & legacy redirects
- **Date:** 2026-11-24
- **Decision owner:** DBERT Product Owner (via `/grill-me`)
- **Decision:** `/learners/courses/{slug}` is the single canonical route for all 11 tracks. The overlapping `/courses/[domain]` route (and any legacy alias like `/courses/data-science` or `/courses/backend-engineering`) must redirect permanently (308/301) to `/learners/courses/{slug}` (or `/learners/courses` for `/courses` if applicable, or proper 404 for invalid slugs).
- **Alternatives:** Migrating to `/fellowships/{slug}` or `/courses/{slug}`.
- **Reason:** Preserves existing SEO authority and `seo.config.ts` / `nav.config.json` links under `/learners/courses/*`.
- **Affected routes/data:** `apps/website/next.config.js`, `src/app/courses/[domain]/page.tsx`, `src/app/page.tsx`, `src/app/sitemap.ts`, `src/data/qa_knowledge_base.json`.
- **Approved by:** User (2026-11-24 `/grill-me`)

## DEC-004 — Fellowship fee structure (₹1,999 total program fee)
- **Date:** 2026-11-24
- **Decision owner:** DBERT Product Owner (via `/grill-me`)
- **Decision:** The ₹1,999 fee is the **total program fee** for the 2-month (8-week) fellowship, covering 1-on-1 mentorship, senior PR code reviews, active repository assignment, and verifiable 3-document credential issuance. (When a candidate has already paid the ₹499 caution deposit, the remaining balance is ₹1,500, as defined in `src/config/pricing.config.ts`.)
- **Affected routes/data:** All 11 course pages (which currently carry stale ₹28,000–₹38,000 JSON-LD offers), `/learners/fellowship`, `/pricing`, `/enroll/1999`.
- **Approved by:** User (2026-11-24 `/grill-me`)

## DEC-005 — Placement guarantee definition
- **Date:** 2026-11-24
- **Decision owner:** DBERT Product Owner (via `/grill-me`)
- **Decision:** "100% Guaranteed Production Internship with Dedicated Placement Assistance" means guaranteed assignment to an active internal DBERT venture (Gayatri AI, Alkame, Aivara) or verified external partner project upon successful sprint completion — it is a real production internship assignment, **not** an unconditional full-time job guarantee.
- **Eligibility:** Completion of 8-week sprint milestones, audited code quality/security/testing/documentation benchmarks, and Turnitin < 5% originality where applicable.
- **Approved by:** User (2026-11-24 `/grill-me`)

## DEC-006 — Uniform fellowship pathway across all 11 tracks & content parity
- **Date:** 2026-11-24
- **Decision owner:** DBERT Product Owner (via `/grill-me`)
- **Decision:** All 11 tracks offer the same 2-month fellowship pathway and guarantees. The 5 thinner non-featured tracks (`cybersecurity`, `devops-cloud`, `digital-marketing`, `mobile-app-development`, `ui-ux-design`) must be upgraded to match the depth and structure of the 6 featured tracks.
- **Approved by:** User (2026-11-24 `/grill-me`)

## DEC-007 — Branching & deployment workflow
- **Date:** 2026-11-24
- **Decision owner:** DBERT Product Owner (via `/grill-me`)
- **Decision:** Work on feature branch `fix/fellowship-landing-pages` (created from `4bfa105a84ae468c1afbf7e72cf0f32f0208fcd1`). Local changes only; **do not deploy** to production EC2 until explicitly authorised.
- **Approved by:** User (2026-11-24 `/grill-me`)
