from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class ApplicationCreateRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str = Field(..., min_length=10)
    city: str
    college: str
    course: str
    semester: str
    year_of_passing: str
    domain: str
    why_join: str = Field(..., min_length=10)
    portfolio: Optional[str] = None
    source: Optional[str] = "web"
    intent_answers: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    city: str
    college: str
    course: str
    semester: str
    year_of_passing: str
    domain: str
    status: str
    why_join: str
    portfolio: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ApplicationTransitionRequest(BaseModel):
    target_status: str
    reason: Optional[str] = None
    mentor_note: Optional[str] = None

class EnrollmentCreateRequest(BaseModel):
    application_id: Optional[int] = None
    name: str
    email: EmailStr
    phone: str
    city: str
    college: str
    course: str
    semester: str
    year_of_passing: str
    domain: str
    joining_date: Optional[str] = None
    batch_label: Optional[str] = None
    product: Optional[str] = "free_deposit"
    amount: Optional[int] = 499
    payment_screenshot: Optional[str] = None
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None

class EnrollmentResponse(BaseModel):
    id: int
    application_id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    domain: Optional[str]
    product: Optional[str]
    amount: Optional[int]
    payment_status: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

class InternProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    college: Optional[str] = None
    course: Optional[str] = None
    semester: Optional[str] = None
    year_of_passing: Optional[str] = None
    domain: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)

class WizardStepRequest(BaseModel):
    step: int
    data: Optional[Dict[str, Any]] = None
