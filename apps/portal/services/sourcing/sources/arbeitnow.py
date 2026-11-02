"""
Arbeitnow API Scraper for Tech Jobs & Internships
"""

import logging
import requests
from typing import List, Dict, Any
from .base import BaseScraper
from ..normalizer import normalize_domain, clean_text

logger = logging.getLogger("sourcing.arbeitnow")

class ArbeitnowScraper(BaseScraper):
    name = "Arbeitnow API"
    region = "International"

    def fetch_leads(self, target_count: int = 1000) -> List[Dict[str, Any]]:
        leads: List[Dict[str, Any]] = []
        page = 1
        headers = {"User-Agent": "DBERT-LMS-CareerHub/1.0"}

        while len(leads) < target_count:
            url = f"https://www.arbeitnow.com/api/job-board-api?page={page}"
            try:
                res = requests.get(url, headers=headers, timeout=12)
                if res.status_code != 200:
                    break
                data = res.json()
                items = data.get("data", [])
                if not items:
                    break

                for item in items:
                    title = clean_text(item.get("title", ""))
                    desc = clean_text(item.get("description", ""))
                    if not title:
                        continue

                    domain = normalize_domain(title, desc)
                    company = clean_text(item.get("company_name", "Unknown"))
                    location = clean_text(item.get("location", "Global"))
                    is_remote = "Yes" if item.get("remote") else "No"
                    job_url = item.get("url", "")

                    leads.append({
                        "Domain": domain,
                        "Company": company,
                        "Role": title,
                        "Location": location,
                        "Is_Remote": is_remote,
                        "Start_Date": "Immediate",
                        "End_Date": "N/A",
                        "Stipend": "Competitive",
                        "URL": job_url,
                        "Description": desc[:500],
                        "Source": "Arbeitnow",
                        "Region": self.region
                    })

                    if len(leads) >= target_count:
                        break

                page += 1
                if page > 15: # safety cap
                    break
            except Exception as e:
                logger.warning(f"Error scraping Arbeitnow page {page}: {e}")
                break

        return leads
