"""
DBERT LMS — Sourcing & Scraping Normalization Engine
Handles domain mapping, stipend normalization, work model classification,
city resolution, date cleansing, and cross-source deduplication hashing.
"""

import re
import datetime
from datetime import timedelta
from typing import Tuple, Optional

# The 4 Canonical DBERT LMS Career Tracks
CANONICAL_DOMAINS = [
    "AI Agent Development",
    "Data Analyst",
    "Full Stack Development",
    "Python Automation"
]

def clean_text(text: Optional[str]) -> str:
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r"<[^>]+>", " ", text)
    # Strip excessive whitespace
    return " ".join(clean.split()).strip()

def normalize_domain(title: str, description: str = "") -> str:
    """Classifies a job role into one of DBERT's 4 core career tracks."""
    t = (title or "").lower()
    d = (description or "").lower()
    combined = f"{t} {d}"

    # 1. AI Agent Development (Generative AI, LLMs, LangChain, Agents, Machine Learning, Deep Learning)
    if any(k in t for k in [
        "ai ", "artificial intelligence", "genai", "generative ai", "agent", "llm", "prompt",
        "machine learning", "ml ", "deep learning", "nlp", "computer vision", "neural",
        "langchain", "llama", "rag", "pytorch", "hugging face"
    ]):
        return "AI Agent Development"

    # 2. Python Automation (Python dev, automation, scripts, scraping, QA, testing, RPA)
    if any(k in t for k in [
        "python", "automation", "rpa", "selenium", "playwright", "scraping",
        "crawler", "scripting", "bot", "qa automation", "sdet", "airflow"
    ]):
        return "Python Automation"

    # 3. Data Analyst (Data science, analytics, BI, Tableau, SQL, data engineer)
    if any(k in t for k in [
        "data analyst", "data analytics", "business analyst", "data science",
        "data engineer", "bi analyst", "tableau", "power bi", "analytics intern", "sql analyst"
    ]):
        return "Data Analyst"

    # 4. Full Stack Development (Web, React, Node, Next.js, Django, Frontend, Backend, Software Engineer)
    if any(k in t for k in [
        "full stack", "fullstack", "web dev", "frontend", "front end", "backend", "back end",
        "react", "angular", "vue", "next.js", "node", "mern", "django", "flask", "fastapi",
        "software engineer", "software developer", "developer intern"
    ]):
        return "Full Stack Development"

    # Secondary fallback check in description
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
