import urllib.request, re

def check(jid):
    req = urllib.request.Request(
        'http://127.0.0.1:5000/internship/lead/' + str(jid),
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    body = urllib.request.urlopen(req).read().decode('utf-8', errors='replace')
    perks      = re.findall(r'perk-text">([^<]+)<', body)
    subs       = re.findall(r'perk-sub">([^<]+)<', body)
    sign_note  = 'Sign in required' in body
    apply_btn  = 'Apply Now' in body
    no_div_wrap = '<div style="display:flex; flex-direction:column' not in body  # removed wrapping div
    print('Lead ' + str(jid))
    print('  Perk titles:            ' + str(perks))
    print('  Perk subs:              ' + str(subs))
    print('  Apply Now visible:      ' + str(apply_btn))
    print('  Sign-in note removed:   ' + str(not sign_note))
    print()

for jid in [1, 1351, 1355]:
    check(jid)

print('Done.')
