import re

with open('apps/portal/app.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update portal_offer_view
old_view_part = """    preview_mode = bool(offer.get("caution_deposit_status") != "VERIFIED")

    return render_template(
        "portal_offer_letter.html",
        locked=False,
        preview_mode=preview_mode,
        offer=offer,
        enrollment=enr_dict,
        app_row=app_dict,
        user=user
    )"""

new_view_part = """    preview_mode = bool(offer.get("caution_deposit_status") != "VERIFIED")
    is_signed = bool(offer.get("signature_name") and offer.get("accepted_at"))
    is_deposit_verified = bool(offer.get("caution_deposit_status") == "VERIFIED")

    return render_template(
        "portal_offer_letter.html",
        locked=False,
        preview_mode=preview_mode,
        is_signed=is_signed,
        is_deposit_verified=is_deposit_verified,
        offer=offer,
        enrollment=enr_dict,
        app_row=app_dict,
        user=user
    )"""

assert old_view_part in c, "old_view_part not found"
c = c.replace(old_view_part, new_view_part)

# 2. Update portal_offer_sign
# Replace the blocking check and update pdf_unlocked
old_sign_pattern = re.compile(
    r'(\s+if not row:\s+offer = get_or_create_offer_letter\(email\)[\s\S]*?row = offer\s+)'
    r'(\s+if row\["caution_deposit_status"\] != "VERIFIED":[\s\S]*?return jsonify\([\s\S]*?403\s+)'
    r'(\s+offer_id = row\["offer_letter_id"\]\s+now_ts = now_str\(\)\s+conn\.execute\([\s\S]*?WHERE offer_letter_id = \?\s+""",\s*\()'
    r'(sig_name,\s*now_ts,\s*now_ts,\s*offer_id\)\s*\)\s*conn\.commit\(\)\s+)'
    r'(return jsonify\(\{[\s\S]*?"accepted_at": now_ts\s*\}\))'
)

new_sign_code = r'''\1
        offer_id = row["offer_letter_id"]
        now_ts = now_str()
        is_verified = (row["caution_deposit_status"] == "VERIFIED")
        pdf_unlocked = 1 if is_verified else 0

        conn.execute(
            """
            UPDATE intern_offer_letters 
            SET signature_name = ?, accepted_at = ?, pdf_unlocked = ?, updated_at = ?
            WHERE offer_letter_id = ?
            """,
            (sig_name, now_ts, pdf_unlocked, now_ts, offer_id)
        )
        conn.commit()

    return jsonify({
        "status": "success",
        "message": "Appointment Agreement digitally signed and accepted successfully.",
        "offer_letter_id": offer_id,
        "signature_name": sig_name,
        "accepted_at": now_ts,
        "requires_deposit": not is_verified
    })'''

c, count = old_sign_pattern.subn(new_sign_code, c)
assert count == 1, f"Expected 1 replacement in portal_offer_sign, got {count}"

with open('apps/portal/app.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully updated app.py!")
