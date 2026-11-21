import json

with open('/tmp/linkedin_stipend_cohort_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

unverified = data.get('all_linkedin_unverified', [])
provisional_completed = [x for x in unverified if x.get('cert_status') == 'PROVISIONAL' and x.get('is_completed')]

print(f"Total provisional completed with LinkedIn: {len(provisional_completed)}")

out_path = "/tmp/provisional_completed_linkedin.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(provisional_completed, f, indent=2)

for i, x in enumerate(provisional_completed, 1):
    print(f"{i}. ID: {x['id']} | {x['name']} | {x['email']} | {x['phone']} | {x['domain']} | {x['cert_id']} | Has UPI: {x['has_upi']} | LinkedIn: {x['linkedin_url']}")
