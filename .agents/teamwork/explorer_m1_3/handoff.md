# Visual and UI/UX Audit Report (Requirement R3 & R2 Modal Conversion)

**Workspace**: `c:\Users\user\Desktop\dbert-website-lms`  
**Target Systems**: `apps/portal` (Flask LMS Portal) & `apps/website` (Next.js Marketing Site)  
**Agent**: `explorer_m1_3`  
**Date**: 2026-11-03  

---

## 1. Observation

### 1.1 Flask LMS Portal (`apps/portal`)

#### Observation 1.1.1: Systemic Interaction Failure via `csp-actions.js`
In `apps/portal/static/js/csp-actions.js`, lines 92–99:
```javascript
function resolve(name) {
  if (!name) return null;
  if (name.charAt(0) === '$') return BUILTINS[name] || null;
  var fn = window[name];
  return (typeof fn === 'function') ? fn : null;
}
```
And lines 130–134:
```javascript
var fn = resolve(name);
if (!fn) {
  if (window.console) console.error('[csp-actions] no such action: ' + name);
  return;
}
```
In `apps/portal/templates/index.html`, lines 571–886: The `<script nonce="{{ csp_nonce() }}">` starts with `'use strict';` inside a script block. Functions declared within this script (such as `openForgotModal`, `closeForgotModal`, `submitForgot`, `toggleMenu`, `toggleFAQ`, `scrollToId`, `updateWhyCount`, `resetSiFlow`, `doEmailCheck`, `doSetPassword`, `doSignin`, `doSignOut`) are locally scoped or declared via `function fn() {}` without binding to `window`. While lines 636–643 and 809–814 explicitly bound certain functions to `window`, the following handlers used by `data-act-click` or `data-act-input` are missing from `window`:
- Line 109: `<button class="mobile-toggle" data-act-click="toggleMenu">` -> `toggleMenu` is NOT on `window`.
- Lines 281, 288, 295, 302, 309, 316, 323: `<button class="faq-q" data-act-click="toggleFAQ">` -> `toggleFAQ` is NOT on `window`.
- Line 473: `<input ... data-act-input="updateWhyCount">` -> `updateWhyCount` is NOT on `window`.
- Line 502: `<button ... data-act-click="doEmailCheck">` -> `doEmailCheck` is NOT on `window`.
- Line 516: `<button ... data-act-click="doSignin">` -> `doSignin` is NOT on `window`.
- Line 517: `<a ... data-act-click="openForgotModal">` -> `openForgotModal` is NOT on `window`.
- Line 529: `<a ... data-act-click="resetSiFlow">` -> `resetSiFlow` is NOT on `window`.
- Line 535: `<button ... data-act-click="doSetPassword">` -> `doSetPassword` is NOT on `window`.
- Line 552: `<button data-act-click="closeForgotModal">` -> `closeForgotModal` is NOT on `window`.
- Line 566: `<button ... data-act-click="submitForgot">` -> `submitForgot` is NOT on `window`.
- Line 580: `scrollToId` is NOT on `window`.
- Line 894: `<button data-act-click="doSignOut">` -> `doSignOut` is NOT on `window`.

The exact same pattern was observed in other portal templates:
- `apps/portal/templates/course_learn.html:12, 17, 49, 79, 86, 98, 119, 120`: `toggleTreeSidebar`, `openGeminiModal`, `closeGeminiModal`, `testAndSaveGeminiKey`, `closeTreeSidebar`, `loadSubtopic`, `sendMessage` are referenced by `data-act-click` but missing from `window`.
- `apps/portal/templates/course_detail.html:84, 101`: `enrollCourse`, `enrollPaid1999` missing from `window`.
- `apps/portal/templates/course_quiz.html:31`: `submitQuiz` missing from `window`.
- `apps/portal/templates/course_submit_project.html:52`: `submitProject` missing from `window`.
- `apps/portal/templates/tasks_list.html:75, 103, 126`: `openSubmitModal`, `closeModal`, `submitTask` missing from `window`.
- `apps/portal/templates/ambassador.html:31, 60, 80`: `copyRefLink`, `requestWithdrawal`, `saveUpi` missing from `window`.
- `apps/portal/templates/cv_editor.html:49, 55, 78, 79`: `addEntry`, `saveThen` missing from `window`.
- `apps/portal/templates/session_booking.html:28`: `bookSlot` missing from `window`.
- `apps/portal/templates/company_dashboard.html:21, 85`: `showTab`, `submitCourse` missing from `window`.

