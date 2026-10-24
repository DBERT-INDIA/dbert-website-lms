from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: str = Field(..., description="User email address or username")
    password: str = Field(..., min_length=4, description="User password")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Dict[str, Any]

class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., description="Valid refresh token")

class SignupStage1Request(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str = Field(..., min_length=10)
    password: str = Field(..., min_length=6)
    referral_code: Optional[str] = None

class SignupStage2Request(BaseModel):
    domain: str = Field(..., description="Selected career domain")
    city: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

class SignupStage3Request(BaseModel):
    college: str
    course: str
    semester: str
    year_of_passing: str

class CompanySignupRequest(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)
    phone: Optional[str] = None
    website: Optional[str] = None
    about: Optional[str] = None

class CheckEmailRequest(BaseModel):
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    account_type: Optional[str] = "intern"

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)

class OtpSendRequest(BaseModel):
    email: EmailStr

class OtpVerifyRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=10)
