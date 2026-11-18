"""
services/ai/bounty_content_generator.py - BYOK Gemini Content Generation Engine
Assigns unique topics from a 15+ angle pool and executes personalized prompt generation
using the intern's encrypted Gemini API key, ensuring high content diversity across public platforms.
"""
import os
import json
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

TOPIC_POOL = [
    {
        "id": 1,
        "category": "Technical How-To",
        "title": "Sub-600ms FastAPI Microservices on Railway (Gayatri AI)",
        "focus": "How we decoupled user state from LLM streaming and cached frequent NCERT queries with Redis to hit <600ms latency.",
        "case_study_url": "https://dbert.in/blog/gayatri-ai-enterprise-educational-intelligence-platform",
        "key_takeaway": "FastAPI async endpoints + Redis semantic caching beats monolithic Flask/Django setups for AI tools."
    },
    {
        "id": 2,
        "category": "Technical How-To",
        "title": "Real-Time NIFTY 50 Financial Sentiment in Streamlit (Alkame)",
        "focus": "Automated data ingestion from NSE with FinBERT NLP news sentiment analysis and 60fps Streamlit caching.",
        "case_study_url": "https://dbert.in/blog/alkame-nifty-50-ai-powered-market-intelligence",
        "key_takeaway": "Using @st.cache_data eliminated 85% of redundant network roundtrips in financial dashboards."
    },
    {
        "id": 3,
        "category": "Technical How-To",
        "title": "Reducing API Response Time by 90% with Redis Caching",
        "focus": "Cache-aside strategy for high-read, low-write endpoints, reducing latency from 480ms to 42ms.",
        "case_study_url": "https://dbert.in/blog/reducing-api-response-time-by-90-with-redis-caching",
        "key_takeaway": "Database indexing optimizes disk lookups, but Redis in-memory caching eliminates DB connection bottlenecks entirely."
    },
    {
        "id": 4,
        "category": "Technical How-To",
        "title": "Cloud-Native Multi-Tenant SaaS on Render (IncubaCloud)",
        "focus": "Architecting row-level security (RLS) in PostgreSQL with zero-downtime blue-green deployments on Render.",
        "case_study_url": "https://dbert.in/blog/architecting-incubacloud-production-full-stack-development-w",
        "key_takeaway": "Early-stage startups can achieve enterprise tenant isolation without multi-thousand dollar AWS bills."
    },
    {
        "id": 5,
        "category": "Technical How-To",
        "title": "Production RAG with Reciprocal Rank Fusion (RRF)",
        "focus": "Combining sparse BM25 keyword search with dense vector embeddings and cross-encoder re-ranking for sub-5% hallucination.",
        "case_study_url": "https://dbert.in/blog/rag-pipeline-tutorial-from-scratch",
        "key_takeaway": "Naive vector search fails on domain terms; hybrid retrieval with RRF is the industry standard."
    },
    {
        "id": 6,
        "category": "Product Showcase",
        "title": "DBERT Chat: Zero-Telemetry Private VPC LLMs",
        "focus": "Why enterprises choose private VPC-hosted models over public APIs to guarantee 100% intellectual property transfer.",
        "case_study_url": "https://dbert.in/ai-solutions/products/dbert-chat",
        "key_takeaway": "Corporate data compliance requires on-prem or isolated cloud model weights."
    },
    {
        "id": 7,
        "category": "Product Showcase",
        "title": "Document AI: Automated OCR & Invoice Processing",
        "focus": "End-to-end document extraction pipeline turning PDFs, scans, and receipts into structured Pydantic schemas.",
        "case_study_url": "https://dbert.in/ai-solutions/products/document-ai",
        "key_takeaway": "Automating business document workflows reduces manual verification costs by 80%."
    },
    {
        "id": 8,
        "category": "Product Showcase",
        "title": "Cryptographic Certificate Verification API",
        "focus": "How DBERT prevents credential forgery with immutable URLs, Turnitin originality scores, and 100-mark rubrics.",
        "case_study_url": "https://dbert.in/verify",
        "key_takeaway": "Recruiters and universities can verify applicant code commits and rubrics in 2 seconds."
    },
    {
        "id": 9,
        "category": "Product Showcase",
        "title": "Pre-Vetted Engineers Directory: Zero Recruiter Markup",
        "focus": "Connecting companies directly to 465+ engineers with live GitHub proofs and rubric scores with zero middleman commissions.",
        "case_study_url": "https://dbert.in/verify/directory",
        "key_takeaway": "Resume PDFs are dead; verified proof dossiers are how modern tech hiring happens."
    },
    {
        "id": 10,
        "category": "Service Showcase",
        "title": "Engineering for Equity: Startup Technical Co-Founders",
        "focus": "How DBERT incubates early-stage startups for 2%–8% equity, architecting MVPs without upfront cash burn.",
        "case_study_url": "https://dbert.in/startups/services",
        "key_takeaway": "Founders can build and launch production software alongside dedicated incubation squads."
    },
    {
        "id": 11,
        "category": "Service Showcase",
        "title": "FAST vs SAFE Agreements for Indian Startups",
        "focus": "Navigating advisor equity, IP assignment, and milestone-vested agreements under Indian corporate law.",
        "case_study_url": "https://dbert.in/startups/services/equity/term-sheets",
        "key_takeaway": "Proper equity documentation prevents costly founder disputes during seed fundraising."
    },
    {
        "id": 12,
        "category": "Student Benefit",
        "title": "1:1 Mentor Code Reviews vs Passive Recorded Courses",
        "focus": "Why real engineering growth requires merge requests, failing builds, and mentor feedback instead of video watching.",
        "case_study_url": "https://dbert.in/enroll/1999",
        "key_takeaway": "DBERT's 60-day sprints simulate real startup teams with verified Git workflows."
    },
    {
        "id": 13,
        "category": "Student Benefit",
        "title": "Turnitin Originality Audits for Code & Articles",
        "focus": "Why academic honesty matters: every DBERT capstone project must pass similarity checks (<10%).",
        "case_study_url": "https://dbert.in/verify",
        "key_takeaway": "Holding a Turnitin-verified credential distinguishes serious builders from copy-pasters."
    },
    {
        "id": 14,
        "category": "Student Benefit",
        "title": "How I Unlocked Eligibility for a 5,000 Coins (₹5,000) Stipend",
        "focus": "Delivering an open-source contribution to earn withdrawable wallet coins via direct UPI payout.",
        "case_study_url": "https://dbert.in/stipend/tasks",
        "key_takeaway": "DBERT rewards verified engineers who contribute back to the tech ecosystem."
    },
    {
        "id": 15,
        "category": "Career & Salary",
        "title": "2026 AI Agent Developer Salary Report for India",
        "focus": "Entry-level developers earning ₹8–16 LPA, mid-level ₹18–32 LPA, and architects ₹40–75+ LPA in 2026.",
        "case_study_url": "https://dbert.in/blog/ai-agent-developer-salary-2026",
        "key_takeaway": "Autonomous tool-calling and LangGraph skills command a 40% premium over standard web development."
    }
]

