from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    counterparty_type = Column(String(50), nullable=False)
    counterparty_id = Column(Integer, nullable=False, index=True)
    post_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, nullable=False, index=True)
    sender_type = Column(String(50), nullable=False)
    sender_id = Column(Integer, nullable=False)
    body = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    kind = Column(String(50), default="system")
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    link = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, unique=True, nullable=False, index=True)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    headline = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    skills_json = Column(Text, nullable=True)
    projects_json = Column(Text, nullable=True)
    experience_json = Column(Text, nullable=True)
    education_json = Column(Text, nullable=True)
    links_json = Column(Text, nullable=True)
    is_public = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class InternCertificate(Base):
    __tablename__ = "intern_certificates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, nullable=False)
    course_title = Column(String(255), nullable=False)
    cert_id = Column(String(100), unique=True, nullable=False, index=True)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    url = Column(Text, nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=True)
    tier = Column(String(50), default="verified")
    email = Column(String(255), nullable=True)


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    referrer_intern_id = Column(Integer, nullable=False, index=True)
    referred_email = Column(String(255), nullable=True)
    referred_intern_id = Column(Integer, nullable=True)
    source_code = Column(String(100), nullable=True)
    status = Column(String(50), default="registered")
    flagged = Column(Boolean, default=False)
    flag_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AmbassadorWithdrawal(Base):
    __tablename__ = "ambassador_withdrawals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, nullable=False)
    status = Column(String(50), default="requested")
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_by_admin_id = Column(Integer, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    admin_note = Column(Text, nullable=True)
    upi_viewed_by = Column(String(255), nullable=True)
    upi_viewed_at = Column(DateTime(timezone=True), nullable=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    coin_reward = Column(Integer, default=50)
    is_active = Column(Boolean, default=True)
    author_type = Column(String(50), default="admin")
    author_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    task_type = Column(String(50), default="general")
    target_domain = Column(String(100), nullable=True)
    payment_type = Column(String(50), default="coins")
    submission_type = Column(String(50), default="link")


class TaskSubmission(Base):
    __tablename__ = "task_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    task_id = Column(Integer, nullable=False, index=True)
    task_version_id = Column(Integer, default=1)
    submission_content = Column(Text, nullable=False)
    status = Column(String(50), default="submitted")
    coins_awarded = Column(Integer, default=0)
    reviewed_by_staff_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    submission_file = Column(Text, nullable=True)
    email = Column(String(255), nullable=True)


class CoinLedgerMirror(Base):
    __tablename__ = "coin_ledger_mirror"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    ledger_kind = Column(String(50), nullable=False)
    delta = Column(Integer, nullable=False)
    balance_after = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=False)
    event_ts = Column(DateTime(timezone=True), server_default=func.now())
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    idem_key = Column(String(100), unique=True, nullable=True)
    email = Column(String(255), nullable=True)


class CohortEnrollment(Base):
    __tablename__ = "cohort_enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cohort_id = Column(Integer, ForeignKey("cohorts.id"), nullable=False)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    reminder_sent = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CompanyFollow(Base):
    __tablename__ = "company_follows"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TaskVersion(Base):
    __tablename__ = "task_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    instructions = Column(Text, nullable=False)
    rubric = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MentorAvailabilitySlot(Base):
    __tablename__ = "mentor_availability_slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mentor_staff_id = Column(Integer, ForeignKey("staff_accounts.id"), nullable=False)
    start_time = Column(String(50), nullable=False)
    end_time = Column(String(50), nullable=False)
    is_booked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MentorSessionBooking(Base):
    __tablename__ = "mentor_session_bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slot_id = Column(Integer, ForeignKey("mentor_availability_slots.id"), nullable=False)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    meeting_link = Column(Text, nullable=True)
    status = Column(String(50), default="booked")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InternArticle(Base):
    __tablename__ = "intern_articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    domain = Column(String(100), nullable=True)
    title = Column(String(255), nullable=False)
    content_markdown = Column(Text, nullable=False)
    status = Column(String(50), default="DRAFT")
    mentor_feedback = Column(Text, nullable=True)
    published_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EcosystemSpotlight(Base):
    __tablename__ = "ecosystem_spotlights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=False)
    target_brand = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SpotlightClick(Base):
    __tablename__ = "spotlight_clicks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=True)
    spotlight_id = Column(Integer, nullable=True)
    clicked_at = Column(DateTime(timezone=True), server_default=func.now())

