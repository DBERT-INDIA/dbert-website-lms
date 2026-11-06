import csv
import difflib

with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
    sent = list(csv.DictReader(f))

with open('aug_oct_sheet.csv', 'r', encoding='utf-8', errors='replace') as f:
    aug = list(csv.DictReader(f))

print("Checking fuzzy matches between sent and Aug-Oct sheet...")
found_any = False
for s in sent:
    s_name = s.get('Name', '').strip()
    s_email = s.get('Email Address', '').strip()
    for idx, a in enumerate(aug):
        a_name = a.get('Name', '').strip()
        a_email = a.get('Email Address', '').strip()
        sim = difflib.SequenceMatcher(None, s_name.lower(), a_name.lower()).ratio()
        if 0.70 <= sim < 1.0 and len(s_name) > 5 and len(a_name) > 5:
            # check if first names or last names match
            s_parts = set(s_name.lower().split())
            a_parts = set(a_name.lower().split())
            if s_parts.intersection(a_parts):
                print(f"Match candidate: Sent [{s_name} | {s_email}] <---> Aug-Oct Row {idx+2} [{a_name} | {a_email}] (Ratio: {sim:.2f})")
                found_any = True

if not found_any:
    print("No additional fuzzy matches found.")
