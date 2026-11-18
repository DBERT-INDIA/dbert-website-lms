"""
config/financial_config.py - Centralized Financial & Payment Ledger Configuration

Single source of truth for all fee schedules, caution deposits, stipend rewards,
referral commissions, and merchant UPI payment coordinates across the DBERT portal.
Each value supports runtime override via environment variables.
"""

import os
from typing import Dict, Any

# Program Fee Structure (INR)
CAUTION_DEPOSIT_INR: int = int(os.environ.get("DBERT_CAUTION_DEPOSIT_INR", "499"))
BALANCE_PAYABLE_INR: int = int(os.environ.get("DBERT_BALANCE_PAYABLE_INR", "1500"))
TOTAL_PROGRAM_FEE_INR: int = int(os.environ.get("DBERT_TOTAL_PROGRAM_FEE_INR", "1999"))
VERIFICATION_CERTIFICATE_FEE_INR: int = int(os.environ.get("DBERT_VERIFICATION_FEE_INR", "299"))

# Incentive & Rewards Structure
STIPEND_REWARD_COINS: int = int(os.environ.get("DBERT_STIPEND_REWARD_COINS", "5000"))
AMBASSADOR_COMMISSION_INR: int = int(os.environ.get("DBERT_AMBASSADOR_COMMISSION_INR", "200"))

# Merchant Payment Coordinates
PRIMARY_UPI_VPA: str = os.environ.get("DBERT_UPI_VPA", "Q652429146@ybl").strip()
PRIMARY_UPI_PAYEE_NAME: str = os.environ.get("DBERT_UPI_PAYEE_NAME", "DBERT Admissions").strip()
QR_CODE_IMAGE_PATH: str = os.environ.get("DBERT_QR_CODE_PATH", "/images/qrcode.jpeg").strip()

# Formatted currency helpers
def format_inr(amount: int) -> str:
    """Format amount as standard Indian Rupee string (e.g. ₹1,500)."""
    return f"₹{amount:,}"


def get_financial_context() -> Dict[str, Any]:
    """Returns a dict suitable for injection into template context processors or APIs."""
    return {
        "caution_deposit": CAUTION_DEPOSIT_INR,
        "caution_deposit_formatted": format_inr(CAUTION_DEPOSIT_INR),
        "balance_payable": BALANCE_PAYABLE_INR,
        "balance_payable_formatted": format_inr(BALANCE_PAYABLE_INR),
        "total_fee": TOTAL_PROGRAM_FEE_INR,
        "total_fee_formatted": format_inr(TOTAL_PROGRAM_FEE_INR),
        "verification_fee": VERIFICATION_CERTIFICATE_FEE_INR,
        "verification_fee_formatted": format_inr(VERIFICATION_CERTIFICATE_FEE_INR),
        "stipend_coins": STIPEND_REWARD_COINS,
        "stipend_coins_formatted": f"{STIPEND_REWARD_COINS:,}",
        "commission_inr": AMBASSADOR_COMMISSION_INR,
        "commission_formatted": format_inr(AMBASSADOR_COMMISSION_INR),
        "upi_vpa": PRIMARY_UPI_VPA,
        "upi_payee": PRIMARY_UPI_PAYEE_NAME,
        "qr_code_image": QR_CODE_IMAGE_PATH,
    }
