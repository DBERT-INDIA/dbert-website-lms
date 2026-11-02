"""
Remotive, Jobicy & RemoteOK API Scrapers for Global Tech Roles
"""

import logging
import requests
from typing import List, Dict, Any
from .base import BaseScraper
from ..normalizer import normalize_domain, clean_text

logger = logging.getLogger("sourcing.global_apis")

class GlobalApisScraper(BaseScraper):
    name = "Global Remote APIs"
    region = "International"

    def fetch_leads(self, target_count: int = 1000) -> List[Dict[str, Any]]:
        leads: List[Dict[str, Any]] = []

        # 1. Remotive API
        try:
            url = "https://remotive.com/api/remote-jobs?limit=500"
            res = requests.get(url, headers={"User-Agent": "DBERT-LMS/1.0"}, timeout=15)
            if res.status_code == 200:
                jobs = res.json().get("jobs", [])
                for j in jobs:
                    title = clean_text(j.get("title", ""))
                    desc = clean_text(j.get("description", ""))
                    if not title:
                        continue
                    domain = normalize_domain(title, desc)
                    company = clean_text(j.get("company_name", "Tech Startup"))
                    salary = clean_text(j.get("salary", "Competitive"))

                    leads.append({
                        "Domain": domain,
                        "Company": company,
                        "Role": title,
                        "Location": clean_text(j.get("candidate_required_location", "Remote Worldwide")),
                        "Is_Remote": "Yes",
                        "Start_Date": "Immediate",
                        "End_Date": "N/A",
                        "Stipend": salary or "Competitive",
                        "URL": j.get("url", ""),
                        "Description": desc[:500],
                        "Source": "Remotive",
                        "Region": self.region
                    })
                    if len(leads) >= target_count:
                        return leads
        except Exception as e:
            logger.warning(f"Remotive API error: {e}")

        # 2. Jobicy API
        try:
            url = "https://jobicy.com/api/v2/remote-jobs?count=100"
            res = requests.get(url, headers={"User-Agent": "DBERT-LMS/1.0"}, timeout=15)
            if res.status_code == 200:
                jobs = res.json().get("jobs", [])
                for j in jobs:
                    title = clean_text(j.get("jobTitle", ""))
                    desc = clean_text(j.get("jobDescription", ""))
                    if not title:
                        continue
                    domain = normalize_domain(title, desc)
                    company = clean_text(j.get("companyName", "Unknown"))

                    leads.append({
                        "Domain": domain,
                        "Company": company,
                        "Role": title,
                        "Location": clean_text(j.get("jobGeo", "Remote")),
                        "Is_Remote": "Yes",
                        "Start_Date": "Immediate",
                        "End_Date": "N/A",
                        "Stipend": "Competitive",
                        "URL": j.get("url", ""),
                        "Description": desc[:500],
                        "Source": "Jobicy",
                        "Region": self.region
                    })
                    if len(leads) >= target_count:
                        return leads
        except Exception as e:
            logger.warning(f"Jobicy API error: {e}")

        # 3. RemoteOK API
        try:
            url = "https://remoteok.com/api"
            res = requests.get(url, headers={"User-Agent": "DBERT-LMS/1.0"}, timeout=15)
            if res.status_code == 200:
                data = res.json()
                for j in data:
                    if not isinstance(j, dict):
                        continue
                    title = clean_text(j.get("position", ""))
                    desc = clean_text(j.get("description", ""))
                    if not title:
                        continue
                    domain = normalize_domain(title, desc)
                    company = clean_text(j.get("company", "Remote Tech"))

                    leads.append({
                        "Domain": domain,
                        "Company": company,
                        "Role": title,
                        "Location": clean_text(j.get("location", "Remote")),
                        "Is_Remote": "Yes",
                        "Start_Date": "Immediate",
                        "End_Date": "N/A",
                        "Stipend": "Competitive",
                        "URL": j.get("url", ""),
                        "Description": desc[:500],
                        "Source": "RemoteOK",
                        "Region": self.region
                    })
                    if len(leads) >= target_count:
                        return leads
        except Exception as e:
            logger.warning(f"RemoteOK API error: {e}")

        return leads
