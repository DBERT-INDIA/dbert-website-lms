"""
services/ai/ats_engine.py - High-Performance AI Resume & ATS Screening Engine
Provides dual-mode evaluation:
1. Deep semantic review & rewrite suggestions via Gemini API
2. Deterministic keyword, metric density, and structure scoring fallback
Safe, quota-resilient, and non-blocking.
"""

import os
import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("ats_engine")

# ── DOMAIN KEYWORD REGISTRIES ────────────────────────────────────────────────
DOMAIN_KEYWORDS: Dict[str, Dict[str, Any]] = {
    "Full Stack Development": {
        "slug": "full-stack-development",
        "primary": ["React", "Next.js", "Node.js", "TypeScript", "JavaScript", "HTML5", "CSS3", "REST API", "PostgreSQL", "SQL"],
        "advanced": ["Docker", "GraphQL", "Redis", "Tailwind CSS", "Microservices", "Jest", "CI/CD", "AWS", "Git", "MongoDB", "Prisma"],
        "critical_check": ["Git", "SQL", "REST API", "React", "TypeScript", "Docker"],
        "default_missing": ["Docker containerization", "TypeScript type-safety", "PostgreSQL indexing & query tuning", "Automated unit testing (Jest/Cypress)", "CI/CD GitHub Actions pipelines"]
    },
    "AI Agent Development": {
        "slug": "ai-agent-development",
        "primary": ["Python", "Large Language Models", "LLM", "Prompt Engineering", "LangChain", "Vector Database", "RAG", "Embeddings", "FastAPI"],
        "advanced": ["CrewAI", "LlamaIndex", "ChromaDB", "pgvector", "Fine-Tuning", "ReAct Framework", "Function Calling", "Tool Calling", "Hugging Face", "PyTorch"],
        "critical_check": ["Python", "LangChain", "RAG", "Vector Database", "FastAPI", "Prompt Engineering"],
        "default_missing": ["pgvector / ChromaDB hybrid search", "Function & Tool-calling agent architectures", "Latency benchmarking & token streaming", "Guardrails & hallucination mitigation", "Production RAG evaluation (Ragas)"]
    },
    "Data Analyst": {
        "slug": "data-analytics",
        "primary": ["SQL", "Python", "Pandas", "NumPy", "Excel", "Data Cleaning", "Data Visualization", "Tableau", "Power BI", "Statistics"],
        "advanced": ["PostgreSQL", "Data Warehousing", "ETL", "A/B Testing", "Time Series", "EDA", "Matplotlib", "Seaborn", "Metabase"],
        "critical_check": ["SQL", "Python", "Pandas", "Power BI", "Data Visualization", "Statistics"],
        "default_missing": ["Advanced SQL (Window functions & CTEs)", "Variance & driver decomposition", "Automated ETL pipeline scheduling", "Interactive executive dashboard design", "Statistical hypothesis testing"]
    },
    "Python Automation": {
        "slug": "python-automation",
        "primary": ["Python", "Selenium", "Playwright", "Web Scraping", "BeautifulSoup", "Automation Scripts", "Requests", "Regex", "Task Scheduling"],
        "advanced": ["Celery", "Redis", "Cron", "Headless Browsers", "REST APIs", "Error Handling", "Logging", "PyTest", "FastAPI"],
        "critical_check": ["Python", "Automation Scripts", "Web Scraping", "Regex", "Selenium", "Requests"],
        "default_missing": ["Playwright headless browser automation", "Resilient exponential backoff & rate-limiting", "Distributed task execution with Celery", "Structured logging & alerting pipelines", "Automated unit test coverage"]
    },
    "DevOps & Cloud": {
        "slug": "devops-cloud",
        "primary": ["Linux", "Docker", "Kubernetes", "AWS", "CI/CD", "GitHub Actions", "Bash", "Terraform", "Git", "Nginx"],
        "advanced": ["Ansible", "Prometheus", "Grafana", "CloudWatch", "Helm", "Infrastructure as Code", "SSL/TLS", "Microservices"],
        "critical_check": ["Docker", "Kubernetes", "AWS", "CI/CD", "Linux", "Terraform"],
        "default_missing": ["Terraform Infrastructure as Code (IaC)", "Kubernetes Helm charts & ingress controllers", "Prometheus & Grafana observability", "Zero-downtime rolling deployment strategies", "Cloud security IAM hardening"]
    },
    "Cybersecurity": {
        "slug": "cybersecurity",
        "primary": ["Network Security", "Vulnerability Assessment", "Penetration Testing", "Burp Suite", "OWASP Top 10", "Linux", "Wireshark", "Cryptography"],
        "advanced": ["SIEM", "Splunk", "SOC Operations", "Threat Intelligence", "Incident Response", "Firewalls", "Python Scripting", "Metasploit"],
        "critical_check": ["OWASP Top 10", "Penetration Testing", "Burp Suite", "Linux", "Network Security", "Vulnerability Assessment"],
        "default_missing": ["OWASP Top 10 web exploitation methodology", "SIEM log correlation & incident response", "Automated vulnerability scanning & remediation", "Burp Suite API security testing", "Zero Trust network architecture"]
    },
    "UI/UX Design": {
        "slug": "ui-ux-design",
        "primary": ["Figma", "UI Design", "UX Research", "Wireframing", "Prototyping", "Design Systems", "User Flows", "Information Architecture"],
        "advanced": ["Auto Layout", "Component Variants", "Design Tokens", "WCAG Accessibility", "Usability Testing", "Micro-Interactions", "Responsive Design"],
        "critical_check": ["Figma", "Wireframing", "Prototyping", "Design Systems", "UX Research", "Auto Layout"],
        "default_missing": ["WCAG 2.1 AA accessibility contrast auditing", "Figma auto-layout & tokenized component libraries", "Interactive prototype micro-animations", "User testing synthesis & heatmaps", "Developer handoff documentation"]
    },
    "Mobile App Development": {
        "slug": "mobile-app-development",
        "primary": ["React Native", "Flutter", "Dart", "Android", "iOS", "JavaScript", "TypeScript", "Mobile UI", "REST APIs", "Git"],
        "advanced": ["Redux", "State Management", "Push Notifications", "Firebase", "App Store Deployment", "Offline Storage", "Performance Profiling"],
        "critical_check": ["React Native", "Flutter", "Mobile UI", "REST APIs", "Git", "State Management"],
        "default_missing": ["Offline-first data synchronization", "Mobile performance & memory leak profiling", "Native bridges & hardware integration", "CI/CD automated app bundle deployment", "Push notification lifecycle handling"]
    },
    "Digital Marketing": {
        "slug": "digital-marketing",
        "primary": ["SEO", "Google Analytics", "Content Strategy", "Social Media Marketing", "Performance Marketing", "Meta Ads", "Google Ads", "Email Marketing"],
        "advanced": ["Conversion Rate Optimization", "CRO", "A/B Testing", "Tag Manager", "Semrush", "Keyword Research", "Copywriting", "Marketing Funnels"],
        "critical_check": ["SEO", "Google Analytics", "Meta Ads", "Conversion Rate Optimization", "Keyword Research", "Email Marketing"],
        "default_missing": ["Google Analytics 4 event debugging & custom funnels", "Technical SEO audits (Core Web Vitals & schema markup)", "Meta CAPI server-side event tracking", "A/B landing page conversion rate optimization", "Multi-touch attribution modeling"]
    }
}

