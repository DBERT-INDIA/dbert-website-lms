# Empirical Adversarial Challenge Report — Milestone 3 (challenger_m3_2)

**Evaluator**: `challenger_m3_2` (Empirical Challenger: critic, specialist)  
**Parent Orchestrator**: `d66c654e-a32e-4bd2-a554-e6ecbf8cc20c`  
**Test Suite**: `apps/portal/tests/test_challenger_m3_2.py` (10 test cases executed in Playwright Chromium & pytest)  
**Timestamp**: 2026-11-04T09:20:00Z  

---

## Challenge Summary

- **Overall Risk Assessment**: **MEDIUM** (1 confirmed CSS layout defect; modal popups and CSP action delegation are robust and verified).
- **Outcome**: 9 tests PASSED, 1 test FAILED (Defect Confirmed).
- **Core Defect**: `apps/portal/static/css/dbert-theme.css:3651` overrides mobile styling with `padding: 28px 30px !important;` outside of any media query, violating the mobile budget of `<= 20px` across 360px, 390px, 412px, and 768px viewports.

---

## 1. Observation

Direct empirical observations gathered via headless Chromium runtime execution (`playwright 1.51.0`, `pytest 9.1.1` on Python 3.12.10) against rendered templates and stylesheets:

### A. Responsive CSS Layout & Mobile Card Padding (Area 3)
1. **Desktop Margin (`.main`)**:
   - In `apps/portal/static/css/dbert-theme.css:3728`, `.has-sidebar .main` is defined with `margin-left: 240px !important;`.
   - Playwright computed style inspection across viewports `961px`, `1024px`, `1440px`, and `1920px` showed:
     ```javascript
     window.getComputedStyle(document.querySelector('.main')).marginLeft === "240px"
     ```
   - Test `test_desktop_main_left_margin_is_exactly_240px`: **PASSED**.
2. **Mobile Card Padding (`.auth-card`)**:
   - In `apps/portal/static/css/dbert-theme.css`, line 3647–3654 specifies:
     ```css
     body.home .auth-card, .auth-card {
       background: #FFFFFF !important;
       border: 1px solid #E2E8F0 !important;
       border-radius: 24px !important;
       padding: 28px 30px !important;
       box-shadow: 0 20px 50px -10px rgba(15, 23, 42, 0.15), 0 10px 20px -5px rgba(15, 23, 42, 0.08) !important;
       color: #0F172A !important;
     }
     ```
   - In `apps/portal/static/css/dbert-theme.css`, line 3895–3900 scopes a separate block:
     ```css
     @media (min-width: 769px) {
       .auth-card,
       body.home .auth-card {
         padding: 26px 32px !important;
       }
     }
     ```
   - In `apps/portal/static/css/dbert-theme.css`, line 2519 specifies:
     ```css
     @media (max-width: 768px) {
       .auth-card {
         padding: 18px 20px;
       }
     }
     ```
   - Playwright computed style inspection across mobile viewports (`360px`, `390px`, `412px`, `768px`) on both `body.home .auth-card` and standalone `.auth-card`:
     - Top Padding: `28px`
     - Bottom Padding: `28px`
     - Left Padding: `30px`
     - Right Padding: `30px`
     - Maximum Padding: `30px` (exceeds `<= 20px` limit)
   - Test `test_auth_card_padding_on_mobile`: **FAILED with AssertionError**:
     ```
     AssertionError: DEFECT FOUND in dbert-theme.css: .auth-card padding exceeds 20px on mobile <= 768px:
       body.home .auth-card at 360px has max padding 30px (top=28, right=30, bottom=28, left=30)
       standalone .auth-card at 360px has max padding 30px (top=28, right=30, bottom=28, left=30)
       body.home .auth-card at 390px has max padding 30px (top=28, right=30, bottom=28, left=30)
       standalone .auth-card at 390px has max padding 30px (top=28, right=30, bottom=28, left=30)
       body.home .auth-card at 412px has max padding 30px (top=28, right=30, bottom=28, left=30)
       standalone .auth-card at 412px has max padding 30px (top=28, right=30, bottom=28, left=30)
       body.home .auth-card at 768px has max padding 30px (top=28, right=30, bottom=28, left=30)
       standalone .auth-card at 768px has max padding 30px (top=28, right=30, bottom=28, left=30)
       Root cause: Line 3651 defines 'body.home .auth-card, .auth-card { padding: 28px 30px !important; }' outside of media queries, overriding mobile styling.
     ```

