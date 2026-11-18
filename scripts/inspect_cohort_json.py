import json
from collections import Counter

with open('data/active_54h_cohort.json', 'r', encoding='utf-8') as f:
    cohort = json.load(f)

with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
    cert_registry = json.load(f)

print("Type of cert_registry:", type(cert_registry))
if isinstance(cert_registry, dict):
    print("Keys of cert_registry:", list(cert_registry.keys())[:5])
    provisional_certs = [v for k, v in cert_registry.items() if isinstance(v, dict) and v.get('isProvisional') is True]
    print(f"Total Provisional Certs in dict registry: {len(provisional_certs)}")
elif isinstance(cert_registry, list):
    print(f"List length: {len(cert_registry)}")

active_emails = {c['email'].lower(): c for c in cohort}

# Match provisional certs with active candidates
matched_provisional = []
for k, v in cert_registry.items():
    if isinstance(v, dict) and v.get('isProvisional') is True:
        email = v.get('candidateEmail', '').lower()
        if email in active_emails:
            matched_provisional.append((email, v.get('candidateName'), k, active_emails[email]))

print(f"Matched active provisional candidates: {len(matched_provisional)}")
for m in matched_provisional[:10]:
    print(f"  {m[0]} | {m[1]} | {m[2]} | Segment: {m[3]['segment']} | Enr: {m[3]['enr_status']}")
