#!/usr/bin/env python3
"""
scripts/ingest_gsc_data.py
================================================================================
Google Search Console (GSC) & Keyword Intelligence Engine for DBERT

Parses GSC export CSVs from data/google/:
- Queries.csv
- Pages.csv
- Devices.csv
- Countries.csv

Calculates:
1. High-Intent Keywords (Clicks > 0).
2. Striking-Distance Keywords (Position 4.0 to 20.0, high impressions ready for SEO push).
3. Meta Title / CTR Optimization Opportunities (High impressions, low CTR).
4. Top Performing Landing Pages by Organic Search Traffic.
5. Device and Geographic split.

Saves structured intelligence to data/seo_keyword_intelligence.json.
================================================================================
"""

import os
import sys
import csv
import json
from datetime import datetime, timezone

def parse_num(val):
    if not val:
        return 0
    val_clean = str(val).strip().replace(',', '')
    try:
        return int(val_clean)
    except ValueError:
        try:
            return float(val_clean)
        except ValueError:
            return 0

def parse_pct(val):
    if not val:
        return 0.0
    val_clean = str(val).strip().replace('%', '')
    try:
        return float(val_clean)
    except ValueError:
        return 0.0

def classify_query_intent(query: str) -> str:
    q = (query or '').lower()
    if 'dbert' in q:
        return 'Brand'
    if any(k in q for k in ['intern', 'stipend', 'hire', 'job', 'career', 'fresher']):
        return 'Internship & Careers'
    if any(k in q for k in ['python', 'ai', 'agent', 'model', 'fastapi', 'rrf', 'rag', 'redis', 'architecture']):
        return 'Technical & Engineering'
    return 'Competitor / Industry'

def ingest_gsc(google_dir: str) -> dict:
    queries_file = os.path.join(google_dir, 'Queries.csv')
    pages_file = os.path.join(google_dir, 'Pages.csv')
    devices_file = os.path.join(google_dir, 'Devices.csv')
    countries_file = os.path.join(google_dir, 'Countries.csv')

    all_queries = []
    top_performing_queries = []
    striking_distance_keywords = []
    ctr_fix_opportunities = []

    if os.path.exists(queries_file):
        with open(queries_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                q = row.get('Top queries', '').strip()
                clicks = parse_num(row.get('Clicks', 0))
                impressions = parse_num(row.get('Impressions', 0))
                ctr = parse_pct(row.get('CTR', 0))
                pos = parse_num(row.get('Position', 0))

                if not q:
                    continue

                intent = classify_query_intent(q)
                # Opportunity score: impressions * log factor of position
                opp_score = round(impressions / max(1.0, pos), 2)

                record = {
                    "query": q,
                    "clicks": clicks,
                    "impressions": impressions,
                    "ctr_pct": ctr,
                    "position": pos,
                    "intent": intent,
                    "opportunity_score": opp_score,
                }
                all_queries.append(record)

                if clicks > 0:
                    top_performing_queries.append(record)

                # Striking distance: rank between 4.0 and 20.0 with >= 5 impressions
                if 4.0 <= pos <= 20.0 and impressions >= 5:
                    striking_distance_keywords.append(record)

                # CTR fix: rank <= 10.0, impressions >= 10, but CTR == 0%
                if pos <= 10.0 and impressions >= 10 and ctr == 0:
                    ctr_fix_opportunities.append(record)

    # Sort
    all_queries.sort(key=lambda x: x['impressions'], reverse=True)
    top_performing_queries.sort(key=lambda x: x['clicks'], reverse=True)
    striking_distance_keywords.sort(key=lambda x: x['opportunity_score'], reverse=True)
    ctr_fix_opportunities.sort(key=lambda x: x['impressions'], reverse=True)

    # Pages
    all_pages = []
    if os.path.exists(pages_file):
        with open(pages_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = row.get('Top pages', '').strip()
                if not p:
                    continue
                all_pages.append({
                    "page": p,
                    "clicks": parse_num(row.get('Clicks', 0)),
                    "impressions": parse_num(row.get('Impressions', 0)),
                    "ctr_pct": parse_pct(row.get('CTR', 0)),
                    "position": parse_num(row.get('Position', 0)),
                })
        all_pages.sort(key=lambda x: x['clicks'], reverse=True)

    # Devices
    devices = []
    if os.path.exists(devices_file):
        with open(devices_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dev = row.get('Device', '').strip()
                if not dev: continue
                devices.append({
                    "device": dev,
                    "clicks": parse_num(row.get('Clicks', 0)),
                    "impressions": parse_num(row.get('Impressions', 0)),
                    "ctr_pct": parse_pct(row.get('CTR', 0)),
                    "position": parse_num(row.get('Position', 0)),
                })

    # Countries
    countries = []
    if os.path.exists(countries_file):
        with open(countries_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                c = row.get('Country', '').strip()
                if not c: continue
                countries.append({
                    "country": c,
                    "clicks": parse_num(row.get('Clicks', 0)),
                    "impressions": parse_num(row.get('Impressions', 0)),
                    "ctr_pct": parse_pct(row.get('CTR', 0)),
                    "position": parse_num(row.get('Position', 0)),
                })
        countries.sort(key=lambda x: x['impressions'], reverse=True)

    return {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "total_queries_indexed": len(all_queries),
        "total_organic_clicks": sum(q['clicks'] for q in all_queries),
        "total_organic_impressions": sum(q['impressions'] for q in all_queries),
        "top_performing_queries": top_performing_queries,
        "striking_distance_keywords": striking_distance_keywords[:20],
        "ctr_fix_opportunities": ctr_fix_opportunities[:20],
        "top_landing_pages": all_pages[:25],
        "devices": devices,
        "top_countries": countries[:10],
    }

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_dir = os.path.join(base_dir, 'data', 'google')

    if not os.path.exists(google_dir):
        print(f"Error: Directory {google_dir} not found.")
        sys.exit(1)

    print(f"Ingesting Search Console files from: {google_dir}")
    intel = ingest_gsc(google_dir)

    output_file = os.path.join(base_dir, 'data', 'seo_keyword_intelligence.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(intel, f, indent=2)

    print(f"Successfully generated: {output_file}")
    print(f"Indexed Queries: {intel['total_queries_indexed']}")
    print(f"Total Organic Clicks: {intel['total_organic_clicks']} | Impressions: {intel['total_organic_impressions']}")
    print(f"Striking Distance Target Keywords: {len(intel['striking_distance_keywords'])}")
    print(f"Top 3 Queries with Clicks:")
    for q in intel['top_performing_queries'][:3]:
        print(f"  - '{q['query']}': {q['clicks']} clicks, {q['impressions']} imp, Pos {q['position']}")

if __name__ == '__main__':
    main()
