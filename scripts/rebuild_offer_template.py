import re
import os

TEMPLATE_PATH = "apps/portal/templates/portal_offer_letter.html"

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    text = f.read()

print("Original length:", len(text))

# 1. Update the Locked State CTA (line ~832) to Google Form instead of 1999
locked_1999_pattern = r'<a href="https://dbert\.in/enroll/1999\?email=\{\{\s*user\.email\s*\}\}" target="_blank" class="btn-gold"[^>]*>[\s\S]*?Pay / Reconcile ₹499 Deposit &rarr;[\s\S]*?</a>'
locked_replacement = """<a href="https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header" target="_blank" class="btn-gold" style="background:linear-gradient(135deg, #fbbf24 0%, #d97706 100%); color:#0b1120 !important; font-weight:800; font-size:13.5px; text-decoration:none; padding:12px 24px; border-radius:9px; display:inline-flex; align-items:center; gap:9px; box-shadow:0 4px 14px rgba(245, 158, 11, 0.35); border:1.5px solid #fde68a;">
            <i class="fa-solid fa-clipboard-check"></i> Complete Verification Form &rarr;
          </a>"""

if re.search(locked_1999_pattern, text):
    text = re.sub(locked_1999_pattern, locked_replacement, text, count=1)
    print("Replaced locked 1999 CTA with Google Form.")
else:
    print("Locked 1999 CTA not matched with regex, checking simple replace...")
    old_sub = 'https://dbert.in/enroll/1999?email={{ user.email }}'
    if old_sub in text:
        text = text.replace(old_sub, 'https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header')
        print("Replaced locked 1999 URL with simple replace.")

# Find section boundaries in text
hero_marker = "<!-- 1. EXECUTIVE HERO BANNER -->"
stepper_marker = "<!-- 2. THREE-STEP PROGRESS STEPPER -->"
action_card_marker = "<!-- 3. ACTION CARD (SEAT CONFIRMATION DEPOSIT OR DIGITAL SIGNATURE) -->"
doc_marker = "<!-- 4. OFFICIAL APPOINTMENT LETTER PARCHMENT DOCUMENT -->"
script_marker = '<script nonce="{{ csp_nonce() }}">'

hero_idx = text.find(hero_marker)
stepper_idx = text.find(stepper_marker)
action_card_idx = text.find(action_card_marker)
doc_idx = text.find(doc_marker)
script_idx = text.find(script_marker)

assert hero_idx != -1, "hero_marker not found"
assert stepper_idx != -1, "stepper_marker not found"
assert action_card_idx != -1, "action_card_marker not found"
assert doc_idx != -1, "doc_marker not found"
assert script_idx != -1, "script_marker not found"

# 2. Re-architect Top Buttons in HERO BANNER
# Between hero_idx and stepper_idx:
hero_block = text[hero_idx:stepper_idx]

# Replace top buttons block in hero banner
old_hero_buttons = """          {% if preview_mode %}
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
          {% endif %}"""

new_hero_buttons = """          {% if is_deposit_verified %}
          <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <button type="button" class="btn-gold" id="btnPrintOfferTop" style="padding:14px 26px; font-size:15px; font-weight:900; box-shadow:0 6px 20px rgba(245, 158, 11, 0.45); border-radius:10px; background:linear-gradient(135deg, #fbbf24 0%, #d97706 100%); color:#0b1120 !important; border:1.5px solid #fde68a; cursor:pointer;">
              <i class="fa-solid fa-file-pdf" style="font-size:17px;"></i> Download Official Signed PDF
            </button>
            <a href="/portal" class="btn-secondary" style="padding:14px 22px; font-size:14px; font-weight:700; border-radius:10px; background:#0f172a; color:#ffffff !important; border:1.5px solid #334155; text-decoration:none;">
              <i class="fa-solid fa-laptop-code"></i> LMS Sprints &rarr;
            </a>
          </div>
          {% elif is_signed %}
            {% if enrollment and (enrollment.utr or enrollment.payment_status in ('Pending', 'Submitted', 'Under Review')) %}
            <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20have%20submitted%20my%20%E2%82%B9499%20caution%20deposit%20(UTR%3A%20{{ enrollment.utr }})%20for%20Offer%20{{ offer.offer_letter_id }}.%20Kindly%20verify." target="_blank" class="btn-gold" style="background:#25D366; color:#ffffff !important; padding:14px 26px; font-size:15px; font-weight:900; box-shadow:0 6px 20px rgba(37,211,102,0.45); border-radius:10px; text-decoration:none;">
              <i class="fa-brands fa-whatsapp" style="font-size:18px;"></i> Expedite Verification &rarr;
            </a>
            {% else %}
            <a href="#signature-section" class="btn-gold btn-gold-pulse" id="btnConfirmSeatTop" style="padding:14px 28px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 6px 22px rgba(245, 158, 11, 0.55); border-radius:10px; background:linear-gradient(135deg, #fbbf24 0%, #d97706 100%); color:#0b1120 !important; border:1.5px solid #fde68a; text-decoration:none;">
              <i class="fa-solid fa-credit-card" style="font-size:17px;"></i> <span>Confirm Seat &amp; Pay ₹499 Now &darr;</span>
            </a>
            {% endif %}
          {% else %}
          <a href="#signature-section" class="btn-emerald btn-gold-pulse" id="btnReviewSignTop" style="padding:14px 28px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; border-radius:10px; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#ffffff !important; border:1.5px solid #6ee7b7; box-shadow:0 6px 22px rgba(16, 185, 129, 0.45); text-decoration:none;">
            <i class="fa-solid fa-file-signature" style="font-size:18px;"></i> Review &amp; Sign Offer Agreement &darr;
          </a>
          {% endif %}"""

