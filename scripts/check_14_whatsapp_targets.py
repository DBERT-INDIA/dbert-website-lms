import json
import psycopg2
import sys

sys.stdout.reconfigure(encoding='utf-8')

subs = json.load(open('data/verification_submissions_299.json', encoding='utf-8'))[4:]

# Query remote DB on EC2 or inspect candidate details locally first
for idx, s in enumerate(subs, 1):
    print(f"{idx}. {s.get('fullName')} | Cert: {s.get('certId')} | Phone: {s.get('phone')} | Email: {s.get('email')}")
