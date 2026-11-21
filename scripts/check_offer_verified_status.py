import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session, get_db

with app.test_client() as client:
    token = create_session("ratnadeepratu737@gmail.com", "intern")
    res = client.get("/portal/offer", headers={"X-Session-Token": token})
    content = res.get_data(as_text=True)
    with get_db() as conn:
        row = conn.execute("SELECT caution_deposit_status, pdf_unlocked FROM intern_offer_letters WHERE email = 'ratnadeepratu737@gmail.com'").fetchone()
        print(f"Offer Letter DB: caution_deposit_status={row[0]}, pdf_unlocked={row[1]}")
    if "Caution Deposit Paid" in content or "DEPOSIT VERIFIED" in content or "Verified" in content:
        print("Verified text present in offer page!")
