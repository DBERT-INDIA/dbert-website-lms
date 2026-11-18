import urllib.request
import csv
import io
import json

URL = 'https://docs.google.com/spreadsheets/d/1DsWUtSTSJopcjLbGtjhDJ67BWTz7Uvv3BqRCt_f77Xk/export?format=csv&gid=198139462'

def analyze_sheet():
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode('utf-8', errors='ignore')

    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    if not rows:
        print("Empty sheet!")
        return

    header = rows[0]
    print(f"Header: {header}")
    data_rows = rows[1:]
    print(f"Total data rows in sheet: {len(data_rows)}")

    # Email column index
    email_idx = -1
    for i, col in enumerate(header):
        if 'email' in col.lower():
            email_idx = i
            break
    print(f"Email column index: {email_idx} ('{header[email_idx]}')")

    emails = []
    seen = set()
    duplicates = 0
    empty = 0
    for r in data_rows:
        if len(r) > email_idx:
            e = r[email_idx].strip().lower()
            if not e:
                empty += 1
            elif e in seen:
                duplicates += 1
                emails.append(e)
            else:
                seen.add(e)
                emails.append(e)
        else:
            empty += 1

    print(f"Total non-empty email entries: {len(emails)}")
    print(f"Unique non-empty emails: {len(seen)}")
    print(f"Duplicate email rows: {duplicates}")
    print(f"Empty email rows: {empty}")

    # Check status / other columns distribution
    if 'Approval Status' in header:
        app_idx = header.index('Approval Status')
        status_counts = {}
        for r in data_rows:
            st = r[app_idx].strip() if len(r) > app_idx else ''
            status_counts[st] = status_counts.get(st, 0) + 1
        print("\nApproval Status distribution in sheet:")
        for st, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  '{st}': {count}")

    # Save unique emails to a json file for cross-checking against production DB
    with open("data/sheet_emails_198139462.json", "w", encoding="utf-8") as f:
        json.dump(list(seen), f, indent=2)
    print(f"\nSaved {len(seen)} unique emails to data/sheet_emails_198139462.json")

if __name__ == '__main__':
    analyze_sheet()
