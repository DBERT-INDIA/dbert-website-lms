# Technical Handoff Report: Requirement R2 (Modal Popup Conversion)

**Agent**: `explorer_m1_2` (Teamwork Explorer)  
**Parent Orchestrator**: `dbert-orchestrator` (`d66c654e-a32e-4bd2-a554-e6ecbf8cc20c`)  
**Working Directory**: `c:\Users\user\Desktop\dbert-website-lms\.agents\teamwork\explorer_m1_2`  
**Date**: 2026-11-03  
**Status**: Complete  

---

## 1. Observation

### Observation 1.1: Password Reset Form Location and HTML Markup
- **Exact File**: `c:\Users\user\Desktop\dbert-website-lms\apps\portal\templates\index.html`
- **Lines**: 548–569
- **Verbatim Code**:
```html
  <!-- FORGOT PASSWORD MODAL (MATCHING IMAGE 4) -->
  <div id="forgotOverlay" style="position:fixed;inset:0;z-index:99999;background:rgba(9,12,20,0.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:none;align-items:center;justify-content:center;padding:16px;">
    <div style="background:#0E111A;border:1px solid rgba(255,255,255,0.08);border-radius:20px;max-width:440px;width:100%;box-shadow:0 25px 60px rgba(0,0,0,0.7);padding:28px 26px;" role="dialog" aria-modal="true" aria-labelledby="forgotTitle">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
        <h3 id="forgotTitle" style="font-size:18px;font-weight:800;color:#FFFFFF;margin:0;">Reset your password</h3>
        <button data-act-click="closeForgotModal" aria-label="Close" style="background:none;border:none;color:#8E9AA8;font-size:22px;cursor:pointer;line-height:1;">&times;</button>
      </div>
      <p style="font-size:13px;color:#8E9AA8;line-height:1.6;margin:0 0 18px;">Enter your account email and we'll send a reset link if an account exists. The link expires in 1 hour.</p>

      <div class="auth-error" id="forgotError" role="alert" style="display:none;align-items:center;gap:8px;background:rgba(220,38,38,0.15);border:1px solid rgba(220,38,38,0.3);border-radius:10px;color:#F87171;font-size:13px;font-weight:600;padding:10px 14px;margin-bottom:14px;"><i class="fa fa-circle-exclamation"></i><span></span></div>
      <div id="forgotSuccess" role="status" aria-live="polite" style="display:none;flex-direction:column;gap:10px;background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);color:#22C55E;border-radius:10px;font-size:13px;font-weight:600;padding:12px 16px;margin-bottom:14px;">
        <div style="display:flex;align-items:center;gap:8px;"><i class="fa fa-circle-check"></i><span id="forgotSuccessText"></span></div>
        <div id="forgotDirectLink" style="display:none;"></div>
      </div>

      <div id="forgotFormArea">
        <div class="form-group"><label class="field-label" for="fp_email" style="color:#FFFFFF;font-size:11px;font-weight:800;letter-spacing:0.6px;text-transform:uppercase;margin-bottom:6px;display:block;">Email</label><input type="email" id="fp_email" class="field-input" placeholder="you@example.com" autocomplete="email"/></div>
        <input type="text" name="company_website" id="fp_company_website" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" aria-label="Leave this field blank" style="display:none !important;position:absolute !important;left:-9999px !important;top:-9999px !important;width:0 !important;height:0 !important;opacity:0 !important;pointer-events:none !important;"/>

        <button class="btn-auth-submit" id="forgotBtn" data-act-click="submitForgot" style="margin-top:14px;"><span class="btn-label"><i class="fas fa-paper-plane"></i> &nbsp;Send Reset Link</span><span class="btn-spinner"></span></button>
      </div>
    </div>
  </div>
```
- **Trigger Link in Sign In panel**: `apps/portal/templates/index.html` line 517:
```html
<p style="text-align:center;margin-top:14px;font-size:12px;"><a href="#" style="color:#2563EB;font-weight:700;text-decoration:none;" data-act-click="openForgotModal" data-prevent-click>Forgot password?</a></p>
```

