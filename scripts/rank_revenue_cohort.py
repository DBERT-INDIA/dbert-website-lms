import json

with open('data/active_54h_cohort.json', 'r', encoding='utf-8') as f:
    cohort = json.load(f)

print(f"Total Cohort: {len(cohort)}")

# 1. Tier 1: Rejected Enrollments (26 candidates who submitted UTR/tried paying ₹499)
tier1_rejected = [c for c in cohort if c.get('enr_status') == 'Rejected']
for c in tier1_rejected:
    c['conversion_target'] = '₹499 Caution Deposit (Re-submission / Reconciliation)'
    c['priority_tier'] = 1
    c['priority_label'] = 'Tier 1 - Highest Intent (Payment Failed/Flagged)'

# 2. Tier 2: Highly Active SELECTED Candidates (Logged in multiple times or logged in today)
tier2_selected_high = [
    c for c in cohort 
    if c.get('segment') == 'SELECTED' and (c.get('session_count', 0) > 1 or '2026-11-13 1' in str(c.get('last_login')) or '2026-11-14' in str(c.get('last_login')))
]
for c in tier2_selected_high:
    c['conversion_target'] = '₹499 Caution Deposit (Fast-Pay Enrollment)'
    c['priority_tier'] = 2
    c['priority_label'] = 'Tier 2 - Very High Intent (Multi-Session Selected)'

# 3. Tier 3: Active Fellows with 2+ Gates Completed (Gate 1 + Gate 4 active, needing ₹299 Verification Gate 3)
tier3_fellows_gates = [
    c for c in cohort 
    if c.get('segment') == 'ENROLLED_FELLOW' and (c.get('g1_linkedin') or c.get('g4_github') or c.get('g2_status') != 'NOT_SUBMITTED')
]
for c in tier3_fellows_gates:
    c['conversion_target'] = '₹299 Verification & Executive Dossier (Gate 3 to Unlock ₹5,000 Stipend)'
    c['priority_tier'] = 3
    c['priority_label'] = 'Tier 3 - Fellowship Milestone Active (Sprint Unlocking)'

# 4. Tier 4: Selected Candidates with Single Session (Recent First-Time Explorers)
tier4_selected_recent = [
    c for c in cohort 
    if c.get('segment') == 'SELECTED' and c not in tier2_selected_high
]
# Sort tier 4 by recency
tier4_selected_recent.sort(key=lambda x: str(x.get('last_login')), reverse=True)
for c in tier4_selected_recent:
    c['conversion_target'] = '₹499 Caution Deposit (Fast-Pay Enrollment)'
    c['priority_tier'] = 4
    c['priority_label'] = 'Tier 4 - Selected Fresh Explorers'

# 5. Tier 5: Remaining Fellows needing ₹299 verification
tier5_fellows_other = [
    c for c in cohort 
    if c.get('segment') == 'ENROLLED_FELLOW' and c not in tier3_fellows_gates
]
for c in tier5_fellows_other:
    c['conversion_target'] = '₹299 Verification & Executive Dossier (Gate 3)'
    c['priority_tier'] = 5
    c['priority_label'] = 'Tier 5 - Enrolled Fellow Initial Stage'

print(f"Tier 1 (Failed/Flagged ₹499): {len(tier1_rejected)}")
print(f"Tier 2 (High-Intent Multi-Session Selected ₹499): {len(tier2_selected_high)}")
print(f"Tier 3 (Fellows with 2+ Gates completed ₹299): {len(tier3_fellows_gates)}")
print(f"Tier 4 (Fresh Selected Explorers ₹499): {len(tier4_selected_recent)}")
print(f"Tier 5 (Other Fellows ₹299): {len(tier5_fellows_other)}")

total_priority = len(tier1_rejected) + len(tier2_selected_high) + len(tier3_fellows_gates)
print(f"\nTop High-Conversion Pool (Tiers 1 + 2 + 3): {total_priority} candidates")

# Assemble the Top 100 WhatsApp Target List
top_100_whatsapp = []
top_100_whatsapp.extend(tier1_rejected) # 26
top_100_whatsapp.extend(tier2_selected_high) # 31 -> Total 57
top_100_whatsapp.extend(tier3_fellows_gates) # 8 -> Total 65
remaining_slots = 100 - len(top_100_whatsapp) # 35 slots
top_100_whatsapp.extend(tier4_selected_recent[:remaining_slots]) # 35

print(f"\nTop 100 WhatsApp Cohort Assembled: {len(top_100_whatsapp)} candidates")

# Save structured target dataset
with open('data/revenue_target_cohort_100.json', 'w', encoding='utf-8') as f:
    json.dump(top_100_whatsapp, f, indent=2)

print("Saved to data/revenue_target_cohort_100.json")
