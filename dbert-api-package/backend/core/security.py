import time
import re
import hmac
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from backend.core.config import settings

ALGORITHM = "HS256"
_LEGACY_HASH_RE = re.compile(r"^[0-9a-f]{64}$")

def hash_password(password: str) -> str:
    """Hash password using salted PBKDF2:SHA256 (matches werkzeug & Flask portal format)."""
    return generate_password_hash(password or "", method="pbkdf2:sha256")

def is_legacy_hash(stored_hash: str) -> bool:
    """Detect old unsalted SHA-256 64-hex hash from legacy SQLite tables."""
    return bool(stored_hash) and bool(_LEGACY_HASH_RE.match(stored_hash))

def verify_password(stored_hash: str, plain_password: str) -> bool:
    """Verify password supporting both new salted KDF and legacy SHA-256."""
    if not stored_hash or not plain_password:
        return False
    if is_legacy_hash(stored_hash):
        legacy_digest = hashlib.sha256(plain_password.encode()).hexdigest()
        return hmac.compare_digest(stored_hash, legacy_digest)
    try:
        return check_password_hash(stored_hash, plain_password)
    except Exception:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create short-lived JWT access token (1 hour default)."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(seconds=settings.ACCESS_TOKEN_TTL)
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": secrets.token_hex(16),
        "type": "access"
    })
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create long-lived JWT refresh token (60 days default)."""
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(seconds=settings.REFRESH_TOKEN_TTL)
    to_encode.update({
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": secrets.token_hex(16),
        "type": "refresh"
    })
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token signature and expiration."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

def encrypt_pii(plaintext: str) -> str:
    """Encrypt sensitive PII (such as ambassador UPI IDs) using Fernet if key is set."""
    if not settings.FERNET_KEY or not plaintext:
        return plaintext
    try:
        from cryptography.fernet import Fernet
        f = Fernet(settings.FERNET_KEY.encode())
        return f.encrypt(plaintext.encode()).decode()
    except Exception:
        return plaintext

def decrypt_pii(ciphertext: str) -> str:
    """Decrypt sensitive PII using Fernet."""
    if not settings.FERNET_KEY or not ciphertext:
        return ciphertext
    try:
        from cryptography.fernet import Fernet
        f = Fernet(settings.FERNET_KEY.encode())
        return f.decrypt(ciphertext.encode()).decode()
    except Exception:
        return ciphertext
