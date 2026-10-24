from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func
from backend.core.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=False)
    city = Column(String(100), nullable=False)
    college = Column(String(255), nullable=False)
    course = Column(String(100), nullable=False)
    semester = Column(String(50), nullable=False)
    year_of_passing = Column(String(50), nullable=False)
    domain = Column(String(100), nullable=False)
    why_join = Column(Text, nullable=False)
    portfolio = Column(Text, nullable=True)
    status = Column(String(50), default="Apply Pending", index=True)
    mentor_note = Column(Text, nullable=True)
    mentor_email = Column(String(255), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    visitor_id = Column(String(100), nullable=True)
    source = Column(String(50), default="web")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    rejected_at = Column(DateTime(timezone=True), nullable=True)
    enroll_reminders_sent = Column(Integer, default=0)
    last_reminder_at = Column(DateTime(timezone=True), nullable=True)
    intent_answers = Column(Text, nullable=True)


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, nullable=False, index=True)
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    changed_by = Column(String(255), nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(Text, nullable=True)
    request_id = Column(String(100), nullable=True)
    metadata_json = Column("metadata", Text, nullable=True)


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True)
    city = Column(String(100), nullable=True)
    college = Column(String(255), nullable=True)
    course = Column(String(100), nullable=True)
    semester = Column(String(50), nullable=True)
    year_of_passing = Column(String(50), nullable=True)
    domain = Column(String(100), nullable=True)
    joining_date = Column(String(50), nullable=True)
    batch_label = Column(String(100), nullable=True)
    payment_screenshot = Column(Text, nullable=True)
    payment_status = Column(String(50), default="Pending Verification", index=True)
    admin_note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    product = Column(String(50), default="free_deposit")
    amount = Column(Integer, nullable=True)
    razorpay_order_id = Column(String(100), nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    razorpay_signature = Column(Text, nullable=True)


class EnrollmentStatusHistory(Base):
    __tablename__ = "enrollment_status_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    enrollment_id = Column(Integer, nullable=False, index=True)
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    changed_by = Column(String(255), nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    reason = Column(Text, nullable=True)
    request_id = Column(String(100), nullable=True)
    metadata_json = Column("metadata", Text, nullable=True)


class PostApplication(Base):
    __tablename__ = "post_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, nullable=False, index=True)
    intern_id = Column(Integer, nullable=False, index=True)
    comment = Column(Text, nullable=False)
    cv_id = Column(Integer, nullable=True)
    status = Column(String(50), default="Applied")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    needed_certs_json = Column(Text, nullable=True)
    decision_note = Column(Text, nullable=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    notified_at = Column(DateTime(timezone=True), nullable=True)
    email = Column(String(255), nullable=True)


class SecurityDeposit(Base):
    __tablename__ = "security_deposits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    amount = Column(Integer, default=499)
    payment_screenshot = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    payment_type = Column(String(50), default="pending")
    razorpay_order_id = Column(String(100), nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    razorpay_signature = Column(Text, nullable=True)
    admin_note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)


class PostHireDeposit(Base):
    __tablename__ = "post_hire_deposits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_application_id = Column(Integer, nullable=False, index=True)
    intern_id = Column(Integer, nullable=False, index=True)
    post_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=True)
    payment_screenshot = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    admin_note = Column(Text, nullable=True)
    refunded_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    razorpay_order_id = Column(String(100), nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    razorpay_signature = Column(Text, nullable=True)
