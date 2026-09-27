class GeminiProviderError(Exception):
    """Base exception for Gemini provider errors."""
    pass

class GeminiRateLimitError(GeminiProviderError):
    """Raised when 429 Too Many Requests is encountered across all fallbacks."""
    pass

class GeminiAuthError(GeminiProviderError):
    """Raised for 401 or 403 API key issues."""
    pass

class GeminiModelRetiredError(GeminiProviderError):
    """Raised for 404 Model Not Found errors."""
    pass

class GeminiTimeoutError(GeminiProviderError):
    """Raised when the API times out."""
    pass
