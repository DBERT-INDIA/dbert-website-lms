import os
import re
import json
from datetime import datetime
import xml.etree.ElementTree as ET

print("=== GENERATING UPGRADED WEBSITE SITEMAP ===")

BASE_URL = 'https://dbert.in'
TODAY = datetime.now().strftime('%Y-%m-%d')

# 1. Read existing public/sitemap.xml to preserve all historical routes
historical_routes = set()
pub_xml_path = 'apps/website/public/sitemap.xml'
if os.path.exists(pub_xml_path):
    tree = ET.parse(pub_xml_path)
    for c in tree.getroot():
        loc = c.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
        if loc is not None and loc.text:
            r = loc.text.replace(BASE_URL, '').replace('https://dbert.in', '')
            historical_routes.add(r)
print(f"Historical routes preserved: {len(historical_routes)}")

# 2. Read seo.config.ts
with open('apps/website/src/data/seo.config.ts', encoding='utf-8') as f:
    seo_text = f.read()

seo_routes = set()
for r in re.findall(r"'(\/[^']*)':\s*\{", seo_text):
    m = re.search(r"'" + re.escape(r) + r"':\s*\{[^}]*noindex:\s*true", seo_text)
    if not m:
        seo_routes.add(r)
print(f"Active SEO config routes: {len(seo_routes)}")

# 3. Read domains.config.ts
with open('apps/website/src/data/domains.config.ts', encoding='utf-8') as f:
    dom_text = f.read()
domain_slugs = re.findall(r"slug:\s*'([a-z0-9-]+)'", dom_text)
domain_routes = [f"/verify/directory/{s}" for s in set(domain_slugs)]
print(f"Canonical domain directory routes: {len(domain_routes)} -> {domain_routes}")

# 4. Domain courses routes
course_slugs = [
    'ai-agent-development',
    'generative-ai',
    'full-stack-development',
    'data-analytics',
    'cybersecurity',
    'devops-cloud',
    'mobile-app-development',
    'python-automation',
    'ui-ux-design',
]
course_routes = [f"/courses/{s}" for s in course_slugs]
print(f"Direct course routes: {len(course_routes)}")

# 5. Read geo_domains.config.ts
with open('apps/website/src/data/geo_domains.config.ts', encoding='utf-8') as f:
    geo_text = f.read()
cities = [c[0] for c in re.findall(r"'([a-z0-9-]+)':\s*\{\s*slug:\s*'([a-z0-9-]+)'", geo_text[:geo_text.find('GEO_ROLES')])]
roles = [r[0] for r in re.findall(r"'([a-z0-9-]+)':\s*\{\s*slug:\s*'([a-z0-9-]+)'", geo_text[geo_text.find('GEO_ROLES'):])]
geo_routes = []
for r in roles:
    for c in cities:
        geo_routes.append(f"/internships/{r}/{c}")
print(f"Geo internship routes: {len(geo_routes)} (roles: {len(roles)}, cities: {len(cities)})")

# 6. Read verified certificates from certificates_registry.json
with open('apps/website/src/data/certificates_registry.json', encoding='utf-8') as f:
    certs = json.load(f)
verified_cert_routes = [f"/verify/{cid}" for cid, c in certs.items() if c.get('verified') is True]
print(f"Verified certificate routes: {len(verified_cert_routes)}")

# 7. Read blog slugs
blog_slugs = set()
blog_dir = 'apps/website/src/content/blog'
if os.path.exists(blog_dir):
    for f in os.listdir(blog_dir):
        if f.endswith('.md') or f.endswith('.mdx'):
            blog_slugs.add(f[:-3] if f.endswith('.md') else f[:-4])

pub_art_path = 'apps/website/src/data/published_articles.json'
if os.path.exists(pub_art_path):
    with open(pub_art_path, encoding='utf-8') as f:
        pub_articles = json.load(f)
    for p in pub_articles:
        if p.get('slug'):
            blog_slugs.add(p['slug'])

blog_routes = [f"/blog/{s}" for s in blog_slugs]
print(f"Blog routes: {len(blog_routes)}")

# 8. Priority and Change Frequency calculation
def get_priority(route):
    if route in ('', '/'):
        return '1.0'
    if route in ['/startups', '/ai-solutions', '/learners', '/labs', '/learners/courses', '/learners/fellowship', '/learners/jobs', '/internships', '/cohorts/aivara', '/verify/directory', '/hire/pre-vetted-engineers', '/fellows/verified', '/qa', '/about/team']:
        return '0.95'
    if route.startswith('/verify/directory/'):
        return '0.90'
    if route in ['/verify', '/about/careers', '/labs/opensource', '/learners/accelerate', '/learners/launchpad']:
        return '0.9'
    if route.startswith('/learners/courses/') or route.startswith('/courses/'):
        return '0.9'
    if route.startswith('/internships/'):
        return '0.85'
    if route.startswith('/ai-solutions/products/'):
        return '0.9'
    if route.startswith('/startups/services/'):
        return '0.85'
    if route in ['/enroll/1999', '/about/credentials', '/pricing']:
        return '0.85'
    if route.startswith('/blog/'):
        return '0.85'
    if route.startswith('/verify/'):
        return '0.8'
    if route in ['/privacy', '/terms', '/refund']:
        return '0.5'
    depth = len([p for p in route.split('/') if p])
    if depth <= 2:
        return '0.8'
    return '0.7'

def get_changefreq(route):
    if route in ('', '/'):
        return 'daily'
    if route in ['/learners/jobs', '/learners/fellowship', '/cohorts/aivara', '/verify/directory', '/hire/pre-vetted-engineers', '/fellows/verified', '/qa', '/about/team'] or route.startswith('/verify/directory/'):
        return 'daily'
    if route.startswith('/learners/courses') or route.startswith('/courses/') or route.startswith('/internships/') or route.startswith('/blog/') or route.startswith('/verify/'):
        return 'weekly'
    if route in ['/startups', '/ai-solutions', '/learners', '/verify', '/enroll/1999', '/about/careers', '/labs/opensource']:
        return 'weekly'
    if route in ['/privacy', '/terms', '/refund']:
        return 'yearly'
    return 'monthly'

# Combine and deduplicate
all_routes = set(['', '/fellows/verified'])
all_routes.update(historical_routes)
all_routes.update(seo_routes)
all_routes.update(domain_routes)
all_routes.update(course_routes)
all_routes.update(geo_routes)
all_routes.update(verified_cert_routes)
all_routes.update(blog_routes)

def route_sort_key(r):
    if r in ('', '/'):
        return (0, '')
    p = float(get_priority(r))
    return (1 - p, r)

sorted_routes = sorted(all_routes, key=route_sort_key)
print(f"Total upgraded unique routes in sitemap: {len(sorted_routes)}")

# Build XML
xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]

for r in sorted_routes:
    route_norm = r.rstrip('/') if r != '/' else ''
    url = f"{BASE_URL}{route_norm}"
    p = get_priority(r)
    f = get_changefreq(r)
    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{url}</loc>')
    xml_lines.append(f'    <lastmod>{TODAY}</lastmod>')
    xml_lines.append(f'    <changefreq>{f}</changefreq>')
    xml_lines.append(f'    <priority>{p}</priority>')
    xml_lines.append('  </url>')

xml_lines.append('</urlset>\n')
xml_content = '\n'.join(xml_lines)

# Write to apps/website/public/sitemap.xml
with open('apps/website/public/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(xml_content)
print("Updated apps/website/public/sitemap.xml successfully!")

# Write to apps/website/sitemap.xml
with open('apps/website/sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(xml_content)
print("Updated apps/website/sitemap.xml successfully!")
