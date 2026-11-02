import json
import re
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token, require_intern
from backend.models.features import CV, InternCertificate
from backend.models.auth import InternAccount

router = APIRouter(tags=["CV & Credentials"])

class CVUpdateRequest(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    skills: Optional[list] = None
    projects: Optional[list] = None
    experience: Optional[list] = None
    education: Optional[list] = None
    links: Optional[dict] = None
    is_public: Optional[bool] = True

@router.get("/cv", summary="Get Authenticated Intern CV")
async def get_my_cv(
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    stmt = select(CV).where(CV.intern_id == user_id)
    res = await db.execute(stmt)
    cv = res.scalar_one_or_none()
    if not cv:
        return {"exists": False, "cv": None}
    return {"exists": True, "cv": cv}

@router.post("/cv", summary="Create or Update Intern CV")
async def save_my_cv(
    req: CVUpdateRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    stmt = select(CV).where(CV.intern_id == user_id)
    res = await db.execute(stmt)
    cv = res.scalar_one_or_none()

    if not cv:
        # Generate slug from user name or email
        email = current_user.get("email", "intern")
        base_slug = re.sub(r"[^a-zA-Z0-9]", "-", email.split("@")[0].lower())
        slug = f"{base_slug}-{user_id}"
        cv = CV(
            intern_id=user_id,
            slug=slug,
            headline=req.headline,
            summary=req.summary,
            skills_json=json.dumps(req.skills or []),
            projects_json=json.dumps(req.projects or []),
            experience_json=json.dumps(req.experience or []),
            education_json=json.dumps(req.education or []),
            links_json=json.dumps(req.links or {}),
            is_public=req.is_public if req.is_public is not None else True
        )
        db.add(cv)
    else:
        if req.headline is not None: cv.headline = req.headline
        if req.summary is not None: cv.summary = req.summary
        if req.skills is not None: cv.skills_json = json.dumps(req.skills)
        if req.projects is not None: cv.projects_json = json.dumps(req.projects)
        if req.experience is not None: cv.experience_json = json.dumps(req.experience)
        if req.education is not None: cv.education_json = json.dumps(req.education)
        if req.links is not None: cv.links_json = json.dumps(req.links)
        if req.is_public is not None: cv.is_public = req.is_public

    await db.commit()
    await db.refresh(cv)
    return {"status": "success", "slug": cv.slug}

@router.get("/cv/{slug}", summary="Public CV Verification Page")
async def get_public_cv(slug: str, db: AsyncSession = Depends(get_db)):
    stmt = select(CV).where(CV.slug == slug, CV.is_public == True)
    res = await db.execute(stmt)
    cv = res.scalar_one_or_none()
    if not cv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV not found or private")

    # Get intern details
    usr_stmt = select(InternAccount.name, InternAccount.domain, InternAccount.college).where(InternAccount.id == cv.intern_id)
    user = (await db.execute(usr_stmt)).fetchone()

    return {
        "candidate": {
            "name": user[0] if user else "Candidate",
            "domain": user[1] if user else "",
            "college": user[2] if user else ""
        },
        "headline": cv.headline,
        "summary": cv.summary,
        "skills": json.loads(cv.skills_json or "[]"),
        "projects": json.loads(cv.projects_json or "[]"),
        "experience": json.loads(cv.experience_json or "[]"),
        "education": json.loads(cv.education_json or "[]")
    }

@router.get("/certificate/{cert_id}", summary="Public Digital Certificate Verification")
async def verify_certificate(cert_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(InternCertificate).where(InternCertificate.cert_id == cert_id)
    res = await db.execute(stmt)
    cert = res.scalar_one_or_none()
    if not cert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate ID not recognized")

    return {
        "verified": True,
        "cert_id": cert.cert_id,
        "course_title": cert.course_title,
        "issued_at": cert.issued_at,
        "tier": cert.tier
    }
