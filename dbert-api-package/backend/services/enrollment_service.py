from datetime import datetime, timezone
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models.portal import Enrollment, EnrollmentStatusHistory
from backend.services.application_service import transition_application, STATUS_ENROLLED, STATUS_ACCEPTED

ENROLLMENT_STATUS_PENDING  = "Pending Verification"
ENROLLMENT_STATUS_ACCEPTED = "Accepted"
ENROLLMENT_STATUS_REJECTED = "Rejected"
ENROLLMENT_STATUS_REFUNDED = "Refunded"

VALID_ENROLLMENT_STATUSES = {
    ENROLLMENT_STATUS_PENDING,
    ENROLLMENT_STATUS_ACCEPTED,
    ENROLLMENT_STATUS_REJECTED,
    ENROLLMENT_STATUS_REFUNDED,
}

VALID_ENROLLMENT_TRANSITIONS = {
    ENROLLMENT_STATUS_PENDING:  {ENROLLMENT_STATUS_ACCEPTED, ENROLLMENT_STATUS_REJECTED},
    ENROLLMENT_STATUS_REJECTED: {ENROLLMENT_STATUS_PENDING},
    ENROLLMENT_STATUS_ACCEPTED: {ENROLLMENT_STATUS_REJECTED, ENROLLMENT_STATUS_REFUNDED},
    ENROLLMENT_STATUS_REFUNDED: set(),
}

class EnrollmentStateMachineError(Exception):
    pass

class EnrollmentNotFoundError(EnrollmentStateMachineError):
    pass

class InvalidEnrollmentTransitionError(EnrollmentStateMachineError):
    pass

async def transition_enrollment(
    db: AsyncSession,
    enrollment_id: int,
    target_status: str,
    actor_role: str = "admin",
    actor_email: Optional[str] = None,
    reason: Optional[str] = None,
    request_id: Optional[str] = None
) -> Tuple[Enrollment, EnrollmentStatusHistory]:
    """Execute enrollment state transition and sync application status."""
    if target_status not in VALID_ENROLLMENT_STATUSES:
        raise InvalidEnrollmentTransitionError(f"Target status '{target_status}' is invalid.")

    stmt = select(Enrollment).where(Enrollment.id == enrollment_id)
    res = await db.execute(stmt)
    enrollment = res.scalar_one_or_none()
    if not enrollment:
        raise EnrollmentNotFoundError(f"Enrollment id {enrollment_id} not found.")

    current_status = enrollment.payment_status or ENROLLMENT_STATUS_PENDING
    if current_status == target_status:
        return enrollment, None

    if actor_role != "admin" and target_status not in VALID_ENROLLMENT_TRANSITIONS.get(current_status, set()):
        raise InvalidEnrollmentTransitionError(f"Illegal transition from '{current_status}' to '{target_status}'.")

    # Audit history
    history = EnrollmentStatusHistory(
        enrollment_id=enrollment.id,
        old_status=current_status,
        new_status=target_status,
        changed_by=actor_email or actor_role,
        reason=reason,
        request_id=request_id
    )
    db.add(history)

    enrollment.payment_status = target_status

    # Synchronize linked application if accepted
    if target_status == ENROLLMENT_STATUS_ACCEPTED and enrollment.application_id:
        try:
            await transition_application(
                db=db,
                application_id=enrollment.application_id,
                target_status=STATUS_ACCEPTED,
                actor_role="system",
                reason=f"Enrollment {enrollment.id} accepted and verified"
            )
        except Exception:
            pass

    await db.commit()
    await db.refresh(enrollment)
    return enrollment, history