### Observation 1.2: Controller Functions and Keydown Handlers
- **File**: `apps/portal/templates/index.html` lines 646–685:
```javascript
  function openForgotModal(){
    const ov=document.getElementById('forgotOverlay');if(!ov)return;
    const authOv=document.getElementById('authOverlay');if(authOv)authOv.classList.remove('active');
    document.getElementById('forgotError').style.display='none';
    document.getElementById('forgotSuccess').style.display='none';
    document.getElementById('forgotFormArea').style.display='block';
    setLoading('forgotBtn',false);
    const emailInput=document.getElementById('fp_email');
    emailInput.value=_siEmail||document.getElementById('si_email')?.value.trim()||'';
    ov.style.display='flex';
    setTimeout(()=>emailInput.focus(),80);
  }
  function closeForgotModal(){
    const ov=document.getElementById('forgotOverlay');if(ov)ov.style.display='none';
    showAuthOverlay('signin');
  }
```
- **File**: `apps/portal/templates/index.html` lines 906–908:
```javascript
    document.getElementById('fp_email')?.addEventListener('keydown',e=>{if(e.key==='Enter')submitForgot();});
    document.getElementById('forgotOverlay')?.addEventListener('click',e=>{if(e.target.id==='forgotOverlay')closeForgotModal();});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeForgotModal();hideAuthOverlay();}});
```
- **Backend API Route**: `apps/portal/app.py` lines 17750–17800:
  `@app.route("/forgot-password", methods=["POST"])` accepts `{"email": "...", "company_website": "..."}` and returns `{"status": "success", "message": "If that email exists, a reset link has been sent."}`.

### Observation 1.3: CSS Theme Token Violation and Lack of CSS Classes
- In `apps/portal/static/css/dbert-theme.css`:
  - Search for `forgotOverlay` returned zero matches. There are zero CSS classes for `#forgotOverlay` in the stylesheet.
  - Line 15 of `dbert-theme.css` explicitly states:
    `/* RULES (see DBERT_BUILD_SPEC.md §2): New components are added HERE, never inline in a template. */`
  - The design tokens in lines 24–88 define `--bg-surface: #FFFFFF;`, `--border: #E2E8F0;`, `--brand: #2563EB;`, `--tx-head: #0F172A;`.
  - While `#authOverlay`'s sign-in panel is light mode with white backgrounds and blue buttons, `#forgotOverlay` contains 10+ hardcoded inline style attributes (`background:#0E111A`, `border:1px solid rgba(255,255,255,0.08)`, `color:#FFFFFF`, dark gold button).

### Observation 1.4: Similar Inline Forms and Native Dialogs in LMS and Website
1. **LMS Intern Portal Change Password Panel**: `apps/portal/templates/portal.html` lines 673–686 (`<div class="panel" id="panel-password">`). Occupies an entire navigation tab (`data-tab="password"` in line 39) with a wide, empty glass-card container just for 3 inputs.
2. **LMS Intern Portal Apply to Another Domain Panel**: `apps/portal/templates/portal.html` lines 689–709 (`<div class="panel" id="panel-applyanother">`). Takes up an entire navigation tab (`data-tab="applyanother"` in line 40) for a 3-field form. Once the user submits 3 applications, the tab permanently displays a static checkmark.
3. **LMS Intern Portal Unconfirmed Logout**: `apps/portal/templates/portal.html` line 57:
   `<button class="btn-logout-sb" data-act-click="doLogout"><i class="fas fa-sign-out-alt"></i> Logout</button>` and line 3868:
   `async function doLogout(){try{await fetch('/logout',{method:'POST',credentials:'include'});}catch(e){}window.location.href='/';}`
   Immediately logs the user out upon a single click with zero confirmation modal.
4. **Browser-Native `confirm()` Dialogs Across Portal Pages**:
   - `apps/portal/templates/session_booking.html:69`: `if (!confirm('Confirm booking for this 1-on-1 mentor session?')) return;`
   - `apps/portal/templates/company_dashboard.html:179` & `post_form.html:209`: `if(!confirm('Delete this post? Existing applicants will be kept...')) return;`
   - `apps/portal/templates/staff_task_queue.html:234`: `if (!confirm('Are you sure you want to mark task submission #${subId} as ${decision}?')) return;`
   - `apps/portal/templates/staff_project_queue.html:63`: `if (!confirm('Are you sure you want to mark submission #${subId} as ${decision}?')) return;`
   - `apps/portal/templates/admin.html:740, 1236, 1383, 1489, 1609, 1753, 1778`: native `confirm()` for deletions, removals, approvals, and resets.
