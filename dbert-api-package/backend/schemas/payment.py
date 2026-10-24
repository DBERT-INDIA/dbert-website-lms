from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class CreateOrderRequest(BaseModel):
    amount: int = Field(..., description="Amount in INR (e.g. 499)")
    receipt: Optional[str] = "rcpt_portal"
    notes: Optional[Dict[str, Any]] = None

class CreateOrderResponse(BaseModel):
    order_id: str
    amount: int
    currency: str
    key_id: str

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    application_id: Optional[int] = None
    enrollment_id: Optional[int] = None
    course_id: Optional[int] = None
    amount: Optional[int] = None

class VerifyPaymentResponse(BaseModel):
    status: str
    message: str
    payment_id: str
