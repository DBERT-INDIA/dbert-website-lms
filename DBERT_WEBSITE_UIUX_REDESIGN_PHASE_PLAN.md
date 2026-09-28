# DBERT Website UI/UX Redesign & Page-System Remediation Plan
## Target
- Production website: `https://dbert.online`
- Repository: `https://github.com/DBERT-INDIA/dbert-website-lms`
- Scope: `apps/website/**`
- Objective: redesign the public website UI/UX without breaking working business flows, SEO, forms, payments, verification, or links.

> This is an execution plan for a local AI coding agent. The agent MUST work locally first, obtain approval phase-by-phase, test the phase against the whole website/repository, debug all regressions, commit/push only after the phase passes, and only then prepare the next phase.

---

# 1. Non-Negotiable Operating Workflow

For **every phase**:

1. READ current repository state.
2. Inspect all relevant routes/components/styles before editing.
3. Write a detailed phase plan to `WEBSITE_UIUX_PHASE_PLAN.md`.
4. STOP.
5. Wait for explicit approval.
6. Implement locally.
7. Run phase-specific tests.
8. Run whole-site regression tests.
9. Debug until all gates pass.
10. Inspect the resulting UI at desktop/tablet/mobile breakpoints.
11. Verify links, forms, API calls, navigation, SEO, accessibility and content integrity.
12. Commit with a focused commit message.
13. Push to GitHub.
14. Record commit SHA, tests, screenshots/evidence and remaining risks in `WEBSITE_UIUX_PROGRESS.md`.
15. Only then prepare the next phase and STOP for approval.

Never infer approval from silence.

Required checkpoint wording:
`PHASE PLAN READY: Phase N — <name>`
`Awaiting approval to implement Phase N.`

Never:
- edit production directly,
- replace working routes with placeholders,
- delete pages merely to simplify navigation,
- silently change commercial claims/pricing,
- silently change legal/privacy/refund content,
- remove analytics/SEO without replacement,
- break `internship.dbert.online` links,
- change payment/verification behavior while doing a visual redesign,
- hide content only because it looks crowded,
- mark a UI issue fixed without checking responsive states,
- claim a route works based only on source inspection.

---

# 2. Current Repository / Product Map

`apps/website` is a Next.js public website with a shared layout, global CSS/design tokens, reusable UI components, page-specific CSS modules, MDX/blog infrastructure and multiple business verticals.

Current route families discovered:

## Main
- `/`

## Startups
- `/startups`
- `/startups/register`
- `/startups/services`
- `/startups/services/technical`
- `/startups/services/hiring`
- `/startups/services/legal`
- `/startups/services/infrastructure`
- `/startups/services/funding`
- `/startups/services/equity`
- `/startups/services/equity/term-sheets`
- `/startups/investor-network`
- `/startups/portfolio`
- `/startups/portfolio/alkame`
- `/startups/portfolio/cognitive-solutions`
- `/startups/portfolio/digital-blaize`
- `/startups/portfolio/gayatri-ai`

## Enterprise AI
- `/ai-solutions`
- `/ai-solutions/products`
- `/ai-solutions/products/dbert-chat`
- `/ai-solutions/products/document-ai`
- `/ai-solutions/products/certificate-verification-api`
- `/ai-solutions/products/hiring-automation-suite`
- `/ai-solutions/products/intern-management-system`
- `/ai-solutions/consultation`
- `/ai-solutions/llm-training`
- `/ai-solutions/llm-training/pipeline`
- `/ai-solutions/llm-training/dbert-ai`
- `/ai-solutions/llm-training/private-hosting`
- `/ai-consultant`

## Learners
- `/learners`
- `/learners/launchpad`
- `/learners/accelerate`
- `/learners/fellowship`
- `/learners/interview-prep`
- `/learners/jobs`
- `/learners/courses`
- `/learners/courses/ai-agent-development`
- `/learners/courses/data-analytics`
- `/learners/courses/full-stack-development`
- `/learners/courses/generative-ai`
- `/learners/courses/machine-learning`
- `/learners/courses/python-automation`

