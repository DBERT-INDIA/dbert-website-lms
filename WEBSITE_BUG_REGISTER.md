# DBERT Website Bug Register (Phase 0 Baseline)

## Classification Matrix
- **P0 (Blocking)**: Page unusable, content unreadable, primary CTA broken, JS runtime crash, payment/verification failure.
- **P1 (Real Bug)**: Broken responsive layout, inaccessible control, unreadable text, broken form state, failed CI gate.
- **P2 (Major UX Flaw)**: Poor information hierarchy, confusing navigation, excessive density, uninitialized proof metrics.
- **P3 (Visual Inconsistency)**: Typography drift, card variation, spacing mismatch, inline styling sprawl.
- **P4 (Polish)**: Micro-interaction timing, shadow details, border fine-tuning.

---

## Active Bug Register

### 1. [P1] BLOG-UI-001: Dark-on-Dark Text Contrast Failure Across Blog Posts
- **Area**: `/blog/[slug]` (All 5 MDX articles: `ai-agent-developer-salary-2026`, `equity-for-services`, `non-tech-to-ai-career`, `paid-ai-internship-india-guide-2026`, `rag-pipeline-tutorial-from-scratch`)
- **Type**: Readability / Contrast Failure (WCAG AAA/AA violation)
- **Observed**:
  - In `apps/website/src/app/blog/blog.module.css`:
    - Line 36: `.postTitle { color: var(--ink); }`
    - Line 132: `.mdxContent pre { color: var(--ink); }`
    - Line 155: `.mdxContent blockquote { color: var(--ink); }`
    - Line 169: `.mdxContent th { color: var(--ink); }`
    - Line 230: `.authorName { color: var(--ink); }`
  - Global `--ink` is `#06090F`. The post shell `.postBody` is `--card` (`#0F1523`) and `.mdxContent blockquote/th/pre` sits on `--raise` (`#0B101A`).
  - Text renders as `#06090F` on `#0F1523` / `#0B101A`, creating a near-invisible contrast ratio of **1.08:1**.
- **Root Cause**: Semantic misuse of `--ink` (intended as background surface token) as a foreground font color.
- **Planned Fix**:
  - Replace `.postTitle` color with `var(--text)` (`#EEF2FA`).
  - Replace `.mdxContent pre` color with `var(--text)`.
  - Replace `.mdxContent blockquote` color with `var(--text)` / `#D1D9E6`.
  - Replace `.mdxContent th` color with `var(--text)`.
  - Replace `.authorName` color with `var(--text)`.
- **Target Phase**: Phase 4 (Blog & Editorial Experience).
- **Status**: OPEN.

---

### 2. [P1] SEO-ERR-001: Meta Description Length Mismatch in `/hire/pre-vetted-engineers`
- **Area**: `/hire/pre-vetted-engineers` (Route SEO metadata)
- **Type**: CI Test Gate Failure
- **Observed**:
  - Running `npm run check:seo` outputs:
    `✗ /hire/pre-vetted-engineers: description 157 chars (want 140–155)`
  - Current description string in `src/data/seo.config.ts`:
    `"Hire pre-vetted AI, Full Stack, and Data engineers evaluated through live code reviews and system architecture benchmarks. Onboard proven talent in 48 hours."` (157 characters).
- **Root Cause**: Description string is 2 characters over the strict 155-character upper limit enforced by `scripts/check-seo.mjs`.
- **Planned Fix**:
  - Shorten string to 148–152 characters while retaining the primary keyword `"hire pre-vetted AI engineers India"`.
  - Example candidate: `"Hire pre-vetted AI, Full Stack, and Data engineers evaluated through live code reviews and system benchmarks. Onboard proven tech talent in 48 hours."` (151 chars).
- **Status**: RESOLVED (Fixed in Phase 1: description shortened to 151 chars; 100% passes `npm run check:seo`).

---

### 3. [P2] HOME-DAT-001: Zero-Valued Metric Counters on Homepage SSR Initial Render
- **Area**: `/` (Homepage Proof Band)
- **Type**: Data / Hydration UX Flaw
- **Observed**:
  - Live homepage renders initial stat values:
    - `0 ventures incubated`
    - `0 SaaS products live`
    - `0+ fellows trained`
    - `~0 mo faster to market`
  - In web crawlers, search indexing scrapers, and fast scroll passes, the numbers read as zero.
