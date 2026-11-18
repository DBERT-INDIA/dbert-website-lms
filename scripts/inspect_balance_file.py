import json

try:
    with open('data/balance_enrollments_remote.json', 'r', encoding='utf-8') as f:
        d = json.load(f)
    print(f"Total entries in balance_enrollments_1500.json: {len(d)}")
    for item in d:
        print(f"  {item.get('candidateName')} | {item.get('email')} | Paid: {item.get('amountPaid')} | UTR: {item.get('utr')} | Status: {item.get('status')}")
except Exception as e:
    print("Error reading balance file:", e)