## Labs
- `/labs`
- `/labs/collaborate`
- `/labs/opensource`
- `/labs/publications`
- `/labs/research`

## About
- `/about`
- `/about/team`
- `/about/careers`
- `/about/contact`
- `/about/credentials`

## Blog
- `/blog`
- `/blog/[slug]`

## Utility / Trust
- `/pricing`
- `/verify`
- `/privacy`
- `/terms`
- `/refund`

Also account for any deeper routes discovered by the agent from the filesystem, sitemap, navigation config, generated content or dynamic route data. The above is a baseline, not permission to ignore other routes.

---

# 3. Audit Findings From Current Code + Live Website

## 3.1 The biggest UI problem is not one isolated bug: there are multiple visual systems

The website currently contains:
- global v2 design tokens in `globals.css`,
- reusable utility classes,
- page-specific CSS modules,
- some legacy-looking utility conventions,
- multiple long-page shells,
- special blog CSS,
- special learner CSS,
- startup CSS,
- AI solutions CSS,
- component-level inline style objects.

This creates visual drift.

Examples visible in the code:
- `globals.css` defines the global dark “Studio Console” system.
- `page.module.css`, `learners.module.css`, `startups.module.css`, `ai-solutions.module.css`, `about.module.css`, `blog.module.css`, etc. each add local presentation rules.
- Several pages still use inline styles for grid, typography, spacing, colors and layout.
- Some components mix semantic classes with arbitrary utility classes.

This needs a real design-system cleanup, not only individual visual patches.

## 3.2 Live homepage has content integrity signals that look unfinished

The live homepage currently exposes:
- `0 ventures incubated`
- `0 SaaS products live`
- `0+ fellows trained`
- `~0 mo faster to market`

These are visually prominent proof metrics and read as broken/uninitialized counters.

The page simultaneously presents a “live feed” and operational claims. This makes zero-valued counters especially disruptive to credibility.

The local agent must determine whether these values are:
- actual data,
- placeholders,
- intentionally hidden until data exists,
- or stale fallback values.

Do not simply change the numbers for appearance. Fix the data path or render an intentional empty-state.

## 3.3 Homepage live content repeats the status/trust strip

The live homepage contains the sequence:
- studio status/live feed,
- listening/uptime,
- proof stats,
- a long repeated “est. Delhi...chai...” trust line,
- then choose-your-path.

The text extraction shows duplicated repeated content in the same region. This should be examined in the rendered DOM and source for accidental duplication or an animation/content-clone effect.

The redesign must preserve the useful “studio console” personality but remove repetition that feels like a rendering artifact.

## 3.4 Navigation is ambitious but overloaded

`nav.config.json` currently contains:
- For Startups mega-menu,
- Products dropdown,
- Enterprise AI Consulting mega-menu,
- For Learners mega-menu,
- DBERT Labs,
- About,
- CTA.

The mega menu contains many destinations. This is structurally useful but risks:
- information overload,
- weak priority,
- long labels,
- competing CTAs,
- difficulty understanding the main business model quickly.

The agent should redesign the information architecture visually before deleting any route.

The mobile drawer implementation itself is thoughtful:
- focus management,
- Escape,
- focus return,
- tab trapping,
- scroll lock,
- responsive breakpoint.

Do not regress these behaviors during visual redesign.

## 3.5 Blog page has a concrete color/contrast bug

`apps/website/src/app/blog/blog.module.css` contains obvious conflicting values:

`.postTitle { color: var(--ink); }`

while the global design system uses:
`--ink: #06090F`

The article/post shell is dark:
`.postBody { background: var(--card); }`

Similarly:
- `.mdxContent blockquote { color: var(--ink); }`
- `.mdxContent th { color: var(--ink); }`
- `.authorName { color: var(--ink); }`

On dark surfaces this can make text extremely low contrast or effectively disappear.

This matches the observed “blog page fonts and background colour are same” problem.

This is a real UI bug, not merely a design preference.

The local agent must audit every blog color against its actual background, not merely replace one selector.

## 3.6 Blog has mixed “dark console” and “document” semantics

