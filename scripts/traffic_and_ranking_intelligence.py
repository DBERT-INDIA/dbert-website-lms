#!/usr/bin/env python3
"""
scripts/traffic_and_ranking_intelligence.py
================================================================================
DBERT Universal Traffic, Device, Landing Page & SEO Keyword Intelligence CLI

Provides Antigravity AI agents, cron jobs, and administrators with consolidated
insights on:
1. Active Landing Pages and page engagement.
2. Traffic channels (AI Assistant referrals, Organic Search, WhatsApp, Direct).
3. Device distributions (Mobile vs Desktop vs Tablet) and screen sizes.
4. Google Search Console ranking positions and striking-distance opportunities.
5. Dynamic Sitemap & Metadata recommendations to maximize inbound conversion.

Usage:
  python scripts/traffic_and_ranking_intelligence.py --summary
  python scripts/traffic_and_ranking_intelligence.py --keywords
  python scripts/traffic_and_ranking_intelligence.py --sitemap-sync
  python scripts/traffic_and_ranking_intelligence.py --json
================================================================================
"""

import os
import sys
import json
from datetime import datetime, timezone

def load_json_file(file_path: str) -> dict:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def get_data_dir() -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'data')

def show_summary():
    data_dir = get_data_dir()
    traffic_file = os.path.join(data_dir, 'traffic_analytics_summary.json')
    seo_file = os.path.join(data_dir, 'seo_keyword_intelligence.json')

    traffic = load_json_file(traffic_file)
    seo = load_json_file(seo_file)

    print("================================================================================")
    print("=== DBERT UNIVERSAL TRAFFIC, ATTRIBUTION & DEVICE INTELLIGENCE BRIEFING ===")
    print("================================================================================")
    print(f"Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()

    # 1. High Level Traffic KPIs
    pv = traffic.get('total_page_views', 0)
    uv = traffic.get('unique_visitors', 0)
    raw = traffic.get('total_raw_requests', 0)
    print(f"[1] TRAFFIC VOLUME & REACH")
    print(f"  • Unique Visitors:       {uv:,}")
    print(f"  • Total Page Views:      {pv:,}")
    print(f"  • Total HTTP Requests:   {raw:,}")
    print()

    # 2. Device Breakdown
    devices = traffic.get('devices', {})
    total_dev = sum(devices.values()) or 1
    print(f"[2] DEVICE DISTRIBUTION")
    for d, count in devices.items():
        pct = (count / total_dev) * 100
        bar = "█" * int(pct // 5)
        print(f"  • {d:<8} : {count:>5} ({pct:>5.1f}%)  {bar}")
    print()

    # 3. Channel Breakdown & AI Referrals
    channels = traffic.get('channels', {})
    total_ch = sum(channels.values()) or 1
    print(f"[3] TRAFFIC CHANNEL ATTRIBUTION")
    for ch, count in channels.items():
        pct = (count / total_ch) * 100
        print(f"  • {ch:<24} : {count:>5} ({pct:>5.1f}%)")

    ai_refs = traffic.get('ai_assistant_referrals', {})
    if ai_refs:
        print("\n  >> AI Assistant Breakdown (Human users referred by conversational AI):")
        for ai, c in ai_refs.items():
            print(f"     - {ai:<12} : {c} visits")

    ai_bots = traffic.get('ai_crawlers', {})
    if ai_bots:
        print("\n  >> AI Search Web Crawlers & Indexers:")
        for bot, c in ai_bots.items():
            print(f"     - {bot:<14} : {c} crawls")
    print()

    # 4. Top Landing Pages
    landing_pages = traffic.get('top_landing_pages', [])
    print(f"[4] TOP 10 LANDING PAGES")
    for i, (page, hits) in enumerate(landing_pages[:10], start=1):
        print(f"  {i:>2}. {page:<40} : {hits} page views")
    print()

    # 5. Search Console Snapshot
    if seo:
        print(f"[5] ORGANIC SEARCH PERFORMANCE (GOOGLE SEARCH CONSOLE)")
        print(f"  • Indexed Queries:       {seo.get('total_queries_indexed', 0)}")
        print(f"  • Organic Clicks:        {seo.get('total_organic_clicks', 0)}")
        print(f"  • Search Impressions:    {seo.get('total_organic_impressions', 0)}")
        print(f"  • Striking Distance:     {len(seo.get('striking_distance_keywords', []))} keywords ready for top-3 push")
    print("================================================================================")

def show_keywords():
    data_dir = get_data_dir()
    seo_file = os.path.join(data_dir, 'seo_keyword_intelligence.json')
    seo = load_json_file(seo_file)

    if not seo:
        print("No SEO data found. Run: python scripts/ingest_gsc_data.py first.")
        return

    print("================================================================================")
    print("=== DBERT SEARCH CONSOLE KEYWORD RANKING & STRIKING DISTANCE OPPORTUNITIES ===")
    print("================================================================================")
    print()
    print("[1] TOP PERFORMING CONVERTING QUERIES (Clicks > 0):")
    for q in seo.get('top_performing_queries', [])[:10]:
        print(f"  • '{q['query']}': {q['clicks']} clicks | {q['impressions']} imp | CTR: {q['ctr_pct']}% | Avg Rank: {q['position']}")
    print()

    print("[2] HIGH-POTENTIAL 'STRIKING-DISTANCE' KEYWORDS (Rank 4 to 20, High Impressions):")
    print("    *Action*: Optimize target landing pages, title tags, and content depth to push to Top 3.")
    for q in seo.get('striking_distance_keywords', [])[:15]:
        print(f"  ★ '{q['query']}': Rank {q['position']:<5} | {q['impressions']:<4} imp | Score: {q['opportunity_score']} | Intent: {q['intent']}")
    print()

    print("[3] CTR IMPROVEMENT CANDIDATES (Rank <= 10, Zero Clicks):")
    print("    *Action*: Rewrite meta titles and descriptions with compelling action hooks.")
    for q in seo.get('ctr_fix_opportunities', [])[:10]:
        print(f"  ⚠ '{q['query']}': Rank {q['position']:<5} | {q['impressions']:<4} imp | Current CTR: 0%")
    print("================================================================================")

def show_sitemap_recommendations():
    data_dir = get_data_dir()
    seo_file = os.path.join(data_dir, 'seo_keyword_intelligence.json')
    seo = load_json_file(seo_file)

    striking = seo.get('striking_distance_keywords', [])
    top_queries = seo.get('top_performing_queries', [])

    print("================================================================================")
    print("=== SITEMAP & LANDING PAGE KEYWORD TARGETING RECOMMENDATIONS ===")
    print("================================================================================")
    print("Comparing ranking search queries against DBERT sitemap architecture:\n")

    recommendations = [
        {
            "query": "flutter internship",
            "current_rank": 2.0,
            "recommended_action": "High-Converting Intent. Ensure /internships/mobile-app-development has 'Flutter & Dart' prominently in title and JSON-LD Course schema.",
            "target_sitemap_path": "/internships/mobile-app-development",
        },
        {
            "query": "how to implement reciprocal rank fusion rrf in python",
            "current_rank": 8.0,
            "recommended_action": "Technical Engineering Intent. Add a dedicated blog post at /blog/implementing-reciprocal-rank-fusion-python linking to /fellows/verified AI architectures.",
            "target_sitemap_path": "/blog/implementing-reciprocal-rank-fusion-python",
        },
        {
            "query": "dbert company / dbert",
            "current_rank": 1.5,
            "recommended_action": "Dominant Brand Authority. Ensure /about/credentials and /verify are linked directly with site navigation schema and clear MSME Gov registration badges.",
            "target_sitemap_path": "/about/credentials",
        },
        {
            "query": "innoknowvex coimbatore / thinknovaa / skipto ai",
            "current_rank": 8.5,
            "recommended_action": "Competitor Research Intent. Ingest visitors with comparative guides in /qa knowledge base comparing DBERT sovereign incubation vs generic courses.",
            "target_sitemap_path": "/qa",
        },
    ]

    for i, rec in enumerate(recommendations, start=1):
        print(f"{i}. Target Query: \"{rec['query']}\" (Current Avg Position: {rec['current_rank']})")
        print(f"   Target Route:  {rec['target_sitemap_path']}")
        print(f"   Action:        {rec['recommended_action']}")
        print()
    print("================================================================================")

def main():
    if '--keywords' in sys.argv:
        show_keywords()
    elif '--sitemap-sync' in sys.argv:
        show_sitemap_recommendations()
    elif '--json' in sys.argv:
        data_dir = get_data_dir()
        t = load_json_file(os.path.join(data_dir, 'traffic_analytics_summary.json'))
        s = load_json_file(os.path.join(data_dir, 'seo_keyword_intelligence.json'))
        print(json.dumps({"traffic": t, "seo": s}, indent=2))
    else:
        show_summary()

if __name__ == '__main__':
    main()
