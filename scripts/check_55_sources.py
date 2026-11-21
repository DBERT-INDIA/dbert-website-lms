import sys
import os
import json

if os.path.exists('/var/www/dbert-website-lms/apps/portal'):
    sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
else:
    sys.path.insert(0, 'apps/portal')

from app import get_db

with get_db() as conn:
    rows = conn.execute("""
        SELECT id, name, email, phone, domain, source, visitor_id, intent_answers, created_at
        FROM applications
        WHERE status = 'Under Review'
        ORDER BY id DESC
    """).fetchall()

    results = []
    sources_count = {}
    for r in rows:
        d = dict(r) if hasattr(r, 'keys') else {
            'id': r[0], 'name': r[1], 'email': r[2], 'phone': r[3], 'domain': r[4],
            'source': r[5], 'visitor_id': r[6], 'intent_answers': r[7], 'created_at': str(r[8])
        }
        s = str(d.get('source') or 'NULL/Organic')
        sources_count[s] = sources_count.get(s, 0) + 1
        results.append(d)

    print("=== Source Column Breakdown in applications table ===")
    for s, count in sorted(sources_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  Source: '{s}': {count}")

    print("\n=== Check Cross-Referencing in LMS Database ===")
    # Check if they exist in scraped_leads, referrals, or user_sessions
    scraped_matches = 0
    ref_matches = 0
    for cand in results:
        email = cand['email'].lower()
        try:
            sl = conn.execute("SELECT id, source FROM scraped_leads WHERE LOWER(email)=?", (email,)).fetchone()
            if sl:
                cand['scraped_lead'] = dict(sl) if hasattr(sl, 'keys') else {'id': sl[0], 'source': sl[1]}
                scraped_matches += 1
        except Exception:
            pass

        try:
            rf = conn.execute("SELECT id, ref_code, referrer_id FROM referrals WHERE LOWER(referred_email)=?", (email,)).fetchone()
            if rf:
                cand['referral'] = dict(rf) if hasattr(rf, 'keys') else {'id': rf[0], 'ref_code': rf[1]}
                ref_matches += 1
        except Exception:
            pass

    print(f"Found in scraped_leads: {scraped_matches}")
    print(f"Found in referrals: {ref_matches}")

    print("\n=== Sample of 15 Candidates with Source & Created Date ===")
    for cand in results[:15]:
        print(f"  ID {cand['id']}: {cand['name']} | {cand['email']} | Source: {cand.get('source')} | Created: {cand['created_at']}")

    # Save to file on EC2
    with open('/tmp/under_review_sources.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