#### Observation 1.1.2: Requirement R2 Password Reset Overlay & Light/Dark Theme Clash
In `apps/portal/templates/index.html`, lines 548–569:
```html
<div id="forgotOverlay" style="position:fixed;inset:0;z-index:99999;background:rgba(9,12,20,0.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:none;align-items:center;justify-content:center;padding:16px;">
  <div style="background:#0E111A;border:1px solid rgba(255,255,255,0.08);border-radius:20px;max-width:440px;width:100%;box-shadow:0 25px 60px rgba(0,0,0,0.7);padding:28px 26px;" role="dialog" aria-modal="true" aria-labelledby="forgotTitle">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
      <h3 id="forgotTitle" style="font-size:18px;font-weight:800;color:#FFFFFF;margin:0;">Reset your password</h3>
      <button data-act-click="closeForgotModal" aria-label="Close" style="background:none;border:none;color:#8E9AA8;font-size:22px;cursor:pointer;line-height:1;">&times;</button>
    </div>
    <p style="font-size:13px;color:#8E9AA8;line-height:1.6;margin:0 0 18px;">Enter your account email and we'll send a reset link if an account exists. The link expires in 1 hour.</p>
...
```
The modal overlay uses hardcoded inline styles (`background: #0E111A`, `border: 1px solid rgba(255,255,255,0.08)`, `color: #FFFFFF`) representing an outdated dark palette. The rest of `dbert-theme.css` has migrated to a crisp light theme (`--bg-surface: #FFFFFF`, `--tx-head: #0F172A`, `--border-strong: #CBD5E1`). Furthermore, the modal trigger fails because `openForgotModal` is not on `window`.

#### Observation 1.1.3: Double Margin / 480px Squish Layout Bug
In `apps/portal/static/css/dbert-theme.css`, lines 255–260:
```css
@media (min-width: 961px) {
  body.has-sidebar,
  body.has-staff-sidebar,
  .has-sidebar .main,
  .has-sidebar .container,
  .has-sidebar .content-wrap,
  .has-staff-sidebar .main,
  .has-staff-sidebar .container,
  .has-staff-sidebar .content-wrap {
    margin-left: var(--sidebar-w);
  }
}
```
In `apps/portal/templates/coins_ledger.html:7`, `tasks_list.html:7`, `courses_catalog.html:7`:
```html
<body class="has-sidebar">
...
  <main class="main">
```
Because `body.has-sidebar` is in the selector list AND `.has-sidebar .main` is ALSO in the selector list, `margin-left: 240px` is applied to `body`, and another `margin-left: 240px` is applied to `.main`. The total left offset is 480px on screens >= 961px, pushing all page content far to the right and causing severe content truncation and horizontal scrolling.

#### Observation 1.1.4: Mobile Auth Card Padding Override
In `apps/portal/static/css/dbert-theme.css`, line 1758 vs line 3897:
Line 1758:
```css
@media (max-width: 768px) {
  .auth-card {
    padding: 26px 20px;
  }
}
```
Line 3897:
```css
.auth-card, body.home .auth-card {
  padding: 26px 32px !important;
}
```
The `!important` rule at line 3897 overrides the mobile rule. On mobile screens (e.g. 360px–390px viewports), 64px of horizontal padding consumes nearly 20% of the entire screen width, severely crushing input fields, OTP inputs, and phone number selectors.

#### Observation 1.1.5: Inline Forms Requiring Modal Popups (Requirement R2 Extension)
In `apps/portal/templates/course_detail.html`, lines 100–118:
The `#premiumUploadUI` block is an inline expandable container embedded inside the narrow right-hand price card (`max-width: 340px`). Expanding this inline element distorts the price card height and breaks the card alignment.
In `apps/portal/templates/session_booking.html`, lines 68–85:
User slot booking relies on native browser `confirm("Book this session...")` and `alert("Session booked...")`, disrupting the custom UI theme and failing modern headless/web view flows.

