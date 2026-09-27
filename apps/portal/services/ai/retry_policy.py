import time
import logging

logger = logging.getLogger("gemini_retry")

def execute_with_retry(func, max_attempts: int = 3, base_delay: float = 1.0):
    """Executes a function with exponential backoff for 429 and 5xx errors."""
    from .exceptions import GeminiRateLimitError, GeminiAuthError, GeminiModelRetiredError
    
    for attempt in range(max_attempts):
        try:
            return func()
        except (GeminiRateLimitError, Exception) as e:
            if isinstance(e, GeminiAuthError) or isinstance(e, GeminiModelRetiredError):
                raise  # Do not retry fatal errors
                
            if attempt == max_attempts - 1:
                logger.error(f"Failed after {max_attempts} attempts. Last error: {e}")
                raise
                
            sleep_time = base_delay * (2 ** attempt)
            logger.warning(f"Attempt {attempt + 1} failed ({e}). Retrying in {sleep_time}s...")
            time.sleep(sleep_time)
