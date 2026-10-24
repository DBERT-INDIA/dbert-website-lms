from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from backend.core.database import Base

class TimestampMixin:
    """Standard timestamp mixin adding created_at and updated_at to models."""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True)
