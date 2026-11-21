import urllib.request
import csv
import io
import json
import re
from pathlib import Path

def normalize_phone(phone_str):
    if not phone_str:
        return ""
    digits = re.sub(r'\D', '', str(phone_str))
    if len(digits) > 10 and digits.startswith('91'):
        digits = digits[2:]
    elif len(digits) > 10 and digits.startswith('0'):
        digits = digits[1:]
    return digits[-10:] if len(digits) >= 10 else digits

def normalize_email(email_str):
    if not email_str:
        return ""
    return str(email_str).strip().lower()

# 1. Fetch Google Sheet gid=1265293201
url = 'https://docs.google.com/spreadsheets/d/1yacGLZGiTD_8GLOUHMphbdfsORqc8u_DrjvpVRSEDgs/export?format=csv&gid=1265293201'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
print(f"Downloading sheet from {url} ...")
with urllib.request.urlopen(req, timeout=20) as resp:
    csv_text = resp.read().decode('utf-8')

reader = csv.reader(io.StringIO(csv_text))
sheet_rows = list(reader)
print(f"Total rows in Google Sheet: {len(sheet_rows)}")
header = sheet_rows[0]
print("Header:", header)

# Map sheet records
sheet_records = []
for row_idx, r in enumerate(sheet_rows[1:], start=2):
    # Let's inspect column mapping
    row_dict = {
        "row_idx": row_idx,
        "raw": r,
        "email": normalize_email(r[1] if len(r) > 1 else ""),
        "phone": normalize_phone(r[7] if len(r) > 7 else (r[2] if len(r) > 2 else "")),
        "name": r[5] if len(r) > 5 else "",
        "track": r[3] if len(r) > 3 else "",
        "college": r[6] if len(r) > 6 else "",
    }
    # Also check if any column looks like phone
    for cell in r:
        p_clean = normalize_phone(cell)
        if len(p_clean) == 10 and p_clean.isdigit():
            row_dict["all_phones"] = row_dict.get("all_phones", []) + [p_clean]
    sheet_records.append(row_dict)

print(f"Parsed {len(sheet_records)} sheet records.")

# Save locally to inspect
with open("data/sheet_1265293201_parsed.json", "w", encoding="utf-8") as f:
    json.dump(sheet_records, f, indent=2)

print("Saved to data/sheet_1265293201_parsed.json")
