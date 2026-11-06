import csv
from datetime import datetime
from collections import defaultdict

def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ('%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y'):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            pass
    return None

def main():
    with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Load 56 sent
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        r2 = csv.reader(f)
        h2 = [c.strip() for c in next(r2)]
        sent_emails = {r[h2.index('Email Address')].strip().lower() for r in r2 if any(r) and 'Email Address' in h2 and r[h2.index('Email Address')].strip()}

    cohort_mapping = {}

    for r in rows:
        email = (r.get('Email') or '').strip().lower()
        if not email or email in sent_emails:
            continue
        
        batch_src = (r.get('Source_Batches_List') or '').strip()
        ts_early = parse_date(r.get('Earliest_Registration_Timestamp'))
        ts_late = parse_date(r.get('Latest_Registration_Timestamp'))
        ts = ts_late or ts_early

        key = (batch_src, ts.strftime('%Y-%m') if ts else 'No Date')
        cohort_mapping[key] = cohort_mapping.get(key, 0) + 1

    print("Batch + Registration Month Distribution:")
    for (b, m), cnt in sorted(cohort_mapping.items(), key=lambda x: (x[0][0], x[0][1])):
        print(f"  Batch: {b:<35} | Reg Month: {m:<10} | Candidates: {cnt}")

if __name__ == '__main__':
    main()
