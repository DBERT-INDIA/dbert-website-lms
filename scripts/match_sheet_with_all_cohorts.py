import json
import re

def normalize_phone(phone_str):
    if not phone_str:
        return ""
    digits = re.sub(r'\D', '', str(phone_str))
    if len(digits) > 10 and digits.startswith('91'):
        digits = digits[2:]
    elif len(digits) > 10 and digits.startswith('0'):
        digits = digits[1:]
    return digits[-10:] if len(digits) >= 10 else digits

def normalize_email(email_str):
    if not email_str:
        return ""
    return str(email_str).strip().lower()

# 1. Load Google Sheet records
with open("data/sheet_1265293201_parsed.json", "r", encoding="utf-8") as f:
    sheet_records = json.load(f)

sheet_by_email = {}
sheet_by_phone = {}

for r in sheet_records:
    em = normalize_email(r.get("email"))
    if em:
        sheet_by_email[em] = r
    # Collect all phones
    raw_phone = normalize_phone(r.get("phone"))
    if raw_phone:
        sheet_by_phone[raw_phone] = r
    for p in r.get("all_phones", []):
        sheet_by_phone[p] = r

# 2. Load cohort data
with open("data/linkedin_stipend_cohort_results.json", "r", encoding="utf-8") as f:
    cohort_data = json.load(f)

strict_5 = cohort_data.get("strict_only_299_pending", [])
linkedin_upi_7 = cohort_data.get("linkedin_upi_unverified", [])
all_linkedin_unverified_867 = cohort_data.get("all_linkedin_unverified", [])

with open("data/provisional_completed_linkedin.json", "r", encoding="utf-8") as f:
    provisional_completed_38 = json.load(f)

def match_candidate(cand):
    em = normalize_email(cand.get("email"))
    ph = normalize_phone(cand.get("phone"))
    
    match_em = sheet_by_email.get(em)
    match_ph = sheet_by_phone.get(ph)
    
    match = match_em or match_ph
    match_type = []
    if match_em:
        match_type.append("EMAIL")
    if match_ph:
        match_type.append("PHONE")
    
    return match, "+".join(match_type) if match else None

print("=" * 60)
print("1. CHECKING STRICT 5 COHORT (ONLY 299 PENDING)")
print("=" * 60)
strict_matches = []
strict_no_matches = []
for c in strict_5:
    match, m_type = match_candidate(c)
    if match:
        strict_matches.append((c, match, m_type))
        print(f"MATCH FOUND [{m_type}]: ID {c['id']} {c['name']} ({c['email']} / {c['phone']}) -> Sheet Row {match['row_idx']} ({match['name']}, {match['email']}, {match['phone']})")
    else:
        strict_no_matches.append(c)
        print(f"NO MATCH: ID {c['id']} {c['name']} ({c['email']} / {c['phone']})")

print(f"\nStrict matches: {len(strict_matches)}, No match: {len(strict_no_matches)}")

print("\n" + "=" * 60)
print("2. CHECKING 7 LINKEDIN + UPI UNVERIFIED COHORT")
print("=" * 60)
upi_7_matches = []
upi_7_no_matches = []
for c in linkedin_upi_7:
    match, m_type = match_candidate(c)
    if match:
        upi_7_matches.append((c, match, m_type))
        print(f"MATCH FOUND [{m_type}]: ID {c['id']} {c['name']} ({c['email']} / {c['phone']}) -> Sheet Row {match['row_idx']}")
    else:
        upi_7_no_matches.append(c)
        print(f"NO MATCH: ID {c['id']} {c['name']} ({c['email']} / {c['phone']})")

print(f"\n7 UPI cohort matches: {len(upi_7_matches)}, No match: {len(upi_7_no_matches)}")

print("\n" + "=" * 60)
print("3. CHECKING 38 PROVISIONAL COMPLETED FELLOWS WITH LINKEDIN")
print("=" * 60)
prov_38_matches = []
prov_38_no_matches = []
for c in provisional_completed_38:
    match, m_type = match_candidate(c)
    if match:
        prov_38_matches.append((c, match, m_type))
        print(f"MATCH FOUND [{m_type}]: ID {c['id']} {c['name']} ({c['email']} / {c['phone']}) -> Sheet Row {match['row_idx']} ({match['name']}, {match['email']}, {match['phone']})")
    else:
        prov_38_no_matches.append(c)

print(f"38 Provisional Completed matches: {len(prov_38_matches)}, No match: {len(prov_38_no_matches)}")

print("\n" + "=" * 60)
print("4. CHECKING ALL 867 UNVERIFIED INTERNS WITH LINKEDIN")
print("=" * 60)
all_matches = []
all_no_matches = []
for c in all_linkedin_unverified_867:
    match, m_type = match_candidate(c)
    if match:
        all_matches.append((c, match, m_type))
    else:
        all_no_matches.append(c)

print(f"All 867 unverified matches: {len(all_matches)}, No match: {len(all_no_matches)}")
if all_matches:
    print(f"\nAll matches ({len(all_matches)}):")
    for c, match, m_type in all_matches:
        print(f"ID {c['id']} | {c['name']} | Email: {c['email']} | Phone: {c['phone']} | Matched by: {m_type} -> Sheet Row {match['row_idx']} ({match['name']}, {match['email']}, {match['phone']}, Proof: {match['raw'][9] if len(match['raw'])>9 else ''})")

# Save complete audit report to JSON
report = {
    "strict_5": {
        "matched": [{"candidate": c, "sheet_record": m, "match_type": mt} for c, m, mt in strict_matches],
        "unmatched": strict_no_matches
    },
    "upi_7": {
        "matched": [{"candidate": c, "sheet_record": m, "match_type": mt} for c, m, mt in upi_7_matches],
        "unmatched": upi_7_no_matches
    },
    "provisional_completed_38": {
        "matched": [{"candidate": c, "sheet_record": m, "match_type": mt} for c, m, mt in prov_38_matches],
        "unmatched": prov_38_no_matches
    },
    "all_unverified_867": {
        "matched_count": len(all_matches),
        "unmatched_count": len(all_no_matches),
        "matched": [{"candidate": c, "sheet_record": m, "match_type": mt} for c, m, mt in all_matches]
    }
}

with open("data/sheet_matching_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("\nSaved comprehensive audit report to data/sheet_matching_audit_results.json")
