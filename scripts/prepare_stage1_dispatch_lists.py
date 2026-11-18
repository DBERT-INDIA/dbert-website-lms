import json

# 1. Load active logins from last 7 days
with open("data/active_logins_7d.json", "r", encoding="utf-8") as f:
    users = json.load(f)

# 2. Load balance submissions
with open("data/balance_enrollments_1500.json", "r", encoding="utf-8") as f:
    balance_records = json.load(f)

balance_map = {}
for r in balance_records:
    em = (r.get("email") or "").strip().lower()
    if em:
        balance_map[em] = r

# 3. Load 9 verified candidates
try:
    with open("data/dispatch_tracking_9_verified.json", "r", encoding="utf-8") as f:
        v9 = json.load(f)
    v9_emails = {r.get("email", "").strip().lower() for r in v9}
except Exception:
    v9_emails = set()

# 4. Multi-login candidates (>= 2 logins in last 7 days)
multi_users = [u for u in users if u["logins_7d"] > 1]

# Filter and partition
cohort_499 = []
cohort_299 = []
already_reconciled = []
utr_pending_review = []

for u in multi_users:
    em = u["email"].strip().lower()
    
    # Check if approved
    b_rec = balance_map.get(em)
    if b_rec and b_rec.get("status") == "APPROVED":
        already_reconciled.append({**u, "reconciliation_note": "Approved ₹1,999 Incubation Fellow (Bhargavi Poola et al.)"})
        continue

    # Check if verified 9
    if em in v9_emails:
        already_reconciled.append({**u, "reconciliation_note": "Verified ₹299 Candidate (already dispatched)"})
        continue

    # Check if already paid deposit in LMS
    if u["has_security_deposit"] or u["caution_deposit_status"] == "paid":
        already_reconciled.append({**u, "reconciliation_note": "LMS Security Deposit Paid"})
        continue

    # Check if submitted UTR awaiting staff reconciliation
    if b_rec and b_rec.get("status") == "SUBMITTED":
        utr_pending_review.append({**u, "utr": b_rec.get("utrNumber"), "submitted_at": b_rec.get("submittedAt")})
        continue

    # Check if candidate holds an unverified/provisional certificate
    if u["has_certificate"]:
        cohort_299.append(u)
    else:
        cohort_499.append(u)

print("=== STAGE 1 AUDIT & PARTITIONING RESULTS ===")
print(f"Total Multi-Login Candidates: {len(multi_users)}")
print(f"  - Already Reconciled / Approved: {len(already_reconciled)}")
for r in already_reconciled:
    print(f"      * {r['name']} ({r['email']}): {r['reconciliation_note']}")

print(f"  - UTR Submitted Awaiting Review: {len(utr_pending_review)}")
for r in utr_pending_review:
    print(f"      * {r['name']} ({r['email']}): UTR {r['utr']}")

print(f"\n  >>> COHORT 499 (Seat Confirmation & Offer Letter): {len(cohort_499)} candidates")
print(f"  >>> COHORT 299 (Credential Verification Upgrade): {len(cohort_299)} candidates")

# Save exact files
with open("data/stage1_cohort_499_actionable.json", "w", encoding="utf-8") as f:
    json.dump(cohort_499, f, indent=2)

with open("data/stage1_cohort_299_actionable.json", "w", encoding="utf-8") as f:
    json.dump(cohort_299, f, indent=2)

print("\nSaved actionable datasets to data/stage1_cohort_499_actionable.json and data/stage1_cohort_299_actionable.json")
