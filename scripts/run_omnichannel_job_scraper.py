import sys
import os
import argparse
import sqlite3
import datetime
import logging
from typing import List, Dict, Any

# Ensure root path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.scrapers.base import CANONICAL_DOMAINS, ScrapedItem, slugify, generate_fingerprint
from scripts.scrapers.unstop_adapter import UnstopScraper
from scripts.scrapers.international_remote_adapter import InternationalRemoteScraper
from scripts.scrapers.hireintern_adapter import HireInternScraper
from scripts.scrapers.search_aggregator_adapter import SearchAggregatorScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("OmnichannelScraper")

def get_or_create_company(conn: sqlite3.Connection, company_name: str, domain: str = "") -> int:
    cur = conn.cursor()
    cur.execute("SELECT id FROM companies WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))", (company_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    
    # Insert new company
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c_slug = slugify(company_name)
    website = f"https://lms.dbert.in/company/{c_slug}/careers"
    about = f"{company_name} is an active industry partner recruiting technical talent across {domain or 'engineering'} tracks."
    
    cur.execute("""
        INSERT INTO companies (name, email, phone, website, about, password_hash, is_approved, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, 1, 1, ?, ?)
    """, (company_name, f"careers@{c_slug}.com", "N/A", website, about, "EXTERNAL_RECRUITER", now, now))
    conn.commit()
    return cur.lastrowid

def parse_stipend_numbers(stipend_text: str):
    import re
    # Extract numbers from string
    clean = stipend_text.replace(",", "")
    nums = re.findall(r"\d+", clean)
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    elif len(nums) == 1:
        val = int(nums[0])
        return val, val
    return 15000, 25000

def ingest_item(conn: sqlite3.Connection, item: ScrapedItem) -> Dict[str, Any]:
    cur = conn.cursor()
    table_name = "scraped_internships" if item.post_type == "internship" else "scraped_jobs"
    
    # 1. Deduplication check in scraped table
    # Match by Company + Role + Domain + Work_Model (or URL)
    cur.execute(f"""
        SELECT id, URL FROM {table_name}
        WHERE LOWER(TRIM(Company)) = LOWER(TRIM(?))
          AND LOWER(TRIM(Role)) = LOWER(TRIM(?))
          AND LOWER(TRIM(Domain)) = LOWER(TRIM(?))
          AND LOWER(TRIM(Work_Model)) = LOWER(TRIM(?))
    """, (item.company, item.role, item.domain, item.work_model))
    
    existing = cur.fetchone()
    is_new = False
    scraped_id = None
    
    if existing:
        scraped_id = existing[0]
        # Update End_Date and URL if changed
        cur.execute(f"""
            UPDATE {table_name}
            SET End_Date = ?, URL = ?, Stipend = ?, Description = ?
            WHERE id = ?
        """, (item.end_date, item.url, item.stipend, item.description, scraped_id))
    else:
        is_new = True
        cur.execute(f"""
            INSERT INTO {table_name} (
                Domain, Company, Role, Location, Is_Remote, Start_Date, End_Date,
                Stipend, URL, Description, Source, Region, Stipend_Normalized,
                Work_Model, City, Clicks
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            item.domain, item.company, item.role, item.location,
            "Yes" if item.is_remote else "No", item.start_date, item.end_date,
            item.stipend, item.url, item.description, item.source, item.region,
            item.stipend_normalized, item.work_model, item.city
        ))
        scraped_id = cur.lastrowid

    # 2. Dual Ingestion into canonical `posts` table
    post_slug = f"{slugify(item.role)}-at-{slugify(item.company)}-{item.domain[:3].lower()}"
    cur.execute("SELECT id FROM posts WHERE slug = ? OR (LOWER(title) = LOWER(?) AND domain = ?)", (post_slug, item.role, item.domain))
    post_row = cur.fetchone()
    
    if not post_row:
        company_id = get_or_create_company(conn, item.company, item.domain)
        s_min, s_max = parse_stipend_numbers(item.stipend)
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        exp_str = (datetime.datetime.now() + datetime.timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S")
        
        cur.execute("""
            INSERT INTO posts (
                company_id, post_type, domain, title, slug, description,
                responsibilities, skills, location, work_mode, stipend_min,
                stipend_max, pay_period, is_unpaid, duration, openings,
                apply_by, certifications_json, eligibility, status,
                published_at, expires_at, views, created_at, updated_at
            ) VALUES (
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, 'month', 0, '2-3 Months', 3,
                ?, '[]', 'Open to pre-vetted interns, graduates, and professionals with domain competency.', 'published',
                ?, ?, 0, ?, ?
            )
        """, (
            company_id, item.post_type, item.domain, item.role, post_slug,
            item.description,
            f"• Participate in active sprint milestones and code reviews.\n• Deliver production-quality modules according to technical specifications for {item.domain}.\n• Maintain communication standards and sprint deadlines.",
            item.skills or item.domain,
            item.location, item.work_model, s_min, s_max,
            item.end_date, now_str, exp_str, now_str, now_str
        ))
    
    conn.commit()
    return {"is_new": is_new, "domain": item.domain, "id": scraped_id}

def main():
    parser = argparse.ArgumentParser(description="DBERT Omnichannel Job & Internship Scraper")
    parser.add_argument("--all-domains", action="store_true", help="Scrape for all 9 canonical domains")
    parser.add_argument("--domain", type=str, default=None, help="Scrape specific domain")
    parser.add_argument("--post-types", type=str, default="internship,job", help="Comma-separated post types")
    parser.add_argument("--sources", type=str, default="all", help="all or comma-separated: unstop,international,hireintern,aggregator")
    parser.add_argument("--limit-per-domain", type=int, default=15, help="Number of items to fetch per domain per source")
    parser.add_argument("--db", type=str, default="apps/portal/internship.db", help="Path to SQLite database")

    args = parser.parse_args()

    domains = CANONICAL_DOMAINS if args.all_domains or not args.domain else [args.domain]
    post_types = [p.strip() for p in args.post_types.split(",")]
    
    # Initialize scrapers
    scrapers = []
    source_flags = [s.strip().lower() for s in args.sources.split(",")]
    if "all" in source_flags or "unstop" in source_flags:
        scrapers.append(UnstopScraper())
    if "all" in source_flags or "international" in source_flags:
        scrapers.append(InternationalRemoteScraper())
    if "all" in source_flags or "hireintern" in source_flags:
        scrapers.append(HireInternScraper())
    if "all" in source_flags or "aggregator" in source_flags:
        scrapers.append(SearchAggregatorScraper())

    logger.info(f"Starting scraper run with {len(scrapers)} sources across {len(domains)} domains for types: {post_types}")
    conn = sqlite3.connect(args.db)

    stats = {
        "total_scraped": 0,
        "new_inserted": 0,
        "existing_updated": 0,
        "by_domain": {d: 0 for d in domains}
    }

    for ptype in post_types:
        for scraper in scrapers:
            logger.info(f"Running scraper '{scraper.name}' for post_type='{ptype}'...")
            try:
                for d in domains:
                    items = scraper.scrape(domain=d, post_type=ptype, limit=args.limit_per_domain)
                    for item in items:
                        stats["total_scraped"] += 1
                        res = ingest_item(conn, item)
                        if res["is_new"]:
                            stats["new_inserted"] += 1
                        else:
                            stats["existing_updated"] += 1
                        stats["by_domain"][item.domain] = stats["by_domain"].get(item.domain, 0) + 1
            except Exception as e:
                logger.error(f"Error executing scraper {scraper.name}: {e}", exc_info=True)

    conn.close()

    logger.info("=== SCRAPING & INGESTION COMPLETE ===")
    logger.info(f"Total Scraped: {stats['total_scraped']}")
    logger.info(f"New Inserted: {stats['new_inserted']}")
    logger.info(f"Existing Updated: {stats['existing_updated']}")
    logger.info("Counts by Domain:")
    for d, cnt in stats["by_domain"].items():
        logger.info(f"  • {d}: {cnt}")

if __name__ == "__main__":
    main()
