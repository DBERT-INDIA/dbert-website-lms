"""
Web Search & Public Portal Aggregator (DuckDuckGo, LinkedIn, Indeed, Internshala)
"""

import logging
import time
import re
from typing import List, Dict, Any
from .base import BaseScraper
from ..normalizer import normalize_domain, clean_text

logger = logging.getLogger("sourcing.web_aggregator")

class WebAggregatorScraper(BaseScraper):
    name = "Web Aggregator"
    region = "India"

    def fetch_leads(self, target_count: int = 1000) -> List[Dict[str, Any]]:
        leads: List[Dict[str, Any]] = []

        try:
            from duckduckgo_search import DDGS
        except ImportError:
            logger.warning("duckduckgo_search not installed, skipping aggregator")
            return leads

        queries = [
            # AI Agent Development
            ("AI Agent Development", "site:internshala.com \"AI\" internship 2026"),
            ("AI Agent Development", "site:linkedin.com/jobs \"Artificial Intelligence Intern\" India"),
            ("AI Agent Development", "site:wellfound.com \"AI Agent\" internship"),
            ("AI Agent Development", "site:indeed.com \"Machine Learning Intern\" India"),
            # Python Automation
            ("Python Automation", "site:internshala.com \"Python\" internship 2026"),
            ("Python Automation", "site:linkedin.com/jobs \"Python Intern\" India"),
            ("Python Automation", "site:indeed.com \"Automation Intern\" Python India"),
            # Data Analyst
            ("Data Analyst", "site:internshala.com \"Data Analyst\" internship 2026"),
            ("Data Analyst", "site:linkedin.com/jobs \"Data Analytics Intern\" India"),
            ("Data Analyst", "site:indeed.com \"Business Analyst Intern\" India"),
            # Full Stack Development
            ("Full Stack Development", "site:internshala.com \"Full Stack\" internship 2026"),
            ("Full Stack Development", "site:linkedin.com/jobs \"Full Stack Developer Intern\" India"),
            ("Full Stack Development", "site:indeed.com \"Web Development Intern\" India"),
            # UI/UX Design
            ("UI/UX Design", "site:internshala.com \"UI/UX\" internship 2026"),
            ("UI/UX Design", "site:linkedin.com/jobs \"UI UX Design Intern\" India"),
            # DevOps & Cloud
            ("DevOps & Cloud", "site:internshala.com \"DevOps\" internship 2026"),
            ("DevOps & Cloud", "site:linkedin.com/jobs \"Cloud DevOps Intern\" India"),
            # Mobile App Development
            ("Mobile App Development", "site:internshala.com \"Mobile App\" internship 2026"),
            ("Mobile App Development", "site:linkedin.com/jobs \"Flutter React Native Intern\" India"),
            # Cybersecurity
            ("Cybersecurity", "site:internshala.com \"Cybersecurity\" internship 2026"),
            ("Cybersecurity", "site:linkedin.com/jobs \"Cyber Security Intern\" India"),
            # Digital Marketing
            ("Digital Marketing", "site:internshala.com \"Digital Marketing\" internship 2026"),
            ("Digital Marketing", "site:linkedin.com/jobs \"Growth Marketing SEO Intern\" India")
        ]

        with DDGS() as ddgs:
            for domain_hint, q in queries:
                if len(leads) >= target_count:
                    break
                try:
                    results = ddgs.text(q, max_results=60)
                    for r in results:
                        title = clean_text(r.get("title", ""))
                        body = clean_text(r.get("body", ""))
                        href = r.get("href", "")
                        if not title or not href:
                            continue

                        # Extract company name from title
                        comp = "Tech Enterprise"
                        comp_match = re.search(r"(?i)\bat\s+([A-Za-z0-9\s\.\&]+?)(?:\s*\||\s*-|\s*in\b|\s*\(|$)", title)
                        if comp_match:
                            c_cand = comp_match.group(1).strip()
                            if len(c_cand) > 1 and len(c_cand) < 40:
                                comp = c_cand

                        # Strip portal names from title
                        role_clean = re.sub(r"(?i)\s*(-|\|)\s*(internshala|linkedin|indeed|wellfound|glassdoor).*", "", title).strip()

                        domain = normalize_domain(role_clean, body) or domain_hint

                        is_remote = "Yes" if any(w in (title + body).lower() for w in ["remote", "work from home", "wfh"]) else "No"
                        location = "Remote" if is_remote == "Yes" else "India"

                        source_name = "Web"
                        if "internshala.com" in href:
                            source_name = "Internshala"
                        elif "linkedin.com" in href:
                            source_name = "LinkedIn"
                        elif "indeed.com" in href:
                            source_name = "Indeed"
                        elif "wellfound.com" in href:
                            source_name = "Wellfound"

                        leads.append({
                            "Domain": domain,
                            "Company": comp,
                            "Role": role_clean,
                            "Location": location,
                            "Is_Remote": is_remote,
                            "Start_Date": "Immediate",
                            "End_Date": "N/A",
                            "Stipend": "Competitive",
                            "URL": href,
                            "Description": body[:500],
                            "Source": source_name,
                            "Region": "India" if "india" in href.lower() or "internshala" in href.lower() else "International"
                        })

                        if len(leads) >= target_count:
                            break
                    time.sleep(1.5)
                except Exception as e:
                    logger.warning(f"Error on DDG search '{q}': {e}")
                    time.sleep(2)

        return leads
