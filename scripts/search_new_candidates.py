import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/all_409_provisional_registry.json', 'r', encoding='utf-8') as f:
    all_409 = json.load(f)

targets = [
    {'name': 'Deekshitha', 'phone': '9440282987', 'email': 'ndeekshitha07@gmail.com'},
    {'name': 'Rakholiya', 'phone': '7778066181', 'email': 'vasurakholiya108@gmail.com'},
    {'name': 'Janhvi', 'phone': '7905859140', 'email': 'janhvichandel3@gmail.com'}
]

for t in targets:
    print(f"\nSearching for {t['name']} / {t['phone']} / {t['email']}...")
    found = False
    for idx, cand in enumerate(all_409):
        c_name = cand.get('holderName', cand.get('name', '')).lower()
        c_phone = str(cand.get('phone', '')).replace(' ', '').replace('+91', '')
        c_email = cand.get('email', '').lower()
        
        if (t['name'].lower() in c_name) or (t['phone'] in c_phone) or (t['email'] == c_email):
            print(f"  MATCH FOUND at index {idx}: {cand}")
            found = True
    if not found:
        print("  NO MATCH in all_409_provisional_registry.json")
