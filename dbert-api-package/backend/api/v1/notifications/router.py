from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func

from backend.core.database import get_db
from backend.core.dependencies import get_current_user_token
from backend.models.features import Notification

router = APIRouter(prefix="/notifications", tags=["Messaging & Alerts"])

@router.get("", summary="Get User Notifications")
async def list_notifications(
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    stmt = select(Notification).where(Notification.intern_id == user_id).order_by(Notification.created_at.desc()).limit(limit)
    res = await db.execute(stmt)
    notifications = res.scalars().all()

    unread_stmt = select(func.count(Notification.id)).where(Notification.intern_id == user_id, Notification.is_read == False)
    unread_count = (await db.execute(unread_stmt)).scalar() or 0

    return {
        "unread_count": unread_count,
        "notifications": notifications
    }

@router.post("/{notification_id}/read", summary="Mark Single Notification as Read")
async def mark_notification_read(
    notification_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    stmt = update(Notification).where(Notification.id == notification_id).values(is_read=True)
    await db.execute(stmt)
    await db.commit()
    return {"status": "success"}

@router.post("/read-all", summary="Mark All Notifications as Read")
async def mark_all_read(
    current_user: Dict[str, Any] = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    stmt = update(Notification).where(Notification.intern_id == user_id).values(is_read=True)
    await db.execute(stmt)
    await db.commit()
    return {"status": "success"}
