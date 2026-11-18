import sys
sys.path.insert(0, 'apps/portal')
import app

print("app.py imported successfully!")
print(f"PLATFORM_DOMAIN_COURSES count: {len(app.PLATFORM_DOMAIN_COURSES)}")
print(f"DOMAIN_COURSES_METADATA count: {len(app.DOMAIN_COURSES_METADATA)}")
print(f"ALL_DOMAIN_COURSES count: {len(app.ALL_DOMAIN_COURSES)}")
for c in app.ALL_DOMAIN_COURSES:
    print(f" - [{c['domain']}] {c['title']} ({len(c['chapters'])} chapters)")
