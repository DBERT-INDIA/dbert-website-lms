import urllib.request
import urllib.parse
import json
import logging
import datetime
from typing import List, Optional
from scripts.scrapers.base import BaseJobScraper, ScrapedItem, normalize_domain, CANONICAL_DOMAINS

logger = logging.getLogger(__name__)

class InternationalRemoteScraper(BaseJobScraper):
    name = "InternationalRemote"

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    def scrape(self, domain: Optional[str] = None, post_type: str = "internship", limit: int = 40) -> List[ScrapedItem]:
        results: List[ScrapedItem] = []
        
        # 1. Remotive API
        remotive_items = self._scrape_remotive(domain, post_type, limit // 2)
        results.extend(remotive_items)

        # 2. Arbeitnow API
        if len(results) < limit:
            arbeitnow_items = self._scrape_arbeitnow(domain, post_type, limit - len(results))
            results.extend(arbeitnow_items)

        # 3. RemoteOK API
        if len(results) < limit:
            remoteok_items = self._scrape_remoteok(domain, post_type, limit - len(results))
            results.extend(remoteok_items)

        return results[:limit]

    def _scrape_remotive(self, domain: Optional[str], post_type: str, limit: int) -> List[ScrapedItem]:
        items: List[ScrapedItem] = []
        try:
            url = "https://remotive.com/api/remote-jobs?limit=100"
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                jobs = data.get("jobs", [])
                for job in jobs:
                    title = job.get("title", "")
                    raw_desc = job.get("description", "")
                    target_domain = normalize_domain(title, raw_desc)
                    if domain and target_domain != domain:
                        continue

                    company = job.get("company_name", "Global Tech Company")
                    loc = job.get("candidate_required_location") or "Worldwide / Remote"
                    salary = job.get("salary") or ("$1,500 - $3,500 / month" if post_type == "internship" else "$60k - $110k / year")
                    tags = ", ".join(job.get("tags") or [])
                    job_url = job.get("url")

                    today = datetime.date.today()
                    desc_html = f"""<div class="jd-section">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">About {company}</h3>
  <p><strong>{company}</strong> is a distributed remote-first engineering organization operating globally. They value async communication, clean code standards, and practical system development.</p>
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">About the Role</h3>
  <p>We are sourcing candidates for <strong>{title}</strong> within the {target_domain} domain. Candidate location: <strong>{loc}</strong>.</p>
  {raw_desc[:1200]}
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 10px 10px 0;">Required Technical Stack</h3>
  <p>{tags or 'Modern distributed frameworks, cloud services, and version control.'}</p>
</div>"""

                    item = ScrapedItem(
                        domain=target_domain,
                        company=company,
                        role=title,
                        location=loc,
                        is_remote=1,
                        work_model="Remote",
                        start_date=today.strftime("%Y-%m-%d"),
                        end_date=(today + datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
                        stipend=salary,
                        stipend_normalized="Paid",
                        url=job_url,
                        description=desc_html,
                        source="Remotive (Global)",
                        region="International",
                        city="Remote",
                        post_type=post_type,
                        skills=tags
                    )
                    items.append(item)
                    if len(items) >= limit:
                        break
        except Exception as e:
            logger.warning(f"Remotive scraping error: {e}")
        return items

    def _scrape_arbeitnow(self, domain: Optional[str], post_type: str, limit: int) -> List[ScrapedItem]:
        items: List[ScrapedItem] = []
        try:
            url = "https://www.arbeitnow.com/api/job-board-api"
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                jobs = data.get("data", [])
                for job in jobs:
                    title = job.get("title", "")
                    raw_desc = job.get("description", "")
                    target_domain = normalize_domain(title, raw_desc)
                    if domain and target_domain != domain:
                        continue

                    company = job.get("company_name", "European Tech Partner")
                    is_remote = 1 if job.get("remote") else 0
                    work_model = "Remote" if is_remote else "Hybrid"
                    loc = job.get("location") or ("Remote" if is_remote else "Berlin, Germany")
                    city = loc.split(",")[0].strip() if "," in loc else loc
                    tags = ", ".join(job.get("tags") or [])
                    job_url = job.get("url")

                    today = datetime.date.today()
                    desc_html = f"""<div class="jd-section">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">About {company}</h3>
  <p><strong>{company}</strong> develops scalable software and technological infrastructure across Europe and global hubs, welcoming agile engineering talent.</p>
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">About the Role</h3>
  <p>Seeking a dedicated <strong>{title}</strong> in the {target_domain} track. Model: <strong>{work_model}</strong> ({loc}).</p>
  {raw_desc[:1200]}
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 10px 10px 0;">Technologies & Tools</h3>
  <p>{tags or 'Modern toolchain and collaborative development.'}</p>
</div>"""

                    item = ScrapedItem(
                        domain=target_domain,
                        company=company,
                        role=title,
                        location=loc,
                        is_remote=is_remote,
                        work_model=work_model,
                        start_date=today.strftime("%Y-%m-%d"),
                        end_date=(today + datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
                        stipend="Competitive / Performance Stipend" if post_type == "internship" else "€45,000 - €75,000 / year",
                        stipend_normalized="Paid",
                        url=job_url,
                        description=desc_html,
                        source="Arbeitnow (EU)",
                        region="International",
                        city=city,
                        post_type=post_type,
                        skills=tags
                    )
                    items.append(item)
                    if len(items) >= limit:
                        break
        except Exception as e:
            logger.warning(f"Arbeitnow scraping error: {e}")
        return items

    def _scrape_remoteok(self, domain: Optional[str], post_type: str, limit: int) -> List[ScrapedItem]:
        items: List[ScrapedItem] = []
        try:
            url = "https://remoteok.com/api"
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                # first item is usually disclaimer
                jobs = data[1:] if isinstance(data, list) and len(data) > 1 else []
                for job in jobs:
                    title = job.get("position", "")
                    if not title:
                        continue
                    tags_list = job.get("tags") or []
                    tags_str = ", ".join(tags_list)
                    target_domain = normalize_domain(title, tags_str)
                    if domain and target_domain != domain:
                        continue

                    company = job.get("company", "Remote Leader")
                    loc = job.get("location") or "Global Remote"
                    sal_min = job.get("salary_min")
                    sal_max = job.get("salary_max")
                    if sal_min and sal_max and sal_min > 0:
                        salary = f"${int(sal_min):,} - ${int(sal_max):,} / year"
                    else:
                        salary = "$2,000 - $4,000 / month" if post_type == "internship" else "$55k - $95k / year"
                    
                    job_url = job.get("url") or f"https://remoteok.com/remote-jobs/{job.get('id')}"
                    today = datetime.date.today()

                    desc_html = f"""<div class="jd-section">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">About {company}</h3>
  <p><strong>{company}</strong> operates fully distributed remote teams delivering high-impact products across cloud, data, and user experience domains.</p>
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 0 10px;">Role Overview</h3>
  <p>Position: <strong>{title}</strong> in the {target_domain} domain. Candidate location: <strong>{loc}</strong>.</p>
</div>

<div class="jd-section" style="margin-top:20px;">
  <h3 style="font-size:16px;font-weight:800;color:#0F172A;margin:0 10px 10px 0;">Primary Skills</h3>
  <p>{tags_str or 'Modern cloud and engineering stack.'}</p>
</div>"""

                    item = ScrapedItem(
                        domain=target_domain,
                        company=company,
                        role=title,
                        location=loc,
                        is_remote=1,
                        work_model="Remote",
                        start_date=today.strftime("%Y-%m-%d"),
                        end_date=(today + datetime.timedelta(days=90)).strftime("%Y-%m-%d"),
                        stipend=salary,
                        stipend_normalized="Paid",
                        url=job_url,
                        description=desc_html,
                        source="RemoteOK (Global)",
                        region="International",
                        city="Remote",
                        post_type=post_type,
                        skills=tags_str
                    )
                    items.append(item)
                    if len(items) >= limit:
                        break
        except Exception as e:
            logger.warning(f"RemoteOK scraping error: {e}")
        return items