# Domain slug to canonical name mapping
SLUG_TO_DOMAIN: Dict[str, str] = {
    v["slug"]: k for k, v in DOMAIN_KEYWORDS.items()
}
SLUG_TO_DOMAIN["full-stack"] = "Full Stack Development"
SLUG_TO_DOMAIN["data-analyst"] = "Data Analyst"
SLUG_TO_DOMAIN["ai-agent"] = "AI Agent Development"
SLUG_TO_DOMAIN["ai-machine-learning"] = "AI Agent Development"
SLUG_TO_DOMAIN["python"] = "Python Automation"

POWER_ACTION_VERBS = [
    "engineered", "architected", "developed", "deployed", "optimized", "implemented",
    "designed", "automated", "built", "spearheaded", "accelerated", "scaled", "reduced",
    "increased", "integrated", "streamlined", "migrated", "refactored", "orchestrated",
    "executed", "modeled", "configured", "maintained", "analyzed", "published", "secured"
]

METRIC_REGEX = re.compile(
    r"(\d+(\.\d+)?%|\$\d+(?:,\d+)?|\₹\d+(?:,\d+)?|\b\d+\+?\s*(?:ms|seconds|minutes|hours|days|users|requests|records|queries|x|fold|stars|downloads|clients|leads|tickets)\b)",
    re.IGNORECASE
)

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(\+?91[\-\s]?)?[6-9]\d{9}|\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")
LINKS_REGEX = re.compile(r"(github\.com/[a-zA-Z0-9_-]+|linkedin\.com/in/[a-zA-Z0-9_-]+|https?://[^\s]+)")


