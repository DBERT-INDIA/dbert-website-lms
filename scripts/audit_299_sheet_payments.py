import urllib.request
import csv, io, json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

url = 'https://docs.google.com/spreadsheets/d/1yacGLZGiTD_8GLOUHMphbdfsORqc8u_DrjvpVRSEDgs/export?format=csv&gid=1265293201'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    content = resp.read().decode('utf-8')
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)

# Load certificates_registry.json
reg_file = ROOT_DIR / "apps" / "website" / "src" / "data" / "certificates_registry.json"
local_registry = json.load(open(reg_file, encoding='utf-8'))

fully_verified_by_email = {}
provisional_by_email = {}

for cid, c in local_registry.items():
    em = c.get('email', '').strip().lower()
    is_ver = (c.get('verified') is True or c.get('status') == 'VERIFIED') and not c.get('isProvisional', False)
    if is_ver:
        fully_verified_by_email[em] = c
    else:
        provisional_by_email[em] = c

# Also check directory_candidates.json
dir_file = ROOT_DIR / "apps" / "website" / "src" / "data" / "directory_candidates.json"
directory_candidates = json.load(open(dir_file, encoding='utf-8')) if dir_file.exists() else []
dir_by_email = {c.get('email', '').strip().lower(): c for c in directory_candidates}

audit_records = []
for idx, r in enumerate(rows[1:], start=2):
    email = r[1].strip().lower() if len(r) > 1 else ''
    batch = r[2].strip() if len(r) > 2 else ''
    domain = r[3].strip() if len(r) > 3 else ''
    name = r[5].strip() if len(r) > 5 else ''
    college = r[6].strip() if len(r) > 6 else ''
    phone = r[7].strip() if len(r) > 7 else ''
    fee_proof = r[9].strip() if len(r) > 9 else ''
    project = r[10].strip() if len(r) > 10 else ''
    
    if email in fully_verified_by_email:
        status_category = 'VERIFIED'
        cert_info = fully_verified_by_email[email]
    elif email in provisional_by_email:
        status_category = 'PROVISIONAL_NEEDS_UPGRADE'
        cert_info = provisional_by_email[email]
    elif email in dir_by_email:
        status_category = 'IN_DIRECTORY_NEEDS_REGISTRY'
        cert_info = dir_by_email[email]
    else:
        status_category = 'NEW_CANDIDATE'
        cert_info = {}

    audit_records.append({
        'row': idx,
        'timestamp': r[0],
        'email': email,
        'name': name,
        'domain': domain,
        'college': college,
        'phone': phone,
        'batch': batch,
        'fee_proof': fee_proof,
        'project': project,
        'status_category': status_category,
        'cert_id': cert_info.get('certId') or cert_info.get('cert_id') or None,
        'current_score': cert_info.get('score')
    })

counts = {}
for a in audit_records:
    cat = a['status_category']
    counts[cat] = counts.get(cat, 0) + 1

print("=" * 80)
print(f"GOOGLE SHEET 299 AUDIT SUMMARY (Total Responses: {len(audit_records)})")
print("=" * 80)
for k, v in counts.items():
    print(f"  - {k}: {v}")

print("\n--- CANDIDATES REQUIRING ACTION (PROVISIONAL UPGRADES & NEW SUBMISSIONS) ---")
action_needed = [a for a in audit_records if a['status_category'] != 'VERIFIED']
for a in action_needed:
    print(f"Row {a['row']:2d} | [{a['status_category']}] | {a['timestamp']} | {a['email']:30s} | {a['name']:25s} | Cert: {str(a['cert_id']):24s}")

# Save detailed JSON
out_file = ROOT_DIR / "data" / "sheet_299_reconciliation.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({
        'counts': counts,
        'action_needed': action_needed,
        'all_records': audit_records
    }, f, indent=2, ensure_ascii=False)

print(f"\nSaved reconciliation data to: data/sheet_299_reconciliation.json")
