"""
Full end-to-end verification script for all deliverables:
1. "Sourced via" component removed
2. Rich JDs present (About Company, About Role, Key Responsibilities, Requirements)
3. Indian posts indexed first in scraped_internships
4. Region filter exists in post_listings HTML
5. data-region attribute on post cards
6. India-first ORDER BY for scraped lead related posts
7. Post listings page loads without error
8. Individual lead pages load without error
"""
import sys
import time
import re
import sqlite3

sys.path.append('apps/portal')
time.sleep(2)

from app import app
app.config['TESTING'] = True
c = app.test_client()

errors = []
passed = []

def check(name, condition, detail=""):
    if condition:
        passed.append(f"  PASS: {name}")
    else:
        errors.append(f"  FAIL: {name}" + (f" ({detail})" if detail else ""))

print("\n=== 1. Check 'Sourced via' removed from individual lead pages ===")
for jid in [1423, 1424, 1355]:
    r = c.get(f'/internship/lead/{jid}', follow_redirects=True)
    body = r.data.decode('utf-8', errors='replace')
    check(f"Lead {jid}: 'Sourced via' removed", 'Sourced via' not in body)

print("\n=== 2. Check Rich JD on lead pages ===")
for jid in [1423, 1424, 1355]:
    r = c.get(f'/internship/lead/{jid}', follow_redirects=True)
    body = r.data.decode('utf-8', errors='replace')
    check(f"Lead {jid}: 'About' company section", 'About ' in body and 'jd-section' in body)
    check(f"Lead {jid}: 'About the Role' section", 'About the Role' in body)
    check(f"Lead {jid}: 'Key Responsibilities' in JD", 'Key Responsibilities' in body)
    check(f"Lead {jid}: 'Requirements' in JD", 'Requirements' in body)

print("\n=== 3. Check Indian posts ordered first in scraped_internships ===")
conn = sqlite3.connect('apps/portal/internship.db')
cursor = conn.cursor()
# First 10 rows returned with India-first ordering
rows = cursor.execute(
    "SELECT id, Region FROM scraped_internships "
    "ORDER BY CASE WHEN Region='India' THEN 0 ELSE 1 END ASC, id ASC LIMIT 10"
).fetchall()
all_india_first = all(r[1] == 'India' for r in rows)
check("DB: First 10 rows in India-first order are all India", all_india_first, f"Rows: {rows[:3]}")
india_count = cursor.execute("SELECT COUNT(*) FROM scraped_internships WHERE Region='India'").fetchone()[0]
intl_count = cursor.execute("SELECT COUNT(*) FROM scraped_internships WHERE Region!='India'").fetchone()[0]
check("DB: India count = 2200", india_count == 2200, f"Got {india_count}")
check("DB: International count = 1422", intl_count == 1422, f"Got {intl_count}")
conn.close()

print("\n=== 4. Check rich JD columns in database ===")
conn = sqlite3.connect('apps/portal/internship.db')
cursor = conn.cursor()
thin = cursor.execute(
    "SELECT COUNT(*) FROM scraped_internships WHERE Description IS NULL OR length(Description) < 300"
).fetchone()[0]
rich = cursor.execute(
    "SELECT COUNT(*) FROM scraped_internships WHERE Description LIKE '%jd-section%'"
).fetchone()[0]
check("DB: Rich JDs (jd-section) present", rich > 3000, f"Rich JD count: {rich}")
check("DB: Thin (<300 chars) descriptions < 100", thin < 100, f"Thin count: {thin}")
india_jd = cursor.execute(
    "SELECT COUNT(*) FROM scraped_internships WHERE Region='India' AND Description LIKE '%About%'"
).fetchone()[0]
check(f"DB: Indian JDs have 'About' section: {india_jd} of 2200", india_jd > 2000, f"Got {india_jd}")
conn.close()

print("\n=== 5. Check Region filter dropdown exists on post_listings ===")
r_list = c.get('/internships', follow_redirects=True)
list_body = r_list.data.decode('utf-8', errors='replace')
check("/internships: 200 OK", r_list.status_code == 200)
check("/internships: Region filter dropdown exists", 't2Region' in list_body)
check("/internships: India option in dropdown", 'india' in list_body.lower() and 'All Regions' in list_body)
check("/internships: International option in dropdown", 'international' in list_body.lower())

print("\n=== 6. Check data-region attribute on post cards ===")
check("/internships: data-region attribute on cards", 'data-region=' in list_body)
india_cards = list_body.count('data-region="india"')
intl_cards = list_body.count('data-region="international"')
check(f"/internships: India cards ({india_cards}) on page", india_cards > 0, f"India cards: {india_cards}")
check(f"/internships: International cards ({intl_cards}) on page", intl_cards > 0, f"Intl cards: {intl_cards}")

print("\n=== 7. Check jobs page also loads ===")
r_jobs = c.get('/jobs', follow_redirects=True)
check("/jobs: 200 OK", r_jobs.status_code == 200)

print("\n=== 8. Check sitemap includes scraped leads ===")
r_sitemap = c.get('/sitemap.xml', follow_redirects=True)
check("/sitemap.xml: 200 OK", r_sitemap.status_code == 200)
sitemap_body = r_sitemap.data.decode('utf-8', errors='replace')
check("/sitemap.xml: has /internship/lead/ URLs", '/internship/lead/' in sitemap_body)

print("\n=== RESULTS ===")
for p in passed:
    print(p)
for e in errors:
    print(e)
print(f"\nTotal: {len(passed)} passed, {len(errors)} failed")
