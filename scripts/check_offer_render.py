import os
import sys
from dotenv import load_dotenv

portal_dir = "/var/www/dbert-website-lms/apps/portal"
if os.path.exists(portal_dir):
    os.chdir(portal_dir)
    sys.path.insert(0, portal_dir)
    load_dotenv(os.path.join(portal_dir, ".env"))

from app import app
from services.database.adapter import get_db_adapter
from flask import render_template

with app.test_request_context("/portal/offer"):
    with get_db_adapter() as conn:
        offer = conn.execute("SELECT * FROM intern_offer_letters WHERE offer_letter_id = 'DBERT-OFR-2026-DA-9103'").fetchone()
        offer_dict = dict(offer)
        html = render_template(
            "portal_offer_letter.html",
            locked=False,
            preview_mode=True,
            is_signed=False,
            is_deposit_verified=False,
            offer=offer_dict,
            enrollment=None,
            user={"email": "stage3_selected@dbert.test", "role": "intern", "name": "Chirag Gupta"},
            active_page="offer"
        )
        print("HTML rendered successfully! Length:", len(html))
        
        # Check what is inside screenActionSteps:
        idx = html.find('id="screenActionSteps"')
        end_idx = html.find('id="screenOfferReview"') # or look around screenActionSteps
        print("screenActionSteps snippet:")
        print(html[idx:idx+2500])
