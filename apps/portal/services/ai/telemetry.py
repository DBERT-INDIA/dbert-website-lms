import logging

logger = logging.getLogger("gemini_telemetry")

def track_generation(model: str, latency_ms: float, input_tokens: int, output_tokens: int, status: str):
    """Placeholder for telemetry tracking (e.g., Prometheus, Datadog)."""
    logger.info(f"GEMINI_TELEMETRY | model={model} | latency={latency_ms}ms | tokens={input_tokens}+{output_tokens} | status={status}")