assert old_hero_buttons in hero_block, "old_hero_buttons not matched"
hero_block = hero_block.replace(old_hero_buttons, new_hero_buttons)

# 3. Re-architect Stepper: Step 1 (Read terms) -> Step 2 (Sign) -> Step 3 (Confirm Seat ₹499)
new_stepper_block = """<!-- 2. THREE-STEP PROGRESS STEPPER -->
      <div class="no-print offer-stepper-card" style="background:#ffffff; border:1px solid #e2e8f0; border-radius:12px; padding:16px 22px; margin-bottom:22px; display:flex; align-items:center; justify-content:space-between; gap:16px; box-shadow:0 2px 8px rgba(0, 0, 0, 0.04);">
        <!-- Step 1: Selection & Terms Review -->
        <div class="step-item step-completed" id="stepperStep1" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:#10b981; color:#ffffff;">
            <i class="fa-solid fa-check"></i>
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:#10b981;">
              Step 1 Done
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Review Appointment Terms</span>
          </div>
        </div>

        <div class="step-divider" style="width:48px; height:2px; background:#e2e8f0; flex-shrink:0;"></div>

        <!-- Step 2: Digital Signature & Acceptance -->
        <div class="step-item {% if is_signed %}step-completed{% else %}step-active{% endif %}" id="stepperStep2" style="display:flex; align-items:center; gap:12px; flex:1;">
          <div class="step-number" style="width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800; flex-shrink:0; background:{% if is_signed %}#10b981{% else %}#2563eb{% endif %}; color:#ffffff; {% if not is_signed %}box-shadow:0 0 0 3px rgba(37, 99, 235, 0.2);{% endif %}">
            {% if is_signed %}<i class="fa-solid fa-check"></i>{% else %}2{% endif %}
          </div>
          <div class="step-content" style="display:flex; flex-direction:column;">
            <span class="step-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:{% if is_signed %}#10b981{% else %}#2563eb{% endif %};">
              {% if is_signed %}Step 2 Executed{% else %}Action Required{% endif %}
            </span>
            <span class="step-title" style="font-size:13.5px; font-weight:700; color:#0f172a;">Review &amp; Digital Signature</span>
          </div>
        </div>

        <div class="step-divider" style="width:48px; height:2px; background:#e2e8f0; flex-shrink:0;"></div>

        <!-- Step 3: Confirm Seat (₹499 Deposit) -->
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
      </div>
"""

# 4. Extract and update the Parchment Document Block
# From doc_idx to script_idx (excluding closing tags before script)
doc_end_idx = text.rfind("</div>\n\n    </div>\n  </div>\n</div>\n\n<script", 0, script_idx + 100)
if doc_end_idx == -1:
    doc_end_idx = text.rfind("      {% endif %}\n\n    </div>\n  </div>\n</div>\n\n<script", 0, script_idx + 100)

print("doc_end_idx:", doc_end_idx)
# Let's inspect around 91700
doc_raw = text[doc_idx:doc_end_idx]

# Update Parchment Candidate Acceptance Signature Block inside doc_raw:
sig_block_start = doc_raw.find('<!-- 3. Candidate Digital Acceptance -->')
assert sig_block_start != -1, "Candidate Digital Acceptance not found in doc_raw"
sig_block_end = doc_raw.find('<!-- END OF PARCHMENT OR NEXT BLOCK -->', sig_block_start)
if sig_block_end == -1:
    # find the closing </div> of this sig-block
    # It ends before the closing of the 3-column signatures grid
    sig_block_end = doc_raw.find('</div>\n            </div>\n\n          </div>', sig_block_start)
    if sig_block_end == -1:
        # let's find the closing of sig-block
        sig_meta_idx = doc_raw.find('<div class="sig-meta-block"', sig_block_start)
        sig_block_end = doc_raw.find('</div>\n            </div>', sig_meta_idx) + len('</div>\n            </div>')