def canonical_domain(domain_input: Optional[str]) -> str:
    """Resolves arbitrary domain string or slug to canonical key."""
    if not domain_input:
        return "Full Stack Development"
    cleaned = domain_input.strip()
    if cleaned in DOMAIN_KEYWORDS:
        return cleaned
    lower = cleaned.lower().replace("_", "-")
    if lower in SLUG_TO_DOMAIN:
        return SLUG_TO_DOMAIN[lower]
    for k, v in DOMAIN_KEYWORDS.items():
        if v["slug"] in lower or lower in k.lower():
            return k
    return "Full Stack Development"


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> Tuple[str, Optional[str]]:
    """Safely extracts raw text from PDF bytes using pypdf."""
    try:
        import io
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        pages_text = []
        for i, page in enumerate(reader.pages):
            txt = page.extract_text()
            if txt:
                pages_text.append(txt)
        full_text = "\n".join(pages_text).strip()
        if not full_text:
            return "", "PDF was read but contained no extractable text layer (likely a scanned image). Please paste text directly."
        return full_text, None
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return "", f"Could not parse PDF: {str(e)}"


def evaluate_resume_deterministic(text: str, domain: str) -> Dict[str, Any]:
    """
    Computes rigorous 0-100 ATS evaluation without network or external API dependency.
    Guarantees stable, high-value metrics every time.
    """
    domain_key = canonical_domain(domain)
    meta = DOMAIN_KEYWORDS.get(domain_key, DOMAIN_KEYWORDS["Full Stack Development"])
    
    words = re.findall(r"\b[a-zA-Z0-9_+.-]+\b", text)
    word_count = len(words)
    lower_text = text.lower()
    
    # ── 1. Keyword & Tech Stack Alignment (30 pts) ──
    all_keywords = meta["primary"] + meta["advanced"]
    found_keywords = []
    missing_keywords = []
    for kw in all_keywords:
        # Check whole-word or substring match
        pattern = r"\b" + re.escape(kw.lower()) + r"\b"
        if re.search(pattern, lower_text):
            found_keywords.append(kw)
        else:
            missing_keywords.append(kw)
    
    kw_coverage = len(found_keywords) / max(1, len(all_keywords))
    keyword_score = int(min(30, kw_coverage * 40))  # Max 30 points
    
    # ── 2. Action Verbs & Metric Quantification (25 pts) ──
    found_verbs = [v for v in POWER_ACTION_VERBS if re.search(r"\b" + v + r"\b", lower_text)]
    verb_score = min(12, int(len(found_verbs) * 2))
    
    metrics_matches = METRIC_REGEX.findall(text)
    metric_count = len(metrics_matches)
    metric_score = min(13, int(metric_count * 2.5))
    impact_score = verb_score + metric_score  # Max 25 points
    
    # ── 3. Section Completeness & Contact ATS Check (20 pts) ──
    has_email = bool(EMAIL_REGEX.search(text))
    has_phone = bool(PHONE_REGEX.search(text))
    has_links = bool(LINKS_REGEX.search(text))
    
    contact_score = (5 if has_email else 0) + (4 if has_phone else 0) + (3 if has_links else 0)
    
    has_edu = bool(re.search(r"\b(education|b\.?tech|degree|bachelor|master|university|college|cgpa|gpa)\b", lower_text))
    has_exp = bool(re.search(r"\b(experience|projects?|work|internship|developed|built)\b", lower_text))
    has_skills = bool(re.search(r"\b(skills|technologies|tools|stack|programming)\b", lower_text))
    
    sections_score = (3 if has_edu else 0) + (3 if has_exp else 0) + (2 if has_skills else 0)
    structure_score = min(20, contact_score + sections_score)
    
    # ── 4. Length & Formatting Hygiene (15 pts) ──
    # Optimal for freshers: 350-900 words
    if 350 <= word_count <= 950:
        length_score = 15
    elif 200 <= word_count < 350:
        length_score = 9
    elif 950 < word_count <= 1400:
        length_score = 11
    else:
        length_score = 5
        
    # ── 5. Domain Critical Readiness (10 pts) ──
    critical_matches = [k for k in meta["critical_check"] if re.search(r"\b" + re.escape(k.lower()) + r"\b", lower_text)]
    critical_score = int((len(critical_matches) / max(1, len(meta["critical_check"]))) * 10)
    
    # ── Overall Score (0-100) ──
    total_score = min(98, max(28, keyword_score + impact_score + structure_score + length_score + critical_score))
    
    # Grade & Pass Probability
    if total_score >= 85:
        tier = "Distinction Ready"
        badge = "Tier 1 ATS Compatible"
        probability = "92% Pass Probability"
        color = "#10B981"
    elif total_score >= 70:
        tier = "Competitive"
        badge = "Moderate ATS Risk"
        probability = "74% Pass Probability"
        color = "#F59E0B"
    elif total_score >= 55:
        tier = "Needs Optimization"
        badge = "High Filter Rejection Risk"
        probability = "48% Pass Probability"
        color = "#EF4444"
    else:
        tier = "Critical Revision Required"
        badge = "Unlikely to Clear Automated Screening"
        probability = "22% Pass Probability"
        color = "#DC2626"
        
    # Generate top strengths
    strengths = []
    if len(found_keywords) >= 5:
        strengths.append(f"Strong foundational tech stack coverage ({', '.join(found_keywords[:4])}).")
    if metric_count >= 3:
        strengths.append(f"Good quantifiable impact ({metric_count} metric datapoints identified).")
    if has_email and has_phone and has_links:
        strengths.append("Complete ATS contact header (Email, Phone, and Public Profile).")
    if len(found_verbs) >= 4:
        strengths.append("Active leadership voice with modern power action verbs.")
    if not strengths:
        strengths.append("Clear readability and parseable plain-text layout.")
        strengths.append("Clear domain intent for engineering roles.")
        
    # Top critical gaps
    priority_missing = missing_keywords[:5] if missing_keywords else meta["default_missing"][:4]
    
    return {
        "score": total_score,
        "tier": tier,
        "badge": badge,
        "pass_probability": probability,
        "color": color,
        "word_count": word_count,
        "domain": domain_key,
        "breakdown": {
            "keywords": {"score": keyword_score, "max": 30, "percentage": int((keyword_score / 30) * 100)},
            "impact_verbs": {"score": impact_score, "max": 25, "percentage": int((impact_score / 25) * 100)},
            "structure": {"score": structure_score, "max": 20, "percentage": int((structure_score / 20) * 100)},
            "length_hygiene": {"score": length_score, "max": 15, "percentage": int((length_score / 15) * 100)},
            "domain_alignment": {"score": critical_score, "max": 10, "percentage": int((critical_score / 10) * 100)}
        },
        "stats": {
            "found_keywords": found_keywords,
            "missing_keywords_count": len(missing_keywords),
            "action_verbs_found": found_verbs[:6],
            "metrics_count": metric_count,
            "has_email": has_email,
            "has_phone": has_phone,
            "has_links": has_links
        },
        "strengths": strengths[:3],
        "critical_missing_keywords": priority_missing,
        "recommendations": {
            "summary": f"Your resume scores {total_score}/100 for {domain_key}. Adding missing core stack keywords and quantifying your project outcomes with latency/user numbers will boost your score into the top 90+ tier.",
            "bullet_rewrites": [
                {
                    "original": "Worked on frontend features and built REST APIs with database.",
                    "improved": f"Architected responsive Next.js frontend and engineered modular REST APIs in Node.js/PostgreSQL, reducing query response times by 32% for 5,000+ test records.",
                    "why": "Replaces passive 'worked on' with active power verbs ('Architected', 'Engineered') and provides measurable performance outcomes."
                },
                {
                    "original": "Created AI project using Python and helped with data processing.",
                    "improved": "Deployed production RAG pipeline using LangChain, pgvector, and FastAPI; optimized chunking to achieve 180ms retrieval latency across 10,000 document embeddings.",
                    "why": "Explicitly names modern tools (pgvector, FastAPI) and quantifies benchmark speed (180ms latency)."
                }
            ]
        }
    }


