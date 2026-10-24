from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token
from backend.models.marketplace import Post, ScrapedInternship, ScrapedInternshipComment, PostComment

router = APIRouter(prefix="/marketplace", tags=["Job Marketplace"])

@router.get("/jobs", summary="Browse Available Jobs")
async def browse_jobs(
    domain: Optional[str] = None,
    city: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Post).where(Post.status == "published")
    if domain:
        stmt = stmt.where(Post.domain == domain)
    if city:
        stmt = stmt.where(Post.location.ilike(f"%{city}%"))
    stmt = stmt.order_by(Post.published_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/internships", summary="Browse Available Internships")
async def browse_internships(
    domain: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Post).where(Post.status == "published", Post.post_type == "internship")
    if domain:
        stmt = stmt.where(Post.domain == domain)
    stmt = stmt.order_by(Post.published_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/jobs/{slug}", summary="Get Job Details by Slug")
async def get_job_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Post).where(Post.slug == slug)
    res = await db.execute(stmt)
    post = res.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found")

    # Increment view count
    post.views = (post.views or 0) + 1
    await db.commit()
    return post

@router.get("/leads", summary="Browse External Scraped Leads")
async def list_scraped_leads(
    domain: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(ScrapedInternship)
    if domain:
        stmt = stmt.where(ScrapedInternship.Domain == domain)
    stmt = stmt.limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.post("/lead/{job_id}/click", summary="Track External Lead Click")
async def track_lead_click(job_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(ScrapedInternship).where(ScrapedInternship.id == job_id)
    res = await db.execute(stmt)
    lead = res.scalar_one_or_none()
    if lead:
        lead.Clicks = (lead.Clicks or 0) + 1
        await db.commit()
    return {"status": "success"}
