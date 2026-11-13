"""
services/ai/stipend_evaluator.py
Automated AI Pre-Screening and Health Monitoring Service for Stipend Submissions.
Eliminates silent fails by validating GEMINI_API_KEY before submission evaluation.
"""
import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger("stipend_evaluator")

DOMAIN_RUBRICS = {
    "AI & Machine Learning": {
        "title": "AI/ML Capstone Rubric",
        "criteria": [
            "Data preprocessing, pipeline architecture, and model selection.",
            "Code modularity, reproducibility, and version control hygiene.",
            "Evaluation metrics, loss/accuracy validation, and inference demonstration.",
            "Technical report completeness, mathematical intuition, and deployment viability."
        ]
    },
    "AI Agent Development": {
        "title": "Autonomous AI Agent Rubric",
        "criteria": [
            "Prompt engineering, context window management, and structured tool definitions.",
            "Agentic planning loops, ReAct execution, and multi-agent state coordination.",
            "Guardrails, error recovery, API secret hygiene, and runtime safety evaluation.",
            "Production deployment demo, latency optimization, and architecture documentation."
        ]
    },
    "Data Analyst": {
        "title": "Data Analytics & BI Rubric",
        "criteria": [
            "Data wrangling, schema modeling, and SQL/Pandas transformation.",
            "Interactive visualization design, KPI alignment, and UI/UX quality.",
            "Actionable business insights, statistical validity, and executive reporting.",
            "Technical documentation, data dictionary, and reproducible notebooks/dashboards."
        ]
    },
    "Full Stack Web Development": {
        "title": "Full Stack Application Rubric",
        "criteria": [
            "Frontend responsiveness, component hierarchy, and UX state management.",
            "Backend RESTful API design, database schemas, and query optimization.",
            "Authentication, error handling, input validation, and security posture.",
            "Cloud deployment, live demo functionality, and system architecture report."
        ]
    },
    "Full Stack Development": {
        "title": "Full Stack Application Rubric",
        "criteria": [
            "Frontend responsiveness, component hierarchy, and UX state management.",
            "Backend RESTful API design, database schemas, and query optimization.",
            "Authentication, error handling, input validation, and security posture.",
            "Cloud deployment, live demo functionality, and system architecture report."
        ]
    },
    "Python Automation": {
        "title": "Python Automation & RPA Rubric",
        "criteria": [
            "Workflow automation logic, exception recovery, and scheduling resilience.",
            "Headless scraping/parsing or bot efficiency and rate-limit compliance.",
            "Code clean architecture, logging, packaging, and configuration management.",
            "Execution logs demonstration, test harness, and operations runbook PDF."
        ]
    },
    "UI/UX Design": {
        "title": "UI/UX Product Design Rubric",
        "criteria": [
            "User research synthesis, personas, empathy maps, and information architecture.",
            "Figma component architecture, auto-layout responsiveness, and variant matrix.",
            "Design system tokens (typography, color, spacing), WCAG AA/AAA accessibility.",
            "Clickable interactive prototype demo, usability audit report, and developer specs."
        ]
    },
    "DevOps & Cloud": {
        "title": "DevOps & Cloud Infrastructure Rubric",
        "criteria": [
            "Containerization quality, multi-stage Dockerfile efficiency, and non-root security.",
            "CI/CD workflow automation (GitHub Actions), linting, testing, and artifact deployment.",
            "Cloud networking topology (VPC/subnets), IAM least-privilege, and infrastructure as code.",
            "Monitoring instrumentation (Prometheus/Grafana), uptime logs, and runbook report."
        ]
    },
    "Mobile App Development": {
        "title": "Mobile Application Engineering Rubric",
        "criteria": [
            "Cross-platform component architecture (React Native/Flutter) and responsive touch layouts.",
            "State management, asynchronous API data flow, and persistent offline local caching.",
            "Native hardware API integration (camera/geolocation/push) and runtime permission handling.",
            "Performance profiling (60fps scrolling, list virtualization), release bundle, and app demo."
        ]
    },
    "Cybersecurity": {
        "title": "Cybersecurity & SOC Assessment Rubric",
        "criteria": [
            "Attack surface decomposition, STRIDE threat modeling, and risk scoring.",
            "Vulnerability assessment methodology (OWASP Top 10, Burp Suite, Nmap, network traffic).",
            "Defensive remediation strategies, secure coding practices, and patch validation.",
            "Technical penetration test report with CVSS severity ranking and executive summary."
        ]
    },
    "Digital Marketing": {
        "title": "Growth Marketing & Funnel Optimization Rubric",
        "criteria": [
            "Keyword research, search intent mapping, on-page SEO, and Core Web Vitals audit.",
            "Performance ad campaign structure (Google/Meta), targeting, Quality Score, and ad creative.",
            "Web analytics tracking (GA4 custom events, conversion funnels, CAC/LTV, ROAS).",
            "Growth strategy blueprint, channel allocation model, and executive performance deck."
        ]
    }
}


