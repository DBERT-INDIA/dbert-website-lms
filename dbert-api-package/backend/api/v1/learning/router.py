from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.dependencies import require_intern
from backend.models.learning import GLConcept, GLLearningSession, GLLearningTurn, GLStudentMastery

router = APIRouter(prefix="/learning", tags=["Courses & Guided Learning"])

@router.post("/v2/session", summary="Start Guided Learning Session")
async def start_learning_session(
    course_id: int,
    concept_id: int,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    session = GLLearningSession(
        intern_id=intern_id,
        course_id=course_id,
        concept_id=concept_id,
        status="active"
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return {"status": "success", "session_id": session.id}

@router.post("/v2/turn", summary="Submit Guided Learning Turn")
async def submit_learning_turn(
    session_id: int,
    user_message: str,
    db: AsyncSession = Depends(get_db)
):
    # Retrieve session
    stmt = select(GLLearningSession).where(GLLearningSession.id == session_id)
    res = await db.execute(stmt)
    sess = res.scalar_one_or_none()
    if not sess:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning session not found")

    turn = GLLearningTurn(
        session_id=session_id,
        user_message=user_message,
        ai_response="Excellent progress on this concept! Let's explore how this applies to production microservices.",
        mastery_delta=0.1
    )
    db.add(turn)
    await db.commit()
    return {"status": "success", "ai_response": turn.ai_response, "mastery_delta": turn.mastery_delta}

@router.get("/v2/concept-tree/{course_id}", summary="Get Concept Tree for Course")
async def get_concept_tree(course_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(GLConcept).where(GLConcept.course_id == course_id)
    res = await db.execute(stmt)
    concepts = res.scalars().all()
    return concepts
