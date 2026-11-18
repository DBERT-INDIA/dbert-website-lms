
import os, sys
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import app, get_or_create_offer_letter, get_intern_active_gemini_context, create_session, get_db

with get_db() as conn:
    gem = get_intern_active_gemini_context(5042, conn=conn)
    print("get_intern_active_gemini_context(5042):", {
        "has_key": gem.get("has_key"),
        "key_preview": gem.get("api_key")[:10] if gem.get("api_key") else None,
        "default_model": gem.get("default_model"),
        "error": gem.get("error")
    })

token = create_session("nikunjshah0310@gmail.com", "intern")
with app.test_client() as client:
    res = client.get("/tasks/101/guide", headers={"X-Session-Token": token})
    print("GET /tasks/101/guide status:", res.status_code)
    assert res.status_code == 200
    content = res.get_data(as_text=True)
    assert "Assigned Angle & Case Study Context" in content
    assert "1-Click AI Post Synthesis" in content
    print("LIVE VERIFICATION SUCCESS: Course-style bounty guide renders with active Gemini BYOK key!")
