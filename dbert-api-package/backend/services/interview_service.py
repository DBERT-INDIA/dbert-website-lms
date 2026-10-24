import random
import json
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any, Tuple
import httpx

from backend.core.config import settings

INTERVIEW_BLUEPRINT = [
    ("technical", 2), ("applied", 1), ("communication", 1)
]

INTERVIEW_DOMAIN_BANK = {
    "AI Agent Development": {
        "technical": [
            {"key": "ai_tech_01", "text": "In your own words, what is an AI Agent and how does its context window impact autonomous workflows?"},
            {"key": "ai_tech_02", "text": "What is Retrieval-Augmented Generation (RAG) and why is it preferred over raw LLM completions for enterprise documents?"},
            {"key": "ai_tech_03", "text": "Explain how embeddings and vector similarity enable semantic search."},
            {"key": "ai_tech_04", "text": "What is tool/function calling in LLMs and how do agents handle structured tool outputs?"}
        ],
        "applied": [
            {"key": "ai_app_01", "text": "Outline the steps you would take to build an automated agent that analyzes invoices and updates a database."},
            {"key": "ai_app_02", "text": "How do you detect and mitigate hallucination in production agent pipelines?"}
        ],
        "communication": [
            {"key": "ai_comm_01", "text": "Explain what an API key is and why it must remain secret to a non-technical manager."},
            {"key": "ai_comm_02", "text": "How would you explain the trade-off between private LLM hosting and Cloud APIs?"}
        ]
    },
    "Data Analyst": {
        "technical": [
            {"key": "da_tech_01", "text": "Explain the difference between SQL INNER JOIN and LEFT JOIN with a business example."},
            {"key": "da_tech_02", "text": "How do you detect and clean anomalies or missing values in time-series data using Pandas?"},
            {"key": "da_tech_03", "text": "When would you use a window function (e.g. ROW_NUMBER or RANK) in SQL?"}
        ],
        "applied": [
            {"key": "da_app_01", "text": "If weekly sales dropped 15%, what investigative framework would you follow to diagnose the root cause?"},
            {"key": "da_app_02", "text": "How do you structure an executive dashboard in Power BI or Tableau to emphasize actionable KPIs?"}
        ],
        "communication": [
            {"key": "da_comm_01", "text": "Explain the difference between correlation and causation using an everyday scenario."},
            {"key": "da_comm_02", "text": "How do you explain statistical outliers to stakeholders who want to drop them unconditionally?"}
        ]
    },
    "Full Stack Development": {
        "technical": [
            {"key": "fs_tech_01", "text": "What happens under the hood when a browser requests an HTTPS webpage?"},
            {"key": "fs_tech_02", "text": "Explain the difference between JWT stateless authentication and server-side sessions."},
            {"key": "fs_tech_03", "text": "How do database indexes improve read performance, and what are their write trade-offs?"}
        ],
        "applied": [
            {"key": "fs_app_01", "text": "Describe how you would design a rate limiter to protect public API endpoints from abuse."},
            {"key": "fs_app_02", "text": "How do you structure database transactions to prevent race conditions during high-volume purchases?"}
        ],
        "communication": [
            {"key": "fs_comm_01", "text": "Explain the concept of microservices versus a monolithic architecture to a product manager."},
            {"key": "fs_comm_02", "text": "How would you document a REST API so external developers can integrate within hours?"}
        ]
    },
    "Python Automation": {
        "technical": [
            {"key": "py_tech_01", "text": "Explain the difference between synchronous and asynchronous code execution in Python."},
            {"key": "py_tech_02", "text": "How do you handle pagination and rate limits when scraping or consuming external APIs?"},
            {"key": "py_tech_03", "text": "What are Python context managers (the 'with' statement) and why are they critical for resources?"}
        ],
        "applied": [
            {"key": "py_app_01", "text": "How would you build a scheduled pipeline that scrapes job listings daily and handles network errors gracefully?"},
            {"key": "py_app_02", "text": "Describe how you would automate parsing unstructured PDF invoices into clean relational tables."}
        ],
        "communication": [
            {"key": "py_comm_01", "text": "How do you explain the value of automated testing and CI/CD to a startup founder seeking rapid speed?"},
            {"key": "py_comm_02", "text": "How do you convey that an automated web scraper broke due to a third-party DOM update?"}
        ]
    }
}

def assemble_static_bank(domain: str) -> List[Dict[str, str]]:
    """Assemble static blueprint question set guaranteeing 2 technical + 1 applied + 1 communication."""
    domain_data = INTERVIEW_DOMAIN_BANK.get(domain) or INTERVIEW_DOMAIN_BANK["Python Automation"]
    selected = []
    for category, count in INTERVIEW_BLUEPRINT:
        pool = domain_data.get(category, [])
        sample_count = min(count, len(pool))
        chosen = random.sample(pool, sample_count)
        for q in chosen:
            selected.append({
                "key": q["key"],
                "category": category,
                "question": q["text"]
            })
    return selected

def check_interview_eligibility(
    attempts: int,
    last_attempt_at: Optional[datetime],
    locked: bool = False
) -> Tuple[bool, Optional[str], Optional[int]]:
    """Check if intern is eligible to take the interview, enforcing cooling period."""
    if locked:
        return False, "Interview is locked by administration.", None

    if attempts >= settings.INTERVIEW_MAX_ATTEMPTS:
        return False, f"Maximum interview attempts ({settings.INTERVIEW_MAX_ATTEMPTS}) reached.", None

    if last_attempt_at and attempts > 0:
        now = datetime.now(timezone.utc)
        if last_attempt_at.tzinfo is None:
            last_attempt_at = last_attempt_at.replace(tzinfo=timezone.utc)
        cooling_end = last_attempt_at + timedelta(hours=settings.INTERVIEW_COOLING_HOURS)
        if now < cooling_end:
            remaining_seconds = int((cooling_end - now).total_seconds())
            return False, f"Cooling period active. Please retry in {remaining_seconds // 3600}h {(remaining_seconds % 3600) // 60}m.", remaining_seconds

    return True, None, None

async def generate_interview_questions(domain: str, github_username: Optional[str] = None) -> Tuple[List[Dict[str, str]], str]:
    """Generate interview questions using Gemini AI with fallback to domain bank."""
    # Check if Gemini is enabled and keys are configured
    keys = [k.strip() for k in settings.GEMINI_API_KEYS.split(",") if k.strip()]
    if settings.GEMINI_API_KEY:
        keys.append(settings.GEMINI_API_KEY.strip())

    if not settings.INTERVIEW_ENABLED or not keys:
        return assemble_static_bank(domain), "static_bank"

    # Attempt Gemini API with timeout budget
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent"
    prompt = f"Generate 4 short technical interview questions for a junior candidate applying for '{domain}'. Return only JSON array with fields 'key', 'category', 'question'."
    
    for key in keys[:3]:
        try:
            async with httpx.AsyncClient(timeout=float(settings.GEMINI_TIMEOUT)) as client:
                res = await client.post(
                    f"{url}?key={key}",
                    json={"contents": [{"parts": [{"text": prompt}]}]}
                )
                if res.status_code == 200:
                    data = res.json()
                    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                    cleaned = raw_text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                    parsed = json.loads(cleaned)
                    if isinstance(parsed, list) and len(parsed) >= 4:
                        return parsed[:4], settings.GEMINI_MODEL
        except Exception:
            continue

    # Fallback seamlessly to domain bank
    return assemble_static_bank(domain), "static_bank"
