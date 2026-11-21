import os, sys
from dotenv import load_dotenv

sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
load_dotenv('/var/www/dbert-website-lms/apps/portal/.env')

from app import app, get_db, create_session, attendance_ping

# Create temporary session for testing
test_email = 'bhargavi13032007@gmail.com'
token = create_session(test_email, 'intern')
print(f"Created session token for {test_email}")

with app.test_client() as client:
    # 1. Test GET /intern/attendance
    res = client.get('/intern/attendance', headers={'X-Session-Token': token})
    print("GET /intern/attendance HTTP status:", res.status_code)
    data = res.get_json()
    print("GET /intern/attendance status:", data.get('status'))
    print("Number of weeks returned:", len(data.get('weeks', [])))
    if data.get('weeks'):
        cur = data['weeks'][0]
        print(f"Week: {cur['week_start']} to {cur['week_end']} | Mins: {cur['total_minutes']} | Hours: {cur['hours']}h {cur['minutes']}m | Compliant (10h+): {cur['met_threshold']}")

# 2. Test attendance_ping() directly within request context
with app.test_request_context('/attendance/ping', method='POST', headers={'X-Session-Token': token}):
    response = attendance_ping()
    ping_data = response.get_json()
    print("attendance_ping() direct response:", ping_data)
    assert ping_data.get('status') == 'success', f"Expected status 'success', got {ping_data.get('status')}"
    assert ping_data.get('ok') is True, "Expected ok: True"
    print("✓ Assertion passed: status is strictly 'success' and ok: True!")

# Clean up test session token
with get_db() as conn:
    conn.execute("DELETE FROM user_sessions WHERE session_token=?", (token,))
    conn.commit()
print("Cleaned up test session token. Test completed successfully.")
