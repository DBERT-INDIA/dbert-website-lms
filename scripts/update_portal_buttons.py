import re

# 1. Update portal.html
with open('apps/portal/templates/portal.html', 'r', encoding='utf-8') as f:
    portal_html = f.read()

# Update nsAction for Selected
pattern_selected = re.compile(
    r"(\}else if\(_status==='Selected'\|\|_status==='Enrollment Pending'[\s\S]*?nsAction\.innerHTML\s*=\s*`)([\s\S]*?)(`;\s*buildStepBar\('overviewStepBar','Selected'\);)",
    re.MULTILINE
)

new_ns_action = """
        <div style="display:flex;gap:16px;flex-wrap:wrap;margin-top:14px;">
          <a class="na-cta-btn na-btn-gold" href="/portal/offer" style="text-decoration:none;">
            <i class="fas fa-file-signature"></i>&nbsp; View Letter of Offer & Confirm Seat &rarr;
          </a>
          <button class="na-cta-btn na-btn-emerald" onclick="document.getElementById('ovSelected').scrollIntoView({behavior:'smooth'})">
            <i class="fas fa-credit-card"></i>&nbsp; Confirm Seat (₹499 Deposit) &darr;
          </button>
        </div>
      """

portal_html, count1 = pattern_selected.subn(r'\1' + new_ns_action + r'\3', portal_html)
print(f"Updated nsAction in portal.html: {count1} occurrence(s)")

# Update .na-btn-dark and others in portal.html styles to ensure 3D tangible buttons
old_style_target = """.na-btn-dark {
  background: rgba(255, 255, 255, 0.08) !important;
  color: #f8fafc !important;
  border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
}"""

new_style_replacement = """.na-btn-dark {
  background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
  color: #F8FAFC !important;
  border: 2px solid #475569 !important;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4) !important;
}"""

if old_style_target in portal_html:
    portal_html = portal_html.replace(old_style_target, new_style_replacement)
    print("Replaced .na-btn-dark in portal.html")
else:
    print("old_style_target not found in portal.html")

# Ensure gap: 16px in .na-btn-cluster
portal_html = portal_html.replace(
    ".na-btn-cluster {\n  display: flex !important;\n  align-items: center !important;\n  gap: 12px !important;",
    ".na-btn-cluster {\n  display: flex !important;\n  align-items: center !important;\n  gap: 16px !important;\n  margin-top: 6px !important;"
)

with open('apps/portal/templates/portal.html', 'w', encoding='utf-8') as f:
    f.write(portal_html)

# 2. Update portal_offer_letter.html
with open('apps/portal/templates/portal_offer_letter.html', 'r', encoding='utf-8') as f:
    offer_html = f.read()

# Make secondary Admissions desk button vibrant WhatsApp green
old_offer_btn = """          <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20checking%20my%20%E2%82%B9499%20deposit%20verification%20status%20for%20offer%20letter%20unlock%20(Email%3A%20{{ user.email }})." target="_blank" class="btn-secondary" style="background:#1e293b; color:#f1f5f9 !important; font-weight:600; font-size:13px; padding:11px 20px; border-radius:9px; border:1px solid #475569; text-decoration:none; display:inline-flex; align-items:center; gap:8px;">
            <i class="fa-brands fa-whatsapp"></i> Chat with Admissions Desk
          </a>"""

new_offer_btn = """          <a href="https://wa.me/918192911360?text=Hi%20Admissions%20Team%2C%20I%20am%20checking%20my%20%E2%82%B9499%20deposit%20verification%20status%20for%20offer%20letter%20unlock%20(Email%3A%20{{ user.email }})." target="_blank" class="btn-whatsapp" style="background:linear-gradient(135deg, #25D366 0%, #128C7E 100%); color:#ffffff !important; font-weight:800; font-size:13.5px; padding:12px 24px; border-radius:10px; border:2px solid #86EFAC; text-decoration:none; display:inline-flex; align-items:center; gap:8px; box-shadow:0 6px 18px rgba(37,211,102,0.45);">
            <i class="fa-brands fa-whatsapp" style="font-size:16px;"></i> Chat with Admissions Desk
          </a>"""

if old_offer_btn in offer_html:
    offer_html = offer_html.replace(old_offer_btn, new_offer_btn)
    print("Updated Admissions Desk button in portal_offer_letter.html")
    with open('apps/portal/templates/portal_offer_letter.html', 'w', encoding='utf-8') as f:
        f.write(offer_html)
else:
    print("Admissions desk button not matched in portal_offer_letter.html")

print("Finished portal button updates!")
