import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session, get_db

with app.test_client() as client:
    token = create_session("ratnadeepratu737@gmail.com", "intern")
    res = client.get("/portal/offer", headers={"X-Session-Token": token})
    print(f"Status Code: {res.status_code}")
    content = res.get_data(as_text=True)
    print(f"Content Length: {len(content)}")
    if "DBERT-OFR-2026-DA-5278" in content:
        print("SUCCESS: Found Offer Letter ID DBERT-OFR-2026-DA-5278 in rendered page!")
    elif "Offer Letter" in content:
        print("SUCCESS: Rendered Offer Letter page!")
    else:
        print("Notice: check content snippet:")
        print(content[:500])
