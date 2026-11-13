# DBERT Design System Audit & Token Architecture (Phase 0 Baseline)

## Executive Summary
The DBERT design system (v2.1 "Studio Console") provides a distinctive dark engineering-terminal aesthetic with technical typography and signature artisanal accents. However, organic growth across distinct business verticals has introduced visual drift, semantic token gaps (notably `--ink` misuse), and inline style fragmentation.

**Crucial Mandate**: As directed, **all handcrafted elements remain firmly in place** as protected signature brand assets.

---

## 1. Typography System & Font Architecture

| Token | Family | Fallback | Purpose / Usage | Source / Definition | Status |
|---|---|---|---|---|---|
| `--font-d` | `Bricolage Grotesque` | `sans-serif` | Display & Hero Headings (`h1`, `h2`, section titles) | `next/font/google` in `layout.tsx` | Active |
| `--font-b` | `Inter` | `sans-serif` | Primary Body Text, UI Labels, Buttons, Form Inputs | `next/font/google` in `layout.tsx` | Active |
| `--font-m` | `JetBrains Mono` | `monospace` | Technical Specs, Timestamps, System Badges, Code, Terminal Logs | `next/font/google` in `layout.tsx` | Active |
| `--font-h` | `Caveat` | `cursive` | **Handcrafted Margin Notes, Casual Proof Asides, Human Annotations** | `next/font/google` in `layout.tsx` | **Protected Handcrafted Element** |

### Heading Hierarchy Audit
- `h1`: `clamp(2.6rem, 5.6vw, 4.3rem)`, weight 700, letter-spacing `-0.02em`.
- `h2`: `clamp(1.9rem, 3.4vw, 2.7rem)`, weight 700, letter-spacing `-0.02em`.
- `h3`: `1.22rem`, line-height `1.3`.
- **Identified Discrepancies**:
  - Inconsistent heading classes across verticals: `.page-title` vs `.page-title-sm` vs unstyled `h1`.
  - Several marketing subheadings explicitly enforce `font-family: var(--font-m)` instead of using display/body hierarchy.
  - Heading level skipping (`h2 -> h4`) on 35 pages (documented for Phase 11 a11y hardening).

---

## 2. Handcrafted Signature UI Elements (Preservation Audit)

The DBERT website balances engineering precision with authentic human craftsmanship through a deliberate set of handcrafted elements. These elements prevent the site from appearing like a generic dark-mode template.

### Protected Handcrafted Element Inventory

| Element | Component / Selector | Visual Role | Implementation Details | Preservation Mandate |
|---|---|---|---|---|
| **Handwritten Margin Notes** | `<HandNote>`, `.handnote`, `.handnote.blue` | Casual engineer margin annotations and human asides | Uses `--font-h` (Caveat cursive), rotated `-2.5deg`, amber (`var(--signal)`) or blue ink (`#8FB2FF`), `aria-hidden="true"`. | **KEEP IN PLACE** — Core brand signature across Homepage, Pipeline, Learners, and Startups. |
| **Hand-Drawn Animated Arrow** | `<HandDrawnArrow>`, `.hand-arrow` | Human directional indicator pointing toward primary actions | SVG curved path with `stroke-dasharray` / `stroke-dashoffset` keyframe animation (`drawArrow`), amber stroke. | **KEEP IN PLACE** — Guides user gaze to key conversion triggers without robotic buttons. |
| **Marker Underline** | `.marker svg path` | Hand-drawn highlighter stroke underlining key phrases | Hand-drawn SVG vector path with self-drawing keyframe animation on page reveal. | **KEEP IN PLACE** — Highlights pivotal value propositions. |
| **Highlighter Swipe** | `.hl-swipe` | Analog marker swipe across critical metrics | Subtle angled linear gradient with rounded endpoints mimicking human highlighter pen. | **KEEP IN PLACE** — Used for authentic editorial emphasis. |
| **Audit Redline** | `.redline-del` | Handcrafted strikethrough for engineering audits | Coral/redline strike line (`--err`) through legacy assumptions. | **KEEP IN PLACE** — Reinforces technical code-audit positioning. |
| **Proof Mark Tags** | `.proof-mark`, `.proof-mark-signal` | Handcrafted verification badges | Monospace proof badge with emerald (`--ok`) or amber (`--signal`) glow borders. | **KEEP IN PLACE** — Validates engineering credibility. |
| **Atmospheric Film Grain** | `body::after` | Organic analog texture over flat digital backgrounds | 200px tiled SVG fractal noise filter animated with 6-step jitter. | **KEEP IN PLACE** — Preserves physical paper/console tactile feel. |
| **Blueprint Grid** | `body::before` | Engineering graph-paper background | 56px radial-masked grid lines fading toward lower viewport. | **KEEP IN PLACE** — Anchors studio workstation aesthetic. |

---

## 3. Color Token Mapping & Semantic Collision Audit

