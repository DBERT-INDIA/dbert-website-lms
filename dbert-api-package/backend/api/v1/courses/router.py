import json
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token, require_intern
from backend.models.learning import (
    Course, CourseChapter, CourseSubtopic, CourseEnrollment,
    CourseDayQuiz, DayQuizAttempt, CourseSubtopicChat
)
from backend.schemas.learning import (
    CourseResponse, QuizSubmitRequest, QuizSubmitResponse,
    TutorChatRequest, TutorChatResponse
)
from backend.services.learning_service import (
    grade_quiz_submission, generate_socratic_tutor_response
)

router = APIRouter(prefix="/courses", tags=["Courses & Guided Learning"])

@router.get("", response_model=List[CourseResponse], summary="List Published Courses")
async def list_courses(db: AsyncSession = Depends(get_db)):
    stmt = select(Course).where(Course.is_published == True).order_by(Course.id.asc())
    res = await db.execute(stmt)
    courses = res.scalars().all()
    return courses

@router.get("/{course_id}", summary="Get Course Details & Curriculum")
async def get_course_detail(course_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Course).where(Course.id == course_id)
    res = await db.execute(stmt)
    course = res.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # Fetch chapters
    ch_stmt = select(CourseChapter).where(CourseChapter.course_id == course_id).order_by(CourseChapter.order_index.asc())
    ch_res = await db.execute(ch_stmt)
    chapters = ch_res.scalars().all()

    return {
        "course": course,
        "chapters": chapters
    }

@router.post("/{course_id}/enroll", summary="Enroll Intern in Course")
async def enroll_course(
    course_id: int,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    # Check if already enrolled
    chk = select(CourseEnrollment).where(
        CourseEnrollment.intern_id == intern_id,
        CourseEnrollment.course_id == course_id
    )
    res = await db.execute(chk)
    existing = res.scalar_one_or_none()
    if existing:
        return {"status": "success", "message": "Already enrolled in course", "enrollment_id": existing.id}

    enrollment = CourseEnrollment(intern_id=intern_id, course_id=course_id, status="active")
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return {"status": "success", "message": "Enrolled in course successfully", "enrollment_id": enrollment.id}

@router.get("/{course_id}/subtopic/{subtopic_id}", summary="Get Subtopic Lesson Content")
async def get_subtopic(subtopic_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(CourseSubtopic).where(CourseSubtopic.id == subtopic_id)
    res = await db.execute(stmt)
    subtopic = res.scalar_one_or_none()
    if not subtopic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subtopic not found")
    return subtopic

@router.post("/{course_id}/subtopic/{subtopic_id}/chat", response_model=TutorChatResponse, summary="Chat with AI Socratic Tutor")
async def chat_with_tutor(
    course_id: int,
    subtopic_id: int,
    req: TutorChatRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    sub_stmt = select(CourseSubtopic).where(CourseSubtopic.id == subtopic_id)
    sub_res = await db.execute(sub_stmt)
    subtopic = sub_res.scalar_one_or_none()
    title = subtopic.title if subtopic else "Topic"

    # Save user message
    db.add(CourseSubtopicChat(intern_id=intern_id, subtopic_id=subtopic_id, sender="intern", message=req.message))

    # Generate socratic tutor answer
    tutor_reply = await generate_socratic_tutor_response(title, req.message, [])

    # Save tutor reply
    db.add(CourseSubtopicChat(intern_id=intern_id, subtopic_id=subtopic_id, sender="tutor", message=tutor_reply))
    await db.commit()

    return TutorChatResponse(sender="ai_tutor", message=tutor_reply)

@router.post("/{course_id}/quiz/{day_number}/submit", response_model=QuizSubmitResponse, summary="Submit Course Day Quiz")
async def submit_day_quiz(
    course_id: int,
    day_number: int,
    req: QuizSubmitRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    intern_id = int(current_user.get("sub"))
    # In practice compare with stored quiz answer key, mock 100% / passed
    result = grade_quiz_submission(req.answers, {"q1": "a", "q2": "b"})
    attempt = DayQuizAttempt(
        intern_id=intern_id,
        course_id=course_id,
        day_number=day_number,
        score=result["score"],
        passed=result["passed"],
        answers_json=json.dumps(req.answers)
    )
    db.add(attempt)
    await db.commit()
    return QuizSubmitResponse(
        score=result["score"],
        passed=result["passed"],
        correct_count=result["correct_count"],
        total=result["total"]
    )