Blog code tries to be:
- technical research archive,
- editorial article,
- card grid,
- dark IDE-like system.

The typography and surface colors are not consistently separated.

Needed structure:
- blog index: editorial archive surface,
- article hero: strong title + metadata,
- article body: high-readability reading column,
- code: separate code surface,
- tables: high-contrast table surface,
- quotes: intentional callout,
- tags: secondary,
- CTA: visually separate from content.

Do not make long-form reading look like a dashboard.

## 3.7 Several pages use inconsistent typography hierarchy

Examples:
- some pages use `page-title`, others `page-title-sm`, others plain `h1`,
- some h2/h3 are in display font,
- some section headings explicitly use `font-mono`,
- some content is styled via `card-title`,
- some sections use `text-2xl font-mono font-bold text-white`,
- some use `section-title`,
- some use `subsection-title`.

A design system should define:
- display/hero heading,
- section heading,
- subsection heading,
- card heading,
- body,
- metadata,
- overline,
- label,
- CTA,
- legal/readability text.

Avoid arbitrary heading classes per page unless there is a genuine semantic need.

## 3.8 Content density is high in business pages

Several long pages are effectively “everything pages”, especially:
- `/startups`
- `/startups/services`
- `/ai-solutions`
- `/ai-solutions/products`
- `/ai-solutions/consultation`
- `/ai-solutions/llm-training`
- `/learners`
- `/learners/fellowship`
- `/pricing`

The content is not necessarily wrong. The problem is information hierarchy.

Users need:
1. what this is,
2. who it is for,
3. primary outcome,
4. proof,
5. how it works,
6. offer/commercial action,
7. supporting details,
8. FAQ/legal.

The redesign should reorder sections to support scanning.

## 3.9 Some pages are visually inconsistent even when technically correct

Examples discovered in code:
- `ai-consultant/page.tsx` uses many inline `style={{...}}` blocks.
- `BlogClientView.tsx` uses inline search-bar styles and inline button cursor styles.
- `/startups/services`, `/ai-solutions/products`, etc. use combinations of global utility classes, CSS module classes and local layout patterns.
- Several pages use different button classes and text sizing conventions.

This leads to “same website, different designer” behavior.

## 3.10 Long pages need deliberate surface rhythm

Current global CSS already introduces:
- `page-hero`,
- `page-band`,
- `page-cta`,
- `glow-wrapper`,
- alternating surfaces,
- cards.

But the rules have grown into a compatibility/migration layer rather than a clean system.

The redesign should establish a limited set of section surfaces:
- base,
- elevated,
- tinted,
- focus,
- CTA,
- legal/document.

Then migrate pages to those surfaces.

## 3.11 The global atmosphere can become visually noisy

`globals.css` adds:
- fixed blueprint grid,
- animated film grain,
- glow backgrounds,
- hover elevation,
- hand-drawn accents,
- gradient effects.

These are useful as brand language, but everywhere they compete with content.

The agent must audit:
- where effects add hierarchy,
- where they add noise,
- mobile performance,
- `prefers-reduced-motion`,
- readability over backgrounds.

## 3.12 Accessibility must be treated as part of UX

Existing nav code contains good accessibility behavior. The redesign must preserve it.

Audit all routes for:
- keyboard focus visibility,
- heading order,
- form labels,
- button/link semantics,
- target sizes,
- color contrast,
- reduced motion,
- alt text,
- dialog behavior,
- error states,
- loading states.

---

# 4. What Currently Works and Must Be Preserved

The redesign is not a rewrite for its own sake.

Preserve proven patterns where tests confirm them:
- Next.js route structure,
- shared app layout,
- responsive navigation drawer,
- keyboard/ESC behavior,
- reusable FAQ accordion,
- reusable program detail template,
- reusable case-study template,
- shared forms,
- certificate verification flow,
- payment/order API flow,
- external internship portal links,
- SEO metadata generation,
- sitemap/robots,
- blog search/tag filtering,
- existing server/client boundaries,
- validated content data sources.

Before changing a working component, write a regression test or scripted behavior check.

---

# 5. Severity Classification

