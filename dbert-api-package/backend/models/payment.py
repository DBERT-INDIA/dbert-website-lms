from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func
from backend.core.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mentor_email = Column(String(255), nullable=False)
    intern_name = Column(String(255), nullable=True)
    course_title = Column(String(255), nullable=True)
    amount = Column(Integer, nullable=True)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PaymentEvent(Base):
    __tablename__ = "payment_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(100), unique=True, nullable=False, index=True)
    event_type = Column(String(100), nullable=False)
    payload = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="processed")


class CoursePayment(Base):
    __tablename__ = "course_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    course_id = Column(Integer, nullable=False, index=True)
    course_title = Column(String(255), nullable=True)
    amount = Column(Integer, nullable=True)
    payment_screenshot = Column(Text, nullable=True)
    status = Column(String(50), default="pending", index=True)
    admin_note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)
    platform_commission_pct = Column(Float, default=15.0)
    author_earnings_inr = Column(Integer, default=0)
    commission_pct_snapshot = Column(Float, default=0.0)
    commission_amount = Column(Float, default=0.0)
    payee_type = Column(String(50), default="admin")
    settled_at = Column(DateTime(timezone=True), nullable=True)
    razorpay_order_id = Column(String(100), nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    razorpay_signature = Column(Text, nullable=True)
