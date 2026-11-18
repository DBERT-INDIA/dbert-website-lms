import re

with open('apps/portal/templates/portal_offer_letter.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update Top Action Button (around lines 890-917)
old_top_action = """        <div>
          {% if preview_mode %}
            {% if enrollment and (enrollment.utr or enrollment.payment_status in ('Pending', 'Submitted', 'Under Review')) %}
            <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20have%20submitted%20my%20%E2%82%B9499%20caution%20deposit%20(UTR%3A%20{{ enrollment.utr }})%20for%20Offer%20{{ offer.offer_letter_id }}.%20Kindly%20verify." target="_blank" class="btn-gold" style="background:#25D366; color:#ffffff !important; padding:14px 26px; font-size:15px; font-weight:900; box-shadow:0 6px 20px rgba(37,211,102,0.45); border-radius:10px;">
              <i class="fa-brands fa-whatsapp" style="font-size:18px;"></i> Expedite Verification &rarr;
            </a>
            {% else %}
            <a href="#signature-section" class="btn-gold btn-gold-pulse" id="btnConfirmSeatTop" style="padding:14px 28px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 6px 22px rgba(245, 158, 11, 0.55); border-radius:10px;">
              <i class="fa-solid fa-credit-card" style="font-size:17px;"></i> <span>Confirm Seat &amp; Pay ₹499 Now &darr;</span>
            </a>
            {% endif %}
          {% elif offer.pdf_unlocked %}
          <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <button type="button" class="btn-gold" id="btnPrintOfferTop" style="padding:14px 26px; font-size:15px; font-weight:900; box-shadow:0 6px 20px rgba(245, 158, 11, 0.45); border-radius:10px;">
              <i class="fa-solid fa-file-pdf" style="font-size:17px;"></i> Download Official Signed PDF
            </button>
            <a href="/portal" class="btn-secondary" style="padding:14px 22px; font-size:14px; font-weight:700; border-radius:10px;">
              <i class="fa-solid fa-laptop-code"></i> LMS Sprints &rarr;
            </a>
          </div>
          {% else %}
          <a href="#signature-section" class="btn-emerald btn-gold-pulse" id="btnReviewSignTop" style="padding:14px 28px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; border-radius:10px;">
            <i class="fa-solid fa-file-signature" style="font-size:18px;"></i> Review &amp; Sign Offer Agreement &darr;
          </a>
          {% endif %}
        </div>"""

new_top_action = """        <div>
          {% if not is_signed %}
          <a href="#signature-section" class="btn-emerald btn-gold-pulse" id="btnReviewSignTop" style="padding:14px 28px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; border-radius:10px;">
            <i class="fa-solid fa-file-signature" style="font-size:18px;"></i> <span>Review &amp; Sign Offer Agreement &darr;</span>
          </a>
          {% elif not is_deposit_verified %}
            {% if enrollment and (enrollment.utr or enrollment.payment_status in ('Pending', 'Submitted', 'Under Review')) %}
            <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20have%20submitted%20my%20%E2%82%B9499%20caution%20deposit%20(UTR%3A%20{{ enrollment.utr }})%20for%20Offer%20{{ offer.offer_letter_id }}.%20Kindly%20verify." target="_blank" class="btn-whatsapp" style="padding:14px 26px; font-size:15px; font-weight:900; border-radius:10px;">
              <i class="fa-brands fa-whatsapp" style="font-size:18px;"></i> Expedite Verification &rarr;
            </a>
            {% else %}
            <a href="#signature-section" class="btn-gold btn-gold-pulse" id="btnConfirmSeatTop" style="padding:14px 28px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 6px 22px rgba(245, 158, 11, 0.55); border-radius:10px;">
              <i class="fa-solid fa-credit-card" style="font-size:17px;"></i> <span>Confirm Seat &amp; Pay ₹499 Now &darr;</span>
            </a>
            {% endif %}
          {% else %}
          <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <button type="button" class="btn-gold" id="btnPrintOfferTop" style="padding:14px 26px; font-size:15px; font-weight:900; box-shadow:0 6px 20px rgba(245, 158, 11, 0.45); border-radius:10px;">
              <i class="fa-solid fa-file-pdf" style="font-size:17px;"></i> Download Official Signed PDF
            </button>
            <a href="/portal" class="btn-secondary" style="padding:14px 22px; font-size:14px; font-weight:700; border-radius:10px;">
              <i class="fa-solid fa-laptop-code"></i> LMS Sprints &rarr;
            </a>
          </div>
          {% endif %}
        </div>"""

assert old_top_action in c, "old_top_action not found"
c = c.replace(old_top_action, new_top_action)

# 2. Update Three-Step Progress Stepper
old_stepper = """      <!-- 2. THREE-STEP PROGRESS STEPPER -->
      <div class="no-print offer-stepper-card" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:16px 22px; margin-bottom:22px; display:flex; align-items:center; justify-content:space-between; gap:16px; box-shadow:0 2px 8px rgba(0, 0, 0, 0.04);">
        <!-- Step 1: Selection & Terms -->
        <div class="step-item step-completed" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:#10b981; color:#ffffff;">
            <i class="fa-solid fa-check"></i>
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:#10b981;">
              Step 1 Done
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Selected &amp; Terms Preview</span>
          </div>
        </div>

        <div class="step-divider" style="width:48px; height:2px; background:#e2e8f0; flex-shrink:0;"></div>

        <!-- Step 2: Confirm Seat (₹499) -->
        <div class="step-item {% if not preview_mode %}step-completed{% else %}step-active{% endif %}" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:{% if not preview_mode %}#10b981{% else %}#d97706{% endif %}; color:#ffffff; {% if preview_mode %}box-shadow:0 0 0 3px rgba(217, 119, 6, 0.2);{% endif %}">
            {% if not preview_mode %}<i class="fa-solid fa-check"></i>{% else %}2{% endif %}
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:{% if not preview_mode %}#10b981{% else %}#d97706{% endif %};">
              {% if not preview_mode %}Step 2 Reconciled{% else %}Action Required{% endif %}
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Confirm Seat (₹499 Deposit)</span>
          </div>
        </div>

        <div class="step-divider" style="width:48px; height:2px; background:#e2e8f0; flex-shrink:0;"></div>

        <!-- Step 3: Digital Signature & Official PDF -->
        <div class="step-item {% if offer.pdf_unlocked %}step-completed{% elif not preview_mode %}step-active{% else %}step-pending{% endif %}" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:{% if offer.pdf_unlocked %}#10b981{% elif not preview_mode %}#d97706{% else %}#f1f5f9{% endif %}; color:{% if offer.pdf_unlocked or not preview_mode %}#ffffff{% else %}#94a3b8{% endif %}; {% if preview_mode %}border:1px solid #cbd5e1;{% elif not offer.pdf_unlocked %}box-shadow:0 0 0 3px rgba(217, 119, 6, 0.2);{% endif %}">
            {% if offer.pdf_unlocked %}<i class="fa-solid fa-shield-halved"></i>{% else %}3{% endif %}
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:{% if offer.pdf_unlocked %}#10b981{% elif not preview_mode %}#d97706{% else %}#94a3b8{% endif %};">
              {% if offer.pdf_unlocked %}Official Executed{% elif not preview_mode %}Ready to Sign{% else %}Locked{% endif %}
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Digital Signature &amp; Official PDF</span>
          </div>
        </div>
      </div>"""

new_stepper = """      <!-- 2. THREE-STEP PROGRESS STEPPER (Read & Sign First, Deposit Second) -->
      <div class="no-print offer-stepper-card" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:16px 22px; margin-bottom:22px; display:flex; align-items:center; justify-content:space-between; gap:16px; box-shadow:0 2px 8px rgba(0, 0, 0, 0.04);">
        <!-- Step 1: Selection & Terms -->
        <div class="step-item step-completed" id="stepperStep1" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:#10b981; color:#ffffff;">
            <i class="fa-solid fa-check"></i>
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:#10b981;">
              Step 1 Done
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Selection &amp; Terms Preview</span>
          </div>
        </div>

        <div class="step-divider" style="width:48px; height:2px; background:#e2e8f0; flex-shrink:0;"></div>

        <!-- Step 2: Review & Digital Signature -->
        <div class="step-item {% if is_signed %}step-completed{% else %}step-active{% endif %}" id="stepperStep2" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:{% if is_signed %}#10b981{% else %}#d97706{% endif %}; color:#ffffff; {% if not is_signed %}box-shadow:0 0 0 3px rgba(217, 119, 6, 0.2);{% endif %}">
            {% if is_signed %}<i class="fa-solid fa-check"></i>{% else %}2{% endif %}
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:{% if is_signed %}#10b981{% else %}#d97706{% endif %};">
              {% if is_signed %}Step 2 Done{% else %}Action Required{% endif %}
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Review &amp; Digital Signature</span>
          </div>
        </div>

        <div class="step-divider" style="width:48px; height:2px; background:#e2e8f0; flex-shrink:0;"></div>

        <!-- Step 3: Workstation Seat Confirmation (₹499 Deposit) -->
        <div class="step-item {% if is_deposit_verified %}step-completed{% elif is_signed %}step-active{% else %}step-pending{% endif %}" id="stepperStep3" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:{% if is_deposit_verified %}#10b981{% elif is_signed %}#d97706{% else %}#f1f5f9{% endif %}; color:{% if is_deposit_verified or is_signed %}#ffffff{% else %}#94a3b8{% endif %}; {% if not is_signed %}border:1px solid #cbd5e1;{% elif not is_deposit_verified %}box-shadow:0 0 0 3px rgba(217, 119, 6, 0.2);{% endif %}">
            {% if is_deposit_verified %}<i class="fa-solid fa-shield-halved"></i>{% else %}3{% endif %}
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:{% if is_deposit_verified %}#10b981{% elif is_signed %}#d97706{% else %}#94a3b8{% endif %};">
              {% if is_deposit_verified %}Step 3 Reconciled{% elif is_signed %}Action Required{% else %}Pending Signature{% endif %}
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Confirm Seat (₹499 Deposit)</span>
          </div>
        </div>
      </div>"""

assert old_stepper in c, "old_stepper not found"
c = c.replace(old_stepper, new_stepper)

# 3. Update the Signature & Seat Confirmation Section (#signature-section)
# Find the entire #signature-section block
sig_section_start = c.find('<div class="no-print signature-box-wrapper')
sig_section_end = c.find('</div>\n\n    </div>\n  </main>', sig_section_start)
assert sig_section_start != -1 and sig_section_end != -1, "signature-section boundaries not found"

new_sig_section = """<div class="no-print signature-box-wrapper {% if is_signed and is_deposit_verified %}signed-state{% endif %}" id="signature-section" style="background:{% if is_signed and is_deposit_verified %}linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%){% else %}#ffffff{% endif %}; border:1px solid #cbd5e1; border-top:4px solid {% if is_signed and is_deposit_verified %}#10b981{% elif is_signed %}#d97706{% else %}#2563eb{% endif %}; border-radius:12px; padding:26px 30px; margin-bottom:26px; box-shadow:0 8px 20px -4px rgba(0, 0, 0, 0.06);">

        <!-- A. SIGNED CONFIRMATION BANNER (Visible if signed, or revealed dynamically on signing) -->
        <div id="signedBanner" style="display:{% if is_signed %}flex{% else %}none{% endif %}; background:#f0fdf4; border:1.5px solid #86efac; border-radius:10px; padding:16px 20px; margin-bottom:20px; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
          <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#10b981; color:#ffffff; display:flex; align-items:center; justify-content:center; font-size:16px;">
              <i class="fa-solid fa-check"></i>
            </div>
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.8px; color:#15803d;">
                STEP 2 COMPLETE: APPOINTMENT AGREEMENT DIGITALLY SIGNED
              </div>
              <div style="font-size:14px; font-weight:800; color:#0f172a; margin-top:2px;">
                Digitally Executed by <strong id="dispSigName">{{ offer.signature_name or offer.name }}</strong> on <span id="dispSigTs">{{ offer.accepted_at or 'Today' }}</span>
              </div>
            </div>
          </div>
          <span style="font-size:12px; font-weight:700; color:#15803d; background:#dcfce7; padding:4px 10px; border-radius:6px; border:1px solid #86efac;">
            <i class="fa-solid fa-shield-halved"></i> Audit Verified
          </span>
        </div>

        <!-- B. DIGITAL SIGNATURE FORM (Visible when NOT signed yet) -->
        <div id="digitalSignatureCard" style="display:{% if not is_signed %}block{% else %}none{% endif %};">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#dbeafe; color:#1d4ed8; display:flex; align-items:center; justify-content:center; font-size:16px;">
              <i class="fa-solid fa-pen-nib"></i>
            </div>
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.8px; color:#1d4ed8;">
                STEP 2: DIGITAL ACCEPTANCE &amp; LEGAL EXECUTION
              </div>
              <h3 style="margin:2px 0 0; font-size:18px; font-weight:900; color:#0f172a; font-family:'Georgia', serif;">
                Review &amp; Execute Appointment Agreement Digitally
              </h3>
            </div>
          </div>

          <form id="offerSignForm" style="margin-top:12px;">
            <p style="font-size:13.5px; color:#475569; line-height:1.65; margin:0 0 16px;">
              Please review all sections of the appointment letter above. To execute this appointment agreement and secure your seat in the <strong>{{ offer.domain }}</strong> cohort commencing on <strong>{{ offer.batch_start_date }}</strong>, enter your full legal name below to append your legally binding digital signature:
            </p>

            <div class="sig-input-group" style="margin:16px 0; max-width:500px;">
              <label for="sigNameInput" class="sig-input-label" style="display:block; font-size:12px; font-weight:800; color:#334155; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:8px;">Full Legal Name (Digital Signature) *</label>
              <input type="text" id="sigNameInput" placeholder="e.g. {{ offer.name }}" value="{{ offer.name }}" required class="sig-input-field" style="width:100%; padding:14px 16px; border:2px solid #cbd5e1; border-radius:8px; font-size:16px; font-weight:700; color:#0f172a; background:#ffffff; box-sizing:border-box;">
            </div>

            <label class="terms-acceptance-card" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px 18px; margin-bottom:20px; display:flex; align-items:flex-start; gap:14px; cursor:pointer;">
              <input type="checkbox" id="agreeCheckbox" required style="width:18px; height:18px; margin-top:2px; accent-color:#d97706; cursor:pointer; flex-shrink:0;">
              <span class="terms-acceptance-text" style="font-size:13px; line-height:1.6; color:#334155;">
                I, <strong>{{ offer.name }}</strong>, have read, understood, and accept all terms of this Appointment Agreement, including the <strong>2-month remote tenure</strong>, the <strong>₹5,000 fixed milestone stipend</strong> (minimum 10 hrs/week login, 2 LMS course certifications, 75 bounty tasks), the <strong>up to ₹18,000 performance-based variable incentive</strong>, the ₹499 caution deposit refund policy, confidentiality, and intellectual property terms.
              </span>
            </label>

            <div id="signAlertBox" style="display:none; padding:12px 16px; border-radius:8px; font-size:13.5px; font-weight:600; margin-bottom:18px;"></div>

            <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
              <button type="submit" id="signSubmitBtn" class="na-cta-btn na-btn-gold" style="font-size:15px; padding:15px 32px;">
                <i class="fa-solid fa-signature" style="font-size:18px;"></i> Sign &amp; Accept Appointment Agreement &rarr;
              </button>
              <span style="font-size:12px; color:#64748b;">
                <i class="fa-solid fa-lock"></i> Binding digital signature recorded under Indian IT Act, 2000.
              </span>
            </div>
          </form>
        </div>

        <!-- C. SEAT CONFIRMATION & ₹499 CAUTION DEPOSIT SECTION (Revealed after signing if deposit pending) -->
        <div id="postSignPaymentSection" style="display:{% if is_signed and not is_deposit_verified %}block{% else %}none{% endif %}; margin-top:{% if is_signed %}0{% else %}20px{% endif %};">
          {% if enrollment and (enrollment.utr or enrollment.payment_status in ('Pending', 'Submitted', 'Under Review')) %}
          <!-- UTR Submitted State -->
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#dbeafe; color:#1d4ed8; display:flex; align-items:center; justify-content:center; font-size:16px;">
              <i class="fa-solid fa-hourglass-half fa-spin"></i>
            </div>
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.8px; color:#1d4ed8;">
                STEP 3: CAUTION DEPOSIT SUBMITTED
              </div>
              <h3 style="margin:2px 0 0; font-size:18px; font-weight:900; color:#0f172a; font-family:'Georgia', serif;">
                ₹499 Caution Deposit Under Administrative Verification
              </h3>
            </div>
          </div>
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:18px 22px; margin-bottom:18px; font-size:13.5px; color:#334155; line-height:1.6;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
              <span style="color:#64748b; font-weight:600;">Recorded 12-Digit UTR:</span>
              <code style="font-weight:800; color:#0f172a; background:#e2e8f0; padding:3px 10px; border-radius:4px; font-size:13.5px;">{{ enrollment.utr or 'Submitted via Admissions' }}</code>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
              <span style="color:#64748b; font-weight:600;">Admissions Ledger Status:</span>
              <span style="color:#d97706; font-weight:800;"><i class="fa-solid fa-clock"></i> Pending Bank Reconciliation (Estimated: 2–4 Hours)</span>
            </div>
            <p style="margin:10px 0 0; font-size:12.5px; color:#64748b;">
              Your deposit transaction has been registered in the DBERT admissions ledger. Upon administrative verification, official executive A4 PDF download is unlocked.
            </p>
          </div>
          <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20have%20submitted%20my%20%E2%82%B9499%20caution%20deposit%20(UTR%3A%20{{ enrollment.utr }})%20for%20Offer%20{{ offer.offer_letter_id }}.%20Kindly%20verify." target="_blank" class="btn-whatsapp" style="padding:13px 24px; border-radius:10px; text-decoration:none; display:inline-flex; align-items:center; gap:8px;">
              <i class="fa-brands fa-whatsapp"></i> Expedite Verification via WhatsApp &rarr;
            </a>
            <button type="button" onclick="window.location.reload();" class="btn-secondary" style="padding:13px 20px; border-radius:10px; cursor:pointer;">
              <i class="fa-solid fa-rotate"></i> Refresh Status
            </button>
          </div>
          {% else %}
          <!-- Payment QR + 1-Tap UPI Launchers + UTR Form (NO 1999 LINK!) -->
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#fef3c7; color:#b45309; display:flex; align-items:center; justify-content:center; font-size:16px;">
              <i class="fa-solid fa-credit-card"></i>
            </div>
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.8px; color:#b45309;">
                STEP 3: WORKSTATION SEAT CONFIRMATION
              </div>
              <h3 style="margin:2px 0 0; font-size:18px; font-weight:900; color:#0f172a; font-family:'Georgia', serif;">
                Confirm Your Workstation Seat with ₹499 Refundable Caution Deposit
              </h3>
            </div>
          </div>
          <p style="font-size:13.5px; color:#475569; line-height:1.65; margin:0 0 16px;">
            Your appointment agreement is digitally executed. Per Section 5 of your appointment terms, a refundable caution deposit of <strong>₹499</strong> confirms your workstation sandbox, assigns your dedicated technical mentor, and unlocks your official executive A4 signed PDF download. <em>(100% credited / refundable upon sprint completion).</em>
          </p>

          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-bottom:20px; align-items:stretch;">
            <!-- Left: QR Code & 1-Tap UPI Launchers -->
            <div style="background:#0b1120; border:1px solid #1e293b; border-radius:12px; padding:20px; color:#ffffff; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 6px 18px rgba(0,0,0,0.25);">
              <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                  <span style="font-size:11px; font-weight:800; letter-spacing:0.8px; text-transform:uppercase; color:#fbbf24; display:flex; align-items:center; gap:6px;">
                    <i class="fa-solid fa-qrcode"></i> Scan &amp; Pay ₹499
                  </span>
                  <span style="font-size:11px; font-weight:700; background:rgba(16,185,129,0.2); color:#34d399; border:1px solid #10b981; padding:3px 8px; border-radius:6px;">
                    100% Refundable
                  </span>
                </div>

                <!-- QR Display -->
                <div style="text-align:center; padding:12px; background:#ffffff; border-radius:10px; margin-bottom:14px; display:inline-block; width:100%; box-sizing:border-box;">
                  <img src="/static/img/qrcode.jpeg" alt="DBERT Admissions ₹499 UPI QR" style="width:170px; height:170px; object-fit:contain; display:block; margin:0 auto;" onerror="this.onerror=null; this.src='/static/qr.jpg';">
                  <div style="font-size:11px; font-weight:800; color:#0f172a; margin-top:6px; letter-spacing:0.5px; text-transform:uppercase;">
                    Scan with GPay · PhonePe · Paytm · BHIM
                  </div>
                </div>

                <div style="font-size:12px; color:#94a3b8; text-align:center; margin-bottom:12px;">
                  Merchant VPA: <strong style="color:#ffffff; font-family:monospace;">Q652429146@ybl</strong> (DBERT Admissions)
                </div>
              </div>

              <!-- 1-Tap Mobile UPI Buttons -->
              <div>
                <div style="font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;">
                  <i class="fa-solid fa-bolt" style="color:#fbbf24;"></i> Mobile 1-Tap Fast Pay:
                </div>
                <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:8px;">
                  <a href="intent://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}#Intent;scheme=upi;package=com.google.android.apps.nbu.paisa.user;end" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:10px; background:#18181b; border:1px solid #3f3f46; border-radius:8px; color:#ffffff !important; text-decoration:none; font-size:13px; font-weight:700;">
                    <i class="fab fa-google-pay" style="font-size:18px; color:#4285F4;"></i> GPay
                  </a>
                  <a href="phonepe://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:10px; background:#5f259f; border:1px solid #7c3aed; border-radius:8px; color:#ffffff !important; text-decoration:none; font-size:13px; font-weight:700;">
                    <i class="fas fa-mobile-screen" style="font-size:13px; color:#ffffff;"></i> PhonePe
                  </a>
                  <a href="paytmmp://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:10px; background:#002970; border:1px solid #00baf2; border-radius:8px; color:#ffffff !important; text-decoration:none; font-size:13px; font-weight:700;">
                    <i class="fas fa-wallet" style="font-size:13px; color:#00baf2;"></i> Paytm
                  </a>
                  <a href="upi://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:10px; background:#1e293b; border:1px solid #d97706; border-radius:8px; color:#ffffff !important; text-decoration:none; font-size:13px; font-weight:700;">
                    <i class="fas fa-qrcode" style="font-size:13px; color:#fbbf24;"></i> Any UPI
                  </a>
                </div>
              </div>
            </div>

            <!-- Right: UTR Form -->
            <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:12px; padding:24px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 6px 18px rgba(0,0,0,0.04);">
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                  <span style="width:26px; height:26px; border-radius:50%; background:#d97706; color:#ffffff; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800;">
                    2
                  </span>
                  <span style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.7px; color:#0f172a;">
                    Submit UTR for Instant Seat Reconciliation
                  </span>
                </div>

                <p style="font-size:13px; color:#475569; line-height:1.6; margin:0 0 16px;">
                  After completing your ₹499 transfer via QR code or UPI app, copy the <strong>12-Digit Bank UTR / UPI Reference Number</strong> and submit below to secure your seat.
                </p>

                <form id="depositSubmitForm">
                  <div class="sig-input-group" style="margin-bottom:16px;">
                    <label for="depositUtrInput" class="sig-input-label" style="display:block; font-size:12px; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:8px;">
                      12-Digit Bank UTR / UPI Ref Number *
                    </label>
                    <input type="text" id="depositUtrInput" name="utr_number" maxlength="12" pattern="\\d{12}" placeholder="e.g. 679862090077" required class="sig-input-field" style="width:100%; padding:14px 16px; border:2px solid #cbd5e1; border-radius:8px; font-size:16px; font-weight:700; font-family:monospace; color:#0f172a; background:#ffffff; box-sizing:border-box; letter-spacing:1.5px;">
                    <p style="font-size:11.5px; color:#64748b; margin:6px 0 0;">
                      <i class="fa-solid fa-circle-info"></i> Found in transaction receipt on GPay, PhonePe, Paytm, or bank SMS.
                    </p>
                  </div>

                  <input type="hidden" name="domain" value="{{ offer.domain }}">
                  <input type="hidden" name="joining_date" value="{{ offer.batch_start_date }}">

                  <div id="depositAlertBox" style="display:none; padding:12px 16px; border-radius:8px; font-size:13.5px; font-weight:600; margin-bottom:16px;"></div>

                  <button type="submit" id="depositSubmitBtn" class="na-cta-btn na-btn-gold" style="width:100%; justify-content:center; padding:15px 24px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; border-radius:10px;">
                    <i class="fa-solid fa-circle-check" style="font-size:18px;"></i> Submit UTR for Admin Verification &rarr;
                  </button>
                </form>
              </div>

              <div style="margin-top:16px; padding-top:14px; border-top:1px solid #e2e8f0; font-size:12px; color:#64748b; display:flex; align-items:center; gap:8px;">
                <i class="fa-solid fa-shield-halved" style="color:#10b981; font-size:15px;"></i>
                <span>Automated ledger reconciliation &bull; Unlocks official PDF download upon admin check.</span>
              </div>
            </div>
          </div>
          {% endif %}
        </div>

        <!-- D. FINAL EXECUTED DOSSIER (Visible when both Signed AND Deposit Verified) -->
        <div id="finalExecutedDossier" style="display:{% if is_signed and is_deposit_verified %}block{% else %}none{% endif %}; background:#ffffff; border:1px solid #bbf7d0; border-radius:10px; padding:20px 24px; margin-top:14px; box-shadow:0 2px 6px rgba(0,0,0,0.03);">
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:16px; align-items:center;">
            <div>
              <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Candidate Digital Signature</div>
              <div style="font-size:26px; font-family:'Brush Script MT', 'Dancing Script', cursive, serif; color:#0f172a; margin:4px 0 2px;">
                {{ offer.signature_name }}
              </div>
              <div style="font-size:11.5px; color:#15803d; font-weight:700;">
                <i class="fa-solid fa-shield-halved"></i> Cryptographically Executed by {{ offer.name }}
              </div>
            </div>

            <div>
              <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Execution Timestamp</div>
              <div style="font-size:13.5px; font-weight:700; color:#0f172a; margin:4px 0 2px;">
                {{ offer.accepted_at }}
              </div>
              <div style="font-size:11.5px; color:#64748b;">
                Permanent Audit Record &bull; Official PDF Download Unlocked
              </div>
            </div>

            <div style="display:flex; justify-content:flex-end; gap:12px; flex-wrap:wrap; align-items:center;">
              <button type="button" class="na-cta-btn na-btn-gold" id="btnPrintOfferDossier" style="padding:15px 30px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; border-radius:10px;">
                <i class="fa-solid fa-file-pdf" style="font-size:18px;"></i> Download Official Signed PDF (A4) &rarr;
              </button>
              <a href="/portal" class="btn-secondary" style="padding:14px 22px; font-size:14px; font-weight:700; border-radius:10px;">
                <i class="fa-solid fa-gauge-high"></i> Open LMS Board
              </a>
            </div>
          </div>
        </div>"""

c = c[:sig_section_start] + new_sig_section + c[sig_section_end:]

# 4. Update JavaScript handleSignOffer to perform the dynamic transition
old_handle_sign_pattern = re.compile(
    r'function handleSignOffer\(e\) \{[\s\S]*?fetch\(\'/portal/offer/sign\'[\s\S]*?\.then\(function\(data\) \{[\s\S]*?\}\)\s*\.catch\(function\(err\) \{[\s\S]*?\}\);\s*\}'
)

new_handle_sign = """function handleSignOffer(e) {
  e.preventDefault();
  var nameInput = document.getElementById('sigNameInput');
  var name = nameInput ? nameInput.value.trim() : '';
  var agreeBox = document.getElementById('agreeCheckbox');
  var agreed = agreeBox ? agreeBox.checked : false;
  var alertBox = document.getElementById('signAlertBox');
  var btn = document.getElementById('signSubmitBtn');

  if (!name) {
    if (alertBox) {
      alertBox.style.display = 'block';
      alertBox.style.background = '#fef2f2';
      alertBox.style.border = '1px solid #fecaca';
      alertBox.style.color = '#991b1b';
      alertBox.textContent = 'Please type your full legal name to digitally sign.';
    }
    return;
  }
  if (!agreed) {
    if (alertBox) {
      alertBox.style.display = 'block';
      alertBox.style.background = '#fef2f2';
      alertBox.style.border = '1px solid #fecaca';
      alertBox.style.color = '#991b1b';
      alertBox.textContent = 'Please check the agreement box to accept terms.';
    }
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sealing Digital Signature…';

  fetch('/portal/offer/sign', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      signature_name: name,
      agreed: true
    })
  })
  .then(function(res) { return res.json(); })
  .then(function(data) {
    if (data.status === 'success') {
      // 1. Hide the signature input form
      var sigCard = document.getElementById('digitalSignatureCard');
      if (sigCard) sigCard.style.display = 'none';

      // 2. Populate and show the signed confirmation banner
      var dispName = document.getElementById('dispSigName');
      var dispTs = document.getElementById('dispSigTs');
      if (dispName) dispName.textContent = data.signature_name || name;
      if (dispTs) dispTs.textContent = data.accepted_at || 'Just Now';
      var signedBanner = document.getElementById('signedBanner');
      if (signedBanner) signedBanner.style.display = 'flex';

      // 3. Update top stepper to show Step 2 completed, Step 3 active
      var s2 = document.getElementById('stepperStep2');
      if (s2) {
        s2.className = 'step-item step-completed';
        var num2 = s2.querySelector('.step-number');
        if (num2) {
          num2.innerHTML = '<i class="fa-solid fa-check"></i>';
          num2.style.background = '#10b981';
          num2.style.boxShadow = '';
        }
        var lbl2 = s2.querySelector('.step-label');
        if (lbl2) { lbl2.textContent = 'Step 2 Done'; lbl2.style.color = '#10b981'; }
      }
      var s3 = document.getElementById('stepperStep3');
      if (s3) {
        s3.className = 'step-item step-active';
        var num3 = s3.querySelector('.step-number');
        if (num3) {
          num3.innerHTML = '3';
          num3.style.background = '#d97706';
          num3.style.color = '#ffffff';
          num3.style.boxShadow = '0 0 0 3px rgba(217, 119, 6, 0.2)';
        }
        var lbl3 = s3.querySelector('.step-label');
        if (lbl3) { lbl3.textContent = 'Action Required'; lbl3.style.color = '#d97706'; }
      }

      // 4. Update top action button
      var topBtn = document.getElementById('btnReviewSignTop');
      if (topBtn) {
        topBtn.href = '#signature-section';
        topBtn.className = 'btn-gold btn-gold-pulse';
        topBtn.innerHTML = '<i class="fa-solid fa-credit-card"></i> <span>Confirm Seat &amp; Pay ₹499 Now &darr;</span>';
      }

      // 5. Reveal payment section smoothly
      var paySec = document.getElementById('postSignPaymentSection');
      if (paySec) {
        paySec.style.display = 'block';
        paySec.scrollIntoView({ behavior: 'smooth', block: 'start' });
        paySec.style.transition = 'box-shadow 0.4s ease, border-color 0.4s ease';
        paySec.style.boxShadow = '0 0 0 4px rgba(245, 158, 11, 0.4)';
        setTimeout(function() { paySec.style.boxShadow = ''; }, 2500);
      }

      showToast('Agreement Digitally Signed! Complete Step 3 to confirm your seat.', 'green');
    } else {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-signature"></i> Sign &amp; Accept Appointment Agreement →';
      if (alertBox) {
        alertBox.style.display = 'block';
        alertBox.style.background = '#fef2f2';
        alertBox.style.border = '1px solid #fecaca';
        alertBox.style.color = '#991b1b';
        alertBox.textContent = data.message || 'Signing failed. Please try again.';
      }
    }
  })
  .catch(function(err) {
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-signature"></i> Sign &amp; Accept Appointment Agreement →';
    if (alertBox) {
      alertBox.style.display = 'block';
      alertBox.style.background = '#fef2f2';
      alertBox.style.border = '1px solid #fecaca';
      alertBox.style.color = '#991b1b';
      alertBox.textContent = 'Network error: ' + err.message;
    }
  });
}"""

c, count_js = old_handle_sign_pattern.subn(new_handle_sign, c)
assert count_js == 1, f"Expected 1 replacement in handleSignOffer, got {count_js}"

# Update DOMContentLoaded listener to ensure depForm and offerSignForm always attach
old_listener = """  {% if preview_mode %}
  var depForm = document.getElementById('depositSubmitForm');
  if (depForm) {
    depForm.addEventListener('submit', handleDepositSubmit);
  }
  {% endif %}

  var form = document.getElementById('offerSignForm');
  if (form) {
    form.addEventListener('submit', handleSignOffer);
  }"""

new_listener = """  var depForm = document.getElementById('depositSubmitForm');
  if (depForm) {
    depForm.addEventListener('submit', handleDepositSubmit);
  }

  var form = document.getElementById('offerSignForm');
  if (form) {
    form.addEventListener('submit', handleSignOffer);
  }"""

if old_listener in c:
    c = c.replace(old_listener, new_listener)

with open('apps/portal/templates/portal_offer_letter.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully updated portal_offer_letter.html!")
