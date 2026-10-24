import sys
sys.path.append('apps/portal')
from app import get_db, row_to_dict

with get_db() as conn:
    row = conn.execute("SELECT id, Role, Company, Domain, Location, Work_Model, Region, City, Start_Date, End_Date FROM scraped_internships WHERE id=1423").fetchone()
    print("Row 1423:", dict(row))
    
    # check date('now') vs End_Date
    now = conn.execute("SELECT date('now')").fetchone()[0]
    print("date('now'):", now, "End_Date:", row['End_Date'])
    matches = conn.execute("SELECT COUNT(*) FROM scraped_internships WHERE id=1423 AND (End_Date >= date('now') OR End_Date IS NULL)").fetchone()[0]
    print("Matches date filter:", matches)
