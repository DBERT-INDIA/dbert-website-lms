"""
DBERT LMS — Sourcing CLI for Internships and Jobs
Usage:
  python -m services.sourcing.cli --type jobs --count 3000
  python -m services.sourcing.cli --type internships --count 1000
"""

import sys
import os
import argparse

# Add apps/portal to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from services.sourcing.pipeline import SourcingPipeline

def main():
    parser = argparse.ArgumentParser(description="DBERT LMS Multi-Source Scraper & Ingestion Pipeline")
    parser.add_argument("--type", choices=["jobs", "internships"], default="jobs", help="Target opportunity type")
    parser.add_argument("--count", type=int, default=3000, help="Number of new unique leads to ingest")
    args = parser.parse_args()

    table_name = "scraped_jobs" if args.type == "jobs" else "scraped_internships"

    print(f"[*] Starting DBERT LMS Sourcing Pipeline ({args.type.upper()} -> {table_name}, Target: {args.count} new unique records)...")
    pipeline = SourcingPipeline(target_table=table_name)
    result = pipeline.run(target_new_count=args.count)
    print("\n[+] Sourcing Pipeline Execution Summary:")
    for k, v in result.items():
        print(f"    {k}: {v}")

if __name__ == "__main__":
    main()
