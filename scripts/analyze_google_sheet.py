import csv
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/google_sheet_1265293201.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

with open('data/all_409_provisional_registry.json', 'r', encoding='utf-8') as f:
    all_409 = json.load(f)

with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
    cert_reg = json.load(f)

with open('data/dispatch_tracking_409.json', 'r', encoding='utf-8') as f:
    disp = json.load(f)

def norm(e):
    return (e or '').strip().lower()

emails_409 = {norm(x.get('email')): x for x in all_409 if x.get('email')}

reg_56 = {}
reg_prov = {}
for k, v in cert_reg.items():
    if v.get('provisional') is True or v.get('isProvisional') is True:
        reg_prov[norm(v.get('recipientEmail') or v.get('email'))] = v
    else:
        reg_56[norm(v.get('recipientEmail') or v.get('email'))] = v

disp_sent = {norm(x.get('email')): x for x in disp if x.get('status') == 'SENT'}
disp_pending = {norm(x.get('email')): x for x in disp if x.get('status') != 'SENT'}

print("=== ROW-BY-ROW BREAKDOWN OF GOOGLE SHEET (65 ROWS) ===")
counts = {
    'ORIGINAL_56_VERIFIED': 0,
    'IN_409_SENT': 0,
    'IN_409_PENDING': 0,
    'BRAND_NEW': 0
}

brand_new_list = []

for idx, r in enumerate(rows, 1):
    em = norm(r.get('Email Address'))
    name = r.get('Name', '').strip()
    track = r.get('Select Internship', '').strip()
    batch = r.get('Choose Internship Batch ', '').strip()
    ts = r.get('Timestamp', '').strip()
    phone = r.get('WhatsApp number ', '').strip()
    college = r.get('College Name', '').strip()
    
    in_56 = em in reg_56
    in_409_list = em in emails_409
    sent_in_409 = em in disp_sent
    pending_in_409 = em in disp_pending
    
    if in_56:
        counts['ORIGINAL_56_VERIFIED'] += 1
        cert = reg_56[em]
        cid = cert.get('certificateId')
        status_label = "ORIGINAL 56 (VERIFIED)"
        detail = f"{cid} | Status: Verified"
    elif in_409_list:
        cand = emails_409[em]
        cid = cand.get('certId')
        if sent_in_409:
            counts['IN_409_SENT'] += 1
            status_label = "IN 409 (ALREADY SENT)"
            detail = f"{cid} | Sent at: {disp_sent[em].get('sent_at', '')[:19]}"
        else:
            counts['IN_409_PENDING'] += 1
            status_label = "IN 409 (PENDING SEND)"
            detail = f"{cid} | Status: PENDING in 409 queue"
    else:
        counts['BRAND_NEW'] += 1
        status_label = ">>> BRAND NEW CANDIDATE <<<"
        detail = f"NEW | {track} | {batch} | {college}"
        brand_new_list.append({
            'row': idx,
            'timestamp': ts,
            'name': name,
            'email': em,
            'phone': phone,
            'college': college,
            'batch': batch,
            'track': track
        })
        
    print(f"Row {idx:2d} | {ts[:10]} | {name[:20]:20s} | {em[:30]:30s} | {status_label:27s} | {detail}")

print("\n" + "="*70)
print(f"SUMMARY COUNTS FOR GOOGLE SHEET (gid=1265293201):")
print(f"  Total Rows: {len(rows)}")
print(f"  1. Original 56 Verified Candidates (Already processed earlier): {counts['ORIGINAL_56_VERIFIED']}")
print(f"  2. Candidates in 409 Provisional Batch - ALREADY SENT by Daemon: {counts['IN_409_SENT']}")
print(f"  3. Candidates in 409 Provisional Batch - PENDING in Queue: {counts['IN_409_PENDING']}")
print(f"  4. Completely NEW Candidates (Not in 56, not in 409): {counts['BRAND_NEW']}")
print("="*70)

if brand_new_list:
    print(f"\nDETAILS OF BRAND NEW CANDIDATES ({len(brand_new_list)}):")
    for bn in brand_new_list:
        print(f"  Row {bn['row']}:")
        print(f"    Name:       {bn['name']}")
        print(f"    Email:      {bn['email']}")
        print(f"    Phone:      {bn['phone']}")
        print(f"    College:    {bn['college']}")
        print(f"    Batch:      {bn['batch']}")
        print(f"    Track:      {bn['track']}")
        print(f"    Timestamp:  {bn['timestamp']}")