Every finding discovered by the agent must be classified:

### P0 — Blocking
Page unusable, content unreadable, primary CTA impossible, broken navigation, JS runtime crash, payment/verification broken.

### P1 — Real bug
Incorrect route, broken responsive layout, broken form state, inaccessible control, unreadable text, duplicate/hidden content, incorrect active state.

### P2 — Major UX flaw
Poor hierarchy, confusing navigation, excessive density, inconsistent spacing, weak CTA placement, unclear audience.

### P3 — Visual inconsistency
Typography drift, card variation, spacing mismatch, inconsistent button styles, surface mismatch.

### P4 — Polish
Micro-interactions, animation timing, shadow detail, border tone, small alignment issues.

Do not call ordinary subjective taste a bug. Record it as design debt/opportunity.

---

# 6. Required Audit Artifacts

Before Phase 1 implementation, create:

- `WEBSITE_UIUX_AUDIT.md`
- `WEBSITE_ROUTE_INVENTORY.md`
- `WEBSITE_DESIGN_SYSTEM_AUDIT.md`
- `WEBSITE_BUG_REGISTER.md`
- `WEBSITE_CONTENT_HIERARCHY_AUDIT.md`
- `WEBSITE_UIUX_PROGRESS.md`

Each route must have a row with:
- URL
- page purpose
- audience
- layout/template used
- CSS module/global styles
- hero type
- CTA
- content density
- responsive behavior
- known bug
- UX concern
- design priority
- test status
- screenshot/evidence path

---

# 7. Phase Plan

## Phase 0 — Baseline, Route Inventory, Visual Evidence
### Goal
Create a complete baseline before any redesign.

### Tasks
- enumerate every route from source, sitemap, navigation config and filesystem,
- identify dynamic routes,
- map each route to its page/template/component,
- run local build,
- run lint/type checks,
- start site locally,
- capture screenshots at:
  - 1440x900
  - 1280x800
  - 1024x768
  - 768x1024
  - 390x844
  - 360x800
- inspect homepage, blog, representative startup, enterprise, learner, legal and verification pages,
- run automated link inventory,
- record runtime console errors.

### Exit gate
Complete route inventory + baseline screenshots + no undocumented runtime/build failures.

---

## Phase 1 — Design System Consolidation
### Goal
Create a single visual language.

### Define
- color tokens,
- text colors by surface,
- surface hierarchy,
- spacing scale,
- container widths,
- typography scale,
- border radii,
- shadows,
- button variants,
- link styles,
- badge/tag styles,
- section spacing,
- responsive breakpoints,
- focus states,
- reduced motion.

### Special requirement
Define semantic tokens like:
- `--surface-base`
- `--surface-raised`
- `--surface-card`
- `--surface-strong`
- `--text-primary`
- `--text-secondary`
- `--text-muted`
- `--text-on-accent`
- `--border-subtle`
- `--border-strong`

Do not use `--ink` as a generic text color.

### Exit gate
A small reference page containing every design-system primitive renders correctly in light/dark surface contexts used by the website.

---

## Phase 2 — Global Shell: Header, Navigation, Footer
### Goal
Make the whole website feel like one product.

### Tasks
- redesign header hierarchy,
- simplify primary nav presentation without removing route coverage,
- visually prioritize one primary CTA,
- refine mega menus,
- preserve keyboard and screen-reader behavior,
- improve mobile drawer visual hierarchy,
- make active route discoverable,
- redesign footer information architecture,
- make external portal links clearly distinguishable where useful.

### Acceptance
A user can identify:
- DBERT,
- startups path,
- enterprise/product path,
- learner path,
- labs/about,
- primary action
within seconds.

No regression in keyboard/mobile navigation.

---

## Phase 3 — Homepage Recomposition
### Goal
Turn homepage into the clearest explanation of the DBERT model.

### Recommended information hierarchy
1. One-sentence positioning
2. Three audiences / three business doors
3. Proof/operating model
4. Products
5. Learner ladder
6. Studio/case proof
7. About / founder statement
8. Primary CTA

