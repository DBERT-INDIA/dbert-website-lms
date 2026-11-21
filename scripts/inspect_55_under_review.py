import sys
import os
import json
import re

if os.path.exists('/var/www/dbert-website-lms/apps/portal'):
    sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
else:
    sys.path.insert(0, 'apps/portal')

from app import get_db

with get_db() as conn:
    rows = conn.execute("""
        SELECT a.id, a.name, a.email, a.phone, a.domain, a.status, a.created_at,
               (SELECT count(*) FROM intern_offer_letters o WHERE LOWER(o.email) = LOWER(a.email)) as has_offer,
               (SELECT count(*) FROM enrollments e WHERE LOWER(e.email) = LOWER(a.email)) as has_enr
        FROM applications a
        WHERE a.status = 'Under Review'
        ORDER BY a.id DESC
    """).fetchall()

    results = []
    print(f"Total Under Review Applications: {len(rows)}")
    for r in rows:
        d = dict(r) if hasattr(r, 'keys') else {
            'id': r[0], 'name': r[1], 'email': r[2], 'phone': r[3], 'domain': r[4],
            'status': r[5], 'created_at': str(r[6]), 'has_offer': r[7], 'has_enr': r[8]
        }
        # Clean phone
        raw_phone = d.get('phone', '')
        digits = re.sub(r'\D', '', str(raw_phone))
        if digits.startswith('91') and len(digits) == 12:
            clean_p = digits
        elif len(digits) == 10:
            clean_p = '91' + digits
        elif digits.startswith('0') and len(digits) == 11:
            clean_p = '91' + digits[1:]
        else:
            clean_p = digits
        d['clean_phone'] = clean_p
        d['is_valid_phone'] = len(clean_p) == 12 and clean_p.startswith('91')
        results.append(d)

    print("\n--- Summary Breakdown ---")
    valid_phones = sum(1 for x in results if x['is_valid_phone'])
    has_offers = sum(1 for x in results if x['has_offer'] > 0)
    has_enrs = sum(1 for x in results if x['has_enr'] > 0)
    print(f"Total: {len(results)}")
    print(f"Valid Indian Phone (+91 10-digits): {valid_phones}")
    print(f"Already have Offer Letter: {has_offers}")
    print(f"Already have Enrollment Record: {has_enrs}")

    print("\n--- Domains Breakdown ---")
    domains = {}
    for x in results:
        dom = x['domain']
        domains[dom] = domains.get(dom, 0) + 1
    for dom, cnt in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dom}: {cnt}")

    print("\n--- First 15 Candidates ---")
    for x in results[:15]:
        print(f"  ID {x['id']}: {x['name']} | {x['email']} | {x['clean_phone']} (valid: {x['is_valid_phone']}) | {x['domain']} | {x['created_at']}")

    # Save to file on EC2 for reference
    with open('/tmp/under_review_55.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print("\nSaved full list to /tmp/under_review_55.json")
