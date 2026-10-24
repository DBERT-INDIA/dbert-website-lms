import json
from datetime import datetime, timezone
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.dependencies import require_intern
from backend.models.auth import InternAccount
from backend.models.learning import Interview
from backend.services.interview_service import (
    check_interview_eligibility, generate_interview_questions
)
from backend.schemas.learning import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewSubmitRequest, InterviewSubmitResponse
)

router = APIRouter(prefix="/intern/interview", tags=["Intern Workspace"])

@router.get("/status", summary="Get Interview Eligibility and History")
async def get_interview_status(
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if not intern:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intern account not found")

    eligible, reason, remaining_secs = check_interview_eligibility(
        attempts=intern.interview_attempts or 0,
        last_attempt_at=intern.interview_last_attempt_at,
        locked=intern.interview_locked or False
    )

    # Fetch latest interview
    inv_stmt = select(Interview).where(Interview.intern_id == intern_id).order_by(Interview.id.desc())
    inv_res = await db.execute(inv_stmt)
    latest_interview = inv_res.scalar_one_or_none()

    return {
        "eligible": eligible,
        "reason": reason,
        "remaining_cooling_seconds": remaining_secs,
        "attempts_taken": intern.interview_attempts or 0,
        "latest_interview": {
            "id": latest_interview.id if latest_interview else None,
            "status": latest_interview.status if latest_interview else None,
            "score": latest_interview.score if latest_interview else None,
            "completed_at": latest_interview.completed_at if latest_interview else None
        } if latest_interview else None
    }

@router.post("/start", response_model=InterviewStartResponse, summary="Start AI Interview Session")
async def start_interview(
    req: InterviewStartRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    stmt = select(InternAccount).where(InternAccount.id == intern_id)
    res = await db.execute(stmt)
    intern = res.scalar_one_or_none()
    if not intern:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Intern account not found")

    eligible, reason, remaining_secs = check_interview_eligibility(
        attempts=intern.interview_attempts or 0,
        last_attempt_at=intern.interview_last_attempt_at,
        locked=intern.interview_locked or False
    )
    if not eligible:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=reason)

    domain = req.domain or intern.domain or "Python Automation"
    questions, model_used = await generate_interview_questions(domain)

    current_attempt = (intern.interview_attempts or 0) + 1
    new_interview = Interview(
        intern_id=intern.id,
        email=intern.email,
        name=intern.name,
        domain=domain,
        questions_json=json.dumps(questions),
        status="in_progress",
        attempt_number=current_attempt,
        generator_model=model_used
    )
    db.add(new_interview)

    intern.interview_attempts = current_attempt
    intern.interview_last_attempt_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(new_interview)

    return InterviewStartResponse(
        interview_id=new_interview.id,
        attempt_number=current_attempt,
        domain=domain,
        generator_model=model_used,
        questions=questions
    )

@router.post("/submit", response_model=InterviewSubmitResponse, summary="Submit Interview Answers")
async def submit_interview(
    req: InterviewSubmitRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Interview).where(Interview.id == req.interview_id)
    res = await db.execute(stmt)
    interview = res.scalar_one_or_none()
    if not interview:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found")

    interview.answers_json = json.dumps(req.answers)
    interview.status = "completed"
    interview.completed_at = datetime.now(timezone.utc)
    interview.score = 85.0
    interview.feedback = "Technical comprehension demonstrates foundational competence and readiness."

    await db.commit()
    return InterviewSubmitResponse(
        status="completed",
        message="Interview answers successfully submitted and processed",
        score=interview.score,
        feedback=interview.feedback
    )