5. **Marketing Website Program Checkout Form**: `apps/website/src/components/layout/ProgramDetailTemplate.tsx` lines 317–358:
   Inline checkout form (`<form onSubmit={handleCheckout} className={s.checkoutForm}>` with Name, Email, Phone, and `Enrol for {price}`) statically embedded in the sticky right sidebar. On mobile screens, this stacks underneath extensive syllabus modules.
6. **Marketing Website Demo Request Forms**: `apps/website/src/components/ui/DemoRequestForm.tsx`:
   Statically embedded at the bottom of 5 SaaS product pages (`/ai-solutions/products/intern-management-system`, `hiring-automation-suite`, `document-ai`, `dbert-chat`, `certificate-verification-api`).
7. **Marketing Website Admin Dossier Modal A11y Gaps**: `apps/website/src/app/admin/cohort-applications/CohortApplicationsClient.tsx` lines 308–330:
   Modal overlay lacks `role="dialog"`, `aria-modal="true"`, focus trapping, and Escape key dismissal.

---

## 2. Logic Chain

1. **Why the Password Reset Form Appears Broken / "Inline"**:
   - From **Observation 1.1**, the form is embedded directly into the DOM tree with `style="display:none;position:fixed;..."`.
   - From **Observation 1.3**, there are no CSS class rules in `dbert-theme.css` for `#forgotOverlay`. If the inline `display:none` is removed or modified, the form behaves as an un-styled inline block in the page layout.
   - From **Observation 1.2**, when triggered, `openForgotModal()` forcibly tears down `#authOverlay` by removing `.active`, and directly mutates `#forgotOverlay.style.display = 'flex'`. When dismissed, it invokes `showAuthOverlay('signin')`. There are no CSS transitions, no opacity or transform easing, and no focus return to the invoking trigger link.
   - Screen readers and keyboard users cannot navigate this reliably: pressing Tab allows focus to escape outside the dialog into inert background elements.

2. **Why Other Forms & Dialogs Cause Severe UX Degradation**:
   - In `apps/portal/templates/portal.html` (**Observation 1.4, Item 1 & 2**), dedicating full sidebar navigation tabs to minor 3-field forms ("Change Password" and "Apply to Another Domain") clutters the navigation bar and forces the intern out of their learning dashboard. Moving these into on-demand modal popups preserves user context and creates a cleaner dashboard experience.
   - In `portal.html` (**Observation 1.4, Item 3**), the absence of a confirmation modal on "Logout" poses a critical usability risk for mobile and tablet users who frequently touch near the bottom sidebar.
   - Across `session_booking.html`, `company_dashboard.html`, and `admin.html` (**Observation 1.4, Item 4**), native `confirm()` dialogs freeze the JavaScript execution thread, cannot be branded, and look visually obsolete compared to the rest of the DBERT design system.
   - In `apps/website` (**Observation 1.4, Item 5 & 6**), embedding checkout and demo request forms inline at the bottom of long pages increases abandonment rates on mobile devices. Modal popups triggered by sticky "Enrol Now" or "Book Demo" CTAs improve conversion and visual clarity.

---

## 3. Caveats

1. **Backend Exemption**: The backend route `/forgot-password` in `apps/portal/app.py` is fully functional and hardened with anti-enumeration (AUTH-002), honeypot checks, and dual IP/email rate limits. No backend API alterations are required.
2. **Read-Only Investigation**: In accordance with the Teamwork Explorer protocol, no direct code mutations have been executed in `apps/portal` or `apps/website`. Complete drop-in code snippets and implementation instructions are provided below for the implementer agent.

---

## 4. Conclusion & Technical Recommendations

### 4.1 Recommendation 1: Convert Password Reset Form to Unified DBERT Modal
Replace the inline-styled `#forgotOverlay` in `apps/portal/templates/index.html` with a modern semantic modal structure, add unified CSS classes to `apps/portal/static/css/dbert-theme.css`, and implement accessible focus trap and smooth scale/opacity animations.