def enhance_with_gemini(text: str, domain: str, base_eval: Dict[str, Any], api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Attempts to refine bullet rewrites and recommendations using Gemini.
    Universal Mandate: Uses intern-provided Gemini API key when available.
    Gracefully returns base_eval if Gemini is unconfigured or rate-limited.
    """
    try:
        from .gemini_provider import GeminiProvider
        provider = GeminiProvider(api_key=api_key)
        if not provider.api_key:
            return base_eval
            
        snippet = text[:2500]  # Safe token budget
        domain_name = base_eval["domain"]
        
        prompt = f"""You are an elite Silicon Valley ATS auditor and technical recruiter evaluating a candidate for a '{domain_name}' role.
Candidate Resume Excerpt:
\"\"\"
{snippet}
\"\"\"

Current Preliminary Score: {base_eval['score']}/100.
Found Keywords: {', '.join(base_eval['stats']['found_keywords'][:6])}

Analyze the resume and return a STRICT JSON object with these keys:
{{
  "personalized_summary": "2-3 punchy sentences giving executive recruiter feedback on what makes them stand out and what immediately hurts their ATS chances.",
  "top_missing_keywords": ["list 4-5 exact modern technical keywords missing that a recruiter in {domain_name} searches for"],
  "bullet_rewrites": [
    {{
      "original": "an actual weak or unquantified bullet point extracted from the resume excerpt",
      "improved": "the rewritten high-impact version starting with a strong action verb and realistic metric/scale",
      "why": "why the change clears ATS filters and catches recruiter attention"
    }}
  ]
}}
Do NOT include markdown formatting or backticks outside the JSON. Return valid JSON only."""

        resp = provider.generate_content(prompt, temperature=0.3, max_tokens=1024)
        if resp and resp.text:
            cleaned = resp.text.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned)
            data = json.loads(cleaned)
            
            if data.get("personalized_summary"):
                base_eval["recommendations"]["summary"] = data["personalized_summary"]
            if data.get("top_missing_keywords") and len(data["top_missing_keywords"]) >= 3:
                base_eval["critical_missing_keywords"] = data["top_missing_keywords"][:5]
            if data.get("bullet_rewrites") and len(data["bullet_rewrites"]) > 0:
                base_eval["recommendations"]["bullet_rewrites"] = data["bullet_rewrites"][:2]
                
    except Exception as e:
        logger.info(f"Gemini ATS enhancement skipped (using deterministic analysis): {e}")
        
    return base_eval
