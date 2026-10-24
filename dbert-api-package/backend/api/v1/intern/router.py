from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token, require_intern
from backend.core.security import verify_password, hash_password
from backend.models.auth import InternAccount
from backend.models.portal import Application
from backend.schemas.portal import (
    InternProfileUpdateRequest, ChangePasswordRequest,
    WizardStepRequest, ApplicationResponse
)

router = APIRouter(prefix="/intern", tags=["Intern Workspace"])

@router.get("/me", summary="Get Current Intern Profile")
async def get_my_profile(
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if not intern:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intern profile not found")

    return {
        "id": intern.id,
        "name": intern.name,
        "email": intern.email,
        "phone": intern.phone,
        "city": intern.city,
        "college": intern.college,
        "course": intern.course,
        "semester": intern.semester,
        "year_of_passing": intern.year_of_passing,
        "domain": intern.domain,
        "linkedin_url": intern.linkedin_url,
        "github_url": intern.github_url,
        "signup_stage": intern.signup_stage,
        "tutor_completion_pct": intern.tutor_completion_pct,
        "interview_attempts": intern.interview_attempts,
        "account_status": intern.account_status,
        "program": intern.program
    }

@router.post("/update-profile", summary="Update Intern Profile")
async def update_profile(
    req: InternProfileUpdateRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if not intern:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intern profile not found")

    update_data = req.dict(exclude_unset=True)
    for field, val in update_data.items():
        setattr(intern, field, val)

    await db.commit()
    return {"status": "success", "message": "Profile updated successfully"}

@router.post("/change-password", summary="Change Intern Password")
async def change_password(
    req: ChangePasswordRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if not intern or not verify_password(intern.password_hash, req.old_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    intern.password_hash = hash_password(req.new_password)
    intern.password_set = True
    await db.commit()
    return {"status": "success", "message": "Password changed successfully"}

@router.get("/my-applications", response_model=List[ApplicationResponse], summary="List Intern's Applications")
async def get_my_applications(
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    email = current_user.get("email")
    stmt = select(Application).where(Application.email == email).order_by(Application.created_at.desc())
    res = await db.execute(stmt)
    applications = res.scalars().all()
    return applications

@router.get("/wizard-status", summary="Get Onboarding Wizard Status")
async def get_wizard_status(
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount.signup_stage).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    stage = res.scalar_one_or_none() or 1
    return {"current_step": stage, "completed": (stage >= 3)}

@router.post("/save-wizard-step", summary="Save Onboarding Wizard Step")
async def save_wizard_step(
    req: WizardStepRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if intern:
        intern.signup_stage = max(intern.signup_stage or 1, req.step)
        await db.commit()
    return {"status": "success", "step": req.step}
