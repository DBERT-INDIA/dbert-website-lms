import csv

with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    batches = {}
    for r in reader:
        b = r.get('Source_Batches_List', '')
        batches[b] = batches.get(b, 0) + 1

print(f"Total rows in all_enrolled_interns_master_detailed.csv: {sum(batches.values())}")
print("Top 15 batch values:")
for b, c in sorted(batches.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {b}: {c}")
