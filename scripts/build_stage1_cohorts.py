import json

with open("data/active_logins_7d.json", "r", encoding="utf-8") as f:
    users = json.load(f)

multi_users = [u for u in users if u["logins_7d"] > 1]

# Filter out already paid
unpaid_multi = [u for u in multi_users if not (u["has_security_deposit"] or u["caution_deposit_status"] == "paid")]

# Segment A: 26 candidates with certificates (for ₹299 Verification Upgrade)
cohort_299 = [u for u in unpaid_multi if u["has_certificate"]]

# Segment B: 136 candidates without certificates (for ₹499 Incubation / Seat Confirmation)
cohort_499 = [u for u in unpaid_multi if not u["has_certificate"]]

print(f"Total Multi-Login Unpaid Candidates: {len(unpaid_multi)}")
print(f"Cohort 499 (Seat Confirmation & Offer Letter): {len(cohort_499)}")
print(f"Cohort 299 (Certificate Verification Upgrade): {len(cohort_299)}")

# Save cohorts
with open("data/cohort_499_multilogin_136.json", "w", encoding="utf-8") as f:
    json.dump(cohort_499, f, indent=2)

with open("data/cohort_299_multilogin_26.json", "w", encoding="utf-8") as f:
    json.dump(cohort_299, f, indent=2)

print("\nSample 5 from Cohort 499:")
for u in cohort_499[:5]:
    print(f"  {u['name']} | {u['email']} | Logins: {u['logins_7d']} | Domain: {u['domain']} | Status: {u['app_status']}")

print("\nSample 5 from Cohort 299:")
for u in cohort_299[:5]:
    print(f"  {u['name']} | {u['email']} | Logins: {u['logins_7d']} | Domain: {u['domain']} | Cert: {u['cert_id']}")
