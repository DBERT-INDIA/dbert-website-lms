from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.sql import func
from backend.core.database import Base

class AbuseLog(Base):
    __tablename__ = "abuse_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip = Column(String(50), nullable=False)
    route = Column(String(255), nullable=False)
    bucket = Column(String(100), nullable=False)
    reason = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)


class EventOutbox(Base):
    __tablename__ = "event_outbox"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(100), nullable=False, index=True)
    aggregate_type = Column(String(100), nullable=False)
    aggregate_id = Column(String(100), nullable=False)
    payload_json = Column(Text, nullable=False)
    status = Column(String(50), default="pending", index=True)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=5)
    next_retry_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    processed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EmailLog(Base):
    __tablename__ = "email_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=False)
    email_sent = Column(String(20), default="sent")
    opened_at = Column(DateTime(timezone=True), nullable=True)


class DeviceProfile(Base):
    __tablename__ = "device_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    visitor_id = Column(String(100), nullable=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    screen_res = Column(String(50), nullable=True)
    timezone = Column(String(50), nullable=True)
    language = Column(String(50), nullable=True)
    device_type = Column(String(50), nullable=True)
    referrer = Column(Text, nullable=True)
    is_return_visit = Column(Boolean, default=False)
    visit_count = Column(Integer, default=1)
    time_on_page = Column(Integer, default=0)
    intent_score = Column(Integer, default=0)
    path = Column(String(255), nullable=True)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, nullable=False, index=True)
    week_start = Column(String(50), nullable=False)
    week_end = Column(String(50), nullable=False)
    total_minutes = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(String(255), nullable=True)


class CheckLog(Base):
    __tablename__ = "check_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(String(255), nullable=False)
    name = Column(String(255), nullable=True)
    check_count = Column(Integer, default=1)
    ip = Column(String(50), nullable=True)


class DbertFallbackUsage(Base):
    __tablename__ = "dbert_fallback_usage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intern_id = Column(Integer, ForeignKey("intern_accounts.id"), nullable=False)
    usage_date = Column(DateTime(timezone=True), server_default=func.now())
    count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PlatformConfig(Base):
    __tablename__ = "platform_config"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class RateEvent(Base):
    __tablename__ = "rate_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bucket = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReviewLog(Base):
    __tablename__ = "review_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    queue_name = Column(String(100), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff_accounts.id"), nullable=False)
    subject_type = Column(String(100), nullable=False)
    subject_id = Column(Integer, nullable=False)
    decision = Column(String(50), nullable=False)
    reason_code = Column(String(100), nullable=True)
    reviewed_input_snapshot = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

