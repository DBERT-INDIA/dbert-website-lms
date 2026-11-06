from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.core.config import settings
from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token, require_privileged
from backend.models.portal import Application, ApplicationStatusHistory
from backend.services.application_service import (
    transition_application, ApplicationStateMachineError,
    InvalidTransitionError, UnauthorizedTransitionError, ApplicationNotFoundError,
    STATUS_APPLY_PENDING
)
from backend.schemas.portal import (
    ApplicationCreateRequest, ApplicationResponse, ApplicationTransitionRequest,
    ApplicationPublicStatusResponse
)

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/apply", response_model=ApplicationResponse, summary="Submit New Internship Application")
async def apply_for_internship(
    req: ApplicationCreateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # Rule: Check maximum applications per person
    email = req.email.lower().strip()
    count_stmt = select(func.count(Application.id)).where(
        Application.email == email,
        Application.status.not_in(["Rejected", "Accepted"])
    )
    res = await db.execute(count_stmt)
    active_count = res.scalar() or 0
    if active_count >= settings.MAX_APPLICATIONS_PER_PERSON:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You have reached the maximum allowed active applications ({settings.MAX_APPLICATIONS_PER_PERSON})."
        )

    new_app = Application(
        name=req.name.strip(),
        email=email,
        phone=req.phone.strip(),
        city=req.city.strip(),
        college=req.college.strip(),
        course=req.course.strip(),
        semester=req.semester.strip(),
        year_of_passing=req.year_of_passing.strip(),
        domain=req.domain.strip(),
        why_join=req.why_join.strip(),
        portfolio=req.portfolio,
        status=STATUS_APPLY_PENDING,
        source=req.source or "web",
        intent_answers=req.intent_answers
    )
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)

    # Initial history entry
    req_id = getattr(request.state, "request_id", None)
    history = ApplicationStatusHistory(
        application_id=new_app.id,
        old_status=None,
        new_status=STATUS_APPLY_PENDING,
        changed_by="applicant",
        reason="Initial application submission",
        request_id=req_id
    )
    db.add(history)
    await db.commit()

    return new_app

@router.get("/{app_id}", response_model=ApplicationResponse, summary="Get Application Details")
async def get_application(
    app_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application).where(Application.id == app_id)
    res = await db.execute(stmt)
    app = res.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    user_role = current_user.get("role", "")
    user_email = (current_user.get("email") or "").lower().strip()
    user_sub = str(current_user.get("sub", ""))

    # Privileged staff/admin/mentor can access applications
    if user_role in ("admin", "staff", "mentor"):
        return app

    # Candidate can only access their own application
    app_email = (app.email or "").lower().strip()
    if user_email and app_email == user_email:
        return app
    if user_sub and hasattr(app, "user_id") and str(getattr(app, "user_id", "")) == user_sub:
        return app

    # Privacy-preserving 404 to prevent ID enumeration
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

@router.get("/{app_id}/status", response_model=ApplicationPublicStatusResponse, summary="Get Public Application Status Tracking")
async def get_application_public_status(app_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Application).where(Application.id == app_id)
    res = await db.execute(stmt)
    app = res.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return app

@router.post("/{app_id}/transition", response_model=ApplicationResponse, summary="Transition Application Status")
async def update_application_status(
    app_id: int,
    req: ApplicationTransitionRequest,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_privileged),
    db: AsyncSession = Depends(get_db)
):
    req_id = getattr(request.state, "request_id", None)
    try:
        app, _ = await transition_application(
            db=db,
            application_id=app_id,
            target_status=req.target_status,
            actor_role=current_user.get("role", "staff"),
            actor_email=current_user.get("email"),
            reason=req.reason,
            mentor_note=req.mentor_note,
            request_id=req_id
        )
        return app
    except InvalidTransitionError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UnauthorizedTransitionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ApplicationNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
