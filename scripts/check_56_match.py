import csv
import json

def main():
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h = [col.strip() for col in next(reader)]
        rows = [r for r in reader if any(cell.strip() for cell in r)]
    sent_56 = [{col: val.strip() for col, val in zip(h, r)} for r in rows]

    with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        master_interns = list(reader)

    master_emails = {m.get('Email', '').strip().lower(): m for m in master_interns if m.get('Email')}
    master_names = {m.get('Full_Name', '').strip().lower(): m for m in master_interns if m.get('Full_Name')}

    matched_by_email = []
    matched_by_name_only = []
    unmatched_56 = []

    for s in sent_56:
        em = s.get('Email Address', '').strip().lower()
        name = s.get('Intern Name', '').strip().lower()

        if em in master_emails:
            matched_by_email.append((s, master_emails[em]))
        elif name in master_names:
            matched_by_name_only.append((s, master_names[name]))
        else:
            unmatched_56.append(s)

    print(f"56 Sent total: {len(sent_56)}")
    print(f"Matched by exact email in master: {len(matched_by_email)}")
    print(f"Matched by name only (different email) in master: {len(matched_by_name_only)}")
    print(f"Unmatched in master: {len(unmatched_56)}")

    if matched_by_name_only:
        print("\nMatched by name only:")
        for s, m in matched_by_name_only:
            print(f"  Name: {s.get('Intern Name')} | Sent Email: {s.get('Email Address')} | Master Email: {m.get('Email')}")

    if unmatched_56:
        print("\nUnmatched 56 candidates (sample):")
        for s in unmatched_56[:5]:
            print(f"  {s.get('Intern Name')} | {s.get('Email Address')} | Batch: {s.get('Batch')}")

if __name__ == '__main__':
    main()
