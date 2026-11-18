
import os, sys
from dotenv import load_dotenv
load_dotenv("/var/www/dbert-website-lms/apps/portal/.env")
sys.path.insert(0, "/var/www/dbert-website-lms/apps/portal")

from app import app, create_session

token = create_session("bhargavi13032007@gmail.com", "intern")

with app.test_client() as client:
    # Set Flask session cookie with _csrf
    with client.session_transaction() as sess:
        sess["_csrf"] = "dbert_test_csrf_secret_token"
        sess["user_id"] = 5222
        sess["role"] = "intern"
        sess["email"] = "bhargavi13032007@gmail.com"

    res = client.post(
        "/api/tasks/101/generate-content",
        json={"task_id": 101},
        headers={
            "X-Session-Token": token,
            "X-CSRF-Token": "dbert_test_csrf_secret_token"
        }
    )
    print("POST status:", res.status_code)
    data = res.get_json()
    if data and data.get("status") == "success":
        print("AI GENERATION SUCCESS!")
        print("  Model:", data.get("model"))
        print("  Snippet:", data.get("copy")[:200].replace('\n', ' '))
    else:
        print("Response data:", data)
