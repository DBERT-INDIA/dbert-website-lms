from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class InterviewStartRequest(BaseModel):
    domain: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None

class InterviewQuestion(BaseModel):
    key: str
    category: str
    question: str

class InterviewStartResponse(BaseModel):
    interview_id: int
    attempt_number: int
    domain: str
    generator_model: str
    questions: List[InterviewQuestion]

class InterviewSubmitRequest(BaseModel):
    interview_id: int
    answers: Dict[str, str] = Field(..., description="Map of question key to candidate answer text")

class InterviewSubmitResponse(BaseModel):
    status: str
    message: str
    score: Optional[float] = None
    feedback: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    slug: str
    title: str
    domain: str
    description: Optional[str]
    price: int
    total_hours: float
    total_lessons: int
    instructor_name: str

    class Config:
        from_attributes = True

class QuizSubmitRequest(BaseModel):
    answers: Dict[str, Any]

class QuizSubmitResponse(BaseModel):
    score: float
    passed: bool
    correct_count: int
    total: int

class TutorChatRequest(BaseModel):
    message: str = Field(..., min_length=2)

class TutorChatResponse(BaseModel):
    sender: str = "ai_tutor"
    message: str
