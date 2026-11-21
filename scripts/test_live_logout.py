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

print("--- 1. Testing GET https://lms.dbert.in/logout ---")
req1 = urllib.request.Request(
    'https://lms.dbert.in/logout',
    headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
)
try:
    res1 = opener.open(req1)
    print('GET Code:', res1.code, res1.headers.get('Location'))
except urllib.error.HTTPError as e:
    print('GET Code:', e.code, e.headers.get('Location'))

print("\n--- 2. Fetching home page to establish session & get CSRF ---")
res_home = opener.open('https://lms.dbert.in/')
home_html = res_home.read().decode('utf-8')
m = re.search(r'name=[\"\']_csrf[\"\']\s+value=[\"\']([^\"\']+)[\"\']', home_html)
csrf_val = m.group(1) if m else None
print('CSRF token found:', bool(csrf_val))

if csrf_val:
    print("\n--- 3. Testing POST form to https://lms.dbert.in/logout ---")
    data = urllib.parse.urlencode({'_csrf': csrf_val}).encode('utf-8')
    req2 = urllib.request.Request(
        'https://lms.dbert.in/logout',
        data=data,
        headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    try:
        res2 = opener.open(req2)
        print('POST Form Code:', res2.code, res2.headers.get('Location'))
    except urllib.error.HTTPError as e:
        print('POST Form Code:', e.code, e.headers.get('Location'))

print("\n--- 4. Testing browser follow-redirect on GET https://lms.dbert.in/logout ---")
opener_follow = urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ctx),
    urllib.request.HTTPCookieProcessor(cj)
)
req3 = urllib.request.Request('https://lms.dbert.in/logout', headers={'User-Agent': 'Mozilla/5.0'})
res3 = opener_follow.open(req3)
print('Final URL reached:', res3.geturl())
print('HTTP Status Code:', res3.code)
