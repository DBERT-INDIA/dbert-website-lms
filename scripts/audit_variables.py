import csv
from collections import Counter

with open('sheet_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = [r for r in reader if any(r.values())]

print(f"Total valid candidate rows: {len(rows)}")
print("=" * 80)

# 1. Batches
print("\n--- 1. CHOOSE INTERNSHIP BATCH ---")
batches = Counter(r['Choose Internship Batch '].strip() if 'Choose Internship Batch ' in r else r['Choose Internship Batch'].strip() for r in rows)
for b, count in batches.most_common():
    print(f"  {count:2d} candidates: '{b}'")

# 2. Domains
print("\n--- 2. SELECT INTERNSHIP (DOMAINS) ---")
domains = Counter(r['Select Internship'].strip() for r in rows)
for d, count in domains.most_common():
    print(f"  {count:2d} candidates: '{d}'")

# 3. Projects
print("\n--- 3. PROJECT CONTRIBUTED ON ---")
projects = Counter(r['Project Contibuted On'].strip() for r in rows)
for p, count in projects.most_common():
    print(f"  {count:2d} candidates: '{p}'")

# 4. Colleges
print("\n--- 4. SAMPLE COLLEGES ---")
colleges = [r['College Name'].strip() for r in rows]
for c in colleges[:10]:
    print(f"  - '{c}'")

# 5. WhatsApp numbers
print("\n--- 5. WHATSAPP NUMBERS SAMPLE ---")
phones = [r.get('WhatsApp number ', r.get('WhatsApp number', '')).strip() for r in rows]
for p in phones[:5]:
    print(f"  - '{p}'")
