import csv
import re

def clean_phone(p):
    d = re.sub(r'\D', '', str(p or ''))
    return d[-10:] if len(d) >= 10 else ''

def main():
    with open('sheet_data.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_sent = [h.strip() for h in next(reader)]
        rows_sent = [r for r in reader if any(cell.strip() for cell in r)]
    sent = [{h: val.strip() for h, val in zip(h_sent, r)} for r in rows_sent]

    with open('aug_oct_sheet.csv', 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        h_aug = [h.strip() for h in next(reader)]
        rows_aug = [r for r in reader if any(cell.strip() for cell in r)]
    aug = [{h: val.strip() for h, val in zip(h_aug, r)} for r in rows_aug]

    sent_emails = {s.get('Email Address', '').strip().lower(): s for s in sent}
    sent_phones = {clean_phone(s.get('WhatsApp number', '')): s for s in sent if clean_phone(s.get('WhatsApp number', ''))}
    sent_names = {s.get('Name', '').strip().lower(): s for s in sent}

    matched_indices = {}

    # Pass 1: exact email
    for idx, a in enumerate(aug):
        em = a.get('Email Address', '').strip().lower()
        if em in sent_emails:
            matched_indices[idx] = ('Email', sent_emails[em])

    # Pass 2: phone
    for idx, a in enumerate(aug):
        if idx in matched_indices:
            continue
        ph = clean_phone(a.get('WhatsApp number', ''))
        if ph in sent_phones:
            matched_indices[idx] = (f'Phone ({ph})', sent_phones[ph])

    # Pass 3: exact full name (case-insensitive)
    for idx, a in enumerate(aug):
        if idx in matched_indices:
            continue
        nm = a.get('Name', '').strip().lower()
        if nm in sent_names:
            matched_indices[idx] = (f'Exact Name ({a.get("Name")})', sent_names[nm])

    print("=================================================================")
    print("PRECISE MATCH RESULTS:")
    print("=================================================================")
    print(f"Total entries in Aug-Oct sheet: {len(aug)}")
    print(f"Matched entries: {len(matched_indices)}")
    print(f"Unmatched entries: {len(aug) - len(matched_indices)}")
    print("-----------------------------------------------------------------")

    for idx, (method, s) in sorted(matched_indices.items()):
        a = aug[idx]
        print(f"Row {idx+2:03d}: {a.get('Name')} | Aug-Email: {a.get('Email Address')} | Sent-Email: {s.get('Email Address')} | Via: {method}")

if __name__ == '__main__':
    main()
