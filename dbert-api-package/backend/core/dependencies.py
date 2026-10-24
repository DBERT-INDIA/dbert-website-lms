from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
import jwt
from backend.core.config import settings
from backend.core.security import decode_token

security_scheme = HTTPBearer(auto_error=False)

async def get_current_user_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)
) -> Dict[str, Any]:
    """Extract and validate bearer JWT token from Authorization header."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    try:
        payload = decode_token(token)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, Exception) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(*allowed_roles: str):
    """Factory dependency to enforce role-based access control."""
    async def role_checker(token: Dict[str, Any] = Depends(get_current_user_token)) -> Dict[str, Any]:
        user_role = token.get("role", "")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: role '{user_role}' is not authorized for this resource"
            )
        return token
    return role_checker

# Concrete role dependencies
require_intern = require_role("intern")
require_company = require_role("company")
require_admin = require_role("admin")
require_mentor = require_role("mentor")
require_staff = require_role("staff")
require_privileged = require_role("admin", "staff")

async def verify_cron_secret(x_cron_secret: Optional[str] = Header(None, alias="X-Cron-Secret")) -> bool:
    """Authorize background cron trigger requests via header secret."""
    if not x_cron_secret or x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing X-Cron-Secret header"
        )
    return True