### B. Modal Popup Behavior (Area 1)
1. **`#forgotOverlay` on `apps/portal/templates/index.html`**:
   - **ARIA Attributes**: `role="dialog"`, `aria-modal="true"`, `aria-labelledby="forgotTitle"`, `aria-describedby="forgotDesc"`. Initial display is `none`. (`test_index_forgot_modal_aria_attributes` PASSED).
   - **Smooth Centering & Focus Management**: Invoking `window.openForgotModal()` adds `.active` class, computes `display: flex`, vertically/horizontally centers the `.dbert-modal-box`, locks `document.body.style.overflow = "hidden"`, and transfers focus directly to `#fp_email` (`activeElement.id === 'fp_email'`). (`test_index_forgot_modal_centering_and_focus` PASSED).
   - **Escape Key Dismissal**: Pressing `Escape` key closes overlay, returns display to `none`, resets `document.body.style.overflow = ""`. (`test_index_forgot_modal_keyboard_escape_dismissal` PASSED).
   - **Backdrop Dismissal**: Clicking on the backdrop (`.dbert-modal-backdrop` at point `(10, 10)`) dismisses the modal, whereas clicking within the modal box does not dismiss it. (`test_index_forgot_modal_backdrop_dismissal` PASSED).
   - **Validation & Honeypot**:
     - Bot honeypot `#fp_company_website` has `tabindex="-1"` and `style="display:none;"`. Populating it silently drops submission without sending network request.
     - Empty/invalid email triggers red DOM alert `.field-feedback.err` without dispatching request.
     - Valid email triggers `fetch("/forgot-password")`, transitions form to success state `.dbert-modal-success`, and updates title to "Check your inbox". (`test_index_forgot_modal_validation_and_honeypot` PASSED).
2. **`portal.html` Modals**:
   - `#passwordModal`, `#applyDomainModal`, `#logoutConfirmModal` all feature `role="dialog"`, `aria-modal="true"`, and appropriate `aria-labelledby`.
   - Cycling through all 11 tabs (`dashboard`, `browse_jobs`, `my_applications`, `profile`, `browse_courses`, `my_courses`, `tasks`, `documents`, `change_password`, `domain_selection`, `contact_support`) produced **zero runtime JavaScript exceptions**. (`test_portal_modals_and_tab_switching_no_exceptions` PASSED).
   - Clicking sidebar signout invokes `window.openLogoutConfirmModal()`, which opens `#logoutConfirmModal` without calling `/logout`. An explicit click on "Yes, Sign Out" (`#confirmLogoutBtn`) is required to navigate to `/logout`. (`test_portal_logout_confirmation_gate_enforcement` PASSED).

### C. CSP Action Delegation Resolution (Area 2)
- Scanned all 37 HTML templates in `apps/portal/templates/` for `data-act-*` attributes.
- Found 114 dynamic actions across templates including `admin.html`, `portal.html`, `course_learn.html`, `company_dashboard.html`, `ambassador.html`, `cv_editor.html`, etc.
- In headless Chromium, each template was rendered and loaded with its corresponding scripts (`csp-actions.js`, `portal-all.js`, inline scripts).
- For every non-builtin function name, evaluated `typeof window[fn] === 'function'`.
- Result: **0 unresolved actions** out of 114 actions verified.
- Test `test_all_templates_csp_action_resolution`: **PASSED**.

---

## 2. Logic Chain

1. **Premise 1**: Milestone 2 remediation intended `.auth-card` to expand horizontally up to 730px on desktop while maintaining compact mobile padding `<= 20px` on viewports `<= 768px`.
2. **Observation Step**: In `dbert-theme.css`, `worker_m2_1` wrapped lines 3895–3900 (`padding: 26px 32px !important;`) inside `@media (min-width: 769px)`.
3. **Observation Step**: However, earlier in the same file at lines 3647–3654, rule `body.home .auth-card, .auth-card { padding: 28px 30px !important; }` remained unmodified outside of any media queries.
4. **CSS Specificity and Precedence Mechanics**:
   - At `<= 768px`, line 2519 (`padding: 18px 20px;`) does not use `!important`.
   - Line 3651 uses `!important`.
   - Under CSS Cascading & Specificity specifications (CSS Cascade Level 4), declarations with `!important` take precedence over all normal declarations regardless of selector specificity.
   - For `body.home .auth-card`, line 3651 also has higher specificity (`0,1,1,0`) than line 2519 (`0,0,1,0`).