new_parchment_sig_block = """<!-- 3. Candidate Digital Acceptance -->
            <div class="sig-block" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px 16px; display:flex; flex-direction:column; justify-content:space-between; box-sizing:border-box;">
              <div>
                <div class="sig-block-label" style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.6px; color:#64748b; margin-bottom:10px;">Accepted &amp; Digitally Signed</div>
                <div class="sig-handwritten-zone" id="parchmentCandidateSigZone" style="height:48px; display:flex; align-items:center; margin-bottom:6px;">
                  {% if is_signed %}
                  <div class="sig-cursive-font" style="color:#15803d; font-family:'Brush Script MT', 'Dancing Script', cursive, serif; font-size:26px; line-height:1;">
                    {{ offer.signature_name }}
                  </div>
                  {% else %}
                  <div style="font-size:12px; color:#94a3b8; font-style:italic; line-height:1.4;">
                    [ Awaiting Digital Signature via Agreement Form Below ]
                  </div>
                  {% endif %}
                </div>
              </div>
              <div class="sig-meta-block" style="border-top:1px solid #cbd5e1; padding-top:6px; display:flex; flex-direction:column; gap:2px;">
                <div class="sig-meta-name" style="font-size:13px; font-weight:800; color:#0f172a;">{{ offer.signature_name or offer.name }}</div>
                <div class="sig-meta-role" style="font-size:11.5px; color:#475569; font-weight:600;">{{ offer.domain }} Intern</div>
                <div class="sig-meta-org" id="parchmentCandidateSigStatus" style="color:{% if is_signed %}#15803d; font-weight:700;{% else %}#64748b;{% endif %}; font-size:11px;">
                  {% if is_signed %}
                  <i class="fa-solid fa-check-double"></i> Executed: {{ offer.accepted_at }}
                  {% else %}
                  Awaiting Signature
                  {% endif %}
                </div>
              </div>
            </div>"""

doc_raw = doc_raw[:sig_block_start] + new_parchment_sig_block + doc_raw[sig_block_end:]


