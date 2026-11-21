import json

with open('/tmp/linkedin_stipend_cohort_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

unverified = data.get('all_linkedin_unverified', [])
print(f"Total unverified with LinkedIn: {len(unverified)}")

provisional_with_cert = [x for x in unverified if x.get('cert_status') == 'PROVISIONAL']
print(f"Total provisional with official Cert ID: {len(provisional_with_cert)}")

completed = [x for x in unverified if x.get('is_completed')]
print(f"Total unverified with completion date passed: {len(completed)}")

completed_provisional = [x for x in provisional_with_cert if x.get('is_completed')]
print(f"Total provisional with cert ID + completion date passed: {len(completed_provisional)}")

upi_added = [x for x in unverified if x.get('has_upi')]
print(f"Total unverified with UPI added: {len(upi_added)}")

print("\n--- Provisional Cert Holders who have added LinkedIn and UPI ---")
for x in data['linkedin_upi_unverified']:
    print(f"ID: {x['id']} | Name: {x['name']} | Email: {x['email']} | Phone: {x['phone']} | Track: {x['domain']} | Completed: {x['is_completed']} ({x['completion_date']}) | Cert: {x['cert_id']} ({x['cert_status']}) | LinkedIn: {x['linkedin_url']}")

print("\n--- Provisional Cert Holders with LinkedIn (Sample of 10) ---")
for x in provisional_with_cert[:10]:
    print(f"ID: {x['id']} | Name: {x['name']} | Email: {x['email']} | Phone: {x['phone']} | Cert: {x['cert_id']} | Has UPI: {x['has_upi']} | Completed: {x['is_completed']} | LinkedIn: {x['linkedin_url']}")
