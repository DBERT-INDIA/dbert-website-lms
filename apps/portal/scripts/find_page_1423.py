import sys
sys.path.append('apps/portal')
from app import app
c = app.test_client()

r = c.get('/internships')
print("Status:", r.status_code)
# Search all pages or check where 1423 is
r_lead = c.get('/internships?page=1')
body = r_lead.data.decode('utf-8', errors='replace')
import re
cards = re.findall(r'href="([^"]+)"[^>]*>.*?<h2>([^<]+)</h2>.*?class="co"><i class="fas fa-building"></i>\s*([^<]+)</div>', body, re.DOTALL)
print(f"Total cards on page 1: {len(cards)}")
for i, card in enumerate(cards[:10]):
    print(f" {i+1}: {card[1].strip()} at {card[2].strip()} -> {card[0]}")

# Now let's see which page has 1423
for p in range(1, 10):
    r_p = c.get(f'/internships?page={p}')
    b_p = r_p.data.decode('utf-8', errors='replace')
    if '1423' in b_p:
        print(f"*** Lead 1423 found on page {p}! ***")
        break
else:
    print("Not found in first 10 pages")