def get_intern_gemini_key(conn, intern_id: int) -> Optional[str]:
    """Retrieves and decrypts the intern's active Gemini API key from intern_accounts."""
    if not conn or not intern_id:
        return None
    try:
        row = conn.execute("SELECT gemini_api_key_encrypted FROM intern_accounts WHERE id = ?", (intern_id,)).fetchone()
        if not row or not row["gemini_api_key_encrypted"]:
            return None
        from flask import current_app
        if hasattr(current_app, "decrypt_gemini_key"):
            decrypted = current_app.decrypt_gemini_key(row["gemini_api_key_encrypted"])
            if decrypted:
                return decrypted
        # Direct decrypt attempt using Fernet
        raw = row["gemini_api_key_encrypted"].strip()
        if raw.startswith("AIzaSy"):
            return raw
        key = os.environ.get("FERNET_KEY") or os.environ.get("SECRET_KEY")
        if key:
            from cryptography.fernet import Fernet
            return Fernet(key.encode() if isinstance(key, str) else key).decrypt(raw.encode()).decode()
    except Exception as e:
        logger.error(f"[get_intern_gemini_key] Error: {e}")
    return None


def get_active_gemini_key(conn=None, intern_id: Optional[int] = None) -> Optional[str]:
    """
    Retrieves active Gemini API key.
    Universal Mandate: Prioritizes intern-provided key when intern_id is passed.
    1. intern_accounts.gemini_api_key_encrypted (decrypted)
    2. os.environ['GEMINI_API_KEY']
    3. os.environ['GEMINI_API_KEYS'] (first key)
    4. platform_config table (key='gemini_api_key')
    """
    if conn and intern_id:
        intern_key = get_intern_gemini_key(conn, intern_id)
        if intern_key:
            return intern_key

    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if key and key != "your_gemini_api_key":
        return key

    keys = [k.strip() for k in os.environ.get("GEMINI_API_KEYS", "").split(",") if k.strip() and k.strip() != "your_gemini_api_key"]
    if keys:
        return keys[0]

    # Check platform_config
    if conn:
        try:
            row = conn.execute("SELECT value FROM platform_config WHERE key = 'gemini_api_key'").fetchone()
            if row and row["value"]:
                val = row["value"].strip()
                if val and val != "your_gemini_api_key":
                    return val
        except Exception:
            pass

    return None


