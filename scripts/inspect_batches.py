import csv

with open('sheet_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    batches = {}
    total = 0
    for r in reader:
        b = r.get('Choose Internship Batch', '').strip()
        batches[b] = batches.get(b, 0) + 1
        total += 1

print(f"Total rows: {total}")
for b, count in sorted(batches.items(), key=lambda x: -x[1]):
    print(f"  Batch: '{b}' -> {count} candidates")
