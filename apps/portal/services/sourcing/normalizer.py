"""
DBERT LMS — Sourcing & Scraping Normalization Engine
Handles domain mapping, stipend normalization, work model classification,
city resolution, date cleansing, and cross-source deduplication hashing.
"""

import re
import datetime
from datetime import timedelta
from typing import Tuple, Optional

# The 9 Canonical DBERT LMS Career Tracks
CANONICAL_DOMAINS = [
    "AI Agent Development",
    "Data Analyst",
    "Full Stack Development",
    "Python Automation",
    "UI/UX Design",
    "DevOps & Cloud",
    "Mobile App Development",
    "Cybersecurity",
    "Digital Marketing",
]

def clean_text(text: Optional[str]) -> str:
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r"<[^>]+>", " ", text)
    # Strip excessive whitespace
    return " ".join(clean.split()).strip()

def normalize_domain(title: str, description: str = "") -> str:
    """Classifies a job role into one of DBERT's 9 core career tracks with high precision."""
    t = (title or "").lower().strip()
    d = (description or "").lower().strip()

    # 1. UI/UX Design (visual, figma, design, graphics, video editing)
    if any(k in t for k in [
        "ui/ux", "ui & ux", "ui and ux", "ux design", "ui design", "product design",
        "figma", "user experience", "user interface", "ux researcher", "interaction design",
        "graphic design", "graphic designer", "visual design", "visual designer", "motion graphic",
        "web design", "web designer", "illustrator", "creative design", "3d design", "animat",
        "video edit", "video creator", "video specialist", "design intern", "kreation/grafik"
    ]):
        return "UI/UX Design"

    # 2. Digital Marketing (SEO, social media, content writing, campaigns, ads, brand)
    if any(k in t for k in [
        "digital marketing", "marketing", "seo", "sem", "social media", "content writ",
        "copywrit", "growth market", "performance market", "meta ads", "google ads",
        "adwords", "brand market", "influencer", "email market", "lead generation",
        "market research", "creative writ", "pr & communication", "public relation",
        "growth & operations", "content creator", "content strategy", "brand & visual design",
        "social media automation", "marketing automation", "community promoter", "organic growth"
    ]):
        return "Digital Marketing"

    # 3. Mobile App Development (Flutter, React Native, Android, iOS, Swift, Kotlin)
    if any(k in t for k in [
        "mobile app", "mobile application", "android", "ios", "flutter", "react native",
        "swift", "kotlin", "mobile developer", "app developer", "mobile engineering"
    ]):
        return "Mobile App Development"

    # 4. Cybersecurity (Security, SOC, pen test, ethical hacking, infosec)
    if any(k in t for k in [
        "cybersecurity", "cyber security", "infosec", "information security", "soc analyst",
        "penetration", "pen test", "ethical hack", "vulnerability", "network security",
        "security analyst", "security engineer", "incident response", "security operations"
    ]):
        return "Cybersecurity"

    # 5. DevOps & Cloud (Docker, K8s, AWS, GCP, Azure, CI/CD, Terraform, SRE, SysAdmin)
    if any(k in t for k in [
        "devops", "cloud engineer", "cloud architect", "cloud computing", "aws", "azure", "gcp",
        "kubernetes", "k8s", "docker", "ci/cd", "terraform", "sre", "site reliability",
        "infrastructure engineer", "cloud infrastructure", "platform engineer", "system administrator",
        "sysadmin", "linux engineer", "network engineer", "systems engineer"
    ]):
        return "DevOps & Cloud"

    # 6. Data Analyst / Data Science (Analytics, BI, Tableau, SQL, data engineering)
    if any(k in t for k in [
        "data analyst", "data analytics", "business analyst", "bi analyst", "data science",
        "data scientist", "tableau", "power bi", "sql analyst", "data engineer", "data platform",
        "analytics intern", "data annotat", "data entry", "quantitative", "statistician"
    ]):
        return "Data Analyst"

    # 7. AI Agent Development (Generative AI, LLMs, Agents, ML, Computer Vision, Prompt)
    if any(k in t for k in [
        "ai agent", "artificial intelligence", "genai", "generative ai", "llm",
        "prompt engineer", "machine learning", "ml ", "ai/ml", "ai & ml", "deep learning",
        "nlp", "computer vision", "neural", "langchain", "llama", "rag", "pytorch",
        "hugging face", "reinforcement learning", "ai developer", "ai engineer", "ai research",
        "ai magician", "ai video", "ai tech trainer"
    ]):
        return "AI Agent Development"

    # 8. Python Automation (Automation, Selenium, Playwright, Scraping, RPA, SDET)
    if any(k in t for k in [
        "python", "automation", "rpa", "selenium", "playwright", "scraping",
        "crawler", "scripting", "bot developer", "qa automation", "sdet", "test automation"
    ]):
        return "Python Automation"

    # 9. Full Stack Development (Web, React, Node, Frontend, Backend, Software Engineer)
    if any(k in t for k in [
        "full stack", "fullstack", "web dev", "frontend", "front end", "backend", "back end",
        "react", "angular", "vue", "next.js", "node", "mern", "django", "flask", "fastapi",
        "software engineer", "software developer", "developer intern", "golang", "java", "php"
    ]):
        return "Full Stack Development"

    # Secondary fallback check in description
    if "figma" in d or "ui/ux" in d or "user experience" in d:
        return "UI/UX Design"
    if "marketing" in d or "seo" in d or "social media" in d:
        return "Digital Marketing"
    if "docker" in d or "kubernetes" in d or "devops" in d or "aws" in d:
        return "DevOps & Cloud"
    if "react native" in d or "flutter" in d or "mobile app" in d:
        return "Mobile App Development"
    if "cybersecurity" in d or "penetration testing" in d or "soc" in d:
        return "Cybersecurity"
    if "agent" in d or "llm" in d or "generative ai" in d:
        return "AI Agent Development"
    if "data analyst" in d or "business analytics" in d:
        return "Data Analyst"
    if "automation" in d or "python" in d:
        return "Python Automation"

    return "Full Stack Development"

