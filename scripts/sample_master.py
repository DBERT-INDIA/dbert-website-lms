import csv

with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
    reader = csv.DictReader(f)
    for i, r in enumerate(reader):
        if i >= 20: break
        print(f"{i+1}. {r.get('Full_Name')} | {r.get('Email')} | {r.get('Primary_Technical_Domain')} | Batch: {r.get('Source_Batches_List')} | TS: {r.get('Earliest_Registration_Timestamp')}")
