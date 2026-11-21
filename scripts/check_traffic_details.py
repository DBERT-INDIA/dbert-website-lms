import sys
import os
import json

if os.path.exists('/var/www/dbert-website-lms/apps/portal'):
    sys.path.insert(0, '/var/www/dbert-website-lms/apps/portal')
else:
    sys.path.insert(0, 'apps/portal')

from app import get_db

with get_db() as conn:
    # Check tables related to visitors or traffic
    tables = [r[0] for r in conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'").fetchall()]
    print("Tables in DB:", [t for t in tables if any(k in t for k in ['visit', 'event', 'track', 'lead', 'click', 'session', 'log'])])

    # Check visitor_id in visitor_events if table exists
    if 'visitor_events' in tables:
        events = conn.execute("""
            SELECT ve.event_type, ve.page_url, ve.referrer, count(*)
            FROM visitor_events ve
            JOIN applications a ON a.visitor_id = ve.visitor_id
            WHERE a.status = 'Under Review'
            GROUP BY ve.event_type, ve.page_url, ve.referrer
            ORDER BY count(*) DESC
            LIMIT 15
        """).fetchall()
        print("\n=== Visitor Events for Under Review Candidates ===")
        for e in events:
            print(dict(e) if hasattr(e, 'keys') else e)
    else:
        print("No visitor_events table.")

    # Check applications intent_answers and college
    apps = conn.execute("""
        SELECT id, name, college, city, why_join, domain, source, created_at
        FROM applications
        WHERE status = 'Under Review'
        ORDER BY id DESC
        LIMIT 10
    """).fetchall()
    print("\n=== Sample Application Metadata (College, City, Why Join) ===")
    for a in apps:
        d = dict(a) if hasattr(a, 'keys') else {'id': a[0], 'name': a[1], 'college': a[2], 'city': a[3], 'why_join': a[4], 'domain': a[5], 'source': a[6], 'created_at': str(a[7])}
        print(f"ID {d['id']}: {d['name']} | College: {d['college']} | City: {d['city']} | Created: {d['created_at']}")
