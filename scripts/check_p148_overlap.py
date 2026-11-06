import csv

def main():
    with open('data/grand_total_pending_candidates.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        p148 = list(reader)
    p148_emails = {p['email'].strip().lower() for p in p148}

    with open('all_enrolled_interns_master_detailed.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)
        master = list(reader)
    master_emails = {m.get('Email', '').strip().lower() for m in master}

    in_both = p148_emails.intersection(master_emails)
    only_in_p148 = p148_emails - master_emails
    only_in_master = master_emails - p148_emails

    print(f"Total in 148 pending: {len(p148_emails)}")
    print(f"Total in master file: {len(master_emails)}")
    print(f"Overlap (in both): {len(in_both)}")
    print(f"In 148 pending but NOT in master: {len(only_in_p148)}")
    print(f"In master but NOT in 148 pending: {len(only_in_master)}")

    if only_in_p148:
        print("\nSamples in 148 pending but not in master:")
        for em in list(only_in_p148)[:5]:
            print(f"  {em}")

if __name__ == '__main__':
    main()
