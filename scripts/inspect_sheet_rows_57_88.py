import json
import csv
import io
import urllib.request

reg = json.load(open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8"))

url = 'https://docs.google.com/spreadsheets/d/1yacGLZGiTD_8GLOUHMphbdfsORqc8u_DrjvpVRSEDgs/export?format=csv&gid=1265293201'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read().decode('utf-8')

reader = csv.reader(io.StringIO(data))
rows = list(reader)

print(f"Total rows: {len(rows)}")

reg_by_email = { (c.get('email') or '').strip().lower(): (cid, c) for cid, c in reg.items() }

for idx in range(57, len(rows)):
    r = rows[idx-1]
    ts = r[0]
    em = (r[1] or '').strip().lower()
    track = r[3]
    name = r[5]
    phone = r[7]
    proof = r[9]

    in_reg = reg_by_email.get(em)
    if in_reg:
        cid, c = in_reg
        print(f"Row {idx}: {name} | {em} | {phone} | Cert: {cid} | Ver: {c.get('verified')} | Prov: {c.get('isProvisional')} | Status: {c.get('status')}")
    else:
        # Check by name
        match_c = None
        for cid, c in reg.items():
            if name and name.lower() in (c.get('holderName') or '').lower():
                match_c = (cid, c)
                break
        if match_c:
            cid, c = match_c
            print(f"Row {idx} [Name Match]: {name} | {em} | {phone} | Cert: {cid} | Ver: {c.get('verified')} | Prov: {c.get('isProvisional')} | Status: {c.get('status')}")
        else:
            print(f"Row {idx} [NOT IN REGISTRY]: {name} | {em} | {phone} | Proof: {proof}")
