from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func
from backend.core.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False, index=True)
    post_type = Column(String(50), default="internship")
    domain = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True, index=True)
    description = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    location = Column(String(100), default="Remote")
    work_mode = Column(String(50), default="Remote")
    stipend_min = Column(Integer, default=0)
    stipend_max = Column(Integer, default=0)
    pay_period = Column(String(50), default="month")
    is_unpaid = Column(Boolean, default=False)
    duration = Column(String(50), default="2 months")
    openings = Column(Integer, default=1)
    apply_by = Column(String(50), nullable=True)
    certifications_json = Column(Text, nullable=True)
    eligibility = Column(Text, nullable=True)
    status = Column(String(50), default="draft", index=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    views = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PostComment(Base):
    __tablename__ = "post_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, nullable=False, index=True)
    intern_id = Column(Integer, nullable=False, index=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PostQuestion(Base):
    __tablename__ = "post_questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, nullable=False, index=True)
    company_id = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    sort_order = Column(Integer, default=1)
    status = Column(String(50), default="active")
    options = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Cohort(Base):
    __tablename__ = "cohorts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    skills = Column(Text, nullable=True)
    platform = Column(String(100), default="Google Meet")
    meeting_url = Column(Text, nullable=True)
    starts_at = Column(DateTime(timezone=True), nullable=True)
    capacity = Column(Integer, default=30)
    status = Column(String(50), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ScrapedInternship(Base):
    __tablename__ = "scraped_internships"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Domain = Column(String(100), nullable=True, index=True)
    Company = Column(String(255), nullable=True)
    Role = Column(String(255), nullable=True)
    Location = Column(String(100), nullable=True)
    Is_Remote = Column(String(20), default="Yes")
    Start_Date = Column(String(50), nullable=True)
    End_Date = Column(String(50), nullable=True)
    Stipend = Column(String(100), nullable=True)
    URL = Column(Text, nullable=True)
    Description = Column(Text, nullable=True)
    Source = Column(String(100), default="web")
    Region = Column(String(100), nullable=True)
    Stipend_Normalized = Column(String(100), nullable=True)
    Work_Model = Column(String(50), default="Remote")
    City = Column(String(100), nullable=True)
    Clicks = Column(Integer, default=0)


class ScrapedInternshipComment(Base):
    __tablename__ = "scraped_internship_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(Integer, nullable=False, index=True)
    intern_id = Column(Integer, nullable=False)
    intern_name = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
