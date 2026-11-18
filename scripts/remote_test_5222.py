
import os, sys
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import app, get_intern_active_gemini_context, create_session, get_db

with get_db() as conn:
    cur = conn.cursor()
    cur.execute("SELECT id, email, name FROM intern_accounts WHERE id = 5222")
    row = cur.fetchone()
    print("Intern 5222:", row)
    
    gem = get_intern_active_gemini_context(5222, conn=conn)
    print("get_intern_active_gemini_context(5222):", {
        "has_key": gem.get("has_key"),
        "key_preview": gem.get("api_key")[:10] if gem.get("api_key") else None,
        "default_model": gem.get("default_model"),
        "error": gem.get("error")
    })

if row and gem.get("has_key"):
    email = row[1]
    token = create_session(email, "intern")
    with app.test_client() as client:
        res = client.get("/tasks/101/guide", headers={"X-Session-Token": token})
        print("GET /tasks/101/guide with active key HTTP status:", res.status_code)
        assert res.status_code == 200
        content = res.get_data(as_text=True)
        assert "Assigned Angle & Case Study Context" in content
        assert "1-Click AI Post Synthesis" in content
        assert "Publish to Platform" in content
        print("SUCCESS: Full 4-step course-style bounty guide renders with active Gemini key!")