- **Root Cause**:
  - `src/components/ui/CountUp.tsx` Line 81 renders hardcoded `{prefix}0{suffix}` in SSR markup:
    ```tsx
    return <Tag ref={ref} className={className}>{prefix}0{suffix}</Tag>;
    ```
  - The real figures (`end={4}`, `end={5}`, `end={120}`, `end={6}`) are only written client-side after `IntersectionObserver` triggers at `threshold: 0.5`.
- **Planned Fix**:
  - Implement progressive enhancement: SSR markup renders the real approved target figure (`end`).
  - When JS runs and enters viewport, client animation starts from 0 smoothly up to `end`. If JS fails, is disabled, or is scraped, the authentic numbers are visible immediately.
- **Status**: RESOLVED (Fixed in Phase 3: CountUp renders approved target end value in SSR markup with progressive client count-up enhancement).

---

### 4. [P2] HOME-REP-001: Visual Duplication in Fact Ticker Strip
- **Area**: `/` (Homepage Marquee Band)
- **Type**: Visual Rhythm / Cognitive Repetition
- **Observed**:
  - The live homepage repeats the sequence `'est. Delhi, India'`, `'chai consumed this sprint: 214 cups'`, `'every application gets a human reply'`, `'fellows write real production code, not todo apps'` in close proximity to the studio status console and proof numbers.
- **Root Cause**:
  - `src/components/ui/FactTicker.tsx` duplicates the facts array twice in the DOM for continuous CSS marquee animation loop. In text extractors and slow animation frames, the duplicate text reads like an accidental double-render.
- **Planned Fix**:
  - Refine FactTicker layout, ensure robust `aria-hidden="true"`, smooth the velocity, and visually demarcate the ticker as an ambient marquee bar distinct from core proof metrics.
- **Status**: RESOLVED (Fixed in Phase 3: applied edge gradient masks, refined velocity to 42s, and enforced ambient styling).

---

### 5. [P2] NAV-UX-001: High Information Density in Desktop Mega Menus
- **Area**: Primary Header Navigation (`apps/website/src/components/layout/MegaMenu.tsx`)
- **Type**: Information Architecture / Cognitive Load
- **Observed**:
  - The Startups, Products, and Learners mega menus present dense lists of 8–12 routes simultaneously, leading to scanning hesitation for first-time visitors.
- **Root Cause**: Direct flattening of route sitemaps into multi-column dropdowns without clear primary vs secondary visual grouping.
- **Planned Fix**:
  - Redesign mega-menu visual hierarchy: highlight the primary "Featured Route" per vertical with high-contrast card styling, group secondary routes under concise categorised headers, and retain full keyboard accessibility and mobile drawer parity without deleting any route.
- **Status**: RESOLVED (Fixed in Phase 2: integrated featured cards, category column dividers, active route tracking, and 4-column footer architecture).

---

### 6. [P3] STYLE-SPRAWL-001: Inline Style Proliferation in Key Pages
- **Area**: Multiple pages, notably `src/app/admin/cohort-applications/CohortApplicationsClient.tsx` (29), `src/app/hire/pre-vetted-engineers/page.tsx` (14), `src/app/ai-consultant/page.tsx` (12), `BlogClientView.tsx` (5).
- **Type**: Maintainability / Design System Drift
- **Observed**:
  - Hardcoded inline styles for borders, box-shadows, grid templates, and colors bypass global tokens and CSS modules.
- **Root Cause**: Rapid prototyping without extracting recurring components.
- **Planned Fix**:
  - Migrate static inline style objects into scoped CSS module classes or shared utility tokens during Phase 10 cleanup.
- **Target Phase**: Phase 10 (Component Cleanup & Style Drift Remediation).
- **Status**: OPEN.

---

### 7. [P3] A11Y-HEAD-001: Skipped Heading Levels in 35 Pages
- **Area**: 35 routed pages across Enterprise AI, Startups, and Cohorts
- **Type**: Accessibility / Semantic Structure
- **Observed**:
  - Headings jump from `h2 -> h4` or `h1 -> h3` without intermediate `h2`/`h3` tags (e.g. `src/app/ai-consultant/page.tsx: h1 -> h3`, `ai-solutions/consultation/page.tsx: h2 -> h4`).
- **Root Cause**: Developers used heading tags as font-size selectors rather than semantic document outlines.
- **Planned Fix**:
  - Normalize document heading order to strictly follow `h1 -> h2 -> h3 -> h4` sequentially, using CSS classes for sizing rather than skipping HTML tags.
- **Target Phase**: Phase 11 (Responsive & Accessibility Hardening).
- **Status**: OPEN.
