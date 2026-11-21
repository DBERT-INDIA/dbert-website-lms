import json
import csv
import io
import urllib.request
import re

def normalize_email(em):
    return (em or "").strip().lower()

def normalize_phone(ph):
    digits = re.sub(r'\D', '', str(ph or ''))
    if len(digits) > 10 and digits.startswith('91'):
        digits = digits[2:]
    elif len(digits) > 10 and digits.startswith('0'):
        digits = digits[1:]
    return digits[-10:] if len(digits) >= 10 else digits

# Load registry
reg_path = "apps/website/src/data/certificates_registry.json"
with open(reg_path, "r", encoding="utf-8") as f:
    registry = json.load(f)

reg_by_email = {}
reg_by_cert = {}
for cid, c in registry.items():
    em = normalize_email(c.get("email"))
    if em:
        reg_by_email[em] = (cid, c)
    reg_by_cert[cid.strip().upper()] = c

# Fetch Google Sheet
url = 'https://docs.google.com/spreadsheets/d/1yacGLZGiTD_8GLOUHMphbdfsORqc8u_DrjvpVRSEDgs/export?format=csv&gid=1265293201'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read().decode('utf-8')

reader = csv.reader(io.StringIO(data))
rows = list(reader)

sheet_pending = []
sheet_verified = []

for idx, r in enumerate(rows[1:], start=2):
    ts = r[0]
    em = normalize_email(r[1] if len(r) > 1 else "")
    batch = r[2] if len(r) > 2 else ""
    track = r[3] if len(r) > 3 else ""
    name = r[5] if len(r) > 5 else ""
    college = r[6] if len(r) > 6 else ""
    phone = normalize_phone(r[7] if len(r) > 7 else "")
    proof = r[9] if len(r) > 9 else ""
    project = r[10] if len(r) > 10 else ""

    cand_reg = reg_by_email.get(em)
    if cand_reg:
        cid, c_data = cand_reg
        is_prov = bool(c_data.get("isProvisional", False))
        status = (c_data.get("status") or "").upper()
        if not is_prov and status in ("VERIFIED", "APPROVED"):
            sheet_verified.append({"row": idx, "email": em, "name": name, "cert_id": cid, "status": "ALREADY_VERIFIED"})
        else:
            sheet_pending.append({
                "row": idx, "email": em, "name": name, "phone": phone, "college": college, 
                "track": track, "proof": proof, "project": project, "cert_id": cid, 
                "current_status": status, "is_provisional": is_prov, "in_registry": True
            })
    else:
        # Check by name in registry
        found_name = None
        for cid, c_data in registry.items():
            if name and name.lower() in (c_data.get("holderName") or "").lower():
                found_name = (cid, c_data)
                break
        if found_name:
            cid, c_data = found_name
            is_prov = bool(c_data.get("isProvisional", False))
            status = (c_data.get("status") or "").upper()
            if not is_prov and status in ("VERIFIED", "APPROVED"):
                sheet_verified.append({"row": idx, "email": em, "name": name, "cert_id": cid, "status": "ALREADY_VERIFIED_BY_NAME"})
            else:
                sheet_pending.append({
                    "row": idx, "email": em, "name": name, "phone": phone, "college": college, 
                    "track": track, "proof": proof, "project": project, "cert_id": cid, 
                    "current_status": status, "is_provisional": is_prov, "in_registry": True,
                    "reg_email": c_data.get("email")
                })
        else:
            sheet_pending.append({
                "row": idx, "email": em, "name": name, "phone": phone, "college": college, 
                "track": track, "proof": proof, "project": project, "cert_id": "", 
                "current_status": "NOT_IN_REGISTRY", "is_provisional": True, "in_registry": False
            })

print(f"Total Sheet Submissions: {len(rows)-1}")
print(f"Already Fully Verified: {len(sheet_verified)}")
print(f"Pending Approval/Upgrade in Sheet: {len(sheet_pending)}")

print("\n--- PENDING CANDIDATES IN GOOGLE SHEET ---")
for p in sheet_pending:
    print(f"Row {p['row']}: {p['name']} | Email: {p['email']} | Cert: {p['cert_id']} | Status: {p['current_status']} | Prov: {p['is_provisional']}")