### Fix
- zero/uninitialized metrics,
- duplicate feed/trust content,
- overly dense proof blocks,
- CTA competition,
- mobile hero crowding.

### Acceptance
A first-time visitor can answer:
“What is DBERT, who is it for, and what should I do next?” without reading the whole page.

---

## Phase 4 — Blog & Editorial Reading Experience
### Goal
Fix the concrete contrast bug and turn the blog into a high-quality technical publication surface.

### Fix immediately
Audit all selectors in:
- `blog.module.css`
- blog component styles
- MDX styles

for dark-surface vs `var(--ink)` collisions.

### Required article structure
- editorial hero,
- metadata,
- title,
- summary,
- tags,
- reading column,
- headings,
- lists,
- code,
- blockquotes,
- tables,
- images,
- author,
- related content,
- next CTA.

### UX
- sticky or contextual article navigation for long posts,
- search/filter state should remain understandable,
- empty result state,
- keyboard behavior,
- mobile tag overflow handling,
- readable line length.

### Acceptance
No low-contrast text in the complete blog route family.

---

## Phase 5 — Learner Experience Redesign
### Goal
Make learner pages conversion-oriented and easy to compare.

### Routes
- `/learners`
- `/learners/launchpad`
- `/learners/accelerate`
- `/learners/fellowship`
- `/learners/courses`
- course detail routes,
- `/learners/interview-prep`
- `/learners/jobs`

### Define a common program page pattern
Hero →
who it is for →
what you build →
curriculum →
proof →
timeline →
price/outcome →
FAQ →
CTA.

Avoid pages that require users to parse large walls of text before understanding the offer.

---

## Phase 6 — Startup Experience Redesign
### Goal
Make startup pages easier for founders to navigate and understand.

### Routes
- `/startups`
- services
- portfolio
- investor network
- registration
- case studies.

### Fix
- dense tables,
- too many sections without clear priority,
- overlapping commercial messages,
- unclear “who is this for?” placement,
- case-study proof hierarchy.

### Acceptance
Founder can reach:
services → proof → process → application
without hunting through the page.

---

## Phase 7 — Enterprise AI / Product Experience Redesign
### Routes
- `/ai-solutions`
- product catalog
- product details
- consultation
- LLM training
- AI consultant.

### Goal
Separate:
- capability,
- product,
- consulting,
- implementation,
- technical details,
- CTA.

Avoid presenting all enterprise content as one giant technical document.

### Add
clear product comparison patterns,
use-case blocks,
security/architecture proof,
implementation process,
CTA.

---

## Phase 8 — Labs, About, Careers, Contact, Credentials
### Goal
Improve trust and institutional storytelling.

### Routes
- `/labs/*`
- `/about/*`

### Focus
- people-first content,
- credentials separated from marketing,
- contact form clarity,
- careers route hierarchy,
- research vs commercial content separation.

---

## Phase 9 — Utility / Legal / Verification UX
### Routes
- `/pricing`
- `/verify`
- `/privacy`
- `/terms`
- `/refund`

### Goal
Give utility and legal pages a consistent, trustworthy system.

### Verification
- strong empty state,
- loading state,
- valid result state,
- invalid state,
- network error state,
- accessible form controls.

Legal pages:
- reading width,
- sticky mini-TOC if long enough,
- consistent revision metadata,
- high legibility.

---

## Phase 10 — Component Cleanup & Remove Style Drift
### Goal
Remove the root causes of future visual drift.

Refactor repeated inline styles from:
- `ai-consultant/page.tsx`
- `BlogClientView.tsx`
- startup/product pages
- other discovered pages.

Promote only reusable semantics into shared components.

Avoid building a giant utility CSS replacement for Tailwind.

---

## Phase 11 — Responsive + Accessibility Hardening
### Required viewport matrix
- 360
- 375
- 390
- 414
- 768
- 820
- 1024
- 1280
- 1440
- 1920

Test:
- no horizontal scrolling,
- no clipped headings,
- no overlapping buttons,
- no inaccessible dropdowns,
- no off-screen dialogs,
- readable form errors,
- touch targets,
- focus visibility,
- reduced motion.

---

