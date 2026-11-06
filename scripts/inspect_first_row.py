import csv

with open('sheet_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    first_row = next(reader)

for k, v in first_row.items():
    print(f"  {k:40s}: '{v}'")