# 5. Build the Clean, Complete #signature-section (Action Card placed AFTER the parchment document)
new_action_card = """      <!-- 4. ACTION CARD (DIGITAL SIGNATURE & SEAT CONFIRMATION DEPOSIT) -->
      <div class="no-print signature-box-wrapper {% if is_signed and is_deposit_verified %}signed-state{% endif %}" id="signature-section" style="background:{% if is_signed and is_deposit_verified %}linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%){% else %}#ffffff{% endif %}; border:1px solid #cbd5e1; border-top:4px solid {% if is_signed and is_deposit_verified %}#10b981{% elif is_signed %}#d97706{% else %}#2563eb{% endif %}; border-radius:12px; padding:26px 30px; margin-top:26px; margin-bottom:26px; box-shadow:0 8px 20px -4px rgba(0, 0, 0, 0.06);">

        <!-- A. SIGNED CONFIRMATION BANNER (Visible if signed, or revealed dynamically on signing) -->
        <div id="signedBanner" style="display:{% if is_signed %}flex{% else %}none{% endif %}; background:#f0fdf4; border:1.5px solid #86efac; border-radius:10px; padding:16px 20px; margin-bottom:20px; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
          <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:38px; height:38px; border-radius:50%; background:#10b981; color:#ffffff; display:flex; align-items:center; justify-content:center; font-size:17px; flex-shrink:0;">
              <i class="fa-solid fa-check"></i>
            </div>
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.8px; color:#15803d;">
                STEP 2 COMPLETED: AGREEMENT EXECUTED
              </div>
              <div style="font-size:15px; font-weight:800; color:#0f172a; margin-top:2px;">
                Appointment Agreement Digitally Signed &amp; Accepted
              </div>
              <div style="font-size:12px; color:#475569; margin-top:2px;">
                Signed by <strong style="color:#0f172a;" id="signedNameDisplay">{{ offer.signature_name }}</strong> on <span id="signedDateDisplay">{{ offer.accepted_at }}</span> &bull; Recorded under Indian IT Act, 2000
              </div>
            </div>
          </div>
          <span style="display:inline-flex; align-items:center; gap:6px; background:#dcfce7; color:#166534; font-weight:800; font-size:12px; padding:6px 14px; border-radius:99px; border:1px solid #86efac;">
            <i class="fa-solid fa-circle-check"></i> Legally Accepted
          </span>
        </div>

        {% if not is_signed %}
        <!-- B. DIGITAL SIGNATURE FORM (Visible first: Candidate reads letter and signs here) -->
        <div id="offerSignCard">
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#eff6ff; color:#2563eb; display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0; border:1px solid #bfdbfe;">
              <i class="fa-solid fa-signature"></i>
            </div>
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.8px; color:#2563eb;">
                STEP 2: REVIEW &amp; DIGITAL ACCEPTANCE
              </div>
              <h3 style="margin:2px 0 0; font-size:18px; font-weight:900; color:#0f172a; font-family:'Georgia', serif;">
                Execute Appointment Agreement
              </h3>
            </div>
          </div>
          <p style="font-size:13.5px; color:#475569; line-height:1.65; margin:0 0 16px;">
            To execute this appointment agreement and secure your workstation seat in the <strong>{{ offer.domain }}</strong> cohort, please confirm your legal name and accept the terms below.
          </p>

          <form id="offerSignForm" onsubmit="handleSignOffer(event);">
            <div class="sig-input-group" style="margin:16px 0; max-width:520px;">
              <label for="sigNameInput" class="sig-input-label" style="display:block; font-size:12px; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:8px;">
                Full Legal Name (Digital Signature) *
              </label>
              <input type="text" id="sigNameInput" placeholder="e.g. {{ offer.name }}" value="{{ offer.name }}" required class="sig-input-field" style="width:100%; padding:13px 16px; border:2px solid #cbd5e1; border-radius:8px; font-size:15px; font-weight:700; color:#0f172a; background:#ffffff; box-sizing:border-box;">
              <p style="font-size:11.5px; color:#64748b; margin:6px 0 0;">
                <i class="fa-solid fa-circle-info"></i> Must match candidate identification on official academic records.
              </p>
            </div>

            <label class="terms-acceptance-card" style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:14px 18px; display:flex; align-items:flex-start; gap:12px; margin-bottom:18px; cursor:pointer;">
              <input type="checkbox" id="agreeCheckbox" required style="width:18px; height:18px; margin-top:2px; accent-color:#10b981; cursor:pointer;">
              <span class="terms-acceptance-text" style="font-size:13px; line-height:1.6; color:#334155;">
                I, <strong>{{ offer.name }}</strong>, have read, understood, and accept all terms of this Appointment Letter &amp; Technical Engagement, including attendance commitments, remote sprint deliverables, intellectual property assignments, and the ₹499 refundable caution deposit terms.
              </span>
            </label>

            <div id="signAlertBox" style="display:none; padding:12px 16px; border-radius:8px; font-size:13.5px; font-weight:600; margin-bottom:16px;"></div>

            <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
              <button type="submit" id="signSubmitBtn" class="btn-emerald btn-gold-pulse" style="padding:15px 32px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; border-radius:10px; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#ffffff !important; border:1.5px solid #6ee7b7; box-shadow:0 6px 20px rgba(16, 185, 129, 0.45); cursor:pointer; display:inline-flex; align-items:center; gap:10px;">
                <i class="fa-solid fa-signature" style="font-size:19px;"></i> Sign &amp; Accept Appointment Agreement
              </button>
              <span style="font-size:12px; color:#64748b;">
                <i class="fa-solid fa-lock"></i> Binding digital signature recorded under Indian IT Act, 2000.
              </span>
            </div>
          </form>
        </div>
        {% endif %}

        <!-- C. POST-SIGN PAYMENT SECTION (REVEALED IN-PLACE AFTER SIGNING OR IF ALREADY SIGNED) -->
        <div id="postSignPaymentSection" style="display:{% if is_signed and not is_deposit_verified %}block{% else %}none{% endif %}; margin-top:{% if not is_signed %}24px{% else %}0{% endif %};">

          {% if enrollment and (enrollment.utr or enrollment.payment_status in ('Pending', 'Submitted', 'Under Review')) %}
          <!-- ── STATE 3A: DEPOSIT SUBMITTED & UNDER ADMIN VERIFICATION ── -->
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#dbeafe; color:#1d4ed8; display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0;">
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
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:18px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; flex-wrap:wrap;">
              <span style="color:#64748b; font-weight:600;">Recorded 12-Digit UTR:</span>
              <code style="font-weight:800; color:#0f172a; background:#e2e8f0; padding:3px 10px; border-radius:5px; font-size:13.5px;">{{ enrollment.utr }}</code>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; flex-wrap:wrap;">
              <span style="color:#64748b; font-weight:600;">Admissions Ledger Status:</span>
              <span style="color:#d97706; font-weight:800;"><i class="fa-solid fa-clock"></i> Pending Bank Reconciliation</span>
            </div>
            <p style="margin:10px 0 0; font-size:12.5px; color:#64748b;">
              Your deposit transaction has been registered in the DBERT admissions ledger. Upon administrative verification, your official signed PDF download will be permanently unlocked.
            </p>
          </div>
          <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20have%20submitted%20my%20%E2%82%B9499%20caution%20deposit%20(UTR%3A%20{{ enrollment.utr }})%20for%20Offer%20{{ offer.offer_letter_id }}.%20Kindly%20verify." target="_blank" class="btn-whatsapp" style="background:linear-gradient(135deg, #25D366 0%, #128C7E 100%); color:#ffffff !important; padding:13px 22px; font-size:14px; font-weight:800; border-radius:10px; border:1.5px solid #86EFAC; display:inline-flex; align-items:center; gap:8px; text-decoration:none; box-shadow:0 6px 18px rgba(37,211,102,0.45);">
              <i class="fa-brands fa-whatsapp"></i> Expedite Verification via WhatsApp &rarr;
            </a>
            <button type="button" onclick="window.location.reload();" class="btn-secondary" style="padding:13px 20px; font-size:13.5px; font-weight:700; border-radius:10px; background:#0f172a; color:#ffffff; border:1.5px solid #334155; cursor:pointer; display:inline-flex; align-items:center; gap:8px;">
              <i class="fa-solid fa-rotate"></i> Refresh Status
            </button>
          </div>

          {% else %}
          <!-- ── STATE 3B: DEPOSIT PENDING SUBMISSION (QR + 1-TAP UPI + UTR INPUT) ── -->
          <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
            <div style="width:36px; height:36px; border-radius:50%; background:#fef3c7; color:#b45309; display:flex; align-items:center; justify-content:center; font-size:16px; flex-shrink:0;">
              <i class="fa-solid fa-lock"></i>
            </div>
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; letter-spacing:0.8px; color:#b45309;">
                STEP 3: COHORT SEAT CONFIRMATION
              </div>
              <h3 style="margin:2px 0 0; font-size:18px; font-weight:900; color:#0f172a; font-family:'Georgia', serif;">
                Confirm Your Cohort Seat with ₹499 Refundable Caution Deposit
              </h3>
            </div>
          </div>
          <p style="font-size:13.5px; color:#475569; line-height:1.65; margin:0 0 16px;">
            Per Section 5 of your appointment terms above, a refundable caution deposit of <strong>₹499</strong> is required to finalize cohort enrollment, secure dedicated mentor bandwidth, and unlock your official signed PDF.
          </p>

          <!-- Scan & Pay QR Code + 1-Tap UPI Launchers + UTR Submission Grid -->
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:20px; margin-bottom:18px;">

            <!-- Left: QR Code & Fast Pay Card -->
            <div style="background:#0b1120; border:1px solid #1e293b; border-radius:12px; padding:20px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
              <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                  <span style="font-size:11px; font-weight:800; letter-spacing:0.8px; text-transform:uppercase; color:#fbbf24;">
                    <i class="fa-solid fa-qrcode"></i> Scan &amp; Pay ₹499
                  </span>
                  <span style="font-size:11px; font-weight:700; background:rgba(16,185,129,0.2); color:#34d399; padding:3px 8px; border-radius:99px; border:1px solid #10b981;">
                    100% Refundable
                  </span>
                </div>

                <!-- QR Display -->
                <div style="text-align:center; padding:12px; background:#ffffff; border-radius:10px; margin-bottom:12px;">
                  <img src="/static/img/qrcode.jpeg" alt="DBERT Admissions ₹499 UPI QR" style="width:170px; height:170px; object-fit:contain; border-radius:6px; display:inline-block;">
                  <div style="font-size:11px; font-weight:800; color:#0f172a; margin-top:6px; letter-spacing:0.5px;">
                    Scan with GPay &bull; PhonePe &bull; Paytm &bull; BHIM
                  </div>
                </div>

                <div style="font-size:12px; color:#94a3b8; text-align:center; margin-bottom:12px;">
                  Merchant VPA: <strong style="color:#ffffff; font-family:monospace; background:rgba(255,255,255,0.1); padding:2px 6px; border-radius:4px;">Q652429146@ybl</strong>
                </div>
              </div>

              <!-- 1-Tap Mobile UPI Buttons -->
              <div>
                <div style="font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.5px;">
                  <i class="fa-solid fa-bolt" style="color:#fbbf24;"></i> Mobile 1-Tap Fast Pay (₹499):
                </div>
                <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:8px; margin-bottom:6px;">
                  <a href="intent://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}#Intent;scheme=upi;package=com.google.android.apps.nbu.paisa.user;end" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:11px 12px; background:#ffffff; border:1.5px solid #e2e8f0; border-radius:8px; color:#0f172a !important; text-decoration:none; font-size:13px; font-weight:800; box-shadow:0 3px 8px rgba(0,0,0,0.12);">
                    <i class="fab fa-google-pay" style="font-size:20px; color:#4285F4;"></i> GPay
                  </a>
                  <a href="phonepe://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:11px 12px; background:#5f259f; border:1.5px solid #7c3aed; border-radius:8px; color:#ffffff !important; text-decoration:none; font-size:13px; font-weight:800; box-shadow:0 3px 8px rgba(95,37,159,0.35);">
                    <i class="fas fa-mobile-screen" style="font-size:14px; color:#ffffff;"></i> PhonePe
                  </a>
                  <a href="paytmmp://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:11px 12px; background:#002970; border:1.5px solid #00baf2; border-radius:8px; color:#ffffff !important; text-decoration:none; font-size:13px; font-weight:800; box-shadow:0 3px 8px rgba(0,186,242,0.35);">
                    <i class="fas fa-wallet" style="font-size:14px; color:#00baf2;"></i> Paytm
                  </a>
                  <a href="upi://pay?pa=Q652429146@ybl&pn=DBERT%20Admissions&am=499&cu=INR&tn=DBERT-DEPOSIT-{{ offer.offer_letter_id }}" target="_blank" rel="noopener" style="display:flex; align-items:center; justify-content:center; gap:6px; padding:11px 12px; background:#1e293b; border:1.5px solid #f59e0b; border-radius:8px; color:#ffffff !important; text-decoration:none; font-size:13px; font-weight:800; box-shadow:0 3px 8px rgba(0,0,0,0.25);">
                    <i class="fas fa-qrcode" style="font-size:14px; color:#fbbf24;"></i> Any UPI
                  </a>
                </div>
              </div>
            </div>

            <!-- Right: UTR Entry Form Card -->
            <div style="background:#f8fafc; border:1.5px solid #cbd5e1; border-radius:12px; padding:24px; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 6px 18px rgba(0,0,0,0.04);">
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                  <span style="width:26px; height:26px; border-radius:50%; background:#d97706; color:#ffffff; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:800;">
                    2
                  </span>
                  <span style="font-size:12px; font-weight:800; text-transform:uppercase; letter-spacing:0.7px; color:#0f172a;">
                    Submit UTR for Seat Confirmation
                  </span>
                </div>

                <p style="font-size:13px; color:#475569; line-height:1.6; margin:0 0 16px;">
                  After completing your ₹499 transfer via QR code or 1-Tap UPI app, copy the <strong>12-Digit Bank UTR / UPI Reference Number</strong> and enter it below to confirm your cohort workstation seat.
                </p>

                <!-- UTR Submission Form -->
                <form id="depositSubmitForm" onsubmit="handleDepositSubmit(event);">
                  <div class="sig-input-group" style="margin-bottom:16px;">
                    <label for="depositUtrInput" class="sig-input-label" style="display:block; font-size:12px; font-weight:800; color:#0f172a; text-transform:uppercase; letter-spacing:0.6px; margin-bottom:8px;">
                      12-Digit Bank UTR / UPI Ref Number *
                    </label>
                    <input type="text" id="depositUtrInput" name="utr_number" maxlength="12" pattern="\\d{12}" placeholder="e.g. 679862090077" required class="sig-input-field" style="width:100%; padding:14px 16px; border:2px solid #cbd5e1; border-radius:8px; font-size:16px; font-weight:700; font-family:monospace; color:#0f172a; background:#ffffff; box-sizing:border-box; letter-spacing:1.5px;">
                    <p style="font-size:11.5px; color:#64748b; margin:6px 0 0;">
                      <i class="fa-solid fa-circle-info"></i> Found in transaction details on GPay, PhonePe, Paytm, or bank SMS receipt.
                    </p>
                  </div>

                  <input type="hidden" name="domain" value="{{ offer.domain }}">
                  <input type="hidden" name="joining_date" value="{{ offer.batch_start_date }}">

                  <div id="depositAlertBox" style="display:none; padding:12px 16px; border-radius:8px; font-size:13.5px; font-weight:600; margin-bottom:16px;"></div>

                  <button type="submit" id="depositSubmitBtn" class="btn-gold btn-gold-pulse" style="width:100%; justify-content:center; padding:15px 24px; font-size:15px; font-weight:900; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 6px 20px rgba(245, 158, 11, 0.45); border-radius:10px; background:linear-gradient(135deg, #fbbf24 0%, #d97706 100%); color:#0b1120 !important; border:1.5px solid #fde68a; cursor:pointer; display:inline-flex; align-items:center; gap:10px;">
                    <i class="fa-solid fa-circle-check" style="font-size:18px;"></i> Submit UTR for Admin Verification &rarr;
                  </button>
                </form>
              </div>

              <div style="margin-top:16px; padding-top:14px; border-top:1px solid #e2e8f0; font-size:12px; color:#64748b; display:flex; align-items:center; gap:8px;">
                <i class="fa-solid fa-shield-halved" style="color:#10b981; font-size:15px;"></i>
                <span>Automated admissions ledger reconciliation &bull; Unlocks official signed PDF upon admin check.</span>
              </div>
            </div>

          </div>
          {% endif %}

        </div>

        {% if is_deposit_verified %}
        <!-- D. EXECUTED & VERIFIED SUCCESS DOSSIER -->
        <div id="verifiedDossierCard" style="background:#ffffff; border:1.5px solid #bbf7d0; border-radius:10px; padding:20px; box-shadow:0 4px 12px rgba(16,185,129,0.08);">
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:18px; align-items:center;">
            <div>
              <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">
                Candidate Digital Acceptance
              </div>
              <div style="font-size:26px; font-family:'Brush Script MT', 'Dancing Script', cursive, serif; color:#15803d; margin:4px 0 2px;">
                {{ offer.signature_name }}
              </div>
              <div style="font-size:11.5px; color:#15803d; font-weight:700;">
                <i class="fa-solid fa-shield-halved"></i> Cryptographically Executed by {{ offer.name }}
              </div>
            </div>

            <div>
              <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">
                Timestamp &amp; Status
              </div>
              <div style="font-size:13.5px; font-weight:700; color:#0f172a; margin:4px 0 2px;">
                {{ offer.accepted_at }}
              </div>
              <div style="font-size:11.5px; color:#166534; font-weight:700;">
                <i class="fa-solid fa-circle-check"></i> Reconciled &bull; Official Signed PDF Download Unlocked
              </div>
            </div>

            <div style="display:flex; justify-content:flex-end; gap:12px; flex-wrap:wrap; align-items:center;">
              <button type="button" class="btn-gold btn-gold-pulse" id="btnPrintOfferDossier" style="padding:14px 24px; font-size:14.5px; font-weight:900; box-shadow:0 6px 20px rgba(245, 158, 11, 0.45); border-radius:10px; background:linear-gradient(135deg, #fbbf24 0%, #d97706 100%); color:#0b1120 !important; border:1.5px solid #fde68a; cursor:pointer; display:inline-flex; align-items:center; gap:8px;">
                <i class="fa-solid fa-file-pdf" style="font-size:18px;"></i> Download Official Signed PDF &rarr;
              </button>
              <a href="/portal" class="btn-secondary" style="padding:14px 20px; font-size:14px; font-weight:700; border-radius:10px; background:#0f172a; color:#ffffff !important; border:1.5px solid #334155; text-decoration:none; display:inline-flex; align-items:center; gap:8px;">
                <i class="fa-solid fa-gauge-high"></i> Open LMS Board
              </a>
            </div>
          </div>
        </div>
        {% endif %}

      </div>
"""

