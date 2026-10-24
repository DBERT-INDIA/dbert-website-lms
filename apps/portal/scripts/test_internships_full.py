import sys
sys.path.append('apps/portal')
from app import app
import re

c = app.test_client()

print("\n--- 1. Testing GET /internships (Page 1) ---")
r1 = c.get('/internships')
assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
b1 = r1.data.decode('utf-8', errors='replace')

assert '1423' in b1, "Lead 1423 must be present on /internships Page 1"
assert 'OMNIDYA TECH LLP' in b1, "OMNIDYA TECH LLP must be present on /internships Page 1"
assert 'Data Annotator' in b1, "Data Annotator role must be present on /internships Page 1"
assert '/internship/lead/1423/' in b1, "Card link to lead 1423 must exist on /internships Page 1"
assert 'pagination-wrapper' in b1, "Pagination wrapper must exist on /internships"
assert 'pag-btn' in b1, "Pagination buttons must exist"
print("PASS: /internships Page 1 displays lead 1423 with card and link, and pagination controls!")

# Check total count and page count
match_total = re.search(r'Page <strong>1</strong> of <strong>(\d+)</strong> \((\d+) total', b1)
if match_total:
    print(f"PASS: Found pagination summary: Page 1 of {match_total.group(1)} ({match_total.group(2)} total internships)")

print("\n--- 2. Testing GET /internships?page=2 ---")
r2 = c.get('/internships?page=2')
assert r2.status_code == 200, f"Expected 200, got {r2.status_code}"
b2 = r2.data.decode('utf-8', errors='replace')
assert 'Page <strong>2</strong>' in b2 or 'Page 2' in b2, "Page 2 must indicate current page 2"
print("PASS: Page 2 loads and renders successfully!")

print("\n--- 3. Testing GET /internships?q=OMNIDYA ---")
rq = c.get('/internships?q=OMNIDYA')
assert rq.status_code == 200
bq = rq.data.decode('utf-8', errors='replace')
assert 'OMNIDYA TECH LLP' in bq
assert '1423' in bq
print("PASS: Search for OMNIDYA finds lead 1423!")

print("\n--- 4. Testing GET /internships?domain=AI+Agent+Development ---")
rd = c.get('/internships?domain=AI+Agent+Development')
assert rd.status_code == 200
bd = rd.data.decode('utf-8', errors='replace')
assert '1423' in bd
print("PASS: Filtering by AI Agent Development includes lead 1423 on Page 1!")

print("\n--- 5. Testing GET /internships?region=india ---")
ri = c.get('/internships?region=india')
assert ri.status_code == 200
bi = ri.data.decode('utf-8', errors='replace')
assert '1423' in bi
print("PASS: Filtering by region=india includes lead 1423!")

print("\n--- 6. Testing GET /internship/lead/1423/data-annotator-omnidya-tech-llp ---")
rl = c.get('/internship/lead/1423/data-annotator-omnidya-tech-llp')
assert rl.status_code == 200
bl = rl.data.decode('utf-8', errors='replace')
assert 'OMNIDYA TECH LLP' in bl
assert 'Data Annotator' in bl
assert 'Job Description &amp; Overview' in bl
print("PASS: Lead detail page loads with 200 and full content!")

print("\nALL 6/6 TEST SUITES PASSED PERFECTLY!")
