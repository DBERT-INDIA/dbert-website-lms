import sys
sys.path.append('apps/portal')
from app import get_db, row_to_dict

with get_db() as conn:
    rows = [row_to_dict(r) for r in conn.execute("SELECT p.*, c.name AS company_name, 0 as applications_count FROM posts p JOIN companies c ON c.id=p.company_id WHERE p.post_type='internship'").fetchall()]
    for d in rows:
        d['source'] = 'post'
        t = (d.get('title') or '').lower()
        india_cities = ['bangalore', 'delhi', 'mumbai', 'pune', 'hyderabad',
                        'kolkata', 'chennai', 'jaipur', 'noida', 'gurgaon',
                        'ahmedabad', 'chandigarh', 'ncr', 'india']
        d['region'] = 'india' if any(c in t for c in india_cities) else 'international'
        
    lead_rows = conn.execute("SELECT id, Role, Company, Domain, Location, Work_Model, Region, City, Start_Date, End_Date FROM scraped_internships WHERE (End_Date >= date('now') OR End_Date IS NULL) ORDER BY id ASC").fetchall()
    leads = []
    for lr in lead_rows:
        d = row_to_dict(lr)
        d['title'] = d['Role']
        d['company_name'] = d['Company']
        d['published_at'] = d.get('Start_Date') or ''
        d['region'] = (d.get('Region') or 'International').lower()
        d['source'] = 'lead'
        leads.append(d)
        
    all_items = rows + leads
    
    # Stable sort: first by (published_at, id) DESC
    all_items.sort(key=lambda p: (str(p.get("published_at") or "2000-01-01"), int(p.get("id") or 0)), reverse=True)
    # Then stably by India (0) vs International (1)
    all_items.sort(key=lambda p: 0 if (p.get("region") or "").lower() == "india" else 1)
    
    print("Total items:", len(all_items))
    print("Index of 1423:", next(i for i, x in enumerate(all_items) if x.get('id') == 1423 and x.get('source') == 'lead'))
    print("First 10 items:")
    for i, it in enumerate(all_items[:10]):
        print(f" {i+1}: ID={it['id']} [{it['source']}] {it['title']} at {it['company_name']} ({it['region']}) pub={it['published_at']}")
