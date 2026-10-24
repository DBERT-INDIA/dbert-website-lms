import hmac
import hashlib
import uuid
from typing import Dict, Any, Optional, Tuple
import httpx

from backend.core.config import settings

RAZORPAY_API_URL = "https://api.razorpay.com/v1"

class RazorpayError(Exception):
    pass

class RazorpaySignatureVerificationError(RazorpayError):
    pass

def is_razorpay_configured() -> bool:
    return bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET)

def get_public_config() -> Dict[str, Any]:
    return {
        "enabled": is_razorpay_configured(),
        "key_id": settings.RAZORPAY_KEY_ID,
        "currency": "INR",
        "upi_id": settings.UPI_ID,
        "default_amount": settings.UPI_AMOUNT,
        "paid_program_amount": settings.PAID_PROGRAM_AMOUNT
    }

async def create_razorpay_order(amount_paise: int, receipt: str, notes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Create order in Razorpay (or mock in development if credentials unset)."""
    if not is_razorpay_configured():
        # Fallback simulation order for local dev
        return {
            "id": f"order_sim_{uuid.uuid4().hex[:12]}",
            "entity": "order",
            "amount": amount_paise,
            "amount_paid": 0,
            "amount_due": amount_paise,
            "currency": "INR",
            "receipt": receipt,
            "status": "created",
            "notes": notes or {}
        }

    async with httpx.AsyncClient(timeout=10.0) as client:
        auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        payload = {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": receipt,
            "notes": notes or {}
        }
        res = await client.post(f"{RAZORPAY_API_URL}/orders", json=payload, auth=auth)
        if res.status_code >= 400:
            raise RazorpayError(f"Razorpay API Error ({res.status_code}): {res.text}")
        return res.json()

def verify_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """Verify Razorpay payment signature via HMAC SHA256."""
    if not is_razorpay_configured():
        # In test/dev mode without secret, allow mock signature check
        if signature.startswith("sim_sig_") or settings.ENVIRONMENT == "development":
            return True

    secret = settings.RAZORPAY_KEY_SECRET.encode()
    message = f"{order_id}|{payment_id}".encode()
    generated_sig = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return hmac.compare_digest(generated_sig, signature)

def verify_webhook_signature(payload_bytes: bytes, signature: str) -> bool:
    """Verify webhook signature against raw request body."""
    if not settings.RAZORPAY_KEY_SECRET:
        return True
    secret = settings.RAZORPAY_KEY_SECRET.encode()
    generated = hmac.new(secret, payload_bytes, hashlib.sha256).hexdigest()
    return hmac.compare_digest(generated, signature)