5. **Deduction**: Because line 3651 is outside of any `@media` block, browsers apply `padding: 28px 30px !important` across all screen widths below 769px.
6. **Empirical Confirmation**: Testing in Playwright Chromium at 360px, 390px, 412px, and 768px viewports directly confirmed that `window.getComputedStyle(.auth-card).paddingLeft` is `30px` and `paddingTop` is `28px`, breaking the `<= 20px` mobile padding specification.
7. **Deduction regarding Modals & CSP**:
   - The `#forgotOverlay` modal implements all WCAG dialog requirements, Escape/backdrop closing, focus trapping, validation, honeypot protection, and success messaging.
   - The `portal.html` modals operate cleanly with zero runtime exceptions across all tabs and maintain an explicit logout confirmation barrier.
   - All 114 CSP `data-act-*` handlers resolve to functions on `window` or valid `$builtins`.

---

## 3. Caveats

1. **Touch Gesture Interactions**: Tested keyboard (`Escape`, `Tab`), mouse clicks, and window events. Touch gesture drag-to-dismiss (swipe down) on iOS Safari was not tested, as it was not specified in the requirements.
2. **Review-Only Constraint**: In accordance with the Challenger archetype constraints, this agent did not modify `dbert-theme.css`. The defect is documented with full root cause and mitigation instructions for the worker agent.
3. **Template Mock Contexts**: In `test_all_templates_csp_action_resolution`, Jinja rendering for complex admin dashboards (`admin_integrity_dashboard.html`, `admin_cohorts.html`) required mock context dictionaries matching backend database models to render without server-side template errors.

---

## 4. Conclusion & Verdict

- **Overall Verdict**: **CONDITIONAL PASS WITH 1 DEFECT**.
- **Dimension 1 (Modal Popups)**: **PASS** — Flawless implementation of WCAG dialog accessibility, smooth centering, focus management, honeypot security, and logout gating.
- **Dimension 2 (CSP Action Delegation)**: **PASS** — 100% resolution rate across all 37 templates (114 actions verified).
- **Dimension 3 (Responsive Layout)**:
  - Desktop `.main` margin: **PASS** (strictly 240px).
  - Mobile `.auth-card` padding: **FAIL (DEFECT CONFIRMED)**.

### Recommended Remediation for Worker Agent
In `apps/portal/static/css/dbert-theme.css`:
Either:
1. Wrap lines 3647–3654 inside `@media (min-width: 769px)`:
   ```css
   @media (min-width: 769px) {
     body.home .auth-card, .auth-card {
       background: #FFFFFF !important;
       border: 1px solid #E2E8F0 !important;
       border-radius: 24px !important;
       padding: 28px 30px !important;
       box-shadow: 0 20px 50px -10px rgba(15, 23, 42, 0.15), 0 10px 20px -5px rgba(15, 23, 42, 0.08) !important;
       color: #0F172A !important;
     }
   }
   ```
2. OR explicitly add a mobile override after line 3654:
   ```css
   @media (max-width: 768px) {
     body.home .auth-card,
     .auth-card {
       padding: 18px 16px !important;
     }
   }
   ```

---

## 5. Verification Method

To independently reproduce all observations and verify the defect and passing checks:

1. **Run the Empirical Test Suite**:
   ```powershell
   cd apps/portal
   pytest tests/test_challenger_m3_2.py -v
   ```
2. **Expected Test Suite Output**:
   - 9 tests PASSED.
   - 1 test FAILED: `test_auth_card_padding_on_mobile` failing at assertion line 575 with `AssertionError: DEFECT FOUND in dbert-theme.css: .auth-card padding exceeds 20px on mobile <= 768px`.
3. **Invalidation Condition**:
   Once the worker agent applies the remediation above, running `pytest tests/test_challenger_m3_2.py -v` will produce **10 passed, 0 failed in ~29s**.
