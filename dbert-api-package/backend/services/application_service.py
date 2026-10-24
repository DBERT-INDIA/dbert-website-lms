import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from backend.models.portal import Application, ApplicationStatusHistory

STATUS_APPLY_PENDING      = "Apply Pending"
STATUS_UNDER_REVIEW       = "Under Review"
STATUS_ON_HOLD            = "On Hold"
STATUS_SELECTED           = "Selected"
STATUS_ENROLLMENT_PENDING = "Enrollment Pending"
STATUS_ENROLLED           = "Enrolled"
STATUS_ACCEPTED           = "Accepted"
STATUS_REJECTED           = "Rejected"
STATUS_PAID_ENROLLED      = "Paid-Enrolled"

VALID_APPLICATION_STATUSES = {
    STATUS_APPLY_PENDING,
    STATUS_UNDER_REVIEW,
    STATUS_ON_HOLD,
    STATUS_SELECTED,
    STATUS_ENROLLMENT_PENDING,
    STATUS_ENROLLED,
    STATUS_ACCEPTED,
    STATUS_REJECTED,
    STATUS_PAID_ENROLLED,
}

VALID_APP_TRANSITIONS: Dict[str, set] = {
    STATUS_APPLY_PENDING:      {STATUS_UNDER_REVIEW, STATUS_REJECTED},
    STATUS_UNDER_REVIEW:       {STATUS_ON_HOLD, STATUS_SELECTED, STATUS_REJECTED},
    STATUS_ON_HOLD:            {STATUS_UNDER_REVIEW, STATUS_SELECTED, STATUS_REJECTED},
    STATUS_SELECTED:           {STATUS_ENROLLMENT_PENDING, STATUS_ENROLLED, STATUS_ACCEPTED, STATUS_PAID_ENROLLED, STATUS_REJECTED},
    STATUS_ENROLLMENT_PENDING: {STATUS_ENROLLED, STATUS_ACCEPTED, STATUS_SELECTED, STATUS_REJECTED, STATUS_PAID_ENROLLED},
    STATUS_ENROLLED:           {STATUS_ACCEPTED, STATUS_ENROLLMENT_PENDING, STATUS_REJECTED},
    STATUS_ACCEPTED:           {STATUS_ENROLLED, STATUS_REJECTED},
    STATUS_PAID_ENROLLED:      {STATUS_ACCEPTED, STATUS_ENROLLED, STATUS_REJECTED},
    STATUS_REJECTED:           {STATUS_UNDER_REVIEW},
}

class ApplicationStateMachineError(Exception):
    pass

class ApplicationNotFoundError(ApplicationStateMachineError):
    pass

class InvalidTransitionError(ApplicationStateMachineError):
    pass

class UnauthorizedTransitionError(ApplicationStateMachineError):
    pass

async def transition_application(
    db: AsyncSession,
    application_id: int,
    target_status: str,
    actor_role: str = "admin",
    actor_email: Optional[str] = None,
    reason: Optional[str] = None,
    mentor_note: Optional[str] = None,
    request_id: Optional[str] = None
) -> Tuple[Application, ApplicationStatusHistory]:
    """Execute state transition with validation, permission enforcement, and history tracking."""
    if target_status not in VALID_APPLICATION_STATUSES:
        raise InvalidTransitionError(f"Target status '{target_status}' is not a recognized application status.")

    stmt = select(Application).where(Application.id == application_id)
    res = await db.execute(stmt)
    app = res.scalar_one_or_none()
    if not app:
        raise ApplicationNotFoundError(f"Application id {application_id} not found.")

    current_status = app.status or STATUS_APPLY_PENDING
    if current_status == target_status:
        # No-op: status is already target
        return app, None

    allowed_targets = VALID_APP_TRANSITIONS.get(current_status, set())
    # Admin is granted override for workflow correction
    if actor_role != "admin" and target_status not in allowed_targets:
        raise InvalidTransitionError(f"Illegal transition jump from '{current_status}' to '{target_status}'.")

    # Mentor role guards
    if actor_role == "mentor" and target_status not in {STATUS_UNDER_REVIEW, STATUS_ON_HOLD, STATUS_SELECTED, STATUS_REJECTED}:
        raise UnauthorizedTransitionError(f"Mentor is not authorized to move application to '{target_status}'.")

    # Record audit history
    history = ApplicationStatusHistory(
        application_id=app.id,
        old_status=current_status,
        new_status=target_status,
        changed_by=actor_email or actor_role,
        reason=reason,
        request_id=request_id
    )
    db.add(history)

    # Update application
    app.status = target_status
    if mentor_note:
        app.mentor_note = mentor_note
    if actor_role == "mentor" and actor_email:
        app.mentor_email = actor_email
        app.reviewed_at = datetime.now(timezone.utc)
    if target_status == STATUS_REJECTED:
        app.rejected_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(app)
    return app, history