---

### 1.2 Next.js Marketing Website (`apps/website`)

#### Observation 1.2.1: Undefined CSS Custom Properties
In `apps/website/src/components/cohorts/cohort.module.css`, lines 51, 83, 88:
```css
51: background: var(--bg);
83: color: var(--fg);
88: background: var(--surface);
```
In `apps/website/src/app/globals.css`, lines 1644, 1677:
```css
1644: background: var(--bg);
1677: background: var(--bg);
```
In `apps/website/src/app/page.module.css`, lines 9, 110, 182, 231:
```css
9: background: var(--bg);
110: background: var(--bg);
182: background: var(--bg);
231: background: var(--bg);
```
In `apps/website/src/app/globals.css`, `:root` defines `--surface-base`, `--surface-card`, `--text-primary`, `--ink`, but NEVER defines `--bg`, `--fg`, or `--surface`. As a consequence, these elements fallback to browser default transparent backgrounds and unstyled text colors.

#### Observation 1.2.2: Mobile Drawer vs. WhatsApp Floating Button Z-Index Clash
In `apps/website/src/components/layout/WhatsAppFloat.module.css`, lines 15–20:
```css
.whatsappFloat {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
}
```
In `apps/website/src/components/layout/MegaMenu.module.css`, line 342:
```css
.mobileDrawer {
  position: fixed;
  inset: 0;
  z-index: 200;
  background: var(--surface-base);
}
```
When a mobile user opens the hamburger navigation drawer (`z-index: 200`), the WhatsApp floating button (`z-index: 9999`) sits on top of drawer links and menu navigation items, intercepting touch events.

#### Observation 1.2.3: Heading Hierarchy Defect in Blog Reader
Tool execution: `npm --prefix apps/website run audit:headings` returned:
```
Missing <h1>: src/app/blog/reader/page.tsx
```
In `apps/website/src/app/blog/reader/page.tsx`, the post title is rendered inside a `<div>` or dynamic header component without an explicit semantic `<h1>` tag, failing SEO standards and accessibility audits.

#### Observation 1.2.4: Outdated Legacy Domain References
Audit of package configurations and content templates identified 130+ references to legacy URLs (`dbert.online`, `internship.dbert.online`, `http://localhost:5000`) across `dbert-api-package/website-content/` and static text blocks instead of unified environment-configured URLs or relative routes.

---

## 2. Logic Chain

1. **Premise 1**: The Flask LMS application enforces a strict Content Security Policy (CSP) with a per-request nonce on script elements, eliminating `unsafe-inline`.
2. **Premise 2**: To support interactivity without inline handlers, `csp-actions.js` listens to document events and dispatches actions via `window[name]`.
3. **Inference 1**: Any function declared inside a `'use strict'` script block that is not assigned to `window[name]` is unreachable by `csp-actions.js`.
4. **Conclusion 1**: When users click "Forgot password?", "Sign In", "Continue to Sign In", mobile hamburger toggle, or FAQ items on `templates/index.html`, or interact with quizzes, task submissions, or Gemini AI in LMS pages, the browser executes `csp-actions.js`, fails to resolve `window[name]`, logs `[csp-actions] no such action`, and does nothing. This completely paralyzes primary user flows.
5. **Premise 3**: In CSS, margin properties applied to nested parent-child elements (`body` and `.main`) are additive when both have declared margins.
6. **Inference 2**: In `dbert-theme.css`, declaring `body.has-sidebar { margin-left: 240px; }` and `.has-sidebar .main { margin-left: 240px; }` applies a 480px left margin to `.main`.
7. **Conclusion 2**: On desktop monitors (>= 961px), all authenticated LMS pages (`courses_catalog.html`, `tasks_list.html`, `coins_ledger.html`, etc.) render with half the screen blank on the left and content overflowing on the right.
8. **Premise 4**: CSS `var(--bg)` and `var(--surface)` without a declared token value in `:root` fall back to `initial` (transparent).
9. **Inference 3**: Component cards in `cohort.module.css` and sections in `page.module.css` have transparent backgrounds rather than the intended theme card surfaces.
10. **Conclusion 3**: The Next.js website exhibits visual styling breakage on cohort listings and feature sections.
11. **Premise 5**: A higher `z-index` element (9999) stacks on top of a lower `z-index` element (200) regardless of DOM order when both have fixed positioning.
12. **Inference 4**: The WhatsApp button hovers over the mobile navigation drawer.
13. **Conclusion 4**: Mobile navigation touch targets are obstructed by the WhatsApp floating widget.

