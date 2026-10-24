import sys
sys.path.append('apps/portal')
from app import get_db, row_to_dict

with get_db() as conn:
    rows = [row_to_dict(r) for r in conn.execute("SELECT p.*, c.name AS company_name, 0 as applications_count FROM posts p JOIN companies c ON c.id=p.company_id WHERE p.post_type='internship'").fetchall()]
    for d in rows:
        d['source'] = 'post'
        d['region'] = d.get('region', '')
        
    lead_rows = conn.execute("SELECT id, Role, Company, Domain, Location, Work_Model, Region, City, Start_Date, End_Date FROM scraped_internships WHERE (End_Date >= date('now') OR End_Date IS NULL) ORDER BY CASE WHEN Region='India' THEN 0 ELSE 1 END ASC, id ASC").fetchall()
    leads = []
    for lr in lead_rows:
        d = row_to_dict(lr)
        d['title'] = d['Role']
        d['company_name'] = d['Company']
        d['published_at'] = d.get('Start_Date') or ''
        d['region'] = (d.get('Region') or 'International').lower()
        leads.append(d)
        
    all_items = rows + leads
    print('Before sort, index of 1423:', next(i for i, x in enumerate(all_items) if x.get('id') == 1423))
    
    def _sort_key(p):
        reg = (p.get('region') or '').lower()
        if not reg:
            t = (p.get('title') or '').lower()
            india_cities = ['bangalore', 'delhi', 'mumbai', 'pune', 'hyderabad',
                            'kolkata', 'chennai', 'jaipur', 'noida', 'gurgaon',
                            'ahmedabad', 'chandigarh', 'ncr', 'india']
            reg = 'india' if any(c in t for c in india_cities) else 'international'
        return (0 if reg == 'india' else 1, -(hash(p.get('published_at') or '')))

    all_items.sort(key=_sort_key)
    idx = next(i for i, x in enumerate(all_items) if x.get('id') == 1423)
    print('After sort, index of 1423:', idx)
    print('Page for 1423 (page size 24):', (idx // 24) + 1)
