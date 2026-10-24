"""
Quick visual preview of a live Indian lead page - print key sections
"""
import sys
sys.path.append('apps/portal')
from app import app
app.config['TESTING'] = True
c = app.test_client()
import re

for jid, label in [(1423, 'Indian Lead (OMNIDYA, Ahmedabad)'), (1424, 'Indian Lead (Almost Magic, AI)')]:
    r = c.get(f'/internship/lead/{jid}', follow_redirects=True)
    body = r.data.decode('utf-8', errors='replace')
    
    # Extract and show the JD sections
    jd_blocks = re.findall(r'<h3[^>]*>([^<]+)</h3>\s*<p>(.*?)</p>', body, re.DOTALL)
    perks = re.findall(r'perk-text">([^<]+)<', body)
    perk_subs = re.findall(r'perk-sub">([^<]+)<', body)
    sourced_via = 'Sourced via' in body
    co_line = re.search(r'class="co">(.*?)</div>', body, re.DOTALL)
    
    print(f"\n{'='*60}")
    print(f"Lead {jid}: {label}")
    print(f"  Status: {r.status_code}")
    print(f"  'Sourced via' present: {sourced_via}")
    print(f"  Company line: {re.sub(r'<[^>]+>', '', (co_line.group(1) if co_line else 'N/A')).strip()}")
    print(f"  Perk Titles: {perks}")
    print(f"  Perk Subs: {perk_subs}")
    print(f"  JD Sections found: {[b[0] for b in jd_blocks[:6]]}")

print("\nDone.")