---

## 3. Caveats

- **Static Analysis Scope**: This audit was executed via AST parsing, regex searches, template tree inspection, and CSS rule hierarchy analysis without running a live browser daemon (due to read-only explorer permissions).
- **Backend Auth Endpoints**: The visual and interaction audit covers frontend client binding, styling, and markup structure. While the API routes (`/api/auth/forgot-password`, `/api/auth/signin`) are called by these scripts, backend endpoint unit tests should be verified by backend worker agents.
- **Legacy Static Export**: `cpanel_public_html/` contains static assets and pre-built files from previous deployments. Changes made to `apps/website` must be rebuilt (`npm run build`) before synchronizing to deployment directories.

---

## 4. Conclusion & Actionable Fixes

To resolve all identified visual, responsive, and UI/UX issues, the following concrete modifications are required.

### 4.1 LMS Portal Fixes (`apps/portal`)

#### Fix 4.1.1: Export all missing action handlers to `window` in `apps/portal/templates/index.html`
**Target File**: `apps/portal/templates/index.html`  
**Location**: End of the `<script nonce="{{ csp_nonce() }}">` block (around line 885)  
**Action**: Add explicit `window` assignments for all missing CSP delegated actions:
```javascript
// Expose all delegated csp-actions handlers to window
window.toggleMenu = toggleMenu;
window.toggleFAQ = toggleFAQ;
window.scrollToId = scrollToId;
window.updateWhyCount = updateWhyCount;
window.resetSiFlow = resetSiFlow;
window.doEmailCheck = doEmailCheck;
window.doSetPassword = doSetPassword;
window.doSignin = doSignin;
window.doSignOut = doSignOut;
window.openForgotModal = openForgotModal;
window.closeForgotModal = closeForgotModal;
window.submitForgot = submitForgot;
```

#### Fix 4.1.2: Refactor `#forgotOverlay` to unified light `.modal` theme and ensure toggle functions work
**Target File**: `apps/portal/templates/index.html`  
**Location**: Lines 548–569  
**Action**: Replace the dark inline-styled `#forgotOverlay` with the standard `.modal` / `.modal-box` light theme styling from `dbert-theme.css`:
```html
<!-- FORGOT PASSWORD MODAL (Requirement R2 Popup Modal) -->
<div id="forgotOverlay" class="modal" role="dialog" aria-modal="true" aria-labelledby="forgotTitle">
  <div class="modal-box" style="max-width:440px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
      <h3 id="forgotTitle" style="font-size:18px;font-weight:700;color:var(--tx-head);margin:0;">Reset your password</h3>
      <button data-act-click="closeForgotModal" aria-label="Close" class="btn-ghost" style="font-size:22px;line-height:1;padding:4px 8px;cursor:pointer;">&times;</button>
    </div>
    <p style="font-size:13px;color:var(--tx-muted);line-height:1.6;margin:0 0 18px;">
      Enter your account email and we'll send a reset link if an account exists. The link expires in 1 hour.
    </p>

    <div class="auth-error" id="forgotError" role="alert" style="display:none;align-items:center;gap:8px;background:rgba(220,38,38,0.1);border:1px solid rgba(220,38,38,0.25);border-radius:var(--r-md);color:#DC2626;font-size:13px;font-weight:600;padding:10px 14px;margin-bottom:14px;">
      <i class="fa fa-circle-exclamation"></i><span></span>
    </div>
    <div id="forgotSuccess" role="status" aria-live="polite" style="display:none;flex-direction:column;gap:10px;background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.25);color:#16A34A;border-radius:var(--r-md);font-size:13px;font-weight:600;padding:12px 16px;margin-bottom:14px;">
      <div style="display:flex;align-items:center;gap:8px;"><i class="fa fa-circle-check"></i><span id="forgotSuccessText"></span></div>
      <div id="forgotDirectLink" style="display:none;"></div>
    </div>

    <div id="forgotFormArea">
      <div class="form-group" style="margin-bottom:16px;">
        <label class="field-label" for="fp_email" style="color:var(--tx-head);font-size:12px;font-weight:700;letter-spacing:0.4px;text-transform:uppercase;margin-bottom:6px;display:block;">Email Address</label>
        <input type="email" id="fp_email" class="field-input" placeholder="you@example.com" autocomplete="email" style="width:100%;padding:10px 12px;border:1px solid var(--border-strong);border-radius:var(--r-md);background:var(--bg-card);color:var(--tx-body);font-size:14px;"/>
      </div>
      <input type="text" name="company_website" id="fp_company_website" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" aria-label="Leave this field blank" style="display:none !important;position:absolute !important;left:-9999px !important;top:-9999px !important;width:0 !important;height:0 !important;opacity:0 !important;pointer-events:none !important;"/>

      <button class="btn btn-primary" id="forgotBtn" data-act-click="submitForgot" style="width:100%;padding:11px 16px;font-weight:600;display:flex;align-items:center;justify-content:center;gap:8px;">
        <span class="btn-label"><i class="fas fa-paper-plane"></i> Send Reset Link</span>
        <span class="btn-spinner" style="display:none;"></span>
      </button>
    </div>
  </div>
</div>
```
And in `index.html` JS script:
```javascript
function openForgotModal() {
  const modal = document.getElementById('forgotOverlay');
  if (modal) {
    modal.classList.add('open');
    modal.style.display = 'flex';
    const email = document.getElementById('si_email');
    const fpEmail = document.getElementById('fp_email');
    if (email && fpEmail && email.value) fpEmail.value = email.value.trim();
    if (fpEmail) fpEmail.focus();
  }
}
function closeForgotModal() {
  const modal = document.getElementById('forgotOverlay');
  if (modal) {
    modal.classList.remove('open');
    modal.style.display = 'none';
  }
}
```

