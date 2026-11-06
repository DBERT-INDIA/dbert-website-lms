import csv
import re
import json

def clean_phone(p):
    digits = re.sub(r'\D', '', str(p or ''))
    return digits[-10:] if len(digits) >= 10 else ''

def clean_name(n):
    return re.sub(r'[^a-z0-9]', '', str(n or '').lower())

def main():
    # 1. Load sent 56 certificates
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_sent = [h.strip() for h in next(reader)]
        rows_sent = [r for r in reader if any(cell.strip() for cell in r)]
    sent_list = [{h: val.strip() for h, val in zip(h_sent, r)} for r in rows_sent]

    with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)

    # Attach certId
    for s in sent_list:
        s_name = clean_name(s.get('Name', ''))
        s['certId'] = ''
        for cid, reg in registry.items():
            if clean_name(reg.get('holderName', '')) == s_name:
                s['certId'] = cid
                break

    # 2. Load Aug-Oct sheet (154 entries)
    with open('aug_oct_sheet.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_aug = [h.strip() for h in next(reader)]
        rows_aug = [r for r in reader if any(cell.strip() for cell in r)]
    aug_list = [{h: val.strip() for h, val in zip(h_aug, r)} for r in rows_aug]

    # Map sent entries
    sent_by_email = {s.get('Email Address', '').lower().strip(): s for s in sent_list}
    sent_by_phone = {clean_phone(s.get('WhatsApp number', '')): s for s in sent_list if clean_phone(s.get('WhatsApp number', ''))}
    sent_by_name = {clean_name(s.get('Name', '')): s for s in sent_list}

    # Match each Aug-Oct row
    matched_aug = []
    unmatched_aug = []
    matched_sent_ids = set()

    for idx, a in enumerate(aug_list):
        row_num = idx + 2
        em = a.get('Email Address', '').lower().strip()
        ph = clean_phone(a.get('WhatsApp number', ''))
        nm = clean_name(a.get('Name', ''))

        matched_s = None
        how = ""

        if em in sent_by_email:
            matched_s = sent_by_email[em]
            how = "Exact Email"
        elif ph and ph in sent_by_phone:
            matched_s = sent_by_phone[ph]
            how = f"WhatsApp ({ph})"
        elif nm and nm in sent_by_name:
            matched_s = sent_by_name[nm]
            how = f"Name match ({a.get('Name')})"

        if matched_s:
            matched_aug.append({
                'row_num': row_num,
                'aug': a,
                'sent': matched_s,
                'how': how
            })
            matched_sent_ids.add(matched_s.get('certId') or matched_s.get('Email Address'))
        else:
            unmatched_aug.append({
                'row_num': row_num,
                'aug': a
            })

    # Now check the 56 sent certificates
    sent_in_aug_sheet = []
    sent_not_in_aug_sheet = []

    for s in sent_list:
        ident = s.get('certId') or s.get('Email Address')
        if ident in matched_sent_ids:
            sent_in_aug_sheet.append(s)
        else:
            sent_not_in_aug_sheet.append(s)

    print("================================================================================")
    print("EXECUTIVE SUMMARY:")
    print("================================================================================")
    print(f"Total entries in Aug-Oct Google Sheet: {len(aug_list)}")
    print(f"Total sent certificate packages: {len(sent_list)}")
    print("--------------------------------------------------------------------------------")
    print(f"1. Aug-Oct entries ALREADY in the 56 sent certificates: {len(matched_aug)}")
    print(f"2. Aug-Oct entries NOT in the 56 sent certificates: {len(unmatched_aug)}")
    print("--------------------------------------------------------------------------------")
    print(f"Of the 56 sent certificates:")
    print(f" - Found in Aug-Oct Sheet: {len(sent_in_aug_sheet)}")
    print(f" - NOT in Aug-Oct Sheet: {len(sent_not_in_aug_sheet)} (Other batches or distinct emails)")
    print("================================================================================")

    print("\n--- BATCH COMPOSITION OF SENT CERTIFICATES NOT IN AUG-OCT SHEET ---")
    other_batches = {}
    for s in sent_not_in_aug_sheet:
        b = s.get('Choose Internship Batch', 'Unknown')
        other_batches[b] = other_batches.get(b, 0) + 1
    for b, c in other_batches.items():
        print(f"  {b}: {c}")

    print("\n--- LIST OF 56 SENT WHO WERE NOT IN THE AUG-OCT SHEET ---")
    for s in sent_not_in_aug_sheet:
        print(f"  {s.get('certId')} | {s.get('Name')} | {s.get('Email Address')} | Batch: {s.get('Choose Internship Batch')} | Domain: {s.get('Select Internship')}")

    print("\n--- SUMMARY OF UNMATCHED AUG-OCT CANDIDATES (117) BY DOMAIN ---")
    domains = {}
    for u in unmatched_aug:
        dom = u['aug'].get('Select Internship', 'Unknown')
        domains[dom] = domains.get(dom, 0) + 1
    for d, c in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        print(f"  {d}: {c}")

    print("\n--- SUMMARY OF UNMATCHED AUG-OCT CANDIDATES BY REFUNDABLE DEPOSIT (499/-) ---")
    deposits_with_link = 0
    deposits_without_link = 0
    for u in unmatched_aug:
        dep = u['aug'].get('Refundable Security Deposit of 499/-', '').strip()
        if dep.startswith('http'):
            deposits_with_link += 1
        else:
            deposits_without_link += 1
    print(f"  Deposit screenshot uploaded (Google Drive link): {deposits_with_link}")
    print(f"  No deposit link: {deposits_without_link}")

if __name__ == '__main__':
    main()
