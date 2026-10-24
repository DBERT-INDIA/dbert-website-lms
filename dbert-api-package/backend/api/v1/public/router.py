from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.core.database import get_db
from backend.models.marketplace import Post, ScrapedInternship
from backend.models.learning import Course

router = APIRouter(prefix="/public", tags=["Public Discovery"])

@router.get("/stats/openings", summary="Get Live Openings Count")
async def get_live_openings(db: AsyncSession = Depends(get_db)):
    post_count = (await db.execute(select(func.count(Post.id)).where(Post.status == "published"))).scalar() or 0
    scraped_count = (await db.execute(select(func.count(ScrapedInternship.id)))).scalar() or 0
    return {
        "verified_company_posts": post_count,
        "scraped_opportunities": scraped_count,
        "total_active_openings": post_count + scraped_count
    }

@router.get("/jd/{domain}", summary="Get Standard Domain Job Description")
async def get_domain_jd(domain: str):
    descriptions = {
        "AI Agent Development": {
            "title": "AI Agent Development Fellow / Intern",
            "stipend": "₹8,000 – ₹18,000/month",
            "duration": "2 months",
            "skills": ["Python", "LangChain", "OpenAI API", "RAG Pipelines", "FastAPI"],
            "responsibilities": ["Build LLM-powered autonomous agents", "Design and implement RAG pipelines", "Integrate external APIs with AI workflows"]
        },
        "Data Analyst": {
            "title": "Data Analyst Fellow / Intern",
            "stipend": "₹6,000 – ₹14,000/month",
            "duration": "2 months",
            "skills": ["Python", "SQL", "Excel", "Power BI", "Pandas"],
            "responsibilities": ["Clean and process raw datasets", "Build interactive dashboards", "Generate weekly insight reports"]
        },
        "Full Stack Development": {
            "title": "Full Stack Development Fellow / Intern",
            "stipend": "₹7,000 – ₹16,000/month",
            "duration": "2 months",
            "skills": ["HTML/CSS", "JavaScript", "React or FastAPI", "REST APIs", "SQL"],
            "responsibilities": ["Build responsive web interfaces", "Develop and consume REST APIs", "Maintain and extend existing codebases"]
        },
        "Python Automation": {
            "title": "Python Automation Fellow / Intern",
            "stipend": "₹5,000 – ₹12,000/month",
            "duration": "2 months",
            "skills": ["Python", "Selenium", "BeautifulSoup", "APIs", "Scheduling"],
            "responsibilities": ["Build web scrapers and bots", "Automate repetitive business workflows", "Create scheduled data pipelines"]
        }
    }
    return descriptions.get(domain) or descriptions["Python Automation"]
