"""Payment status endpoint for clients using the modular routes."""

from flask import Blueprint, jsonify
from services.payment_service import PaymentService


payment_bp = Blueprint("payment", __name__)


@payment_bp.get("/api/payment/status")
def api_payment_status():
    """Return payment gateway availability and the public configuration."""
    return jsonify({
        "status": "success",
        "gateway_enabled": PaymentService.is_enabled(),
        "config": PaymentService.get_client_config(),
    })
