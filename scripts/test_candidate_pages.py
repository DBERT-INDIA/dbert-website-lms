import sys
sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
from app import app, create_session

app.config["TESTING"] = True
client = app.test_client()

for email in ["abhinav.sharma@dbert.vom", "abhinav.sharma@dbert.in"]:
    print(f"\n=======================================================")
    print(f"TESTING EMAIL: {email}")
    print(f"=======================================================")
    token = create_session(email, "intern")
    
    # 1. Request /portal
    res_portal = client.get("/portal", headers={"X-Session-Token": token})
    print(f"/portal Status: {res_portal.status_code}")
    portal_html = res_portal.get_data(as_text=True)
    
    keywords_portal = [
        "Complete Your Academic Profile",
        "Pending Profile",
        "Stage 1",
        "Under Evaluation",
        "Fast-Track Incubation Allocation",
        "Stage 2",
        "Stage 3",
        "Stage 4",
        "Stage 5",
        "Grace Period",
        "balance_grace_expired",
        "7-Day Balance",
        "Confirmed & Enrolled"
    ]
    print("Keywords in /portal:")
    for kw in keywords_portal:
        if kw in portal_html:
            print(f"   [FOUND] '{kw}'")
            
    # 2. Request /portal/offer
    res_offer = client.get("/portal/offer", headers={"X-Session-Token": token})
    print(f"\n/portal/offer Status: {res_offer.status_code}")
    offer_html = res_offer.get_data(as_text=True)
    
    keywords_offer = [
        "DBERT-OFR-2026-FSD-5166",
        "ACCEPTED & SIGNED",
        "Appointment Terms Preview",
        "PREVIEW ONLY",
        "Official Signed PDF",
        "STEP 3: COHORT SEAT CONFIRMATION",
        "Confirm Your Cohort Seat with ₹499 Refundable Caution Deposit",
        "Scan & Pay ₹499",
        "12-Digit Bank UTR"
    ]
    print("Keywords in /portal/offer:")
    for kw in keywords_offer:
        if kw in offer_html:
            print(f"   [FOUND] '{kw}'")