## Phase 12 — UX Functional QA
Audit every interaction:
- links,
- dropdowns,
- mobile menu,
- search,
- filters,
- accordions,
- forms,
- API-backed verification,
- payment initiation,
- checkout redirects,
- external portal navigation,
- scroll-to-anchor actions,
- back-to-top,
- WhatsApp CTA,
- image behavior.

Every failure must be reproduced, classified and fixed.

---

## Phase 13 — Performance / Rendering Polish
Check:
- LCP,
- CLS,
- JS bundle impact,
- font loading,
- image sizing,
- animated grain cost,
- backdrop-filter usage,
- large SVGs,
- unnecessary client components.

Keep brand motion but respect:
`prefers-reduced-motion: reduce`.

---

## Phase 14 — SEO + Content Integrity Regression
Verify:
- title,
- description,
- canonical,
- OG image,
- structured data,
- sitemap,
- robots,
- heading order,
- internal links,
- no accidental `noindex`,
- no broken canonical routes,
- no duplicated visible content.

Do not alter factual claims merely to improve visual conversion.

---

## Phase 15 — Production Preflight
Before deployment:
- production build,
- environment validation,
- route smoke test,
- static asset test,
- API endpoint smoke test,
- payment flow smoke test in safe test mode if available,
- certificate verification,
- external internship portal links,
- no console errors,
- no failed network requests expected for normal page loads.

Create:
`WEBSITE_UIUX_PRODUCTION_PREFLIGHT.md`

---

## Phase 16 — Final Whole-Repo Audit
Search for:
- old design tokens,
- inline styles that should have been removed,
- duplicated CSS,
- contradictory color rules,
- invalid links,
- orphan routes,
- dead components,
- placeholder numbers,
- TODO/FIXME related to UI,
- console logging,
- accidental debug overlays,
- inconsistent CTA labels,
- inconsistent page metadata.

Run complete build + test + route scan again.

---

# 8. Blog-Specific Bug Register Entry That Must Exist

Create a bug entry similar to:

ID: BLOG-UI-001
Severity: P1
Area: `/blog/[slug]`
Type: readability / contrast
Observed:
- `postTitle`, `blockquote`, `th`, `authorName` use `var(--ink)` on dark surfaces.
Expected:
- text remains readable against its actual surface.
Root cause:
- semantic surface/text token mismatch.
Fix:
- introduce surface-aware text tokens and remove semantic misuse of `--ink`.
Regression:
- test article title, quote, table header, author name on dark theme.
Status:
- open until screenshot + contrast verification passes.

The agent must expand this into all affected selectors.

---

# 9. Design Rules For The New Website

## Typography
Use a deliberate hierarchy:
- Hero: display face
- Section title: display face
- Body: readable sans
- Technical metadata: mono
- Handwritten accent: optional and sparse

Do not use mono for large marketing headings unless the page is intentionally technical.

## Color
Dark theme remains available as the DBERT identity, but every text color must be selected for the surface it sits on.

No arbitrary `#FFFFFF`, `#05070C`, `var(--ink)` etc. when a semantic token exists.

## Spacing
Use the shared spacing scale.

No random one-off margins unless documented.

## Cards
Use fewer, stronger card types:
- feature,
- product,
- program,
- proof,
- process,
- testimonial/case,
- CTA.

## Sections
Every long page should visibly answer:
“Why am I seeing this section now?”

## Buttons
Keep:
- primary,
- secondary/outline,
- tertiary/text.

Do not put two competing primary CTAs beside each other.

## Images
Use images as proof or storytelling, not decoration everywhere.

## Motion
Use motion to reinforce hierarchy, not keep everything moving.

---

# 10. Automated Checks To Add

Create scripts where practical:

`apps/website/scripts/audit-routes.mjs`
`apps/website/scripts/check-links.mjs`
`apps/website/scripts/check-ui-tokens.mjs`
`apps/website/scripts/check-inline-styles.mjs`
`apps/website/scripts/check-headings.mjs`
`apps/website/scripts/check-placeholders.mjs`

