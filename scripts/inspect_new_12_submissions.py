import json

subs = json.load(open('data/verification_submissions_299.json', encoding='utf-8'))
certs = json.load(open('apps/website/src/data/certificates_registry.json', encoding='utf-8'))
directory = json.load(open('apps/website/src/data/directory_candidates.json', encoding='utf-8'))

cert_map = certs
dir_map = {d.get('certId'): d for d in directory}

print(f"Total submissions: {len(subs)}")
print("=" * 105)
print(f"{'#':<3} | {'Tag':<6} | {'Cert ID':<24} | {'Name':<28} | {'Cert Reg Status':<22} | {'Directory Status'}")
print("-" * 105)

for idx, sub in enumerate(subs, 1):
    cid = sub.get('certId')
    name = sub.get('fullName')
    c_info = cert_map.get(cid)
    d_info = dir_map.get(cid)
    
    c_status = f"{c_info.get('status')} (prov={c_info.get('isProvisional')}, ver={c_info.get('verified')})" if c_info else "NOT FOUND"
    d_status = f"Found (ver={d_info.get('verified')}, prov={d_info.get('isProvisional')})" if d_info else "NOT IN DIRECTORY"
    
    tag = "[NEW]" if idx >= 5 else "[PREV]"
    print(f"{idx:<3} | {tag:<6} | {cid:<24} | {name[:27]:<28} | {c_status:<22} | {d_status}")