#### Proposed HTML Markup (`apps/portal/templates/index.html` replacing lines 548–569):
```html
  <!-- MODAL: FORGOT / RESET PASSWORD (REPLACES INLINE FORGOTOVERLAY) -->
  <div id="forgotModal" class="dbert-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="forgotTitle" aria-describedby="forgotDesc" style="display:none;">
    <div class="dbert-modal-backdrop" data-act-click="closeForgotModal"></div>
    <div class="dbert-modal-container">
      <div class="dbert-modal-box">
        <!-- Close Button -->
        <button type="button" class="dbert-modal-close" data-act-click="closeForgotModal" aria-label="Close password reset dialog">
          <i class="fas fa-times" aria-hidden="true"></i>
        </button>

        <!-- Modal Header -->
        <div class="dbert-modal-header">
          <div class="dbert-modal-icon-badge">
            <i class="fas fa-key" aria-hidden="true"></i>
          </div>
          <h3 id="forgotTitle" class="dbert-modal-title">Reset your password</h3>
          <p id="forgotDesc" class="dbert-modal-desc">Enter your account email and we'll send a reset link if an account exists. The link expires in 1 hour.</p>
        </div>

        <!-- Feedback Alerts -->
        <div class="dbert-modal-alert dbert-alert-error" id="forgotError" role="alert" style="display:none;">
          <i class="fas fa-circle-exclamation" aria-hidden="true"></i>
          <span class="dbert-alert-text"></span>
        </div>

        <div class="dbert-modal-alert dbert-alert-success" id="forgotSuccess" role="status" aria-live="polite" style="display:none;">
          <div class="dbert-alert-header">
            <i class="fas fa-circle-check" aria-hidden="true"></i>
            <span id="forgotSuccessText"></span>
          </div>
          <div id="forgotDirectLink" style="display:none;"></div>
        </div>

        <!-- Form Area -->
        <form id="forgotForm" onsubmit="event.preventDefault(); submitForgot();" novalidate>
          <div id="forgotFormArea">
            <div class="form-group" style="margin-bottom:14px;">
              <label class="field-label" for="fp_email" style="display:block;margin-bottom:6px;">Account Email</label>
              <div class="input-wrap" style="position:relative;display:flex;align-items:center;">
                <i class="fas fa-envelope" aria-hidden="true" style="position:absolute;left:14px;color:#64748B;font-size:13px;pointer-events:none;"></i>
                <input type="email" id="fp_email" class="field-input" placeholder="you@example.com" autocomplete="email" required style="padding-left:38px !important;width:100%;" />
              </div>
            </div>

            <!-- Bot Honeypot -->
            <input type="text" name="company_website" id="fp_company_website" class="hp-field" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none !important;" />

            <div class="dbert-modal-actions">
              <button type="button" class="btn-modal-cancel" data-act-click="closeForgotModal">Cancel</button>
              <button type="submit" class="btn-modal-submit" id="forgotBtn">
                <span class="btn-label"><i class="fas fa-paper-plane" aria-hidden="true"></i> &nbsp;Send Reset Link</span>
                <span class="btn-spinner" aria-hidden="true"></span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
```