#### Fix 4.1.3: Eliminate Double-Margin in `apps/portal/static/css/dbert-theme.css`
**Target File**: `apps/portal/static/css/dbert-theme.css`  
**Location**: Lines 255–260  
**Change**: Remove `body.has-sidebar` and `body.has-staff-sidebar` from the selector list so only `.main`, `.container`, and `.content-wrap` receive `margin-left: var(--sidebar-w)`:
```css
/* BEFORE */
@media (min-width: 961px) {
  body.has-sidebar,
  body.has-staff-sidebar,
  .has-sidebar .main,
  .has-sidebar .container,
  .has-sidebar .content-wrap,
  .has-staff-sidebar .main,
  .has-staff-sidebar .container,
  .has-staff-sidebar .content-wrap {
    margin-left: var(--sidebar-w);
  }
}

/* AFTER */
@media (min-width: 961px) {
  .has-sidebar .main,
  .has-sidebar .container,
  .has-sidebar .content-wrap,
  .has-staff-sidebar .main,
  .has-staff-sidebar .container,
  .has-staff-sidebar .content-wrap {
    margin-left: var(--sidebar-w);
  }
}
```

#### Fix 4.1.4: Fix Mobile Auth Card Padding in `dbert-theme.css`
**Target File**: `apps/portal/static/css/dbert-theme.css`  
**Location**: Line 3897  
**Change**: Scope the 32px padding to desktop viewports only (`min-width: 769px`):
```css
/* BEFORE */
.auth-card, body.home .auth-card { padding: 26px 32px !important; }

/* AFTER */
@media (min-width: 769px) {
  .auth-card, body.home .auth-card { padding: 26px 32px; }
}
```

#### Fix 4.1.5: Export missing handlers across other portal templates
In each of the following templates, ensure local functions are explicitly assigned to `window`:
- `apps/portal/templates/course_learn.html`:
  `window.toggleTreeSidebar = toggleTreeSidebar; window.openGeminiModal = openGeminiModal; window.closeGeminiModal = closeGeminiModal; window.testAndSaveGeminiKey = testAndSaveGeminiKey; window.closeTreeSidebar = closeTreeSidebar; window.loadSubtopic = loadSubtopic; window.sendMessage = sendMessage;`
