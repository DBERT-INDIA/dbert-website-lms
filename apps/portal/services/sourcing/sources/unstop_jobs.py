"""
Unstop API Scraper for Graduate & Lateral Tech Jobs in India
"""

import logging
import requests
import time
from typing import List, Dict, Any
from .base import BaseScraper
from ..normalizer import normalize_domain, clean_text

logger = logging.getLogger("sourcing.unstop_jobs")

JOB_KEYWORDS = [
    # AI Agent Track
    "ai engineer", "machine learning engineer", "generative ai developer", "data scientist", "nlp engineer",
    # Python Track
    "python developer", "automation engineer", "qa automation", "backend python", "sdet",
    # Data Analyst Track
    "data analyst", "business analyst", "data analytics", "power bi developer", "sql analyst",
    # Full Stack Track
    "software engineer", "full stack developer", "frontend developer", "backend developer", "react developer", "node developer"
]

class UnstopJobsScraper(BaseScraper):
    name = "Unstop Jobs"
    region = "India"

    def fetch_leads(self, target_count: int = 1500) -> List[Dict[str, Any]]:
        leads: List[Dict[str, Any]] = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }

        for keyword in JOB_KEYWORDS:
            if len(leads) >= target_count:
                break
            
            for page in range(1, 10):
                url = f"https://unstop.com/api/public/opportunity/search-result?opportunity=jobs&keyword={keyword}&page={page}&per_page=40"
                try:
                    res = requests.get(url, headers=headers, timeout=10)
                    if res.status_code != 200:
                        break
                    
                    data_obj = res.json().get("data", {})
                    items = data_obj.get("data", []) if isinstance(data_obj, dict) else []
                    if not items:
                        break

                    for item in items:
                        if not isinstance(item, dict):
                            continue

                        title = clean_text(item.get("title", ""))
                        if not title:
                            continue

                        org = item.get("organisation", {})
                        company = clean_text(org.get("name", "Unknown")) if isinstance(org, dict) else "Unknown"

                        desc = clean_text(item.get("description", "") or item.get("banner_mobile", ""))
                        if not desc:
                            desc = f"{title} job opportunity at {company}."

                        domain = normalize_domain(title, desc)

                        job_detail = item.get("jobDetail") or {}
                        j_type = str(job_detail.get("type", "") if isinstance(job_detail, dict) else "").lower()
                        loc_type = str(item.get("job_type", "")).lower()

                        loc_list = []
                        raw_locs = item.get("locations", [])
                        if isinstance(raw_locs, list):
                            for loc in raw_locs:
                                if isinstance(loc, dict):
                                    city_name = loc.get("city") or loc.get("location") or loc.get("name")
                                    if city_name:
                                        loc_list.append(str(city_name))
                                elif isinstance(loc, str):
                                    loc_list.append(loc)

                        is_remote = "No"
                        if "wfh" in j_type or "remote" in j_type or "wfh" in loc_type or "remote" in loc_type:
                            is_remote = "Yes"
                            location = "Remote"
                        elif loc_list:
                            location = ", ".join(loc_list)
                            if any("remote" in l.lower() for l in loc_list):
                                is_remote = "Yes"
                        else:
                            location = "India"

                        stipend = "Competitive"
                        if isinstance(job_detail, dict):
                            s_min = job_detail.get("min_salary")
                            s_max = job_detail.get("max_salary")
                            if s_min or s_max:
                                stipend = f"₹{s_min or ''} - ₹{s_max or ''} /year"

                        seo_url = item.get("seo_url", "")
                        job_url = f"https://unstop.com/jobs/{seo_url}" if seo_url else f"https://unstop.com/opportunity/{item.get('id', '')}"

                        leads.append({
                            "Domain": domain,
                            "Company": company,
                            "Role": title,
                            "Location": location,
                            "Is_Remote": is_remote,
                            "Start_Date": item.get("start_date", "Immediate") or "Immediate",
                            "End_Date": item.get("end_date", "N/A") or "N/A",
                            "Stipend": stipend,
                            "URL": job_url,
                            "Description": desc[:500],
                            "Source": "Unstop Jobs",
                            "Region": self.region
                        })

                        if len(leads) >= target_count:
                            break
                    time.sleep(0.3)
                except Exception as e:
                    logger.warning(f"Unstop Jobs error on '{keyword}' page {page}: {e}")
                    break

        return leads
