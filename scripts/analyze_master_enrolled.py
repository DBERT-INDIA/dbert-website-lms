import csv
import json
from datetime import datetime

def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y'):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            pass
    return None

def main():
    # 1. Load the 56 already sent
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_sent = [h.strip() for h in next(reader)]
        rows_sent = [r for r in reader if any(cell.strip() for cell in r)]
    sent = [{h: val.strip() for h, val in zip(h_sent, r)} for r in rows_sent]
    sent_emails = {s.get('Email Address', '').strip().lower() for s in sent if s.get('Email Address')}
    print(f"Loaded {len(sent)} sent records ({len(sent_emails)} unique emails).")

    # 2. Also check certificates_registry.json
    with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)
    reg_sent_emails = {r.get('email', '').strip().lower() for r in registry.values() if not r.get('isProvisional') and r.get('email')}
    print(f"Verified non-provisional emails in registry: {len(reg_sent_emails)}")
    all_excluded_emails = sent_emails.union(reg_sent_emails)

    # 3. Read all_enrolled_interns_master_detailed.csv
    with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"\nTotal rows in all_enrolled_interns_master_detailed.csv: {len(rows)}")

    # Check columns
    print("Columns:", reader.fieldnames)

    # Analyze
    unique_candidates = {}
    already_sent_count = 0
    excluded_rows = []
    eligible_rows = []

    for r in rows:
        email = (r.get('Email') or '').strip().lower()
        if not email:
            continue
        
        if email in all_excluded_emails:
            already_sent_count += 1
            excluded_rows.append(r)
        else:
            if email not in unique_candidates:
                unique_candidates[email] = r
                eligible_rows.append(r)

    print(f"Candidates matched to 56 already sent: {already_sent_count}")
    print(f"Unique eligible candidates to be sent emails: {len(unique_candidates)}")

    # Analyze domains for eligible
    domain_counts = {}
    batch_source_counts = {}
    timestamp_distribution = {}

    for r in eligible_rows:
        dom = (r.get('Primary_Technical_Domain') or 'Unknown').strip()
        domain_counts[dom] = domain_counts.get(dom, 0) + 1

        b_src = (r.get('Source_Batches_List') or 'None').strip()
        batch_source_counts[b_src] = batch_source_counts.get(b_src, 0) + 1

        # Timestamps
        earliest = (r.get('Earliest_Registration_Timestamp') or '').strip()
        latest = (r.get('Latest_Registration_Timestamp') or '').strip()
        ts = earliest or latest
        if ts:
            dt = parse_date(ts)
            if dt:
                month_key = dt.strftime('%Y-%m')
            else:
                month_key = ts[:7]
        else:
            month_key = 'Missing'
        timestamp_distribution[month_key] = timestamp_distribution.get(month_key, 0) + 1

    print("\n--- ELIGIBLE CANDIDATES BY DOMAIN ---")
    for d, c in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {d}: {c}")

    print("\n--- ELIGIBLE CANDIDATES BY SOURCE BATCH LIST ---")
    for b, c in sorted(batch_source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {b}: {c}")

    print("\n--- ELIGIBLE CANDIDATES BY REGISTRATION MONTH (TIMESTAMP) ---")
    for m, c in sorted(timestamp_distribution.items()):
        print(f"  {m}: {c}")

if __name__ == '__main__':
    main()
