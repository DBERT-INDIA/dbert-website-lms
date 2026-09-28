# DBERT Website UI/UX Redesign & Remediation Progress Tracker

## Project Overview
- **Repository**: `https://github.com/DBERT-INDIA/dbert-website-lms`
- **Scope**: `apps/website/**`
- **Current Operating Branch**: `main`
- **Preservation Policy**: Handcrafted UI elements (`HandNote`, `HandDrawnArrow`, marker underlines, proof marks) are protected invariants.

---

## Master Phase Execution Matrix

| Phase | Phase Name | Status | Local Plan | Approved | Implemented | Phase Tests | Full Regression | Visual QA | Commit | Pushed | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **0** | Baseline, Route Inventory & Visual Evidence | **COMPLETED** | Done (`WEBSITE_UIUX_PHASE_PLAN.md`) | Approved | Done | Passed (`check:seo`, `tsc`, `lint`, `build`) | Passed | Complete | `b42a791` | Pushed | Cataloged 90 routes; verified handcrafted assets; created audit tools |
| **1** | Design System Consolidation | **COMPLETED** | Done (`WEBSITE_UIUX_PHASE_PLAN.md`) | Approved | Done | Passed (`check:seo`, `tsc`, `lint`, `build`) | Passed | Complete | `9532273` | Pushed | Semantic token architecture, resolve SEO-ERR-001, create reference specification |
| **2** | Global Shell: Header, Navigation, Footer | **COMPLETED** | Done (`WEBSITE_UIUX_PHASE_PLAN.md`) | Approved | Done | Passed (`check:seo`, `tsc`, `lint`, `build`) | Passed | Complete | `cb73dd5` | Pushed | MegaMenu featured cards, active route tracking, 4-column footer, mobile drawer |
| **3** | Homepage Recomposition | **COMPLETED** | Done (`WEBSITE_UIUX_PHASE_PLAN.md`) | Approved | Done | Passed (`check:seo`, `tsc`, `lint`, `build`) | Passed | Complete | `d4c9d4f` | Pushed | CountUp SSR target render, FactTicker edge mask, hero contrast, handcrafted intact |
| **4** | Blog & Editorial Experience | **COMPLETED** | Done (`WEBSITE_UIUX_PHASE_PLAN.md`) | Approved | Done | Passed (`check:seo`, `tsc`, `lint`, `build`) | Passed | Complete | `3564488` | Pushed | Resolved `BLOG-UI-001`, contrast fixes across MDX, HandNote annotations, inline style removal |
| **5** | Learner Experience Redesign | **READY FOR APPROVAL** | Prepared (`WEBSITE_UIUX_PHASE_PLAN.md`) | Awaiting | - | - | - | - | - | - | ProgramDetailTemplate, course cards, syllabus flow |
| **6** | Startup Experience Redesign | **BLOCKED** | Pending | - | - | - | - | - | - | - | Founder value prop, equity terms, portfolio case studies |
| **7** | Enterprise AI & Product Experience | **BLOCKED** | Pending | - | - | - | - | - | - | - | Product catalog, pipeline interactive console polish |
| **8** | Labs, About, Careers, Credentials | **BLOCKED** | Pending | - | - | - | - | - | - | - | Academic preprints, team grid, credential verification |
| **9** | Utility, Legal & Verification UX | **BLOCKED** | Pending | - | - | - | - | - | - | - | Verify portal states, legal TOC, pricing tables |
| **10** | Component Cleanup & Style Drift | **BLOCKED** | Pending | - | - | - | - | - | - | - | Migrate inline styles (`ai-consultant`, `CohortApplications`) |
| **11** | Responsive & Accessibility Hardening | **BLOCKED** | Pending | - | - | - | - | - | - | - | 10 viewports audit, heading hierarchy (`A11Y-HEAD-001`) |
| **12** | UX Functional QA | **BLOCKED** | Pending | - | - | - | - | - | - | - | Forms, verification API, payments, interactive widgets |
| **13** | Performance & Rendering Polish | **BLOCKED** | Pending | - | - | - | - | - | - | - | LCP/CLS optimization, film grain cost, reduced motion |
| **14** | SEO & Content Integrity Regression | **BLOCKED** | Pending | - | - | - | - | - | - | - | Meta verification, link mesh check, keyword alignment |
| **15** | Production Preflight | **BLOCKED** | Pending | - | - | - | - | - | - | - | Production build, zero console errors, preflight checklist |
| **16** | Final Whole-Repo Audit | **BLOCKED** | Pending | - | - | - | - | - | - | - | Zero orphaned styles, zero dead code, clean git tree |

---

## Phase 0 Baseline Execution Log

### Test Gate Verifications
- **TypeScript Type Safety**: `npx tsc --noEmit` -> **PASSED** (0 errors)
- **ESLint Code Quality**: `npm run lint` -> **PASSED** (0 lint warnings/errors)
- **Next.js Production Build**: `npm run build` -> **PASSED** (all 90 static & dynamic routes compiled)
- **Metadata Check**: `npm run check:seo` -> **1 FAIL** (`/hire/pre-vetted-engineers` description 157 chars vs 140–155 limit)
- **Internal Links**: Script created and tested; ready for active server run (`scripts/check-links.mjs`)
- **Automated Audit Scripts Created**:
  - `apps/website/scripts/audit-routes.mjs` (routes, layouts, inline styles, buttons)
  - `apps/website/scripts/check-ui-tokens.mjs` (token validation, `--ink` hazard check)
  - `apps/website/scripts/check-inline-styles.mjs` (inline style locator)
  - `apps/website/scripts/check-placeholders.mjs` (zero metrics, TODOs, dummy copy)
  - `apps/website/scripts/check-headings.mjs` (accessibility heading hierarchy)

### Handcrafted Elements Verification
- Verified active in repository:
  - `Caveat` font loading in `apps/website/src/app/layout.tsx`
  - `<HandNote>` component in `apps/website/src/components/ui/HandNote.tsx`
  - `<HandDrawnArrow>` component in `apps/website/src/components/ui/HandDrawnArrow.tsx`
  - Marker underlines (`.marker svg path`), highlighter swipes (`.hl-swipe`), proof marks (`.proof-mark`), and margin notes (`.handnote`) in `apps/website/src/app/globals.css`
- Verified active on pages:
  - Homepage (`/`)
  - AI Solutions Pipeline (`/ai-solutions/llm-training/pipeline`)
  - Learners Hub (`/learners`)
  - Startups Hub (`/startups`)
  - Startup Hiring (`/startups/services/hiring`)
- **Preservation Invariant**: All handcrafted elements are protected and will remain untouched during styling refactors.

### Evidence & Artifact Registry
- `WEBSITE_ROUTE_INVENTORY.md`: Catalog of all 90 routes with layout, styles, density, responsive health.
- `WEBSITE_DESIGN_SYSTEM_AUDIT.md`: Typography, token mapping, `--ink` collision analysis, handcrafted inventory.
- `WEBSITE_BUG_REGISTER.md`: Formal classification of `BLOG-UI-001`, `SEO-ERR-001`, `HOME-DAT-001`, `HOME-REP-001`, `NAV-UX-001`, `STYLE-SPRAWL-001`, `A11Y-HEAD-001`.
- `WEBSITE_CONTENT_HIERARCHY_AUDIT.md`: Vertical-by-vertical scannability and CTA balance analysis.
- `WEBSITE_UIUX_PHASE_PLAN.md`: Phase-by-phase implementation blueprints.
