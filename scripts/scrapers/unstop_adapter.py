import urllib.request
import urllib.parse
import json
import logging
import datetime
from typing import List, Optional
from scripts.scrapers.base import BaseJobScraper, ScrapedItem, normalize_domain, CANONICAL_DOMAINS

logger = logging.getLogger(__name__)

class UnstopScraper(BaseJobScraper):
    name = "Unstop"

    def __init__(self):
        self.base_url = "https://unstop.com/api/public/opportunity/search-result"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }

    def scrape(self, domain: Optional[str] = None, post_type: str = "internship", limit: int = 30) -> List[ScrapedItem]:
        opp_type = "internships" if post_type == "internship" else "jobs"
        results: List[ScrapedItem] = []
        
        # Paginate through results
        page = 1
        max_pages = max(1, (limit // 25) + 2)
        
        while len(results) < limit and page <= max_pages:
            params = {
                "opportunity": opp_type,
                "per_page": 25,
                "page": page
            }
            if domain:
                # Add domain search query to parameter if specific domain requested
                params["search"] = domain

            url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
            try:
                req = urllib.request.Request(url, headers=self.headers)
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    opps = data.get("data", {}).get("data", [])
                    if not opps:
                        break

                    for opp in opps:
                        item = self._parse_opportunity(opp, post_type)
                        if item:
                            if domain and item.domain != domain:
                                continue
                            results.append(item)
                            if len(results) >= limit:
                                break
                    page += 1
            except Exception as e:
                logger.warning(f"UnstopScraper error on page {page}: {e}")
                break

        return results

    def _parse_opportunity(self, opp: dict, post_type: str) -> Optional[ScrapedItem]:
        try:
            title = opp.get("title", "").strip()
            if not title:
                return None

            org_info = opp.get("organisation") or {}
            company = org_info.get("name", "Corporate Partner").strip()
            
            raw_details = opp.get("details", "") or ""
            target_domain = normalize_domain(title, raw_details)
            
            # Location & Work Model
            loc_list = opp.get("locations") or []
            city = "Remote"
            location = "Pan India"
            is_remote_val = 0
            work_model = "Onsite"
            
            job_detail = opp.get("jobDetail") or {}
            mode_type = job_detail.get("type", "").lower()
            if "virtual" in mode_type or "remote" in mode_type or "work from home" in mode_type:
                work_model = "Remote"
                is_remote_val = 1
                city = "Remote"
                location = "Remote"
            elif loc_list:
                first_loc = loc_list[0]
                city = first_loc.get("city") or "Bangalore"
                state = first_loc.get("state") or ""
                country = first_loc.get("country") or "India"
                location = f"{city}, {state}" if state else city
                work_model = "Onsite"

            # Stipend
            stipend_raw = "Competitive"
            stipend_norm = "Paid"
            min_sal = job_detail.get("min_salary")
            max_sal = job_detail.get("max_salary")
            if min_sal and max_sal:
                stipend_raw = f"₹{int(min_sal):,} - ₹{int(max_sal):,} / month"
            elif min_sal:
                stipend_raw = f"₹{int(min_sal):,} / month"
            elif opp.get("isPaid") is False or job_detail.get("paid_unpaid") == "unpaid":
                stipend_raw = "Unpaid / Performance Incentive"
                stipend_norm = "Unpaid"
            else:
                stipend_raw = "₹15,000 - ₹25,000 / month" if post_type == "internship" else "₹4.5 - ₹8.0 LPA"

            # Dates
            today = datetime.date.today()
            start_date = today.strftime("%Y-%m-%d")
            end_date = (today + datetime.timedelta(days=90)).strftime("%Y-%m-%d")
            
            # Skills
            req_skills = opp.get("required_skills") or []
            if isinstance(req_skills, list):
                skill_names = [s.get("name") if isinstance(s, dict) else str(s) for s in req_skills]
                skills_str = ", ".join(filter(None, skill_names))
            else:
                skills_str = str(req_skills)
            
            url = opp.get("seo_url") or opp.get("public_url") or f"https://unstop.com/o/{opp.get('id')}"
            if not url.startswith("http"):
                url = f"https://unstop.com/{url.lstrip('/')}"

            # Format standardized HTML description matching DBERT post styling
            description_html = f"""<div class="jd-section">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">About {company}</h3>
  <p><strong>{company}</strong> is partnering with high-velocity hiring teams across India. Selected candidates collaborate on engineering and delivery sprints, gaining hands-on exposure to production systems and mentored workflows.</p>
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">About the Role</h3>
  <p>We are seeking a proactive <strong>{title}</strong> to join the {target_domain} team. Structured as a <strong>{work_model}</strong> engagement based out of <strong>{location}</strong>.</p>
  {raw_details}
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 10px 10px 0;">Key Skills & Technologies</h3>
  <p>{skills_str or 'Relevant domain tools and software practices.'}</p>
</div>"""

            return ScrapedItem(
                domain=target_domain,
                company=company,
                role=title,
                location=location,
                is_remote=is_remote_val,
                work_model=work_model,
                start_date=start_date,
                end_date=end_date,
                stipend=stipend_raw,
                stipend_normalized=stipend_norm,
                url=url,
                description=description_html,
                source="Unstop",
                region="India",
                city=city,
                post_type=post_type,
                skills=skills_str
            )
        except Exception as e:
            logger.debug(f"Failed parsing Unstop opportunity: {e}")
            return None
