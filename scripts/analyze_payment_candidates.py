import json
from datetime import datetime

with open('data/active_54h_cohort.json', 'r', encoding='utf-8') as f:
    cohort = json.load(f)

# Group by segments
rejected_enr = [c for c in cohort if c.get('enr_status') == 'Rejected']
pending_seg = [c for c in cohort if c.get('segment') == 'ENROLLMENT_PENDING']
selected_seg = [c for c in cohort if c.get('segment') == 'SELECTED']
fellows = [c for c in cohort if c.get('segment') == 'ENROLLED_FELLOW']

print(f"Total Cohort: {len(cohort)}")
print(f"Rejected Enrollments (Payment Attempted, Flagged/Rejected): {len(rejected_enr)}")
print(f"Segment ENROLLMENT_PENDING: {len(pending_seg)}")
print(f"Segment SELECTED: {len(selected_seg)}")
print(f"Segment ENROLLED_FELLOW: {len(fellows)}")

# Let's see Rejected Enrollments details
print("\n--- SAMPLE REJECTED ENROLLMENTS (Candidates who tried to pay ₹499) ---")
for r in rejected_enr[:10]:
    print(f"Name: {r['name']} | Email: {r['email']} | Phone: {r['phone']} | Sessions: {r.get('session_count')} | Last Login: {r.get('last_login')}")

# Check SELECTED candidates with high activity (session_count > 1 or login today)
print("\n--- HIGH INTENT SELECTED CANDIDATES (Session count > 1 or very recent login) ---")
high_intent_selected = [c for c in selected_seg if c.get('session_count', 0) > 1 or '2026-11-14' in str(c.get('last_login'))]
print(f"High Intent Selected Count: {len(high_intent_selected)}")
for h in high_intent_selected[:10]:
    print(f"Name: {h['name']} | Email: {h['email']} | Phone: {h['phone']} | Sessions: {h.get('session_count')} | Last Login: {h.get('last_login')}")
