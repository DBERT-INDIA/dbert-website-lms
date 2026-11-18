import json

with open('data/active_54h_cohort.json', 'r', encoding='utf-8') as f:
    cohort = json.load(f)

fellows = [c for c in cohort if c.get('segment') == 'ENROLLED_FELLOW']
print(f"Total ENROLLED_FELLOW in active cohort: {len(fellows)}")

for f in fellows:
    print(f"Name: {f['name']} | Email: {f['email']} | Phone: {f['phone']} | G1(LI): {f.get('g1_linkedin')} | G2(Art): {f.get('g2_status')} | G3(Ver): {f.get('g3_verified')} | G4(Git): {f.get('g4_github')} | Sessions: {f.get('session_count')} | Last Login: {f.get('last_login')}")