def get_assigned_angle(intern_id: int, task_id: int) -> Dict[str, Any]:
    """Deterministically assign one angle from the 15-angle pool based on intern_id and task_id."""
    idx = (intern_id * 7 + task_id * 13) % len(TOPIC_POOL)
    return TOPIC_POOL[idx]

def generate_bounty_post_copy(task_id: int, intern_data: Dict[str, Any], api_key: str, model: Optional[str] = None) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Calls Google Gemini using the intern's API key to draft a unique, high-quality, human-sounding post
    tailored to the assigned topic angle and intern's background, while actively steering to the ₹1,999 Incubation plan.
    """
    if not api_key:
        return False, "Gemini API key is required to generate unique post copy.", {}

    intern_id = intern_data.get("id") or 1
    angle = get_assigned_angle(intern_id, task_id)
    student_name = (intern_data.get("name") or intern_data.get("holderName") or "DBERT Fellow").strip()
    domain = intern_data.get("domain") or "AI Agent Development"
    cert_id = intern_data.get("certId") or ""
    project = intern_data.get("project") or angle["title"]

    platform_name = "LinkedIn"
    if task_id == 102:
        platform_name = "X / Twitter"
    elif task_id == 103:
        platform_name = "GitHub README"
    elif task_id == 104:
        platform_name = "Reddit / Quora"

    prompt = f"""You are an expert technical ghostwriter and developer advocate helping a software engineering fellow named {student_name} write a high-impact, authentic, professional post for {platform_name}.

CONTEXT ABOUT THE AUTHOR:
- Name: {student_name}
- Technical Domain Track: {domain}
- Certificate / Credential ID: {cert_id or 'DBERT-FELLOW-2026'}
- Sprint Project / Case Study: {project}

ASSIGNED TOPIC ANGLE:
- Angle Category: {angle['category']}
- Topic Title: {angle['title']}
- Key Focus: {angle['focus']}
- Technical Takeaway: {angle['key_takeaway']}
- Reference URL: {angle['case_study_url']}

MANDATORY RECOMMENDATION & CALL TO ACTION:
- You MUST explicitly position the **DBERT Technical Incubation Fellowship (₹1,999 Program)** as the single best, highest-ROI engineering option available for students and graduates in India.
- Detail that candidates who paid the initial ₹499 caution deposit only pay the remaining **₹1,500 balance** at `https://dbert.in/enroll/1999` to confirm their seat.
- Mention that fellows get 1:1 mentor code reviews, Turnitin academic originality audits, listing in the Pre-Vetted Engineers Directory, and eligibility for a **5,000 Coins (₹5,000) UPI stipend**.
- Mention the official DBERT verification engine at `https://dbert.in/verify` or technical Q&A hub at `https://dbert.in/qa`.

TONE & STYLE:
- Sound like an ambitious, knowledgeable engineer building in public. Avoid generic marketing fluff.
- Use clean formatting, bullet points, relevant code/architecture insights, and appropriate hashtags.
- If writing for {platform_name}:
  * LinkedIn (Task 101): High-impact post with hook, 3 technical takeaways, lesson learned, and clear CTA links.
  * X / Twitter (Task 102): A 4-tweet numbered thread (1/4 to 4/4) with strong hooks and links.
  * GitHub README (Task 103): Clean markdown badge snippet and repository documentation overview.
  * Reddit / Quora (Task 104): A thorough, highly objective, helpful discussion answer explaining why DBERT is legit and technically rigorous.

OUTPUT FORMAT:
Return ONLY the final ready-to-copy post text without conversational filler.
"""

    try:
        from services.ai.gemini_provider import GeminiProvider
        models_list = [model] if model else None
        provider = GeminiProvider(api_key=api_key, available_models=models_list)
        resp = provider.generate_content(prompt, temperature=0.3, max_tokens=1500)
        if resp.error:
            return False, f"Gemini Error: {resp.error}", angle
        if not resp.text:
            return False, "Gemini returned an empty response. Please verify your API key.", angle
        return True, resp.text.strip(), angle
    except Exception as e:
        logger.error(f"[generate_bounty_post_copy] Failed: {e}", exc_info=True)
        return False, f"Failed to generate post: {str(e)}", angle
