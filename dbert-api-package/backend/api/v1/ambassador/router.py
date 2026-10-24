from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.dependencies import require_intern
from backend.models.features import Referral, AmbassadorWithdrawal
from backend.models.auth import InternAccount

router = APIRouter(prefix="/ambassador", tags=["Intern Workspace"])

class WithdrawalRequest(BaseModel):
    amount: int
    upi_id: str

@router.get("", summary="Get Campus Ambassador Stats")
async def get_ambassador_dashboard(
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    ref_stmt = select(func.count(Referral.id)).where(Referral.referrer_intern_id == user_id)
    total_referrals = (await db.execute(ref_stmt)).scalar() or 0

    return {
        "referral_code": f"DBERT{user_id:04d}",
        "total_referrals": total_referrals,
        "earned_inr": total_referrals * 100,
        "available_balance_inr": total_referrals * 100
    }

@router.post("/withdraw", summary="Request Ambassador Earnings Payout")
async def request_withdrawal(
    req: WithdrawalRequest,
    current_user: Dict[str, Any] = Depends(require_intern),
    db: AsyncSession = Depends(get_db)
):
    user_id = int(current_user.get("sub"))
    if req.amount < 500:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Minimum withdrawal amount is ₹500.")

    withdrawal = AmbassadorWithdrawal(
        intern_id=user_id,
        amount=req.amount,
        status="requested"
    )
    db.add(withdrawal)
    await db.commit()
    return {"status": "success", "message": "Withdrawal request submitted for review"}
