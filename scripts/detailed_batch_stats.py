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
    # Load 56 sent emails
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h = [col.strip() for col in next(reader)]
        rows = [r for r in reader if any(cell.strip() for cell in r)]
    sent_56_emails = {r[h.index('Email Address')].strip().lower() for r in rows if 'Email Address' in h and r[h.index('Email Address')].strip()}

    with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)

    print(f"Total rows in master file: {len(all_rows)}")

    # Deduplicate by email while excluding 56
    excluded_count = 0
    unique_candidates = {}

    for r in all_rows:
        em = (r.get('Email') or '').strip().lower()
        if not em:
            continue
        if em in sent_56_emails:
            excluded_count += 1
            continue
        if em not in unique_candidates:
            unique_candidates[em] = r

    print(f"56 Sent candidates excluded: {excluded_count}")
    print(f"Total unique eligible candidates remaining: {len(unique_candidates)}")

    # Group by Source_Batches_List and analyze timestamps
    batch_stats = defaultdict(lambda: {'count': 0, 'min_ts': None, 'max_ts': None, 'domains': defaultdict(int), 'sample_dates': []})

    for em, r in unique_candidates.items():
        src_batch = (r.get('Source_Batches_List') or 'UNKNOWN').strip()
        domain = (r.get('Primary_Technical_Domain') or 'General').strip()
        
        ts_str = (r.get('Earliest_Registration_Timestamp') or r.get('Latest_Registration_Timestamp') or '').strip()
        dt = parse_date(ts_str)

        st = batch_stats[src_batch]
        st['count'] += 1
        st['domains'][domain] += 1
        if dt:
            if st['min_ts'] is None or dt < st['min_ts']:
                st['min_ts'] = dt
            if st['max_ts'] is None or dt > st['max_ts']:
                st['max_ts'] = dt
            st['sample_dates'].append(dt)

    print("\n" + "=" * 90)
    print("DETAILED BATCH BREAKDOWN (SORTED BY COUNT)")
    print("=" * 90)
    for src_batch, st in sorted(batch_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        min_s = st['min_ts'].strftime('%Y-%m-%d') if st['min_ts'] else 'N/A'
        max_s = st['max_ts'].strftime('%Y-%m-%d') if st['max_ts'] else 'N/A'
        print(f"\nBatch Tag: '{src_batch}' | Candidates: {st['count']} | Reg Date Range: {min_s} to {max_s}")
        print("  Domains:")
        for dom, d_cnt in sorted(st['domains'].items(), key=lambda x: x[1], reverse=True):
            print(f"    - {dom}: {d_cnt}")

if __name__ == '__main__':
    main()