def probe_gemini_key(api_key: str) -> Tuple[bool, str]:
    """
    Actively probes Google Gemini API using the provided key.
    Returns (is_valid: bool, status_message: str).
    """
    if not api_key:
        return False, "No Gemini API key provided."

    clean_key = api_key.strip()
    if len(clean_key) < 20:
        return False, "Invalid API key format (length too short)."

    probe_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={clean_key}"
    try:
        resp = requests.get(probe_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            models = [m.get("name", "").replace("models/", "") for m in data.get("models", [])]
            flash_models = [m for m in models if "flash" in m]
            return True, f"Active and verified. Access to {len(models)} models ({', '.join(flash_models[:3])})."
        elif resp.status_code in (400, 401, 403):
            err_msg = resp.json().get("error", {}).get("message", "Authentication failed.")
            return False, f"Google API authentication failed: {err_msg}"
        elif resp.status_code == 429:
            return True, "Key is valid, but currently rate-limited (HTTP 429)."
        else:
            return False, f"Google API returned unexpected status {resp.status_code}: {resp.text[:100]}"
    except requests.Timeout:
        return False, "Connection timed out while probing Google Gemini API."
    except requests.RequestException as e:
        return False, f"Network error connecting to Gemini API: {str(e)}"


class StipendEvaluator:
    """Evaluates intern technical submissions against domain rubrics."""

    @staticmethod
    def evaluate(submission_data: Dict[str, Any], domain: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes real-time pre-screening evaluation.
        Returns detailed evaluation dictionary with 0-100 score and rubric breakdown.
        """
        active_key = api_key or get_active_gemini_key()
        if not active_key:
            return {
                "score": 75,
                "status": "ai_unconfigured",
                "notes": "Automated evaluation skipped: GEMINI_API_KEY is not configured. Queued for mentor staff review.",
                "rubric_breakdown": {"total_score": 75, "verdict": "AWAITING_MANUAL_REVIEW"},
                "verdict": "AWAITING_MANUAL_REVIEW",
                "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        rubric = DOMAIN_RUBRICS.get(domain, DOMAIN_RUBRICS["Full Stack Web Development"])

        prompt = f"""
You are the Chief Academic & Technical Evaluator at DBERT (Digital Blinc Education Research and Technology).
Evaluate the following intern technical contribution for the domain: '{domain}'.

Deliverables Submitted:
- Candidate Name: {submission_data.get('holder_name', 'Student')}
- GitHub Repository URL: {submission_data.get('github_repo_url', 'N/A')}
- Live Deployment / Demo URL: {submission_data.get('live_demo_url', 'N/A')}
- Report Attachment: {submission_data.get('report_file_url', 'N/A')}
- Architectural Notes / Overview:
\"\"\"{submission_data.get('submission_content', 'N/A')}\"\"\"

Evaluation Rubric for {domain}:
1. {rubric['criteria'][0]} (Weight: 25 points)
2. {rubric['criteria'][1]} (Weight: 25 points)
3. {rubric['criteria'][2]} (Weight: 25 points)
4. {rubric['criteria'][3]} (Weight: 25 points)

Instructions:
Evaluate the submission thoroughly. Be constructive and objective.
Respond with a JSON object adhering to this schema:
{{
    "code_architecture_score": <int 0-25>,
    "documentation_score": <int 0-25>,
    "deployment_quality_score": <int 0-25>,
    "domain_relevance_score": <int 0-25>,
    "total_score": <int 0-100>,
    "verdict": "<'RECOMMENDED_APPROVE' or 'RECOMMENDED_REVISION'>",
    "summary_notes": "<2-3 sentence executive evaluation summary>",
    "strengths": ["<strength 1>", "<strength 2>"],
    "recommendations": ["<recommendation 1>", "<recommendation 2>"]
}}
"""
        from services.ai.gemini_provider import GeminiProvider
        provider = GeminiProvider(api_key=active_key)

        try:
            response = provider.generate_content(
                prompt=prompt,
                temperature=0.2,
                max_tokens=1024
            )
            raw_text = response.text or ""
            # Parse JSON from response
            cleaned_json = raw_text.strip()
            if "```json" in cleaned_json:
                cleaned_json = cleaned_json.split("```json")[1].split("```")[0].strip()
            elif "```" in cleaned_json:
                cleaned_json = cleaned_json.split("```")[1].split("```")[0].strip()

            eval_dict = json.loads(cleaned_json)
            total_score = int(eval_dict.get("total_score", 75))
            return {
                "score": total_score,
                "status": "evaluated",
                "notes": eval_dict.get("summary_notes", "Evaluation completed successfully."),
                "rubric_breakdown": eval_dict,
                "verdict": eval_dict.get("verdict", "RECOMMENDED_APPROVE" if total_score >= 70 else "RECOMMENDED_REVISION"),
                "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.error(f"Error during AI pre-screening: {e}")
            return {
                "score": None,
                "status": "AI_FAILED_MANUAL_REVIEW",
                "notes": f"Automated AI pre-screening unavailable: {str(e)[:100]}. Queued for manual mentor staff review.",
                "rubric_breakdown": {"verdict": "PENDING_STAFF_REVIEW", "error": str(e)[:100]},
                "verdict": "PENDING_STAFF_REVIEW",
                "evaluated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }


def generate_capstone_case_study(meta: Dict[str, Any], api_key: str) -> str:
    """
    Invokes Google Gemini with the intern's active API key to generate a rich,
    publication-grade 800+ word technical Case Study in Markdown.
    """
    from services.ai.gemini_provider import GeminiProvider

    author_name = meta.get("author_name") or "DBERT Fellow"
    domain = meta.get("domain") or "AI & Full Stack Engineering"
    cert_id = meta.get("cert_id") or "In Evaluation"
    repo_url = meta.get("repo_url") or ""
    demo_url = meta.get("demo_url") or ""
    project_name = meta.get("project_name") or "Capstone Engineering System"
    rubric_score = meta.get("rubric_score") or 75
    rubric_notes = meta.get("rubric_notes") or ""

    prompt = f"""You are a Principal Software & AI Architect at DBERT (Digital Blinc Education Research and Technology).
Write a comprehensive, publication-grade, 800+ word Technical Case Study in Github Flavored Markdown for an engineering fellow who just completed their intensive 60-day sprint at DBERT.

Candidate Profile & Submission Details:
- Author: {author_name}
- Domain Specialization: {domain}
- DBERT Credential ID: {cert_id}
- Pre-Screening Evaluation Rubric Score: {rubric_score}/100 (High Merit)
- Evaluator Feedback: {rubric_notes}
- Production GitHub Repository: {repo_url or 'https://github.com/dbert-fellows/' + project_name.lower().replace(' ', '-')}
- Interactive Live Cloud Deployment: {demo_url or 'https://' + project_name.lower().replace(' ', '-') + '.dbert.in'}
- Project Title: {project_name}

Structure & Content Requirements (Strictly follow this structure in Github-flavored Markdown):

# Architecting {project_name}: Production {domain} with DBERT Verified Evaluation

*Author: {author_name} · Track: {domain} · DBERT Credential ID: [{cert_id}](https://dbert.in/verify/{cert_id})*

---

## 1. System Overview & Problem Statement
Explain why this project was engineered, the real-world problem it solves, and why production standards are essential in {domain}.
Include clean clickable bullet links to GitHub, Live Demo, and DBERT Verified Credential:
- **Production Source Code**: [{repo_url or 'GitHub Repository'}]({repo_url or '#'})
- **Interactive Live Deployment**: [{demo_url or 'Live Cloud App'}]({demo_url or '#'})
- **DBERT Verified Credential**: [https://dbert.in/verify/{cert_id}](https://dbert.in/verify/{cert_id})
- **Pre-Screening Rubric Score**: **{rubric_score}/100 (High Merit)**

---

## 2. Architectural Blueprint & Technical Stack Decisions
Discuss modular architectural choices, asynchronous processing, data model design, and error recovery.
Include an ASCII architecture diagram representing data flow between the client, API gateway, core domain engine, database, and background services.

---

## 3. Core Implementation & Engineering Highlights
Deep dive into 2-3 specific implementation components with concrete, clean code snippets illustrating best practices (error handling, schemas, caching, or model pipelines) tailored specifically to {domain}.

---

## 4. Engineering Hurdles, Edge Cases & Performance Tuning
Discuss 3 specific engineering challenges faced during development and how they were solved (e.g. latency, race conditions, edge-case sanitization, rubric compliance).

---

## 5. Deployment, Live Verification & Reflections
Reflect on the production deployment, the 9-dimension evaluation rubric score ({rubric_score}/100), and key learnings from the DBERT incubation sprint.

---

*Interested in building production AI & Full Stack systems with 1:1 mentorship and verified credentials? Explore the [DBERT AI Fellowship](https://lms.dbert.in).*

Ensure strictly professional engineering tone, accurate markdown syntax, concrete code snippets, and zero generic placeholders.
"""

    provider = GeminiProvider(api_key=api_key)
    response = provider.generate_content(
        prompt=prompt,
        temperature=0.3,
        max_tokens=3000
    )
    raw_markdown = response.text or ""
    clean_md = raw_markdown.strip()
    if clean_md.startswith("```markdown"):
        clean_md = clean_md[len("```markdown"):].strip()
    if clean_md.startswith("```md"):
        clean_md = clean_md[len("```md"):].strip()
    if clean_md.endswith("```"):
        clean_md = clean_md[:-3].strip()

    return clean_md

