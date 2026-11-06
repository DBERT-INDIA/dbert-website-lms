import json
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.core.config import settings
from backend.core.database import get_db
from backend.services.razorpay_client import (
    get_public_config, create_razorpay_order, verify_payment_signature,
    verify_webhook_signature, RazorpayError
)
from backend.models.payment import Payment, PaymentEvent
from backend.models.portal import Enrollment, SecurityDeposit
from backend.schemas.payment import (
    CreateOrderRequest, CreateOrderResponse, VerifyPaymentRequest, VerifyPaymentResponse
)

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.get("/config", summary="Get Razorpay Public Configuration")
async def get_payment_config():
    """Returns frontend public configuration (key_id, currency, amounts)."""
    return get_public_config()

@router.post("/razorpay/create-order", response_model=CreateOrderResponse, summary="Create Razorpay Order")
async def create_order(req: CreateOrderRequest):
    """Creates a server-side order with Razorpay in paise."""
    amount_paise = req.amount * 100
    try:
        order = await create_razorpay_order(
            amount_paise=amount_paise,
            receipt=req.receipt or "rcpt",
            notes=req.notes
        )
        return CreateOrderResponse(
            order_id=order["id"],
            amount=req.amount,
            currency="INR",
            key_id=settings.RAZORPAY_KEY_ID
        )
    except RazorpayError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

@router.post("/razorpay/verify-payment", response_model=VerifyPaymentResponse, summary="Verify Payment Signature")
async def verify_payment(req: VerifyPaymentRequest, db: AsyncSession = Depends(get_db)):
    """Verifies HMAC signature and records verified payment."""
    is_valid = verify_payment_signature(
        order_id=req.razorpay_order_id,
        payment_id=req.razorpay_payment_id,
        signature=req.razorpay_signature
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid cryptographic payment signature"
        )

    # Update enrollment if provided
    if req.enrollment_id:
        stmt = select(Enrollment).where(Enrollment.id == req.enrollment_id)
        res = await db.execute(stmt)
        enrollment = res.scalar_one_or_none()
        if enrollment:
            enrollment.payment_status = "Accepted"
            enrollment.razorpay_order_id = req.razorpay_order_id
            enrollment.razorpay_payment_id = req.razorpay_payment_id
            enrollment.razorpay_signature = req.razorpay_signature

    await db.commit()
    return VerifyPaymentResponse(
        status="success",
        message="Payment verified successfully",
        payment_id=req.razorpay_payment_id
    )

@router.post("/razorpay/webhook", summary="Process Razorpay Webhook Events")
async def handle_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """Idempotently process incoming Razorpay webhooks."""
    body_bytes = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")

    if not verify_webhook_signature(body_bytes, signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid webhook signature")

    payload = json.loads(body_bytes.decode("utf-8"))
    event_id = payload.get("event_id") or payload.get("id") or str(request.headers.get("X-Request-ID"))
    event_type = payload.get("event", "unknown")

    # Check idempotency
    stmt = select(PaymentEvent).where(PaymentEvent.event_id == event_id)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        return {"status": "ignored", "reason": "duplicate event"}

    # Reconcile enrollment on payment capture (Finding DBERT-009)
    if event_type in ("payment.captured", "order.paid"):
        payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        order_id = payment_entity.get("order_id") or payload.get("payload", {}).get("order", {}).get("entity", {}).get("id")
        payment_id = payment_entity.get("id")

        if order_id:
            enr_stmt = select(Enrollment).where(Enrollment.razorpay_order_id == order_id)
            enr_res = await db.execute(enr_stmt)
            enr = enr_res.scalar_one_or_none()
            if enr:
                enr.payment_status = "Accepted"
                if payment_id:
                    enr.razorpay_payment_id = payment_id

    db.add(PaymentEvent(
        event_id=event_id,
        event_type=event_type,
        payload=json.dumps(payload),
        status="processed"
    ))
    await db.commit()
    return {"status": "success", "event_id": event_id}
