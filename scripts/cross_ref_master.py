import csv
import json

def main():
    # Load 56 sent
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_sent = [h.strip() for h in next(reader)]
        rows_sent = [r for r in reader if any(cell.strip() for cell in r)]
    sent = [{h: val.strip() for h, val in zip(h_sent, r)} for r in rows_sent]
    sent_emails = {s.get('Email Address', '').strip().lower() for s in sent}

    # Load 148 pending
    with open('data/grand_total_pending_candidates.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        pending_148 = list(reader)
    pending_emails = {p['email'].strip().lower() for p in pending_148}

    # Load all_enrolled_interns_master_detailed.csv
    with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        all_master = list(reader)

    print(f"Total rows in all_enrolled_interns_master_detailed.csv: {len(all_master)}")
    
    in_sent = 0
    in_pending_148 = 0
    other_not_in_sent = 0
    
    batches_summary = {}

    for r in all_master:
        em = r.get('Email', '').strip().lower()
        b = r.get('Source_Batches_List', '')
        
        is_sent = em in sent_emails
        is_p148 = em in pending_emails
        
        if is_sent:
            in_sent += 1
        elif is_p148:
            in_pending_148 += 1
        else:
            other_not_in_sent += 1
            batches_summary[b] = batches_summary.get(b, 0) + 1

    print(f"Master file interns in 56 Sent: {in_sent}")
    print(f"Master file interns in 148 Pending (Aug-Oct): {in_pending_148}")
    print(f"Master file interns NOT in Sent and NOT in 148: {other_not_in_sent}")
    print("\nBatches of other master file interns:")
    for b, c in sorted(batches_summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  {b}: {c}")

if __name__ == '__main__':
    main()
