import sys
from pathlib import Path

if Path("/var/www/dbert-website-lms").exists():
    sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")
else:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "apps" / "portal"))

from app import app, get_db

from app import app, get_db, create_session

token = create_session("aryanbhakuni2006@gmail.com", "intern")

with app.test_client() as client:
    resp = client.get("/stipend/tasks", headers={"X-Session-Token": token})
    print(f"\nResponse status code for Aryan: {resp.status_code}")
    html = resp.get_data(as_text=True)
    if "All 4 Gates Verified &amp; Approved" in html:
        print("PASS: 'All 4 Gates Verified & Approved' found in rendered HTML!")
    if "Stipend Disbursement Scheduled" in html:
        print("PASS: 'Stipend Disbursement Scheduled' found in rendered HTML!")
    if "₹5499 /-" in html or "₹5,499 /-" in html:
        print("PASS: '₹5,499 /-' amount found in rendered HTML!")
    if "Alkameinc" in html:
        print("PASS: 'Alkameinc' organization found in rendered HTML!")
    if "checklist-grid" not in html:
        print("PASS: 'checklist-grid' successfully replaced/suppressed!")

