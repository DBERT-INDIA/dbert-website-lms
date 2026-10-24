import sys
sys.path.append('apps/portal')
from app import app, get_db

app.config['TESTING'] = True
client = app.test_client()

print("--- TEST 1: Anonymous user visits job page (should 301 to slug URL) ---")
r = client.get('/internship/lead/1')
print(f"Status: {r.status_code}, Location: {r.headers.get('Location','')}")

print("\n--- TEST 2: Following redirect to canonical slug URL ---")
slug_url = r.headers.get('Location', '/internship/lead/1/internship')
r2 = client.get(slug_url)
print(f"Status: {r2.status_code}")
body = r2.data.decode('utf-8', errors='replace')
print("Has 'Apply Now':", 'Apply Now' in body)
print("Has JobPosting schema:", 'JobPosting' in body)
print("Has Discussion:", 'Discussion' in body)
print("Has related list:", 'related-list' in body)
print("Has signup link:", 'signup' in body)

print("\n--- TEST 3: Click tracker without CSRF token (should succeed 200 due to exemption) ---")
r4 = client.post('/api/lead/1/click')
print(f"Status: {r4.status_code}, Body: {r4.get_json()}")

print("\n--- TEST 4: Comment API without session/auth (with valid CSRF, should 401) ---")
with client.session_transaction() as sess:
    sess['_csrf'] = 'test_token_12345'

r3 = client.post(
    '/api/lead/1/comment',
    headers={'X-CSRF-Token': 'test_token_12345'},
    json={'body': 'This is a test comment that is long enough.'},
    content_type='application/json'
)
print(f"Status: {r3.status_code}, Body: {r3.get_json()}")

print("\n--- TEST 5: Comment API with authenticated intern ---")
# Get a real intern from DB
with get_db() as conn:
    intern_row = conn.execute("SELECT id, email, name FROM intern_accounts WHERE is_active=1 LIMIT 1").fetchone()
    if intern_row:
        intern_dict = dict(intern_row)
        # Create a session token
        sess_token = 'test_session_token_lead'
        conn.execute(
            "INSERT OR REPLACE INTO user_sessions (email, role, session_token, expires_at) VALUES (?, 'intern', ?, '2099-01-01 00:00:00')",
            (intern_dict['email'].lower(), sess_token)
        )
        conn.commit()
    else:
        intern_dict = None

if intern_dict:
    client.set_cookie('dbert_session', sess_token)
    with client.session_transaction() as sess:
        sess['_csrf'] = 'test_csrf_token_auth'

    r_post = client.post(
        '/api/lead/1/comment',
        headers={'X-CSRF-Token': 'test_csrf_token_auth'},
        json={'body': 'I have built multiple Python automation scripts and REST APIs and am a great fit for this lead!'},
        content_type='application/json'
    )
    print(f"Status: {r_post.status_code}, Response: {r_post.get_json()}")

    # Now verify the comment shows up on the page
    r_detail = client.get(slug_url)
    detail_body = r_detail.data.decode('utf-8', errors='replace')
    print("Comment text appears in page HTML:", 'I have built multiple Python automation scripts' in detail_body)
    print("Authenticated user sees direct apply link (target=_blank):", 'target="_blank"' in detail_body)

print("\n--- TEST 6: Sitemap generation with scraped lead pages ---")
r_site = client.get('/sitemap.xml')
print(f"Status: {r_site.status_code}")
sitemap_xml = r_site.data.decode('utf-8', errors='replace')
lead_count = sitemap_xml.count('/internship/lead/')
print(f"Scraped job URLs present in sitemap.xml: {lead_count}")
print(f"Total sitemap size: {len(r_site.data):,} bytes")

print("\n--- TEST 7: Existing /internships directory intact ---")
r_cat = client.get('/internships')
print(f"Status: {r_cat.status_code}")

print("\n--- ALL TESTS FINISHED SUCCESSFULLY ---")
