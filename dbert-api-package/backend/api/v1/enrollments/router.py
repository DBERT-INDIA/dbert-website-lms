from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token, require_privileged
from backend.models.portal import Enrollment, EnrollmentStatusHistory, Application
from backend.services.enrollment_service import (
    transition_enrollment, ENROLLMENT_STATUS_PENDING, ENROLLMENT_STATUS_ACCEPTED,
    InvalidEnrollmentTransitionError, EnrollmentNotFoundError
)
from backend.services.application_service import transition_application, STATUS_ENROLLED, STATUS_PAID_ENROLLED
from backend.schemas.portal import EnrollmentCreateRequest, EnrollmentResponse

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/enroll", response_model=EnrollmentResponse, summary="Submit Enrollment Form")
async def create_enrollment(
    req: EnrollmentCreateRequest,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    new_enrollment = Enrollment(
        application_id=req.application_id,
        name=req.name,
        email=req.email.lower().strip(),
        phone=req.phone,
        city=req.city,
        college=req.college,
        course=req.course,
        semester=req.semester,
        year_of_passing=req.year_of_passing,
        domain=req.domain,
        joining_date=req.joining_date,
        batch_label=req.batch_label,
        product=req.product or "free_deposit",
        amount=req.amount or 499,
        payment_screenshot=req.payment_screenshot,
        payment_status=ENROLLMENT_STATUS_PENDING,
        razorpay_order_id=req.razorpay_order_id,
        razorpay_payment_id=req.razorpay_payment_id,
        razorpay_signature=req.razorpay_signature
    )
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)

    # Initial history
    req_id = getattr(request.state, "request_id", None)
    history = EnrollmentStatusHistory(
        enrollment_id=new_enrollment.id,
        old_status=None,
        new_status=ENROLLMENT_STATUS_PENDING,
        changed_by="student",
        reason="Enrollment submitted",
        request_id=req_id
    )
    db.add(history)

    # Synchronize application status to Enrolled
    if req.application_id:
        target_app_status = STATUS_PAID_ENROLLED if req.product == "paid_program" else STATUS_ENROLLED
        try:
            await transition_application(
                db=db,
                application_id=req.application_id,
                target_status=target_app_status,
                actor_role="system",
                reason=f"Enrollment {new_enrollment.id} created",
                request_id=req_id
            )
        except Exception:
            pass

    await db.commit()
    return new_enrollment

@router.get("/enrollment-count", summary="Public Enrollment Counter")
async def get_enrollment_count(db: AsyncSession = Depends(get_db)):
    stmt = select(func.count(Enrollment.id))
    res = await db.execute(stmt)
    total = res.scalar() or 0
    return {"count": total, "target": 500}

@router.post("/{enrollment_id}/review", response_model=EnrollmentResponse, summary="Review Enrollment Status")
async def review_enrollment(
    enrollment_id: int,
    target_status: str,
    request: Request,
    current_user: Dict[str, Any] = Depends(require_privileged),
    db: AsyncSession = Depends(get_db)
):
    req_id = getattr(request.state, "request_id", None)
    try:
        enrollment, _ = await transition_enrollment(
            db=db,
            enrollment_id=enrollment_id,
            target_status=target_status,
            actor_role=current_user.get("role", "admin"),
            actor_email=current_user.get("email"),
            reason="Admin manual review",
            request_id=req_id
        )
        return enrollment
    except (InvalidEnrollmentTransitionError, EnrollmentNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
