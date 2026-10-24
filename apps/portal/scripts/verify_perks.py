import sys, time
sys.path.append('apps/portal')
time.sleep(1)

from app import app, get_db
app.config['TESTING'] = True
c = app.test_client()

# Test lead with disclosed stipend (id 1351 had $20k-$35k)
tests = [
    (1,    'No stipend – should show Performance Stipend'),
    (1351, 'Has $20k-$35k stipend'),
    (2,    'Remote – Flexible Hours'),
    (1355, 'Has full-time + $90k-$105k stipend'),
]

for job_id, label in tests:
    r = c.get(f'/internship/lead/{job_id}')
    r2 = c.get(r.headers.get('Location', f'/internship/lead/{job_id}/x'))
    body = r2.data.decode('utf-8', errors='replace')
    
    # Extract perk-text values from HTML
    import re
    perk_texts = re.findall(r'class="perk-text">(.*?)<', body)
    perk_subs  = re.findall(r'class="perk-sub">(.*?)<', body)
    
    no_signin_note = 'Sign in required' not in body
    
    print(f"\n[{job_id}] {label}")
    print(f"  Status: {r2.status_code}")
    print(f"  Perk titles: {perk_texts}")
    print(f"  Perk subs:   {perk_subs}")
    print(f"  Sign-in note removed: {no_signin_note}")

print("\n--- ALL CHECKS DONE ---")