- `apps/portal/templates/course_detail.html`:
  `window.enrollCourse = enrollCourse; window.enrollPaid1999 = enrollPaid1999;`
- `apps/portal/templates/course_quiz.html`:
  `window.submitQuiz = submitQuiz;`
- `apps/portal/templates/course_submit_project.html`:
  `window.submitProject = submitProject;`
- `apps/portal/templates/tasks_list.html`:
  `window.openSubmitModal = openSubmitModal; window.closeModal = closeModal; window.submitTask = submitTask;`
- `apps/portal/templates/ambassador.html`:
  `window.copyRefLink = copyRefLink; window.requestWithdrawal = requestWithdrawal; window.saveUpi = saveUpi;`
- `apps/portal/templates/cv_editor.html`:
  `window.addEntry = addEntry; window.saveThen = saveThen;`
- `apps/portal/templates/session_booking.html`:
  `window.bookSlot = bookSlot;`
- `apps/portal/templates/company_dashboard.html`:
  `window.showTab = showTab; window.submitCourse = submitCourse;`

---

### 4.2 Marketing Website Fixes (`apps/website`)

#### Fix 4.2.1: Define `--bg`, `--surface`, and `--fg` Token Aliases in `globals.css`
**Target File**: `apps/website/src/app/globals.css`  
**Location**: In `:root` definition (around line 20)  
**Action**: Add the missing custom property aliases:
```css
:root {
  /* Existing tokens */
  --surface-base: #FFFFFF;
  --surface-card: #F8FAFC;
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --border: #E2E8F0;

  /* Token Aliases for compatibility */
  --bg: var(--surface-base);
  --surface: var(--surface-card);
  --fg: var(--text-primary);
}
```

#### Fix 4.2.2: Adjust WhatsApp Float Widget Z-Index
**Target File**: `apps/website/src/components/layout/WhatsAppFloat.module.css`  
**Location**: Line 15  
**Change**: Lower `z-index` from `9999` to `95` so the mobile navigation drawer (`z-index: 200`) cleanly layers above it:
```css
/* BEFORE */
.whatsappFloat {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
}

/* AFTER */
.whatsappFloat {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 95;
}
```

#### Fix 4.2.3: Add Semantic `<h1>` in Blog Reader
**Target File**: `apps/website/src/app/blog/reader/page.tsx`  
**Action**: Ensure the article title or page header is rendered inside a semantic `<h1>` tag:
```tsx
<header className={styles.postHeader}>
  <h1 className={styles.postTitle}>{post.title || "DBERT Tech Blog"}</h1>
</header>
```

---

## 5. Verification Method

To verify that these issues have been completely resolved once worker agents apply the changes:

1. **CSP Action Delegation Verification**:
   - In browser developer tools on `http://localhost:5000/` (or running portal), click the "Forgot password?" link (`data-act-click="openForgotModal"`).
   - Verify that `#forgotOverlay` displays as a centered modal popup with light theme styling (`var(--bg-surface)`).
   - Verify console logs contain 0 occurrences of `[csp-actions] no such action: openForgotModal`.
   - Test the mobile hamburger button, FAQ accordion items, and login button. Verify console logs contain 0 `[csp-actions] no such action` warnings.

2. **Sidebar Offset / Double Margin Verification**:
   - Navigate to `/courses`, `/tasks`, or `/ledger`.
   - Inspect `<main class="main">` in DevTools at screen width >= 1024px.
   - Verify computed `margin-left` is exactly `240px` (sidebar width), NOT `480px`.
   - Verify page content fills the available width without right horizontal overflow.

3. **Mobile Padding Verification**:
   - Set viewport to 360px x 640px.
   - Inspect `.auth-card`. Verify computed horizontal padding is `20px` (not overridden by `32px !important`).

4. **Next.js Design System & Tokens Verification**:
   - Run: `npm --prefix apps/website run audit:tokens`
   - Run: `npm --prefix apps/website run audit:styles`
   - Run: `npm --prefix apps/website run audit:headings`
   - Verify all 3 scripts return exit code 0.
   - Open mobile drawer (<500px). Verify WhatsApp floating icon is obscured beneath the drawer backdrop, not hovering on top of menu links.
