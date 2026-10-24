import sys
sys.path.append('apps/portal')
from app import app
c = app.test_client()

r1 = c.get('/internships')
print("Page 1 Status:", r1.status_code)
b1 = r1.data.decode('utf-8', errors='replace')
print("1423 in Page 1?", "1423" in b1)
print("OMNIDYA in Page 1?", "OMNIDYA" in b1)
print("Data Annotator in Page 1?", "Data Annotator" in b1)

# Check search for OMNIDYA
r_q = c.get('/internships?q=OMNIDYA')
print("\nSearch Q=OMNIDYA Status:", r_q.status_code)
bq = r_q.data.decode('utf-8', errors='replace')
print("1423 in Search results?", "1423" in bq)
print("OMNIDYA in Search results?", "OMNIDYA" in bq)

# Check AI Agent Development domain
r_dom = c.get('/internships?domain=AI+Agent+Development')
print("\nDomain=AI Agent Development Status:", r_dom.status_code)
bd = r_dom.data.decode('utf-8', errors='replace')
print("1423 in Domain results?", "1423" in bd)
