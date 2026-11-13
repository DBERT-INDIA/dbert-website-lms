import re
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

CANONICAL_DOMAINS = [
    "AI Agent Development",
    "Cybersecurity",
    "Data Analyst",
    "DevOps & Cloud",
    "Digital Marketing",
    "Full Stack Development",
    "Mobile App Development",
    "Python Automation",
    "UI/UX Design"
]

DOMAIN_KEYWORDS = {
    "AI Agent Development": [
        "ai agent", "artificial intelligence", "generative ai", "genai", "llm", "deep learning", 
        "machine learning", "nlp", "computer vision", "langchain", "prompt engineer", "ai engineer"
    ],
    "Cybersecurity": [
        "cybersecurity", "cyber security", "infosec", "information security", "soc analyst", 
        "penetration test", "ethical hacker", "network security", "vulnerability", "threat analyst"
    ],
    "Data Analyst": [
        "data analyst", "data analytics", "data science", "data engineer", "business analyst", 
        "bi analyst", "power bi", "tableau", "sql analyst", "data modeling", "pandas", "data visualization"
    ],
    "DevOps & Cloud": [
        "devops", "cloud engineer", "aws", "azure", "gcp", "kubernetes", "docker", "ci/cd", 
        "sre", "site reliability", "terraform", "infrastructure", "ansible"
    ],
    "Digital Marketing": [
        "digital marketing", "seo", "sem", "content marketing", "social media", "growth marketing", 
        "performance marketing", "email marketing", "copywriter", "marketing analyst"
    ],
    "Full Stack Development": [
        "full stack", "fullstack", "web development", "backend", "frontend", "react", "next.js", 
        "node.js", "django", "flask", "software engineer", "software developer", "javascript developer"
    ],
    "Mobile App Development": [
        "mobile app", "android", "ios", "flutter", "react native", "swift", "kotlin", 
        "mobile developer", "app developer"
    ],
    "Python Automation": [
        "python automation", "python developer", "rpa", "automation engineer", "playwright", 
        "selenium", "qa automation", "scripting", "bot developer", "web scraping"
    ],
    "UI/UX Design": [
        "ui/ux", "ui designer", "ux designer", "product designer", "figma", "user experience", 
        "user interface", "wireframe", "graphic design", "visual designer"
    ]
}

def normalize_domain(title: str, description: str = "") -> str:
    """Classifies any role title and description into one of the 9 canonical domains."""
    comb = f"{title.lower()} {description.lower()}"
    
    # Priority matching
    scores = {}
    for domain, kw_list in DOMAIN_KEYWORDS.items():
        score = 0
        for kw in kw_list:
            if kw in title.lower():
                score += 5  # High weight if in title
            elif kw in comb:
                score += 1
        if score > 0:
            scores[domain] = score

    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]

    return "Full Stack Development"  # Default fallback

def slugify(text: str) -> str:
    """Generates an SEO-safe URL slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")

def generate_fingerprint(company: str, role: str, domain: str, work_model: str = "") -> str:
    """Calculates SHA-256 composite fingerprint for zero-duplicate idempotency."""
    c = slugify(company)
    r = slugify(role)
    d = slugify(domain)
    w = slugify(work_model or "remote")
    raw = f"{c}::{r}::{d}::{w}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

@dataclass
class ScrapedItem:
    domain: str
    company: str
    role: str
    location: str
    is_remote: int
    work_model: str
    start_date: str
    end_date: str
    stipend: str
    stipend_normalized: str
    url: str
    description: str
    source: str
    region: str
    city: str
    post_type: str = "internship"  # 'internship' or 'job'
    skills: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @property
    def fingerprint(self) -> str:
        return generate_fingerprint(self.company, self.role, self.domain, self.work_model)

    @property
    def company_slug(self) -> str:
        return slugify(self.company)

    @property
    def role_slug(self) -> str:
        return f"{slugify(self.role)}-at-{slugify(self.company)}"

class BaseJobScraper:
    """Abstract base class for all job and internship sourcing adapters."""
    name: str = "BaseScraper"

    def scrape(self, domain: Optional[str] = None, post_type: str = "internship", limit: int = 20) -> List[ScrapedItem]:
        raise NotImplementedError("Scrapers must implement scrape()")