Useful scans:
- all route files,
- all `href`,
- all `Link href`,
- all `style={{`,
- all hex color literals,
- all uses of `var(--ink)` in text contexts,
- suspicious zero metrics,
- `TODO`,
- `FIXME`,
- duplicate content strings.

Do not automatically rewrite code using regex without AST awareness or a tightly scoped migration.

---

# 11. Browser / Visual QA Rules

For every page touched:
1. load fresh,
2. hard reload,
3. scroll top-to-bottom,
4. interact with every visible control,
5. test keyboard,
6. test mobile width,
7. inspect console,
8. inspect network failures,
9. screenshot before/after,
10. compare visual hierarchy.

For long pages additionally:
- check section transition,
- sticky header,
- anchor scrolling,
- footer reachability,
- no layout jumps after fonts/images load.

---

# 12. Definition Of Done

A phase is complete only when:

- code changed locally,
- phase tests pass,
- full repository tests pass,
- route smoke test passes,
- touched pages render correctly at desktop/mobile,
- no new console errors,
- no new broken links,
- accessibility checks pass for touched components,
- design-system rules are documented,
- `WEBSITE_UIUX_PROGRESS.md` is updated,
- commit exists,
- commit pushed to GitHub,
- remote state verified,
- next phase plan is prepared,
- agent stops and asks for approval.

---

# 13. Progress Tracker Template

| Phase | Status | Local Plan | Approved | Implemented | Phase Tests | Full Regression | Visual QA | Commit | Pushed | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | NOT STARTED | | | | | | | | | |
| 1 | BLOCKED | | | | | | | | | |
| 2 | BLOCKED | | | | | | | | | |
| 3 | BLOCKED | | | | | | | | | |
| 4 | BLOCKED | | | | | | | | | |
| 5 | BLOCKED | | | | | | | | | |
| 6 | BLOCKED | | | | | | | | | |
| 7 | BLOCKED | | | | | | | | | |
| 8 | BLOCKED | | | | | | | | | |
| 9 | BLOCKED | | | | | | | | | |
| 10 | BLOCKED | | | | | | | | | |
| 11 | BLOCKED | | | | | | | | | |
| 12 | BLOCKED | | | | | | | | | |
| 13 | BLOCKED | | | | | | | | | |
| 14 | BLOCKED | | | | | | | | | |
| 15 | BLOCKED | | | | | | | | | |
| 16 | BLOCKED | | | | | | | | | |

---

# 14. First Action Required From The Local AI Agent

The first response from the agent must contain **only**:

1. repository/branch/worktree assessment,
2. discovered complete route inventory,
3. Phase 0 plan,
4. baseline test commands,
5. visual QA strategy,
6. initial bug/UX findings,
7. exact files it proposes to inspect/change,
8. `PHASE PLAN READY: Phase 0 — Baseline, Route Inventory, Visual Evidence`
9. `Awaiting approval to implement Phase 0.`

It must NOT edit application code before approval.

---

# 15. Important Existing Evidence To Start From

Current live site is `https://dbert.online`.

Current live homepage exposes a strong “venture studio” positioning and several audience doors, but also currently shows zero-valued proof metrics and a duplicated-looking operational/trust strip. These need source-level verification before any content change.

Current live blog is `/blog` and is a technical research archive. The source CSS contains a concrete text/surface mismatch that can make dark-on-dark content unreadable.

Current global styling uses a dark “Studio Console” visual system with blueprint grid, grain, glows, blue accent, amber signal color and multiple shared utilities. The next redesign should retain the recognizable DBERT identity while reducing style drift and information overload.

---

# 16. Agent Safety Rule

When source inspection reveals a visual problem that might actually be caused by:
- data,
- API response,
- font loading,
- image sizing,
- hydration,
- runtime CSS,
- route mismatch,
- server-side rendering,
- browser-specific behavior,

the agent must prove the cause before changing the presentation.

Classify:
`REAL BUG`
vs
`UX DESIGN ISSUE`
vs
`DESIGN DEBT`
vs
`CONTENT ISSUE`
vs
`DATA/INTEGRATION ISSUE`

Never disguise one category as another.