#### Proposed CSS Rules (Add to `apps/portal/static/css/dbert-theme.css`):
```css
/* ==========================================================================
   DBERT UNIFIED MODAL COMPONENT SYSTEM
   ========================================================================== */
.dbert-modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100000;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.22s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.22s;
}

.dbert-modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.dbert-modal-backdrop {
  position: absolute;
  inset: 0;
  background: rgba(9, 12, 20, 0.82);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  cursor: pointer;
}

.dbert-modal-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 460px;
  padding: 16px;
  box-sizing: border-box;
  pointer-events: none;
}

.dbert-modal-box {
  pointer-events: auto;
  background: #0E111A;
  color: #FFFFFF;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);
  padding: 28px 26px;
  position: relative;
  transform: scale(0.95) translateY(10px);
  transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
}

.dbert-modal-overlay.active .dbert-modal-box {
  transform: scale(1) translateY(0);
}

.dbert-modal-close {
  position: absolute;
  top: 18px;
  right: 18px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.05);
  color: #8E9AA8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.15s ease;
}

.dbert-modal-close:hover {
  background: rgba(255, 255, 255, 0.15);
  color: #FFFFFF;
  transform: scale(1.05);
}

.dbert-modal-close:focus-visible {
  outline: 2px solid #2563EB;
  outline-offset: 2px;
}

.dbert-modal-header {
  margin-bottom: 20px;
  padding-right: 28px;
}

.dbert-modal-icon-badge {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(37,99,235,0.2), rgba(37,99,235,0.08));
  border: 1px solid rgba(37,99,235,0.3);
  color: #3B82F6;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-bottom: 14px;
}

.dbert-modal-title {
  font-size: 19px;
  font-weight: 800;
  margin: 0 0 6px;
  line-height: 1.3;
  color: #FFFFFF;
}

.dbert-modal-desc {
  font-size: 13px;
  color: #8E9AA8;
  line-height: 1.6;
  margin: 0;
}

.dbert-modal-alert {
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  padding: 11px 15px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.dbert-alert-error {
  background: rgba(220, 38, 38, 0.15);
  border: 1px solid rgba(220, 38, 38, 0.3);
  color: #F87171;
}

.dbert-alert-success {
  background: rgba(34, 197, 94, 0.12);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #22C55E;
  flex-direction: column;
  align-items: stretch;
}

.dbert-alert-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dbert-modal-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 20px;
}

.btn-modal-cancel {
  flex: 0 0 auto;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.14);
  color: #CBD5E1;
  font-weight: 700;
  font-size: 13px;
  padding: 10px 18px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-modal-cancel:hover {
  background: rgba(255, 255, 255, 0.16);
  color: #FFFFFF;
}

.btn-modal-submit {
  flex: 1;
  background: #2563EB;
  color: #FFFFFF;
  font-weight: 800;
  font-size: 13.5px;
  border: none;
  border-radius: 999px;
  padding: 10px 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
  transition: all 0.15s ease;
}

.btn-modal-submit:hover:not(:disabled) {
  background: #1D4ED8;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45);
}

.btn-modal-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
```

