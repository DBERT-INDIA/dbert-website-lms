import urllib.request
import urllib.parse
import http.cookiejar
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(cj),
    NoRedirectHandler
)

print("--- 1. Authenticating via magic token ---")
magic_url = "https://lms.dbert.in/auth/activate?e=stage1_apply@dbert.test&t=9ed5c198f6468bd6fc5237deab404804&next=/courses"
try:
    r_auth = opener.open(magic_url)
    print("Auth redirect:", r_auth.code, r_auth.headers.get("Location"))
except urllib.error.HTTPError as e:
    print("Auth redirect code:", e.code, e.headers.get("Location"))

print("\n--- 2. Fetching /courses to retrieve CSRF token from sidebar ---")
opener_follow = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(cj)
)
courses_html = opener_follow.open("https://lms.dbert.in/courses").read().decode("utf-8")
m = re.search(r'name=[\"\'](_csrf|_csrf_token)[\"\']\s+value=[\"\']([^\"\']+)[\"\']', courses_html)
csrf_val = m.group(2) if m else None
csrf_name = m.group(1) if m else None
print(f"CSRF token found: {csrf_name} = {csrf_val[:10]}...")

if csrf_val:
    print("\n--- 3. Submitting Form POST to /logout ---")
    data = urllib.parse.urlencode({csrf_name: csrf_val}).encode('utf-8')
    req_logout = urllib.request.Request(
        'https://lms.dbert.in/logout',
        data=data,
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    try:
        res_logout = opener.open(req_logout)
        print('Logout response code:', res_logout.code, 'Location:', res_logout.headers.get('Location'))
    except urllib.error.HTTPError as e:
        print('Logout redirect code:', e.code, 'Location:', e.headers.get('Location'))

    print("\n--- 4. Following full browser redirect on Form POST to /logout ---")
    res_full = opener_follow.open(req_logout)
    print('Final landed URL:', res_full.geturl())
    print('Final status:', res_full.code)
    body = res_full.read().decode('utf-8')
    is_home = 'DBERT' in body and '{"message":"Logged out."' not in body
    print('Cleanly reached LMS homepage (no raw JSON):', is_home)
