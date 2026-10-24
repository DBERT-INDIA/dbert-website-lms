import sys, re
sys.path.append('apps/portal')
from app import app
app.config['TESTING'] = True
c = app.test_client()

r = c.get('/internship/lead/1423', follow_redirects=True)
body = r.data.decode('utf-8', errors='replace')
sections = body.count('jd-section')
h3s = re.findall(r'<h3[^>]*>([A-Za-z0-9 &;]+)</h3>', body)
sourced = 'Sourced via' in body
sign_note = 'Sign in required' in body
print('Lead 1423 - OMNIDYA TECH LLP (Ahmedabad, India):')
print('  Status:', r.status_code)
print('  Sourced via removed:', not sourced)
print('  Sign-in note removed:', not sign_note)
print('  JD sections found:', sections)
print('  H3 headings in JD:', h3s)

r2 = c.get('/internship/lead/1355', follow_redirects=True)
body2 = r2.data.decode('utf-8', errors='replace')
sections2 = body2.count('jd-section')
h3s2 = re.findall(r'<h3[^>]*>([A-Za-z0-9 &;]+)</h3>', body2)
sourced2 = 'Sourced via' in body2
print()
print('Lead 1355 - KoboToolbox (International):')
print('  Status:', r2.status_code)
print('  Sourced via removed:', not sourced2)
print('  JD sections found:', sections2)
print('  H3 headings in JD:', h3s2)
