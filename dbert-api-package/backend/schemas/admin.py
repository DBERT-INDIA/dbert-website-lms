from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AdminStatsResponse(BaseModel):
    total_interns: int
    total_applications: int
    total_enrollments: int
    total_companies: int
    conversion_rate_pct: float

class AdminUserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None

class CronJobResult(BaseModel):
    job: str
    status: str
    items_affected: int
    duration_ms: float
