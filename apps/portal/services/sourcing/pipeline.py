"""
DBERT LMS — Unified Sourcing & Database Ingestion Pipeline
Guarantees zero-duplicate ingestion across multi-source scrapers directly
into the active database (PostgreSQL in production, SQLite in development).
Supports both internships and full-time jobs.
"""

import os
import sys
import logging
from typing import List, Dict, Any, Set

from .normalizer import (
    normalize_domain,
    normalize_stipend,
    normalize_work_model,
    normalize_dates,
    make_dedup_hash
)
from .sources import (
    UnstopScraper,
    UnstopJobsScraper,
    ArbeitnowScraper,
    GlobalApisScraper,
    WebAggregatorScraper
)

logger = logging.getLogger("sourcing.pipeline")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class SourcingPipeline:
    def __init__(self, target_table: str = "scraped_internships", db_conn=None):
        self.target_table = target_table
        self.conn = db_conn
        self.seen_content_keys: Set[str] = set()
        self.seen_urls: Set[str] = set()

    def _get_connection(self):
        if self.conn:
            return self.conn
        
        # Try portal database adapter
        try:
            from services.database.adapter import get_db_adapter
            return get_db_adapter()
        except Exception:
            # Fallback to direct sqlite
            import sqlite3
            db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "internship.db"))
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn

    def load_existing_signatures(self, conn) -> int:
        """Preloads existing company+role hashes and URLs to prevent ANY duplicates."""
        cursor = conn.cursor()
        cursor.execute(f'SELECT "Company", "Role", "URL" FROM {self.target_table}')
        count = 0
        for row in cursor.fetchall():
            c = row[0] if isinstance(row, (tuple, list)) else row["Company"]
            r = row[1] if isinstance(row, (tuple, list)) else row["Role"]
            u = row[2] if isinstance(row, (tuple, list)) else row["URL"]
            
            ck, uk = make_dedup_hash(c, r, u)
            if ck:
                self.seen_content_keys.add(ck)
            if uk:
                self.seen_urls.add(uk)
            count += 1
        return count

    def run(self, target_new_count: int = 3000) -> Dict[str, Any]:
        """
        Runs all scrapers until target_new_count non-duplicate leads are ingested into self.target_table.
        """
        conn = self._get_connection()
        initial_db_count = self.load_existing_signatures(conn)
        logger.info(f"Target table: {self.target_table}. Loaded {initial_db_count} existing signatures for strict deduplication.")

        if self.target_table == "scraped_jobs":
            scrapers = [
                UnstopJobsScraper(),
                ArbeitnowScraper(),
                GlobalApisScraper(),
                WebAggregatorScraper()
            ]
        else:
            scrapers = [
                UnstopScraper(),
                ArbeitnowScraper(),
                GlobalApisScraper(),
                WebAggregatorScraper()
            ]

        total_scraped = 0
        total_duplicates_skipped = 0
        new_leads_to_insert: List[Dict[str, Any]] = []

        domain_counts: Dict[str, int] = {
            "AI Agent Development": 0,
            "Data Analyst": 0,
            "Full Stack Development": 0,
            "Python Automation": 0
        }

        for scraper in scrapers:
            remaining_needed = target_new_count - len(new_leads_to_insert)
            if remaining_needed <= 0:
                break
            
            fetch_quota = max(400, remaining_needed + 200)
            logger.info(f"[*] Running scraper: {scraper.name} (fetching quota: {fetch_quota}, remaining needed: {remaining_needed})...")
            
            try:
                raw_leads = scraper.fetch_leads(target_count=fetch_quota)
            except Exception as e:
                logger.error(f"Scraper {scraper.name} encountered error: {e}")
                raw_leads = []

            total_scraped += len(raw_leads)
            scraper_accepted = 0

            for lead in raw_leads:
                ck, uk = make_dedup_hash(lead.get("Company", ""), lead.get("Role", ""), lead.get("URL", ""))
                
                # Check for duplicate
                if (ck and ck in self.seen_content_keys) or (uk and uk in self.seen_urls):
                    total_duplicates_skipped += 1
                    continue

                # Register as seen immediately to prevent duplicates within this batch
                if ck:
                    self.seen_content_keys.add(ck)
                if uk:
                    self.seen_urls.add(uk)

                # Normalize fields
                domain = lead.get("Domain") or normalize_domain(lead.get("Role", ""), lead.get("Description", ""))
                stip_norm = normalize_stipend(lead.get("Stipend"))
                work_model, city = normalize_work_model(lead.get("Location"), lead.get("Is_Remote"))
                start_d, end_d = normalize_dates(lead.get("Start_Date"), lead.get("End_Date"))

                new_leads_to_insert.append({
                    "Domain": domain,
                    "Company": lead.get("Company", "Tech Enterprise"),
                    "Role": lead.get("Role", ""),
                    "Location": lead.get("Location", "India"),
                    "Is_Remote": lead.get("Is_Remote", "No"),
                    "Start_Date": start_d,
                    "End_Date": end_d,
                    "Stipend": lead.get("Stipend", "Competitive"),
                    "URL": lead.get("URL", ""),
                    "Description": lead.get("Description", "")[:500],
                    "Source": lead.get("Source", scraper.name),
                    "Region": lead.get("Region", scraper.region),
                    "Stipend_Normalized": stip_norm,
                    "Work_Model": work_model,
                    "City": city,
                    "Clicks": 0
                })

                domain_counts[domain] = domain_counts.get(domain, 0) + 1
                scraper_accepted += 1

                if len(new_leads_to_insert) >= target_new_count:
                    break

            logger.info(f"    --> {scraper.name}: Scraped {len(raw_leads)}, Accepted {scraper_accepted} unique non-duplicate leads.")

        # Batch insert into database
        logger.info(f"[*] Inserting {len(new_leads_to_insert)} verified unique records into {self.target_table}...")
        cursor = conn.cursor()

        insert_sql = f"""
            INSERT INTO {self.target_table} (
                "Domain", "Company", "Role", "Location", "Is_Remote",
                "Start_Date", "End_Date", "Stipend", "URL", "Description",
                "Source", "Region", "Stipend_Normalized", "Work_Model", "City", "Clicks"
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        rows_tuples = [
            (
                d["Domain"], d["Company"], d["Role"], d["Location"], d["Is_Remote"],
                d["Start_Date"], d["End_Date"], d["Stipend"], d["URL"], d["Description"],
                d["Source"], d["Region"], d["Stipend_Normalized"], d["Work_Model"], d["City"], d["Clicks"]
            )
            for d in new_leads_to_insert
        ]

        # Chunked inserts of 500 for safety and transaction speed
        chunk_size = 500
        for i in range(0, len(rows_tuples), chunk_size):
            chunk = rows_tuples[i:i + chunk_size]
            cursor.executemany(insert_sql, chunk)
            conn.commit()

        # Final DB count
        cursor.execute(f"SELECT COUNT(*) FROM {self.target_table}")
        final_db_count = cursor.fetchone()[0]

        summary = {
            "target_table": self.target_table,
            "initial_db_count": initial_db_count,
            "total_scraped": total_scraped,
            "duplicates_filtered": total_duplicates_skipped,
            "new_inserted": len(new_leads_to_insert),
            "final_db_count": final_db_count,
            "domain_breakdown": domain_counts
        }

        logger.info("=" * 60)
        logger.info(f" SOURCING RUN COMPLETED FOR {self.target_table}")
        logger.info(f" Initial DB Count       : {initial_db_count}")
        logger.info(f" Total Leads Scraped    : {total_scraped}")
        logger.info(f" Duplicates Filtered    : {total_duplicates_skipped}")
        logger.info(f" Unique Leads Added     : {len(new_leads_to_insert)}")
        logger.info(f" Final DB Count         : {final_db_count}")
        logger.info(f" Domain Breakdown       : {domain_counts}")
        logger.info("=" * 60)

        return summary
