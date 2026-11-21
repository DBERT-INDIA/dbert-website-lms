import json
import re

with open("data/sheet_1265293201_parsed.json", "r", encoding="utf-8") as f:
    sheet_records = json.load(f)

with open("data/linkedin_stipend_cohort_results.json", "r", encoding="utf-8") as f:
    cohort_data = json.load(f)

strict_5 = cohort_data.get("strict_only_299_pending", [])
upi_7 = cohort_data.get("linkedin_upi_unverified", [])
with open("data/provisional_completed_linkedin.json", "r", encoding="utf-8") as f:
    prov_38 = json.load(f)

def clean_name(n):
    return set(re.sub(r'[^a-zA-Z\s]', '', (n or '').lower()).split())

print("=== CHECKING ALL NAMES IN SHEET AGAINST COHORT CANDIDATES ===")
all_cohort_cands = {c['id']: c for c in strict_5 + upi_7 + prov_38}.values()

for cand in all_cohort_cands:
    c_tokens = clean_name(cand['name'])
    for r in sheet_records:
        s_tokens = clean_name(r['name'])
        common = c_tokens.intersection(s_tokens)
        # ignore very common short tokens
        common = {t for t in common if len(t) > 2 and t not in ('kumar', 'singh', 'patel', 'sharma', 'reddy')}
        if len(common) >= 2 or (len(common) == 1 and len(c_tokens) <= 2 and len(s_tokens) <= 2 and list(common)[0] in ('bhasker', 'sruthi', 'deekshitha', 'rajesh', 'lalam', 'omeshwar')):
            print(f"Name Match: Candidate [{cand['id']}] '{cand['name']}' (Email: {cand['email']}, Phone: {cand['phone']}) <-> Sheet Row {r['row_idx']} '{r['name']}' (Email: {r['email']}, Phone: {r['phone']}) - Common: {common}")
