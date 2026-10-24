import csv
import io
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from backend.core.database import get_db
from backend.core.dependencies import require_admin
from backend.models.auth import InternAccount, Company, Mentor, StaffAccount, MobileRefreshToken
from backend.models.portal import Application, Enrollment
from backend.models.admin import AbuseLog, Attendance
from backend.services.telemetry_service import get_telemetry_snapshot
from backend.schemas.admin import AdminStatsResponse, AdminUserUpdateRequest

router = APIRouter(prefix="/admin", tags=["Admin Control Plane"])

@router.get("/stats", response_model=AdminStatsResponse, summary="Get Platform Metrics Snapshot")
async def get_admin_stats(
    current_user: Dict[str, Any] = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    intern_count = (await db.execute(select(func.count(InternAccount.id)))).scalar() or 0
    app_count = (await db.execute(select(func.count(Application.id)))).scalar() or 0
    enroll_count = (await db.execute(select(func.count(Enrollment.id)))).scalar() or 0
    comp_count = (await db.execute(select(func.count(Company.id)))).scalar() or 0

    conv_rate = (enroll_count / app_count * 100.0) if app_count else 0.0

    return AdminStatsResponse(
        total_interns=intern_count,
        total_applications=app_count,
        total_enrollments=enroll_count,
        total_companies=comp_count,
        conversion_rate_pct=round(conv_rate, 2)
    )

@router.get("/applications", summary="List All Applications")
async def list_applications(
    status: Optional[str] = None,
    domain: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: Dict[str, Any] = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application)
    if status:
        stmt = stmt.where(Application.status == status)
    if domain:
        stmt = stmt.where(Application.domain == domain)
    stmt = stmt.order_by(Application.created_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/enrollments", summary="List All Enrollments")
async def list_enrollments(
    limit: int = 50,
    offset: int = 0,
    current_user: Dict[str, Any] = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Enrollment).order_by(Enrollment.created_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/users", summary="List All Intern Users")
async def list_users(
    limit: int = 50,
    offset: int = 0,
    current_user: Dict[str, Any] = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(InternAccount).order_by(InternAccount.created_at.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/abuse-log", summary="Get Abuse and Rate Limit Events")
async def get_abuse_log(
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(AbuseLog).order_by(AbuseLog.timestamp.desc()).limit(limit)
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/telemetry", summary="Get Live System Telemetry")
async def get_telemetry(current_user: Dict[str, Any] = Depends(require_admin)):
    return get_telemetry_snapshot()

@router.get("/csv/applications", summary="Export Applications as CSV")
async def export_applications_csv(
    current_user: Dict[str, Any] = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application).order_by(Application.id.desc())
    res = await db.execute(stmt)
    apps = res.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Email", "Phone", "Domain", "Status", "College", "Course", "Created At"])
    for a in apps:
        writer.writerow([a.id, a.name, a.email, a.phone, a.domain, a.status, a.college, a.course, a.created_at])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=applications_export.csv"}
    )