def normalize_stipend(stipend_raw: Optional[str]) -> str:
    """Standardizes any raw currency / rate string into clean monthly INR bands."""
    if not stipend_raw or str(stipend_raw).strip().lower() in ["not disclosed", "nan", "none", "unknown", ""]:
        return "Not Disclosed"
    
    stip = str(stipend_raw).lower()
    if "unpaid" in stip or "free" in stip:
        return "Unpaid"

    is_hourly = any(h in stip for h in ["/hour", "/hr", "per hour", "hr", "hourly"])
    
    multiplier = 1.0
    if "$" in stip or "usd" in stip:
        multiplier = 84.0
    elif "€" in stip or "eur" in stip:
        multiplier = 90.0
    elif "£" in stip or "gbp" in stip:
        multiplier = 108.0

    # Extract numbers (supporting 'k' suffix e.g. 15k)
    clean_nums = stip.replace(",", "")
    matches = re.findall(r"[\d\.]+(?:k)?", clean_nums)
    nums = []
    for m in matches:
        try:
            if m.endswith("k"):
                nums.append(float(m[:-1]) * 1000)
            else:
                nums.append(float(m))
        except ValueError:
            continue

    if not nums:
        return "Not Disclosed"

    inr_vals = []
    for n in nums:
        val = n * multiplier
        if is_hourly:
            val = val * 160  # 160 working hours/month
        elif val > 10000000:  # > 1 crore is yearly CTC
            val = val / 12
        elif val > 1200000 and multiplier > 1:  # > $15k USD is yearly
            val = val / 12
        inr_vals.append(val)

    avg = sum(inr_vals) / len(inr_vals)

    if avg < 10000:
        return "< ₹10,000 /month"
    elif avg <= 30000:
        return "₹10,000 - ₹30,000 /month"
    elif avg <= 50000:
        return "₹30,000 - ₹50,000 /month"
    elif avg <= 100000:
        return "₹50,000 - ₹1,00,000 /month"
    else:
        return "> ₹1,00,000 /month"

def normalize_work_model(location: Optional[str], is_remote: Optional[str] = None) -> Tuple[str, str]:
    """Resolves Work_Model (Remote, Hybrid, Onsite) and canonical City name."""
    loc = (location or "").strip()
    loc_lower = loc.lower()
    rem = (is_remote or "").strip().lower()

    if "hybrid" in loc_lower:
        work_model = "Hybrid"
    elif "remote" in loc_lower or "work from home" in loc_lower or rem in ["yes", "true", "1", "remote"]:
        work_model = "Remote"
    else:
        work_model = "Onsite"

    city = "Remote" if work_model == "Remote" else "Unknown"
    if work_model != "Remote" and loc:
        parts = loc.split(",")
        if parts:
            raw_city = parts[0].strip()
            # Clean common fluff
            clean_city = re.sub(r"(?i)\b(greater|area|metropolitan|city|region|district|cyber)\b", "", raw_city).strip()
            city = clean_city.title() if clean_city else "Unknown"

    return work_model, city

def normalize_dates(start_date: Optional[str], end_date: Optional[str]) -> Tuple[str, str]:
    """Ensures standard YYYY-MM-DD dates."""
    today = datetime.datetime.now()
    default_start = today.strftime("%Y-%m-%d")
    default_end = (today + timedelta(days=90)).strftime("%Y-%m-%d")

    s = default_start
    if start_date and str(start_date).strip().lower() not in ["immediate", "nan", "none", "unknown", ""]:
        try:
            s = str(start_date)[:10]
        except Exception:
            s = default_start

    e = default_end
    if end_date and str(end_date).strip().lower() not in ["n/a", "unknown", "nan", "none", ""]:
        try:
            e = str(end_date)[:10]
        except Exception:
            e = default_end

    return s, e

def make_dedup_hash(company: str, role: str, url: str = "") -> Tuple[str, str]:
    """
    Builds canonical deduplication tokens:
    1. content_key: normalized (company + role)
    2. url_key: normalized URL without query params/utm
    """
    comp_norm = re.sub(r"[^a-z0-9]", "", (company or "").lower())
    # Strip common suffixes in role like ' - Internshala', ' | LinkedIn'
    role_clean = re.sub(r"(?i)\s*(-|\|)\s*(internshala|linkedin|indeed|unstop|glassdoor|remotive|arbeitnow).*", "", role or "")
    role_norm = re.sub(r"[^a-z0-9]", "", role_clean.lower())
    
    content_key = f"{comp_norm}:{role_norm}"
    
    # Strip UTM parameters from URL
    url_clean = (url or "").split("?")[0].rstrip("/").lower()
    
    return content_key, url_clean
