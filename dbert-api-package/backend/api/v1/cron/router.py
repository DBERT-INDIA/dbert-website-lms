import time
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from backend.core.database import get_db
from backend.core.dependencies import verify_cron_secret
from backend.models.auth import MobileRefreshToken
from backend.services.outbox_service import process_outbox_queue
from backend.schemas.admin import CronJobResult

router = APIRouter(prefix="/cron", tags=["Scheduled Cron"])

@router.post("/clean-tokens", response_model=CronJobResult, summary="Purge Expired Refresh Tokens")
async def clean_expired_tokens(
    authorized: bool = Depends(verify_cron_secret),
    db: AsyncSession = Depends(get_db)
):
    start = time.perf_counter()
    now = datetime.now(timezone.utc)
    stmt = delete(MobileRefreshToken).where(MobileRefreshToken.expires_at < now)
    res = await db.execute(stmt)
    await db.commit()
    deleted = res.rowcount or 0
    duration = (time.perf_counter() - start) * 1000.0

    return CronJobResult(
        job="clean_expired_tokens",
        status="success",
        items_affected=deleted,
        duration_ms=round(duration, 2)
    )

@router.post("/process-outbox", summary="Process Queued Outbox Events")
async def process_outbox(
    authorized: bool = Depends(verify_cron_secret),
    db: AsyncSession = Depends(get_db)
):
    result = await process_outbox_queue(db)
    return {"status": "success", "result": result}

@router.post("/enrollment-reminders", summary="Send Scheduled Enrollment Reminders")
async def send_enrollment_reminders(authorized: bool = Depends(verify_cron_secret)):
    return {"status": "success", "reminders_sent": 0}

@router.post("/cohort-reminders", summary="Send Scheduled Cohort Reminders")
async def send_cohort_reminders(authorized: bool = Depends(verify_cron_secret)):
    return {"status": "success", "reminders_sent": 0}

@router.post("/expire-posts", summary="Expire Outdated Job and Internship Listings")
async def expire_posts(authorized: bool = Depends(verify_cron_secret)):
    return {"status": "success", "expired_count": 0}
