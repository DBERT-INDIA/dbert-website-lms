import csv
import json
import re
import os

def clean_phone(p):
    digits = re.sub(r'\D', '', str(p or ''))
    return digits[-10:] if len(digits) >= 10 else ''

def main():
    # 1. Load sent certificates (sheet_data.csv)
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_sent = [h.strip() for h in next(reader)]
        rows_sent = [r for r in reader if any(cell.strip() for cell in r)]
    sent_list = [{h: val.strip() for h, val in zip(h_sent, r)} for r in rows_sent]

    # Load registry
    with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)

    for s in sent_list:
        s['certId'] = ''
        s_email = s.get('Email Address', '').strip().lower()
        for cid, reg in registry.items():
            # Check match by holder name or verification url
            reg_name = reg.get('holderName', '').strip().lower()
            s_name = s.get('Name', '').strip().lower()
            if reg_name == s_name:
                s['certId'] = cid
                break

    # 2. Load Aug-Oct sheet (aug_oct_sheet.csv)
    with open('aug_oct_sheet.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_aug = [h.strip() for h in next(reader)]
        rows_aug = [r for r in reader if any(cell.strip() for cell in r)]
    aug_list = [{h: val.strip() for h, val in zip(h_aug, r)} for r in rows_aug]

    # Map sent
    sent_by_email = {s['Email Address'].strip().lower(): s for s in sent_list}
    
    # Phone overrides for students who used university email on registration and personal gmail on cert form
    # 6280719402 -> Gurveer Singh
    # 6290747930 -> Arnak Ray
    # 7540083220 -> Sakthi P
    # 9082013565 -> Nikita Khandu Ghuge (Row 90 and Row 92)
    phone_map = {
        '6280719402': sent_by_email.get('gurveersukhan0613@gmail.com'),
        '6290747930': sent_by_email.get('arnakraydbpc@gmail.com'),
        '7540083220': sent_by_email.get('sakthi220107@gmail.com'),
        '9082013565': sent_by_email.get('nikitaghuge44@gmail.com'),
    }

    matched = []
    unmatched = []

    for idx, a in enumerate(aug_list):
        row_id = idx + 2
        a_email = a.get('Email Address', '').strip().lower()
        a_phone = clean_phone(a.get('WhatsApp number', ''))
        
        match_record = None
        method = ""
        
        if a_email in sent_by_email:
            match_record = sent_by_email[a_email]
            method = "Exact Email"
        elif a_phone in phone_map:
            match_record = phone_map[a_phone]
            method = f"Phone Match ({a_phone})"

        if match_record:
            matched.append({
                'sheet_row': row_id,
                'name': a.get('Name'),
                'sheet_email': a.get('Email Address'),
                'sent_email': match_record.get('Email Address'),
                'domain': a.get('Select Internship'),
                'college': a.get('College Name'),
                'phone': a.get('WhatsApp number'),
                'cert_id': match_record.get('certId', ''),
                'match_method': method
            })
        else:
            unmatched.append({
                'sheet_row': row_id,
                'timestamp': a.get('Timestamp'),
                'name': a.get('Name'),
                'email': a.get('Email Address'),
                'domain': a.get('Select Internship'),
                'college': a.get('College Name'),
                'phone': a.get('WhatsApp number'),
                'placement_needed': a.get('Do you require job placement after completion of Internship?'),
                'paid_training_open': a.get('Are you open for Paid Training with Placement Guarantee ?'),
                'security_deposit_url': a.get('Refundable Security Deposit of 499/-')
            })

    os.makedirs('data', exist_ok=True)

    # Save matched
    with open('data/aug_oct_matched_56.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'sheet_row', 'name', 'sheet_email', 'sent_email', 'domain', 'college', 'phone', 'cert_id', 'match_method'
        ])
        writer.writeheader()
        writer.writerows(matched)

    # Save unmatched
    with open('data/aug_oct_unmatched_pending.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'sheet_row', 'timestamp', 'name', 'email', 'domain', 'college', 'phone', 'placement_needed', 'paid_training_open', 'security_deposit_url'
        ])
        writer.writeheader()
        writer.writerows(unmatched)

    print(f"Aug-Oct Sheet Total Rows: {len(aug_list)}")
    print(f"Matched in Sent Batch: {len(matched)} rows (representing {len(set(m['name'].strip().lower() for m in matched))} unique individuals)")
    print(f"Unmatched (Pending): {len(unmatched)} rows")
    print("Files saved:")
    print("  - data/aug_oct_matched_56.csv")
    print("  - data/aug_oct_unmatched_pending.csv")

if __name__ == '__main__':
    main()
