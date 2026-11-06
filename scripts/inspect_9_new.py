import csv
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/google_sheet_1265293201.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

with open('data/all_409_provisional_registry.json', 'r', encoding='utf-8') as f:
    all_409 = json.load(f)

# Find max cert numbers per track to know next available IDs
track_counters = {'DA': 0, 'AIML': 0, 'FSD': 0, 'PA': 0, 'UIUX': 0}
for c in all_409:
    cid = c.get('certId', '')
    parts = cid.split('-')
    if len(parts) >= 5:
        track = parts[3]
        num = int(parts[4]) if parts[4].isdigit() else 0
        if track in track_counters:
            track_counters[track] = max(track_counters[track], num)
        else:
            track_counters[track] = num

print("Highest Cert IDs in existing 409 registry:")
for k, v in track_counters.items():
    print(f"  {k}: {v} (Next: CERT-DBERT-2026-{k}-{v+1:03d})")

print("\n--- DETAILED INSPECTION OF THE 9 NEW FORM RESPONSES (Rows 57-65) ---")
for idx in range(56, 65):
    r = rows[idx]
    row_num = idx + 1
    ts = r.get('Timestamp')
    em = r.get('Email Address').strip()
    name = r.get('Name').strip()
    college = r.get('College Name').strip()
    phone = r.get('WhatsApp number ').strip()
    batch = r.get('Choose Internship Batch ').strip()
    track = r.get('Select Internship').strip()
    drive_link = r.get('Certification Fee 299/-').strip()
    project = r.get('Project Contibuted On').strip()
    placement = r.get('Do You want Placement and Interview Prepration ?').strip()
    
    # Check if in 409
    match_409 = None
    for c in all_409:
        if c.get('email', '').lower() == em.lower() or c.get('phone', '').replace(' ', '') == phone.replace(' ', ''):
            match_409 = c
            break
            
    print(f"\n[Row {row_num}] {name} ({em})")
    print(f"  Timestamp:     {ts}")
    print(f"  Phone:         {phone}")
    print(f"  College:       {college}")
    print(f"  Track / Batch: {track} | {batch}")
    print(f"  Project:       {project}")
    print(f"  Payment Link:  {drive_link}")
    print(f"  Placement:     {placement}")
    if match_409:
        print(f"  -> MATCHED IN 409: CertID={match_409.get('certId')}, Status=PROVISIONAL ({match_409.get('status')})")
    else:
        print(f"  -> BRAND NEW CANDIDATE: Needs new CertID & Directory Entry")
