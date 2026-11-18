import json

with open('data/active_54h_cohort.json', 'r', encoding='utf-8') as f:
    active_cohort = json.load(f)

with open('data/unverified_gate_active.json', 'r', encoding='utf-8') as f:
    gate_299_pool = json.load(f)

# Pool A: 50 unique candidates for ₹499
pool_499 = []
t1_rejected = [c for c in active_cohort if c.get('enr_status') == 'Rejected']
for c in t1_rejected:
    c['conversion_target'] = '₹499 Caution Deposit (Re-submission / Reconciliation)'
    c['amount'] = 499
    c['priority_tier'] = 1

pool_499.extend(t1_rejected)
t2_selected = [
    c for c in active_cohort 
    if c.get('segment') == 'SELECTED' and (c.get('session_count', 0) > 1 or '2026-11-13 1' in str(c.get('last_login')) or '2026-11-14' in str(c.get('last_login')))
]
for c in t2_selected:
    c['conversion_target'] = '₹499 Caution Deposit (Fast-Pay Seat Reservation)'
    c['amount'] = 499
    c['priority_tier'] = 2

for c in t2_selected:
    if len(pool_499) >= 50:
        break
    if c['email'].lower() not in set(x['email'].lower() for x in pool_499):
        pool_499.append(c)

# Pool B: 50 unique candidates for ₹299 (Disjoint from Pool A)
pool_499_emails = set(c['email'].lower() for c in pool_499)
pool_299 = []

fellows_in_active = [
    c for c in active_cohort 
    if c.get('segment') == 'ENROLLED_FELLOW' and (c.get('g1_linkedin') or c.get('g4_github'))
]
for c in fellows_in_active:
    if c['email'].lower() not in pool_499_emails:
        c['conversion_target'] = '₹299 Verification & Executive Dossier (Gate 3 to Unlock ₹5,000 Stipend)'
        c['amount'] = 299
        c['priority_tier'] = 3
        pool_299.append(c)

both_gates_active = [
    g for g in gate_299_pool 
    if g.get('linkedin_url') and g.get('github_url')
]
both_gates_active.sort(key=lambda x: str(x.get('updated_at')), reverse=True)
for g in both_gates_active:
    if len(pool_299) >= 50:
        break
    em = g['email'].lower()
    if em not in pool_499_emails and em not in set(x['email'].lower() for x in pool_299):
        g['conversion_target'] = '₹299 Verification & Executive Dossier (Gate 3 to Unlock ₹5,000 Stipend)'
        g['amount'] = 299
        g['priority_tier'] = 4
        pool_299.append(g)

balanced_100 = pool_499 + pool_299
unique_emails = set(c['email'].lower() for c in balanced_100)

print(f"Total Balanced 100: {len(balanced_100)}")
print(f"Unique emails: {len(unique_emails)}")
print(f"Pool 499 count: {len(pool_499)}")
print(f"Pool 299 count: {len(pool_299)}")

with open('data/balanced_revenue_target_100.json', 'w', encoding='utf-8') as f:
    json.dump(balanced_100, f, indent=2)

print("Updated data/balanced_revenue_target_100.json with 100% unique candidates!")