#### Proposed JavaScript Controller (`apps/portal/templates/index.html` lines 645–685):
```javascript
  // ── FORGOT PASSWORD MODAL CONTROLLER (WITH FOCUS TRAP & WCAG A11Y) ──
  let _lastActiveTrigger = null;

  function openForgotModal() {
    _lastActiveTrigger = document.activeElement;
    const modal = document.getElementById('forgotModal');
    if (!modal) return;

    const authOv = document.getElementById('authOverlay');
    if (authOv && authOv.classList.contains('active')) {
      authOv.classList.remove('active');
      modal.dataset.returnToAuth = 'true';
    }

    document.getElementById('forgotError').style.display = 'none';
    document.getElementById('forgotSuccess').style.display = 'none';
    document.getElementById('forgotFormArea').style.display = 'block';
    setLoading('forgotBtn', false);

    const emailInput = document.getElementById('fp_email');
    emailInput.value = _siEmail || document.getElementById('si_email')?.value.trim() || '';

    modal.style.display = 'flex';
    void modal.offsetWidth; // Force reflow
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    setTimeout(() => emailInput.focus(), 80);
  }

  function closeForgotModal() {
    const modal = document.getElementById('forgotModal');
    if (!modal) return;

    modal.classList.remove('active');
    document.body.style.overflow = '';

    setTimeout(() => {
      modal.style.display = 'none';
      if (modal.dataset.returnToAuth === 'true') {
        delete modal.dataset.returnToAuth;
        showAuthOverlay('signin');
      } else if (_lastActiveTrigger && typeof _lastActiveTrigger.focus === 'function') {
        _lastActiveTrigger.focus();
      }
    }, 220);
  }

  function showForgotError(msg) {
    const el = document.getElementById('forgotError');
    el.querySelector('.dbert-alert-text').textContent = msg;
    el.style.display = 'flex';
  }

  async function submitForgot() {
    document.getElementById('forgotError').style.display = 'none';
    const email = document.getElementById('fp_email').value.trim().toLowerCase();
    if (!email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      showForgotError('Please enter a valid email address.');
      return;
    }
    setLoading('forgotBtn', true);
    try {
      const res = await fetch('/forgot-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ email, company_website: document.getElementById('fp_company_website').value })
      });
      const data = await res.json();
      if (data.status === 'success') {
        document.getElementById('forgotFormArea').style.display = 'none';
        document.getElementById('forgotSuccessText').textContent = data.message || 'Password reset link has been sent to your email.';
        const directEl = document.getElementById('forgotDirectLink');
        if (data.reset_url && directEl) {
          directEl.style.display = 'block';
          directEl.innerHTML = `<div style="background:rgba(37,99,235,0.12);border:1px solid rgba(37,99,235,0.3);border-radius:8px;padding:10px 12px;margin-top:8px;font-size:12px;"><span style="color:#60A5FA;font-weight:800;">Password Reset Link:</span><br/><a href="${data.reset_url}" style="color:#FFFFFF;text-decoration:underline;word-break:break-all;font-weight:600;display:inline-block;margin-top:4px;">Open Password Reset Page &rarr;</a></div>`;
        }
        document.getElementById('forgotSuccess').style.display = 'flex';
      } else {
        showForgotError(data.message || 'Unable to process reset request. Please check your email or Sign Up.');
        setLoading('forgotBtn', false);
      }
    } catch (e) {
      showForgotError('Network error. Please try again.');
      setLoading('forgotBtn', false);
    }
  }

  // Keyboard navigation & Focus Trapping for Modal
  document.addEventListener('keydown', e => {
    const modal = document.getElementById('forgotModal');
    if (!modal || !modal.classList.contains('active')) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      closeForgotModal();
      return;
    }

    if (e.key === 'Tab') {
      const focusables = Array.from(modal.querySelectorAll(
        'button:not([disabled]), input:not([disabled]):not([type="hidden"]), a[href], [tabindex]:not([tabindex="-1"])'
      ));
      if (focusables.length === 0) return;
      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });
```

---

### 4.2 Recommendation 2: Universal `DbertConfirmModal` to Replace Browser-Native `confirm()`
Implement an asynchronous, styled confirmation dialog component for all portal confirmation needs.

#### Markup:
```html
<div id="dbertConfirmModal" class="dbert-modal-overlay" role="alertdialog" aria-modal="true" aria-labelledby="confirmTitle" aria-describedby="confirmDesc" style="display:none;">
  <div class="dbert-modal-backdrop" onclick="DbertConfirm.cancel()"></div>
  <div class="dbert-modal-container" style="max-width:420px;">
    <div class="dbert-modal-box" style="text-align:center;padding:26px 22px;">
      <div id="confirmIconWrap" class="dbert-modal-icon-badge" style="margin:0 auto 14px;">
        <i id="confirmIcon" class="fas fa-triangle-exclamation"></i>
      </div>
      <h3 id="confirmTitle" class="dbert-modal-title" style="font-size:18px;">Confirm Action</h3>
      <p id="confirmDesc" class="dbert-modal-desc" style="margin-bottom:22px;"></p>
      <div class="dbert-modal-actions" style="justify-content:center;">
        <button type="button" class="btn-modal-cancel" onclick="DbertConfirm.cancel()" id="confirmCancelBtn">Cancel</button>
        <button type="button" class="btn-modal-submit" onclick="DbertConfirm.proceed()" id="confirmActionBtn" style="flex:none;min-width:120px;">Confirm</button>
      </div>
    </div>
  </div>
</div>
```

