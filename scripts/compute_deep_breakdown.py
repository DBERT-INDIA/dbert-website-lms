import json
import glob
from collections import Counter, defaultdict
from datetime import datetime

with open("data/live_ec2_cache.json", "r", encoding="utf-8") as f:
    ec2 = json.load(f)

apps = [dict(zip(ec2['applications']['columns'], r)) for r in ec2['applications']['rows']]
sessions = [dict(zip(ec2['user_sessions']['columns'], r)) for r in ec2['user_sessions']['rows']]
devices = [dict(zip(ec2['device_profiles']['columns'], r)) for r in ec2['device_profiles']['rows']]
offers = [dict(zip(ec2['intern_offer_letters']['columns'], r)) for r in ec2['intern_offer_letters']['rows']]
deposits = [dict(zip(ec2['security_deposits']['columns'], r)) for r in ec2['security_deposits']['rows']]
accounts = [dict(zip(ec2['intern_accounts']['columns'], r)) for r in ec2['intern_accounts']['rows']]

with open("apps/website/src/data/certificates_registry.json", "r", encoding="utf-8") as f:
    registry = json.load(f)

# Collect all sent emails
sent_emails = set()
email_to_campaign = {}
for fpath in glob.glob('data/*dispatch*.json') + glob.glob('data/*tracking*.json'):
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            d = json.load(f)
            cname = fpath.split('\\')[-1].replace('dispatch_tracking_', '').replace('.json', '')
            for r in d:
                em = (r.get('email') or '').strip().lower()
                st = (r.get('status') or '').upper()
                if em and (st in ('SENT', 'SUCCESS', 'DELIVERED') or 'status' not in r or st == ''):
                    sent_emails.add(em)
                    if em not in email_to_campaign:
                        email_to_campaign[em] = cname
    except:
        pass

# Maps
app_map = {a['email'].strip().lower(): a for a in apps if a.get('email')}
acc_map = {a['email'].strip().lower(): a for a in accounts if a.get('email')}
offer_map = {o['email'].strip().lower(): o for o in offers if o.get('email')}
dep_interns = set(d['intern_id'] for d in deposits)

# User session stats per email
user_session_counts = Counter()
user_last_session = {}
for s in sessions:
    em = (s.get('email') or '').strip().lower()
    if em:
        user_session_counts[em] += 1
        created = str(s.get('created_at') or '')
        if em not in user_last_session or created > user_last_session[em]:
            user_last_session[em] = created

recent_session_emails = set(user_session_counts.keys())

# Device map per user_id or email
# device_profiles has user_id
device_by_user = defaultdict(list)
for dev in devices:
    uid = dev.get('user_id')
    if uid:
        device_by_user[uid].append(dev)

# -------------------------------------------------------------------------
# PART 1: 320 CANDIDATES FOR ₹499 (ACTIVE LOGINS PAST 7D, UNPAID)
# -------------------------------------------------------------------------
unpaid_selected = []
for a in apps:
    em = (a['email'] or '').strip().lower()
    if a['status'] in ('Selected', 'Accepted', 'Enrollment Pending') and em in recent_session_emails:
        off = offer_map.get(em)
        acc = acc_map.get(em)
        has_dep = bool(acc and acc['id'] in dep_interns)
        is_paid = (off and off.get('caution_deposit_status') == 'VERIFIED') or has_dep
        if not is_paid:
            unpaid_selected.append(a)

print("="*75)
print(f"PART 1: ₹499 ACTIVE CANDIDATES (Total: {len(unpaid_selected)})")
print("="*75)

# Breakdown: Email Drive vs Organic / Web Direct
email_drive_499 = []
organic_499 = []

for a in unpaid_selected:
    em = a['email'].strip().lower()
    src = (a.get('source') or '').lower()
    if em in sent_emails:
        email_drive_499.append(a)
    else:
        organic_499.append(a)

print(f"1. Sourced from Sent Email Drives: {len(email_drive_499)} ({len(email_drive_499)/len(unpaid_selected)*100:.1f}%)")
# Top email campaigns among these
email_camps = Counter(email_to_campaign.get(a['email'].strip().lower(), 'Other') for a in email_drive_499)
for c, cnt in email_camps.most_common(5):
    print(f"     - Campaign {c}: {cnt}")

print(f"2. Sourced from Organic Search / Direct Web Signup: {len(organic_499)} ({len(organic_499)/len(unpaid_selected)*100:.1f}%)")
organic_srcs = Counter(a.get('source') or 'direct_signup' for a in organic_499)
for s, cnt in organic_srcs.most_common(5):
    print(f"     - Form Source {s}: {cnt}")

