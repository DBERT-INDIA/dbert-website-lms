from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.dependencies import require_intern
from backend.models.features import Task, TaskSubmission, CoinLedgerMirror

router = APIRouter(prefix="/tasks", tags=["Intern Workspace"])

class TaskSubmissionRequest(BaseModel):
    submission_content: str
    submission_file: str = None

@router.get("", summary="List Available Tasks")
async def list_tasks(
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Task).where(Task.is_active == True).order_by(Task.id.desc())
    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/{task_id}", summary="Get Task Details")
async def get_task_detail(task_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Task).where(Task.id == task_id)
    res = await db.execute(stmt)
    task = res.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.post("/{task_id}/submit", summary="Submit Task Deliverable")
async def submit_task(
    task_id: int,
    req: TaskSubmissionRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    sub = TaskSubmission(
        intern_id=user_id,
        task_id=task_id,
        submission_content=req.submission_content,
        submission_file=req.submission_file,
        status="submitted",
        email=current_user.get("email")
    )
    db.add(sub)
    await db.commit()
    return {"status": "success", "message": "Task submitted for evaluation"}