#### JavaScript Service:
```javascript
const DbertConfirm = (function() {
  let _resolve = null;

  function show({ title = 'Confirm Action', message, confirmText = 'Confirm', cancelText = 'Cancel', variant = 'danger' }) {
    return new Promise(resolve => {
      _resolve = resolve;
      document.getElementById('confirmTitle').textContent = title;
      document.getElementById('confirmDesc').textContent = message;
      document.getElementById('confirmActionBtn').textContent = confirmText;
      document.getElementById('confirmCancelBtn').textContent = cancelText;

      const badge = document.getElementById('confirmIconWrap');
      const icon = document.getElementById('confirmIcon');
      const btn = document.getElementById('confirmActionBtn');

      if (variant === 'danger') {
        badge.style.background = 'rgba(220,38,38,0.15)';
        badge.style.color = '#F87171';
        badge.style.borderColor = 'rgba(220,38,38,0.3)';
        icon.className = 'fas fa-trash-can';
        btn.style.background = '#DC2626';
      } else {
        badge.style.background = 'rgba(37,99,235,0.15)';
        badge.style.color = '#60A5FA';
        badge.style.borderColor = 'rgba(37,99,235,0.3)';
        icon.className = 'fas fa-circle-question';
        btn.style.background = '#2563EB';
      }

      const modal = document.getElementById('dbertConfirmModal');
      modal.style.display = 'flex';
      void modal.offsetWidth;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
      document.getElementById('confirmActionBtn').focus();
    });
  }

  function proceed() {
    close();
    if (_resolve) _resolve(true);
    _resolve = null;
  }

  function cancel() {
    close();
    if (_resolve) _resolve(false);
    _resolve = null;
  }

  function close() {
    const modal = document.getElementById('dbertConfirmModal');
    if (modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
      setTimeout(() => { modal.style.display = 'none'; }, 220);
    }
  }

  return { show, proceed, cancel };
})();
```

---

### 4.3 Recommendation 3: Convert LMS Dashboard "Change Password" and "Apply Domain" to Modals
In `apps/portal/templates/portal.html`:
1. Remove tabs `password` and `applyanother` from the primary sidebar strip (`lines 39 & 40`).
2. Move the forms from panels into accessible modal dialogs (`changePasswordModal` and `applyDomainModal`).
3. Add trigger buttons in the intern profile header or user avatar menu.

---

### 4.4 Recommendation 4: React Next.js Reusable Modal Component (`apps/website`)
For `apps/website`, implement a clean React component in `apps/website/src/components/ui/Modal.tsx`:
```tsx
'use client';

import React, { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { X } from 'lucide-react';
import s from './modal.module.css';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  description?: string;
  children: React.ReactNode;
  maxWidth?: string;
}

export default function Modal({ isOpen, onClose, title, description, children, maxWidth = '500px' }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;
    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKeydown);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleKeydown);
      document.body.style.overflow = '';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div className={s.overlay} role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <div className={s.backdrop} onClick={onClose} />
      <div className={s.container} style={{ maxWidth }}>
        <div className={s.box} ref={modalRef}>
          <button className={s.closeBtn} onClick={onClose} aria-label="Close dialog">
            <X size={18} />
          </button>
          <div className={s.header}>
            <h3 id="modal-title" className={s.title}>{title}</h3>
            {description && <p className={s.desc}>{description}</p>}
          </div>
          <div className={s.content}>{children}</div>
        </div>
      </div>
    </div>,
    document.body
  );
}
```

---

## 5. Verification Method

### 5.1 Static Verification Commands
Run grep to verify references to old `forgotOverlay` inline styles:
```powershell
rg "forgotOverlay" apps/portal/templates/index.html
```

### 5.2 Functional Testing Steps
1. Navigate to `http://localhost:5001/` (or LMS home route).
2. Click "Sign In" in top navigation bar to open `#authOverlay`.
3. Click "Forgot password?" link on the sign-in step.
4. **Verify**:
   - `#forgotModal` emerges smoothly with backdrop blur and subtle scaling animation.
   - Background scrolling on body is locked (`document.body.style.overflow === 'hidden'`).
   - `#fp_email` is automatically focused.
   - Pressing `Escape` or clicking the backdrop dismisses the modal and restores `#authOverlay`.
   - Pressing `Tab` cycles focus solely between the email input, Cancel button, Send Reset Link button, and Close button without escaping to background elements.
   - Submitting an empty or invalid email displays inline alert `.dbert-alert-error`.
   - Submitting a valid test email returns neutral success response in `.dbert-alert-success`.

### 5.3 Automated Regression Tests
Run the portal test suite to ensure no regressions in auth workflows:
```powershell
python -m pytest apps/portal/tests/test_auth_routes.py -v
```
