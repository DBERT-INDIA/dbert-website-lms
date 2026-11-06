import csv
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/google_sheet_1265293201.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

print(f"Total rows: {len(rows)}")

indices_to_check = [56, 57, 58, 59, 60, 61, 62, 63, 64] # 0-indexed: 56 is row 57

for idx in indices_to_check:
    r = rows[idx]
    print(f"\n--- Row {idx+1} ---")
    for k, v in r.items():
        print(f"  {k}: {v}")
