import json
import os
import re

with open("data/verification_submissions_299.json", "r", encoding="utf-8") as f:
    submissions = json.load(f)

with open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
    certs = json.load(f)

with open("apps/website/src/data/directory_candidates.json", "r", encoding="utf-8") as f:
    dir_candidates = json.load(f)

print(f"Total Submissions in verification_submissions_299.json: {len(submissions)}")
print("-" * 80)

for idx, s in enumerate(submissions, 1):
    cid = s.get("certId")
    em = s.get("email", "").strip().lower()
    cinfo = certs.get(cid) if cid else None
    
    # Check directory entry
    in_dir = False
    dir_verified = False
    for dc in dir_candidates:
        if dc.get("certId") == cid or (em and dc.get("email", "").strip().lower() == em):
            in_dir = True
            dir_verified = dc.get("verified", False)
            break
            
    cert_status = cinfo.get("status") if cinfo else "NOT_IN_REGISTRY"
    cert_is_prov = cinfo.get("isProvisional") if cinfo else None
    cert_score = cinfo.get("score") if cinfo else None

    print(f"#{idx:2d} | SubID: {s.get('id')} | Name: {s.get('fullName')}")
    print(f"     Email: {em} | Phone: {s.get('phone')} | UTR: {s.get('utrNumber')}")
    print(f"     Cert: {cid} | Score: {cert_score} | Registry Status: {cert_status} | Prov: {cert_is_prov}")
    print(f"     Directory: InDir={in_dir}, Verified={dir_verified} | Submitted: {s.get('submittedAt')}")
    print("-" * 80)
