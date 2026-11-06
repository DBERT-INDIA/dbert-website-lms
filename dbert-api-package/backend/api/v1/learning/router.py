from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.config import settings
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
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    clean_msg = (user_message or "").strip()
    if not clean_msg:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty")
    if len(clean_msg) > 4000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message exceeds maximum allowed length (4000 characters)")

    # Retrieve session and enforce learner ownership (Finding DBERT-002)
    stmt = select(GLLearningSession).where(GLLearningSession.id == session_id)
    res = await db.execute(stmt)
    sess = res.scalar_one_or_none()
    if not sess:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning session not found")

    intern_id = int(current_user.get("sub"))
    if sess.intern_id != intern_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning session not found")

    if sess.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Learning session is closed or inactive")

    # Fetch concept context
    concept_stmt = select(GLConcept).where(GLConcept.id == sess.concept_id)
    c_res = await db.execute(concept_stmt)
    concept = c_res.scalar_one_or_none()
    concept_title = concept.title if concept else "Software Engineering"

    # Contextual tutor evaluation (Finding DBERT-017)
    ai_response = ""
    mastery_delta = 0.0

    gemini_key = settings.GEMINI_API_KEY
    if gemini_key:
        try:
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={gemini_key}"
            prompt = (
                f"You are an expert AI Tutor at DBERT Academy for the concept '{concept_title}'. "
                f"The student asks: {clean_msg}\n"
                f"Provide a clear, pedagogical, concise response guiding them to understand the concept."
            )
            async with httpx.AsyncClient(timeout=float(settings.GEMINI_TIMEOUT)) as client:
                resp = await client.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts:
                            ai_response = parts[0].get("text", "")
                            mastery_delta = 0.05
        except Exception:
            pass

    if not ai_response:
        ai_response = (
            f"The live AI tutor integration for concept '{concept_title}' is currently offline. "
            "Your response has been logged for mentor evaluation."
        )
        mastery_delta = 0.0

    turn = GLLearningTurn(
        session_id=session_id,
        user_message=clean_msg,
        ai_response=ai_response,
        mastery_delta=mastery_delta
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
