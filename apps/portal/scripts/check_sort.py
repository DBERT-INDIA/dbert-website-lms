import sys
sys.path.append('apps/portal')
from app import get_db, row_to_dict, _post_path, _lead_seo_slug
import re

with get_db() as conn:
    # emulate _render_listings
    rows = conn.execute("SELECT p.*, c.name AS company_name, 0 as applications_count FROM posts p JOIN companies c ON c.id=p.company_id WHERE p.post_type='internship'").fetchall()
    
    lead_where = "(End_Date >= date('now') OR End_Date IS NULL)"
    lead_rows = conn.execute(
        f"SELECT id, Role, Company, Domain, Location, Work_Model, Region, City, "
        f"Stipend, Stipend_Normalized, Start_Date, End_Date, Clicks "
        f"FROM scraped_internships WHERE {lead_where} "
        f"ORDER BY CASE WHEN Region='India' THEN 0 ELSE 1 END ASC, id ASC"
    ).fetchall()
    
    scraped_leads = []
    for lr in lead_rows:
        d = row_to_dict(lr)
        scraped_leads.append(d)
        
    print(f"Total canonical posts: {len(rows)}")
    print(f"Total scraped leads: {len(scraped_leads)}")
    
    # Check if 1423 is in scraped_leads
    idx_1423 = next((i for i, d in enumerate(scraped_leads) if d['id'] == 1423), None)
    print(f"Index of 1423 in scraped_leads: {idx_1423}")
    
    # Check what items come before 1423
    print("First 5 scraped_leads:", [(d['id'], d['Role'], d['Company'], d['Region']) for d in scraped_leads[:5]])