# Rate the Top 25 High-Intent Leads for ₹499
# Scoring:
# - Logins in past 7d (10 pts per login, max 40)
# - Has offer letter generated (+25 pts)
# - Offer letter caution deposit status == 'PENDING' (attempted or viewed) (+15 pts)
# - Has phone number (+10 pts)
# - Recency bonus: logged in within last 24h (+10 pts)
scored_499 = []
for a in unpaid_selected:
    em = a['email'].strip().lower()
    sc = 0
    l_count = user_session_counts[em]
    sc += min(l_count * 10, 40)
    
    off = offer_map.get(em)
    if off:
        sc += 25
        if off.get('caution_deposit_status') == 'PENDING':
            sc += 15
    if a.get('phone') and len(str(a['phone'])) >= 10:
        sc += 10
    
    last_log = user_last_session.get(em, '')
    if last_log.startswith('2026-11-19') or last_log.startswith('2026-11-18'):
        sc += 10
        
    scored_499.append({
        'name': a['name'],
        'email': em,
        'phone': a.get('phone') or 'N/A',
        'domain': a.get('domain') or 'N/A',
        'college': a.get('college') or 'N/A',
        'app_status': a['status'],
        'has_offer': bool(off),
        'caution_status': off.get('caution_deposit_status') if off else 'None',
        'logins_7d': l_count,
        'last_login': last_log,
        'channel': 'Email Drive (' + email_to_campaign.get(em, 'Generic') + ')' if em in sent_emails else 'Organic / Web (' + (a.get('source') or 'Direct') + ')',
        'score': sc
    })

scored_499.sort(key=lambda x: (x['score'], x['logins_7d']), reverse=True)

print(f"\nTop 10 of Top 25 High-Intent ₹499 Leads:")
for i, l in enumerate(scored_499[:10], 1):
    print(f"  {i}. [Score: {l['score']}/100] {l['name']} | {l['email']} | {l['phone']} | {l['domain']} | Logins: {l['logins_7d']} | Channel: {l['channel']}")


# -------------------------------------------------------------------------
# PART 2: 378 PROVISIONAL INTERNS FOR ₹299
# -------------------------------------------------------------------------
prov_certs = {k: v for k, v in registry.items() if v.get('isProvisional') is True}
print("\n" + "="*75)
print(f"PART 2: ₹299 PROVISIONAL INTERNS (Total: {len(prov_certs)})")
print("="*75)

prov_with_sessions = []
prov_without_sessions = []

for cid, c in prov_certs.items():
    em = (c.get('email') or '').strip().lower()
    l_cnt = user_session_counts.get(em, 0)
    last_log = user_last_session.get(em, None)
    has_acc = em in acc_map
    
    c_info = {
        'certId': cid,
        'name': c.get('holderName') or 'N/A',
        'email': em,
        'phone': c.get('phone') or (acc_map[em].get('phone') if has_acc else 'N/A'),
        'domain': c.get('domain') or 'N/A',
        'college': c.get('college') or 'N/A',
        'score': c.get('score', 0),
        'has_portal_account': has_acc,
        'logins_7d': l_cnt,
        'last_login': last_log,
    }
    
    if l_cnt > 0 or (last_log is not None):
        prov_with_sessions.append(c_info)
    else:
        prov_without_sessions.append(c_info)

print(f"1. Provisional Interns who LOGGED IN RECENTLY (past 7 days): {len(prov_with_sessions)} ({len(prov_with_sessions)/len(prov_certs)*100:.1f}%)")
print(f"2. Provisional Interns with NO recent portal session: {len(prov_without_sessions)} ({len(prov_without_sessions)/len(prov_certs)*100:.1f}%)")

# Rate the Top 25 High-Intent Leads for ₹299
# Scoring:
# - Logins past 7d (10 pts per login, max 40)
# - Evaluation Score on cert (80-89: +15, 90-100: +25)
# - Has portal account (+15)
# - Recency bonus (last login 18/19 Nov): +20
scored_299 = []
for c in prov_with_sessions:
    sc = 0
    l_cnt = c['logins_7d']
    sc += min(l_cnt * 10, 40)
    if c['score'] >= 90:
        sc += 25
    elif c['score'] >= 80:
        sc += 15
    if c['has_portal_account']:
        sc += 15
    if c['last_login'] and (c['last_login'].startswith('2026-11-19') or c['last_login'].startswith('2026-11-18')):
        sc += 20
    
    c_entry = dict(c)
    c_entry['intent_score'] = sc
    scored_299.append(c_entry)

# If less than 25 with sessions, fill from highest score in prov_without_sessions with portal accounts
if len(scored_299) < 25:
    sorted_without = sorted(prov_without_sessions, key=lambda x: (x['has_portal_account'], x['score']), reverse=True)
    for c in sorted_without[:(25 - len(scored_299))]:
        c_entry = dict(c)
        c_entry['intent_score'] = 20 if c['has_portal_account'] else 10
        scored_299.append(c_entry)

scored_299.sort(key=lambda x: (x['intent_score'], x['logins_7d'], x['score']), reverse=True)

print(f"\nTop 10 of Top 25 High-Intent ₹299 Leads:")
for i, l in enumerate(scored_299[:10], 1):
    print(f"  {i}. [Score: {l['intent_score']}/100] {l['name']} | {l['email']} | Cert: {l['certId']} | Domain: {l['domain']} | Eval: {l['score']}/100 | Logins: {l['logins_7d']} | Last: {l['last_login']}")

# Save clean JSON outputs for top 25 and full breakdowns
with open('data/top_25_leads_499.json', 'w', encoding='utf-8') as f:
    json.dump(scored_499[:25], f, indent=2)

with open('data/top_25_leads_299.json', 'w', encoding='utf-8') as f:
    json.dump(scored_299[:25], f, indent=2)

with open('data/active_320_499_full.json', 'w', encoding='utf-8') as f:
    json.dump(scored_499, f, indent=2)

with open('data/provisional_378_299_full.json', 'w', encoding='utf-8') as f:
    json.dump(prov_with_sessions + prov_without_sessions, f, indent=2)

print("\nSaved detailed candidate JSON caches in data/ folder.")
