import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.dependencies import require_company
from backend.models.auth import Company
from backend.models.marketplace import Post, Cohort
from backend.models.portal import PostApplication

router = APIRouter(prefix="/company", tags=["Company & Employer"])

class CreatePostRequest(BaseModel):
    title: str
    domain: str
    description: str
    responsibilities: Optional[str] = None
    skills: Optional[str] = None
    location: Optional[str] = "Remote"
    work_mode: Optional[str] = "Remote"
    stipend_min: Optional[int] = 0
    stipend_max: Optional[int] = 0
    duration: Optional[str] = "2 months"
    openings: Optional[int] = 1

@router.get("/profile", summary="Get Company Profile")
async def get_company_profile(
    current_user: Dict[str, Any] = Depends(require_company),
    db: AsyncSession = Depends(get_db)
):
    comp_id = int(current_user.get("sub"))
    stmt = select(Company).where(Company.id == comp_id)
    res = await db.execute(stmt)
    comp = res.scalar_one_or_none()
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return comp

@router.post("/posts", summary="Create New Job or Internship Post")
async def create_post(
    req: CreatePostRequest,
    current_user: Dict[str, Any] = Depends(require_company),
    db: AsyncSession = Depends(get_db)
):
    comp_id = int(current_user.get("sub"))
    base_slug = re.sub(r"[^a-zA-Z0-9]", "-", req.title.lower()).strip("-")
    slug = f"{base_slug}-{comp_id}-{int(datetime.now(timezone.utc).timestamp())}"

    post = Post(
        company_id=comp_id,
        title=req.title,
        domain=req.domain,
        slug=slug,
        description=req.description,
        responsibilities=req.responsibilities,
        skills=req.skills,
        location=req.location,
        work_mode=req.work_mode,
        stipend_min=req.stipend_min,
        stipend_max=req.stipend_max,
        duration=req.duration,
        openings=req.openings,
        status="draft"
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return {"status": "success", "post_id": post.id, "slug": post.slug}

@router.post("/posts/{post_id}/publish", summary="Publish Post")
async def publish_post(
    post_id: int,
    current_user: Dict[str, Any] = Depends(require_company),
    db: AsyncSession = Depends(get_db)
):
    comp_id = int(current_user.get("sub"))
    stmt = select(Post).where(Post.id == post_id, Post.company_id == comp_id)
    res = await db.execute(stmt)
    post = res.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    post.status = "published"
    post.published_at = datetime.now(timezone.utc)
    await db.commit()
    return {"status": "success", "message": "Post published to public job board"}

@router.get("/posts/{post_id}/applicants", summary="Get Applicants for Post")
async def get_applicants(
    post_id: int,
    current_user: Dict[str, Any] = Depends(require_company),
    db: AsyncSession = Depends(get_db)
):
    comp_id = int(current_user.get("sub"))
    # Verify company ownership
    p_stmt = select(Post.id).where(Post.id == post_id, Post.company_id == comp_id)
    if not (await db.execute(p_stmt)).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized for this post")

    stmt = select(PostApplication).where(PostApplication.post_id == post_id).order_by(PostApplication.created_at.desc())
    res = await db.execute(stmt)
    return res.scalars().all()
