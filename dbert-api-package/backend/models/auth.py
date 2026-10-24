from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base

class InternAccount(Base):
    __tablename__ = "intern_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    city = Column(String(100), nullable=True)
    college = Column(String(255), nullable=True)
    course = Column(String(100), nullable=True)
    semester = Column(String(50), nullable=True)
    year_of_passing = Column(String(50), nullable=True)
    domain = Column(String(100), nullable=True)
    password_hash = Column(Text, nullable=True)
    password_set = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    tutor_completion_pct = Column(Float, default=0.0)
    tutor_updated_at = Column(DateTime(timezone=True), nullable=True)
    tutor_seconds_credited = Column(Integer, default=0)
    tutor_week_credited = Column(String(50), default="")
    linkedin_url = Column(Text, nullable=True)
    github_url = Column(Text, nullable=True)
    interview_attempts = Column(Integer, default=0)
    interview_last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    interview_locked = Column(Boolean, default=False)
    terms_accepted_at = Column(DateTime(timezone=True), nullable=True)
    newsletter_opt_in = Column(Boolean, default=False)
    signup_stage = Column(Integer, default=3)
    referral_code = Column(String(100), nullable=True)
    referred_by_intern_id = Column(BigInteger, nullable=True)
    upi_id_encrypted = Column(Text, nullable=True)
    email_verified = Column(Boolean, default=False)
    account_status = Column(String(50), default="active")
    visitor_id = Column(String(100), nullable=True)
    program = Column(String(100), default="fellowship")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    about = Column(Text, nullable=True)
    password_hash = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    domain = Column(String(100), nullable=False)
    password_hash = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class StaffAccount(Base):
    __tablename__ = "staff_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(String(50), default="staff")


class MobileRefreshToken(Base):
    __tablename__ = "mobile_refresh_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token_hash = Column(String(255), nullable=False, unique=True, index=True)
    intern_id = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)


class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    account_type = Column(String(50), default="intern")
    account_id = Column(Integer, nullable=True)
    used_at = Column(DateTime(timezone=True), nullable=True)


class SignupOtp(Base):
    __tablename__ = "signup_otps"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, index=True)
    otp = Column(String(20), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    role = Column(String(50), default="intern")
    session_token = Column(String(255), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    next_url = Column(Text, nullable=True)


class UserApiKey(Base):
    __tablename__ = "user_api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    encrypted_key = Column(Text, nullable=False)
    key_hash = Column(String(255), nullable=True)
    validated_at = Column(DateTime(timezone=True), server_default=func.now())
    available_models_json = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StaffQueueRole(Base):
    __tablename__ = "staff_queue_roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey("staff_accounts.id"), nullable=False)
    queue_name = Column(String(100), nullable=False)