# 6. Re-architect the JavaScript functions
new_script_block = """<script nonce="{{ csp_nonce() }}">
function showToastNotification(msg) {
  var existing = document.getElementById('offerToastNotification');
  if (existing) { existing.remove(); }
  var toast = document.createElement('div');
  toast.id = 'offerToastNotification';
  toast.style.position = 'fixed';
  toast.style.bottom = '24px';
  toast.style.right = '24px';
  toast.style.background = '#0f172a';
  toast.style.color = '#fbbf24';
  toast.style.border = '1.5px solid #d97706';
  toast.style.borderRadius = '8px';
  toast.style.padding = '12px 18px';
  toast.style.fontSize = '13px';
  toast.style.fontWeight = '700';
  toast.style.boxShadow = '0 10px 25px rgba(0,0,0,0.3)';
  toast.style.zIndex = '99999';
  toast.innerHTML = '<i class="fa-solid fa-circle-check" style="margin-right:8px; color:#10b981;"></i>' + msg;
  document.body.appendChild(toast);
  setTimeout(function() {
    toast.style.transition = 'opacity 0.4s ease';
    toast.style.opacity = '0';
    setTimeout(function() { toast.remove(); }, 400);
  }, 4000);
}

function highlightSignatureCard() {
  var card = document.getElementById('signature-section');
  if (card) {
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.style.transition = 'box-shadow 0.3s ease, border-color 0.3s ease';
    card.style.borderColor = '#fbbf24';
    card.style.boxShadow = '0 0 0 4px rgba(251, 191, 36, 0.4)';
    setTimeout(function() {
      card.style.boxShadow = '';
      card.style.borderColor = '';
    }, 2000);
  }
}

function handleDepositSubmit(e) {
  e.preventDefault();
  var form = e.target;
  var utrInput = document.getElementById('depositUtrInput');
  var utr = utrInput ? utrInput.value.trim() : '';
  var alertBox = document.getElementById('depositAlertBox');
  var btn = document.getElementById('depositSubmitBtn');

  if (!/^\\d{12}$/.test(utr)) {
    alertBox.style.display = 'block';
    alertBox.style.background = '#fef2f2';
    alertBox.style.border = '1px solid #fecaca';
    alertBox.style.color = '#991b1b';
    alertBox.textContent = 'Please enter a valid 12-digit numeric UPI UTR number from your payment receipt.';
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Registering in Admissions Ledger…';

  var formData = new FormData(form);

  fetch('/enroll', {
    method: 'POST',
    body: formData
  })
  .then(function(res) { return res.json(); })
  .then(function(data) {
    if (data.status === 'success' || data.status === 'enrolled') {
      alertBox.style.display = 'block';
      alertBox.style.background = '#f0fdf4';
      alertBox.style.border = '1px solid #bbf7d0';
      alertBox.style.color = '#166534';
      alertBox.innerHTML = '<i class="fa-solid fa-circle-check"></i> <strong>₹499 Caution Deposit Submitted!</strong> Registered for admin reconciliation…';
      setTimeout(function() {
        window.location.reload();
      }, 1200);
    } else {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-circle-check"></i> Submit UTR for Admin Verification &rarr;';
      alertBox.style.display = 'block';
      alertBox.style.background = '#fef2f2';
      alertBox.style.border = '1px solid #fecaca';
      alertBox.style.color = '#991b1b';
      alertBox.textContent = data.message || 'Submission failed. Please check your UTR number or contact Admissions.';
    }
  })
  .catch(function(err) {
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-circle-check"></i> Submit UTR for Admin Verification &rarr;';
    alertBox.style.display = 'block';
    alertBox.style.background = '#fef2f2';
    alertBox.style.border = '1px solid #fecaca';
    alertBox.style.color = '#991b1b';
    alertBox.textContent = 'Network error: ' + err.message;
  });
}

function handleSignOffer(e) {
  e.preventDefault();
  var name = document.getElementById('sigNameInput').value.trim();
  var agreed = document.getElementById('agreeCheckbox').checked;
  var alertBox = document.getElementById('signAlertBox');
  var btn = document.getElementById('signSubmitBtn');

  if (!name) {
    alertBox.style.display = 'block';
    alertBox.style.background = '#fef2f2';
    alertBox.style.border = '1px solid #fecaca';
    alertBox.style.color = '#991b1b';
    alertBox.textContent = 'Please type your full legal name to digitally sign.';
    return;
  }
  if (!agreed) {
    alertBox.style.display = 'block';
    alertBox.style.background = '#fef2f2';
    alertBox.style.border = '1px solid #fecaca';
    alertBox.style.color = '#991b1b';
    alertBox.textContent = 'Please check the agreement box to accept terms.';
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing Digital Signature…';

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
      // 1. Hide the sign form card
      var formCard = document.getElementById('offerSignCard');
      if (formCard) formCard.style.display = 'none';

      // 2. Show the signed banner
      var banner = document.getElementById('signedBanner');
      if (banner) {
        banner.style.display = 'flex';
        var nameSpan = document.getElementById('signedNameDisplay');
        if (nameSpan) nameSpan.textContent = data.signature_name || name;
        var dateSpan = document.getElementById('signedDateDisplay');
        if (dateSpan) dateSpan.textContent = data.accepted_at || 'Just now';
      }

      // 3. Update candidate digital signature block in the parchment document above
      var parchmentSigZone = document.getElementById('parchmentCandidateSigZone');
      if (parchmentSigZone) {
        parchmentSigZone.innerHTML = '<div class="sig-cursive-font" style="color:#15803d; font-family:\\'Brush Script MT\\', \\'Dancing Script\\', cursive, serif; font-size:24px; font-weight:700;">' + (data.signature_name || name) + '</div>';
      }
      var parchmentSigStatus = document.getElementById('parchmentCandidateSigStatus');
      if (parchmentSigStatus) {
        parchmentSigStatus.innerHTML = '<span style="color:#15803d; font-weight:700;"><i class="fa-solid fa-check-double"></i> Executed: ' + (data.accepted_at || 'Just now') + '</span>';
      }

      // 4. Update the Progress Stepper
      var step2Item = document.getElementById('stepperStep2');
      if (step2Item) {
        step2Item.className = 'step-item step-completed';
        var step2Num = step2Item.querySelector('.step-number');
        if (step2Num) {
          step2Num.style.background = '#10b981';
          step2Num.style.color = '#ffffff';
          step2Num.innerHTML = '<i class="fa-solid fa-check"></i>';
        }
        var step2Lbl = step2Item.querySelector('.step-label');
        if (step2Lbl) {
          step2Lbl.style.color = '#10b981';
          step2Lbl.textContent = 'Step 2 Executed';
        }
      }

      var step3Item = document.getElementById('stepperStep3');
      if (step3Item) {
        step3Item.className = 'step-item step-active';
        var step3Num = step3Item.querySelector('.step-number');
        if (step3Num) {
          step3Num.style.background = '#d97706';
          step3Num.style.color = '#ffffff';
          step3Num.style.boxShadow = '0 0 0 3px rgba(217, 119, 6, 0.2)';
        }
        var step3Lbl = step3Item.querySelector('.step-label');
        if (step3Lbl) {
          step3Lbl.style.color = '#d97706';
          step3Lbl.textContent = 'Action Required';
        }
      }

      // 5. Update Top Action Button
      var topBtnReview = document.getElementById('btnReviewSignTop');
      if (topBtnReview) {
        topBtnReview.id = 'btnConfirmSeatTop';
        topBtnReview.className = 'btn-gold btn-gold-pulse';
        topBtnReview.href = '#signature-section';
        topBtnReview.style.background = 'linear-gradient(135deg, #fbbf24 0%, #d97706 100%)';
        topBtnReview.style.color = '#0b1120';
        topBtnReview.style.border = '1.5px solid #fde68a';
        topBtnReview.innerHTML = '<i class="fa-solid fa-credit-card" style="font-size:17px;"></i> Confirm Seat &amp; Pay ₹499 Now &darr;';
      }

      // 6. Unfold the ₹499 payment section with smooth scroll
      var paymentSec = document.getElementById('postSignPaymentSection');
      if (paymentSec) {
        paymentSec.style.display = 'block';
        paymentSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }

      showToastNotification('Appointment Agreement Digitally Signed! Complete ₹499 caution deposit below to confirm your cohort seat.');
    } else {
      btn.disabled = false;
      btn.innerHTML = '<i class="fa-solid fa-signature"></i> Sign &amp; Accept Appointment Agreement';
      alertBox.style.display = 'block';
      alertBox.style.background = '#fef2f2';
      alertBox.style.border = '1px solid #fecaca';
      alertBox.style.color = '#991b1b';
      alertBox.textContent = data.message || 'Signing failed. Please try again.';
    }
  })
  .catch(function(err) {
    btn.disabled = false;
    btn.innerHTML = '<i class="fa-solid fa-signature"></i> Sign &amp; Accept Appointment Agreement';
    alertBox.style.display = 'block';
    alertBox.style.background = '#fef2f2';
    alertBox.style.border = '1px solid #fecaca';
    alertBox.style.color = '#991b1b';
    alertBox.textContent = 'Network error: ' + err.message;
  });
}

document.addEventListener('DOMContentLoaded', function() {
  var btnPrintTop = document.getElementById('btnPrintOfferTop');
  if (btnPrintTop) {
    btnPrintTop.addEventListener('click', function() {
      window.open('/portal/offer/print', '_blank');
    });
  }
  var btnPrintDossier = document.getElementById('btnPrintOfferDossier');
  if (btnPrintDossier) {
    btnPrintDossier.addEventListener('click', function() {
      window.open('/portal/offer/print', '_blank');
    });
  }
});
</script>
</body>
</html>
"""

# Re-assemble the entire HTML:
# Part 1: Top of file up to hero_idx
part1 = text[:hero_idx]
# Part 2: hero_block
part2 = hero_block
# Part 3: new_stepper_block
part3 = new_stepper_block
# Part 4: doc_raw (The parchment document, which candidate reads first!)
part4 = doc_raw
# Part 5: new_action_card (#signature-section placed right under parchment document)
part5 = new_action_card
# Part 6: closing container tags
part6 = """      {% endif %}

    </div>
  </div>
</div>

"""
# Part 7: new_script_block
part7 = new_script_block

final_html = part1 + part2 + part3 + part4 + part5 + part6 + part7

with open(TEMPLATE_PATH, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Rebuilt template successfully! Final length:", len(final_html))
