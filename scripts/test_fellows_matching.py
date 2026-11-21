import json

with open('apps/website/src/data/certificates_registry.json', 'r', encoding='utf-8') as f:
    certs = json.load(f)

with open('data/active_54h_cohort.json', 'r', encoding='utf-8') as f:
    cohort = json.load(f)

with open('data/provisional_completed_linkedin.json', 'r', encoding='utf-8') as f:
    prov_li = json.load(f)

with open('data/published_articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

li_map = {}
for x in cohort:
    em = x.get('email', '').strip().lower()
    if em and x.get('linkedin_url'):
        li_map[em] = {
            'linkedin_url': x.get('linkedin_url'),
            'github_url': x.get('github_url'),
            'name': x.get('name')
        }

for x in prov_li:
    em = x.get('email', '').strip().lower()
    if em and x.get('linkedin_url') and em not in li_map:
        li_map[em] = {
            'linkedin_url': x.get('linkedin_url'),
            'cert_id': x.get('cert_id'),
            'name': x.get('name')
        }

print(f'Total candidates with LinkedIn: {len(li_map)}')

art_map = {}
for a in articles:
    cid = a.get('certId')
    auth = a.get('author', '').strip().lower()
    if cid:
        art_map[cid] = a
    if auth:
        art_map[auth] = a

# Match with all certificates (both verified and provisional)
print(f'Total certificates in registry: {len(certs)}')

verified_count = 0
matches = []
for cid, c in certs.items():
    em = (c.get('email') or '').strip().lower()
    hn = (c.get('holderName') or '').strip().lower()
    is_ver = c.get('status') == 'VERIFIED' or (c.get('verified') and not c.get('isProvisional'))
    
    li_data = li_map.get(em, {})
    art_data = art_map.get(cid, art_map.get(hn, {}))
    
    if li_data or art_data or is_ver:
        matches.append({
            'certId': cid,
            'name': c.get('holderName'),
            'email': em,
            'domain': c.get('domain'),
            'college': c.get('college'),
            'score': c.get('score'),
            'isVerified': is_ver,
            'linkedin_url': li_data.get('linkedin_url'),
            'github_url': li_data.get('github_url'),
            'article_title': art_data.get('title'),
            'article_slug': art_data.get('slug'),
            'article_url': art_data.get('canonicalUrl')
        })

print(f'Total enriched fellows matched: {len(matches)}')
print('\nSample matches:')
for m in matches[:15]:
    ver_str = 'VERIFIED' if m['isVerified'] else 'PROVISIONAL'
    li_str = 'LI: YES' if m['linkedin_url'] else 'LI: NO'
    art_str = f"ART: {m['article_slug']}" if m['article_slug'] else 'ART: NO'
    print(f"[{m['certId']}] {m['name']} ({ver_str}) | {li_str} | {art_str}")
