import time
from typing import Dict, Any
from collections import defaultdict

_telemetry = {
    "total_requests": 0,
    "error_count": 0,
    "start_time": time.time(),
    "endpoints": defaultdict(lambda: {"count": 0, "total_duration_ms": 0.0})
}

def record_metric(method: str, path: str, status_code: int, duration_ms: float):
    _telemetry["total_requests"] += 1
    if status_code >= 400:
        _telemetry["error_count"] += 1
    ep = f"{method} {path}"
    _telemetry["endpoints"][ep]["count"] += 1
    _telemetry["endpoints"][ep]["total_duration_ms"] += duration_ms

def get_telemetry_snapshot() -> Dict[str, Any]:
    uptime = time.time() - _telemetry["start_time"]
    top_endpoints = []
    for ep, data in sorted(_telemetry["endpoints"].items(), key=lambda x: x[1]["count"], reverse=True)[:10]:
        avg_lat = (data["total_duration_ms"] / data["count"]) if data["count"] else 0.0
        top_endpoints.append({
            "endpoint": ep,
            "requests": data["count"],
            "avg_latency_ms": round(avg_lat, 2)
        })

    return {
        "uptime_seconds": int(uptime),
        "total_requests": _telemetry["total_requests"],
        "error_count": _telemetry["error_count"],
        "error_rate_pct": round((_telemetry["error_count"] / _telemetry["total_requests"] * 100.0) if _telemetry["total_requests"] else 0.0, 2),
        "top_endpoints": top_endpoints
    }
