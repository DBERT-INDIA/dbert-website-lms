import json

subs = json.load(open('data/verification_submissions_299.json', encoding='utf-8'))
certs = json.load(open('apps/website/src/data/certificates_registry.json', encoding='utf-8'))
directory = json.load(open('apps/website/src/data/directory_candidates.json', encoding='utf-8'))

dir_map = {d.get('certId'): d for d in directory}

# The 12 new submissions from today (indices 4 to 15 in 0-indexed list)
new_subs = subs[4:]

print(f"Analyzing {len(new_subs)} new submissions from Nov 20:")
print("=" * 110)

for idx, s in enumerate(new_subs, 1):
    cid = s.get('certId')
    name = s.get('fullName')
    email = s.get('email')
    phone = s.get('phone')
    utr = s.get('utrNumber')
    domain = s.get('domain')
    submitted_at = s.get('submittedAt')
    
    cert_entry = certs.get(cid, {})
    dir_entry = dir_map.get(cid, {})
    
    print(f"\n{idx}. [{cid}] {name} ({email})")
    print(f"   UTR: {utr} | Submitted: {submitted_at} | Domain in Sub: {domain}")
    print(f"   Cert Reg Record: exists={bool(cert_entry)}")
    if cert_entry:
        print(f"     holderName: {cert_entry.get('holderName')}")
        print(f"     domain: {cert_entry.get('domain')}")
        print(f"     status: {cert_entry.get('status')}")
        print(f"     verified: {cert_entry.get('verified')}")
        print(f"     isProvisional: {cert_entry.get('isProvisional')}")
        print(f"     score: {cert_entry.get('score')} | grade: {cert_entry.get('grade')}")
        print(f"     issueDate: {cert_entry.get('issueDate')} | endDate: {cert_entry.get('endDate')}")
    print(f"   Directory Record: exists={bool(dir_entry)}")
    if dir_entry:
        print(f"     holderName: {dir_entry.get('holderName')}")
        print(f"     status: {dir_entry.get('status')}")
        print(f"     isProvisional: {dir_entry.get('isProvisional')}")
        print(f"     score: {dir_entry.get('score')}")
