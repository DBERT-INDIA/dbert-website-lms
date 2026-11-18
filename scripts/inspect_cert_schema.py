import json

with open('data/active_54h_cohort.json', 'r', encoding='utf-8') as f:
    cohort = json.load(f)

with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
    cert_registry = json.load(f)

active_emails = {c['email'].strip().lower(): c for c in cohort}

matched_provisional = []
matched_verified = []

for cert_id, data in cert_registry.items():
    em = data.get('email', '').strip().lower()
    is_prov = data.get('isProvisional', False) or (data.get('verified') is False)
    if em in active_emails:
        if is_prov:
            matched_provisional.append((cert_id, data, active_emails[em]))
        else:
            matched_verified.append((cert_id, data, active_emails[em]))

print(f"Active Cohort Size: {len(cohort)}")
print(f"Active candidates with Verified Certs: {len(matched_verified)}")
print(f"Active candidates with Provisional Certs: {len(matched_provisional)}")

print("\n--- Provisional Cert Matches ---")
for cid, cdata, act in matched_provisional:
    print(f"{cid} | {cdata.get('holderName')} | {cdata.get('email')} | Segment: {act.get('segment')} | Enr: {act.get('enr_status')}")

# Also check all 409 provisional registry
try:
    with open('data/all_409_provisional_registry.json', 'r', encoding='utf-8') as f:
        all_409 = json.load(f)
    print(f"\nTotal in all_409_provisional_registry.json: {len(all_409)}")
    active_in_409 = [p for p in all_409 if p.get('email', '').strip().lower() in active_emails]
    print(f"Active 54h candidates in all_409: {len(active_in_409)}")
    for a in active_in_409[:10]:
        print(f"  {a.get('cert_id')} | {a.get('name')} | {a.get('email')} | {a.get('domain')}")
except Exception as e:
    print("Error reading all_409:", e)
