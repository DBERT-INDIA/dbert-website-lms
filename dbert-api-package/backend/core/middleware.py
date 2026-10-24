import time
import uuid
import logging
import json
from collections import defaultdict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.core.config import settings

logger = logging.getLogger("dbert_api")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s] %(message)s'))
if not logger.handlers:
    logger.addHandler(handler)

# In-memory sliding-window rate limiter for fast worker-level checking
_rate_buckets = defaultdict(list)

def check_rate_limit(key: str, limit: int, window_seconds: int) -> bool:
    """Sliding-window rate limiter. Returns True if allowed, False if exceeded."""
    if settings.DISABLE_RATE_LIMIT:
        return True
    now = time.time()
    cutoff = now - window_seconds
    timestamps = [t for t in _rate_buckets[key] if t > cutoff]
    if len(timestamps) >= limit:
        _rate_buckets[key] = timestamps
        return False
    timestamps.append(now)
    _rate_buckets[key] = timestamps
    return True

class RequestContextMiddleware(BaseHTTPMiddleware):
    """Middleware for injecting Request ID, measuring latency, and logging."""
    async def dispatch(self, request: Request, call_next):
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.perf_counter()
        
        # Attach request ID to request state
        request.state.request_id = req_id
        
        response = await call_next(request)
        
        duration_ms = (time.perf_counter() - start_time) * 1000.0
        response.headers["X-Request-ID"] = req_id
        response.headers["X-Request-Duration-Ms"] = f"{duration_ms:.2f}"
        
        # Log non-health requests
        if request.url.path not in ("/health", "/ready"):
            client_ip = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For") or (request.client.host if request.client else "unknown")
            logger.info(f"{request.method} {request.url.path} {response.status_code} {duration_ms:.2f}ms - IP:{client_ip} [ReqID:{req_id}]")
            
        return response
