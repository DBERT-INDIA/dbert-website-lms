import json
from collections import Counter

with open("data/active_logins_7d.json", "r", encoding="utf-8") as f:
    users = json.load(f)

print(f"Total active users: {len(users)}")

multi_users = [u for u in users if u["logins_7d"] > 1]
single_users = [u for u in users if u["logins_7d"] == 1]

print(f"Multi-login (>=2): {len(multi_users)}")
print(f"Single-login (==1): {len(single_users)}")

# Multi-login conversion breakdown
paid_deposit_multi = [u for u in multi_users if u["has_security_deposit"] or u["caution_deposit_status"] == "paid"]
unpaid_deposit_multi = [u for u in multi_users if not (u["has_security_deposit"] or u["caution_deposit_status"] == "paid")]

print(f"\nAmong 172 Multi-login Candidates:")
print(f"  Already Paid Caution Deposit (₹499): {len(paid_deposit_multi)}")
print(f"  UNPAID Caution Deposit (₹499): {len(unpaid_deposit_multi)}")

# For unpaid multi-login candidates:
# How many have offer letters?
unpaid_with_offer = [u for u in unpaid_deposit_multi if u["has_offer_letter"]]
unpaid_without_offer = [u for u in unpaid_deposit_multi if not u["has_offer_letter"]]
print(f"    - With Offer Letter generated: {len(unpaid_with_offer)}")
print(f"    - Without Offer Letter (Ready for offer generation): {len(unpaid_without_offer)}")

# How many have certificates?
unpaid_with_cert = [u for u in unpaid_deposit_multi if u["has_certificate"]]
unpaid_without_cert = [u for u in unpaid_deposit_multi if not u["has_certificate"]]
print(f"    - With Certificate (Ready for ₹299 verification upgrade): {len(unpaid_with_cert)}")
print(f"    - Without Certificate (Primary ₹499 caution deposit target): {len(unpaid_without_cert)}")

# Login frequency buckets among multi-logins
login_counts = Counter(u["logins_7d"] for u in multi_users)
print("\nLogin Frequency Distribution (7 Days):")
for cnt in sorted(login_counts.keys()):
    print(f"  {cnt} logins: {login_counts[cnt]} users")

# Let's inspect the top 20 multi-login unpaid users
print("\nTop 20 Unpaid Multi-Login Users (Highest Intent):")
sorted_unpaid = sorted(unpaid_deposit_multi, key=lambda x: (x["logins_7d"], x["lifetime_logins"]), reverse=True)
for i, u in enumerate(sorted_unpaid[:20], 1):
    print(f"  {i}. {u['name']} ({u['email']}) | 7d Logins: {u['logins_7d']} | Lifetime: {u['lifetime_logins']} | Status: {u['app_status']} | Domain: {u['domain']} | Offer: {u['has_offer_letter']} | Cert: {u['has_certificate']}")

# Now let's check single-login candidates
unpaid_single = [u for u in single_users if not (u["has_security_deposit"] or u["caution_deposit_status"] == "paid")]
print(f"\nAmong 329 Single-login Candidates:")
print(f"  Already Paid: {len(single_users) - len(unpaid_single)}")
print(f"  Unpaid: {len(unpaid_single)}")
print(f"    - With Certificate: {sum(1 for u in unpaid_single if u['has_certificate'])}")
print(f"    - With Offer Letter: {sum(1 for u in unpaid_single if u['has_offer_letter'])}")
