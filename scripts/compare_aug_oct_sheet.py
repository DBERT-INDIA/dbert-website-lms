import csv
import re
import json

def clean_phone(p):
    digits = re.sub(r'\D', '', str(p or ''))
    return digits[-10:] if len(digits) >= 10 else ''

def clean_name(n):
    return re.sub(r'[^a-z0-9]', '', str(n or '').lower())

def main():
    # 1. Load the 56 sent certificates from sheet_data.csv
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_sent = [h.strip() for h in next(reader)]
        rows_sent = [r for r in reader if any(cell.strip() for cell in r)]
    sent_list = [{h: val.strip() for h, val in zip(h_sent, r)} for r in rows_sent]

    # Load registry to also see certIds
    with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
        registry = json.load(f)

    # Attach certId to sent_list by matching name
    for s in sent_list:
        s_name = clean_name(s.get('Name', ''))
        s['certId'] = ''
        for cid, reg in registry.items():
            if clean_name(reg.get('holderName', '')) == s_name:
                s['certId'] = cid
                break

    # Build lookup dictionaries
    sent_by_email = {}
    sent_by_phone = {}
    sent_by_name = {}

    for s in sent_list:
        em = s.get('Email Address', '').lower().strip()
        if em:
            sent_by_email[em] = s
        ph = clean_phone(s.get('WhatsApp number', ''))
        if ph:
            sent_by_phone[ph] = s
        nm = clean_name(s.get('Name', ''))
        if nm:
            sent_by_name[nm] = s

    # 2. Load aug_oct_sheet.csv
    with open('aug_oct_sheet.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_aug = [h.strip() for h in next(reader)]
        rows_aug = [r for r in reader if any(cell.strip() for cell in r)]
    aug_list = [{h: val.strip() for h, val in zip(h_aug, r)} for r in rows_aug]

    matched = []
    unmatched = []

    for idx, a in enumerate(aug_list):
        a_email = a.get('Email Address', '').lower().strip()
        a_phone = clean_phone(a.get('WhatsApp number', ''))
        a_name = clean_name(a.get('Name', ''))

        matched_sent = None
        match_type = None

        if a_email and a_email in sent_by_email:
            matched_sent = sent_by_email[a_email]
            match_type = f"Email: {a_email}"
        elif a_phone and a_phone in sent_by_phone:
            matched_sent = sent_by_phone[a_phone]
            match_type = f"Phone: {a_phone}"
        elif a_name and a_name in sent_by_name:
            matched_sent = sent_by_name[a_name]
            match_type = f"Name: {a.get('Name')}"

        if matched_sent:
            matched.append({
                'row_num': idx + 2, # accounting for header
                'aug': a,
                'sent': matched_sent,
                'match_type': match_type
            })
        else:
            unmatched.append({
                'row_num': idx + 2,
                'aug': a
            })

    print(f"Total rows in Aug-Oct sheet: {len(aug_list)}")
    print(f"Matched in 56 sent certificates: {len(matched)}")
    print(f"Not matched in 56 sent certificates: {len(unmatched)}")
    print("=" * 80)

    print("\nMATCHED CANDIDATES (" + str(len(matched)) + "):")
    for m in matched:
        a = m['aug']
        s = m['sent']
        print(f"Row {m['row_num']:03d}: {a.get('Name')} | {a.get('Email Address')} | Domain: {a.get('Select Internship')} | CertId: {s.get('certId')} (Matched via {m['match_type']})")

    print("\nUNMATCHED CANDIDATES (" + str(len(unmatched)) + ") - SAMPLE FIRST 15:")
    for u in unmatched[:15]:
        a = u['aug']
        print(f"Row {u['row_num']:03d}: {a.get('Name')} | {a.get('Email Address')} | {a.get('WhatsApp number')} | Domain: {a.get('Select Internship')} | College: {a.get('College Name')}")

    # Check domains in unmatched
    unmatched_domains = {}
    for u in unmatched:
        dom = u['aug'].get('Select Internship', 'Unknown')
        unmatched_domains[dom] = unmatched_domains.get(dom, 0) + 1
    print("\nUNMATCHED CANDIDATES BY DOMAIN:")
    for d, c in sorted(unmatched_domains.items(), key=lambda x: x[1], reverse=True):
        print(f"  {d}: {c}")

    # Check security deposit column in unmatched
    deposit_col_vals = {}
    for u in unmatched:
        dep = u['aug'].get('Refundable Security Deposit of 499/-', 'None')
        deposit_col_vals[dep] = deposit_col_vals.get(dep, 0) + 1
    print("\nUNMATCHED CANDIDATES BY REFUNDABLE DEPOSIT (499/-):")
    for dep, c in deposit_col_vals.items():
        print(f"  {dep}: {c}")

if __name__ == '__main__':
    main()