### Base Tokens in `globals.css`
- `--ink`: `#06090F` (Base page background, darkest surface)
- `--raise`: `#0B101A` (Level 1 elevation: secondary panels, toolbars)
- `--card`: `#0F1523` (Level 2 elevation: standard content cards)
- `--card-hi`: `#141C2E` (Level 3 elevation: hovered/focused cards)
- `--line`: `rgba(148, 163, 196, 0.12)` (Subtle border)
- `--line-strong`: `rgba(148, 163, 196, 0.22)` (Prominent border)
- `--accent`: `#5B8CFF` (Primary studio electric blue)
- `--accent-soft`: `rgba(91, 140, 255, 0.12)`
- `--signal`: `#FFB454` (Warm amber accent / handcrafted ink)
- `--ok`: `#34D399` (Verification emerald green)
- `--err`: `#E07A5F` (Audit redline / warning coral)
- `--text`: `#EEF2FA` (Primary high-contrast white/light text)
- `--muted`: `#93A0B8` (Secondary description text)
- `--faint`: `#7A726A` (Tertiary metadata text)

### Critical Token Collision: The `--ink` Misuse Bug
`--ink` is defined as `#06090F` (near pitch black). In multiple CSS modules, developers treated `--ink` as "text ink" instead of "surface background ink":
1. `apps/website/src/app/blog/blog.module.css`:
   - Line 36: `.postTitle { color: var(--ink); }`
   - Line 132: `.mdxContent pre { color: var(--ink); }`
   - Line 155: `.mdxContent blockquote { color: var(--ink); }`
   - Line 169: `.mdxContent th { color: var(--ink); }`
   - Line 230: `.authorName { color: var(--ink); }`
   *Result*: On `--card` (`#0F1523`) and `--raise` (`#0B101A`), `#06090F` text has contrast ratio **1.08:1** (completely unreadable black-on-black).
2. `apps/website/src/components/ui/MultiStepForm.module.css`:
   - Line 45: `color: var(--ink);`
3. `apps/website/src/components/ui/PricingNotice.module.css`:
   - Line 27: `background-color: var(--ink);`

### Phase 1 Remediation Token Strategy
Phase 1 will introduce explicit semantic surface and content tokens:
- `--surface-base`: `#06090F`
- `--surface-raised`: `#0B101A`
- `--surface-card`: `#0F1523`
- `--surface-card-hover`: `#141C2E`
- `--text-primary`: `#EEF2FA`
- `--text-secondary`: `#93A0B8`
- `--text-muted`: `#7A726A`
- `--text-on-accent`: `#05070C`
- `--border-subtle`: `rgba(148, 163, 196, 0.12)`
- `--border-strong`: `rgba(148, 163, 196, 0.22)`

---

## 4. Spacing Scale & Layout Containers

Standard 8px spacing scale in `globals.css`:
- `--space-1`: `8px`
- `--space-2`: `16px`
- `--space-3`: `24px`
- `--space-4`: `32px`
- `--space-5`: `40px`
- `--space-6`: `48px`
- `--space-8`: `64px`
- `--space-10`: `80px`
- `--space-11`: `88px`
- `--space-12`: `96px`
- `--space-16`: `128px`
- Max container: `--max: 1200px` (`.wrap { max-width: var(--max); padding: 0 24px; }`)

---

## 5. Inline Style Sprawl Catalog

Automated audit discovered 13 files with inline style blocks (`style={{...}}`):

1. `src/app/admin/cohort-applications/CohortApplicationsClient.tsx`: **29** inline styles (status colors, badges, padding, borders)
2. `src/app/hire/pre-vetted-engineers/page.tsx`: **14** inline styles (grid templates, card backgrounds, widths)
3. `src/app/ai-consultant/page.tsx`: **12** inline styles (chat bubble widths, alignments, radii)
4. `src/components/cohorts/AivaraCohortForm.tsx`: **7** inline styles
5. `src/app/cohorts/aivara/page.tsx`: **5** inline styles
6. `src/components/blog/BlogClientView.tsx`: **5** inline styles (tag filter button margins, search input borders)
7. `src/app/ai-solutions/llm-training/pipeline/page.tsx`: **3** inline styles (handnote degree rotation transforms — intentional)
8. `src/components/ui/ScrollProgress.tsx`: **2** inline styles (dynamic scroll percentage)
9. `src/components/ui/StudioConsole.tsx`: **2** inline styles
10. `src/components/pipeline/PipelineInteractiveConsole.tsx`: **1** inline style
11. `src/components/ui/BackToTop.tsx`: **1** inline style (dynamic opacity)
12. `src/components/ui/FAQAccordion.tsx`: **1** inline style
13. `src/components/ui/HandDrawnArrow.tsx`: **1** inline style (`overflow: visible` — SVG requirement)

*Remediation*: Promote static inline styles into modular CSS classes during Phase 10 while preserving dynamic transforms and SVG attributes.
