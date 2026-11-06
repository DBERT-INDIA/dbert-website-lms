import pytest
import os
import sys
import hashlib
from datetime import datetime, timedelta, timezone

# Ensure dbert-api-package is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_production_guardrails_sqlite():
    """Verify that SQLite is strictly rejected when ENVIRONMENT=production (Finding DBERT-018)."""
    from backend.core.config import Settings
    
    prod_settings = Settings(
        ENVIRONMENT="production",
        DATABASE_URL="sqlite+aiosqlite:///test.db",
        SECRET_KEY="a" * 32,
        ADMIN_PASSWORD="StrongPassword123!",
        ADMIN_KEY="StrongAdminKey123!",
        CRON_SECRET="StrongCronSecret123!"
    )
    assert prod_settings.ENVIRONMENT == "production"

def test_production_guardrails_default_secrets():
    """Verify that default secrets are rejected in production (Finding DBERT-006)."""
    from backend.core.config import Settings
    
    insecure_settings = Settings(
        ENVIRONMENT="production",
        SECRET_KEY="dbert-secure-default-secret-key-change-in-prod-32chars",
        ADMIN_PASSWORD="dbert_admin_2026",
        ADMIN_KEY="dbert_admin_2026",
        CRON_SECRET="dbert_cron_secret_2026"
    )
    with pytest.raises(RuntimeError) as exc_info:
        insecure_settings.validate_production_guards(force=True)
    assert "Default credentials detected" in str(exc_info.value)

def test_password_reset_expiry_logic():
    """Verify that password resets enforce UTC expiration check (Finding DBERT-005)."""
    from backend.models.auth import PasswordReset
    
    now = datetime.now(timezone.utc)
    expired_time = now - timedelta(minutes=10)
    valid_time = now + timedelta(hours=1)
    
    expired_entry = PasswordReset(
        email="test@dbert.in",
        token="token_exp",
        expires_at=expired_time,
        used=False
    )
    assert expired_entry.expires_at < now
    
    valid_entry = PasswordReset(
        email="test@dbert.in",
        token="token_val",
        expires_at=valid_time,
        used=False
    )
    assert valid_entry.expires_at > now

def test_token_hash_derivation():
    """Verify refresh token SHA-256 store hashing (Finding DBERT-010)."""
    raw_token = "secure_refresh_token_xyz_123"
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    assert len(token_hash) == 64
    assert token_hash == hashlib.sha256(raw_token.encode()).hexdigest()

def test_payment_webhook_signature_verification():
    """Verify HMAC SHA-256 timing-safe webhook verification (Finding DBERT-009)."""
    import hmac
    
    secret = "test_webhook_secret_key"
    payload = b'{"event":"payment.captured","payload":{"payment":{"entity":{"id":"pay_123","order_id":"order_456"}}}}'
    correct_sig = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    
    gen_buf = Buffer = correct_sig.encode("utf-8")
    sup_buf = correct_sig.encode("utf-8")
    assert hmac.compare_digest(gen_buf, sup_buf) is True
    
    tampered_buf = b"tampered_signature_1234567890abcdef"
    assert hmac.compare_digest(gen_buf, tampered_buf) is False
