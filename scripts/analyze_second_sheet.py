import csv
import re
import json

def clean_phone(p):
    digits = re.sub(r'\D', '', str(p or ''))
    return digits[-10:] if len(digits) >= 10 else ''

def clean_name(n):
    return re.sub(r'[^a-z0-9]', '', str(n or '').lower())

def main():
    # 1. Load 56 sent certificates
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_sent = [h.strip() for h in next(reader)]
        rows_sent = [r for r in reader if any(cell.strip() for cell in r)]
    sent_list = [{h: val.strip() for h, val in zip(h_sent, r)} for r in rows_sent]

    # Load registry
    with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)

    # 2. Load Sheet 1 (aug_oct_sheet.csv, 154 rows)
    with open('aug_oct_sheet.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h1 = [h.strip() for h in next(reader)]
        rows1 = [r for r in reader if any(cell.strip() for cell in r)]
    sheet1 = [{h: val.strip() for h, val in zip(h1, r)} for r in rows1]

    # 3. Load Sheet 2 (second_sheet.csv, 34 rows)
    with open('second_sheet.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h2 = [h.strip() for h in next(reader)]
        rows2 = [r for r in reader if any(cell.strip() for cell in r)]
    sheet2 = [{h: val.strip() for h, val in zip(h2, r)} for r in rows2]

    sent_emails = {s.get('Email Address', '').strip().lower(): s for s in sent_list}
    sent_phones = {clean_phone(s.get('WhatsApp number', '')): s for s in sent_list if clean_phone(s.get('WhatsApp number', ''))}
    # known phone overrides from previous analysis
    sent_phones['6280719402'] = sent_emails.get('gurveersukhan0613@gmail.com') # Gurveer Singh
    sent_phones['6290747930'] = sent_emails.get('arnakraydbpc@gmail.com')       # Arnak Ray
    sent_phones['7540083220'] = sent_emails.get('sakthi220107@gmail.com')       # Sakthi P
    sent_phones['9082013565'] = sent_emails.get('nikitaghuge44@gmail.com')      # Nikita Ghuge

    sheet1_emails = {s.get('Email Address', '').strip().lower(): s for s in sheet1}
    sheet1_phones = {clean_phone(s.get('WhatsApp number', '')): s for s in sheet1 if clean_phone(s.get('WhatsApp number', ''))}

    print("================================================================================")
    print("ANALYZING SHEET 2 (34 rows)")
    print("================================================================================")
    
    sheet2_in_sent = []
    sheet2_not_in_sent = []
    sheet2_in_sheet1 = []

    for idx, r in enumerate(sheet2):
        em = r.get('Email Address', '').strip().lower()
        ph = clean_phone(r.get('WhatsApp number', ''))
        nm = r.get('Name', '').strip()

        # check if in sent
        is_sent = False
        sent_match = None
        if em in sent_emails:
            is_sent = True
            sent_match = sent_emails[em]
        elif ph in sent_phones:
            is_sent = True
            sent_match = sent_phones[ph]

        if is_sent:
            sheet2_in_sent.append((idx + 2, r, sent_match))
        else:
            sheet2_not_in_sent.append((idx + 2, r))

        # check if in sheet 1
        if em in sheet1_emails or (ph and ph in sheet1_phones):
            sheet2_in_sheet1.append((idx + 2, r))

    print(f"Total rows in Sheet 2: {len(sheet2)}")
    print(f"Sheet 2 entries ALREADY in Sent 56: {len(sheet2_in_sent)}")
    for row, r, s in sheet2_in_sent:
        print(f"  Row {row:02d}: {r.get('Name')} | {r.get('Email Address')} | Sent Email: {s.get('Email Address')}")

    print(f"\nSheet 2 entries NOT in Sent 56 (Pending): {len(sheet2_not_in_sent)}")
    print(f"Sheet 2 entries overlapping with Sheet 1: {len(sheet2_in_sheet1)}")
    for row, r in sheet2_in_sheet1:
        print(f"  Overlap Row {row:02d}: {r.get('Name')} | {r.get('Email Address')}")

    # Now let's calculate GRAND TOTAL of remaining candidates across Sheet 1 + Sheet 2
    # Combined unique candidates
    all_pending_dict = {} # key = email
    
    # 1. From Sheet 1
    sheet1_pending_count = 0
    for idx, r in enumerate(sheet1):
        em = r.get('Email Address', '').strip().lower()
        ph = clean_phone(r.get('WhatsApp number', ''))
        if em not in sent_emails and ph not in sent_phones:
            sheet1_pending_count += 1
            if em not in all_pending_dict:
                all_pending_dict[em] = {
                    'source': 'Sheet 1 (Aug-Oct Main)',
                    'row': idx + 2,
                    'name': r.get('Name', '').strip(),
                    'email': em,
                    'phone': ph or r.get('WhatsApp number', '').strip(),
                    'domain': r.get('Select Internship', '').strip(),
                    'college': r.get('College Name', '').strip(),
                    'timestamp': r.get('Timestamp', '').strip(),
                    'security_deposit': r.get('Refundable Security Deposit of 499/-', '').strip()
                }

    # 2. From Sheet 2
    sheet2_new_pending_count = 0
    for idx, r in enumerate(sheet2):
        em = r.get('Email Address', '').strip().lower()
        ph = clean_phone(r.get('WhatsApp number', ''))
        if em not in sent_emails and ph not in sent_phones:
            if em not in all_pending_dict:
                sheet2_new_pending_count += 1
                all_pending_dict[em] = {
                    'source': 'Sheet 2 (Oct Sub-batch)',
                    'row': idx + 2,
                    'name': r.get('Name', '').strip(),
                    'email': em,
                    'phone': ph or r.get('WhatsApp number', '').strip(),
                    'domain': r.get('Select Internship', '').strip(),
                    'college': r.get('College Name', '').strip(),
                    'timestamp': r.get('Timestamp', '').strip(),
                    'security_deposit': r.get('Refundable Security Deposit of 499/-', '').strip()
                }
            else:
                print(f"Notice: {em} exists in both Sheet 1 and Sheet 2")

    print("\n" + "=" * 80)
    print("GRAND TOTAL CONSOLIDATION:")
    print("=" * 80)
    print(f"Sheet 1 Total Rows: {len(sheet1)}")
    print(f"  - In Sent 56: {len(sheet1) - sheet1_pending_count}")
    print(f"  - Pending in Sheet 1: {sheet1_pending_count}")
    print(f"Sheet 2 Total Rows: {len(sheet2)}")
    print(f"  - In Sent 56: {len(sheet2_in_sent)}")
    print(f"  - Pending in Sheet 2: {len(sheet2_not_in_sent)}")
    print(f"  - New unique pending from Sheet 2: {sheet2_new_pending_count}")
    print("--------------------------------------------------------------------------------")
    print(f"TOTAL UNIQUE PENDING CANDIDATES ACROSS BOTH SHEETS: {len(all_pending_dict)}")
    print("=" * 80)

    # Save to consolidated CSV
    with open('data/grand_total_pending_candidates.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'source', 'row', 'name', 'email', 'phone', 'domain', 'college', 'timestamp', 'security_deposit'
        ])
        writer.writeheader()
        writer.writerows(all_pending_dict.values())
    print("Saved consolidated pending list to data/grand_total_pending_candidates.csv")

if __name__ == '__main__':
    main()
