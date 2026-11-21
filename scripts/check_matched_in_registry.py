import json

reg = json.load(open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8'))

targets = [
    ('Oishani', '9831800941', 'skylvies@gmail.com', 'majumderoishani@gmail.com'),
    ('Deekshitha', '9440282987', 'ndeekshitha07.24@kgpian.iitkgp.ac.in', 'ndeekshitha07@gmail.com'),
    ('Pravallika', '9618864488', 'pravallikapotnuru1816@gmail.com', 'pravallikapotnuru18@gmail.com'),
    ('Siva Sankar', '6302880826', 't.sivasankardell@gmail.com', 'sivasankar.t1606@gmail.com'),
    ('Tehreem', '8958006294', 'tehreemfatimabsmath@gmail.com', 'tehreemfatimabsmath@gmail.com')
]

for name, phone, lms_em, sheet_em in targets:
    found = []
    for cid, c in reg.items():
        em = c.get('email', '').strip().lower()
        hname = c.get('holderName', '').strip().lower()
        if em in (lms_em.lower(), sheet_em.lower()) or name.lower() in hname:
            found.append({
                "cert_id": cid,
                "name": c.get('holderName'),
                "email": c.get('email'),
                "status": c.get('status'),
                "is_provisional": c.get('isProvisional'),
                "tier": c.get('tier')
            })
    print(f"\n=== TARGET: {name} (LMS: {lms_em}, Sheet: {sheet_em}, Phone: {phone}) ===")
    if found:
        for f in found:
            print(f"  Found: {f['cert_id']} | {f['name']} | {f['email']} | Status: {f['status']} | Provisional: {f['is_provisional']}")
    else:
        print("  NO CERTIFICATE FOUND in registry")
